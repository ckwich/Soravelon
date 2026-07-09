"""Production settings ownership and secret-hygiene regression tests."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class TestProductionSecretOwnership(unittest.TestCase):
    def test_environment_secret_cannot_be_overridden_by_local_settings_module(self):
        """Production owns SECRET_KEY through the environment only."""
        script = """
import sys
import types

local_settings = types.ModuleType("server.conf.secret_settings")
local_settings.SECRET_KEY = "local-development-override"
sys.modules["server.conf.secret_settings"] = local_settings

from server.conf import settings

raise SystemExit(0 if settings.SECRET_KEY == "production-environment-key" else 23)
"""
        env = os.environ.copy()
        env.update(
            {
                "ALLOWED_HOSTS": "localhost,127.0.0.1",
                "DATABASE_ENGINE": "sqlite3",
                "DATABASE_NAME": "server/evennia.db3",
                "SECRET_KEY": "production-environment-key",
                "SORAVELON_ENV": "production",
            }
        )

        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unknown_environment_fails_closed(self):
        """Typos must not silently select development configuration."""
        env = os.environ.copy()
        env["SORAVELON_ENV"] = "prodution"

        result = subprocess.run(
            [sys.executable, "-c", "from server.conf import settings"],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unsupported SORAVELON_ENV", result.stderr)
