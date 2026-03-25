"""
Tests for the AreaBuilder class (Build Order Step 12).
"""

from unittest.mock import patch, MagicMock
from evennia.utils.test_resources import EvenniaTest
from evennia import create_object

from world.area_builder import AreaBuilder, AreaBuilderValidationError
from world import zone_registry, area_builder as area_builder_module


class AreaBuilderTestBase(EvenniaTest):
    """Base class for AreaBuilder tests with common setup."""

    def setUp(self):
        super().setUp()
        zone_registry.clear()

    def _make_builder(self, zone_id="test_zone"):
        """Create an AreaBuilder with zone() already called."""
        ab = AreaBuilder(zone_id)
        ab.zone(
            name="Test Zone",
            tier=1,
            zone_type="ancient_forest",
            continent="varath",
            region="test_region",
            hub_city="hub_1",
            has_node=False,
            faction_territory="neutral",
        )
        return ab

    def _make_room(self, ab, room_id="room_001", **kwargs):
        """Create a room via the builder with sensible defaults."""
        defaults = {
            "name": f"Room {room_id}",
            "desc": "A test room.",
            "room_type": "path",
            "indoor": False,
            "terrain": "forest_floor",
        }
        defaults.update(kwargs)
        return ab.room(room_id, **defaults)


# ------------------------------------------------------------------
# Zone tests
# ------------------------------------------------------------------

class TestZoneCreatesZoneObject(AreaBuilderTestBase):
    def test_zone_creates_zone_object(self):
        """area.zone() creates ZoneObject with correct zone_id and metadata."""
        ab = self._make_builder("my_zone")
        self.assertIsNotNone(ab._zone_obj)
        self.assertEqual(ab._zone_obj.db.zone_id, "my_zone")
        self.assertEqual(ab._zone_obj.db.name, "Test Zone")
        self.assertEqual(ab._zone_obj.db.tier, 1)
        self.assertEqual(ab._zone_obj.db.zone_type, "ancient_forest")
        self.assertEqual(ab._zone_obj.db.continent, "varath")
        self.assertEqual(ab._zone_obj.db.faction_territory, "neutral")


class TestZoneIdempotent(AreaBuilderTestBase):
    def test_zone_idempotent(self):
        """Loading same zone twice does not create duplicate ZoneObjects."""
        ab1 = self._make_builder("idem_zone")
        zone_obj_1 = ab1._zone_obj

        ab2 = self._make_builder("idem_zone")
        zone_obj_2 = ab2._zone_obj

        self.assertEqual(zone_obj_1.id, zone_obj_2.id)


class TestZoneNoLevelFloorCap(AreaBuilderTestBase):
    def test_zone_no_level_floor_cap(self):
        """ZoneObject has no level_floor or level_cap after zone()."""
        ab = self._make_builder()
        zone_obj = ab._zone_obj
        # These should not be set — db access returns None for missing attrs
        self.assertIsNone(zone_obj.db.level_floor)
        self.assertIsNone(zone_obj.db.level_cap)


# ------------------------------------------------------------------
# Room tests
# ------------------------------------------------------------------

class TestRoomCreatesWithCorrectTags(AreaBuilderTestBase):
    def test_room_tagged_with_zone_id_and_room_type(self):
        """Room tagged with zone_id and room_type in correct categories."""
        ab = self._make_builder()
        room = self._make_room(ab, "room_001", room_type="clearing")

        self.assertTrue(room.tags.get("test_zone", category="zone_id"))
        self.assertTrue(room.tags.get("clearing", category="room_type"))


class TestRoomTaggedWithRoomId(AreaBuilderTestBase):
    def test_room_tagged_with_room_id(self):
        """Room tagged with room_id in category 'room_id' for idempotent lookup."""
        ab = self._make_builder()
        room = self._make_room(ab, "room_042")

        self.assertTrue(room.tags.get("room_042", category="room_id"))


class TestRoomIdempotent(AreaBuilderTestBase):
    def test_room_idempotent(self):
        """Loading same zone twice does not create duplicate rooms."""
        ab1 = self._make_builder("room_idem_zone")
        r1 = self._make_room(ab1, "room_001")

        ab1.build()

        ab2 = self._make_builder("room_idem_zone")
        r2 = self._make_room(ab2, "room_001")

        self.assertEqual(r1.id, r2.id)


# ------------------------------------------------------------------
# Exit tests
# ------------------------------------------------------------------

class TestExitCreatesSoravelonExit(AreaBuilderTestBase):
    def test_exit_creates_soravelon_exit(self):
        """Standard exit creates SoravelonExit between two rooms."""
        from typeclasses.exits import SoravelonExit

        ab = self._make_builder()
        r1 = self._make_room(ab, "room_001")
        r2 = self._make_room(ab, "room_002")
        ab.exit(r1, r2, "north", desc="North passage.")

        exits = [ex for ex in r1.exits if ex.key == "north"]
        self.assertEqual(len(exits), 1)
        self.assertIsInstance(exits[0], SoravelonExit)
        self.assertEqual(exits[0].destination, r2)


class TestExitCreatesHiddenExit(AreaBuilderTestBase):
    def test_exit_creates_hidden_exit(self):
        """hidden=True creates HiddenExit."""
        from typeclasses.exits import HiddenExit

        ab = self._make_builder()
        r1 = self._make_room(ab, "room_001")
        r2 = self._make_room(ab, "room_002")
        ab.exit(r1, r2, "east", hidden=True)

        exits = [ex for ex in r1.exits if ex.key == "east"]
        self.assertEqual(len(exits), 1)
        self.assertIsInstance(exits[0], HiddenExit)


class TestExitCreatesLockedExit(AreaBuilderTestBase):
    def test_exit_creates_locked_exit(self):
        """locked=True creates LockedExit."""
        from typeclasses.exits import LockedExit

        ab = self._make_builder()
        r1 = self._make_room(ab, "room_001")
        r2 = self._make_room(ab, "room_002")
        ab.exit(r1, r2, "west", locked=True, lock_tag="silver_key")

        exits = [ex for ex in r1.exits if ex.key == "west"]
        self.assertEqual(len(exits), 1)
        self.assertIsInstance(exits[0], LockedExit)
        self.assertEqual(exits[0].db.lock_tag, "silver_key")


class TestExitCrossZoneDeferred(AreaBuilderTestBase):
    def test_exit_cross_zone_deferred(self):
        """Cross-zone exit stored as deferred, not created immediately."""
        ab = self._make_builder()
        r1 = self._make_room(ab, "room_001")
        ab.exit(r1, "other_zone:room_010", "south")

        # No exit created yet
        exits = [ex for ex in r1.exits if ex.key == "south"]
        self.assertEqual(len(exits), 0)

        # Stored in deferred list
        self.assertEqual(len(ab._deferred_exits), 1)
        self.assertEqual(ab._deferred_exits[0]["to"], "other_zone:room_010")


# ------------------------------------------------------------------
# Spawn tests
# ------------------------------------------------------------------

class TestSpawnStoredOnRoom(AreaBuilderTestBase):
    def test_spawn_stored_on_room(self):
        """Spawn definition stored in room.db.spawn_definitions."""
        ab = self._make_builder()
        r1 = self._make_room(ab, "room_001")
        ab.spawn(
            r1, "forest_wolf",
            behavior=["aggressive"],
            count_min=1,
            count_max=3,
            respawn_minutes=15,
        )

        spawns = r1.db.spawn_definitions
        self.assertEqual(len(spawns), 1)
        self.assertEqual(spawns[0]["mob"], "forest_wolf")
        self.assertEqual(spawns[0]["count_max"], 3)


# ------------------------------------------------------------------
# Named mob tests
# ------------------------------------------------------------------

class TestNamedMobStoredOnRoom(AreaBuilderTestBase):
    def test_named_mob_stored_in_spawn_definitions(self):
        """Named mob stored in room.db.spawn_definitions with is_named=True.

        Named mobs were merged into the standard spawn definition schema
        (D-13/D-14). area.named_mob() is now a thin wrapper around
        area.spawn() with is_named=True.
        """
        ab = self._make_builder()
        r1 = self._make_room(ab, "room_001")
        ab.named_mob(
            "old_guardian", r1,
            behavior=["territorial"],
            respawn_minutes=120,
            tome_drop="tome_verdant",
        )

        spawns = r1.db.spawn_definitions
        self.assertEqual(len(spawns), 1)
        spawn = spawns[0]
        self.assertEqual(spawn["mob"], "old_guardian")
        self.assertTrue(spawn["is_named"])
        self.assertEqual(spawn["tome_drop"], "tome_verdant")
        self.assertEqual(spawn["respawn_minutes"], 120)
        self.assertEqual(spawn["count_min"], 1)
        self.assertEqual(spawn["count_max"], 1)


class TestNamedMobIsNamedFlag(AreaBuilderTestBase):
    def test_named_mob_has_is_named_true_in_spawn_def(self):
        """Named mob spawn definition has is_named=True after build()."""
        ab = self._make_builder()
        r1 = self._make_room(ab, "room_001")
        ab.named_mob("world_boss_1", r1, behavior=["territorial"])
        ab.build()

        spawns = r1.db.spawn_definitions
        self.assertTrue(any(s.get("is_named") for s in spawns))
        named_spawn = next(s for s in spawns if s.get("is_named"))
        self.assertEqual(named_spawn["mob"], "world_boss_1")


# ------------------------------------------------------------------
# NPC tests
# ------------------------------------------------------------------

class TestNpcStoredOnRoom(AreaBuilderTestBase):
    def test_npc_stored_on_room(self):
        """NPC definition stored in room.db.npc_definitions."""
        ab = self._make_builder()
        r1 = self._make_room(ab, "room_001")
        ab.npc(r1, "maren_warden", quest="wolves_quest", faction="wardens")

        npcs = r1.db.npc_definitions
        self.assertEqual(len(npcs), 1)
        self.assertEqual(npcs[0]["npc_id"], "maren_warden")
        self.assertEqual(npcs[0]["quest"], "wolves_quest")


# ------------------------------------------------------------------
# Node tests
# ------------------------------------------------------------------

class TestNodeCallsInitializeNode(AreaBuilderTestBase):
    def test_node_calls_initialize_node(self):
        """area.node() causes build() to call zone_obj.initialize_node()."""
        ab = AreaBuilder("node_zone")
        ab.zone(
            name="Node Zone",
            tier=1,
            zone_type="ancient_forest",
            continent="varath",
            has_node=True,
            node_type="cognitive",
            node_failure_start=15,
            faction_territory="neutral",
        )
        r1 = self._make_room(ab, "room_001")
        ab.node(center_room=r1, radius=2)

        with patch("world.zone_object.initialize_node") as mock_init:
            ab.build()
            mock_init.assert_called_once()
            call_kwargs = mock_init.call_args
            self.assertEqual(call_kwargs.kwargs["node_type"], "cognitive")
            self.assertEqual(call_kwargs.kwargs["center_room"], r1)
            self.assertEqual(call_kwargs.kwargs["radius"], 2)


# ------------------------------------------------------------------
# Quest tests
# ------------------------------------------------------------------

class TestQuestStoredOnZone(AreaBuilderTestBase):
    def test_quest_stored_on_zone(self):
        """Quest definition stored in zone_obj.db.quest_definitions."""
        ab = self._make_builder()
        ab.quest(
            "wolf_hunt",
            quest_type="incursion",
            quest_giver="maren_warden",
            objective_type="kill_and_gather",
            objective_target="forest_wolf",
            objective_count=30,
        )

        quests = ab._zone_obj.db.quest_definitions
        self.assertEqual(len(quests), 1)
        self.assertEqual(quests[0]["quest_id"], "wolf_hunt")
        self.assertEqual(quests[0]["objective_count"], 30)


# ------------------------------------------------------------------
# Material tests
# ------------------------------------------------------------------

class TestMaterialStoredOnZone(AreaBuilderTestBase):
    def test_material_stored_on_zone(self):
        """Material definition stored in zone_obj.db.material_definitions."""
        ab = self._make_builder()
        ab.material(
            "pala_heartwood",
            tier=2,
            terrain="forest_floor",
            absorbed_property="attunement_touched",
        )

        materials = ab._zone_obj.db.material_definitions
        self.assertEqual(len(materials), 1)
        self.assertEqual(materials[0]["material"], "pala_heartwood")
        self.assertEqual(materials[0]["tier"], 2)


# ------------------------------------------------------------------
# Lore fragment tests
# ------------------------------------------------------------------

class TestLoreFragmentStoredOnRoom(AreaBuilderTestBase):
    def test_lore_fragment_stored_on_room(self):
        """Lore fragment stored in room.db.lore_fragments."""
        ab = self._make_builder()
        r1 = self._make_room(ab, "room_001")
        ab.lore_fragment(
            "lore_cantera_001", r1,
            discovery_method="investigate_node",
            text="The stone is older than the trees.",
            insight_gain=25,
        )

        frags = r1.db.lore_fragments
        self.assertEqual(len(frags), 1)
        self.assertEqual(frags[0]["fragment_id"], "lore_cantera_001")
        self.assertEqual(frags[0]["insight_gain"], 25)


# ------------------------------------------------------------------
# Build tests
# ------------------------------------------------------------------

class TestBuildReturnsReport(AreaBuilderTestBase):
    def test_build_returns_report(self):
        """build() returns dict with rooms_created, exits_created, warnings."""
        ab = self._make_builder()
        r1 = self._make_room(ab, "room_001")
        r2 = self._make_room(ab, "room_002")
        ab.exit(r1, r2, "north")
        ab.spawn(r1, "wolf")

        report = ab.build()

        self.assertIn("rooms_created", report)
        self.assertIn("exits_created", report)
        self.assertIn("warnings", report)
        self.assertEqual(report["rooms_created"], 2)
        self.assertEqual(report["exits_created"], 1)
        self.assertIsInstance(report["warnings"], list)


class TestBuildRegistersZone(AreaBuilderTestBase):
    def test_build_registers_zone(self):
        """zone_registry.get_zone() returns zone after build()."""
        ab = self._make_builder("reg_zone")
        ab.build()

        zone_obj = zone_registry.get_zone("reg_zone")
        self.assertIsNotNone(zone_obj)
        self.assertEqual(zone_obj.db.zone_id, "reg_zone")


# ------------------------------------------------------------------
# Validation tests
# ------------------------------------------------------------------

class TestValidationInvalidZoneType(AreaBuilderTestBase):
    def test_validation_invalid_zone_type(self):
        """Raises AreaBuilderValidationError for unknown zone_type."""
        ab = AreaBuilder("bad_zone")
        with self.assertRaises(AreaBuilderValidationError) as ctx:
            ab.zone(name="Bad", zone_type="bog", continent="varath",
                     faction_territory="neutral")
        self.assertIn("bog", str(ctx.exception))


class TestValidationInvalidDirection(AreaBuilderTestBase):
    def test_validation_invalid_direction(self):
        """Raises error for unknown exit direction."""
        ab = self._make_builder()
        r1 = self._make_room(ab, "room_001")
        r2 = self._make_room(ab, "room_002")
        with self.assertRaises(AreaBuilderValidationError) as ctx:
            ab.exit(r1, r2, "sideways")
        self.assertIn("sideways", str(ctx.exception))


# ------------------------------------------------------------------
# Cross-zone exit resolution
# ------------------------------------------------------------------

class TestCrossZoneExitResolvedWhenTargetLoaded(AreaBuilderTestBase):
    def test_cross_zone_exit_resolved_when_target_loaded(self):
        """After both zones loaded, cross-zone exit resolves correctly."""
        # Build zone A with a target room
        ab_a = self._make_builder("zone_a")
        target = self._make_room(ab_a, "target_room")
        ab_a.build()

        # Build zone B with a cross-zone exit to zone_a:target_room
        ab_b = AreaBuilder("zone_b")
        ab_b.zone(
            name="Zone B", tier=1, zone_type="plains",
            continent="varath", faction_territory="neutral",
        )
        origin = self._make_room(ab_b, "origin_room")
        ab_b.exit(origin, "zone_a:target_room", "south")
        ab_b.build()

        exits = [ex for ex in origin.exits if ex.key == "south"]
        self.assertEqual(len(exits), 1)
        self.assertEqual(exits[0].destination, target)


# ------------------------------------------------------------------
# File loading tests
# ------------------------------------------------------------------

class TestZoneLoadsFromFile(AreaBuilderTestBase):
    def test_zone_loads_from_file(self):
        """A minimal area file can be imported and build() called."""
        # Simulate what an area file does
        ab = AreaBuilder("file_test_zone")
        ab.zone(
            name="File Test",
            tier=1,
            zone_type="plains",
            continent="varath",
            faction_territory="neutral",
        )
        r1 = ab.room("room_001", name="Start", desc="Start room.",
                      room_type="path", indoor=False, terrain="plains")
        r2 = ab.room("room_002", name="End", desc="End room.",
                      room_type="path", indoor=False, terrain="plains")
        ab.exit(r1, r2, "north")
        ab.exit(r2, r1, "south")
        ab.spawn(r1, "plains_wolf", count_min=1, count_max=2)
        ab.npc(r2, "test_npc", quest="test_quest")

        report = ab.build()

        self.assertEqual(report["rooms_created"], 2)
        self.assertEqual(report["exits_created"], 2)
        self.assertIsNotNone(zone_registry.get_zone("file_test_zone"))


class TestServerStartLoadsAreasDir(AreaBuilderTestBase):
    def test_server_start_loads_areas_dir(self):
        """_load_all_zones() processes .py files in world/areas/ without error."""
        from server.conf.at_server_startstop import _load_all_zones

        # Should not raise even with empty areas directory
        _load_all_zones()

        # Verify registries were cleared and rebuilt (empty is fine)
        self.assertIsInstance(zone_registry.get_all_zones(), list)


# ------------------------------------------------------------------
# Grid coordinate tests (CLI-07)
# ------------------------------------------------------------------

class TestRoomGridCoordsExplicit(AreaBuilderTestBase):
    def test_explicit_grid_coords_stored_on_room(self):
        """area.room() with grid_x/grid_y stores those values on room.db."""
        ab = self._make_builder()
        room = self._make_room(ab, "room_001", grid_x=3, grid_y=-1)
        self.assertEqual(room.db.grid_x, 3)
        self.assertEqual(room.db.grid_y, -1)


class TestRoomGridCoordsDefaultNone(AreaBuilderTestBase):
    def test_room_without_coords_defaults_to_none(self):
        """area.room() without grid_x/grid_y stores None on room.db."""
        ab = self._make_builder()
        room = self._make_room(ab, "room_001")
        self.assertIsNone(room.db.grid_x)
        self.assertIsNone(room.db.grid_y)


class TestZoneWorldCoords(AreaBuilderTestBase):
    def test_zone_world_coords_stored_on_zone_obj(self):
        """area.zone() with world_x/world_y/world_radius/fog_of_war stores those attrs."""
        ab = AreaBuilder("world_coord_zone")
        ab.zone(
            name="World Coord Zone",
            tier=1,
            zone_type="ancient_forest",
            continent="varath",
            faction_territory="neutral",
            world_x=10,
            world_y=5,
            world_radius=2,
            fog_of_war=True,
        )
        self.assertEqual(ab._zone_obj.db.world_x, 10)
        self.assertEqual(ab._zone_obj.db.world_y, 5)
        self.assertEqual(ab._zone_obj.db.world_radius, 2)
        self.assertTrue(ab._zone_obj.db.fog_of_war)


class TestZoneWorldCoordsDefaults(AreaBuilderTestBase):
    def test_zone_world_coords_default_none_and_false(self):
        """area.zone() without world coords stores None/None/None/False."""
        ab = self._make_builder()
        self.assertIsNone(ab._zone_obj.db.world_x)
        self.assertIsNone(ab._zone_obj.db.world_y)
        self.assertIsNone(ab._zone_obj.db.world_radius)
        self.assertFalse(ab._zone_obj.db.fog_of_war)


# ------------------------------------------------------------------
# Auto-layout tests (CLI-07)
# ------------------------------------------------------------------

class TestAutoLayoutAssignsCoords(AreaBuilderTestBase):
    def test_auto_layout_fills_none_coords_after_build(self):
        """build() assigns non-None grid_x/grid_y to rooms without explicit coords."""
        ab = self._make_builder("layout_zone")
        r1 = self._make_room(ab, "room_001")
        r2 = self._make_room(ab, "room_002")
        ab.exit(r1, r2, "north")
        ab.build()

        self.assertIsNotNone(r1.db.grid_x)
        self.assertIsNotNone(r1.db.grid_y)
        self.assertIsNotNone(r2.db.grid_x)
        self.assertIsNotNone(r2.db.grid_y)


class TestAutoLayoutNorthChain(AreaBuilderTestBase):
    def test_auto_layout_north_chain_coords(self):
        """BFS north-chain: r1=(0,0), r2=(0,1), r3=(0,2)."""
        ab = self._make_builder("north_chain_zone")
        r1 = self._make_room(ab, "room_001")
        r2 = self._make_room(ab, "room_002")
        r3 = self._make_room(ab, "room_003")
        ab.exit(r1, r2, "north")
        ab.exit(r2, r3, "north")
        ab.build()

        self.assertEqual(r1.db.grid_x, 0)
        self.assertEqual(r1.db.grid_y, 0)
        self.assertEqual(r2.db.grid_x, 0)
        self.assertEqual(r2.db.grid_y, 1)
        self.assertEqual(r3.db.grid_x, 0)
        self.assertEqual(r3.db.grid_y, 2)


class TestAutoLayoutPreservesExplicitCoords(AreaBuilderTestBase):
    def test_auto_layout_does_not_overwrite_explicit_coords(self):
        """Rooms with explicit grid_x/grid_y keep those values after build()."""
        ab = self._make_builder("explicit_zone")
        r1 = self._make_room(ab, "room_001", grid_x=5, grid_y=5)
        r2 = self._make_room(ab, "room_002")
        ab.exit(r1, r2, "north")
        ab.build()

        # r1 coords unchanged
        self.assertEqual(r1.db.grid_x, 5)
        self.assertEqual(r1.db.grid_y, 5)
        # r2 was auto-laid out
        self.assertIsNotNone(r2.db.grid_x)
        self.assertIsNotNone(r2.db.grid_y)


class TestAutoLayoutNoCollision(AreaBuilderTestBase):
    def test_auto_layout_no_two_rooms_share_coords(self):
        """After build(), no two rooms share the same (grid_x, grid_y)."""
        ab = self._make_builder("collision_zone")
        r1 = self._make_room(ab, "room_001")
        r2 = self._make_room(ab, "room_002")
        r3 = self._make_room(ab, "room_003")
        # Connect with up/down which would cause (0,0) collision without nudge
        ab.exit(r1, r2, "north")
        ab.exit(r1, r3, "up")
        ab.build()

        coords = [(r.db.grid_x, r.db.grid_y) for r in [r1, r2, r3]]
        self.assertEqual(len(coords), len(set(coords)), f"Collision detected: {coords}")


# ------------------------------------------------------------------
# Additional coordinate tests (CLI-07, plan 02-04)
# ------------------------------------------------------------------

class TestExplicitCoordsPreserved(AreaBuilderTestBase):
    """Builder-placed coords are preserved exactly after build()."""

    def test_explicit_coords_not_overwritten(self):
        """Rooms with specific grid_x/grid_y in area spec keep those exact values."""
        ab = self._make_builder("coord_zone_4")
        r1 = self._make_room(ab, "placed_1", grid_x=5, grid_y=3)
        r2 = self._make_room(ab, "placed_2", grid_x=6, grid_y=3)
        ab.exit(r1, r2, "east")
        ab.build()
        self.assertEqual(r1.db.grid_x, 5)
        self.assertEqual(r1.db.grid_y, 3)
        self.assertEqual(r2.db.grid_x, 6)
        self.assertEqual(r2.db.grid_y, 3)

    def test_mixed_explicit_and_auto(self):
        """One room with explicit coords, adjacent room gets auto-assigned coords."""
        ab = self._make_builder("coord_zone_5")
        r1 = self._make_room(ab, "anchor", grid_x=10, grid_y=0)
        r2 = self._make_room(ab, "auto_placed")
        ab.exit(r1, r2, "east")
        ab.build()
        # Explicit coord preserved
        self.assertEqual(r1.db.grid_x, 10)
        # Auto-placed room received a coord
        self.assertIsNotNone(r2.db.grid_x)
        self.assertIsNotNone(r2.db.grid_y)


class TestAutoLayoutAllRoomsGetCoords(AreaBuilderTestBase):
    """Every room in a zone receives grid coords after build(), even in 5-room chains."""

    def test_all_rooms_get_coords_after_build(self):
        """Every room in the zone has non-None grid_x and grid_y after build()."""
        ab = self._make_builder("coord_zone_all")
        rooms = [self._make_room(ab, f"rx{i}") for i in range(5)]
        for i in range(len(rooms) - 1):
            ab.exit(rooms[i], rooms[i + 1], "east")
        ab.build()
        for r in rooms:
            self.assertIsNotNone(r.db.grid_x, f"room {r.key} has no grid_x")
            self.assertIsNotNone(r.db.grid_y, f"room {r.key} has no grid_y")

    def test_up_down_exits_no_collision(self):
        """Up/down exits (no 2D offset) do not cause two rooms to share coords."""
        ab = self._make_builder("coord_zone_updown")
        r1 = self._make_room(ab, "base")
        r2 = self._make_room(ab, "above")
        r3 = self._make_room(ab, "below")
        ab.exit(r1, r2, "up")
        ab.exit(r1, r3, "down")
        ab.build()
        coords = [(r.db.grid_x, r.db.grid_y) for r in (r1, r2, r3)]
        self.assertEqual(len(coords), len(set(coords)), "Two rooms share the same coordinates")


class TestZoneWorldCoordsExtra(AreaBuilderTestBase):
    """Extra coverage for zone world_x/world_y/world_radius/fog_of_war storage."""

    def test_fog_of_war_defaults_false(self):
        """Zone without fog_of_war=True stores False on zone_obj.db.fog_of_war."""
        ab = self._make_builder("fog_default_zone_extra")
        self.assertFalse(ab._zone_obj.db.fog_of_war)

    def test_world_coords_stored_on_zone_obj(self):
        """zone() with world_x/world_y/world_radius/fog_of_war stores all four attrs."""
        ab = AreaBuilder("world_coord_zone_2")
        ab.zone(
            name="World Coord Zone 2",
            tier=1,
            zone_type="plains",
            continent="varath",
            faction_territory="neutral",
            world_x=15,
            world_y=8,
            world_radius=3,
            fog_of_war=True,
        )
        self.assertEqual(ab._zone_obj.db.world_x, 15)
        self.assertEqual(ab._zone_obj.db.world_y, 8)
        self.assertEqual(ab._zone_obj.db.world_radius, 3)
        self.assertTrue(ab._zone_obj.db.fog_of_war)


# ------------------------------------------------------------------
# Unresolved exit registry tests (BLD-06, plan 03-02)
# ------------------------------------------------------------------

class TestUnresolvedExitsTracked(AreaBuilderTestBase):
    """AreaBuilder tracks cross-zone exits that could not be resolved."""

    def test_unresolved_exits_list_initialized(self):
        """AreaBuilder.__init__ creates _unresolved_exits list."""
        ab = AreaBuilder("init_test_zone")
        self.assertIsInstance(ab._unresolved_exits, list)
        self.assertEqual(len(ab._unresolved_exits), 0)

    def test_expose_unresolved_exits_method_exists(self):
        """expose_unresolved_exits() method exists and returns a list."""
        ab = self._make_builder()
        result = ab.expose_unresolved_exits()
        self.assertIsInstance(result, list)

    def test_unresolved_exit_captured_after_build(self):
        """After build() with unresolvable cross-zone exit, _unresolved_exits is populated."""
        ab = self._make_builder("zone_src")
        r1 = self._make_room(ab, "room_001")
        ab.exit(r1, "nonexistent_zone:room_999", "north")
        ab.build()

        unresolved = ab.expose_unresolved_exits()
        self.assertEqual(len(unresolved), 1)
        self.assertEqual(unresolved[0]["to"], "nonexistent_zone:room_999")
        self.assertEqual(unresolved[0]["direction"], "north")

    def test_unresolved_exit_preserves_from_room(self):
        """Unresolved exit dict preserves 'from_room' key for retry."""
        ab = self._make_builder("zone_src2")
        r1 = self._make_room(ab, "room_001")
        ab.exit(r1, "no_zone:room_x", "south")
        ab.build()

        unresolved = ab.expose_unresolved_exits()
        self.assertEqual(len(unresolved), 1)
        self.assertIn("from_room", unresolved[0])
        self.assertEqual(unresolved[0]["from_room"], r1)

    def test_resolved_exit_not_in_unresolved(self):
        """Exit that resolves successfully is NOT added to _unresolved_exits."""
        # Build target zone first
        ab_target = AreaBuilder("target_zone_r")
        ab_target.zone(
            name="Target Zone R", tier=1, zone_type="plains",
            continent="varath", faction_territory="neutral",
        )
        self._make_room(ab_target, "room_tgt")
        ab_target.build()

        # Build source zone with resolvable cross-zone exit
        ab_src = self._make_builder("zone_src_r")
        r1 = self._make_room(ab_src, "room_001")
        ab_src.exit(r1, "target_zone_r:room_tgt", "east")
        ab_src.build()

        unresolved = ab_src.expose_unresolved_exits()
        self.assertEqual(len(unresolved), 0)

    def test_build_report_contains_unresolved_exits_key(self):
        """build() return dict contains 'unresolved_exits' key."""
        ab = self._make_builder("report_zone")
        r1 = self._make_room(ab, "room_001")
        ab.exit(r1, "missing_zone:room_x", "west")
        report = ab.build()

        self.assertIn("unresolved_exits", report)
        self.assertIsInstance(report["unresolved_exits"], list)

    def test_build_report_unresolved_exits_routing_info_only(self):
        """build() unresolved_exits list contains 'to' and 'direction' only."""
        ab = self._make_builder("report_zone2")
        r1 = self._make_room(ab, "room_001")
        ab.exit(r1, "missing_zone:room_y", "up")
        report = ab.build()

        self.assertEqual(len(report["unresolved_exits"]), 1)
        item = report["unresolved_exits"][0]
        self.assertEqual(item["to"], "missing_zone:room_y")
        self.assertEqual(item["direction"], "up")
        self.assertNotIn("from_room", item)

    def test_module_level_registry_populated_on_unresolved(self):
        """Module-level _UNRESOLVED_EXITS_REGISTRY is populated when exits are unresolved."""
        from world.area_builder import clear_unresolved_exits, get_unresolved_exits
        clear_unresolved_exits()

        ab = self._make_builder("module_reg_zone")
        r1 = self._make_room(ab, "room_001")
        ab.exit(r1, "ghost_zone:ghost_room", "north")
        ab.build()

        registry = get_unresolved_exits()
        self.assertGreater(len(registry), 0)
        self.assertEqual(registry[0]["to"], "ghost_zone:ghost_room")

    def test_clear_unresolved_exits_empties_registry(self):
        """clear_unresolved_exits() resets the module-level registry to empty."""
        from world.area_builder import clear_unresolved_exits, get_unresolved_exits
        # Populate it
        ab = self._make_builder("clear_test_zone")
        r1 = self._make_room(ab, "room_001")
        ab.exit(r1, "phantom_zone:r1", "east")
        ab.build()

        # Now clear
        clear_unresolved_exits()
        self.assertEqual(get_unresolved_exits(), [])


# ------------------------------------------------------------------
# Two-pass _load_all_zones tests (BLD-06, plan 03-02)
# ------------------------------------------------------------------

class TestTwoPassLoadAllZones(AreaBuilderTestBase):
    """_load_all_zones() uses two-pass strategy for cross-zone exits."""

    def test_load_all_zones_calls_clear_unresolved_exits(self):
        """_load_all_zones() clears the unresolved exit registry before pass 1."""
        from server.conf.at_server_startstop import _load_all_zones
        from world.area_builder import clear_unresolved_exits, get_unresolved_exits

        with patch("world.area_builder.clear_unresolved_exits") as mock_clear:
            _load_all_zones()
            mock_clear.assert_called_once()

    def test_load_all_zones_calls_get_unresolved_exits(self):
        """_load_all_zones() calls get_unresolved_exits() after pass 1."""
        from server.conf.at_server_startstop import _load_all_zones

        with patch("world.area_builder.get_unresolved_exits", return_value=[]) as mock_get:
            _load_all_zones()
            mock_get.assert_called_once()

    def test_second_pass_resolves_cross_zone_exit(self):
        """
        Exit that was unresolved in pass 1 (target not yet loaded) gets
        resolved in pass 2 once all zones are available.
        This is a full integration test simulating two-zone load order problem.
        """
        from world.area_builder import clear_unresolved_exits

        # Build zone A (destination) and zone B (source with exit to A)
        # Zone B is loaded BEFORE zone A — simulates the BLD-06 failure case
        clear_unresolved_exits()

        # Build zone_b first with an exit pointing to zone_a (not yet built)
        ab_b = AreaBuilder("bld06_zone_b")
        ab_b.zone(
            name="Zone B BLD06", tier=1, zone_type="plains",
            continent="varath", faction_territory="neutral",
        )
        origin_room = self._make_room(ab_b, "origin_room_b")
        ab_b.exit(origin_room, "bld06_zone_a:entry_room_a", "north")
        ab_b.build()

        # Exit is unresolved (zone_a not built yet)
        unresolved_after_b = ab_b.expose_unresolved_exits()
        self.assertEqual(len(unresolved_after_b), 1)

        # Now build zone_a (target)
        ab_a = AreaBuilder("bld06_zone_a")
        ab_a.zone(
            name="Zone A BLD06", tier=1, zone_type="plains",
            continent="varath", faction_territory="neutral",
        )
        self._make_room(ab_a, "entry_room_a")
        ab_a.build()

        # Manually simulate the second pass retry
        from world.area_builder import get_unresolved_exits
        import evennia as _ev

        all_unresolved = get_unresolved_exits()
        self.assertGreater(len(all_unresolved), 0,
                           "Module registry must have the unresolved exit from zone_b")

        # Second pass: try to resolve each unresolved exit
        for exit_data in all_unresolved:
            target_str = exit_data["to"]
            target_zone_id, target_room_id = target_str.split(":", 1)
            candidates = _ev.search_tag(target_room_id, category="room_id")
            target = None
            for room in candidates:
                if (room.db.zone_id or "") == target_zone_id:
                    target = room
                    break
            if target:
                from_room = exit_data["from_room"]
                direction = exit_data["direction"]
                from world.area_builder import AreaBuilder as _AB
                retry_builder = _AB.__new__(_AB)
                retry_builder._zone_id = from_room.db.zone_id or "unknown"
                retry_builder._exits_created = 0
                retry_builder._create_exit_object(from_room, target, direction)

        # Verify the exit now exists
        exits = [ex for ex in origin_room.exits if ex.key == "north"]
        self.assertEqual(len(exits), 1, "Second-pass retry must have created the exit")
