"""Fail-closed settings for an isolated local protocol playtest server."""

from __future__ import annotations

import os
from pathlib import Path

from .settings import *  # noqa: F403


def _required_absolute_path(name: str) -> Path:
    raw_value = os.environ.get(name, "").strip()
    if not raw_value:
        raise RuntimeError(f"{name} is required for isolated playtest settings.")
    path = Path(raw_value).expanduser()
    if not path.is_absolute():
        raise RuntimeError(f"{name} must be an absolute path.")
    return path


def _playtest_port_base() -> int:
    raw_value = os.environ.get("SORAVELON_PLAYTEST_PORT_BASE", "").strip()
    if not raw_value:
        raise RuntimeError(
            "SORAVELON_PLAYTEST_PORT_BASE is required for isolated playtest settings."
        )
    try:
        port = int(raw_value)
    except ValueError as exc:
        raise RuntimeError(
            "SORAVELON_PLAYTEST_PORT_BASE must be an integer."
        ) from exc
    if not 1024 <= port <= 65528:
        raise RuntimeError(
            "SORAVELON_PLAYTEST_PORT_BASE must leave ports BASE through BASE+7 "
            "inside the unprivileged TCP range."
        )
    return port


_database_path = _required_absolute_path("SORAVELON_PLAYTEST_DATABASE")
_log_dir = _required_absolute_path("SORAVELON_PLAYTEST_LOG_DIR")
_port_base = _playtest_port_base()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(_database_path),
    }
}

TELNET_ENABLED = True
TELNET_PORTS = [_port_base]
TELNET_INTERFACES = ["127.0.0.1"]

WEBSERVER_PORTS = [(_port_base + 1, _port_base + 5)]
WEBSERVER_INTERFACES = ["127.0.0.1"]
WEBSOCKET_CLIENT_PORT = _port_base + 2
WEBSOCKET_CLIENT_INTERFACE = "127.0.0.1"

AMP_PORT = _port_base + 6
AMP_INTERFACE = "127.0.0.1"

SSH_ENABLED = False
SSL_ENABLED = False

SERVER_LOG_FILE = str(_log_dir / "server.log")
PORTAL_LOG_FILE = str(_log_dir / "portal.log")
HTTP_LOG_FILE = str(_log_dir / "http.log")
LOG_DIR = str(_log_dir)
LOCKWARNING_LOG_FILE = str(_log_dir / "lockwarnings.log")
