"""
Production overrides for Soravelon.

This file is imported from ``server/conf/settings.py`` when
``SORAVELON_ENV=production``. It is intentionally environment-driven so a clean
checkout can be deployed without editing tracked source files.
"""

from __future__ import annotations

import os
from pathlib import Path


GAME_DIR = Path(__file__).resolve().parents[2]


def _env(name: str, default=None, required: bool = False):
    value = os.environ.get(name, default)
    if required and (value is None or value == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _env_bool(name: str, default: bool = False) -> bool:
    value = str(_env(name, str(default))).strip().lower()
    return value in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    return int(_env(name, default))


SECRET_KEY = _env("SECRET_KEY", required=True)
DEBUG = _env_bool("DEBUG", False)
ALLOWED_HOSTS = [
    host.strip()
    for host in _env("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

SERVER_HOSTNAME = _env("SERVER_HOSTNAME", ALLOWED_HOSTS[0] if ALLOWED_HOSTS else "localhost")

TELNET_PORTS = [_env_int("TELNET_PORT", 4000)]
WEBSERVER_PORTS = [(SERVER_HOSTNAME, _env_int("WEBSERVER_PORT", 4001))]
SSH_PORTS = [_env_int("SSH_PORT", 4002)]
SSL_PORTS = [_env_int("SSL_PORT", 4003)]
WEBSOCKET_CLIENT_PORT = _env_int("WEBSOCKET_CLIENT_PORT", 4005)

LOG_DIR = _env("LOG_DIR", str(GAME_DIR / "server" / "logs"))

database_engine = _env("DATABASE_ENGINE", "postgresql").lower()
if database_engine in {"postgres", "postgresql", "psql"}:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": _env("DATABASE_NAME", required=True),
            "USER": _env("DATABASE_USER", required=True),
            "PASSWORD": _env("DATABASE_PASSWORD", required=True),
            "HOST": _env("DATABASE_HOST", "127.0.0.1"),
            "PORT": _env("DATABASE_PORT", "5432"),
        }
    }
elif database_engine == "sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(GAME_DIR / _env("DATABASE_NAME", "server/evennia.db3")),
        }
    }
else:
    raise RuntimeError(
        f"Unsupported DATABASE_ENGINE '{database_engine}'. Expected postgresql or sqlite3."
    )

CSRF_TRUSTED_ORIGINS = [
    f"http://{host}" for host in ALLOWED_HOSTS if host not in {"localhost", "127.0.0.1"}
] + [
    f"https://{host}" for host in ALLOWED_HOSTS if host not in {"localhost", "127.0.0.1"}
]

try:
    from server.conf.production_settings.local import *  # noqa: F403
except ImportError:
    pass
