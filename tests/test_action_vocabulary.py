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
        """ACTION_HANDLERS has exactly 22 keys."""
        from world.action_vocabulary import ACTION_HANDLERS

        self.assertEqual(len(ACTION_HANDLERS), 22)

    def test_all_expected_action_types_present(self):
        """All 21 required action types are registered."""
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
            "discover_flight_point",
            "open_dialogue",
            "log_world_event",
            "modify_attunement",
            "add_room_flag",
            "give_scales",
            "give_skill_xp",
            "grant_practice",
            "grant_access",
            "release_social_claim",
            "modify_node_failure",
            "learn_recipe",
            "record_social_event",
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
        char.move_to.assert_called_once_with(target_room, quiet=False, move_hooks=False)

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
        char.move_to.assert_called_once_with(mob_room, quiet=False, move_hooks=False)

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
             patch("world.quest_engine.accept_quest", return_value=(True, "Quest accepted")) as mock_accept, \
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
        action = {"action_type": "give_skill_xp", "skill_id": "reflexes", "count": 5}
        with patch("world.skill_engine.accumulate_skill_use") as mock_acc:
            success, msg = execute_action(action, context)
        self.assertTrue(success)
        mock_acc.assert_called_once_with(char, "reflexes", 5)

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

    def test_unknown_skill_id_fails_without_accumulating(self):
        """give_skill_xp rejects stale or misspelled skill ids."""
        from world.action_vocabulary import execute_action

        char = MagicMock()
        context = {"character": char}
        action = {"action_type": "give_skill_xp", "skill_id": "not_a_skill", "count": 5}
        with patch("world.skill_engine.accumulate_skill_use") as mock_acc:
            success, msg = execute_action(action, context)
        self.assertFalse(success)
        self.assertIn("unknown skill_id", msg)
        mock_acc.assert_not_called()

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


class TestGrantPracticeHandler(unittest.TestCase):
    """Test grant_practice action handler."""

    def test_calls_practice_engine_with_action_payload_and_context(self):
        from world.action_vocabulary import execute_action

        char = MagicMock()
        context = {"character": char, "room": MagicMock(), "args": "canal winch"}
        action = {
            "action_type": "grant_practice",
            "opportunity_id": "vp_canal_winch_repair",
            "verb": "repair",
            "target": "canal winch",
        }

        with patch("world.practice_engine.resolve_practice_opportunity", return_value=(True, "")) as mock_resolve:
            success, msg = execute_action(action, context)

        self.assertTrue(success)
        self.assertEqual(msg, "")
        mock_resolve.assert_called_once_with(action, context)


class TestRecordSocialEventHandler(EvenniaTest):
    """record_social_event writes durable Social Web state from action rewards."""

    def _warden_report_social_action(self):
        return {
            "action_type": "record_social_event",
            "nodes": [
                {
                    "node_type": "player",
                    "identifier_template": "{character_id}",
                    "display_name_template": "{character_key}",
                    "zone_id": "vaels_crossing",
                    "settlement_id": "vaels_crossing",
                },
                {
                    "node_type": "npc",
                    "identifier": "npc_warden_agent_calloway",
                    "display_name": "Agent Calloway",
                    "zone_id": "vaels_crossing",
                    "settlement_id": "vaels_crossing",
                    "faction_id": "wardens",
                },
                {
                    "node_type": "npc",
                    "identifier": "npc_warden_outpost_commander",
                    "display_name": "Commander Harven",
                    "zone_id": "ashreach_plains",
                    "settlement_id": "ashreach_outpost",
                    "faction_id": "wardens",
                },
                {
                    "node_type": "npc",
                    "identifier": "npc_innkeeper_whistle",
                    "display_name": "Whistle",
                    "zone_id": "vaels_crossing",
                    "settlement_id": "vaels_crossing",
                },
            ],
            "edges": [
                {
                    "source_node_key": "npc:npc_warden_agent_calloway",
                    "target_node_key": "npc:npc_warden_outpost_commander",
                    "edge_type": "warden_report",
                    "directionality": "one_way",
                    "trust": 0.95,
                    "latency_seconds": 0,
                    "scope_tags": ["warden", "report", "quest"],
                }
            ],
            "fact": {
                "fact_key_template": "fact:{character_id}:vc_q_warden_report:delivered",
                "subject_node_key_template": "player:{character_id}",
                "actor_node_key_template": "player:{character_id}",
                "scope_node_key": "npc:npc_warden_agent_calloway",
                "event_type": "quest_completed",
                "summary": "The player delivered Calloway's sealed field report.",
                "tags": ["reliable", "warden", "report", "quest"],
                "visibility": "institutional",
                "evidence": {"quest_id": "vc_q_warden_report", "source": "quest_reward"},
            },
            "claim": {
                "claim_key_template": "claim:calloway:{character_id}:vc_q_warden_report:delivered",
                "speaker_node_key": "npc:npc_warden_agent_calloway",
                "subject_node_key_template": "player:{character_id}",
                "claim_type": "report",
                "summary": "Calloway reports that the player carried Warden business cleanly.",
                "status": "supported",
                "confidence": 1.0,
                "bias_tags": ["warden", "report", "quest"],
            },
            "knowledge": [
                {
                    "node_key": "npc:npc_warden_agent_calloway",
                    "fact_key_template": "fact:{character_id}:vc_q_warden_report:delivered",
                    "channel": "official_report",
                    "confidence": 1.0,
                    "spreading": False,
                },
                {
                    "node_key": "npc:npc_warden_agent_calloway",
                    "claim_key_template": "claim:calloway:{character_id}:vc_q_warden_report:delivered",
                    "channel": "official_report",
                    "confidence": 1.0,
                    "spreading": True,
                }
            ],
            "propagate": {
                "source_node_key": "npc:npc_warden_agent_calloway",
                "claim_key_template": "claim:calloway:{character_id}:vc_q_warden_report:delivered",
                "required": True,
            },
        }

    def test_records_claim_propagates_route_and_is_idempotent(self):
        from world.action_vocabulary import execute_action
        from world.models import (
            SocialClaim,
            SocialEdge,
            SocialFact,
            SocialKnowledge,
            SocialNode,
            SocialTrace,
        )

        action = self._warden_report_social_action()
        action["edges"][0]["required_tags"] = ["warden", "report"]
        action["edges"][0]["blocked_tags"] = ["sealed"]

        for _repeat in range(2):
            success, msg = execute_action(action, {"character": self.char1})
            self.assertTrue(success, msg)

        fact_key = f"fact:{self.char1.id}:vc_q_warden_report:delivered"
        claim_key = f"claim:calloway:{self.char1.id}:vc_q_warden_report:delivered"
        player = SocialNode.objects.get(node_key=f"player:{self.char1.id}")
        calloway = SocialNode.objects.get(node_key="npc:npc_warden_agent_calloway")
        harven = SocialNode.objects.get(node_key="npc:npc_warden_outpost_commander")
        whistle = SocialNode.objects.get(node_key="npc:npc_innkeeper_whistle")
        claim = SocialClaim.objects.get(claim_key=claim_key)

        self.assertEqual(player.display_name, self.char1.key)
        self.assertEqual(
            SocialNode.objects.filter(
                node_key__in=[
                    player.node_key,
                    calloway.node_key,
                    harven.node_key,
                    whistle.node_key,
                ]
            ).count(),
            4,
        )
        edge = SocialEdge.objects.get(
            source_node=calloway,
            target_node=harven,
            edge_type="warden_report",
        )
        self.assertEqual(SocialEdge.objects.filter(pk=edge.pk).count(), 1)
        self.assertEqual(edge.required_tags, ["warden", "report"])
        self.assertEqual(edge.blocked_tags, ["sealed"])
        self.assertEqual(SocialFact.objects.filter(fact_key=fact_key).count(), 1)
        self.assertEqual(SocialClaim.objects.filter(claim_key=claim_key).count(), 1)
        self.assertTrue(
            SocialKnowledge.objects.filter(
                node=calloway,
                fact__fact_key=fact_key,
                claim__isnull=True,
            ).exists()
        )
        self.assertEqual(
            SocialKnowledge.objects.filter(claim__claim_key=claim_key).count(),
            2,
        )
        self.assertTrue(
            SocialKnowledge.objects.filter(node=calloway, claim=claim).exists()
        )
        harven_knowledge = SocialKnowledge.objects.get(node=harven, claim=claim)
        self.assertEqual(harven_knowledge.edge.edge_type, "warden_report")
        self.assertFalse(
            SocialKnowledge.objects.filter(node=whistle, claim=claim).exists()
        )
        self.assertEqual(
            SocialTrace.objects.filter(knowledge=harven_knowledge).count(),
            1,
        )
        self.assertEqual(
            SocialTrace.objects.get(knowledge=harven_knowledge).edge.edge_type,
            "warden_report",
        )
        self.assertIsNone(harven_knowledge.fact)

    def test_knowledge_payload_must_be_explicit_and_unambiguous(self):
        from world.action_vocabulary import execute_action

        for knowledge_def in (
            {
                "node_key": "npc:npc_warden_agent_calloway",
                "channel": "official_report",
            },
            {
                "node_key": "npc:npc_warden_agent_calloway",
                "fact_key_template": "fact:{character_id}:vc_q_warden_report:delivered",
                "claim_key_template": "claim:calloway:{character_id}:vc_q_warden_report:delivered",
                "channel": "official_report",
            },
        ):
            action = self._warden_report_social_action()
            action["knowledge"] = [knowledge_def]

            success, message = execute_action(action, {"character": self.char1})

            self.assertFalse(success)
            self.assertIn(
                "knowledge 0 must name exactly one of fact_key or claim_key",
                message,
            )

    def test_propagation_payload_must_be_explicit_and_unambiguous(self):
        from world.action_vocabulary import execute_action

        for propagate_def in (
            {
                "source_node_key": "npc:npc_warden_agent_calloway",
            },
            {
                "source_node_key": "npc:npc_warden_agent_calloway",
                "fact_key_template": "fact:{character_id}:vc_q_warden_report:delivered",
                "claim_key_template": "claim:calloway:{character_id}:vc_q_warden_report:delivered",
            },
        ):
            action = self._warden_report_social_action()
            action["propagate"] = propagate_def

            success, message = execute_action(action, {"character": self.char1})

            self.assertFalse(success)
            self.assertIn(
                "propagate 0 must name exactly one of fact_key or claim_key",
                message,
            )

    def test_missing_character_fails(self):
        from world.action_vocabulary import execute_action

        success, msg = execute_action(self._warden_report_social_action(), {})

        self.assertFalse(success)
        self.assertIn("character", msg)

    def test_required_propagation_failure_rolls_back_social_writes(self):
        from world.action_vocabulary import execute_action
        from world.models import SocialFact, SocialNode

        action = self._warden_report_social_action()
        action["edges"][0]["scope_tags"] = ["market"]

        success, msg = execute_action(action, {"character": self.char1})

        self.assertFalse(success)
        self.assertIn("required propagation", msg)
        self.assertFalse(
            SocialFact.objects.filter(
                fact_key=f"fact:{self.char1.id}:vc_q_warden_report:delivered"
            ).exists()
        )
        self.assertFalse(
            SocialNode.objects.filter(
                node_key="npc:npc_warden_agent_calloway"
            ).exists()
        )


class TestModifyNodeFailureHandler(unittest.TestCase):
    """Test _handle_modify_node_failure action handler (D-14)."""

    def test_adjusts_failure_upward(self):
        """modify_node_failure increases failure by delta."""
        from world.action_vocabulary import execute_action

        zone_obj = MagicMock()
        script = MagicMock()
        script.db.failure = 50.0
        zone_obj.scripts.get.return_value = [script]

        with patch("world.action_vocabulary.search_objects_by_exact_tag", return_value=[zone_obj]):
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

        with patch("world.action_vocabulary.search_objects_by_exact_tag", return_value=[zone_obj]):
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

        with patch("world.action_vocabulary.search_objects_by_exact_tag", return_value=[zone_obj]):
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

        with patch("world.action_vocabulary.search_objects_by_exact_tag", return_value=[zone_obj]):
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

        with patch("world.action_vocabulary.search_objects_by_exact_tag", return_value=[]):
            action = {"action_type": "modify_node_failure", "zone_id": "nonexistent", "delta": 10}
            success, msg = execute_action(action, {})

        self.assertFalse(success)
        self.assertIn("not found", msg.lower())

    def test_no_node_script_fails(self):
        """Zone without node_script returns failure."""
        from world.action_vocabulary import execute_action

        zone_obj = MagicMock()
        zone_obj.scripts.get.return_value = []

        with patch("world.action_vocabulary.search_objects_by_exact_tag", return_value=[zone_obj]):
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

        with patch("world.action_vocabulary.search_objects_by_exact_tag", return_value=[zone_obj]):
            action = {"action_type": "modify_node_failure", "zone_id": "ashreach", "delta": 10}
            execute_action(action, {})

        script._update_state.assert_called_once_with(40.0, 50.0)
