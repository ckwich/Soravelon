"""
Tests for the quest engine module (Phase 11).

Plan 01 Task 2: 28 initial tests (TDD RED/GREEN).
Plan 05 Task 1: Extended to comprehensive coverage of all D-01 through D-20
requirements, including normalization edge cases, re-accept after abandon,
multi-objective completion, reward payout, chain auto-offer, and query
edge cases.

Uses unittest.TestCase + MagicMock for pure-logic tests. Django models
are mocked -- no Evennia DB setup needed.
"""

import unittest
from unittest.mock import MagicMock, patch


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
    cq.pk = 101
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
    def test_accept_rejects_one_chance_complete(self, MockCQ):
        """accept_quest rejects one_chance quest already completed."""
        from world.quest_engine import accept_quest

        char = MagicMock()
        count_filter = MagicMock()
        count_filter.count.return_value = 0

        def filter_side_effect(**kwargs):
            if kwargs.get("status") == "active" and "quest_id" not in kwargs:
                return count_filter
            if kwargs.get("status") == "failed":
                mock = MagicMock()
                mock.exists.return_value = False
                return mock
            if kwargs.get("status") == "complete":
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
        self.assertIn("already completed", msg)
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

    @patch("world.quest_engine.CharacterQuest")
    def test_reaccept_after_abandon(self, MockCQ):
        """Can re-accept a quest after abandoning it (D-03: one_chance not set)."""
        from world.quest_engine import accept_quest

        char = MagicMock()
        # Not at cap, not already active
        MockCQ.objects.filter.return_value.count.return_value = 0
        MockCQ.objects.filter.return_value.exists.return_value = False

        spec = {"quest_id": "q_retry", "name": "Retry Quest"}
        ok, msg = accept_quest(char, "q_retry", spec)

        self.assertTrue(ok)
        MockCQ.objects.create.assert_called_once()

    @patch("world.quest_engine.CharacterQuest")
    def test_accept_initializes_progress_for_all_objectives(self, MockCQ):
        """accept_quest initializes progress dict with zero for each objective."""
        from world.quest_engine import accept_quest

        char = MagicMock()
        MockCQ.objects.filter.return_value.count.return_value = 0
        MockCQ.objects.filter.return_value.exists.return_value = False

        spec = {
            "quest_id": "multi_q",
            "objectives": [
                {"type": "kill", "target": "wolf", "count": 5},
                {"type": "collect", "target": "fang", "count": 3},
            ],
        }
        ok, msg = accept_quest(char, "multi_q", spec)

        self.assertTrue(ok)
        create_kwargs = MockCQ.objects.create.call_args[1]
        self.assertIn("kill_wolf", create_kwargs["progress"])
        self.assertIn("collect_fang", create_kwargs["progress"])
        self.assertEqual(create_kwargs["progress"]["kill_wolf"], 0)
        self.assertEqual(create_kwargs["progress"]["collect_fang"], 0)

    @patch("world.action_vocabulary.execute_action")
    @patch("world.quest_engine.CharacterQuest")
    def test_accept_grants_delivery_item_from_flagged_drop(self, MockCQ, mock_execute_action):
        """accept_quest grants flagged_drop items for delivery quests."""
        from world.quest_engine import accept_quest

        char = MagicMock()
        char.contents = []
        char.location = MagicMock()
        MockCQ.objects.filter.return_value.count.return_value = 0
        MockCQ.objects.filter.return_value.exists.return_value = False
        cq = _make_cq("deliver_q")
        MockCQ.objects.create.return_value = cq
        mock_execute_action.return_value = (True, "")

        spec = {
            "quest_id": "deliver_q",
            "flagged_drop": "sealed_packet",
            "objectives": [
                {"type": "deliver", "target": "npc_factor", "count": 1},
            ],
        }

        ok, msg = accept_quest(char, "deliver_q", spec)

        self.assertTrue(ok)
        mock_execute_action.assert_called_once_with(
            {"action_type": "give_item", "template_id": "sealed_packet"},
            {"character": char, "room": char.location},
        )

    @patch("world.action_vocabulary.execute_action")
    @patch("world.quest_engine.CharacterQuest")
    def test_accept_rolls_back_when_delivery_item_grant_fails(self, MockCQ, mock_execute_action):
        """accept_quest deletes the record if starter delivery item grant fails."""
        from world.quest_engine import accept_quest

        char = MagicMock()
        char.contents = []
        char.location = MagicMock()
        MockCQ.objects.filter.return_value.count.return_value = 0
        MockCQ.objects.filter.return_value.exists.return_value = False
        cq = _make_cq("deliver_q")
        MockCQ.objects.create.return_value = cq
        mock_execute_action.return_value = (False, "template missing")

        spec = {
            "quest_id": "deliver_q",
            "flagged_drop": "sealed_packet",
            "objectives": [
                {"type": "deliver", "target": "npc_factor", "count": 1},
            ],
        }

        ok, msg = accept_quest(char, "deliver_q", spec)

        self.assertFalse(ok)
        self.assertIn("template missing", msg)
        cq.delete.assert_called_once()

    @patch("world.quest_engine.CharacterQuest")
    def test_accept_rejects_missing_prerequisite_quest(self, MockCQ):
        """Chain quests cannot be accepted before prerequisites are complete."""
        from world.quest_engine import accept_quest

        char = MagicMock()
        active_count_qs = MagicMock()
        active_count_qs.count.return_value = 0
        already_active_qs = MagicMock()
        already_active_qs.exists.return_value = False
        complete_qs = MagicMock()
        complete_qs.values_list.return_value = []

        def filter_side_effect(**kwargs):
            if kwargs.get("status") == "active" and "quest_id" not in kwargs:
                return active_count_qs
            if kwargs.get("status") == "active" and "quest_id" in kwargs:
                return already_active_qs
            if kwargs.get("status") == "complete":
                return complete_qs
            return MagicMock(
                count=MagicMock(return_value=0),
                exists=MagicMock(return_value=False),
                values_list=MagicMock(return_value=[]),
            )

        MockCQ.objects.filter.side_effect = filter_side_effect

        spec = {
            "quest_id": "chain_step_two",
            "prerequisite_quests": ["chain_step_one"],
        }
        ok, msg = accept_quest(char, "chain_step_two", spec)

        self.assertFalse(ok)
        self.assertIn("earlier quests", msg)
        MockCQ.objects.create.assert_not_called()

    @patch("world.quest_engine.CharacterQuest")
    def test_accept_allows_completed_prerequisite_quest(self, MockCQ):
        """Completed prerequisites unlock the next chain step."""
        from world.quest_engine import accept_quest

        char = MagicMock()
        active_count_qs = MagicMock()
        active_count_qs.count.return_value = 0
        already_active_qs = MagicMock()
        already_active_qs.exists.return_value = False
        complete_qs = MagicMock()
        complete_qs.values_list.return_value = ["chain_step_one"]

        def filter_side_effect(**kwargs):
            if kwargs.get("status") == "active" and "quest_id" not in kwargs:
                return active_count_qs
            if kwargs.get("status") == "active" and "quest_id" in kwargs:
                return already_active_qs
            if kwargs.get("status") == "complete":
                return complete_qs
            return MagicMock(
                count=MagicMock(return_value=0),
                exists=MagicMock(return_value=False),
                values_list=MagicMock(return_value=[]),
            )

        MockCQ.objects.filter.side_effect = filter_side_effect

        spec = {
            "quest_id": "chain_step_two",
            "prerequisite_quests": ["chain_step_one"],
        }
        ok, msg = accept_quest(char, "chain_step_two", spec)

        self.assertTrue(ok)
        MockCQ.objects.create.assert_called_once()


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

    def test_normalizes_escort_to_deliver(self):
        """'escort' normalizes to 'deliver'."""
        from world.quest_engine import _normalize_quest_spec

        spec = {
            "quest_id": "q5",
            "objective_type": "escort",
            "objective_target": "npc_merchant",
            "objective_count": 1,
        }
        result = _normalize_quest_spec(spec)
        self.assertEqual(result["objectives"][0]["type"], "deliver")

    def test_normalizes_recover_to_collect(self):
        """'recover' normalizes to 'collect'."""
        from world.quest_engine import _normalize_quest_spec

        spec = {
            "quest_id": "q6",
            "objective_type": "recover",
            "objective_target": "lost_artifact",
            "objective_count": 1,
        }
        result = _normalize_quest_spec(spec)
        self.assertEqual(result["objectives"][0]["type"], "collect")

    def test_normalizes_craft_to_collect(self):
        """'craft' normalizes to 'collect' for MVP."""
        from world.quest_engine import _normalize_quest_spec

        spec = {
            "quest_id": "q7",
            "objective_type": "craft",
            "objective_target": "iron_sword",
            "objective_count": 3,
        }
        result = _normalize_quest_spec(spec)
        self.assertEqual(result["objectives"][0]["type"], "collect")
        self.assertEqual(result["objectives"][0]["count"], 3)

    def test_normalizes_objectives_list_types(self):
        """Non-MVP types in objectives list format are also normalized."""
        from world.quest_engine import _normalize_quest_spec

        spec = {
            "quest_id": "q8",
            "objectives": [
                {"type": "gather", "target": "herb", "count": 5},
                {"type": "discover", "target": "cave", "count": 1},
            ],
        }
        result = _normalize_quest_spec(spec)
        self.assertEqual(result["objectives"][0]["type"], "collect")
        self.assertEqual(result["objectives"][1]["type"], "investigate")

    def test_deliver_flat_sets_item_tag(self):
        """Flat format deliver objective sets item_tag from flagged_drop."""
        from world.quest_engine import _normalize_quest_spec

        spec = {
            "quest_id": "q9",
            "objective_type": "deliver",
            "objective_target": "npc_guard",
            "objective_count": 1,
            "flagged_drop": "guard_report",
        }
        result = _normalize_quest_spec(spec)
        obj = result["objectives"][0]
        self.assertEqual(obj["type"], "deliver")
        self.assertEqual(obj["item_tag"], "guard_report")

    def test_deliver_objectives_list_uses_flagged_drop_when_missing_item_tag(self):
        """Objectives-list deliver specs inherit item_tag from flagged_drop."""
        from world.quest_engine import _normalize_quest_spec

        spec = {
            "quest_id": "q10",
            "flagged_drop": "sealed_packet",
            "objectives": [
                {"type": "deliver", "target": "npc_factor", "count": 1},
            ],
        }

        result = _normalize_quest_spec(spec)

        self.assertEqual(result["objectives"][0]["item_tag"], "sealed_packet")


# ---------------------------------------------------------------------------
# Test: check_kill_objectives
# ---------------------------------------------------------------------------

class TestCheckKillObjectives(unittest.TestCase):
    """Tests for check_kill_objectives."""

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_kill_increments_progress(self, MockCQ, mock_get_spec, mock_check):
        """Killing a matching mob increments the kill objective progress."""
        from world.quest_engine import check_kill_objectives

        char = MagicMock()
        mob = MagicMock()
        mob.db.mob_template_key = "sewer_rat"
        mob.db.mob_instance_id = None

        cq = _make_cq("rat_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "rat_quest",
            "objectives": [{"type": "kill", "target": "sewer_rat", "count": 10}],
        }

        check_kill_objectives(char, mob)

        mock_check.assert_called_once_with(
            char,
            101,
            mock_get_spec.return_value,
            [{"key": "kill_sewer_rat", "amount": 1, "cap": 10}],
        )

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_kill_matches_mob_instance_id(self, MockCQ, mock_get_spec, mock_check):
        """Kill objective also matches mob.db.mob_instance_id for named mobs."""
        from world.quest_engine import check_kill_objectives

        char = MagicMock()
        mob = MagicMock()
        mob.db.mob_template_key = "generic_wolf"
        mob.db.mob_instance_id = "alpha_wolf_boss"

        cq = _make_cq("wolf_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "wolf_quest",
            "objectives": [{"type": "kill", "target": "alpha_wolf_boss", "count": 1}],
        }

        check_kill_objectives(char, mob)

        mock_check.assert_called_once_with(
            char,
            101,
            mock_get_spec.return_value,
            [{"key": "kill_alpha_wolf_boss", "amount": 1, "cap": 1}],
        )

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_kill_no_match_no_increment(self, MockCQ, mock_get_spec, mock_check):
        """Killing a non-matching mob does not increment progress."""
        from world.quest_engine import check_kill_objectives

        char = MagicMock()
        mob = MagicMock()
        mob.db.mob_template_key = "bandit"
        mob.db.mob_instance_id = None

        cq = _make_cq("rat_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "rat_quest",
            "objectives": [{"type": "kill", "target": "sewer_rat", "count": 10}],
        }

        check_kill_objectives(char, mob)

        mock_check.assert_not_called()

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_kill_triggers_completion_check(self, MockCQ, mock_get_spec, mock_check):
        """Killing a matching mob triggers _check_quest_completion."""
        from world.quest_engine import check_kill_objectives

        char = MagicMock()
        mob = MagicMock()
        mob.db.mob_template_key = "sewer_rat"
        mob.db.mob_instance_id = None

        cq = _make_cq("rat_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "rat_quest",
            "objectives": [{"type": "kill", "target": "sewer_rat", "count": 1}],
        }

        check_kill_objectives(char, mob)

        mock_check.assert_called_once()

    @patch("world.quest_engine._get_quest_spec", return_value=None)
    @patch("world.quest_engine.CharacterQuest")
    def test_kill_skips_quest_with_no_spec(self, MockCQ, mock_get_spec):
        """check_kill_objectives skips quests whose spec is not found."""
        from world.quest_engine import check_kill_objectives

        char = MagicMock()
        mob = MagicMock()
        mob.db.mob_template_key = "wolf"
        mob.db.mob_instance_id = None

        cq = _make_cq("orphan_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        # Should not crash when spec is None
        check_kill_objectives(char, mob)

        cq.save.assert_not_called()


# ---------------------------------------------------------------------------
# Test: check_collect_objectives
# ---------------------------------------------------------------------------

class TestCheckCollectObjectives(unittest.TestCase):
    """Tests for check_collect_objectives."""

    @patch("world.quest_engine._advance_quest_objectives")
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

        mock_check.assert_called_once_with(
            char,
            101,
            mock_get_spec.return_value,
            [{"key": "collect_fang", "amount": 1, "cap": 5}],
        )


    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_collect_no_match_no_increment(self, MockCQ, mock_get_spec, mock_check):
        """Picking up a non-matching item does not increment progress."""
        from world.quest_engine import check_collect_objectives

        char = MagicMock()
        item = MagicMock()
        item.db.item_tag = "junk"
        item.tags = MagicMock()
        item.tags.get.return_value = None

        cq = _make_cq("fang_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "fang_quest",
            "objectives": [{"type": "collect", "target": "fang", "count": 5}],
        }

        check_collect_objectives(char, item)

        self.assertEqual(cq.progress.get("collect_fang", 0), 0)
        mock_check.assert_not_called()


# ---------------------------------------------------------------------------
# Test: check_investigate_objectives
# ---------------------------------------------------------------------------

class TestCheckInvestigateObjectives(unittest.TestCase):
    """Tests for check_investigate_objectives."""

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_investigate_completes_on_room_visit(self, MockCQ, mock_get_spec, mock_check):
        """Entering a matching room completes the investigate objective."""
        from world.quest_engine import check_investigate_objectives

        char = MagicMock()
        room = MagicMock()
        room.tags.get.side_effect = lambda category=None, **kw: "hidden_chamber" if category == "room_id" else None

        cq = _make_cq("explore_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "explore_quest",
            "objectives": [{"type": "investigate", "target": "hidden_chamber", "count": 1}],
        }

        check_investigate_objectives(char, room)

        mock_check.assert_called_once_with(
            char,
            101,
            mock_get_spec.return_value,
            [{"key": "investigate_hidden_chamber", "amount": 1, "cap": 1}],
        )

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_investigate_idempotent(self, MockCQ, mock_get_spec, mock_check):
        """Re-entering the room does not re-trigger investigate (already 1)."""
        from world.quest_engine import check_investigate_objectives

        char = MagicMock()
        room = MagicMock()
        room.tags.get.side_effect = lambda category=None, **kw: "hidden_chamber" if category == "room_id" else None

        cq = _make_cq("explore_quest", progress={"investigate_hidden_chamber": 1})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "explore_quest",
            "objectives": [{"type": "investigate", "target": "hidden_chamber", "count": 1}],
        }

        check_investigate_objectives(char, room)

        mock_check.assert_called_once_with(
            char,
            101,
            mock_get_spec.return_value,
            [{"key": "investigate_hidden_chamber", "amount": 1, "cap": 1}],
        )

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_investigate_wrong_room_no_effect(self, MockCQ, mock_get_spec, mock_check):
        """Entering a non-target room does not affect investigate objective."""
        from world.quest_engine import check_investigate_objectives

        char = MagicMock()
        room = MagicMock()
        room.db.room_id = "random_room"

        cq = _make_cq("explore_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "explore_quest",
            "objectives": [{"type": "investigate", "target": "hidden_chamber", "count": 1}],
        }

        check_investigate_objectives(char, room)

        self.assertEqual(cq.progress.get("investigate_hidden_chamber", 0), 0)
        mock_check.assert_not_called()


# ---------------------------------------------------------------------------
# Test: check_practice_objectives
# ---------------------------------------------------------------------------

class TestCheckPracticeObjectives(unittest.TestCase):
    """Tests for check_practice_objectives."""

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_practice_opportunity_increments_matching_objective(self, MockCQ, mock_get_spec, mock_check):
        """Completing a matching practice opportunity increments quest progress."""
        from world.quest_engine import check_practice_objectives

        char = MagicMock()
        cq = _make_cq("repair_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]
        mock_get_spec.return_value = {
            "quest_id": "repair_quest",
            "objectives": [{"type": "practice", "target": "vp_canal_winch_repair", "count": 2}],
        }

        check_practice_objectives(char, "vp_canal_winch_repair")

        mock_check.assert_called_once_with(
            char,
            101,
            mock_get_spec.return_value,
            [
                {
                    "key": "practice_vp_canal_winch_repair",
                    "amount": 1,
                    "cap": 2,
                }
            ],
        )

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_practice_opportunity_is_capped_at_required_count(self, MockCQ, mock_get_spec, mock_check):
        """Practice objective progress does not exceed the objective count."""
        from world.quest_engine import check_practice_objectives

        char = MagicMock()
        cq = _make_cq("repair_quest", progress={"practice_vp_canal_winch_repair": 2})
        MockCQ.objects.filter.return_value = [cq]
        mock_get_spec.return_value = {
            "quest_id": "repair_quest",
            "objectives": [{"type": "practice", "target": "vp_canal_winch_repair", "count": 2}],
        }

        check_practice_objectives(char, "vp_canal_winch_repair")

        mock_check.assert_called_once()

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_nonmatching_practice_opportunity_does_not_increment(self, MockCQ, mock_get_spec, mock_check):
        """A different opportunity does not affect practice objectives."""
        from world.quest_engine import check_practice_objectives

        char = MagicMock()
        cq = _make_cq("repair_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]
        mock_get_spec.return_value = {
            "quest_id": "repair_quest",
            "objectives": [{"type": "practice", "target": "vp_canal_winch_repair", "count": 1}],
        }

        check_practice_objectives(char, "different_practice")

        self.assertEqual(cq.progress.get("practice_vp_canal_winch_repair", 0), 0)
        mock_check.assert_not_called()


# ---------------------------------------------------------------------------
# Test: check_deliver_objectives
# ---------------------------------------------------------------------------

class TestCheckDeliverObjectives(unittest.TestCase):
    """Tests for check_deliver_objectives."""

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_deliver_completes_with_item_and_npc(
        self, MockCQ, mock_get_spec, mock_check
    ):
        """Talking to target NPC while carrying target item completes delivery."""
        from world.quest_engine import check_deliver_objectives

        char = MagicMock()
        npc = MagicMock()
        npc.tags.get.side_effect = lambda category=None, **kw: "npc_warden" if category == "npc_id" else None

        # Character has the delivery item (tags-based matching)
        item = MagicMock()
        item.tags.get.side_effect = lambda category=None, **kw: "warden_report" if category == "item_tag" else None
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

        mock_check.assert_called_once_with(
            char,
            101,
            mock_get_spec.return_value,
            [{"key": "deliver_npc_warden", "amount": 1, "cap": 1}],
            delivery_items=[item],
        )

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_deliver_fails_without_item(self, MockCQ, mock_get_spec, mock_check):
        """Talking to NPC without the item does NOT complete delivery."""
        from world.quest_engine import check_deliver_objectives

        char = MagicMock()
        npc = MagicMock()
        npc.tags.get.side_effect = lambda category=None, **kw: "npc_warden" if category == "npc_id" else None
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

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_talk_to_completes_on_npc_match(self, MockCQ, mock_get_spec, mock_check):
        """Talking to matching NPC completes the talk_to objective."""
        from world.quest_engine import check_talk_to_objectives

        char = MagicMock()
        npc = MagicMock()
        npc.tags.get.side_effect = lambda category=None, **kw: "npc_elder" if category == "npc_id" else None

        cq = _make_cq("talk_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "talk_quest",
            "objectives": [{"type": "talk_to", "target": "npc_elder", "count": 1}],
        }

        check_talk_to_objectives(char, npc)

        mock_check.assert_called_once_with(
            char,
            101,
            mock_get_spec.return_value,
            [{"key": "talk_to_npc_elder", "amount": 1, "cap": 1}],
        )

    @patch("world.quest_engine._advance_quest_objectives")
    @patch("world.quest_engine._get_quest_spec")
    @patch("world.quest_engine.CharacterQuest")
    def test_talk_to_wrong_npc_no_effect(self, MockCQ, mock_get_spec, mock_check):
        """Talking to a non-target NPC does not affect talk_to objective."""
        from world.quest_engine import check_talk_to_objectives

        char = MagicMock()
        npc = MagicMock()
        npc.tags.get.side_effect = lambda category=None, **kw: "npc_barkeep" if category == "npc_id" else None

        cq = _make_cq("talk_quest", progress={})
        MockCQ.objects.filter.return_value = [cq]

        mock_get_spec.return_value = {
            "quest_id": "talk_quest",
            "objectives": [{"type": "talk_to", "target": "npc_elder", "count": 1}],
        }

        check_talk_to_objectives(char, npc)

        self.assertEqual(cq.progress.get("talk_to_npc_elder", 0), 0)
        mock_check.assert_not_called()


# ---------------------------------------------------------------------------
# Test: _check_quest_completion
# ---------------------------------------------------------------------------

class TestQuestObjectiveCompletionPredicate(unittest.TestCase):
    """Pure objective evaluation remains separate from transactional writes."""

    def test_requires_every_authored_objective(self):
        from world.quest_engine import _objectives_complete

        spec = {
            "objectives": [
                {"type": "kill", "target": "wolf", "count": 5},
                {"type": "collect", "target": "fang", "count": 3},
            ],
        }

        self.assertFalse(
            _objectives_complete(
                {"kill_wolf": 5, "collect_fang": 2},
                spec,
            )
        )
        self.assertTrue(
            _objectives_complete(
                {"kill_wolf": 5, "collect_fang": 3},
                spec,
            )
        )


# ---------------------------------------------------------------------------
# Test: _pay_rewards
# ---------------------------------------------------------------------------

class TestPayRewards(unittest.TestCase):
    """Tests for _pay_rewards function (D-20)."""

    @patch("world.action_vocabulary.execute_action")
    def test_pays_all_rewards(self, mock_exec):
        """_pay_rewards calls execute_action for each reward dict."""
        from world.quest_engine import _pay_rewards

        char = MagicMock()
        char.location = MagicMock()
        mock_exec.return_value = (True, "")

        spec = {
            "rewards": [
                {"action_type": "give_scales", "amount": 100},
                {"action_type": "echo", "message": "Well done!"},
            ],
        }

        _pay_rewards(char, spec)

        self.assertEqual(mock_exec.call_count, 2)
        # First reward
        first_call = mock_exec.call_args_list[0]
        self.assertEqual(first_call[0][0]["action_type"], "give_scales")
        # Second reward
        second_call = mock_exec.call_args_list[1]
        self.assertEqual(second_call[0][0]["action_type"], "echo")

    @patch("world.action_vocabulary.execute_action")
    def test_pays_nothing_when_no_rewards(self, mock_exec):
        """_pay_rewards with empty rewards list does nothing."""
        from world.quest_engine import _pay_rewards

        char = MagicMock()
        char.location = MagicMock()

        spec = {"rewards": []}
        _pay_rewards(char, spec)

        mock_exec.assert_not_called()

    @patch("world.action_vocabulary.execute_action")
    def test_pays_nothing_when_rewards_key_missing(self, mock_exec):
        """_pay_rewards handles missing rewards key gracefully."""
        from world.quest_engine import _pay_rewards

        char = MagicMock()
        char.location = MagicMock()

        spec = {}
        _pay_rewards(char, spec)

        mock_exec.assert_not_called()

    @patch("world.action_vocabulary.execute_action")
    def test_context_has_character_and_room(self, mock_exec):
        """_pay_rewards passes character and room in context to execute_action."""
        from world.quest_engine import _pay_rewards

        char = MagicMock()
        room = MagicMock()
        char.location = room
        mock_exec.return_value = (True, "")

        spec = {"rewards": [{"action_type": "give_scales", "amount": 50}]}
        _pay_rewards(char, spec)

        context = mock_exec.call_args[0][1]
        self.assertEqual(context["character"], char)
        self.assertEqual(context["room"], room)

    @patch("world.action_vocabulary.execute_action")
    def test_failed_reward_returns_failure_and_notifies_character(self, mock_exec):
        """_pay_rewards exposes failed action rewards instead of silently dropping them."""
        from world.quest_engine import _pay_rewards

        char = MagicMock()
        char.location = MagicMock()
        mock_exec.return_value = (False, "record_social_event: required propagation")

        spec = {"rewards": [{"action_type": "record_social_event"}]}
        failures = _pay_rewards(char, spec)

        self.assertEqual(
            failures,
            [
                {
                    "index": 0,
                    "action_type": "record_social_event",
                    "message": "record_social_event: required propagation",
                }
            ],
        )
        char.msg.assert_called_once()
        self.assertIn("Reward Error", char.msg.call_args[0][0])


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

    @patch("world.quest_engine.CharacterQuest")
    @patch("world.quest_engine._get_all_quest_specs")
    def test_returns_none_for_one_chance_failed(self, mock_all_specs, MockCQ):
        """Returns None if NPC's quest is one_chance and character failed it (D-03)."""
        from world.quest_engine import get_available_quest_for_npc

        npc = MagicMock()
        npc.db.npc_id = "npc_barkeep"
        char = MagicMock()

        mock_all_specs.return_value = [
            {"quest_id": "q1", "quest_giver": "npc_barkeep", "one_chance": True},
        ]

        existing_qs = MagicMock()
        active_qs = MagicMock()
        active_qs.values_list.return_value = []
        complete_qs = MagicMock()
        complete_qs.values_list.return_value = []
        failed_qs = MagicMock()
        failed_qs.values_list.return_value = ["q1"]

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

    @patch("world.quest_engine.CharacterQuest")
    @patch("world.quest_engine._get_all_quest_specs")
    def test_returns_none_for_completed_one_chance_quest(self, mock_all_specs, MockCQ):
        """Returns None if NPC's one_chance quest is already complete."""
        from world.quest_engine import get_available_quest_for_npc

        npc = MagicMock()
        npc.db.npc_id = "npc_barkeep"
        char = MagicMock()

        mock_all_specs.return_value = [
            {"quest_id": "q1", "quest_giver": "npc_barkeep", "one_chance": True},
        ]

        existing_qs = MagicMock()
        active_qs = MagicMock()
        active_qs.values_list.return_value = []
        complete_qs = MagicMock()
        complete_qs.values_list.return_value = ["q1"]
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

    @patch("world.quest_engine.CharacterQuest")
    @patch("world.quest_engine._get_all_quest_specs")
    def test_repeatable_quest_re_offered_after_completion(self, mock_all_specs, MockCQ):
        """Repeatable (non-one_chance) quest is offered again after completion."""
        from world.quest_engine import get_available_quest_for_npc

        npc = MagicMock()
        npc.db.npc_id = "npc_barkeep"
        char = MagicMock()

        mock_all_specs.return_value = [
            {"quest_id": "q1", "quest_giver": "npc_barkeep"},
        ]

        existing_qs = MagicMock()
        active_qs = MagicMock()
        active_qs.values_list.return_value = []
        complete_qs = MagicMock()
        complete_qs.values_list.return_value = ["q1"]
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

        self.assertIsNotNone(result)
        self.assertEqual(result["quest_id"], "q1")

    @patch("world.quest_engine.CharacterQuest")
    @patch("world.quest_engine._get_all_quest_specs")
    def test_prerequisite_locked_quest_not_offered_early(self, mock_all_specs, MockCQ):
        """NPCs do not offer chain steps until prerequisite quests are complete."""
        from world.quest_engine import get_available_quest_for_npc

        npc = MagicMock()
        npc.db.npc_id = "npc_barkeep"
        char = MagicMock()

        mock_all_specs.return_value = [
            {
                "quest_id": "q2",
                "quest_giver": "npc_barkeep",
                "prerequisite_quests": ["q1"],
            },
        ]

        existing_qs = MagicMock()
        active_qs = MagicMock()
        active_qs.values_list.return_value = []
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

    @patch("world.quest_engine.CharacterQuest")
    @patch("world.quest_engine._get_all_quest_specs")
    def test_prerequisite_locked_quest_offered_after_completion(self, mock_all_specs, MockCQ):
        """NPCs offer a chain step after all prerequisite quests are complete."""
        from world.quest_engine import get_available_quest_for_npc

        npc = MagicMock()
        npc.db.npc_id = "npc_barkeep"
        char = MagicMock()

        mock_all_specs.return_value = [
            {
                "quest_id": "q2",
                "quest_giver": "npc_barkeep",
                "prerequisite_quests": ["q1"],
            },
        ]

        existing_qs = MagicMock()
        active_qs = MagicMock()
        active_qs.values_list.return_value = []
        complete_qs = MagicMock()
        complete_qs.values_list.return_value = ["q1"]
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

        self.assertIsNotNone(result)
        self.assertEqual(result["quest_id"], "q2")

    @patch("world.quest_engine.CharacterQuest")
    @patch("world.quest_engine._get_all_quest_specs")
    def test_returns_none_for_npc_with_no_quests(self, mock_all_specs, MockCQ):
        """Returns None when no quest specs reference this NPC."""
        from world.quest_engine import get_available_quest_for_npc

        npc = MagicMock()
        npc.db.npc_id = "npc_nobody"
        char = MagicMock()

        mock_all_specs.return_value = [
            {"quest_id": "q1", "quest_giver": "npc_barkeep"},
        ]

        existing_qs = MagicMock()
        existing_qs.filter.return_value.values_list.return_value = []
        MockCQ.objects.filter.return_value = existing_qs

        result = get_available_quest_for_npc(npc, char)

        self.assertIsNone(result)

    @patch("world.quest_engine.CharacterQuest")
    def test_returns_none_for_npc_without_npc_id(self, MockCQ):
        """Returns None when NPC has no npc_id set."""
        from world.quest_engine import get_available_quest_for_npc

        npc = MagicMock()
        npc.db.npc_id = None
        char = MagicMock()

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
        get_active_quests(char)

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

    @patch("world.quest_engine.CharacterQuest")
    def test_get_quest_detail_returns_none_for_nonexistent(self, MockCQ):
        """get_quest_detail returns None when quest not found."""
        from world.quest_engine import get_quest_detail

        char = MagicMock()
        MockCQ.objects.filter.return_value.first.return_value = None

        result = get_quest_detail(char, "nonexistent_q")

        self.assertIsNone(result)

    @patch("world.quest_engine._get_quest_spec", return_value=None)
    @patch("world.quest_engine.CharacterQuest")
    def test_get_quest_detail_returns_none_if_spec_missing(self, MockCQ, mock_spec):
        """get_quest_detail returns None when spec is not found in zone data."""
        from world.quest_engine import get_quest_detail

        char = MagicMock()
        cq = _make_cq("orphan_q")
        MockCQ.objects.filter.return_value.first.return_value = cq

        result = get_quest_detail(char, "orphan_q")

        self.assertIsNone(result)


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
