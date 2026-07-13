#!/usr/bin/env python3
"""Audit playable world reachability from the authored fresh start."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from world.connectivity_audit import audit_world_connectivity
from world.content_compiler import compile_world_manifest


def main() -> int:
    compilation = compile_world_manifest(ROOT / "world" / "areas")
    if compilation.manifest is None:
        for diagnostic in compilation.diagnostics:
            print(f"{diagnostic.code}: {diagnostic.message}")
        return 1

    audit = audit_world_connectivity(compilation.manifest)
    if audit.passed:
        print(
            f"World connectivity passed: {len(audit.reachable_rooms)} rooms "
            f"reachable from {audit.start_room}."
        )
        return 0

    print(f"World connectivity failed from {audit.start_room}:")
    for diagnostic in audit.diagnostics:
        print(f"- {diagnostic.code} [{diagnostic.entity_id}]: {diagnostic.message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
