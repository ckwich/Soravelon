"""Rollback and contention contracts for inventory ownership mutations."""

from unittest.mock import patch

from django.db import IntegrityError, transaction
from evennia import create_object
from evennia.objects.models import ObjectDB
from evennia.utils.test_resources import EvenniaTest

from world.models import InventoryItem


class AtomicInventoryTestBase(EvenniaTest):
    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom

        self.room = create_object(SoravelonRoom, key="Inventory Transaction Room")
        self.char1.location = self.room
        self.char2.location = self.room

    def make_item(self, key="item", location=None, **attributes):
        from typeclasses.objects import SoravelonItem

        item = create_object(
            SoravelonItem,
            key=key,
            location=self.room if location is None else location,
        )
        for name, value in attributes.items():
            setattr(item.db, name, value)
        return item

    def make_equipment(self, key="helm", slot="head"):
        from typeclasses.objects import SoravelonEquipment

        item = create_object(SoravelonEquipment, key=key, location=self.char1)
        item.db.equipment_slot = slot
        InventoryItem.objects.create(
            character_id=self.char1.id,
            item_id=item.id,
        )
        return item

    def make_container(self, key="bag"):
        from typeclasses.objects import SoravelonContainer

        item = create_object(SoravelonContainer, key=key, location=self.char1)
        item.db.weight_capacity = 50.0
        InventoryItem.objects.create(
            character_id=self.char1.id,
            item_id=item.id,
        )
        return item

    @staticmethod
    def fail_at(expected_checkpoint):
        def _fail(checkpoint):
            if checkpoint == expected_checkpoint:
                raise RuntimeError(f"injected failure at {checkpoint}")

        return _fail

    def assert_location(self, item, expected):
        stored_location_id = ObjectDB.objects.values_list(
            "db_location_id",
            flat=True,
        ).get(pk=item.id)
        self.assertEqual(stored_location_id, expected.id if expected else None)
        self.assertEqual(item.location, expected)


class TestAtomicPickup(AtomicInventoryTestBase):
    def test_direct_player_spawn_registers_real_character_typeclass(self):
        from world.item_spawner import create_item_from_catalog

        item = create_item_from_catalog("iron_dagger", location=self.char1)

        record = InventoryItem.objects.get(item_id=item.id)
        self.assertEqual(record.character_id, self.char1.id)
        self.assert_location(item, self.char1)

    def test_pickup_rolls_back_location_and_ownership_after_every_write(self):
        from world.inventory_engine import pick_up

        for checkpoint in ("item_moved", "ownership_registered"):
            with self.subTest(checkpoint=checkpoint):
                item = self.make_item(key=f"gem {checkpoint}")
                with patch(
                    "world.inventory_transactions._after_write",
                    side_effect=self.fail_at(checkpoint),
                ), self.assertRaisesRegex(RuntimeError, checkpoint):
                    pick_up(self.char1, item)

                self.assert_location(item, self.room)
                self.assertFalse(
                    InventoryItem.objects.filter(item_id=item.id).exists()
                )

    def test_stack_pickup_rolls_back_quantity_and_source_deletion(self):
        from world.inventory_engine import pick_up

        existing = self.make_item(
            "wolf pelt",
            location=self.char1,
            stackable=True,
            item_type="material",
        )
        InventoryItem.objects.create(
            character_id=self.char1.id,
            item_id=existing.id,
            quantity=5,
        )

        for checkpoint in ("stack_incremented", "source_item_deleted"):
            with self.subTest(checkpoint=checkpoint):
                source = self.make_item(
                    "wolf pelt",
                    stackable=True,
                    item_type="material",
                    quantity=2,
                )
                source_id = source.id
                with patch(
                    "world.inventory_transactions._after_write",
                    side_effect=self.fail_at(checkpoint),
                ), self.assertRaisesRegex(RuntimeError, checkpoint):
                    pick_up(self.char1, source)

                self.assertEqual(
                    InventoryItem.objects.get(item_id=existing.id).quantity,
                    5,
                )
                self.assertTrue(ObjectDB.objects.filter(pk=source_id).exists())
                self.assert_location(source, self.room)

    def test_second_actor_cannot_claim_a_stale_item(self):
        from world.inventory_engine import pick_up

        item = self.make_item("single claim")
        first_ok, _ = pick_up(self.char1, item)
        second_ok, _ = pick_up(self.char2, item)

        self.assertTrue(first_ok)
        self.assertFalse(second_ok)
        record = InventoryItem.objects.get(item_id=item.id)
        self.assertEqual(record.character_id, self.char1.id)
        self.assert_location(item, self.char1)


class TestAtomicDrop(AtomicInventoryTestBase):
    def test_full_drop_rolls_back_every_durable_write(self):
        from world.inventory_engine import drop_item

        item = self.make_item("ore", location=self.char1, stackable=True)
        InventoryItem.objects.create(
            character_id=self.char1.id,
            item_id=item.id,
            quantity=4,
        )

        for checkpoint in (
            "item_moved",
            "world_quantity_written",
            "ownership_unregistered",
        ):
            with self.subTest(checkpoint=checkpoint):
                with patch(
                    "world.inventory_transactions._after_write",
                    side_effect=self.fail_at(checkpoint),
                ), self.assertRaisesRegex(RuntimeError, checkpoint):
                    drop_item(self.char1, item)

                self.assert_location(item, self.char1)
                self.assertEqual(
                    InventoryItem.objects.get(item_id=item.id).quantity,
                    4,
                )

    def test_partial_drop_rolls_back_created_object_and_stack_quantity(self):
        from world.inventory_engine import drop_item

        item = self.make_item("ore", location=self.char1, stackable=True)
        InventoryItem.objects.create(
            character_id=self.char1.id,
            item_id=item.id,
            quantity=4,
        )
        original_ids = set(ObjectDB.objects.values_list("id", flat=True))

        for checkpoint in ("split_item_created", "stack_decremented"):
            with self.subTest(checkpoint=checkpoint):
                with patch(
                    "world.inventory_transactions._after_write",
                    side_effect=self.fail_at(checkpoint),
                ), self.assertRaisesRegex(RuntimeError, checkpoint):
                    drop_item(self.char1, item, quantity=2)

                self.assertEqual(
                    InventoryItem.objects.get(item_id=item.id).quantity,
                    4,
                )
                self.assertEqual(
                    set(ObjectDB.objects.values_list("id", flat=True)),
                    original_ids,
                )

    def test_rejects_invalid_partial_quantities_without_mutation(self):
        from world.inventory_engine import drop_item

        item = self.make_item("ore", location=self.char1, stackable=True)
        InventoryItem.objects.create(
            character_id=self.char1.id,
            item_id=item.id,
            quantity=4,
        )

        for quantity in (0, -1, 5, True, 1.5):
            with self.subTest(quantity=quantity):
                ok, _ = drop_item(self.char1, item, quantity=quantity)
                self.assertFalse(ok)
                self.assertEqual(
                    InventoryItem.objects.get(item_id=item.id).quantity,
                    4,
                )
                self.assert_location(item, self.char1)


class TestAtomicContainerAndEquipment(AtomicInventoryTestBase):
    def test_database_rejects_two_items_in_one_equipment_slot(self):
        first = self.make_equipment("first helm")
        second = self.make_equipment("second helm")
        InventoryItem.objects.filter(item_id=first.id).update(
            is_equipped=True,
            equipment_slot="head",
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            InventoryItem.objects.filter(item_id=second.id).update(
                is_equipped=True,
                equipment_slot="head",
            )

    def test_container_assignment_rolls_back(self):
        from world.inventory_engine import put_in_container

        bag = self.make_container()
        item = self.make_item("gem", location=self.char1, weight=0.5)
        InventoryItem.objects.create(
            character_id=self.char1.id,
            item_id=item.id,
        )

        with patch(
            "world.inventory_transactions._after_write",
            side_effect=self.fail_at("container_assigned"),
        ), self.assertRaisesRegex(RuntimeError, "container_assigned"):
            put_in_container(self.char1, item, bag)

        self.assertIsNone(
            InventoryItem.objects.get(item_id=item.id).container_id
        )

    def test_equipment_assignment_rolls_back(self):
        from world.inventory_engine import equip_item

        item = self.make_equipment()
        with patch(
            "world.inventory_transactions._after_write",
            side_effect=self.fail_at("equipment_updated"),
        ), self.assertRaisesRegex(RuntimeError, "equipment_updated"):
            equip_item(self.char1, item)

        record = InventoryItem.objects.get(item_id=item.id)
        self.assertFalse(record.is_equipped)
        self.assertIsNone(record.equipment_slot)


class TestAtomicTransfer(AtomicInventoryTestBase):
    def test_destroy_owned_item_rolls_back_row_and_object(self):
        from world.inventory_transactions import destroy_owned_item

        item = self.make_item("consumable", location=self.char1)
        InventoryItem.objects.create(
            character_id=self.char1.id,
            item_id=item.id,
        )

        for checkpoint in ("ownership_unregistered", "owned_item_deleted"):
            with self.subTest(checkpoint=checkpoint):
                with patch(
                    "world.inventory_transactions._after_write",
                    side_effect=self.fail_at(checkpoint),
                ), self.assertRaisesRegex(RuntimeError, checkpoint):
                    destroy_owned_item(self.char1, item)

                self.assertTrue(ObjectDB.objects.filter(pk=item.id).exists())
                self.assertTrue(
                    InventoryItem.objects.filter(item_id=item.id).exists()
                )
                self.assert_location(item, self.char1)

    def test_bulk_world_container_transfer_rolls_back_all_items(self):
        from world.inventory_transactions import move_owned_items_to_world_container

        corpse = self.make_container("corpse")
        first = self.make_item("first", location=self.char1)
        second = self.make_item("second", location=self.char1)
        InventoryItem.objects.create(
            character_id=self.char1.id,
            item_id=first.id,
        )
        InventoryItem.objects.create(
            character_id=self.char1.id,
            item_id=second.id,
        )

        with patch(
            "world.inventory_transactions._after_write",
            side_effect=self.fail_at("ownership_unregistered"),
        ), self.assertRaisesRegex(RuntimeError, "ownership_unregistered"):
            move_owned_items_to_world_container(
                self.char1,
                [first, second],
                corpse,
            )

        self.assert_location(first, self.char1)
        self.assert_location(second, self.char1)
        self.assertEqual(
            InventoryItem.objects.filter(
                character_id=self.char1.id,
                item_id__in=[first.id, second.id],
            ).count(),
            2,
        )

    def test_transfer_rolls_back_location_and_owner_after_every_write(self):
        from world.inventory_transactions import transfer_item

        item = self.make_item("gift", location=self.char1)
        InventoryItem.objects.create(
            character_id=self.char1.id,
            item_id=item.id,
        )

        for checkpoint in ("item_moved", "ownership_transferred"):
            with self.subTest(checkpoint=checkpoint):
                with patch(
                    "world.inventory_transactions._after_write",
                    side_effect=self.fail_at(checkpoint),
                ), self.assertRaisesRegex(RuntimeError, checkpoint):
                    transfer_item(self.char1, self.char2, item)

                self.assert_location(item, self.char1)
                self.assertEqual(
                    InventoryItem.objects.get(item_id=item.id).character_id,
                    self.char1.id,
                )
