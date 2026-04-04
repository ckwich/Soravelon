"""
Tests for world/area_validator.py — pure-Python zone validation module.

Uses unittest.TestCase (not EvenniaTest) because area_validator.py has
zero Django/Evennia imports at module level.
"""

import unittest

from world.area_validator import (
    validate_zone,
    ValidationError,
    VALID_ZONE_TYPES,
    VALID_CONTINENTS,
    VALID_NODE_TYPES,
    VALID_DIRECTIONS,
    VALID_FACTION_TERRITORIES,
    VALID_ROOM_TYPES,
)


class TestValidationErrorDataclass(unittest.TestCase):
    """ValidationError is a dataclass with severity, field_path, message."""

    def test_fields_exist(self):
        """ValidationError has severity, field_path, message fields."""
        err = ValidationError(severity="error", field_path="zone.name", message="name is required")
        self.assertEqual(err.severity, "error")
        self.assertEqual(err.field_path, "zone.name")
        self.assertEqual(err.message, "name is required")

    def test_warning_severity(self):
        """ValidationError accepts 'warning' severity."""
        err = ValidationError(severity="warning", field_path="zone.name", message="name low")
        self.assertEqual(err.severity, "warning")


class TestConstantsDefined(unittest.TestCase):
    """All six constant sets are defined and non-empty."""

    def test_valid_zone_types_non_empty(self):
        self.assertIsInstance(VALID_ZONE_TYPES, (set, frozenset))
        self.assertIn("ancient_forest", VALID_ZONE_TYPES)
        self.assertIn("plains", VALID_ZONE_TYPES)

    def test_valid_continents_non_empty(self):
        self.assertIsInstance(VALID_CONTINENTS, (set, frozenset))
        self.assertIn("varath", VALID_CONTINENTS)

    def test_valid_node_types_non_empty(self):
        self.assertIsInstance(VALID_NODE_TYPES, (set, frozenset))
        self.assertIn("resonance", VALID_NODE_TYPES)

    def test_valid_faction_territories_non_empty(self):
        self.assertIsInstance(VALID_FACTION_TERRITORIES, (set, frozenset))
        self.assertIn("neutral", VALID_FACTION_TERRITORIES)

    def test_valid_directions_non_empty(self):
        self.assertIsInstance(VALID_DIRECTIONS, (set, frozenset))
        self.assertIn("north", VALID_DIRECTIONS)
        self.assertIn("up", VALID_DIRECTIONS)

    def test_valid_room_types_non_empty(self):
        self.assertIsInstance(VALID_ROOM_TYPES, (set, frozenset))
        self.assertIn("path", VALID_ROOM_TYPES)


class TestValidateZoneMissingName(unittest.TestCase):
    """zone.name missing or empty returns error."""

    def test_missing_name_field_returns_error(self):
        """zone dict without 'name' key returns error with field_path 'zone.name'."""
        errors = validate_zone({"zone": {}, "rooms": [], "exits": []})
        field_paths = [e.field_path for e in errors]
        self.assertIn("zone.name", field_paths)
        name_errors = [e for e in errors if e.field_path == "zone.name"]
        self.assertEqual(name_errors[0].severity, "error")

    def test_empty_name_returns_error(self):
        """zone.name == '' returns error with field_path 'zone.name'."""
        errors = validate_zone({"zone": {"name": ""}, "rooms": [], "exits": []})
        field_paths = [e.field_path for e in errors]
        self.assertIn("zone.name", field_paths)

    def test_none_name_returns_error(self):
        """zone.name == None returns error."""
        errors = validate_zone({"zone": {"name": None}, "rooms": [], "exits": []})
        field_paths = [e.field_path for e in errors]
        self.assertIn("zone.name", field_paths)


class TestValidateZoneType(unittest.TestCase):
    """zone.zone_type validation."""

    def test_invalid_zone_type_returns_error(self):
        """Unknown zone_type returns error with field_path 'zone.zone_type'."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "bog"},
            "rooms": [], "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertIn("zone.zone_type", field_paths)

    def test_invalid_zone_type_message_contains_value(self):
        """Error message contains the invalid zone_type value."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "bog"},
            "rooms": [], "exits": [],
        })
        zone_type_errors = [e for e in errors if e.field_path == "zone.zone_type"]
        self.assertTrue(any("bog" in e.message for e in zone_type_errors))

    def test_valid_zone_type_no_error(self):
        """Valid zone_type produces no zone.zone_type error."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "plains",
                     "continent": "varath", "faction_territory": "neutral"},
            "rooms": [], "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertNotIn("zone.zone_type", field_paths)

    def test_missing_zone_type_no_error(self):
        """Missing zone_type (not present in dict) produces no error."""
        errors = validate_zone({
            "zone": {"name": "Test", "continent": "varath",
                     "faction_territory": "neutral"},
            "rooms": [], "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertNotIn("zone.zone_type", field_paths)


class TestValidateContinent(unittest.TestCase):
    """zone.continent validation."""

    def test_invalid_continent_returns_error(self):
        """Unknown continent returns error with field_path 'zone.continent'."""
        errors = validate_zone({
            "zone": {"name": "Test", "continent": "atlantis"},
            "rooms": [], "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertIn("zone.continent", field_paths)

    def test_valid_continent_no_error(self):
        """Valid continent produces no zone.continent error."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "plains",
                     "continent": "varath", "faction_territory": "neutral"},
            "rooms": [], "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertNotIn("zone.continent", field_paths)

    def test_missing_continent_no_error(self):
        """Missing continent (not present) produces no error."""
        errors = validate_zone({
            "zone": {"name": "Test", "faction_territory": "neutral"},
            "rooms": [], "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertNotIn("zone.continent", field_paths)


class TestValidateNodeType(unittest.TestCase):
    """zone.node_type validation."""

    def test_invalid_node_type_returns_error(self):
        """Unknown node_type returns error."""
        errors = validate_zone({
            "zone": {"name": "Test", "node_type": "unknown_node"},
            "rooms": [], "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertIn("zone.node_type", field_paths)

    def test_valid_node_type_no_error(self):
        """Valid node_type produces no zone.node_type error."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "plains", "continent": "varath",
                     "faction_territory": "neutral", "node_type": "resonance"},
            "rooms": [], "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertNotIn("zone.node_type", field_paths)

    def test_missing_node_type_no_error(self):
        """Missing node_type produces no error."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "plains", "continent": "varath",
                     "faction_territory": "neutral"},
            "rooms": [], "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertNotIn("zone.node_type", field_paths)


class TestValidateFactionTerritory(unittest.TestCase):
    """zone.faction_territory validation."""

    def test_invalid_faction_territory_returns_error(self):
        """Unknown faction_territory returns error."""
        errors = validate_zone({
            "zone": {"name": "Test", "faction_territory": "pirate"},
            "rooms": [], "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertIn("zone.faction_territory", field_paths)

    def test_valid_faction_territory_no_error(self):
        """Valid faction_territory produces no error."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "plains", "continent": "varath",
                     "faction_territory": "imperial"},
            "rooms": [], "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertNotIn("zone.faction_territory", field_paths)

    def test_missing_faction_territory_no_error(self):
        """Missing faction_territory (defaults to 'neutral') produces no error."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "plains", "continent": "varath"},
            "rooms": [], "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertNotIn("zone.faction_territory", field_paths)


class TestValidateRooms(unittest.TestCase):
    """rooms[N].room_type validation."""

    def test_invalid_room_type_returns_error(self):
        """Unknown room_type in rooms list returns error with indexed field_path."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "plains", "continent": "varath",
                     "faction_territory": "neutral"},
            "rooms": [{"room_type": "dungeon"}],
            "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertIn("rooms[0].room_type", field_paths)

    def test_second_room_invalid_type_correct_index(self):
        """Invalid room_type at index 1 uses field_path 'rooms[1].room_type'."""
        errors = validate_zone({
            "zone": {"name": "Test", "faction_territory": "neutral"},
            "rooms": [{"room_type": "path"}, {"room_type": "bog"}],
            "exits": [],
        })
        field_paths = [e.field_path for e in errors]
        self.assertIn("rooms[1].room_type", field_paths)
        self.assertNotIn("rooms[0].room_type", field_paths)

    def test_valid_room_type_no_error(self):
        """Valid room_type in rooms produces no rooms error."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "plains", "continent": "varath",
                     "faction_territory": "neutral"},
            "rooms": [{"room_type": "clearing"}],
            "exits": [],
        })
        room_errors = [e for e in errors if e.field_path.startswith("rooms[")]
        self.assertEqual(room_errors, [])

    def test_room_without_room_type_no_error(self):
        """Room missing room_type key produces no error (field not required)."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "plains", "continent": "varath",
                     "faction_territory": "neutral"},
            "rooms": [{"name": "A room"}],
            "exits": [],
        })
        room_errors = [e for e in errors if e.field_path.startswith("rooms[")]
        self.assertEqual(room_errors, [])


class TestValidateExits(unittest.TestCase):
    """exits[N].direction validation."""

    def test_invalid_direction_returns_error(self):
        """Unknown direction in exits list returns error with indexed field_path."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "plains", "continent": "varath",
                     "faction_territory": "neutral"},
            "rooms": [],
            "exits": [{"direction": "sideways"}],
        })
        field_paths = [e.field_path for e in errors]
        self.assertIn("exits[0].direction", field_paths)

    def test_second_exit_invalid_direction_correct_index(self):
        """Invalid direction at index 2 uses field_path 'exits[2].direction'."""
        errors = validate_zone({
            "zone": {"name": "Test", "faction_territory": "neutral"},
            "rooms": [],
            "exits": [
                {"direction": "north"},
                {"direction": "south"},
                {"direction": "diagonal"},
            ],
        })
        field_paths = [e.field_path for e in errors]
        self.assertIn("exits[2].direction", field_paths)
        self.assertNotIn("exits[0].direction", field_paths)
        self.assertNotIn("exits[1].direction", field_paths)

    def test_valid_direction_no_error(self):
        """Valid direction in exits produces no exits error."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "plains", "continent": "varath",
                     "faction_territory": "neutral"},
            "rooms": [],
            "exits": [{"direction": "north"}],
        })
        exit_errors = [e for e in errors if e.field_path.startswith("exits[")]
        self.assertEqual(exit_errors, [])

    def test_exit_without_direction_no_error(self):
        """Exit missing direction key produces no error."""
        errors = validate_zone({
            "zone": {"name": "Test", "zone_type": "plains", "continent": "varath",
                     "faction_territory": "neutral"},
            "rooms": [],
            "exits": [{"from": "room_001", "to": "room_002"}],
        })
        exit_errors = [e for e in errors if e.field_path.startswith("exits[")]
        self.assertEqual(exit_errors, [])


class TestValidateZoneFullyValid(unittest.TestCase):
    """A fully valid zone dict returns an empty list."""

    def test_fully_valid_zone_returns_empty_list(self):
        """validate_zone() returns [] when all fields are valid."""
        errors = validate_zone({
            "zone": {
                "name": "Test Zone",
                "zone_type": "plains",
                "continent": "varath",
                "faction_territory": "neutral",
            },
            "rooms": [],
            "exits": [],
        })
        self.assertEqual(errors, [])

    def test_fully_valid_zone_with_rooms_and_exits(self):
        """validate_zone() returns [] for valid zone with rooms and exits."""
        errors = validate_zone({
            "zone": {
                "name": "Forest Test",
                "zone_type": "ancient_forest",
                "continent": "sorath",
                "faction_territory": "warden",
                "node_type": "temporal",
            },
            "rooms": [
                {"room_type": "path"},
                {"room_type": "clearing"},
                {"room_type": "ruins"},
            ],
            "exits": [
                {"direction": "north"},
                {"direction": "south"},
                {"direction": "up"},
            ],
        })
        self.assertEqual(errors, [])

    def test_multiple_errors_returned_together(self):
        """Multiple validation errors are all returned in a single call."""
        errors = validate_zone({
            "zone": {"name": "", "zone_type": "bog", "continent": "atlantis"},
            "rooms": [{"room_type": "swamp"}],
            "exits": [{"direction": "diagonal"}],
        })
        field_paths = [e.field_path for e in errors]
        self.assertIn("zone.name", field_paths)
        self.assertIn("zone.zone_type", field_paths)
        self.assertIn("zone.continent", field_paths)
        self.assertIn("rooms[0].room_type", field_paths)
        self.assertIn("exits[0].direction", field_paths)


if __name__ == "__main__":
    unittest.main()
