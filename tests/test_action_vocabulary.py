"""
Tests for the action vocabulary dispatch module (Plan 01-01, Task 1).

Plan 01-01: 21 initial tests (TDD RED).
Plan 11-05: Extended with 20 tests for 3 new quest reward handlers
            (give_scales, give_skill_xp, modify_node_failure).

Tests written FIRST per TDD discipline — RED phase.
All tests must fail before world/action_vocabulary.py is created.
"""

import os
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")

import django  # noqa: E402
django.setup()

from evennia.utils.test_resources import EvenniaTest  # noqa: E402


class TestExecuteActionDepthLimit(EvenniaTest):
    """Depth limit guard blocks chained trigger execution at depth >= 3."""

    def test_depth_3_returns_false(self):
        """execute_action at depth 3 returns (False, 'Trigger chain depth limit reached.')."""
        from world.action_vocabulary import execute_action

        success, msg = execute_action({"action_type": "echo", "message": "hi"}, {}, _depth=3)
        self.assertFalse(success)
        self.assertIn("depth limit", msg.lower())

    def test_depth_4_also_blocked(self):
        """execute_action at depth > 3 is also blocked."""
        from world.action_vocabulary import execute_action

        success, msg = execute_action({"action_type": "echo", "message": "hi"}, {}, _depth=10)
        self.assertFalse(success)

    def test_depth_2_is_allowed(self):
        """execute_action at depth 2 proceeds normally (not yet at limit)."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        success, msg = execute_action(
            {"action_type": "echo", "message": "hi"},
            {"character": char},
            _depth=2,
        )
        self.assertTrue(success)
        char.msg.assert_called_once_with("hi")


class TestExecuteActionUnknownType(EvenniaTest):
    """Unknown action_type returns (False, descriptive message)."""

    def test_unknown_action_type(self):
        """Unknown action_type returns (False, 'Unknown action type: X')."""
        from world.action_vocabulary import execute_action

        success, msg = execute_action({"action_type": "fly_to_moon"}, {})
        self.assertFalse(success)
        self.assertIn("fly_to_moon", msg)

    def test_missing_action_type(self):
        """Missing action_type key returns (False, error message)."""
        from world.action_vocabulary import execute_action

        success, msg = execute_action({}, {})
        self.assertFalse(success)
        self.assertIn("Unknown action type", msg)


class TestActionHandlersRegistry(EvenniaTest):
    """ACTION_HANDLERS dict contains all registered action types."""

    def test_handler_count(self):
        """ACTION_HANDLERS has exactly 16 keys (12 original + add_room_flag + 3 quest reward handlers)."""
        from world.action_vocabulary import ACTION_HANDLERS

        self.assertEqual(len(ACTION_HANDLERS), 16)

    def test_all_expected_action_types_present(self):
        """All 16 required action types are registered."""
        from world.action_vocabulary import ACTION_HANDLERS

        expected = {
            "teleport",
            "teleport_to_mob",
            "echo",
            "give_item",
            "take_item",
            "set_quest_flag",
            "modify_standing",
            "spawn_mob",
            "despawn_self",
            "open_dialogue",
            "log_world_event",
            "modify_attunement",
            "add_room_flag",
            "give_scales",
            "give_skill_xp",
            "modify_node_failure",
        }
        self.assertEqual(set(ACTION_HANDLERS.keys()), expected)


class TestEchoAction(EvenniaTest):
    """echo action sends message to character."""

    def test_echo_sends_message(self):
        """echo action calls character.msg(message)."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        success, msg = execute_action(
            {"action_type": "echo", "message": "hello world"},
            {"character": char},
        )
        self.assertTrue(success)
        char.msg.assert_called_once_with("hello world")

    def test_echo_no_character_returns_false(self):
        """echo action without character context returns (False, error)."""
        from world.action_vocabulary import execute_action

        success, msg = execute_action({"action_type": "echo", "message": "hello"}, {})
        self.assertFalse(success)


class TestTeleportAction(EvenniaTest):
    """teleport action moves character to target room."""

    def test_teleport_moves_character(self):
        """teleport calls character.move_to(room)."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        target_room = MagicMock()
        target_room.id = 999

        with patch("evennia.search_object") as mock_search:
            mock_search.return_value = [target_room]
            success, msg = execute_action(
                {"action_type": "teleport", "target_room_id": 999},
                {"character": char},
            )

        self.assertTrue(success)
        char.move_to.assert_called_once_with(target_room, quiet=False)

    def test_teleport_room_not_found_returns_false(self):
        """teleport with invalid room_id returns (False, error)."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        with patch("evennia.search_object") as mock_search:
            mock_search.return_value = []
            success, msg = execute_action(
                {"action_type": "teleport", "target_room_id": 9999},
                {"character": char},
            )

        self.assertFalse(success)


class TestTeleportToMobAction(EvenniaTest):
    """teleport_to_mob action moves character to mob's location."""

    def test_teleport_to_mob_moves_character(self):
        """teleport_to_mob looks up named mob and moves character there."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        mob_room = MagicMock()
        mob_obj = MagicMock()
        mob_obj.location = mob_room

        with patch("evennia.search_object") as mock_search:
            mock_search.return_value = [mob_obj]
            success, msg = execute_action(
                {"action_type": "teleport_to_mob", "mob_key": "guard_01"},
                {"character": char},
            )

        self.assertTrue(success)
        char.move_to.assert_called_once_with(mob_room, quiet=False)

    def test_teleport_to_mob_not_found_returns_false(self):
        """teleport_to_mob with unknown mob_key returns (False, error)."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        with patch("evennia.search_object") as mock_search:
            mock_search.return_value = []
            success, msg = execute_action(
                {"action_type": "teleport_to_mob", "mob_key": "nonexistent_mob"},
                {"character": char},
            )

        self.assertFalse(success)


class TestSetQuestFlagCallsQuestEngine(EvenniaTest):
    """set_quest_flag handler wires into quest_engine for real quest flag operations."""

    def test_set_quest_flag_calls_quest_engine(self):
        """set_quest_flag calls quest_engine.get_quest_detail and sets flag on active quest."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        detail = {"status": "active", "quest_id": "wolves_hunt"}

        with patch("world.quest_engine.get_quest_detail", return_value=detail) as mock_detail:
            cq = MagicMock()
            cq.quest_id = "wolves_hunt"
            cq.progress = {}
            with patch("world.quest_engine.get_active_quests", return_value=[cq]):
                success, msg = execute_action(
                    {"action_type": "set_quest_flag", "quest_id": "wolves_hunt", "flag_name": "talked_to_guard"},
                    {"character": char},
                )

        self.assertTrue(success)
        mock_detail.assert_called_once_with(char, "wolves_hunt")

    def test_set_quest_flag_no_character_fails(self):
        """set_quest_flag without character in context returns failure."""
        from world.action_vocabulary import execute_action

        success, msg = execute_action(
            {"action_type": "set_quest_flag", "quest_id": "q1", "flag_name": "f1"}, {}
        )
        self.assertFalse(success)


class TestOpenDialogueCallsQuestEngine(EvenniaTest):
    """open_dialogue handler wires into quest_engine and dialogue_engine."""

    def test_open_dialogue_calls_quest_engine(self):
        """open_dialogue checks for available quest via quest_engine and sends greeting."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        npc = MagicMock()
        quest_spec = {"quest_id": "wolves_hunt", "name": "Hunt the Wolves"}

        with patch("world.quest_engine.get_available_quest_for_npc", return_value=quest_spec) as mock_avail, \
             patch("world.quest_engine.accept_quest") as mock_accept, \
             patch("world.dialogue_engine.resolve_greeting", return_value=("Hello!", "neutral")):
            success, msg = execute_action(
                {"action_type": "open_dialogue"},
                {"character": char, "npc": npc},
            )

        self.assertTrue(success)
        mock_avail.assert_called_once_with(npc, char)
        mock_accept.assert_called_once_with(char, "wolves_hunt", quest_spec)

    def test_open_dialogue_no_character_fails(self):
        """open_dialogue without character in context returns failure."""
        from world.action_vocabulary import execute_action

        success, msg = execute_action({"action_type": "open_dialogue"}, {})
        self.assertFalse(success)


class TestDespawnSelfAction(EvenniaTest):
    """despawn_self deletes the mob object from context."""

    def test_despawn_self_deletes_mob(self):
        """despawn_self calls mob.delete()."""
        from world.action_vocabulary import execute_action

        mob = MagicMock()
        success, msg = execute_action(
            {"action_type": "despawn_self"},
            {"mob": mob},
        )
        self.assertTrue(success)
        mob.delete.assert_called_once()

    def test_despawn_self_no_mob_returns_false(self):
        """despawn_self without mob in context returns (False, error)."""
        from world.action_vocabulary import execute_action

        success, msg = execute_action({"action_type": "despawn_self"}, {})
        self.assertFalse(success)


class TestModifyStandingAction(EvenniaTest):
    """modify_standing action calls world_state.modify_standing."""

    def test_modify_standing_calls_engine(self):
        """modify_standing dispatches to world_state.modify_standing."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        with patch("world.world_state.modify_standing") as mock_ms:
            success, msg = execute_action(
                {"action_type": "modify_standing", "faction_id": "empire", "delta": 10},
                {"character": char},
            )

        self.assertTrue(success)
        mock_ms.assert_called_once()
        call_args = mock_ms.call_args
        self.assertEqual(call_args[0][0], char)
        self.assertEqual(call_args[0][1], "empire")


class TestModifyAttunementAction(EvenniaTest):
    """modify_attunement action calls world_state.update_zone_attunement."""

    def test_modify_attunement_calls_engine(self):
        """modify_attunement dispatches to world_state.update_zone_attunement."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        with patch("world.world_state.update_zone_attunement") as mock_ua:
            success, msg = execute_action(
                {"action_type": "modify_attunement", "zone_id": "zone_01", "delta": 5},
                {"character": char},
            )

        self.assertTrue(success)
        mock_ua.assert_called_once()


class TestLogWorldEventAction(EvenniaTest):
    """log_world_event action calls world_state.log_world_event."""

    def test_log_world_event_calls_engine(self):
        """log_world_event dispatches to world_state.log_world_event."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        with patch("world.world_state.log_world_event") as mock_lwe:
            success, msg = execute_action(
                {"action_type": "log_world_event", "event_type": "discovery", "data": {}},
                {"character": char},
            )

        self.assertTrue(success)
        mock_lwe.assert_called_once()


# ---------------------------------------------------------------------------
# Phase 11 Plan 05: Tests for 3 new quest reward action handlers
# ---------------------------------------------------------------------------


class TestGiveScalesHandler(unittest.TestCase):
    """Test _handle_give_scales action handler (D-14)."""

    def test_gives_correct_amount(self):
        """give_scales adds amount to carried_scales."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        char.db.carried_scales = 100
        context = {"character": char}
        action = {"action_type": "give_scales", "amount": 50}
        success, msg = execute_action(action, context)
        self.assertTrue(success)
        self.assertEqual(char.db.carried_scales, 150)

    def test_gives_to_zero_balance(self):
        """give_scales adds to a character with 0 Scales."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        char.db.carried_scales = 0
        context = {"character": char}
        action = {"action_type": "give_scales", "amount": 75}
        success, msg = execute_action(action, context)
        self.assertTrue(success)
        self.assertEqual(char.db.carried_scales, 75)

    def test_gives_to_none_balance(self):
        """give_scales treats None carried_scales as 0."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        char.db.carried_scales = None
        context = {"character": char}
        action = {"action_type": "give_scales", "amount": 25}
        success, msg = execute_action(action, context)
        self.assertTrue(success)
        self.assertEqual(char.db.carried_scales, 25)

    def test_zero_amount_rejected(self):
        """give_scales with amount=0 returns failure."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        char.db.carried_scales = 100
        context = {"character": char}
        action = {"action_type": "give_scales", "amount": 0}
        success, msg = execute_action(action, context)
        self.assertFalse(success)
        self.assertIn("invalid", msg.lower())

    def test_negative_amount_rejected(self):
        """give_scales with negative amount returns failure."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        char.db.carried_scales = 100
        context = {"character": char}
        action = {"action_type": "give_scales", "amount": -10}
        success, msg = execute_action(action, context)
        self.assertFalse(success)

    def test_no_character_fails(self):
        """give_scales with no character in context fails gracefully."""
        from world.action_vocabulary import execute_action

        action = {"action_type": "give_scales", "amount": 50}
        success, msg = execute_action(action, {})
        self.assertFalse(success)
        self.assertIn("no character", msg.lower())

    def test_sends_notification_message(self):
        """give_scales sends a [+N Scales] message to the character."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        char.db.carried_scales = 0
        context = {"character": char}
        action = {"action_type": "give_scales", "amount": 100}
        execute_action(action, context)
        char.msg.assert_called_once()
        msg_text = char.msg.call_args[0][0]
        self.assertIn("100", msg_text)
        self.assertIn("Scales", msg_text)


class TestGiveSkillXpHandler(unittest.TestCase):
    """Test _handle_give_skill_xp action handler (D-14)."""

    def test_calls_accumulate_skill_use(self):
        """give_skill_xp calls accumulate_skill_use with correct args."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        context = {"character": char}
        action = {"action_type": "give_skill_xp", "skill_id": "combat", "count": 5}
        with patch("world.skill_engine.accumulate_skill_use") as mock_acc:
            success, msg = execute_action(action, context)
        self.assertTrue(success)
        mock_acc.assert_called_once_with(char, "combat", 5)

    def test_default_count_is_1(self):
        """give_skill_xp defaults to count=1 when not specified."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        context = {"character": char}
        action = {"action_type": "give_skill_xp", "skill_id": "herbalism"}
        with patch("world.skill_engine.accumulate_skill_use") as mock_acc:
            success, msg = execute_action(action, context)
        self.assertTrue(success)
        mock_acc.assert_called_once_with(char, "herbalism", 1)

    def test_missing_skill_id_fails(self):
        """give_skill_xp without skill_id returns failure."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        context = {"character": char}
        action = {"action_type": "give_skill_xp", "count": 5}
        success, msg = execute_action(action, context)
        self.assertFalse(success)
        self.assertIn("skill_id", msg.lower())

    def test_no_character_fails(self):
        """give_skill_xp with no character in context fails gracefully."""
        from world.action_vocabulary import execute_action

        action = {"action_type": "give_skill_xp", "skill_id": "combat", "count": 3}
        success, msg = execute_action(action, {})
        self.assertFalse(success)
        self.assertIn("no character", msg.lower())

    def test_sends_notification_message(self):
        """give_skill_xp sends a [+N Skill XP] message to the character."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        context = {"character": char}
        action = {"action_type": "give_skill_xp", "skill_id": "herbalism", "count": 3}
        with patch("world.skill_engine.accumulate_skill_use"):
            execute_action(action, context)
        char.msg.assert_called_once()
        msg_text = char.msg.call_args[0][0]
        self.assertIn("3", msg_text)
        self.assertIn("Herbalism", msg_text)


class TestModifyNodeFailureHandler(unittest.TestCase):
    """Test _handle_modify_node_failure action handler (D-14)."""

    def test_adjusts_failure_upward(self):
        """modify_node_failure increases failure by delta."""
        from world.action_vocabulary import execute_action

        zone_obj = MagicMock()
        script = MagicMock()
        script.db.failure = 50.0
        zone_obj.scripts.get.return_value = [script]

        with patch("evennia.search_tag", return_value=[zone_obj]):
            action = {"action_type": "modify_node_failure", "zone_id": "ashreach", "delta": 10}
            success, msg = execute_action(action, {})

        self.assertTrue(success)
        self.assertEqual(script.db.failure, 60.0)

    def test_adjusts_failure_downward(self):
        """modify_node_failure decreases failure by negative delta."""
        from world.action_vocabulary import execute_action

        zone_obj = MagicMock()
        script = MagicMock()
        script.db.failure = 50.0
        zone_obj.scripts.get.return_value = [script]

        with patch("evennia.search_tag", return_value=[zone_obj]):
            action = {"action_type": "modify_node_failure", "zone_id": "ashreach", "delta": -20}
            success, msg = execute_action(action, {})

        self.assertTrue(success)
        self.assertEqual(script.db.failure, 30.0)

    def test_clamps_to_zero(self):
        """Failure percentage cannot go below 0."""
        from world.action_vocabulary import execute_action

        zone_obj = MagicMock()
        script = MagicMock()
        script.db.failure = 10.0
        zone_obj.scripts.get.return_value = [script]

        with patch("evennia.search_tag", return_value=[zone_obj]):
            action = {"action_type": "modify_node_failure", "zone_id": "ashreach", "delta": -50}
            success, msg = execute_action(action, {})

        self.assertTrue(success)
        self.assertEqual(script.db.failure, 0.0)

    def test_clamps_to_100(self):
        """Failure percentage cannot exceed 100."""
        from world.action_vocabulary import execute_action

        zone_obj = MagicMock()
        script = MagicMock()
        script.db.failure = 90.0
        zone_obj.scripts.get.return_value = [script]

        with patch("evennia.search_tag", return_value=[zone_obj]):
            action = {"action_type": "modify_node_failure", "zone_id": "ashreach", "delta": 50}
            success, msg = execute_action(action, {})

        self.assertTrue(success)
        self.assertEqual(script.db.failure, 100.0)

    def test_missing_zone_fails(self):
        """modify_node_failure without zone_id returns failure."""
        from world.action_vocabulary import execute_action

        action = {"action_type": "modify_node_failure", "delta": 10}
        success, msg = execute_action(action, {})
        self.assertFalse(success)
        self.assertIn("zone_id", msg.lower())

    def test_zone_not_found_fails(self):
        """modify_node_failure with unknown zone_id returns failure."""
        from world.action_vocabulary import execute_action

        with patch("evennia.search_tag", return_value=[]):
            action = {"action_type": "modify_node_failure", "zone_id": "nonexistent", "delta": 10}
            success, msg = execute_action(action, {})

        self.assertFalse(success)
        self.assertIn("not found", msg.lower())

    def test_no_node_script_fails(self):
        """Zone without node_script returns failure."""
        from world.action_vocabulary import execute_action

        zone_obj = MagicMock()
        zone_obj.scripts.get.return_value = []

        with patch("evennia.search_tag", return_value=[zone_obj]):
            action = {"action_type": "modify_node_failure", "zone_id": "ashreach", "delta": 10}
            success, msg = execute_action(action, {})

        self.assertFalse(success)
        self.assertIn("node_script", msg.lower())

    def test_calls_update_state(self):
        """modify_node_failure calls script._update_state after adjusting failure."""
        from world.action_vocabulary import execute_action

        zone_obj = MagicMock()
        script = MagicMock()
        script.db.failure = 40.0
        zone_obj.scripts.get.return_value = [script]

        with patch("evennia.search_tag", return_value=[zone_obj]):
            action = {"action_type": "modify_node_failure", "zone_id": "ashreach", "delta": 10}
            execute_action(action, {})

        script._update_state.assert_called_once_with(40.0, 50.0)
