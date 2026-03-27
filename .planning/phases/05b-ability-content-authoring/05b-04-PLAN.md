---
phase: 05b-ability-content-authoring
plan: 04
type: execute
wave: 1
depends_on: []
files_modified: [world/ability_registry.py]
autonomous: false
requirements: [ABL-04]

must_haves:
  truths:
    - "Naturalism domain has 15 pool abilities (tiers 1-4) with concrete values"
    - "Alchemy domain has 15 pool abilities (tiers 1-4) with concrete values"
    - "All 9 Naturalism-primary subclasses have 2 signature abilities each (Tier 3 + Tier 4)"
    - "All 9 Alchemy-primary subclasses have 2 signature abilities each (Tier 3 + Tier 4)"
    - "Naturalism abilities use balance resource; Alchemy abilities use reagents resource"
    - "Rotweald signatures feel distinct from Mireweald signatures despite shared domains"
  artifacts:
    - path: "world/ability_registry.py"
      provides: "66 ability entries for naturalism + alchemy domains"
      contains: "wild_mend"
  key_links:
    - from: "world/ability_registry.py"
      to: "world/guild_engine.py SUBCLASSES"
      via: "subclass_id field matches SUBCLASSES keys"
      pattern: "subclass_id.*thornfist|venomfang"
---

<objective>
Author all 66 ability definitions for the Naturalism + Alchemy domain pair: 15 Naturalism pool abilities, 15 Alchemy pool abilities, 18 Naturalism-primary subclass signatures, and 18 Alchemy-primary subclass signatures.

Purpose: Naturalism (Calibrate/Balance) and Alchemy (Prepare/Reagents) are the nature and chemical domains. Both lean into DoTs and status effects but through radically different resource models -- Balance is a spectrum (Feral vs Calm), Reagents are pre-crafted consumables. Authoring together ensures Rotweald (Naturalism+Alchemy) and Mireweald (Alchemy+Naturalism) feel distinct despite shared domains.

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
    "naturalism": "resonance",
    "alchemy": "acuity",
}
```

From world/status_effects.py — DoT-relevant effects:
```python
STACKABLE_EFFECTS = {
    "poison": {"max_stacks": 5, "base_damage": 8, "diminishing": [8, 5, 3, 2, 1]},
    "bleed": {"max_stacks": 4, "base_damage": 6, "diminishing": [6, 4, 3, 2]},
    "burn": {"max_stacks": 4, "base_damage": 7, "diminishing": [7, 5, 3, 2]},
    "weaken": {"max_stacks": 3, "reduction_per_stack": 0.08},
    "drain": {"max_stacks": 2, "drain_per_stack": 5},
}
COMPOUND_MATRIX keys: (poison,slow)=venom_lag, (weaken,poison)=corruption, (slow,root)=petrify, (burn,wet)=steam
```

From world/guild_engine.py — Naturalism-primary subclasses:
- thornfist (naturalism+combat): Shapeshift-adjacent, physical strikes apply nature DoTs
- rootstalker (naturalism+subterfuge): Outdoor Vanish no cooldown, ambush from natural cover
- cantera (naturalism+resonance): Nature via old magic, node attunement accelerates in nature zones
- stormcaller (naturalism+arcana): Elemental forces, rain/lightning/wind, wet+charged room flags
- greentongue (naturalism+diplomacy): Speaks for nature, Druid/Warden Standing growth
- rotweald (naturalism+alchemy): Dark nature, decay/rot/toxic growth
- wildcommand (naturalism+tactics): Commands animals as tactical force, beast companion scripting
- growthwright (naturalism+engineering): Grows living structures, organic construction
- deeproot (naturalism+remnance): World-memory in old growth, dragon-adjacent nature

From world/guild_engine.py — Alchemy-primary subclasses:
- venomfang (alchemy+combat): Highest melee poison rate, Bleed+Poison simultaneously
- nightshade (alchemy+subterfuge): Vanish-applied poison, delayed onset toxins
- mireweald (alchemy+naturalism): Decay-focused nature, terrain poisoning
- voidbrewer (alchemy+resonance): Compounds interact with old magic, write/read room flags
- fumecaster (alchemy+arcana): Spell-delivered poisons, range on melee-only effects
- sweetpoison (alchemy+diplomacy): Charming poisoner, social access as delivery
- plaguecommand (alchemy+tactics): Tactical toxicology, area-denial poisons
- fumewright (alchemy+engineering): Gas traps, chemical payload devices
- firstblight (alchemy+remnance): Ancient poison, dragon-adjacent toxicology
</interfaces>

<vault_refs>
MANDATORY — Read these vault files before authoring abilities:
- C:\Obsidian\brain\Soravelon\soravelon-guilds.md — Guild of Verdance and Guild of Thornwork sections
- C:\Obsidian\brain\Soravelon\soravelon-abilities.md — Balance (spectrum) resource, Reagents (consumable stock) resource
- C:\Obsidian\brain\Soravelon\soravelon-fingerprints.md — Naturalism (CALIBRATE) and Alchemy (PREPARE) fingerprints
</vault_refs>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Author 66 Naturalism + Alchemy ability definitions</name>
  <files>world/ability_registry.py</files>
  <action>
Read the three vault docs listed in vault_refs. Pay special attention to the Naturalism Balance spectrum (Feral vs Calm) and Alchemy Reagent consumable model.

**Naturalism domain pool (15 abilities, resource_type="balance"):**
- Tier 1 (4 abilities): Basic nature effects. Per D-17: fingerprint verb is "Calibrate" -- names evoke duality and nature (Wild Mend, Thorn Lash, Nature's Ward, Feral Strike).
- Tier 2 (4 abilities): Core spectrum management. Some push Feral (offensive), some push Calm (defensive/healing). Description should note which direction the ability pushes.
- Tier 3 (4 abilities): Advanced nature. DoTs (poison, bleed through nature), heals, compound effects.
- Tier 4 (3 abilities): Domain capstones. Extreme spectrum abilities or powerful neutral-only effects.
- CRITICAL: Balance is a SPECTRUM, not a pool. Abilities should describe whether they push Feral or Calm. Include this in the description text: "Pushes toward Feral" or "Pushes toward Calm" or "Requires neutral Balance."
- Per D-08: Naturalism is NOT a heavy caster domain. Mostly instant (charge_turns=0), occasional charge.
- Per D-10: Naturalism elements are poison and nature.
- Per D-12: Room flags written: "fading_life", "living_wood", "overgrown", "rotting"

**Alchemy domain pool (15 abilities, resource_type="reagents"):**
- Tier 1 (4 abilities): Basic compounds. Per D-17: fingerprint verb is "Prepare" -- names evoke preparation and chemical effects (Reagent Toss, Acid Flask, Smoke Screen, etc.)
- Tier 2 (4 abilities): Core alchemy. DoTs (poison, burn), debuffs. Reagent costs reflect consumable nature.
- Tier 3 (4 abilities): Advanced compounds. Compound_trigger effects, multi-status applications.
- Tier 4 (3 abilities): Domain capstones. Devastating mixtures, massive DoT ceilings.
- CRITICAL: Reagents are PRE-CRAFTED CONSUMABLES. Costs represent actual stock depletion. Running out mid-fight is a design-intended failure state. Costs should feel finite: T1 costs 5-10, T2 costs 10-20, T3 costs 15-30, T4 costs 25-50.
- Per D-08: Alchemy is NOT a caster domain. Mostly instant (tossing compounds). Some charge_turns=1 for complex mixtures.
- Per D-10: Alchemy elements are poison and fire (chemical).
- Per D-12: Room flags written: "toxic_air", "poisoned_air", "caustic", "burning"

**Naturalism-primary subclass signatures (18 abilities = 9 subclasses x 2):**
- thornfist: T3=nature fist (physical+nature DoT), T4=primal shift (temporary transformation, massive stat buff+nature damage)
- rootstalker: T3=vine ambush (stealth+root from nature), T4=one with the wilds (sustained outdoor stealth+evasion+nature DoT aura)
- cantera: T3=ancient grove (heal+buff from node energy), T4=forest memory (massive heal+nature buff, resonance-amplified)
- stormcaller: T3=lightning strike (damage+wet+charged flag), T4=storm call (massive AoE, charge_turns=2, burn+wet+charged)
- greentongue: T3=nature's voice (social debuff+nature theme), T4=forest decree (AoE charm on beasts+nature-aligned, presence scaling)
- rotweald: T3=rot cloud (AoE poison+bleed), T4=consuming decay (sustained area DoT zone, poison+weaken)
- wildcommand: T3=beast rush (summon beast attack), T4=pack alpha (sustained beast companion + tactical buffs)
- growthwright: T3=living barricade (damage reduction structure), T4=grove fortress (sustained living construction, compound_trigger)
- deeproot: T3=deep memory (buff from ancient nature), T4=worldroot pulse (massive heal+buff, ancient nature power)

**Alchemy-primary subclass signatures (18 abilities = 9 subclasses x 2):**
- venomfang: T3=toxic bite (melee+bleed+poison), T4=apex predator (self-buff, all attacks apply double poison stacks)
- nightshade: T3=silent toxin (stealth poison application), T4=midnight bloom (delayed massive poison, triggers after 3 rounds)
- mireweald: T3=swamp rot (area poison+slow), T4=mire zone (sustained toxic terrain, damage+slow to all enemies)
- voidbrewer: T3=resonant compound (poison+resonance flag interaction), T4=old world brew (compound_trigger, room flag amplified poison)
- fumecaster: T3=poison bolt (ranged poison delivery), T4=noxious storm (AoE ranged poison+burn, charge_turns=1)
- sweetpoison: T3=honeyed words (social+poison), T4=killing kindness (charm+delayed lethal poison)
- plaguecommand: T3=gas deployment (area poison+weaken), T4=scorched earth (massive area denial, poison+burn+slow zone)
- fumewright: T3=gas trap (placed device, poison on trigger), T4=chemical engine (sustained device, compound_trigger effects)
- firstblight: T3=ancient venom (unique poison, higher ceiling), T4=dragon blight (massive unique DoT, scales with echoes)

Per D-06: Reagent costs should feel finite. Naturalism Balance costs are not "spending" but "shifting."

**Implementation notes:**
- Remove existing naturalism/alchemy stubs (wild_mend, reagent_toss, venom_coat) and replace
- Keep non-naturalism/non-alchemy stubs untouched
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "
from world.ability_registry import ABILITIES, DOMAIN_ABILITIES, SUBCLASS_SIGNATURES
nat_pool = DOMAIN_ABILITIES.get('naturalism', {})
nat_count = sum(len(v) for v in nat_pool.values())
assert nat_count == 15, f'Naturalism pool: {nat_count} != 15'
alc_pool = DOMAIN_ABILITIES.get('alchemy', {})
alc_count = sum(len(v) for v in alc_pool.values())
assert alc_count == 15, f'Alchemy pool: {alc_count} != 15'
nat_subs = ['thornfist','rootstalker','cantera','stormcaller','greentongue','rotweald','wildcommand','growthwright','deeproot']
for sc in nat_subs:
    assert sc in SUBCLASS_SIGNATURES, f'Missing sigs for {sc}'
    assert len(SUBCLASS_SIGNATURES[sc]) == 2, f'{sc} has {len(SUBCLASS_SIGNATURES[sc])} sigs, expected 2'
alc_subs = ['venomfang','nightshade','mireweald','voidbrewer','fumecaster','sweetpoison','plaguecommand','fumewright','firstblight']
for sc in alc_subs:
    assert sc in SUBCLASS_SIGNATURES, f'Missing sigs for {sc}'
    assert len(SUBCLASS_SIGNATURES[sc]) == 2, f'{sc} has {len(SUBCLASS_SIGNATURES[sc])} sigs, expected 2'
for aid, a in ABILITIES.items():
    if a['domain'] in ('naturalism', 'alchemy'):
        assert '[STUB' not in a['description'], f'{aid} still has stub description'
print('PASS: 66 naturalism+alchemy abilities validated')
"</automated>
  </verify>
  <done>
    - 15 Naturalism pool abilities exist with Balance spectrum descriptions
    - 15 Alchemy pool abilities exist with finite Reagent costs
    - 18 Naturalism-primary subclass signatures exist (2 per subclass)
    - 18 Alchemy-primary subclass signatures exist (2 per subclass)
    - No [STUB] descriptions remain for naturalism or alchemy domains
  </done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <name>Task 2: User review of ability definitions</name>
  <action>User reviews ability definitions for balance, distinctiveness, and lore fidelity.</action>
  <what-built>66 Naturalism + Alchemy ability definitions authored in ability_registry.py</what-built>
  <how-to-verify>
    1. Review Naturalism pool -- do abilities clearly indicate Feral/Calm spectrum push?
    2. Review Alchemy pool -- do Reagent costs feel finite and meaningful?
    3. Check Rotweald (Naturalism+Alchemy) vs Mireweald (Alchemy+Naturalism) signatures -- do they feel distinct?
    4. Verify DoT-heavy abilities reference correct status effects from status_effects.py
    5. Mark any abilities needing revision
  </how-to-verify>
  <resume-signal>Type "approved" or describe specific abilities to revise</resume-signal>
</task>

</tasks>

<verification>
- All naturalism abilities use resource_type="balance"
- All alchemy abilities use resource_type="reagents"
- Naturalism descriptions mention Feral/Calm direction where applicable
- Alchemy costs reflect consumable finite stock
</verification>

<success_criteria>
- 30 domain pool abilities authored with no stubs
- 36 subclass signatures authored with no stubs
- User has reviewed and approved
</success_criteria>

<output>
After completion, create `.planning/phases/05b-ability-content-authoring/05b-04-SUMMARY.md`
</output>
