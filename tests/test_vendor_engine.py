"""
Tests for the vendor engine.

Uses unittest.TestCase + MagicMock — no Evennia DB needed.
All vendor_engine functions are pure logic operating on mock objects.
"""

import math
import unittest
from unittest.mock import MagicMock, patch, PropertyMock


def _make_character(carried_scales=100):
    """Create a mock character with carried_scales."""
    char = MagicMock()
    char.db = MagicMock()
    char.db.carried_scales = carried_scales
    char.location = MagicMock()
    char.location.contents = []
    char.contents = []
    return char


def _make_vendor(vendor_accepts=None, vendor_faction=None, player_stock=None):
    """Create a mock vendor NPC."""
    vendor = MagicMock()
    vendor.db = MagicMock()
    vendor.db.is_vendor = True
    vendor.db.is_npc = True
    vendor.db.vendor_accepts = vendor_accepts or ["equipment"]
    vendor.db.vendor_faction = vendor_faction
    vendor.db.player_stock = player_stock or {}
    return vendor


def _make_item(key="Iron Sword", item_type="equipment", value_scales=25,
               is_quest_item=False, item_id="iron_sword", weight=3.0,
               rarity="normal", equipment_slot="main_hand",
               stat_bonuses=None, damage_min=8, damage_max=14):
    """Create a mock item."""
    item = MagicMock()
    item.key = key
    item.db = MagicMock()
    item.db.item_type = item_type
    item.db.value_scales = value_scales
    item.db.item_id = item_id
    item.db.weight = weight
    item.db.rarity = rarity
    item.db.desc = "A test item."
    item.db.equipment_slot = equipment_slot
    item.db.stat_bonuses = stat_bonuses or {}
    item.db.damage_min = damage_min
    item.db.damage_max = damage_max
    item.db.armor_value = 0
    item.db.is_quest_item = is_quest_item
    item.can_be_sold = MagicMock(return_value=(True, None))
    return item


class TestBuyItem(unittest.TestCase):
    """Tests for buy_item()."""

    @patch("world.vendor_engine.create_item_from_template")
    @patch("world.vendor_engine.CATALOG", {
        "iron_sword": {
            "item_id": "iron_sword", "key": "Iron Sword",
            "item_type": "equipment", "value": 25,
        },
    })
    def test_buy_item_success(self, mock_create):
        from world.vendor_engine import buy_item

        mock_item = MagicMock()
        mock_item.key = "Iron Sword"
        mock_create.return_value = mock_item

        char = _make_character(carried_scales=100)
        vendor = _make_vendor(vendor_accepts=["equipment"])

        ok, msg = buy_item(char, vendor, "iron_sword")

        self.assertTrue(ok)
        self.assertIn("Iron Sword", msg)
        self.assertIn("25", msg)
        self.assertEqual(char.db.carried_scales, 75)
        mock_create.assert_called_once()

    @patch("world.vendor_engine.CATALOG", {
        "iron_sword": {
            "item_id": "iron_sword", "key": "Iron Sword",
            "item_type": "equipment", "value": 25,
        },
    })
    def test_buy_item_insufficient_funds(self):
        from world.vendor_engine import buy_item

        char = _make_character(carried_scales=10)
        vendor = _make_vendor(vendor_accepts=["equipment"])

        ok, msg = buy_item(char, vendor, "iron_sword")

        self.assertFalse(ok)
        self.assertIn("Scales", msg)
        # Scales unchanged
        self.assertEqual(char.db.carried_scales, 10)

    @patch("world.vendor_engine.CATALOG", {})
    def test_buy_item_not_in_stock(self):
        from world.vendor_engine import buy_item

        char = _make_character(carried_scales=100)
        vendor = _make_vendor(vendor_accepts=["equipment"])

        ok, msg = buy_item(char, vendor, "nonexistent_item")

        self.assertFalse(ok)
        self.assertIn("not available", msg)


class TestSellItem(unittest.TestCase):
    """Tests for sell_item()."""

    def test_sell_item_success(self):
        from world.vendor_engine import sell_item

        char = _make_character(carried_scales=50)
        vendor = _make_vendor(vendor_accepts=["equipment"])
        item = _make_item(key="Iron Sword", item_type="equipment", value_scales=25)

        ok, msg = sell_item(char, vendor, item)

        self.assertTrue(ok)
        expected_price = max(1, math.floor(25 * 0.33))  # 8
        self.assertEqual(char.db.carried_scales, 50 + expected_price)
        self.assertIn("Iron Sword", msg)
        self.assertIn(str(expected_price), msg)
        item.delete.assert_called_once()

    def test_sell_item_quest_blocked(self):
        from world.vendor_engine import sell_item

        char = _make_character(carried_scales=50)
        vendor = _make_vendor(vendor_accepts=["equipment"])
        item = _make_item(is_quest_item=True)
        item.can_be_sold = MagicMock(return_value=(False, "A vendor wouldn't take that from you."))

        ok, msg = sell_item(char, vendor, item)

        self.assertFalse(ok)
        self.assertIn("vendor", msg.lower())
        item.delete.assert_not_called()

    def test_sell_item_type_rejected(self):
        from world.vendor_engine import sell_item

        char = _make_character(carried_scales=50)
        vendor = _make_vendor(vendor_accepts=["equipment"])  # only equipment
        item = _make_item(item_type="consumable")  # trying to sell consumable

        ok, msg = sell_item(char, vendor, item)

        self.assertFalse(ok)
        self.assertIn("doesn't deal", msg)
        item.delete.assert_not_called()


class TestGetVendorStock(unittest.TestCase):
    """Tests for get_vendor_stock()."""

    @patch("world.vendor_engine.CATALOG", {
        "iron_sword": {"item_id": "iron_sword", "item_type": "equipment", "value": 25},
        "minor_healing_potion": {"item_id": "minor_healing_potion", "item_type": "consumable", "value": 10},
    })
    def test_get_vendor_stock_filters_by_type(self):
        from world.vendor_engine import get_vendor_stock

        vendor = _make_vendor(vendor_accepts=["equipment"])

        stock = get_vendor_stock(vendor)

        self.assertIn("iron_sword", stock)
        self.assertNotIn("minor_healing_potion", stock)

    @patch("world.vendor_engine.CATALOG", {
        "iron_sword": {"item_id": "iron_sword", "item_type": "equipment", "value": 25},
    })
    def test_player_sold_items_in_stock(self):
        from world.vendor_engine import get_vendor_stock

        player_stock = {
            "used_sword": {
                "item_id": "used_sword", "key": "Used Sword",
                "item_type": "equipment", "value": 15,
            }
        }
        vendor = _make_vendor(vendor_accepts=["equipment"], player_stock=player_stock)

        stock = get_vendor_stock(vendor)

        self.assertIn("iron_sword", stock)
        self.assertIn("used_sword", stock)


class TestAppraiseItem(unittest.TestCase):
    """Tests for appraise_item()."""

    def test_appraise_returns_sell_price(self):
        from world.vendor_engine import appraise_item

        char = _make_character()
        vendor = _make_vendor(vendor_accepts=["equipment"])
        item = _make_item(value_scales=25)

        ok, msg = appraise_item(char, vendor, item)

        self.assertTrue(ok)
        expected = max(1, math.floor(25 * 0.33))  # 8
        self.assertIn(str(expected), msg)


class TestViewItem(unittest.TestCase):
    """Tests for view_item()."""

    @patch("world.vendor_engine.CATALOG", {
        "iron_sword": {
            "item_id": "iron_sword", "key": "Iron Sword",
            "item_type": "equipment", "value": 25,
            "damage_min": 8, "damage_max": 14,
            "stat_bonuses": {"strength": 1},
            "desc": "A sturdy sword.",
            "rarity": "normal",
        },
    })
    def test_view_item_returns_stats(self):
        from world.vendor_engine import view_item

        vendor = _make_vendor(vendor_accepts=["equipment"])

        ok, msg = view_item(vendor, "iron_sword")

        self.assertTrue(ok)
        self.assertIn("Iron Sword", msg)
        self.assertIn("8", msg)  # damage_min
        self.assertIn("14", msg)  # damage_max
        self.assertIn("strength", msg)
        self.assertIn("25", msg)  # value

    @patch("world.vendor_engine.CATALOG", {})
    def test_view_item_not_found(self):
        from world.vendor_engine import view_item

        vendor = _make_vendor(vendor_accepts=["equipment"])

        ok, msg = view_item(vendor, "nonexistent")

        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
