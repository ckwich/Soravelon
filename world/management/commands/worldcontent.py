import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from world.content_compiler import compile_world_manifest
from world.content_revisions import (
    ApplyPreconditionError,
    BootstrapAdoptionError,
    ContentApplyError,
    adopt_bootstrap,
    apply_world_content,
    get_world_content_status,
    serialize_change_plan,
)
from world.content_runtime import verify_runtime_manifest


class Command(BaseCommand):
    help = "Validate, inspect, or explicitly adopt revisioned Soravelon world content."

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            choices=(
                "validate",
                "plan",
                "status",
                "bootstrap-check",
                "bootstrap-adopt",
                "apply",
            ),
        )
        parser.add_argument(
            "--format",
            choices=("human", "json"),
            default="human",
            dest="output_format",
        )
        parser.add_argument("--git-commit")
        parser.add_argument("--maintenance-approved", action="store_true")

    def handle(self, *args, **options):
        action = options["action"]
        output_format = options["output_format"]
        areas_dir = Path(settings.GAME_DIR) / "world" / "areas"

        if action in {"validate", "bootstrap-check", "bootstrap-adopt", "apply"}:
            result = compile_world_manifest(areas_dir)
            valid = result.manifest is not None
            payload = {
                "command": action,
                "valid": valid,
                "state": "valid" if valid else "invalid-source",
                "target_manifest_hash": (
                    result.manifest.manifest_hash if result.manifest else None
                ),
                "zone_count": len(result.manifest.zones) if result.manifest else 0,
                "diagnostics": [
                    {
                        "source_path": diagnostic.source_path,
                        "line": diagnostic.line,
                        "column": diagnostic.column,
                        "code": diagnostic.code,
                        "message": diagnostic.message,
                    }
                    for diagnostic in result.diagnostics
                ],
            }
            if (
                action in {"bootstrap-check", "bootstrap-adopt"}
                and result.manifest is not None
            ):
                verification = verify_runtime_manifest(result.manifest)
                valid = verification.verified_manifest_hash is not None
                payload.update(
                    {
                        "valid": valid,
                        "state": "bootstrap-ready" if valid else "runtime-drift",
                        "runtime_diagnostics": [
                            {
                                "source_path": diagnostic.source_path,
                                "line": diagnostic.line,
                                "column": diagnostic.column,
                                "zone_id": diagnostic.zone_id,
                                "entity_id": str(diagnostic.entity_id),
                                "code": diagnostic.code,
                                "message": diagnostic.message,
                            }
                            for diagnostic in verification.diagnostics
                        ],
                    }
                )
                if action == "bootstrap-adopt" and valid:
                    git_commit = options.get("git_commit")
                    if not git_commit:
                        raise CommandError(
                            "bootstrap-adopt requires an explicit --git-commit."
                        )
                    try:
                        revision = adopt_bootstrap(
                            result.manifest,
                            git_commit=git_commit,
                        )
                    except BootstrapAdoptionError as exc:
                        raise CommandError(str(exc)) from exc
                    payload.update(
                        {
                            "state": "bootstrap-adopted",
                            "git_commit": revision.git_commit,
                            "revision_id": revision.pk,
                        }
                    )
            elif action == "apply" and result.manifest is not None:
                git_commit = options.get("git_commit")
                if not git_commit:
                    raise CommandError("apply requires an explicit --git-commit.")
                try:
                    apply_result = apply_world_content(
                        result.manifest,
                        git_commit=git_commit,
                        maintenance_approved=options["maintenance_approved"],
                    )
                except (ApplyPreconditionError, ContentApplyError) as exc:
                    raise CommandError(str(exc)) from exc
                payload.update(
                    {
                        "state": apply_result.state,
                        "git_commit": apply_result.revision.git_commit,
                        "revision_id": apply_result.revision.pk,
                    }
                )
        else:
            status = get_world_content_status(areas_dir)
            valid = not status.state.startswith("invalid")
            payload = {
                "command": action,
                "valid": valid,
                "state": status.state,
                "target_manifest_hash": status.target_manifest_hash,
                "applied_manifest_hash": status.applied_manifest_hash,
                "error": status.error,
                "diagnostics": [
                    {
                        "source_path": diagnostic.source_path,
                        "line": diagnostic.line,
                        "column": diagnostic.column,
                        "code": diagnostic.code,
                        "message": diagnostic.message,
                    }
                    for diagnostic in status.diagnostics
                ],
            }
            if action == "plan":
                payload["plan"] = (
                    serialize_change_plan(status.plan) if status.plan else None
                )

        if output_format == "json":
            self.stdout.write(json.dumps(payload, sort_keys=True))
        else:
            self.stdout.write(
                f"worldcontent {action}: {payload['state']} "
                f"target={payload.get('target_manifest_hash') or '-'}"
            )
            if action == "plan" and payload.get("plan"):
                self.stdout.write(
                    f"changes={len(payload['plan']['changes'])} "
                    f"applied={payload.get('applied_manifest_hash') or '-'}"
                )
            for diagnostic in payload["diagnostics"]:
                self.stdout.write(
                    f"{diagnostic['source_path']}:{diagnostic['line']}:"
                    f"{diagnostic['column']} {diagnostic['code']}: "
                    f"{diagnostic['message']}"
                )
            for diagnostic in payload.get("runtime_diagnostics", []):
                self.stdout.write(
                    f"{diagnostic['source_path']}:{diagnostic['line']}:"
                    f"{diagnostic['column']} {diagnostic['code']} "
                    f"[{diagnostic['zone_id']}:{diagnostic['entity_id']}]: "
                    f"{diagnostic['message']}"
                )
        if not payload["valid"]:
            raise CommandError(payload.get("error") or "World content is invalid.")
