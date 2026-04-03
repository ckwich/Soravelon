"""
Tests for the quest engine module (Phase 11 Plan 01, Task 2).

Uses unittest.TestCase + MagicMock for pure-logic tests. Django models
are mocked -- no Evennia DB setup needed.

TDD RED phase: all tests written first.
"""

import unittest
from unittest.mock import MagicMock, patch, PropertyMock


# ---------------------------------------------------------------------------
# Helper: build a mock CharacterQuest
# ---------------------------------------------------------------------------

def _make_cq(quest_id, status="active", progress=None):
    """Create a mock CharacterQuest record."""
    cq = MagicMock()
    cq.quest_id = quest_id
    cq.status = status
    cq.progress = dict(progress or {})
    cq.completed_at = None
    cq.save = MagicMock()
    cq.refresh_from_db = MagicMock()
    cq.delete = MagicMock()
    return cq


# ---------------------------------------------------------------------------
# Test: accept_quest
# ---------------------------------------------------------------------------

class TestAcceptQuest(unittest.TestCase):
    """Tests for accept_quest function."""

    @patch("world.quest_engine.CharacterQuest")
    def test_accept_creates_record(self, MockCQ):
        """accept_quest creates a CharacterQuest with status=active."""
        from world.quest_engine import accept_quest

        char = MagicMock()
        # No active quests
        MockCQ.objects.filter.return_value.count.return_value = 0
        MockCQ.objects.filter.return_value.exists.return_value = False

        spec = {"quest_id": "test_q", "name": "Test Quest"}
        ok, msg = accept_quest(char, "test_q", spec)

        self.assertTrue(ok)
        MockCQ.objects.create.assert_called_once()

    @patch("world.quest_engine.CharacterQuest")
    def test_accept_rejects_at_cap(self, MockCQ):
        """accept_quest rejects when 5 active quests exist (D-02)."""
        from world.quest_engine import accept_quest

        char = MagicMock()
        # 5 active quests
        filter_mock = MagicMock()
        filter_mock.count.return_value = 5
        filter_mock.exists.return_value = False
        MockCQ.objects.filter.return_value = filter_mock

        spec = {"quest_id": "test_q", "name": "Test Quest"}
        ok, msg = accept_quest(char, "test_q", spec)

        self.assertFalse(ok)
        self.assertIn("5", msg)
        MockCQ.objects.create.assert_not_called()

    @patch("world.quest_engine.CharacterQuest")
    def test_accept_rejects_one_chance_failed(self, MockCQ):
        """accept_quest rejects one_chance quest already failed (D-03)."""
        from world.quest_engine import accept_quest

        char = MagicMock()
        # Not at cap
        count_filter = MagicMock()
        count_filter.count.return_value = 0

        def filter_side_effect(**kwargs):
            if kwargs.get("status") == "active" and "quest_id" not in kwargs:
                return count_filter
            if kwargs.get("status") == "failed":
                mock = MagicMock()
                mock.exists.return_value = True
                return mock
            if kwargs.get("status") == "active" and "quest_id" in kwargs:
                mock = MagicMock()
                mock.exists.return_value = False
                return mock
            return MagicMock(count=MagicMock(return_value=0), exists=MagicMock(return_value=False))

        MockCQ.objects.filter.side_effect = filter_side_effect

        spec = {"quest_id": "test_q", "name": "Test Quest", "one_chance": True}
        ok, msg = accept_quest(char, "test_q", spec)

        self.assertFalse(ok)
        MockCQ.objects.create.assert_not_called()

    @patch("world.quest_engine.CharacterQuest")
    def test_accept_rejects_already_active(self, MockCQ):
        """accept_quest rejects quest that is already active."""
        from world.quest_engine import accept_quest

        char = MagicMock()
        count_filter = MagicMock()
        count_filter.count.return_value = 1

        def filter_side_effect(**kwargs):
            if kwargs.get("status") == "active" and "quest_id" not in kwargs:
                return count_filter
            if kwargs.get("status") == "active" and "quest_id" in kwargs:
                mock = MagicMock()
                mock.exists.return_value = True
                return mock
            return MagicMock(count=MagicMock(return_value=0), exists=MagicMock(return_value=False))

        MockCQ.objects.filter.side_effect = filter_side_effect

        spec = {"quest_id": "test_q", "name": "Test Quest"}
        ok, msg = accept_quest(char, "test_q", spec)

        self.assertFalse(ok)
        MockCQ.objects.create.assert_not_called()

    @patch("world.quest_engine.CharacterQuest")
    def test_accept_returns_bool_str(self, MockCQ):
        """accept_quest returns (bool, str) tuple."""
        from world.quest_engine import accept_quest

        char = MagicMock()
        MockCQ.objects.filter.return_value.count.return_value = 0
        MockCQ.objects.filter.return_value.exists.return_value = False

        result = accept_quest(char, "test_q", {"quest_id": "test_q"})
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)
        self.assertIsInstance(result[1], str)


# ---------------------------------------------------------------------------
# Test: abandon_quest
# ---------------------------------------------------------------------------

class TestAbandonQuest(unittest.TestCase):
    """Tests for abandon_quest function."""

    @patch("world.quest_engine.CharacterQuest")
    def test_abandon_sets_status(self, MockCQ):
        """abandon_quest sets status to abandoned (D-04)."""
        from world.quest_engine import abandon_quest

        char = MagicMock()
        cq = _make_cq("test_q", status="active")
        MockCQ.objects.filter.return_value.first.return_value = cq

        ok, msg = abandon_quest(char, "test_q")

        self.assertTrue(ok)
        self.assertEqual(cq.status, "abandoned")
        cq.save.assert_called()

    @patch("world.quest_engine.CharacterQuest")
    def test_abandon_nonexistent_returns_false(self, MockCQ):
        """abandon_quest returns False for quest not found."""
        from world.quest_engine import abandon_quest

        char = MagicMock()
        MockCQ.objects.filter.return_value.first.return_value = None

        ok, msg = abandon_quest(char, "nonexistent_q")

        self.assertFalse(ok)


# ---------------------------------------------------------------------------
# Test: _normalize_quest_spec
# ---------------------------------------------------------------------------

class TestNormalizeQuestSpec(unittest.TestCase):
    """Tests for _normalize_quest_spec internal function."""

    def test_already_has_objectives(self):
        """Spec with objectives list is returned as-is."""
        from world.quest_engine import _normalize_quest_spec

        spec = {
            "quest_id": "q1",
            "objectives": [{"type": "kill", "target": "wolf", "count": 5}],
        }
        result = _normalize_quest_spec(spec)
        self.assertEqual(len(result["objectives"]), 1)
        self.assertEqual(result["objectives"][0]["type"], "kill")

    def test_flat_format_converts(self):
        """Flat format (objective_type/target/count) converts to objectives list."""
        from world.quest_engine import _normalize_quest_spec

        spec = {
            "quest_id": "q2",
            "objective_type": "kill",
            "objective_target": "sewer_rat",
            "objective_count": 10,
        }
        result = _normalize_quest_spec(spec)
        self.assertIn("objectives", result)
        self.assertEqual(len(result["objectives"]), 1)
        obj = result["objectives"][0]
        self.assertEqual(obj["type"], "kill")
        self.assertEqual(obj["target"], "sewer_rat")
        self.assertEqual(obj["count"], 10)

    def test_normalizes_gather_to_collect(self):
        """Non-MVP types like 'gather' normalize to 'collect'."""
        from world.quest_engine import _normalize_quest_spec

        spec = {
            "quest_id": "q3",
            "objective_type": "gather",
            "objective_target": "herb",
            "objective_count": 5,
        }
        result = _normalize_quest_spec(spec)
        self.assertEqual(result["objectives"][0]["type"], "collect")

    def test_normalizes_discover_to_investigate(self):
        """'discover' normalizes to 'investigate'."""
        from world.quest_engine import _normalize_quest_spec

        spec = {
            "quest_id": "q4",
            "objective_type": "discover",
            "objective_target": "hidden_cave",
            "objective_count": 1,
        }
        result = _normalize_quest_spec(spec)
        self.assertEqual(result["objectives"][0]["type"], "investigate")


# ---------------------------------------------------------------------------
# Test: check_kill_objectives
# ---------------------------------------------------------------------------

class TestCheckKillObjectives(unittest.TestCase):
    """Tests for check_kill_objectives."""

    @patch("world.quest_engine._check_quest_completion")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_kill_increments_progress(self, MockCQ, mock_get_spec, mock_check):
        """Killing a matching mob increments the kill objective progress."""
        from world.quest_engine import check_kill_objectives

        char = MagicMock()
        mob = MagicMock()
        mob.db.mob_template = "sewer_rat"
        mob.db.mob_id = None

        cq = _make_cq("rat_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "rat_quest",
            "objectives": [{"type": "kill", "target": "sewer_rat", "count": 10}],
        }

        check_kill_objectives(char, mob)

        # Progress should have been incremented
        self.assertEqual(cq.progress.get("kill_sewer_rat", 0), 1)
        cq.save.assert_called()

    @patch("world.quest_engine._check_quest_completion")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_kill_matches_mob_id(self, MockCQ, mock_get_spec, mock_check):
        """Kill objective also matches mob.db.mob_id for named mobs."""
        from world.quest_engine import check_kill_objectives

        char = MagicMock()
        mob = MagicMock()
        mob.db.mob_template = "generic_wolf"
        mob.db.mob_id = "alpha_wolf_boss"

        cq = _make_cq("wolf_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "wolf_quest",
            "objectives": [{"type": "kill", "target": "alpha_wolf_boss", "count": 1}],
        }

        check_kill_objectives(char, mob)

        self.assertEqual(cq.progress.get("kill_alpha_wolf_boss", 0), 1)

    @patch("world.quest_engine._check_quest_completion")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_kill_no_match_no_increment(self, MockCQ, mock_get_spec, mock_check):
        """Killing a non-matching mob does not increment progress."""
        from world.quest_engine import check_kill_objectives

        char = MagicMock()
        mob = MagicMock()
        mob.db.mob_template = "bandit"
        mob.db.mob_id = None

        cq = _make_cq("rat_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "rat_quest",
            "objectives": [{"type": "kill", "target": "sewer_rat", "count": 10}],
        }

        check_kill_objectives(char, mob)

        self.assertEqual(cq.progress.get("kill_sewer_rat", 0), 0)


# ---------------------------------------------------------------------------
# Test: check_collect_objectives
# ---------------------------------------------------------------------------

class TestCheckCollectObjectives(unittest.TestCase):
    """Tests for check_collect_objectives."""

    @patch("world.quest_engine._check_quest_completion")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_collect_increments_progress(self, MockCQ, mock_get_spec, mock_check):
        """Picking up a matching item increments the collect objective progress."""
        from world.quest_engine import check_collect_objectives

        char = MagicMock()
        item = MagicMock()
        item.db.item_tag = "fang"
        item.tags = MagicMock()
        item.tags.get.return_value = None

        cq = _make_cq("fang_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "fang_quest",
            "objectives": [{"type": "collect", "target": "fang", "count": 5}],
        }

        check_collect_objectives(char, item)

        self.assertEqual(cq.progress.get("collect_fang", 0), 1)


# ---------------------------------------------------------------------------
# Test: check_investigate_objectives
# ---------------------------------------------------------------------------

class TestCheckInvestigateObjectives(unittest.TestCase):
    """Tests for check_investigate_objectives."""

    @patch("world.quest_engine._check_quest_completion")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_investigate_completes_on_room_visit(self, MockCQ, mock_get_spec, mock_check):
        """Entering a matching room completes the investigate objective."""
        from world.quest_engine import check_investigate_objectives

        char = MagicMock()
        room = MagicMock()
        room.db.room_id = "hidden_chamber"

        cq = _make_cq("explore_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "explore_quest",
            "objectives": [{"type": "investigate", "target": "hidden_chamber", "count": 1}],
        }

        check_investigate_objectives(char, room)

        self.assertEqual(cq.progress.get("investigate_hidden_chamber", 0), 1)


# ---------------------------------------------------------------------------
# Test: check_deliver_objectives
# ---------------------------------------------------------------------------

class TestCheckDeliverObjectives(unittest.TestCase):
    """Tests for check_deliver_objectives."""

    @patch("world.quest_engine._check_quest_completion")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_deliver_completes_with_item_and_npc(self, MockCQ, mock_get_spec, mock_check):
        """Talking to target NPC while carrying target item completes delivery."""
        from world.quest_engine import check_deliver_objectives

        char = MagicMock()
        npc = MagicMock()
        npc.db.npc_id = "npc_warden"

        # Character has the delivery item
        item = MagicMock()
        item.db.item_tag = "warden_report"
        char.contents = [item]

        cq = _make_cq("deliver_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "deliver_quest",
            "objectives": [{
                "type": "deliver",
                "target": "npc_warden",
                "item_tag": "warden_report",
                "count": 1,
            }],
        }

        check_deliver_objectives(char, npc)

        self.assertEqual(cq.progress.get("deliver_npc_warden", 0), 1)

    @patch("world.quest_engine._check_quest_completion")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_deliver_fails_without_item(self, MockCQ, mock_get_spec, mock_check):
        """Talking to NPC without the item does NOT complete delivery."""
        from world.quest_engine import check_deliver_objectives

        char = MagicMock()
        npc = MagicMock()
        npc.db.npc_id = "npc_warden"
        char.contents = []  # No items

        cq = _make_cq("deliver_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "deliver_quest",
            "objectives": [{
                "type": "deliver",
                "target": "npc_warden",
                "item_tag": "warden_report",
                "count": 1,
            }],
        }

        check_deliver_objectives(char, npc)

        self.assertEqual(cq.progress.get("deliver_npc_warden", 0), 0)


# ---------------------------------------------------------------------------
# Test: check_talk_to_objectives
# ---------------------------------------------------------------------------

class TestCheckTalkToObjectives(unittest.TestCase):
    """Tests for check_talk_to_objectives."""

    @patch("world.quest_engine._check_quest_completion")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_talk_to_completes_on_npc_match(self, MockCQ, mock_get_spec, mock_check):
        """Talking to matching NPC completes the talk_to objective."""
        from world.quest_engine import check_talk_to_objectives

        char = MagicMock()
        npc = MagicMock()
        npc.db.npc_id = "npc_elder"

        cq = _make_cq("talk_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "talk_quest",
            "objectives": [{"type": "talk_to", "target": "npc_elder", "count": 1}],
        }

        check_talk_to_objectives(char, npc)

        self.assertEqual(cq.progress.get("talk_to_npc_elder", 0), 1)


# ---------------------------------------------------------------------------
# Test: _check_quest_completion
# ---------------------------------------------------------------------------

class TestCheckQuestCompletion(unittest.TestCase):
    """Tests for _check_quest_completion."""

    @patch("world.quest_engine._pay_rewards")
    def test_completes_when_all_objectives_met(self, mock_pay):
        """Quest completes when all objectives are met."""
        from world.quest_engine import _check_quest_completion

        char = MagicMock()
        cq = _make_cq("q1", progress={"kill_wolf": 5})

        spec = {
            "quest_id": "q1",
            "name": "Wolf Hunt",
            "objectives": [{"type": "kill", "target": "wolf", "count": 5}],
            "rewards": [{"action_type": "echo", "message": "Quest complete!"}],
        }

        _check_quest_completion(char, cq, spec)

        self.assertEqual(cq.status, "complete")
        self.assertIsNotNone(cq.completed_at)
        mock_pay.assert_called_once()

    @patch("world.quest_engine._pay_rewards")
    def test_no_complete_when_progress_incomplete(self, mock_pay):
        """Quest does not complete when objectives are not met."""
        from world.quest_engine import _check_quest_completion

        char = MagicMock()
        cq = _make_cq("q1", progress={"kill_wolf": 3})

        spec = {
            "quest_id": "q1",
            "objectives": [{"type": "kill", "target": "wolf", "count": 5}],
        }

        _check_quest_completion(char, cq, spec)

        self.assertEqual(cq.status, "active")  # Not changed
        mock_pay.assert_not_called()

    @patch("world.quest_engine._pay_rewards")
    def test_chain_sets_pending_quest(self, mock_pay):
        """On completion, next_quest_id sets ndb.pending_quest_offer (D-05)."""
        from world.quest_engine import _check_quest_completion

        char = MagicMock()
        char.ndb = MagicMock()
        cq = _make_cq("q1", progress={"kill_wolf": 5})

        spec = {
            "quest_id": "q1",
            "name": "Wolf Hunt",
            "objectives": [{"type": "kill", "target": "wolf", "count": 5}],
            "rewards": [],
            "next_quest_id": "q2_sequel",
        }

        _check_quest_completion(char, cq, spec)

        self.assertEqual(cq.status, "complete")
        self.assertEqual(char.ndb.pending_quest_offer, "q2_sequel")


# ---------------------------------------------------------------------------
# Test: get_available_quest_for_npc
# ---------------------------------------------------------------------------

class TestGetAvailableQuestForNpc(unittest.TestCase):
    """Tests for get_available_quest_for_npc."""

    @patch("world.quest_engine.CharacterQuest")
    @patch("world.quest_engine._get_all_quest_specs")
    def test_returns_quest_for_npc(self, mock_all_specs, MockCQ):
        """get_available_quest_for_npc returns a quest spec for matching NPC."""
        from world.quest_engine import get_available_quest_for_npc

        npc = MagicMock()
        npc.db.npc_id = "npc_barkeep"
        char = MagicMock()

        mock_all_specs.return_value = [
            {"quest_id": "q1", "quest_giver": "npc_barkeep", "name": "Rat Problem"},
        ]
        MockCQ.objects.filter.return_value.exists.return_value = False
        MockCQ.objects.filter.return_value.values_list.return_value = []

        result = get_available_quest_for_npc(npc, char)

        self.assertIsNotNone(result)
        self.assertEqual(result["quest_id"], "q1")

    @patch("world.quest_engine.CharacterQuest")
    @patch("world.quest_engine._get_all_quest_specs")
    def test_returns_none_if_already_active(self, mock_all_specs, MockCQ):
        """Returns None if the NPC's quest is already active."""
        from world.quest_engine import get_available_quest_for_npc

        npc = MagicMock()
        npc.db.npc_id = "npc_barkeep"
        char = MagicMock()

        mock_all_specs.return_value = [
            {"quest_id": "q1", "quest_giver": "npc_barkeep", "name": "Rat Problem"},
        ]

        # Build separate mocks for each chained filter call
        existing_qs = MagicMock()
        active_qs = MagicMock()
        active_qs.values_list.return_value = ["q1"]
        complete_qs = MagicMock()
        complete_qs.values_list.return_value = []
        failed_qs = MagicMock()
        failed_qs.values_list.return_value = []

        def filter_side_effect(**kwargs):
            if "status" not in kwargs:
                return existing_qs
            if kwargs.get("status") == "active":
                return active_qs
            if kwargs.get("status") == "complete":
                return complete_qs
            if kwargs.get("status") == "failed":
                return failed_qs
            return MagicMock(values_list=MagicMock(return_value=[]))

        MockCQ.objects.filter.side_effect = filter_side_effect
        existing_qs.filter.side_effect = filter_side_effect

        result = get_available_quest_for_npc(npc, char)

        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# Test: get_active_quests / get_quest_detail
# ---------------------------------------------------------------------------

class TestQuestQueries(unittest.TestCase):
    """Tests for get_active_quests and get_quest_detail."""

    @patch("world.quest_engine.CharacterQuest")
    def test_get_active_quests_filters_active(self, MockCQ):
        """get_active_quests returns only active quests."""
        from world.quest_engine import get_active_quests

        char = MagicMock()
        result = get_active_quests(char)

        MockCQ.objects.filter.assert_called_with(
            character=char, status="active"
        )

    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_get_quest_detail_returns_dict(self, MockCQ, mock_get_spec):
        """get_quest_detail returns a dict with quest info."""
        from world.quest_engine import get_quest_detail

        char = MagicMock()
        cq = _make_cq("q1", progress={"kill_wolf": 3})
        MockCQ.objects.filter.return_value.first.return_value = cq

        mock_get_spec.return_value = {
            "quest_id": "q1",
            "name": "Wolf Hunt",
            "description": "Kill 5 wolves.",
            "objectives": [{"type": "kill", "target": "wolf", "count": 5}],
            "rewards": [{"action_type": "give_scales", "amount": 100}],
        }

        result = get_quest_detail(char, "q1")

        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Wolf Hunt")
        self.assertIn("objectives", result)
        self.assertEqual(result["objectives"][0]["progress"], 3)
        self.assertEqual(result["objectives"][0]["count"], 5)


# ---------------------------------------------------------------------------
# Test: MAX_ACTIVE_QUESTS constant
# ---------------------------------------------------------------------------

class TestConstants(unittest.TestCase):
    """Tests for module-level constants."""

    def test_max_active_quests_is_5(self):
        """MAX_ACTIVE_QUESTS equals 5 per D-02."""
        from world.quest_engine import MAX_ACTIVE_QUESTS
        self.assertEqual(MAX_ACTIVE_QUESTS, 5)

    def test_objective_types(self):
        """OBJECTIVE_TYPES contains all 5 MVP types."""
        from world.quest_engine import OBJECTIVE_TYPES
        self.assertIn("kill", OBJECTIVE_TYPES)
        self.assertIn("collect", OBJECTIVE_TYPES)
        self.assertIn("investigate", OBJECTIVE_TYPES)
        self.assertIn("deliver", OBJECTIVE_TYPES)
        self.assertIn("talk_to", OBJECTIVE_TYPES)


if __name__ == "__main__":
    unittest.main()
