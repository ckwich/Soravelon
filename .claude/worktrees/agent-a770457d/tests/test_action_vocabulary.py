"""
Tests for the action vocabulary dispatch module (Plan 01-01, Task 1).

Tests written FIRST per TDD discipline — RED phase.
All tests must fail before world/action_vocabulary.py is created.
"""

from unittest.mock import MagicMock, patch
from evennia.utils.test_resources import EvenniaTest


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
    """ACTION_HANDLERS dict contains exactly 12 action types."""

    def test_handler_count(self):
        """ACTION_HANDLERS has exactly 12 keys."""
        from world.action_vocabulary import ACTION_HANDLERS

        self.assertEqual(len(ACTION_HANDLERS), 12)

    def test_all_expected_action_types_present(self):
        """All 12 required action types are registered."""
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


class TestStubActions(EvenniaTest):
    """Stub actions return (False, descriptive message) without crashing."""

    def test_set_quest_flag_stub(self):
        """set_quest_flag returns (False, not-implemented message)."""
        from world.action_vocabulary import execute_action

        success, msg = execute_action({"action_type": "set_quest_flag"}, {})
        self.assertFalse(success)
        self.assertIn("not", msg.lower())

    def test_open_dialogue_stub(self):
        """open_dialogue returns (False, not-implemented message)."""
        from world.action_vocabulary import execute_action

        success, msg = execute_action({"action_type": "open_dialogue"}, {})
        self.assertFalse(success)

    def test_spawn_mob_stub(self):
        """spawn_mob returns (False, not-implemented message)."""
        from world.action_vocabulary import execute_action

        success, msg = execute_action({"action_type": "spawn_mob"}, {})
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
