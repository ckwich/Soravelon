#!/usr/bin/env python3
"""Prove one disposable PostgreSQL world-content release rehearsal."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Callable, Mapping


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

REHEARSAL_DATABASE_PATTERN = re.compile(
    r"^soravelon_rehearsal_[a-z0-9][a-z0-9_]{0,62}$"
)


class RehearsalSafetyError(RuntimeError):
    """The configured database is not provably a disposable rehearsal target."""


class ContentRehearsalError(RuntimeError):
    """The world-content rehearsal did not satisfy its release contract."""


@dataclass(frozen=True)
class DatabaseIdentity:
    engine: str
    name: str


@dataclass(frozen=True)
class ContentRehearsalEvidence:
    database_kind: str
    database_name: str
    manifest_hash: str
    initial_state: str
    first_state: str
    reapply_state: str
    final_state: str
    revision_id: int
    git_commit: str


def require_disposable_postgres(
    database: Mapping[str, Any],
    *,
    expected_name: str,
) -> DatabaseIdentity:
    """Return the exact DB identity or refuse a non-rehearsal target."""

    engine = str(database.get("ENGINE") or "")
    name = str(database.get("NAME") or "")
    if not engine.startswith("django.db.backends.postgresql"):
        raise RehearsalSafetyError(
            f"Content release rehearsal requires PostgreSQL; got {engine!r}."
        )
    if name != expected_name:
        raise RehearsalSafetyError(
            f"Configured database {name!r} does not match the explicit expected "
            f"name {expected_name!r}."
        )
    if REHEARSAL_DATABASE_PATTERN.fullmatch(name) is None:
        raise RehearsalSafetyError(
            "Content release rehearsal database must use the disposable "
            "soravelon_rehearsal_* naming contract."
        )
    return DatabaseIdentity(engine=engine, name=name)


def _status_failure(status: Any) -> str:
    details = [str(getattr(status, "error", "") or "").strip()]
    details.extend(
        f"{item.source_path}:{item.line} [{item.code}] {item.message}"
        for item in getattr(status, "diagnostics", ())
    )
    return "; ".join(detail for detail in details if detail)


def rehearse_content_revision(
    *,
    database_kind: str,
    database_name: str,
    manifest: Any,
    git_commit: str,
    load_status: Callable[[], Any],
    initialize: Callable[..., Any],
    apply: Callable[..., Any],
    verify_runtime: Callable[[Any], Any],
) -> ContentRehearsalEvidence:
    """Apply one revision, verify runtime truth, and require a no-op reapply."""

    if database_kind not in {"fresh", "restored"}:
        raise ContentRehearsalError(
            "Database kind must be exactly 'fresh' or 'restored'."
        )
    initial = load_status()
    expected_initial_states = (
        {"uninitialized"} if database_kind == "fresh" else {"current", "drifted"}
    )
    if initial.state not in expected_initial_states:
        expected = " or ".join(sorted(expected_initial_states))
        details = _status_failure(initial)
        suffix = f" Details: {details}" if details else ""
        raise ContentRehearsalError(
            f"{database_kind.title()} rehearsal requires initial state {expected}; "
            f"got {initial.state}.{suffix}"
        )
    if initial.target_manifest_hash != manifest.manifest_hash:
        raise ContentRehearsalError(
            "Status target hash disagrees with the compiled rehearsal manifest."
        )

    if database_kind == "fresh":
        first = initialize(manifest, git_commit=git_commit)
        if first.state != "initialized":
            raise ContentRehearsalError(
                f"Fresh rehearsal must initialize content; got {first.state}."
            )
    else:
        first = apply(manifest, git_commit=git_commit)
        if first.state not in {"applied", "no-op"}:
            raise ContentRehearsalError(
                f"Restored rehearsal must apply or be current; got {first.state}."
            )

    repeated = apply(manifest, git_commit=git_commit)
    if repeated.state != "no-op":
        raise ContentRehearsalError(
            f"Idempotent content reapply must be no-op; got {repeated.state}."
        )
    if repeated.revision.pk != first.revision.pk:
        raise ContentRehearsalError(
            "Idempotent content reapply changed the applied revision identity."
        )

    final = load_status()
    if (
        final.state != "current"
        or final.target_manifest_hash != manifest.manifest_hash
        or final.applied_manifest_hash != manifest.manifest_hash
    ):
        details = _status_failure(final)
        suffix = f" Details: {details}" if details else ""
        raise ContentRehearsalError(
            "Final content status is not current at the compiled manifest hash."
            + suffix
        )
    verification = verify_runtime(manifest)
    if verification.verified_manifest_hash != manifest.manifest_hash:
        diagnostics = "; ".join(
            f"{item.source_path}:{item.line} [{item.code}] {item.message}"
            for item in getattr(verification, "diagnostics", ())
        )
        suffix = f" Details: {diagnostics}" if diagnostics else ""
        raise ContentRehearsalError(
            "Runtime content does not exactly match the compiled manifest." + suffix
        )

    return ContentRehearsalEvidence(
        database_kind=database_kind,
        database_name=database_name,
        manifest_hash=manifest.manifest_hash,
        initial_state=initial.state,
        first_state=first.state,
        reapply_state=repeated.state,
        final_state=final.state,
        revision_id=first.revision.pk,
        git_commit=git_commit,
    )


def _run(args: argparse.Namespace) -> ContentRehearsalEvidence:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
    import django

    django.setup()

    from django.conf import settings
    from world.content_compiler import compile_world_manifest
    from world.content_revisions import (
        apply_world_content,
        get_world_content_status,
        initialize_world_content,
    )
    from world.content_runtime import verify_runtime_manifest

    database_identity = require_disposable_postgres(
        settings.DATABASES["default"],
        expected_name=args.expected_database_name,
    )
    areas_dir = Path(settings.GAME_DIR) / "world" / "areas"
    compilation = compile_world_manifest(areas_dir)
    if compilation.manifest is None:
        diagnostics = "; ".join(
            f"{item.source_path}:{item.line} [{item.code}] {item.message}"
            for item in compilation.diagnostics
        )
        raise ContentRehearsalError(
            f"World content compilation failed before rehearsal: {diagnostics}"
        )

    return rehearse_content_revision(
        database_kind=args.database_kind,
        database_name=database_identity.name,
        manifest=compilation.manifest,
        git_commit=args.git_commit,
        load_status=lambda: get_world_content_status(areas_dir),
        initialize=initialize_world_content,
        apply=apply_world_content,
        verify_runtime=verify_runtime_manifest,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database-kind",
        required=True,
        choices=("fresh", "restored"),
    )
    parser.add_argument("--expected-database-name", required=True)
    parser.add_argument("--git-commit", required=True)
    parser.add_argument("--format", choices=("human", "json"), default="human")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        evidence = _run(args)
    except (ContentRehearsalError, RehearsalSafetyError) as exc:
        print(f"Content release rehearsal FAILED: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(asdict(evidence), sort_keys=True))
    else:
        print(
            "Content release rehearsal passed: "
            f"{evidence.database_name} ({evidence.database_kind}) "
            f"{evidence.first_state} -> "
            f"{evidence.reapply_state}; manifest={evidence.manifest_hash} "
            f"revision={evidence.revision_id} commit={evidence.git_commit}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
