"""
Detect repository hygiene problems that can poison local release work.

Current checks:
- tracked gitlinks or tracked files under `.claude/worktrees`
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    result = _git("ls-files", "--stage", ".claude/worktrees")
    if result.returncode != 0:
        print(result.stderr.strip() or result.stdout.strip())
        return result.returncode or 1

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        print("Repo hygiene OK: no tracked entries under .claude/worktrees")
        return 0

    gitlinks = [line for line in lines if line.startswith("160000 ")]
    regular = [line for line in lines if not line.startswith("160000 ")]

    print("Repo hygiene issue: tracked entries exist under .claude/worktrees")
    print(f"gitlinks: {len(gitlinks)}")
    print(f"regular files: {len(regular)}")

    preview = gitlinks[:10] + regular[:10]
    for line in preview:
        print(line)
    if len(lines) > len(preview):
        print(f"... {len(lines) - len(preview)} more")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
