"""PostgreSQL contention proof for exactly-once quest completion."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest import skipUnless

from django.db import close_old_connections, connection
from django.test import TransactionTestCase
from evennia import create_object
from evennia.objects.models import ObjectDB

from world.models import CharacterQuest, GameOperation


@skipUnless(
    connection.vendor == "postgresql",
    "row-lock contention requires PostgreSQL",
)
class TestPostgresQuestContention(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        from typeclasses.characters import Character
        from typeclasses.rooms import SoravelonRoom

        self.room = create_object(SoravelonRoom, key="Quest Contention Room")
        self.character = create_object(Character, key="Quest Claimant")
        self.character.location = self.room
        self.character.db.carried_scales = 0
        self.quest = CharacterQuest.objects.create(
            character=self.character,
            quest_id="quest_contention",
            progress={"talk_to_witness": 1},
        )
        self.spec = {
            "quest_id": "quest_contention",
            "name": "Quest Contention",
            "objectives": [
                {"type": "talk_to", "target": "witness", "count": 1},
            ],
            "rewards": [{"action_type": "give_scales", "amount": 25}],
        }

    def test_concurrent_completion_pays_once(self):
        barrier = Barrier(2)

        def complete(_attempt):
            close_old_connections()
            try:
                from world.quest_engine import _check_quest_completion

                character = ObjectDB.objects.get(pk=self.character.id)
                quest = CharacterQuest.objects.get(pk=self.quest.id)
                barrier.wait(timeout=5)
                return _check_quest_completion(character, quest, self.spec)
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(complete, range(2)))

        self.assertEqual(results, [True, True])
        self.quest.refresh_from_db()
        self.assertEqual(self.quest.status, "complete")
        character = ObjectDB.objects.get(pk=self.character.id)
        self.assertEqual(character.db.carried_scales, 25)
        self.assertEqual(
            GameOperation.objects.filter(
                operation_type="quest_rewards",
                related_id="quest-rewards:quest_contention",
            ).count(),
            1,
        )
        self.assertEqual(
            GameOperation.objects.filter(
                operation_type="quest_completion",
                related_id=f"quest:quest_contention:{self.quest.pk}",
            ).count(),
            1,
        )

    def test_concurrent_progress_events_do_not_lose_an_increment(self):
        quest = CharacterQuest.objects.create(
            character=self.character,
            quest_id="quest_progress_contention",
            progress={},
        )
        spec = {
            "quest_id": "quest_progress_contention",
            "name": "Quest Progress Contention",
            "objectives": [
                {"type": "kill", "target": "wolf", "count": 2},
            ],
            "rewards": [{"action_type": "give_scales", "amount": 25}],
        }
        barrier = Barrier(2)

        def advance(_attempt):
            close_old_connections()
            try:
                from world.quest_engine import _advance_quest_objectives

                character = ObjectDB.objects.get(pk=self.character.id)
                barrier.wait(timeout=5)
                return _advance_quest_objectives(
                    character,
                    quest.pk,
                    spec,
                    [{"key": "kill_wolf", "amount": 1, "cap": 2}],
                )
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(advance, range(2)))

        self.assertEqual(sum(bool(result) for result in results), 1, results)
        quest.refresh_from_db()
        self.assertEqual(quest.progress, {"kill_wolf": 2})
        self.assertEqual(quest.status, "complete")
        character = ObjectDB.objects.get(pk=self.character.id)
        self.assertEqual(character.db.carried_scales, 25)
