"""Tests for broad weapon-family skill handling."""

import unittest
from unittest.mock import MagicMock


class TestWeaponFamilyRegistry(unittest.TestCase):
    """Weapon families should be real general skills, not ad-hoc metadata."""

    def test_weapon_family_skills_are_registered_general_skills(self):
        from world.skill_definitions import SKILL_DEFINITIONS
        from world.weapon_skills import WEAPON_FAMILY_SKILLS

        expected_families = {
            "blade",
            "axe",
            "hafted",
            "polearm",
            "bow",
            "thrown",
            "staff",
            "shield",
            "unarmed",
        }
        self.assertEqual(set(WEAPON_FAMILY_SKILLS), expected_families)

        for family, config in WEAPON_FAMILY_SKILLS.items():
            skill_id = config["skill_id"]
            self.assertIn(skill_id, SKILL_DEFINITIONS, family)
            definition = SKILL_DEFINITIONS[skill_id]
            self.assertEqual(definition["skill_type"], "general")
            self.assertIn("weapon", definition["description"].lower())
            self.assertIn(25, definition["thresholds"])
            self.assertIn(100, definition["thresholds"])

    def test_weapon_skill_damage_bonus_is_modest_and_capped(self):
        from world.weapon_skills import weapon_skill_damage_bonus

        self.assertEqual(weapon_skill_damage_bonus(0), 0.0)
        self.assertAlmostEqual(weapon_skill_damage_bonus(50), 0.05)
        self.assertAlmostEqual(weapon_skill_damage_bonus(100), 0.10)
        self.assertAlmostEqual(weapon_skill_damage_bonus(150), 0.10)


class TestWeaponFamilyInference(unittest.TestCase):
    """Existing items should work even before builders add explicit families."""

    def test_explicit_weapon_family_normalizes_to_family_and_skill(self):
        from world.weapon_skills import (
            infer_weapon_family_from_item,
            weapon_skill_for_item,
        )

        weapon = MagicMock()
        weapon.key = "Training Sword"
        weapon.db.weapon_family = "Blades"

        self.assertEqual(infer_weapon_family_from_item(weapon), "blade")
        self.assertEqual(weapon_skill_for_item(weapon), "weapon_blades")

    def test_static_catalog_weapons_infer_from_authored_names(self):
        from world.item_catalog import CATALOG
        from world.weapon_skills import infer_weapon_family_from_item

        cases = {
            "iron_sword": "blade",
            "iron_dagger": "blade",
            "iron_mace": "hafted",
            "iron_staff": "staff",
            "iron_greataxe": "axe",
            "iron_bow": "bow",
        }
        for item_id, expected_family in cases.items():
            self.assertEqual(
                infer_weapon_family_from_item(CATALOG[item_id]),
                expected_family,
                item_id,
            )

    def test_throwing_weapon_text_prefers_thrown_over_blade(self):
        from world.weapon_skills import infer_weapon_family_from_item

        item_def = {
            "item_id": "throwing_knife",
            "key": "Throwing Knife",
            "item_type": "equipment",
            "equip_slot": "main_hand",
            "damage_min": 2,
            "damage_max": 5,
        }

        self.assertEqual(infer_weapon_family_from_item(item_def), "thrown")

    def test_non_weapon_item_has_no_weapon_family(self):
        from world.weapon_skills import infer_weapon_family_from_item

        item_def = {
            "item_id": "apple",
            "key": "apple",
            "item_type": "item",
        }

        self.assertIsNone(infer_weapon_family_from_item(item_def))

    def test_attack_without_weapon_uses_unarmed_skill(self):
        from world.weapon_skills import weapon_skill_for_attack

        self.assertEqual(weapon_skill_for_attack(None), "weapon_unarmed")
