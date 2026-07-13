"""Read-only revision authority over immutable world-content manifests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from world.content_compiler import (
    CompilationDiagnostic,
    ManifestIntegrityError,
    WorldChangePlan,
    compile_world_manifest,
    compile_world_sources,
    deserialize_world_manifest,
    plan_world_changes,
)


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
