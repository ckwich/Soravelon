import io
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, transaction
from django.test import TestCase
from evennia.utils.test_resources import EvenniaTest

AREAS_DIR = Path(__file__).resolve().parents[1] / "world" / "areas"


class TestWorldContentRevisionStatus(TestCase):
    def test_database_permits_only_one_applied_revision(self):
        from world.models import WorldContentRevision

        common = {
            "schema_version": "soravelon.world-content.v1",
            "manifest": {},
            "git_commit": "test",
            "status": "applied",
        }
        WorldContentRevision.objects.create(manifest_hash="a" * 64, **common)

        with self.assertRaises(IntegrityError), transaction.atomic():
            WorldContentRevision.objects.create(manifest_hash="b" * 64, **common)

    def test_uninitialized_status_plans_creates_without_writing(self):
        from world.content_revisions import get_world_content_status
        from world.models import WorldContentRevision

        status = get_world_content_status(AREAS_DIR)

        self.assertEqual(status.state, "uninitialized")
        self.assertIsNone(status.applied_manifest_hash)
        self.assertRegex(status.target_manifest_hash, r"^[0-9a-f]{64}$")
        self.assertIsNotNone(status.plan)
        self.assertTrue(status.plan.changes)
        self.assertTrue(
            all(change.action == "create" for change in status.plan.changes)
        )
        self.assertEqual(WorldContentRevision.objects.count(), 0)

    def test_applied_manifest_reports_current_without_writing(self):
        from world.content_compiler import (
            compile_world_manifest,
            serialize_world_manifest,
        )
        from world.content_revisions import get_world_content_status
        from world.models import WorldContentRevision

        manifest = compile_world_manifest(AREAS_DIR).manifest
        assert manifest is not None
        WorldContentRevision.objects.create(
            manifest_hash=manifest.manifest_hash,
            schema_version=manifest.schema_version,
            manifest=serialize_world_manifest(manifest),
            status="applied",
            git_commit="test-current",
        )

        status = get_world_content_status(AREAS_DIR)

        self.assertEqual(status.state, "current")
        self.assertEqual(status.applied_manifest_hash, manifest.manifest_hash)
        self.assertEqual(status.plan.changes, ())
        self.assertEqual(WorldContentRevision.objects.count(), 1)

    def test_drifted_status_plans_against_durable_applied_manifest(self):
        from world.content_compiler import (
            compile_world_sources,
            serialize_world_manifest,
        )
        from world.content_revisions import get_world_content_status
        from world.models import WorldContentRevision

        old_source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("old")
    area.zone(name="Old", zone_type="frontier", continent="varath")
    return area.build()
"""
        old = compile_world_sources({"world/areas/old.py": old_source}).manifest
        assert old is not None
        WorldContentRevision.objects.create(
            manifest_hash=old.manifest_hash,
            schema_version=old.schema_version,
            manifest=serialize_world_manifest(old),
            status="applied",
            git_commit="test-old",
        )

        status = get_world_content_status(AREAS_DIR)

        self.assertEqual(status.state, "drifted")
        self.assertEqual(status.applied_manifest_hash, old.manifest_hash)
        self.assertTrue(status.plan.changes)
        self.assertEqual(WorldContentRevision.objects.count(), 1)

    def test_corrupt_applied_manifest_fails_status_closed(self):
        from world.content_revisions import get_world_content_status
        from world.models import WorldContentRevision

        WorldContentRevision.objects.create(
            manifest_hash="0" * 64,
            schema_version="soravelon.world-content.v1",
            manifest={
                "schema_version": "soravelon.world-content.v1",
                "manifest_hash": "0" * 64,
                "zones": [],
            },
            status="applied",
            git_commit="test-corrupt",
        )

        status = get_world_content_status(AREAS_DIR)

        self.assertEqual(status.state, "invalid-applied-manifest")
        self.assertIsNone(status.plan)
        self.assertIn("integrity", status.error.lower())


class TestWorldContentReadOnlyCommand(TestCase):
    def test_validate_plan_and_status_are_json_and_read_only(self):
        from world.models import WorldContentRevision

        for action in ("validate", "plan", "status"):
            output = io.StringIO()
            call_command("worldcontent", action, "--format", "json", stdout=output)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["command"], action)
            self.assertEqual(payload["valid"], True)

        self.assertEqual(WorldContentRevision.objects.count(), 0)


class TestRuntimeManifestBootstrapVerification(EvenniaTest):
    def _build_runtime_and_manifest(self):
        from world.area_builder import AreaBuilder
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("bootstrap")
    area.zone(name="Bootstrap", zone_type="frontier", continent="varath")
    entry = area.room("entry", name="Entry", desc="A threshold.")
    square = area.room("square", name="Square", desc="An open square.")
    area.exit(entry, square, "north")
    area.exit(square, entry, "south")
    area.npc(entry, "npc_keeper", name="Keeper", faction="wardens")
    area.item("welcome_note", key="Welcome Note", item_type="item")
    area.quest("welcome", quest_giver="npc_keeper", objectives=[
        {"type": "investigate", "target": "square", "count": 1},
    ])
    return area.build()
"""
        area = AreaBuilder("bootstrap")
        area.zone(name="Bootstrap", zone_type="frontier", continent="varath")
        entry = area.room("entry", name="Entry", desc="A threshold.")
        square = area.room("square", name="Square", desc="An open square.")
        area.exit(entry, square, "north")
        area.exit(square, entry, "south")
        area.npc(entry, "npc_keeper", name="Keeper", faction="wardens")
        area.item("welcome_note", key="Welcome Note", item_type="item")
        area.quest(
            "welcome",
            quest_giver="npc_keeper",
            objectives=[{"type": "investigate", "target": "square", "count": 1}],
        )
        area.build()
        manifest = compile_world_sources({"world/areas/bootstrap.py": source}).manifest
        assert manifest is not None
        return manifest, entry

    def test_exact_runtime_can_be_verified_without_writing(self):
        from world.content_runtime import verify_runtime_manifest
        from world.models import WorldContentRevision

        manifest, _entry = self._build_runtime_and_manifest()
        result = verify_runtime_manifest(manifest)

        self.assertEqual(result.diagnostics, ())
        self.assertEqual(result.verified_manifest_hash, manifest.manifest_hash)
        self.assertEqual(WorldContentRevision.objects.count(), 0)

        output = io.StringIO()
        with patch(
            "world.management.commands.worldcontent.compile_world_manifest",
            return_value=SimpleNamespace(manifest=manifest, diagnostics=()),
        ):
            call_command(
                "worldcontent",
                "bootstrap-check",
                "--format",
                "json",
                stdout=output,
            )
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["state"], "bootstrap-ready")
        self.assertEqual(WorldContentRevision.objects.count(), 0)

    def test_runtime_drift_refuses_bootstrap_adoption(self):
        from world.content_revisions import BootstrapAdoptionError, adopt_bootstrap
        from world.content_runtime import verify_runtime_manifest
        from world.models import WorldContentRevision

        manifest, entry = self._build_runtime_and_manifest()
        entry.db.desc = "Runtime drift."

        result = verify_runtime_manifest(manifest)

        self.assertIsNone(result.verified_manifest_hash)
        self.assertTrue(result.diagnostics)
        self.assertEqual(result.diagnostics[0].code, "runtime-value-mismatch")
        self.assertIn("entry.desc", result.diagnostics[0].entity_id)

        with self.assertRaisesRegex(BootstrapAdoptionError, "runtime drift"):
            adopt_bootstrap(manifest, git_commit="a" * 40)
        self.assertEqual(WorldContentRevision.objects.count(), 0)

    def test_bootstrap_adoption_records_verified_runtime_without_mutating_it(self):
        from world.content_revisions import adopt_bootstrap
        from world.models import WorldContentRevision

        manifest, entry = self._build_runtime_and_manifest()
        original_desc = entry.db.desc

        revision = adopt_bootstrap(manifest, git_commit="a" * 40)

        revision.refresh_from_db()
        entry.refresh_from_db()
        self.assertEqual(revision.status, "applied")
        self.assertEqual(revision.manifest_hash, manifest.manifest_hash)
        self.assertEqual(revision.git_commit, "a" * 40)
        self.assertEqual(revision.plan["kind"], "bootstrap-adoption")
        self.assertEqual(revision.plan["runtime_verified"], True)
        self.assertTrue(revision.plan["changes"])
        self.assertTrue(
            all(change["action"] == "create" for change in revision.plan["changes"])
        )
        self.assertIsNotNone(revision.applied_at)
        self.assertIsNotNone(revision.finished_at)
        self.assertEqual(entry.db.desc, original_desc)

    def test_bootstrap_adoption_refuses_existing_authority(self):
        from world.content_revisions import BootstrapAdoptionError, adopt_bootstrap

        manifest, _entry = self._build_runtime_and_manifest()
        adopt_bootstrap(manifest, git_commit="a" * 40)

        with self.assertRaisesRegex(BootstrapAdoptionError, "already initialized"):
            adopt_bootstrap(manifest, git_commit="b" * 40)

    def test_bootstrap_adoption_requires_git_object_id(self):
        from world.content_revisions import BootstrapAdoptionError, adopt_bootstrap
        from world.models import WorldContentRevision

        manifest, _entry = self._build_runtime_and_manifest()

        with self.assertRaisesRegex(BootstrapAdoptionError, "Git object ID"):
            adopt_bootstrap(manifest, git_commit="not-a-commit")
        self.assertEqual(WorldContentRevision.objects.count(), 0)

    def test_bootstrap_adopt_command_requires_commit_and_records_revision(self):
        from world.models import WorldContentRevision

        manifest, _entry = self._build_runtime_and_manifest()
        with patch(
            "world.management.commands.worldcontent.compile_world_manifest",
            return_value=SimpleNamespace(manifest=manifest, diagnostics=()),
        ):
            with self.assertRaises(CommandError):
                call_command("worldcontent", "bootstrap-adopt")

            output = io.StringIO()
            call_command(
                "worldcontent",
                "bootstrap-adopt",
                "--git-commit",
                "a" * 40,
                "--format",
                "json",
                stdout=output,
            )

        payload = json.loads(output.getvalue())
        self.assertEqual(payload["state"], "bootstrap-adopted")
        self.assertEqual(payload["git_commit"], "a" * 40)
        self.assertEqual(WorldContentRevision.objects.count(), 1)


class TestWorldContentApplyOccupancy(EvenniaTest):
    def _room_deletion_plan(self):
        from world.area_builder import AreaBuilder
        from world.content_compiler import compile_world_sources, plan_world_changes

        old_source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("occupied")
    area.zone(name="Occupied", zone_type="frontier", continent="varath")
    safe = area.room("safe", name="Safe", desc="Safe.")
    doomed = area.room("doomed", name="Doomed", desc="Doomed.")
    return area.build()
"""
        new_source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("occupied")
    area.zone(name="Occupied", zone_type="frontier", continent="varath")
    safe = area.room("safe", name="Safe", desc="Safe.")
    return area.build()
"""
        area = AreaBuilder("occupied")
        area.zone(name="Occupied", zone_type="frontier", continent="varath")
        area.room("safe", name="Safe", desc="Safe.")
        doomed = area.room("doomed", name="Doomed", desc="Doomed.")
        area.build()
        old = compile_world_sources({"world/areas/occupied.py": old_source}).manifest
        new = compile_world_sources({"world/areas/occupied.py": new_source}).manifest
        assert old is not None and new is not None
        planning = plan_world_changes(old, new)
        assert planning.plan is not None
        return planning.plan, doomed

    def test_occupied_destructive_room_requires_maintenance_approval(self):
        from evennia import create_object
        from typeclasses.characters import Character
        from world.content_revisions import (
            ApplyPreconditionError,
            ensure_apply_occupancy_allowed,
            find_occupied_destructive_rooms,
        )

        plan, doomed = self._room_deletion_plan()
        character = create_object(Character, key="occupant", location=doomed)

        occupied = find_occupied_destructive_rooms(plan)

        self.assertEqual(len(occupied), 1)
        self.assertEqual(occupied[0].zone_id, "occupied")
        self.assertEqual(occupied[0].room_id, "doomed")
        self.assertEqual(occupied[0].character_ids, (character.id,))
        with self.assertRaisesRegex(ApplyPreconditionError, "maintenance approval"):
            ensure_apply_occupancy_allowed(plan, maintenance_approved=False)
        self.assertEqual(
            ensure_apply_occupancy_allowed(plan, maintenance_approved=True), occupied
        )

    def test_unoccupied_destructive_room_does_not_require_maintenance_approval(self):
        from world.content_revisions import ensure_apply_occupancy_allowed

        plan, _doomed = self._room_deletion_plan()

        self.assertEqual(
            ensure_apply_occupancy_allowed(plan, maintenance_approved=False), ()
        )


class TestWorldContentManifestMaterializer(EvenniaTest):
    def test_manifest_replay_updates_and_reconciles_without_importing_source(self):
        from world.area_builder import AreaBuilder
        from world.content_compiler import compile_world_sources
        from world.content_materializer import materialize_world_manifest
        from world.content_runtime import verify_runtime_manifest

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("replay")
    area.zone(name="Replay", zone_type="frontier", continent="varath")
    entry = area.room("entry", name="Entry", desc="Updated threshold.")
    area.npc(entry, "keeper", name="Keeper", faction="wardens")
    return area.build()
"""
        area = AreaBuilder("replay")
        area.zone(name="Replay", zone_type="frontier", continent="varath")
        entry = area.room("entry", name="Entry", desc="Old threshold.")
        area.room("removed", name="Removed", desc="Removed room.")
        area.npc(entry, "keeper", name="Keeper", faction="wardens")
        area.build()
        manifest = compile_world_sources({"world/areas/replay.py": source}).manifest
        assert manifest is not None

        report = materialize_world_manifest(manifest)
        verification = verify_runtime_manifest(manifest)

        entry.refresh_from_db()
        self.assertEqual(entry.db.desc, "Updated threshold.")
        self.assertEqual(report["zones"], ("replay",))
        self.assertEqual(report["reconciled"]["rooms_deleted"], 1)
        self.assertEqual(verification.diagnostics, ())
        self.assertEqual(verification.verified_manifest_hash, manifest.manifest_hash)
