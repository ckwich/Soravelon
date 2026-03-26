---
phase: 06a-base-attributes-and-combat
plan: 03
type: execute
wave: 2
depends_on: ["06a-01", "06a-02"]
files_modified:
  - world/combat_engine.py
  - typeclasses/objects.py
  - world/ability_engine.py
autonomous: true
requirements:
  - CMB-01
  - CMB-02
  - CMB-04
must_haves:
  truths:
    - "resolve_damage computes raw damage, applies zone scaling, applies resistance, reduces target HP"
    - "Critical hits roll from Acuity stat and multiply damage by 2.0x per D-20"
    - "Ability effect handlers dispatch to real combat resolution instead of returning stubs"
    - "CorpseContainer spawns on mob death with killer-locked loot phases"
    - "Group loot modes determine who can access corpse contents"
    - "Elite/boss scaling modifiers apply correctly per vault spec"
  artifacts:
    - path: "world/combat_engine.py"
      provides: "Damage resolution, basic attack, ability damage, crit system, corpse spawning, death handling"
      exports: ["resolve_basic_attack", "resolve_ability_damage", "resolve_heal", "apply_elite_boss_scaling", "roll_crit", "handle_mob_death", "handle_player_death", "spawn_corpse", "check_death", "DOMAIN_TO_STAT"]
    - path: "typeclasses/objects.py"
      provides: "CorpseContainer typeclass"
      contains: "class CorpseContainer"
    - path: "world/ability_engine.py"
      provides: "Real effect handlers replacing stubs"
  key_links:
    - from: "world/combat_engine.py"
      to: "world/zone_scaling.py"
      via: "get_player_damage_to_mob, get_mob_damage_for_player, apply_resistance"
      pattern: "zone_scaling\\."
    - from: "world/combat_engine.py"
      to: "world/status_effects.py"
      via: "apply_effect calls for ability status effects"
      pattern: "status_effects\\.apply_effect"
    - from: "world/combat_engine.py"
      to: "world/base_attributes.py"
      via: "stat lookups for damage formulas and crit chance"
      pattern: "base_attributes\\."
    - from: "world/ability_engine.py"
      to: "world/combat_engine.py"
      via: "Effect handlers delegate to combat_engine resolution"
      pattern: "combat_engine\\."
---

<objective>
Build the combat engine core: damage resolution formulas (including critical hits per D-20), ability effect handler wiring, corpse containers, and death handling for both mobs and players.

Purpose: This is the mathematical heart of combat. Damage formulas, zone scaling integration, resistance application, critical hit system, and loot container mechanics all live here. The ability engine's 10 stub handlers get replaced with real combat resolution.
Output: world/combat_engine.py with all damage/heal/death/crit functions. CorpseContainer typeclass. ability_engine.py stubs replaced.
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

@world/ability_engine.py
@world/ability_registry.py
@world/zone_scaling.py
@typeclasses/objects.py
@typeclasses/mobs.py
@world/group_engine.py

<interfaces>
<!-- From Plan 01: world/base_attributes.py -->
```python
STAT_NAMES = ("strength", "agility", "endurance", "mana", "acuity", "presence", "resonance")
def derive_max_hp(character) -> int: ...
def derive_max_stamina(character) -> int: ...
def get_damage_modifier(actions_per_turn) -> float: ...
def record_stat_use(character, action_type, amount=1) -> None: ...
```

<!-- From Plan 02: world/status_effects.py -->
```python
def apply_effect(target, effect_type, duration, magnitude, source_id) -> (bool, str): ...
def check_compound_triggers(target) -> list[str]: ...
def clear_all_effects(target) -> None: ...
def get_effect_modifiers(target) -> dict: ...
```

<!-- From existing: world/zone_scaling.py -->
```python
def get_combat_scale(mob, character) -> float: ...
def get_player_damage_to_mob(base_player_damage, mob, character) -> int: ...
def get_mob_damage_for_player(mob, character) -> (int, int): ...
def apply_resistance(damage, element, target) -> int: ...
```

<!-- From existing: world/ability_registry.py -->
```python
ABILITIES = {
    "momentum_strike": {
        "effect_type": "damage", "scaling_primary": "combat",
        "scaling_secondary": None, "damage_base": ..., ...
    }, ...
}
```
NOTE: scaling_primary uses DOMAIN names ("combat", "subterfuge", etc.), NOT stat names.
The DOMAIN_TO_STAT mapping must be validated against actual ability_registry.py entries.
Read world/ability_registry.py at execution time to confirm all domain values used in
scaling_primary/scaling_secondary are covered by DOMAIN_TO_STAT.

<!-- From existing: typeclasses/objects.py -->
```python
class SoravelonContainer(SoravelonItem):
    # Has weight_reduction, weight_capacity, stack_capacity, can_accept
```

<!-- From existing: world/group_engine.py -->
```python
VALID_LOOT_MODES = ("personal", "ffa", "round_robin", "need_pass")
def _get_leader(character): ...
def _get_group_members(leader): ...
```
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create world/combat_engine.py with damage resolution, crit system, death handling, and corpse containers</name>
  <files>world/combat_engine.py, typeclasses/objects.py</files>
  <action>
Create world/combat_engine.py implementing all combat resolution per D-19 through D-22, D-26, D-27.

**DOMAIN_TO_STAT mapping (validate against ability_registry.py at execution time):**
DOMAIN_TO_STAT dict at module level. Maps domain names used in ability scaling_primary/scaling_secondary
to base stat names. IMPORTANT: Read world/ability_registry.py and confirm every unique scaling_primary
value has a mapping entry. Current expected mapping:
combat->strength, subterfuge->agility, naturalism->resonance, resonance->resonance,
arcana->mana, diplomacy->presence, alchemy->acuity, tactics->acuity, engineering->acuity,
remnance->mana. If any ability uses a domain not in this mapping, add it before proceeding.

**Critical hit system (per D-20 -- "Crits for 1000+ at appropriate tiers are a design goal"):**
roll_crit(attacker) -> (bool, float):
- Base crit chance: 5% (0.05).
- Acuity bonus: +0.2% per point of Acuity stat. E.g., Acuity 50 = 5% + 10% = 15% crit chance.
- For mobs: use mob.db.crit_chance if set, else 3% flat (mobs don't scale with Acuity).
- Roll random.random() < crit_chance.
- Crit multiplier: 2.0x base. (Future: equipment/buffs can modify this.)
- Return (is_crit: bool, multiplier: float). multiplier is 2.0 on crit, 1.0 on non-crit.
- Record stat use: if attacker is character and crit lands, record_stat_use(attacker, "critical_hit").

**Basic attack resolution (per D-19):**
resolve_basic_attack(attacker, target, weapon=None) -> (bool, str, int):
- Read weapon damage range from attacker equipment (or bare-hands fallback: 3-6 damage).
- For characters: raw = randint(weapon_min, weapon_max) + (strength * 0.5). Element from weapon (default "physical").
- For mobs: raw = randint(mob.db.ref_damage_min, mob.db.ref_damage_max). Element from mob.db.element or "physical".
- Apply crit: is_crit, crit_mult = roll_crit(attacker). raw *= crit_mult.
- Apply zone scaling: if attacker is mob, use get_mob_damage_for_player. If attacker is character, use get_player_damage_to_mob.
- Apply resistance: apply_resistance(scaled, element, target).
- Apply elite/boss scaling modifiers if target is mob with rarity elite/legendary.
- Reduce target.ndb.hp by final damage. Clamp to 0.
- Record stat use: if attacker is character, record_stat_use(attacker, "melee_hit"). If target is character, record_stat_use(target, "damage_taken").
- Check miss chance: if target has "blind" effect on attacker, roll against miss_chance_increase.
- Include "|y*CRITICAL*|n" in damage message if is_crit.
- Return (True, damage_message, final_damage) or (False, miss_message, 0).

**Ability damage resolution (per D-08, vault formula):**
resolve_ability_damage(character, ability, target) -> (bool, str, int):
- ability_base = ability["damage_base"] (add this field to ability registry entries)
- primary_stat = character.db.base_stats.get(DOMAIN_TO_STAT.get(ability["scaling_primary"], "strength"), 10)
- secondary_stat from scaling_secondary mapped similarly (0 if None).
- raw = ability_base * (1 + primary * 0.02 + secondary * 0.01)
- Apply crit: is_crit, crit_mult = roll_crit(character). raw *= crit_mult.
- Apply zone scaling, resistance, elite/boss modifiers same as basic attack.
- Apply status effects from ability if ability has "status_effect" field: call status_effects.apply_effect.
- Include "|y*CRITICAL*|n" in message if is_crit.
- Return (True, message, damage).

**Heal resolution:**
resolve_heal(character, ability, target) -> (bool, str, int):
- heal_amount = ability.get("heal_base", 20) * (1 + primary_stat * 0.015)
- target.ndb.hp = min(derive_max_hp(target), target.ndb.hp + heal_amount)
- Return (True, message, heal_amount).

**Elite/Boss scaling (per D-21):**
apply_elite_boss_scaling(damage, mob_rarity, is_incoming=True) -> int:
- For "elite" (or rare mob): if is_incoming (mob attacking player), mult 1.40. If outgoing (player attacking mob), reduce by 0.25.
- For "legendary" (boss): if is_incoming, mult 1.80. If outgoing, reduce by 0.50.
- For "normal"/"magic": no modification.
- Return adjusted damage.

**Death handling (per D-26, D-27):**
check_death(combatant) -> bool:
- Return True if combatant.ndb.hp <= 0.

handle_mob_death(mob, killer) -> str:
- Call mob.at_death(killer=killer) (existing -- handles loot, room flags, respawn).
- Call spawn_corpse(mob, killer) for corpse container.
- Clear mob from combat (remove from combatant list).
- Return death message.

handle_player_death(character) -> str:
- Per D-26: spawn corpse at death location with all carried equipment.
- Move all items from character inventory to corpse container.
- Set character.ndb.hp = 0.
- Return death message. (Actual respawn teleport handled by CombatScript on cleanup.)

**Corpse container (per D-27 and research):**
Add CorpseContainer class to typeclasses/objects.py (after SoravelonContainer):

```python
class CorpseContainer(SoravelonContainer):
    GRACE_PERIOD = 120      # 2 minutes killer-locked
    OPEN_PERIOD = 300       # 5 minutes open to all

    def at_object_creation(self):
        super().at_object_creation()
        self.db.killer_id = None
        self.db.killer_group_leader_id = None
        self.db.loot_phase = "locked"
        self.db.mob_key = ""
        self.db.mob_rarity = "normal"
        self.db.decay_at = None  # timestamp for crash-recovery cleanup
        self.locks.add("get:false()")

    def can_loot(self, character):
        # locked: killer or killer's group only
        # open: anyone
        # decayed: nobody
```

spawn_corpse(mob, killer) -> CorpseContainer:
- Create CorpseContainer at mob.location.
- Set killer_id, killer_group_leader_id (from killer.ndb.group_leader_id if grouped per D-30).
- Move loot items from mob death into corpse (already dropped to room by at_death, move to corpse instead).
- Schedule phase transitions with delay(): GRACE_PERIOD -> "open", GRACE_PERIOD+OPEN_PERIOD -> delete.
- Set decay_at for crash-recovery sweep.
- Return corpse object.

_transition_corpse(corpse_id, new_phase): helper for delay callback.
  </action>
  <verify>
    <automated>python -c "from world.combat_engine import resolve_basic_attack, resolve_ability_damage, handle_mob_death, spawn_corpse, DOMAIN_TO_STAT, roll_crit; from typeclasses.objects import CorpseContainer; print('OK')"</automated>
  </verify>
  <done>combat_engine.py resolves basic attacks and ability damage with zone scaling, resistance, and critical hits (Acuity-based crit chance, 2.0x multiplier per D-20). Handles mob/player death with corpse spawning. CorpseContainer typeclass has killer-locked loot phases with timed transitions. Elite/boss scaling applies vault-spec multipliers. DOMAIN_TO_STAT mapping validated against ability_registry.py.</done>
</task>

<task type="auto">
  <name>Task 2: Wire ability_engine.py stub handlers to real combat resolution</name>
  <files>world/ability_engine.py</files>
  <action>
Replace the 10 stub effect handlers in ability_engine.py with real combat resolution. Per research wiring table:

Replace each handler function. All handlers receive (character, ability, target) and return (bool, str) message per project convention. The use_ability() dispatch and cooldown/resource logic remains unchanged -- only the handler implementations change.

**_handle_damage(character, ability, target):**
- Import combat_engine.resolve_ability_damage lazily.
- ok, msg, dmg = resolve_ability_damage(character, ability, target)
- Return msg string.

**_handle_dot(character, ability, target):**
- Import status_effects.apply_effect lazily.
- effect_type = ability.get("status_effect", "poison")
- duration = ability.get("effect_duration", 3)
- magnitude = ability.get("effect_magnitude", ability.get("damage_base", 8))
- ok, msg = apply_effect(target, effect_type, duration, magnitude, character.id)
- Return msg.

**_handle_buff(character, ability, target):**
- effect_type = ability.get("buff_type", "haste")
- Apply buff to character (self-buff): apply_effect(character, effect_type, duration, magnitude, character.id)
- Return message.

**_handle_debuff(character, ability, target):**
- effect_type = ability.get("debuff_type", "weaken")
- Apply debuff to target: apply_effect(target, effect_type, duration, magnitude, character.id)
- Return message.

**_handle_utility(character, ability, target):**
- Context-dependent. Check ability for "utility_action" key. If "flee_boost", add haste. If "reveal", reveal affix. Default: return descriptive text.

**_handle_social(character, ability, target):**
- Apply "charm" effect to target if applicable. Record stat use "social_ability".
- Return message.

**_handle_tactical(character, ability, target):**
- If ability has "tactical_action": "group_buff", apply buff to all group members.
- Record stat use for tactics.
- Return message.

**_handle_compound_trigger(character, ability, target):**
- Import status_effects.check_compound_triggers.
- compounds = check_compound_triggers(target)
- Return message listing triggered compounds.

**_handle_heal(character, ability, target):**
- Import combat_engine.resolve_heal.
- ok, msg, healed = resolve_heal(character, ability, target or character)
- Return msg.

**_handle_status(character, ability, target):**
- effect_type = ability.get("status_effect", "slow")
- Application chance: roll random.random() against ability["application_chance"]. On miss, return "resisted" message.
- apply_effect(target, effect_type, duration, magnitude, character.id)
- Return message.

Each handler uses lazy imports to avoid circular dependencies (standard project pattern).
  </action>
  <verify>
    <automated>python -c "from world.ability_engine import EFFECT_HANDLERS, _handle_damage; import inspect; src = inspect.getsource(_handle_damage); assert 'stub' not in src.lower() and 'combat_engine' in src, 'Handler still a stub'; print('All handlers:', list(EFFECT_HANDLERS.keys())); print('OK')"</automated>
  </verify>
  <done>All 10 ability effect handlers dispatch to real combat resolution in combat_engine.py and status_effects.py. No stub text remains. Handlers return proper combat messages with damage numbers, effect applications, and heal amounts.</done>
</task>

</tasks>

<verification>
- resolve_basic_attack with a mock character/mob produces damage in expected range
- resolve_ability_damage applies stat scaling correctly
- Critical hits trigger based on Acuity stat; crit multiplier applies 2.0x damage
- CorpseContainer.can_loot returns True for killer, False for others in locked phase
- Elite mob damage uses 1.40x multiplier
- ability_engine handlers no longer return "[stub]" text (verify via inspect.getsource)
- Zone scaling functions are called (not bypassed) during damage resolution
- DOMAIN_TO_STAT covers all domains used in ability_registry.py scaling_primary fields
</verification>

<success_criteria>
Combat damage resolution integrates zone scaling (CMB-02), base stat formulas, elemental resistance, and critical hits (D-20: Acuity-driven crit chance, 2.0x multiplier enabling 1000+ crits at appropriate tiers). Ability effect handlers wire to real combat (CMB-01). Corpse containers support killer-locked loot with group awareness (CMB-04). Elite/boss scaling matches vault spec per D-21.
</success_criteria>

<output>
After completion, create `.planning/phases/06a-base-attributes-and-combat/06a-03-SUMMARY.md`
</output>
