---
phase: 05b-ability-content-authoring
plan: 05
type: execute
wave: 1
depends_on: []
files_modified: [world/ability_registry.py]
autonomous: false
requirements: [ABL-04]

must_haves:
  truths:
    - "Engineering domain has 15 pool abilities (tiers 1-4) with concrete values"
    - "Remnance domain has 15 pool abilities (tiers 1-4) with concrete values"
    - "All 9 Engineering-primary subclasses have 2 signature abilities each (Tier 3 + Tier 4)"
    - "All 9 Remnance-primary subclasses have 2 signature abilities each (Tier 3 + Tier 4)"
    - "Engineering abilities use components resource; Remnance abilities use echoes resource"
    - "Bucketborn signatures reflect the accidental base-8 construction lore"
  artifacts:
    - path: "world/ability_registry.py"
      provides: "66 ability entries for engineering + remnance domains"
      contains: "deploy_turret"
  key_links:
    - from: "world/ability_registry.py"
      to: "world/guild_engine.py SUBCLASSES"
      via: "subclass_id field matches SUBCLASSES keys"
      pattern: "subclass_id.*ironsmith|sealbreaker"
---

<objective>
Author all 66 ability definitions for the Engineering + Remnance domain pair: 15 Engineering pool abilities, 15 Remnance pool abilities, 18 Engineering-primary subclass signatures, and 18 Remnance-primary subclass signatures.

Purpose: Engineering (Construct/Components) and Remnance (Excavate/Echoes) are the construction and forbidden knowledge domains. Engineering is unique because its identity centers on a mechanical companion (for Engineering-primary subclasses). Remnance is the hidden domain -- intellectual curiosity as combat power. Authoring together ensures Bucketborn (Engineering+Remnance) and Dragonwright (Remnance+Engineering) reflect their lore connections.

Output: 66 new ABILITIES dict entries in world/ability_registry.py.
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

From world/combat_engine.py — stat mapping:
```python
DOMAIN_TO_STAT = {
    "engineering": "acuity",
    "remnance": "mana",
}
```

From world/guild_engine.py — Engineering-primary subclasses:
- ironsmith (engineering+combat): Most combat-capable companion chassis, advanced weaponry
- gearhand (engineering+subterfuge): Scout companion, backstab capability, lock interface
- growsmith (engineering+naturalism): Living wood companion, regenerates HP, bark armor tank
- runewright (engineering+resonance): Rune-slotted companion, highest versatility
- sparkshaper (engineering+arcana): Magical device companion, enchanted components
- dealsmith (engineering+diplomacy): Consortium companion, economic applications
- siegewright (engineering+tactics): Heavy construct, cover/chokepoints, group defensive
- fumehand (engineering+alchemy): Chemical delivery companion, Enhanced Fuel specialist
- bucketborn (engineering+remnance): Accidentally correct base-8, unpredictable, named for Bucket

From world/guild_engine.py — Remnance-primary subclasses:
- dragonkin (remnance+combat): Body changed by old power, ancient physical enhancements
- truthshadow (remnance+subterfuge): Knows things they shouldn't, deepest info access
- worldroot (remnance+naturalism): Connected to world's actual foundation, dragon lore through nature
- sealbreaker (remnance+resonance): Most dangerous subclass, actively breaking dragon curse
- firstform (remnance+arcana): Pre-school spellforms, dragon-origin spells
- ancientvoice (remnance+diplomacy): Authority of true history, political leverage from forbidden knowledge
- rootpoison (remnance+alchemy): Dragon-origin alchemy, not learned alchemy
- firstblade (remnance+tactics): Pre-curse combat doctrine, ancient tactical abilities
- dragonwright (remnance+engineering): Dragon-made construction knowledge fragments
</interfaces>

<vault_refs>
MANDATORY — Read these vault files before authoring abilities:
- C:\Obsidian\brain\Soravelon\soravelon-guilds.md — Guild of Forge and Guild of Vaelborn sections
- C:\Obsidian\brain\Soravelon\soravelon-abilities.md — Components (consumable stock) resource, Echoes (investigation bonus) resource
- C:\Obsidian\brain\Soravelon\soravelon-fingerprints.md — Engineering (CONSTRUCT) and Remnance (EXCAVATE) fingerprints, companion chassis details
</vault_refs>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Author 66 Engineering + Remnance ability definitions</name>
  <files>world/ability_registry.py</files>
  <action>
Read the three vault docs listed in vault_refs. Pay special attention to Engineering's companion-centric identity and the three fuel tiers (Standard, Enhanced, Overcharge), and Remnance's investigation bonus mechanic.

**Engineering domain pool (15 abilities, resource_type="components"):**
- Tier 1 (4 abilities): Basic constructions and devices. Per D-17: fingerprint verb is "Construct" -- names evoke building and deploying (Deploy, Assemble, Construct, Repair).
- Tier 2 (4 abilities): Core engineering. Companion commands, device deployment. Mix of compound_trigger, damage, buff.
- Tier 3 (4 abilities): Advanced devices. Enhanced Fuel abilities, complex constructs.
- Tier 4 (3 abilities): Domain capstones. Overcharge abilities, masterwork constructions.
- CRITICAL: Engineering-primary abilities often reference the mechanical companion. Pool abilities should include companion commands (attack, defend, intercept) alongside device/trap abilities. The companion IS the Engineering identity for Engineering-primary characters.
- Per D-08: Engineering has some charge_turns for complex deployments. charge_turns=1 for device setup.
- Components are PRE-CRAFTED CONSUMABLES like Reagents. Costs: T1=10-15, T2=15-25, T3=20-35, T4=30-50.
- Per D-12: Room flags written: "fortified", "trapped", "mechanized"

**Remnance domain pool (15 abilities, resource_type="echoes"):**
- Tier 1 (4 abilities): Basic excavation, probing. Per D-17: fingerprint verb is "Excavate" -- names evoke digging, remembering, uncovering (Echo Probe, Memory Strike, Ancient Recall, etc.)
- Tier 2 (4 abilities): Core remnance. Mix of damage, utility, debuff. Abilities that reward investigation (higher starting Echoes = stronger effects).
- Tier 3 (4 abilities): Advanced ancient knowledge. Unique debuffs, powerful damage.
- Tier 4 (3 abilities): Domain capstones. Pre-curse power expressions.
- CRITICAL: Remnance is the HIDDEN domain. Flavor text should suggest power from ancient knowledge, not traditional magic. Abilities are described as "remembering" how things worked, not "casting spells."
- Per D-08: Remnance IS a caster-adjacent domain. charge_turns=1 for some abilities (channeling memories).
- Echoes build from abilities AND investigation bonus (+15 per lore fragment, +10 per ancient site, persists 3 encounters, stacks to 40 starting).
- Per D-12: Room flags written: "ancient_presence", "void_touched", "corrupted_death", "excavated"

**Engineering-primary subclass signatures (18 abilities = 9 subclasses x 2):**
Each Engineering-primary subclass has a different companion chassis. Signatures should reflect the chassis identity:
- ironsmith: T3=combat chassis assault (companion burst attack, strength scaling), T4=ironforged protocol (companion enters overdrive, sustained enhanced attacks)
- gearhand: T3=scout strike (companion backstab from adjacent room), T4=ghost protocol (companion operates independently for N rounds, stealth+damage)
- growsmith: T3=bark shield (companion intercepts damage for ally), T4=living fortress (companion becomes immovable tank, massive damage reduction zone)
- runewright: T3=rune swap (change companion loadout mid-combat), T4=full rune activation (all rune slots fire simultaneously, massive compound_trigger)
- sparkshaper: T3=arcane payload (companion delivers magical damage), T4=overload device (companion self-destructs for massive AoE, charge_turns=1)
- dealsmith: T3=trade advantage (companion generates economic buff), T4=consortium protocol (companion provides sustained group resource generation)
- siegewright: T3=siege stance (companion creates chokepoint), T4=fortress protocol (companion becomes static fortress, massive group defense)
- fumehand: T3=chemical spray (companion delivers area DoT), T4=overcharge protocol (companion enters Overcharge, highest output + risk)
- bucketborn: T3=anomalous function (companion does something unpredictable but beneficial), T4=base-8 resonance (companion achieves impossible synchrony, unique ancient effect)

**Remnance-primary subclass signatures (18 abilities = 9 subclasses x 2):**
- dragonkin: T3=ancient body (physical enhancement buff), T4=dragonform (temporary transformation, massive physical stats)
- truthshadow: T3=hidden knowledge (reveal+debuff from forbidden info), T4=truth strike (damage that ignores all defenses, scales with lore)
- worldroot: T3=deep nature (heal from world-memory), T4=foundation pulse (massive nature+ancient hybrid, area heal+damage)
- sealbreaker: T3=seal probe (damage+resonance interaction), T4=curse break (the most dangerous ability -- massive damage + unique world-altering effect, charge_turns=2)
- firstform: T3=ancient spell (damage in pre-school form), T4=firstcasting (spell that predates all magic schools, unique effect)
- ancientvoice: T3=voice of the past (social+damage debuff), T4=decree of truth (AoE massive debuff, presence+echoes scaling)
- rootpoison: T3=dragon venom (unique ancient poison), T4=first toxin (poison that interacts with dragon curse, unique compound)
- firstblade: T3=ancient formation (group tactical buff from old knowledge), T4=forgotten war (tactical ability from pre-curse doctrine, compound_trigger)
- dragonwright: T3=ancient construct (temporary construct from dragon knowledge), T4=drake engine (summon ancient construct, charge_turns=2, compound_trigger)

Per D-06: Components and Echoes are both finite/buildable. Costs reflect their acquisition difficulty.
Per D-14: Bucketborn T4 should feel like something went wonderfully right by accident. Sealbreaker T4 should feel genuinely dangerous.

**Implementation notes:**
- Remove existing engineering/remnance stubs (deploy_turret, echo_probe) and replace
- Keep non-engineering/non-remnance stubs untouched
- Verify exact subclass_id keys from guild_engine.py SUBCLASSES dict
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "
from world.ability_registry import ABILITIES, DOMAIN_ABILITIES, SUBCLASS_SIGNATURES
eng_pool = DOMAIN_ABILITIES.get('engineering', {})
eng_count = sum(len(v) for v in eng_pool.values())
assert eng_count == 15, f'Engineering pool: {eng_count} != 15'
rem_pool = DOMAIN_ABILITIES.get('remnance', {})
rem_count = sum(len(v) for v in rem_pool.values())
assert rem_count == 15, f'Remnance pool: {rem_count} != 15'
eng_subs = ['ironsmith','gearhand','growsmith','sparkshaper','dealsmith','siegewright','fumehand','bucketborn']
for sc in eng_subs:
    assert sc in SUBCLASS_SIGNATURES, f'Missing sigs for {sc}'
    assert len(SUBCLASS_SIGNATURES[sc]) == 2, f'{sc} has {len(SUBCLASS_SIGNATURES[sc])} sigs, expected 2'
# Check runewright (Engineering+Resonance) -- verify exact key
from world.guild_engine import SUBCLASSES
eng_res_key = [k for k,v in SUBCLASSES.items() if v['primary_domain']=='engineering' and v['secondary_domain']=='resonance'][0]
assert eng_res_key in SUBCLASS_SIGNATURES, f'Missing sigs for {eng_res_key}'
rem_subs = ['dragonkin','truthshadow','worldroot','sealbreaker','firstform','ancientvoice','rootpoison','firstblade','dragonwright']
for sc in rem_subs:
    assert sc in SUBCLASS_SIGNATURES, f'Missing sigs for {sc}'
    assert len(SUBCLASS_SIGNATURES[sc]) == 2, f'{sc} has {len(SUBCLASS_SIGNATURES[sc])} sigs, expected 2'
for aid, a in ABILITIES.items():
    if a['domain'] in ('engineering', 'remnance'):
        assert '[STUB' not in a['description'], f'{aid} still has stub description'
print('PASS: 66 engineering+remnance abilities validated')
"</automated>
  </verify>
  <done>
    - 15 Engineering pool abilities exist with companion-centric design
    - 15 Remnance pool abilities exist with investigation-as-power theme
    - 18 Engineering-primary subclass signatures exist reflecting companion chassis
    - 18 Remnance-primary subclass signatures exist reflecting ancient knowledge
    - No [STUB] descriptions remain for engineering or remnance domains
  </done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <name>Task 2: User review of ability definitions</name>
  <action>User reviews ability definitions for balance, distinctiveness, and lore fidelity.</action>
  <what-built>66 Engineering + Remnance ability definitions authored in ability_registry.py</what-built>
  <how-to-verify>
    1. Review Engineering pool -- do abilities reference the companion meaningfully?
    2. Review Remnance pool -- does "knowledge as power" come through in the ability design?
    3. Check Bucketborn signatures -- do they feel like happy accidents?
    4. Check Sealbreaker T4 -- does it feel like the most dangerous ability in the game?
    5. Verify Engineering companion chassis specialization shows in subclass signatures
    6. Mark any abilities needing revision
  </how-to-verify>
  <resume-signal>Type "approved" or describe specific abilities to revise</resume-signal>
</task>

</tasks>

<verification>
- All engineering abilities use resource_type="components"
- All remnance abilities use resource_type="echoes"
- Engineering companion references are consistent
- Remnance flavor text avoids "spell" language (uses "remember", "excavate", "uncover")
</verification>

<success_criteria>
- 30 domain pool abilities authored with no stubs
- 36 subclass signatures authored with no stubs
- User has reviewed and approved
</success_criteria>

<output>
After completion, create `.planning/phases/05b-ability-content-authoring/05b-05-SUMMARY.md`
</output>
