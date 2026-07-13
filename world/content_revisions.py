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


@dataclass(frozen=True)
class OccupiedDestructiveRoom:
    zone_id: str
    room_id: str
    character_ids: tuple[int, ...]


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
