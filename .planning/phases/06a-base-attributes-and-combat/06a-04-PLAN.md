---
phase: 06a-base-attributes-and-combat
plan: 04
type: execute
wave: 2
depends_on: ["06a-02"]
files_modified:
  - world/combat_ai.py
autonomous: true
requirements:
  - CMB-03
must_haves:
  truths:
    - "Mob selects abilities based on weight, cooldown state, and target conditions"
    - "Mobs always fall back to basic attack if no ability is usable"
    - "Mob targeting follows last-attacker priority with random fallback"
    - "Named mob scripted sequences fire at HP thresholds and round counts"
  artifacts:
    - path: "world/combat_ai.py"
      provides: "Mob turn AI: ability selection, targeting, sequence triggers"
      exports: ["select_mob_action", "get_mob_target", "check_scripted_sequence", "process_mob_turn"]
  key_links:
    - from: "world/combat_ai.py"
      to: "world/ability_registry.py"
      via: "Reads mob.db.abilities list to find available abilities"
      pattern: "ability_registry"
    - from: "world/combat_ai.py"
      to: "world/status_effects.py"
      via: "Checks target conditions for ability prerequisites"
      pattern: "status_effects\\.has_effect"
---

<objective>
Build the mob combat AI module: ability selection by weighted priority, targeting logic, and named mob scripted sequence execution.

Purpose: Mobs need to act intelligently during their combat turns. This module decides what ability a mob uses and who it targets, making CMB-03 functional.
Output: world/combat_ai.py with mob action selection, targeting, and scripted sequence support.
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

@typeclasses/mobs.py
@world/ability_registry.py

<interfaces>
<!-- Mob ability schema from soravelon-mobs.md vault spec -->
<!-- mob.db.abilities is a list of dicts, each with: -->
```python
{
    "ability_id": "wolf_bite",
    "weight": 60,           # selection weight (higher = more likely)
    "cooldown": 2,          # rounds between uses
    "condition": None,       # condition string: "target_below_50hp", "no_allies_alive", etc.
    "element": "physical",
    "damage_base": 12,
    "status_effect": None,   # optional: "bleed", "poison", etc.
    "effect_duration": 3,
    "effect_magnitude": 6,
    "application_chance": 0.8,
}
```

<!-- From Plan 02: world/status_effects.py -->
```python
def has_effect(target, effect_type) -> bool: ...
def get_effect_stacks(target, effect_type) -> int: ...
```

<!-- Mob targeting from soravelon-mobs.md -->
<!-- 1. Target whoever most recently damaged the mob -->
<!-- 2. No damage yet: random valid target in room -->
<!-- 3. Current target flees: re-roll random -->
<!-- 4. Vanish: cannot be targeted for one round -->
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create world/combat_ai.py with ability selection, targeting, and scripted sequences</name>
  <files>world/combat_ai.py</files>
  <action>
Create world/combat_ai.py implementing mob AI for combat turns per D-13, CMB-03, and vault mob spec.

**Condition vocabulary (from soravelon-mobs.md):**
CONDITION_CHECKS dict mapping condition strings to lambda/function evaluators:
- "target_below_50hp": target.ndb.hp < derive_max_hp(target) * 0.5
- "target_below_25hp": target.ndb.hp < derive_max_hp(target) * 0.25
- "self_below_50hp": mob.ndb.hp < mob.db.hp_max * 0.5
- "self_below_25hp": mob.ndb.hp < mob.db.hp_max * 0.25
- "target_has_poison": has_effect(target, "poison")
- "target_has_bleed": has_effect(target, "bleed")
- "target_has_burn": has_effect(target, "burn")
- "no_allies_alive": no other mobs in room's combat
- "allies_present": other mobs in room's combat
- None: always passes (unconditional)

**check_condition(condition_str, mob, target, combat_handler) -> bool:**
- Look up condition in CONDITION_CHECKS, evaluate, return bool.
- Unknown conditions return False (safe fallback).

**Ability selection:**
select_mob_action(mob, target, combat_handler) -> dict:
- Read mob.db.abilities list.
- Filter to abilities NOT on cooldown (check mob.ndb.ability_cooldowns dict, same pattern as player abilities).
- Filter to abilities whose condition passes (check_condition).
- If no abilities pass: return basic_attack action dict.
- Weight-based random selection from remaining abilities: random.choices with weights.
- Return selected ability dict. The action dict should include a "type" field: "ability" or "basic_attack".

**Basic attack fallback (per Pitfall 7):**
- Every mob always has a basic attack available: use mob.db.ref_damage_min/max with "physical" element.
- Return {"type": "basic_attack", "element": "physical"}.

**Targeting (per soravelon-mobs.md):**
get_mob_target(mob, combat_handler) -> target|None:
- Priority 1: mob.ndb.last_attacker_id — whoever most recently damaged this mob.
- Priority 2: random valid target from players in combat (combat_handler.get_player_combatants()).
- Priority 3: None (no valid targets — combat should end).
- Skip targets with "vanish" effect active (cannot be targeted for one round).
- If current target fled the room, re-roll random.

**Scripted sequences (from soravelon-mobs.md):**
check_scripted_sequence(mob, combat_handler) -> list[dict]|None:
- Read mob.db.scripted_sequence list (if exists, for named mobs).
- Check each sequence entry's trigger against current state:
  - "combat_start": fires once at round 1
  - "hp_below_X": fires when mob HP% < X (fire once per threshold)
  - "round_N": fires on round N
  - "target_flees": fires when current target flees
  - "on_death": fires when mob reaches 0 HP
- Track fired triggers on mob.ndb.fired_sequence_triggers set.
- Return list of actions to execute, or None.

**Sequence actions:**
execute_sequence_action(action, mob, combat_handler) -> str:
- "echo": Return action["text"] for room display.
- "ability": Force mob to use specific ability (bypasses weight selection).
- "spawn": Call mob_spawner to add mobs to room mid-combat.
- "call_for_help": Find same-type mobs within N rooms via BFS, add to combat.
- "modify_behavior": Change mob.db.base_aggression mid-combat.
- "zone_echo": Send message to adjacent rooms.

**Main entry point:**
process_mob_turn(mob, combat_handler) -> list[str]:
- Check scripted sequences first (may override normal action).
- Get target via get_mob_target.
- Select action via select_mob_action.
- Return list of action dicts that CombatScript will resolve.
- Does NOT resolve damage directly — returns action instructions for CombatScript to dispatch.

**Flee behavior (flee_low_hp):**
- If mob has flee_low_hp behavior and HP below threshold, attempt flee instead of attack.
- Flee check: same as player flee (speed check against exits).

**Call for help (cap at 3 per encounter per Pitfall 2 from research):**
- combat_handler.ndb.call_for_help_count tracks limit.
  </action>
  <verify>
    <automated>python -c "from world.combat_ai import select_mob_action, get_mob_target, check_scripted_sequence, process_mob_turn, CONDITION_CHECKS; print('OK:', len(CONDITION_CHECKS), 'conditions')"</automated>
  </verify>
  <done>combat_ai.py selects mob abilities by weight with cooldown/condition filtering. Basic attack always available as fallback. Targeting follows last-attacker priority. Named mob scripted sequences fire at HP thresholds and round counts. Call-for-help capped at 3 per encounter.</done>
</task>

</tasks>

<verification>
- select_mob_action with all abilities on cooldown returns basic_attack
- select_mob_action respects condition checks (target_below_50hp only fires when target is low)
- get_mob_target returns last_attacker when available, random when not
- check_scripted_sequence fires hp_below_50 trigger once, not repeatedly
- process_mob_turn returns valid action list for CombatScript
</verification>

<success_criteria>
Mob abilities fire based on weight, cooldown, and condition vocabulary (CMB-03). Every mob always has a basic attack fallback (no infinite loops). Targeting follows vault spec. Named mob sequences provide dramatic combat moments at HP thresholds.
</success_criteria>

<output>
After completion, create `.planning/phases/06a-base-attributes-and-combat/06a-04-SUMMARY.md`
</output>
