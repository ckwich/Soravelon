"""
Tests for world/zone_serializer.py — JSON→AreaBuilder adapter.

Uses EvenniaTest to provide DB-backed Evennia objects (rooms, zone objects).
Tests are organized by behavior: validation gating, section mapping, and
cross-zone exit handling.
"""

import json
from unittest.mock import patch, MagicMock
from evennia.utils.test_resources import EvenniaTest

from world.area_builder import AreaBuilderValidationError
from world import zone_registry, named_mob_registry


# ---------------------------------------------------------------------------
# Minimal valid zone_data fixture
# ---------------------------------------------------------------------------

def _minimal_zone_data(zone_id="test_json_zone"):
    """Return the smallest valid zone_data dict load_zone_from_json accepts."""
    return {
        "zone": {
            "zone_id": zone_id,
            "name": "Test JSON Zone",
            "zone_type": "ancient_forest",
            "continent": "varath",
        }
    }


def _zone_data_with_rooms(zone_id="test_json_zone"):
    """Zone data with two rooms and one local exit."""
    return {
        "zone": {
            "zone_id": zone_id,
            "name": "Test JSON Zone",
            "zone_type": "ancient_forest",
            "continent": "varath",
        },
        "rooms": [
            {
                "room_id": "room_001",
                "name": "First Room",
                "desc": "A forest clearing.",
                "room_type": "clearing",
            },
            {
                "room_id": "room_002",
                "name": "Second Room",
                "desc": "A narrow path.",
                "room_type": "path",
            },
        ],
        "exits": [
            {
                "from_room": "room_001",
                "to": "room_002",
                "direction": "north",
            },
            {
                "from_room": "room_002",
                "to": "room_001",
                "direction": "south",
            },
        ],
    }


# ---------------------------------------------------------------------------
# Base test class
# ---------------------------------------------------------------------------

class ZoneSerializerTestBase(EvenniaTest):
    """Common setup for zone serializer tests."""

    def setUp(self):
        super().setUp()
        zone_registry.clear()
        named_mob_registry.clear()

    def tearDown(self):
        zone_registry.clear()
        named_mob_registry.clear()
        super().tearDown()


# ---------------------------------------------------------------------------
# Import and callable tests
# ---------------------------------------------------------------------------

class TestZoneSerializerImport(ZoneSerializerTestBase):
    def test_import_ok(self):
        """load_zone_from_json can be imported from world.zone_serializer."""
        from world.zone_serializer import load_zone_from_json
        self.assertTrue(callable(load_zone_from_json))

    def test_returns_dict(self):
        """load_zone_from_json returns a dict with expected build() keys."""
        from world.zone_serializer import load_zone_from_json
        report = load_zone_from_json(_minimal_zone_data())
        self.assertIsInstance(report, dict)
        self.assertIn("zone_id", report)
        self.assertIn("rooms_created", report)
        self.assertIn("exits_created", report)
        self.assertIn("warnings", report)


# ---------------------------------------------------------------------------
# Validation gating tests
# ---------------------------------------------------------------------------

class TestValidationGating(ZoneSerializerTestBase):
    def test_raises_on_error_severity_validation(self):
        """load_zone_from_json raises AreaBuilderValidationError for invalid zone data."""
        from world.zone_serializer import load_zone_from_json

        bad_data = {
            "zone": {
                "zone_id": "bad_zone",
                "name": "Bad Zone",
                "zone_type": "INVALID_TYPE",  # not in VALID_ZONE_TYPES
                "continent": "varath",
            }
        }
        with self.assertRaises(AreaBuilderValidationError):
            load_zone_from_json(bad_data)

    def test_calls_validate_zone_before_building(self):
        """load_zone_from_json calls validate_zone() before calling AreaBuilder."""
        from world.zone_serializer import load_zone_from_json
        from world import area_validator

        calls = []
        original_validate = area_validator.validate_zone

        def mock_validate(zone_data):
            calls.append(zone_data)
            return original_validate(zone_data)

        with patch("world.zone_serializer.validate_zone", side_effect=mock_validate):
            load_zone_from_json(_minimal_zone_data())

        self.assertEqual(len(calls), 1)

    def test_missing_zone_key_raises(self):
        """load_zone_from_json raises if 'zone' key is missing."""
        from world.zone_serializer import load_zone_from_json

        # Missing required "zone" top-level key — should raise
        with self.assertRaises((KeyError, AreaBuilderValidationError)):
            load_zone_from_json({})

    def test_warning_severity_does_not_raise(self):
        """Validation warnings (not errors) do not prevent zone from loading."""
        from world.zone_serializer import load_zone_from_json
        from world.area_validator import ValidationError

        # Patch validate_zone to return a warning (not an error)
        warning = ValidationError(severity="warning", field_path="zone.tier", message="tier missing")
        with patch("world.zone_serializer.validate_zone", return_value=[warning]):
            # Should NOT raise
            report = load_zone_from_json(_minimal_zone_data())
        self.assertIsInstance(report, dict)


# ---------------------------------------------------------------------------
# Zone section tests
# ---------------------------------------------------------------------------

class TestZoneSectionMapping(ZoneSerializerTestBase):
    def test_zone_created_with_correct_id(self):
        """load_zone_from_json creates zone object with zone_id from JSON."""
        from world.zone_serializer import load_zone_from_json
        import evennia

        report = load_zone_from_json(_minimal_zone_data("json_zone_abc"))
        self.assertEqual(report["zone_id"], "json_zone_abc")

    def test_zone_id_excluded_from_zone_kwargs(self):
        """zone_id is not passed as a kwarg to area.zone() — it's the constructor arg."""
        from world.zone_serializer import load_zone_from_json
        from world.area_builder import AreaBuilder

        call_kwargs = {}
        original_zone = AreaBuilder.zone

        def recording_zone(self_ab, **kwargs):
            call_kwargs.update(kwargs)
            return original_zone(self_ab, **kwargs)

        with patch.object(AreaBuilder, "zone", recording_zone):
            load_zone_from_json(_minimal_zone_data("kwarg_test_zone"))

        self.assertNotIn("zone_id", call_kwargs)
        self.assertIn("name", call_kwargs)
        self.assertIn("zone_type", call_kwargs)


# ---------------------------------------------------------------------------
# Rooms section tests
# ---------------------------------------------------------------------------

class TestRoomsSection(ZoneSerializerTestBase):
    def test_rooms_created(self):
        """load_zone_from_json creates rooms specified in JSON."""
        from world.zone_serializer import load_zone_from_json
        import evennia

        zone_data = _zone_data_with_rooms("rooms_test_zone")
        report = load_zone_from_json(zone_data)
        self.assertEqual(report["rooms_created"], 2)

    def test_rooms_key_missing_defaults_empty(self):
        """load_zone_from_json handles missing 'rooms' key gracefully."""
        from world.zone_serializer import load_zone_from_json

        data = _minimal_zone_data("no_rooms_zone")
        # No "rooms" key at all
        report = load_zone_from_json(data)
        self.assertEqual(report["rooms_created"], 0)

    def test_room_id_excluded_from_room_kwargs(self):
        """room_id is passed positionally to area.room(), not as a kwarg."""
        from world.zone_serializer import load_zone_from_json
        from world.area_builder import AreaBuilder

        positional_ids = []
        original_room = AreaBuilder.room

        def recording_room(self_ab, room_id, **kwargs):
            positional_ids.append(room_id)
            self.assertNotIn("room_id", kwargs)
            return original_room(self_ab, room_id, **kwargs)

        zone_data = _zone_data_with_rooms("room_kwargs_test")
        with patch.object(AreaBuilder, "room", recording_room):
            load_zone_from_json(zone_data)

        self.assertIn("room_001", positional_ids)
        self.assertIn("room_002", positional_ids)


# ---------------------------------------------------------------------------
# Exits section tests
# ---------------------------------------------------------------------------

class TestExitsSection(ZoneSerializerTestBase):
    def test_local_exits_created(self):
        """load_zone_from_json creates local exits between rooms in the zone."""
        from world.zone_serializer import load_zone_from_json

        zone_data = _zone_data_with_rooms("exits_test_zone")
        report = load_zone_from_json(zone_data)
        self.assertEqual(report["exits_created"], 2)

    def test_cross_zone_exit_uses_string_target(self):
        """Cross-zone exits with 'zone_id:room_id' format pass string to area.exit()."""
        from world.zone_serializer import load_zone_from_json
        from world.area_builder import AreaBuilder

        exit_targets = []
        original_exit = AreaBuilder.exit

        def recording_exit(self_ab, from_room, to_room, direction, **kwargs):
            exit_targets.append(to_room)
            # For cross-zone, pass string; for local, pass room object
            if isinstance(to_room, str):
                # Cannot create cross-zone exit in test (target not loaded)
                # Just record that we got a string
                return
            return original_exit(self_ab, from_room, to_room, direction, **kwargs)

        zone_data = _zone_data_with_rooms("cross_exit_zone")
        zone_data["exits"].append({
            "from_room": "room_001",
            "to": "other_zone:room_999",
            "direction": "east",
        })

        with patch.object(AreaBuilder, "exit", recording_exit):
            load_zone_from_json(zone_data)

        # The cross-zone exit should have been passed as a string
        self.assertIn("other_zone:room_999", exit_targets)

    def test_from_room_not_found_adds_warning(self):
        """Exit with unknown from_room adds a warning and is skipped."""
        from world.zone_serializer import load_zone_from_json

        zone_data = _minimal_zone_data("missing_from_room")
        zone_data["rooms"] = [
            {"room_id": "room_001", "name": "Room 1", "room_type": "path"},
        ]
        zone_data["exits"] = [
            {
                "from_room": "room_NONEXISTENT",
                "to": "room_001",
                "direction": "north",
            }
        ]
        report = load_zone_from_json(zone_data)
        # Exit skipped, warning added
        self.assertEqual(report["exits_created"], 0)
        self.assertTrue(
            any("from_room" in w or "not in" in w for w in report.get("warnings", [])),
            f"Expected warning about missing from_room. Warnings: {report.get('warnings', [])}"
        )


# ---------------------------------------------------------------------------
# Optional sections default to empty list
# ---------------------------------------------------------------------------

class TestOptionalSectionsDefault(ZoneSerializerTestBase):
    def test_all_optional_sections_absent_ok(self):
        """load_zone_from_json succeeds when all optional sections are absent."""
        from world.zone_serializer import load_zone_from_json

        # Only "zone" key — everything else absent
        data = _minimal_zone_data("all_optional_zone")
        report = load_zone_from_json(data)
        self.assertIsInstance(report, dict)
        self.assertEqual(report["zone_id"], "all_optional_zone")

    def test_spawns_absent_ok(self):
        """Missing 'spawns' key does not cause an error."""
        from world.zone_serializer import load_zone_from_json
        data = _minimal_zone_data("no_spawns_zone")
        report = load_zone_from_json(data)
        self.assertIsInstance(report, dict)

    def test_node_null_ok(self):
        """node: null in JSON is handled without error."""
        from world.zone_serializer import load_zone_from_json
        data = _minimal_zone_data("null_node_zone")
        data["node"] = None
        report = load_zone_from_json(data)
        self.assertIsInstance(report, dict)

    def test_node_absent_ok(self):
        """Missing 'node' key is handled without error."""
        from world.zone_serializer import load_zone_from_json
        data = _minimal_zone_data("absent_node_zone")
        # No "node" key
        report = load_zone_from_json(data)
        self.assertIsInstance(report, dict)


# ---------------------------------------------------------------------------
# Materials and quests section (delegated to AreaBuilder stub)
# ---------------------------------------------------------------------------

class TestMaterialsSection(ZoneSerializerTestBase):
    def test_materials_passed_to_area_builder(self):
        """load_zone_from_json calls area.material() for each materials entry."""
        from world.zone_serializer import load_zone_from_json
        from world.area_builder import AreaBuilder

        mat_calls = []
        original_material = AreaBuilder.material

        def recording_material(self_ab, material, **kwargs):
            mat_calls.append(material)
            return original_material(self_ab, material, **kwargs)

        data = _minimal_zone_data("mat_test_zone")
        data["materials"] = [
            {"material": "iron_ore", "tier": 1, "terrain": "underground"},
        ]

        with patch.object(AreaBuilder, "material", recording_material):
            load_zone_from_json(data)

        self.assertIn("iron_ore", mat_calls)


# ---------------------------------------------------------------------------
# Idempotency test
# ---------------------------------------------------------------------------

class TestIdempotency(ZoneSerializerTestBase):
    def test_load_twice_does_not_double_rooms(self):
        """Loading the same zone JSON twice does not create duplicate rooms."""
        from world.zone_serializer import load_zone_from_json
        import evennia

        zone_data = _zone_data_with_rooms("idempotent_json_zone")

        report1 = load_zone_from_json(zone_data)
        zone_registry.clear()
        named_mob_registry.clear()
        report2 = load_zone_from_json(zone_data)

        # Both passes should report 2 rooms (not 4)
        self.assertEqual(report1["rooms_created"], 2)
        self.assertEqual(report2["rooms_created"], 2)

        # Total rooms for this zone should still be 2 in DB
        rooms = evennia.search_tag("idempotent_json_zone", category="zone_id")
        room_objs = [r for r in rooms if hasattr(r, "exits")]
        self.assertEqual(len(room_objs), 2)
