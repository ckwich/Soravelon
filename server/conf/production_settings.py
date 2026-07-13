"""
Production overrides for Soravelon.

This file is imported from ``server/conf/settings.py`` when
``SORAVELON_ENV=production``. It is intentionally environment-driven so a clean
checkout can be deployed without editing tracked source files.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
from urllib.parse import urlsplit

from evennia.settings_default import MIDDLEWARE as EVENNIA_MIDDLEWARE


GAME_DIR = Path(__file__).resolve().parents[2]


def _env(name: str, default=None, required: bool = False):
    value = os.environ.get(name, default)
    if required and (value is None or value == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _env_bool(name: str, default: bool = False) -> bool:
    value = str(_env(name, str(default))).strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    raise RuntimeError(
        f"Environment variable {name} must be a boolean value; got '{value}'."
    )


def _env_int(name: str, default: int) -> int:
    return int(_env(name, default))


def _env_port(name: str, default: int) -> int:
    try:
        value = _env_int(name, default)
    except (TypeError, ValueError) as exc:
        raise RuntimeError(
            f"Environment variable {name} must be an integer port."
        ) from exc
    if not 1 <= value <= 65535:
        raise RuntimeError(
            f"Environment variable {name} must be between 1 and 65535."
        )
    return value


def _env_list(name: str, *, required: bool = False) -> list[str]:
    value = _env(name, required=required)
    items = [item.strip() for item in str(value or "").split(",") if item.strip()]
    if required and not items:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return items


def _production_secret_key() -> str:
    value = str(_env("SECRET_KEY", required=True)).strip()
    normalized = value.lower()
    placeholders = {
        "change-me",
        "changeme",
        "replace-me",
        "replace-me-for-local-dev",
        "replace-me-for-production",
        "test-secret",
        "your-secret-key",
    }
    if (
        len(value) < 50
        or len(set(value)) < 5
        or normalized in placeholders
        or normalized.startswith("django-insecure-")
    ):
        raise RuntimeError(
            "SECRET_KEY must be a non-placeholder value with at least "
            "50 characters and 5 unique characters."
        )
    return value


def _production_database_password() -> str:
    value = str(_env("DATABASE_PASSWORD", required=True)).strip()
    if value.lower() in {
        "change-me",
        "changeme",
        "replace-me",
        "password",
        "your-password",
    }:
        raise RuntimeError("DATABASE_PASSWORD must not be a placeholder value.")
    return value


SECRET_KEY = _production_secret_key()
DEBUG = _env_bool("DEBUG", False)
if DEBUG:
    raise RuntimeError("DEBUG must remain false in production.")
ALLOWED_HOSTS = _env_list("ALLOWED_HOSTS", required=True)
if "*" in ALLOWED_HOSTS:
    raise RuntimeError("ALLOWED_HOSTS may not use a wildcard in production.")
if any(
    "://" in host
    or "@" in host
    or "/" in host
    or "?" in host
    or "#" in host
    or any(character.isspace() for character in host)
    for host in ALLOWED_HOSTS
):
    raise RuntimeError(
        "ALLOWED_HOSTS must contain host names, not URLs or credentials."
    )
CSRF_TRUSTED_ORIGINS = _env_list("CSRF_TRUSTED_ORIGINS", required=True)


def _is_absolute_https_origin(origin: str) -> bool:
    try:
        parsed = urlsplit(origin)
        parsed.port
    except ValueError:
        return False
    return all(
        (
            parsed.scheme == "https",
            parsed.hostname is not None,
            parsed.username is None,
            parsed.password is None,
            parsed.path in {"", "/"},
            not parsed.query,
            not parsed.fragment,
        )
    )


if any(not _is_absolute_https_origin(origin) for origin in CSRF_TRUSTED_ORIGINS):
    raise RuntimeError(
        "CSRF_TRUSTED_ORIGINS must contain only absolute HTTPS origins."
    )

SECURITY_MIDDLEWARE = "django.middleware.security.SecurityMiddleware"
XFRAME_MIDDLEWARE = "django.middleware.clickjacking.XFrameOptionsMiddleware"
MIDDLEWARE = [
    SECURITY_MIDDLEWARE,
    *(
        middleware
        for middleware in EVENNIA_MIDDLEWARE
        if middleware not in {SECURITY_MIDDLEWARE, XFRAME_MIDDLEWARE}
    ),
    XFRAME_MIDDLEWARE,
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_HSTS_SECONDS = _env_int("SECURE_HSTS_SECONDS", 3600)
if SECURE_HSTS_SECONDS < 1:
    raise RuntimeError("SECURE_HSTS_SECONDS must be at least 1 in production.")
SECURE_HSTS_INCLUDE_SUBDOMAINS = _env_bool(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    True,
)
SECURE_HSTS_PRELOAD = _env_bool("SECURE_HSTS_PRELOAD", True)
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Lax"
X_FRAME_OPTIONS = "DENY"

SERVER_HOSTNAME = _env("SERVER_HOSTNAME", ALLOWED_HOSTS[0] if ALLOWED_HOSTS else "localhost")

TELNET_PORT = _env_port("TELNET_PORT", 4000)
WEBSERVER_PORT = _env_port("WEBSERVER_PORT", 4001)
WEBSOCKET_CLIENT_PORT = _env_port("WEBSOCKET_CLIENT_PORT", 4002)
SSL_PORT = _env_port("SSL_PORT", 4003)
SSH_PORT = _env_port("SSH_PORT", 4004)
WEBSERVER_INTERNAL_PORT = _env_port("WEBSERVER_INTERNAL_PORT", 4005)

SSH_ENABLED = _env_bool("SSH_ENABLED", False)
SSL_ENABLED = _env_bool("SSL_ENABLED", False)
TELNET_ENABLED = _env_bool("TELNET_ENABLED", False)

TELNET_PORTS = [TELNET_PORT] if TELNET_ENABLED else []
WEBSERVER_PORTS = [(WEBSERVER_PORT, WEBSERVER_INTERNAL_PORT)]
SSH_PORTS = [SSH_PORT] if SSH_ENABLED else []
SSL_PORTS = [SSL_PORT] if SSL_ENABLED else []

enabled_listener_ports = {
    "WEBSERVER_PORT": WEBSERVER_PORT,
    "WEBSOCKET_CLIENT_PORT": WEBSOCKET_CLIENT_PORT,
    "WEBSERVER_INTERNAL_PORT": WEBSERVER_INTERNAL_PORT,
}
if TELNET_ENABLED:
    enabled_listener_ports["TELNET_PORT"] = TELNET_PORT
if SSH_ENABLED:
    enabled_listener_ports["SSH_PORT"] = SSH_PORT
if SSL_ENABLED:
    enabled_listener_ports["SSL_PORT"] = SSL_PORT

port_owners: dict[int, list[str]] = {}
for listener_name, port in enabled_listener_ports.items():
    port_owners.setdefault(port, []).append(listener_name)
port_collisions = {
    port: owners for port, owners in port_owners.items() if len(owners) > 1
}
if port_collisions:
    collision_text = "; ".join(
        f"{port}: {', '.join(owners)}"
        for port, owners in sorted(port_collisions.items())
    )
    raise RuntimeError(
        f"Enabled listener ports must be unique; collisions: {collision_text}."
    )

LOG_DIR = _env("LOG_DIR", str(GAME_DIR / "server" / "logs"))

database_engine = _env("DATABASE_ENGINE", "postgresql").lower()
if database_engine not in {"postgres", "postgresql", "psql"}:
    raise RuntimeError(
        f"Production requires PostgreSQL; got DATABASE_ENGINE '{database_engine}'."
    )

database_name = _env("DATABASE_NAME", required=True)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": database_name,
        "USER": _env("DATABASE_USER", required=True),
        "PASSWORD": _production_database_password(),
        "HOST": _env("DATABASE_HOST", "127.0.0.1"),
        "PORT": str(_env_port("DATABASE_PORT", 5432)),
    }
}

test_database_name = str(_env("DATABASE_TEST_NAME", "") or "").strip()
if test_database_name:
    if re.fullmatch(
        r"soravelon_rehearsal_[a-z0-9][a-z0-9_]*",
        str(database_name),
    ) is None:
        raise RuntimeError(
            "DATABASE_TEST_NAME is allowed only with a disposable "
            "soravelon_rehearsal_* database."
        )
    if (
        re.fullmatch(
            r"test_soravelon_rehearsal_[a-z0-9][a-z0-9_]*",
            test_database_name,
        )
        is None
        or len(test_database_name) > 63
    ):
        raise RuntimeError(
            "DATABASE_TEST_NAME must use the "
            "test_soravelon_rehearsal_* disposable naming contract."
        )
    DATABASES["default"]["TEST"] = {"NAME": test_database_name}
