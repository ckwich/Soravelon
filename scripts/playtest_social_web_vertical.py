#!/usr/bin/env python3
"""Verify the live Vael's Crossing Social Web vertical."""

from __future__ import annotations

import argparse
import os
import pathlib
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")


def _verify_live_runtime():
    import django

    django.setup()
    from world.social_playtest_verification import verify_social_web_runtime

    return verify_social_web_runtime()


def main(argv=None, *, verify_runtime=None):
    """Run the explicit live-runtime verification gate."""
    parser = argparse.ArgumentParser(
        description="Verify the live Vael's Crossing Social Web vertical."
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="check migrations, topology, exits, edge policy, and route state",
    )
    args = parser.parse_args(argv)
    if not args.verify:
        parser.error("--verify is required; this script no longer prints a fake route.")

    from world.social_playtest_verification import SocialWebRuntimeVerificationError

    try:
        checks = (verify_runtime or _verify_live_runtime)()
    except SocialWebRuntimeVerificationError as exc:
        print(f"FAIL {exc}")
        return 1
    for check, detail in checks.items():
        print(f"PASS {check}: {detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
