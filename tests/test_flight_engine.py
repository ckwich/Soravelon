"""
Tests for flight engine (fare_for_route, book_flight) and FlightScript.

Uses EvenniaTest base class to ensure proper Django/Evennia setup.
Flight engine functions use lazy imports, so we patch at call site.
"""

from unittest.mock import MagicMock, patch
from evennia.utils.test_resources import EvenniaTest


class TestFareForRoute(EvenniaTest):
    """fare_for_route applies Consortium Standing discount tiers correctly."""

    def setUp(self):
        super().setUp()
        from world.flight_registry import FlightRegistry
        FlightRegistry.clear()

    def tearDown(self):
        from world.flight_registry import FlightRegistry
        FlightRegistry.clear()
        super().tearDown()

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
        FlightRegistry.register_route(
            "point_a", "point_b", base_fare=base_fare, leg_duration=30
        )

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
            FlightRegistry.register_point(
                f"stop_{i+1}", room_next, name=f"Stop {i+1}"
            )
            FlightRegistry.register_route(
                f"stop_{i}", f"stop_{i+1}", base_fare=fare, leg_duration=30
            )

    @patch("world.world_state.get_standing")
    def _call_fare(self, standing, base_fare, mock_standing):
        from world.flight_engine import fare_for_route
        self._register_single_route(base_fare)
        legs = [("point_a", "point_b")]
        char = MagicMock()
        mock_standing.return_value = standing
        return fare_for_route(char, legs)

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

    @patch("world.world_state.get_standing")
    def test_multi_leg_sums_before_discount(self, mock_standing):
        """3 legs at 100 each = 300 base. Standing 50 -> 20% off -> 240."""
        from world.flight_engine import fare_for_route
        self._register_multi_routes([100, 100, 100])
        legs = [("stop_0", "stop_1"), ("stop_1", "stop_2"), ("stop_2", "stop_3")]
        char = MagicMock()
        mock_standing.return_value = 50
        result = fare_for_route(char, legs)
        self.assertEqual(result, 240)

    def test_fare_never_negative(self):
        self.assertEqual(self._call_fare(100, 0), 0)

    def test_rounds_down(self):
        """Standing 25 = 10% off. Base 101 -> 101 * 0.9 = 90.9 -> int = 90."""
        self.assertEqual(self._call_fare(25, 101), 90)


class TestBookFlight(EvenniaTest):
    """book_flight validates discovery, balance, deducts via banking.deduct_from_bank()."""

    def setUp(self):
        super().setUp()
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
        FlightRegistry.register_route(
            "point_a", "point_b", base_fare=50, leg_duration=30
        )

    def tearDown(self):
        from world.flight_registry import FlightRegistry
        FlightRegistry.clear()
        super().tearDown()

    def _make_char(self, discovered=None):
        char = MagicMock()
        char.db.discovered_flight_points = set(discovered) if discovered else set()
        char.scripts.add.return_value = MagicMock()
        return char

    @patch("world.banking.deduct_from_bank")
    @patch("world.banking.get_balance")
    @patch("world.world_state.get_standing")
    def test_unknown_origin_returns_false(self, mock_standing, mock_bal, mock_wd):
        from world.flight_engine import book_flight
        mock_standing.return_value = 0
        char = self._make_char(discovered={"point_b"})
        ok, msg = book_flight(char, "unknown_point", "point_b")
        self.assertFalse(ok)
        self.assertIn("Unknown flight point", msg)

    @patch("world.banking.deduct_from_bank")
    @patch("world.banking.get_balance")
    @patch("world.world_state.get_standing")
    def test_unknown_destination_returns_false(self, mock_standing, mock_bal, mock_wd):
        from world.flight_engine import book_flight
        mock_standing.return_value = 0
        char = self._make_char(discovered={"point_a"})
        ok, msg = book_flight(char, "point_a", "unknown_point")
        self.assertFalse(ok)
        self.assertIn("Unknown flight point", msg)

    @patch("world.banking.deduct_from_bank")
    @patch("world.banking.get_balance")
    @patch("world.world_state.get_standing")
    def test_undiscovered_destination_returns_false(self, mock_standing, mock_bal, mock_wd):
        from world.flight_engine import book_flight
        mock_standing.return_value = 0
        char = self._make_char(discovered=set())
        ok, msg = book_flight(char, "point_a", "point_b")
        self.assertFalse(ok)
        self.assertIn("not discovered", msg)

    @patch("world.banking.deduct_from_bank")
    @patch("world.banking.get_balance")
    @patch("world.world_state.get_standing")
    def test_insufficient_funds_returns_false(self, mock_standing, mock_bal, mock_wd):
        from world.flight_engine import book_flight
        mock_standing.return_value = 0
        mock_bal.return_value = 10
        char = self._make_char(discovered={"point_b"})
        ok, msg = book_flight(char, "point_a", "point_b")
        self.assertFalse(ok)
        self.assertIn("Insufficient funds", msg)

    @patch("world.banking.deduct_from_bank")
    @patch("world.banking.get_balance")
    @patch("world.world_state.get_standing")
    def test_successful_booking_returns_true(self, mock_standing, mock_bal, mock_wd):
        from world.flight_engine import book_flight
        mock_standing.return_value = 0
        mock_bal.return_value = 100
        mock_wd.return_value = (True, "ok")
        char = self._make_char(discovered={"point_b"})
        ok, msg = book_flight(char, "point_a", "point_b")
        self.assertTrue(ok)

    @patch("world.banking.deduct_from_bank")
    @patch("world.banking.get_balance")
    @patch("world.world_state.get_standing")
    def test_successful_booking_calls_deduct(self, mock_standing, mock_bal, mock_wd):
        from world.flight_engine import book_flight
        mock_standing.return_value = 0
        mock_bal.return_value = 100
        mock_wd.return_value = (True, "ok")
        char = self._make_char(discovered={"point_b"})
        book_flight(char, "point_a", "point_b")
        mock_wd.assert_called_once()

    @patch("world.banking.deduct_from_bank")
    @patch("world.banking.get_balance")
    @patch("world.world_state.get_standing")
    def test_deduct_failure_returns_false(self, mock_standing, mock_bal, mock_wd):
        from world.flight_engine import book_flight
        mock_standing.return_value = 0
        mock_bal.return_value = 100
        mock_wd.return_value = (False, "Insufficient funds.")
        char = self._make_char(discovered={"point_b"})
        ok, msg = book_flight(char, "point_a", "point_b")
        self.assertFalse(ok)
        self.assertIn("Payment failed", msg)

    @patch("world.banking.deduct_from_bank")
    @patch("world.banking.get_balance")
    @patch("world.world_state.get_standing")
    def test_same_origin_destination_no_route(self, mock_standing, mock_bal, mock_wd):
        """origin == destination -> find_route_legs returns [] -> No route."""
        from world.flight_engine import book_flight
        mock_standing.return_value = 0
        char = self._make_char(discovered={"point_a"})
        ok, msg = book_flight(char, "point_a", "point_a")
        self.assertFalse(ok)
        self.assertIn("No route", msg)


class TestFlightScriptImportable(EvenniaTest):
    """FlightScript module is importable and has required attributes."""

    def test_flightscript_importable(self):
        from world.scripts.flight_script import FlightScript
        self.assertIsNotNone(FlightScript)

    def test_has_required_methods(self):
        from world.scripts.flight_script import FlightScript
        self.assertTrue(hasattr(FlightScript, "start_journey"))
        self.assertTrue(hasattr(FlightScript, "do_disembark"))
        self.assertTrue(hasattr(FlightScript, "_arrive_final"))
        self.assertTrue(hasattr(FlightScript, "_begin_leg"))
