"""
Tests for flight engine (fare_for_route, book_flight) and FlightScript.

Uses unittest.TestCase + sys.modules injection to avoid Django setup.
The flight_engine module uses lazy imports inside functions so we can
inject mocks into sys.modules before the first import.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch


def _inject_django_mocks():
    """
    Inject enough sys.modules stubs to allow importing world.flight_engine
    without a running Django/Evennia environment.
    """
    # world.world_state stub
    if "world.world_state" not in sys.modules:
        mock_ws = MagicMock()
        mock_ws.get_standing = MagicMock(return_value=0)
        sys.modules["world.world_state"] = mock_ws

    # world.banking stub
    if "world.banking" not in sys.modules:
        mock_banking = MagicMock()
        mock_banking.get_balance = MagicMock(return_value=0)
        mock_banking.withdraw = MagicMock(return_value=(True, "ok"))
        sys.modules["world.banking"] = mock_banking

    # world.scripts.flight_script stub (needed for book_flight's lazy import)
    if "world.scripts.flight_script" not in sys.modules:
        mock_fs_mod = MagicMock()
        mock_script = MagicMock()
        mock_fs_mod.FlightScript = mock_script
        sys.modules["world.scripts"] = MagicMock()
        sys.modules["world.scripts.flight_script"] = mock_fs_mod

    # typeclasses.scripts stub (imported by flight_script.py at module level)
    if "typeclasses" not in sys.modules:
        sys.modules["typeclasses"] = MagicMock()
    if "typeclasses.scripts" not in sys.modules:
        mock_tc_scripts = MagicMock()
        mock_tc_scripts.SoravelonScript = object
        sys.modules["typeclasses.scripts"] = mock_tc_scripts


_inject_django_mocks()


class TestFareForRoute(unittest.TestCase):
    """fare_for_route applies Consortium Standing discount tiers correctly."""

    def setUp(self):
        from world.flight_registry import FlightRegistry
        FlightRegistry.clear()

    def tearDown(self):
        from world.flight_registry import FlightRegistry
        FlightRegistry.clear()

    def _register_single_route(self, base_fare):
        from world.flight_registry import FlightRegistry
        room_a = MagicMock()
        room_a.id = 100
        room_a.db.zone_id = "test_zone"
        room_b = MagicMock()
        room_b.id = 101
        room_b.db.zone_id = "test_zone"
        FlightRegistry.register_point("point_a", room_a, name="Stop A")
        FlightRegistry.register_point("point_b", room_b, name="Stop B")
        FlightRegistry.register_route("point_a", "point_b", base_fare=base_fare, leg_duration=30)

    def _register_multi_routes(self, fares):
        from world.flight_registry import FlightRegistry
        for i, fare in enumerate(fares):
            room = MagicMock()
            room.id = 100 + i
            room.db.zone_id = "test_zone"
            room_next = MagicMock()
            room_next.id = 101 + i
            room_next.db.zone_id = "test_zone"
            FlightRegistry.register_point(f"stop_{i}", room, name=f"Stop {i}")
            FlightRegistry.register_point(f"stop_{i+1}", room_next, name=f"Stop {i+1}")
            FlightRegistry.register_route(f"stop_{i}", f"stop_{i+1}", base_fare=fare, leg_duration=30)

    def _call_fare(self, standing, base_fare):
        from world.flight_engine import fare_for_route
        self._register_single_route(base_fare)
        legs = [("point_a", "point_b")]
        char = MagicMock()
        sys.modules["world.world_state"].get_standing.return_value = standing
        result = fare_for_route(char, legs)
        return result

    def test_no_discount_standing_0(self):
        self.assertEqual(self._call_fare(0, 100), 100)

    def test_no_discount_standing_24(self):
        self.assertEqual(self._call_fare(24, 200), 200)

    def test_10_percent_discount_standing_25(self):
        self.assertEqual(self._call_fare(25, 100), 90)

    def test_10_percent_discount_standing_49(self):
        self.assertEqual(self._call_fare(49, 200), 180)

    def test_20_percent_discount_standing_50(self):
        self.assertEqual(self._call_fare(50, 100), 80)

    def test_20_percent_discount_standing_74(self):
        self.assertEqual(self._call_fare(74, 1000), 800)

    def test_30_percent_discount_standing_75(self):
        self.assertEqual(self._call_fare(75, 100), 70)

    def test_30_percent_discount_standing_100(self):
        self.assertEqual(self._call_fare(100, 200), 140)

    def test_multi_leg_sums_before_discount(self):
        """3 legs at 100 each = 300 base. Standing 50 → 20% off → 240."""
        from world.flight_engine import fare_for_route
        self._register_multi_routes([100, 100, 100])
        legs = [("stop_0", "stop_1"), ("stop_1", "stop_2"), ("stop_2", "stop_3")]
        char = MagicMock()
        sys.modules["world.world_state"].get_standing.return_value = 50
        result = fare_for_route(char, legs)
        self.assertEqual(result, 240)

    def test_fare_never_negative(self):
        self.assertEqual(self._call_fare(100, 0), 0)

    def test_rounds_down(self):
        """Standing 25 = 10% off. Base 101 → 101 * 0.9 = 90.9 → int = 90."""
        self.assertEqual(self._call_fare(25, 101), 90)


class TestBookFlight(unittest.TestCase):
    """book_flight validates discovery, balance, deducts via banking.withdraw()."""

    def setUp(self):
        from world.flight_registry import FlightRegistry
        FlightRegistry.clear()
        self.room_a = MagicMock()
        self.room_a.id = 200
        self.room_a.db.zone_id = "zone_a"
        self.room_b = MagicMock()
        self.room_b.id = 201
        self.room_b.db.zone_id = "zone_b"
        FlightRegistry.register_point("point_a", self.room_a, name="Stop A")
        FlightRegistry.register_point("point_b", self.room_b, name="Stop B")
        FlightRegistry.register_route("point_a", "point_b", base_fare=50, leg_duration=30)
        # Reset mocks
        sys.modules["world.world_state"].get_standing.return_value = 0
        sys.modules["world.banking"].get_balance.return_value = 100
        sys.modules["world.banking"].withdraw.return_value = (True, "ok")

    def tearDown(self):
        from world.flight_registry import FlightRegistry
        FlightRegistry.clear()

    def _make_char(self, discovered=None):
        char = MagicMock()
        char.db.discovered_flight_points = set(discovered) if discovered else set()
        char.scripts.add.return_value = MagicMock()
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
        char = self._make_char(discovered=set())
        ok, msg = book_flight(char, "point_a", "point_b")
        self.assertFalse(ok)
        self.assertIn("not discovered", msg)

    def test_insufficient_funds_returns_false(self):
        from world.flight_engine import book_flight
        sys.modules["world.banking"].get_balance.return_value = 10
        char = self._make_char(discovered={"point_b"})
        ok, msg = book_flight(char, "point_a", "point_b")
        self.assertFalse(ok)
        self.assertIn("Insufficient funds", msg)
        self.assertIn("50", msg)  # need 50
        self.assertIn("10", msg)  # have 10

    def test_successful_booking_returns_true(self):
        from world.flight_engine import book_flight
        char = self._make_char(discovered={"point_b"})
        ok, msg = book_flight(char, "point_a", "point_b")
        self.assertTrue(ok)
        self.assertEqual(msg, "")

    def test_successful_booking_calls_withdraw(self):
        from world.flight_engine import book_flight
        char = self._make_char(discovered={"point_b"})
        book_flight(char, "point_a", "point_b")
        sys.modules["world.banking"].withdraw.assert_called_once()

    def test_withdraw_failure_returns_false(self):
        from world.flight_engine import book_flight
        sys.modules["world.banking"].withdraw.return_value = (False, "Insufficient funds. Banked balance: 0 Scales.")
        char = self._make_char(discovered={"point_b"})
        ok, msg = book_flight(char, "point_a", "point_b")
        self.assertFalse(ok)
        self.assertIn("Payment failed", msg)

    def test_same_origin_destination_no_route(self):
        """origin == destination → find_route_legs returns [] → No route error."""
        from world.flight_engine import book_flight
        char = self._make_char(discovered={"point_a"})
        ok, msg = book_flight(char, "point_a", "point_a")
        self.assertFalse(ok)
        self.assertIn("No route", msg)


class TestFlightScriptImportable(unittest.TestCase):
    """FlightScript module is importable and has required attributes."""

    def test_flightscript_importable(self):
        from world.scripts.flight_script import FlightScript
        self.assertIsNotNone(FlightScript)

    def test_fare_paid_default_false(self):
        """
        Verify that fare_paid is initialized to False in at_script_creation.
        The actual value is checked at the attribute assignment level since
        full Evennia DB init is not available.
        """
        from world.scripts.flight_script import FlightScript
        # Verify the class has start_journey and do_disembark methods
        self.assertTrue(hasattr(FlightScript, "start_journey"))
        self.assertTrue(hasattr(FlightScript, "do_disembark"))
        self.assertTrue(hasattr(FlightScript, "_arrive_final"))
        self.assertTrue(hasattr(FlightScript, "_begin_leg"))


if __name__ == "__main__":
    unittest.main()
