#!/usr/bin/env python3
"""Instrument a rehearsal PostgreSQL DB and report startup content writes."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Iterable

from psycopg import sql


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.rehearse_content_release import (  # noqa: E402
    RehearsalSafetyError,
    require_checkout_commit,
    require_disposable_postgres,
)


AUDIT_SCHEMA = "soravelon_m6_audit"
AUDIT_TABLE = "events"
AUDIT_FUNCTION = "record_content_write"
AUDIT_TRIGGER = "soravelon_m6_content_write_audit"
CORE_CONTENT_TABLES = frozenset(
    {
        "objects_objectdb",
        "objects_objectdb_db_attributes",
        "objects_objectdb_db_tags",
        "typeclasses_attribute",
        "typeclasses_tag",
    }
)


class StartupWriteAuditError(RuntimeError):
    """Startup write instrumentation could not prove its contract."""


def content_table_names(available_tables: Iterable[str]) -> tuple[str, ...]:
    """Return every project world table plus core authored object storage."""

    available = frozenset(str(table) for table in available_tables)
    missing = sorted(CORE_CONTENT_TABLES - available)
    if missing:
        raise StartupWriteAuditError(
            "Startup write audit is missing core authored tables: "
            + ", ".join(missing)
        )
    selected = CORE_CONTENT_TABLES | {
        table for table in available if table.startswith("world_")
    }
    return tuple(sorted(selected))


def build_write_report(rows: Iterable[tuple[str, str, int]]) -> dict[str, object]:
    """Build stable JSON evidence from grouped audit rows."""

    writes = [
        {
            "table": str(table),
            "operation": str(operation),
            "count": int(count),
        }
        for table, operation, count in sorted(rows)
    ]
    return {
        "total_writes": sum(item["count"] for item in writes),
        "writes": writes,
    }


def _install(connection) -> tuple[str, ...]:
    tables = content_table_names(connection.introspection.table_names())
    with connection.cursor() as cursor:
        cursor.execute(
            sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
                sql.Identifier(AUDIT_SCHEMA)
            )
        )
        cursor.execute(
            sql.SQL(
                """
            CREATE TABLE IF NOT EXISTS {} (
                id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                table_name text NOT NULL,
                operation text NOT NULL,
                recorded_at timestamptz NOT NULL DEFAULT clock_timestamp()
            )
            """
            ).format(sql.Identifier(AUDIT_SCHEMA, AUDIT_TABLE))
        )
        cursor.execute(
            sql.SQL(
                """
            CREATE OR REPLACE FUNCTION
                {}()
            RETURNS trigger
            LANGUAGE plpgsql
            AS $function$
            BEGIN
                INSERT INTO {}
                    (table_name, operation)
                VALUES (TG_TABLE_NAME, TG_OP);
                IF TG_OP = 'DELETE' THEN
                    RETURN OLD;
                END IF;
                RETURN NEW;
            END;
            $function$
            """
            ).format(
                sql.Identifier(AUDIT_SCHEMA, AUDIT_FUNCTION),
                sql.Identifier(AUDIT_SCHEMA, AUDIT_TABLE),
            )
        )
        for table in tables:
            cursor.execute(
                sql.SQL("DROP TRIGGER IF EXISTS {} ON {}").format(
                    sql.Identifier(AUDIT_TRIGGER),
                    sql.Identifier(table),
                )
            )
            cursor.execute(
                sql.SQL(
                    """
                CREATE TRIGGER {}
                AFTER INSERT OR UPDATE OR DELETE ON {}
                FOR EACH ROW EXECUTE FUNCTION
                    {}()
                """
                ).format(
                    sql.Identifier(AUDIT_TRIGGER),
                    sql.Identifier(table),
                    sql.Identifier(AUDIT_SCHEMA, AUDIT_FUNCTION),
                )
            )
        cursor.execute(
            sql.SQL("TRUNCATE TABLE {}").format(
                sql.Identifier(AUDIT_SCHEMA, AUDIT_TABLE)
            )
        )
    return tables


def _reset(connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            sql.SQL("TRUNCATE TABLE {}").format(
                sql.Identifier(AUDIT_SCHEMA, AUDIT_TABLE)
            )
        )


def _report(connection) -> dict[str, object]:
    with connection.cursor() as cursor:
        cursor.execute(
            sql.SQL(
                """
            SELECT table_name, operation, count(*)
            FROM {}
            GROUP BY table_name, operation
            ORDER BY table_name, operation
            """
            ).format(sql.Identifier(AUDIT_SCHEMA, AUDIT_TABLE))
        )
        return build_write_report(cursor.fetchall())


def _uninstall(connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(
                sql.Identifier(AUDIT_SCHEMA)
            )
        )


def _load_connection(args: argparse.Namespace):
    require_checkout_commit(args.git_commit)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
    import django

    django.setup()

    from django.conf import settings
    from django.db import connection

    require_disposable_postgres(
        settings.DATABASES["default"],
        expected_name=args.expected_database_name,
    )
    return connection


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "reset", "report", "uninstall"))
    parser.add_argument("--expected-database-name", required=True)
    parser.add_argument("--git-commit", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        connection = _load_connection(args)
        if args.action == "install":
            tables = _install(connection)
            payload = {
                "action": "install",
                "instrumented_tables": list(tables),
            }
        elif args.action == "reset":
            _reset(connection)
            payload = {"action": "reset", "total_writes": 0}
        elif args.action == "report":
            payload = {"action": "report", **_report(connection)}
        else:
            _uninstall(connection)
            payload = {"action": "uninstall"}
    except (RehearsalSafetyError, StartupWriteAuditError) as exc:
        print(f"Startup content-write audit FAILED: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, sort_keys=True))
    if args.action == "report" and payload["total_writes"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
