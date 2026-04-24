"""Direct command coverage for guild joining flows."""

import os
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django
django.setup()


class _MockDB:
    """Simple attribute bag that mimics Evennia's db handler."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def _make_character(
    guild_id=None,
    remnance_discovered=False,
    domain_scores=None,
    subclass_id="war_scout",
):
    character = MagicMock()
    character.db = _MockDB(
        guild_id=guild_id,
        remnance_discovered=remnance_discovered,
        domain_scores=domain_scores or {},
        subclass_id=subclass_id,
    )
    character.msg = MagicMock()
    return character


class TestCmdJoinGuild(unittest.TestCase):
    """Behavior-focused tests for CmdJoinGuild branching."""

    def _make_cmd(self, character, args=""):
        from commands.cmd_guild import CmdJoinGuild

        cmd = CmdJoinGuild()
        cmd.caller = character
        cmd.args = args
        return cmd

    @patch.dict("world.guild_engine.GUILDS", {
        "warblades": {"name": "Warblades", "primary_domain": "combat"},
    }, clear=True)
    def test_joinguild_rejects_already_guilded_characters(self):
        character = _make_character(guild_id="warblades")
        cmd = self._make_cmd(character)

        cmd.func()

        message = character.msg.call_args[0][0]
        self.assertIn("already a member of Warblades", message)

    @patch.dict("world.guild_engine.GUILDS", {
        "warblades": {
            "name": "Warblades",
            "primary_domain": "combat",
            "motto": "Steel answers first.",
            "hidden": False,
        },
        "embersigil": {
            "name": "Embersigil",
            "primary_domain": "arcana",
            "motto": "Every spark remembers.",
            "hidden": False,
        },
        "vaelborn": {
            "name": "Vaelborn",
            "primary_domain": "sorcery",
            "motto": "Silence keeps the old bargains.",
            "hidden": True,
        },
    }, clear=True)
    @patch("world.guild_engine.check_guild_eligibility", return_value=["warblades", "embersigil", "vaelborn"])
    def test_joinguild_lists_only_visible_invitations(self, _mock_eligibility):
        character = _make_character()
        cmd = self._make_cmd(character)

        cmd.func()

        message = character.msg.call_args[0][0]
        self.assertIn("Guild Invitations", message)
        self.assertIn("Warblades", message)
        self.assertIn("Embersigil", message)
        self.assertNotIn("Vaelborn", message)
        self.assertIn("joinguild <guild_name> <secondary_domain>", message)

    @patch.dict("world.guild_engine.GUILDS", {
        "warblades": {
            "name": "Warblades",
            "primary_domain": "combat",
            "motto": "Steel answers first.",
            "hidden": False,
        },
    }, clear=True)
    @patch("world.guild_engine.check_guild_eligibility", return_value=["warblades"])
    def test_joinguild_prompts_for_secondary_domain(self, _mock_eligibility):
        character = _make_character(
            domain_scores={"combat": 55, "subterfuge": 22, "naturalism": 10}
        )
        cmd = self._make_cmd(character, "warblades")

        cmd.func()

        message = character.msg.call_args[0][0]
        self.assertIn("Choose a secondary domain", message)
        self.assertIn("subterfuge", message.lower())
        self.assertIn("(recommended)", message)

    @patch.dict("world.guild_engine.GUILDS", {
        "warblades": {
            "name": "Warblades",
            "primary_domain": "combat",
            "motto": "Steel answers first.",
            "hidden": False,
        },
    }, clear=True)
    @patch.dict("world.guild_engine.SUBCLASSES", {
        "war_scout": {"name": "War Scout"},
    }, clear=True)
    @patch("world.guild_engine.join_guild", return_value=(True, "You swear the guild oath."))
    @patch("world.guild_engine.check_guild_eligibility", return_value=["warblades"])
    def test_joinguild_calls_join_engine_and_reports_welcome(
        self,
        _mock_eligibility,
        mock_join_guild,
    ):
        character = _make_character(
            domain_scores={"combat": 55, "wilderness": 22},
            subclass_id="war_scout",
        )
        cmd = self._make_cmd(character, "warblades wilderness")

        cmd.func()

        mock_join_guild.assert_called_once_with(character, "warblades", "wilderness")
        messages = [call.args[0] for call in character.msg.call_args_list]
        self.assertIn("You swear the guild oath.", messages[0])
        self.assertIn("Warblades welcomes you", messages[1])
        self.assertIn("War Scout", messages[1])
