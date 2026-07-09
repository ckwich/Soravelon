"""Durable identity contracts for composite gameplay effects."""

from django.db import IntegrityError, transaction
from evennia.utils.test_resources import EvenniaTest

from world.models import GameOperation


class TestGameOperations(EvenniaTest):
    def test_matching_receipt_replays_and_conflicting_reuse_fails(self):
        from world.game_operations import (
            GameOperationConflict,
            get_operation_replay,
            record_operation,
        )

        record_operation(
            character=self.char1,
            operation_id="vendor-buy:one",
            operation_type="vendor_buy",
            related_id="vendor:1:item:iron_dagger",
            result={"price": 25},
        )
        replay = get_operation_replay(
            character=self.char1,
            operation_id="vendor-buy:one",
            operation_type="vendor_buy",
            related_id="vendor:1:item:iron_dagger",
        )
        self.assertEqual(replay.result, {"price": 25})

        with self.assertRaises(GameOperationConflict):
            get_operation_replay(
                character=self.char1,
                operation_id="vendor-buy:one",
                operation_type="vendor_buy",
                related_id="vendor:1:item:steel_dagger",
            )

    def test_actor_snapshot_survives_character_deletion(self):
        receipt = GameOperation.objects.create(
            character_id=self.char1.id,
            character_ref=self.char1.id,
            operation_type="test",
            related_id="test:one",
        )
        character_id = self.char1.id
        self.char1.delete()
        receipt.refresh_from_db()
        self.assertIsNone(receipt.character_id)
        self.assertEqual(receipt.character_ref, character_id)

    def test_database_rejects_mismatched_actor_snapshot(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            GameOperation.objects.create(
                character_id=self.char1.id,
                character_ref=self.char2.id,
                operation_type="test",
                related_id="test:mismatch",
            )
