import io
import json
from pathlib import Path

from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase

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
