"""
Tests for the combat engine (world/combat_engine.py).

Covers basic attack resolution, ability damage, elite/boss scaling,
zone scaling integration, resistance, corpse locking, and death handling.
Uses unittest.TestCase + MagicMock (no Evennia DB required).
"""

import unittest
from types import SimpleNamespace
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

        with patch("world.skill_engine.get_skill_value", return_value=0):
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
        ) as mock_scale, patch(
            "world.skill_engine.get_skill_value",
            return_value=0,
        ):
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

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    def test_weapon_family_skill_adds_modest_damage_bonus(self, mock_res, mock_scale, mock_crit):
        """A matching weapon-family skill slightly improves basic attack damage."""
        from world.combat_engine import resolve_basic_attack

        player = _make_player(strength=10)
        mob = _make_mob()
        weapon = MagicMock()
        weapon.key = "Practice Sword"
        weapon.db.damage_min = 10
        weapon.db.damage_max = 10
        weapon.db.element = "physical"
        weapon.db.weapon_family = "blade"

        with patch("world.skill_engine.get_skill_value", return_value=100), \
             patch("world.skill_engine.accumulate_skill_use") as mock_accumulate:
            ok, msg, dmg = resolve_basic_attack(player, mob, weapon=weapon)

        self.assertTrue(ok)
        self.assertIn("TestPlayer", msg)
        self.assertEqual(dmg, 16)
        mock_accumulate.assert_any_call(player, "weapon_blades")

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    def test_unarmed_basic_attack_accumulates_unarmed_skill(self, mock_res, mock_scale, mock_crit):
        """Bare-handed basic attacks should still train the unarmed family."""
        from world.combat_engine import resolve_basic_attack

        player = _make_player(strength=10)
        mob = _make_mob()

        with patch("world.skill_engine.get_skill_value", return_value=0), \
             patch("world.skill_engine.accumulate_skill_use") as mock_accumulate:
            ok, _, _ = resolve_basic_attack(player, mob, weapon=None)

        self.assertTrue(ok)
        mock_accumulate.assert_any_call(player, "weapon_unarmed")

    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    def test_weapon_uses_authored_scaling_stat_instead_of_strength(
        self,
        mock_res,
        mock_scale,
    ):
        from world.combat_engine import resolve_basic_attack

        player = _make_player(strength=100, agility=10)
        mob = _make_mob()
        weapon = MagicMock()
        weapon.key = "Practice Dagger"
        weapon.db.damage_min = 10
        weapon.db.damage_max = 10
        weapon.db.scaling_stat = "agility"
        weapon.db.element = "physical"
        weapon.db.weapon_family = "blade"

        with patch(
            "world.equipment_effects.get_effective_stats",
            return_value=player.db.base_stats,
        ) as mock_effective_stats, patch(
            "world.combat_engine.random.random",
            return_value=1.0,
        ), patch(
            "world.weapon_skills.weapon_skill_damage_bonus_for_attack",
            return_value=0,
        ), patch("world.weapon_skills.accumulate_weapon_skill_for_attack"):
            ok, _, damage = resolve_basic_attack(player, mob, weapon=weapon)

        self.assertTrue(ok)
        self.assertEqual(damage, 15)
        mock_effective_stats.assert_called_once_with(player)

    def test_mob_raw_damage_retains_inventory_free_path(self):
        from world.combat_engine import _compute_raw_damage

        mob = _make_mob(ref_min=12, ref_max=12)
        with patch(
            "world.equipment_effects.get_effective_stats",
            side_effect=AssertionError("mob effective equipment queried"),
        ), patch(
            "world.equipment_effects.get_weapon_damage_profile",
            side_effect=AssertionError("mob weapon equipment queried"),
        ):
            damage, element = _compute_raw_damage(mob, weapon=None)

        self.assertEqual(damage, 12)
        self.assertEqual(element, "physical")


class TestEquipmentArmorInCombat(unittest.TestCase):
    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_mob_damage_for_player", return_value=(20, 20))
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    @patch("world.equipment_effects.get_total_equipped_armor", return_value=50)
    def test_player_equipped_armor_mitigates_incoming_damage(
        self,
        mock_armor,
        mock_resistance,
        mock_scale,
        mock_crit,
    ):
        from world.combat_engine import resolve_basic_attack

        mob = _make_mob(ref_min=20, ref_max=20)
        player = _make_player()

        ok, _, damage = resolve_basic_attack(mob, player)

        self.assertTrue(ok)
        self.assertEqual(damage, 10)
        mock_armor.assert_called_once_with(player)

    def test_mob_target_does_not_query_player_equipment_armor(self):
        from world.combat_engine import _apply_incoming_damage

        attacker = _make_player()
        mob = _make_mob(hp=80)
        with patch(
            "world.equipment_effects.get_total_equipped_armor",
            side_effect=AssertionError("mob armor inventory queried"),
        ):
            damage, absorbed, reflected = _apply_incoming_damage(
                attacker,
                mob,
                20,
            )

        self.assertEqual((damage, absorbed, reflected), (20, 0, 0))


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

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: int(d * 0.5))
    def test_piercing_bypasses_resistance(self, mock_res, mock_scale, mock_crit):
        from world.combat_engine import resolve_ability_damage

        player = _make_player()
        mob = _make_mob()
        ability = {
            "name": "Arcane Bolt",
            "scaling_primary": "combat",
            "element": "arcane",
            "effect_params": {"damage_base": 20, "piercing": True},
        }

        ok, _, dmg = resolve_ability_damage(player, ability, mob)

        self.assertTrue(ok)
        self.assertEqual(dmg, 24)

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    def test_ignores_armor_skips_reduction_and_absorb(self, mock_res, mock_scale, mock_crit):
        from world.combat_engine import resolve_ability_damage

        player = _make_player()
        mob = _make_mob()
        mob.ndb.active_effects = [
            {
                "type": "warding",
                "stacks": 1,
                "duration": 3,
                "magnitude": 0.5,
                "source_id": None,
                "max_stacks": 1,
                "is_compound": False,
                "data": {"value": 0.5},
            },
            {
                "type": "damage_absorb",
                "stacks": 1,
                "duration": 3,
                "magnitude": 10,
                "source_id": None,
                "max_stacks": 1,
                "is_compound": False,
                "data": {"remaining": 10},
            },
        ]
        ability = {
            "name": "Truth Strike",
            "scaling_primary": "combat",
            "element": "physical",
            "effect_params": {"damage_base": 20, "ignores_armor": True},
        }

        ok, _, dmg = resolve_ability_damage(player, ability, mob)

        self.assertTrue(ok)
        self.assertEqual(dmg, 24)
        self.assertEqual(mob.ndb.active_effects[1]["data"]["remaining"], 10)

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    def test_echo_scaling_rewards_accumulated_lore(self, mock_res, mock_scale, mock_crit):
        from world.combat_engine import resolve_ability_damage

        low_player = _make_player()
        high_player = _make_player()
        low_player.ndb.domain_resource = {"type": "echoes", "current": 0, "max": 100}
        high_player.ndb.domain_resource = {"type": "echoes", "current": 40, "max": 100}
        high_player.db.echoes_investigation_bonus = {"amount": 20}
        mob = _make_mob()
        ability = {
            "name": "Unbroken Memory",
            "scaling_primary": "combat",
            "element": "physical",
            "effect_params": {"damage_base": 20, "echo_scaling": True},
        }

        _, _, low_dmg = resolve_ability_damage(low_player, ability, mob)
        mob.ndb.hp = 80
        _, _, high_dmg = resolve_ability_damage(high_player, ability, mob)

        self.assertGreater(high_dmg, low_dmg)

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    def test_ability_aggregates_equipment_once_for_all_scaling_stats(
        self,
        mock_res,
        mock_scale,
        mock_crit,
    ):
        from world.combat_engine import resolve_ability_damage

        player = _make_player()
        mob = _make_mob()
        ability = {
            "name": "Coordinated Strike",
            "damage_base": 20,
            "scaling_primary": "combat",
            "scaling_secondary": "tactics",
            "element": "physical",
        }
        with patch(
            "world.equipment_effects.get_effective_stats",
            return_value=player.db.base_stats,
        ) as mock_effective_stats:
            ok, _, _damage = resolve_ability_damage(player, ability, mob)

        self.assertTrue(ok)
        mock_effective_stats.assert_called_once_with(player)

    @patch("world.combat_engine.roll_crit", return_value=(False, 1.0))
    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, m, c: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, e, t: d)
    def test_guaranteed_crit_attack_buff_is_consumed_on_hit(self, mock_res, mock_scale, mock_crit):
        from world.combat_engine import resolve_ability_damage
        from world.status_effects import apply_effect

        player = _make_player()
        player.ndb.domain_resource = {"type": "momentum", "current": 50, "max": 100}
        mob = _make_mob()
        apply_effect(player, "guaranteed_crit", duration=1, data={})
        ability = {
            "name": "Ambush",
            "scaling_primary": "combat",
            "element": "physical",
            "effect_params": {"damage_base": 20},
        }

        ok, _, dmg = resolve_ability_damage(player, ability, mob)

        self.assertTrue(ok)
        self.assertEqual(dmg, 48)
        self.assertEqual(player.ndb.active_effects, [])


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

    def _make_corpse(self, killer_id=1, authorized_looter_ids=None, loot_phase="locked"):
        corpse = MagicMock()
        corpse.db.killer_id = killer_id
        corpse.db.authorized_looter_ids = authorized_looter_ids or []
        corpse.db.killer_group_leader_id = None
        corpse.db.loot_phase = loot_phase
        return corpse

    def _can_loot(self, corpse, character):
        """Inline can_loot logic matching CorpseContainer.can_loot."""
        phase = corpse.db.loot_phase or "locked"
        if phase == "decayed":
            return False, "Nothing remains here."
        if phase == "open":
            return True, ""
        authorized_ids = list(corpse.db.authorized_looter_ids or [])
        if authorized_ids:
            if character.id in authorized_ids:
                return True, ""
        elif character.id == corpse.db.killer_id:
            return True, ""
        return False, "This corpse's loot is still being claimed by the killer."

    def test_killer_can_loot(self):
        """Killer can access locked corpse."""
        corpse = self._make_corpse(killer_id=1, authorized_looter_ids=[1])
        char = MagicMock()
        char.id = 1
        char.ndb.group_leader_id = None
        ok, msg = self._can_loot(corpse, char)
        self.assertTrue(ok)

    def test_non_killer_blocked(self):
        """Non-killer blocked from locked corpse."""
        corpse = self._make_corpse(killer_id=1, authorized_looter_ids=[1])
        char = MagicMock()
        char.id = 99
        char.ndb.group_leader_id = None
        ok, msg = self._can_loot(corpse, char)
        self.assertFalse(ok)

    def test_group_member_can_loot(self):
        """Authorized group snapshot member can access locked corpse."""
        corpse = self._make_corpse(killer_id=1, authorized_looter_ids=[1, 2])
        char = MagicMock()
        char.id = 2  # not the killer
        char.ndb.group_leader_id = None
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
            mock_spawn.assert_called_once_with(
                mob,
                killer,
                authorized_looter_ids=[],
            )
            self.assertIn("slain", msg.lower())

    def test_mob_death_snapshots_participants_before_reward_generation(self):
        """The corpse lock and death lifecycle receive the same eligible roster."""
        from world.combat_engine import handle_mob_death

        mob = _make_mob()
        killer = _make_player()
        ally = _make_player()
        ally.id = 3
        corpse = MagicMock()
        corpse.id = 101

        with (
            patch(
                "world.encounter_rewards.snapshot_reward_recipients",
                return_value=[killer, ally],
            ),
            patch("world.combat_engine.spawn_corpse", return_value=corpse) as spawn,
            patch("world.combat_engine._move_room_loot_to_corpse"),
        ):
            handle_mob_death(mob, killer)

        spawn.assert_called_once_with(
            mob,
            killer,
            authorized_looter_ids=[killer.id, ally.id],
        )
        self.assertEqual(mob.ndb.encounter_reward_recipients, [killer, ally])
        self.assertIs(mob.ndb.encounter_reward_corpse, corpse)

    def test_spawn_corpse_stores_butcherable_mob_type_identity(self):
        """Corpse butcher identity should use mob_type, not the display name."""
        from world.combat_engine import spawn_corpse

        mob = _make_mob()
        mob.key = "Ash Wolf"
        mob.db.mob_type = "ash_wolf"
        mob.db.mob_template_key = "ash_wolf_hunter"
        killer = _make_player()

        corpse = MagicMock()
        corpse.id = 123
        with patch("world.group_engine.get_group_member_ids", return_value=[killer.id]), \
             patch("evennia.create_object", return_value=corpse), \
             patch("evennia.utils.delay"):
            result = spawn_corpse(mob, killer)

        self.assertIs(result, corpse)
        self.assertEqual(corpse.db.mob_key, "ash_wolf")
        self.assertNotEqual(corpse.db.mob_key, "Ash Wolf")

    def test_player_death_creates_corpse(self):
        """handle_player_death moves carried items to the corpse."""
        from world.combat_engine import handle_player_death

        player = _make_player()
        item1 = MagicMock()
        item1.id = 1
        item2 = MagicMock()
        item2.id = 2
        player.contents = [item1, item2]

        with patch("world.combat_engine._spawn_player_corpse") as mock_corpse, \
             patch(
                 "world.inventory_engine.get_equipped_items",
                 return_value=[],
             ), \
             patch(
                 "world.inventory_engine.move_owned_items_to_world_container"
             ) as mock_transfer, \
             patch("world.banking.on_character_death"):
            corpse = MagicMock()
            mock_corpse.return_value = corpse
            msg = handle_player_death(player)
            mock_corpse.assert_called_once()
            mock_transfer.assert_called_once_with(
                player,
                [item1, item2],
                corpse,
            )
            self.assertIn("fallen", msg.lower())

    def test_player_death_preserves_equipped_items(self):
        """Death drops carried possessions without stripping equipped gear."""
        from world.combat_engine import handle_player_death

        player = _make_player()
        equipped_item = MagicMock()
        equipped_item.id = 1
        carried_item = MagicMock()
        carried_item.id = 2
        player.contents = [equipped_item, carried_item]

        with patch("world.combat_engine._spawn_player_corpse") as mock_corpse, \
             patch(
                 "world.inventory_engine.get_equipped_items",
                 return_value=[(equipped_item, MagicMock())],
             ), \
             patch(
                 "world.inventory_engine.move_owned_items_to_world_container"
             ) as mock_transfer, \
             patch("world.banking.on_character_death"):
            corpse = MagicMock()
            mock_corpse.return_value = corpse

            handle_player_death(player)

            mock_transfer.assert_called_once_with(
                player,
                [carried_item],
                corpse,
            )

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


class TestRespawnHandling(unittest.TestCase):
    """Respawn routing and refresh behavior."""

    def _make_room(self, room_id, is_respawn=False):
        room = MagicMock()
        room.id = hash(room_id)
        room.key = room_id
        room.db = SimpleNamespace(zone_id="zone")
        room.exits = []

        def has_tag(key, category=None):
            return key == "respawn_point" and category == "spawn_point" and is_respawn

        def get_tag(category=None):
            if category == "room_id":
                return room_id
            return None

        room.tags.has.side_effect = has_tag
        room.tags.get.side_effect = get_tag
        return room

    def test_respawn_uses_nearest_reachable_respawn_point(self):
        from world.combat_engine import _respawn_player

        start = self._make_room("start")
        mid = self._make_room("mid")
        scenic = self._make_room("scenic")
        detour = self._make_room("detour")
        near_respawn = self._make_room("near_respawn", is_respawn=True)
        far_respawn = self._make_room("far_respawn", is_respawn=True)

        start.exits = [
            MagicMock(destination=mid),
            MagicMock(destination=scenic),
        ]
        mid.exits = [MagicMock(destination=near_respawn)]
        scenic.exits = [MagicMock(destination=detour)]
        detour.exits = [MagicMock(destination=far_respawn)]
        near_respawn.exits = []
        far_respawn.exits = []

        character = MagicMock()
        character.location = start
        character.home = None
        character.db.visited_room_ids = set()
        character.ndb.oob_debounce = {"map_update": 1.0}

        with patch("evennia.utils.search.search_tag", return_value=[far_respawn, near_respawn]), \
             patch("world.base_attributes.derive_max_hp", return_value=120), \
             patch("world.base_attributes.derive_max_stamina", return_value=80), \
             patch("world.oob_publisher.push_status_update"), \
             patch("world.oob_publisher.push_stat_update"), \
             patch("world.oob_publisher.push_map_update"), \
             patch("world.oob_publisher.push_inventory_update"):
            _respawn_player(character)

        character.move_to.assert_called_once_with(
            near_respawn, quiet=True, move_hooks=False
        )

    def test_respawn_refreshes_player_state_and_marks_room_visited(self):
        from world.combat_engine import _respawn_player

        death_room = self._make_room("death_room")
        respawn_room = self._make_room("respawn_room", is_respawn=True)
        death_room.exits = [MagicMock(destination=respawn_room)]
        respawn_room.exits = []

        character = MagicMock()
        character.location = death_room
        character.home = None
        character.db.visited_room_ids = set()
        character.ndb.oob_debounce = {"map_update": 1.0}

        with patch("evennia.utils.search.search_tag", return_value=[respawn_room]), \
             patch("world.base_attributes.derive_max_hp", return_value=120), \
             patch("world.base_attributes.derive_max_stamina", return_value=80), \
             patch("world.oob_publisher.push_status_update") as mock_push_status, \
             patch("world.oob_publisher.push_stat_update") as mock_push_stat, \
             patch("world.oob_publisher.push_map_update") as mock_push_map, \
             patch("world.oob_publisher.push_inventory_update") as mock_push_inventory:
            _respawn_player(character)

        self.assertEqual(character.ndb.hp, 30)
        self.assertEqual(character.ndb.stamina, 20)
        self.assertEqual(character.db.visited_room_ids, {"respawn_room"})
        self.assertEqual(character.ndb.oob_debounce, {})
        mock_push_status.assert_called_once_with(character)
        mock_push_stat.assert_called_once_with(character)
        mock_push_map.assert_called_once_with(character)
        mock_push_inventory.assert_called_once_with(character)
