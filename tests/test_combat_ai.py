"""
Tests for mob combat AI (world/combat_ai.py).

Covers weighted ability selection, cooldown filtering, condition vocabulary,
targeting priority, vanish skip, and scripted sequences (CMB-03).
Uses unittest.TestCase + MagicMock (no Evennia DB required).
"""

import unittest
from unittest.mock import MagicMock, patch


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
    ch.ndb.round_number = round_number
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
        mob = _make_mob()

        # Target at full HP -- condition should fail, fall back to basic attack
        player = _make_player(hp=100, hp_max=200)
        ch = _make_combat_handler(players=[player])
        action = select_mob_action(mob, player, ch)
        self.assertEqual(action["type"], "basic_attack")

        # Target at low HP -- condition should pass
        player.ndb.hp = 50  # below 50% of 200
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
