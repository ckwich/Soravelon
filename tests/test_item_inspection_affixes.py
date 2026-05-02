"""Tests for item inspection display of generated equipment affixes."""

import unittest


class _DbStub:
    def __init__(self, **values):
        self._values = values

    def __getattr__(self, name):
        return self._values.get(name)


class _ItemStub:
    def __init__(self, key, **db_values):
        self.key = key
        self.db = _DbStub(**db_values)


class TestItemInspectionAffixes(unittest.TestCase):
    """Generated affixes and provenance should be visible to appraisal."""

    def test_item_stats_include_equipment_affixes(self):
        from commands.cmd_inspect import _get_item_stats

        item = _ItemStub(
            "Balanced test blade",
            damage_min=8,
            damage_max=17,
            armor_value=0,
            stat_bonuses={"agility": 2},
            equipment_slot="main_hand",
            rarity="magic",
            value_scales=46,
            material_tier=2,
            weapon_family="blade",
            equipment_affixes=[
                {"id": "balanced", "name": "Balanced"},
                {"id": "keen", "name": "Keen"},
            ],
            drop_provenance={"source_name": "Test Raider"},
        )

        stats = _get_item_stats(item)

        self.assertEqual(stats["Weapon Family"], "Blades")
        self.assertEqual(stats["Affixes"], "Balanced, Keen")
        self.assertEqual(stats["Recovered From"], "Test Raider")
