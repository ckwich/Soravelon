"""
Tests for equipment archetypes and random affix expansion.

The system should let loot tables reference reusable gear bases while keeping
area-authored drop entries as plain builder-safe dicts.
"""

import random
import unittest
from unittest.mock import MagicMock, patch


class TestEquipmentArchetypeBuilder(unittest.TestCase):
    """build_equipment_from_archetype expands a literal drop entry."""

    def test_agile_blade_expands_with_deterministic_affix(self):
        from world.equipment_archetypes import (
            EQUIPMENT_AFFIX_PROFILES,
            build_equipment_from_archetype,
        )

        drop = {
            "item_id": "test_blade",
            "key": "test blade",
            "item_type": "equipment",
            "equipment_archetype": "agile_blade",
            "affix_profile": "test_balanced_only",
            "affix_count_by_tier": [1, 1, 1, 1, 1],
            "value_by_tier": [10, 20, 40, 80, 160],
            "rarity_by_tier": ["normal", "normal", "magic", "rare", "rare"],
            "desc_by_tier": [
                "A plain test blade.",
                "A serviceable test blade.",
                "A well-kept test blade.",
                "A fine test blade.",
                "An exceptional test blade.",
            ],
        }

        with patch.dict(EQUIPMENT_AFFIX_PROFILES, {
            "test_balanced_only": {
                "affixes": [{"id": "balanced", "weight": 1}],
            }
        }):
            item = build_equipment_from_archetype(
                drop,
                tier=3,
                rng=random.Random(7),
                source={"mob_key": "Test Raider", "zone_id": "test_zone"},
            )

        self.assertEqual(item["item_id"], "test_blade")
        self.assertEqual(item["item_type"], "equipment")
        self.assertEqual(item["equip_slot"], "main_hand")
        self.assertEqual(item["weapon_family"], "blade")
        self.assertEqual(item["scaling_stat"], "agility")
        self.assertEqual(item["material_tier"], 2)
        self.assertEqual(item["damage_min"], 8)
        self.assertEqual(item["damage_max"], 17)
        self.assertEqual(item["stat_bonuses"], {"agility": 2})
        self.assertEqual(item["rarity"], "magic")
        self.assertEqual(item["equipment_affixes"][0]["id"], "balanced")
        self.assertIn("Balanced", item["key"])
        self.assertIn("balance invites", item["desc"])
        self.assertEqual(item["drop_provenance"]["source_name"], "Test Raider")

    def test_unknown_archetype_raises_clear_error(self):
        from world.equipment_archetypes import (
            EquipmentArchetypeError,
            build_equipment_from_archetype,
        )

        drop = {
            "item_id": "bad",
            "key": "bad",
            "equipment_archetype": "missing_archetype",
            "value_by_tier": [1, 1, 1, 1, 1],
            "rarity_by_tier": ["normal"] * 5,
            "desc_by_tier": ["bad"] * 5,
        }

        with self.assertRaisesRegex(EquipmentArchetypeError, "missing_archetype"):
            build_equipment_from_archetype(drop, tier=1)

    def test_affixes_do_not_duplicate_when_profile_has_repeats(self):
        from world.equipment_archetypes import (
            EQUIPMENT_AFFIX_PROFILES,
            build_equipment_from_archetype,
        )

        drop = {
            "item_id": "test_mail",
            "key": "test mail",
            "item_type": "equipment",
            "equipment_archetype": "guarded_mail",
            "affix_profile": "test_repeated_guarded",
            "affix_count_by_tier": [2, 2, 2, 2, 2],
            "value_by_tier": [10, 20, 40, 80, 160],
            "rarity_by_tier": ["normal", "normal", "magic", "rare", "rare"],
            "desc_by_tier": ["mail"] * 5,
        }

        with patch.dict(EQUIPMENT_AFFIX_PROFILES, {
            "test_repeated_guarded": {
                "affixes": [
                    {"id": "guarded", "weight": 10},
                    {"id": "guarded", "weight": 10},
                    {"id": "resilient", "weight": 1},
                ],
            }
        }):
            item = build_equipment_from_archetype(
                drop,
                tier=4,
                rng=random.Random(11),
            )

        affix_ids = [affix["id"] for affix in item["equipment_affixes"]]
        self.assertEqual(sorted(affix_ids), ["guarded", "resilient"])
        self.assertGreater(item["armor_value"], 0)


class TestLootTableArchetypeIntegration(unittest.TestCase):
    """roll_loot can expand archetype-backed drops."""

    def test_roll_loot_expands_equipment_archetype_drop(self):
        from world.equipment_archetypes import EQUIPMENT_AFFIX_PROFILES
        from world.loot_tables import LOOT_TABLES, roll_loot

        mob = MagicMock()
        mob.key = "Test Raider"
        mob.db.mob_type = "archetype_test_raider"
        mob.db.loot_table = None
        mob.db.rarity = "normal"
        mob.location = None

        killer = MagicMock()
        killer.db.domain_scores = {"combat": 60}

        table = {
            "mob_type": "archetype_test_raider",
            "relevant_skill": "combat",
            "base_drop_chance": 1.0,
            "drops": [{
                "item_id": "test_raider_blade",
                "key": "test raider blade",
                "item_type": "equipment",
                "equipment_archetype": "agile_blade",
                "affix_profile": "test_balanced_only",
                "affix_count_by_tier": [1, 1, 1, 1, 1],
                "weight_in_pool": 1,
                "value_by_tier": [10, 20, 40, 80, 160],
                "rarity_by_tier": ["normal", "normal", "magic", "rare", "rare"],
                "desc_by_tier": ["blade"] * 5,
            }],
        }

        with patch.dict(LOOT_TABLES, {"archetype_test_raider": table}):
            with patch.dict(EQUIPMENT_AFFIX_PROFILES, {
                "test_balanced_only": {
                    "affixes": [{"id": "balanced", "weight": 1}],
                }
            }):
                drops = roll_loot(mob, killer)

        self.assertEqual(len(drops), 1)
        item = drops[0]
        self.assertEqual(item["item_type"], "equipment")
        self.assertEqual(item["equip_slot"], "main_hand")
        self.assertEqual(item["weapon_family"], "blade")
        self.assertIn("equipment_affixes", item)
        self.assertEqual(item["drop_provenance"]["source_name"], "Test Raider")
