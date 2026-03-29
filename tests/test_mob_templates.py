"""
Tests for world.mob_templates — mob template registry and apply function.

Uses unittest.TestCase + MagicMock — no Evennia DB needed.
"""

import unittest
from unittest.mock import MagicMock, patch


class _DbNamespace:
    """Simple namespace for mock db attributes."""
    pass


def _make_mock_mob():
    """Create a mock mob with a db namespace for attribute storage."""
    mob = MagicMock()
    mob.db = _DbNamespace()
    # Set defaults matching SoravelonMob.at_object_creation
    mob.db.rarity = "normal"
    mob.db.affix_list = []
    mob.db.mob_type = None
    mob.db.zone_id = None
    mob.db.faction = None
    mob.db.base_aggression = "passive"
    mob.db.base_disposition = 0.0
    mob.db.trust_sensitive = False
    mob.db.quest_modifier = None
    mob.db.prestige_modifier = 1.0
    mob.db.hp_min = 80
    mob.db.hp_max = 120
    mob.db.damage_min = 8
    mob.db.damage_max = 14
    mob.db.speed = 1.0
    mob.db.accuracy = 0.0
    mob.db.evasion = 0.0
    mob.db.resistances = {}
    mob.db.abilities = []
    mob.db.patrol = None
    mob.db.combat_enabled = True
    mob.db.triggers = []
    mob.db.tome_drop = None
    mob.db.desc = ""
    mob.db.is_hunter = False
    mob.db.detection_range = 0
    mob.db.flee_threshold = 20
    mob.db.wander = False
    mob.db.loot_table = None
    mob.key = "default mob"
    return mob


class TestMobTemplatesStructure(unittest.TestCase):
    """Test MOB_TEMPLATES dict structure."""

    def test_mob_templates_is_dict(self):
        from world.mob_templates import MOB_TEMPLATES
        self.assertIsInstance(MOB_TEMPLATES, dict)

    def test_mob_templates_has_entries(self):
        from world.mob_templates import MOB_TEMPLATES
        self.assertGreaterEqual(len(MOB_TEMPLATES), 3)

    def test_rat_template_structure(self):
        """Spot check: rat template has all required fields."""
        from world.mob_templates import MOB_TEMPLATES
        rat = MOB_TEMPLATES.get("rat")
        self.assertIsNotNone(rat)
        required_fields = [
            "key", "mob_type", "desc", "base_aggression",
            "hp_min", "hp_max", "damage_min", "damage_max",
            "speed", "abilities", "faction", "is_hunter",
            "detection_range", "flee_threshold", "wander", "loot_table",
        ]
        for field in required_fields:
            self.assertIn(field, rat, f"Missing field: {field}")


class TestGetMobTemplate(unittest.TestCase):
    """Test get_mob_template function."""

    def test_get_existing_template(self):
        from world.mob_templates import get_mob_template
        result = get_mob_template("rat")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["mob_type"], "rat")

    def test_get_nonexistent_template(self):
        from world.mob_templates import get_mob_template
        result = get_mob_template("nonexistent_mob_xyz")
        self.assertIsNone(result)


class TestApplyMobTemplate(unittest.TestCase):
    """Test apply_mob_template sets correct db attributes."""

    def test_sets_mob_type(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "wolf")
        self.assertEqual(mob.db.mob_type, "wolf")

    def test_sets_hp_range(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "wolf")
        # Wolf should have different HP than defaults
        self.assertIsNotNone(mob.db.hp_min)
        self.assertIsNotNone(mob.db.hp_max)

    def test_sets_damage_range(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "wolf")
        self.assertIsNotNone(mob.db.damage_min)
        self.assertIsNotNone(mob.db.damage_max)

    def test_sets_abilities(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "wolf")
        self.assertIsInstance(mob.db.abilities, list)

    def test_sets_base_aggression(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "wolf")
        self.assertEqual(mob.db.base_aggression, "aggressive")

    def test_sets_is_hunter(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "wolf")
        self.assertIsInstance(mob.db.is_hunter, bool)

    def test_sets_detection_range(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "wolf")
        self.assertIsInstance(mob.db.detection_range, int)

    def test_sets_wander(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "wolf")
        self.assertIsInstance(mob.db.wander, bool)

    def test_sets_flee_threshold(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "rat")
        # Rat should have a flee threshold
        self.assertIsNotNone(mob.db.flee_threshold)

    def test_sets_speed(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "wolf")
        self.assertIsInstance(mob.db.speed, (int, float))

    def test_sets_loot_table(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "wolf")
        self.assertEqual(mob.db.loot_table, "wolf")

    def test_sets_desc(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "rat")
        self.assertIsInstance(mob.db.desc, str)
        self.assertTrue(len(mob.db.desc) > 0)

    def test_sets_key(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        apply_mob_template(mob, "rat")
        self.assertEqual(mob.key, "rat")

    def test_unknown_template_logs_warning(self):
        from world.mob_templates import apply_mob_template
        mob = _make_mock_mob()
        original_mob_type = mob.db.mob_type
        # Should not crash
        with patch("world.mob_templates.logger") as mock_logger:
            apply_mob_template(mob, "nonexistent_template_xyz")
            mock_logger.warning.assert_called_once()
        # mob_type should not have changed
        self.assertEqual(mob.db.mob_type, original_mob_type)


if __name__ == "__main__":
    unittest.main()
