"""
Tests for world/room_state.py.

Covers room flag CRUD, lazy decay mechanics, dominant flag priority,
and unknown flag safety. Uses unittest.TestCase + MagicMock -- pure ndb
operations with mocked time.time().
"""
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from world.room_state import (
    ROUND_DURATION_SECONDS,
    FLAG_VOCABULARY,
    SENSE_PRIORITY,
    get_room_flags,
    add_room_flag,
    remove_room_flag,
    get_dominant_flag,
)


# ---------------------------------------------------------------------------
# Helper: mock room with ndb namespace
# ---------------------------------------------------------------------------

def _mock_room(room_state=None, last_activity=None):
    """Create a MagicMock room with ndb attributes for room state tests."""
    room = MagicMock()
    room.ndb = SimpleNamespace(
        room_state=room_state,
        last_activity=last_activity,
    )
    room.key = "Test Room"
    room.id = 1
    return room


# ===========================================================================
# get_room_flags
# ===========================================================================


class TestGetRoomFlags(unittest.TestCase):
    """get_room_flags returns active flags with lazy decay."""

    def test_empty_when_no_state(self):
        """Room with no ndb.room_state returns empty dict."""
        room = _mock_room(room_state=None)
        self.assertEqual(get_room_flags(room), {})

    @patch("world.room_state.time")
    def test_returns_flags_when_current(self, mock_time):
        """Flags returned as-is when no rounds have passed."""
        now = 1000.0
        mock_time.time.return_value = now

        room = _mock_room(room_state={
            "flags": {"charged": 5, "burning": 3},
            "last_updated": now,
        })

        result = get_room_flags(room)
        self.assertEqual(result, {"charged": 5, "burning": 3})

    @patch("world.room_state.time")
    def test_lazy_decay(self, mock_time):
        """Flags decay by elapsed rounds (9 seconds = 3 rounds)."""
        start = 1000.0
        mock_time.time.return_value = start + 9.0  # 9 seconds / 3 = 3 rounds

        room = _mock_room(room_state={
            "flags": {"charged": 5},
            "last_updated": start,
        })

        result = get_room_flags(room)
        self.assertEqual(result["charged"], 2)  # 5 - 3 = 2

    @patch("world.room_state.time")
    def test_expired_flags_removed(self, mock_time):
        """Flags that decay to 0 or below are removed."""
        start = 1000.0
        mock_time.time.return_value = start + 9.0  # 3 rounds

        room = _mock_room(room_state={
            "flags": {"charged": 2},
            "last_updated": start,
        })

        result = get_room_flags(room)
        self.assertNotIn("charged", result)

    @patch("world.room_state.time")
    def test_persistent_flag_no_decay(self, mock_time):
        """Flags with duration -1 never decay."""
        start = 1000.0
        mock_time.time.return_value = start + 300.0  # 100 rounds

        room = _mock_room(room_state={
            "flags": {"node_critical": -1},
            "last_updated": start,
        })

        result = get_room_flags(room)
        self.assertEqual(result["node_critical"], -1)


# ===========================================================================
# add_room_flag
# ===========================================================================


class TestAddRoomFlag(unittest.TestCase):
    """add_room_flag adds or refreshes flags on a room."""

    @patch("world.room_state.time")
    def test_add_new_flag(self, mock_time):
        """Adding a new flag stores it in ndb.room_state."""
        mock_time.time.return_value = 1000.0

        room = _mock_room(room_state=None)
        add_room_flag(room, "charged")

        state = room.ndb.room_state
        self.assertIn("charged", state["flags"])
        self.assertEqual(
            state["flags"]["charged"],
            FLAG_VOCABULARY["charged"]["typical_duration"],
        )

    @patch("world.room_state.time")
    def test_refresh_takes_max(self, mock_time):
        """Refreshing a flag takes the longer duration."""
        mock_time.time.return_value = 1000.0

        room = _mock_room(room_state={
            "flags": {"charged": 3},
            "last_updated": 1000.0,
        })
        add_room_flag(room, "charged", duration=5)

        self.assertEqual(room.ndb.room_state["flags"]["charged"], 5)

    @patch("world.room_state.time")
    def test_refresh_keeps_existing_if_longer(self, mock_time):
        """Refreshing with shorter duration keeps the existing longer value."""
        mock_time.time.return_value = 1000.0

        room = _mock_room(room_state={
            "flags": {"charged": 8},
            "last_updated": 1000.0,
        })
        add_room_flag(room, "charged", duration=3)

        self.assertEqual(room.ndb.room_state["flags"]["charged"], 8)

    @patch("world.room_state.time")
    def test_unknown_flag_logs_warning(self, mock_time):
        """Unknown flag name logs warning, does not crash."""
        mock_time.time.return_value = 1000.0

        room = _mock_room(room_state=None)

        with patch("evennia.logger.log_warn") as mock_warn:
            add_room_flag(room, "fake_flag")
            mock_warn.assert_called_once()
            self.assertIn("fake_flag", mock_warn.call_args[0][0])


# ===========================================================================
# remove_room_flag
# ===========================================================================


class TestRemoveRoomFlag(unittest.TestCase):
    """remove_room_flag removes flags from room state."""

    @patch("world.room_state.time")
    def test_remove_existing(self, mock_time):
        """Removing an existing flag removes it from ndb."""
        mock_time.time.return_value = 1000.0

        room = _mock_room(room_state={
            "flags": {"charged": 5, "burning": 3},
            "last_updated": 1000.0,
        })
        remove_room_flag(room, "charged")

        self.assertNotIn("charged", room.ndb.room_state["flags"])
        self.assertIn("burning", room.ndb.room_state["flags"])


# ===========================================================================
# get_dominant_flag
# ===========================================================================


class TestGetDominantFlag(unittest.TestCase):
    """get_dominant_flag returns highest-priority active flag."""

    @patch("world.room_state.time")
    def test_priority_order(self, mock_time):
        """void_touched has higher priority than blood_soaked."""
        mock_time.time.return_value = 1000.0

        room = _mock_room(room_state={
            "flags": {"blood_soaked": 3, "void_touched": 5},
            "last_updated": 1000.0,
        })

        result = get_dominant_flag(room)
        self.assertEqual(result, "void_touched")

    @patch("world.room_state.time")
    def test_still_when_no_flags(self, mock_time):
        """No active flags and old last_activity returns 'still'."""
        mock_time.time.return_value = 1000.0

        room = _mock_room(
            room_state=None,
            last_activity=0,  # very old
        )

        result = get_dominant_flag(room)
        self.assertEqual(result, "still")

    @patch("world.room_state.time")
    def test_none_when_recent_activity(self, mock_time):
        """No active flags but recent activity returns None."""
        now = 1000.0
        mock_time.time.return_value = now

        room = _mock_room(
            room_state=None,
            last_activity=now - 1,  # 1 second ago -- very recent
        )

        result = get_dominant_flag(room)
        self.assertIsNone(result)


class TestFlagVocabularyCompleteness(unittest.TestCase):
    """FLAG_VOCABULARY has expected count and SENSE_PRIORITY covers all flags."""

    def test_vocabulary_has_21_flags(self):
        self.assertEqual(len(FLAG_VOCABULARY), 21)

    def test_sense_priority_covers_all_flags(self):
        """Every flag in vocabulary appears in SENSE_PRIORITY."""
        for flag in FLAG_VOCABULARY:
            self.assertIn(flag, SENSE_PRIORITY,
                          f"Flag '{flag}' not in SENSE_PRIORITY")
