---
phase: 06a-base-attributes-and-combat
plan: 05
type: execute
wave: 3
depends_on: ["06a-03", "06a-04"]
files_modified:
  - world/combat_script.py
autonomous: true
requirements:
  - CMB-01
  - CMB-04
must_haves:
  truths:
    - "CombatScript attaches to room and manages all combatants in initiative order"
    - "Individual initiative: player and mob turns interleave per D-15"
    - "Round end ticks status effects, decrements cooldowns per D-11"
    - "Solo combat waits indefinitely; group combat has configurable timeout per D-18"
    - "Combat ends cleanly when all enemies die, all players flee, or all disconnect"
    - "Mid-combat join inserts new combatant at correct initiative position"
    - "Charged abilities declare on turn, auto-attack during charge, fire when charge completes per D-10"
  artifacts:
    - path: "world/combat_script.py"
      provides: "CombatScript room-attached state machine"
      exports: ["CombatScript", "start_combat", "join_combat"]
  key_links:
    - from: "world/combat_script.py"
      to: "world/combat_engine.py"
      via: "Resolves damage for player and mob actions"
      pattern: "combat_engine\\.resolve"
    - from: "world/combat_script.py"
      to: "world/combat_ai.py"
      via: "Delegates mob turns to process_mob_turn"
      pattern: "combat_ai\\.process_mob_turn"
    - from: "world/combat_script.py"
      to: "world/status_effects.py"
      via: "tick_effects at round end, clear_all_effects at combat end"
      pattern: "status_effects\\."
    - from: "world/combat_script.py"
      to: "world/ability_engine.py"
      via: "decrement_cooldowns, clear_encounter_cooldowns"
      pattern: "ability_engine\\."
---

<objective>
Build CombatScript -- the room-attached Evennia Script that manages all combat state, drives initiative order, processes turns, and handles round progression.

Purpose: CombatScript is the orchestrator that ties together damage resolution, mob AI, status effects, and player input into a coherent turn-based combat flow. This is the central piece that makes combat playable.
Output: world/combat_script.py with CombatScript class and start_combat/join_combat module-level functions.
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

@.planning/phases/06a-base-attributes-and-combat/06a-01-SUMMARY.md
@.planning/phases/06a-base-attributes-and-combat/06a-02-SUMMARY.md
@.planning/phases/06a-base-attributes-and-combat/06a-03-SUMMARY.md
@.planning/phases/06a-base-attributes-and-combat/06a-04-SUMMARY.md

@typeclasses/scripts.py
@world/oob_publisher.py

<interfaces>
<!-- From Plan 01: world/base_attributes.py -->
```python
def get_initiative(combatant) -> int: ...
def get_actions_per_turn(character) -> int: ...
def get_damage_modifier(actions_per_turn) -> float: ...
def record_stat_use(character, action_type, amount=1): ...
```

<!-- From Plan 02: world/status_effects.py -->
```python
def tick_effects(target) -> list[str]: ...
def clear_all_effects(target): ...
def get_effect_modifiers(target) -> dict: ...  # {skip_turn, action_budget_penalty, ...}
```

<!-- From Plan 03: world/combat_engine.py -->
```python
def resolve_basic_attack(attacker, target, weapon=None) -> (bool, str, int): ...
def resolve_ability_damage(character, ability, target) -> (bool, str, int): ...
def check_death(combatant) -> bool: ...
def handle_mob_death(mob, killer) -> str: ...
def handle_player_death(character) -> str: ...
```

<!-- From Plan 04: world/combat_ai.py -->
```python
def process_mob_turn(mob, combat_handler) -> list[str]: ...
def get_mob_target(mob, combat_handler) -> target|None: ...
```

<!-- From existing: world/ability_engine.py -->
```python
def decrement_cooldowns(character): ...
def clear_encounter_cooldowns(character): ...
def use_ability(character, ability_id, target=None) -> (bool, str): ...
```

<!-- From existing: typeclasses/scripts.py -->
```python
class SoravelonScript(DefaultScript):
    # Base script typeclass
```
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create world/combat_script.py with CombatScript lifecycle, state, and combatant management</name>
  <files>world/combat_script.py</files>
  <action>
Create world/combat_script.py implementing CombatScript lifecycle and state per D-07, D-12, D-15.

**CombatScript class (extends SoravelonScript):**

```python
class CombatScript(SoravelonScript):
    """Room-attached combat manager. One per active encounter."""
```

**db attributes (persistent across reload):**
- combatant_ids: list[int] -- character/mob dbrefs in initiative order
- round_number: int (starts at 1)
- current_turn_index: int -- index into combatant_ids
- initiative_order: list[dict] -- [{id, initiative_value}] sorted desc
- is_group_combat: bool -- True if any player is in a group
- round_timeout: int -- seconds, default 30, only used if is_group_combat
- active_effects_db: dict -- {combatant_id: [effect_list]} for reload survival (Pitfall 1)

**ndb attributes (volatile, rebuilt at_start):**
- turn_timer_id: int|None -- delay() handle for timeout cancel
- pending_charged: dict -- {char_id: {ability_id, rounds_left, target_id}}
- call_for_help_count: int -- capped at 3

**Lifecycle methods:**

at_script_creation():
- Set interval=0 (NOT self-ticking, event-driven per research).
- Set persistent=True (survive reload).
- self.key = "combat_script"

at_start():
- Called on creation AND on server reload.
- Rebuild ndb state from db.
- Restore active_effects from db to each combatant's ndb.
- Re-add CombatCmdSet to all player combatants still connected.
- If current turn is a mob, auto-process. If player, re-prompt.

**Module-level functions:**

start_combat(room, initiator, targets) -> CombatScript:
- Check if room already has a CombatScript (if so, join existing).
- Create CombatScript on room.
- Compute initiative for all combatants via get_initiative().
- Sort by initiative descending (ties broken randomly).
- Store combatant_ids, initiative_order on db.
- Add CombatCmdSet to all player combatants.
- Set combatant ndb: combat_handler = script, combat_target_id, actions_remaining, etc.
- Check is_group_combat (any player in a group).
- Begin first turn.

join_combat(combat_script, newcomer) -> (bool, str):
- Compute initiative for newcomer.
- Insert into initiative_order at correct position.
- Update combatant_ids.
- If player, add CombatCmdSet.
- Set ndb references.

**Combatant management:**

add_combatant(self, combatant):
- Internal method called by join_combat and start_combat.
- Compute initiative, insert into sorted order.

remove_combatant(self, combatant):
- Remove from combatant_ids and initiative_order.
- Clean up ndb references.
- If was current turn, advance to next.
- If no enemies remain, end combat.

**Helper methods:**

get_player_combatants(self) -> list: Return list of player characters in combat.
get_mob_combatants(self) -> list: Return list of mobs in combat.
get_current_combatant(self) -> obj: Return the combatant whose turn it is.
is_combatant(self, obj) -> bool: Check if obj is in this combat.

**Combat end:**

end_combat(self):
- For each player combatant:
  - Remove CombatCmdSet.
  - clear_encounter_cooldowns.
  - clear_all_effects.
  - Reset ndb combat state (combat_handler = None, etc.).
  - Clear pending_charged entries.
- For each mob combatant:
  - Reset ndb combat state.
  - Clear cooldowns.
- Cancel any active timers.
- self.delete() -- remove script from room.

**Auto-engage wiring (D-13):**
- NOT in CombatScript itself. This is handled by room enter hooks (Character.at_after_move or mob patrol arrival).
- When a player enters a room with aggressive mobs: check disposition, if aggressive, call start_combat.
- is_hunter BFS aggro is deferred to Phase 6b (requires patrol tick integration and BFS pathfinding across multiple rooms; Plan 04 combat_ai.py focuses on in-combat mob behavior only).
  </action>
  <verify>
    <automated>python -c "from world.combat_script import CombatScript, start_combat, join_combat; print('CombatScript:', CombatScript.__mro__[1].__name__); assert hasattr(CombatScript, 'at_script_creation'); assert hasattr(CombatScript, 'end_combat')"</automated>
  </verify>
  <done>CombatScript class with full lifecycle (at_script_creation, at_start), combatant management (add/remove/join), and clean end-of-combat teardown. Module-level start_combat and join_combat functions. State persists across server reload via db attributes.</done>
</task>

<task type="auto">
  <name>Task 2: Implement turn processing, round management, and charged ability lifecycle</name>
  <files>world/combat_script.py</files>
  <action>
Add turn processing and round management methods to CombatScript per D-07, D-09, D-10, D-11, D-15, D-18.

**Turn management:**

advance_turn(self):
- Increment current_turn_index (wrap around at end of list).
- If wrapping: call end_round() first.
- Get current combatant from combatant_ids[current_turn_index].
- If combatant is dead or gone (check .pk for mobs, .account for players): skip to next.
- Check get_effect_modifiers for skip_turn (stun/charm): skip turn with message.
- If mob: call _process_mob_turn().
- If player: call _prompt_player_turn().

_prompt_player_turn(self, character):
- Compute actions_remaining from get_actions_per_turn minus effect penalties.
- Set character.ndb.actions_remaining.
- Set character.ndb.ability_used_this_turn = False.
- Check pending_charged: if character has a pending charge, decrement rounds_left.
  If rounds_left == 0: auto-fire the charged ability via use_ability, then clear from pending_charged.
  Character still gets remaining actions (auto-attack during charge per D-10).
- Build turn prompt: show available abilities (from character's loadout, filter cooldowns), show target.
- Push combat_update via oob_publisher (per research OOB schema).
- character.msg() with formatted turn prompt per D-16 (list abilities ready and on cooldown).
- If is_group_combat: start round timer via delay(round_timeout, _auto_attack_timeout, character.id).

_process_mob_turn(self, mob):
- Call combat_ai.process_mob_turn(mob, self).
- For each action returned: resolve via combat_engine (basic attack or ability).
- Check death after each action.
- Advance turn when mob actions complete.

**Player action processing:**

process_player_action(self, character, action_type, target=None, ability_id=None):
- Called by combat commands (CmdAttack, CmdUseAbility, etc.).
- Validate it's this character's turn.
- Cancel round timer if active.
- Execute action:
  - "basic_attack": resolve_basic_attack. Decrement actions_remaining. Record stat use.
  - "ability": use_ability via ability_engine. Set ability_used_this_turn = True per D-09.
  - "charge": Declare a charged ability (per D-10). Validate ability has charge_turns > 0.
    Store in ndb.pending_charged: {character.id: {"ability_id": ability_id, "rounds_left": ability["charge_turns"], "target_id": target.id if target else None}}.
    Character continues with remaining basic attacks this turn (auto-attack during charge).
    Message: "You begin channeling {ability_name}... ({rounds_left} rounds)".
    On subsequent turns, _prompt_player_turn decrements and fires when ready.
    Domain resource still generates normally during charge turns per D-10.
  - "flee": attempt flee (D-28). If rooted/stunned, fail. Speed check + skill check. On success, move to random adjacent exit, remove from combat.
  - "pass": end turn early.
- Check death of target after each action.
- If actions_remaining > 0 and not ability (abilities don't consume all actions): wait for next action.
- If actions_remaining == 0: advance_turn.

_auto_attack_timeout(self, character_id):
- Called when group combat round timer expires per D-18.
- Resolve one basic_attack on character's current target (auto-attack on timeout).
- advance_turn.

**Round management:**

end_round(self):
- For each combatant in initiative order:
  - tick_effects(combatant) -- DoTs deal damage, durations decrease.
  - decrement_cooldowns(combatant) -- ability cooldowns go down.
  - Check death (DoT kills).
- Persist active_effects to db (active_effects_db) for reload survival per Pitfall 1.
- Increment round_number.
- Check if combat should end (no enemies, no players).
  </action>
  <verify>
    <automated>python -c "from world.combat_script import CombatScript; cs = CombatScript.__new__(CombatScript); assert hasattr(cs, 'advance_turn'); assert hasattr(cs, 'process_player_action'); assert hasattr(cs, 'end_round'); print('Turn methods present')"</automated>
  </verify>
  <done>CombatScript manages turn-based combat with initiative-ordered interleaved turns per D-15. process_player_action handles basic_attack, ability, charge, flee, and pass action types. Charged abilities (D-10) declare on turn, store in pending_charged, auto-fire when charge completes, character auto-attacks during charge. Round end ticks effects and cooldowns per D-11. Solo combat waits indefinitely, group combat has configurable timeout with auto-attack per D-18. Combat state survives server reload.</done>
</task>

</tasks>

<verification>
- CombatScript creates with interval=0, persistent=True
- Initiative order sorts combatants correctly (interleaved, not grouped)
- advance_turn skips stunned combatants
- end_round ticks effects and decrements cooldowns
- end_combat removes CombatCmdSet from all players
- Group combat triggers round timer; solo combat does not
- active_effects persist to db for reload survival
- process_player_action accepts "charge" action_type and stores pending_charged
- Charged ability fires after charge_turns rounds, character auto-attacks during charge
</verification>

<success_criteria>
CombatScript orchestrates full turn-based combat flow. Initiative is fixed per encounter (D-07). Individual interleaved turns (D-15). Status effects tick at round end (D-11). Group timeout with auto-attack (D-18). Charged abilities declare, charge over rounds with auto-attack, and fire on completion (D-10). Combat state survives server reload. Clean combat end removes all transient state. Integrates combat_engine, combat_ai, status_effects, and ability_engine.
</success_criteria>

<output>
After completion, create `.planning/phases/06a-base-attributes-and-combat/06a-05-SUMMARY.md`
</output>
