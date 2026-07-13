"""
Canonical Soravelon test runner.

This uses Django's test command with the Soravelon settings module loaded,
which matches how Evennia-backed tests expect to run.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
from typing import Any, Callable, Mapping


_REHEARSAL_DATABASE = re.compile(
    r"soravelon_rehearsal_[a-z0-9][a-z0-9_]*"
)
_REHEARSAL_TEST_DATABASE = re.compile(
    r"test_soravelon_rehearsal_[a-z0-9][a-z0-9_]*"
)


def reset_precreated_test_database(
    database: Mapping[str, Any],
    *,
    connect: Callable[..., Any] | None = None,
) -> None:
    """Reset one explicitly named disposable PostgreSQL test database."""

    engine = str(database.get("ENGINE") or "")
    database_name = str(database.get("NAME") or "")
    test_name = str((database.get("TEST") or {}).get("NAME") or "")
    if (
        engine != "django.db.backends.postgresql"
        or _REHEARSAL_DATABASE.fullmatch(database_name) is None
        or len(database_name) > 63
    ):
        raise RuntimeError(
            "Kept-database reset requires a disposable PostgreSQL "
            "soravelon_rehearsal_* base database."
        )
    if (
        _REHEARSAL_TEST_DATABASE.fullmatch(test_name) is None
        or len(test_name) > 63
    ):
        raise RuntimeError(
            "Kept-database reset requires a disposable "
            "test_soravelon_rehearsal_* test database."
        )

    if connect is None:
        from psycopg import connect as psycopg_connect

        connect = psycopg_connect

    with connect(
        dbname=test_name,
        user=database.get("USER"),
        password=database.get("PASSWORD"),
        host=database.get("HOST"),
        port=database.get("PORT"),
        autocommit=True,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database()")
            row = cursor.fetchone()
            actual_name = row[0] if row else None
            if actual_name != test_name:
                raise RuntimeError(
                    "Refusing kept-database reset because the live database "
                    "identity does not match DATABASE_TEST_NAME."
                )
            cursor.execute("DROP SCHEMA public CASCADE")
            cursor.execute("CREATE SCHEMA public")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--keepdb",
        action="store_true",
        help="Reuse an explicitly configured, pre-created test database.",
    )
    parser.add_argument(
        "--reset-kept-db",
        action="store_true",
        help=(
            "Rebuild the public schema of a disposable pre-created test "
            "database before running tests."
        ),
    )
    parser.add_argument("test_labels", nargs="*")
    args = parser.parse_args(argv)
    if args.reset_kept_db and not args.keepdb:
        parser.error("--reset-kept-db requires --keepdb")

    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")

    import django
    from django.conf import settings
    from django.core.management import call_command

    django.setup()
    if args.reset_kept_db:
        reset_precreated_test_database(settings.DATABASES["default"])
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
