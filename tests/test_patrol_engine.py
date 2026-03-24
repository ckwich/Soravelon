"""
Tests for world/patrol_engine.py.

Covers:
- find_path() BFS with zone boundary enforcement
- next_patrol_step() with wrapping behavior
- check_patrol_encounter() with combat_enabled and disposition checks
"""

from unittest.mock import MagicMock, patch
from evennia.utils.test_resources import EvenniaTestCase


def _make_room(zone_id="zone_test", dbref_id=1):
    """Create a mock room with zone_id and exits."""
    room = MagicMock()
    room.db.zone_id = zone_id
    room.id = dbref_id
    room.exits = []
    return room


def _connect_rooms(room_a, room_b, bidirectional=True):
    """Add exit objects connecting room_a → room_b."""
    exit_ab = MagicMock()
    exit_ab.destination = room_b
    room_a.exits.append(exit_ab)
    if bidirectional:
        exit_ba = MagicMock()
        exit_ba.destination = room_a
        room_b.exits.append(exit_ba)


class TestFindPathSameRoom(EvenniaTestCase):
    """find_path(room_A, room_A) → [room_A]."""

    def test_same_room_returns_single_element_path(self):
        from world.patrol_engine import find_path

        room = _make_room()
        result = find_path(room, room)
        self.assertEqual(result, [room])


class TestFindPathTwoExitsAway(EvenniaTestCase):
    """find_path(A, C) where C is 2 exits away via B → [A, B, C]."""

    def test_two_hops_returns_correct_path(self):
        from world.patrol_engine import find_path

        room_a = _make_room(dbref_id=1)
        room_b = _make_room(dbref_id=2)
        room_c = _make_room(dbref_id=3)

        _connect_rooms(room_a, room_b, bidirectional=False)
        _connect_rooms(room_b, room_c, bidirectional=False)

        result = find_path(room_a, room_c)
        self.assertEqual(result, [room_a, room_b, room_c])


class TestFindPathZoneBoundary(EvenniaTestCase):
    """find_path(A, C) where C is in a different zone → []."""

    def test_zone_boundary_blocks_path(self):
        from world.patrol_engine import find_path

        room_a = _make_room(zone_id="zone_a", dbref_id=1)
        room_b = _make_room(zone_id="zone_b", dbref_id=2)  # different zone
        room_c = _make_room(zone_id="zone_b", dbref_id=3)

        _connect_rooms(room_a, room_b, bidirectional=False)
        _connect_rooms(room_b, room_c, bidirectional=False)

        result = find_path(room_a, room_c)
        self.assertEqual(result, [])


class TestFindPathUnreachable(EvenniaTestCase):
    """find_path(A, B) with no path within max_depth → []."""

    def test_unreachable_returns_empty(self):
        from world.patrol_engine import find_path

        room_a = _make_room(dbref_id=1)
        room_b = _make_room(dbref_id=2)
        # No exits connecting them

        result = find_path(room_a, room_b, max_depth=20)
        self.assertEqual(result, [])


class TestFindPathMaxDepthExceeded(EvenniaTestCase):
    """find_path returns [] when path exceeds max_depth."""

    def test_path_exceeds_max_depth(self):
        from world.patrol_engine import find_path

        # Chain of 5 rooms: A → B → C → D → E
        rooms = [_make_room(dbref_id=i) for i in range(5)]
        for i in range(4):
            _connect_rooms(rooms[i], rooms[i + 1], bidirectional=False)

        # Max depth = 2 should not reach room[4] (5 hops away)
        result = find_path(rooms[0], rooms[4], max_depth=2)
        self.assertEqual(result, [])


class TestNextPatrolStepWraps(EvenniaTestCase):
    """next_patrol_step wraps around at end of route."""

    def test_wraps_from_last_to_first(self):
        from world.patrol_engine import next_patrol_step

        room0 = _make_room(dbref_id=10)

        mob = MagicMock()
        route_ids = [10, 11, 12]

        with patch("evennia.search_object") as mock_search:
            mock_search.return_value = [room0]
            result_room, result_index = next_patrol_step(mob, route_ids, 2)  # at last index

        self.assertEqual(result_room, room0)
        self.assertEqual(result_index, 0)  # wraps to 0

    def test_advances_to_next_index(self):
        from world.patrol_engine import next_patrol_step

        room1 = _make_room(dbref_id=11)

        mob = MagicMock()
        route_ids = [10, 11, 12]

        with patch("evennia.search_object") as mock_search:
            mock_search.return_value = [room1]
            result_room, result_index = next_patrol_step(mob, route_ids, 0)

        self.assertEqual(result_room, room1)
        self.assertEqual(result_index, 1)


class TestNextPatrolStepEmptyRoute(EvenniaTestCase):
    """next_patrol_step returns (None, current_index) when route is empty."""

    def test_empty_route_returns_none(self):
        from world.patrol_engine import next_patrol_step

        mob = MagicMock()
        result_room, result_index = next_patrol_step(mob, [], 0)

        self.assertIsNone(result_room)
        self.assertEqual(result_index, 0)


class TestNextPatrolStepRoomNotFound(EvenniaTestCase):
    """next_patrol_step returns (None, current_index) when room not found."""

    def test_room_not_found_returns_none(self):
        from world.patrol_engine import next_patrol_step

        mob = MagicMock()
        route_ids = [99]

        with patch("evennia.search_object") as mock_search:
            mock_search.return_value = []  # room not found
            result_room, result_index = next_patrol_step(mob, route_ids, 0)

        self.assertIsNone(result_room)
        self.assertEqual(result_index, 0)


class TestCheckPatrolEncounterCombatDisabled(EvenniaTestCase):
    """check_patrol_encounter returns False when combat_enabled=False."""

    def test_combat_disabled_returns_false(self):
        from world.patrol_engine import check_patrol_encounter

        mob = MagicMock()
        mob.db.combat_enabled = False

        room = _make_room()
        result = check_patrol_encounter(mob, room)
        self.assertFalse(result)


class TestCheckPatrolEncounterAggressive(EvenniaTestCase):
    """check_patrol_encounter returns True when behavior is 'aggressive'."""

    def test_aggressive_behavior_returns_true(self):
        from world.patrol_engine import check_patrol_encounter

        mob = MagicMock()
        mob.db.combat_enabled = True

        # A player character in the room
        player = MagicMock()
        player.account = MagicMock()

        room = MagicMock()
        room.contents = [player]

        with patch("world.mob_disposition.get_mob_behavior", return_value="aggressive"):
            result = check_patrol_encounter(mob, room)

        self.assertTrue(result)


class TestCheckPatrolEncounterTerritorial(EvenniaTestCase):
    """check_patrol_encounter returns True when behavior is 'territorial'."""

    def test_territorial_behavior_returns_true(self):
        from world.patrol_engine import check_patrol_encounter

        mob = MagicMock()
        mob.db.combat_enabled = True

        player = MagicMock()
        player.account = MagicMock()

        room = MagicMock()
        room.contents = [player]

        with patch("world.mob_disposition.get_mob_behavior", return_value="territorial"):
            result = check_patrol_encounter(mob, room)

        self.assertTrue(result)


class TestCheckPatrolEncounterPassive(EvenniaTestCase):
    """check_patrol_encounter returns False when behavior is 'passive'."""

    def test_passive_behavior_returns_false(self):
        from world.patrol_engine import check_patrol_encounter

        mob = MagicMock()
        mob.db.combat_enabled = True

        player = MagicMock()
        player.account = MagicMock()

        room = MagicMock()
        room.contents = [player]

        with patch("world.mob_disposition.get_mob_behavior", return_value="passive"):
            result = check_patrol_encounter(mob, room)

        self.assertFalse(result)


class TestCheckPatrolEncounterFriendly(EvenniaTestCase):
    """check_patrol_encounter returns False when behavior is 'friendly'."""

    def test_friendly_behavior_returns_false(self):
        from world.patrol_engine import check_patrol_encounter

        mob = MagicMock()
        mob.db.combat_enabled = True

        player = MagicMock()
        player.account = MagicMock()

        room = MagicMock()
        room.contents = [player]

        with patch("world.mob_disposition.get_mob_behavior", return_value="friendly"):
            result = check_patrol_encounter(mob, room)

        self.assertFalse(result)


class TestCheckPatrolEncounterNoPlayers(EvenniaTestCase):
    """check_patrol_encounter returns False when no player characters in room."""

    def test_no_players_returns_false(self):
        from world.patrol_engine import check_patrol_encounter

        mob = MagicMock()
        mob.db.combat_enabled = True

        # Non-player object (no .account)
        npc = MagicMock()
        npc.account = None

        room = MagicMock()
        room.contents = [npc]

        result = check_patrol_encounter(mob, room)
        self.assertFalse(result)
