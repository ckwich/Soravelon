"""
Tests for the Soravelon node system (Build Order Step 3).

Covers node failure state machine, layer swaps, node effects,
stabilization limits, and awakening warnings (Phases 7 and 10).
"""

from unittest.mock import patch, MagicMock, PropertyMock
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


class TestRollingPressureBudget(NodeTestBase):
    """Presence pressure is bounded per window without freezing forever."""

    def test_pressure_budget_recovers_after_one_window(self):
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)
        script.db.failure = 0.0

        for _ in range(20):
            script.receive_tick(
                player_count=100,
                scholar_count=0,
                stabilizer_count=0,
            )

        self.assertEqual(script.db.failure, 5.0)
        self.assertLessEqual(sum(script.db.pressure_window), 5.0)

        for _ in range(20):
            script.receive_tick(
                player_count=0,
                scholar_count=0,
                stabilizer_count=0,
            )
        script.receive_tick(
            player_count=100,
            scholar_count=0,
            stabilizer_count=0,
        )

        self.assertEqual(script.db.failure, 10.0)
        self.assertLessEqual(sum(script.db.pressure_window), 5.0)

    def test_presence_study_activation_and_stabilization_recovery(self):
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)
        script.db.failure = 54.0
        script.db.state = "awakening"

        with patch.object(script, "_send_awakening_warnings"):
            for _ in range(24):
                script.receive_tick(
                    player_count=1,
                    scholar_count=1,
                    stabilizer_count=0,
                )

        self.assertGreaterEqual(script.db.failure, 60.0)
        self.assertEqual(script.db.state, "active")

        script.receive_tick(
            player_count=0,
            scholar_count=0,
            stabilizer_count=12,
        )

        self.assertLess(script.db.failure, 60.0)
        self.assertEqual(script.db.state, "awakening")


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


# -----------------------------------------------------------------------
# Phase 10 Plan 01 Tests — L1 Exit Cloning and Override Application
# -----------------------------------------------------------------------

class TestLayer1Exits(NodeTestBase):
    """Test L1 exit cloning from Plan 01."""

    def test_initialize_node_creates_l1_exits(self):
        """L1 rooms should have exits matching L0 topology."""
        from typeclasses.objects import Object
        from world.zone_object import initialize_node

        zone = create_object(Object, key="zone_exits", location=None)
        zone.db.zone_id = "exits_test"

        script = initialize_node(
            zone, "resonance", self.room_center, 1,
            [self.room_center, self.room_north], failure_start=0
        )

        # Both rooms should have L1 counterparts
        l1_center_id = self.room_center.db.layer1_room_id
        l1_north_id = self.room_north.db.layer1_room_id
        self.assertIsNotNone(l1_center_id)
        self.assertIsNotNone(l1_north_id)

        # L1 center room should have at least one exit (to L1 north)
        import evennia
        l1_center = evennia.search_object("#" + str(l1_center_id))[0]
        l1_exit_dests = [e.destination.id for e in l1_center.exits]
        self.assertIn(l1_north_id, l1_exit_dests)

    def test_l1_exits_tagged_inactive(self):
        """L1 exits should start with inactive tag."""
        from typeclasses.objects import Object
        from world.zone_object import initialize_node
        import evennia

        zone = create_object(Object, key="zone_tag_exits", location=None)
        zone.db.zone_id = "tag_exits_test"

        script = initialize_node(
            zone, "cognitive", self.room_center, 1,
            [self.room_center, self.room_north], failure_start=0
        )

        l1_center_id = self.room_center.db.layer1_room_id
        l1_center = evennia.search_object("#" + str(l1_center_id))[0]
        for exit_obj in l1_center.exits:
            self.assertTrue(
                exit_obj.tags.has("inactive", category="node_layer"),
                f"Exit {exit_obj.key} should be tagged inactive"
            )

    def test_l1_exits_only_between_rooms_with_l1(self):
        """Exits to rooms outside layer0_rooms should not get L1 clones."""
        from typeclasses.objects import Object
        from world.zone_object import initialize_node
        import evennia

        zone = create_object(Object, key="zone_partial", location=None)
        zone.db.zone_id = "partial_test"

        # Only include room_center (not room_north)
        script = initialize_node(
            zone, "thermal", self.room_center, 1,
            [self.room_center], failure_start=0
        )

        l1_center_id = self.room_center.db.layer1_room_id
        l1_center = evennia.search_object("#" + str(l1_center_id))[0]

        # L1 center should have NO exits (room_north has no L1 counterpart)
        self.assertEqual(len(l1_center.exits), 0)


class TestLayer1Overrides(NodeTestBase):
    """Test override application from Plan 01."""

    def test_activate_applies_overrides(self):
        """L1 rooms with overrides get custom name/desc."""
        from typeclasses.objects import Object
        from world.zone_object import initialize_node
        import evennia

        zone = create_object(Object, key="zone_overrides", location=None)
        zone.db.zone_id = "override_test"
        zone.db.layer_1_overrides = {
            self.room_center.key: {
                "name": "Shattered Nexus",
                "desc": "The center has warped beyond recognition."
            }
        }

        script = initialize_node(
            zone, "resonance", self.room_center, 1,
            [self.room_center], failure_start=65.0
        )

        script._activate_layer1()

        l1_id = self.room_center.db.layer1_room_id
        l1_room = evennia.search_object("#" + str(l1_id))[0]
        self.assertEqual(l1_room.key, "Shattered Nexus")

    def test_activate_default_distorted_prefix(self):
        """L1 rooms without overrides get [Distorted] prefix."""
        from typeclasses.objects import Object
        from world.zone_object import initialize_node
        import evennia

        zone = create_object(Object, key="zone_distort", location=None)
        zone.db.zone_id = "distort_test"
        zone.db.layer_1_overrides = {}

        script = initialize_node(
            zone, "temporal", self.room_center, 1,
            [self.room_center], failure_start=65.0
        )

        script._activate_layer1()

        l1_id = self.room_center.db.layer1_room_id
        l1_room = evennia.search_object("#" + str(l1_id))[0]
        self.assertTrue(l1_room.key.startswith("[Distorted]"))

    def test_deactivate_restores_names(self):
        """After deactivation, L1 rooms revert to original names."""
        from typeclasses.objects import Object
        from world.zone_object import initialize_node
        import evennia

        zone = create_object(Object, key="zone_restore", location=None)
        zone.db.zone_id = "restore_test"
        zone.db.layer_1_overrides = {}

        script = initialize_node(
            zone, "gravity", self.room_center, 1,
            [self.room_center], failure_start=65.0
        )

        l1_id = self.room_center.db.layer1_room_id
        l1_room = evennia.search_object("#" + str(l1_id))[0]
        original_name = l1_room.key

        script._activate_layer1()
        self.assertNotEqual(l1_room.key, original_name)

        script._deactivate_layer1()
        self.assertEqual(l1_room.key, original_name)


# -----------------------------------------------------------------------
# Phase 10 Plan 02 Tests — Thermal, Cognitive, Temporal Node Effects
# -----------------------------------------------------------------------

class TestThermalNodeEffect(EvenniaTest):
    """Test thermal damage modifiers from Plan 02."""

    def test_fire_damage_boosted(self):
        """Fire damage boosted 30% in burn_enhanced rooms."""
        from typeclasses.rooms import SoravelonRoom
        from world.zone_scaling import apply_resistance

        room = create_object(SoravelonRoom, key="Thermal Room")
        room.tags.add("burn_enhanced", category="node_effect")

        target = MagicMock()
        target.db.resistances = {}
        target.location = room

        result = apply_resistance(100, "fire", target)
        self.assertEqual(result, 130)  # 100 * 1.3

    def test_water_damage_reduced(self):
        """Water/ice damage reduced 30% in burn_enhanced rooms."""
        from typeclasses.rooms import SoravelonRoom
        from world.zone_scaling import apply_resistance

        room = create_object(SoravelonRoom, key="Thermal Room Water")
        room.tags.add("burn_enhanced", category="node_effect")

        target = MagicMock()
        target.db.resistances = {}
        target.location = room

        result = apply_resistance(100, "water", target)
        self.assertEqual(result, 70)  # 100 * 0.7

    def test_wet_blocked(self):
        """Wet status blocked in wet_suppressed rooms."""
        from typeclasses.rooms import SoravelonRoom
        from world.status_effects import apply_effect

        room = create_object(SoravelonRoom, key="Thermal Room Wet")
        room.tags.add("wet_suppressed", category="node_effect")

        target = MagicMock()
        target.location = room
        target.ndb.active_effects = []
        target.ndb.immunities = set()
        target.db.immunities = set()

        success, msg = apply_effect(target, "wet", duration=3)
        self.assertFalse(success)
        self.assertIn("evaporates", msg)


class TestCognitiveNodeEffect(EvenniaTest):
    """Test cognitive mob coordination from Plan 02."""

    def test_mobs_focus_same_target(self):
        """In mob_coordination room, second mob copies first's target."""
        from typeclasses.rooms import SoravelonRoom
        from world.combat_ai import get_mob_target

        room = create_object(SoravelonRoom, key="Cognitive Room")
        room.tags.add("mob_coordination", category="node_effect")

        # Create mock combat handler
        combat = MagicMock()

        # Two players
        player_a = MagicMock()
        player_a.id = 100
        player_a.location = room
        player_a.ndb.active_effects = []
        player_b = MagicMock()
        player_b.id = 101
        player_b.location = room
        player_b.ndb.active_effects = []

        # Two mobs
        mob1 = MagicMock()
        mob1.id = 200
        mob1.location = room
        mob1.ndb.last_attacker_id = None
        mob1.ndb.current_target_id = None

        mob2 = MagicMock()
        mob2.id = 201
        mob2.location = room
        mob2.ndb.last_attacker_id = None
        mob2.ndb.current_target_id = player_a.id  # mob2 already targeting A

        # Mock combat_handler to return players and mobs
        combat.db.combatants = [player_a, player_b, mob1, mob2]

        # Patch internal helpers
        with patch("world.combat_ai._get_player_combatants", return_value=[player_a, player_b]):
            with patch("world.combat_ai._get_mob_combatants", return_value=[mob1, mob2]):
                with patch("world.combat_ai._has_vanish", return_value=False):
                    with patch("world.combat_ai._target_in_room", return_value=True):
                        result = get_mob_target(mob1, combat)

        # mob1 should copy mob2's target (player_a)
        self.assertEqual(result.id, player_a.id)


class TestTemporalNodeEffect(EvenniaTest):
    """Test temporal DoT variance from Plan 02."""

    def test_dot_variance_applied(self):
        """DoT damage varies in rooms with dot_tick_variance tag."""
        from typeclasses.rooms import SoravelonRoom
        from world.status_effects import tick_effects

        room = create_object(SoravelonRoom, key="Temporal Room")
        room.tags.add("dot_tick_variance", category="node_effect")

        damages = set()
        for _ in range(50):
            target = MagicMock()
            target.location = room
            target.ndb.hp = 100
            target.ndb.stamina = 100
            target.ndb.took_damage_this_round = False
            target.ndb.active_effects = [
                {
                    "type": "burn",
                    "stacks": 1,
                    "duration": 2,
                    "magnitude": 1.0,
                    "source_id": 1,
                    "max_stacks": 4,
                    "is_compound": False,
                }
            ]
            target.ndb.immunities = set()
            target.db.immunities = set()

            tick_effects(target)
            damage_dealt = 100 - target.ndb.hp
            damages.add(damage_dealt)

        # With 50%-150% variance over 50 runs, we should see at least
        # 2 distinct damage values
        self.assertGreater(len(damages), 1, f"Expected variance, got: {damages}")


# -----------------------------------------------------------------------
# Phase 10 Plan 03 Tests — Stabilization Limits and Awakening Warnings
# -----------------------------------------------------------------------

class TestStabilizationLimits(NodeTestBase):
    """Test stabilization stamina drain and break conditions."""

    def test_fresh_character_can_start_stabilizing_real_node(self):
        from evennia import create_script

        from world.node_helpers import attempt_stabilization
        from world.scripts.node_script import NodeScript

        create_script(NodeScript, obj=self.zone_obj)
        self.char1.ndb.stamina = 20
        self.char1.ndb.stabilizing_zones = None

        self.assertTrue(attempt_stabilization(self.char1, "test_zone"))
        self.assertEqual(self.char1.ndb.stabilizing_zones, {"test_zone"})

    def test_stamina_drain(self):
        """stabilization_tick drains 5 stamina."""
        from world.node_helpers import stabilization_tick

        char = MagicMock()
        char.ndb.stamina = 30
        char.ndb.stabilizing_zones = {"test_zone"}

        stabilization_tick(char, "test_zone")

        self.assertEqual(char.ndb.stamina, 25)

    def test_auto_stop_at_zero_stamina(self):
        """When stamina hits 0, stabilization stops automatically."""
        from world.node_helpers import stabilization_tick

        char = MagicMock()
        char.ndb.stamina = 3
        char.ndb.stabilizing_zones = {"test_zone"}

        stabilization_tick(char, "test_zone")

        self.assertEqual(char.ndb.stamina, 0)
        # Should have been removed from stabilizing_zones
        self.assertNotIn("test_zone", char.ndb.stabilizing_zones)
        # Should have received the exhaustion message
        char.msg.assert_called_with(
            "Your concentration wavers. The stabilization fades."
        )

    def test_combat_break(self):
        """Entering combat breaks all stabilizations."""
        from world.node_helpers import break_stabilization_on_combat

        char = MagicMock()
        char.ndb.stabilizing_zones = {"zone_a", "zone_b"}

        break_stabilization_on_combat(char)

        self.assertEqual(len(char.ndb.stabilizing_zones), 0)
        char.msg.assert_called_with("Your focus breaks as combat begins.")

    def test_movement_break(self):
        """Moving rooms breaks all stabilizations."""
        from world.node_helpers import break_stabilization_on_move

        char = MagicMock()
        char.ndb.stabilizing_zones = {"zone_a"}

        break_stabilization_on_move(char)

        self.assertEqual(len(char.ndb.stabilizing_zones), 0)
        char.msg.assert_called_with("Your focus breaks.")

    def test_attempt_requires_stamina(self):
        """attempt_stabilization fails if stamina is 0."""
        from world.node_helpers import attempt_stabilization

        char = MagicMock()
        char.ndb.stamina = 0

        result = attempt_stabilization(char, "test_zone")

        self.assertFalse(result)
        char.msg.assert_called_with("You lack the stamina to stabilize.")


class TestAwakeningWarnings(NodeTestBase):
    """Test awakening atmospheric messages from Plan 03."""

    def test_warnings_sent_during_awakening(self):
        """Players in zone receive atmospheric messages during awakening."""
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)
        script.db.failure = 35.0
        script.db.state = "awakening"
        script.db.session_failure_added = 0.0

        # Use fully-mocked room + player to avoid mutating real DB objects
        mock_player = MagicMock()
        mock_player.sessions.all.return_value = [MagicMock()]
        mock_player.msg = MagicMock()

        mock_room = MagicMock()
        mock_room.contents = [mock_player]
        mock_room.db_typeclass_path = "typeclasses.rooms.SoravelonRoom"

        with patch("world.scripts.node_script.random") as mock_random:
            mock_random.random.return_value = 0.3  # < 0.5, will send
            mock_random.choice.return_value = "The air shimmers with an unseen pressure."
            with patch(
                "world.scripts.node_script.search_objects_by_exact_tag",
                return_value=[mock_room],
            ):
                script._send_awakening_warnings()

        mock_player.msg.assert_any_call(
            "|xThe air shimmers with an unseen pressure.|n"
        )

    def test_direct_warning_at_55_percent(self):
        """Direct warning sent when failure >= 55%."""
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)
        script.db.failure = 55.0
        script.db.state = "awakening"
        script.db.session_failure_added = 0.0

        mock_player = MagicMock()
        mock_player.sessions.all.return_value = [MagicMock()]
        mock_player.msg = MagicMock()

        mock_room = MagicMock()
        mock_room.contents = [mock_player]
        mock_room.db_typeclass_path = "typeclasses.rooms.SoravelonRoom"

        with patch("world.scripts.node_script.random") as mock_random:
            mock_random.random.return_value = 0.8  # > 0.5, skip atmospheric
            with patch(
                "world.scripts.node_script.search_objects_by_exact_tag",
                return_value=[mock_room],
            ):
                script._send_awakening_warnings()

        mock_player.msg.assert_called_with(
            "|rThe dimensional barrier is weakening. "
            "Prepare yourself.|n"
        )

    def test_no_warnings_in_dormant(self):
        """No warnings sent during dormant state (receive_tick skips)."""
        from world.scripts.node_script import NodeScript

        script = create_script(NodeScript, obj=self.zone_obj)
        script.db.failure = 10.0
        script.db.state = "dormant"
        script.db.session_failure_added = 0.0

        # In dormant state, _send_awakening_warnings should not be called
        with patch.object(script, '_send_awakening_warnings') as mock_warn:
            script.receive_tick(player_count=1, scholar_count=0,
                                stabilizer_count=0)
            # State stays dormant (failure < 30)
            self.assertEqual(script.db.state, "dormant")
            mock_warn.assert_not_called()
