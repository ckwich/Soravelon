"""
Tests for the Soravelon mob disposition system (Build Order Step 5).
Tests written FIRST per TDD.
"""

from evennia.utils.test_resources import EvenniaTest
from evennia import create_object
from world.models import FactionStanding


class DispositionTestBase(EvenniaTest):
    """Base with a room, a mob, and a character with configurable state."""

    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom
        from typeclasses.mobs import SoravelonMob

        self.room = create_object(SoravelonRoom, key="Test Room")
        self.mob = create_object(SoravelonMob, key="guard", location=self.room)

        # Set default character state
        self.char1.db.ancestry = "human"
        self.char1.db.reputation_score = 0.0

    def _set_standing(self, faction_id, standing, trust=50):
        FactionStanding.objects.update_or_create(
            character=self.char1,
            faction_id=faction_id,
            subfaction_id=None,
            defaults={"standing": standing, "trust": trust},
        )


# --- Core computation ---

class TestNeutralBaseNoFactionNoReputation(DispositionTestBase):
    def test_neutral_base_no_faction_no_reputation(self):
        from world.mob_disposition import get_mob_disposition

        self.mob.db.base_disposition = 0.0
        self.mob.db.faction = None
        self.char1.db.reputation_score = 0.0

        d = get_mob_disposition(self.mob, self.char1)
        self.assertAlmostEqual(d, 0.0, places=5)


class TestStandingPositive(DispositionTestBase):
    def test_standing_positive_increases_disposition(self):
        from world.mob_disposition import get_mob_disposition

        self.mob.db.faction = "empire"
        self.mob.db.base_disposition = 0.0
        self._set_standing("empire", 50000)

        d = get_mob_disposition(self.mob, self.char1)
        # +50000/100000 * 0.6 = +0.3, plus human/empire +0.10 = 0.4
        self.assertGreater(d, 0.0)


class TestStandingNegative(DispositionTestBase):
    def test_standing_negative_decreases_disposition(self):
        from world.mob_disposition import get_mob_disposition

        self.mob.db.faction = "empire"
        self.mob.db.base_disposition = 0.0
        self._set_standing("empire", -50000)

        d = get_mob_disposition(self.mob, self.char1)
        self.assertLess(d, 0.0)


class TestStandingMaxMapsTo06(DispositionTestBase):
    def test_standing_max_maps_to_0_6(self):
        from world.mob_disposition import get_standing_modifier

        self._set_standing("empire", 100000)
        mod = get_standing_modifier(self.char1, "empire")
        self.assertAlmostEqual(mod, 0.6, places=5)


class TestStandingMinMapsToNeg06(DispositionTestBase):
    def test_standing_min_maps_to_neg_0_6(self):
        from world.mob_disposition import get_standing_modifier

        self._set_standing("empire", -100000)
        mod = get_standing_modifier(self.char1, "empire")
        self.assertAlmostEqual(mod, -0.6, places=5)


class TestReputationZero(DispositionTestBase):
    def test_reputation_zero_adds_zero(self):
        from world.mob_disposition import get_reputation_modifier

        self.char1.db.reputation_score = 0.0
        mod = get_reputation_modifier(self.char1)
        self.assertAlmostEqual(mod, 0.0, places=5)


class TestReputation100(DispositionTestBase):
    def test_reputation_100_adds_0_2(self):
        from world.mob_disposition import get_reputation_modifier

        self.char1.db.reputation_score = 100.0
        mod = get_reputation_modifier(self.char1)
        self.assertAlmostEqual(mod, 0.2, places=5)


class TestReputationNonNegative(DispositionTestBase):
    def test_reputation_always_non_negative(self):
        from world.mob_disposition import get_reputation_modifier

        for score in (0.0, -10.0, 50.0, 100.0):
            self.char1.db.reputation_score = score
            mod = get_reputation_modifier(self.char1)
            self.assertGreaterEqual(mod, 0.0)


# --- Ancestry ---

class TestSelvarEmpireModifier(DispositionTestBase):
    def test_selvar_empire_modifier(self):
        from world.mob_disposition import get_ancestry_modifier

        mod = get_ancestry_modifier("selvar", "empire")
        self.assertAlmostEqual(mod, -0.15, places=5)


class TestKauroranHomeTerritory(DispositionTestBase):
    def test_kauroran_home_territory(self):
        from world.mob_disposition import get_ancestry_modifier

        mod = get_ancestry_modifier("kauroran", "kauroran")
        self.assertAlmostEqual(mod, 0.20, places=5)


class TestUnlistedComboZero(DispositionTestBase):
    def test_unlisted_combo_returns_zero(self):
        from world.mob_disposition import get_ancestry_modifier

        # Human vs Kau'roran is listed as 0.00
        mod = get_ancestry_modifier("human", "kauroran")
        self.assertAlmostEqual(mod, 0.0, places=5)


class TestStandingAndAncestryAdditive(DispositionTestBase):
    def test_standing_and_ancestry_additive(self):
        """Selvar with max Standing vs Empire: +0.6 + (-0.15) = +0.45"""
        from world.mob_disposition import get_mob_disposition

        self.mob.db.faction = "empire"
        self.mob.db.base_disposition = 0.0
        self.char1.db.ancestry = "selvar"
        self.char1.db.reputation_score = 0.0
        self._set_standing("empire", 100000)

        d = get_mob_disposition(self.mob, self.char1)
        # 0.0 (base) + 0.6 (standing) + 0.0 (rep) + (-0.15) (ancestry) = 0.45
        self.assertAlmostEqual(d, 0.45, places=2)


# --- Trust ---

class TestTrustLowReducesPositive(DispositionTestBase):
    def test_trust_low_reduces_positive_disposition(self):
        from world.mob_disposition import get_mob_disposition

        self.mob.db.faction = "empire"
        self.mob.db.base_disposition = 0.0
        self.mob.db.trust_sensitive = True
        self.char1.db.ancestry = "human"
        self.char1.db.reputation_score = 0.0
        # Standing +66667 → modifier +0.4, ancestry +0.1 → pre-trust ~0.5
        # Trust=0 → should cancel all positive → near 0
        self._set_standing("empire", 66667, trust=0)

        d = get_mob_disposition(self.mob, self.char1)
        self.assertAlmostEqual(d, 0.0, delta=0.05)


class TestTrustMidReducesPartially(DispositionTestBase):
    def test_trust_mid_reduces_partially(self):
        from world.mob_disposition import get_mob_disposition

        self.mob.db.faction = "empire"
        self.mob.db.base_disposition = 0.0
        self.mob.db.trust_sensitive = True
        self.char1.db.ancestry = "human"
        self.char1.db.reputation_score = 0.0
        self._set_standing("empire", 66667, trust=12)

        d = get_mob_disposition(self.mob, self.char1)
        # Pre-trust ~0.5, trust=12 → reduction_factor=0.48, delta≈-0.26
        # Final ~0.24
        self.assertGreater(d, 0.0)
        self.assertLess(d, 0.5)


class TestTrustDefault50NoEffect(DispositionTestBase):
    def test_trust_default_50_no_effect(self):
        from world.mob_disposition import get_trust_modifier

        # No FactionStanding record → get_trust returns 50 (neutral band)
        mod = get_trust_modifier(self.char1, "empire", 0.4)
        self.assertAlmostEqual(mod, 0.0, places=5)


class TestTrustHighAddsBonus(DispositionTestBase):
    def test_trust_high_adds_bonus(self):
        from world.mob_disposition import get_trust_modifier

        self._set_standing("empire", 0, trust=80)
        mod = get_trust_modifier(self.char1, "empire", 0.3)
        self.assertAlmostEqual(mod, 0.1, places=5)


class TestTrustNotAppliedNonSensitive(DispositionTestBase):
    def test_trust_not_applied_non_sensitive(self):
        from world.mob_disposition import get_mob_disposition

        self.mob.db.faction = "empire"
        self.mob.db.base_disposition = 0.0
        self.mob.db.trust_sensitive = False
        self.char1.db.ancestry = "human"
        self.char1.db.reputation_score = 0.0
        self._set_standing("empire", 50000, trust=0)

        d = get_mob_disposition(self.mob, self.char1)
        # Standing +0.3 + ancestry +0.1 = 0.4 — trust NOT applied
        self.assertAlmostEqual(d, 0.4, places=2)


class TestTrustNoEffectOnNegative(DispositionTestBase):
    def test_trust_no_effect_on_negative_disposition(self):
        from world.mob_disposition import get_trust_modifier

        self._set_standing("empire", 0, trust=0)
        # pre_trust_disposition is negative
        mod = get_trust_modifier(self.char1, "empire", -0.3)
        self.assertAlmostEqual(mod, 0.0, places=5)


# --- Behavior translation ---

class TestBehaviorFriendly(DispositionTestBase):
    def test_behavior_friendly_at_0_7(self):
        from world.mob_disposition import get_mob_behavior

        self.mob.db.base_disposition = 0.7
        self.mob.db.faction = None
        behavior = get_mob_behavior(self.mob, self.char1)
        self.assertEqual(behavior, "friendly")


class TestBehaviorPassive(DispositionTestBase):
    def test_behavior_passive_at_0_4(self):
        from world.mob_disposition import get_mob_behavior

        self.mob.db.base_disposition = 0.4
        self.mob.db.faction = None
        behavior = get_mob_behavior(self.mob, self.char1)
        self.assertEqual(behavior, "passive")


class TestBehaviorNeutralPassiveBase(DispositionTestBase):
    def test_behavior_neutral_band_passive_base(self):
        from world.mob_disposition import get_mob_behavior

        self.mob.db.base_disposition = 0.0
        self.mob.db.base_aggression = "passive"
        self.mob.db.faction = None
        behavior = get_mob_behavior(self.mob, self.char1)
        self.assertEqual(behavior, "passive")


class TestBehaviorNeutralTerritorialBase(DispositionTestBase):
    def test_behavior_neutral_band_territorial_base(self):
        from world.mob_disposition import get_mob_behavior

        self.mob.db.base_disposition = 0.0
        self.mob.db.base_aggression = "territorial"
        self.mob.db.faction = None
        behavior = get_mob_behavior(self.mob, self.char1)
        self.assertEqual(behavior, "territorial")


class TestBehaviorNeutralAggressiveBase(DispositionTestBase):
    def test_behavior_neutral_band_aggressive_base(self):
        from world.mob_disposition import get_mob_behavior

        self.mob.db.base_disposition = 0.0
        self.mob.db.base_aggression = "aggressive"
        self.mob.db.faction = None
        behavior = get_mob_behavior(self.mob, self.char1)
        self.assertEqual(behavior, "aggressive")


class TestBehaviorElevatedPassiveTerritorial(DispositionTestBase):
    def test_behavior_elevated_passive_becomes_territorial(self):
        from world.mob_disposition import get_mob_behavior

        self.mob.db.base_disposition = -0.4
        self.mob.db.base_aggression = "passive"
        self.mob.db.faction = None
        behavior = get_mob_behavior(self.mob, self.char1)
        self.assertEqual(behavior, "territorial")


class TestBehaviorElevatedTerritorialAggressive(DispositionTestBase):
    def test_behavior_elevated_territorial_becomes_aggressive(self):
        from world.mob_disposition import get_mob_behavior

        self.mob.db.base_disposition = -0.4
        self.mob.db.base_aggression = "territorial"
        self.mob.db.faction = None
        behavior = get_mob_behavior(self.mob, self.char1)
        self.assertEqual(behavior, "aggressive")


class TestBehaviorMaximallyHostile(DispositionTestBase):
    def test_behavior_maximally_hostile(self):
        from world.mob_disposition import get_mob_behavior

        self.mob.db.base_disposition = -0.8
        self.mob.db.base_aggression = "passive"
        self.mob.db.faction = None
        behavior = get_mob_behavior(self.mob, self.char1)
        self.assertEqual(behavior, "aggressive")


# --- Edge cases ---

class TestDispositionClampedUpper(DispositionTestBase):
    def test_disposition_clamped_upper(self):
        from world.mob_disposition import get_mob_disposition

        self.mob.db.base_disposition = 1.0
        self.mob.db.faction = "kauroran"
        self.char1.db.ancestry = "kauroran"
        self.char1.db.reputation_score = 100.0
        self._set_standing("kauroran", 100000, trust=90)
        self.mob.db.trust_sensitive = True

        d = get_mob_disposition(self.mob, self.char1)
        self.assertLessEqual(d, 1.0)


class TestDispositionClampedLower(DispositionTestBase):
    def test_disposition_clamped_lower(self):
        from world.mob_disposition import get_mob_disposition

        self.mob.db.base_disposition = -1.0
        self.mob.db.faction = "empire"
        self.char1.db.ancestry = "kauroran"
        self._set_standing("empire", -100000)

        d = get_mob_disposition(self.mob, self.char1)
        self.assertGreaterEqual(d, -1.0)


class TestNoFactionSkipsAll(DispositionTestBase):
    def test_no_faction_mob_skips_standing_ancestry_trust(self):
        from world.mob_disposition import get_mob_disposition

        self.mob.db.faction = None
        self.mob.db.base_disposition = 0.1
        self.char1.db.reputation_score = 50.0
        # Standing/trust records exist but should be ignored
        self._set_standing("empire", 100000, trust=0)

        d = get_mob_disposition(self.mob, self.char1)
        # Only base (0.1) + reputation (50/100*0.2 = 0.1) = 0.2
        self.assertAlmostEqual(d, 0.2, places=2)


class TestQuestModifierAlwaysZero(DispositionTestBase):
    def test_quest_modifier_always_zero(self):
        from world.mob_disposition import get_quest_modifier

        self.assertEqual(get_quest_modifier(self.char1, "some_quest"), 0.0)
        self.assertEqual(get_quest_modifier(self.char1, None), 0.0)
