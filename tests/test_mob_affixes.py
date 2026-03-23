"""
Tests for the Soravelon mob affix system (Build Order Step 4).

Tests written FIRST per TDD. These must all fail before production code.
"""

import random
from unittest.mock import patch
from evennia.utils.test_resources import EvenniaTest
from evennia import create_object


class AffixTestBase(EvenniaTest):
    """Base class that creates a room for mob spawning."""

    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom

        self.room = create_object(SoravelonRoom, key="Test Room")
        self.room.db.zone_id = "test_zone"

        # Node room variant
        self.node_room = create_object(SoravelonRoom, key="Node Room")
        self.node_room.db.zone_id = "node_zone"
        self.node_room.db.node_type = "resonance"
        self.node_room.tags.add("mob_affixes_active", category="node_effect")


class TestNormalMobNoAffixes(AffixTestBase):
    def test_normal_mob_no_affixes(self):
        from typeclasses.mobs import SoravelonMob
        from world.mob_affix_roller import apply_affixes_to_mob

        mob = create_object(SoravelonMob, key="wolf", location=self.room)
        with patch("world.mob_affix_roller.roll_rarity", return_value="normal"):
            apply_affixes_to_mob(mob, self.room)

        self.assertEqual(mob.db.rarity, "normal")
        self.assertEqual(len(mob.db.affix_list), 0)
        affix_tags = mob.tags.get(category="mob_affix", return_list=True)
        self.assertEqual(len(affix_tags), 0)


class TestMagicMobOneAffix(AffixTestBase):
    def test_magic_mob_one_affix(self):
        from typeclasses.mobs import SoravelonMob
        from world.mob_affix_roller import apply_affixes_to_mob

        mob = create_object(SoravelonMob, key="wolf", location=self.room)
        with patch("world.mob_affix_roller.roll_rarity", return_value="magic"):
            apply_affixes_to_mob(mob, self.room)

        self.assertEqual(mob.db.rarity, "magic")
        self.assertEqual(len(mob.db.affix_list), 1)


class TestRareMobTwoAffixes(AffixTestBase):
    def test_rare_mob_two_affixes(self):
        from typeclasses.mobs import SoravelonMob
        from world.mob_affix_roller import apply_affixes_to_mob

        mob = create_object(SoravelonMob, key="wolf", location=self.room)
        with patch("world.mob_affix_roller.roll_rarity", return_value="rare"):
            apply_affixes_to_mob(mob, self.room)

        self.assertEqual(mob.db.rarity, "rare")
        self.assertEqual(len(mob.db.affix_list), 2)


class TestLegendaryMobThreeAffixes(AffixTestBase):
    def test_legendary_mob_three_affixes(self):
        from typeclasses.mobs import SoravelonMob
        from world.mob_affix_roller import apply_affixes_to_mob

        mob = create_object(SoravelonMob, key="wolf", location=self.room)
        with patch("world.mob_affix_roller.roll_rarity", return_value="legendary"):
            apply_affixes_to_mob(mob, self.room)

        self.assertEqual(mob.db.rarity, "legendary")
        self.assertEqual(len(mob.db.affix_list), 3)


class TestForbiddenComboNotRolled(AffixTestBase):
    def test_forbidden_combo_not_rolled(self):
        """stun_immune + root_immune never appear together."""
        from world.mob_affix_roller import roll_affixes

        pool = ["stun_immune", "root_immune", "enraged", "armored",
                "vampiric", "slowing"]
        for _ in range(200):
            result = roll_affixes(2, pool)
            self.assertFalse(
                {"stun_immune", "root_immune"}.issubset(set(result)),
                f"Forbidden combo rolled: {result}"
            )


class TestDefensiveLimit(AffixTestBase):
    def test_defensive_limit(self):
        """Max 1 defensive affix even when rolling 3."""
        from world.mob_affix_roller import roll_affixes
        from world.mob_affixes import DEFENSIVE_AFFIXES

        # Pool with many defensive options
        pool = list(DEFENSIVE_AFFIXES) + ["enraged", "slowing",
                                           "draining", "frenzied"]
        for _ in range(200):
            result = roll_affixes(3, pool)
            def_count = sum(1 for a in result if a in DEFENSIVE_AFFIXES)
            self.assertLessEqual(
                def_count, 1,
                f"Too many defensive affixes: {result}"
            )


class TestRegeneratingVampiricNotTogether(AffixTestBase):
    def test_regenerating_vampiric_not_together(self):
        from world.mob_affix_roller import roll_affixes

        pool = ["regenerating", "vampiric", "enraged", "slowing",
                "frenzied", "draining"]
        for _ in range(200):
            result = roll_affixes(2, pool)
            self.assertFalse(
                {"regenerating", "vampiric"}.issubset(set(result)),
                f"Forbidden combo: {result}"
            )


class TestStarDisplayGreen(AffixTestBase):
    def test_star_display_green_one_star(self):
        from typeclasses.mobs import SoravelonMob

        mob = create_object(SoravelonMob, key="wolf", location=self.room)
        mob.db.rarity = "magic"
        name = mob.get_display_name(self.char1)
        self.assertTrue(name.startswith("|g★|n"))


class TestStarDisplayYellow(AffixTestBase):
    def test_star_display_yellow_two_stars(self):
        from typeclasses.mobs import SoravelonMob

        mob = create_object(SoravelonMob, key="wolf", location=self.room)
        mob.db.rarity = "rare"
        name = mob.get_display_name(self.char1)
        self.assertTrue(name.startswith("|y★★|n"))


class TestStarDisplayRed(AffixTestBase):
    def test_star_display_red_three_stars(self):
        from typeclasses.mobs import SoravelonMob

        mob = create_object(SoravelonMob, key="wolf", location=self.room)
        mob.db.rarity = "legendary"
        name = mob.get_display_name(self.char1)
        self.assertTrue(name.startswith("|r★★★|n"))


class TestNormalNoStar(AffixTestBase):
    def test_normal_no_star(self):
        from typeclasses.mobs import SoravelonMob

        mob = create_object(SoravelonMob, key="wolf", location=self.room)
        mob.db.rarity = "normal"
        name = mob.get_display_name(self.char1)
        self.assertFalse(name.startswith("|"))


class TestAffixRevealFiresOnce(AffixTestBase):
    def test_affix_reveal_fires_once(self):
        from typeclasses.mobs import SoravelonMob

        mob = create_object(SoravelonMob, key="wolf", location=self.room)
        mob.db.rarity = "magic"
        mob.db.affix_list = ["enraged"]
        mob.tags.add("enraged", category="mob_affix")

        msg1 = mob.reveal_affix(self.char1, "enraged")
        self.assertIsNotNone(msg1)
        self.assertIn("enraged", msg1.lower())

        msg2 = mob.reveal_affix(self.char1, "enraged")
        self.assertIsNone(msg2)


class TestImmunityCheck(AffixTestBase):
    def test_immunity_check(self):
        from typeclasses.mobs import SoravelonMob

        mob = create_object(SoravelonMob, key="wolf", location=self.room)
        mob.tags.add("fire_immune", category="mob_affix")
        mob.db.affix_list = ["fire_immune"]

        immune, _ = mob.has_immunity("burn")
        self.assertTrue(immune)

        normal_mob = create_object(
            SoravelonMob, key="normal_wolf", location=self.room
        )
        not_immune, _ = normal_mob.has_immunity("burn")
        self.assertFalse(not_immune)


class TestImmunityRevealOnFirstCheck(AffixTestBase):
    def test_immunity_reveal_on_first_check(self):
        from typeclasses.mobs import SoravelonMob

        mob = create_object(SoravelonMob, key="wolf", location=self.room)
        mob.tags.add("poison_immune", category="mob_affix")
        mob.db.affix_list = ["poison_immune"]

        _, msg1 = mob.has_immunity("poison")
        self.assertIsNotNone(msg1)

        _, msg2 = mob.has_immunity("poison")
        self.assertIsNone(msg2)


class TestNodePoolUsed(AffixTestBase):
    def test_node_pool_used_in_node_room(self):
        from world.mob_affix_roller import get_affix_pool
        from world.mob_affixes import NODE_AFFIX_POOLS

        pool = get_affix_pool(self.node_room)
        self.assertEqual(pool, NODE_AFFIX_POOLS["resonance"])


class TestGeneralPoolOutsideNode(AffixTestBase):
    def test_general_pool_outside_node(self):
        from world.mob_affix_roller import get_affix_pool
        from world.mob_affixes import GENERAL_AFFIX_POOL

        pool = get_affix_pool(self.room)
        self.assertEqual(pool, GENERAL_AFFIX_POOL)


class TestPackSpawnedForMagic(AffixTestBase):
    def test_pack_spawned_for_magic(self):
        from typeclasses.mobs import SoravelonMob
        from world.mob_affix_roller import spawn_mob_with_pack

        with patch("world.mob_affix_roller.roll_rarity", return_value="magic"):
            mob, pack = spawn_mob_with_pack(
                SoravelonMob, "wolf", self.room,
                mob_type="forest_wolf",
                zone_id="test_zone"
            )

        self.assertEqual(mob.db.rarity, "magic")
        self.assertGreaterEqual(len(pack), 1)
        self.assertLessEqual(len(pack), 2)


class TestPackMobsAlwaysNormal(AffixTestBase):
    def test_pack_mobs_always_normal(self):
        from typeclasses.mobs import SoravelonMob
        from world.mob_affix_roller import spawn_mob_with_pack

        with patch("world.mob_affix_roller.roll_rarity", return_value="rare"):
            mob, pack = spawn_mob_with_pack(
                SoravelonMob, "wolf", self.room,
                mob_type="forest_wolf",
                zone_id="test_zone"
            )

        for pack_mob in pack:
            self.assertEqual(pack_mob.db.rarity, "normal")
            self.assertEqual(len(pack_mob.db.affix_list), 0)


class TestLootTierMatchesRarity(AffixTestBase):
    def test_loot_tier_matches_rarity(self):
        from typeclasses.mobs import SoravelonMob

        for rarity in ("normal", "magic", "rare", "legendary"):
            mob = create_object(
                SoravelonMob, key="wolf", location=self.room
            )
            mob.db.rarity = rarity
            self.assertEqual(mob.get_loot_tier(), rarity)


class TestRollAffixPoolExhaustion(AffixTestBase):
    def test_roll_affix_pool_exhaustion(self):
        """roll_affixes handles small pools gracefully."""
        from world.mob_affix_roller import roll_affixes

        # Pool too small for requested count
        result = roll_affixes(3, ["enraged", "slowing"])
        self.assertLessEqual(len(result), 2)
        # Shouldn't crash or infinite loop
