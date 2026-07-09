"""Production settings ownership and secret-hygiene regression tests."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

PRODUCTION_ENV_KEYS = {
    "ALLOWED_HOSTS",
    "CSRF_TRUSTED_ORIGINS",
    "DATABASE_ENGINE",
    "DATABASE_HOST",
    "DATABASE_NAME",
    "DATABASE_PASSWORD",
    "DATABASE_PORT",
    "DATABASE_USER",
    "DEBUG",
    "SECRET_KEY",
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    "SECURE_HSTS_PRELOAD",
    "SECURE_HSTS_SECONDS",
    "SERVER_HOSTNAME",
    "SORAVELON_ENV",
    "SSH_ENABLED",
    "SSH_PORT",
    "SSL_ENABLED",
    "SSL_PORT",
    "TELNET_ENABLED",
    "TELNET_PORT",
    "WEBSERVER_INTERNAL_PORT",
    "WEBSERVER_PORT",
    "WEBSOCKET_CLIENT_PORT",
}


def _valid_production_env() -> dict[str, str]:
    env = os.environ.copy()
    for name in PRODUCTION_ENV_KEYS:
        env.pop(name, None)
    env.update(
        {
            "ALLOWED_HOSTS": "game.example.test,admin.example.test",
            "CSRF_TRUSTED_ORIGINS": (
                "https://game.example.test,https://admin.example.test"
            ),
            "DATABASE_ENGINE": "postgresql",
            "DATABASE_HOST": "127.0.0.1",
            "DATABASE_NAME": "soravelon_test",
            "DATABASE_PASSWORD": "database-test-password",
            "DATABASE_PORT": "5432",
            "DATABASE_USER": "soravelon_test",
            "SECRET_KEY": (
                "soravelon-production-test-key-"
                "0123456789-ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ),
            "SORAVELON_ENV": "production",
        }
    )
    return env


def _run_production_import(
    *,
    overrides: dict[str, str] | None = None,
    missing: tuple[str, ...] = (),
    preamble: str = "",
    probe: str = "",
) -> subprocess.CompletedProcess[str]:
    env = _valid_production_env()
    env.update(overrides or {})
    for name in missing:
        env.pop(name, None)
    script = (
        preamble
        + "\nfrom server.conf import production_settings as settings\n"
        + probe
    )
    return subprocess.run(
        [sys.executable, "-c", script],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


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

raise SystemExit(
    0
    if settings.SECRET_KEY
    == "production-environment-key-0123456789-abcdefghijklmno"
    else 23
)
"""
        env = _valid_production_env()
        env["SECRET_KEY"] = (
            "production-environment-key-0123456789-abcdefghijklmno"
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


class TestProductionEnvironmentValidation(unittest.TestCase):
    def test_unsafe_or_implicit_production_configuration_fails_closed(self):
        cases = (
            (
                "placeholder secret",
                {"SECRET_KEY": "replace-me-for-production"},
                (),
                "SECRET_KEY",
            ),
            ("implicit allowed hosts", {}, ("ALLOWED_HOSTS",), "ALLOWED_HOSTS"),
            (
                "implicit csrf origins",
                {},
                ("CSRF_TRUSTED_ORIGINS",),
                "CSRF_TRUSTED_ORIGINS",
            ),
            (
                "insecure csrf origin",
                {"CSRF_TRUSTED_ORIGINS": "http://game.example.test"},
                (),
                "HTTPS",
            ),
            (
                "sqlite production database",
                {"DATABASE_ENGINE": "sqlite3"},
                (),
                "PostgreSQL",
            ),
            (
                "placeholder database password",
                {"DATABASE_PASSWORD": "replace-me"},
                (),
                "DATABASE_PASSWORD",
            ),
            (
                "debug enabled",
                {"DEBUG": "true"},
                (),
                "DEBUG",
            ),
            (
                "wildcard allowed host",
                {"ALLOWED_HOSTS": "*"},
                (),
                "wildcard",
            ),
        )

        for label, overrides, missing, expected_error in cases:
            with self.subTest(label=label):
                result = _run_production_import(
                    overrides=overrides,
                    missing=missing,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected_error, result.stderr)


class TestProductionDjangoSecuritySurface(unittest.TestCase):
    def test_secure_web_policy_is_complete_and_cannot_be_locally_overridden(self):
        result = _run_production_import(
            preamble="""
import sys
import types

local_settings = types.ModuleType("server.conf.production_settings.local")
local_settings.DEBUG = True
local_settings.SESSION_COOKIE_SECURE = False
sys.modules["server.conf.production_settings.local"] = local_settings
""",
            probe="""
import json

print(json.dumps({
    "csrf_cookie_secure": settings.CSRF_COOKIE_SECURE,
    "debug": settings.DEBUG,
    "frame_options": settings.X_FRAME_OPTIONS,
    "hsts_include_subdomains": settings.SECURE_HSTS_INCLUDE_SUBDOMAINS,
    "hsts_preload": settings.SECURE_HSTS_PRELOAD,
    "hsts_seconds": settings.SECURE_HSTS_SECONDS,
    "middleware": settings.MIDDLEWARE,
    "proxy_ssl_header": settings.SECURE_PROXY_SSL_HEADER,
    "referrer_policy": settings.SECURE_REFERRER_POLICY,
    "secure_content_type_nosniff": settings.SECURE_CONTENT_TYPE_NOSNIFF,
    "secure_ssl_redirect": settings.SECURE_SSL_REDIRECT,
    "session_cookie_secure": settings.SESSION_COOKIE_SECURE,
}))
""",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        policy = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertFalse(policy["debug"])
        self.assertEqual(
            policy["middleware"][0],
            "django.middleware.security.SecurityMiddleware",
        )
        self.assertIn(
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
            policy["middleware"],
        )
        self.assertEqual(
            policy["proxy_ssl_header"],
            ["HTTP_X_FORWARDED_PROTO", "https"],
        )
        self.assertTrue(policy["session_cookie_secure"])
        self.assertTrue(policy["csrf_cookie_secure"])
        self.assertTrue(policy["secure_ssl_redirect"])
        self.assertTrue(policy["secure_content_type_nosniff"])
        self.assertEqual(
            policy["referrer_policy"],
            "strict-origin-when-cross-origin",
        )
        self.assertEqual(policy["frame_options"], "DENY")
        self.assertEqual(policy["hsts_seconds"], 3600)
        self.assertTrue(policy["hsts_include_subdomains"])
        self.assertTrue(policy["hsts_preload"])


class TestProductionListenerConfiguration(unittest.TestCase):
    def test_environment_example_matches_safe_production_defaults(self):
        values = {}
        for raw_line in (REPO_ROOT / ".env.example").read_text().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            values[key] = value

        self.assertEqual(values["SORAVELON_ENV"], "production")
        self.assertTrue(values["ALLOWED_HOSTS"])
        self.assertTrue(values["CSRF_TRUSTED_ORIGINS"].startswith("https://"))
        self.assertEqual(values["DATABASE_ENGINE"], "postgresql")
        self.assertEqual(values["TELNET_ENABLED"], "false")
        self.assertEqual(values["SSH_ENABLED"], "false")
        self.assertEqual(values["SSL_ENABLED"], "false")
        self.assertEqual(values["TELNET_PORT"], "4000")
        self.assertEqual(values["WEBSERVER_PORT"], "4001")
        self.assertEqual(values["WEBSOCKET_CLIENT_PORT"], "4002")
        self.assertEqual(values["SSL_PORT"], "4003")
        self.assertEqual(values["SSH_PORT"], "4004")
        self.assertEqual(values["WEBSERVER_INTERNAL_PORT"], "4005")

    def test_standard_ports_disable_optional_listeners_by_default(self):
        result = _run_production_import(
            probe="""
import json

print(json.dumps({
    "telnet_enabled": settings.TELNET_ENABLED,
    "ssh_enabled": settings.SSH_ENABLED,
    "ssh_ports": settings.SSH_PORTS,
    "ssl_enabled": settings.SSL_ENABLED,
    "ssl_ports": settings.SSL_PORTS,
    "telnet_ports": settings.TELNET_PORTS,
    "webserver_internal_port": settings.WEBSERVER_INTERNAL_PORT,
    "webserver_ports": settings.WEBSERVER_PORTS,
    "websocket_client_port": settings.WEBSOCKET_CLIENT_PORT,
}))
"""
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        listeners = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertFalse(listeners["telnet_enabled"])
        self.assertEqual(listeners["telnet_ports"], [])
        self.assertEqual(listeners["webserver_ports"], [[4001, 4005]])
        self.assertEqual(listeners["webserver_internal_port"], 4005)
        self.assertEqual(listeners["websocket_client_port"], 4002)
        self.assertFalse(listeners["ssh_enabled"])
        self.assertEqual(listeners["ssh_ports"], [])
        self.assertFalse(listeners["ssl_enabled"])
        self.assertEqual(listeners["ssl_ports"], [])

    def test_enabled_optional_listeners_use_their_standard_ports(self):
        result = _run_production_import(
            overrides={"SSH_ENABLED": "true", "SSL_ENABLED": "true"},
            probe="""
import json

print(json.dumps({
    "ssh_enabled": settings.SSH_ENABLED,
    "ssh_ports": settings.SSH_PORTS,
    "ssl_enabled": settings.SSL_ENABLED,
    "ssl_ports": settings.SSL_PORTS,
}))
""",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        listeners = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertTrue(listeners["ssh_enabled"])
        self.assertEqual(listeners["ssh_ports"], [4004])
        self.assertTrue(listeners["ssl_enabled"])
        self.assertEqual(listeners["ssl_ports"], [4003])

    def test_enabled_listener_port_collisions_fail_closed(self):
        cases = (
            (
                "always-enabled listeners",
                {"WEBSOCKET_CLIENT_PORT": "4005"},
            ),
            (
                "enabled ssh listener",
                {"SSH_ENABLED": "true", "SSH_PORT": "4002"},
            ),
            (
                "enabled ssl listener",
                {"SSL_ENABLED": "true", "SSL_PORT": "4001"},
            ),
        )

        for label, overrides in cases:
            with self.subTest(label=label):
                result = _run_production_import(overrides=overrides)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("unique", result.stderr.lower())

    def test_disabled_optional_listener_port_does_not_claim_the_port(self):
        result = _run_production_import(
            overrides={"SSH_ENABLED": "false", "SSH_PORT": "4002"},
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_disabled_telnet_port_does_not_claim_the_port(self):
        result = _run_production_import(
            overrides={"TELNET_ENABLED": "false", "WEBSOCKET_CLIENT_PORT": "4000"},
        )

        self.assertEqual(result.returncode, 0, result.stderr)
