"""Current-era Remnance blackout coverage.

Remnance exists in internal data for future world-event content, but it must
not be visible to players until the dragon curse story reaches that point.
"""

import ast
import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django
django.setup()


class TestCurrentEraRemnanceBlackout(unittest.TestCase):
    """Player-facing surfaces must not expose Remnance or Vaelborn."""

    def test_public_help_entries_do_not_name_remnance_or_vaelborn(self):
        from world.help_entries import HELP_ENTRY_DICTS

        leaks = []
        for entry in HELP_ENTRY_DICTS:
            if entry.get("locks") != "read:all()":
                continue
            haystack = " ".join(
                [
                    str(entry.get("key", "")),
                    " ".join(entry.get("aliases") or []),
                    str(entry.get("category", "")),
                    str(entry.get("text", "")),
                ]
            )
            for forbidden in ("Remnance", "remnance", "Vaelborn", "vaelborn"):
                if forbidden in haystack:
                    leaks.append((entry.get("key"), forbidden))

        self.assertEqual(leaks, [])

    def test_dynamic_ability_help_does_not_resolve_remnance_linked_abilities(self):
        from commands.cmd_help import resolve_ability_help_query

        abilities = {
            "echo_lash": {
                "id": "echo_lash",
                "name": "Echo Lash",
                "domain": "remnance",
                "scaling_primary": "remnance",
                "resource_type": "echoes",
            },
            "momentum_strike": {
                "id": "momentum_strike",
                "name": "Momentum Strike",
                "domain": "combat",
                "scaling_primary": "combat",
                "resource_type": "momentum",
            },
        }

        ability, matches = resolve_ability_help_query("echo lash", abilities)

        self.assertIsNone(ability)
        self.assertEqual(matches, [])

    def test_domains_command_ignores_legacy_remnance_discovered_flag(self):
        from commands.cmd_domains import CmdDomains

        character = MagicMock()
        character.db = SimpleNamespace(
            domain_scores={"combat": 12, "remnance": 80},
            guild_id=None,
            remnance_discovered=True,
            remnance_player_visible=False,
        )
        character.msg = MagicMock()
        cmd = CmdDomains()
        cmd.caller = character

        cmd.func()

        message = character.msg.call_args[0][0]
        self.assertIn("Combat", message)
        self.assertNotIn("Remnance", message)

    @patch.dict(
        "world.guild_engine.GUILDS",
        {
            "vaelborn": {
                "name": "Guild of Vaelborn",
                "primary_domain": "remnance",
                "motto": "The sealed road waits.",
                "hidden": True,
            }
        },
        clear=True,
    )
    @patch("world.guild_engine.check_guild_eligibility", return_value=["vaelborn"])
    def test_joinguild_hides_vaelborn_even_with_legacy_discovery_flag(
        self, _mock_eligibility
    ):
        from commands.cmd_guild import CmdJoinGuild

        character = MagicMock()
        character.db = SimpleNamespace(
            guild_id=None,
            domain_scores={"remnance": 100},
            subclass_id=None,
            remnance_discovered=True,
            remnance_player_visible=False,
        )
        character.msg = MagicMock()
        cmd = CmdJoinGuild()
        cmd.caller = character
        cmd.args = ""

        cmd.func()

        message = character.msg.call_args[0][0]
        self.assertIn("No guild", message)
        self.assertNotIn("Vaelborn", message)

    @patch.dict(
        "world.guild_engine.GUILDS",
        {
            "vaelborn": {
                "name": "Guild of Vaelborn",
                "primary_domain": "remnance",
                "hidden": True,
            }
        },
        clear=True,
    )
    @patch("world.guild_engine.check_guild_eligibility", return_value=["vaelborn"])
    def test_login_guidance_ignores_hidden_only_guild_offers(
        self, _mock_eligibility
    ):
        from world.session_lifecycle import get_new_player_guidance

        character = MagicMock()
        character.db = SimpleNamespace(
            ancestry="human",
            backend_level=1,
            guild_id=None,
            remnance_discovered=True,
            remnance_player_visible=False,
        )
        character.ndb = SimpleNamespace()

        guidance = get_new_player_guidance(character)

        self.assertNotIn("invitation is waiting", guidance.lower())
        self.assertNotIn("vaelborn", guidance.lower())
        self.assertIn("keep practicing", guidance.lower())

    @patch.dict(
        "world.guild_engine.GUILDS",
        {
            "vaelborn": {
                "name": "Guild of Vaelborn",
                "primary_domain": "remnance",
                "hidden": True,
            }
        },
        clear=True,
    )
    @patch("world.guild_engine.check_guild_eligibility", return_value=["vaelborn"])
    def test_guild_discovery_message_ignores_hidden_only_guild_offers(
        self, _mock_eligibility
    ):
        from world.world_state import _check_guild_discovery

        character = MagicMock()
        character.db = SimpleNamespace(
            guild_id=None,
            remnance_discovered=True,
            remnance_player_visible=False,
        )
        character.msg = MagicMock()

        _check_guild_discovery(character)

        character.msg.assert_not_called()

    def test_area_and_lore_string_constants_do_not_name_current_era_remnance(self):
        repo_root = Path(__file__).resolve().parents[1]
        paths = list((repo_root / "world" / "areas").glob("*.py"))
        paths.append(repo_root / "world" / "lore_registry.py")
        leaks = []

        for path in paths:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                    continue
                if "Remnance" in node.value or "Vaelborn" in node.value:
                    leaks.append(f"{path.name}:{node.lineno}")

        self.assertEqual(leaks, [])
