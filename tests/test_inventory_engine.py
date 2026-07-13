"""
Tests for Soravelon inventory engine (Build Order Step 9).
Tests written FIRST per TDD.
"""

from evennia.utils.test_resources import EvenniaTest
from evennia import create_object
from unittest.mock import patch

from world.models import InventoryItem


class InvTestBase(EvenniaTest):
    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom
        self.room = create_object(SoravelonRoom, key="Test Room")
        self.char1.location = self.room
        self.char1.db.strength = 10  # capacity = 60 kg

    def _make_item(self, key="item", location=None, **kwargs):
        from typeclasses.objects import SoravelonItem
        loc = location if location is not None else self.room
        item = create_object(SoravelonItem, key=key, location=loc)
        for k, v in kwargs.items():
            setattr(item.db, k, v)
        return item

    def _make_container(self, key="bag", location=None, **kwargs):
        from typeclasses.objects import SoravelonContainer
        loc = location if location is not None else self.char1
        bag = create_object(SoravelonContainer, key=key, location=loc)
        for k, v in kwargs.items():
            setattr(bag.db, k, v)
        InventoryItem.objects.create(character_id=self.char1.id, item_id=bag.id)
        return bag

    def _make_equipment(self, key="sword", slot="right_hand", location=None):
        from typeclasses.objects import SoravelonEquipment
        loc = location if location is not None else self.char1
        eq = create_object(SoravelonEquipment, key=key, location=loc)
        eq.db.equipment_slot = slot
        InventoryItem.objects.create(character_id=self.char1.id, item_id=eq.id)
        return eq


# --- Container weight rolling ---

class TestCommonContainerReduction(InvTestBase):
    def test_common_container_reduction_range(self):
        from world.inventory_engine import roll_container_weight_reduction
        for _ in range(100):
            r = roll_container_weight_reduction("common")
            self.assertGreaterEqual(r, 0)
            self.assertLessEqual(r, 10)


class TestRareContainerReduction(InvTestBase):
    def test_rare_container_reduction_range(self):
        from world.inventory_engine import roll_container_weight_reduction
        for _ in range(100):
            r = roll_container_weight_reduction("rare")
            self.assertGreaterEqual(r, 25)
            self.assertLessEqual(r, 50)


class TestMasterworkContainerReduction(InvTestBase):
    def test_masterwork_container_reduction_range(self):
        from world.inventory_engine import roll_container_weight_reduction
        for _ in range(100):
            r = roll_container_weight_reduction("masterwork")
            self.assertGreaterEqual(r, 50)
            self.assertLessEqual(r, 75)


class TestInitializeContainer(InvTestBase):
    def test_initialize_container_sets_reduction(self):
        from typeclasses.objects import SoravelonContainer
        from world.inventory_engine import initialize_container
        bag = create_object(SoravelonContainer, key="bag")
        initialize_container(bag, "rare")
        self.assertGreaterEqual(bag.db.weight_reduction, 25)
        self.assertLessEqual(bag.db.weight_reduction, 50)
        self.assertEqual(bag.db.rarity, "rare")


# --- Pickup ---

class TestPickUpCreatesRecord(InvTestBase):
    def test_pick_up_creates_inventory_record(self):
        from world.inventory_engine import pick_up
        item = self._make_item("gem")
        success, _ = pick_up(self.char1, item)
        self.assertTrue(success)
        self.assertEqual(item.location, self.char1)
        self.assertTrue(
            InventoryItem.objects.filter(
                character_id=self.char1.id, item_id=item.id
            ).exists()
        )


class TestPickUpAutoStack(InvTestBase):
    def test_pick_up_auto_stack(self):
        from world.inventory_engine import pick_up
        # Create existing stack in inventory
        existing = self._make_item("wolf pelt", location=self.char1,
                                    stackable=True, item_type="material")
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=existing.id, quantity=5
        )
        # Create new item on ground
        new_item = self._make_item("wolf pelt", location=self.room,
                                    stackable=True, item_type="material")
        pick_up(self.char1, new_item)
        record = InventoryItem.objects.get(
            character_id=self.char1.id, item_id=existing.id
        )
        self.assertEqual(record.quantity, 6)


class TestPickUpNoStackNonStackable(InvTestBase):
    def test_pick_up_no_stack_non_stackable(self):
        from world.inventory_engine import pick_up
        item1 = self._make_item("sword", location=self.char1, stackable=False)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item1.id
        )
        item2 = self._make_item("sword", location=self.room, stackable=False)
        pick_up(self.char1, item2)
        count = InventoryItem.objects.filter(
            character_id=self.char1.id
        ).count()
        self.assertEqual(count, 2)


class TestPickUpKeyringItem(InvTestBase):
    def test_pick_up_keyring_item_sets_keyring_flag(self):
        from typeclasses.objects import SoravelonKeyringItem
        from world.inventory_engine import pick_up
        key = create_object(SoravelonKeyringItem, key="seld key",
                            location=self.room)
        pick_up(self.char1, key)
        record = InventoryItem.objects.get(
            character_id=self.char1.id, item_id=key.id
        )
        self.assertTrue(record.keyring)


class TestPickUpFromContainer(InvTestBase):
    def test_pick_up_from_container(self):
        """Taking item from a room-container into direct carry."""
        from world.inventory_engine import pick_up
        # Item is in a container on the ground (not in char inventory)
        bag = self._make_container("chest", location=self.room)
        item = self._make_item("gem", location=bag)
        # There's no existing inventory record for item (it's in a room container)

        success, _ = pick_up(self.char1, item, container=bag)
        self.assertTrue(success)
        self.assertEqual(item.location, self.char1)


# --- Drop ---

class TestDropDeletesRecord(InvTestBase):
    def test_drop_item_deletes_record(self):
        from world.inventory_engine import drop_item
        item = self._make_item("rock", location=self.char1)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id
        )
        success, _ = drop_item(self.char1, item)
        self.assertTrue(success)
        self.assertEqual(item.location, self.room)
        self.assertFalse(
            InventoryItem.objects.filter(item_id=item.id).exists()
        )


class TestDropQuestItemFails(InvTestBase):
    def test_drop_quest_item_fails(self):
        from world.inventory_engine import drop_item
        item = self._make_item("quest gem", location=self.char1)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id,
            is_quest_item=True
        )
        success, _ = drop_item(self.char1, item)
        self.assertFalse(success)


class TestDropEquippedFails(InvTestBase):
    def test_drop_equipped_item_fails(self):
        from world.inventory_engine import drop_item
        eq = self._make_equipment("sword", "right_hand", location=self.char1)
        record = InventoryItem.objects.get(item_id=eq.id)
        record.is_equipped = True
        record.equipment_slot = "right_hand"
        record.save()
        success, _ = drop_item(self.char1, eq)
        self.assertFalse(success)


class TestDropPartialStack(InvTestBase):
    def test_drop_partial_stack(self):
        from world.inventory_engine import drop_item
        item = self._make_item("pelt", location=self.char1,
                                stackable=True, item_type="material")
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id, quantity=12
        )
        success, _ = drop_item(self.char1, item, quantity=5)
        self.assertTrue(success)
        record = InventoryItem.objects.get(item_id=item.id)
        self.assertEqual(record.quantity, 7)


class TestDropFullStack(InvTestBase):
    def test_drop_full_stack(self):
        from world.inventory_engine import drop_item
        item = self._make_item("pelt", location=self.char1, stackable=True)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id, quantity=12
        )
        success, _ = drop_item(self.char1, item)
        self.assertTrue(success)
        self.assertFalse(InventoryItem.objects.filter(item_id=item.id).exists())


# --- Container operations ---

class TestPutInContainerSetsId(InvTestBase):
    def test_put_in_container_sets_container_id(self):
        from world.inventory_engine import put_in_container
        bag = self._make_container("bag", weight_capacity=50.0)
        item = self._make_item("gem", location=self.char1, weight=0.5)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id
        )
        success, _ = put_in_container(self.char1, item, bag)
        self.assertTrue(success)
        record = InventoryItem.objects.get(item_id=item.id)
        self.assertEqual(record.container_id, bag.id)


class TestPutContainerInContainerFails(InvTestBase):
    def test_put_container_in_container_fails(self):
        from world.inventory_engine import put_in_container
        bag1 = self._make_container("bag1", weight_capacity=50.0)
        bag2 = self._make_container("bag2", weight_capacity=50.0)
        success, msg = put_in_container(self.char1, bag2, bag1)
        self.assertFalse(success)


class TestPutExceedsCapacityFails(InvTestBase):
    def test_put_exceeds_capacity_fails(self):
        from world.inventory_engine import put_in_container
        bag = self._make_container("tiny bag", weight_capacity=1.0,
                                    weight_reduction=0)
        item = self._make_item("heavy rock", location=self.char1, weight=5.0)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id
        )
        success, _ = put_in_container(self.char1, item, bag)
        self.assertFalse(success)


class TestTakeFromContainer(InvTestBase):
    def test_take_from_container_clears_container_id(self):
        from world.inventory_engine import put_in_container, take_from_container
        bag = self._make_container("bag", weight_capacity=50.0)
        item = self._make_item("gem", location=self.char1, weight=0.1)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id
        )
        put_in_container(self.char1, item, bag)
        success, _ = take_from_container(self.char1, item, bag)
        self.assertTrue(success)
        record = InventoryItem.objects.get(item_id=item.id)
        self.assertIsNone(record.container_id)


class TestTakeFromWrongContainer(InvTestBase):
    def test_take_from_wrong_container_fails(self):
        from world.inventory_engine import put_in_container, take_from_container
        bag_a = self._make_container("bag A", weight_capacity=50.0)
        bag_b = self._make_container("bag B", weight_capacity=50.0)
        item = self._make_item("gem", location=self.char1, weight=0.1)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id
        )
        put_in_container(self.char1, item, bag_a)
        success, _ = take_from_container(self.char1, item, bag_b)
        self.assertFalse(success)


class TestContainerContentsWeightWithReduction(InvTestBase):
    def test_container_contents_weight_with_reduction(self):
        from world.inventory_engine import _get_container_contents_weight
        bag = self._make_container("magic bag", weight_capacity=100.0,
                                    weight_reduction=50)
        item = self._make_item("ore", location=self.char1, weight=10.0)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id,
            container_id=bag.id, quantity=2
        )
        # 10.0 * 2 * (1 - 0.50) = 10.0
        weight = _get_container_contents_weight(self.char1, bag)
        self.assertAlmostEqual(weight, 10.0, places=1)


# --- Equip / Unequip ---

class TestEquipSetsFlag(InvTestBase):
    def test_equip_item_sets_equipped_flag(self):
        from world.inventory_engine import equip_item
        eq = self._make_equipment("helm", "head", location=self.char1)
        success, _ = equip_item(self.char1, eq)
        self.assertTrue(success)
        record = InventoryItem.objects.get(item_id=eq.id)
        self.assertTrue(record.is_equipped)
        self.assertEqual(record.equipment_slot, "head")


class TestEquipInContainerFails(InvTestBase):
    def test_equip_in_container_fails(self):
        from world.inventory_engine import equip_item
        bag = self._make_container("bag", weight_capacity=50.0)
        eq = self._make_equipment("helm", "head", location=self.char1)
        record = InventoryItem.objects.get(item_id=eq.id)
        record.container_id = bag.id
        record.save()
        success, _ = equip_item(self.char1, eq)
        self.assertFalse(success)


class TestEquipOccupiedSlotFails(InvTestBase):
    def test_equip_occupied_slot_fails(self):
        from world.inventory_engine import equip_item
        eq1 = self._make_equipment("sword1", "right_hand", location=self.char1)
        equip_item(self.char1, eq1)
        eq2 = self._make_equipment("sword2", "right_hand", location=self.char1)
        success, _ = equip_item(self.char1, eq2)
        self.assertFalse(success)


class TestUnequipClearsFlags(InvTestBase):
    def test_unequip_clears_flags(self):
        from world.inventory_engine import equip_item, unequip_item
        eq = self._make_equipment("helm", "head", location=self.char1)
        equip_item(self.char1, eq)
        success, _ = unequip_item(self.char1, eq)
        self.assertTrue(success)
        record = InventoryItem.objects.get(item_id=eq.id)
        self.assertFalse(record.is_equipped)
        self.assertIsNone(record.equipment_slot)


class TestUnequipNotEquippedFails(InvTestBase):
    def test_unequip_not_equipped_fails(self):
        from world.inventory_engine import unequip_item
        eq = self._make_equipment("helm", "head", location=self.char1)
        success, _ = unequip_item(self.char1, eq)
        self.assertFalse(success)


class TestEquipItemsInEmptySlots(InvTestBase):
    def test_auto_equip_fills_empty_slots_without_displacing_existing_gear(self):
        from world.inventory_engine import equip_item, equip_items_in_empty_slots

        existing_chest = self._make_equipment(
            "existing coat", "chest", location=self.char1
        )
        starter_chest = self._make_equipment(
            "starter vest", "chest", location=self.char1
        )
        starter_weapon = self._make_equipment(
            "starter sword", "main_hand", location=self.char1
        )
        equip_item(self.char1, existing_chest)

        ok, msg = equip_items_in_empty_slots(
            self.char1,
            [starter_chest, starter_weapon],
        )

        self.assertTrue(ok, msg)
        existing_record = InventoryItem.objects.get(item_id=existing_chest.id)
        chest_record = InventoryItem.objects.get(item_id=starter_chest.id)
        weapon_record = InventoryItem.objects.get(item_id=starter_weapon.id)
        self.assertTrue(existing_record.is_equipped)
        self.assertFalse(chest_record.is_equipped)
        self.assertTrue(weapon_record.is_equipped)
        self.assertEqual(weapon_record.equipment_slot, "main_hand")

    def test_auto_equip_equips_only_one_item_per_empty_slot(self):
        from world.inventory_engine import equip_items_in_empty_slots

        first = self._make_equipment("first dagger", "main_hand", self.char1)
        second = self._make_equipment("second dagger", "main_hand", self.char1)

        ok, msg = equip_items_in_empty_slots(self.char1, [first, second])

        self.assertTrue(ok, msg)
        first_record = InventoryItem.objects.get(item_id=first.id)
        second_record = InventoryItem.objects.get(item_id=second.id)
        self.assertTrue(first_record.is_equipped)
        self.assertFalse(second_record.is_equipped)


# --- Encumbrance ---

class TestOverloadedBlocksMovement(InvTestBase):
    def test_overloaded_blocks_movement(self):
        from typeclasses.rooms import SoravelonRoom
        dest = create_object(SoravelonRoom, key="Dest Room")
        # Add 100 kg (capacity 60, 167% = overloaded)
        heavy = self._make_item("boulder", location=self.char1, weight=100.0)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=heavy.id
        )
        result = self.char1.at_before_move(dest)
        self.assertFalse(result)


class TestEncumberedAllowsMovement(InvTestBase):
    @patch("world.recovery_engine.push_stat_update")
    def test_encumbered_movement_costs_two_stamina(self, _push_update):
        from typeclasses.rooms import SoravelonRoom
        dest = create_object(SoravelonRoom, key="Dest Room")
        # Add 70 kg (capacity 60, 117% = encumbered, not overloaded)
        heavy = self._make_item("pack", location=self.char1, weight=70.0)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=heavy.id
        )
        self.char1.ndb.stamina = 10

        result = self.char1.at_before_move(dest)

        self.assertTrue(result)
        self.assertEqual(self.char1.ndb.stamina, 8)

    @patch("world.recovery_engine.push_stat_update")
    def test_heavy_movement_costs_five_stamina(self, _push_update):
        from typeclasses.rooms import SoravelonRoom

        dest = create_object(SoravelonRoom, key="Dest Room")
        pack = self._make_item("loaded pack", location=self.char1, weight=90.0)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=pack.id
        )
        self.char1.ndb.stamina = 10

        result = self.char1.at_before_move(dest)

        self.assertTrue(result)
        self.assertEqual(self.char1.ndb.stamina, 5)

    @patch("world.recovery_engine.push_stat_update")
    def test_encumbered_movement_requires_enough_stamina(self, _push_update):
        from typeclasses.rooms import SoravelonRoom

        dest = create_object(SoravelonRoom, key="Dest Room")
        pack = self._make_item("pack", location=self.char1, weight=70.0)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=pack.id
        )
        self.char1.ndb.stamina = 1

        result = self.char1.at_before_move(dest)

        self.assertFalse(result)
        self.assertEqual(self.char1.ndb.stamina, 1)


# --- Query helpers ---

class TestInventoryDisplayStructure(InvTestBase):
    def test_get_inventory_display_data_structure(self):
        from world.inventory_engine import get_inventory_display_data
        data = get_inventory_display_data(self.char1)
        for key in ("equipped", "containers", "carried", "keyring",
                     "carried_scales", "carry_state", "carry_weight",
                     "carry_capacity"):
            self.assertIn(key, data)


class TestFilteredInventoryByName(InvTestBase):
    def test_get_filtered_inventory_by_name(self):
        from world.inventory_engine import get_filtered_inventory
        item = self._make_item("wolf pelt", location=self.char1)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id
        )
        matches = get_filtered_inventory(self.char1, "pelt")
        self.assertEqual(len(matches), 1)


class TestFilteredInventoryByType(InvTestBase):
    def test_get_filtered_inventory_by_type(self):
        from world.inventory_engine import get_filtered_inventory
        item = self._make_item("health draught", location=self.char1,
                                item_type="consumable")
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id
        )
        matches = get_filtered_inventory(self.char1, "consumable")
        self.assertEqual(len(matches), 1)


class TestGetEquippedItems(InvTestBase):
    def test_get_equipped_items(self):
        from world.inventory_engine import equip_item, get_equipped_items
        eq = self._make_equipment("helm", "head", location=self.char1)
        equip_item(self.char1, eq)
        unequipped = self._make_item("rock", location=self.char1)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=unequipped.id
        )
        equipped = get_equipped_items(self.char1)
        self.assertEqual(len(equipped), 1)
        self.assertEqual(equipped[0][0], eq)
