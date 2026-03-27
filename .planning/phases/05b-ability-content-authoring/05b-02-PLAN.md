---
phase: 05b-ability-content-authoring
plan: 02
type: execute
wave: 1
depends_on: []
files_modified: [world/ability_registry.py]
autonomous: false
requirements: [ABL-04]

must_haves:
  truths:
    - "Subterfuge domain has 15 pool abilities (tiers 1-4) with concrete values"
    - "Diplomacy domain has 15 pool abilities (tiers 1-4) with concrete values"
    - "All 9 Subterfuge-primary subclasses have 2 signature abilities each (Tier 3 + Tier 4)"
    - "All 9 Diplomacy-primary subclasses have 2 signature abilities each (Tier 3 + Tier 4)"
    - "Subterfuge abilities use focus resource; Diplomacy abilities use influence resource"
    - "Grimwarden signatures feel mechanically distinct from Blackthorn signatures"
  artifacts:
    - path: "world/ability_registry.py"
      provides: "66 ability entries for subterfuge + diplomacy domains"
      contains: "shadow_read"
  key_links:
    - from: "world/ability_registry.py"
      to: "world/guild_engine.py SUBCLASSES"
      via: "subclass_id field matches SUBCLASSES keys"
      pattern: "subclass_id.*grimwarden|shadowbroker"
---

<objective>
Author all 66 ability definitions for the Subterfuge + Diplomacy domain pair: 15 Subterfuge pool abilities, 15 Diplomacy pool abilities, 18 Subterfuge-primary subclass signatures, and 18 Diplomacy-primary subclass signatures.

Purpose: Subterfuge (Read/Focus) and Diplomacy (Leverage/Influence) are the information and social power domains. Authoring them together ensures cross-domain awareness -- a Tally Agent (Subterfuge+Diplomacy) signature should bridge both pools, and a Shadowbroker (Diplomacy+Subterfuge) should feel distinct despite sharing domains.

Output: 66 new ABILITIES dict entries in world/ability_registry.py replacing and extending the existing subterfuge/diplomacy stubs.
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
    "id": str, "name": str, "domain": str, "tier": int,
    "resource_cost": int, "resource_type": str, "cooldown": int,
    "charge_turns": int, "effect_type": str, "scaling_primary": str,
    "scaling_secondary": str | None, "application_chance": float,
    "description": str, "room_flag_written": str | None,
    "attuned_variants": dict, "subclass_id": str | None,
}
```

From world/combat_engine.py — damage formula and stat mapping:
```python
DOMAIN_TO_STAT = {
    "subterfuge": "agility",
    "diplomacy": "presence",
}
# raw = ability_base * (1 + primary_stat*0.02 + secondary_stat*0.01)
```

From world/status_effects.py — available effects:
```python
STACKABLE_EFFECTS = {"poison", "bleed", "burn", "weaken", "drain"}
NON_STACKABLE_EFFECTS = {"slow", "root", "blind", "stun", "charm", "haste", "wet"}
```

From world/guild_engine.py — Subterfuge-primary subclasses:
- grimwarden (subterfuge+combat): Brutal assassin, Focus from ambush, cooldown reset on stealth re-entry
- hollowstep (subterfuge+naturalism): Wilderness ghost, outdoor stealth, terrain traps
- veilreader (subterfuge+resonance): Reads magical signatures, enemy ability telegraph
- nullshadow (subterfuge+arcana): Magic from stealth without breaking Vanish
- tally_agent (subterfuge+diplomacy): Info warfare, Network dimension, Standing manipulation
- blackthorn (subterfuge+alchemy): Classic poisoner, Vanish-applied poison, highest single-target poison ceiling
- shadecommand (subterfuge+tactics): Special ops, group stealth, disable enemy tactical advantages
- lockjaw (subterfuge+engineering): Trap-setting master, mechanical devices mid-combat
- hollowseen (subterfuge+remnance): Impossible awareness, lore fragment discovery rate

From world/guild_engine.py — Diplomacy-primary subclasses:
- civicguard (diplomacy+combat): Diplomat with teeth, intimidation scales with combat record
- shadowbroker (diplomacy+subterfuge): Info networks, double Standing gains
- wayfinder (diplomacy+naturalism): Empathy-based, Bond dimension bonuses
- spiritvoice (diplomacy+resonance): Old magic amplifies social power, Presence scales off Resonance
- highcourt (diplomacy+arcana): Social-magical abilities, passive NPC disposition
- silkpoison (diplomacy+alchemy): Subtle threat, poison through social encounters
- bannerspeaker (diplomacy+tactics): Morale at scale, military faction Standing
- dealwright (diplomacy+engineering): Crafted obligations, gifting mechanics
- truthwarden (diplomacy+remnance): Hidden faction access, forbidden knowledge
</interfaces>

<vault_refs>
MANDATORY — Read these vault files before authoring abilities:
- C:\Obsidian\brain\Soravelon\soravelon-guilds.md — Guild of Veilcraft and Guild of Accord sections
- C:\Obsidian\brain\Soravelon\soravelon-abilities.md — Focus (window-based) resource, Influence resource
- C:\Obsidian\brain\Soravelon\soravelon-fingerprints.md — Subterfuge (READ) and Diplomacy (LEVERAGE) fingerprints
</vault_refs>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Author 66 Subterfuge + Diplomacy ability definitions</name>
  <files>world/ability_registry.py</files>
  <action>
Read the three vault docs listed in vault_refs to absorb domain identity, fingerprint verbs, subclass hooks, and resource mechanics.

Then author abilities in world/ability_registry.py by replacing existing subterfuge/diplomacy stubs and adding new entries to the ABILITIES dict.

**Subterfuge domain pool (15 abilities, resource_type="focus"):**
- Tier 1 (4 abilities): Reads, opening strikes, debuffs. Per D-17: fingerprint verb is "Read" -- names evoke observation and timing (Expose, Probe, Shadow Strike, etc.)
- Tier 2 (4 abilities): Core combo abilities. Mix of damage and debuff. Abilities that reward timing within guard windows.
- Tier 3 (4 abilities): Advanced debuffs, chain abilities. blind, weaken applications.
- Tier 4 (3 abilities): Domain capstones. Devastating chain payoffs, guaranteed debuff applications.
- Per D-09: Subterfuge differentiates via information asymmetry, debuff stacking, and timing windows. Focus is window-based, not a pool -- abilities describe what happens on correct vs missed timing.
- Per D-08: Subterfuge is physical domain. charge_turns=0 for nearly all abilities (instant strikes).
- Per D-12: Room flags written: "shadow_marked", "exposed", "scouted"

**Diplomacy domain pool (15 abilities, resource_type="influence"):**
- Tier 1 (4 abilities): Social leverage, basic debuffs on enemies. Per D-17: fingerprint verb is "Leverage" -- names evoke persuasion and authority (Compel, Decree, Appeal, etc.)
- Tier 2 (4 abilities): Core social combat. Mix of social, debuff, and buff effect_types.
- Tier 3 (4 abilities): Advanced manipulation. Charm, weaken applications. Group buffs.
- Tier 4 (3 abilities): Domain capstones. Powerful social effects, morale manipulation.
- Per D-11: Diplomacy is solo-viable with group bonus. Solo abilities work independently; group abilities scale with party. Presence is the primary scaling stat.
- Per D-08: Diplomacy is NOT a caster domain. charge_turns=0 for most (spoken commands).
- Per D-12: Room flags written: "intimidated", "inspired", "ordered"

**Subterfuge-primary subclass signatures (18 abilities = 9 subclasses x 2):**
Use each subclass's hook:
- grimwarden: T3=ambush strike (massive damage from stealth), T4=death from shadows (guaranteed kill threshold on low-HP targets)
- hollowstep: T3=terrain trap (root+damage), T4=wilderness ghost (sustained outdoor stealth + evasion buff)
- veilreader: T3=read intent (reveal enemy next ability), T4=precognition field (group dodge bonus)
- nullshadow: T3=shadow spell (damage from stealth, no break), T4=void cloak (sustained magical stealth, abilities don't break it)
- tally_agent: T3=intelligence leak (debuff from info), T4=double agent (redirect enemy buff to allies)
- blackthorn: T3=concentrated venom (high poison from stealth), T4=lethal dose (highest single-target poison ceiling)
- shadecommand: T3=tactical shadow (group stealth 1 round), T4=black operation (group stealth + ambush bonus + disable enemy buffs)
- lockjaw: T3=mechanical trap (damage+root device), T4=killbox (deploy multiple traps, compound_trigger on entry)
- hollowseen: T3=echo sight (reveal hidden enemies + room flags), T4=impossible awareness (preemptive dodge + counter for N rounds)

**Diplomacy-primary subclass signatures (18 abilities = 9 subclasses x 2):**
- civicguard: T3=iron diplomacy (intimidate debuff, strength scaling), T4=violent persuasion (damage + charm, unique hybrid)
- shadowbroker: T3=information trade (buff from intel), T4=network collapse (massive debuff using accumulated Standing)
- wayfinder: T3=empathic bond (heal+buff ally), T4=heart of the wild (group heal + Bond dimension bonus)
- spiritvoice: T3=resonant word (debuff amplified by resonance), T4=voice of ages (AoE charm, resonance+presence scaling)
- highcourt: T3=enchant word (magical charm), T4=sovereign presence (passive AoE debuff aura, sustained)
- silkpoison: T3=poisoned word (poison through social), T4=fatal courtesy (delayed massive poison, undetectable)
- bannerspeaker: T3=rallying banner (group buff, scales with party), T4=morale surge (group haste + damage buff)
- dealwright: T3=contractual obligation (debuff that strengthens on target action), T4=binding deal (compound_trigger, enemy constrained)
- truthwarden: T3=forbidden knowledge (unique debuff from lore), T4=truth revealed (massive debuff + damage, echoes scaling)

Per D-06: resource_cost matches effect type impact. Damage=cheap (10-20), CC=moderate (20-35), compound=expensive (35-60).
Per D-14: Tier 4 power is VARIED -- Blackthorn T4 is raw poison damage, Tally Agent T4 is a sideways mechanic.

**Implementation notes:**
- Remove existing subterfuge/diplomacy stubs (shadow_read, diplomatic_leverage) and replace with full entries
- Keep non-subterfuge/non-diplomacy stubs untouched
- The DOMAIN_ABILITIES and SUBCLASS_SIGNATURES derived lookups rebuild automatically
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "
from world.ability_registry import ABILITIES, DOMAIN_ABILITIES, SUBCLASS_SIGNATURES
sub_pool = DOMAIN_ABILITIES.get('subterfuge', {})
sub_count = sum(len(v) for v in sub_pool.values())
assert sub_count == 15, f'Subterfuge pool: {sub_count} != 15'
dip_pool = DOMAIN_ABILITIES.get('diplomacy', {})
dip_count = sum(len(v) for v in dip_pool.values())
assert dip_count == 15, f'Diplomacy pool: {dip_count} != 15'
sub_subs = ['grimwarden','hollowstep','veilreader','nullshadow','tally_agent','blackthorn','shadecommand','lockjaw','hollowseen']
for sc in sub_subs:
    assert sc in SUBCLASS_SIGNATURES, f'Missing sigs for {sc}'
    assert len(SUBCLASS_SIGNATURES[sc]) == 2, f'{sc} has {len(SUBCLASS_SIGNATURES[sc])} sigs, expected 2'
dip_subs = ['civicguard','shadowbroker','wayfinder','spiritvoice','highcourt','silkpoison','bannerspeaker','dealwright','truthwarden']
for sc in dip_subs:
    assert sc in SUBCLASS_SIGNATURES, f'Missing sigs for {sc}'
    assert len(SUBCLASS_SIGNATURES[sc]) == 2, f'{sc} has {len(SUBCLASS_SIGNATURES[sc])} sigs, expected 2'
for aid, a in ABILITIES.items():
    if a['domain'] in ('subterfuge', 'diplomacy'):
        assert '[STUB' not in a['description'], f'{aid} still has stub description'
print('PASS: 66 subterfuge+diplomacy abilities validated')
"</automated>
  </verify>
  <done>
    - 15 Subterfuge pool abilities exist with concrete values across tiers 1-4
    - 15 Diplomacy pool abilities exist with concrete values across tiers 1-4
    - 18 Subterfuge-primary subclass signatures exist (2 per subclass)
    - 18 Diplomacy-primary subclass signatures exist (2 per subclass)
    - No [STUB] descriptions remain for subterfuge or diplomacy domains
  </done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <name>Task 2: User review of ability definitions</name>
  <action>User reviews ability definitions for balance, distinctiveness, and lore fidelity.</action>
  <what-built>66 Subterfuge + Diplomacy ability definitions authored in ability_registry.py</what-built>
  <how-to-verify>
    1. Review Subterfuge pool abilities -- do they reward timing and patience (Read fingerprint)?
    2. Review Diplomacy pool abilities -- are they solo-viable with group scaling (per D-11)?
    3. Review subclass signatures -- does Blackthorn (poison from stealth) feel distinct from Grimwarden (brutal ambush)?
    4. Check that Diplomacy abilities scale off presence stat
    5. Mark any abilities needing revision
  </how-to-verify>
  <resume-signal>Type "approved" or describe specific abilities to revise</resume-signal>
</task>

</tasks>

<verification>
- All subterfuge abilities use resource_type="focus"
- All diplomacy abilities use resource_type="influence"
- Every subclass_id matches a key in guild_engine.SUBCLASSES
- No duplicate ability_id values
</verification>

<success_criteria>
- 30 domain pool abilities authored (15 subterfuge + 15 diplomacy) with no stubs
- 36 subclass signatures authored with no stubs
- User has reviewed and approved the ability tables
</success_criteria>

<output>
After completion, create `.planning/phases/05b-ability-content-authoring/05b-02-SUMMARY.md`
</output>
