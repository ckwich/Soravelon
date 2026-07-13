"""Contracts for PostgreSQL startup content-write instrumentation."""

import unittest
from unittest.mock import MagicMock

from psycopg import sql


class TestStartupContentTableSelection(unittest.TestCase):
    def test_selects_world_and_authored_object_storage_only(self):
        from scripts.audit_startup_content_writes import content_table_names

        selected = content_table_names(
            {
                "world_worldcontentrevision",
                "world_socialnode",
                "objects_objectdb",
                "objects_objectdb_db_attributes",
                "objects_objectdb_db_tags",
                "typeclasses_attribute",
                "typeclasses_tag",
                "accounts_accountdb",
                "server_serverconfig",
                "scripts_scriptdb",
                "django_migrations",
                "soravelon_m6_events",
            }
        )

        self.assertEqual(
            selected,
            (
                "objects_objectdb",
                "objects_objectdb_db_attributes",
                "objects_objectdb_db_tags",
                "typeclasses_attribute",
                "typeclasses_tag",
                "world_socialnode",
                "world_worldcontentrevision",
            ),
        )

    def test_requires_every_core_authored_storage_table(self):
        from scripts.audit_startup_content_writes import StartupWriteAuditError
        from scripts.audit_startup_content_writes import content_table_names

        with self.assertRaisesRegex(StartupWriteAuditError, "missing core"):
            content_table_names({"world_worldcontentrevision"})


class TestStartupWriteReport(unittest.TestCase):
    def test_zero_and_nonzero_reports_are_stable_json_values(self):
        from scripts.audit_startup_content_writes import build_write_report

        zero = build_write_report([])
        writes = build_write_report(
            [
                ("objects_objectdb", "UPDATE", 2),
                ("world_socialnode", "INSERT", 1),
            ]
        )

        self.assertEqual(zero, {"total_writes": 0, "writes": []})
        self.assertEqual(
            writes,
            {
                "total_writes": 3,
                "writes": [
                    {
                        "table": "objects_objectdb",
                        "operation": "UPDATE",
                        "count": 2,
                    },
                    {
                        "table": "world_socialnode",
                        "operation": "INSERT",
                        "count": 1,
                    },
                ],
            },
        )


class TestStartupWriteSqlComposition(unittest.TestCase):
    def test_install_composes_every_dynamic_identifier(self):
        from scripts.audit_startup_content_writes import CORE_CONTENT_TABLES
        from scripts.audit_startup_content_writes import _install

        hostile_table = "world_events; DROP TABLE players"
        connection = MagicMock()
        connection.introspection.table_names.return_value = {
            *CORE_CONTENT_TABLES,
            hostile_table,
        }
        cursor = connection.cursor.return_value.__enter__.return_value

        _install(connection)

        queries = [call.args[0] for call in cursor.execute.call_args_list]
        self.assertTrue(queries)
        for query in queries:
            with self.subTest(query=query):
                self.assertIsInstance(query, sql.Composable)
        rendered = "\n".join(query.as_string(None) for query in queries)
        self.assertIn(f'"{hostile_table}"', rendered)


if __name__ == "__main__":
    unittest.main()
