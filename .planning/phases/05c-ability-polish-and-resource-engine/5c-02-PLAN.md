---
phase: 05c-ability-polish-and-resource-engine
plan: 02
type: execute
wave: 1
depends_on: []
files_modified:
  - world/ability_engine.py
  - world/combat_script.py
  - world/combat_engine.py
autonomous: true
requirements:
  - ABL-04
must_haves:
  truths:
    - "Focus combo points build on hit (1 point), reset on miss, cap at 5, spenders cost 1-5, consumes_all_focus scales damage"
    - "Balance pendulum shifts on ability use (0-100, 50 start), damage scales with Feral position, heals scale with Calm position"
    - "Resonance decays -10 per round during combat, builders generate resonance, spenders cost 60/80/100"
    - "Influence pool starts at f(Reputation), does not regenerate in combat"
    - "Momentum builds on hits landed and damage taken, decays between encounters"
    - "Mana persists across encounters, recovers partially at encounter end"
    - "Reagents and Components are finite stock that never regenerate"
    - "Command builds on ally actions, 50% solo rate, decays between encounters"
    - "Echoes build from abilities, investigation bonus persists 3 encounters"
  artifacts:
    - path: "world/ability_engine.py"
      provides: "10 resource handler functions + dispatch table + lifecycle hooks"
      contains: "RESOURCE_HANDLERS"
    - path: "world/combat_script.py"
      provides: "Per-round resource decay and encounter-end resource lifecycle"
      contains: "decay_resonance"
    - path: "world/combat_engine.py"
      provides: "Momentum build on basic attack hit and damage taken"
      contains: "build_momentum"
  key_links:
    - from: "world/ability_engine.py"
      to: "world/guild_engine.py"
      via: "FINGERPRINTS resource_type lookup"
      pattern: "FINGERPRINTS"
    - from: "world/ability_engine.py"
      to: "world/world_state.py"
      via: "get_dimension_score for Influence"
      pattern: "get_dimension_score"
    - from: "world/combat_script.py"
      to: "world/ability_engine.py"
      via: "decay_resonance + on_round_end_resources calls"
      pattern: "decay_resonance"
---

<objective>
Implement all 10 domain resource systems as type-aware handlers in ability_engine.py, with combat lifecycle integration.

Purpose: Per D-03 through D-13, each domain must have mechanically distinct resource behavior. The current generic pool system treats all domains identically. This plan makes Focus, Balance, Resonance, Influence, Momentum, Mana, Reagents, Command, Components, and Echoes all behave differently.
Output: Resource handler dispatch table in ability_engine.py, combat lifecycle hooks in combat_script.py and combat_engine.py
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/05c-ability-polish-and-resource-engine/5c-CONTEXT.md
@.planning/phases/05c-ability-polish-and-resource-engine/05C-RESEARCH.md

<interfaces>
<!-- From world/ability_engine.py — current resource API to extend -->
def get_domain_resource(character): ...  # Returns ndb.domain_resource dict or None
def build_domain_resource(character, amount): ...  # Adds to current, caps at max
def spend_domain_resource(character, amount): ...  # Returns (bool, str)
def initialize_domain_resource(character): ...  # Sets ndb.domain_resource from guild fingerprint
def _check_and_spend_resource(character, ability): ...  # Checks cost and spends

<!-- From world/guild_engine.py — resource types per domain -->
FINGERPRINTS = {
    "combat": {"resource_type": "momentum", ...},
    "subterfuge": {"resource_type": "focus", ...},
    "naturalism": {"resource_type": "balance", ...},
    "resonance": {"resource_type": "resonance", ...},
    "arcana": {"resource_type": "mana", ...},
    "diplomacy": {"resource_type": "influence", ...},
    "alchemy": {"resource_type": "reagents", ...},
    "tactics": {"resource_type": "command", ...},
    "engineering": {"resource_type": "components", ...},
    "remnance": {"resource_type": "echoes", ...},
}

<!-- From world/combat_script.py — lifecycle hooks -->
CombatScript.end_round()  # line 592 — ticks effects, decrements cooldowns
CombatScript.end_combat()  # line 700 — clears cooldowns, effects, combat state

<!-- From world/combat_engine.py — damage resolution -->
resolve_basic_attack(attacker, target, weapon=None)  # line 121, returns (bool, str, int)
resolve_ability_damage(character, ability, target)  # line 237, returns (ok, msg, dmg)
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Implement resource handler dispatch table and type-aware initialization</name>
  <files>world/ability_engine.py</files>
  <read_first>
    - world/ability_engine.py (full file -- understand existing resource functions, effect handlers, use_ability flow)
    - world/guild_engine.py (lines 1-130 -- FINGERPRINTS dict with resource_type per domain)
    - world/world_state.py (lines 1-80 -- get_dimension_score function signature and ALL_DIMENSIONS)
    - .planning/phases/05c-ability-polish-and-resource-engine/05C-RESEARCH.md (code examples for each handler)
  </read_first>
  <action>
Add 10 resource handler functions and a RESOURCE_HANDLERS dispatch table to ability_engine.py. Modify `_check_and_spend_resource` and `initialize_domain_resource` to be type-aware. Add post-ability resource hooks to `use_ability`.

**1. Add resource handler functions** (before EFFECT_HANDLERS dict, after the existing resource management section):

Each handler takes (character, ability) and returns (bool, str). They are called from `_check_and_spend_resource` instead of the generic `spend_domain_resource`.

```python
def _handle_momentum_spend(character, ability):
    """Momentum: traditional pool spend. Build happens elsewhere."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)

def _handle_focus_spend(character, ability):
    """Focus combo points: builders free, spenders cost 1-5, consumes_all needs >= 1."""
    params = ability.get("effect_params", {})
    if params.get("is_builder"):
        return True, ""  # Builders cost nothing; Focus added after hit
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    if params.get("consumes_all_focus"):
        res = character.ndb.domain_resource
        if not res or res["current"] < 1:
            return False, "No Focus points to spend."
        return True, ""  # Consumed in post-ability hook
    res = character.ndb.domain_resource
    if not res or res["current"] < cost:
        current = res["current"] if res else 0
        return False, f"Insufficient Focus ({current}/{cost} needed)."
    res = dict(res)
    res["current"] -= cost
    character.ndb.domain_resource = res
    return True, ""

def _handle_balance_spend(character, ability):
    """Balance pendulum: shift position, never spend. resource_cost always 0."""
    params = ability.get("effect_params", {})
    shift = params.get("balance_shift", 0)
    if shift == 0:
        return True, ""
    res = character.ndb.domain_resource
    if not res:
        return True, ""
    res = dict(res)
    res["current"] = max(0, min(100, res["current"] + shift))
    character.ndb.domain_resource = res
    return True, ""

def _handle_resonance_spend(character, ability):
    """Resonance: builders free (generate after), spenders cost from pool."""
    params = ability.get("effect_params", {})
    if params.get("resonance_generated"):
        return True, ""  # Builder; resonance added in post-ability hook
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)

def _handle_mana_spend(character, ability):
    """Mana: traditional pool spend. Persists across encounters."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)

def _handle_influence_spend(character, ability):
    """Influence: encounter-scoped pool, no regen. Standard spend."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)

def _handle_reagents_spend(character, ability):
    """Reagents: finite stock, standard spend. Running out is intentional."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)

def _handle_command_spend(character, ability):
    """Command: pool spend. Builds from ally actions."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)

def _handle_components_spend(character, ability):
    """Components: finite stock like reagents. Standard spend."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)

def _handle_echoes_spend(character, ability):
    """Echoes: pool spend. Builds from abilities and investigation bonus."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)
```

**2. Add dispatch table:**
```python
RESOURCE_HANDLERS = {
    "momentum": _handle_momentum_spend,
    "focus": _handle_focus_spend,
    "balance": _handle_balance_spend,
    "resonance": _handle_resonance_spend,
    "mana": _handle_mana_spend,
    "influence": _handle_influence_spend,
    "reagents": _handle_reagents_spend,
    "command": _handle_command_spend,
    "components": _handle_components_spend,
    "echoes": _handle_echoes_spend,
}
```

**3. Modify `_check_and_spend_resource`** to use dispatch:
```python
def _check_and_spend_resource(character, ability):
    res = character.ndb.domain_resource
    if not res:
        cost = ability.get("resource_cost", 0)
        if cost <= 0:
            return True, ""
        return False, "No domain resource available."
    handler = RESOURCE_HANDLERS.get(res["type"])
    if handler:
        return handler(character, ability)
    # Fallback to generic spend
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)
```

**4. Modify `initialize_domain_resource`** to be type-aware:
- Mana: start at max (persists across encounters, starts full)
- Focus: current=0, max=5
- Balance: current=50, max=100
- Influence: pool from Reputation via lazy import `from world.world_state import get_dimension_score`. Formula: `pool = int(20 + get_dimension_score(character, "reputation") * 0.5)`. Min pool 20.
- Momentum: current=0, max=100
- Resonance: current=0, max=100
- Command: current=0, max=100
- Echoes: current=0 + investigation_bonus (from `character.db.echoes_investigation_bonus` dict with `amount` key, default 0), max=100
- Reagents: current=character.db.reagent_stock or 50 (default starting stock), max=100
- Components: current=character.db.component_stock or 50 (default starting stock), max=100

Use resource_type from FINGERPRINTS to branch. Keep the existing generic path as fallback.

**5. Add post-ability resource hooks** in `use_ability`, after the effect handler returns successfully (after `result = handler(...)` line):

```python
# Post-ability resource hooks
_post_ability_resource_hook(character, ability, result)
```

Create `_post_ability_resource_hook(character, ability, result)`:
- Focus builder: if `effect_params.is_builder` and resource type is "focus", add 1 to current (cap at max 5). Only if ability succeeded (result is truthy string).
- Resonance builder: if `effect_params.resonance_generated` and resource type is "resonance", add `resonance_generated` amount to current (cap at max).
- consumes_all_focus: if `effect_params.consumes_all_focus` and resource type is "focus", set current to 0 (all Focus consumed).
- Momentum build: if resource type is "momentum", build 10 on successful ability use.
- Echoes build: if resource type is "echoes", build 5 on each ability use.
- Command build: if resource type is "command" and ability used successfully, build 5 (solo rate).

**6. Add Focus miss handler** (exported):
```python
def handle_focus_miss(character):
    """Reset Focus to 0 on miss. Called from combat_engine on ability miss."""
    res = character.ndb.domain_resource
    if res and res["type"] == "focus":
        res = dict(res)
        res["current"] = 0
        character.ndb.domain_resource = res
```

**7. Add Balance scaling helper** (exported):
```python
def get_balance_modifier(character, balance_type):
    """Return damage/heal modifier based on Balance pendulum position.
    position 0 (Feral) = 1.5x damage, position 100 (Calm) = 1.5x heal,
    position 50 = 1.0x both. Linear interpolation."""
    res = character.ndb.domain_resource
    if not res or res["type"] != "balance":
        return 1.0
    position = res["current"]
    if balance_type == "feral":
        return 1.0 + (50 - position) * 0.01
    elif balance_type == "calm":
        return 1.0 + (position - 50) * 0.01
    return 1.0
```

**8. Add decay/lifecycle functions** (exported):
```python
def decay_resonance(combatant):
    """Decay Resonance by 10 per round. Called from combat_script.end_round."""
    res = combatant.ndb.domain_resource
    if res and res["type"] == "resonance":
        res = dict(res)
        res["current"] = max(0, res["current"] - 10)
        combatant.ndb.domain_resource = res

def on_round_end_resources(combatant, combat_handler):
    """Per-round resource hooks. Called from combat_script.end_round for each combatant."""
    res = combatant.ndb.domain_resource
    if not res:
        return
    rtype = res["type"]
    if rtype == "resonance":
        decay_resonance(combatant)
    elif rtype == "focus":
        # Check if subterfuge character skipped their turn this round
        if not getattr(combatant.ndb, "ability_used_this_turn", False):
            res = dict(res)
            res["current"] = 0
            combatant.ndb.domain_resource = res
    elif rtype == "command":
        # Build Command from ally actions (group combat)
        _build_command_from_allies(combatant, combat_handler)

def _build_command_from_allies(combatant, combat_handler):
    """Build Command resource based on ally actions this round."""
    res = combatant.ndb.domain_resource
    if not res or res["type"] != "command":
        return
    # Count allies who acted this round
    ally_action_count = getattr(combat_handler.ndb, "ally_action_count", {})
    my_allies = ally_action_count.get(str(combatant.id), 0)
    if my_allies > 0:
        amount = my_allies * 10  # 10 Command per ally action
    else:
        amount = 5  # Solo rate: 50% of 10
    res = dict(res)
    res["current"] = min(res["max"], res["current"] + amount)
    combatant.ndb.domain_resource = res

def on_encounter_end_resources(combatant):
    """Encounter-end resource lifecycle. Called from combat_script.end_combat."""
    res = combatant.ndb.domain_resource
    if not res:
        return
    rtype = res["type"]
    if rtype == "mana":
        # Mana recovers 15% at encounter end, persists
        res = dict(res)
        recovery = int(res["max"] * 0.15)
        res["current"] = min(res["max"], res["current"] + recovery)
        combatant.ndb.domain_resource = res
    elif rtype in ("focus", "influence", "command"):
        # Reset encounter-scoped resources
        res = dict(res)
        res["current"] = 0
        combatant.ndb.domain_resource = res
    elif rtype == "momentum":
        # Momentum decays between encounters
        res = dict(res)
        res["current"] = 0
        combatant.ndb.domain_resource = res
    elif rtype == "echoes":
        # Decrement investigation bonus persistence
        bonus = combatant.db.echoes_investigation_bonus
        if bonus and bonus.get("encounters_remaining", 0) > 0:
            bonus = dict(bonus)
            bonus["encounters_remaining"] -= 1
            if bonus["encounters_remaining"] <= 0:
                bonus["amount"] = 0
            combatant.db.echoes_investigation_bonus = bonus
    # resonance: no decay between encounters (persists)
    # reagents/components: persist as-is (finite stock, no regen)

def build_momentum_on_damage(character, amount=10):
    """Build Momentum when character lands a hit or takes damage.
    Called from combat_engine. Only applies if resource type is momentum."""
    res = character.ndb.domain_resource
    if res and res["type"] == "momentum":
        res = dict(res)
        res["current"] = min(res["max"], res["current"] + amount)
        character.ndb.domain_resource = res
```

**9. Update exports** in module docstring to include new functions:
`decay_resonance, on_round_end_resources, on_encounter_end_resources,
handle_focus_miss, get_balance_modifier, build_momentum_on_damage, RESOURCE_HANDLERS`
  </action>
  <verify>
    <automated>python -c "from world.ability_engine import RESOURCE_HANDLERS, decay_resonance, on_round_end_resources, on_encounter_end_resources, handle_focus_miss, get_balance_modifier, build_momentum_on_damage; print(f'Handlers: {len(RESOURCE_HANDLERS)}'); assert len(RESOURCE_HANDLERS) == 10, 'Expected 10 handlers'"</automated>
  </verify>
  <acceptance_criteria>
    - world/ability_engine.py contains `RESOURCE_HANDLERS` dict with exactly 10 entries (momentum, focus, balance, resonance, mana, influence, reagents, command, components, echoes)
    - world/ability_engine.py contains `_handle_focus_spend` function with `is_builder` and `consumes_all_focus` checks
    - world/ability_engine.py contains `_handle_balance_spend` function with `max(0, min(100,` clamping
    - world/ability_engine.py contains `_handle_resonance_spend` function with `resonance_generated` check
    - world/ability_engine.py contains `handle_focus_miss` function that resets current to 0
    - world/ability_engine.py contains `get_balance_modifier` function returning float
    - world/ability_engine.py contains `decay_resonance` function decrementing by 10
    - world/ability_engine.py contains `on_round_end_resources` function
    - world/ability_engine.py contains `on_encounter_end_resources` function
    - world/ability_engine.py contains `build_momentum_on_damage` function
    - `_check_and_spend_resource` uses `RESOURCE_HANDLERS.get(res["type"])` dispatch
    - `initialize_domain_resource` has type-aware branches for focus (max=5), balance (current=50, max=100), mana (start at max), influence (from Reputation)
    - `_post_ability_resource_hook` exists and is called from `use_ability` after effect handler
    - All existing imports and function signatures preserved (no breaking changes to existing callers)
  </acceptance_criteria>
  <done>10 resource handlers implemented with dispatch table. Type-aware initialization for all domains. Post-ability hooks for Focus/Resonance/Momentum/Echoes/Command builders. Decay, miss, and scaling helper functions exported.</done>
</task>

<task type="auto">
  <name>Task 2: Wire resource lifecycle hooks into combat_script and combat_engine</name>
  <files>world/combat_script.py, world/combat_engine.py</files>
  <read_first>
    - world/combat_script.py (full file -- understand end_round at line 592, end_combat at line 700, process_player_action flow)
    - world/combat_engine.py (full file -- understand resolve_basic_attack at line 121, resolve_ability_damage at line 237)
    - world/ability_engine.py (after Task 1 changes -- verify new exports exist)
  </read_first>
  <action>
Wire the new resource lifecycle functions from ability_engine.py into the combat lifecycle.

**1. In combat_script.py `end_round()` (after line 610 `decrement_cooldowns(combatant)`):**

Add import at top of function:
```python
from world.ability_engine import on_round_end_resources
```

After the `decrement_cooldowns(combatant)` call, add:
```python
on_round_end_resources(combatant, self)
```

This ensures Resonance decays, Focus resets on skipped turns, and Command builds from ally actions every round.

**2. In combat_script.py `end_combat()` (inside the for-loop at line 710, after `clear_all_effects(combatant)`):**

Add import at top of function:
```python
from world.ability_engine import on_encounter_end_resources
```

For player combatants (inside the `if _is_player(combatant):` block), add after `clear_all_effects`:
```python
on_encounter_end_resources(combatant)
```

This handles Mana recovery, Focus/Influence/Command/Momentum resets, and Echoes investigation bonus decrement.

**3. In combat_script.py `process_player_action()` — track ally actions for Command:**

At the end of the `action_type == "ability"` branch and `action_type == "basic_attack"` branch, after the action resolves successfully, add tracking:
```python
# Track for Command resource ally-action build
ally_counts = dict(getattr(self.ndb, "ally_action_count", None) or {})
for cid in (self.db.combatant_ids or []):
    if cid != character.id:
        key = str(cid)
        ally_counts[key] = ally_counts.get(key, 0) + 1
self.ndb.ally_action_count = ally_counts
```

At the start of `end_round()`, reset the ally action counter:
```python
self.ndb.ally_action_count = {}
```

**4. In combat_engine.py `resolve_basic_attack()` — Momentum build on hit:**

At the end of the function, after damage is applied and before the return statement, add:
```python
from world.ability_engine import build_momentum_on_damage
# Build Momentum for attacker on hit (D-04)
build_momentum_on_damage(attacker, 10)
```

**5. In combat_engine.py — Momentum build on damage taken:**

In the damage application section (where target HP is reduced), add:
```python
# Build Momentum for target on damage taken (D-04)
from world.ability_engine import build_momentum_on_damage
build_momentum_on_damage(target, 5)
```

This goes in both `resolve_basic_attack` (for the target) and `resolve_ability_damage` (for the target). Only add the target build in `resolve_basic_attack` since ability damage will also trigger it through `resolve_ability_damage`.

**6. In combat_engine.py `resolve_ability_damage()` — Focus miss handling:**

After the miss check (where miss_chance is evaluated and returns early), add:
```python
from world.ability_engine import handle_focus_miss
handle_focus_miss(attacker)
```

This ensures Focus resets to 0 on a missed ability.

**7. In combat_engine.py `resolve_ability_damage()` — Balance scaling:**

Before the final damage calculation, check if the ability has `balance_type` in effect_params:
```python
from world.ability_engine import get_balance_modifier
params = ability.get("effect_params", {})
balance_type = params.get("balance_type")
if balance_type:
    balance_mod = get_balance_modifier(attacker, balance_type)
    raw = int(raw * balance_mod)
```

Similarly in `resolve_heal()`, check for balance_type "calm" and apply the modifier.
  </action>
  <verify>
    <automated>python -c "import ast; src=open('world/combat_script.py').read(); tree=ast.parse(src); print('on_round_end_resources' in src and 'on_encounter_end_resources' in src and 'ally_action_count' in src)"</automated>
  </verify>
  <acceptance_criteria>
    - world/combat_script.py `end_round` method contains `on_round_end_resources(combatant, self)` call
    - world/combat_script.py `end_combat` method contains `on_encounter_end_resources(combatant)` call
    - world/combat_script.py `process_player_action` method contains `ally_action_count` tracking
    - world/combat_script.py `end_round` starts with `self.ndb.ally_action_count = {}`
    - world/combat_engine.py `resolve_basic_attack` contains `build_momentum_on_damage(attacker, 10)` call
    - world/combat_engine.py `resolve_basic_attack` contains `build_momentum_on_damage(target, 5)` call
    - world/combat_engine.py `resolve_ability_damage` contains `handle_focus_miss` call after miss check
    - world/combat_engine.py `resolve_ability_damage` contains `get_balance_modifier` call with balance_type check
    - No existing tests break (all imports resolve, no removed functions)
  </acceptance_criteria>
  <done>Combat lifecycle hooks wired: Resonance decays per-round, Focus resets on skip/miss, Command builds from ally actions, Momentum builds on hits/damage, Balance scales damage/heals, Mana recovers at encounter end.</done>
</task>

</tasks>

<verification>
- `python -c "from world.ability_engine import RESOURCE_HANDLERS; print(len(RESOURCE_HANDLERS))"` prints 10
- `python -c "from world.combat_script import CombatScript"` imports without error
- `python -c "from world.combat_engine import resolve_basic_attack"` imports without error
- `python -m pytest tests/test_ability_engine.py -x` passes (existing tests)
</verification>

<success_criteria>
- All 10 resource types have handler functions and dispatch correctly
- Combat lifecycle hooks call resource functions at correct points
- Existing test suite passes without regressions
- No circular imports introduced
</success_criteria>

<output>
After completion, create `.planning/phases/05c-ability-polish-and-resource-engine/5c-02-SUMMARY.md`
</output>
