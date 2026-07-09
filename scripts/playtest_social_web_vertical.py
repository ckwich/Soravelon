#!/usr/bin/env python3
"""Print the Vael's Crossing Social Web vertical playtest route."""

from __future__ import annotations

import os
import pathlib
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")


def _renderer_fallback_line():
    from world.social_llm_renderer import render_social_quest_offer
    from world.social_quest_offers import get_social_quest_spec_by_id

    spec = get_social_quest_spec_by_id("vc_sq_under_seal_dustwalkers_rest")
    rendered = render_social_quest_offer(spec)
    mode = "renderer fallback" if rendered["fallback_used"] else "provider"
    return f"{mode}: {rendered['speech'][:120]}"


def build_playtest_beats():
    """Return deterministic human-readable beats for the vertical route."""
    return [
        {
            "title": "Warden report completion",
            "commands": [
                "talk Agent Calloway",
                "accept",
                "talk Commander Harven",
            ],
            "expected": (
                "The authored Warden report path completes, pays its rewards, "
                "and records Social Web fact/claim state for Calloway and Harven."
            ),
        },
        {
            "title": "Calloway explanation",
            "commands": [
                "talk Agent Calloway",
                "ask Agent Calloway why",
                "ask Agent Calloway about me",
            ],
            "expected": (
                "Calloway explains the supported Warden route without exposing "
                "raw fact keys, claim keys, confidence, or hidden trace internals."
            ),
        },
        {
            "title": "Harven cross-zone knowledge",
            "commands": [
                "travel to Ashreach Outpost",
                "talk Commander Harven",
                "ask Commander Harven about me",
            ],
            "expected": (
                "Harven knows only what a real Warden-report edge carried across "
                "zones, with Warden institutional framing."
            ),
        },
        {
            "title": "Whistle local rumor knowledge",
            "commands": [
                "talk Whistle",
                "ask Whistle about me",
                "trigger the inn-traveler rumor route",
                "ask Whistle about me",
            ],
            "expected": (
                "Whistle starts ignorant of sealed Warden details, then can speak "
                "only to the local rumor or traveler route after propagation."
            ),
        },
        {
            "title": "dynamic social quest lifecycle",
            "commands": [
                "talk Agent Calloway",
                "accept",
                "talk Whistle",
                "look",
                "talk Raith",
                "talk Agent Calloway",
            ],
            "expected": (
                "The Social Web quest offer accepts, progresses through Whistle, "
                "the inn room, Raith, and Calloway, then records completion "
                "consequences."
            ),
        },
        {
            "title": "denial/repair verb",
            "commands": [
                "deny Whistle about me",
                "ask Whistle about me",
            ],
            "expected": (
                "The denial creates a new player-spoken contested claim through "
                "direct_witness knowledge. The original rumor remains intact."
            ),
        },
        {
            "title": "renderer fallback",
            "commands": [
                "python scripts/playtest_social_web_vertical.py",
            ],
            "expected": _renderer_fallback_line(),
        },
        {
            "title": "socialmemory inspection",
            "commands": [
                "socialmemory npc:npc_warden_agent_calloway player:<id>",
                "socialmemory npc:npc_warden_outpost_commander player:<id>",
                "socialmemory npc:npc_innkeeper_whistle player:<id>",
            ],
            "expected": (
                "Admin inspection shows the claims, channels, and traces that "
                "explain who knows what, without implying omniscient spread."
            ),
        },
    ]


def main():
    print("Soravelon Social Web Vael's Crossing playtest vertical")
    print("=" * 64)
    for index, beat in enumerate(build_playtest_beats(), start=1):
        print(f"\n{index}. {beat['title']}")
        print("   Commands:")
        for command in beat["commands"]:
            print(f"   - {command}")
        print(f"   Expected: {beat['expected']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
