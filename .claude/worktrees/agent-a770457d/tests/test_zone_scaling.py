"""
Tests for per-player logarithmic zone scaling (redesigned session 8 patch).
Tests written FIRST per TDD.
"""

from evennia.utils.test_resources import EvenniaTest
from evennia import create_object


class ScalingTestBase(EvenniaTest):
    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom
        from typeclasses.mobs import SoravelonMob

        self.room = create_object(SoravelonRoom, key="Test Room")
        self.room.db.zone_id = "test_zone"

        self.mob = create_object(SoravelonMob, key="wolf", location=self.room)
        self.mob.db.rarity = "normal"
        self.mob.db.hp_min = 80
        self.mob.db.hp_max = 120
        self.mob.db.damage_min = 8
        self.mob.db.damage_max = 14
        self.mob.db.prestige_modifier = 1.0

        self.char1.db.backend_level = 10
        self.char1.location = self.room


class TestScaleFactorAtReference(ScalingTestBase):
    def test_scale_factor_at_reference_level(self):
        from world.zone_scaling import get_scale_factor
        self.assertAlmostEqual(get_scale_factor(10), 1.0, places=5)


class TestScaleFactorFloor(ScalingTestBase):
    def test_scale_factor_floor_applied(self):
        from world.zone_scaling import get_scale_factor, SCALE_FLOOR
        self.assertAlmostEqual(get_scale_factor(1), SCALE_FLOOR, places=2)


class TestScaleFactorBackend5(ScalingTestBase):
    def test_scale_factor_backend_5(self):
        from world.zone_scaling import get_scale_factor, SCALE_FLOOR
        s = get_scale_factor(5)
        self.assertGreater(s, SCALE_FLOOR)
        self.assertLess(s, 1.0)


class TestScaleFactorBackend30(ScalingTestBase):
    def test_scale_factor_backend_30(self):
        from world.zone_scaling import get_scale_factor
        self.assertGreater(get_scale_factor(30), 1.0)


class TestScaleFactorBackend50(ScalingTestBase):
    def test_scale_factor_backend_50(self):
        from world.zone_scaling import get_scale_factor
        s = get_scale_factor(50)
        self.assertGreater(s, 1.0)
        self.assertLess(s, 2.0)


class TestScaleFactorNeverBelowFloor(ScalingTestBase):
    def test_scale_factor_never_below_floor(self):
        from world.zone_scaling import get_scale_factor, SCALE_FLOOR
        for lvl in range(1, 51):
            self.assertGreaterEqual(get_scale_factor(lvl), SCALE_FLOOR)


class TestCombatScaleCached(ScalingTestBase):
    def test_combat_scale_cached_after_first_call(self):
        from world.zone_scaling import get_combat_scale, initialize_mob_combat_stats
        initialize_mob_combat_stats(self.mob)
        s1 = get_combat_scale(self.mob, self.char1)
        s2 = get_combat_scale(self.mob, self.char1)
        self.assertEqual(s1, s2)
        self.assertEqual(len(self.mob.ndb.combat_scales), 1)


class TestCombatScaleIndependentPerChar(ScalingTestBase):
    def test_combat_scale_independent_per_character(self):
        from world.zone_scaling import get_combat_scale, initialize_mob_combat_stats
        initialize_mob_combat_stats(self.mob)
        self.char1.db.backend_level = 10
        self.char2.db.backend_level = 40
        s1 = get_combat_scale(self.mob, self.char1)
        s2 = get_combat_scale(self.mob, self.char2)
        self.assertNotAlmostEqual(s1, s2)
        self.assertEqual(len(self.mob.ndb.combat_scales), 2)


class TestCombatScaleClearsOnDeath(ScalingTestBase):
    def test_combat_scale_clears_on_death(self):
        from world.zone_scaling import get_combat_scale, initialize_mob_combat_stats
        initialize_mob_combat_stats(self.mob)
        get_combat_scale(self.mob, self.char1)
        self.mob.at_death()
        scales = getattr(self.mob.ndb, 'combat_scales', {})
        self.assertEqual(len(scales), 0)


class TestMobDamageScalesWithBackend(ScalingTestBase):
    def test_mob_damage_scales_with_backend(self):
        from world.zone_scaling import (
            get_mob_damage_for_player, get_combat_scale,
            initialize_mob_combat_stats
        )
        initialize_mob_combat_stats(self.mob)
        self.char1.db.backend_level = 10
        get_combat_scale(self.mob, self.char1)
        dmg_min_10, dmg_max_10 = get_mob_damage_for_player(self.mob, self.char1)

        self.char2.db.backend_level = 40
        get_combat_scale(self.mob, self.char2)
        dmg_min_40, dmg_max_40 = get_mob_damage_for_player(self.mob, self.char2)

        self.assertGreater(dmg_max_40, dmg_max_10)


class TestPlayerDamageScalesWithBackend(ScalingTestBase):
    def test_player_damage_scales_with_backend(self):
        from world.zone_scaling import (
            get_player_damage_to_mob, get_combat_scale,
            initialize_mob_combat_stats
        )
        initialize_mob_combat_stats(self.mob)
        self.char1.db.backend_level = 10
        get_combat_scale(self.mob, self.char1)
        d10 = get_player_damage_to_mob(100, self.mob, self.char1)

        self.char2.db.backend_level = 40
        get_combat_scale(self.mob, self.char2)
        d40 = get_player_damage_to_mob(100, self.mob, self.char2)

        self.assertGreater(d40, d10)


class TestInitMobStatsNormal(ScalingTestBase):
    def test_initialize_mob_combat_stats_normal_rarity(self):
        from world.zone_scaling import initialize_mob_combat_stats
        self.mob.db.rarity = "normal"
        initialize_mob_combat_stats(self.mob)
        self.assertGreaterEqual(self.mob.db.hp, 80)
        self.assertLessEqual(self.mob.db.hp, 120)


class TestInitMobStatsLegendary(ScalingTestBase):
    def test_initialize_mob_combat_stats_legendary_rarity(self):
        from world.zone_scaling import initialize_mob_combat_stats
        self.mob.db.rarity = "legendary"
        initialize_mob_combat_stats(self.mob)
        self.assertGreaterEqual(self.mob.db.hp, int(80 * 2.5))
        self.assertLessEqual(self.mob.db.hp, int(120 * 2.5))


class TestInitMobStatsPrestige(ScalingTestBase):
    def test_initialize_mob_combat_stats_prestige(self):
        from world.zone_scaling import initialize_mob_combat_stats
        self.mob.db.rarity = "normal"
        self.mob.db.prestige_modifier = 2.0
        initialize_mob_combat_stats(self.mob)
        self.assertGreaterEqual(self.mob.db.hp, 160)  # 80*2.0
        self.assertLessEqual(self.mob.db.hp, 240)     # 120*2.0


class TestApplyResistanceFull(ScalingTestBase):
    def test_apply_resistance_full(self):
        from world.zone_scaling import apply_resistance
        self.mob.db.resistances = {"fire": 0.5}
        result = apply_resistance(100, "fire", self.mob)
        self.assertEqual(result, 50)


class TestApplyResistanceNone(ScalingTestBase):
    def test_apply_resistance_none(self):
        from world.zone_scaling import apply_resistance
        self.mob.db.resistances = {}
        result = apply_resistance(100, "fire", self.mob)
        self.assertEqual(result, 100)


class TestApplyResistanceMinOne(ScalingTestBase):
    def test_apply_resistance_minimum_one(self):
        from world.zone_scaling import apply_resistance
        self.mob.db.resistances = {"fire": 1.0}
        result = apply_resistance(100, "fire", self.mob)
        self.assertEqual(result, 1)


class TestMaterialTierSkill0(ScalingTestBase):
    def test_material_tier_skill_0(self):
        from world.zone_scaling import get_material_tier
        self.assertEqual(get_material_tier(0), 1)


class TestMaterialTierSkill50(ScalingTestBase):
    def test_material_tier_skill_50(self):
        from world.zone_scaling import get_material_tier
        self.assertEqual(get_material_tier(50), 2)


class TestMaterialTierSkill75(ScalingTestBase):
    def test_material_tier_skill_75(self):
        from world.zone_scaling import get_material_tier
        self.assertEqual(get_material_tier(75), 3)


class TestMaterialTierSkill90(ScalingTestBase):
    def test_material_tier_skill_90(self):
        from world.zone_scaling import get_material_tier
        self.assertEqual(get_material_tier(90), 4)


class TestMaterialTierSkill100(ScalingTestBase):
    def test_material_tier_skill_100(self):
        from world.zone_scaling import get_material_tier
        self.assertEqual(get_material_tier(100), 5)


class TestMaterialTierNoZoneParam(ScalingTestBase):
    def test_material_tier_function_signature(self):
        """get_material_tier takes only skill_score — no zone parameter."""
        from world.zone_scaling import get_material_tier
        import inspect
        sig = inspect.signature(get_material_tier)
        params = list(sig.parameters.keys())
        self.assertEqual(params, ["skill_score"])


class TestNoZoneLevelAttributes(ScalingTestBase):
    def test_no_zone_level_attributes(self):
        """ZoneObject does not have level_floor or level_cap."""
        from typeclasses.objects import Object
        zone = create_object(Object, key="zone", location=None)
        zone.db.zone_id = "test"
        # These should be None (never set)
        self.assertIsNone(zone.db.level_floor)
        self.assertIsNone(zone.db.level_cap)


class TestMobHasNoBaseLevel(ScalingTestBase):
    def test_mob_has_no_base_level(self):
        """SoravelonMob should not have db.base_level in new design."""
        from typeclasses.mobs import SoravelonMob
        fresh_mob = create_object(SoravelonMob, key="fresh", location=self.room)
        self.assertIsNone(fresh_mob.db.base_level)
