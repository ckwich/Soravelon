"""Canonical standing-scale helpers shared by every relationship consumer."""

import unittest
from unittest.mock import MagicMock

from evennia.utils.test_resources import EvenniaTest


class TestStandingScale(unittest.TestCase):
    def test_fraction_clamps_to_the_documented_internal_range(self):
        from world.standing import standing_fraction

        self.assertEqual(standing_fraction(-200_000), -1.0)
        self.assertEqual(standing_fraction(-50_000), -0.5)
        self.assertEqual(standing_fraction(50_000), 0.5)
        self.assertEqual(standing_fraction(200_000), 1.0)

    def test_benefit_fraction_never_turns_negative_standing_into_a_discount(self):
        from world.standing import standing_benefit_fraction

        self.assertEqual(standing_benefit_fraction(-100_000), 0.0)
        self.assertEqual(standing_benefit_fraction(0), 0.0)
        self.assertEqual(standing_benefit_fraction(50_000), 0.5)
        self.assertEqual(standing_benefit_fraction(100_000), 1.0)


class TestStandingEconomyVertical(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.flight_registry import FlightRegistry

        FlightRegistry.clear()

    def tearDown(self):
        from world.flight_registry import FlightRegistry

        FlightRegistry.clear()
        super().tearDown()

    def test_authored_action_persists_and_changes_two_real_economy_consumers(self):
        from world.action_vocabulary import execute_action
        from world.flight_engine import fare_for_route
        from world.flight_registry import FlightRegistry
        from world.vendor_engine import get_vendor_price
        from world.world_state import get_standing

        success, message = execute_action(
            {
                "action_type": "modify_standing",
                "faction_id": "consortium",
                "delta": 25_000,
            },
            {"character": self.char1},
        )

        self.assertTrue(success, message)
        self.assertEqual(get_standing(self.char1, "consortium"), 25_000)

        origin = MagicMock(id=101)
        origin.db.zone_id = "test_zone"
        destination = MagicMock(id=102)
        destination.db.zone_id = "test_zone"
        FlightRegistry.register_point("origin", origin, name="Origin")
        FlightRegistry.register_point("destination", destination, name="Destination")
        FlightRegistry.register_route(
            "origin",
            "destination",
            base_fare=100,
            leg_duration=30,
        )
        self.assertEqual(
            fare_for_route(self.char1, [("origin", "destination")]),
            90,
        )

        vendor = MagicMock()
        vendor.db.vendor_faction = "consortium"
        self.assertEqual(
            get_vendor_price(vendor, {"value": 100}, self.char1),
            95,
        )


if __name__ == "__main__":
    unittest.main()
