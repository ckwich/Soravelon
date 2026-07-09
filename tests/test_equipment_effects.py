"""Behavior contracts for equipped combat and base-stat effects."""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest

from world.models import InventoryItem


class TestEquipmentEffectAggregation(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.char1.db.base_stats = {
            "strength": 10,
            "agility": 10,
            "endurance": 10,
            "mana": 10,
            "acuity": 10,
            "presence": 10,
            "resonance": 10,
        }
        self.char1.db.backend_level = 1

    def _make_equipment(
        self,
        key,
        slot,
        *,
        equipped=True,
        bonuses=None,
        armor=0,
    ):
        from typeclasses.objects import SoravelonEquipment

        item = create_object(
            SoravelonEquipment,
            key=key,
            location=self.char1,
        )
        item.db.equipment_slot = slot
        item.db.stat_bonuses = bonuses or {}
        item.db.armor_value = armor
        InventoryItem.objects.create(
            character_id=self.char1.id,
            item_id=item.id,
            is_equipped=equipped,
            equipment_slot=slot if equipped else None,
        )
        return item

    def test_effective_stats_add_each_equipped_bonus_exactly_once(self):
        from world.equipment_effects import get_effective_stats

        self._make_equipment(
            "iron helm",
            "head",
            bonuses={"strength": 2, "endurance": 1},
        )
        self._make_equipment(
            "iron gauntlets",
            "hands",
            bonuses={"strength": 3},
        )
        self._make_equipment(
            "carried charm",
            "amulet",
            equipped=False,
            bonuses={"strength": 99},
        )
        self._make_equipment(
            "invalid domain charm",
            "back",
            bonuses={"combat": 99},
        )

        effective = get_effective_stats(self.char1)

        self.assertEqual(effective["strength"], 15)
        self.assertEqual(effective["endurance"], 11)
        self.assertNotIn("combat", effective)
        self.assertEqual(self.char1.db.base_stats["strength"], 10)

    def test_total_armor_sums_only_equipped_items(self):
        from world.equipment_effects import get_total_equipped_armor

        self._make_equipment("helm", "head", armor=4)
        self._make_equipment("breastplate", "chest", armor=8)
        self._make_equipment(
            "carried shield",
            "off_hand",
            equipped=False,
            armor=50,
        )

        self.assertEqual(get_total_equipped_armor(self.char1), 12)

    def test_derived_stats_consume_equipped_bonuses(self):
        from world.base_attributes import (
            derive_max_hp,
            derive_max_stamina,
            get_actions_per_turn,
            get_initiative,
        )

        self._make_equipment(
            "test harness",
            "chest",
            bonuses={"endurance": 2, "agility": 20},
        )

        self.assertEqual(derive_max_hp(self.char1), 120)
        self.assertEqual(derive_max_stamina(self.char1), 54)
        self.assertEqual(get_actions_per_turn(self.char1), 2)
        with patch("world.base_attributes.random.randint", return_value=1):
            self.assertEqual(get_initiative(self.char1), 31)

    def test_basic_attack_consumes_weapon_profile_and_bonus_once(self):
        from world.combat_engine import _compute_raw_damage

        weapon = self._make_equipment(
            "practice dagger",
            "main_hand",
            bonuses={"agility": 2},
        )
        weapon.db.damage_min = 10
        weapon.db.damage_max = 10
        weapon.db.scaling_stat = "agility"
        weapon.db.element = "physical"

        with patch(
            "world.weapon_skills.weapon_skill_damage_bonus_for_attack",
            return_value=0,
        ):
            damage, element = _compute_raw_damage(self.char1, weapon)

        self.assertEqual(damage, 16)
        self.assertEqual(element, "physical")

    def test_incoming_damage_consumes_persisted_equipped_armor(self):
        from world.combat_engine import _apply_incoming_damage

        self._make_equipment("test plate", "chest", armor=50)
        attacker = MagicMock()
        attacker.ndb.hp = 100
        self.char1.ndb.hp = 100
        self.char1.ndb.active_effects = []

        damage, absorbed, reflected = _apply_incoming_damage(
            attacker,
            self.char1,
            100,
        )

        self.assertEqual((damage, absorbed, reflected), (50, 0, 0))
        self.assertEqual(self.char1.ndb.hp, 50)

    def test_unequipping_endurance_clamps_current_resources_to_new_caps(self):
        from world.inventory_engine import unequip_item

        equipment = self._make_equipment(
            "endurance harness",
            "chest",
            bonuses={"endurance": 10},
        )
        self.char1.ndb.hp = 160
        self.char1.ndb.stamina = 70

        ok, message = unequip_item(self.char1, equipment)

        self.assertTrue(ok, message)
        self.assertEqual(self.char1.ndb.hp, 110)
        self.assertEqual(self.char1.ndb.stamina, 50)


class TestWeaponAndArmorFormulas(unittest.TestCase):
    def test_weapon_profile_uses_authored_base_stat_and_damage(self):
        from world.equipment_effects import get_weapon_damage_profile

        weapon = MagicMock()
        weapon.db.damage_min = 4
        weapon.db.damage_max = 10
        weapon.db.scaling_stat = "agility"
        weapon.db.element = "physical"

        profile = get_weapon_damage_profile(weapon)

        self.assertEqual(profile.minimum, 4)
        self.assertEqual(profile.maximum, 10)
        self.assertEqual(profile.scaling_stat, "agility")
        self.assertEqual(profile.element, "physical")

    def test_weapon_profile_rejects_domain_score_as_gear_scaling(self):
        from world.equipment_effects import get_weapon_damage_profile

        weapon = MagicMock()
        weapon.db.damage_min = 8
        weapon.db.damage_max = 14
        weapon.db.scaling_stat = "combat"
        weapon.db.element = "physical"

        self.assertEqual(
            get_weapon_damage_profile(weapon).scaling_stat,
            "strength",
        )

    def test_unarmed_profile_preserves_existing_damage_path(self):
        from world.equipment_effects import get_weapon_damage_profile

        profile = get_weapon_damage_profile(None)

        self.assertEqual((profile.minimum, profile.maximum), (3, 6))
        self.assertEqual(profile.scaling_stat, "strength")
        self.assertEqual(profile.element, "physical")

    def test_non_finite_weapon_damage_falls_back_safely(self):
        from world.equipment_effects import get_weapon_damage_profile

        weapon = MagicMock()
        weapon.db.damage_min = float("nan")
        weapon.db.damage_max = float("inf")
        weapon.db.scaling_stat = "strength"
        weapon.db.element = "physical"

        profile = get_weapon_damage_profile(weapon)

        self.assertEqual((profile.minimum, profile.maximum), (3, 6))

    def test_armor_curve_is_diminishing_and_hard_capped(self):
        from world.equipment_effects import (
            apply_armor_mitigation,
            get_armor_mitigation,
        )

        self.assertEqual(get_armor_mitigation(0), 0.0)
        self.assertAlmostEqual(get_armor_mitigation(50), 0.5)
        self.assertEqual(get_armor_mitigation(500), 0.75)
        first_ten = get_armor_mitigation(10) - get_armor_mitigation(0)
        second_ten = get_armor_mitigation(20) - get_armor_mitigation(10)
        self.assertGreater(first_ten, second_ten)
        self.assertEqual(apply_armor_mitigation(100, 50), 50)
        self.assertEqual(apply_armor_mitigation(100, 500), 25)

    def test_low_armor_does_not_gain_a_full_point_from_integer_flooring(self):
        from world.equipment_effects import apply_armor_mitigation

        self.assertEqual(apply_armor_mitigation(10, 1), 10)

    def test_npc_without_base_stats_never_queries_player_inventory(self):
        from world.equipment_effects import (
            get_effective_stats,
            get_total_equipped_armor,
        )

        npc = SimpleNamespace(db=SimpleNamespace(base_stats=None), id=99)
        with patch(
            "world.inventory_engine.get_equipped_items",
            side_effect=AssertionError("NPC inventory queried"),
        ):
            self.assertEqual(get_effective_stats(npc), {})
            self.assertEqual(get_total_equipped_armor(npc), 0)

    def test_npc_with_base_stats_still_never_queries_player_inventory(self):
        from world.equipment_effects import (
            get_effective_stats,
            get_total_equipped_armor,
        )

        class _NpcTags:
            def has(self, key, category=None):
                return False

        npc = SimpleNamespace(
            db=SimpleNamespace(base_stats={"strength": 22}),
            id=99,
            tags=_NpcTags(),
        )
        with patch(
            "world.inventory_engine.get_equipped_items",
            side_effect=AssertionError("NPC inventory queried"),
        ):
            self.assertEqual(get_effective_stats(npc), {"strength": 22})
            self.assertEqual(get_total_equipped_armor(npc), 0)


if __name__ == "__main__":
    unittest.main()
