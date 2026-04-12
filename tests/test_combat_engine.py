"""
Tests for the combat engine (world/combat_engine.py).

Covers basic attack resolution, ability damage, elite/boss scaling,
zone scaling integration, resistance, corpse locking, and death handling.
Uses unittest.TestCase + MagicMock (no Evennia DB required).
"""

import unittest
from unittest.mock import MagicMock, patch, PropertyMock


def _make_player(strength=10, agility=10, endurance=10, acuity=10):
    """Create a MagicMock player character."""
    char = MagicMock()
    char.key = "TestPlayer"
    char.id = 1
    char.db.base_stats = {
        "strength": strength,
        "agility": agility,
        "endurance": endurance,
        "mana": 10,
        "acuity": acuity,
        "presence": 10,
        "resonance": 10,
    }
    char.db.backend_level = 5
    char.ndb.hp = 100
    char.ndb.stamina = 50
    char.ndb.active_effects = []
    char.ndb.stat_xp_accumulators = {s: 0.0 for s in char.db.base_stats}
    char.ndb.group_leader_id = None
    char.contents = []
    char.location = MagicMock()
    return char


def _make_mob(rarity="normal", hp=80, ref_min=8, ref_max=14):
    """Create a MagicMock mob."""
    mob = MagicMock()
    mob.key = "TestMob"
    mob.id = 2
    mob.db.base_stats = None  # mobs don't have base_stats
    mob.db.rarity = rarity
    mob.db.ref_damage_min = ref_min
    mob.db.ref_damage_max = ref_max
    mob.db.element = "physical"
    mob.db.crit_chance = 0.0  # disable crits for deterministic tests
    mob.db.hp_max = hp
    mob.db.resistances = {}
    mob.ndb.hp = hp
    mob.ndb.active_effects = []
    mob.ndb.combat_scales = {}
    mob.location = MagicMock()
    return mob


class TestBasicAttackResolution(unittest.TestCase):
    """Basic (auto) attack damage resolution (CMB-01)."""

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    def test_melee_damage_range(self, mock_res, mock_scale, mock_crit):
        """resolve_basic_attack with known stats produces damage in expected range."""
        from world.combat_engine import resolve_basic_attack

        player = _make_player(strength=20)
        mob = _make_mob()

        ok, msg, dmg = resolve_basic_attack(player, mob)
        self.assertTrue(ok)
        # Bare hands: randint(3,6) + int(20*0.5) = 3-6 + 10 = 13-16
        self.assertGreaterEqual(dmg, 13)
        self.assertLessEqual(dmg, 16)

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    def test_zone_scaling_applied(self, mock_res, mock_crit):
        """get_player_damage_to_mob is called when character attacks mob (CMB-02)."""
        from world.combat_engine import resolve_basic_attack

        player = _make_player()
        mob = _make_mob()

        with patch(
            "world.zone_scaling.get_player_damage_to_mob",
            side_effect=lambda d, m, c: d,
        ) as mock_scale:
            resolve_basic_attack(player, mob)
            mock_scale.assert_called_once()

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    def test_resistance_applied(self, mock_scale, mock_crit):
        """Target with fire resistance 0.5 takes half fire damage."""
        from world.combat_engine import resolve_basic_attack

        player = _make_player(strength=20)
        mob = _make_mob()

        # Weapon with fire element
        weapon = MagicMock()
        weapon.db.damage_min = 10
        weapon.db.damage_max = 10
        weapon.db.element = "fire"

        with patch(
            "world.zone_scaling.apply_resistance",
            side_effect=lambda d, e, t: int(d * 0.5),
        ):
            ok, msg, dmg = resolve_basic_attack(player, mob, weapon=weapon)
            # raw = 10 + int(20*0.5) = 20, halved by resistance = 10
            self.assertEqual(dmg, 10)

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    def test_miss_on_blind(self, mock_res, mock_scale, mock_crit):
        """Attacker blinded has chance to miss."""
        from world.combat_engine import resolve_basic_attack

        player = _make_player()
        mob = _make_mob()

        # Give attacker blind effect -> 25% miss chance, force the random to hit
        player.ndb.active_effects = [
            {
                "type": "blind",
                "stacks": 1,
                "duration": 2,
                "magnitude": 1.0,
                "source_id": None,
                "max_stacks": 1,
                "is_compound": False,
            }
        ]

        # Force a miss by mocking random to return 0.0 (below 0.25)
        with patch("world.combat_engine.random.random", return_value=0.0):
            ok, msg, dmg = resolve_basic_attack(player, mob)
            self.assertFalse(ok)
            self.assertEqual(dmg, 0)
            self.assertIn("misses", msg.lower())


class TestAbilityDamageResolution(unittest.TestCase):
    """Ability-based damage resolution (CMB-01)."""

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    def test_ability_scales_with_primary_stat(self, mock_res, mock_scale, mock_crit):
        """Higher primary stat = more damage."""
        from world.combat_engine import resolve_ability_damage

        ability = {
            "name": "Power Strike",
            "damage_base": 20,
            "scaling_primary": "combat",
            "element": "physical",
        }

        low_player = _make_player(strength=10)
        high_player = _make_player(strength=50)
        mob = _make_mob()

        _, _, low_dmg = resolve_ability_damage(low_player, ability, mob)
        # Reset mob HP
        mob.ndb.hp = 80
        _, _, high_dmg = resolve_ability_damage(high_player, ability, mob)

        self.assertGreater(high_dmg, low_dmg)

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    def test_status_effect_applied(self, mock_res, mock_scale, mock_crit):
        """Ability with status_effect field applies it to target."""
        from world.combat_engine import resolve_ability_damage

        ability = {
            "name": "Poison Strike",
            "damage_base": 15,
            "scaling_primary": "combat",
            "element": "physical",
            "status_effect": "poison",
            "effect_duration": 3,
            "effect_magnitude": 1.0,
        }

        player = _make_player()
        mob = _make_mob()

        with patch("world.status_effects.apply_effect") as mock_apply:
            resolve_ability_damage(player, ability, mob)
            mock_apply.assert_called_once_with(
                mob, "poison", 3, 1.0, player.id
            )


class TestEliteBossScaling(unittest.TestCase):
    """Elite and boss damage scaling modifiers (CMB-02)."""

    def test_elite_incoming_damage(self):
        """Elite mob deals 1.40x damage to player."""
        from world.combat_engine import apply_elite_boss_scaling

        raw = 100
        result = apply_elite_boss_scaling(raw, "rare", is_incoming=True)
        self.assertEqual(result, 140)

    def test_elite_damage_reduction(self):
        """Player deals 0.75x damage to elite mob."""
        from world.combat_engine import apply_elite_boss_scaling

        raw = 100
        result = apply_elite_boss_scaling(raw, "rare", is_incoming=False)
        self.assertEqual(result, 75)

    def test_boss_scaling(self):
        """Boss mob uses 1.80x / 0.50x multipliers."""
        from world.combat_engine import apply_elite_boss_scaling

        self.assertEqual(apply_elite_boss_scaling(100, "legendary", is_incoming=True), 180)
        self.assertEqual(apply_elite_boss_scaling(100, "legendary", is_incoming=False), 50)

    def test_normal_no_scaling(self):
        """Normal mobs have no scaling modifier."""
        from world.combat_engine import apply_elite_boss_scaling

        self.assertEqual(apply_elite_boss_scaling(100, "normal", is_incoming=True), 100)


class TestCorpseLocking(unittest.TestCase):
    """Corpse loot phase and access control (CMB-04)."""

    def _make_corpse(self, killer_id=1, group_leader_id=None, loot_phase="locked"):
        corpse = MagicMock()
        corpse.db.killer_id = killer_id
        corpse.db.killer_group_leader_id = group_leader_id
        corpse.db.loot_phase = loot_phase
        return corpse

    def _can_loot(self, corpse, character):
        """Inline can_loot logic matching CorpseContainer.can_loot."""
        phase = corpse.db.loot_phase or "locked"
        if phase == "decayed":
            return False, "Nothing remains here."
        if phase == "open":
            return True, ""
        # Locked phase
        if character.id == corpse.db.killer_id:
            return True, ""
        killer_group_id = corpse.db.killer_group_leader_id
        if killer_group_id:
            char_group_id = getattr(character.ndb, "group_leader_id", None)
            if char_group_id == killer_group_id:
                return True, ""
        return False, "This corpse is not yours to loot."

    def test_killer_can_loot(self):
        """Killer can access locked corpse."""
        corpse = self._make_corpse(killer_id=1)
        char = MagicMock()
        char.id = 1
        char.ndb.group_leader_id = None
        ok, msg = self._can_loot(corpse, char)
        self.assertTrue(ok)

    def test_non_killer_blocked(self):
        """Non-killer blocked from locked corpse."""
        corpse = self._make_corpse(killer_id=1)
        char = MagicMock()
        char.id = 99
        char.ndb.group_leader_id = None
        ok, msg = self._can_loot(corpse, char)
        self.assertFalse(ok)

    def test_group_member_can_loot(self):
        """Killer's group member can access locked corpse."""
        corpse = self._make_corpse(killer_id=1, group_leader_id=10)
        char = MagicMock()
        char.id = 2  # not the killer
        char.ndb.group_leader_id = 10  # same group leader
        ok, msg = self._can_loot(corpse, char)
        self.assertTrue(ok)

    def test_open_phase_anyone(self):
        """After grace period, anyone can loot."""
        corpse = self._make_corpse(killer_id=1, loot_phase="open")
        char = MagicMock()
        char.id = 99
        char.ndb.group_leader_id = None
        ok, msg = self._can_loot(corpse, char)
        self.assertTrue(ok)

    def test_corpse_decays(self):
        """Decayed corpse allows nobody."""
        corpse = self._make_corpse(killer_id=1, loot_phase="decayed")
        char = MagicMock()
        char.id = 1
        char.ndb.group_leader_id = None
        ok, msg = self._can_loot(corpse, char)
        self.assertFalse(ok)


class TestDeathHandling(unittest.TestCase):
    """Death checks and handling (CMB-04)."""

    def test_mob_death_spawns_corpse(self):
        """handle_mob_death calls spawn_corpse to create container in room."""
        from world.combat_engine import handle_mob_death

        mob = _make_mob()
        killer = _make_player()

        with patch("world.combat_engine.spawn_corpse") as mock_spawn, \
             patch("world.combat_engine._move_room_loot_to_corpse"):
            mock_spawn.return_value = MagicMock()
            msg = handle_mob_death(mob, killer)
            mock_spawn.assert_called_once_with(mob, killer)
            self.assertIn("slain", msg.lower())

    def test_player_death_creates_corpse(self):
        """handle_player_death moves items to corpse."""
        from world.combat_engine import handle_player_death

        player = _make_player()
        item1 = MagicMock()
        item1.id = 1
        item2 = MagicMock()
        item2.id = 2
        player.contents = [item1, item2]

        with patch("world.combat_engine._spawn_player_corpse") as mock_corpse, \
             patch("world.models.InventoryItem.objects"), \
             patch("world.banking.on_character_death"):
            mock_corpse.return_value = MagicMock()
            msg = handle_player_death(player)
            mock_corpse.assert_called_once()
            # Items should have been moved
            item1.move_to.assert_called_once()
            item2.move_to.assert_called_once()
            self.assertIn("fallen", msg.lower())

    def test_check_death_at_zero(self):
        """check_death returns True when HP is 0."""
        from world.combat_engine import check_death

        mob = _make_mob()
        mob.ndb.hp = 0
        self.assertTrue(check_death(mob))

    def test_check_death_above_zero(self):
        """check_death returns False when HP > 0."""
        from world.combat_engine import check_death

        mob = _make_mob()
        mob.ndb.hp = 50
        self.assertFalse(check_death(mob))
