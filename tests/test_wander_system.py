"""
Tests for the wandering mob system.

Uses unittest.TestCase + MagicMock — pure-logic module with no Evennia DB needed.
"""

import unittest
from unittest.mock import MagicMock, patch


class TestWanderMob(unittest.TestCase):
    """Tests for wander_mob() — single mob movement logic."""

    def _make_mob(self, wander=True, in_combat=False, has_patrol=False, is_dead=False):
        """Create a mock mob with configurable state."""
        mob = MagicMock()
        mob.db.wander = wander
        mob.db.is_dead = is_dead
        if in_combat:
            mob.ndb.combat_handler = MagicMock()

        # Patrol script check
        if has_patrol:
            mob.scripts.get.return_value = [MagicMock()]
        else:
            mob.scripts.get.return_value = []

        # Default location with exits
        mob.location = self._make_room("zone_a")
        mob.key = "wolf"

        return mob

    def _make_room(self, zone_id, room_id="room_1", no_mobs=False):
        """Create a mock room."""
        room = MagicMock()
        room.db.zone_id = zone_id
        room.tags.get.return_value = True if no_mobs else None
        # Override tags.get to respond correctly to specific queries
        def tags_get(key=None, category=None):
            if key == "no_mobs" and category == "room_flag":
                return True if no_mobs else None
            return None
        room.tags.get = tags_get
        return room

    def _make_exit(self, destination):
        """Create a mock exit."""
        exit_obj = MagicMock()
        exit_obj.destination = destination
        return exit_obj

    def test_mob_moves_to_random_connected_room(self):
        """wander_mob moves mob to a random connected exit destination."""
        from world.wander_system import wander_mob

        mob = self._make_mob(wander=True)
        dest_room = self._make_room("zone_a")
        exit_obj = self._make_exit(dest_room)
        mob.location.exits = [exit_obj]
        mob.location.db.zone_id = "zone_a"

        with patch("world.wander_system.random") as mock_random:
            mock_random.choice.return_value = exit_obj
            result = wander_mob(mob)

        self.assertTrue(result)
        self.assertEqual(mob.location, dest_room)
        mob.move_to.assert_not_called()

    def test_skips_mob_if_wander_false(self):
        """wander_mob skips mob if mob.db.wander is False."""
        from world.wander_system import wander_mob

        mob = self._make_mob(wander=False)
        result = wander_mob(mob)

        self.assertFalse(result)
        mob.move_to.assert_not_called()

    def test_skips_mob_if_wander_missing(self):
        """wander_mob skips mob if mob.db.wander is None/missing."""
        from world.wander_system import wander_mob

        mob = self._make_mob(wander=None)
        result = wander_mob(mob)

        self.assertFalse(result)
        mob.move_to.assert_not_called()

    def test_skips_mob_in_combat(self):
        """wander_mob skips mob if mob is in combat."""
        from world.wander_system import wander_mob

        mob = self._make_mob(wander=True, in_combat=True)
        dest_room = self._make_room("zone_a")
        exit_obj = self._make_exit(dest_room)
        mob.location.exits = [exit_obj]
        mob.location.db.zone_id = "zone_a"

        result = wander_mob(mob)

        self.assertFalse(result)
        self.assertNotEqual(mob.location, dest_room)
        mob.move_to.assert_not_called()

    def test_combat_handler_guard_handles_none_internal_dict(self):
        """Evennia ndb handlers can expose a non-dict vars() result."""
        from world.wander_system import _get_combat_handler

        class NdbWithNoneDict:
            @property
            def __dict__(self):
                return None

        mob = MagicMock()
        mob.ndb = NdbWithNoneDict()

        self.assertIsNone(_get_combat_handler(mob))

    def test_combat_handler_guard_reads_dynamic_ndb_attribute(self):
        """Evennia ndb holders can resolve combat_handler outside __dict__."""
        from world.wander_system import _get_combat_handler

        handler = object()

        class DynamicNdb:
            def __getattr__(self, name):
                if name == "combat_handler":
                    return handler
                raise AttributeError(name)

        mob = MagicMock()
        mob.ndb = DynamicNdb()

        self.assertIs(_get_combat_handler(mob), handler)

    def test_skips_mob_with_active_patrol(self):
        """wander_mob skips mob if mob has active PatrolScript."""
        from world.wander_system import wander_mob

        mob = self._make_mob(wander=True, has_patrol=True)
        result = wander_mob(mob)

        self.assertFalse(result)
        mob.move_to.assert_not_called()

    def test_skips_dead_mob(self):
        """wander_mob skips mob if mob is dead."""
        from world.wander_system import wander_mob

        mob = self._make_mob(wander=True, is_dead=True)
        result = wander_mob(mob)

        self.assertFalse(result)
        mob.move_to.assert_not_called()

    def test_does_not_move_to_no_mobs_room(self):
        """wander_mob does not move to rooms with no_mobs tag."""
        from world.wander_system import wander_mob

        mob = self._make_mob(wander=True)
        no_mobs_room = self._make_room("zone_a", no_mobs=True)
        exit_obj = self._make_exit(no_mobs_room)
        mob.location.exits = [exit_obj]
        mob.location.db.zone_id = "zone_a"

        result = wander_mob(mob)

        self.assertFalse(result)
        mob.move_to.assert_not_called()

    def test_does_not_cross_zone_boundary(self):
        """wander_mob does not move to rooms in a different zone."""
        from world.wander_system import wander_mob

        mob = self._make_mob(wander=True)
        other_zone_room = self._make_room("zone_b")
        exit_obj = self._make_exit(other_zone_room)
        mob.location.exits = [exit_obj]
        mob.location.db.zone_id = "zone_a"

        result = wander_mob(mob)

        self.assertFalse(result)
        mob.move_to.assert_not_called()

    def test_returns_true_if_moved(self):
        """wander_mob returns True when mob successfully moves."""
        from world.wander_system import wander_mob

        mob = self._make_mob(wander=True)
        dest_room = self._make_room("zone_a")
        exit_obj = self._make_exit(dest_room)
        mob.location.exits = [exit_obj]
        mob.location.db.zone_id = "zone_a"

        with patch("world.wander_system.random") as mock_random:
            mock_random.choice.return_value = exit_obj
            result = wander_mob(mob)

        self.assertTrue(result)

    def test_returns_false_if_no_valid_exits(self):
        """wander_mob returns False when no valid exits exist."""
        from world.wander_system import wander_mob

        mob = self._make_mob(wander=True)
        mob.location.exits = []
        mob.location.db.zone_id = "zone_a"

        result = wander_mob(mob)

        self.assertFalse(result)

    def test_uses_random_choice(self):
        """wander_mob uses random.choice among valid exits."""
        from world.wander_system import wander_mob

        mob = self._make_mob(wander=True)
        dest1 = self._make_room("zone_a")
        dest2 = self._make_room("zone_a")
        exit1 = self._make_exit(dest1)
        exit2 = self._make_exit(dest2)
        mob.location.exits = [exit1, exit2]
        mob.location.db.zone_id = "zone_a"

        with patch("world.wander_system.random") as mock_random:
            mock_random.choice.return_value = exit2
            result = wander_mob(mob)

        mock_random.choice.assert_called_once()
        # Verify the valid exits list was passed to choice
        valid_exits = mock_random.choice.call_args[0][0]
        self.assertEqual(len(valid_exits), 2)
        self.assertTrue(result)
        self.assertEqual(mob.location, dest2)
        mob.move_to.assert_not_called()

    def test_echoes_arrival_message(self):
        """wander_mob echoes an arrival message to the destination room."""
        from world.wander_system import wander_mob

        mob = self._make_mob(wander=True)
        dest_room = self._make_room("zone_a")
        exit_obj = self._make_exit(dest_room)
        mob.location.exits = [exit_obj]
        mob.location.db.zone_id = "zone_a"

        with patch("world.wander_system.random") as mock_random:
            mock_random.choice.return_value = exit_obj
            wander_mob(mob)

        dest_room.msg_contents.assert_called()


class TestWanderTick(unittest.TestCase):
    """Tests for wander_tick() — batch tick function."""

    @patch("world.wander_system.wander_mob")
    @patch("world.wander_system.search_objects_by_exact_tag")
    def test_finds_all_wandering_mobs(self, mock_search, mock_wander_mob):
        """wander_tick finds all wandering mobs via tag search and calls wander_mob."""
        from world.wander_system import wander_tick

        mob1 = MagicMock()
        mob2 = MagicMock()
        mock_search.return_value = [mob1, mob2]

        with patch("world.wander_system.random") as mock_random:
            # Both mobs pass the 40% chance roll
            mock_random.random.side_effect = [0.1, 0.2]
            wander_tick()

        mock_search.assert_called_once_with("wanderer", "mob_behavior")
        self.assertEqual(mock_wander_mob.call_count, 2)

    @patch("world.wander_system.wander_mob")
    @patch("world.wander_system.search_objects_by_exact_tag")
    def test_stochastic_movement_chance(self, mock_search, mock_wander_mob):
        """wander_tick applies stochastic chance — some mobs may not move."""
        from world.wander_system import wander_tick

        mob1 = MagicMock()
        mob2 = MagicMock()
        mock_search.return_value = [mob1, mob2]

        with patch("world.wander_system.random") as mock_random:
            # mob1 passes (0.1 < 0.4), mob2 fails (0.8 >= 0.4)
            mock_random.random.side_effect = [0.1, 0.8]
            wander_tick()

        self.assertEqual(mock_wander_mob.call_count, 1)
        mock_wander_mob.assert_called_once_with(mob1)

    @patch("world.wander_system.wander_mob")
    @patch("world.wander_system.search_objects_by_exact_tag")
    def test_handles_empty_mob_list(self, mock_search, mock_wander_mob):
        """wander_tick handles no wandering mobs gracefully."""
        from world.wander_system import wander_tick

        mock_search.return_value = []
        wander_tick()

        mock_wander_mob.assert_not_called()


if __name__ == "__main__":
    unittest.main()
