---
phase: 06b-spawn-system-skills-and-mob-ai
plan: 04
type: execute
wave: 1
depends_on: []
files_modified:
  - world/combat_ai.py
  - world/combat_script.py
autonomous: true
requirements: [CMB-04]

must_haves:
  truths:
    - "Mob abilities with cast_time > 0 telegraph at cast start and resolve N rounds later"
    - "Stun or Root during cast window interrupts (cancels) the pending cast"
    - "Missing condition keys from D-13 added: target_rooted, target_blinded, no_target_dot"
    - "is_hunter mobs chase fleeing players via BFS within detection range"
  artifacts:
    - path: "world/combat_ai.py"
      provides: "Casting time state management, missing conditions, is_hunter chase"
      contains: "target_rooted"
    - path: "world/combat_script.py"
      provides: "Pending cast resolution at round start, interrupt check"
  key_links:
    - from: "world/combat_ai.py"
      to: "world/combat_script.py"
      via: "process_mob_turn returns cast_start action; CombatScript processes pending_mob_casts at round start"
      pattern: "pending_mob_casts"
    - from: "world/combat_ai.py"
      to: "world/status_effects.py"
      via: "has_effect() checks for stun/root interrupt and target_rooted/target_blinded conditions"
      pattern: "has_effect"
---

<objective>
Extend mob combat AI with casting time mechanics, missing condition vocabulary, and is_hunter chase behavior.

Purpose: The combat_ai.py from Phase 6a has the core weight-based ability selection and scripted sequences. This plan adds the remaining mob AI features from the vault spec: casting time (D-11), the three missing condition checks from D-13, and is_hunter pathfinding chase (D-15). These make mob encounters more tactical -- players can interrupt telegraphed spells and must be wary of hunter mobs that pursue across rooms.

Output: Extended combat_ai.py, extended combat_script.py with cast resolution.
</objective>

<execution_context>
@C:\Users\colek\.claude\get-shit-done\workflows\execute-plan.md
@C:\Users\colek\.claude\get-shit-done\templates\summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md

@C:\Obsidian\brain\Soravelon\soravelon-mobs.md

@world/combat_ai.py
@world/combat_script.py
</context>

<interfaces>
<!-- Existing combat_ai.py interface -->
From world/combat_ai.py:
```python
CONDITION_CHECKS = {
    "target_below_50hp": ..., "target_below_25hp": ...,
    "self_below_50hp": ..., "self_below_25hp": ...,
    "target_has_poison": ..., "target_has_bleed": ..., "target_has_burn": ...,
    "no_allies_alive": ..., "allies_present": ...,
}
def check_condition(condition_str, mob, target, combat_handler): ...
def select_mob_action(mob, target, combat_handler): ...
def process_mob_turn(mob, combat_handler): ...
```

From world/combat_script.py:
```python
class CombatScript:
    # ndb.pending_charged = {}  # existing player charged ability tracking
    # Need to add: ndb.pending_mob_casts = {}
```

From world/status_effects.py:
```python
def has_effect(target, effect_type) -> bool: ...
```
</interfaces>

<tasks>

<task type="auto">
  <name>Task 1: Missing conditions + casting time in combat_ai.py</name>
  <files>world/combat_ai.py</files>
  <action>
**Step 1: Add missing condition keys to CONDITION_CHECKS** per D-13 gap analysis:

Add these entries to CONDITION_CHECKS dict:
```python
"pack_present": lambda mob, target, ch: len(_get_mob_combatants(ch, exclude=mob)) > 0,
# (Same logic as allies_present but with vault-spec key name)

"hp_below_50": lambda mob, target, ch: (
    getattr(mob.ndb, "hp", 0) < (mob.db.hp_max or 1) * 0.5
),
"hp_below_25": lambda mob, target, ch: (
    getattr(mob.ndb, "hp", 0) < (mob.db.hp_max or 1) * 0.25
),
# (Aliases for self_below_50hp/self_below_25hp with vault-spec key names)

"target_rooted": lambda mob, target, ch: (
    target is not None and _target_has_effect(target, "root")
),
"target_blinded": lambda mob, target, ch: (
    target is not None and _target_has_effect(target, "blind")
),
"no_target_dot": lambda mob, target, ch: (
    target is not None
    and not _target_has_effect(target, "poison")
    and not _target_has_effect(target, "bleed")
    and not _target_has_effect(target, "burn")
),
```

Keep existing keys as aliases for backward compatibility.

**Step 2: Modify select_mob_action() for casting time** per D-11:

When the selected ability has `cast_time > 0`:
- Instead of returning the ability action directly, return a `"cast_start"` action:
```python
if selected.get("cast_time", 0) > 0:
    return {
        "type": "cast_start",
        "ability": selected,
        "target_id": None,  # target_id set by process_mob_turn after targeting
        "cast_time": selected["cast_time"],
        "emote": selected.get("emote", ""),
    }
```
- The emote fires immediately (telegraph to players)
- CombatScript will track the pending cast and resolve it N rounds later

**Step 3: Add `start_mob_cast()` helper:**

```python
def start_mob_cast(mob, ability, target, combat_handler):
    """Register a pending mob cast on the combat handler."""
    pending = dict(combat_handler.ndb.pending_mob_casts or {})
    pending[mob.id] = {
        "ability": ability,
        "target_id": target.id,
        "rounds_left": ability.get("cast_time", 1),
    }
    combat_handler.ndb.pending_mob_casts = pending
```

**Step 4: Add `resolve_pending_casts()` for CombatScript to call at round start:**

```python
def resolve_pending_casts(combat_handler):
    """
    Decrement cast timers and resolve any that complete.
    Called at the START of each round by CombatScript.
    Returns list of action dicts for completed casts.

    Per D-11/Pitfall 6: Check for stun/root INTERRUPT at resolution time.
    If mob has stun or root when cast resolves, cancel the cast.
    """
    pending = dict(combat_handler.ndb.pending_mob_casts or {})
    resolved_actions = []
    still_pending = {}

    for mob_id, cast_info in pending.items():
        cast_info["rounds_left"] -= 1
        if cast_info["rounds_left"] <= 0:
            # Cast completes -- check for interrupt
            mob = _resolve_combatant(mob_id, combat_handler)
            if mob is None:
                continue  # mob died during cast
            from world.status_effects import has_effect
            if has_effect(mob, "stun") or has_effect(mob, "root"):
                # Interrupted!
                if mob.location:
                    mob.location.msg_contents(
                        f"|y{mob.key}'s spell is interrupted!|n"
                    )
                continue  # cast cancelled, not added to resolved
            # Cast resolves
            ability = cast_info["ability"]
            resolved_actions.append({
                "type": "ability",
                "ability_id": ability.get("ability_id"),
                "element": ability.get("element", "physical"),
                "damage_base": ability.get("damage_base", 0),
                "status_effect": ability.get("status_effect"),
                "effect_duration": ability.get("effect_duration", 0),
                "effect_magnitude": ability.get("effect_magnitude", 0),
                "application_chance": ability.get("application_chance", 1.0),
                "cooldown": ability.get("cooldown", 0),
                "target_id": cast_info["target_id"],
                "mob_id": mob_id,
                "from_cast": True,
            })
        else:
            still_pending[mob_id] = cast_info

    combat_handler.ndb.pending_mob_casts = still_pending
    return resolved_actions
```

Add `_resolve_combatant(mob_id, combat_handler)` helper that finds the mob object from combat handler's combatant lists.

**Step 5: Add is_hunter chase behavior** per D-15:

```python
DEFAULT_HUNTER_DETECTION_RANGE = 3

def attempt_hunter_chase(mob, target, room):
    """
    is_hunter mob chases a fleeing player via BFS pathfinding.
    Returns True if mob moved toward target, False otherwise.
    Only called when mob has is_hunter flag and target fled.

    Uses patrol_engine.find_path() for BFS -- same pathfinding
    already tested and proven. Capped at mob.db.detection_range
    or DEFAULT_HUNTER_DETECTION_RANGE.
    """
    if not (mob.db.is_hunter or False):
        return False
    detection_range = mob.db.detection_range or DEFAULT_HUNTER_DETECTION_RANGE
    from world.patrol_engine import find_path
    path = find_path(mob.location, target.location, max_depth=detection_range)
    if not path or len(path) < 2:
        return False
    # Move mob to next room in path
    next_room = path[1]
    mob.move_to(next_room, quiet=True)
    if mob.location == target.location:
        # Arrived -- initiate combat
        mob.location.msg_contents(
            f"|r{mob.key} has tracked you down!|n"
        )
    return True
```

Add `mob.db.is_hunter = False` and `mob.db.detection_range = None` to SoravelonMob.at_object_creation() -- but do NOT modify mobs.py in this plan (that file is owned by Plan 01). Instead, the is_hunter flag is set by spawn definitions at spawn time via mob.db, and combat_ai checks it defensively with `mob.db.is_hunter or False`.

Update `process_mob_turn()` to integrate casting time: when select_mob_action returns `"cast_start"`, call `start_mob_cast()` and return the echo action (telegraph).
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "from world.combat_ai import CONDITION_CHECKS, resolve_pending_casts, start_mob_cast, attempt_hunter_chase, DEFAULT_HUNTER_DETECTION_RANGE; assert 'target_rooted' in CONDITION_CHECKS; assert 'target_blinded' in CONDITION_CHECKS; assert 'no_target_dot' in CONDITION_CHECKS; assert 'pack_present' in CONDITION_CHECKS; assert callable(resolve_pending_casts); assert callable(attempt_hunter_chase); print('OK')"</automated>
  </verify>
  <done>CONDITION_CHECKS has all D-13 conditions including target_rooted, target_blinded, no_target_dot, pack_present, hp_below_50, hp_below_25. Casting time returns cast_start action with telegraph emote, tracked via start_mob_cast(), resolved by resolve_pending_casts() with stun/root interrupt check. is_hunter uses BFS pathfinding within detection range to chase fleeing players.</done>
</task>

<task type="auto">
  <name>Task 2: CombatScript cast resolution integration</name>
  <files>world/combat_script.py</files>
  <action>
Extend CombatScript to handle casting time resolution and cast_start actions from combat_ai.

**Step 1: Add ndb.pending_mob_casts** initialization:

In `at_script_creation()`, add:
```python
self.ndb.pending_mob_casts = {}
```

In `at_start()` (server reload rebuild), add:
```python
if self.ndb.pending_mob_casts is None:
    self.ndb.pending_mob_casts = {}
```

**Step 2: Add cast resolution at round start:**

Find the round progression logic (where round_number increments or round processing begins). At the START of each new round, before processing individual turns, add:

```python
# Resolve any pending mob casts
from world.combat_ai import resolve_pending_casts
resolved = resolve_pending_casts(self)
for cast_action in resolved:
    # Dispatch the resolved cast through normal ability processing
    # Find the mob and target, apply damage/effects via combat_engine
    self._dispatch_resolved_cast(cast_action)
```

Add `_dispatch_resolved_cast(self, cast_action)` method:
- Resolve mob from cast_action["mob_id"]
- Resolve target from cast_action["target_id"]
- If either is dead/gone, skip
- Dispatch through the same ability resolution path as normal ability actions (call combat_engine.resolve_ability or whatever the existing combat resolution function is)
- Apply cooldown for the ability

**Step 3: Handle cast_start actions from process_mob_turn:**

In the section where CombatScript processes mob turn results (iterating action dicts from process_mob_turn), add handling for `"cast_start"` type:

```python
if action["type"] == "cast_start":
    # Telegraph emote fires immediately
    room.msg_contents(action.get("emote", ""))
    # Casting state already registered by process_mob_turn via start_mob_cast
```

The cast will resolve on a future round via resolve_pending_casts.

**Step 4: Clear pending casts on combat end:**

In the combat cleanup/end logic, add:
```python
self.ndb.pending_mob_casts = {}
```

Also clear pending casts for a specific mob when that mob dies mid-cast:
```python
# In mob death handling within CombatScript
pending = dict(self.ndb.pending_mob_casts or {})
if dead_mob.id in pending:
    del pending[dead_mob.id]
    self.ndb.pending_mob_casts = pending
```
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "src = open('world/combat_script.py').read(); assert 'pending_mob_casts' in src, 'CombatScript missing pending_mob_casts'; assert 'resolve_pending_casts' in src, 'CombatScript missing resolve call'; print('OK')"</automated>
  </verify>
  <done>CombatScript initializes pending_mob_casts in at_script_creation and at_start. Pending casts resolve at round start via resolve_pending_casts(). cast_start actions display telegraph emote immediately. Pending casts cleared on combat end and mob death.</done>
</task>

</tasks>

<verification>
- CONDITION_CHECKS has all 6 new keys from D-13 plus existing keys preserved
- Ability with cast_time=2 returns cast_start on selection, resolves 2 rounds later
- Stunned mob's pending cast is cancelled (not resolved)
- is_hunter mob with detection_range=3 chases via BFS up to 3 rooms
- CombatScript handles cast_start action type and resolves pending casts at round start
</verification>

<success_criteria>
Mob abilities with casting time telegraph to players and resolve after the delay, with interrupt possible via Stun or Root. All vault-spec condition vocabulary keys work in combat_ai. is_hunter mobs chase fleeing players across rooms using existing BFS pathfinding. CombatScript correctly tracks and resolves pending mob casts.
</success_criteria>

<output>
After completion, create `.planning/phases/06b-spawn-system-skills-and-mob-ai/06b-04-SUMMARY.md`
</output>
