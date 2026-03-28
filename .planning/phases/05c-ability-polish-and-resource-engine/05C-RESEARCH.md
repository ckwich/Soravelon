# Phase 5c: Ability Polish & Resource Engine - Research

**Researched:** 2026-03-27
**Domain:** Ability redesign + domain resource system implementation (Python, Evennia, game engine)
**Confidence:** HIGH

## Summary

Phase 5c has two workstreams: (1) fix ~18 redundant abilities across 8 domains so every ability is loadout-worthy, and (2) implement all 10 domain resource systems in `ability_engine.py` with distinct build/spend/decay mechanics. The current resource system is a generic pool (`build_domain_resource`, `spend_domain_resource`, `get_domain_resource`, `initialize_domain_resource`) that treats all domains identically. It needs to become resource-type-aware to handle Focus combo points (cap 5, reset on miss), Balance pendulum (0-100 spectrum, shifts not spends), Resonance decay (-10/round), Influence from Reputation score, Momentum from hits taken, etc.

The ability data layer is already well-prepared. Phase 5b authored all 330 abilities with effect_params containing `is_builder`, `consumes_all_focus`, `balance_shift`, `balance_type`, and `resonance_generated` fields. The engine just doesn't read or act on them yet. The combat integration points are clear: `use_ability()` for spend/build, `end_round()` for per-round decay, `end_combat()` for encounter-end resets, and `resolve_basic_attack()` for Momentum build-on-hit.

**Primary recommendation:** Implement resource handlers as a function dispatch table keyed by resource type string (matching FINGERPRINTS resource_type), called from the existing `_check_and_spend_resource`, `build_domain_resource`, and `initialize_domain_resource` functions. This keeps the existing API stable while adding type-aware behavior.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- D-01: ~18 abilities across 8 domains need redesign. Each must gain a unique mechanic that makes it attractive alongside its tier-mates. No ability should be strictly worse than another at the same or higher tier within its domain.
- D-02: Fix approach: redesign the weaker ability with a new secondary effect, condition, or unique mechanic -- don't just bump damage numbers. The goal is loadout CHOICES, not power inflation.
- D-03: All 10 resource systems implemented as handlers in ability_engine.py. Each resource has distinct build/spend/decay mechanics.
- D-04: Momentum (Combat) -- builds on hits landed AND damage taken. Decays between encounters only. Pool-style resource.
- D-05: Focus (Subterfuge) -- Combo point system, cap 5. Builders generate 1 on hit. Miss = reset to 0. Skip Subterfuge turn = reset to 0. Spenders cost 1-5. consumes_all_focus abilities scale with Focus spent. Persists between turns, not encounters.
- D-06: Balance (Naturalism) -- Pendulum spectrum 0-100 (0=Feral, 100=Calm, 50=start). NOT a pool. Calm abilities push toward Feral (negative shift), Feral abilities push toward Calm (positive shift). Damage scales with Feral position, heals scale with Calm position. resource_cost always 0.
- D-07: Resonance -- Builder/spender. Builders (cost 0) generate resonance. Spenders at thresholds 60/80/100. Decay: -10 per round during combat. No decay between encounters. Cap 100.
- D-08: Mana (Arcana) -- Traditional pool. Persists across encounters. Regenerates slowly between encounters (meditation). Largest pool size.
- D-09: Influence (Diplomacy) -- Reputation-fueled pool. Starting pool each encounter = f(Reputation dimension score). Does NOT regenerate in-combat. Rationing like mana but encounter-scoped.
- D-10: Reagents (Alchemy) -- Finite consumable stock. Does NOT regenerate in combat or between encounters. Replenished only through gathering/purchasing. Running out mid-fight is intentional.
- D-11: Command (Tactics) -- Builds on ally actions in same round. Solo rate: builds at 50% rate without allies. Decays between encounters.
- D-12: Components (Engineering) -- Finite consumable stock like Reagents. Pre-crafted. Does NOT regenerate.
- D-13: Echoes (Remnance) -- Builds from abilities used in combat. Investigation bonus: +15 per lore fragment, +10 per ancient site, persists 3 encounters, stacks to 40 starting echoes. Decays between encounters.

### Specific Redundancies to Fix
- Combat: press_the_line (T1, 30 dmg) -- identical to crushing_advance but weaker
- Subterfuge: death_of_a_thousand_reads (T4, 180 dmg) -- dominated by phantom_execution
- Arcana: arcane_bolt (T1, 35 dmg), frost_shard (T1, 30 dmg) -- dominated by spark_jolt
- Arcana: meteor_strike (T4, 200 dmg), absolute_zero (T4, 180 dmg) -- dominated by arcane_cataclysm
- Resonance: dissonance_wave (T2), echo_mend (T2), harmonic_shield (T3) -- niche/situational
- Naturalism: bramble_burst (T2), thorn_lash (T1) -- superseded by higher tiers. Calm abilities need variety
- Alchemy: venom_coat (T1), smoke_screen (T1) -- superseded by T2 versions
- Engineering: enhanced_fuel_injection (T2) -- superseded by overcharge_protocol (T3)
- Remnance: fragment_pulse (T1), forgotten_impact (T2), pre_curse_strike (T3) -- weaker versions. Weaken debuff undifferentiated across tiers

### Claude's Discretion
- Exact redesign of each redundant ability (within the constraint: must be loadout-worthy)
- Resource pool sizes and formulas (within vault-defined parameters)
- Implementation pattern for resource handlers (function dispatch, class hierarchy, or simple if/elif)
- Test coverage granularity for resource systems

### Deferred Ideas (OUT OF SCOPE)
- Typed resource gathering/inventory for Engineering components and Alchemy reagents
- Resource UI display in combat prompt (needs client/OOB integration)
- Balance tuning from playtesting (Phase 7+)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| ABL-04 | All 90 subclasses have mechanically distinct ability sets (4 tiers each) | Redundancy fixes ensure all 330 abilities are loadout-worthy; resource engine implementation makes domains play differently in combat |
</phase_requirements>

## Project Constraints (from CLAUDE.md)

- Store game state on `db` (persisted) or `ndb` (volatile) -- never raw Django fields on typeclasses
- All game logic lives in `world/` modules; typeclasses call into them
- Return `(bool, str)` tuples from game logic -- no exceptions for normal flow
- SaverDict copy pattern: copy `db.*` dict to plain dict, mutate, assign once
- OOB messages go through `oob_publisher` -- never call `character.msg()` directly for OOB
- Tests use `EvenniaTestCase` or `unittest.TestCase` with MagicMock for pure logic
- Room state flags must be defined in `FLAG_VOCABULARY` before use

## Standard Stack

No new libraries needed. This phase is entirely within existing codebase:

### Core
| Module | Purpose | Why |
|--------|---------|-----|
| `world/ability_engine.py` | Resource handlers + ability dispatch | Already owns resource management and ability execution |
| `world/ability_registry.py` | Ability data definitions (330 entries) | Where redundant abilities get redesigned |
| `world/combat_script.py` | Round lifecycle hooks | Where per-round decay and encounter-end resets trigger |
| `world/combat_engine.py` | Damage resolution | Where Momentum build-on-hit triggers; Balance scaling hooks |

### Supporting
| Module | Purpose | When Used |
|--------|---------|-----------|
| `world/guild_engine.py` | FINGERPRINTS dict (resource types per domain) | Resource initialization reads resource_type |
| `world/world_state.py` | `get_dimension_score()` for Reputation | Influence pool calculation at encounter start |
| `world/status_effects.py` | Status effect application | Already integrated, no changes needed |
| `world/base_attributes.py` | `record_stat_use()` | Already integrated, no changes needed |

## Architecture Patterns

### Resource Handler Dispatch Pattern

The recommended implementation pattern is a **function dispatch table** keyed by `resource_type` string. This matches the existing `EFFECT_HANDLERS` pattern in ability_engine.py and the `condition vocabulary` pattern in combat_ai.py.

```python
# In ability_engine.py

RESOURCE_HANDLERS = {
    "momentum": _handle_momentum,
    "focus": _handle_focus,
    "balance": _handle_balance,
    "resonance": _handle_resonance,
    "mana": _handle_mana,
    "influence": _handle_influence,
    "reagents": _handle_reagents,
    "command": _handle_command,
    "components": _handle_components,
    "echoes": _handle_echoes,
}
```

Each handler is called from the modified `_check_and_spend_resource()` and returns `(bool, str)`. The handler decides how to interpret the ability's `resource_cost`, `effect_params.is_builder`, `effect_params.balance_shift`, etc.

### Domain Resource ndb Shape (Enhanced)

The current `ndb.domain_resource` dict stores `{type, current, max}`. For Focus and Balance, the shape needs extension:

```python
# Focus (Subterfuge)
character.ndb.domain_resource = {
    "type": "focus",
    "current": 0,   # combo points (0-5)
    "max": 5,
}

# Balance (Naturalism)
character.ndb.domain_resource = {
    "type": "balance",
    "current": 50,   # pendulum position (0=Feral, 100=Calm)
    "max": 100,
}

# Influence (Diplomacy) -- encounter-scoped
character.ndb.domain_resource = {
    "type": "influence",
    "current": 35,    # remaining pool
    "max": 35,         # calculated from Reputation at encounter start
}
```

### Integration Points in Combat Lifecycle

| Event | Resource Action | Where |
|-------|----------------|-------|
| Encounter start | `initialize_domain_resource()` -- type-aware init | `combat_script.py:start_combat()` |
| Ability use (pre) | `_check_and_spend_resource()` -- type-aware spend/build | `ability_engine.py:use_ability()` |
| Ability hit | Build Focus (if is_builder), build Momentum | `ability_engine.py:use_ability()` after handler |
| Ability miss | Reset Focus to 0 | `ability_engine.py:use_ability()` on miss |
| Basic attack hit | Build Momentum | `combat_engine.py:resolve_basic_attack()` |
| Damage taken | Build Momentum | `combat_engine.py` damage resolution |
| Round end | Resonance decay (-10), Focus skip-turn reset | `combat_script.py:end_round()` |
| Ally acts | Build Command | `combat_script.py:process_player_action()` or `end_round()` |
| Encounter end | Reset Focus, Resonance persists, Momentum decays, Mana persists | `combat_script.py:end_combat()` |

### Ability Redesign Pattern

For each redundant ability, the fix follows this template:
1. Identify what niche is unfilled in that tier/domain
2. Add a unique mechanic via `effect_params` (new status effect, conditional bonus, positional advantage, multi-target, ramp-up, etc.)
3. Ensure the ability is competitive with -- but not strictly better than -- its tier-mates
4. Update `description` to reflect the new identity

### Anti-Patterns to Avoid
- **Power creep via number bumps:** Don't fix redundancy by just increasing damage_base. The goal is unique mechanics, not bigger numbers.
- **Modifying EFFECT_HANDLERS for resource logic:** Resource handling is separate from effect handling. Don't mix them.
- **Hardcoding resource type checks in use_ability:** Use the dispatch table pattern, not if/elif chains in the main function.
- **Storing resource state in db:** Resources are volatile combat state -- always `ndb`. Only Reagents/Components (inventory-backed) might eventually need persistence, but that's deferred.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Dimension score lookup | Custom Reputation query | `world_state.get_dimension_score(char, "reputation")` | Already exists, returns float |
| Status effect application | Custom effect logic | `status_effects.apply_effect()` | Already handles stacking, immunity, compounds |
| Damage scaling | New damage formula | `combat_engine.resolve_ability_damage()` | Already reads effect_params.damage_base + stat scaling |
| Group member iteration | Custom group lookup | `group_engine._get_group_members()` | Already used by tactical handler |

## Common Pitfalls

### Pitfall 1: SaverDict Mutation Trap
**What goes wrong:** Mutating `character.ndb.domain_resource["current"]` directly sometimes silently fails or triggers excessive re-pickle.
**Why it happens:** Evennia's `ndb` uses SaverDict in some contexts.
**How to avoid:** Always copy to plain dict, mutate, assign back -- as `build_domain_resource()` already does: `res = dict(res); res["current"] = ...; character.ndb.domain_resource = res`.
**Warning signs:** Resource values not updating after operations.

### Pitfall 2: Focus Reset Timing
**What goes wrong:** Focus resets at wrong time (start of turn vs end of miss resolution).
**Why it happens:** Multiple places could trigger reset -- miss handler, turn-skip detection, encounter end.
**How to avoid:** Focus reset on miss must happen in the ability resolution path (after hit/miss is determined). Turn-skip detection must happen at end_round when checking if a Subterfuge character acted. Encounter-end reset happens in end_combat.
**Warning signs:** Focus persisting after a miss, or resetting at wrong moments.

### Pitfall 3: Balance Pendulum Off-by-One
**What goes wrong:** Balance shifts that should clamp at 0 or 100 go out of range or don't clamp.
**Why it happens:** Missing bounds check on the pendulum shift.
**How to avoid:** Always `max(0, min(100, current + shift))`. Balance is never spent (resource_cost=0), only shifted.
**Warning signs:** Balance values outside 0-100 range.

### Pitfall 4: Resonance Decay Stacking
**What goes wrong:** Resonance decays too fast because decay is applied per-combatant-tick instead of once per round.
**Why it happens:** `end_round()` iterates all combatants -- if decay is in the per-combatant loop, it triggers for each combatant but should only apply to the Resonance user.
**How to avoid:** Decay only applies to combatants whose `ndb.domain_resource["type"] == "resonance"`. The per-combatant loop is correct as long as each combatant's own resource is checked.
**Warning signs:** Resonance dropping to 0 in 2-3 rounds instead of 10.

### Pitfall 5: Influence Pool Initialization Ordering
**What goes wrong:** Influence pool is 0 because Reputation score isn't available at combat start.
**Why it happens:** `get_dimension_score()` requires the character object to have `db.reputation_score`.
**How to avoid:** Characters always have `db.reputation_score` (defaults to 0 via lazy init pattern). The formula f(reputation) must handle 0 gracefully -- a new Diplomacy character should still get a small starting pool.
**Warning signs:** All Diplomacy characters starting combat with 0 Influence.

### Pitfall 6: Momentum Double-Build
**What goes wrong:** Momentum builds twice from a single damage ability (once from ability resolution, once from hit detection).
**Why it happens:** Both `resolve_ability_damage()` and `use_ability()` try to build momentum.
**How to avoid:** Momentum build-on-hit triggers in ONE place only. The cleanest spot is post-ability-resolution in `use_ability()`, gated by `resource_type == "momentum"`. Basic attack build happens in `resolve_basic_attack()` return path.
**Warning signs:** Momentum jumping by 20+ per ability instead of 10.

### Pitfall 7: Circular Import with world_state
**What goes wrong:** Importing `world_state.get_dimension_score` at module level causes circular import.
**Why it happens:** `ability_engine` -> `world_state` -> `models` -> potential back-reference.
**How to avoid:** Lazy import inside the Influence handler function, matching the existing pattern in ability_engine.py.
**Warning signs:** ImportError at module load time.

## Code Examples

### Resource Handler: Focus (Combo Points)

```python
def _handle_focus_spend(character, ability):
    """Focus combo point system: build on hit, spend 1-5, reset on miss."""
    params = ability.get("effect_params", {})
    res = dict(character.ndb.domain_resource)

    if params.get("is_builder"):
        # Builders cost nothing -- Focus generated AFTER hit resolution
        return True, ""

    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""

    if params.get("consumes_all_focus"):
        if res["current"] < 1:
            return False, "No Focus points to spend."
        # Will consume all on resolution -- allow the spend
        return True, ""

    if res["current"] < cost:
        return False, f"Insufficient Focus ({res['current']}/{cost} needed)."

    res["current"] -= cost
    character.ndb.domain_resource = res
    return True, ""
```

### Resource Handler: Balance (Pendulum Shift)

```python
def _handle_balance_spend(character, ability):
    """Balance pendulum: shift position, never spend. resource_cost always 0."""
    params = ability.get("effect_params", {})
    shift = params.get("balance_shift", 0)
    if shift == 0:
        return True, ""

    res = dict(character.ndb.domain_resource)
    res["current"] = max(0, min(100, res["current"] + shift))
    character.ndb.domain_resource = res
    return True, ""
```

### Resonance Decay in end_round

```python
# In combat_script.py:end_round(), after ticking effects and cooldowns:
from world.ability_engine import decay_resonance

for combatant in self._resolve_combatants():
    if combatant is None:
        continue
    # ... existing tick_effects, decrement_cooldowns ...
    decay_resonance(combatant)  # -10 if resource_type is resonance
```

### Focus Build on Hit

```python
# In ability_engine.py:use_ability(), after effect handler succeeds:
if ability.get("effect_params", {}).get("is_builder"):
    res = character.ndb.domain_resource
    if res and res["type"] == "focus":
        # Check if the ability hit (handler returned success)
        res = dict(res)
        res["current"] = min(res["max"], res["current"] + 1)
        character.ndb.domain_resource = res
```

### Focus Reset on Miss

```python
# When resolve_ability_damage returns miss (ok=False):
def _handle_focus_miss(character):
    """Reset Focus to 0 on miss."""
    res = character.ndb.domain_resource
    if res and res["type"] == "focus":
        res = dict(res)
        res["current"] = 0
        character.ndb.domain_resource = res
```

### Balance Scaling Hook

```python
def get_balance_modifier(character, balance_type):
    """Return damage/heal modifier based on Balance position."""
    res = character.ndb.domain_resource
    if not res or res["type"] != "balance":
        return 1.0
    position = res["current"]  # 0=Feral, 100=Calm
    if balance_type == "feral":
        # Damage scales with Feral position (lower = stronger)
        return 1.0 + (50 - position) * 0.01  # e.g., position 0 = 1.5x, position 50 = 1.0x
    elif balance_type == "calm":
        # Heal scales with Calm position (higher = stronger)
        return 1.0 + (position - 50) * 0.01  # e.g., position 100 = 1.5x, position 50 = 1.0x
    return 1.0
```

### Influence Initialization from Reputation

```python
def _initialize_influence(character):
    """Set Influence pool from Reputation dimension score."""
    from world.world_state import get_dimension_score
    rep_score = get_dimension_score(character, "reputation")
    # Pool = 20 base + reputation * 0.5 (0 rep = 20 pool, 100 rep = 70 pool)
    pool = int(20 + rep_score * 0.5)
    character.ndb.domain_resource = {
        "type": "influence",
        "current": pool,
        "max": pool,
    }
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Generic resource pool (all domains same) | Type-aware resource handlers | Phase 5c (now) | Each domain plays mechanically differently |
| Stub effect handlers | Real combat-wired handlers | Phase 6a (done) | Abilities resolve actual damage/effects |
| ~20 stub abilities | 330 authored abilities | Phase 5b (done) | Full content, but ~18 have redundancy issues |

## Open Questions

1. **Momentum build amount per hit**
   - What we know: Builds on hits landed AND damage taken. Decays between encounters.
   - What's unclear: Exact amount per hit (5? 10? proportional to damage?). Amount on damage taken.
   - Recommendation: Use fixed amounts (10 per hit landed, 5 per hit taken) -- simple, predictable. Ability costs in registry already assume pool-style spend.

2. **Command build-on-ally-action granularity**
   - What we know: Builds when allies act in same round. Solo rate 50%.
   - What's unclear: How to detect "ally acted this round" in combat_script round tracking.
   - Recommendation: Track in end_round -- count player actions this round via a simple counter on the script. Each allied action adds Command to Tactics characters.

3. **Echoes investigation bonus persistence**
   - What we know: +15 per lore fragment, +10 per ancient site, persists 3 encounters, stacks to 40 starting echoes.
   - What's unclear: Where to store the investigation bonus counter (encounters remaining). ndb won't survive disconnect.
   - Recommendation: Use `db.echoes_investigation_bonus` (persisted dict with {amount, encounters_remaining}). Decremented at encounter end.

4. **Mana regeneration between encounters**
   - What we know: Regenerates slowly between encounters (meditation).
   - What's unclear: Rate/trigger for regeneration. Timer-based? Action-based?
   - Recommendation: Flat percentage recovery at encounter end (e.g., 10-15% of max). Keep it simple for now; meditation command deferred.

5. **Balance scaling formula**
   - What we know: Damage scales with Feral position (low Balance), heals scale with Calm position (high Balance).
   - What's unclear: Exact multiplier curve (linear? diminishing returns?).
   - Recommendation: Linear 0-50% bonus. Position 0 (full Feral) = 1.5x damage. Position 100 (full Calm) = 1.5x heal. Position 50 (neutral) = 1.0x both. Simple and intuitive.

6. **consumes_all_focus damage scaling formula**
   - What we know: Some Subterfuge capstones consume all Focus and scale with points spent.
   - What's unclear: Exact scaling per Focus point.
   - Recommendation: Base damage * (1 + 0.2 * focus_spent). At 5 Focus = 2.0x base. Makes the full combo feel powerful.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | unittest + MagicMock (project standard for pure logic) |
| Config file | None (inline with `evennia test --settings settings tests/` or `pytest`) |
| Quick run command | `python -m pytest tests/test_ability_engine.py -x` |
| Full suite command | `python -m pytest tests/ -x` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ABL-04-R1 | No obsolete abilities (uniqueness check) | unit | `pytest tests/test_ability_engine.py::TestAbilityRedundancy -x` | Wave 0 |
| ABL-04-R2 | 10 resource systems initialize correctly | unit | `pytest tests/test_ability_engine.py::TestResourceInitialization -x` | Wave 0 |
| ABL-04-R3 | Focus combo: build on hit, reset on miss, cap 5 | unit | `pytest tests/test_ability_engine.py::TestFocusResource -x` | Wave 0 |
| ABL-04-R4 | Balance pendulum: shift, clamp 0-100, scaling modifier | unit | `pytest tests/test_ability_engine.py::TestBalanceResource -x` | Wave 0 |
| ABL-04-R5 | Resonance decay -10/round | unit | `pytest tests/test_ability_engine.py::TestResonanceResource -x` | Wave 0 |
| ABL-04-R6 | Influence pool from Reputation score | unit | `pytest tests/test_ability_engine.py::TestInfluenceResource -x` | Wave 0 |
| ABL-04-R7 | Momentum build on hit/damage taken | unit | `pytest tests/test_ability_engine.py::TestMomentumResource -x` | Wave 0 |
| ABL-04-R8 | Reagents/Components finite stock, no regen | unit | `pytest tests/test_ability_engine.py::TestFiniteResources -x` | Wave 0 |
| ABL-04-R9 | Command build on ally actions, 50% solo rate | unit | `pytest tests/test_ability_engine.py::TestCommandResource -x` | Wave 0 |
| ABL-04-R10 | Echoes build from abilities + investigation bonus | unit | `pytest tests/test_ability_engine.py::TestEchoesResource -x` | Wave 0 |
| ABL-04-R11 | consumes_all_focus scales damage with Focus spent | unit | `pytest tests/test_ability_engine.py::TestFocusScaling -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/test_ability_engine.py -x`
- **Per wave merge:** `python -m pytest tests/ -x`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_ability_engine.py::TestResourceInitialization` -- test all 10 resource types initialize with correct shape
- [ ] `tests/test_ability_engine.py::TestFocusResource` -- Focus combo point lifecycle
- [ ] `tests/test_ability_engine.py::TestBalanceResource` -- Balance pendulum mechanics
- [ ] `tests/test_ability_engine.py::TestResonanceResource` -- Resonance decay
- [ ] `tests/test_ability_engine.py::TestInfluenceResource` -- Influence from Reputation
- [ ] `tests/test_ability_engine.py::TestMomentumResource` -- Momentum build triggers
- [ ] `tests/test_ability_engine.py::TestFiniteResources` -- Reagents/Components depletion
- [ ] `tests/test_ability_engine.py::TestCommandResource` -- Command ally-action build
- [ ] `tests/test_ability_engine.py::TestEchoesResource` -- Echoes investigation bonus
- [ ] `tests/test_ability_engine.py::TestAbilityRedundancy` -- structural uniqueness validation

## Sources

### Primary (HIGH confidence)
- `world/ability_engine.py` -- current resource functions (4 generic functions, 9 effect handlers)
- `world/ability_registry.py` -- 330 ability definitions with effect_params including is_builder, consumes_all_focus, balance_shift, balance_type, resonance_generated
- `world/combat_script.py` -- CombatScript with end_round() at line 592, end_combat() at line 700
- `world/combat_engine.py` -- resolve_basic_attack() at line 121, resolve_ability_damage() at line 237
- `world/guild_engine.py` -- FINGERPRINTS dict with resource_type per domain
- `world/world_state.py` -- get_dimension_score() at line 63, ALL_DIMENSIONS includes "reputation"
- `.claude/skills/combat-system/skill.md` -- comprehensive combat system reference
- `feedback_resource_designs.md` -- user corrections on Focus, Influence, Balance, typed resources

### Secondary (MEDIUM confidence)
- CONTEXT.md D-04 through D-13 -- resource specifications from user discussion

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all code is in existing modules, no new dependencies
- Architecture: HIGH -- dispatch table pattern matches existing codebase patterns (EFFECT_HANDLERS, condition vocabulary)
- Pitfalls: HIGH -- identified from direct code inspection of mutation patterns and integration points
- Ability redesign: MEDIUM -- specific redesigns are Claude's discretion; the constraint (loadout-worthy, not power inflation) is clear but creative application varies

**Research date:** 2026-03-27
**Valid until:** 2026-04-27 (stable internal codebase, no external dependencies)
