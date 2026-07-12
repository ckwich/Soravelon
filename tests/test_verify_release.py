"""Executable release verification contract tests."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scripts import verify_release


REPO_ROOT = Path(__file__).resolve().parents[1]
VERIFY_RELEASE = REPO_ROOT / "scripts" / "verify_release.py"


class TestVerifyReleaseCli(unittest.TestCase):
    def test_executable_bootstraps_the_repository_import_path(self):
        script = f"""
import runpy
import sys

repo_root = {str(REPO_ROOT)!r}
sys.path = [entry for entry in sys.path if entry != repo_root]
runpy.run_path({str(VERIFY_RELEASE)!r}, run_name="verify_release_contract_test")
raise SystemExit(0 if repo_root in sys.path else 29)
"""
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=REPO_ROOT.parent,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_full_dry_run_lists_every_owned_gate_without_claiming_host_proof(self):
        result = subprocess.run(
            [sys.executable, str(VERIFY_RELEASE), "full", "--dry-run"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        for step_name in (
            "repository hygiene",
            "working-tree diff check",
            "staged diff check",
            "world migration drift",
            "fresh database migration",
            "production deployment check",
            "smoke imports",
            "economy and inventory reconciliation",
            "canonical tests",
        ):
            self.assertIn(step_name, result.stdout.lower())
        self.assertNotIn("tls verified", result.stdout.lower())
        self.assertNotIn("systemd verified", result.stdout.lower())


class TestReleasePlan(unittest.TestCase):
    def test_full_plan_uses_the_canonical_commands(self):
        steps = verify_release.build_release_steps("full")
        commands = {step.name: step.command for step in steps}

        self.assertEqual(
            commands["World migration drift"],
            (
                sys.executable,
                "-m",
                "django",
                "makemigrations",
                "world",
                "--check",
                "--dry-run",
                "--settings=server.conf.settings",
            ),
        )
        self.assertEqual(
            commands["Fresh database migration"],
            (
                sys.executable,
                "-m",
                "django",
                "migrate",
                "--noinput",
                "--settings=server.conf.settings",
            ),
        )
        self.assertIn("--deploy", commands["Production deployment check"])
        self.assertIn("WARNING", commands["Production deployment check"])
        self.assertEqual(
            commands["Canonical tests"],
            (sys.executable, "scripts/run_tests.py"),
        )

    def test_four_shards_partition_every_canonical_test_module_once(self):
        labels = verify_release._discover_test_labels()
        shards = [
            verify_release._test_labels_for_shard(f"{index}/4")
            for index in range(1, 5)
        ]

        flattened = [label for shard in shards for label in shard]
        self.assertCountEqual(flattened, labels)
        self.assertEqual(len(flattened), len(set(flattened)))

    def test_execution_stops_at_the_first_failed_gate(self):
        steps = (
            verify_release.ReleaseStep("one", ("one",)),
            verify_release.ReleaseStep("two", ("two",)),
            verify_release.ReleaseStep("three", ("three",)),
        )
        results = [
            SimpleNamespace(returncode=0),
            SimpleNamespace(returncode=7),
        ]

        with patch("scripts.verify_release.subprocess.run", side_effect=results) as run:
            return_code = verify_release.execute_steps(steps)

        self.assertEqual(return_code, 7)
        self.assertEqual(run.call_count, 2)


class TestEconomyInventoryReconciliation(unittest.TestCase):
    def test_consistent_ledger_and_inventory_have_no_issues(self):
        issues = verify_release.find_reconciliation_issues(
            accounts=[SimpleNamespace(character_id=1, balance=5)],
            transactions=[
                SimpleNamespace(
                    id=10,
                    character_id=1,
                    amount=5,
                    balance_after=5,
                )
            ],
            inventory_items=[
                SimpleNamespace(
                    id=20,
                    character_id=1,
                    item_id=100,
                    quantity=1,
                    container_id=None,
                    is_equipped=True,
                    equipment_slot="head",
                )
            ],
            objects_by_id={100: SimpleNamespace(id=100, db_location_id=1)},
        )

        self.assertEqual(issues, [])

    def test_reconciliation_reports_ledger_and_ownership_contradictions(self):
        issues = verify_release.find_reconciliation_issues(
            accounts=[SimpleNamespace(character_id=1, balance=10)],
            transactions=[
                SimpleNamespace(
                    id=10,
                    character_id=1,
                    amount=5,
                    balance_after=5,
                ),
                SimpleNamespace(
                    id=11,
                    character_id=2,
                    amount=3,
                    balance_after=3,
                ),
            ],
            inventory_items=[
                SimpleNamespace(
                    id=20,
                    character_id=1,
                    item_id=100,
                    quantity=0,
                    container_id=200,
                    is_equipped=True,
                    equipment_slot=None,
                )
            ],
            objects_by_id={},
        )

        report = "\n".join(issues)
        self.assertIn("account character_id=1", report)
        self.assertIn("transaction id=11", report)
        self.assertIn("inventory id=20", report)
        self.assertNotIn("TOP_SECRET", report)


class TestReleaseWorkflowWiring(unittest.TestCase):
    def test_ci_uses_postgresql_and_the_executable_release_gate(self):
        workflow = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text()

        self.assertIn("postgres:16", workflow)
        self.assertIn("python scripts/verify_release.py preflight", workflow)
        self.assertIn("shard: [1, 2, 3, 4]", workflow)
        self.assertIn(
            "python scripts/verify_release.py full --shard ${{ matrix.shard }}/4",
            workflow,
        )
        self.assertNotIn(
            "python scripts/verify_release.py tests --shard ${{ matrix.shard }}/4",
            workflow,
        )
        self.assertIn("SORAVELON_ENV: production", workflow)
        self.assertNotIn("python scripts/smoke_start.py", workflow)
        self.assertNotIn("python scripts/run_tests.py", workflow)
