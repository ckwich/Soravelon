"""Executable contracts for the production service topology."""

from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SERVICE_PATH = ROOT / "deploy" / "systemd" / "soravelon.service"


class TestSystemdService(unittest.TestCase):
    def test_systemd_sandboxes_the_network_service(self):
        service = SERVICE_PATH.read_text()

        required_directives = (
            "CapabilityBoundingSet=",
            "LockPersonality=true",
            "NoNewPrivileges=true",
            "PrivateDevices=true",
            "PrivateTmp=true",
            "ProtectClock=true",
            "ProtectControlGroups=true",
            "ProtectHome=true",
            "ProtectHostname=true",
            "ProtectKernelLogs=true",
            "ProtectKernelModules=true",
            "ProtectKernelTunables=true",
            "ProtectProc=invisible",
            "ProtectSystem=full",
            "RemoveIPC=true",
            "RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6",
            "RestrictNamespaces=true",
            "RestrictRealtime=true",
            "RestrictSUIDSGID=true",
            "SystemCallArchitectures=native",
            "UMask=0077",
        )
        for directive in required_directives:
            with self.subTest(directive=directive):
                self.assertIn(directive, service)

    def test_systemd_supervises_the_foreground_portal(self):
        service = SERVICE_PATH.read_text()

        self.assertIn("Type=simple", service)
        self.assertIn(
            "Environment=PATH=/srv/soravelon/.venv/bin:/usr/local/sbin:"
            "/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            service,
        )
        self.assertIn("ExecStart=/srv/soravelon/.venv/bin/evennia ipstart", service)
        self.assertNotIn("/evennia start", service)
        self.assertIn("KillMode=control-group", service)
        # Evennia's launcher does not propagate the Portal child's exit code,
        # so a crashed Portal can still make the foreground launcher exit 0.
        self.assertIn("Restart=always", service)

    def test_systemd_runs_fail_closed_prestart_and_journald_logging(self):
        service = SERVICE_PATH.read_text()

        self.assertIn(
            "ExecStartPre=/usr/bin/install -d -m 0750 "
            "/srv/soravelon/server/logs",
            service,
        )
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

    def test_runs_config_migration_bootstrap_smoke_and_collectstatic_checks_in_order(self):
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
                    str(ROOT / "scripts" / "verify_runtime_bootstrap.py"),
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


class TestRuntimeBootstrap(unittest.TestCase):
    def test_executable_bootstraps_the_repository_import_path(self):
        script = f"""
import runpy
import sys

repo_root = {str(ROOT)!r}
sys.path = [entry for entry in sys.path if entry != repo_root]
runpy.run_path(
    {str(ROOT / "scripts" / "verify_runtime_bootstrap.py")!r},
    run_name="runtime_bootstrap_contract_test",
)
raise SystemExit(0 if repo_root in sys.path else 29)
"""
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=ROOT.parent,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_accepts_initialized_admin_account_one(self):
        from scripts.verify_runtime_bootstrap import verify_runtime_bootstrap

        with patch(
            "scripts.verify_runtime_bootstrap._account_one_is_admin",
            return_value=True,
        ):
            self.assertEqual(verify_runtime_bootstrap(), 0)

    def test_rejects_database_without_initialized_admin_account_one(self):
        from scripts.verify_runtime_bootstrap import verify_runtime_bootstrap

        with patch(
            "scripts.verify_runtime_bootstrap._account_one_is_admin",
            return_value=False,
        ):
            self.assertEqual(verify_runtime_bootstrap(), 2)
