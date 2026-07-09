"""Stable identity helpers for exactly-once economy operations."""

from __future__ import annotations

import uuid


def new_operation_id() -> str:
    """Return an opaque operation identifier suitable for durable uniqueness."""

    return uuid.uuid4().hex
