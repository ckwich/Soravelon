"""Behavior tests for authored Dragon Courier destination knowledge."""

from evennia.utils.test_resources import EvenniaTest
from unittest.mock import Mock


class TestDiscoverFlightPointAction(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.flight_registry import FlightRegistry

        FlightRegistry.clear()
        FlightRegistry.register_point(
            "varath_prime_courier",
            self.room1,
            name="Varath Prime Courier Platform",
        )
        self.char1.db.discovered_flight_points = set()

    def tearDown(self):
        from world.flight_registry import FlightRegistry

        FlightRegistry.clear()
        super().tearDown()

    def test_grants_destination_knowledge_without_moving_character(self):
        from world.action_vocabulary import execute_action

        original_location = self.char1.location
        self.char1.msg = Mock()
        success, message = execute_action(
            {
                "action_type": "discover_flight_point",
                "point_id": "varath_prime_courier",
                "message": "The courier clerk marks Varath Prime on your route slate.",
            },
            {"character": self.char1},
        )

        self.assertTrue(success, message)
        self.assertEqual(
            self.char1.db.discovered_flight_points,
            {"varath_prime_courier"},
        )
        self.assertEqual(self.char1.location, original_location)
        self.assertIn("route slate", self.char1.msg.call_args.args[0])

    def test_repeat_is_idempotent(self):
        from world.action_vocabulary import execute_action

        action = {
            "action_type": "discover_flight_point",
            "point_id": "varath_prime_courier",
        }
        first = execute_action(action, {"character": self.char1})
        second = execute_action(action, {"character": self.char1})

        self.assertTrue(first[0])
        self.assertTrue(second[0])
        self.assertEqual(
            self.char1.db.discovered_flight_points,
            {"varath_prime_courier"},
        )

    def test_unknown_point_fails_without_mutation(self):
        from world.action_vocabulary import execute_action

        success, message = execute_action(
            {
                "action_type": "discover_flight_point",
                "point_id": "missing_stop",
            },
            {"character": self.char1},
        )

        self.assertFalse(success)
        self.assertIn("unknown point_id", message)
        self.assertEqual(self.char1.db.discovered_flight_points, set())

    def test_atomic_batch_rollback_restores_prior_knowledge(self):
        from world.action_vocabulary import execute_action

        callbacks = []
        success, message = execute_action(
            {
                "action_type": "discover_flight_point",
                "point_id": "varath_prime_courier",
            },
            {"character": self.char1, "_rollback_callbacks": callbacks},
        )
        self.assertTrue(success, message)

        callbacks[0]()

        self.assertEqual(self.char1.db.discovered_flight_points, set())
