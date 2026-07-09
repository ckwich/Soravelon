"""Executable contracts for the production service topology."""

from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SERVICE_PATH = ROOT / "deploy" / "systemd" / "soravelon.service"


class TestSystemdService(unittest.TestCase):
    def test_systemd_supervises_the_foreground_portal(self):
        service = SERVICE_PATH.read_text()

        self.assertIn("Type=simple", service)
        self.assertIn("ExecStart=/srv/soravelon/.venv/bin/evennia ipstart", service)
        self.assertNotIn("/evennia start", service)
        self.assertIn("KillMode=control-group", service)
        # Evennia's launcher does not propagate the Portal child's exit code,
        # so a crashed Portal can still make the foreground launcher exit 0.
        self.assertIn("Restart=always", service)

    def test_systemd_runs_fail_closed_prestart_and_journald_logging(self):
        service = SERVICE_PATH.read_text()

        self.assertIn(
            "ExecStartPre=/srv/soravelon/.venv/bin/python "
            "scripts/verify_service_prestart.py",
            service,
        )
        self.assertIn("ExecStop=/srv/soravelon/.venv/bin/evennia stop", service)
        self.assertIn("ExecReload=/srv/soravelon/.venv/bin/evennia reload", service)
        self.assertIn("StandardOutput=journal", service)
        self.assertIn("StandardError=journal", service)


class TestServicePrestart(unittest.TestCase):
    def test_rejects_a_nonproduction_environment(self):
        from scripts.verify_service_prestart import run_prestart

        with patch.dict("os.environ", {"SORAVELON_ENV": "development"}, clear=True):
            self.assertEqual(run_prestart(), 2)

    def test_runs_config_migration_smoke_and_collectstatic_checks_in_order(self):
        from scripts.verify_service_prestart import run_prestart

        completed = subprocess.CompletedProcess(args=[], returncode=0)
        with patch.dict(
            "os.environ",
            {
                "SORAVELON_ENV": "production",
                "DJANGO_SETTINGS_MODULE": "server.conf.settings",
            },
            clear=True,
        ), patch(
            "scripts.verify_service_prestart.subprocess.run",
            return_value=completed,
        ) as mock_run:
            result = run_prestart(python="/venv/bin/python")

        self.assertEqual(result, 0)
        commands = [call.args[0] for call in mock_run.call_args_list]
        self.assertEqual(
            commands,
            [
                (
                    "/venv/bin/python",
                    "-m",
                    "django",
                    "check",
                    "--deploy",
                    "--fail-level",
                    "WARNING",
                ),
                (
                    "/venv/bin/python",
                    "-m",
                    "django",
                    "migrate",
                    "--check",
                ),
                (
                    "/venv/bin/python",
                    str(ROOT / "scripts" / "smoke_start.py"),
                ),
                (
                    "/venv/bin/python",
                    "-m",
                    "django",
                    "collectstatic",
                    "--noinput",
                ),
            ],
        )

    def test_stops_at_the_first_failed_gate(self):
        from scripts.verify_service_prestart import run_prestart

        failure = subprocess.CompletedProcess(args=[], returncode=7)
        with patch.dict(
            "os.environ",
            {
                "SORAVELON_ENV": "production",
                "DJANGO_SETTINGS_MODULE": "server.conf.settings",
            },
            clear=True,
        ), patch(
            "scripts.verify_service_prestart.subprocess.run",
            return_value=failure,
        ) as mock_run:
            result = run_prestart(python="/venv/bin/python")

        self.assertEqual(result, 7)
        mock_run.assert_called_once()
