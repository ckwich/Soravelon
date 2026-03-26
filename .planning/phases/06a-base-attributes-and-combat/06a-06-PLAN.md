---
phase: 06a-base-attributes-and-combat
plan: 06
type: execute
wave: 3
depends_on: ["06a-05"]
files_modified:
  - commands/combat_commands.py
  - commands/default_cmdsets.py
  - typeclasses/characters.py
  - world/oob_publisher.py
autonomous: true
requirements:
  - CMB-01
  - CMB-04
must_haves:
  truths:
    - "CmdAttack initiates combat or performs basic attack on current target"
    - "CmdFlee attempts escape with speed/skill check per D-28"
    - "CmdTarget switches auto-target per D-14"
    - "CombatCmdSet replaces default movement during combat per D-17"
    - "push_combat_update sends structured combat state to client"
    - "push_stat_update sends HP/stamina/resource bars to client"
    - "Auto-engage triggers when player enters room with aggressive mob per D-13"
  artifacts:
    - path: "commands/combat_commands.py"
      provides: "CmdAttack, CmdFlee, CmdTarget, CmdPass, CombatCmdSet"
      exports: ["CmdAttack", "CmdFlee", "CmdTarget", "CmdPass", "CombatCmdSet"]
    - path: "world/oob_publisher.py"
      provides: "Filled push_combat_update and push_stat_update"
  key_links:
    - from: "commands/combat_commands.py"
      to: "world/combat_script.py"
      via: "Commands call process_player_action on CombatScript"
      pattern: "combat_script"
    - from: "typeclasses/characters.py"
      to: "world/combat_script.py"
      via: "at_after_move checks for aggressive mobs and starts combat"
      pattern: "start_combat"
    - from: "world/oob_publisher.py"
      to: "world/combat_script.py"
      via: "CombatScript calls push_combat_update on turn changes"
      pattern: "push_combat_update"
---

<objective>
Build combat commands (CmdAttack, CmdFlee, CmdTarget, CmdPass), CombatCmdSet, auto-engage wiring, and OOB combat/stat update publishers.

Purpose: This is the player-facing layer. Commands translate player input into combat actions. CombatCmdSet restricts available commands during combat. OOB publishers push combat state to the desktop client. Auto-engage makes aggressive mobs start fights.
Output: commands/combat_commands.py with all combat commands and CombatCmdSet. OOB publishers filled. Character hooks for auto-engage.
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

@.planning/phases/06a-base-attributes-and-combat/06a-05-SUMMARY.md

@commands/default_cmdsets.py
@commands/cmd_abilities.py
@typeclasses/characters.py
@world/oob_publisher.py

<interfaces>
<!-- From Plan 05: world/combat_script.py -->
```python
class CombatScript(SoravelonScript): ...
def start_combat(room, initiator, targets) -> CombatScript: ...
def join_combat(combat_script, newcomer) -> (bool, str): ...
# CombatScript methods:
#   process_player_action(character, action_type, target, ability_id)
#   is_combatant(obj) -> bool
#   get_current_combatant() -> obj
```

<!-- From existing: commands/cmd_abilities.py -->
```python
class CmdUseAbility(Command):
    key = "use"
    # Dispatches to ability_engine.use_ability
```

<!-- From existing: world/oob_publisher.py -->
```python
def _should_send(character, msg_type): ...
def _mark_sent(character, msg_type): ...
# push_combat_update and push_stat_update are Phase 6 placeholders
```

<!-- From existing: world/mob_disposition.py -->
```python
def get_mob_behavior(mob, character) -> str: ...  # "aggressive", "territorial", etc.
```
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create combat commands and CombatCmdSet</name>
  <files>commands/combat_commands.py, commands/default_cmdsets.py</files>
  <action>
Create commands/combat_commands.py with all combat commands per D-14, D-16, D-17, D-28.

**CombatCmdSet (per research design):**
```python
class CombatCmdSet(CmdSet):
    key = "CombatCmdSet"
    mergetype = "Replace"
    priority = 10
    no_exits = True  # Block normal exit traversal during combat
```
Contains: CmdAttack, CmdUseAbility (import from cmd_abilities), CmdFlee, CmdTarget, CmdPass.
Also re-add CmdAbilities for checking ability list during combat.
Also include basic look command so players can still look around.

**CmdAttack:**
- key = "attack"
- aliases = ["a", "hit", "strike"]
- Parse target from args. If no args, use auto-target (character.ndb.combat_target_id per D-14).
- If not in combat: find mob in room, call start_combat. Set auto-target.
- If in combat: validate it's this character's turn. Call combat_script.process_player_action(character, "basic_attack", target).
- Update auto-target to last attacked mob (D-14).

**CmdFlee (per D-28):**
- key = "flee"
- aliases = ["escape", "run"]
- Check: cannot flee while rooted or stunned (get_effect_modifiers).
- Speed check: character agility vs mob agility. Skill bonus from stealth domain score.
- Exit check: must have at least one exit from room.
- On failure: lose turn ("You fail to escape!").
- On success: move to random adjacent room. Remove from combat. Message room.
- Call combat_script.process_player_action(character, "flee").

**CmdTarget (per D-14):**
- key = "target"
- aliases = ["t"]
- Parse target name from args. Find matching mob in combat.
- Set character.ndb.combat_target_id = target.id.
- Does NOT consume an action.
- Message: "You focus your attention on {target}."

**CmdPass:**
- key = "pass"
- aliases = ["wait", "skip"]
- End turn early (forfeit remaining actions).
- Call combat_script.process_player_action(character, "pass").

**Register CombatCmdSet:**
CombatCmdSet is NOT added to CharacterCmdSet (it's added/removed dynamically by CombatScript).
No changes needed to at_cmdset_creation.

**Register CmdAttack in CharacterCmdSet:**
In default_cmdsets.py, add CmdAttack to CharacterCmdSet.at_cmdset_creation() so players can initiate combat outside of CombatCmdSet:
```python
from commands.combat_commands import CmdAttack
self.add(CmdAttack())
```
The CombatCmdSet version overrides this when combat is active.
  </action>
  <verify>
    <automated>python -c "from commands.combat_commands import CmdAttack, CmdFlee, CmdTarget, CmdPass, CombatCmdSet; print('OK:', CombatCmdSet.key, 'priority', CombatCmdSet.priority)"</automated>
  </verify>
  <done>All combat commands created: CmdAttack (initiates/performs attacks), CmdFlee (speed check escape), CmdTarget (switch focus), CmdPass (skip turn). CombatCmdSet replaces default commands during combat. CmdAttack registered in CharacterCmdSet for combat initiation.</done>
</task>

<task type="auto">
  <name>Task 2: Wire auto-engage, OOB publishers, and combat cleanup hooks</name>
  <files>typeclasses/characters.py, world/oob_publisher.py</files>
  <action>
**Auto-engage in Character.at_after_move (per D-13):**
Add to at_after_move, after existing map_update logic:
```python
# Auto-engage: check for aggressive mobs in room
if self.location and not self.ndb.combat_handler:
    from world.combat_script import start_combat
    aggressive_mobs = []
    for obj in self.location.contents:
        if hasattr(obj, 'get_behavior_toward'):
            behavior = obj.get_behavior_toward(self)
            if behavior == "aggressive" and (obj.db.combat_enabled is not False):
                aggressive_mobs.append(obj)
    if aggressive_mobs:
        start_combat(self.location, aggressive_mobs[0], [self])
```
Only trigger if character is NOT already in combat. Multiple aggressive mobs join the same combat.

**Combat cleanup in at_pre_unpuppet:**
Add before existing commit logic:
```python
# Clean disconnect from combat
if self.ndb.combat_handler:
    self.ndb.combat_handler.remove_combatant(self)
```
This handles Pitfall 5 from research.

**OOB push_combat_update (fill Phase 6 placeholder):**
In oob_publisher.py, replace push_combat_update placeholder with real implementation:
```python
def push_combat_update(character):
    if not _should_send(character, "combat_update"):
        return
    handler = character.ndb.combat_handler
    if not handler:
        return
    # Build combatants list
    combatants = []
    for cid in handler.db.combatant_ids:
        obj = _resolve_combatant(cid)
        if not obj:
            continue
        is_mob = not hasattr(obj, 'account')
        hp_pct = (obj.ndb.hp or 0) / max(1, obj.db.hp_max if is_mob else derive_max_hp(obj))
        effects = [e["type"] for e in (obj.ndb.active_effects or [])]
        combatants.append({
            "id": cid, "name": obj.key, "hp_pct": round(hp_pct, 2),
            "is_mob": is_mob, "effects": effects,
            "is_current": cid == handler.db.combatant_ids[handler.db.current_turn_index],
        })
    # Build available abilities
    available = _get_available_abilities(character)
    payload = {
        "state": "active",
        "round": handler.db.round_number,
        "your_turn": handler.get_current_combatant() == character,
        "actions_remaining": character.ndb.actions_remaining or 0,
        "combatants": combatants,
        "available_abilities": available,
        "target_id": character.ndb.combat_target_id,
    }
    character.msg(combat_update=payload)
    _mark_sent(character, "combat_update")
```

**OOB push_stat_update (fill Phase 6 placeholder):**
```python
def push_stat_update(character):
    if not _should_send(character, "stat_update"):
        return
    from world.base_attributes import derive_max_hp, derive_max_stamina
    from world.ability_engine import get_domain_resource
    resource = get_domain_resource(character)
    payload = {
        "hp": character.ndb.hp or 0,
        "hp_max": derive_max_hp(character),
        "stamina": character.ndb.stamina or 0,
        "stamina_max": derive_max_stamina(character),
        "domain_resource": resource,
        "conditions": [f"{e['type']}_{e.get('stacks', 1)}" for e in (character.ndb.active_effects or [])],
    }
    character.msg(stat_update=payload)
    _mark_sent(character, "stat_update")
```

Helper _resolve_combatant(cid) and _get_available_abilities(character) as internal functions in oob_publisher.
  </action>
  <verify>
    <automated>python -c "from world.oob_publisher import push_combat_update, push_stat_update; print('OOB publishers importable')"</automated>
  </verify>
  <done>Auto-engage fires when player enters room with aggressive mobs. Combat cleanup on disconnect prevents orphaned CombatCmdSets. push_combat_update sends structured combat state per research OOB schema. push_stat_update sends HP/stamina/resource bars. Both respect debounce intervals.</done>
</task>

</tasks>

<verification>
- CmdAttack in non-combat context creates CombatScript and begins combat
- CmdAttack in combat context resolves basic attack on target
- CmdFlee blocked when rooted, succeeds with movement on speed check pass
- CmdTarget sets ndb.combat_target_id without consuming action
- Auto-engage triggers for aggressive mob when player enters room
- push_combat_update sends valid payload matching research schema
- push_stat_update includes HP, stamina, domain resource, and conditions
- Character disconnect removes from active combat cleanly
</verification>

<success_criteria>
Player-facing combat commands handle all input types per D-17 (typed commands). Auto-target works per D-14. Flee mechanics follow D-28 (speed check, exit required, blocked by root/stun). Auto-engage from disposition per D-13. OOB publishers deliver combat and stat data to desktop client. Combat cleanup prevents orphaned state on disconnect.
</success_criteria>

<output>
After completion, create `.planning/phases/06a-base-attributes-and-combat/06a-06-SUMMARY.md`
</output>
