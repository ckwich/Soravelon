"""
Tests for world/loot_tables.py — skill-based loot resolution system.

Uses unittest.TestCase + MagicMock. No Evennia DB required.
Roll quality is determined by killer's relevant domain skill score (D-34).
DO NOT test level-based loot — the system uses skill scores exclusively.
"""

import unittest
from unittest.mock import MagicMock, patch


def _make_mob(mob_type="wolf", rarity="normal", location=None):
    """Build a minimal mock mob for testing."""
    mob = MagicMock()
    mob.db.mob_type = mob_type
    mob.db.rarity = rarity
    mob.location = location
    return mob


def _make_killer(domain_scores=None):
    """Build a minimal mock killer for testing."""
    killer = MagicMock()
    killer.db.domain_scores = domain_scores or {}
    return killer


class TestGetLootModifiers(unittest.TestCase):
    """get_loot_modifiers returns rarity-correct modifier dict."""

    def setUp(self):
        from world.loot_tables import get_loot_modifiers
        self.get_loot_modifiers = get_loot_modifiers

    def test_normal_mob(self):
        mob = _make_mob(rarity="normal")
        result = self.get_loot_modifiers(mob)
        self.assertEqual(result["extra_rolls"], 0)
        self.assertEqual(result["tome_chance"], 0.00)

    def test_magic_mob(self):
        mob = _make_mob(rarity="magic")
        result = self.get_loot_modifiers(mob)
        self.assertEqual(result["extra_rolls"], 1)

    def test_rare_mob(self):
        mob = _make_mob(rarity="rare")
        result = self.get_loot_modifiers(mob)
        self.assertEqual(result["extra_rolls"], 1)
        self.assertEqual(result["tome_chance"], 0.05)

    def test_legendary_mob(self):
        mob = _make_mob(rarity="legendary")
        result = self.get_loot_modifiers(mob)
        self.assertEqual(result["extra_rolls"], 2)
        self.assertEqual(result["tome_chance"], 0.15)
        self.assertEqual(result["ancient_chance"], 0.02)

    def test_unknown_rarity_defaults_to_normal(self):
        mob = _make_mob(rarity="unknown_tier")
        result = self.get_loot_modifiers(mob)
        self.assertEqual(result["extra_rolls"], 0)


class TestRollLootMissingMobType(unittest.TestCase):
    """roll_loot returns [] when mob_type not in any loot table."""

    def test_unknown_mob_type_returns_empty(self):
        from world.loot_tables import roll_loot
        mob = _make_mob(mob_type="does_not_exist")
        killer = _make_killer({"combat": 50})
        result = roll_loot(mob, killer)
        self.assertEqual(result, [])

    def test_none_mob_type_returns_empty(self):
        from world.loot_tables import roll_loot
        mob = _make_mob(mob_type=None)
        killer = _make_killer({"combat": 50})
        result = roll_loot(mob, killer)
        self.assertEqual(result, [])


class TestRollLootDropChance(unittest.TestCase):
    """base_drop_chance gate works correctly."""

    def test_zero_drop_chance_returns_empty(self):
        """base_drop_chance=0.0 — random.random() > 0.0 is always True → always []"""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        killer = _make_killer({"combat": 50})

        with patch.dict(LOOT_TABLES, {
            "wolf": dict(LOOT_TABLES["wolf"], base_drop_chance=0.0)
        }):
            # random.random() always > 0.0, so always skips
            result = roll_loot(mob, killer)
        self.assertEqual(result, [])

    def test_one_drop_chance_always_drops(self):
        """base_drop_chance=1.0 — random.random() never > 1.0 → always drops"""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        killer = _make_killer({"combat": 50})

        with patch.dict(LOOT_TABLES, {
            "wolf": dict(LOOT_TABLES["wolf"], base_drop_chance=1.0)
        }):
            result = roll_loot(mob, killer)
        self.assertGreater(len(result), 0)


class TestRollLootSkillTier(unittest.TestCase):
    """Killer skill score drives material tier (D-34)."""

    def setUp(self):
        from world.loot_tables import LOOT_TABLES
        # Use wolf with guaranteed drop (base_drop_chance=1.0) for determinism
        self._wolf_entry = dict(LOOT_TABLES["wolf"], base_drop_chance=1.0)

    def test_skill_0_gives_tier_1_values(self):
        """Skill 0 → tier 1 → index 0 in value_by_tier/rarity_by_tier/desc_by_tier."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        killer = _make_killer({"combat": 0})

        with patch.dict(LOOT_TABLES, {"wolf": self._wolf_entry}):
            results = roll_loot(mob, killer)

        self.assertGreater(len(results), 0)
        item = results[0]
        self.assertEqual(item["value"], 2)        # value_by_tier[0]
        self.assertEqual(item["rarity"], "normal") # rarity_by_tier[0]
        self.assertIn("rough", item["desc"].lower())  # desc_by_tier[0]

    def test_skill_25_gives_tier_1(self):
        """Boundary: skill 25 → tier 1."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        killer = _make_killer({"combat": 25})

        with patch.dict(LOOT_TABLES, {"wolf": self._wolf_entry}):
            results = roll_loot(mob, killer)

        item = results[0]
        self.assertEqual(item["value"], 2)

    def test_skill_60_gives_tier_3_values(self):
        """Skill 60 → tier 3 → index 2."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        killer = _make_killer({"combat": 60})

        with patch.dict(LOOT_TABLES, {"wolf": self._wolf_entry}):
            results = roll_loot(mob, killer)

        self.assertGreater(len(results), 0)
        item = results[0]
        self.assertEqual(item["value"], 10)        # value_by_tier[2]
        self.assertEqual(item["rarity"], "normal") # rarity_by_tier[2]
        self.assertIn("quality", item["desc"].lower())

    def test_skill_76_gives_tier_4(self):
        """Boundary: skill 76 → tier 4 → index 3."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        killer = _make_killer({"combat": 76})

        with patch.dict(LOOT_TABLES, {"wolf": self._wolf_entry}):
            results = roll_loot(mob, killer)

        item = results[0]
        self.assertEqual(item["value"], 20)        # value_by_tier[3]
        self.assertEqual(item["rarity"], "magic")  # rarity_by_tier[3]

    def test_skill_100_gives_tier_5(self):
        """Max skill → tier 5 → index 4."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        killer = _make_killer({"combat": 100})

        with patch.dict(LOOT_TABLES, {"wolf": self._wolf_entry}):
            results = roll_loot(mob, killer)

        item = results[0]
        self.assertEqual(item["value"], 40)        # value_by_tier[4]
        self.assertEqual(item["rarity"], "rare")   # rarity_by_tier[4]
        self.assertIn("exceptional", item["desc"].lower())

    def test_no_domain_scores_defaults_to_tier_1(self):
        """Killer with no domain_scores dict → skill 0 → tier 1."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        # db.domain_scores returns None (not set)
        killer = MagicMock()
        killer.db.domain_scores = None

        with patch.dict(LOOT_TABLES, {"wolf": self._wolf_entry}):
            results = roll_loot(mob, killer)

        self.assertGreater(len(results), 0)
        item = results[0]
        self.assertEqual(item["value"], 2)  # tier 1

    def test_missing_relevant_skill_defaults_to_combat(self):
        """Killer with domain_scores but missing the relevant key → defaults to 0."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        killer = _make_killer({"subterfuge": 80})  # combat not present

        with patch.dict(LOOT_TABLES, {"wolf": self._wolf_entry}):
            results = roll_loot(mob, killer)

        item = results[0]
        self.assertEqual(item["value"], 2)  # combat defaults to 0 → tier 1


class TestRollLootExtraRolls(unittest.TestCase):
    """Mob rarity extra_rolls stack on top of base drop."""

    def test_normal_mob_one_drop(self):
        """Normal mob (extra_rolls=0) → exactly 1 item_def."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf", rarity="normal")
        killer = _make_killer({"combat": 50})

        entry = dict(LOOT_TABLES["wolf"], base_drop_chance=1.0)
        with patch.dict(LOOT_TABLES, {"wolf": entry}):
            results = roll_loot(mob, killer)

        self.assertEqual(len(results), 1)

    def test_legendary_mob_three_drops(self):
        """Legendary mob (extra_rolls=2) → base 1 + 2 extra = 3 total drops."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf", rarity="legendary")
        killer = _make_killer({"combat": 50})

        entry = dict(LOOT_TABLES["wolf"], base_drop_chance=1.0)
        with patch.dict(LOOT_TABLES, {"wolf": entry}):
            results = roll_loot(mob, killer)

        self.assertEqual(len(results), 3)

    def test_magic_mob_two_drops(self):
        """Magic mob (extra_rolls=1) → 1 base + 1 extra = 2."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf", rarity="magic")
        killer = _make_killer({"combat": 50})

        entry = dict(LOOT_TABLES["wolf"], base_drop_chance=1.0)
        with patch.dict(LOOT_TABLES, {"wolf": entry}):
            results = roll_loot(mob, killer)

        self.assertEqual(len(results), 2)


class TestRollLootItemDefShape(unittest.TestCase):
    """item_def dicts returned by roll_loot have correct keys."""

    def test_item_def_keys_present(self):
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        killer = _make_killer({"combat": 50})

        entry = dict(LOOT_TABLES["wolf"], base_drop_chance=1.0)
        with patch.dict(LOOT_TABLES, {"wolf": entry}):
            results = roll_loot(mob, killer)

        self.assertGreater(len(results), 0)
        item = results[0]
        for key in ("item_id", "key", "item_type", "weight", "rarity", "value", "desc"):
            self.assertIn(key, item, f"Missing key: {key}")

    def test_item_id_is_wolf_pelt(self):
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        killer = _make_killer({"combat": 50})

        entry = dict(LOOT_TABLES["wolf"], base_drop_chance=1.0)
        with patch.dict(LOOT_TABLES, {"wolf": entry}):
            results = roll_loot(mob, killer)

        self.assertEqual(results[0]["item_id"], "wolf_pelt")


class TestRollLootZoneOverride(unittest.TestCase):
    """zone_obj.db.loot_table_overrides replaces LOOT_TABLES entry for mob_type."""

    def test_zone_override_replaces_default_table(self):
        """When zone defines a wolf override, it uses that instead of LOOT_TABLES["wolf"]."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        killer = _make_killer({"combat": 50})

        # Override loot table for wolf in zone
        override_entry = {
            "mob_type": "wolf",
            "relevant_skill": "combat",
            "base_drop_chance": 1.0,
            "drops": [
                {
                    "item_id": "zone_wolf_fang",
                    "key": "wolf fang",
                    "item_type": "item",
                    "weight": 0.1,
                    "weight_in_pool": 10,
                    "value_by_tier": [5, 10, 20, 40, 80],
                    "rarity_by_tier": ["normal", "normal", "magic", "rare", "rare"],
                    "desc_by_tier": [
                        "A rough fang.", "A standard fang.", "A quality fang.",
                        "A refined fang.", "An exceptional fang.",
                    ],
                }
            ],
        }

        zone_obj = MagicMock()
        zone_obj.db.loot_table_overrides = {"wolf": override_entry}

        # Patch get_zone_obj_for_room to return our mock zone
        with patch("world.loot_tables.get_zone_obj_for_room", return_value=zone_obj):
            mob.location = MagicMock()  # room exists so override path runs
            results = roll_loot(mob, killer)

        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["item_id"], "zone_wolf_fang")

    def test_no_zone_obj_falls_back_to_default(self):
        """When get_zone_obj_for_room returns None, LOOT_TABLES is used."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        killer = _make_killer({"combat": 50})

        entry = dict(LOOT_TABLES["wolf"], base_drop_chance=1.0)
        with patch.dict(LOOT_TABLES, {"wolf": entry}):
            with patch("world.loot_tables.get_zone_obj_for_room", return_value=None):
                mob.location = MagicMock()
                results = roll_loot(mob, killer)

        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["item_id"], "wolf_pelt")

    def test_no_location_uses_default_table(self):
        """Mob with no location (mob.location is None) → skip zone check, use LOOT_TABLES."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf", location=None)
        killer = _make_killer({"combat": 50})

        entry = dict(LOOT_TABLES["wolf"], base_drop_chance=1.0)
        with patch.dict(LOOT_TABLES, {"wolf": entry}):
            results = roll_loot(mob, killer)

        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["item_id"], "wolf_pelt")


class TestRollLootRelevantSkill(unittest.TestCase):
    """relevant_skill field in loot table drives which domain score is used."""

    def test_custom_relevant_skill(self):
        """If loot table specifies relevant_skill='naturalism', that domain drives tier."""
        from world.loot_tables import roll_loot, LOOT_TABLES
        mob = _make_mob(mob_type="wolf")
        # High naturalism, low combat
        killer = _make_killer({"combat": 10, "naturalism": 80})

        custom_entry = {
            "mob_type": "wolf",
            "relevant_skill": "naturalism",  # NOT combat
            "base_drop_chance": 1.0,
            "drops": LOOT_TABLES["wolf"]["drops"],
        }

        with patch.dict(LOOT_TABLES, {"wolf": custom_entry}):
            results = roll_loot(mob, killer)

        # naturalism=80 → tier 4 → value_by_tier[3]=20
        self.assertEqual(results[0]["value"], 20)


if __name__ == "__main__":
    unittest.main()
