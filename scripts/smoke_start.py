"""
Low-cost startup smoke check.

This validates that the game settings import, Django boots, and the authored
help entries / area modules are importable before attempting a real server
boot on staging or production.
"""

from __future__ import annotations

import importlib
import os
from pathlib import Path
import pkgutil
import sys


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")

    import django

    django.setup()

    settings = importlib.import_module("server.conf.settings")
    for module_name in getattr(settings, "FILE_HELP_ENTRY_MODULES", []):
        importlib.import_module(module_name)

    areas_pkg = importlib.import_module("world.areas")
    for module in pkgutil.iter_modules(areas_pkg.__path__):
        if module.name.startswith("_"):
            continue
        importlib.import_module(f"world.areas.{module.name}")

    print("Soravelon smoke imports passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
