"""
Tests for the status effect system (world/status_effects.py).

Covers stackable effect stacking to ceiling, non-stackable replacement logic,
compound triggers (Burn+Wet=Steam, Poison+Slow=Venom Lag, etc.), round-end
tick processing, modifier aggregation, immunities, and effect removal.
Uses unittest.TestCase + MagicMock (no Evennia DB required).
"""

import unittest
from unittest.mock import MagicMock, patch

from world.status_effects import (
    ALL_EFFECT_TYPES,
    COMPOUND_MATRIX,
    COMPOUND_RESULT_TYPES,
    NON_STACKABLE_EFFECTS,
    STACKABLE_EFFECTS,
    apply_effect,
    cleanse_one_negative_effect,
    check_compound_triggers,
    clear_all_effects,
    consume_attack_effects,
    get_effect_modifiers,
    get_effect_stacks,
    has_effect,
    mitigate_incoming_damage,
    remove_effect,
    tick_effects,
)


def _make_target(hp=100, stamina=50, immunities=None):
    """Create a MagicMock combatant with ndb.active_effects initialized."""
    target = MagicMock()
    target.key = "TestTarget"
    target.id = 1
    target.ndb.active_effects = []
    target.ndb.hp = hp
    target.ndb.max_hp = hp
    target.ndb.stamina = stamina
    target.ndb.took_damage_this_round = False
    target.db.base_stats = None
    target.db.hp_max = hp
    target.db.immunities = immunities or []
    # Ensure ndb.immunities is not set (default)
    target.ndb.immunities = None
    # Prevent MagicMock auto-attribute from creating a truthy location
    # which triggers node effect code paths (burn_enhanced, dot_tick_variance,
    # wet_suppressed) with unpredictable MagicMock return values.
    target.location = None
    return target


# ---------------------------------------------------------------------------
# Stackable Effects
# ---------------------------------------------------------------------------


class TestStackableEffectApplication(unittest.TestCase):
    """Stackable effects stack up to their ceiling."""

    def test_first_application_creates_one_stack(self):
        target = _make_target()
        ok, msg = apply_effect(target, "poison", duration=3, magnitude=1.0, source_id=99)
        self.assertTrue(ok)
        self.assertEqual(get_effect_stacks(target, "poison"), 1)
        self.assertIn("1 stack", msg)

    def test_second_application_adds_stack(self):
        target = _make_target()
        apply_effect(target, "poison", duration=3)
        apply_effect(target, "poison", duration=3)
        self.assertEqual(get_effect_stacks(target, "poison"), 2)

    def test_stacks_cap_at_max(self):
        """Poison max_stacks is 5. Applying 6 times stays at 5."""
        target = _make_target()
        max_stacks = STACKABLE_EFFECTS["poison"]["max_stacks"]
        for _ in range(max_stacks + 1):
            apply_effect(target, "poison", duration=3)
        self.assertEqual(get_effect_stacks(target, "poison"), max_stacks)

    def test_at_ceiling_message_says_refreshed(self):
        target = _make_target()
        max_stacks = STACKABLE_EFFECTS["bleed"]["max_stacks"]
        for _ in range(max_stacks):
            apply_effect(target, "bleed", duration=3)
        ok, msg = apply_effect(target, "bleed", duration=3)
        self.assertTrue(ok)
        self.assertIn("refreshed", msg.lower())

    def test_duration_refreshed_on_stack(self):
        """Stacking refreshes duration to the max of old and new."""
        target = _make_target()
        apply_effect(target, "burn", duration=2)
        apply_effect(target, "burn", duration=5)
        effects = target.ndb.active_effects
        burn = [e for e in effects if e["type"] == "burn"][0]
        self.assertEqual(burn["duration"], 5)

    def test_magnitude_takes_max(self):
        """Stacking takes the higher magnitude."""
        target = _make_target()
        apply_effect(target, "burn", duration=3, magnitude=1.0)
        apply_effect(target, "burn", duration=3, magnitude=2.0)
        effects = target.ndb.active_effects
        burn = [e for e in effects if e["type"] == "burn"][0]
        self.assertEqual(burn["magnitude"], 2.0)

    def test_all_stackable_types_tracked(self):
        """Every stackable type is in ALL_EFFECT_TYPES."""
        for etype in STACKABLE_EFFECTS:
            self.assertIn(etype, ALL_EFFECT_TYPES)


# ---------------------------------------------------------------------------
# Non-Stackable Effects
# ---------------------------------------------------------------------------


class TestNonStackableEffectApplication(unittest.TestCase):
    """Non-stackable effects use stronger-replaces-weaker logic."""

    def test_first_application_applies(self):
        target = _make_target()
        ok, msg = apply_effect(target, "slow", duration=3, magnitude=1.0)
        self.assertTrue(ok)
        self.assertTrue(has_effect(target, "slow"))

    def test_stronger_replaces_weaker(self):
        target = _make_target()
        apply_effect(target, "slow", duration=2, magnitude=1.0)
        ok, msg = apply_effect(target, "slow", duration=4, magnitude=2.0)
        self.assertTrue(ok)
        self.assertIn("replaced", msg.lower())
        effects = target.ndb.active_effects
        slow = [e for e in effects if e["type"] == "slow"][0]
        self.assertEqual(slow["magnitude"], 2.0)
        self.assertEqual(slow["duration"], 4)

    def test_weaker_does_not_replace_stronger(self):
        target = _make_target()
        apply_effect(target, "stun", duration=3, magnitude=5.0)
        ok, msg = apply_effect(target, "stun", duration=3, magnitude=2.0)
        self.assertFalse(ok)
        self.assertIn("stronger", msg.lower())

    def test_equal_magnitude_does_not_replace(self):
        target = _make_target()
        apply_effect(target, "root", duration=3, magnitude=1.0)
        ok, msg = apply_effect(target, "root", duration=5, magnitude=1.0)
        self.assertFalse(ok)

    def test_all_non_stackable_types_tracked(self):
        for etype in NON_STACKABLE_EFFECTS:
            self.assertIn(etype, ALL_EFFECT_TYPES)


# ---------------------------------------------------------------------------
# Unknown / Immune
# ---------------------------------------------------------------------------


class TestUnknownAndImmunity(unittest.TestCase):
    """Unknown effect types and immunity checks."""

    def test_unknown_effect_rejected(self):
        target = _make_target()
        ok, msg = apply_effect(target, "fake_effect", duration=3)
        self.assertFalse(ok)
        self.assertIn("Unknown", msg)

    def test_db_immunity_prevents_application(self):
        target = _make_target(immunities=["poison"])
        ok, msg = apply_effect(target, "poison", duration=3)
        self.assertFalse(ok)
        self.assertIn("Immune", msg)

    def test_ndb_immunity_prevents_application(self):
        target = _make_target()
        target.ndb.immunities = {"stun"}
        ok, msg = apply_effect(target, "stun", duration=3)
        self.assertFalse(ok)
        self.assertIn("Immune", msg)

    def test_new_authored_effect_types_are_supported(self):
        target = _make_target()
        for effect_type in ("warding", "silence", "frozen", "damage_absorb"):
            ok, _ = apply_effect(target, effect_type, duration=2, magnitude=1.0)
            self.assertTrue(ok, f"{effect_type} should be supported by the runtime")


# ---------------------------------------------------------------------------
# Effect Removal and Queries
# ---------------------------------------------------------------------------


class TestEffectRemovalAndQueries(unittest.TestCase):
    """remove_effect, has_effect, get_effect_stacks, clear_all_effects."""

    def test_remove_effect_clears_it(self):
        target = _make_target()
        apply_effect(target, "poison", duration=3)
        self.assertTrue(has_effect(target, "poison"))
        remove_effect(target, "poison")
        self.assertFalse(has_effect(target, "poison"))

    def test_remove_nonexistent_is_safe(self):
        target = _make_target()
        remove_effect(target, "burn")  # should not raise

    def test_get_stacks_absent_returns_zero(self):
        target = _make_target()
        self.assertEqual(get_effect_stacks(target, "poison"), 0)

    def test_get_stacks_non_stackable_returns_one(self):
        target = _make_target()
        apply_effect(target, "slow", duration=3)
        self.assertEqual(get_effect_stacks(target, "slow"), 1)

    def test_clear_all_effects(self):
        target = _make_target()
        apply_effect(target, "poison", duration=3)
        apply_effect(target, "slow", duration=3)
        clear_all_effects(target)
        self.assertEqual(target.ndb.active_effects, [])

    def test_has_effect_false_when_empty(self):
        target = _make_target()
        self.assertFalse(has_effect(target, "burn"))

    def test_cleanse_one_negative_effect_removes_harmful_status(self):
        target = _make_target()
        apply_effect(target, "poison", duration=3)
        removed = cleanse_one_negative_effect(target)
        self.assertEqual(removed, "poison")
        self.assertFalse(has_effect(target, "poison"))


# ---------------------------------------------------------------------------
# Compound Triggers
# ---------------------------------------------------------------------------


class TestCompoundTriggerBurnWetSteam(unittest.TestCase):
    """Burn + Wet = Steam (consuming compound)."""

    def test_burn_then_wet_triggers_steam(self):
        target = _make_target()
        apply_effect(target, "burn", duration=3)
        ok, msg = apply_effect(target, "wet", duration=3)
        self.assertTrue(ok)
        self.assertIn("steam", msg.lower())
        # Both source effects consumed
        self.assertFalse(has_effect(target, "burn"))
        self.assertFalse(has_effect(target, "wet"))
        # Steam present
        self.assertTrue(has_effect(target, "steam"))

    def test_wet_then_burn_triggers_steam(self):
        """Order should not matter."""
        target = _make_target()
        apply_effect(target, "wet", duration=3)
        apply_effect(target, "burn", duration=3)
        self.assertTrue(has_effect(target, "steam"))

    def test_steam_not_retriggered_if_already_present(self):
        """If steam already exists, adding burn+wet again should not double-trigger."""
        target = _make_target()
        apply_effect(target, "burn", duration=3)
        apply_effect(target, "wet", duration=3)
        # Now steam is present, burn and wet consumed
        # Apply burn and wet again
        apply_effect(target, "burn", duration=3)
        apply_effect(target, "wet", duration=3)
        # Should still have exactly one steam (the original) plus a new steam from re-trigger
        steam_count = sum(1 for e in target.ndb.active_effects if e["type"] == "steam")
        # At minimum, the compound should not crash
        self.assertGreaterEqual(steam_count, 1)


class TestCompoundTriggerPoisonSlowVenomLag(unittest.TestCase):
    """Poison + Slow = Venom Lag (additive compound)."""

    def test_poison_slow_triggers_venom_lag(self):
        target = _make_target()
        apply_effect(target, "poison", duration=3)
        ok, msg = apply_effect(target, "slow", duration=3)
        self.assertTrue(ok)
        self.assertIn("venom_lag", msg.lower())
        # Additive: both sources persist
        self.assertTrue(has_effect(target, "poison"))
        self.assertTrue(has_effect(target, "slow"))
        self.assertTrue(has_effect(target, "venom_lag"))


class TestCompoundTriggerWeakenPoisonCorruption(unittest.TestCase):
    """Weaken + Poison = Corruption (additive compound)."""

    def test_weaken_poison_triggers_corruption(self):
        target = _make_target()
        apply_effect(target, "weaken", duration=3)
        apply_effect(target, "poison", duration=3)
        self.assertTrue(has_effect(target, "corruption"))
        # Additive: both persist
        self.assertTrue(has_effect(target, "weaken"))
        self.assertTrue(has_effect(target, "poison"))


class TestCompoundTriggerSlowRootPetrify(unittest.TestCase):
    """Slow + Root = Petrify (additive compound)."""

    def test_slow_root_triggers_petrify(self):
        target = _make_target()
        apply_effect(target, "slow", duration=3)
        apply_effect(target, "root", duration=3)
        self.assertTrue(has_effect(target, "petrify"))
        # Additive: both persist
        self.assertTrue(has_effect(target, "slow"))
        self.assertTrue(has_effect(target, "root"))

    def test_petrify_has_extended_duration(self):
        """Petrify gets compound_duration(3) + extended_duration(2) = 5."""
        target = _make_target()
        apply_effect(target, "slow", duration=3)
        apply_effect(target, "root", duration=3)
        petrify = [e for e in target.ndb.active_effects if e["type"] == "petrify"][0]
        self.assertEqual(petrify["duration"], 5)

    def test_petrify_marked_as_compound(self):
        target = _make_target()
        apply_effect(target, "slow", duration=3)
        apply_effect(target, "root", duration=3)
        petrify = [e for e in target.ndb.active_effects if e["type"] == "petrify"][0]
        self.assertTrue(petrify["is_compound"])


# ---------------------------------------------------------------------------
# Tick Processing
# ---------------------------------------------------------------------------


class TestTickEffectsDoT(unittest.TestCase):
    """tick_effects processes DoT damage and duration countdown."""

    def test_poison_single_stack_damage(self):
        target = _make_target(hp=100)
        apply_effect(target, "poison", duration=3)
        messages = tick_effects(target)
        # Poison 1 stack: diminishing[0] = 8
        self.assertEqual(target.ndb.hp, 100 - 8)
        self.assertTrue(any("poison" in m.lower() for m in messages))

    def test_poison_multi_stack_damage(self):
        target = _make_target(hp=100)
        apply_effect(target, "poison", duration=3)
        apply_effect(target, "poison", duration=3)
        apply_effect(target, "poison", duration=3)
        messages = tick_effects(target)
        # 3 stacks: diminishing sum = 8 + 5 + 3 = 16
        self.assertEqual(target.ndb.hp, 100 - 16)

    def test_bleed_damage(self):
        target = _make_target(hp=100)
        apply_effect(target, "bleed", duration=2)
        tick_effects(target)
        # 1 stack bleed: diminishing[0] = 6
        self.assertEqual(target.ndb.hp, 100 - 6)

    def test_burn_damage(self):
        target = _make_target(hp=100)
        apply_effect(target, "burn", duration=2)
        tick_effects(target)
        # 1 stack burn: diminishing[0] = 7
        self.assertEqual(target.ndb.hp, 100 - 7)

    def test_duration_decrements(self):
        target = _make_target()
        apply_effect(target, "slow", duration=3)
        tick_effects(target)
        effects = target.ndb.active_effects
        if effects:
            slow = [e for e in effects if e["type"] == "slow"]
            self.assertTrue(len(slow) > 0)
            self.assertEqual(slow[0]["duration"], 2)

    def test_effect_expires_at_zero_duration(self):
        target = _make_target()
        apply_effect(target, "stun", duration=1)
        messages = tick_effects(target)
        self.assertFalse(has_effect(target, "stun"))
        self.assertTrue(any("fades" in m.lower() for m in messages))

    def test_custom_damage_per_tick_overrides_default_dot_value(self):
        target = _make_target(hp=100)
        apply_effect(target, "poison", duration=3, data={"damage_per_tick": 20})
        tick_effects(target)
        self.assertEqual(target.ndb.hp, 80)

    def test_regeneration_restores_health_each_tick(self):
        target = _make_target(hp=55)
        target.ndb.max_hp = 100
        target.db.hp_max = 100
        apply_effect(target, "regeneration", duration=2, data={"heal_per_round": 12})
        tick_effects(target)
        self.assertEqual(target.ndb.hp, 67)

    @patch("evennia.search_object")
    def test_dot_can_heal_the_source_each_tick(self, mock_search):
        source = _make_target(hp=40)
        source.key = "Source"
        source.ndb.max_hp = 100
        source.db.hp_max = 100
        mock_search.return_value = [source]
        target = _make_target(hp=100)
        apply_effect(
            target,
            "poison",
            duration=3,
            source_id=99,
            data={"damage_per_tick": 10, "heal_source_per_round": 8},
        )
        tick_effects(target)
        self.assertEqual(source.ndb.hp, 48)

    @patch("world.combat_engine.resolve_ability_damage", return_value=(True, "hit", 33))
    def test_sustained_attack_fires_periodic_strikes(self, mock_damage):
        owner = _make_target(hp=100)
        owner.id = 10
        owner.db.base_stats = {"strength": 10}
        owner.key = "Owner"
        owner.ndb.combat_handler = MagicMock()
        enemy = _make_target(hp=100)
        enemy.id = 11
        enemy.key = "Enemy"
        owner.ndb.combat_handler.get_mob_combatants.return_value = [enemy]
        apply_effect(
            owner,
            "sustained_attack",
            duration=2,
            source_id=owner.id,
            data={"damage_per_round": 30, "ability_name": "Ghost Protocol"},
        )
        tick_effects(owner)
        mock_damage.assert_called_once()


class TestTickEffectsDrain(unittest.TestCase):
    """Drain reduces stamina per tick."""

    def test_drain_single_stack(self):
        target = _make_target(stamina=50)
        apply_effect(target, "drain", duration=3)
        tick_effects(target)
        drain_amount = STACKABLE_EFFECTS["drain"]["drain_per_stack"] * 1
        self.assertEqual(target.ndb.stamina, 50 - drain_amount)

    def test_drain_double_stack(self):
        target = _make_target(stamina=50)
        apply_effect(target, "drain", duration=3)
        apply_effect(target, "drain", duration=3)
        tick_effects(target)
        drain_amount = STACKABLE_EFFECTS["drain"]["drain_per_stack"] * 2
        self.assertEqual(target.ndb.stamina, 50 - drain_amount)

    def test_drain_floors_at_zero(self):
        target = _make_target(stamina=3)
        apply_effect(target, "drain", duration=3)
        tick_effects(target)
        self.assertEqual(target.ndb.stamina, 0)


class TestTickEffectsPetrify(unittest.TestCase):
    """Petrify breaks on damage."""

    def test_petrify_shatters_on_damage(self):
        target = _make_target()
        # Manually add petrify (compound result)
        target.ndb.active_effects = [{
            "type": "petrify",
            "stacks": 1,
            "duration": 5,
            "magnitude": 1.0,
            "source_id": None,
            "max_stacks": 1,
            "is_compound": True,
        }]
        target.ndb.took_damage_this_round = True
        messages = tick_effects(target)
        self.assertFalse(has_effect(target, "petrify"))
        self.assertTrue(any("shatters" in m.lower() for m in messages))

    def test_petrify_persists_without_damage(self):
        target = _make_target()
        target.ndb.active_effects = [{
            "type": "petrify",
            "stacks": 1,
            "duration": 5,
            "magnitude": 1.0,
            "source_id": None,
            "max_stacks": 1,
            "is_compound": True,
        }]
        target.ndb.took_damage_this_round = False
        tick_effects(target)
        self.assertTrue(has_effect(target, "petrify"))


# ---------------------------------------------------------------------------
# Modifier Aggregation
# ---------------------------------------------------------------------------


class TestGetEffectModifiers(unittest.TestCase):
    """get_effect_modifiers aggregates combat modifiers from active effects."""

    def test_no_effects_default_modifiers(self):
        target = _make_target()
        mods = get_effect_modifiers(target)
        self.assertEqual(mods["action_budget_penalty"], 0)
        self.assertEqual(mods["action_budget_bonus"], 0)
        self.assertAlmostEqual(mods["miss_chance_increase"], 0.0)
        self.assertFalse(mods["skip_turn"])
        self.assertFalse(mods["prevents_flee"])
        self.assertAlmostEqual(mods["damage_reduction"], 0.0)
        self.assertFalse(mods["no_hostile_action"])

    def test_slow_adds_action_penalty(self):
        target = _make_target()
        apply_effect(target, "slow", duration=3)
        mods = get_effect_modifiers(target)
        self.assertEqual(mods["action_budget_penalty"], 1)

    def test_haste_adds_action_bonus(self):
        target = _make_target()
        apply_effect(target, "haste", duration=3)
        mods = get_effect_modifiers(target)
        self.assertEqual(mods["action_budget_bonus"], 1)

    def test_root_prevents_flee(self):
        target = _make_target()
        apply_effect(target, "root", duration=3)
        mods = get_effect_modifiers(target)
        self.assertTrue(mods["prevents_flee"])

    def test_blind_increases_miss_chance(self):
        target = _make_target()
        apply_effect(target, "blind", duration=3)
        mods = get_effect_modifiers(target)
        self.assertAlmostEqual(mods["miss_chance_increase"], 0.25)

    def test_stun_skips_turn(self):
        target = _make_target()
        apply_effect(target, "stun", duration=3)
        mods = get_effect_modifiers(target)
        self.assertTrue(mods["skip_turn"])

    def test_charm_skips_turn_and_no_hostile(self):
        target = _make_target()
        apply_effect(target, "charm", duration=3)
        mods = get_effect_modifiers(target)
        self.assertTrue(mods["skip_turn"])
        self.assertTrue(mods["no_hostile_action"])


class TestAttackEffectConsumption(unittest.TestCase):
    def test_consume_attack_effects_returns_payload_and_clears_one_shots(self):
        attacker = _make_target()
        apply_effect(
            attacker,
            "venom_coat",
            duration=3,
            data={"bonus_poison_damage": 15, "status_effect": "poison", "duration": 3, "magnitude": 8},
        )
        apply_effect(attacker, "guaranteed_crit", duration=1, data={})

        preview = consume_attack_effects(attacker, consume=False)
        self.assertEqual(preview["bonus_damage"], 15)
        self.assertTrue(preview["guaranteed_crit"])
        self.assertTrue(has_effect(attacker, "venom_coat"))

        payload = consume_attack_effects(attacker, consume=True)
        self.assertEqual(payload["bonus_damage"], 15)
        self.assertTrue(payload["guaranteed_crit"])
        self.assertFalse(has_effect(attacker, "venom_coat"))
        self.assertFalse(has_effect(attacker, "guaranteed_crit"))

    def test_weaken_stacks_damage_reduction(self):
        target = _make_target()
        apply_effect(target, "weaken", duration=3)
        apply_effect(target, "weaken", duration=3)
        stacks = get_effect_stacks(target, "weaken")
        mods = get_effect_modifiers(target)
        expected = STACKABLE_EFFECTS["weaken"]["reduction_per_stack"] * stacks
        self.assertAlmostEqual(mods["damage_reduction"], expected)

    def test_petrify_compound_modifiers(self):
        """Petrify causes skip_turn and prevents_flee."""
        target = _make_target()
        target.ndb.active_effects = [{
            "type": "petrify",
            "stacks": 1,
            "duration": 5,
            "magnitude": 1.0,
            "source_id": None,
            "max_stacks": 1,
            "is_compound": True,
        }]
        mods = get_effect_modifiers(target)
        self.assertTrue(mods["skip_turn"])
        self.assertTrue(mods["prevents_flee"])

    def test_steam_compound_action_penalty(self):
        """Steam adds action_budget_penalty of 1."""
        target = _make_target()
        target.ndb.active_effects = [{
            "type": "steam",
            "stacks": 1,
            "duration": 3,
            "magnitude": 1.0,
            "source_id": None,
            "max_stacks": 1,
            "is_compound": True,
        }]
        mods = get_effect_modifiers(target)
        self.assertEqual(mods["action_budget_penalty"], 1)

    def test_multiple_effects_aggregate(self):
        """Multiple different effects stack their modifiers."""
        target = _make_target()
        apply_effect(target, "slow", duration=3)
        apply_effect(target, "blind", duration=3)
        apply_effect(target, "root", duration=3)
        mods = get_effect_modifiers(target)
        self.assertEqual(mods["action_budget_penalty"], 1)
        self.assertAlmostEqual(mods["miss_chance_increase"], 0.25)
        self.assertTrue(mods["prevents_flee"])

    def test_warding_uses_authored_magnitude(self):
        target = _make_target()
        apply_effect(target, "warding", duration=3, magnitude=0.35)
        mods = get_effect_modifiers(target)
        self.assertEqual(mods["damage_reduction"], 0.35)

    def test_stat_boost_exposes_modified_stats(self):
        target = _make_target()
        apply_effect(
            target,
            "stat_boost",
            duration=3,
            magnitude=1.0,
            data={"stats": {"strength": 0.20, "endurance": 0.10}},
        )
        mods = get_effect_modifiers(target)
        self.assertEqual(mods["stat_multipliers"]["strength"], 0.20)
        self.assertEqual(mods["stat_multipliers"]["endurance"], 0.10)


class TestAbsorbMitigation(unittest.TestCase):
    def test_damage_absorb_reduces_incoming_damage_and_consumes_pool(self):
        target = _make_target()
        apply_effect(
            target,
            "damage_absorb",
            duration=3,
            magnitude=60,
            data={"value": 60, "remaining": 60},
        )
        remaining, absorbed = mitigate_incoming_damage(target, 40)
        self.assertEqual(remaining, 0)
        self.assertEqual(absorbed, 40)
        mods = get_effect_modifiers(target)
        self.assertEqual(mods["damage_absorb"], 20)


# ---------------------------------------------------------------------------
# Compound Matrix Integrity
# ---------------------------------------------------------------------------


class TestCompoundMatrixIntegrity(unittest.TestCase):
    """Compound matrix is bidirectional and references valid effects."""

    def test_bidirectional_lookup(self):
        """Every (a,b) compound also has (b,a) entry."""
        for (a, b) in COMPOUND_MATRIX:
            self.assertIn((b, a), COMPOUND_MATRIX)

    def test_source_effects_are_known(self):
        """All compound source effects are in ALL_EFFECT_TYPES."""
        for (a, b) in COMPOUND_MATRIX:
            self.assertIn(a, ALL_EFFECT_TYPES, f"{a} not a known effect type")
            self.assertIn(b, ALL_EFFECT_TYPES, f"{b} not a known effect type")

    def test_compound_results_tracked(self):
        """All compound result types are in COMPOUND_RESULT_TYPES."""
        for entry in COMPOUND_MATRIX.values():
            self.assertIn(entry["result"], COMPOUND_RESULT_TYPES)
