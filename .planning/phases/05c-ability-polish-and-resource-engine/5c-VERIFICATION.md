---
phase: 05c-ability-polish-and-resource-engine
verified: 2026-03-27T22:00:00Z
status: gaps_found
score: 3/4 success criteria verified
re_verification: false
gaps:
  - truth: "Typed resource variants for Engineering (component types) and Alchemy (reagent types) have data-layer support (variant fields on abilities)"
    status: failed
    reason: "No reagent_type or component_type variant fields exist on any ability in ability_registry.py. Reagents and Components use a single undifferentiated pool (reagent_stock / component_stock). CONTEXT.md notes this was deferred, but ROADMAP success criterion 4 expects at minimum data-layer fields on abilities."
    artifacts:
      - path: "world/ability_registry.py"
        issue: "No alchemy ability has a reagent_type field; no engineering ability has a component_type field"
      - path: "world/ability_engine.py"
        issue: "_handle_reagents_spend and _handle_components_spend treat resources as generic pools with no type differentiation"
    missing:
      - "Add reagent_type field to alchemy abilities (e.g., 'volatile', 'curative', 'toxic') in effect_params"
      - "Add component_type field to engineering abilities (e.g., 'gear', 'conduit', 'plating') in effect_params"
      - "Update _handle_reagents_spend and _handle_components_spend to read variant fields (even if stock tracking remains a single pool for now)"
---

# Phase 5c: Ability Polish & Resource Engine Verification Report

**Phase Goal:** Fix ~18 redundant/obsolete abilities so every ability is attractive in an 8-slot loadout, and implement all 10 domain resource systems in the ability engine so combat mechanically differentiates every domain
**Verified:** 2026-03-27T22:00:00Z
**Status:** gaps_found
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths (from ROADMAP Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Zero obsolete abilities -- no ability is strictly worse than a tier-mate; every ability brings something unique to a loadout | VERIFIED | 17 abilities redesigned with unique effect_params (piercing, is_multi_hit, aoe, heal_over_time, reflect_damage, bleed, applies_to_next_attack, resource_refund, echoes_generated, ignores_armor). TestAbilityRedundancy passes. 330 total abilities preserved. |
| 2 | All 10 domain resource systems have handler functions that dispatch correctly based on resource_type | VERIFIED | RESOURCE_HANDLERS dict has 10 entries (momentum, focus, balance, resonance, mana, influence, reagents, command, components, echoes). _check_and_spend_resource dispatches via RESOURCE_HANDLERS.get(res["type"]). Type-aware initialize_domain_resource for all 10 types. |
| 3 | Resource-specific ability behaviors work: Focus builders generate points on hit (miss resets), Balance shifts on ability use and scales damage/healing, Resonance decays -10/round during combat | VERIFIED | Focus: _handle_focus_spend with is_builder/consumes_all_focus checks, handle_focus_miss resets to 0, on_round_end_resources resets on skip. Balance: _handle_balance_spend shifts and clamps 0-100, get_balance_modifier returns linear scaling. Resonance: decay_resonance subtracts 10 per round, on_round_end_resources calls it. All wired in combat_script.py and combat_engine.py. 61 tests pass including TestFocusResource (6 tests), TestBalanceResource (5 tests), TestResonanceResource (3 tests). |
| 4 | Typed resource variants for Engineering (component types) and Alchemy (reagent types) have data-layer support (variant fields on abilities) | FAILED | No reagent_type or component_type fields exist on any ability. Reagents and Components are undifferentiated pools. CONTEXT.md explicitly deferred this ("if practical"), but the ROADMAP success criterion expects it. |

**Score:** 3/4 success criteria verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `world/ability_registry.py` | 17 redesigned abilities with unique mechanics | VERIFIED | All 17 abilities confirmed with unique effect_params: press_the_line (debuff/slow), death_of_a_thousand_reads (multi-hit), arcane_bolt (piercing), frost_shard (status/slow), meteor_strike (aoe), absolute_zero (status/frozen), dissonance_wave (aoe+weaken), echo_mend (heal_over_time), harmonic_shield (reflect_damage), bramble_burst (aoe), thorn_lash (bleed), venom_coat (applies_to_next_attack), smoke_screen (aoe+blind), enhanced_fuel_injection (resource_refund), fragment_pulse (echoes_generated), forgotten_impact (ignores_armor), pre_curse_strike (damage+weaken) |
| `world/ability_engine.py` | 10 resource handler functions + dispatch table + lifecycle hooks | VERIFIED | 10 _handle_*_spend functions (lines 207-310), RESOURCE_HANDLERS dict (line 312), _post_ability_resource_hook (line 330), handle_focus_miss (line 376), get_balance_modifier (line 389), decay_resonance (line 408), on_round_end_resources (line 417), on_encounter_end_resources (line 453), build_momentum_on_damage (line 488) |
| `world/combat_script.py` | Per-round resource decay and encounter-end resource lifecycle | VERIFIED | on_round_end_resources called at line 631, on_encounter_end_resources called at line 739, ally_action_count tracking at lines 450/482, reset at line 620 |
| `world/combat_engine.py` | Momentum build on basic attack hit and damage taken | VERIFIED | build_momentum_on_damage(attacker, 10) at line 225, build_momentum_on_damage(target, 5) at lines 226/334, handle_focus_miss at line 265, get_balance_modifier at lines 293/393 |
| `tests/test_ability_engine.py` | Resource system tests + redundancy validation | VERIFIED | 11 test classes: TestResourceInitialization, TestFocusResource, TestBalanceResource, TestResonanceResource, TestInfluenceResource, TestMomentumResource, TestFiniteResources, TestCommandResource, TestEchoesResource, TestFocusScaling, TestAbilityRedundancy. 61 tests, all passing. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| world/ability_engine.py | world/guild_engine.py | FINGERPRINTS resource_type lookup | WIRED | initialize_domain_resource reads FINGERPRINTS[guild_id]["resource_type"] for type-aware branching |
| world/ability_engine.py | world/world_state.py | get_dimension_score for Influence | WIRED | Line uses lazy import for Influence initialization from Reputation score |
| world/combat_script.py | world/ability_engine.py | on_round_end_resources + on_encounter_end_resources | WIRED | Both imported and called at correct lifecycle points (end_round line 631, end_combat line 739) |
| world/combat_engine.py | world/ability_engine.py | build_momentum_on_damage, handle_focus_miss, get_balance_modifier | WIRED | All three imported and called at correct points in resolve_basic_attack and resolve_ability_damage |
| tests/test_ability_engine.py | world/ability_engine.py | imports and function calls | WIRED | All 10 resource handler functions, lifecycle hooks, and helpers imported and tested |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| All abilities load without import errors | `python -c "from world.ability_registry import ABILITIES; print(len(ABILITIES))"` | 330 | PASS |
| 10 resource handlers in dispatch table | `python -c "from world.ability_engine import RESOURCE_HANDLERS; print(len(RESOURCE_HANDLERS))"` | 10 | PASS |
| All exported lifecycle functions importable | `from world.ability_engine import decay_resonance, on_round_end_resources, on_encounter_end_resources, handle_focus_miss, get_balance_modifier, build_momentum_on_damage` | Success | PASS |
| Full test suite passes | `python -m pytest tests/test_ability_engine.py -x` | 61 passed | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| ABL-04 | 5c-01, 5c-02, 5c-03 | All 90 subclasses have mechanically distinct ability sets (4 tiers each) | SATISFIED | 17 redundant abilities redesigned with unique mechanics; TestAbilityRedundancy confirms no two same-tier abilities in a domain share identical (effect_type, effect_params); 10 resource handlers differentiate domain combat |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| None | - | - | - | No TODO/FIXME/PLACEHOLDER/stub patterns found in modified files |

### Human Verification Required

### 1. Loadout Attractiveness in Play

**Test:** Create characters in several domains and build 8-slot loadouts. Verify that no ability feels like a "wasted slot" and each provides a distinct tactical choice.
**Expected:** Players have meaningful decisions about which 8 abilities to equip from their domain+subclass pool.
**Why human:** Loadout attractiveness is a design/feel judgment that cannot be verified by code inspection alone.

### 2. Balance Pendulum Feel

**Test:** Play a Naturalism character and alternate between Feral and Calm abilities. Verify the pendulum swing feels responsive and the 1.5x modifier at extremes creates meaningful gameplay decisions.
**Expected:** Shifting toward Feral for damage then Calm for healing creates a satisfying risk/reward dynamic.
**Why human:** The numerical system exists but whether it creates engaging gameplay requires playtesting.

### 3. Focus Combo Flow

**Test:** Play a Subterfuge character, build Focus through builders, and use spenders. Miss an attack and verify Focus resets to 0.
**Expected:** The build-spend-reset cycle creates tension and rewards accuracy.
**Why human:** Mechanical correctness verified by tests, but gameplay feel requires human judgment.

### Gaps Summary

One gap found against ROADMAP success criterion 4: **Typed resource variants for Engineering and Alchemy are not implemented.** No ability in ability_registry.py has a `reagent_type` or `component_type` field. The `_handle_reagents_spend` and `_handle_components_spend` functions treat these as generic pools with no type differentiation.

The phase CONTEXT.md (line 76) notes this was deferred ("5c only adds the variant data fields to abilities if practical") and lists it under "Deferred Ideas" (line 126). However, the ROADMAP success criterion 4 explicitly expects "data-layer support (variant fields on abilities)." Adding variant fields to effect_params would be a small, low-risk change that satisfies the criterion even without implementing the full gathering/inventory system.

The remaining 3 of 4 success criteria are fully verified with comprehensive test coverage (61 tests passing), all artifacts substantive and wired, and no anti-patterns detected.

---

_Verified: 2026-03-27T22:00:00Z_
_Verifier: Claude (gsd-verifier)_
