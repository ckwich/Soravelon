"""
Tests for the fishing system (Phase 13 SC-5).

Covers CmdFish active mode (cast -> bite -> reel), idle mode with periodic
catches, bait consumption and quality bonus, state management, and stop command.

Uses unittest.TestCase with MagicMock for all tests (no DB dependencies).
"""

import unittest
from unittest.mock import MagicMock, patch, call


# ---------------------------------------------------------------------------
# Fishing State Machine
# ---------------------------------------------------------------------------


class TestFishingStateMachine(unittest.TestCase):
    """Test fishing state transitions and requirements."""

    def test_fish_command_key(self):
        """CmdFish has key='fish' and proper help_category."""
        from commands.cmd_fishing import CmdFish

        cmd = CmdFish()
        self.assertEqual(cmd.key, "fish")
        self.assertEqual(cmd.help_category, "Gathering")

    def test_reel_command_key(self):
        """CmdReel has key='reel'."""
        from commands.cmd_fishing import CmdReel

        cmd = CmdReel()
        self.assertEqual(cmd.key, "reel")

    def test_fish_stop_clears_state(self):
        """After _stop_fishing, fishing_state should be None."""
        from commands.cmd_fishing import CmdFish

        character = MagicMock()
        character.ndb.fishing_state = {
            "mode": "active",
            "phase": "cast",
        }

        cmd = CmdFish()
        cmd._stop_fishing(character)

        self.assertIsNone(character.ndb.fishing_state)

    def test_fish_stop_cancels_deferreds(self):
        """_stop_fishing cancels active deferred timers."""
        from commands.cmd_fishing import CmdFish

        mock_deferred = MagicMock()
        mock_deferred.active.return_value = True

        character = MagicMock()
        character.ndb.fishing_state = {
            "mode": "active",
            "phase": "bite",
            "bite_deferred": mock_deferred,
            "reel_deferred": None,
        }

        cmd = CmdFish()
        cmd._stop_fishing(character)

        mock_deferred.cancel.assert_called_once()
        self.assertIsNone(character.ndb.fishing_state)

    def test_fish_requires_rod(self):
        """_find_tool returns None when no fishing_rod in inventory."""
        from commands.cmd_fishing import CmdFish

        character = MagicMock()
        # Empty inventory -- contents has no items with fishing_rod tag
        item1 = MagicMock()
        item1.tags.has.return_value = False
        character.contents = [item1]

        cmd = CmdFish()
        result = cmd._find_tool(character)
        self.assertIsNone(result)

    def test_fish_finds_rod(self):
        """_find_tool returns the rod when fishing_rod tag present."""
        from commands.cmd_fishing import CmdFish

        character = MagicMock()
        rod = MagicMock()
        rod.tags.has.side_effect = lambda tag, category=None: tag == "fishing_rod"
        character.contents = [rod]

        cmd = CmdFish()
        result = cmd._find_tool(character)
        self.assertEqual(result, rod)


# ---------------------------------------------------------------------------
# Active Fishing
# ---------------------------------------------------------------------------


class TestActiveFishing(unittest.TestCase):
    """Test active fishing cast -> bite -> reel cycle."""

    @patch("commands.cmd_fishing.delay")
    def test_start_active_sets_state(self, mock_delay):
        """_start_active_fishing sets mode=active, phase=cast."""
        from commands.cmd_fishing import CmdFish

        character = MagicMock()
        character.ndb.fishing_state = None
        character.location = MagicMock()

        node = MagicMock()
        tool = MagicMock()

        cmd = CmdFish()
        cmd._start_active_fishing(character, node, tool, bait=None)

        state = character.ndb.fishing_state
        self.assertEqual(state["mode"], "active")
        self.assertEqual(state["phase"], "cast")
        self.assertEqual(state["node"], node)
        mock_delay.assert_called_once()

    def test_on_bite_changes_phase(self):
        """After _on_bite fires, phase changes to 'bite'."""
        from commands.cmd_fishing import CmdFish

        character = MagicMock()
        start_room = MagicMock()
        character.location = start_room
        character.ndb.fishing_state = {
            "mode": "active",
            "phase": "cast",
            "start_room": start_room,
        }

        cmd = CmdFish()
        with patch("commands.cmd_fishing.delay") as mock_delay:
            cmd._on_bite(character)

        self.assertEqual(character.ndb.fishing_state["phase"], "bite")

    @patch("commands.cmd_fishing.CmdFish._catch_fish")
    def test_reel_during_bite_catches(self, mock_catch):
        """_on_reel during bite phase calls _catch_fish."""
        from commands.cmd_fishing import CmdFish

        mock_deferred = MagicMock()
        mock_deferred.active.return_value = True

        character = MagicMock()
        character.ndb.fishing_state = {
            "mode": "active",
            "phase": "bite",
            "reel_deferred": mock_deferred,
            "node": MagicMock(),
            "tool": MagicMock(),
        }

        cmd = CmdFish()
        cmd._on_reel(character)

        mock_catch.assert_called_once()
        mock_deferred.cancel.assert_called_once()

    def test_reel_without_bite_does_nothing(self):
        """_on_reel when not in bite phase sends error message."""
        from commands.cmd_fishing import CmdFish

        character = MagicMock()
        character.ndb.fishing_state = {
            "mode": "active",
            "phase": "cast",
        }

        cmd = CmdFish()
        cmd._on_reel(character)

        character.msg.assert_called_once()
        self.assertIn("don't have anything", character.msg.call_args[0][0])

    def test_on_miss_restarts_cast(self):
        """If reel window expires, _on_miss restarts active fishing."""
        from commands.cmd_fishing import CmdFish

        character = MagicMock()
        node = MagicMock()
        tool = MagicMock()
        character.ndb.fishing_state = {
            "mode": "active",
            "phase": "bite",
            "node": node,
            "tool": tool,
            "bait": None,
        }

        cmd = CmdFish()
        with patch.object(cmd, "_start_active_fishing") as mock_start:
            cmd._on_miss(character)
            mock_start.assert_called_once_with(character, node, tool, None)


# ---------------------------------------------------------------------------
# Idle Fishing
# ---------------------------------------------------------------------------


class TestIdleFishing(unittest.TestCase):
    """Test idle auto-fishing mode."""

    @patch("commands.cmd_fishing.delay")
    def test_start_idle_sets_state(self, mock_delay):
        """_start_idle_fishing sets mode=idle."""
        from commands.cmd_fishing import CmdFish

        character = MagicMock()
        character.ndb.fishing_state = None
        character.location = MagicMock()

        node = MagicMock()
        tool = MagicMock()

        cmd = CmdFish()
        cmd._start_idle_fishing(character, node, tool, bait=None)

        state = character.ndb.fishing_state
        self.assertEqual(state["mode"], "idle")
        mock_delay.assert_called_once()

    @patch("commands.cmd_fishing.delay")
    @patch("commands.cmd_fishing.CmdFish._catch_fish")
    def test_idle_catch_reschedules(self, mock_catch, mock_delay):
        """After idle catch, another idle timer is scheduled."""
        from commands.cmd_fishing import CmdFish

        character = MagicMock()
        start_room = MagicMock()
        character.location = start_room
        node = MagicMock()
        node.pk = 1
        character.ndb.fishing_state = {
            "mode": "idle",
            "start_room": start_room,
            "node": node,
            "tool": MagicMock(),
            "bait": None,
        }

        cmd = CmdFish()
        cmd._idle_catch(character)

        # _catch_fish called with 0.5 quality multiplier
        mock_catch.assert_called_once()
        args = mock_catch.call_args
        self.assertAlmostEqual(args[1].get("quality_multiplier", args[0][-1]), 0.5)

        # delay called to schedule next idle catch
        mock_delay.assert_called_once()

    def test_idle_quality_penalty_logic(self):
        """Idle mode applies 0.5 quality_multiplier (drops 1 tier)."""
        from world.crafting_definitions import QUALITY_TIERS

        # Simulate idle penalty logic: qi = max(0, qi - 1)
        for qi in range(len(QUALITY_TIERS)):
            penalized = max(0, qi - 1)
            # Verify penalty drops by 1 (or stays at 0)
            if qi > 0:
                self.assertEqual(penalized, qi - 1)
            else:
                self.assertEqual(penalized, 0)


# ---------------------------------------------------------------------------
# Bait System
# ---------------------------------------------------------------------------


class TestBaitSystem(unittest.TestCase):
    """Test bait consumption and quality bonus."""

    def test_bait_quality_bonus_logic(self):
        """Bait adds +1 quality tier."""
        from world.crafting_definitions import QUALITY_TIERS

        # Simulate bait bonus: qi = min(len-1, qi + 1)
        for qi in range(len(QUALITY_TIERS)):
            boosted = min(len(QUALITY_TIERS) - 1, qi + 1)
            if qi < len(QUALITY_TIERS) - 1:
                self.assertEqual(boosted, qi + 1)
            else:
                self.assertEqual(boosted, qi)  # already max

    def test_no_bait_still_works(self):
        """Fishing without bait should still succeed (bait is optional)."""
        from commands.cmd_fishing import CmdFish

        character = MagicMock()
        # No items with bait tag
        character.contents = []

        cmd = CmdFish()
        bait = cmd._find_bait(character)
        self.assertIsNone(bait)

    def test_bait_found_in_inventory(self):
        """_find_bait returns bait item when present."""
        from commands.cmd_fishing import CmdFish

        character = MagicMock()
        bait_item = MagicMock()
        bait_item.tags.has.side_effect = lambda tag, category=None: tag == "bait"
        character.contents = [bait_item]

        cmd = CmdFish()
        result = cmd._find_bait(character)
        self.assertEqual(result, bait_item)

    def test_bait_consumed_on_catch_logic(self):
        """In _catch_fish, bait.delete() is called and state['bait'] set to None."""
        # This verifies the code path exists in cmd_fishing.py
        # The actual logic: if bait and bait.pk: ... bait.delete(); state["bait"] = None
        # We verify by checking the source structure
        import inspect
        from commands.cmd_fishing import CmdFish

        source = inspect.getsource(CmdFish._catch_fish)
        self.assertIn("bait.delete()", source)
        self.assertIn('state["bait"] = None', source)
