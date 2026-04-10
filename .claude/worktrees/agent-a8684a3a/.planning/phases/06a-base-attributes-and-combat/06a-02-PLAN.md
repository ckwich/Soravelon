---
phase: 06a-base-attributes-and-combat
plan: 02
type: execute
wave: 1
depends_on: []
files_modified:
  - world/status_effects.py
autonomous: true
requirements:
  - CMB-01
must_haves:
  truths:
    - "Stackable effects accumulate up to max_stacks with diminishing damage per stack"
    - "Non-stackable effects replace weaker with stronger (higher magnitude)"
    - "Compound triggers fire when both prerequisite effects are present"
    - "Consuming compounds remove both source effects and apply result"
    - "Additive compounds keep both sources and add the compound effect"
    - "tick_effects reduces duration and applies DoT damage each round"
  artifacts:
    - path: "world/status_effects.py"
      provides: "Status effect application, stacking, compounds, tick logic"
      exports: ["STACKABLE_EFFECTS", "NON_STACKABLE_EFFECTS", "COMPOUND_MATRIX", "apply_effect", "remove_effect", "tick_effects", "check_compound_triggers", "clear_all_effects", "has_effect", "get_effect_stacks"]
  key_links:
    - from: "world/status_effects.py"
      to: "ndb.active_effects"
      via: "All functions read/write target.ndb.active_effects list"
      pattern: "ndb\\.active_effects"
---

<objective>
Build the complete status effect system with stackable/non-stackable effects, compound triggers, and per-round tick logic.

Purpose: Status effects are core combat mechanics. DoT builds, crowd control, and compound combos all depend on this module. Must exist before combat engine can resolve ability effects.
Output: world/status_effects.py with all effect constants, application logic, compound matrix, and tick processing.
</objective>

<execution_context>
@C:\Users\colek\.claude\get-shit-done\workflows\execute-plan.md
@C:\Users\colek\.claude\get-shit-done\templates\summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/06a-base-attributes-and-combat/06a-CONTEXT.md
@.planning/phases/06a-base-attributes-and-combat/06A-RESEARCH.md

<interfaces>
<!-- Status effects operate on combatant.ndb.active_effects list -->
<!-- Each effect entry is a dict: {type, stacks, duration, magnitude, source_id, max_stacks} -->
<!-- SaverDict copy pattern required for ndb list mutations -->
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create world/status_effects.py with effect constants and application logic</name>
  <files>world/status_effects.py</files>
  <action>
Create world/status_effects.py implementing the full status effect system per D-23 through D-25.

**Effect constants (from research, vault canonical):**
```python
STACKABLE_EFFECTS = {
    "poison": {"max_stacks": 5, "base_damage": 8, "diminishing": [8, 5, 3, 2, 1]},
    "bleed":  {"max_stacks": 4, "base_damage": 6, "diminishing": [6, 4, 3, 2]},
    "burn":   {"max_stacks": 4, "base_damage": 7, "diminishing": [7, 5, 3, 2]},
    "weaken": {"max_stacks": 3, "reduction_per_stack": 0.08},
    "drain":  {"max_stacks": 2, "drain_per_stack": 5},
}

NON_STACKABLE_EFFECTS = {
    "slow":  {"action_budget_penalty": 1},
    "root":  {"prevents_flee": True},
    "blind": {"miss_chance_increase": 0.25},
    "stun":  {"skip_turn": True},
    "charm": {"skip_turn": True, "no_hostile_action": True},
    "haste": {"action_budget_bonus": 1},
    "wet":   {"burn_chance_reduction": 0.50, "burn_magnitude_reduction": 0.25,
              "action_penalty_on_apply": 1},
}
```

**Compound matrix (per D-24, vault canonical):**
```python
COMPOUND_MATRIX = {
    # Additive compounds: both persist + new effect added
    ("poison", "slow"): {"type": "additive", "result": "venom_lag",
                          "effect": {"bonus_poison_damage": 4}},
    ("weaken", "poison"): {"type": "additive", "result": "corruption",
                            "effect": {"poison_stack_ceiling_bonus": 1}},
    ("slow", "root"): {"type": "additive", "result": "petrify",
                        "effect": {"extended_duration": 2, "breaks_on_damage": True}},
    # Consuming compounds: both consumed, replaced by result
    ("burn", "wet"): {"type": "consuming", "result": "steam",
                       "effect": {"burst_damage_pct": 0.75,
                                  "action_budget_penalty": 1,
                                  "armor_reduction_duration": 2}},
}
```
Store compound keys in both orderings for O(1) lookup: if (a,b) in matrix, also add (b,a) pointing to same entry.

**Core functions:**

apply_effect(target, effect_type, duration, magnitude, source_id) -> (bool, str):
- Check if target has immunity (mob.has_immunity if mob)
- If stackable: find existing effect of same type, increment stacks up to max, refresh duration. If new, create entry with stacks=1.
- If non-stackable: find existing. If existing magnitude >= new magnitude, reject ("A stronger effect is already active"). If new is stronger, replace.
- After application, call check_compound_triggers(target) to detect compounds.
- Use SaverDict copy pattern for ndb.active_effects mutations.
- Return (True, "Poison applied (2 stacks)") or (False, "Immune to poison").

remove_effect(target, effect_type) -> None:
- Remove all entries of this effect_type from active_effects.

has_effect(target, effect_type) -> bool:
- Return True if target has at least one active entry of this type.

get_effect_stacks(target, effect_type) -> int:
- Return current stack count for stackable, 1 for non-stackable if present, 0 if absent.

check_compound_triggers(target) -> list[str]:
- Scan active_effects for any pair matching COMPOUND_MATRIX keys.
- For additive: keep both source effects, add compound effect entry.
- For consuming: remove both source effects, add compound result entry.
- Return list of compound result names that triggered (for combat messaging).
- Only trigger each compound ONCE per application (track in a set during the check).

tick_effects(target) -> list[str]:
- Called at end of each combat round per D-11.
- For each active effect:
  - DoT effects (poison, bleed, burn): deal damage based on stacks and diminishing table. Damage = sum of diminishing[0:stacks]. Reduce target.ndb.hp.
  - Drain: reduce target stamina by drain_per_stack * stacks.
  - Reduce duration by 1. Remove if duration reaches 0.
  - Petrify with breaks_on_damage: check if target took damage this round (via flag), if so remove.
- Return list of message strings describing what happened (for combat log).

clear_all_effects(target) -> None:
- Set target.ndb.active_effects = []. Called at encounter end per D-23.

get_effect_modifiers(target) -> dict:
- Return aggregated modifiers from all active effects: {"action_budget_penalty": N, "action_budget_bonus": N, "miss_chance_increase": float, "skip_turn": bool, "prevents_flee": bool, "damage_reduction": float (from weaken stacks)}
- Combat engine calls this when computing action budgets and checks.
  </action>
  <verify>
    <automated>python -c "from world.status_effects import STACKABLE_EFFECTS, NON_STACKABLE_EFFECTS, COMPOUND_MATRIX, apply_effect, tick_effects, check_compound_triggers, get_effect_modifiers; print('OK:', len(STACKABLE_EFFECTS), 'stackable,', len(NON_STACKABLE_EFFECTS), 'non-stackable,', len(COMPOUND_MATRIX), 'compounds')"</automated>
  </verify>
  <done>world/status_effects.py exists with all stackable/non-stackable effect constants, compound matrix with both orderings, apply/remove/tick/compound functions. All functions use SaverDict copy pattern for ndb mutations. Compound triggers fire correctly for both additive and consuming types.</done>
</task>

</tasks>

<verification>
- All effect types from vault spec are represented in constants
- Compound matrix has entries for all 4 compounds from D-24
- apply_effect for stackable increments stacks correctly
- apply_effect for non-stackable replaces weaker with stronger
- tick_effects deals correct diminishing damage for multi-stack DoTs
- check_compound_triggers detects and resolves burn+wet -> steam
</verification>

<success_criteria>
Status effect system fully implements D-23 through D-25. All stackable effects respect max_stacks with diminishing damage. Non-stackable effects enforce stronger-replaces-weaker. All 4 compound combinations from vault spec trigger correctly. tick_effects processes DoTs with correct damage values. Module is self-contained and importable without combat engine.
</success_criteria>

<output>
After completion, create `.planning/phases/06a-base-attributes-and-combat/06a-02-SUMMARY.md`
</output>
