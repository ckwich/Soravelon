"""
Tests for world/oob_publisher.py — CLI-06 coverage.

Uses unittest.TestCase with @patch decorators to mock lazy-imported dependencies.
Django is configured at module level (no EvenniaTest DB setup needed since all
characters are MagicMock — no real Evennia DB objects touched).

MagicMock character simulates a connected player with all expected db/ndb attrs.
"""

import os
import time
import unittest
from unittest.mock import MagicMock, patch

# Configure Django settings before any world.* imports.
# We need Django configured so that world modules can be imported, but we
# do NOT need the full Evennia DB (all characters are MagicMock).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django
django.setup()


# Stub context packet returned by get_character_context_packet
CONTEXT_PACKET = {
    "reputation": 42.0,
    "network": 10.0,
    "bond": 5.0,
    "legacy": 0.0,
    "attunement": 20.0,
    "ancestry": None,
    "primary_domain": None,
    "secondary_domain": None,
    "guild": None,
    "subclass": None,
    "backend_level": None,
    "standing": None,
    "trust": None,
    "betrayal_flag": None,
    "zone_attunement": None,
    "companion_present": False,
    "companion_type": None,
    "companion_tier": None,
    "world_event_summary": None,
}


def _make_char(connected=True):
    """Build a MagicMock character with all db/ndb attrs needed by push_* functions."""
    char = MagicMock()
    char.ndb.oob_debounce = None  # start as None — Pitfall 1
    if connected:
        char.sessions.all.return_value = [MagicMock()]
    else:
        char.sessions.all.return_value = []

    # Dimension scores (read by push_status_update)
    char.db.reputation_score = 42.0
    char.db.network_score = 10.0
    char.db.bond_score = 5.0
    char.db.legacy_score = 0.0
    char.db.attunement_score = 20.0

    # Domain scores + currency
    char.db.domain_scores = {"combat": 35}
    char.db.carried_scales = 100

    # Companion fields
    char.db.companion_id = None
    char.db.companion_type = None
    char.db.companion_tier = None

    # Location (needed by push_map_update)
    char.location = MagicMock()
    char.location.db.zone_id = "test_zone"
    char.location.db.fog_of_war = False
    char.location.tags.get.return_value = "test_room_001"

    # Visited room IDs (fog-of-war)
    char.db.visited_room_ids = set()

    return char


# ---------------------------------------------------------------------------
# push_status_update
# ---------------------------------------------------------------------------

class TestPushStatusUpdate(unittest.TestCase):

    def setUp(self):
        self.char = _make_char()

    @patch("world.world_state.get_character_context_packet", return_value=CONTEXT_PACKET)
    def test_sends_status_update_kwarg(self, mock_ctx):
        from world.oob_publisher import push_status_update
        push_status_update(self.char)
        self.char.msg.assert_called_once()
        kwargs = self.char.msg.call_args.kwargs
        self.assertIn("status_update", kwargs)

    @patch("world.world_state.get_character_context_packet", return_value=CONTEXT_PACKET)
    def test_dimensions_included(self, mock_ctx):
        from world.oob_publisher import push_status_update
        push_status_update(self.char)
        data = self.char.msg.call_args.kwargs["status_update"]
        self.assertEqual(data["dimensions"]["reputation"], 42.0)
        self.assertEqual(data["dimensions"]["network"], 10.0)
        self.assertEqual(data["dimensions"]["bond"], 5.0)
        self.assertEqual(data["dimensions"]["legacy"], 0.0)
        self.assertEqual(data["dimensions"]["attunement"], 20.0)

    @patch("world.world_state.get_character_context_packet", return_value=CONTEXT_PACKET)
    def test_domains_included(self, mock_ctx):
        from world.oob_publisher import push_status_update
        push_status_update(self.char)
        data = self.char.msg.call_args.kwargs["status_update"]
        self.assertEqual(data["domains"], {"combat": 35})

    @patch("world.world_state.get_character_context_packet", return_value=CONTEXT_PACKET)
    def test_no_send_when_no_session(self, mock_ctx):
        from world.oob_publisher import push_status_update
        char = _make_char(connected=False)
        push_status_update(char)
        char.msg.assert_not_called()

    @patch("world.world_state.get_character_context_packet", return_value=CONTEXT_PACKET)
    def test_carried_scales_included(self, mock_ctx):
        from world.oob_publisher import push_status_update
        push_status_update(self.char)
        data = self.char.msg.call_args.kwargs["status_update"]
        self.assertEqual(data["carried_scales"], 100)


# ---------------------------------------------------------------------------
# push_stat_update
# ---------------------------------------------------------------------------

class TestPushStatUpdate(unittest.TestCase):

    def setUp(self):
        self.char = _make_char()

    def test_sends_stat_update(self):
        from world.oob_publisher import push_stat_update
        push_stat_update(self.char)
        self.char.msg.assert_called_once()
        kwargs = self.char.msg.call_args.kwargs
        self.assertIn("stat_update", kwargs)

    def test_stat_fields_present(self):
        from world.oob_publisher import push_stat_update
        push_stat_update(self.char)
        data = self.char.msg.call_args.kwargs["stat_update"]
        self.assertIn("hp", data)
        self.assertIn("hp_max", data)
        self.assertIn("conditions", data)

    def test_no_send_disconnected(self):
        from world.oob_publisher import push_stat_update
        char = _make_char(connected=False)
        push_stat_update(char)
        char.msg.assert_not_called()


# ---------------------------------------------------------------------------
# push_node_event
# ---------------------------------------------------------------------------

class TestPushNodeEvent(unittest.TestCase):

    def setUp(self):
        self.char = _make_char()

    def test_sends_node_event(self):
        from world.oob_publisher import push_node_event
        push_node_event(self.char, "z1", "dormant", "awakening")
        self.char.msg.assert_called_once()
        data = self.char.msg.call_args.kwargs["node_event"]
        self.assertEqual(data["zone_id"], "z1")
        self.assertEqual(data["old_state"], "dormant")
        self.assertEqual(data["new_state"], "awakening")

    def test_no_debounce_two_calls_both_send(self):
        """node_event has interval=0.0 — two rapid calls both send."""
        from world.oob_publisher import push_node_event
        push_node_event(self.char, "z1", "dormant", "awakening")
        push_node_event(self.char, "z1", "awakening", "active")
        self.assertEqual(self.char.msg.call_count, 2)


# ---------------------------------------------------------------------------
# push_flight_progress
# ---------------------------------------------------------------------------

class TestPushFlightProgress(unittest.TestCase):

    def setUp(self):
        self.char = _make_char()

    def test_sends_flight_progress(self):
        from world.oob_publisher import push_flight_progress
        push_flight_progress(self.char, 0, 3, "Varath Landing", False)
        self.char.msg.assert_called_once()
        data = self.char.msg.call_args.kwargs["flight_progress"]
        self.assertEqual(data["leg_index"], 0)
        self.assertEqual(data["total_legs"], 3)
        self.assertEqual(data["destination_name"], "Varath Landing")
        self.assertFalse(data["disembark_available"])

    def test_disembark_available_true(self):
        from world.oob_publisher import push_flight_progress
        push_flight_progress(self.char, 1, 3, "Midstop", True)
        data = self.char.msg.call_args.kwargs["flight_progress"]
        self.assertTrue(data["disembark_available"])


# ---------------------------------------------------------------------------
# push_combat_update
# ---------------------------------------------------------------------------

class TestPushCombatUpdate(unittest.TestCase):

    def setUp(self):
        self.char = _make_char()

    def test_sends_combat_update(self):
        from world.oob_publisher import push_combat_update
        payload = {"phase": "active", "targets": []}
        push_combat_update(self.char, payload)
        self.char.msg.assert_called_once()
        data = self.char.msg.call_args.kwargs["combat_update"]
        self.assertEqual(data["phase"], "active")

    def test_no_send_disconnected(self):
        from world.oob_publisher import push_combat_update
        char = _make_char(connected=False)
        push_combat_update(char, {})
        char.msg.assert_not_called()


# ---------------------------------------------------------------------------
# push_quest_update
# ---------------------------------------------------------------------------

class TestPushQuestUpdate(unittest.TestCase):

    def setUp(self):
        self.char = _make_char()

    @patch("world.quest_engine.get_active_quests", return_value=[])
    def test_sends_quest_update(self, mock_quests):
        from world.oob_publisher import push_quest_update
        payload = {"quest_id": "wolves_hunt", "event": "accepted"}
        push_quest_update(self.char, payload)
        self.char.msg.assert_called_once()
        data = self.char.msg.call_args.kwargs["quest_update"]
        self.assertEqual(data["event_quest_id"], "wolves_hunt")

    @patch("world.quest_engine.get_active_quests", return_value=[])
    def test_quest_update_payload_shape(self, mock_quests):
        """quest_update payload has active_quests list, event, and event_quest_id fields."""
        from world.oob_publisher import push_quest_update
        push_quest_update(self.char, {"event": "progress", "quest_id": "q1"})
        data = self.char.msg.call_args.kwargs["quest_update"]
        self.assertIn("active_quests", data)
        self.assertIsInstance(data["active_quests"], list)
        self.assertIn("event", data)
        self.assertIn("event_quest_id", data)


# ---------------------------------------------------------------------------
# push_inventory_update
# ---------------------------------------------------------------------------

class TestPushInventoryUpdate(unittest.TestCase):

    def setUp(self):
        self.char = _make_char()

    @patch("world.inventory_helpers.get_carry_state", return_value="light")
    def test_sends_inventory_update(self, mock_carry):
        from world.oob_publisher import push_inventory_update
        push_inventory_update(self.char)
        self.char.msg.assert_called_once()
        data = self.char.msg.call_args.kwargs["inventory_update"]
        self.assertIn("items", data)
        self.assertIn("encumbrance", data)

    @patch("world.inventory_helpers.get_carry_state", return_value="encumbered")
    def test_encumbrance_value_passed(self, mock_carry):
        from world.oob_publisher import push_inventory_update
        push_inventory_update(self.char)
        data = self.char.msg.call_args.kwargs["inventory_update"]
        self.assertEqual(data["encumbrance"], "encumbered")

    @patch("world.inventory_helpers.get_carry_state", return_value="light")
    def test_items_stub_is_empty_list(self, mock_carry):
        from world.oob_publisher import push_inventory_update
        push_inventory_update(self.char)
        data = self.char.msg.call_args.kwargs["inventory_update"]
        self.assertEqual(data["items"], [])


# ---------------------------------------------------------------------------
# Debounce gate
# ---------------------------------------------------------------------------

class TestDebounceGate(unittest.TestCase):
    """Tests that debounce prevents duplicate sends within the configured window."""

    def setUp(self):
        self.char = _make_char()

    @patch("world.world_state.get_character_context_packet", return_value=CONTEXT_PACKET)
    def test_first_call_sends(self, mock_ctx):
        from world.oob_publisher import push_status_update
        push_status_update(self.char)
        self.char.msg.assert_called_once()

    @patch("world.world_state.get_character_context_packet", return_value=CONTEXT_PACKET)
    def test_second_call_within_window_blocked(self, mock_ctx):
        """Two immediate push_status_update calls — second blocked by 2.0s window."""
        from world.oob_publisher import push_status_update
        push_status_update(self.char)
        push_status_update(self.char)
        self.assertEqual(self.char.msg.call_count, 1)

    @patch("world.world_state.get_character_context_packet", return_value=CONTEXT_PACKET)
    def test_call_after_window_allowed(self, mock_ctx):
        """Setting debounce timestamp to 3s ago allows the next send (past 2.0s)."""
        from world.oob_publisher import push_status_update
        self.char.ndb.oob_debounce = {"status_update": time.monotonic() - 3.0}
        push_status_update(self.char)
        self.char.msg.assert_called_once()

    def test_node_event_never_debounced(self):
        """node_event has interval=0.0 — two rapid calls both go through."""
        from world.oob_publisher import push_node_event
        push_node_event(self.char, "z1", "dormant", "awakening")
        push_node_event(self.char, "z1", "awakening", "active")
        self.assertEqual(self.char.msg.call_count, 2)


# ---------------------------------------------------------------------------
# Session guard
# ---------------------------------------------------------------------------

class TestSessionGuard(unittest.TestCase):
    """OOB messages must not be sent to disconnected characters."""

    def test_no_send_disconnected(self):
        from world.oob_publisher import push_stat_update
        char = _make_char(connected=False)
        push_stat_update(char)
        char.msg.assert_not_called()

    def test_sends_when_connected(self):
        from world.oob_publisher import push_stat_update
        char = _make_char(connected=True)
        push_stat_update(char)
        char.msg.assert_called_once()


# ---------------------------------------------------------------------------
# _should_send helper
# ---------------------------------------------------------------------------

class TestShouldSendHelper(unittest.TestCase):
    """Unit tests for the internal _should_send helper function."""

    def setUp(self):
        self.char = _make_char()

    def test_returns_true_when_debounce_none(self):
        """First call with ndb.oob_debounce=None — should return True."""
        from world.oob_publisher import _should_send
        self.char.ndb.oob_debounce = None
        result = _should_send(self.char, "status_update")
        self.assertTrue(result)

    def test_returns_false_within_window(self):
        """Recent timestamp within 2.0s window — should return False."""
        from world.oob_publisher import _should_send
        self.char.ndb.oob_debounce = {"status_update": time.monotonic()}
        result = _should_send(self.char, "status_update")
        self.assertFalse(result)

    def test_returns_true_for_zero_interval(self):
        """node_event has interval=0.0 — _should_send always returns True."""
        from world.oob_publisher import _should_send
        self.char.ndb.oob_debounce = {"node_event": time.monotonic()}
        result = _should_send(self.char, "node_event")
        self.assertTrue(result)

    def test_returns_true_after_window_expires(self):
        """Timestamp older than interval — should return True."""
        from world.oob_publisher import _should_send
        self.char.ndb.oob_debounce = {"status_update": time.monotonic() - 5.0}
        result = _should_send(self.char, "status_update")
        self.assertTrue(result)
