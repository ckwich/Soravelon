---
phase: 05b-ability-content-authoring
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: [world/ability_registry.py]
autonomous: false
requirements: [ABL-04]

must_haves:
  truths:
    - "Combat domain has 15 pool abilities (tiers 1-4) with concrete damage values, resource costs, cooldowns"
    - "Tactics domain has 15 pool abilities (tiers 1-4) with concrete damage values, resource costs, cooldowns"
    - "All 9 Combat-primary subclasses have 2 signature abilities each (Tier 3 + Tier 4)"
    - "All 9 Tactics-primary subclasses have 2 signature abilities each (Tier 3 + Tier 4)"
    - "Combat abilities use momentum resource; Tactics abilities use command resource"
    - "Duskblade signatures feel mechanically distinct from Vanguard signatures"
  artifacts:
    - path: "world/ability_registry.py"
      provides: "66 ability entries for combat + tactics domains"
      contains: "momentum_strike"
  key_links:
    - from: "world/ability_registry.py"
      to: "world/guild_engine.py SUBCLASSES"
      via: "subclass_id field matches SUBCLASSES keys"
      pattern: "subclass_id.*duskblade|vanguard|warbringer"
---

<objective>
Author all 66 ability definitions for the Combat + Tactics domain pair: 15 Combat pool abilities, 15 Tactics pool abilities, 18 Combat-primary subclass signatures, and 18 Tactics-primary subclass signatures.

Purpose: Combat (Press/Momentum) and Tactics (Orchestrate/Command) are the physical aggression and battlefield control domains. Authoring them together ensures cross-domain awareness -- a Vanguard (Combat+Tactics) signature should complement both domain pools, and a Warbringer (Tactics+Combat) should feel distinct despite sharing the same two domains.

Output: 66 new ABILITIES dict entries in world/ability_registry.py replacing and extending the existing combat/tactics stubs.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/05b-ability-content-authoring/5b-CONTEXT.md

@world/ability_registry.py
@world/combat_engine.py
@world/status_effects.py
@world/guild_engine.py
@world/base_attributes.py

<interfaces>
From world/ability_registry.py — ability entry schema (16 fields per D-18):
```python
{
    "id": str,              # unique ability_id, snake_case
    "name": str,            # display name
    "domain": str,          # "combat" or "tactics"
    "tier": int,            # 1-4
    "resource_cost": int,   # cost in domain resource
    "resource_type": str,   # "momentum" or "command"
    "cooldown": int,        # rounds, 0 = spammable
    "charge_turns": int,    # 0 = instant, 1+ = charged
    "effect_type": str,     # from EFFECT_TYPES tuple
    "scaling_primary": str, # domain name for stat lookup
    "scaling_secondary": str | None,
    "application_chance": float,  # 0.0-1.0
    "description": str,     # flavor text (no [STUB])
    "room_flag_written": str | None,
    "attuned_variants": dict,  # {} for non-resonance domains
    "subclass_id": str | None,  # None for pool, subclass key for signatures
}
```

From world/combat_engine.py — damage formula:
```python
# resolve_ability_damage formula:
# raw = ability_base * (1 + primary_stat*0.02 + secondary_stat*0.01)
# Then crit (2x), zone scaling, resistance, elite/boss modifiers
DOMAIN_TO_STAT = {
    "combat": "strength",
    "tactics": "acuity",
}
```

From world/status_effects.py — available effects:
```python
STACKABLE_EFFECTS = {"poison", "bleed", "burn", "weaken", "drain"}
NON_STACKABLE_EFFECTS = {"slow", "root", "blind", "stun", "charm", "haste", "wet"}
```

From world/guild_engine.py — Combat-primary subclasses:
- duskblade (combat+subterfuge): Momentum Vanish, burst on re-entry
- thornguard (combat+naturalism): Nature self-buffs
- ruinborn (combat+resonance): Resonance stacks via strikes, node burst
- spellbreaker (combat+arcana): Anti-magic, Mana disruption
- ironvoice (combat+diplomacy): Intimidation debuffs, Presence scaling
- ashfang (combat+alchemy): Bleed+Poison on melee
- vanguard (combat+tactics): Guard mechanics, group action budget
- ironwright (combat+engineering): Mid-battle weapon crafting, no companion
- dragonblooded (combat+remnance): Ancient enhancements, Resonance-stat resistances

From world/guild_engine.py — Tactics-primary subclasses:
- warbringer (tactics+combat): Frontline commander, Guard + Command
- greycommand (tactics+subterfuge): Scouting, group stealth, intel advantage
- wildtactician (tactics+naturalism): Zone control via nature
- nodewarden (tactics+resonance): Node manipulation in combat
- siegecaller (tactics+arcana): Long-range magical area placement
- warlord (tactics+diplomacy): Morale mechanics, Presence-scaled Command
- siegemaster (tactics+alchemy): Area DoT tactics, chemical area denial
- fieldwright (tactics+engineering): Combat construction, field fortifications
- oathbreaker (tactics+remnance): Ancient tactical knowledge, pre-curse doctrine
</interfaces>

<vault_refs>
MANDATORY — Read these vault files before authoring abilities:
- C:\Obsidian\brain\Soravelon\soravelon-guilds.md — Guild of Ironblood and Guild of Warcraft sections
- C:\Obsidian\brain\Soravelon\soravelon-abilities.md — Combat system, Momentum resource, Command resource
- C:\Obsidian\brain\Soravelon\soravelon-fingerprints.md — Combat (PRESS) and Tactics (ORCHESTRATE) fingerprints
</vault_refs>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Author 66 Combat + Tactics ability definitions</name>
  <files>world/ability_registry.py</files>
  <action>
Read the three vault docs listed in vault_refs to absorb domain identity, fingerprint verbs, subclass hooks, and resource mechanics.

Then author abilities in world/ability_registry.py by replacing existing combat/tactics stubs and adding new entries to the ABILITIES dict. Follow the exact 16-field schema from the interfaces block.

**Combat domain pool (15 abilities, resource_type="momentum"):**
- Tier 1 (4 abilities): Basic strikes, momentum builders. Damage effect_type, 0-1 cooldown, 0 charge_turns. Per D-05: derive damage values from combat_engine formula (ability_base 12-18 for T1). Per D-07: damage abilities are 0-1 round cooldown. Per D-08: Combat is physical domain, charge_turns=0 for nearly all abilities.
- Tier 2 (4 abilities): Core combat rhythm. Mix of damage and buff/debuff. Cooldowns 1-3.
- Tier 3 (4 abilities): Advanced strikes, compound effects. Cooldowns 2-4. Higher resource costs.
- Tier 4 (3 abilities): Domain capstones. Powerful damage or compound_trigger. Cooldowns 4-6.
- Per D-17: Combat fingerprint verb is "Press" -- ability names should evoke sustained aggression (Break, Crush, Charge, Rampage, etc.)
- Per D-09: Differentiate via status effect patterns. Combat abilities should lean into bleed, weaken, and raw damage. No spatial positioning.
- Per D-12: Most abilities write temporary room flags (e.g., "bloodied", "shattered", "crushed")

**Tactics domain pool (15 abilities, resource_type="command"):**
- Tier 1 (4 abilities): Basic commands, group buffs. Mix of tactical and buff effect_types. Cooldown 1-3.
- Tier 2 (4 abilities): Core battlefield control. Debuffs, tactical effects. Cooldowns 2-4.
- Tier 3 (4 abilities): Advanced coordination. Compound_trigger, area buffs. Cooldowns 3-5.
- Tier 4 (3 abilities): Domain capstones. Powerful tactical or compound_trigger. Cooldowns 5-8.
- Per D-17: Tactics fingerprint verb is "Orchestrate" -- ability names should evoke command and coordination (Rally, Direct, Coordinate, Formation, etc.)
- Per D-11: Tactics is group-oriented but solo-viable. Solo abilities work at reduced effect, group abilities scale with party size.
- Per D-08: Tactics is NOT a caster domain. charge_turns=0 for most abilities (instant commands).

**Combat-primary subclass signatures (18 abilities = 9 subclasses x 2):**
For each of the 9 Combat-primary subclasses, author:
- Tier 3 signature (subclass_id set, tier=3): Enhanced domain blend per D-13. resource_type="momentum".
- Tier 4 signature (subclass_id set, tier=4): Mechanically unique defining ability per D-13/D-14.

Use each subclass's hook from guild_engine.py to drive the signature design:
- duskblade: T3=stealth burst strike, T4=mid-combat Vanish+guaranteed crit re-entry
- thornguard: T3=nature armor self-buff, T4=living reinforcement (absorb + reflect)
- ruinborn: T3=resonance-stack melee, T4=node burst detonation (damage all + room flag)
- spellbreaker: T3=mana drain strike, T4=anti-magic field (silence area)
- ironvoice: T3=intimidation debuff (presence scaling), T4=warcry (AoE weaken+slow)
- ashfang: T3=toxic cleave (bleed+poison AoE), T4=blood frenzy (self-buff, attacks apply double stacks)
- vanguard: T3=guard stance (absorb for ally), T4=formation break (AoE damage + group action bonus)
- ironwright: T3=improvised weapon (bonus damage), T4=field-forged masterwork (create temporary weapon with unique effect)
- dragonblooded: T3=ancient resilience (resistance buff), T4=dragonfire strike (massive damage + burn, scales off resonance stat)

**Tactics-primary subclass signatures (18 abilities = 9 subclasses x 2):**
- warbringer: T3=commanding charge (damage+command build), T4=warfront (sustained AoE buff zone)
- greycommand: T3=intelligence report (reveal enemy abilities), T4=shadow operation (group stealth + ambush bonus)
- wildtactician: T3=terrain control (root area), T4=beast assault (summon beast wave, tactical damage)
- nodewarden: T3=node manipulation (write resonant flag), T4=node weaponization (massive area damage from node energy)
- siegecaller: T3=arcane barrage (ranged area damage), T4=siege spell (delayed massive damage, charge_turns=2)
- warlord: T3=rally cry (group buff, presence scaling), T4=sovereign command (AoE charm on enemies, skip turn)
- siegemaster: T3=chemical barrage (area DoT), T4=plague zone (sustained area poison+slow)
- fieldwright: T3=deploy barricade (group damage reduction), T4=field fortress (compound_trigger, sustained zone control)
- oathbreaker: T3=ancient formation (group buff from pre-curse knowledge), T4=forgotten doctrine (unique tactical ability, echoes-amplified)

Per D-06: resource_cost matches effect type impact, NOT tier. Damage=cheap (10-20), CC=moderate (20-35), compound=expensive (35-60).
Per D-14: Tier 4 signature power is VARIED -- some are big damage, some are unique sideways mechanics.

**Implementation notes:**
- Remove existing combat/tactics stubs (momentum_strike, command_rally) and replace with full entries
- Keep the ability_id naming convention: snake_case, descriptive (e.g., "crushing_advance", "tactical_rally")
- scaling_primary should match the domain. scaling_secondary for signatures should match the secondary domain.
- The DOMAIN_ABILITIES and SUBCLASS_SIGNATURES derived lookups rebuild automatically from ABILITIES dict.
- Keep existing non-combat/non-tactics stubs untouched.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "
from world.ability_registry import ABILITIES, DOMAIN_ABILITIES, SUBCLASS_SIGNATURES
# Check combat pool count
combat_pool = DOMAIN_ABILITIES.get('combat', {})
combat_count = sum(len(v) for v in combat_pool.values())
assert combat_count == 15, f'Combat pool: {combat_count} != 15'
# Check tactics pool count
tactics_pool = DOMAIN_ABILITIES.get('tactics', {})
tactics_count = sum(len(v) for v in tactics_pool.values())
assert tactics_count == 15, f'Tactics pool: {tactics_count} != 15'
# Check combat subclass sigs (9 subclasses x 2)
combat_subs = ['duskblade','thornguard','ruinborn','spellbreaker','ironvoice','ashfang','vanguard','ironwright','dragonblooded']
for sc in combat_subs:
    assert sc in SUBCLASS_SIGNATURES, f'Missing sigs for {sc}'
    assert len(SUBCLASS_SIGNATURES[sc]) == 2, f'{sc} has {len(SUBCLASS_SIGNATURES[sc])} sigs, expected 2'
# Check tactics subclass sigs (9 subclasses x 2)
tactics_subs = ['warbringer','greycommand','wildtactician','nodewarden','siegecaller','warlord','siegemaster','fieldwright','oathbreaker']
for sc in tactics_subs:
    assert sc in SUBCLASS_SIGNATURES, f'Missing sigs for {sc}'
    assert len(SUBCLASS_SIGNATURES[sc]) == 2, f'{sc} has {len(SUBCLASS_SIGNATURES[sc])} sigs, expected 2'
# Check no stubs remain
for aid, a in ABILITIES.items():
    if a['domain'] in ('combat', 'tactics'):
        assert '[STUB' not in a['description'], f'{aid} still has stub description'
print('PASS: 66 combat+tactics abilities validated')
"</automated>
  </verify>
  <done>
    - 15 Combat pool abilities exist with concrete values across tiers 1-4
    - 15 Tactics pool abilities exist with concrete values across tiers 1-4
    - 18 Combat-primary subclass signatures exist (2 per subclass)
    - 18 Tactics-primary subclass signatures exist (2 per subclass)
    - No [STUB] descriptions remain for combat or tactics domains
    - DOMAIN_ABILITIES and SUBCLASS_SIGNATURES derived lookups return correct data
  </done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <name>Task 2: User review of ability definitions</name>
  <action>User reviews ability definitions for balance, distinctiveness, and lore fidelity.</action>
  <what-built>66 Combat + Tactics ability definitions authored in ability_registry.py</what-built>
  <how-to-verify>
    1. Review the table of Combat pool abilities (15) for balance: damage values, resource costs, cooldowns
    2. Review the table of Tactics pool abilities (15) for balance and solo-viability
    3. Review Combat-primary subclass signatures (18) -- do Duskblade sigs feel distinct from Ironvoice sigs?
    4. Review Tactics-primary subclass signatures (18) -- does Warbringer feel distinct from Warlord?
    5. Check that fingerprint verbs (Press, Orchestrate) are reflected in ability naming
    6. Mark any abilities needing revision
  </how-to-verify>
  <resume-signal>Type "approved" or describe specific abilities to revise</resume-signal>
</task>

</tasks>

<verification>
- `python -c "from world.ability_registry import ABILITIES; print(len(ABILITIES))"` shows increase from 14
- All combat abilities use resource_type="momentum"
- All tactics abilities use resource_type="command"
- Every subclass_id matches a key in guild_engine.SUBCLASSES
- No duplicate ability_id values
</verification>

<success_criteria>
- 30 domain pool abilities authored (15 combat + 15 tactics) with no stubs
- 36 subclass signatures authored (18 combat-primary + 18 tactics-primary) with no stubs
- User has reviewed and approved the ability tables
- DOMAIN_ABILITIES["combat"] and DOMAIN_ABILITIES["tactics"] return correct tier breakdowns
</success_criteria>

<output>
After completion, create `.planning/phases/05b-ability-content-authoring/05b-01-SUMMARY.md`
</output>
