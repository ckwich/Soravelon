"""Fail closed before Evennia attempts interactive first-run setup."""

from __future__ import annotations

import os
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _account_one_is_admin() -> bool:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")

    import django

    django.setup()

    from evennia.accounts.models import AccountDB

    return AccountDB.objects.filter(id=1, is_superuser=True).exists()


def verify_runtime_bootstrap() -> int:
    if _account_one_is_admin():
        print("Runtime bootstrap passed: admin account #1 exists.")
        return 0

    print(
        "Runtime bootstrap FAILED: admin account #1 is missing or is not "
        "a superuser. Run 'python -m django createsuperuser' interactively "
        "before starting the service.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(verify_runtime_bootstrap())
