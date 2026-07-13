#!/usr/bin/env python3
"""Validate a complete, secret-free Soravelon M6 release-evidence record."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any, Mapping


SCHEMA_VERSION = "soravelon.release-evidence.v1"
REHEARSAL_DATABASE_PATTERN = re.compile(
    r"^soravelon_rehearsal_[a-z0-9][a-z0-9_]{0,62}$"
)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
GIT_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40,64}$")
BUILDER_PLATFORMS = {
    "macos-arm64",
    "macos-x64",
    "windows-x64",
    "linux-x64",
}
SECRET_FIELD_PARTS = (
    "password",
    "secret",
    "credential",
    "private_key",
    "access_token",
    "api_key",
)


def _mapping(value: Any, path: str, issues: list[str]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        issues.append(f"{path} must be an object.")
        return {}
    return value


def _list(value: Any, path: str, issues: list[str]) -> list[Any]:
    if not isinstance(value, list):
        issues.append(f"{path} must be a list.")
        return []
    return value


def _nonempty_string(value: Any, path: str, issues: list[str]) -> str:
    if not isinstance(value, str) or not value.strip():
        issues.append(f"{path} must be a non-empty string.")
        return ""
    return value


def _sha256(value: Any, path: str, issues: list[str]) -> str:
    text = _nonempty_string(value, path, issues)
    if text and SHA256_PATTERN.fullmatch(text) is None:
        issues.append(f"{path} must be a lowercase SHA-256 hex digest.")
    return text


def _git_commit(value: Any, path: str, issues: list[str]) -> str:
    text = _nonempty_string(value, path, issues)
    if text and GIT_COMMIT_PATTERN.fullmatch(text) is None:
        issues.append(f"{path} must be a 40-64 character lowercase Git object ID.")
    return text


def _true(value: Any, path: str, issues: list[str]) -> None:
    if value is not True:
        issues.append(f"{path} must be true.")


def _relative_artifact(value: Any, path: str, issues: list[str]) -> str:
    text = _nonempty_string(value, path, issues)
    if not text:
        return text
    artifact = PurePosixPath(text)
    if artifact.is_absolute() or ".." in artifact.parts:
        issues.append(f"{path} must be a safe relative artifact path.")
    return text


def _database_name(value: Any, path: str, issues: list[str]) -> str:
    text = _nonempty_string(value, path, issues)
    if text and REHEARSAL_DATABASE_PATTERN.fullmatch(text) is None:
        issues.append(f"{path} must use the soravelon_rehearsal_* naming contract.")
    return text


def _find_secret_fields(value: Any, path: str, issues: list[str]) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key).casefold()
            if any(part in key_text for part in SECRET_FIELD_PARTS):
                issues.append(f"{path}.{key} is a forbidden secret-like field.")
            _find_secret_fields(item, f"{path}.{key}", issues)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _find_secret_fields(item, f"{path}[{index}]", issues)


def _validate_content_evidence(
    value: Any,
    *,
    path: str,
    expected_kind: str,
    release_commit: str,
    release_manifest: str,
    issues: list[str],
) -> str:
    content = _mapping(value, path, issues)
    if content.get("database_kind") != expected_kind:
        issues.append(f"{path}.database_kind must be {expected_kind!r}.")
    database_name = _database_name(
        content.get("database_name"),
        f"{path}.database_name",
        issues,
    )
    expected_initial = {"uninitialized"} if expected_kind == "fresh" else {
        "current",
        "drifted",
    }
    if content.get("initial_state") not in expected_initial:
        issues.append(
            f"{path}.initial_state must be one of {sorted(expected_initial)}."
        )
    expected_first = {"initialized"} if expected_kind == "fresh" else {
        "applied",
        "no-op",
    }
    if content.get("first_state") not in expected_first:
        issues.append(f"{path}.first_state must be one of {sorted(expected_first)}.")
    if content.get("reapply_state") != "no-op":
        issues.append(f"{path}.reapply_state must be 'no-op'.")
    if content.get("final_state") != "current":
        issues.append(f"{path}.final_state must be 'current'.")
    manifest_hash = _sha256(
        content.get("manifest_hash"),
        f"{path}.manifest_hash",
        issues,
    )
    if release_manifest and manifest_hash and manifest_hash != release_manifest:
        issues.append(f"{path}.manifest_hash must match release.manifest_hash.")
    git_commit = _git_commit(
        content.get("git_commit"),
        f"{path}.git_commit",
        issues,
    )
    if release_commit and git_commit and git_commit != release_commit:
        issues.append(f"{path}.git_commit must match release.git_commit.")
    revision_id = content.get("revision_id")
    if not isinstance(revision_id, int) or isinstance(revision_id, bool) or revision_id < 1:
        issues.append(f"{path}.revision_id must be a positive integer.")
    return database_name


def _validate_rehearsal(
    value: Any,
    *,
    index: int,
    release_commit: str,
    release_manifest: str,
    issues: list[str],
) -> tuple[str, set[str]]:
    path = f"rehearsals[{index}]"
    rehearsal = _mapping(value, path, issues)
    run_id = _nonempty_string(rehearsal.get("run_id"), f"{path}.run_id", issues)
    databases = {
        _validate_content_evidence(
            rehearsal.get("fresh_content"),
            path=f"{path}.fresh_content",
            expected_kind="fresh",
            release_commit=release_commit,
            release_manifest=release_manifest,
            issues=issues,
        ),
        _validate_content_evidence(
            rehearsal.get("restored_content"),
            path=f"{path}.restored_content",
            expected_kind="restored",
            release_commit=release_commit,
            release_manifest=release_manifest,
            issues=issues,
        ),
        _database_name(
            rehearsal.get("candidate_database"),
            f"{path}.candidate_database",
            issues,
        ),
    }
    databases.discard("")
    if len(databases) != 3:
        issues.append(f"{path} must name three distinct rehearsal databases.")

    backup = _mapping(rehearsal.get("backup"), f"{path}.backup", issues)
    _relative_artifact(backup.get("artifact"), f"{path}.backup.artifact", issues)
    _sha256(backup.get("sha256"), f"{path}.backup.sha256", issues)
    _true(backup.get("restore_verified"), f"{path}.backup.restore_verified", issues)

    failure = _mapping(
        rehearsal.get("failure_injection"),
        f"{path}.failure_injection",
        issues,
    )
    for proof in ("content", "economy", "inventory", "quest"):
        _true(failure.get(proof), f"{path}.failure_injection.{proof}", issues)

    lifecycle = _mapping(rehearsal.get("lifecycle"), f"{path}.lifecycle", issues)
    for proof in (
        "start",
        "crash_restart",
        "reload",
        "stop",
        "reboot",
        "listeners_recovered",
        "portal_pid_preserved_on_reload",
    ):
        _true(lifecycle.get(proof), f"{path}.lifecycle.{proof}", issues)
    if lifecycle.get("startup_content_writes") != [0, 0]:
        issues.append(f"{path}.lifecycle.startup_content_writes must be [0, 0].")

    candidate = _mapping(rehearsal.get("candidate"), f"{path}.candidate", issues)
    _true(candidate.get("passed"), f"{path}.candidate.passed", issues)
    _sha256(
        candidate.get("output_sha256"),
        f"{path}.candidate.output_sha256",
        issues,
    )
    return run_id, databases


def validate_release_evidence(record: Any) -> list[str]:
    """Return stable validation issues; an empty list is release-ready."""

    issues: list[str] = []
    root = _mapping(record, "record", issues)
    _find_secret_fields(root, "record", issues)
    if root.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"schema_version must be {SCHEMA_VERSION!r}.")

    release = _mapping(root.get("release"), "release", issues)
    release_commit = _git_commit(release.get("git_commit"), "release.git_commit", issues)
    release_manifest = _sha256(
        release.get("manifest_hash"),
        "release.manifest_hash",
        issues,
    )
    created_at = _nonempty_string(
        release.get("created_at_utc"),
        "release.created_at_utc",
        issues,
    )
    if created_at:
        try:
            parsed = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            if not created_at.endswith("Z") or parsed.utcoffset() is None:
                raise ValueError
        except ValueError:
            issues.append("release.created_at_utc must be an ISO-8601 UTC timestamp.")
    limitations = _list(release.get("limitations"), "release.limitations", issues)
    if not limitations or any(not isinstance(item, str) or not item.strip() for item in limitations):
        issues.append("release.limitations must explicitly list non-empty limitations.")
    rollback = _list(
        release.get("rollback_instructions"),
        "release.rollback_instructions",
        issues,
    )
    if len(rollback) < 3 or any(not isinstance(item, str) or not item.strip() for item in rollback):
        issues.append("release.rollback_instructions must contain at least three steps.")

    environment = _mapping(root.get("environment"), "environment", issues)
    for field in ("os", "architecture", "python", "postgresql", "django", "evennia", "psycopg"):
        _nonempty_string(environment.get(field), f"environment.{field}", issues)

    rehearsals = _list(root.get("rehearsals"), "rehearsals", issues)
    if len(rehearsals) != 2:
        issues.append("rehearsals must contain exactly two independent runs.")
    run_ids: list[str] = []
    all_databases: list[str] = []
    for index, rehearsal in enumerate(rehearsals):
        run_id, databases = _validate_rehearsal(
            rehearsal,
            index=index,
            release_commit=release_commit,
            release_manifest=release_manifest,
            issues=issues,
        )
        if run_id:
            run_ids.append(run_id)
        all_databases.extend(databases)
    if len(run_ids) != len(set(run_ids)):
        issues.append("rehearsal run_id values must be unique.")
    if len(all_databases) != len(set(all_databases)):
        issues.append("all rehearsal database names must be unique across runs.")

    packages = _list(root.get("builder_packages"), "builder_packages", issues)
    platforms: list[str] = []
    for index, value in enumerate(packages):
        path = f"builder_packages[{index}]"
        package = _mapping(value, path, issues)
        platform = _nonempty_string(package.get("platform"), f"{path}.platform", issues)
        if platform:
            platforms.append(platform)
        _relative_artifact(package.get("artifact"), f"{path}.artifact", issues)
        _sha256(package.get("sha256"), f"{path}.sha256", issues)
        _true(package.get("tests_passed"), f"{path}.tests_passed", issues)
    if set(platforms) != BUILDER_PLATFORMS or len(platforms) != len(BUILDER_PLATFORMS):
        issues.append(
            "builder_packages must contain exactly macos-arm64, macos-x64, "
            "windows-x64, and linux-x64."
        )

    acceptance = _mapping(root.get("human_acceptance"), "human_acceptance", issues)
    for proof in ("timed_fresh_player", "co_op", "living_world"):
        _true(acceptance.get(proof), f"human_acceptance.{proof}", issues)
    _nonempty_string(acceptance.get("observed_by"), "human_acceptance.observed_by", issues)
    _nonempty_string(acceptance.get("notes"), "human_acceptance.notes", issues)

    artifacts = _list(root.get("artifacts"), "artifacts", issues)
    if not artifacts:
        issues.append("artifacts must contain at least one release artifact.")
    artifact_paths: list[str] = []
    for index, value in enumerate(artifacts):
        path = f"artifacts[{index}]"
        artifact = _mapping(value, path, issues)
        artifact_path = _relative_artifact(artifact.get("path"), f"{path}.path", issues)
        if artifact_path:
            artifact_paths.append(artifact_path)
        _sha256(artifact.get("sha256"), f"{path}.sha256", issues)
        size = artifact.get("size_bytes")
        if not isinstance(size, int) or isinstance(size, bool) or size < 1:
            issues.append(f"{path}.size_bytes must be a positive integer.")
    if len(artifact_paths) != len(set(artifact_paths)):
        issues.append("artifact paths must be unique.")

    return sorted(set(issues))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args(argv)
    try:
        record = json.loads(args.record.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Release evidence FAILED: {exc}", file=sys.stderr)
        return 1
    issues = validate_release_evidence(record)
    if issues:
        print(f"Release evidence FAILED: {len(issues)} issue(s)", file=sys.stderr)
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1
    print(f"Release evidence passed: {args.record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
