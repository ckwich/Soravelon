"""Pure vendor catalog, appraisal, and rendering tests.

Mutation behavior lives in ``test_composite_economy`` because buy and sell are
now database-backed, exactly-once workflows rather than mock-object logic.
"""

import math
import unittest
from unittest.mock import MagicMock, patch


def _make_character():
    character = MagicMock()
    character.db.carried_scales = 100
    return character


def _make_vendor(
    vendor_accepts=None,
    vendor_faction=None,
    player_stock=None,
    vendor_item_ids=None,
    vendor_exclude_item_ids=None,
):
    vendor = MagicMock()
    vendor.db.is_vendor = True
    vendor.db.vendor_accepts = vendor_accepts or ["equipment"]
    vendor.db.vendor_faction = vendor_faction
    vendor.db.player_stock = player_stock or {}
    vendor.db.vendor_item_ids = vendor_item_ids or []
    vendor.db.vendor_exclude_item_ids = vendor_exclude_item_ids or []
    return vendor


def _make_item(value_scales=25):
    item = MagicMock()
    item.key = "Iron Sword"
    item.db.item_type = "equipment"
    item.db.value_scales = value_scales
    item.can_be_sold.return_value = (True, None)
    return item


class TestGetVendorStock(unittest.TestCase):
    @patch(
        "world.vendor_engine.CATALOG",
        {
            "iron_sword": {
                "item_id": "iron_sword",
                "item_type": "equipment",
                "value": 25,
            },
            "minor_healing_potion": {
                "item_id": "minor_healing_potion",
                "item_type": "consumable",
                "value": 10,
            },
        },
    )
    def test_get_vendor_stock_filters_by_type(self):
        from world.vendor_engine import get_vendor_stock

        stock = get_vendor_stock(_make_vendor(vendor_accepts=["equipment"]))

        self.assertIn("iron_sword", stock)
        self.assertNotIn("minor_healing_potion", stock)

    @patch(
        "world.vendor_engine.CATALOG",
        {
            "iron_sword": {
                "item_id": "iron_sword",
                "item_type": "equipment",
                "value": 25,
            },
            "steel_sword": {
                "item_id": "steel_sword",
                "item_type": "equipment",
                "value": 60,
            },
        },
    )
    def test_vendor_item_ids_curate_base_stock(self):
        from world.vendor_engine import get_vendor_stock

        stock = get_vendor_stock(
            _make_vendor(
                vendor_accepts=["equipment"],
                vendor_item_ids=["steel_sword"],
            )
        )

        self.assertNotIn("iron_sword", stock)
        self.assertIn("steel_sword", stock)

    @patch(
        "world.vendor_engine.CATALOG",
        {
            "stolen_artifact": {
                "item_id": "stolen_artifact",
                "item_type": "item",
                "value": 0,
                "is_quest_item": True,
            }
        },
    )
    def test_vendor_stock_excludes_base_quest_items(self):
        from world.vendor_engine import get_vendor_stock

        stock = get_vendor_stock(_make_vendor(vendor_accepts=["item"]))
        self.assertNotIn("stolen_artifact", stock)

    @patch(
        "world.vendor_engine.CATALOG",
        {
            "iron_sword": {
                "item_id": "iron_sword",
                "item_type": "equipment",
                "value": 25,
            }
        },
    )
    def test_player_sold_items_in_stock(self):
        from world.vendor_engine import get_vendor_stock

        stock = get_vendor_stock(
            _make_vendor(
                vendor_accepts=["equipment"],
                player_stock={
                    "used_sword": {
                        "item_id": "used_sword",
                        "key": "Used Sword",
                        "item_type": "equipment",
                        "value": 15,
                    }
                },
            )
        )

        self.assertIn("iron_sword", stock)
        self.assertIn("used_sword", stock)


class TestGetVendorPrice(unittest.TestCase):
    @patch("world.world_state.get_standing", return_value=-100_000)
    def test_negative_standing_never_becomes_an_unadvertised_markup(self, _standing):
        from world.vendor_engine import get_vendor_price

        price = get_vendor_price(
            _make_vendor(vendor_faction="consortium"),
            {"value": 100},
            _make_character(),
        )

        self.assertEqual(price, 100)

    @patch("world.world_state.get_standing", return_value=50_000)
    def test_half_scale_standing_earns_half_the_maximum_discount(self, _standing):
        from world.vendor_engine import get_vendor_price

        price = get_vendor_price(
            _make_vendor(vendor_faction="consortium"),
            {"value": 100},
            _make_character(),
        )

        self.assertEqual(price, 90)

    @patch("world.world_state.get_standing", return_value=100_000)
    def test_canonical_maximum_standing_earns_twenty_percent_discount(self, _standing):
        from world.vendor_engine import get_vendor_price

        price = get_vendor_price(
            _make_vendor(vendor_faction="consortium"),
            {"value": 100},
            _make_character(),
        )

        self.assertEqual(price, 80)


class TestAppraiseItem(unittest.TestCase):
    def test_appraise_returns_sell_price(self):
        from world.vendor_engine import appraise_item

        ok, message = appraise_item(
            _make_character(),
            _make_vendor(vendor_accepts=["equipment"]),
            _make_item(value_scales=25),
        )

        self.assertTrue(ok)
        self.assertIn(str(max(1, math.floor(25 * 0.33))), message)


class TestViewItem(unittest.TestCase):
    @patch(
        "world.vendor_engine.CATALOG",
        {
            "iron_sword": {
                "item_id": "iron_sword",
                "key": "Iron Sword",
                "item_type": "equipment",
                "value": 25,
                "damage_min": 8,
                "damage_max": 14,
                "stat_bonuses": {"strength": 1},
                "desc": "A sturdy sword.",
                "rarity": "normal",
            }
        },
    )
    def test_view_item_returns_stats(self):
        from world.vendor_engine import view_item

        ok, message = view_item(
            _make_vendor(vendor_accepts=["equipment"]),
            "iron_sword",
        )

        self.assertTrue(ok)
        for expected in ("Iron Sword", "8", "14", "strength", "25"):
            self.assertIn(expected, message)

    @patch("world.vendor_engine.CATALOG", {})
    def test_view_item_not_found(self):
        from world.vendor_engine import view_item

        ok, _ = view_item(
            _make_vendor(vendor_accepts=["equipment"]),
            "nonexistent",
        )
        self.assertFalse(ok)

    @patch("world.vendor_engine.CATALOG", {})
    def test_view_item_shows_player_stock_quantity(self):
        from world.vendor_engine import view_item

        ok, message = view_item(
            _make_vendor(
                vendor_accepts=["equipment"],
                player_stock={
                    "used_sword": {
                        "item_id": "used_sword",
                        "key": "Used Sword",
                        "item_type": "equipment",
                        "value": 15,
                        "stock_quantity": 3,
                    }
                },
            ),
            "used_sword",
        )

        self.assertTrue(ok)
        self.assertIn("Stock: 3", message)


if __name__ == "__main__":
    unittest.main()
