"""Direct command coverage for guild joining flows."""

import os
import unittest
from types import SimpleNamespace
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
        "verdance": {"name": "Guild of Verdance", "primary_domain": "naturalism"},
        "arcane": {"name": "Guild of the Arcane", "primary_domain": "arcana"},
    }, clear=True)
    @patch("world.guild_engine.get_open_guild_recruitments")
    def test_joinguild_lists_durable_invitations_and_contact_routes(self, mock_open):
        mock_open.return_value = [
            SimpleNamespace(
                guild_id="verdance",
                contact_npc_id="npc_guildmaster_naturalism_elwen",
                location_zone_id="vaels_crossing",
                location_room_id="gq_naturalism_hall",
            ),
            SimpleNamespace(
                guild_id="arcane",
                contact_npc_id="npc_guildmaster_arcana_thessa",
                location_zone_id="vaels_crossing",
                location_room_id="gq_arcana_hall",
            ),
        ]
        character = _make_character()
        cmd = self._make_cmd(character)

        cmd.func()

        message = character.msg.call_args[0][0]
        self.assertIn("Guild Invitations", message)
        self.assertIn("Guild of Verdance", message)
        self.assertIn("Elwen", message)
        self.assertIn("Naturalism Hall", message)
        self.assertIn("talk", message.lower())
        self.assertNotIn("score", message.lower())

    @patch("world.guild_engine.get_open_guild_recruitments", return_value=[])
    def test_joinguild_without_durable_invitation_does_not_infer_from_scores(self, _open):
        character = _make_character(domain_scores={"naturalism": 99})
        cmd = self._make_cmd(character)

        cmd.func()

        message = character.msg.call_args[0][0]
        self.assertIn("No guild has sent you an invitation", message)

    @patch.dict("world.guild_engine.GUILDS", {
        "verdance": {"name": "Guild of Verdance", "primary_domain": "naturalism"},
    }, clear=True)
    @patch("world.guild_engine.get_open_guild_recruitments")
    @patch("world.guild_engine.join_guild", return_value=(True, "remote join"))
    def test_joinguild_arguments_cannot_remotely_mutate_membership(
        self, mock_join_guild, mock_open
    ):
        mock_open.return_value = [
            SimpleNamespace(
                guild_id="verdance",
                contact_npc_id="npc_guildmaster_naturalism_elwen",
                location_zone_id="vaels_crossing",
                location_room_id="gq_naturalism_hall",
            )
        ]
        character = _make_character()
        cmd = self._make_cmd(character, "verdance resonance")

        cmd.func()

        mock_join_guild.assert_not_called()
        message = character.msg.call_args[0][0]
        self.assertIn("Elwen", message)
        self.assertIn("talk", message.lower())
