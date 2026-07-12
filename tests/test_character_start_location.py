"""Tests for Soravelon's new-character start location handoff."""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


class TestCharacterStartLocation(unittest.TestCase):
    def test_get_start_location_finds_authored_arrival_room(self):
        from typeclasses.characters import Character

        wrong_zone = SimpleNamespace(db=SimpleNamespace(zone_id="other"))
        arrival = SimpleNamespace(db=SimpleNamespace(zone_id="vaels_crossing"))

        with patch(
            "typeclasses.characters.search_objects_by_exact_tag",
            return_value=[wrong_zone, arrival],
        ):
            self.assertIs(Character._get_start_location(object()), arrival)

    def test_place_at_start_location_sets_home_and_location(self):
        from typeclasses.characters import Character

        arrival = SimpleNamespace(db=SimpleNamespace(zone_id="vaels_crossing"))
        character = SimpleNamespace(
            db=SimpleNamespace(needs_start_location=True),
            home=None,
            location=None,
            _get_start_location=MagicMock(return_value=arrival),
        )

        placed = Character._place_at_start_location_if_available(character)

        self.assertTrue(placed)
        self.assertIs(character.home, arrival)
        self.assertIs(character.location, arrival)
        self.assertFalse(character.db.needs_start_location)

    def test_ensure_start_location_moves_limbo_character_after_areas_load(self):
        from typeclasses.characters import Character

        arrival = SimpleNamespace(db=SimpleNamespace(zone_id="vaels_crossing"))
        limbo = SimpleNamespace(db=SimpleNamespace(zone_id=None))
        character = SimpleNamespace(
            db=SimpleNamespace(needs_start_location=True),
            home=None,
            location=limbo,
            move_to=MagicMock(),
            _get_start_location=MagicMock(return_value=arrival),
        )

        moved = Character._ensure_start_location(character)

        self.assertTrue(moved)
        self.assertIs(character.home, arrival)
        character.move_to.assert_called_once_with(arrival, quiet=True)
        self.assertFalse(character.db.needs_start_location)

    def test_ensure_start_location_repairs_unflagged_new_limbo_character(self):
        from typeclasses.characters import Character

        arrival = SimpleNamespace(db=SimpleNamespace(zone_id="vaels_crossing"))
        limbo = SimpleNamespace(key="Limbo", db=SimpleNamespace(zone_id=None))
        character = SimpleNamespace(
            db=SimpleNamespace(needs_start_location=False, ancestry=None),
            home=limbo,
            location=None,
            move_to=MagicMock(),
            _get_start_location=MagicMock(return_value=arrival),
        )

        moved = Character._ensure_start_location(character)

        self.assertTrue(moved)
        self.assertIs(character.home, arrival)
        character.move_to.assert_called_once_with(arrival, quiet=True)
        self.assertFalse(character.db.needs_start_location)

    def test_ensure_start_location_repairs_limbo_home_without_moving_valid_location(self):
        from typeclasses.characters import Character

        arrival = SimpleNamespace(db=SimpleNamespace(zone_id="vaels_crossing"))
        valid_room = SimpleNamespace(key="Market Square", db=SimpleNamespace(zone_id="vaels_crossing"))
        limbo = SimpleNamespace(key="Limbo", db=SimpleNamespace(zone_id=None))
        character = SimpleNamespace(
            db=SimpleNamespace(needs_start_location=False, ancestry=None),
            home=limbo,
            location=valid_room,
            move_to=MagicMock(),
            _get_start_location=MagicMock(return_value=arrival),
        )

        repaired = Character._ensure_start_location(character)

        self.assertTrue(repaired)
        self.assertIs(character.home, arrival)
        self.assertIs(character.location, valid_room)
        character.move_to.assert_not_called()
        self.assertFalse(character.db.needs_start_location)
