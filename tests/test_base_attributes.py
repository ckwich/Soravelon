"""
Tests for the base attribute system (world/base_attributes.py).

Covers point-buy validation, descriptor lookup, HP/stamina derivation,
action budget, initiative, stat growth tracking, and ancestry modifiers.
Uses unittest.TestCase + MagicMock (no Evennia DB required).
"""

import math
import unittest
from unittest.mock import MagicMock, patch

from world.base_attributes import (
    ANCESTRY_STAT_MODIFIERS,
    BASE_HP,
    BASE_STAMINA,
    HP_PER_ENDURANCE,
    HP_PER_LEVEL,
    POINT_BUY_CONFIG,
    STAMINA_PER_ENDURANCE,
    STAT_GROWTH_ACTIONS,
    STAT_NAMES,
    STAT_XP_PER_USE,
    apply_ancestry_modifiers,
    apply_point_buy,
    commit_stat_growth,
    derive_hp,
    derive_max_hp,
    derive_max_stamina,
    derive_stamina,
    get_actions_per_turn,
    get_damage_modifier,
    get_initiative,
    get_stat_descriptor,
    record_stat_use,
    validate_point_buy,
    _get_stat_growth_rate,
)


def _make_character(
    strength=10, agility=10, endurance=10, mana=10,
    acuity=10, presence=10, resonance=10,
    backend_level=1, ancestry=None,
):
    """Create a MagicMock character with base_stats on db."""
    char = MagicMock()
    char.key = "TestChar"
    char.id = 1
    char.db.base_stats = {
        "strength": strength,
        "agility": agility,
        "endurance": endurance,
        "mana": mana,
        "acuity": acuity,
        "presence": presence,
        "resonance": resonance,
    }
    char.db.backend_level = backend_level
    char.db.ancestry = ancestry
    char.db.stat_xp = {}
    char.ndb.hp = None
    char.ndb.stamina = None
    char.ndb.stat_xp_accumulators = {s: 0.0 for s in STAT_NAMES}
    return char


def _make_mob(speed=1.0):
    """Create a MagicMock mob (no base_stats, uses speed)."""
    mob = MagicMock()
    mob.key = "TestMob"
    mob.id = 2
    mob.db.base_stats = None
    mob.db.speed = speed
    return mob


def _valid_allocation(**overrides):
    """Return a valid default allocation (all 10s + 20 bonus spread evenly).

    Default: all stats at base 10, then distribute 20 bonus by adding ~3 each.
    Total pool = 7*10 + 20 = 90. Default: each stat = 90/7 is not integer,
    so we use a manual valid spread.
    """
    # 7 stats at base 10 = 70, bonus 20, total pool = 90
    alloc = {
        "strength": 13,
        "agility": 13,
        "endurance": 13,
        "mana": 13,
        "acuity": 13,
        "presence": 13,
        "resonance": 12,
    }
    alloc.update(overrides)
    return alloc


# ---------------------------------------------------------------------------
# Descriptor Lookup
# ---------------------------------------------------------------------------


class TestStatDescriptorLookup(unittest.TestCase):
    """get_stat_descriptor returns correct tier word for stat values."""

    def test_lowest_tier(self):
        """Value 0 returns the first descriptor."""
        self.assertEqual(get_stat_descriptor("strength", 0), "Feeble")

    def test_mid_tier(self):
        """Value 50 returns the tier-6 descriptor."""
        self.assertEqual(get_stat_descriptor("strength", 50), "Powerful")

    def test_max_tier(self):
        """Value 100 returns the highest descriptor."""
        self.assertEqual(get_stat_descriptor("strength", 100), "Prodigious")

    def test_boundary_exactly_on_threshold(self):
        """Value exactly at threshold belongs to that tier."""
        self.assertEqual(get_stat_descriptor("agility", 10), "Clumsy")
        self.assertEqual(get_stat_descriptor("agility", 9), "Sluggish")

    def test_clamp_above_100(self):
        """Values above 100 are clamped to 100."""
        self.assertEqual(get_stat_descriptor("endurance", 150), "Indomitable")

    def test_clamp_below_0(self):
        """Values below 0 are clamped to 0."""
        self.assertEqual(get_stat_descriptor("endurance", -5), "Fragile")

    def test_unknown_stat(self):
        """Unknown stat name returns 'Unknown'."""
        self.assertEqual(get_stat_descriptor("luck", 50), "Unknown")

    def test_all_seven_stats_have_descriptors(self):
        """Every stat in STAT_NAMES has a descriptor table entry."""
        for stat in STAT_NAMES:
            desc = get_stat_descriptor(stat, 50)
            self.assertNotEqual(desc, "Unknown", f"{stat} missing from descriptors")

    def test_each_stat_has_ten_tiers(self):
        """Each stat should produce 10 distinct descriptors across the range."""
        for stat in STAT_NAMES:
            descriptors = set()
            for val in range(0, 100, 10):
                descriptors.add(get_stat_descriptor(stat, val))
            self.assertEqual(len(descriptors), 10, f"{stat} has fewer than 10 tiers")


# ---------------------------------------------------------------------------
# Point-Buy Validation
# ---------------------------------------------------------------------------


class TestPointBuyValidation(unittest.TestCase):
    """validate_point_buy enforces all constraints."""

    def test_valid_allocation_passes(self):
        ok, msg = validate_point_buy(_valid_allocation())
        self.assertTrue(ok)
        self.assertIn("Valid", msg)

    def test_missing_stat_rejected(self):
        alloc = _valid_allocation()
        del alloc["resonance"]
        ok, msg = validate_point_buy(alloc)
        self.assertFalse(ok)
        self.assertIn("Missing stat", msg)

    def test_extra_stat_rejected(self):
        alloc = _valid_allocation()
        alloc["luck"] = 10
        ok, msg = validate_point_buy(alloc)
        self.assertFalse(ok)

    def test_below_minimum_rejected(self):
        stat_min = POINT_BUY_CONFIG["per_stat_min"]
        alloc = _valid_allocation(strength=stat_min - 1, agility=91 - 6 * 13)
        ok, msg = validate_point_buy(alloc)
        self.assertFalse(ok)
        self.assertIn("below minimum", msg)

    def test_above_maximum_rejected(self):
        stat_max = POINT_BUY_CONFIG["per_stat_max"]
        alloc = _valid_allocation(strength=stat_max + 1)
        ok, msg = validate_point_buy(alloc)
        self.assertFalse(ok)
        self.assertIn("above maximum", msg)

    def test_wrong_total_rejected(self):
        """Total points must equal 7*base + bonus."""
        alloc = _valid_allocation()
        alloc["strength"] = alloc["strength"] + 1  # over by 1
        ok, msg = validate_point_buy(alloc)
        self.assertFalse(ok)
        self.assertIn("Point total", msg)

    def test_non_numeric_rejected(self):
        alloc = _valid_allocation(strength="high")
        ok, msg = validate_point_buy(alloc)
        self.assertFalse(ok)
        self.assertIn("must be a number", msg)

    def test_unknown_stat_name_rejected(self):
        """An allocation with a stat not in STAT_NAMES is rejected."""
        alloc = _valid_allocation()
        del alloc["resonance"]
        alloc["luck"] = 12  # unknown stat, same count
        ok, msg = validate_point_buy(alloc)
        self.assertFalse(ok)


class TestApplyPointBuy(unittest.TestCase):
    """apply_point_buy validates then sets character.db.base_stats."""

    def test_valid_allocation_applied(self):
        char = _make_character()
        alloc = _valid_allocation()
        ok, msg = apply_point_buy(char, alloc)
        self.assertTrue(ok)
        self.assertEqual(char.db.base_stats["strength"], 13)

    def test_invalid_allocation_not_applied(self):
        char = _make_character()
        alloc = _valid_allocation(strength=0)  # below min
        ok, msg = apply_point_buy(char, alloc)
        self.assertFalse(ok)


# ---------------------------------------------------------------------------
# Ancestry Modifiers
# ---------------------------------------------------------------------------


class TestAncestryModifiers(unittest.TestCase):
    """apply_ancestry_modifiers adds stat bonuses/penalties per ancestry."""

    def test_human_gets_presence_and_acuity(self):
        char = _make_character(ancestry="human")
        char.db.base_stats = {s: 10 for s in STAT_NAMES}
        apply_ancestry_modifiers(char)
        stats = char.db.base_stats
        self.assertEqual(stats["presence"], 12)
        self.assertEqual(stats["acuity"], 11)

    def test_kauroran_gets_strength_endurance_minus_acuity(self):
        char = _make_character(ancestry="kauroran")
        char.db.base_stats = {s: 10 for s in STAT_NAMES}
        apply_ancestry_modifiers(char)
        stats = char.db.base_stats
        self.assertEqual(stats["strength"], 13)
        self.assertEqual(stats["endurance"], 12)
        self.assertEqual(stats["acuity"], 8)

    def test_veth_modifiers(self):
        char = _make_character(ancestry="veth")
        char.db.base_stats = {s: 10 for s in STAT_NAMES}
        apply_ancestry_modifiers(char)
        stats = char.db.base_stats
        self.assertEqual(stats["acuity"], 12)
        self.assertEqual(stats["agility"], 12)
        self.assertEqual(stats["strength"], 9)

    def test_selvar_modifiers(self):
        char = _make_character(ancestry="selvar")
        char.db.base_stats = {s: 10 for s in STAT_NAMES}
        apply_ancestry_modifiers(char)
        stats = char.db.base_stats
        self.assertEqual(stats["resonance"], 12)
        self.assertEqual(stats["presence"], 11)
        self.assertEqual(stats["agility"], 11)
        self.assertEqual(stats["endurance"], 9)

    def test_stat_floor_at_1(self):
        """No stat can go to 0 from ancestry penalty."""
        char = _make_character(ancestry="kauroran")
        char.db.base_stats = {s: 1 for s in STAT_NAMES}
        apply_ancestry_modifiers(char)
        stats = char.db.base_stats
        self.assertGreaterEqual(stats["acuity"], 1)

    def test_no_ancestry_is_noop(self):
        char = _make_character(ancestry=None)
        original = {s: 10 for s in STAT_NAMES}
        char.db.base_stats = dict(original)
        apply_ancestry_modifiers(char)
        self.assertEqual(char.db.base_stats, original)

    def test_unknown_ancestry_is_noop(self):
        char = _make_character(ancestry="dragonborn")
        original = {s: 10 for s in STAT_NAMES}
        char.db.base_stats = dict(original)
        apply_ancestry_modifiers(char)
        self.assertEqual(char.db.base_stats, original)

    def test_case_insensitive(self):
        char = _make_character(ancestry="Human")
        char.db.base_stats = {s: 10 for s in STAT_NAMES}
        apply_ancestry_modifiers(char)
        self.assertEqual(char.db.base_stats["presence"], 12)


# ---------------------------------------------------------------------------
# HP and Stamina Derivation
# ---------------------------------------------------------------------------


class TestHPDerivation(unittest.TestCase):
    """derive_max_hp uses endurance + backend level formula."""

    def test_default_values(self):
        """10 endurance, level 1: 50 + 50 + 10 = 110."""
        char = _make_character(endurance=10, backend_level=1)
        hp = derive_max_hp(char)
        self.assertEqual(hp, BASE_HP + 10 * HP_PER_ENDURANCE + 1 * HP_PER_LEVEL)

    def test_high_endurance_high_level(self):
        char = _make_character(endurance=25, backend_level=10)
        hp = derive_max_hp(char)
        self.assertEqual(hp, BASE_HP + 25 * HP_PER_ENDURANCE + 10 * HP_PER_LEVEL)

    def test_missing_base_stats_defaults(self):
        """Character with no base_stats uses endurance=10 default."""
        char = _make_character()
        char.db.base_stats = {}
        hp = derive_max_hp(char)
        self.assertEqual(hp, BASE_HP + 10 * HP_PER_ENDURANCE + 1 * HP_PER_LEVEL)

    def test_derive_hp_returns_ndb_if_set(self):
        """derive_hp returns cached ndb.hp when available."""
        char = _make_character()
        char.ndb.hp = 42
        self.assertEqual(derive_hp(char), 42)

    def test_derive_hp_returns_max_if_ndb_unset(self):
        """derive_hp falls back to max HP when ndb.hp is None."""
        char = _make_character(endurance=10, backend_level=1)
        char.ndb.hp = None
        self.assertEqual(derive_hp(char), derive_max_hp(char))


class TestStaminaDerivation(unittest.TestCase):
    """derive_max_stamina uses endurance formula."""

    def test_default_values(self):
        char = _make_character(endurance=10)
        stamina = derive_max_stamina(char)
        self.assertEqual(stamina, BASE_STAMINA + 10 * STAMINA_PER_ENDURANCE)

    def test_high_endurance(self):
        char = _make_character(endurance=50)
        stamina = derive_max_stamina(char)
        self.assertEqual(stamina, BASE_STAMINA + 50 * STAMINA_PER_ENDURANCE)

    def test_derive_stamina_returns_ndb_if_set(self):
        char = _make_character()
        char.ndb.stamina = 15
        self.assertEqual(derive_stamina(char), 15)

    def test_derive_stamina_returns_max_if_ndb_unset(self):
        char = _make_character(endurance=10)
        char.ndb.stamina = None
        self.assertEqual(derive_stamina(char), derive_max_stamina(char))


# ---------------------------------------------------------------------------
# Action Budget
# ---------------------------------------------------------------------------


class TestActionBudget(unittest.TestCase):
    """get_actions_per_turn scales with agility, clamped 1-4."""

    def test_low_agility_gives_one_action(self):
        """Agility 10: floor(1 + 10/30) = floor(1.33) = 1."""
        char = _make_character(agility=10)
        self.assertEqual(get_actions_per_turn(char), 1)

    def test_mid_agility_gives_two_actions(self):
        """Agility 30: floor(1 + 30/30) = 2."""
        char = _make_character(agility=30)
        self.assertEqual(get_actions_per_turn(char), 2)

    def test_high_agility_gives_three_actions(self):
        """Agility 60: floor(1 + 60/30) = 3."""
        char = _make_character(agility=60)
        self.assertEqual(get_actions_per_turn(char), 3)

    def test_max_agility_capped_at_four(self):
        """Agility 100: floor(1 + 100/30) = 4, capped at 4."""
        char = _make_character(agility=100)
        self.assertEqual(get_actions_per_turn(char), 4)

    def test_minimum_one_action(self):
        """Even agility 0 gives at least 1 action."""
        char = _make_character(agility=0)
        self.assertEqual(get_actions_per_turn(char), 1)

    def test_no_base_stats_defaults_to_one(self):
        char = _make_character()
        char.db.base_stats = {}
        self.assertEqual(get_actions_per_turn(char), 1)


class TestDamageModifier(unittest.TestCase):
    """get_damage_modifier scales inversely with action count."""

    def test_one_action_full_damage(self):
        self.assertAlmostEqual(get_damage_modifier(1), 1.0)

    def test_two_actions_reduced(self):
        expected = 1.0 / math.sqrt(2)
        self.assertAlmostEqual(get_damage_modifier(2), expected)

    def test_four_actions_half_damage(self):
        expected = 1.0 / math.sqrt(4)
        self.assertAlmostEqual(get_damage_modifier(4), 0.5)

    def test_zero_treated_as_one(self):
        """Zero actions floor to 1 to avoid division by zero."""
        self.assertAlmostEqual(get_damage_modifier(0), 1.0)


# ---------------------------------------------------------------------------
# Initiative
# ---------------------------------------------------------------------------


class TestInitiative(unittest.TestCase):
    """get_initiative uses agility (characters) or speed (mobs)."""

    @patch("world.base_attributes.random.randint", return_value=10)
    def test_character_initiative(self, mock_rand):
        """Character initiative = agility + d20."""
        char = _make_character(agility=25)
        result = get_initiative(char)
        self.assertEqual(result, 25 + 10)
        mock_rand.assert_called_once_with(1, 20)

    @patch("world.base_attributes.random.randint", return_value=5)
    def test_mob_initiative(self, mock_rand):
        """Mob initiative = int(speed * 10) + d20."""
        mob = _make_mob(speed=1.5)
        result = get_initiative(mob)
        self.assertEqual(result, 15 + 5)

    @patch("world.base_attributes.random.randint", return_value=1)
    def test_mob_default_speed(self, mock_rand):
        """Mob with no speed attribute defaults to 1.0."""
        mob = _make_mob()
        mob.db.speed = None
        # speed defaults to 1.0, int(1.0*10) = 10, plus d20=1 => 11
        result = get_initiative(mob)
        self.assertEqual(result, 10 + 1)


# ---------------------------------------------------------------------------
# Stat Growth
# ---------------------------------------------------------------------------


class TestStatGrowthRates(unittest.TestCase):
    """Diminishing returns brackets for stat XP gain."""

    def test_low_stat_full_rate(self):
        self.assertEqual(_get_stat_growth_rate(0), 1.0)
        self.assertEqual(_get_stat_growth_rate(24), 1.0)

    def test_mid_stat_reduced_rate(self):
        self.assertEqual(_get_stat_growth_rate(25), 0.75)
        self.assertEqual(_get_stat_growth_rate(49), 0.75)

    def test_high_stat_slow_rate(self):
        self.assertEqual(_get_stat_growth_rate(50), 0.40)

    def test_very_high_stat_crawl_rate(self):
        self.assertEqual(_get_stat_growth_rate(75), 0.10)

    def test_near_cap_minimal_rate(self):
        self.assertEqual(_get_stat_growth_rate(90), 0.02)

    def test_at_cap_zero_rate(self):
        self.assertEqual(_get_stat_growth_rate(100), 0.0)


class TestRecordStatUse(unittest.TestCase):
    """record_stat_use accumulates XP on ndb with diminishing returns."""

    def test_known_action_accumulates_xp(self):
        char = _make_character(strength=10)
        record_stat_use(char, "melee_hit")
        acc = char.ndb.stat_xp_accumulators
        # strength at 10 -> rate 1.0 -> 0.5 * 1 * 1.0 = 0.5
        self.assertAlmostEqual(acc["strength"], STAT_XP_PER_USE * 1.0)

    def test_multiple_uses_accumulate(self):
        char = _make_character(strength=10)
        record_stat_use(char, "melee_hit", amount=3)
        acc = char.ndb.stat_xp_accumulators
        self.assertAlmostEqual(acc["strength"], STAT_XP_PER_USE * 3 * 1.0)

    def test_high_stat_diminished_accumulation(self):
        char = _make_character(strength=80)
        record_stat_use(char, "melee_hit")
        acc = char.ndb.stat_xp_accumulators
        # strength at 80 -> rate 0.10
        self.assertAlmostEqual(acc["strength"], STAT_XP_PER_USE * 0.10)

    def test_unknown_action_ignored(self):
        char = _make_character()
        record_stat_use(char, "unknown_action")
        # All accumulators should remain at 0
        for val in char.ndb.stat_xp_accumulators.values():
            self.assertAlmostEqual(val, 0.0)

    def test_no_accumulators_is_noop(self):
        """If ndb.stat_xp_accumulators is None, does nothing."""
        char = _make_character()
        char.ndb.stat_xp_accumulators = None
        record_stat_use(char, "melee_hit")  # should not raise

    def test_all_action_types_mapped(self):
        """Every action type in STAT_GROWTH_ACTIONS maps to a valid stat."""
        for action, stat in STAT_GROWTH_ACTIONS.items():
            self.assertIn(stat, STAT_NAMES)


class TestCommitStatGrowth(unittest.TestCase):
    """commit_stat_growth converts accumulated XP to stat points."""

    def test_enough_xp_increases_stat(self):
        """10 XP = 1 stat point."""
        char = _make_character(strength=10)
        char.ndb.stat_xp_accumulators = {"strength": 10.0}
        char.db.stat_xp = {}
        commit_stat_growth(char)
        self.assertEqual(char.db.base_stats["strength"], 11)

    def test_fractional_xp_stored_as_remainder(self):
        """XP below 10 is stored persistently for later."""
        char = _make_character(strength=10)
        char.ndb.stat_xp_accumulators = {"strength": 7.5}
        char.db.stat_xp = {}
        commit_stat_growth(char)
        # 7.5 XP < 10 threshold, no stat increase
        self.assertEqual(char.db.base_stats["strength"], 10)
        # Remainder stored
        self.assertAlmostEqual(char.db.stat_xp["strength"], 7.5)

    def test_persistent_xp_carries_over(self):
        """Previous remainder combines with new accumulation."""
        char = _make_character(strength=10)
        char.ndb.stat_xp_accumulators = {"strength": 6.0}
        char.db.stat_xp = {"strength": 5.0}
        commit_stat_growth(char)
        # total = 5.0 + 6.0 = 11.0 -> 1 point, remainder 1.0
        self.assertEqual(char.db.base_stats["strength"], 11)
        self.assertAlmostEqual(char.db.stat_xp["strength"], 1.0)

    def test_stat_capped_at_100(self):
        char = _make_character(strength=99)
        char.ndb.stat_xp_accumulators = {"strength": 20.0}
        char.db.stat_xp = {}
        commit_stat_growth(char)
        self.assertEqual(char.db.base_stats["strength"], 100)

    def test_no_accumulators_is_noop(self):
        char = _make_character()
        char.ndb.stat_xp_accumulators = None
        commit_stat_growth(char)  # should not raise

    def test_accumulator_reset_after_commit(self):
        char = _make_character(strength=10)
        char.ndb.stat_xp_accumulators = {"strength": 10.0}
        char.db.stat_xp = {}
        commit_stat_growth(char)
        self.assertAlmostEqual(char.ndb.stat_xp_accumulators["strength"], 0.0)
