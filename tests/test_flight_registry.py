"""Direct contract coverage for the flight registry graph."""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from world.flight_registry import FlightRegistry


def _make_room(room_id, zone_id="zone", key="Room"):
    room = MagicMock()
    room.id = room_id
    room.key = key
    room.db = SimpleNamespace(zone_id=zone_id)
    return room


class TestFlightRegistry(unittest.TestCase):
    """Flight registry behavior should remain small, explicit, and reliable."""

    def setUp(self):
        FlightRegistry.clear()

    def tearDown(self):
        FlightRegistry.clear()

    def test_register_route_is_bidirectional(self):
        point_a = _make_room(101, zone_id="vaels_crossing", key="Harbor Tower")
        point_b = _make_room(202, zone_id="varath_prime", key="Sky Quay")

        FlightRegistry.register_point("vael_harbor", point_a)
        FlightRegistry.register_point("varath_quay", point_b)
        FlightRegistry.register_route("vael_harbor", "varath_quay", 18, 45)

        self.assertEqual(
            FlightRegistry.get_route("vael_harbor", "varath_quay"),
            FlightRegistry.get_route("varath_quay", "vael_harbor"),
        )
        self.assertEqual(
            FlightRegistry.connected_points("vael_harbor"),
            ["varath_quay"],
        )

    def test_find_route_legs_returns_shortest_multileg_path(self):
        FlightRegistry.register_route("a", "b", 10, 30)
        FlightRegistry.register_route("b", "c", 10, 30)
        FlightRegistry.register_route("c", "d", 10, 30)
        FlightRegistry.register_route("a", "detour", 10, 30)
        FlightRegistry.register_route("detour", "dead_end", 10, 30)

        self.assertEqual(
            FlightRegistry.find_route_legs("a", "d"),
            [("a", "b"), ("b", "c"), ("c", "d")],
        )

    def test_clear_resets_points_and_routes(self):
        FlightRegistry.register_point("a", _make_room(1))
        FlightRegistry.register_point("b", _make_room(2))
        FlightRegistry.register_route("a", "b", 10, 30)

        FlightRegistry.clear()

        self.assertEqual(FlightRegistry.flight_points, {})
        self.assertEqual(FlightRegistry.flight_routes, {})
