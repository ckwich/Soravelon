"""
Tests for world/recovery_engine.py — HP/stamina recovery system.

Uses unittest.TestCase + MagicMock (pure logic module, no Evennia DB needed).
"""

import unittest
from unittest.mock import MagicMock, patch, PropertyMock
import time


def _make_character(hp=50, max_hp=100, stamina=25, max_stamina=50,
                    in_combat=False, recovery_state="active",
                    is_sleeping=False, carried_scales=100,
                    blessing_cooldowns=None):
    """Create a mock character with ndb/db attributes."""
    char = MagicMock()

    # ndb attributes (volatile)
    char.ndb.hp = hp
    char.ndb.stamina = stamina
    char.ndb.combat_handler = MagicMock() if in_combat else None
    char.ndb.recovery_state = recovery_state
    char.ndb.is_sleeping = is_sleeping
    char.ndb.regen_handle = None

    # db attributes (persistent)
    char.db.carried_scales = carried_scales
    char.db.blessing_cooldowns = blessing_cooldowns or {}
    char.db.base_stats = {"endurance": 10}
    char.db.backend_level = 1

    # location mock
    char.location = MagicMock()
    char.location.contents = []

    return char


class TestRegenTick(unittest.TestCase):
    """Test the _regen_tick function."""

    @patch("world.recovery_engine._schedule_next_tick")
    @patch("world.recovery_engine.push_stat_update")
    @patch("world.base_attributes.derive_max_stamina", return_value=50)
    @patch("world.base_attributes.derive_max_hp", return_value=100)
    def test_passive_regen_hp(self, mock_max_hp, mock_max_stam, mock_push, mock_sched):
        """Active state out of combat: 1% of max HP per tick."""
        from world.recovery_engine import _regen_tick
        char = _make_character(hp=50, max_hp=100, stamina=50, max_stamina=50)
        char.ndb.recovery_state = "active"
        _regen_tick(char)
        # 1% of 100 = 1, but min is 1 anyway. 50 + 1 = 51
        self.assertEqual(char.ndb.hp, 51)

    @patch("world.recovery_engine._schedule_next_tick")
    @patch("world.recovery_engine.push_stat_update")
    @patch("world.base_attributes.derive_max_stamina", return_value=50)
    @patch("world.base_attributes.derive_max_hp", return_value=100)
    def test_passive_regen_skipped_in_combat(self, mock_max_hp, mock_max_stam, mock_push, mock_sched):
        """In combat: tick does NOT change HP."""
        from world.recovery_engine import _regen_tick
        char = _make_character(hp=50, in_combat=True)
        _regen_tick(char)
        self.assertEqual(char.ndb.hp, 50)

    @patch("world.recovery_engine._schedule_next_tick")
    @patch("world.recovery_engine.push_stat_update")
    @patch("world.base_attributes.derive_max_stamina", return_value=50)
    @patch("world.base_attributes.derive_max_hp", return_value=100)
    def test_rest_regen_rate(self, mock_max_hp, mock_max_stam, mock_push, mock_sched):
        """Resting state: 3% of max HP per tick."""
        from world.recovery_engine import _regen_tick
        char = _make_character(hp=50, recovery_state="resting")
        _regen_tick(char)
        # 3% of 100 = 3. 50 + 3 = 53
        self.assertEqual(char.ndb.hp, 53)

    @patch("world.recovery_engine._schedule_next_tick")
    @patch("world.recovery_engine.push_stat_update")
    @patch("world.base_attributes.derive_max_stamina", return_value=50)
    @patch("world.base_attributes.derive_max_hp", return_value=100)
    def test_sleep_regen_rate(self, mock_max_hp, mock_max_stam, mock_push, mock_sched):
        """Sleeping state (no bed): 6% of max HP per tick."""
        from world.recovery_engine import _regen_tick
        char = _make_character(hp=50, recovery_state="sleeping")
        # No bed in room
        char.location.contents = []
        with patch("world.recovery_engine._room_has_bed", return_value=False):
            _regen_tick(char)
        # 6% of 100 = 6. 50 + 6 = 56
        self.assertEqual(char.ndb.hp, 56)

    @patch("world.recovery_engine._schedule_next_tick")
    @patch("world.recovery_engine.push_stat_update")
    @patch("world.base_attributes.derive_max_stamina", return_value=50)
    @patch("world.base_attributes.derive_max_hp", return_value=100)
    def test_sleep_bed_regen_rate(self, mock_max_hp, mock_max_stam, mock_push, mock_sched):
        """Sleeping with bed: 10% of max HP per tick."""
        from world.recovery_engine import _regen_tick
        char = _make_character(hp=50, recovery_state="sleeping")
        with patch("world.recovery_engine._room_has_bed", return_value=True):
            _regen_tick(char)
        # 10% of 100 = 10. 50 + 10 = 60
        self.assertEqual(char.ndb.hp, 60)

    @patch("world.recovery_engine._schedule_next_tick")
    @patch("world.recovery_engine.push_stat_update")
    @patch("world.base_attributes.derive_max_stamina", return_value=50)
    @patch("world.base_attributes.derive_max_hp", return_value=100)
    def test_stamina_regens_same_rate(self, mock_max_hp, mock_max_stam, mock_push, mock_sched):
        """Stamina follows same rate as HP for given state."""
        from world.recovery_engine import _regen_tick
        char = _make_character(hp=100, stamina=25, recovery_state="resting")
        _regen_tick(char)
        # 3% of 50 = 1 (max(1, int(50*0.03))=max(1,1)=1). 25 + 1 = 26
        self.assertEqual(char.ndb.stamina, 26)

    @patch("world.recovery_engine._schedule_next_tick")
    @patch("world.recovery_engine.push_stat_update")
    @patch("world.base_attributes.derive_max_stamina", return_value=50)
    @patch("world.base_attributes.derive_max_hp", return_value=100)
    def test_regen_stops_at_full(self, mock_max_hp, mock_max_stam, mock_push, mock_sched):
        """At full HP and stamina, tick does not schedule next tick."""
        from world.recovery_engine import _regen_tick
        char = _make_character(hp=100, stamina=50)
        _regen_tick(char)
        # HP and stamina both at max — _schedule_next_tick should NOT be called
        mock_sched.assert_not_called()


class TestRecoveryState(unittest.TestCase):
    """Test set_recovery_state and cancel_recovery."""

    @patch("world.recovery_engine._schedule_next_tick")
    def test_set_recovery_state_rest(self, mock_sched):
        from world.recovery_engine import set_recovery_state
        char = _make_character()
        ok, msg = set_recovery_state(char, "resting")
        self.assertTrue(ok)
        self.assertEqual(char.ndb.recovery_state, "resting")
        self.assertFalse(char.ndb.is_sleeping)

    @patch("world.recovery_engine._schedule_next_tick")
    def test_set_recovery_state_sleep(self, mock_sched):
        from world.recovery_engine import set_recovery_state
        char = _make_character()
        ok, msg = set_recovery_state(char, "sleeping")
        self.assertTrue(ok)
        self.assertEqual(char.ndb.recovery_state, "sleeping")
        self.assertTrue(char.ndb.is_sleeping)

    @patch("world.recovery_engine._schedule_next_tick")
    def test_set_recovery_state_blocked_in_combat(self, mock_sched):
        from world.recovery_engine import set_recovery_state
        char = _make_character(in_combat=True)
        ok, msg = set_recovery_state(char, "resting")
        self.assertFalse(ok)

    def test_cancel_recovery(self):
        from world.recovery_engine import cancel_recovery
        char = _make_character(recovery_state="sleeping", is_sleeping=True)
        ok, msg = cancel_recovery(char)
        self.assertTrue(ok)
        self.assertEqual(char.ndb.recovery_state, "active")
        self.assertFalse(char.ndb.is_sleeping)
        self.assertIn("wake", msg.lower())


class TestBlessings(unittest.TestCase):
    """Test apply_blessing function."""

    @patch("world.recovery_engine.push_stat_update")
    @patch("world.base_attributes.derive_max_hp", return_value=100)
    def test_apply_blessing_heal(self, mock_max_hp, mock_push):
        from world.recovery_engine import apply_blessing
        char = _make_character(hp=30, carried_scales=100)
        medic = MagicMock()
        medic.id = 999
        ok, msg = apply_blessing(char, medic, "heal")
        self.assertTrue(ok)
        self.assertEqual(char.ndb.hp, 100)  # healed to full
        self.assertEqual(char.db.carried_scales, 80)  # 100 - 20 cost

    @patch("world.status_effects.apply_effect", return_value=(True, "Applied"))
    def test_apply_blessing_fortify(self, mock_apply):
        from world.recovery_engine import apply_blessing
        char = _make_character(carried_scales=100)
        medic = MagicMock()
        medic.id = 999
        ok, msg = apply_blessing(char, medic, "fortify")
        self.assertTrue(ok)
        mock_apply.assert_called_once()
        self.assertEqual(char.db.carried_scales, 70)  # 100 - 30 cost

    def test_apply_blessing_cooldown(self):
        from world.recovery_engine import apply_blessing
        # Set cooldown to current time (still on cooldown)
        char = _make_character(carried_scales=200,
                               blessing_cooldowns={"heal": time.time()})
        medic = MagicMock()
        medic.id = 999
        ok, msg = apply_blessing(char, medic, "heal")
        self.assertFalse(ok)
        self.assertIn("cooldown", msg.lower())

    def test_apply_blessing_not_enough_scales(self):
        from world.recovery_engine import apply_blessing
        char = _make_character(carried_scales=5)
        medic = MagicMock()
        medic.id = 999
        ok, msg = apply_blessing(char, medic, "heal")
        self.assertFalse(ok)
        self.assertIn("scales", msg.lower())


class TestStartStopRegen(unittest.TestCase):

    @patch("world.recovery_engine._schedule_next_tick")
    def test_start_regen(self, mock_sched):
        from world.recovery_engine import start_regen
        char = _make_character()
        char.ndb.recovery_state = None
        ok, msg = start_regen(char)
        self.assertTrue(ok)
        self.assertEqual(char.ndb.recovery_state, "active")
        mock_sched.assert_called_once()

    def test_stop_regen(self):
        from world.recovery_engine import stop_regen
        char = _make_character()
        handle = MagicMock()
        char.ndb.regen_handle = handle
        ok, msg = stop_regen(char)
        self.assertTrue(ok)
        handle.cancel.assert_called_once()
        self.assertIsNone(char.ndb.regen_handle)


if __name__ == "__main__":
    unittest.main()
