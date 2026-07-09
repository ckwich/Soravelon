"""Fail releases when transient or sensitive files are tracked by Git."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


REPO_ROOT = Path(__file__).resolve().parents[1]

_DATABASE_NAME = re.compile(
    r"(?i).+\.(?:db|db3|sqlite|sqlite3)(?:-(?:journal|shm|wal))?$"
)
_GENERATED_EXACT_PATHS = {
    ".claude/code-map.md",
    ".claude/graph-index.json",
    ".claude/graph.json",
    ".claude/scheduled_tasks.lock",
}
_ALLOWED_RUNTIME_DIRECTORY_MARKERS = {".gitkeep", "README.md"}


class GitInspectionError(RuntimeError):
    """The Git index could not be inspected reliably."""


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def _git_paths(*args: str) -> set[str]:
    result = _git(*args, "-z")
    if result.returncode != 0:
        raise GitInspectionError("Git index inspection failed.")
    return {path for path in result.stdout.split("\0") if path}


def _is_environment_file(path: PurePosixPath) -> bool:
    name = path.name
    return name == ".env" or (
        name.startswith(".env.") and not name.endswith(".example")
    )


def _is_secret_settings(path: PurePosixPath) -> bool:
    return (
        path.parent.as_posix() == "server/conf"
        and path.name.startswith("secret_settings")
        and path.name != "secret_settings.example.py"
    )


def _is_runtime_log(path: PurePosixPath) -> bool:
    return (
        path.as_posix().startswith("server/logs/")
        and path.name not in _ALLOWED_RUNTIME_DIRECTORY_MARKERS
    )


def _is_area_temporary_file(path: PurePosixPath) -> bool:
    if not path.as_posix().startswith("world/areas/"):
        return False
    name = path.name.lower()
    return name.endswith(("~", ".bak", ".orig", ".rej", ".swo", ".swp", ".tmp"))


def _is_generated_file(path: PurePosixPath) -> bool:
    path_string = path.as_posix()
    parts = path.parts
    return any(
        (
            path_string in _GENERATED_EXACT_PATHS,
            path_string.startswith(".agents/"),
            path.name == ".DS_Store",
            path.name.startswith("CODEX_ROUND_") and path.suffix == ".md",
            path.suffix.lower() in {".pyc", ".pyo", ".pid"},
            "__pycache__" in parts,
            ".pytest_cache" in parts,
            bool(parts and parts[0] in {".venv", "venv"}),
            bool(parts and parts[0].startswith("pytest-cache-files-")),
            any(part.endswith(".egg-info") for part in parts),
        )
    )


def _is_forbidden_tracked_path(path_string: str) -> bool:
    path = PurePosixPath(path_string)
    normalized = path.as_posix()
    return any(
        (
            _is_environment_file(path),
            _is_secret_settings(path),
            _is_runtime_log(path),
            normalized == "server/.static"
            or normalized.startswith("server/.static/"),
            normalized == ".claude/worktrees"
            or normalized.startswith(".claude/worktrees/"),
            bool(_DATABASE_NAME.fullmatch(path.name)),
            _is_area_temporary_file(path),
            _is_generated_file(path),
        )
    )


def find_hygiene_violations() -> list[str]:
    """Return sorted tracked paths that cannot ship in a release commit."""
    tracked_paths = _git_paths("ls-files", "--cached")
    tracked_ignored_paths = _git_paths(
        "ls-files",
        "--cached",
        "--ignored",
        "--exclude-standard",
    )
    violations = tracked_ignored_paths | {
        path for path in tracked_paths if _is_forbidden_tracked_path(path)
    }
    return sorted(violations)


def main() -> int:
    try:
        violations = find_hygiene_violations()
    except GitInspectionError:
        print("Repo hygiene ERROR: Git index inspection failed.", file=sys.stderr)
        return 2

    if not violations:
        print("Repo hygiene OK: no forbidden tracked paths")
        return 0

    print(f"Repo hygiene FAILED: {len(violations)} forbidden tracked path(s)")
    for path in violations:
        print(path)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
