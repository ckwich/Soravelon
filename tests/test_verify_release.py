"""Executable release verification contract tests."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

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
            "git object integrity",
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

    def test_candidate_dry_run_requires_and_prints_exact_live_inputs(self):
        result = subprocess.run(
            [
                sys.executable,
                str(VERIFY_RELEASE),
                "candidate",
                "--dry-run",
                "--expected-database-name",
                "soravelon_rehearsal_candidate_1",
                "--test-database-name",
                "test_soravelon_rehearsal_candidate_1",
                "--git-commit",
                "a" * 40,
                "--protocol-host",
                "127.0.0.1",
                "--telnet-port",
                "4000",
                "--web-port",
                "4001",
                "--websocket-port",
                "4002",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--database-kind prepared", result.stdout)
        self.assertIn("soravelon_rehearsal_candidate_1", result.stdout)
        self.assertIn("--keepdb", result.stdout)
        self.assertIn("--reset-kept-db", result.stdout)
        self.assertIn("Authored content prose", result.stdout)
        self.assertIn("Live player protocols", result.stdout)

    def test_candidate_refuses_implicit_database_or_protocol_targets(self):
        result = subprocess.run(
            [sys.executable, str(VERIFY_RELEASE), "candidate", "--dry-run"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("candidate mode requires", result.stderr)


class TestReleasePlan(unittest.TestCase):
    def test_full_plan_uses_the_canonical_commands(self):
        steps = verify_release.build_release_steps("full")
        commands = {step.name: step.command for step in steps}

        self.assertEqual(
            commands["Git object integrity"],
            ("git", "fsck", "--full", "--no-reflogs"),
        )
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

    def test_candidate_plan_requires_exact_rehearsal_and_protocol_inputs(self):
        with self.assertRaisesRegex(ValueError, "candidate inputs"):
            verify_release.build_release_steps("candidate")

    def test_candidate_plan_names_every_mud_release_surface(self):
        candidate = verify_release.ReleaseCandidateInputs(
            expected_database_name="soravelon_rehearsal_candidate_1",
            test_database_name="test_soravelon_rehearsal_candidate_1",
            git_commit="a" * 40,
            protocol_host="127.0.0.1",
            telnet_port=4000,
            web_port=4001,
            websocket_port=4002,
        )

        steps = verify_release.build_release_steps(
            "candidate",
            candidate=candidate,
        )
        commands = {step.name: step.command for step in steps}

        self.assertEqual(steps[0].name, "Git object integrity")
        self.assertEqual(steps[1].name, "Prepared world-content verification")
        self.assertEqual(
            commands["Prepared world-content verification"],
            (
                sys.executable,
                "scripts/rehearse_content_release.py",
                "--database-kind",
                "prepared",
                "--expected-database-name",
                "soravelon_rehearsal_candidate_1",
                "--git-commit",
                "a" * 40,
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            commands["Playable world connectivity"],
            (sys.executable, "scripts/audit_world_connectivity.py"),
        )
        self.assertEqual(
            commands["Authored content prose"],
            (sys.executable, "scripts/audit_content_prose.py"),
        )
        verticals = commands["Release gameplay verticals"]
        for label in (
            "tests.test_m3_golden_path",
            "tests.test_m4_living_world_vertical",
            "tests.test_social_web_warden_route",
            "tests.test_cooperative_combat_vertical",
        ):
            self.assertIn(label, verticals)
        self.assertEqual(
            commands["Canonical tests"],
            (
                sys.executable,
                "scripts/run_tests.py",
                "--keepdb",
                "--reset-kept-db",
            ),
        )
        rollback = commands["Transactional failure injection"]
        self.assertIn("--keepdb", rollback)
        self.assertIn("--reset-kept-db", rollback)
        for label in (
            "tests.test_content_revisions.TestWorldContentApplyLifecycle.test_injected_failure_rolls_back_runtime_and_persists_failure",
            "tests.test_economy_transactions.TestAtomicCashAndBankOperations.test_deposit_rolls_back_after_every_write",
            "tests.test_inventory_transactions.TestAtomicPickup.test_pickup_rolls_back_location_and_ownership_after_every_write",
            "tests.test_quest_outcomes.TestAtomicQuestOutcomes.test_failure_after_outcome_writes_rolls_back_every_effect",
        ):
            self.assertIn(label, rollback)
        self.assertEqual(
            commands["Live player protocols"],
            (
                sys.executable,
                "scripts/smoke_protocols.py",
                "--host",
                "127.0.0.1",
                "--telnet-port",
                "4000",
                "--web-port",
                "4001",
                "--websocket-port",
                "4002",
                "--forwarded-https",
            ),
        )

    def test_candidate_plan_does_not_allow_test_sharding(self):
        candidate = verify_release.ReleaseCandidateInputs(
            expected_database_name="soravelon_rehearsal_restored_1",
            test_database_name="test_soravelon_rehearsal_restored_1",
            git_commit="a" * 40,
            protocol_host="127.0.0.1",
            telnet_port=4000,
            web_port=4001,
            websocket_port=4002,
        )

        with self.assertRaisesRegex(ValueError, "unsharded"):
            verify_release.build_release_steps(
                "candidate",
                shard="1/4",
                candidate=candidate,
            )

    def test_candidate_inputs_reject_normal_database_name_before_execution(self):
        with self.assertRaisesRegex(ValueError, "soravelon_rehearsal"):
            verify_release.ReleaseCandidateInputs(
                expected_database_name="soravelon",
                test_database_name="test_soravelon_rehearsal_candidate_1",
                git_commit="a" * 40,
                protocol_host="127.0.0.1",
                telnet_port=4000,
                web_port=4001,
                websocket_port=4002,
            )

    def test_candidate_inputs_reject_non_disposable_test_database_name(self):
        with self.assertRaisesRegex(ValueError, "test_soravelon_rehearsal"):
            verify_release.ReleaseCandidateInputs(
                expected_database_name="soravelon_rehearsal_candidate_1",
                test_database_name="soravelon",
                git_commit="a" * 40,
                protocol_host="127.0.0.1",
                telnet_port=4000,
                web_port=4001,
                websocket_port=4002,
            )


class TestCanonicalTestRunner(unittest.TestCase):
    def test_keepdb_is_a_runner_option_not_a_test_label(self):
        from scripts import run_tests

        with (
            patch("django.setup"),
            patch("django.core.management.call_command") as call_command,
        ):
            result = run_tests.main(["--keepdb", "tests.test_example"])

        self.assertEqual(result, 0)
        call_command.assert_called_once_with(
            "test",
            "tests.test_example",
            verbosity=1,
            keepdb=True,
        )

    def test_reset_kept_db_is_a_runner_option_and_runs_before_tests(self):
        from scripts import run_tests

        database = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "soravelon_rehearsal_candidate_1",
            "TEST": {"NAME": "test_soravelon_rehearsal_candidate_1"},
        }
        with (
            patch("django.setup"),
            patch("django.conf.settings", SimpleNamespace(DATABASES={"default": database})),
            patch("scripts.run_tests.reset_precreated_test_database") as reset,
            patch("scripts.run_tests.prepare_precreated_test_database") as prepare,
            patch("django.core.management.call_command") as call_command,
        ):
            result = run_tests.main(
                ["--keepdb", "--reset-kept-db", "tests.test_example"]
            )

        self.assertEqual(result, 0)
        reset.assert_called_once_with(database)
        prepare.assert_called_once_with(database, REPO_ROOT)
        call_command.assert_called_once_with(
            "test",
            "tests.test_example",
            verbosity=1,
            keepdb=True,
        )

    def test_reset_kept_db_requires_keepdb(self):
        from scripts import run_tests

        with self.assertRaises(SystemExit):
            run_tests.main(["--reset-kept-db", "tests.test_example"])


class TestPrecreatedTestDatabaseReset(unittest.TestCase):
    @staticmethod
    def _database(**overrides):
        database = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "soravelon_rehearsal_candidate_1",
            "USER": "soravelon",
            "PASSWORD": "secret",
            "HOST": "127.0.0.1",
            "PORT": "5432",
            "TEST": {"NAME": "test_soravelon_rehearsal_candidate_1"},
        }
        database.update(overrides)
        return database

    def test_valid_disposable_database_resets_public_schema(self):
        from scripts.run_tests import reset_precreated_test_database

        cursor = MagicMock()
        cursor.fetchone.return_value = ("test_soravelon_rehearsal_candidate_1",)
        connection = MagicMock()
        connection.__enter__.return_value.cursor.return_value.__enter__.return_value = (
            cursor
        )
        connect = MagicMock(return_value=connection)

        reset_precreated_test_database(self._database(), connect=connect)

        connect.assert_called_once_with(
            dbname="test_soravelon_rehearsal_candidate_1",
            user="soravelon",
            password="secret",
            host="127.0.0.1",
            port="5432",
            autocommit=True,
        )
        self.assertEqual(
            [call.args[0] for call in cursor.execute.call_args_list],
            [
                "SELECT current_database()",
                "DROP SCHEMA public CASCADE",
                "CREATE SCHEMA public",
            ],
        )

    def test_unsafe_names_refuse_before_connecting(self):
        from scripts.run_tests import reset_precreated_test_database

        cases = (
            self._database(NAME="soravelon"),
            self._database(TEST={"NAME": "soravelon"}),
        )
        for database in cases:
            with self.subTest(database=database):
                connect = MagicMock()
                with self.assertRaisesRegex(RuntimeError, "disposable"):
                    reset_precreated_test_database(database, connect=connect)
                connect.assert_not_called()

    def test_live_database_identity_mismatch_refuses_before_drop(self):
        from scripts.run_tests import reset_precreated_test_database

        cursor = MagicMock()
        cursor.fetchone.return_value = ("soravelon",)
        connection = MagicMock()
        connection.__enter__.return_value.cursor.return_value.__enter__.return_value = (
            cursor
        )

        with self.assertRaisesRegex(RuntimeError, "identity"):
            reset_precreated_test_database(
                self._database(),
                connect=MagicMock(return_value=connection),
            )

        self.assertEqual(
            [call.args[0] for call in cursor.execute.call_args_list],
            ["SELECT current_database()"],
        )


class TestPrecreatedTestDatabasePreparation(unittest.TestCase):
    def test_preparation_targets_only_explicit_test_database(self):
        from scripts.run_tests import prepare_precreated_test_database

        database = {
            "NAME": "soravelon_rehearsal_candidate_1",
            "TEST": {"NAME": "test_soravelon_rehearsal_candidate_1"},
        }
        run = MagicMock()

        prepare_precreated_test_database(
            database,
            Path("/srv/soravelon"),
            run=run,
            environ={
                "DATABASE_NAME": "soravelon_rehearsal_candidate_1",
                "DATABASE_TEST_NAME": "test_soravelon_rehearsal_candidate_1",
                "SECRET_KEY": "preserved",
            },
        )

        run.assert_called_once()
        command = run.call_args.args[0]
        self.assertEqual(
            command,
            [
                sys.executable,
                "scripts/prepare_candidate_test_database.py",
                "--expected-database-name",
                "test_soravelon_rehearsal_candidate_1",
            ],
        )
        self.assertEqual(run.call_args.kwargs["cwd"], Path("/srv/soravelon"))
        self.assertTrue(run.call_args.kwargs["check"])
        child_env = run.call_args.kwargs["env"]
        self.assertEqual(
            child_env["DATABASE_NAME"],
            "test_soravelon_rehearsal_candidate_1",
        )
        self.assertNotIn("DATABASE_TEST_NAME", child_env)
        self.assertEqual(child_env["SECRET_KEY"], "preserved")


class TestCandidateTestDatabaseFoundation(unittest.TestCase):
    def test_database_identity_must_be_explicit_and_disposable(self):
        from scripts.prepare_candidate_test_database import require_candidate_database

        database = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "test_soravelon_rehearsal_candidate_1",
        }

        require_candidate_database(
            database,
            expected_name="test_soravelon_rehearsal_candidate_1",
            actual_name="test_soravelon_rehearsal_candidate_1",
        )
        for changed in (
            {**database, "NAME": "soravelon"},
            {**database, "ENGINE": "django.db.backends.sqlite3"},
        ):
            with self.subTest(database=changed):
                with self.assertRaisesRegex(RuntimeError, "disposable PostgreSQL"):
                    require_candidate_database(
                        changed,
                        expected_name="test_soravelon_rehearsal_candidate_1",
                        actual_name="test_soravelon_rehearsal_candidate_1",
                    )
        with self.assertRaisesRegex(RuntimeError, "live database identity"):
            require_candidate_database(
                database,
                expected_name="test_soravelon_rehearsal_candidate_1",
                actual_name="soravelon",
            )

    def test_seed_creates_unusable_admin_and_evennia_objects(self):
        from scripts.prepare_candidate_test_database import seed_evennia_foundation

        account = SimpleNamespace(
            pk=1,
            is_superuser=True,
            is_staff=True,
            has_usable_password=MagicMock(return_value=False),
        )
        account_model = SimpleNamespace(objects=MagicMock())
        account_model.objects.exists.return_value = False
        account_model.objects.create_superuser.return_value = account
        object_model = SimpleNamespace(objects=MagicMock())
        object_model.objects.filter.return_value.count.return_value = 2
        initialize = MagicMock()

        seed_evennia_foundation(
            account_model=account_model,
            object_model=object_model,
            initialize=initialize,
        )

        account_model.objects.create_superuser.assert_called_once_with(
            username="CandidateTestAdmin",
            email="candidate-test-admin@example.invalid",
            password=None,
        )
        initialize.assert_called_once_with()
        object_model.objects.filter.assert_called_once_with(pk__in=(1, 2))

    def test_seed_refuses_nonempty_database_before_creating_account(self):
        from scripts.prepare_candidate_test_database import seed_evennia_foundation

        account_model = SimpleNamespace(objects=MagicMock())
        account_model.objects.exists.return_value = True

        with self.assertRaisesRegex(RuntimeError, "empty account table"):
            seed_evennia_foundation(
                account_model=account_model,
                object_model=SimpleNamespace(objects=MagicMock()),
                initialize=MagicMock(),
            )

        account_model.objects.create_superuser.assert_not_called()


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
