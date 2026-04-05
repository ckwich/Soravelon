"""
Tests for SpawnRecord lifecycle (world/mob_spawner.py).

Covers SpawnRecord creation, spawn_tick processing, death hook scheduling,
initialize_spawn_records idempotency, and named mob WorldEventLog integration.
Uses unittest.TestCase + MagicMock (no Evennia DB required).

Django setup required for model introspection tests (TestSpawnRecordModel).
sys.modules injection for pure-logic tests to avoid Django DB setup.
"""

import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch, call

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
django.setup()


def _make_room(room_id=100, zone_id="test_zone", spawn_defs=None):
    """Create a MagicMock room with spawn_definitions."""
    room = MagicMock()
    room.id = room_id
    room.db.zone_id = zone_id
    room.db.spawn_definitions = spawn_defs or []
    room.tags = MagicMock()
    room.tags.get = MagicMock(return_value=None)
    room.contents = []
    room.msg_contents = MagicMock()
    return room


def _make_mob(mob_id=200, key="Wolf", spawn_record_id=None, location=None):
    """Create a MagicMock mob for death hook tests."""
    mob = MagicMock()
    mob.id = mob_id
    mob.key = key
    mob.db.spawn_record_id = spawn_record_id
    mob.db.zone_id = "test_zone"
    mob.location = location
    mob.tags = MagicMock()
    return mob


def _make_spawn_record(
    record_id=1,
    room_id=100,
    spawn_index=0,
    mob_template_key="Wolf",
    active_mob_ids=None,
    respawn_at=None,
    is_named=False,
    named_id="",
):
    """Create a MagicMock SpawnRecord."""
    record = MagicMock()
    record.id = record_id
    record.room_id = room_id
    record.spawn_index = spawn_index
    record.mob_template_key = mob_template_key
    record.active_mob_ids = active_mob_ids or []
    record.respawn_at = respawn_at
    record.is_named = is_named
    record.named_id = named_id
    record.save = MagicMock()
    record.delete = MagicMock()
    return record


class TestScheduleRespawnFromDeath(unittest.TestCase):
    """Death hook removes mob from active list and schedules respawn."""

    @patch("world.mob_spawner.random")
    @patch("world.mob_spawner.timezone")
    @patch("world.models.SpawnRecord.objects")
    def test_mob_removed_from_active_ids(self, mock_sr_objects, mock_tz, mock_random):
        """Mob ID removed from active_mob_ids on death (reassign, not mutate)."""
        from world.mob_spawner import schedule_respawn_from_death

        record = _make_spawn_record(
            active_mob_ids=[200, 201], respawn_at=None
        )
        mock_sr_objects.get.return_value = record

        room = _make_room(
            spawn_defs=[{"mob": "Wolf", "respawn_minutes": 10, "respawn_variance": 2}]
        )
        mob = _make_mob(mob_id=200, spawn_record_id=1, location=room)

        schedule_respawn_from_death(mob)

        # Mob 200 removed, mob 201 remains
        self.assertNotIn(200, record.active_mob_ids)
        self.assertIn(201, record.active_mob_ids)
        record.save.assert_called_once()

    @patch("world.mob_spawner.random")
    @patch("world.mob_spawner.timezone")
    @patch("world.models.SpawnRecord.objects")
    def test_all_dead_sets_respawn_at(self, mock_sr_objects, mock_tz, mock_random):
        """When all mobs dead, respawn_at set to future time."""
        from world.mob_spawner import schedule_respawn_from_death

        mock_random.uniform.return_value = 0  # no variance
        now = datetime(2026, 1, 1, 12, 0, 0)
        mock_tz.now.return_value = now

        record = _make_spawn_record(active_mob_ids=[200], respawn_at=None)
        mock_sr_objects.get.return_value = record

        room = _make_room(
            spawn_defs=[{"mob": "Wolf", "respawn_minutes": 10, "respawn_variance": 0}]
        )
        mob = _make_mob(mob_id=200, spawn_record_id=1, location=room)

        schedule_respawn_from_death(mob)

        self.assertEqual(record.active_mob_ids, [])
        self.assertIsNotNone(record.respawn_at)
        record.save.assert_called_once()

    @patch("world.mob_spawner.timezone")
    @patch("world.models.SpawnRecord.objects")
    def test_some_alive_no_respawn(self, mock_sr_objects, mock_tz):
        """When some mobs remain alive, respawn_at stays None."""
        from world.mob_spawner import schedule_respawn_from_death

        record = _make_spawn_record(
            active_mob_ids=[200, 201], respawn_at=None
        )
        mock_sr_objects.get.return_value = record

        room = _make_room(spawn_defs=[{"mob": "Wolf"}])
        mob = _make_mob(mob_id=200, spawn_record_id=1, location=room)

        schedule_respawn_from_death(mob)

        # 201 still alive, so no respawn scheduled
        self.assertIsNone(record.respawn_at)

    def test_no_record_id_noop(self):
        """Mob without spawn_record_id is a no-op."""
        from world.mob_spawner import schedule_respawn_from_death

        mob = _make_mob(spawn_record_id=None)
        schedule_respawn_from_death(mob)
        # No error raised, function returns early


class TestSpawnTick(unittest.TestCase):
    """spawn_tick processes due SpawnRecords."""

    @patch("world.mob_spawner._process_spawn_record")
    @patch("world.models.SpawnRecord.objects")
    @patch("world.mob_spawner.timezone")
    def test_processes_due_records(self, mock_tz, mock_sr_objects, mock_process):
        """Due records are processed by spawn_tick."""
        from world.mob_spawner import spawn_tick

        now = datetime(2026, 1, 1, 12, 0, 0)
        mock_tz.now.return_value = now

        record1 = _make_spawn_record(record_id=1)
        record2 = _make_spawn_record(record_id=2)
        mock_sr_objects.filter.return_value = [record1, record2]

        spawn_tick()

        self.assertEqual(mock_process.call_count, 2)

    @patch("world.mob_spawner._process_spawn_record")
    @patch("world.models.SpawnRecord.objects")
    @patch("world.mob_spawner.timezone")
    def test_error_continues_processing(self, mock_tz, mock_sr_objects, mock_process):
        """Exception in one record doesn't stop processing others."""
        from world.mob_spawner import spawn_tick

        mock_tz.now.return_value = datetime(2026, 1, 1, 12, 0, 0)

        r1 = _make_spawn_record(record_id=1)
        r2 = _make_spawn_record(record_id=2)
        mock_sr_objects.filter.return_value = [r1, r2]
        mock_process.side_effect = [Exception("boom"), None]

        spawn_tick()  # should not raise
        self.assertEqual(mock_process.call_count, 2)


class TestProcessSpawnRecord(unittest.TestCase):
    """_process_spawn_record resolves room, spawns mob, updates record."""

    @patch("world.mob_spawner.spawn_single_mob")
    @patch("world.mob_spawner._is_respawn", return_value=False)
    @patch("world.mob_spawner._evaluate_spawn_condition", return_value=True)
    @patch("world.mob_spawner.evennia")
    @patch("world.mob_spawner.timezone")
    def test_spawns_mob_and_updates_record(
        self, mock_tz, mock_evennia, mock_eval, mock_is_resp, mock_spawn
    ):
        """Successful spawn adds mob.id to active_mob_ids and clears respawn_at."""
        from world.mob_spawner import _process_spawn_record

        mock_mob = _make_mob(mob_id=300)
        mock_spawn.return_value = mock_mob

        room = _make_room(spawn_defs=[{"mob": "Wolf"}])
        mock_evennia.search_object.return_value = [room]

        record = _make_spawn_record(
            room_id=100, spawn_index=0, active_mob_ids=[]
        )

        _process_spawn_record(record)

        mock_spawn.assert_called_once()
        self.assertIn(300, record.active_mob_ids)
        self.assertIsNone(record.respawn_at)
        record.save.assert_called()

    @patch("world.mob_spawner._evaluate_spawn_condition", return_value=False)
    @patch("world.mob_spawner.evennia")
    @patch("world.mob_spawner.timezone")
    def test_condition_not_met_reschedules(self, mock_tz, mock_evennia, mock_eval):
        """When spawn condition not met, reschedule 5 minutes out."""
        from world.mob_spawner import _process_spawn_record

        now = datetime(2026, 1, 1, 12, 0, 0)
        mock_tz.now.return_value = now

        room = _make_room(spawn_defs=[{"mob": "Wolf", "spawn_condition": "node_active"}])
        mock_evennia.search_object.return_value = [room]

        record = _make_spawn_record(room_id=100, spawn_index=0)

        _process_spawn_record(record)

        self.assertEqual(record.respawn_at, now + timedelta(minutes=5))
        record.save.assert_called()

    @patch("world.mob_spawner.evennia")
    def test_missing_room_deletes_record(self, mock_evennia):
        """Room not found -> record deleted."""
        from world.mob_spawner import _process_spawn_record

        mock_evennia.search_object.return_value = []
        record = _make_spawn_record(room_id=999)

        _process_spawn_record(record)

        record.delete.assert_called_once()


class TestInitializeSpawnRecords(unittest.TestCase):
    """initialize_spawn_records creates entries for rooms with spawn_definitions."""

    @patch("world.models.SpawnRecord.objects")
    @patch("world.mob_spawner.timezone")
    @patch("world.mob_spawner.evennia")
    def test_creates_records_per_definition(self, mock_evennia, mock_tz, mock_sr_objects):
        """Each spawn_definition gets a SpawnRecord via get_or_create."""
        from world.mob_spawner import initialize_spawn_records

        now = datetime(2026, 1, 1, 12, 0, 0)
        mock_tz.now.return_value = now

        room = _make_room(
            room_id=100,
            spawn_defs=[
                {"mob": "Wolf", "is_named": False},
                {"mob": "Bear", "is_named": True},
            ],
        )
        room.tags.get.return_value = None  # not a zone_object
        mock_evennia.search_tag.return_value = [room]

        mock_sr_objects.get_or_create.return_value = (MagicMock(), True)

        initialize_spawn_records()

        self.assertEqual(mock_sr_objects.get_or_create.call_count, 2)

    @patch("world.models.SpawnRecord.objects")
    @patch("world.mob_spawner.timezone")
    @patch("world.mob_spawner.evennia")
    def test_existing_records_preserved(self, mock_evennia, mock_tz, mock_sr_objects):
        """Existing records are not overwritten (idempotent)."""
        from world.mob_spawner import initialize_spawn_records

        mock_tz.now.return_value = MagicMock()

        room = _make_room(spawn_defs=[{"mob": "Wolf"}])
        room.tags.get.return_value = None
        mock_evennia.search_tag.return_value = [room]

        # Existing record
        mock_sr_objects.get_or_create.return_value = (MagicMock(), False)

        initialize_spawn_records()

        # Still called, but was_created=False means no new record
        mock_sr_objects.get_or_create.assert_called_once()


class TestNamedMobDeath(unittest.TestCase):
    """Named mob death integration with WorldEventLog."""

    @patch("world.mob_spawner.random")
    @patch("world.mob_spawner.timezone")
    @patch("world.models.SpawnRecord.objects")
    def test_death_updates_record(self, mock_sr_objects, mock_tz, mock_random):
        """Named mob death removes from active IDs like normal mobs."""
        from world.mob_spawner import schedule_respawn_from_death

        mock_random.uniform.return_value = 0
        mock_tz.now.return_value = datetime(2026, 1, 1, 12, 0, 0)

        record = _make_spawn_record(
            active_mob_ids=[200],
            is_named=True,
            named_id="boss_wolf",
        )
        mock_sr_objects.get.return_value = record

        room = _make_room(
            spawn_defs=[{
                "mob": "Boss Wolf",
                "is_named": True,
                "respawn_minutes": 30,
                "respawn_variance": 10,
            }]
        )
        mob = _make_mob(mob_id=200, key="Boss Wolf", spawn_record_id=1, location=room)

        schedule_respawn_from_death(mob)

        self.assertEqual(record.active_mob_ids, [])
        self.assertIsNotNone(record.respawn_at)
        record.save.assert_called_once()


class TestSpawnRecordModel(unittest.TestCase):
    """SpawnRecord model has correct fields and constraints."""

    def test_unique_together_constraint(self):
        """Verify unique_together is defined for room_id + spawn_index."""
        from world.models import SpawnRecord

        meta = SpawnRecord._meta
        self.assertIn(
            ("room_id", "spawn_index"),
            meta.unique_together,
        )

    def test_model_fields_exist(self):
        """All expected fields are present on the model."""
        from world.models import SpawnRecord

        field_names = [f.name for f in SpawnRecord._meta.get_fields()]
        for expected in ("room_id", "spawn_index", "mob_template_key",
                         "active_mob_ids", "respawn_at", "is_named", "named_id"):
            self.assertIn(expected, field_names, f"Missing field: {expected}")


if __name__ == "__main__":
    unittest.main()
