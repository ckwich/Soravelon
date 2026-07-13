"""Prepare one pre-created candidate test database without CREATEDB power."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
from typing import Any, Callable, Mapping


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

_TEST_DATABASE_PATTERN = re.compile(
    r"test_soravelon_rehearsal_[a-z0-9][a-z0-9_]*"
)


def require_candidate_database(
    database: Mapping[str, Any],
    *,
    expected_name: str,
    actual_name: str,
) -> None:
    """Fail closed unless every identity names the same disposable database."""

    configured_name = str(database.get("NAME") or "")
    if (
        database.get("ENGINE") != "django.db.backends.postgresql"
        or _TEST_DATABASE_PATTERN.fullmatch(expected_name) is None
        or len(expected_name) > 63
        or configured_name != expected_name
    ):
        raise RuntimeError(
            "Candidate test preparation requires one explicit disposable "
            "PostgreSQL test_soravelon_rehearsal_* database."
        )
    if actual_name != expected_name:
        raise RuntimeError(
            "Refusing candidate test preparation because the live database "
            "identity does not match the expected database."
        )


def seed_evennia_foundation(
    *,
    account_model: Any,
    object_model: Any,
    initialize: Callable[[], Any],
) -> None:
    """Create durable test-only Account #1 and Evennia object foundation."""

    if account_model.objects.exists():
        raise RuntimeError(
            "Candidate test foundation requires an empty account table."
        )
    account = account_model.objects.create_superuser(
        username="CandidateTestAdmin",
        email="candidate-test-admin@example.invalid",
        password=None,
    )
    if (
        account.pk != 1
        or not account.is_superuser
        or not account.is_staff
        or account.has_usable_password()
    ):
        raise RuntimeError(
            "Candidate test admin must be unusable-password superuser account #1."
        )

    initialize()
    if object_model.objects.filter(pk__in=(1, 2)).count() != 2:
        raise RuntimeError(
            "Candidate test preparation did not create Evennia objects #1 and #2."
        )


def prepare_candidate_test_database(expected_name: str) -> None:
    """Migrate and seed the configured disposable candidate test database."""

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
    import django

    django.setup()

    from django.conf import settings
    from django.core.management import call_command
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database()")
        row = cursor.fetchone()
    require_candidate_database(
        settings.DATABASES["default"],
        expected_name=expected_name,
        actual_name=row[0] if row else "",
    )

    call_command("migrate", interactive=False, verbosity=0, database="default")

    from evennia.accounts.models import AccountDB
    from evennia.objects.models import ObjectDB
    from world.content_revisions import _ensure_evennia_runtime_initialized

    seed_evennia_foundation(
        account_model=AccountDB,
        object_model=ObjectDB,
        initialize=_ensure_evennia_runtime_initialized,
    )
    print(f"Candidate test foundation prepared: {expected_name}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-database-name", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    prepare_candidate_test_database(args.expected_database_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
