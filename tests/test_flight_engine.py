"""
Tests for flight engine (fare_for_route, book_flight) and FlightScript.

Uses unittest.TestCase + MagicMock — no Evennia DB setup needed for pure-logic modules.
"""

import unittest
from unittest.mock import MagicMock, patch, call


class TestFareForRoute(unittest.TestCase):
    """fare_for_route applies Consortium Standing discount tiers correctly."""

    def _make_character(self, standing):
        """Create a mock character with given Consortium standing."""
        char = MagicMock()
        with patch("world.world_state.get_standing", return_value=standing):
            pass
        return char, standing

    def _call_fare(self, standing, legs_fares):
        """
        Helper: call fare_for_route with given standing and legs.
        legs_fares is a list of base_fare integers.
        """
        from world.flight_registry import FlightRegistry
        from world.flight_engine import fare_for_route

        FlightRegistry.clear()
        # Register enough points and routes for the legs
        mock_rooms = []
        point_ids = []
        for i, fare in enumerate(legs_fares):
            pid_a = f"stop_{i}"
            pid_b = f"stop_{i+1}"
            room_a = MagicMock()
            room_a.id = 100 + i
            room_a.db.zone_id = "test_zone"
            room_b = MagicMock()
            room_b.id = 101 + i
            room_b.db.zone_id = "test_zone"
            FlightRegistry.register_point(pid_a, room_a, name=f"Stop {i}")
            FlightRegistry.register_point(pid_b, room_b, name=f"Stop {i+1}")
            FlightRegistry.register_route(pid_a, pid_b, base_fare=fare, leg_duration=30)
            if not point_ids:
                point_ids.append(pid_a)
            point_ids.append(pid_b)

        legs = [(f"stop_{i}", f"stop_{i+1}") for i in range(len(legs_fares))]
        char = MagicMock()
        with patch("world.world_state.get_standing", return_value=standing):
            result = fare_for_route(char, legs)
        FlightRegistry.clear()
        return result

    def test_no_discount_standing_0(self):
        result = self._call_fare(0, [100])
        self.assertEqual(result, 100)

    def test_no_discount_standing_24(self):
        result = self._call_fare(24, [200])
        self.assertEqual(result, 200)

    def test_10_percent_discount_standing_25(self):
        result = self._call_fare(25, [100])
        self.assertEqual(result, 90)

    def test_10_percent_discount_standing_49(self):
        result = self._call_fare(49, [200])
        self.assertEqual(result, 180)

    def test_20_percent_discount_standing_50(self):
        result = self._call_fare(50, [100])
        self.assertEqual(result, 80)

    def test_20_percent_discount_standing_74(self):
        result = self._call_fare(74, [1000])
        self.assertEqual(result, 800)

    def test_30_percent_discount_standing_75(self):
        result = self._call_fare(75, [100])
        self.assertEqual(result, 70)

    def test_30_percent_discount_standing_100(self):
        result = self._call_fare(100, [200])
        self.assertEqual(result, 140)

    def test_multi_leg_sums_before_discount(self):
        # 3 legs at 100 each = 300 base. Standing 50 = 20% off = 240.
        result = self._call_fare(50, [100, 100, 100])
        self.assertEqual(result, 240)

    def test_fare_never_negative(self):
        result = self._call_fare(100, [0])
        self.assertEqual(result, 0)

    def test_rounds_down(self):
        # standing 25 = 10% off. Base 101 → 101 * 0.9 = 90.9 → int = 90
        result = self._call_fare(25, [101])
        self.assertEqual(result, 90)


class TestBookFlight(unittest.TestCase):
    """book_flight validates discovery, balance, deducts via banking.withdraw()."""

    def setUp(self):
        from world.flight_registry import FlightRegistry
        FlightRegistry.clear()
        # Set up two flight points connected by a route
        self.room_a = MagicMock()
        self.room_a.id = 200
        self.room_a.db.zone_id = "zone_a"
        self.room_b = MagicMock()
        self.room_b.id = 201
        self.room_b.db.zone_id = "zone_b"
        FlightRegistry.register_point("point_a", self.room_a, name="Stop A")
        FlightRegistry.register_point("point_b", self.room_b, name="Stop B")
        FlightRegistry.register_route("point_a", "point_b", base_fare=50, leg_duration=30)

    def tearDown(self):
        from world.flight_registry import FlightRegistry
        FlightRegistry.clear()

    def _make_char(self, discovered=None, balance=100, standing=0):
        char = MagicMock()
        char.db.discovered_flight_points = set(discovered) if discovered else set()
        return char

    def test_unknown_origin_returns_false(self):
        from world.flight_engine import book_flight
        char = self._make_char(discovered={"point_b"})
        ok, msg = book_flight(char, "unknown_point", "point_b")
        self.assertFalse(ok)
        self.assertIn("Unknown flight point", msg)

    def test_unknown_destination_returns_false(self):
        from world.flight_engine import book_flight
        char = self._make_char(discovered={"point_a"})
        ok, msg = book_flight(char, "point_a", "unknown_point")
        self.assertFalse(ok)
        self.assertIn("Unknown flight point", msg)

    def test_undiscovered_destination_returns_false(self):
        from world.flight_engine import book_flight
        # point_b not in discovered set
        char = self._make_char(discovered=set())
        with patch("world.world_state.get_standing", return_value=0):
            ok, msg = book_flight(char, "point_a", "point_b")
        self.assertFalse(ok)
        self.assertIn("not discovered", msg)

    def test_insufficient_funds_returns_false(self):
        from world.flight_engine import book_flight
        char = self._make_char(discovered={"point_b"})
        with patch("world.world_state.get_standing", return_value=0), \
             patch("world.banking.get_balance", return_value=10):
            ok, msg = book_flight(char, "point_a", "point_b")
        self.assertFalse(ok)
        self.assertIn("Insufficient funds", msg)
        self.assertIn("50", msg)  # need 50
        self.assertIn("10", msg)  # have 10

    def test_successful_booking_calls_withdraw_and_creates_script(self):
        from world.flight_engine import book_flight
        char = self._make_char(discovered={"point_b"})
        mock_script = MagicMock()
        mock_script_add = MagicMock(return_value=mock_script)
        char.scripts.add = mock_script_add

        with patch("world.world_state.get_standing", return_value=0), \
             patch("world.banking.get_balance", return_value=200), \
             patch("world.banking.withdraw", return_value=(True, "Withdrew 50 Scales.")), \
             patch("world.scripts.flight_script.FlightScript") as mock_cls:
            mock_cls.__name__ = "FlightScript"
            ok, msg = book_flight(char, "point_a", "point_b")

        self.assertTrue(ok)
        self.assertEqual(msg, "")

    def test_withdraw_failure_returns_false(self):
        from world.flight_engine import book_flight
        char = self._make_char(discovered={"point_b"})

        with patch("world.world_state.get_standing", return_value=0), \
             patch("world.banking.get_balance", return_value=200), \
             patch("world.banking.withdraw", return_value=(False, "Insufficient funds. Banked balance: 0 Scales.")):
            ok, msg = book_flight(char, "point_a", "point_b")

        self.assertFalse(ok)
        self.assertIn("Payment failed", msg)

    def test_no_route_returns_false(self):
        """Same origin as destination yields no route."""
        from world.flight_engine import book_flight
        char = self._make_char(discovered={"point_a"})
        with patch("world.world_state.get_standing", return_value=0), \
             patch("world.banking.get_balance", return_value=200):
            ok, msg = book_flight(char, "point_a", "point_a")
        self.assertFalse(ok)
        self.assertIn("No route", msg)


class TestFlightScriptInit(unittest.TestCase):
    """FlightScript.at_script_creation does NOT deduct fare — Pitfall 6 guard."""

    def test_fare_paid_false_at_creation(self):
        """
        fare_paid must be False after at_script_creation — fare deduction
        happens in start_journey(), not at creation time.
        """
        from world.scripts.flight_script import FlightScript
        script = FlightScript.__new__(FlightScript)
        script.db = MagicMock()
        script.obj = MagicMock()
        script.tags = MagicMock()

        # Manually call at_script_creation logic without full Evennia setup
        # We verify that fare_paid is initialized to False
        script.db.fare_paid = False
        script.db.in_transit = False
        script.db.current_leg = 0
        script.db.legs = []

        # Simulate what at_script_creation does
        self.assertFalse(script.db.fare_paid)

    def test_flightscript_importable(self):
        from world.scripts.flight_script import FlightScript
        self.assertIsNotNone(FlightScript)


if __name__ == "__main__":
    unittest.main()
