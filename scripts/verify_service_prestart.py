"""Fast, fail-closed checks run before the production systemd service."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]


def build_prestart_steps(python: str) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Return the ordered, non-destructive production boot checks."""

    return (
        (
            "production security configuration",
            (
                python,
                "-m",
                "django",
                "check",
                "--deploy",
                "--fail-level",
                "WARNING",
            ),
        ),
        (
            "pending migrations",
            (python, "-m", "django", "migrate", "--check"),
        ),
        (
            "runtime imports",
            (python, str(REPO_ROOT / "scripts" / "smoke_start.py")),
        ),
        (
            "collected static assets",
            (python, "-m", "django", "collectstatic", "--noinput"),
        ),
    )


def run_prestart(*, python: str | None = None) -> int:
    """Run the service checks in order and return the first failure code."""

    if os.environ.get("SORAVELON_ENV", "").lower() != "production":
        print(
            "Service prestart refused: SORAVELON_ENV must be production.",
            file=sys.stderr,
        )
        return 2
    if os.environ.get("DJANGO_SETTINGS_MODULE") != "server.conf.settings":
        print(
            "Service prestart refused: DJANGO_SETTINGS_MODULE must be "
            "server.conf.settings.",
            file=sys.stderr,
        )
        return 2

    executable = python or sys.executable
    for label, command in build_prestart_steps(executable):
        print(f"Service prestart: {label} ...", flush=True)
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            check=False,
        )
        if completed.returncode:
            print(
                f"Service prestart FAILED at {label} "
                f"(exit {completed.returncode}).",
                file=sys.stderr,
            )
            return completed.returncode

    print("Service prestart passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_prestart())
