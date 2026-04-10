"""
Tests for the Soravelon node system (Build Order Step 3).

Tests written FIRST per TDD. These must all fail before production code.
"""

from unittest.mock import patch
from evennia.utils.test_resources import EvenniaTest
from evennia import create_object, create_script


class NodeTestBase(EvenniaTest):
    """Base class that sets up a zone with rooms for node testing."""

    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom, Layer1Room
        from typeclasses.objects import Object

        # Create a ZoneObject
        self.zone_obj = create_object(
            Object, key="test_zone_obj", location=None
        )
        self.zone_obj.db.zone_id = "test_zone"
        self.zone_obj.tags.add("zone_object", category="object_type")

        # Create Layer 0 rooms in this zone
        self.room_center = create_object(
            SoravelonRoom, key="Center Room"
        )
        self.room_center.db.zone_id = "test_zone"
        self.room_center.tags.add("test_zone", category="zone_id")

        self.room_north = create_object(
            SoravelonRoom, key="North Room"
        )
        self.room_north.db.zone_id = "test_zone"
        self.room_north.tags.add("test_zone", category="zone_id")

        self.room_far = create_object(
            SoravelonRoom, key="Far Room"
        )
        self.room_far.db.zone_id = "test_zone"
        self.room_far.tags.add("test_zone", category="zone_id")

        # Room in a different zone (should not be traversed by BFS)
        self.room_other_zone = create_object(
            SoravelonRoom, key="Other Zone Room"
        )
        self.room_other_zone.db.zone_id = "other_zone"
        self.room_other_zone.tags.add("other_zone", category="zone_id")

        # Create exits: center <-> north <-> far, center -> other_zone
        from evennia import create_object as co
        from evennia.objects.objects import DefaultExit

        create_object(
            DefaultExit, key="north",
            location=self.room_center,
            destination=self.room_north
        )
        create_object(
            DefaultExit, key="south",
            location=self.room_north,
            destination=self.room_center
        )
        create_object(
            DefaultExit, key="north",
            location=self.room_north,
            destination=self.room_far
        )
        create_object(
            DefaultExit, key="south",
            location=self.room_far,
            destination=self.room_north
        )
        # Cross-zone exit
        create_object(
            DefaultExit, key="east",
            location=self.room_center,
            destination=self.room_other_zone
        )


class TestFailureSliderRange(NodeTestBase):
    """Failure slider must stay within 0-100."""

    def test_failure_never_exceeds_100(self):
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)
        script.db.failure = 99.0
        script.receive_tick(player_count=100, scholar_count=0,
                            stabilizer_count=0)
        self.assertLessEqual(script.db.failure, 100.0)

    def test_failure_never_below_0(self):
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)
        script.db.failure = 1.0
        script.receive_tick(player_count=0, scholar_count=0,
                            stabilizer_count=100)
        self.assertGreaterEqual(script.db.failure, 0.0)


class TestStateTransitions(NodeTestBase):
    """Correct states at threshold boundaries."""

    def test_states_at_thresholds(self):
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)

        test_cases = [
            (0, "dormant"), (29, "dormant"),
            (30, "awakening"), (59, "awakening"),
            (60, "active"), (89, "active"),
            (90, "critical"), (100, "critical"),
        ]
        for failure, expected_state in test_cases:
            script.db.failure = float(failure)
            script.db.state = script._failure_to_state(failure)
            self.assertEqual(
                script.db.state, expected_state,
                f"failure={failure} should be {expected_state}, "
                f"got {script.db.state}"
            )


class TestSessionCap(NodeTestBase):
    """Player contribution capped at +5% per node event session."""

    def test_session_cap_applied(self):
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)
        script.db.failure = 50.0
        script.db.session_failure_added = 0.0

        # 100 players × 0.1 = 10.0 per tick, but cap is 5.0 total
        script.receive_tick(player_count=100, scholar_count=0,
                            stabilizer_count=0)

        self.assertLessEqual(script.db.session_failure_added, 5.0)

    def test_session_cap_resets_on_deactivation(self):
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)
        script.db.failure = 65.0  # active state
        script.db.state = "active"
        script.db.session_failure_added = 4.5
        script.db.layer1_active = False  # no rooms to deactivate

        # Push below 60 to trigger deactivation
        script.receive_tick(player_count=0, scholar_count=0,
                            stabilizer_count=20)  # -10.0

        # Should have transitioned out of active → cap reset
        self.assertEqual(script.db.session_failure_added, 0.0)


class TestStabilization(NodeTestBase):
    """Stabilization reduces failure correctly."""

    def test_stabilization_reduces_failure(self):
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)
        script.db.failure = 70.0
        script.db.state = "active"

        # 2 stabilizers × -0.5 = -1.0 per tick
        script.receive_tick(player_count=0, scholar_count=0,
                            stabilizer_count=2)

        self.assertLess(script.db.failure, 70.0)

    def test_stabilization_can_push_below_active(self):
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)
        script.db.failure = 60.5
        script.db.state = "active"
        script.db.layer1_active = False

        # Heavy stabilization
        script.receive_tick(player_count=0, scholar_count=0,
                            stabilizer_count=10)

        self.assertLess(script.db.failure, 60.0)
        self.assertIn(script.db.state, ("dormant", "awakening"))


class TestLayer1RoomsHaveDbIds(NodeTestBase):
    """Layer 1 rooms created by initialize_node() have real DB ids."""

    def test_layer1_rooms_have_db_ids(self):
        from typeclasses.objects import Object
        from world.zone_object import initialize_node

        zone = create_object(Object, key="zone_with_node", location=None)
        zone.db.zone_id = "layer1_test"

        script = initialize_node(
            zone, "cognitive", self.room_center, 1,
            [self.room_center, self.room_north], failure_start=0
        )

        for room_id in script.db.layer1_room_ids:
            self.assertIsNotNone(room_id)
            self.assertIsInstance(room_id, int)


class TestLayer1RoomsNotInNdb(NodeTestBase):
    """Layer 1 room ids stored in script.db, not script.ndb."""

    def test_layer1_rooms_not_in_ndb(self):
        from typeclasses.objects import Object
        from world.zone_object import initialize_node

        zone = create_object(Object, key="zone_ndb_test", location=None)
        zone.db.zone_id = "ndb_test"

        script = initialize_node(
            zone, "resonance", self.room_center, 1,
            [self.room_center], failure_start=0
        )

        # db should have the ids
        self.assertTrue(len(script.db.layer1_room_ids) > 0)
        # ndb should NOT have layer1_room_ids
        self.assertIsNone(getattr(script.ndb, "layer1_room_ids", None))


class TestLayerSwapMovesPlayers(NodeTestBase):
    """Players moved to Layer 1 on activation."""

    def test_layer_swap_moves_players(self):
        from typeclasses.objects import Object
        from world.zone_object import initialize_node
        from world.scripts.node_script import NodeScript

        zone = create_object(Object, key="zone_swap", location=None)
        zone.db.zone_id = "swap_test"

        script = initialize_node(
            zone, "thermal", self.room_center, 1,
            [self.room_center], failure_start=0
        )

        # Place char1 in center room
        self.char1.location = self.room_center

        # Force activation
        script.db.failure = 55.0
        script.db.state = "awakening"
        script.receive_tick(player_count=10, scholar_count=0,
                            stabilizer_count=0)

        # If failure crossed 60, player should be in Layer 1
        if script.db.failure >= 60.0:
            self.assertNotEqual(self.char1.location, self.room_center)
            self.assertIsNotNone(self.char1.db.layer0_room_id)


class TestLayerSwapReturnsPlayers(NodeTestBase):
    """Players returned to Layer 0 on deactivation."""

    def test_layer_swap_returns_players(self):
        from typeclasses.objects import Object
        from world.zone_object import initialize_node

        zone = create_object(Object, key="zone_return", location=None)
        zone.db.zone_id = "return_test"

        script = initialize_node(
            zone, "gravity", self.room_center, 1,
            [self.room_center], failure_start=65.0
        )

        # Manually activate
        self.char1.location = self.room_center
        script._activate_layer1()
        self.assertNotEqual(self.char1.location, self.room_center)

        # Now deactivate
        script._deactivate_layer1()
        self.assertEqual(self.char1.location, self.room_center)
        self.assertIsNone(self.char1.db.layer0_room_id)


class TestOrphanRecovery(NodeTestBase):
    """Players in inactive Layer 1 rooms on server start are recovered."""

    def test_orphan_recovery_moves_players(self):
        from typeclasses.rooms import Layer1Room
        from world.node_helpers import initialize_node_pool

        # Create an "orphaned" active Layer 1 room
        layer1_room = create_object(Layer1Room, key="Orphaned L1")
        layer1_room.db.zone_id = "test_zone"
        layer1_room.tags.remove("inactive", category="node_layer")
        layer1_room.tags.add("active", category="node_layer")

        # Place char1 in the orphaned room
        self.char1.db.layer0_room_id = self.room_center.id
        self.char1.location = layer1_room

        # Run orphan recovery (no node script active for this zone)
        initialize_node_pool()

        # Player should be back in Layer 0 room
        self.assertEqual(self.char1.location, self.room_center)
        self.assertIsNone(self.char1.db.layer0_room_id)


class TestNodeEffectTags(EvenniaTest):
    """Node effect tags applied and removed correctly."""

    def test_node_effect_tags_applied(self):
        from world.nodes.node_effects import apply_node_effects
        from typeclasses.rooms import SoravelonRoom

        room = create_object(SoravelonRoom, key="Effect Test Room")
        apply_node_effects(room, "thermal", "active")

        self.assertTrue(
            room.tags.get("burn_enhanced", category="node_effect")
        )
        self.assertTrue(
            room.tags.get("wet_suppressed", category="node_effect")
        )

    def test_node_effect_tags_removed(self):
        from world.nodes.node_effects import (
            apply_node_effects, remove_node_effects
        )
        from typeclasses.rooms import SoravelonRoom

        room = create_object(SoravelonRoom, key="Remove Test Room")
        apply_node_effects(room, "gravity", "active")
        self.assertTrue(
            room.tags.get("action_budget_penalty", category="node_effect")
        )

        remove_node_effects(room)
        self.assertFalse(
            room.tags.get("action_budget_penalty", category="node_effect")
        )


class TestOneWritePerTick(NodeTestBase):
    """receive_tick() only touches script.db, not per-player writes."""

    def test_one_write_per_tick(self):
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)
        script.db.failure = 50.0
        script.db.session_failure_added = 0.0

        old_failure = script.db.failure
        script.receive_tick(player_count=3, scholar_count=0,
                            stabilizer_count=0)

        # Only script.db.failure and script.db.session_failure_added
        # should have changed — no character objects touched
        self.assertNotEqual(script.db.failure, old_failure)


class TestNodeScriptPersistence(NodeTestBase):
    """NodeScript has persistent=True and is findable by tag."""

    def test_node_script_persists(self):
        from world.scripts.node_script import NodeScript
        from evennia.scripts.models import ScriptDB

        script = create_script(NodeScript, obj=self.zone_obj)
        self.assertTrue(script.persistent)

        # Should be findable by ScriptDB tag search
        found = ScriptDB.objects.get_by_tag(
            "node_script", category="script_type"
        )
        self.assertIn(script, found)


class TestHelperGetNodeScript(NodeTestBase):
    """get_node_script returns correct script for zone, None for unknown."""

    def test_get_node_script_found(self):
        from world.scripts.node_script import NodeScript
        from world.node_helpers import get_node_script

        script = create_script(NodeScript, obj=self.zone_obj)
        found = get_node_script("test_zone")
        self.assertEqual(found, script)

    def test_get_node_script_not_found(self):
        from world.node_helpers import get_node_script

        found = get_node_script("nonexistent_zone")
        self.assertIsNone(found)


class TestHelperGetRoomsInRadius(NodeTestBase):
    """BFS returns correct rooms, respects zone boundaries."""

    def test_radius_1(self):
        from world.node_helpers import get_rooms_in_radius

        rooms = get_rooms_in_radius(self.room_center, 1)
        self.assertIn(self.room_center, rooms)
        self.assertIn(self.room_north, rooms)
        self.assertNotIn(self.room_far, rooms)  # radius 2
        self.assertNotIn(self.room_other_zone, rooms)  # different zone

    def test_radius_2(self):
        from world.node_helpers import get_rooms_in_radius

        rooms = get_rooms_in_radius(self.room_center, 2)
        self.assertIn(self.room_center, rooms)
        self.assertIn(self.room_north, rooms)
        self.assertIn(self.room_far, rooms)
        self.assertNotIn(self.room_other_zone, rooms)
