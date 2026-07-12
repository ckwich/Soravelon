"""
Tests for social commands (who, shout, whisper) and channel typeclasses.

Uses unittest.TestCase + MagicMock + django.setup() — pure logic tests,
no Evennia DB needed (all characters are MagicMock).
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch, PropertyMock

# Configure Django settings before any Evennia/world imports.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django
django.setup()



class _MockDB:
    """Simple attribute bag that mimics Evennia's db handler."""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class _MockNDB:
    """Simple attribute bag for ndb (volatile) attributes."""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def _make_char(name, zone_id="vaels_crossing", ancestry="Human",
               domain_scores=None, guild_name=None, stamina=100,
               sessions_count=1, is_npc=False):
    """Create a mock character with standard attributes."""
    char = MagicMock()
    char.key = name
    char.id = id(char)
    # Remove puppet attr so channel code recognizes this as a character, not account
    del char.puppet
    char.db = _MockDB(
        ancestry=ancestry,
        domain_scores=domain_scores or {},
        guild_name=guild_name,
        guild_id=None,
        is_npc=is_npc,
    )
    char.ndb = _MockNDB(
        stamina=stamina,
        is_sleeping=False,
        hp=100,
        combat_handler=None,
    )

    # Location with zone tag
    location = MagicMock()
    tags = MagicMock()
    tags.get.return_value = [zone_id] if zone_id else []
    location.tags = tags
    location.contents = []
    char.location = location

    # Sessions
    sessions = MagicMock()
    sessions.count.return_value = sessions_count
    char.sessions = sessions

    return char


# ---------------------------------------------------------------------------
# CmdWho tests
# ---------------------------------------------------------------------------

class TestCmdWho(unittest.TestCase):

    @patch("commands.cmd_social.evennia")
    def test_who_lists_online_players(self, mock_evennia):
        """CmdWho lists all puppeted characters with name, ancestry, guild, zone."""
        from commands.cmd_social import CmdWho

        char1 = _make_char("Alice", ancestry="Human",
                           domain_scores={"combat": 50}, guild_name="Warblades")
        char2 = _make_char("Bob", ancestry="Kau'roran",
                           domain_scores={"naturalism": 30})

        # Session handler returns two sessions
        sess1 = MagicMock()
        sess1.get_puppet.return_value = char1
        sess2 = MagicMock()
        sess2.get_puppet.return_value = char2
        mock_evennia.SESSION_HANDLER.get_sessions.return_value = [sess1, sess2]

        cmd = CmdWho()
        cmd.caller = _make_char("Viewer")
        cmd.args = ""
        cmd.func()

        output = cmd.caller.msg.call_args[0][0]
        self.assertIn("Alice", output)
        self.assertIn("Bob", output)
        self.assertIn("2 player(s) online", output)

    @patch("commands.cmd_social.evennia")
    def test_who_no_players(self, mock_evennia):
        """CmdWho shows message when no one is online."""
        from commands.cmd_social import CmdWho

        mock_evennia.SESSION_HANDLER.get_sessions.return_value = []

        cmd = CmdWho()
        cmd.caller = _make_char("Viewer")
        cmd.args = ""
        cmd.func()

        output = cmd.caller.msg.call_args[0][0]
        self.assertIn("No one is online", output)

    @patch("commands.cmd_social.evennia")
    def test_who_deduplicates_multiple_sessions_on_same_character(self, mock_evennia):
        """CmdWho should only list a character once even with multiple sessions."""
        from commands.cmd_social import CmdWho

        char1 = _make_char("Alice", ancestry="Human")

        sess1 = MagicMock()
        sess1.get_puppet.return_value = char1
        sess2 = MagicMock()
        sess2.get_puppet.return_value = char1
        mock_evennia.SESSION_HANDLER.get_sessions.return_value = [sess1, sess2]

        cmd = CmdWho()
        cmd.caller = _make_char("Viewer")
        cmd.args = ""
        cmd.func()

        output = cmd.caller.msg.call_args[0][0]
        self.assertEqual(output.count("Alice"), 1)
        self.assertIn("1 player(s) online", output)


# ---------------------------------------------------------------------------
# CmdShout tests
# ---------------------------------------------------------------------------

class TestCmdShout(unittest.TestCase):

    @patch("world.recovery_engine.push_stat_update")
    @patch("commands.cmd_social.search_objects_by_exact_tag")
    def test_shout_reaches_zone(self, mock_search, mock_push):
        """CmdShout sends message to all characters in same zone."""
        from commands.cmd_social import CmdShout

        caller = _make_char("Shouter", stamina=50)
        listener = _make_char("Listener")

        # Set up zone search: one room with caller, one with listener
        room1 = caller.location
        room1.contents = [caller]
        room2 = listener.location
        room2.contents = [listener]
        mock_search.return_value = [room1, room2]

        cmd = CmdShout()
        cmd.caller = caller
        cmd.args = " Hello zone!"
        cmd.func()

        # Listener should have received the shout
        listener.msg.assert_called_once()
        msg = listener.msg.call_args[0][0]
        self.assertIn("Shouter", msg)
        self.assertIn("Hello zone!", msg)

    @patch("world.recovery_engine.push_stat_update")
    @patch("commands.cmd_social.evennia")
    def test_shout_costs_stamina(self, mock_evennia, mock_push):
        """Shout deducts 10 stamina from caller."""
        from commands.cmd_social import CmdShout, SHOUT_STAMINA_COST

        caller = _make_char("Shouter", stamina=50)
        mock_evennia.search_tag.return_value = [caller.location]
        caller.location.contents = [caller]

        cmd = CmdShout()
        cmd.caller = caller
        cmd.args = " test"
        cmd.func()

        self.assertEqual(caller.ndb.stamina, 50 - SHOUT_STAMINA_COST)

    @patch("commands.cmd_social.evennia")
    def test_shout_fails_no_stamina(self, mock_evennia):
        """Shout with < 10 stamina returns error."""
        from commands.cmd_social import CmdShout

        caller = _make_char("Tired", stamina=5)

        cmd = CmdShout()
        cmd.caller = caller
        cmd.args = " help!"
        cmd.func()

        output = cmd.caller.msg.call_args[0][0]
        self.assertIn("exhausted", output.lower())

    @patch("commands.cmd_social.evennia")
    def test_shout_no_args(self, mock_evennia):
        """Shout with no message returns error."""
        from commands.cmd_social import CmdShout

        caller = _make_char("Shouter")
        cmd = CmdShout()
        cmd.caller = caller
        cmd.args = ""
        cmd.func()

        output = cmd.caller.msg.call_args[0][0]
        self.assertIn("Shout what?", output)


# ---------------------------------------------------------------------------
# CmdWhisper tests
# ---------------------------------------------------------------------------

class TestCmdWhisper(unittest.TestCase):

    def test_whisper_delivers_to_target(self):
        """Whisper sends message to target."""
        from commands.cmd_social import CmdWhisper

        caller = _make_char("Whisperer")
        target = _make_char("Listener")
        caller.location.contents = [caller, target]
        caller.search = MagicMock(return_value=target)

        cmd = CmdWhisper()
        cmd.caller = caller
        cmd.args = " Listener secret message"
        cmd.func()

        # Target got the whisper
        target.msg.assert_called_once()
        msg = target.msg.call_args[0][0]
        self.assertIn("secret message", msg)

    def test_whisper_shows_notification(self):
        """Others in room see 'X whispers something to Y'."""
        from commands.cmd_social import CmdWhisper

        caller = _make_char("Whisperer")
        target = _make_char("Listener")
        bystander = _make_char("Bystander")
        caller.location.contents = [caller, target, bystander]
        caller.search = MagicMock(return_value=target)

        cmd = CmdWhisper()
        cmd.caller = caller
        cmd.args = " Listener secret message"
        cmd.func()

        # Bystander sees notification
        bystander.msg.assert_called_once()
        msg = bystander.msg.call_args[0][0]
        self.assertIn("whispers something", msg)
        self.assertNotIn("secret message", msg)

    def test_whisper_no_args(self):
        """Whisper with no args returns usage."""
        from commands.cmd_social import CmdWhisper

        caller = _make_char("Whisperer")
        cmd = CmdWhisper()
        cmd.caller = caller
        cmd.args = ""
        cmd.func()

        output = cmd.caller.msg.call_args[0][0]
        self.assertIn("Usage", output)

    def test_whisper_rejects_non_player_targets(self):
        """Whisper should reject NPCs so it does not overlap with tell."""
        from commands.cmd_social import CmdWhisper

        caller = _make_char("Whisperer")
        npc = _make_char("Steward", is_npc=True, sessions_count=0)
        caller.location.contents = [caller, npc]
        caller.search = MagicMock(return_value=npc)

        cmd = CmdWhisper()
        cmd.caller = caller
        cmd.args = " Steward secret message"
        cmd.func()

        output = cmd.caller.msg.call_args[0][0]
        self.assertIn("another player", output.lower())
        npc.msg.assert_not_called()


# ---------------------------------------------------------------------------
# Channel typeclass tests
# ---------------------------------------------------------------------------

class TestOOCChannel(unittest.TestCase):

    def test_ooc_channel_prefix(self):
        """OOCChannel has [OOC] prefix."""
        from typeclasses.channels import OOCChannel
        ch = OOCChannel.__new__(OOCChannel)
        prefix = ch.channel_prefix()
        self.assertIn("OOC", prefix)


class TestDomainChannel(unittest.TestCase):

    def _make_channel(self, domain_name="combat"):
        """Create a mock-friendly DomainChannel instance."""
        from typeclasses.channels import DomainChannel
        ch = MagicMock(spec=DomainChannel)
        ch.key = "combat"
        ch.db = _MockDB(domain_name=domain_name)
        # Bind the real at_pre_msg method to our mock
        ch.at_pre_msg = DomainChannel.at_pre_msg.__get__(ch)
        return ch

    def test_domain_channel_checks_membership(self):
        """DomainChannel.at_pre_msg rejects non-members."""
        ch = self._make_channel()

        # Create message mock — sender has naturalism as primary
        sender = _make_char("Outsider", domain_scores={"naturalism": 50, "combat": 10})
        message = MagicMock()
        message.senders = [sender]

        result = ch.at_pre_msg(message)
        self.assertFalse(result)

    def test_domain_channel_allows_member(self):
        """DomainChannel allows message from matching domain member."""
        from evennia.comms.comms import DefaultChannel
        ch = self._make_channel()

        sender = _make_char("Fighter", domain_scores={"combat": 50, "naturalism": 10})
        message = MagicMock()
        message.senders = [sender]

        with patch.object(DefaultChannel, "at_pre_msg", return_value=True):
            result = ch.at_pre_msg(message)
        self.assertTrue(result)


class TestDefaultChannelConfiguration(unittest.TestCase):

    def test_default_channels_include_domain_channels(self):
        """Every Soravelon domain is provisioned as a default channel."""
        from django.conf import settings
        from world.world_state import ALL_DOMAINS

        default_channels = settings.DEFAULT_CHANNELS
        domain_channels = [
            channel for channel in default_channels
            if channel.get("typeclass") == "typeclasses.channels.DomainChannel"
        ]

        self.assertEqual(len(domain_channels), len(ALL_DOMAINS))

        keyed_channels = {channel["key"].lower(): channel for channel in domain_channels}
        self.assertEqual(set(keyed_channels.keys()), set(ALL_DOMAINS))

        for domain_name in ALL_DOMAINS:
            channel = keyed_channels[domain_name]
            self.assertEqual(channel.get("aliases"), (domain_name,))
            self.assertEqual(
                channel.get("attrs"),
                [("domain_name", domain_name)],
            )


# ---------------------------------------------------------------------------
# Item inspection tests (will be added in Task 2)
# ---------------------------------------------------------------------------

class TestCmdInspect(unittest.TestCase):

    def test_inspect_no_skill_shows_basic(self):
        """Inspect with 0 appraisal shows desc but not stats."""
        from commands.cmd_inspect import CmdInspect

        caller = _make_char("Noob")
        item = MagicMock()
        item.key = "Iron Sword"
        item.db = _MockDB(
            desc="A rusty blade.",
            rarity="magic",
            material_tier=2,
            damage_min=5,
            damage_max=10,
            armor_value=0,
            stat_bonuses={},
            equipment_slot="weapon",
            value_scales=100,
        )
        caller.search = MagicMock(return_value=item)

        cmd = CmdInspect()
        cmd.caller = caller
        cmd.args = " Iron Sword"

        with patch("commands.cmd_inspect.get_skill_value", return_value=0):
            cmd.func()

        output = cmd.caller.msg.call_args[0][0]
        self.assertIn("Iron Sword", output)
        self.assertIn("too low", output.lower())
        # Should NOT show damage stats
        self.assertNotIn("5-10", output)

    def test_inspect_with_skill_shows_stats(self):
        """Inspect with sufficient appraisal shows damage, armor, bonuses."""
        from commands.cmd_inspect import CmdInspect

        caller = _make_char("Appraiser")
        item = MagicMock()
        item.key = "Iron Sword"
        item.db = _MockDB(
            desc="A fine blade.",
            rarity="magic",
            material_tier=2,
            damage_min=5,
            damage_max=10,
            armor_value=0,
            stat_bonuses={"strength": 3},
            equipment_slot="weapon",
            value_scales=100,
        )
        caller.search = MagicMock(return_value=item)

        cmd = CmdInspect()
        cmd.caller = caller
        cmd.args = " Iron Sword"

        # DC for magic + tier 2 = 15 + 10 = 25
        with patch("commands.cmd_inspect.get_skill_value", return_value=30):
            with patch("commands.cmd_inspect.accumulate_skill_use"):
                cmd.func()

        output = cmd.caller.msg.call_args[0][0]
        self.assertIn("5-10", output)
        self.assertIn("Strength", output)

    def test_inspect_dc_formula(self):
        """DC = (rarity_number * 15) + (material_tier * 5)."""
        from commands.cmd_inspect import _get_appraisal_dc

        item = MagicMock()
        # normal tier-1: 0 + 5 = 5
        item.db = _MockDB(rarity="normal", material_tier=1)
        self.assertEqual(_get_appraisal_dc(item), 5)

        # rare tier-3: 30 + 15 = 45
        item.db = _MockDB(rarity="rare", material_tier=3)
        self.assertEqual(_get_appraisal_dc(item), 45)


class TestCmdCompare(unittest.TestCase):

    def test_compare_two_items(self):
        """Compare shows side-by-side stat differences."""
        from commands.cmd_inspect import CmdCompare

        caller = _make_char("Comparer")
        item1 = MagicMock()
        item1.key = "Iron Sword"
        item1.db = _MockDB(
            rarity="normal", material_tier=1,
            damage_min=5, damage_max=10, armor_value=0,
            stat_bonuses={}, equipment_slot="weapon", value_scales=50,
        )
        item2 = MagicMock()
        item2.key = "Steel Sword"
        item2.db = _MockDB(
            rarity="magic", material_tier=2,
            damage_min=8, damage_max=15, armor_value=0,
            stat_bonuses={"strength": 2}, equipment_slot="weapon", value_scales=120,
        )

        def search_side_effect(name):
            if "Iron" in name:
                return item1
            return item2

        caller.search = MagicMock(side_effect=search_side_effect)

        cmd = CmdCompare()
        cmd.caller = caller
        cmd.args = " Iron Sword to Steel Sword"

        # Both items need low DC for appraisal check
        with patch("commands.cmd_inspect.get_skill_value", return_value=100):
            cmd.func()

        output = cmd.caller.msg.call_args[0][0]
        self.assertIn("Iron Sword", output)
        self.assertIn("Steel Sword", output)
        self.assertIn("Damage", output)

    def test_compare_missing_item(self):
        """Compare with missing item shows search error (handled by search)."""
        from commands.cmd_inspect import CmdCompare

        caller = _make_char("Comparer")
        caller.search = MagicMock(return_value=None)

        cmd = CmdCompare()
        cmd.caller = caller
        cmd.args = " missing1 to missing2"
        cmd.func()

        # search returns None, so func returns early — no crash


if __name__ == "__main__":
    unittest.main()
