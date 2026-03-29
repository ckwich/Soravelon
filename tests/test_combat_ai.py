"""
Tests for mob combat AI (world/combat_ai.py).

Covers weighted ability selection, cooldown filtering, condition vocabulary,
targeting priority, vanish skip, scripted sequences (CMB-03), casting time
state machine (D-11), new condition keys (D-13), and is_hunter chase (D-15).
Uses unittest.TestCase + MagicMock (no Evennia DB required).
"""

import os
import unittest
from unittest.mock import MagicMock, patch

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
django.setup()


def _make_mob(abilities=None, hp=100, hp_max=100):
    """Create a MagicMock mob with AI-relevant attributes."""
    mob = MagicMock()
    mob.key = "TestMob"
    mob.id = 10
    mob.db.abilities = abilities or []
    mob.db.base_stats = None
    mob.db.hp_max = hp_max
    mob.db.ref_damage_min = 8
    mob.db.ref_damage_max = 14
    mob.db.damage_min = None
    mob.db.damage_max = None
    mob.db.mob_type = "wolf"
    mob.db.base_aggression = 0.5
    mob.db.speed = 1.0
    mob.db.flee_low_hp = None
    mob.db.scripted_sequence = None
    mob.db.is_hunter = False
    mob.db.detection_range = 3
    mob.ndb.hp = hp
    mob.ndb.ability_cooldowns = {}
    mob.ndb.last_attacker_id = None
    mob.ndb.fired_sequence_triggers = None
    mob.ndb.active_effects = []
    mob.ndb.target_fled = False
    mob.location = MagicMock()
    mob.tags = MagicMock()
    mob.tags.get = MagicMock(return_value=None)
    return mob


def _make_player(player_id=1, hp=100, hp_max=200):
    """Create a MagicMock player for targeting tests."""
    player = MagicMock()
    player.key = "TestPlayer"
    player.id = player_id
    player.db.base_stats = {"strength": 10, "agility": 10, "endurance": 10,
                            "mana": 10, "acuity": 10, "presence": 10, "resonance": 10}
    player.db.backend_level = 5
    player.ndb.hp = hp
    player.ndb.active_effects = []
    player.tags = MagicMock()
    player.tags.get = MagicMock(return_value="player_character")
    return player


def _make_combat_handler(players=None, mobs=None, round_number=1):
    """Create a MagicMock combat handler."""
    ch = MagicMock()
    ch.ndb.player_combatants = players or []
    ch.ndb.mob_combatants = mobs or []
    ch.db.round_number = round_number
    ch.ndb.call_for_help_count = 0
    return ch


class TestAbilitySelection(unittest.TestCase):
    """Weight-based ability selection with cooldown/condition filtering (CMB-03)."""

    def test_selects_by_weight(self):
        """Higher weight abilities selected more often (statistical N=100)."""
        from world.combat_ai import select_mob_action

        abilities = [
            {"ability_id": "heavy", "weight": 10, "damage_base": 20},
            {"ability_id": "light", "weight": 1, "damage_base": 5},
        ]
        mob = _make_mob(abilities=abilities)
        player = _make_player()
        ch = _make_combat_handler(players=[player])

        counts = {"heavy": 0, "light": 0}
        for _ in range(200):
            action = select_mob_action(mob, player, ch)
            if action.get("type") == "ability":
                counts[action["ability_id"]] += 1

        # heavy should be selected significantly more often than light
        self.assertGreater(counts["heavy"], counts["light"] * 3)

    def test_cooldown_filtered(self):
        """Ability on cooldown is not selected."""
        from world.combat_ai import select_mob_action

        abilities = [
            {"ability_id": "fireball", "weight": 10, "damage_base": 30, "cooldown": 3},
        ]
        mob = _make_mob(abilities=abilities)
        mob.ndb.ability_cooldowns = {"fireball": 2}
        player = _make_player()
        ch = _make_combat_handler(players=[player])

        action = select_mob_action(mob, player, ch)
        self.assertEqual(action["type"], "basic_attack")

    def test_condition_checked(self):
        """'target_below_50hp' only passes when target HP < 50%."""
        from world.combat_ai import select_mob_action

        abilities = [
            {
                "ability_id": "execute",
                "weight": 10,
                "damage_base": 50,
                "condition": "target_below_50hp",
            },
        ]
        mob = _make_mob(abilities=abilities)

        # Target at full HP -- condition should fail, fall back to basic attack
        player = _make_player(hp=100, hp_max=200)
        ch = _make_combat_handler(players=[player])
        action = select_mob_action(mob, player, ch)
        self.assertEqual(action["type"], "basic_attack")

        # Target at low HP -- condition should pass
        # derive_max_hp uses endurance=10, level=5: 50+50+50=150. 50% = 75
        player.ndb.hp = 50  # below 50% of 150
        action = select_mob_action(mob, player, ch)
        self.assertEqual(action["type"], "ability")
        self.assertEqual(action["ability_id"], "execute")

    def test_fallback_basic_attack(self):
        """All abilities on cooldown -> returns basic_attack."""
        from world.combat_ai import select_mob_action

        abilities = [
            {"ability_id": "a1", "weight": 5, "damage_base": 10, "cooldown": 2},
            {"ability_id": "a2", "weight": 5, "damage_base": 10, "cooldown": 2},
        ]
        mob = _make_mob(abilities=abilities)
        mob.ndb.ability_cooldowns = {"a1": 1, "a2": 1}
        player = _make_player()
        ch = _make_combat_handler(players=[player])

        action = select_mob_action(mob, player, ch)
        self.assertEqual(action["type"], "basic_attack")

    def test_no_infinite_loop(self):
        """Mob with empty ability list returns basic_attack immediately."""
        from world.combat_ai import select_mob_action

        mob = _make_mob(abilities=[])
        player = _make_player()
        ch = _make_combat_handler(players=[player])

        action = select_mob_action(mob, player, ch)
        self.assertEqual(action["type"], "basic_attack")


class TestMobTargeting(unittest.TestCase):
    """Mob targeting priority: last attacker > random (CMB-03)."""

    def test_last_attacker_priority(self):
        """Mob targets whoever last hit it."""
        from world.combat_ai import get_mob_target

        p1 = _make_player(player_id=1)
        p2 = _make_player(player_id=2)
        mob = _make_mob()
        mob.ndb.last_attacker_id = 2

        # Both players in same room as mob
        p1.location = mob.location
        p2.location = mob.location

        ch = _make_combat_handler(players=[p1, p2])

        target = get_mob_target(mob, ch)
        self.assertEqual(target.id, 2)

    def test_random_fallback(self):
        """No attacker -> random target from players."""
        from world.combat_ai import get_mob_target

        p1 = _make_player(player_id=1)
        mob = _make_mob()
        mob.ndb.last_attacker_id = None
        p1.location = mob.location

        ch = _make_combat_handler(players=[p1])

        target = get_mob_target(mob, ch)
        self.assertIsNotNone(target)
        self.assertEqual(target.id, 1)

    def test_vanish_skipped(self):
        """Target with vanish effect is not targeted."""
        from world.combat_ai import get_mob_target

        p1 = _make_player(player_id=1)
        p1.ndb.active_effects = [
            {
                "type": "vanish",
                "stacks": 1,
                "duration": 1,
                "magnitude": 1.0,
                "source_id": None,
                "max_stacks": 1,
                "is_compound": False,
            }
        ]
        p1.location = mob_loc = MagicMock()
        mob = _make_mob()
        mob.location = mob_loc

        ch = _make_combat_handler(players=[p1])

        target = get_mob_target(mob, ch)
        self.assertIsNone(target)


class TestScriptedSequence(unittest.TestCase):
    """Scripted sequence triggers for named mobs (CMB-03)."""

    def test_hp_threshold_fires(self):
        """Sequence with hp_below_50 fires when mob at 40% HP."""
        from world.combat_ai import check_scripted_sequence

        mob = _make_mob(hp=40, hp_max=100)
        mob.db.scripted_sequence = [
            {
                "trigger": "hp_below_50",
                "trigger_key": "hp50",
                "actions": [{"type": "echo", "text": "The beast roars!"}],
            }
        ]
        ch = _make_combat_handler(round_number=3)

        result = check_scripted_sequence(mob, ch)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "echo")

    def test_fires_once(self):
        """Same threshold doesn't fire twice."""
        from world.combat_ai import check_scripted_sequence

        mob = _make_mob(hp=40, hp_max=100)
        mob.db.scripted_sequence = [
            {
                "trigger": "hp_below_50",
                "trigger_key": "hp50",
                "actions": [{"type": "echo", "text": "The beast roars!"}],
            }
        ]
        ch = _make_combat_handler(round_number=3)

        # First call fires
        result1 = check_scripted_sequence(mob, ch)
        self.assertIsNotNone(result1)

        # Second call should not fire again
        result2 = check_scripted_sequence(mob, ch)
        self.assertIsNone(result2)

    def test_combat_start_fires(self):
        """Round 1 fires combat_start triggers."""
        from world.combat_ai import check_scripted_sequence

        mob = _make_mob(hp=100, hp_max=100)
        mob.db.scripted_sequence = [
            {
                "trigger": "combat_start",
                "trigger_key": "start",
                "actions": [{"type": "echo", "text": "A challenger approaches!"}],
            }
        ]
        ch = _make_combat_handler(round_number=1)

        result = check_scripted_sequence(mob, ch)
        self.assertIsNotNone(result)
        self.assertEqual(result[0]["text"], "A challenger approaches!")


# ---------------------------------------------------------------------------
# Phase 6b extension tests: new conditions, casting time, hunter chase
# ---------------------------------------------------------------------------

class TestNewConditions(unittest.TestCase):
    """Verify 6 new condition keys from D-13 vault spec (CMB-04)."""

    @patch("world.combat_ai._target_has_effect")
    def test_target_rooted_true(self, mock_has_effect):
        """target_rooted returns True when target has root effect."""
        from world.combat_ai import CONDITION_CHECKS

        mock_has_effect.return_value = True
        mob = _make_mob()
        target = _make_player()
        ch = _make_combat_handler()

        result = CONDITION_CHECKS["target_rooted"](mob, target, ch)
        self.assertTrue(result)
        mock_has_effect.assert_called_with(target, "root")

    @patch("world.combat_ai._target_has_effect")
    def test_target_rooted_false(self, mock_has_effect):
        """target_rooted returns False when target has no root effect."""
        from world.combat_ai import CONDITION_CHECKS

        mock_has_effect.return_value = False
        mob = _make_mob()
        target = _make_player()
        ch = _make_combat_handler()

        result = CONDITION_CHECKS["target_rooted"](mob, target, ch)
        self.assertFalse(result)

    @patch("world.combat_ai._target_has_effect")
    def test_target_blinded_true(self, mock_has_effect):
        """target_blinded returns True when target has blind effect."""
        from world.combat_ai import CONDITION_CHECKS

        mock_has_effect.return_value = True
        mob = _make_mob()
        target = _make_player()
        ch = _make_combat_handler()

        result = CONDITION_CHECKS["target_blinded"](mob, target, ch)
        self.assertTrue(result)
        mock_has_effect.assert_called_with(target, "blind")

    @patch("world.combat_ai._target_has_effect")
    def test_target_blinded_false(self, mock_has_effect):
        """target_blinded returns False without blind effect."""
        from world.combat_ai import CONDITION_CHECKS

        mock_has_effect.return_value = False
        mob = _make_mob()
        target = _make_player()
        ch = _make_combat_handler()

        result = CONDITION_CHECKS["target_blinded"](mob, target, ch)
        self.assertFalse(result)

    @patch("world.combat_ai._target_has_effect")
    def test_no_target_dot_true(self, mock_has_effect):
        """no_target_dot returns True when no poison/bleed/burn on target."""
        from world.combat_ai import CONDITION_CHECKS

        mock_has_effect.return_value = False  # no effects
        mob = _make_mob()
        target = _make_player()
        ch = _make_combat_handler()

        result = CONDITION_CHECKS["no_target_dot"](mob, target, ch)
        self.assertTrue(result)

    @patch("world.combat_ai._target_has_effect")
    def test_no_target_dot_false_with_poison(self, mock_has_effect):
        """no_target_dot returns False when target has poison."""
        from world.combat_ai import CONDITION_CHECKS

        def side_effect(target, effect_type):
            return effect_type == "poison"

        mock_has_effect.side_effect = side_effect
        mob = _make_mob()
        target = _make_player()
        ch = _make_combat_handler()

        result = CONDITION_CHECKS["no_target_dot"](mob, target, ch)
        self.assertFalse(result)

    def test_pack_present_true(self):
        """pack_present returns True when other mobs alive in combat."""
        from world.combat_ai import CONDITION_CHECKS

        mob = _make_mob()
        mob2 = _make_mob()
        mob2.id = 11
        mob2.ndb.hp = 50
        target = _make_player()
        ch = _make_combat_handler(mobs=[mob, mob2])

        result = CONDITION_CHECKS["pack_present"](mob, target, ch)
        self.assertTrue(result)

    def test_pack_present_false(self):
        """pack_present returns False when mob is alone."""
        from world.combat_ai import CONDITION_CHECKS

        mob = _make_mob()
        target = _make_player()
        ch = _make_combat_handler(mobs=[mob])

        result = CONDITION_CHECKS["pack_present"](mob, target, ch)
        self.assertFalse(result)

    def test_hp_below_50(self):
        """hp_below_50 checks mob's own HP percentage."""
        from world.combat_ai import CONDITION_CHECKS

        mob = _make_mob(hp=40, hp_max=100)
        target = _make_player()
        ch = _make_combat_handler()

        self.assertTrue(CONDITION_CHECKS["hp_below_50"](mob, target, ch))

        mob.ndb.hp = 60
        self.assertFalse(CONDITION_CHECKS["hp_below_50"](mob, target, ch))

    def test_hp_below_25(self):
        """hp_below_25 checks mob's own HP percentage at 25% threshold."""
        from world.combat_ai import CONDITION_CHECKS

        mob = _make_mob(hp=20, hp_max=100)
        target = _make_player()
        ch = _make_combat_handler()

        self.assertTrue(CONDITION_CHECKS["hp_below_25"](mob, target, ch))

        mob.ndb.hp = 30
        self.assertFalse(CONDITION_CHECKS["hp_below_25"](mob, target, ch))

    def test_all_new_conditions_exist(self):
        """All 6 new condition keys exist in CONDITION_CHECKS."""
        from world.combat_ai import CONDITION_CHECKS

        new_keys = [
            "target_rooted", "target_blinded", "no_target_dot",
            "pack_present", "hp_below_50", "hp_below_25",
        ]
        for key in new_keys:
            self.assertIn(key, CONDITION_CHECKS, f"Missing condition: {key}")


class TestCastingTimeStart(unittest.TestCase):
    """Casting time: mob selects ability with cast_time > 0 (D-11)."""

    @patch("world.combat_ai._target_has_effect", return_value=False)
    @patch("world.combat_ai._has_vanish", return_value=False)
    def test_cast_start_returned(self, mock_vanish, mock_effect):
        """Ability with cast_time=2 returns cast_start action dict."""
        from world.combat_ai import select_mob_action

        abilities = [
            {
                "ability_id": "fireball",
                "weight": 10,
                "damage_base": 50,
                "cast_time": 2,
                "emote": "|yThe wolf begins gathering fire...|n",
            },
        ]
        mob = _make_mob(abilities=abilities)
        target = _make_player()
        ch = _make_combat_handler()

        action = select_mob_action(mob, target, ch)

        self.assertEqual(action["type"], "cast_start")
        self.assertEqual(action["cast_time"], 2)
        self.assertIn("emote", action)
        self.assertIn("ability", action)


class TestStartMobCast(unittest.TestCase):
    """start_mob_cast registers pending cast on combat handler."""

    def test_registers_pending_cast(self):
        """Pending cast entry created with correct rounds_left."""
        from world.combat_ai import start_mob_cast

        mob = _make_mob()
        ability = {"ability_id": "fireball", "cast_time": 2, "damage_base": 50}
        target = _make_player()
        ch = _make_combat_handler()
        ch.ndb.pending_mob_casts = {}

        start_mob_cast(mob, ability, target, ch)

        pending = ch.ndb.pending_mob_casts
        self.assertIn(mob.id, pending)
        self.assertEqual(pending[mob.id]["rounds_left"], 2)
        self.assertEqual(pending[mob.id]["target_id"], target.id)
        self.assertEqual(pending[mob.id]["ability"]["ability_id"], "fireball")


class TestResolvePendingCasts(unittest.TestCase):
    """resolve_pending_casts decrements timers and resolves completed casts."""

    @patch("world.status_effects.has_effect", return_value=False)
    @patch("world.combat_ai._resolve_combatant")
    def test_cast_resolves_when_done(self, mock_resolve, mock_has_effect):
        """Cast with rounds_left=1 resolves on next call."""
        from world.combat_ai import resolve_pending_casts

        mob = _make_mob()
        mock_resolve.return_value = mob

        ch = _make_combat_handler()
        ch.ndb.pending_mob_casts = {
            mob.id: {
                "ability": {
                    "ability_id": "fireball",
                    "element": "fire",
                    "damage_base": 50,
                    "status_effect": None,
                    "effect_duration": 0,
                    "effect_magnitude": 0,
                    "application_chance": 1.0,
                    "cooldown": 3,
                },
                "target_id": 1,
                "rounds_left": 1,
            }
        }

        resolved = resolve_pending_casts(ch)

        self.assertEqual(len(resolved), 1)
        self.assertEqual(resolved[0]["type"], "ability")
        self.assertEqual(resolved[0]["ability_id"], "fireball")
        self.assertTrue(resolved[0]["from_cast"])
        # Pending should be cleared
        self.assertNotIn(mob.id, ch.ndb.pending_mob_casts)

    @patch("world.combat_ai._resolve_combatant")
    def test_cast_stays_pending(self, mock_resolve):
        """Cast with rounds_left=2 decrements to 1, stays pending."""
        from world.combat_ai import resolve_pending_casts

        mob = _make_mob()
        mock_resolve.return_value = mob

        ch = _make_combat_handler()
        ch.ndb.pending_mob_casts = {
            mob.id: {
                "ability": {"ability_id": "fireball"},
                "target_id": 1,
                "rounds_left": 2,
            }
        }

        resolved = resolve_pending_casts(ch)

        self.assertEqual(len(resolved), 0)
        self.assertIn(mob.id, ch.ndb.pending_mob_casts)
        self.assertEqual(ch.ndb.pending_mob_casts[mob.id]["rounds_left"], 1)


class TestCastInterrupt(unittest.TestCase):
    """Cast is interrupted when mob has stun/root effect at resolution time."""

    @patch("world.status_effects.has_effect")
    @patch("world.combat_ai._resolve_combatant")
    def test_stun_cancels_cast(self, mock_resolve, mock_has_effect):
        """Mob with stun effect has cast cancelled at resolution."""
        from world.combat_ai import resolve_pending_casts

        mob = _make_mob()
        mock_resolve.return_value = mob

        def has_effect_side(target, effect_type):
            return effect_type == "stun"

        mock_has_effect.side_effect = has_effect_side

        ch = _make_combat_handler()
        ch.ndb.pending_mob_casts = {
            mob.id: {
                "ability": {"ability_id": "fireball"},
                "target_id": 1,
                "rounds_left": 1,
            }
        }

        resolved = resolve_pending_casts(ch)

        # Cast should be cancelled (not in resolved actions)
        self.assertEqual(len(resolved), 0)
        # Pending should be cleared (cast failed)
        self.assertNotIn(mob.id, ch.ndb.pending_mob_casts)
        # Room should get interrupt message
        mob.location.msg_contents.assert_called()

    @patch("world.status_effects.has_effect")
    @patch("world.combat_ai._resolve_combatant")
    def test_root_cancels_cast(self, mock_resolve, mock_has_effect):
        """Mob with root effect has cast cancelled at resolution."""
        from world.combat_ai import resolve_pending_casts

        mob = _make_mob()
        mock_resolve.return_value = mob

        def has_effect_side(target, effect_type):
            return effect_type == "root"

        mock_has_effect.side_effect = has_effect_side

        ch = _make_combat_handler()
        ch.ndb.pending_mob_casts = {
            mob.id: {
                "ability": {"ability_id": "fireball"},
                "target_id": 1,
                "rounds_left": 1,
            }
        }

        resolved = resolve_pending_casts(ch)

        self.assertEqual(len(resolved), 0)
        mob.location.msg_contents.assert_called()


class TestHunterChase(unittest.TestCase):
    """is_hunter mob chases fleeing player via BFS (D-15)."""

    @patch("world.patrol_engine.find_path")
    def test_hunter_moves_toward_target(self, mock_find_path):
        """Hunter mob moves to next room in BFS path."""
        from world.combat_ai import attempt_hunter_chase

        mob = _make_mob()
        mob.db.is_hunter = True
        mob.db.detection_range = 3

        target = _make_player()
        target.location = MagicMock()  # different room

        room1 = MagicMock()
        room2 = MagicMock()
        mock_find_path.return_value = [room1, room2]

        result = attempt_hunter_chase(mob, target, room1)

        self.assertTrue(result)
        mob.move_to.assert_called_once_with(room2, quiet=True)

    @patch("world.patrol_engine.find_path")
    def test_hunter_fails_out_of_range(self, mock_find_path):
        """Hunter returns False when target out of detection range."""
        from world.combat_ai import attempt_hunter_chase

        mob = _make_mob()
        mob.db.is_hunter = True
        mob.db.detection_range = 3

        target = _make_player()
        target.location = MagicMock()

        mock_find_path.return_value = []  # no path found

        result = attempt_hunter_chase(mob, target, MagicMock())

        self.assertFalse(result)
        mob.move_to.assert_not_called()

    def test_non_hunter_returns_false(self):
        """Non-hunter mob always returns False."""
        from world.combat_ai import attempt_hunter_chase

        mob = _make_mob()
        mob.db.is_hunter = False

        target = _make_player()
        result = attempt_hunter_chase(mob, target, MagicMock())

        self.assertFalse(result)
