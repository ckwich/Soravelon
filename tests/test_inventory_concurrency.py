"""PostgreSQL contention proof for inventory row-lock ordering."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest import skipUnless

from django.db import close_old_connections, connection
from django.test import TransactionTestCase
from evennia import create_object
from evennia.objects.models import ObjectDB

from world.models import InventoryItem


@skipUnless(
    connection.vendor == "postgresql",
    "row-lock contention requires PostgreSQL",
)
class TestPostgresInventoryContention(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        from typeclasses.characters import Character
        from typeclasses.objects import SoravelonItem
        from typeclasses.rooms import SoravelonRoom

        self.room = create_object(SoravelonRoom, key="Contention Room")
        self.first = create_object(Character, key="First Claimant")
        self.second = create_object(Character, key="Second Claimant")
        self.first.location = self.room
        self.second.location = self.room
        self.item = create_object(
            SoravelonItem,
            key="Single Contended Item",
            location=self.room,
        )

    def test_concurrent_pickup_creates_exactly_one_owner(self):
        barrier = Barrier(2)

        def attempt(character_id):
            close_old_connections()
            try:
                from world.inventory_engine import pick_up

                character = ObjectDB.objects.get(pk=character_id)
                item = ObjectDB.objects.get(pk=self.item.id)
                barrier.wait(timeout=5)
                success, message = pick_up(character, item)
                return character_id, success, message
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(
                executor.map(attempt, [self.first.id, self.second.id])
            )

        winners = [character_id for character_id, success, _ in results if success]
        self.assertEqual(len(winners), 1, results)
        record = InventoryItem.objects.get(item_id=self.item.id)
        self.assertEqual(record.character_id, winners[0])
        stored_location = ObjectDB.objects.values_list(
            "db_location_id",
            flat=True,
        ).get(pk=self.item.id)
        self.assertEqual(stored_location, winners[0])
