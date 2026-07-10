"""Atomic quest progress, completion, and reward contracts."""

from unittest.mock import MagicMock, patch

from evennia import create_object
from evennia.objects.models import ObjectDB
from evennia.utils.test_resources import EvenniaTest

from world.models import CharacterQuest, GameOperation, InventoryItem


class TestAtomicQuestOutcomes(EvenniaTest):
    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom

        self.room = create_object(SoravelonRoom, key="Quest Outcome Room")
        self.char1.location = self.room
        self.char1.db.carried_scales = 0
        self.char1.msg = MagicMock()

    def _quest(self, *, quest_id="atomic_quest", progress=None):
        return CharacterQuest.objects.create(
            character=self.char1,
            quest_id=quest_id,
            progress=progress or {"talk_to_witness": 1},
        )

    @staticmethod
    def _spec(*, quest_id="atomic_quest", rewards=None):
        return {
            "quest_id": quest_id,
            "name": "Atomic Quest",
            "objectives": [
                {"type": "talk_to", "target": "witness", "count": 1},
            ],
            "rewards": rewards or [],
        }

    def test_reward_rejection_leaves_quest_active_and_unpaid(self):
        from world.quest_engine import _check_quest_completion

        quest = self._quest()
        completed = _check_quest_completion(
            self.char1,
            quest,
            self._spec(
                rewards=[{"action_type": "give_scales", "amount": -1}],
            ),
        )

        quest.refresh_from_db()
        self.assertFalse(completed)
        self.assertEqual(quest.status, "active")
        self.assertIsNone(quest.completed_at)
        self.assertIsNone(quest.outcome_operation_id)
        self.assertEqual(self.char1.db.carried_scales, 0)
        self.assertFalse(GameOperation.objects.exists())
        messages = [
            str(call.args[0])
            for call in self.char1.msg.call_args_list
            if call.args
        ]
        self.assertTrue(any("Reward Error" in message for message in messages))
        self.assertFalse(any("Quest Complete" in message for message in messages))

    def test_completion_retry_pays_once_and_records_one_outcome(self):
        from world.quest_engine import _check_quest_completion

        quest = self._quest()
        spec = self._spec(
            rewards=[{"action_type": "give_scales", "amount": 10}],
        )

        with self.captureOnCommitCallbacks(execute=True):
            first = _check_quest_completion(self.char1, quest, spec)
        with self.captureOnCommitCallbacks(execute=True):
            second = _check_quest_completion(self.char1, quest, spec)

        quest.refresh_from_db()
        self.assertTrue(first)
        self.assertTrue(second)
        self.assertEqual(quest.status, "complete")
        self.assertEqual(
            quest.outcome_operation_id,
            f"quest-outcome:{quest.pk}",
        )
        self.assertEqual(self.char1.db.carried_scales, 10)
        self.assertEqual(
            GameOperation.objects.filter(
                operation_type="quest_rewards",
                related_id="quest-rewards:atomic_quest",
            ).count(),
            1,
        )
        self.assertEqual(
            GameOperation.objects.filter(
                operation_type="quest_completion",
                related_id=f"quest:atomic_quest:{quest.pk}",
            ).count(),
            1,
        )
        messages = [
            str(call.args[0])
            for call in self.char1.msg.call_args_list
            if call.args
        ]
        self.assertEqual(
            sum("Quest Complete" in message for message in messages),
            1,
        )
        self.assertEqual(sum("+10 Scales" in message for message in messages), 1)

    def test_failure_after_outcome_writes_rolls_back_every_effect(self):
        from world.quest_engine import _check_quest_completion

        quest = self._quest()
        spec = self._spec(
            rewards=[{"action_type": "give_scales", "amount": 10}],
        )

        with patch(
            "world.quest_engine._quest_after_write",
            side_effect=RuntimeError("injected outcome failure"),
        ), self.assertRaisesRegex(RuntimeError, "injected outcome failure"):
            _check_quest_completion(self.char1, quest, spec)

        quest.refresh_from_db()
        self.assertEqual(quest.status, "active")
        self.assertIsNone(quest.completed_at)
        self.assertIsNone(quest.outcome_operation_id)
        self.assertEqual(self.char1.db.carried_scales, 0)
        self.assertFalse(GameOperation.objects.exists())
        messages = [
            str(call.args[0])
            for call in self.char1.msg.call_args_list
            if call.args
        ]
        self.assertFalse(any("Quest Complete" in message for message in messages))
        self.assertFalse(any("+10 Scales" in message for message in messages))

    def test_session_skill_reward_is_reverted_when_outcome_rolls_back(self):
        from world.quest_engine import _check_quest_completion

        quest = self._quest()
        spec = self._spec(
            rewards=[
                {
                    "action_type": "give_skill_xp",
                    "skill_id": "investigation",
                    "count": 3,
                },
            ],
        )

        with patch(
            "world.quest_engine._quest_after_write",
            side_effect=RuntimeError("injected outcome failure"),
        ), self.assertRaisesRegex(RuntimeError, "injected outcome failure"):
            _check_quest_completion(self.char1, quest, spec)

        self.assertEqual(
            getattr(self.char1.ndb, "skill_use_investigation", 0) or 0,
            0,
        )

    def test_delivery_consumption_and_progress_roll_back_with_failed_reward(self):
        from typeclasses.mobs import SoravelonMob
        from typeclasses.objects import SoravelonItem
        from world.quest_engine import check_deliver_objectives

        quest = CharacterQuest.objects.create(
            character=self.char1,
            quest_id="delivery_atomic_quest",
            progress={},
        )
        report = create_object(
            SoravelonItem,
            key="Sealed Report",
            location=self.char1,
        )
        report.db.item_tag = "sealed_report"
        report.tags.add("sealed_report", category="item_tag")
        InventoryItem.objects.create(
            character=self.char1,
            item_id=report.id,
            quantity=1,
        )
        npc = create_object(SoravelonMob, key="Witness", location=self.room)
        npc.tags.add("delivery_witness", category="npc_id")
        spec = {
            "quest_id": "delivery_atomic_quest",
            "name": "Delivery Atomic Quest",
            "objectives": [
                {
                    "type": "deliver",
                    "target": "delivery_witness",
                    "item_tag": "sealed_report",
                    "count": 1,
                },
            ],
            "rewards": [{"action_type": "give_scales", "amount": -1}],
        }

        with patch("world.quest_engine._get_quest_spec", return_value=spec):
            check_deliver_objectives(self.char1, npc)

        quest.refresh_from_db()
        self.assertEqual(quest.status, "active")
        self.assertEqual(quest.progress, {})
        self.assertTrue(ObjectDB.objects.filter(pk=report.id).exists())
        self.assertTrue(
            InventoryItem.objects.filter(
                character=self.char1,
                item_id=report.id,
            ).exists(),
        )
