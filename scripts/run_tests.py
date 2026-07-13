"""
Canonical Soravelon test runner.

This uses Django's test command with the Soravelon settings module loaded,
which matches how Evennia-backed tests expect to run.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--keepdb",
        action="store_true",
        help="Reuse an explicitly configured, pre-created test database.",
    )
    parser.add_argument("test_labels", nargs="*")
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")

    import django
    from django.core.management import call_command

    django.setup()
    test_labels = args.test_labels or ["tests"]
    call_command(
        "test",
        *test_labels,
        verbosity=1,
        keepdb=args.keepdb,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
