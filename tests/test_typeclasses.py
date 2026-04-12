"""
Tests for Soravelon base typeclass hierarchy (Build Order Step 7).
Tests written FIRST per TDD.
"""

from evennia.utils.test_resources import EvenniaTest
from evennia import create_object
from world.models import InventoryItem


class ObjectTests(EvenniaTest):
    """Tests for SoravelonItem, Container, Equipment, KeyringItem."""

    def test_soravelon_item_creation(self):
        from typeclasses.objects import SoravelonItem
        item = create_object(SoravelonItem, key="wolf pelt")
        self.assertEqual(item.db.weight, 0.1)
        self.assertEqual(item.db.rarity, "common")
        self.assertIsNone(item.db.item_type)
        self.assertFalse(item.db.stackable)

    def test_quest_item_cannot_drop(self):
        from typeclasses.objects import SoravelonItem
        item = create_object(SoravelonItem, key="quest gem", location=self.char1)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id,
            is_quest_item=True, quest_id="test_quest"
        )
        can, msg = item.can_drop(self.char1)
        self.assertFalse(can)
        self.assertIsNotNone(msg)

    def test_non_quest_item_can_drop(self):
        from typeclasses.objects import SoravelonItem
        item = create_object(SoravelonItem, key="rock", location=self.char1)
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id
        )
        can, msg = item.can_drop(self.char1)
        self.assertTrue(can)
        self.assertIsNone(msg)

    def test_container_rejects_container(self):
        from typeclasses.objects import SoravelonContainer
        bag = create_object(SoravelonContainer, key="bag")
        small_bag = create_object(SoravelonContainer, key="small bag")
        can, msg = bag.can_accept(small_bag)
        self.assertFalse(can)
        self.assertIsNotNone(msg)

    def test_container_accepts_item(self):
        from typeclasses.objects import SoravelonContainer, SoravelonItem
        bag = create_object(SoravelonContainer, key="bag")
        item = create_object(SoravelonItem, key="gem")
        can, msg = bag.can_accept(item)
        self.assertTrue(can)
        self.assertIsNone(msg)

    def test_container_weight_reduction(self):
        from typeclasses.objects import SoravelonContainer
        bag = create_object(SoravelonContainer, key="magic bag")
        bag.db.weight_reduction = 25
        effective = bag.get_effective_weight_of(1.0, quantity=1)
        self.assertAlmostEqual(effective, 0.75, places=2)

    def test_equipment_valid_slot(self):
        from typeclasses.objects import SoravelonEquipment
        sword = create_object(SoravelonEquipment, key="iron sword",
                              location=self.char1)
        sword.db.equipment_slot = "main_hand"
        can, msg = sword.can_equip(self.char1)
        self.assertTrue(can)
        self.assertIsNone(msg)

    def test_equipment_invalid_slot(self):
        from typeclasses.objects import SoravelonEquipment
        junk = create_object(SoravelonEquipment, key="broken thing",
                             location=self.char1)
        junk.db.equipment_slot = "invalid"
        can, msg = junk.can_equip(self.char1)
        self.assertFalse(can)

    def test_keyring_item_cannot_drop(self):
        from typeclasses.objects import SoravelonKeyringItem
        key = create_object(SoravelonKeyringItem, key="seld key",
                            location=self.char1)
        can, msg = key.can_drop(self.char1)
        self.assertFalse(can)
        self.assertIsNotNone(msg)

    def test_keyring_item_zero_weight(self):
        from typeclasses.objects import SoravelonKeyringItem
        key = create_object(SoravelonKeyringItem, key="token")
        self.assertEqual(key.db.weight, 0.0)


class ExitTests(EvenniaTest):
    """Tests for exit typeclasses."""

    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom
        self.room_a = create_object(SoravelonRoom, key="Room A")
        self.room_b = create_object(SoravelonRoom, key="Room B")
        self.room_b.db.action_budget_penalty = 0

    def test_locked_exit_no_key_blocks(self):
        from typeclasses.exits import LockedExit
        exit_obj = create_object(
            LockedExit, key="locked door",
            location=self.room_a, destination=self.room_b
        )
        exit_obj.db.lock_tag = "test_key"
        self.char1.location = self.room_a

        result = exit_obj.at_traverse(self.char1, self.room_b)
        self.assertFalse(result)

    def test_locked_exit_with_key_allows(self):
        from typeclasses.exits import LockedExit
        from typeclasses.objects import SoravelonKeyringItem

        exit_obj = create_object(
            LockedExit, key="locked door",
            location=self.room_a, destination=self.room_b
        )
        exit_obj.db.lock_tag = "seld_warren_key"

        key = create_object(
            SoravelonKeyringItem, key="warren key",
            location=self.char1
        )
        key.db.unlocks_exit_tag = "seld_warren_key"
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=key.id, keyring=True
        )

        self.char1.location = self.room_a
        result = exit_obj.at_traverse(self.char1, self.room_b)
        # Evennia's at_traverse returns None on success, False on block
        self.assertNotEqual(result, False)

    def test_locked_exit_no_lock_tag_passthrough(self):
        from typeclasses.exits import LockedExit
        exit_obj = create_object(
            LockedExit, key="unlocked door",
            location=self.room_a, destination=self.room_b
        )
        exit_obj.db.lock_tag = None
        self.char1.location = self.room_a

        result = exit_obj.at_traverse(self.char1, self.room_b)
        # Should pass through (returns result of super, not False)
        self.assertNotEqual(result, False)

    def test_hidden_exit_invisible_before_discovery(self):
        from typeclasses.exits import HiddenExit
        exit_obj = create_object(
            HiddenExit, key="hidden passage",
            location=self.room_a, destination=self.room_b
        )
        self.assertFalse(exit_obj.is_visible(self.char1))

    def test_hidden_exit_visible_after_discovery(self):
        from typeclasses.exits import HiddenExit
        exit_obj = create_object(
            HiddenExit, key="hidden passage",
            location=self.room_a, destination=self.room_b
        )
        self.char1.db.discovered_exits = [exit_obj.id]
        self.assertTrue(exit_obj.is_visible(self.char1))

    def test_gravity_exit_sets_ndb_penalty(self):
        from typeclasses.exits import NodeGravityExit
        exit_obj = create_object(
            NodeGravityExit, key="heavy path",
            location=self.room_a, destination=self.room_b
        )
        self.char1.location = self.room_a
        exit_obj.at_traverse(self.char1, self.room_b)
        self.assertEqual(self.char1.ndb.gravity_penalty, -1)

    def test_base_exit_gravity_from_room_tag(self):
        from typeclasses.exits import SoravelonExit
        self.room_b.db.action_budget_penalty = -1
        exit_obj = create_object(
            SoravelonExit, key="path",
            location=self.room_a, destination=self.room_b
        )
        self.char1.location = self.room_a
        exit_obj.at_traverse(self.char1, self.room_b)
        self.assertEqual(self.char1.ndb.gravity_penalty, -1)


class InventoryWeightTests(EvenniaTest):
    """Tests for get_carry_state weight calculation."""

    def setUp(self):
        super().setUp()
        self.char1.db.strength = 10  # capacity = 10 + 50 = 60 kg

    def _add_item(self, weight, quantity=1, container_id=None):
        from typeclasses.objects import SoravelonItem
        item = create_object(SoravelonItem, key="item", location=self.char1)
        item.db.weight = weight
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=item.id,
            quantity=quantity, container_id=container_id
        )
        return item

    def test_carry_state_normal(self):
        from world.inventory_helpers import get_carry_state
        self._add_item(5.0, quantity=1)  # 5 kg of 60 capacity
        self.assertEqual(get_carry_state(self.char1), "normal")

    def test_carry_state_encumbered(self):
        from world.inventory_helpers import get_carry_state
        self._add_item(10.0, quantity=7)  # 70 kg, 117% of 60
        self.assertEqual(get_carry_state(self.char1), "encumbered")

    def test_carry_state_heavy(self):
        from world.inventory_helpers import get_carry_state
        self._add_item(10.0, quantity=9)  # 90 kg, 150% of 60
        self.assertEqual(get_carry_state(self.char1), "heavy")

    def test_carry_state_overloaded(self):
        from world.inventory_helpers import get_carry_state
        self._add_item(10.0, quantity=10)  # 100 kg, 167% of 60
        self.assertEqual(get_carry_state(self.char1), "overloaded")

    def test_container_weight_reduction_in_carry_calc(self):
        from world.inventory_helpers import get_carry_state
        from typeclasses.objects import SoravelonContainer

        bag = create_object(SoravelonContainer, key="bag", location=self.char1)
        bag.db.weight_reduction = 50
        bag.db.weight = 1.0
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=bag.id
        )
        # Item inside bag: 40kg * 0.5 reduction = 20kg + 1kg bag = 21kg
        self._add_item(40.0, quantity=1, container_id=bag.id)
        self.assertEqual(get_carry_state(self.char1), "normal")

    def test_container_own_weight_full(self):
        from world.inventory_helpers import get_carry_state
        from typeclasses.objects import SoravelonContainer

        bag = create_object(SoravelonContainer, key="heavy bag",
                            location=self.char1)
        bag.db.weight = 55.0  # heavy bag, 92% of capacity alone
        bag.db.weight_reduction = 90
        InventoryItem.objects.create(
            character_id=self.char1.id, item_id=bag.id
        )
        # Bag weighs 55kg of 60 capacity = normal
        self.assertEqual(get_carry_state(self.char1), "normal")


class AccountTests(EvenniaTest):
    """Tests for SoravelonAccount."""

    def test_account_default_preferences(self):
        from typeclasses.accounts import SoravelonAccount
        from evennia import create_account
        acct = create_account(
            "testacct", "test@test.com", "Xk9$mP2vLq!wR4",
            typeclass=SoravelonAccount
        )
        self.assertTrue(acct.db.color_enabled)
        self.assertFalse(acct.db.brief_mode)
        self.assertTrue(acct.db.hints_enabled)
        self.assertEqual(acct.db.inv_sort, "type")

    def test_account_aliases_empty_on_creation(self):
        from typeclasses.accounts import SoravelonAccount
        from evennia import create_account
        acct = create_account(
            "testacct2", "test2@test.com", "Yp7#nQ3wKs!vT8",
            typeclass=SoravelonAccount
        )
        self.assertIn(acct.db.command_aliases, (None, {}))
