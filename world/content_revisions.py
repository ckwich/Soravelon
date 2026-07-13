"""Read-only revision authority over immutable world-content manifests."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from django.db import transaction
from django.utils import timezone

from world.content_compiler import (
    CompilationDiagnostic,
    ManifestIntegrityError,
    WorldChangePlan,
    compile_world_manifest,
    compile_world_sources,
    deserialize_world_manifest,
    plan_world_changes,
    serialize_world_manifest,
)


class BootstrapAdoptionError(RuntimeError):
    """Raised when existing runtime cannot safely become revision authority."""


class ApplyPreconditionError(RuntimeError):
    """Raised when a content apply is unsafe in current runtime state."""


class ContentApplyError(RuntimeError):
    """Raised after a failed apply has rolled back and recorded evidence."""


class WorldContentStartupError(RuntimeError):
    """Raised when startup cannot prove applied content authority."""


@dataclass(frozen=True)
class OccupiedDestructiveRoom:
    zone_id: str
    room_id: str
    character_ids: tuple[int, ...]


@dataclass(frozen=True)
class ContentApplyResult:
    state: str
    revision: object


@dataclass(frozen=True)
class AppliedContentStartupResult:
    revision_id: int
    manifest_hash: str


@dataclass(frozen=True)
class WorldContentStatus:
    state: str
    target_manifest_hash: str | None
    applied_manifest_hash: str | None
    plan: WorldChangePlan | None
    diagnostics: tuple[CompilationDiagnostic, ...] = ()
    error: str = ""


def get_world_content_status(areas_dir: Path) -> WorldContentStatus:
    """Compile and compare current source to durable applied evidence, read-only."""

    from world.models import WorldContentRevision

    target_result = compile_world_manifest(areas_dir)
    if target_result.manifest is None:
        return WorldContentStatus(
            state="invalid-source",
            target_manifest_hash=None,
            applied_manifest_hash=None,
            plan=None,
            diagnostics=target_result.diagnostics,
            error="Current world content failed validation.",
        )
    target = target_result.manifest
    applied_revision = (
        WorldContentRevision.objects.filter(status="applied")
        .order_by("-created_at")
        .first()
    )
    if applied_revision is None:
        empty = compile_world_sources({}).manifest
        assert empty is not None
        planning = plan_world_changes(empty, target)
        return WorldContentStatus(
            state="uninitialized",
            target_manifest_hash=target.manifest_hash,
            applied_manifest_hash=None,
            plan=planning.plan,
            diagnostics=planning.diagnostics,
        )
    try:
        applied = deserialize_world_manifest(applied_revision.manifest)
    except ManifestIntegrityError as exc:
        return WorldContentStatus(
            state="invalid-applied-manifest",
            target_manifest_hash=target.manifest_hash,
            applied_manifest_hash=applied_revision.manifest_hash,
            plan=None,
            error=str(exc),
        )
    if applied.manifest_hash != applied_revision.manifest_hash:
        return WorldContentStatus(
            state="invalid-applied-manifest",
            target_manifest_hash=target.manifest_hash,
            applied_manifest_hash=applied_revision.manifest_hash,
            plan=None,
            error="Applied revision integrity hash disagrees with its manifest payload.",
        )
    planning = plan_world_changes(applied, target)
    if planning.plan is None:
        return WorldContentStatus(
            state="invalid-change-plan",
            target_manifest_hash=target.manifest_hash,
            applied_manifest_hash=applied.manifest_hash,
            plan=None,
            diagnostics=planning.diagnostics,
            error="Current source cannot produce a safe semantic change plan.",
        )
    state = "current" if not planning.plan.changes else "drifted"
    return WorldContentStatus(
        state=state,
        target_manifest_hash=target.manifest_hash,
        applied_manifest_hash=applied.manifest_hash,
        plan=planning.plan,
    )


def serialize_change_plan(plan: WorldChangePlan) -> dict[str, object]:
    """Return stable JSON-safe read-only plan evidence."""

    return {
        "previous_manifest_hash": plan.previous_manifest_hash,
        "target_manifest_hash": plan.target_manifest_hash,
        "changes": [
            {
                "action": change.action,
                "zone_id": change.zone_id,
                "entity_type": change.entity_type,
                "entity_id": change.entity_id,
                "destructive": change.destructive,
                "player_impact": list(change.player_impact),
                "source_path": (
                    change.after.source_path
                    if change.after is not None
                    else change.before.source_path
                ),
                "line": (
                    change.after.line
                    if change.after is not None
                    else change.before.line
                ),
            }
            for change in plan.changes
        ],
    }


@transaction.atomic
def adopt_bootstrap(manifest, *, git_commit: str):
    """Record an exact existing runtime as the initial applied revision.

    This operation deliberately performs no world-content mutation. The runtime
    verifier is repeated inside the transaction so adoption cannot rely on a
    stale preflight result.
    """

    from world.content_runtime import verify_runtime_manifest
    from world.models import WorldContentRevision

    if re.fullmatch(r"[0-9a-f]{7,64}", git_commit or "") is None:
        raise BootstrapAdoptionError(
            "Git commit must be a 7-64 character lowercase hexadecimal Git object ID."
        )
    if WorldContentRevision.objects.exists():
        raise BootstrapAdoptionError("World content authority is already initialized.")

    verification = verify_runtime_manifest(manifest)
    if verification.verified_manifest_hash != manifest.manifest_hash:
        raise BootstrapAdoptionError(
            "Bootstrap adoption refused because runtime drift was detected."
        )

    empty = compile_world_sources({}).manifest
    assert empty is not None
    planning = plan_world_changes(empty, manifest)
    if planning.plan is None:
        raise BootstrapAdoptionError(
            "Bootstrap adoption could not produce a valid initial change plan."
        )
    plan = serialize_change_plan(planning.plan)
    plan.update({"kind": "bootstrap-adoption", "runtime_verified": True})
    now = timezone.now()
    return WorldContentRevision.objects.create(
        manifest_hash=manifest.manifest_hash,
        schema_version=manifest.schema_version,
        manifest=serialize_world_manifest(manifest),
        plan=plan,
        status="applied",
        git_commit=git_commit,
        applied_at=now,
        finished_at=now,
    )


def initialize_world_content(
    target_manifest,
    *,
    git_commit: str,
    after_materialize=None,
) -> ContentApplyResult:
    """Explicitly materialize the first revision into a content-empty database."""

    from world.content_compiler import serialize_world_manifest
    from world.content_materializer import materialize_world_manifest
    from world.content_runtime import (
        hydrate_runtime_registries,
        verify_runtime_manifest,
    )
    from world.models import WorldContentDeploymentLock, WorldContentRevision

    _validate_git_object_id(git_commit)
    failure_message = None
    failed_revision = None
    result = None
    with transaction.atomic():
        WorldContentDeploymentLock.objects.select_for_update().get(pk=1)
        if WorldContentRevision.objects.exclude(status="failed").exists():
            raise ApplyPreconditionError(
                "World content authority is already initialized."
            )
        _ensure_evennia_runtime_initialized()
        empty = compile_world_sources({}).manifest
        assert empty is not None
        hydrate_runtime_registries(empty)
        if verify_runtime_manifest(empty).verified_manifest_hash is None:
            raise ApplyPreconditionError(
                "Database contains authored runtime content; use bootstrap-adopt instead."
            )
        planning = plan_world_changes(empty, target_manifest)
        if planning.plan is None:
            raise ApplyPreconditionError(
                "Initial manifest cannot produce a safe semantic change plan."
            )
        plan_payload = serialize_change_plan(planning.plan)
        plan_payload["kind"] = "initialize"
        revision = WorldContentRevision.objects.create(
            manifest_hash=target_manifest.manifest_hash,
            schema_version=target_manifest.schema_version,
            manifest=serialize_world_manifest(target_manifest),
            plan=plan_payload,
            status="applying",
            git_commit=git_commit,
        )
        try:
            with transaction.atomic():
                materialize_world_manifest(
                    target_manifest,
                    previous_manifest=empty,
                )
                if after_materialize is not None:
                    after_materialize()
                verification = verify_runtime_manifest(target_manifest)
                if verification.verified_manifest_hash is None:
                    raise RuntimeError(
                        "Initialized runtime did not exactly match target manifest."
                    )
        except Exception as exc:
            failure_message = str(exc) or type(exc).__name__
            hydrate_runtime_registries(empty)
            revision.status = "failed"
            revision.error = failure_message
            revision.finished_at = timezone.now()
            revision.save(update_fields=("status", "error", "finished_at"))
            failed_revision = revision
        else:
            now = timezone.now()
            revision.status = "applied"
            revision.applied_at = now
            revision.finished_at = now
            revision.save(update_fields=("status", "applied_at", "finished_at"))
            result = ContentApplyResult(state="initialized", revision=revision)

    if failure_message is not None:
        error = ContentApplyError(failure_message)
        error.revision_id = failed_revision.pk
        raise error
    assert result is not None
    return result


def _ensure_evennia_runtime_initialized() -> None:
    """Complete Evennia's one-time object foundation for explicit initialization."""

    from evennia.accounts.models import AccountDB
    from evennia.objects.models import ObjectDB
    from evennia.server import initial_setup
    from evennia.server.models import ServerConfig

    if not AccountDB.objects.filter(id=1, is_superuser=True).exists():
        raise ApplyPreconditionError(
            "Admin account #1 must exist before world-content initialization."
        )
    if not ObjectDB.objects.filter(id=2).exists():
        initial_setup.create_objects()
        initial_setup.at_initial_setup()
    if not ObjectDB.objects.filter(id=2).exists():
        raise ApplyPreconditionError(
            "Evennia initial setup did not create DEFAULT_HOME object #2."
        )
    ServerConfig.objects.conf("last_initial_setup_step", "done")


def find_occupied_destructive_rooms(
    plan: WorldChangePlan,
) -> tuple[OccupiedDestructiveRoom, ...]:
    """Return exact occupied rooms that a semantic plan will delete."""

    from typeclasses.characters import Character
    from world.tag_search import search_objects_by_exact_tag

    occupied: list[OccupiedDestructiveRoom] = []
    deleted_rooms = {
        (change.zone_id, change.entity_id)
        for change in plan.changes
        if change.action == "delete" and change.entity_type == "room"
    }
    for zone_id, room_id in sorted(deleted_rooms):
        room = next(
            (
                candidate
                for candidate in search_objects_by_exact_tag(room_id, "room_id")
                if (candidate.db.zone_id or "") == zone_id
            ),
            None,
        )
        if room is None:
            continue
        character_ids = tuple(
            sorted(
                content.id
                for content in room.contents
                if isinstance(content, Character) and content.id is not None
            )
        )
        if character_ids:
            occupied.append(
                OccupiedDestructiveRoom(
                    zone_id=zone_id,
                    room_id=room_id,
                    character_ids=character_ids,
                )
            )
    return tuple(occupied)


def ensure_apply_occupancy_allowed(
    plan: WorldChangePlan, *, maintenance_approved: bool
) -> tuple[OccupiedDestructiveRoom, ...]:
    """Refuse occupied room deletion unless maintenance approval is explicit."""

    occupied = find_occupied_destructive_rooms(plan)
    if occupied and not maintenance_approved:
        room_list = ", ".join(f"{item.zone_id}:{item.room_id}" for item in occupied)
        raise ApplyPreconditionError(
            "Destructive content apply requires explicit maintenance approval "
            f"because player characters occupy: {room_list}."
        )
    return occupied


def _validate_git_object_id(git_commit: str) -> None:
    if re.fullmatch(r"[0-9a-f]{7,64}", git_commit or "") is None:
        raise ApplyPreconditionError(
            "Git commit must be a 7-64 character lowercase hexadecimal Git object ID."
        )


def apply_world_content(
    target_manifest,
    *,
    git_commit: str,
    maintenance_approved: bool = False,
    after_materialize=None,
    operation_kind: str = "apply",
    rollback_target_revision_id: int | None = None,
) -> ContentApplyResult:
    """Apply one manifest under the durable deployment mutex and DB transaction."""

    from world.content_compiler import (
        deserialize_world_manifest,
        plan_world_changes,
        serialize_world_manifest,
    )
    from world.content_materializer import materialize_world_manifest
    from world.content_runtime import verify_runtime_manifest
    from world.models import WorldContentDeploymentLock, WorldContentRevision

    _validate_git_object_id(git_commit)
    failure_message = None
    failed_revision = None
    result = None
    with transaction.atomic():
        WorldContentDeploymentLock.objects.select_for_update().get(pk=1)
        applied_revision = (
            WorldContentRevision.objects.select_for_update()
            .filter(status="applied")
            .order_by("-applied_at", "-created_at")
            .first()
        )
        if applied_revision is None:
            raise ApplyPreconditionError(
                "World content has no applied baseline; run bootstrap-adopt first."
            )
        try:
            previous_manifest = deserialize_world_manifest(applied_revision.manifest)
        except ManifestIntegrityError as exc:
            raise ApplyPreconditionError(str(exc)) from exc
        if previous_manifest.manifest_hash != applied_revision.manifest_hash:
            raise ApplyPreconditionError(
                "Applied revision hash disagrees with its manifest payload."
            )
        baseline = verify_runtime_manifest(previous_manifest)
        if baseline.verified_manifest_hash is None:
            raise ApplyPreconditionError(
                "Current runtime does not exactly match the applied baseline."
            )
        if target_manifest.manifest_hash == previous_manifest.manifest_hash:
            result = ContentApplyResult(state="no-op", revision=applied_revision)
        else:
            if operation_kind not in {"apply", "rollback"}:
                raise ApplyPreconditionError(
                    f"Unsupported content operation kind '{operation_kind}'."
                )
            if operation_kind == "rollback":
                target_evidence = WorldContentRevision.objects.filter(
                    pk=rollback_target_revision_id,
                    manifest_hash=target_manifest.manifest_hash,
                ).first()
                if target_evidence is None:
                    raise ApplyPreconditionError(
                        "Rollback target evidence changed or no longer exists."
                    )
            planning = plan_world_changes(previous_manifest, target_manifest)
            if planning.plan is None:
                raise ApplyPreconditionError(
                    "Target manifest cannot produce a safe semantic change plan."
                )
            ensure_apply_occupancy_allowed(
                planning.plan,
                maintenance_approved=maintenance_approved,
            )
            plan_payload = serialize_change_plan(planning.plan)
            plan_payload["kind"] = operation_kind
            if operation_kind == "rollback":
                plan_payload["rollback_target_revision_id"] = (
                    rollback_target_revision_id
                )
            target_revision = WorldContentRevision.objects.create(
                manifest_hash=target_manifest.manifest_hash,
                schema_version=target_manifest.schema_version,
                manifest=serialize_world_manifest(target_manifest),
                plan=plan_payload,
                status="applying",
                previous_revision=applied_revision,
                git_commit=git_commit,
                maintenance_approved=maintenance_approved,
            )
            try:
                with transaction.atomic():
                    materialize_world_manifest(
                        target_manifest,
                        previous_manifest=previous_manifest,
                        maintenance_approved=maintenance_approved,
                    )
                    if after_materialize is not None:
                        after_materialize()
                    verification = verify_runtime_manifest(target_manifest)
                    if verification.verified_manifest_hash is None:
                        raise RuntimeError(
                            "Materialized runtime did not exactly match target manifest."
                        )
            except Exception as exc:
                failure_message = str(exc) or type(exc).__name__
                # The savepoint restored database state; replaying the prior
                # manifest repairs process-local registries and cached topology.
                materialize_world_manifest(
                    previous_manifest,
                    previous_manifest=previous_manifest,
                    maintenance_approved=True,
                )
                restored = verify_runtime_manifest(previous_manifest)
                if restored.verified_manifest_hash is None:
                    failure_message += "; baseline registry restoration failed"
                target_revision.status = "failed"
                target_revision.error = failure_message
                target_revision.finished_at = timezone.now()
                target_revision.save(update_fields=("status", "error", "finished_at"))
                failed_revision = target_revision
            else:
                now = timezone.now()
                applied_revision.status = (
                    "rolled_back" if operation_kind == "rollback" else "superseded"
                )
                applied_revision.finished_at = now
                applied_revision.save(update_fields=("status", "finished_at"))
                target_revision.status = "applied"
                target_revision.applied_at = now
                target_revision.finished_at = now
                target_revision.save(
                    update_fields=("status", "applied_at", "finished_at")
                )
                result = ContentApplyResult(
                    state=(
                        "rolled-back" if operation_kind == "rollback" else "applied"
                    ),
                    revision=target_revision,
                )

    if failure_message is not None:
        error = ContentApplyError(failure_message)
        error.revision_id = failed_revision.pk
        raise error
    assert result is not None
    return result


def rollback_world_content(
    target_revision_id: int,
    *,
    git_commit: str,
    maintenance_approved: bool = False,
) -> ContentApplyResult:
    """Apply a historical manifest as a new, durable rollback attempt."""

    from world.models import WorldContentRevision

    try:
        target_revision = WorldContentRevision.objects.get(pk=target_revision_id)
    except WorldContentRevision.DoesNotExist as exc:
        raise ApplyPreconditionError(
            f"Rollback target revision {target_revision_id} does not exist."
        ) from exc
    try:
        target_manifest = deserialize_world_manifest(target_revision.manifest)
    except ManifestIntegrityError as exc:
        raise ApplyPreconditionError(str(exc)) from exc
    if target_manifest.manifest_hash != target_revision.manifest_hash:
        raise ApplyPreconditionError(
            "Rollback target hash disagrees with its manifest payload."
        )
    return apply_world_content(
        target_manifest,
        git_commit=git_commit,
        maintenance_approved=maintenance_approved,
        operation_kind="rollback",
        rollback_target_revision_id=target_revision.id,
    )


def load_applied_world_content(areas_dir: Path) -> AppliedContentStartupResult:
    """Verify applied source/runtime truth and hydrate only in-memory registries."""

    from world.content_runtime import (
        hydrate_runtime_registries,
        verify_runtime_manifest,
    )
    from world.models import WorldContentRevision

    applied = (
        WorldContentRevision.objects.filter(status="applied")
        .order_by("-applied_at", "-created_at")
        .first()
    )
    if applied is None:
        raise WorldContentStartupError(
            "No applied world-content revision exists; explicit initialization is required."
        )
    try:
        manifest = deserialize_world_manifest(applied.manifest)
    except ManifestIntegrityError as exc:
        raise WorldContentStartupError(str(exc)) from exc
    if manifest.manifest_hash != applied.manifest_hash:
        raise WorldContentStartupError(
            "Applied revision hash disagrees with its manifest payload."
        )
    source = compile_world_manifest(areas_dir)
    if source.manifest is None:
        raise WorldContentStartupError("Current authored source is invalid.")
    if source.manifest.manifest_hash != manifest.manifest_hash:
        raise WorldContentStartupError(
            "Current authored source does not match the applied revision."
        )
    try:
        hydrate_runtime_registries(manifest)
    except RuntimeError as exc:
        raise WorldContentStartupError(str(exc)) from exc
    verification = verify_runtime_manifest(manifest)
    if verification.verified_manifest_hash is None:
        raise WorldContentStartupError(
            "Current runtime does not exactly match the applied revision."
        )
    return AppliedContentStartupResult(
        revision_id=applied.id,
        manifest_hash=manifest.manifest_hash,
    )
