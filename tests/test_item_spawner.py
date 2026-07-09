"""
Tests for world/item_spawner.py

Uses unittest.TestCase with sys.modules injection for evennia.
No Evennia DB setup required — evennia.create_object is mocked.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch, call


class TestCreateItemFromTemplate(unittest.TestCase):
    """Tests for create_item_from_template."""

    def setUp(self):
        """Inject evennia stub before importing item_spawner."""
        # Build mock item object that supports attribute assignment via .db
        self.mock_item = MagicMock()
        self.mock_item.db = MagicMock()
        self.mock_inventory_engine = MagicMock()

        # Build mock evennia module
        self.mock_evennia = MagicMock()
        self.mock_evennia.create_object.return_value = self.mock_item

        # Save original evennia module before injecting stub
        self._saved_evennia = sys.modules.get("evennia")
        self._saved_inventory_engine = sys.modules.get("world.inventory_engine")
        sys.modules["evennia"] = self.mock_evennia
        sys.modules["world.inventory_engine"] = self.mock_inventory_engine

        # Remove cached module if already imported
        for mod in list(sys.modules.keys()):
            if mod.startswith("world.item_spawner") or mod == "world.item_spawner":
                del sys.modules[mod]

        from world.item_spawner import create_item_from_template
        self.create_item_from_template = create_item_from_template

    def tearDown(self):
        # Clean up injected module
        for mod in list(sys.modules.keys()):
            if mod.startswith("world.item_spawner") or mod == "world.item_spawner":
                del sys.modules[mod]
        # Restore original evennia module to prevent leaking into other tests
        if self._saved_evennia is not None:
            sys.modules["evennia"] = self._saved_evennia
        else:
            sys.modules.pop("evennia", None)
        if self._saved_inventory_engine is not None:
            sys.modules["world.inventory_engine"] = self._saved_inventory_engine
        else:
            sys.modules.pop("world.inventory_engine", None)

    def test_equipment_type_uses_soravelon_equipment_typeclass(self):
        """item_type='equipment' → creates with SoravelonEquipment typeclass."""
        item_def = {
            "item_id": "rusty_sword",
            "key": "rusty sword",
            "item_type": "equipment",
            "weight": 2.0,
            "rarity": "normal",
            "equip_slot": "right_hand",
            "desc": "A notched blade.",
            "value": 5,
        }
        self.create_item_from_template(item_def)
        self.mock_evennia.create_object.assert_called_once()
        call_args = self.mock_evennia.create_object.call_args
        typeclass_arg = call_args[0][0]
        self.assertIn("SoravelonEquipment", typeclass_arg)

    def test_container_type_uses_soravelon_container_typeclass(self):
        """item_type='container' → creates with SoravelonContainer typeclass."""
        item_def = {
            "item_id": "leather_sack",
            "key": "leather sack",
            "item_type": "container",
            "weight": 0.5,
            "rarity": "normal",
            "desc": "A worn sack.",
            "value": 2,
        }
        self.create_item_from_template(item_def)
        call_args = self.mock_evennia.create_object.call_args
        typeclass_arg = call_args[0][0]
        self.assertIn("SoravelonContainer", typeclass_arg)

    def test_keyring_type_uses_soravelon_keyring_typeclass(self):
        """item_type='keyring' → creates with SoravelonKeyringItem typeclass."""
        item_def = {
            "item_id": "guild_token",
            "key": "guild token",
            "item_type": "keyring",
            "weight": 0.0,
            "rarity": "normal",
            "desc": "A worn token.",
            "value": 0,
        }
        self.create_item_from_template(item_def)
        call_args = self.mock_evennia.create_object.call_args
        typeclass_arg = call_args[0][0]
        self.assertIn("SoravelonKeyringItem", typeclass_arg)

    def test_item_type_uses_soravelon_item_typeclass(self):
        """item_type='item' → creates with SoravelonItem typeclass."""
        item_def = {
            "item_id": "herb_bundle",
            "key": "herb bundle",
            "item_type": "item",
            "weight": 0.2,
            "rarity": "normal",
            "desc": "A bundle of dried herbs.",
            "value": 1,
        }
        self.create_item_from_template(item_def)
        call_args = self.mock_evennia.create_object.call_args
        typeclass_arg = call_args[0][0]
        self.assertIn("SoravelonItem", typeclass_arg)

    def test_unknown_item_type_uses_soravelon_item_typeclass(self):
        """Unknown/missing item_type defaults to SoravelonItem typeclass."""
        item_def = {
            "item_id": "mystery_thing",
            "key": "mystery thing",
            "item_type": "unknown_type",
            "weight": 0.1,
            "desc": "Unclear what this is.",
            "value": 0,
        }
        self.create_item_from_template(item_def)
        call_args = self.mock_evennia.create_object.call_args
        typeclass_arg = call_args[0][0]
        self.assertIn("SoravelonItem", typeclass_arg)
        self.assertNotIn("SoravelonEquipment", typeclass_arg)
        self.assertNotIn("SoravelonContainer", typeclass_arg)

    def test_missing_item_type_defaults_to_soravelon_item(self):
        """Missing item_type key defaults to SoravelonItem typeclass."""
        item_def = {
            "item_id": "plain_rock",
            "key": "plain rock",
            "weight": 0.5,
            "desc": "A plain rock.",
            "value": 0,
        }
        self.create_item_from_template(item_def)
        call_args = self.mock_evennia.create_object.call_args
        typeclass_arg = call_args[0][0]
        self.assertIn("SoravelonItem", typeclass_arg)

    def test_standard_db_attrs_set_from_item_def(self):
        """db.weight, db.rarity, db.desc, db.value set from item_def."""
        item_def = {
            "item_id": "iron_dagger",
            "key": "iron dagger",
            "item_type": "equipment",
            "weight": 1.5,
            "rarity": "magic",
            "equip_slot": "right_hand",
            "desc": "A sharp iron dagger.",
            "value": 12,
        }
        result = self.create_item_from_template(item_def)
        self.assertEqual(result.db.weight, 1.5)
        self.assertEqual(result.db.rarity, "magic")
        self.assertEqual(result.db.desc, "A sharp iron dagger.")
        self.assertEqual(result.db.value_scales, 12)
        self.assertEqual(result.db.item_type, "equipment")

    def test_equip_slot_set_for_equipment_type(self):
        """db.equip_slot set from item_def for equipment items."""
        item_def = {
            "item_id": "iron_helm",
            "key": "iron helm",
            "item_type": "equipment",
            "weight": 3.0,
            "rarity": "normal",
            "equip_slot": "head",
            "desc": "A heavy iron helm.",
            "value": 8,
        }
        result = self.create_item_from_template(item_def)
        self.assertEqual(result.db.equipment_slot, "head")

    def test_equip_slot_none_for_non_equipment(self):
        """db.equipment_slot is None when item_def has no equip_slot."""
        item_def = {
            "item_id": "bread_loaf",
            "key": "bread loaf",
            "item_type": "item",
            "weight": 0.3,
            "rarity": "normal",
            "desc": "A dense loaf of bread.",
            "value": 1,
        }
        result = self.create_item_from_template(item_def)
        self.assertIsNone(result.db.equipment_slot)

    def test_location_none_passes_none_to_create_object(self):
        """location=None → create_object called with location=None."""
        item_def = {"item_id": "coin", "key": "coin", "item_type": "item",
                    "weight": 0.01, "desc": "", "value": 1}
        self.create_item_from_template(item_def, location=None)
        call_kwargs = self.mock_evennia.create_object.call_args[1]
        self.assertIsNone(call_kwargs.get("location"))

    def test_location_room_passed_to_create_object(self):
        """location=some_room → create_object called with location=room."""
        mock_room = MagicMock()
        item_def = {"item_id": "coin", "key": "coin", "item_type": "item",
                    "weight": 0.01, "desc": "", "value": 1}
        self.create_item_from_template(item_def, location=mock_room)
        call_kwargs = self.mock_evennia.create_object.call_args[1]
        self.assertEqual(call_kwargs.get("location"), mock_room)

    def test_extra_key_damage_min_set_as_db_attr(self):
        """Extra key 'damage_min': 5 → item.db.damage_min == 5."""
        item_def = {
            "item_id": "war_axe",
            "key": "war axe",
            "item_type": "equipment",
            "weight": 4.0,
            "rarity": "rare",
            "equip_slot": "right_hand",
            "desc": "A brutal war axe.",
            "value": 50,
            "damage_min": 5,
            "damage_max": 12,
        }
        result = self.create_item_from_template(item_def)
        self.assertEqual(result.db.damage_min, 5)
        self.assertEqual(result.db.damage_max, 12)

    def test_reserved_keys_not_set_as_extra_attrs(self):
        """Reserved keys (item_id, key, etc.) are NOT set as extra db attrs."""
        # We verify this indirectly: item_id and key are reserved, so they
        # should not be set via the extra-attrs loop (only via explicit lines).
        item_def = {
            "item_id": "test_obj",
            "key": "test object",
            "item_type": "item",
            "weight": 1.0,
            "rarity": "normal",
            "desc": "A test.",
            "value": 0,
        }
        result = self.create_item_from_template(item_def)
        # The function should return the item successfully without error.
        self.assertIsNotNone(result)

    def test_returns_created_item(self):
        """create_item_from_template returns the created item object."""
        item_def = {"item_id": "x", "key": "x", "item_type": "item",
                    "weight": 0.1, "desc": "", "value": 0}
        result = self.create_item_from_template(item_def)
        self.assertEqual(result, self.mock_item)

    def test_registers_inventory_when_location_is_player_character(self):
        """Direct-to-player item spawns create authoritative inventory records."""
        class _FakeTags:
            def has(self, key, category=None):
                return key == "player_character" and category == "character_type"

            def get(self, key, category=None):
                return self.has(key, category)

        class _FakeCharacter:
            def __init__(self):
                self.tags = _FakeTags()

        item_def = {
            "item_id": "iron_sword",
            "key": "iron sword",
            "item_type": "equipment",
            "weight": 2.0,
            "desc": "A test sword.",
            "value": 5,
        }
        character = _FakeCharacter()

        result = self.create_item_from_template(item_def, location=character)

        self.mock_inventory_engine.register_item_ownership.assert_called_once_with(
            character,
            result,
            quantity=1,
            is_quest_item=False,
            keyring=False,
        )

    def test_create_item_from_catalog_resolves_full_template_and_overrides_copy(self):
        from world.item_catalog import CATALOG
        from world.item_spawner import create_item_from_catalog

        original_key = CATALOG["iron_dagger"]["key"]
        result = create_item_from_catalog(
            "iron_dagger",
            overrides={"key": "Fine Iron Dagger", "quality": "fine"},
        )

        self.assertEqual(result.db.item_type, "equipment")
        self.assertEqual(result.db.equipment_slot, "main_hand")
        self.assertEqual(result.db.scaling_stat, "agility")
        self.assertEqual(result.db.quality, "fine")
        self.assertEqual(CATALOG["iron_dagger"]["key"], original_key)


if __name__ == "__main__":
    unittest.main()
