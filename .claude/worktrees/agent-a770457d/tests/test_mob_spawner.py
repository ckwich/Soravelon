"""
Tests for world/mob_spawner.py — spawn engine.

Uses unittest.TestCase + MagicMock throughout. Per-test sys.modules injection
for evennia and twisted to avoid DB/server dependencies.
The `world` package is real (pytest loads it); only sub-dependencies are mocked.
"""

import sys
import types
import unittest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Module-level stubs for deps that can't be imported cleanly in plain pytest
# ---------------------------------------------------------------------------

# Stub typeclasses hierarchy
_MockSoravelonMob = type("SoravelonMob", (), {})
_mobs_mod = types.ModuleType("typeclasses.mobs")
_mobs_mod.SoravelonMob = _MockSoravelonMob

_MockSoravelonScript = type("SoravelonScript", (), {})
_scripts_tc_mod = types.ModuleType("typeclasses.scripts")
_scripts_tc_mod.SoravelonScript = _MockSoravelonScript

_MockPatrolScript = type("PatrolScript", (_MockSoravelonScript,), {})
_patrol_script_mod = types.ModuleType("world.scripts.patrol_script")
_patrol_script_mod.PatrolScript = _MockPatrolScript

_world_scripts_mod = types.ModuleType("world.scripts")

if "typeclasses" not in sys.modules:
    sys.modules["typeclasses"] = types.ModuleType("typeclasses")
if "typeclasses.mobs" not in sys.modules:
    sys.modules["typeclasses.mobs"] = _mobs_mod
if "typeclasses.scripts" not in sys.modules:
    sys.modules["typeclasses.scripts"] = _scripts_tc_mod
if "world.scripts" not in sys.modules:
    sys.modules["world.scripts"] = _world_scripts_mod
if "world.scripts.patrol_script" not in sys.modules:
    sys.modules["world.scripts.patrol_script"] = _patrol_script_mod


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
    mob.location = None
    mob.tags.get = MagicMock(return_value=None)
    mob.scripts = MagicMock()
    mob.__class__ = _MockSoravelonMob
    return mob


def _setup_evennia_stub(create_result=None):
    """Create and inject a fresh evennia stub. Returns the stub."""
    stub = MagicMock()
    stub.create_object = MagicMock(return_value=create_result or _make_mob())
    stub.search_tag = MagicMock(return_value=[])
    sys.modules["evennia"] = stub
    return stub


def _reload_mob_spawner():
    """Remove cached mob_spawner and re-import it."""
    for key in list(sys.modules.keys()):
        if "mob_spawner" in key:
            del sys.modules[key]
    import world.mob_spawner
    return world.mob_spawner


# ---------------------------------------------------------------------------
# Tests: _count_room_mobs
# ---------------------------------------------------------------------------

class TestCountRoomMobs(unittest.TestCase):

    def setUp(self):
        self.mob = _make_mob()
        self.evennia_stub = _setup_evennia_stub(create_result=self.mob)
        self.spawner = _reload_mob_spawner()

    def tearDown(self):
        for key in list(sys.modules.keys()):
            if "mob_spawner" in key:
                del sys.modules[key]

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

        self.evennia_stub.search_tag = MagicMock(return_value=[mob_in_room, mob_elsewhere])

        spawn_def = _make_spawn_def(mob="named_wolf", is_named=True)
        count = self.spawner._count_room_mobs(room, spawn_def)
        self.assertEqual(count, 1)
        self.evennia_stub.search_tag.assert_called_with("named_wolf", category="mob_id")

    def test_counts_only_soravelon_mob_instances(self):
        """Non-mob objects in room contents are ignored."""
        room = _make_room()
        mob = _make_mob(key="wolf")
        non_mob = MagicMock()
        non_mob.__class__ = object  # not a SoravelonMob
        non_mob.key = "wolf"
        room.contents = [mob, non_mob]

        spawn_def = _make_spawn_def(mob="wolf")
        count = self.spawner._count_room_mobs(room, spawn_def)
        self.assertEqual(count, 1)


# ---------------------------------------------------------------------------
# Tests: spawn_single_mob
# ---------------------------------------------------------------------------

class TestSpawnSingleMob(unittest.TestCase):

    def setUp(self):
        self.room = _make_room()
        self.spawn_def = _make_spawn_def(
            mob="wolf",
            base_disposition=-0.5,
            trust_sensitive=True,
            flee_threshold=25,
        )
        self.mob = _make_mob(key="wolf")
        self.evennia_stub = _setup_evennia_stub(create_result=self.mob)
        self.spawner = _reload_mob_spawner()

    def tearDown(self):
        for key in list(sys.modules.keys()):
            if "mob_spawner" in key:
                del sys.modules[key]

    def test_creates_mob_with_correct_key_and_location(self):
        mob = self.spawner.spawn_single_mob(self.spawn_def, self.room)
        self.evennia_stub.create_object.assert_called_once()
        call_kwargs = self.evennia_stub.create_object.call_args
        self.assertEqual(call_kwargs[1]["key"], "wolf")
        self.assertEqual(call_kwargs[1]["location"], self.room)

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

class TestSpawnNamedMob(unittest.TestCase):

    def setUp(self):
        self.room = _make_room()
        self.spawn_def = _make_spawn_def(
            mob="dire_wolf",
            is_named=True,
            prestige_modifier=1.5,
            tome_drop="tome_bestiary_wolf",
        )
        self.mob = _make_mob(key="dire_wolf")
        self.evennia_stub = _setup_evennia_stub(create_result=self.mob)
        self.spawner = _reload_mob_spawner()

    def tearDown(self):
        for key in list(sys.modules.keys()):
            if "mob_spawner" in key:
                del sys.modules[key]

    def test_tags_mob_with_mob_id_category(self):
        self.spawner.spawn_named_mob(self.spawn_def, self.room)
        self.mob.tags.add.assert_called_with("dire_wolf", category="mob_id")

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
        # Patch get_node_script inside mob_spawner module to return None
        with patch.object(self.spawner, "_evaluate_spawn_condition", return_value=False):
            result = self.spawner.spawn_named_mob(self.spawn_def, self.room)
        self.assertIsNone(result)
        self.evennia_stub.create_object.assert_not_called()


# ---------------------------------------------------------------------------
# Tests: spawn_room_mobs — count management
# ---------------------------------------------------------------------------

class TestSpawnRoomMobs(unittest.TestCase):

    def setUp(self):
        self.new_mob = _make_mob(key="wolf")
        self.evennia_stub = _setup_evennia_stub(create_result=self.new_mob)
        self.spawner = _reload_mob_spawner()

    def tearDown(self):
        for key in list(sys.modules.keys()):
            if "mob_spawner" in key:
                del sys.modules[key]

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
        # Patch node_helpers so condition fails
        with patch.dict(sys.modules, {
            "world.node_helpers": MagicMock(get_node_script=MagicMock(return_value=None))
        }):
            spawner = _reload_mob_spawner()
            spawned = spawner.spawn_room_mobs(room)
        self.assertEqual(spawned, 0)
        self.evennia_stub.create_object.assert_not_called()


# ---------------------------------------------------------------------------
# Tests: spawn_zone
# ---------------------------------------------------------------------------

class TestSpawnZone(unittest.TestCase):

    def setUp(self):
        self.new_mob = _make_mob()
        self.evennia_stub = _setup_evennia_stub(create_result=self.new_mob)
        self.spawner = _reload_mob_spawner()

    def tearDown(self):
        for key in list(sys.modules.keys()):
            if "mob_spawner" in key:
                del sys.modules[key]

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

        self.evennia_stub.search_tag = MagicMock(side_effect=_search_tag_side_effect)

        total = self.spawner.spawn_zone(zone_obj)
        # Each room has count_min=1, empty → 1 spawn each → 2 total
        self.assertEqual(total, 2)

    def test_excludes_zone_obj_itself(self):
        """zone_obj (tagged zone_object) must not be passed to spawn_room_mobs."""
        zone_obj = MagicMock()
        zone_obj.db.zone_id = "zone_02"
        zone_obj.tags.get = MagicMock(side_effect=lambda t, category=None: t == "zone_object")
        zone_obj.db.spawn_definitions = [_make_spawn_def(mob="wolf", count_min=5)]

        self.evennia_stub.search_tag = MagicMock(return_value=[zone_obj])
        total = self.spawner.spawn_zone(zone_obj)
        self.assertEqual(total, 0)


# ---------------------------------------------------------------------------
# Tests: _maybe_attach_patrol
# ---------------------------------------------------------------------------

class TestMaybeAttachPatrol(unittest.TestCase):

    def setUp(self):
        self.new_mob = _make_mob()
        self.evennia_stub = _setup_evennia_stub(create_result=self.new_mob)
        self.spawner = _reload_mob_spawner()

    def tearDown(self):
        for key in list(sys.modules.keys()):
            if "mob_spawner" in key:
                del sys.modules[key]

    def test_does_nothing_when_no_zone_obj(self):
        with patch("world.zone_scaling.get_zone_obj_for_room", return_value=None):
            spawner = _reload_mob_spawner()
            mob = _make_mob()
            spawn_def = _make_spawn_def(mob="wolf")
            room = _make_room()
            spawner._maybe_attach_patrol(mob, spawn_def, room)
            mob.scripts.add.assert_not_called()

    def test_does_nothing_when_no_patrol_definitions(self):
        zone_obj = MagicMock()
        zone_obj.db.patrol_definitions = None
        with patch("world.zone_scaling.get_zone_obj_for_room", return_value=zone_obj):
            spawner = _reload_mob_spawner()
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
            spawner = _reload_mob_spawner()
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

        self.evennia_stub.search_tag = MagicMock(side_effect=_search_tag_for_route)

        mock_script = MagicMock()
        mob = _make_mob()
        mob.scripts.get = MagicMock(return_value=[mock_script])
        spawn_def = _make_spawn_def(mob="wolf")
        room = _make_room(zone_id="zone_test")

        with patch("world.zone_scaling.get_zone_obj_for_room", return_value=zone_obj):
            spawner = _reload_mob_spawner()
            # ensure evennia stub is active
            sys.modules["evennia"] = self.evennia_stub
            spawner._maybe_attach_patrol(mob, spawn_def, room)

        mob.scripts.add.assert_called_once()
        self.assertEqual(mock_script.db.route_ids, [101, 102])
        self.assertEqual(mock_script.db.patrol_def, patrol_def)


# ---------------------------------------------------------------------------
# Tests: _schedule_respawn
# ---------------------------------------------------------------------------

class TestScheduleRespawn(unittest.TestCase):

    def setUp(self):
        self.room = _make_room()
        self.new_mob = _make_mob()
        self.evennia_stub = _setup_evennia_stub(create_result=self.new_mob)
        self.spawner = _reload_mob_spawner()

    def tearDown(self):
        for key in list(sys.modules.keys()):
            if "mob_spawner" in key:
                del sys.modules[key]

    def test_calls_call_later_with_valid_delay(self):
        spawn_def = _make_spawn_def(mob="wolf", respawn_minutes=10, respawn_variance=0)
        self.room.contents = []

        mock_reactor = MagicMock()
        with patch.object(self.spawner, "_get_reactor", return_value=mock_reactor):
            self.spawner._schedule_respawn(spawn_def, self.room)

        mock_reactor.callLater.assert_called_once()
        delay_arg = mock_reactor.callLater.call_args[0][0]
        self.assertGreaterEqual(delay_arg, 30)
        # base 10*60=600, variance=0 → should be 600
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

class TestEvaluateSpawnCondition(unittest.TestCase):

    def setUp(self):
        self.evennia_stub = _setup_evennia_stub()
        self.spawner = _reload_mob_spawner()

    def tearDown(self):
        for key in list(sys.modules.keys()):
            if "mob_spawner" in key:
                del sys.modules[key]

    def test_none_condition_always_returns_true(self):
        room = _make_room()
        self.assertTrue(self.spawner._evaluate_spawn_condition(None, room))

    def test_empty_string_returns_true(self):
        room = _make_room()
        self.assertTrue(self.spawner._evaluate_spawn_condition("", room))

    def test_node_failure_above_threshold_false_when_no_script(self):
        with patch("world.node_helpers.get_node_script", return_value=None):
            spawner = _reload_mob_spawner()
            room = _make_room(zone_id="zone_a")
            self.assertFalse(spawner._evaluate_spawn_condition("node_failure_above_50", room))

    def test_node_failure_above_threshold_true_when_met(self):
        mock_script = MagicMock()
        mock_script.db.failure = 75
        with patch("world.node_helpers.get_node_script", return_value=mock_script):
            spawner = _reload_mob_spawner()
            room = _make_room(zone_id="zone_a")
            self.assertTrue(spawner._evaluate_spawn_condition("node_failure_above_50", room))

    def test_node_failure_above_threshold_false_when_below(self):
        mock_script = MagicMock()
        mock_script.db.failure = 30
        with patch("world.node_helpers.get_node_script", return_value=mock_script):
            spawner = _reload_mob_spawner()
            room = _make_room(zone_id="zone_a")
            self.assertFalse(spawner._evaluate_spawn_condition("node_failure_above_50", room))

    def test_node_active_true_when_active(self):
        mock_script = MagicMock()
        mock_script.db.state = "active"
        with patch("world.node_helpers.get_node_script", return_value=mock_script):
            spawner = _reload_mob_spawner()
            room = _make_room(zone_id="zone_a")
            self.assertTrue(spawner._evaluate_spawn_condition("node_active", room))

    def test_node_active_false_when_dormant(self):
        mock_script = MagicMock()
        mock_script.db.state = "dormant"
        with patch("world.node_helpers.get_node_script", return_value=mock_script):
            spawner = _reload_mob_spawner()
            room = _make_room(zone_id="zone_a")
            self.assertFalse(spawner._evaluate_spawn_condition("node_active", room))

    def test_quest_complete_stub_returns_false(self):
        room = _make_room()
        self.assertFalse(self.spawner._evaluate_spawn_condition("quest_complete:some_quest", room))

    def test_time_of_day_stub_returns_true(self):
        room = _make_room()
        self.assertTrue(self.spawner._evaluate_spawn_condition("time_of_day:night", room))

    def test_unknown_condition_returns_true(self):
        room = _make_room()
        self.assertTrue(self.spawner._evaluate_spawn_condition("totally_unknown_condition_xyz", room))


if __name__ == "__main__":
    unittest.main()
