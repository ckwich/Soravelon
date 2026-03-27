---
phase: 05b-ability-content-authoring
plan: 03
type: execute
wave: 1
depends_on: []
files_modified: [world/ability_registry.py]
autonomous: false
requirements: [ABL-04]

must_haves:
  truths:
    - "Arcana domain has 15 pool abilities (tiers 1-4) with concrete values"
    - "Resonance domain has 15 pool abilities (tiers 1-4) with concrete values"
    - "All 9 Arcana-primary subclasses have 2 signature abilities each (Tier 3 + Tier 4)"
    - "All 9 Resonance-primary subclasses have 2 signature abilities each (Tier 3 + Tier 4)"
    - "Arcana abilities use mana resource; Resonance abilities use resonance resource"
    - "Resonance abilities have attuned_variants populated for room flag interactions"
    - "Spellseeker signatures feel distinct from Sealwright signatures despite shared domains"
  artifacts:
    - path: "world/ability_registry.py"
      provides: "66 ability entries for arcana + resonance domains"
      contains: "arcane_bolt"
  key_links:
    - from: "world/ability_registry.py"
      to: "world/guild_engine.py SUBCLASSES"
      via: "subclass_id field matches SUBCLASSES keys"
      pattern: "subclass_id.*battlemage|sealwright"
---

<objective>
Author all 66 ability definitions for the Arcana + Resonance domain pair: 15 Arcana pool abilities, 15 Resonance pool abilities, 18 Arcana-primary subclass signatures, and 18 Resonance-primary subclass signatures.

Purpose: Arcana (Ration/Mana) and Resonance (Attune/Resonance) are the two magical domains with critically different resource models. Arcana manages across encounters (Mana pool depletes); Resonance manages within encounters (builder/spender with decay). Authoring together ensures they feel mechanically distinct despite both being "magic." Resonance abilities uniquely use the attuned_variants field for room flag interactions.

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
    "arcana": "mana",
    "resonance": "resonance",
}
```

Attuned variant schema (for Resonance abilities):
```python
# attuned_variants dict maps room_flag -> variant effect description
# Example from soravelon-fingerprints.md:
"attuned_variants": {
    "charged": {"extra_effect": "arc to second target for 50% damage", "extra_cost": 10},
    "resonant": {"extra_effect": "arc to ALL enemies for 30% damage", "extra_cost": 15},
    "fading_life": {"extra_effect": "apply Rootbound 2 rounds", "extra_cost": 10},
    "ancient_ground": {"extra_effect": "+25% damage", "extra_cost": 5},
}
```

From world/guild_engine.py — Arcana-primary subclasses:
- battlemage (arcana+combat): Mana-fueled physical strikes, Strength+Mana scaling
- mistveil (arcana+subterfuge): Magical invisibility, unique detection bypass
- stormweaver (arcana+naturalism): Elemental nature magic, area effects in natural zones
- spellseeker (arcana+resonance): Node study improves Mana and spellcasting
- enchantvoice (arcana+diplomacy): Words carry literal weight, social-magical hybrids
- fusewright (arcana+alchemy): Potion-powered spell amplification, compound triggers
- wardcaller (arcana+tactics): Magical area control, battlefield zone placement
- runewright_arcana (arcana+engineering): Magic encoded in objects, enchanted devices
- voidscribe (arcana+remnance): Pre-cursor spellforms, Circle of Wizards conflict

From world/guild_engine.py — Resonance-primary subclasses:
- runebreaker (resonance+combat): Physical strikes apply Resonance stacks + charged flag
- greymantle (resonance+subterfuge): Magical blind spots, attuned on shadow_marked/scouted
- thornweald (resonance+naturalism): Nature+old magic DoTs, attuned on fading_life/living_wood
- sealwright (resonance+arcana): Highest burst, attuned on charged/resonant
- lorekeeper (resonance+diplomacy): Lore fragments grant Standing, attuned on ancient_ground/ancient_presence
- corroder (resonance+alchemy): Old magic + chemical, attuned on poisoned_air/toxic_air
- nodecaller (resonance+tactics): Write resonant flag deliberately, attuned on fortified/resonant
- arcanist (resonance+engineering): Old infrastructure, attuned on ancient_presence
- sealreader (resonance+remnance): Uncomfortably close to truth, attuned on void_touched/corrupted_death
</interfaces>

<vault_refs>
MANDATORY — Read these vault files before authoring abilities:
- C:\Obsidian\brain\Soravelon\soravelon-guilds.md — Guild of the Arcane and Guild of Resonance sections
- C:\Obsidian\brain\Soravelon\soravelon-abilities.md — Mana resource, Resonance resource, Sense passive, attuned variants
- C:\Obsidian\brain\Soravelon\soravelon-fingerprints.md — Arcana (RATION) and Resonance (ATTUNE) fingerprints
</vault_refs>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Author 66 Arcana + Resonance ability definitions</name>
  <files>world/ability_registry.py</files>
  <action>
Read the three vault docs listed in vault_refs. Pay special attention to the Resonance fingerprint section which details the Sense passive and attuned variant mechanic in depth.

**Arcana domain pool (15 abilities, resource_type="mana"):**
- Tier 1 (4 abilities): Basic spells. Per D-17: fingerprint verb is "Ration" -- names evoke measured magical force (Arcane Bolt, Mana Surge, Frost Shard, etc.)
- Tier 2 (4 abilities): Core spellcasting. Mix of damage, buff, debuff. Moderate mana costs.
- Tier 3 (4 abilities): Advanced magic. burn, stun applications. Higher mana costs.
- Tier 4 (3 abilities): Domain capstones. Devastating spells, high mana costs.
- Per D-08: Arcana IS a caster domain. charge_turns=1 for many abilities (channeled spells). Some instant cast.
- Per D-10: Arcana elements are fire/ice/lightning primarily.
- Per D-12: Room flags written: "scorched", "frozen", "charged", "arcane_residue"
- Mana is a cross-encounter pool. Costs should feel meaningful -- spending 40 mana on a T3 spell matters when your pool is ~200.

**Resonance domain pool (15 abilities, resource_type="resonance"):**
- Tier 1 (4 abilities): Builders and basic effects. Per D-17: fingerprint verb is "Attune" -- names evoke listening, patterns, echoes.
- Tier 2 (4 abilities): Core attunement. Mix of builders and moderate spenders. Spenders require 60+ resonance resource.
- Tier 3 (4 abilities): Advanced attunement. Powerful spenders, attuned variants become critical.
- Tier 4 (3 abilities): Domain capstones. Full-resource spenders with devastating attuned variants.
- Per D-08: Resonance IS a caster domain. charge_turns=1 for some abilities.
- CRITICAL: Resonance abilities MUST have populated attuned_variants dicts. Each ability should have 2-4 room flag variants with extra_cost and extra_effect. Use the flags from fingerprints doc: charged, fading_life, resonant, ancient_ground, corrupted_death, void_touched, node_critical.
- Per D-12: Room flags written: "charged", "resonant", "disrupted"
- Builder abilities generate +15-20 resonance resource. Spenders cost 60-100.

**Arcana-primary subclass signatures (18 abilities = 9 subclasses x 2):**
- battlemage: T3=mana strike (melee damage scaling both strength+mana), T4=arcane warrior (self-buff, next N attacks are spell-enhanced)
- mistveil: T3=mist shroud (magical stealth, different from Vanish), T4=phantom form (sustained magical invisibility + spell casting)
- stormweaver: T3=chain lightning (multi-target, wet application), T4=tempest (massive AoE, charge_turns=2, burn+wet)
- spellseeker: T3=node tap (restore mana from resonance), T4=arcane resonance (massive damage, amplified by room resonance)
- enchantvoice: T3=binding word (charm + damage), T4=voice of command (AoE charm, presence+mana scaling)
- fusewright: T3=volatile mixture (damage+DoT+compound trigger), T4=transmutation burst (convert DoT stacks into burst damage)
- wardcaller: T3=ward zone (area damage reduction for allies), T4=arcane fortress (sustained area buff + enemy debuff zone)
- runewright_arcana: T3=rune trap (damage+debuff on trigger), T4=masterwork rune (permanent buff until dispelled, charge_turns=2)
- voidscribe: T3=void bolt (damage ignoring resistance), T4=firstform casting (unique ancient spell, massive damage + unique debuff)

NOTE: The subclass_id for Arcana+Engineering is "runewright" in guild_engine.py -- verify this before using. If guild_engine uses a different key, match it exactly.

**Resonance-primary subclass signatures (18 abilities = 9 subclasses x 2):**
ALL Resonance signatures MUST have attuned_variants populated matching their subclass's listed flags.
- runebreaker: T3=resonant strike (damage+resonance stacks, charged flag), T4=node burst (detonate all resonance stacks, massive AoE)
- greymantle: T3=shadow attunement (stealth+resonance build), T4=veil of silence (undetectable + debuff aura, shadow_marked variant)
- thornweald: T3=nature echo (DoT+heal, fading_life variant), T4=ancient growth (sustained AoE DoT+heal zone, living_wood variant)
- sealwright: T3=focused blast (high burst, charged variant), T4=seal break (highest single-target damage, resonant variant)
- lorekeeper: T3=ancient insight (group buff from lore), T4=lorewarden (sustained buff aura, ancient_ground/ancient_presence variants)
- corroder: T3=resonant acid (poison+resonance, toxic_air variant), T4=old corruption (massive DoT, poisoned_air variant)
- nodecaller: T3=node pulse (write resonant flag + damage), T4=node storm (sustained resonant zone + AoE damage each round)
- arcanist: T3=pattern read (reveal + buff from ancient_presence), T4=infrastructure tap (massive utility, ancient_presence variant)
- sealreader: T3=void touch (damage+unique debuff, void_touched variant), T4=truth unbound (most dangerous ability in game, corrupted_death variant)

Per D-06: Mana costs are higher than other resources (pool-based, not per-encounter). Resonance costs follow builder/spender pattern.
Per D-14: T4 variety -- Sealwright T4 is raw burst damage, Lorekeeper T4 is sustained group utility.

**Implementation notes:**
- Remove existing arcana/resonance stubs (arcane_bolt, pulse_attune, resonance_ward) and replace
- Keep non-arcana/non-resonance stubs untouched
- Verify the exact subclass_id keys from guild_engine.py SUBCLASSES dict before writing entries
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "
from world.ability_registry import ABILITIES, DOMAIN_ABILITIES, SUBCLASS_SIGNATURES
arc_pool = DOMAIN_ABILITIES.get('arcana', {})
arc_count = sum(len(v) for v in arc_pool.values())
assert arc_count == 15, f'Arcana pool: {arc_count} != 15'
res_pool = DOMAIN_ABILITIES.get('resonance', {})
res_count = sum(len(v) for v in res_pool.values())
assert res_count == 15, f'Resonance pool: {res_count} != 15'
arc_subs = ['battlemage','mistveil','stormweaver','spellseeker','enchantvoice','fusewright','wardcaller']
for sc in arc_subs:
    assert sc in SUBCLASS_SIGNATURES, f'Missing sigs for {sc}'
    assert len(SUBCLASS_SIGNATURES[sc]) == 2, f'{sc} has {len(SUBCLASS_SIGNATURES[sc])} sigs, expected 2'
# Check voidscribe and runewright (verify exact keys from guild_engine)
from world.guild_engine import SUBCLASSES
arc_eng_key = [k for k,v in SUBCLASSES.items() if v['primary_domain']=='arcana' and v['secondary_domain']=='engineering'][0]
arc_rem_key = [k for k,v in SUBCLASSES.items() if v['primary_domain']=='arcana' and v['secondary_domain']=='remnance'][0]
assert arc_eng_key in SUBCLASS_SIGNATURES, f'Missing sigs for {arc_eng_key}'
assert arc_rem_key in SUBCLASS_SIGNATURES, f'Missing sigs for {arc_rem_key}'
res_subs = ['runebreaker','greymantle','thornweald','sealwright','lorekeeper','corroder','nodecaller','arcanist','sealreader']
for sc in res_subs:
    assert sc in SUBCLASS_SIGNATURES, f'Missing sigs for {sc}'
    assert len(SUBCLASS_SIGNATURES[sc]) == 2, f'{sc} has {len(SUBCLASS_SIGNATURES[sc])} sigs, expected 2'
# Check resonance abilities have attuned_variants
for aid, a in ABILITIES.items():
    if a['domain'] == 'resonance' and a['subclass_id'] is not None:
        assert a['attuned_variants'], f'Resonance sig {aid} missing attuned_variants'
    if a['domain'] in ('arcana', 'resonance'):
        assert '[STUB' not in a['description'], f'{aid} still has stub description'
print('PASS: 66 arcana+resonance abilities validated')
"</automated>
  </verify>
  <done>
    - 15 Arcana pool abilities exist with concrete values across tiers 1-4
    - 15 Resonance pool abilities exist with concrete values across tiers 1-4, with attuned_variants
    - 18 Arcana-primary subclass signatures exist (2 per subclass)
    - 18 Resonance-primary subclass signatures exist (2 per subclass) with attuned_variants
    - No [STUB] descriptions remain for arcana or resonance domains
  </done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <name>Task 2: User review of ability definitions</name>
  <action>User reviews ability definitions for balance, distinctiveness, and lore fidelity.</action>
  <what-built>66 Arcana + Resonance ability definitions authored in ability_registry.py</what-built>
  <how-to-verify>
    1. Review Arcana pool -- do mana costs feel meaningful for cross-encounter rationing?
    2. Review Resonance pool -- do builder/spender dynamics work? Are attuned variants well-designed?
    3. Verify Arcana and Resonance FEEL different despite both being "magic" domains
    4. Review Resonance subclass signatures -- do attuned_variants match each subclass's listed flags?
    5. Check charge_turns distribution -- caster domains should have more charged abilities per D-08
    6. Mark any abilities needing revision
  </how-to-verify>
  <resume-signal>Type "approved" or describe specific abilities to revise</resume-signal>
</task>

</tasks>

<verification>
- All arcana abilities use resource_type="mana"
- All resonance abilities use resource_type="resonance"
- Resonance subclass signatures have non-empty attuned_variants
- Arcana abilities have more charge_turns>0 than physical domains
</verification>

<success_criteria>
- 30 domain pool abilities authored (15 arcana + 15 resonance) with no stubs
- 36 subclass signatures authored with no stubs
- Resonance attuned_variants populated for all resonance signatures
- User has reviewed and approved
</success_criteria>

<output>
After completion, create `.planning/phases/05b-ability-content-authoring/05b-03-SUMMARY.md`
</output>
