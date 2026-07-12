"""
Tests for world/mob_spawner.py — spawn engine.

Uses unittest.TestCase + MagicMock throughout. Per-test sys.modules injection
for evennia and twisted to avoid DB/server dependencies.
The `world` package is real (evennia test loads it); only sub-dependencies
are mocked within setUp/tearDown to prevent leaking into other test modules.
"""

import sys
import types
import unittest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Stub classes (module-level definitions, but NOT injected into sys.modules
# at import time — injection happens only in setUp)
# ---------------------------------------------------------------------------

_MockSoravelonMob = type("SoravelonMob", (), {})
_MockSoravelonScript = type("SoravelonScript", (), {})
_MockPatrolScript = type("PatrolScript", (_MockSoravelonScript,), {})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_room(zone_id="zone_test", spawn_definitions=None):
    room = MagicMock()
    room.db.zone_id = zone_id
    room.db.spawn_definitions = spawn_definitions or []
    room.contents = []
    room.tags.get = MagicMock(return_value=None)
    return room


def _make_spawn_def(**overrides):
    base = {
        "mob": "wolf",
        "count_min": 1,
        "count_max": 3,
        "respawn_minutes": 15,
        "respawn_variance": 5,
        "base_disposition": 0.0,
        "trust_sensitive": False,
        "flee_threshold": 20,
        "is_named": False,
        "prestige_modifier": 1.0,
        "tome_drop": None,
        "spawn_condition": None,
        "sequence": [],
    }
    base.update(overrides)
    return base


def _make_mob(key="wolf", zone_id="zone_test"):
    mob = MagicMock()
    mob.key = key
    mob.db.zone_id = zone_id
    mob.db.mob_template_key = key
    mob.location = None
    mob.tags.get = MagicMock(return_value=None)
    mob.scripts = MagicMock()
    mob.__class__ = _MockSoravelonMob
    return mob


# Module keys that setUp injects and tearDown must restore
_STUB_KEYS = [
    "typeclasses", "typeclasses.mobs", "typeclasses.scripts",
    "world.scripts", "world.scripts.patrol_script", "evennia",
]


class _MobSpawnerTestBase(unittest.TestCase):
    """Base class that handles sys.modules injection/restoration."""

    def setUp(self):
        # Save originals for ALL keys we might touch
        self._saved_modules = {}
        for key in _STUB_KEYS:
            if key in sys.modules:
                self._saved_modules[key] = sys.modules[key]
            # else: key was absent, we'll pop it in tearDown

        # Build stub modules
        mobs_mod = types.ModuleType("typeclasses.mobs")
        mobs_mod.SoravelonMob = _MockSoravelonMob
        scripts_mod = types.ModuleType("typeclasses.scripts")
        scripts_mod.SoravelonScript = _MockSoravelonScript
        patrol_mod = types.ModuleType("world.scripts.patrol_script")
        patrol_mod.PatrolScript = _MockPatrolScript
        world_scripts_mod = types.ModuleType("world.scripts")

        # Inject stubs
        if "typeclasses" not in sys.modules:
            sys.modules["typeclasses"] = types.ModuleType("typeclasses")
        sys.modules["typeclasses.mobs"] = mobs_mod
        sys.modules["typeclasses.scripts"] = scripts_mod
        sys.modules["world.scripts"] = world_scripts_mod
        sys.modules["world.scripts.patrol_script"] = patrol_mod

        # Build evennia stub
        self.evennia_stub = MagicMock()
        self.evennia_stub.create_object = MagicMock(return_value=_make_mob())
        self.evennia_stub.search_tag = MagicMock(return_value=[])
        sys.modules["evennia"] = self.evennia_stub

        # Remove any cached mob_spawner so we import fresh
        for key in list(sys.modules.keys()):
            if "mob_spawner" in key:
                del sys.modules[key]

        import world.mob_spawner
        self.spawner = world.mob_spawner
        self.spawner.search_objects_by_exact_tag = MagicMock(return_value=[])

    def tearDown(self):
        # Remove cached mob_spawner
        for key in list(sys.modules.keys()):
            if "mob_spawner" in key:
                del sys.modules[key]

        # Restore original sys.modules state
        for key in _STUB_KEYS:
            if key in self._saved_modules:
                sys.modules[key] = self._saved_modules[key]
            else:
                sys.modules.pop(key, None)


# ---------------------------------------------------------------------------
# Tests: _count_room_mobs
# ---------------------------------------------------------------------------

class TestCountRoomMobs(_MobSpawnerTestBase):

    def setUp(self):
        super().setUp()
        self.mob = _make_mob()
        self.evennia_stub.create_object.return_value = self.mob

    def test_counts_matching_mobs_in_room(self):
        room = _make_room()
        mob1 = _make_mob(key="wolf")
        mob2 = _make_mob(key="wolf")
        mob3 = _make_mob(key="bear")
        room.contents = [mob1, mob2, mob3]
        spawn_def = _make_spawn_def(mob="wolf")

        count = self.spawner._count_room_mobs(room, spawn_def)
        self.assertEqual(count, 2)

    def test_returns_zero_when_no_matching_mobs(self):
        room = _make_room()
        room.contents = []
        spawn_def = _make_spawn_def(mob="wolf")
        count = self.spawner._count_room_mobs(room, spawn_def)
        self.assertEqual(count, 0)

    def test_named_mob_uses_search_tag(self):
        room = _make_room()
        mob_in_room = _make_mob(key="named_wolf")
        mob_in_room.location = room
        mob_elsewhere = _make_mob(key="named_wolf")
        mob_elsewhere.location = _make_room()

        self.spawner.search_objects_by_exact_tag = MagicMock(
            return_value=[mob_in_room, mob_elsewhere]
        )

        spawn_def = _make_spawn_def(mob="named_wolf", is_named=True)
        count = self.spawner._count_room_mobs(room, spawn_def)
        self.assertEqual(count, 1)
        self.spawner.search_objects_by_exact_tag.assert_called_with(
            "named_wolf",
            "mob_instance_id",
        )

    def test_counts_only_soravelon_mob_instances(self):
        """Non-mob objects in room contents are ignored."""
        room = _make_room()
        mob = _make_mob(key="wolf")
        non_mob = MagicMock()
        non_mob.__class__ = object  # not a SoravelonMob
        non_mob.key = "wolf"
        non_mob.db.mob_template_key = "wolf"
        room.contents = [mob, non_mob]

        spawn_def = _make_spawn_def(mob="wolf")
        count = self.spawner._count_room_mobs(room, spawn_def)
        self.assertEqual(count, 1)


# ---------------------------------------------------------------------------
# Tests: spawn_single_mob
# ---------------------------------------------------------------------------

class TestSpawnSingleMob(_MobSpawnerTestBase):

    def setUp(self):
        super().setUp()
        self.room = _make_room()
        self.spawn_def = _make_spawn_def(
            mob="wolf",
            base_disposition=-0.5,
            trust_sensitive=True,
            flee_threshold=25,
        )
        self.mob = _make_mob(key="wolf")
        self.evennia_stub.create_object.return_value = self.mob

    def test_creates_mob_with_correct_key_and_location(self):
        mob = self.spawner.spawn_single_mob(self.spawn_def, self.room)
        self.evennia_stub.create_object.assert_called_once()
        call_kwargs = self.evennia_stub.create_object.call_args
        self.assertEqual(call_kwargs[1]["key"], "wolf")
        self.assertIsNone(call_kwargs[1]["location"])
        self.assertEqual(mob.location, self.room)
        mob.move_to.assert_not_called()

    def test_sets_zone_id_from_room(self):
        mob = self.spawner.spawn_single_mob(self.spawn_def, self.room)
        self.assertEqual(mob.db.zone_id, self.room.db.zone_id)

    def test_sets_base_disposition_from_spawn_def(self):
        mob = self.spawner.spawn_single_mob(self.spawn_def, self.room)
        self.assertEqual(mob.db.base_disposition, -0.5)

    def test_sets_trust_sensitive_from_spawn_def(self):
        mob = self.spawner.spawn_single_mob(self.spawn_def, self.room)
        self.assertEqual(mob.db.trust_sensitive, True)

    def test_sets_flee_threshold_from_spawn_def(self):
        mob = self.spawner.spawn_single_mob(self.spawn_def, self.room)
        self.assertEqual(mob.db.flee_threshold, 25)

    def test_calls_initialize_for_spawn(self):
        mob = self.spawner.spawn_single_mob(self.spawn_def, self.room)
        mob.initialize_for_spawn.assert_called_once_with(self.room)

    def test_returns_mob_object(self):
        mob = self.spawner.spawn_single_mob(self.spawn_def, self.room)
        self.assertIs(mob, self.mob)


# ---------------------------------------------------------------------------
# Tests: spawn_named_mob
# ---------------------------------------------------------------------------

class TestSpawnNamedMob(_MobSpawnerTestBase):

    def setUp(self):
        super().setUp()
        self.room = _make_room()
        self.spawn_def = _make_spawn_def(
            mob="dire_wolf",
            is_named=True,
            prestige_modifier=1.5,
            tome_drop="tome_bestiary_wolf",
        )
        self.mob = _make_mob(key="dire_wolf")
        self.evennia_stub.create_object.return_value = self.mob

    def test_tags_mob_with_mob_instance_id_category(self):
        self.spawner.spawn_named_mob(self.spawn_def, self.room)
        self.mob.tags.add.assert_called_with("dire_wolf", category="mob_instance_id")

    def test_sets_prestige_modifier(self):
        self.spawner.spawn_named_mob(self.spawn_def, self.room)
        self.assertEqual(self.mob.db.prestige_modifier, 1.5)

    def test_sets_tome_drop(self):
        self.spawner.spawn_named_mob(self.spawn_def, self.room)
        self.assertEqual(self.mob.db.tome_drop, "tome_bestiary_wolf")

    def test_no_room_announce_on_first_spawn(self):
        self.spawner.spawn_named_mob(self.spawn_def, self.room, is_respawn=False)
        self.room.msg_contents.assert_not_called()

    def test_room_announce_on_respawn(self):
        self.spawner.spawn_named_mob(self.spawn_def, self.room, is_respawn=True)
        self.room.msg_contents.assert_called_once()
        announce = self.room.msg_contents.call_args[0][0]
        self.assertIn("dire_wolf", announce)

    def test_skips_spawn_when_condition_fails(self):
        self.spawn_def["spawn_condition"] = "node_failure_above_999"
        with patch.object(self.spawner, "_evaluate_spawn_condition", return_value=False):
            result = self.spawner.spawn_named_mob(self.spawn_def, self.room)
        self.assertIsNone(result)
        self.evennia_stub.create_object.assert_not_called()


# ---------------------------------------------------------------------------
# Tests: spawn_room_mobs — count management
# ---------------------------------------------------------------------------

class TestSpawnRoomMobs(_MobSpawnerTestBase):

    def setUp(self):
        super().setUp()
        self.new_mob = _make_mob(key="wolf")
        self.evennia_stub.create_object.return_value = self.new_mob

    def _setup_room(self, spawn_defs, existing_count=0):
        room = _make_room()
        room.db.spawn_definitions = spawn_defs
        room.contents = []
        for _ in range(existing_count):
            m = _make_mob(key="wolf")
            room.contents.append(m)
        return room

    def test_spawns_count_min_mobs_when_room_empty(self):
        spawn_def = _make_spawn_def(mob="wolf", count_min=2)
        room = self._setup_room([spawn_def], existing_count=0)
        spawned = self.spawner.spawn_room_mobs(room)
        self.assertEqual(spawned, 2)
        self.assertEqual(self.evennia_stub.create_object.call_count, 2)

    def test_does_not_spawn_when_count_already_at_min(self):
        spawn_def = _make_spawn_def(mob="wolf", count_min=2)
        room = self._setup_room([spawn_def], existing_count=2)
        spawned = self.spawner.spawn_room_mobs(room)
        self.assertEqual(spawned, 0)
        self.evennia_stub.create_object.assert_not_called()

    def test_spawns_only_needed_to_reach_count_min(self):
        spawn_def = _make_spawn_def(mob="wolf", count_min=2)
        room = self._setup_room([spawn_def], existing_count=1)
        spawned = self.spawner.spawn_room_mobs(room)
        self.assertEqual(spawned, 1)
        self.assertEqual(self.evennia_stub.create_object.call_count, 1)

    def test_returns_zero_for_empty_spawn_definitions(self):
        room = _make_room(spawn_definitions=[])
        spawned = self.spawner.spawn_room_mobs(room)
        self.assertEqual(spawned, 0)

    def test_skips_def_with_failing_spawn_condition(self):
        spawn_def = _make_spawn_def(
            mob="conditional_mob",
            count_min=1,
            spawn_condition="node_failure_above_999",
        )
        room = self._setup_room([spawn_def], existing_count=0)
        with patch.dict(sys.modules, {
            "world.node_helpers": MagicMock(get_node_script=MagicMock(return_value=None))
        }):
            # Re-import with patched node_helpers
            for key in list(sys.modules.keys()):
                if "mob_spawner" in key:
                    del sys.modules[key]
            import world.mob_spawner as spawner
            spawned = spawner.spawn_room_mobs(room)
        self.assertEqual(spawned, 0)
        self.evennia_stub.create_object.assert_not_called()


# ---------------------------------------------------------------------------
# Tests: spawn_zone
# ---------------------------------------------------------------------------

class TestSpawnZone(_MobSpawnerTestBase):

    def test_calls_spawn_room_mobs_for_each_room(self):
        zone_obj = MagicMock()
        zone_obj.db.zone_id = "zone_01"
        zone_obj.tags.get = MagicMock(side_effect=lambda t, category=None: t == "zone_object")
        zone_obj.db.spawn_definitions = None

        room1 = _make_room(zone_id="zone_01", spawn_definitions=[_make_spawn_def(mob="wolf")])
        room2 = _make_room(zone_id="zone_01", spawn_definitions=[_make_spawn_def(mob="bear")])

        def _search_tag_side_effect(tag, category=None):
            if category == "zone_id":
                return [room1, room2, zone_obj]
            return []

        self.spawner.search_objects_by_exact_tag = MagicMock(
            side_effect=_search_tag_side_effect
        )

        total = self.spawner.spawn_zone(zone_obj)
        self.assertEqual(total, 2)

    def test_excludes_zone_obj_itself(self):
        """zone_obj (tagged zone_object) must not be passed to spawn_room_mobs."""
        zone_obj = MagicMock()
        zone_obj.db.zone_id = "zone_02"
        zone_obj.tags.get = MagicMock(side_effect=lambda t, category=None: t == "zone_object")
        zone_obj.db.spawn_definitions = [_make_spawn_def(mob="wolf", count_min=5)]

        self.spawner.search_objects_by_exact_tag = MagicMock(return_value=[zone_obj])
        total = self.spawner.spawn_zone(zone_obj)
        self.assertEqual(total, 0)


# ---------------------------------------------------------------------------
# Tests: _maybe_attach_patrol
# ---------------------------------------------------------------------------

class TestMaybeAttachPatrol(_MobSpawnerTestBase):

    def test_does_nothing_when_no_zone_obj(self):
        with patch("world.zone_scaling.get_zone_obj_for_room", return_value=None):
            for key in list(sys.modules.keys()):
                if "mob_spawner" in key:
                    del sys.modules[key]
            import world.mob_spawner as spawner
            mob = _make_mob()
            spawn_def = _make_spawn_def(mob="wolf")
            room = _make_room()
            spawner._maybe_attach_patrol(mob, spawn_def, room)
            mob.scripts.add.assert_not_called()

    def test_does_nothing_when_no_patrol_definitions(self):
        zone_obj = MagicMock()
        zone_obj.db.patrol_definitions = None
        with patch("world.zone_scaling.get_zone_obj_for_room", return_value=zone_obj):
            for key in list(sys.modules.keys()):
                if "mob_spawner" in key:
                    del sys.modules[key]
            import world.mob_spawner as spawner
            mob = _make_mob()
            spawn_def = _make_spawn_def(mob="wolf")
            room = _make_room()
            spawner._maybe_attach_patrol(mob, spawn_def, room)
            mob.scripts.add.assert_not_called()

    def test_does_nothing_when_no_matching_patrol_def(self):
        zone_obj = MagicMock()
        zone_obj.db.patrol_definitions = [
            {"mob_key": "bear", "route_room_ids": ["room_01"]}
        ]
        with patch("world.zone_scaling.get_zone_obj_for_room", return_value=zone_obj):
            for key in list(sys.modules.keys()):
                if "mob_spawner" in key:
                    del sys.modules[key]
            import world.mob_spawner as spawner
            mob = _make_mob()
            spawn_def = _make_spawn_def(mob="wolf")
            room = _make_room()
            spawner._maybe_attach_patrol(mob, spawn_def, room)
            mob.scripts.add.assert_not_called()

    def test_attaches_patrol_script_when_matching_patrol_def_found(self):
        zone_obj = MagicMock()
        patrol_def = {
            "mob_key": "wolf",
            "route_room_ids": ["room_01", "room_02"],
            "interrupt_mode": "resume",
            "encounter_delay": 0,
            "echo_radius": 0,
            "move_echo": "A wolf prowls by.",
            "combat_enabled": True,
        }
        zone_obj.db.patrol_definitions = [patrol_def]

        room_obj_1 = MagicMock()
        room_obj_1.id = 101
        room_obj_1.db.zone_id = "zone_test"

        room_obj_2 = MagicMock()
        room_obj_2.id = 102
        room_obj_2.db.zone_id = "zone_test"

        def _search_tag_for_route(tag, category=None):
            if tag == "room_01" and category == "room_id":
                return [room_obj_1]
            if tag == "room_02" and category == "room_id":
                return [room_obj_2]
            return []

        self.spawner.search_objects_by_exact_tag = MagicMock(
            side_effect=_search_tag_for_route
        )

        mock_script = MagicMock()
        mob = _make_mob()
        mob.scripts.get = MagicMock(return_value=[mock_script])
        spawn_def = _make_spawn_def(mob="wolf")
        room = _make_room(zone_id="zone_test")

        with patch("world.zone_scaling.get_zone_obj_for_room", return_value=zone_obj):
            for key in list(sys.modules.keys()):
                if "mob_spawner" in key:
                    del sys.modules[key]
            sys.modules["evennia"] = self.evennia_stub
            import world.mob_spawner as spawner
            spawner.search_objects_by_exact_tag = MagicMock(
                side_effect=_search_tag_for_route
            )
            spawner._maybe_attach_patrol(mob, spawn_def, room)

        mob.scripts.add.assert_called_once()
        self.assertEqual(mock_script.db.route_ids, [101, 102])
        self.assertEqual(mock_script.db.patrol_def, patrol_def)


# ---------------------------------------------------------------------------
# Tests: _schedule_respawn
# ---------------------------------------------------------------------------

class TestScheduleRespawn(_MobSpawnerTestBase):

    def setUp(self):
        super().setUp()
        self.room = _make_room()
        self.new_mob = _make_mob()
        self.evennia_stub.create_object.return_value = self.new_mob

    def test_calls_call_later_with_valid_delay(self):
        spawn_def = _make_spawn_def(mob="wolf", respawn_minutes=10, respawn_variance=0)
        self.room.contents = []

        mock_reactor = MagicMock()
        with patch.object(self.spawner, "_get_reactor", return_value=mock_reactor):
            self.spawner._schedule_respawn(spawn_def, self.room)

        mock_reactor.callLater.assert_called_once()
        delay_arg = mock_reactor.callLater.call_args[0][0]
        self.assertGreaterEqual(delay_arg, 30)
        self.assertAlmostEqual(delay_arg, 600.0, delta=1.0)

    def test_respawn_callback_skips_when_at_count_max(self):
        """If count is already at count_max, callback should not spawn."""
        spawn_def = _make_spawn_def(mob="wolf", count_min=1, count_max=2)
        mob1 = _make_mob(key="wolf")
        mob2 = _make_mob(key="wolf")
        self.room.contents = [mob1, mob2]

        captured = {}

        def capture_call_later(delay, fn):
            captured["fn"] = fn

        mock_reactor = MagicMock()
        mock_reactor.callLater = MagicMock(side_effect=capture_call_later)
        with patch.object(self.spawner, "_get_reactor", return_value=mock_reactor):
            self.spawner._schedule_respawn(spawn_def, self.room)

        self.evennia_stub.create_object.reset_mock()
        captured["fn"]()
        self.evennia_stub.create_object.assert_not_called()

    def test_respawn_callback_spawns_when_below_count_max(self):
        """Respawn callback fires spawn_single_mob when below count_max."""
        spawn_def = _make_spawn_def(mob="wolf", count_min=1, count_max=2)
        self.room.contents = []

        captured = {}

        def capture_call_later(delay, fn):
            captured["fn"] = fn

        mock_reactor = MagicMock()
        mock_reactor.callLater = MagicMock(side_effect=capture_call_later)
        with patch.object(self.spawner, "_get_reactor", return_value=mock_reactor):
            self.spawner._schedule_respawn(spawn_def, self.room)

        self.evennia_stub.create_object.reset_mock()
        captured["fn"]()
        self.evennia_stub.create_object.assert_called_once()


# ---------------------------------------------------------------------------
# Tests: _evaluate_spawn_condition
# ---------------------------------------------------------------------------

class TestEvaluateSpawnCondition(_MobSpawnerTestBase):

    def test_none_condition_always_returns_true(self):
        room = _make_room()
        self.assertTrue(self.spawner._evaluate_spawn_condition(None, room))

    def test_empty_string_returns_true(self):
        room = _make_room()
        self.assertTrue(self.spawner._evaluate_spawn_condition("", room))

    def test_node_failure_above_threshold_false_when_no_script(self):
        with patch("world.node_helpers.get_node_script", return_value=None):
            for key in list(sys.modules.keys()):
                if "mob_spawner" in key:
                    del sys.modules[key]
            import world.mob_spawner as spawner
            room = _make_room(zone_id="zone_a")
            self.assertFalse(spawner._evaluate_spawn_condition("node_failure_above_50", room))

    def test_node_failure_above_threshold_true_when_met(self):
        mock_script = MagicMock()
        mock_script.db.failure = 75
        with patch("world.node_helpers.get_node_script", return_value=mock_script):
            for key in list(sys.modules.keys()):
                if "mob_spawner" in key:
                    del sys.modules[key]
            import world.mob_spawner as spawner
            room = _make_room(zone_id="zone_a")
            self.assertTrue(spawner._evaluate_spawn_condition("node_failure_above_50", room))

    def test_node_failure_above_threshold_false_when_below(self):
        mock_script = MagicMock()
        mock_script.db.failure = 30
        with patch("world.node_helpers.get_node_script", return_value=mock_script):
            for key in list(sys.modules.keys()):
                if "mob_spawner" in key:
                    del sys.modules[key]
            import world.mob_spawner as spawner
            room = _make_room(zone_id="zone_a")
            self.assertFalse(spawner._evaluate_spawn_condition("node_failure_above_50", room))

    def test_node_active_true_when_active(self):
        mock_script = MagicMock()
        mock_script.db.state = "active"
        with patch("world.node_helpers.get_node_script", return_value=mock_script):
            for key in list(sys.modules.keys()):
                if "mob_spawner" in key:
                    del sys.modules[key]
            import world.mob_spawner as spawner
            room = _make_room(zone_id="zone_a")
            self.assertTrue(spawner._evaluate_spawn_condition("node_active", room))

    def test_node_active_false_when_dormant(self):
        mock_script = MagicMock()
        mock_script.db.state = "dormant"
        with patch("world.node_helpers.get_node_script", return_value=mock_script):
            for key in list(sys.modules.keys()):
                if "mob_spawner" in key:
                    del sys.modules[key]
            import world.mob_spawner as spawner
            room = _make_room(zone_id="zone_a")
            self.assertFalse(spawner._evaluate_spawn_condition("node_active", room))

    def test_quest_complete_condition_fails_closed(self):
        room = _make_room()
        self.assertFalse(self.spawner._evaluate_spawn_condition("quest_complete:some_quest", room))

    def test_time_of_day_condition_fails_closed(self):
        room = _make_room()
        self.assertFalse(self.spawner._evaluate_spawn_condition("time_of_day:night", room))

    def test_unknown_condition_fails_closed(self):
        room = _make_room()
        self.assertFalse(self.spawner._evaluate_spawn_condition("totally_unknown_condition_xyz", room))


if __name__ == "__main__":
    unittest.main()
