---
phase: 05b-ability-content-authoring
plan: 06
type: execute
wave: 2
depends_on: [05b-01, 05b-02, 05b-03, 05b-04, 05b-05]
files_modified: [world/ability_registry.py]
autonomous: true
requirements: [ABL-04]

must_haves:
  truths:
    - "ABILITIES dict contains exactly 330 entries (150 pool + 180 signatures)"
    - "All 10 domains have exactly 15 pool abilities each"
    - "All 90 subclasses have exactly 2 signature abilities each"
    - "Every ability has all 16 required fields with valid values"
    - "DOMAIN_ABILITIES returns correct tier breakdowns for every domain"
    - "SUBCLASS_SIGNATURES returns exactly 2 abilities for every subclass in guild_engine.SUBCLASSES"
    - "No duplicate ability_id values exist"
    - "Every resource_type matches the guild's resource_type from guild_engine.GUILDS"
  artifacts:
    - path: "world/ability_registry.py"
      provides: "Complete 330-ability registry"
      contains: "ABILITIES"
  key_links:
    - from: "world/ability_registry.py SUBCLASS_SIGNATURES"
      to: "world/guild_engine.py SUBCLASSES"
      via: "every subclass key has exactly 2 signatures"
      pattern: "SUBCLASS_SIGNATURES"
    - from: "world/ability_registry.py DOMAIN_ABILITIES"
      to: "world/guild_engine.py FINGERPRINTS"
      via: "every domain has 15 pool abilities across 4 tiers"
      pattern: "DOMAIN_ABILITIES"
---

<objective>
Validate the complete 330-ability registry for structural correctness, cross-reference integrity with guild_engine, and fix any issues found during the 5 content authoring plans.

Purpose: After 5 parallel content plans have written abilities independently, this plan merges them (if needed), validates structural integrity, and ensures the derived lookups (DOMAIN_ABILITIES, SUBCLASS_SIGNATURES) are correct for all 10 domains and 90 subclasses.

Output: A validated, structurally sound ability_registry.py with 330 entries.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/05b-ability-content-authoring/5b-CONTEXT.md

@world/ability_registry.py
@world/guild_engine.py
@world/combat_engine.py
@world/status_effects.py
@world/base_attributes.py

<interfaces>
From world/ability_registry.py:
```python
EFFECT_TYPES = ("damage", "dot", "buff", "debuff", "utility", "social", "tactical", "compound_trigger", "heal", "status")
ABILITY_TIERS = {1: 0, 2: 20, 3: 50, 4: 85}
```

From world/guild_engine.py:
```python
GUILDS  # 10 guilds, each with primary_domain and resource_type
SUBCLASSES  # 90 subclasses, each with primary_domain, secondary_domain, guild_id
FINGERPRINTS  # 10 domains, each with resource_type
```

From world/combat_engine.py:
```python
DOMAIN_TO_STAT  # maps domain -> base stat name
```

From world/base_attributes.py:
```python
STAT_NAMES = ("strength", "agility", "endurance", "mana", "acuity", "presence", "resonance")
```
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Validate and fix 330-ability registry</name>
  <files>world/ability_registry.py</files>
  <action>
Run comprehensive structural validation on the complete ABILITIES dict. Fix any issues found.

**Validation checks to perform (all automated via Python script):**

1. **Total count**: ABILITIES has exactly 330 entries.

2. **Per-domain pool counts**: For each of the 10 domains, DOMAIN_ABILITIES[domain] should have exactly 15 abilities distributed across tiers 1-4 (approximately 4/4/4/3 per tier).

3. **Per-subclass signature counts**: For each of the 90 subclass keys in guild_engine.SUBCLASSES, SUBCLASS_SIGNATURES[subclass_id] should contain exactly 2 entries (one Tier 3, one Tier 4).

4. **No duplicate ability_ids**: Every id field is unique across all 330 entries.

5. **Field completeness**: Every ability has all 16 required fields:
   id, name, domain, tier, resource_cost, resource_type, cooldown, charge_turns, effect_type, scaling_primary, scaling_secondary, application_chance, description, room_flag_written, attuned_variants, subclass_id

6. **Field type validation**:
   - tier in (1, 2, 3, 4)
   - effect_type in EFFECT_TYPES
   - resource_cost >= 0 (int)
   - cooldown >= 0 (int)
   - charge_turns >= 0 (int)
   - application_chance between 0.0 and 1.0
   - scaling_primary is a valid domain name (in ALL_DOMAINS from world_state)
   - scaling_secondary is None or a valid domain name
   - attuned_variants is a dict (may be empty)
   - subclass_id is None (pool) or a key in SUBCLASSES (signature)
   - id field matches the dict key

7. **Resource type consistency**: For pool abilities (subclass_id=None), resource_type must match the domain's resource_type from guild_engine.FINGERPRINTS[domain]["resource_type"]. For signature abilities, resource_type must match the guild's resource_type for the subclass's guild_id.

8. **Signature tier validation**: Signature abilities should be Tier 3 or Tier 4. Each subclass should have exactly one Tier 3 and one Tier 4 signature.

9. **No stub descriptions**: No ability description contains "[STUB".

10. **Scaling stat validation**: scaling_primary domain exists in combat_engine.DOMAIN_TO_STAT. scaling_secondary (if not None) also exists.

**If any validation fails:** Fix the issue directly in ability_registry.py. Common fixes:
- Missing subclass: add the 2 missing signature entries
- Wrong resource_type: correct to match guild/fingerprint
- Missing field: add with sensible default
- Duplicate id: rename one of the duplicates
- Wrong tier on signature: correct to 3 or 4

**After all fixes:** Re-run full validation to confirm PASS.

**Also clean up the del statement at module bottom**: The current `del _ability_id, _ability, _domain, _tier, _sc` may need updating if loop variable names changed. Wrap in try/except or use a different cleanup approach.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "
from world.ability_registry import ABILITIES, DOMAIN_ABILITIES, SUBCLASS_SIGNATURES, EFFECT_TYPES
from world.guild_engine import SUBCLASSES, GUILDS, FINGERPRINTS
from world.combat_engine import DOMAIN_TO_STAT
from world.base_attributes import STAT_NAMES

errors = []

# 1. Total count
if len(ABILITIES) != 330:
    errors.append(f'Total: {len(ABILITIES)} != 330')

# 2. Per-domain pool counts
for domain in FINGERPRINTS:
    pool = DOMAIN_ABILITIES.get(domain, {})
    count = sum(len(v) for v in pool.values())
    if count != 15:
        errors.append(f'{domain} pool: {count} != 15')

# 3. Per-subclass signature counts
for sc_id in SUBCLASSES:
    sigs = SUBCLASS_SIGNATURES.get(sc_id, [])
    if len(sigs) != 2:
        errors.append(f'{sc_id} sigs: {len(sigs)} != 2')

# 4. No duplicate ids
ids = [a['id'] for a in ABILITIES.values()]
dupes = [x for x in set(ids) if ids.count(x) > 1]
if dupes:
    errors.append(f'Duplicate ids: {dupes}')

# 5-6. Field completeness and type validation
REQUIRED = {'id','name','domain','tier','resource_cost','resource_type','cooldown','charge_turns','effect_type','scaling_primary','scaling_secondary','application_chance','description','room_flag_written','attuned_variants','subclass_id'}
for aid, a in ABILITIES.items():
    missing = REQUIRED - set(a.keys())
    if missing:
        errors.append(f'{aid} missing fields: {missing}')
    if a.get('tier') not in (1,2,3,4):
        errors.append(f'{aid} bad tier: {a.get(\"tier\")}')
    if a.get('effect_type') not in EFFECT_TYPES:
        errors.append(f'{aid} bad effect_type: {a.get(\"effect_type\")}')
    if not isinstance(a.get('application_chance', 0), (int, float)):
        errors.append(f'{aid} bad application_chance type')
    elif not (0.0 <= a.get('application_chance', 0) <= 1.0):
        errors.append(f'{aid} application_chance out of range')
    if a.get('id') != aid:
        errors.append(f'{aid} id mismatch: {a.get(\"id\")}')
    if '[STUB' in a.get('description', ''):
        errors.append(f'{aid} still has stub description')

# 7. Resource type consistency
for aid, a in ABILITIES.items():
    domain = a.get('domain')
    expected_rt = FINGERPRINTS.get(domain, {}).get('resource_type')
    if a.get('resource_type') != expected_rt:
        errors.append(f'{aid} resource_type {a[\"resource_type\"]} != expected {expected_rt}')

# 8. Signature tier validation
for sc_id in SUBCLASSES:
    sigs = SUBCLASS_SIGNATURES.get(sc_id, [])
    tiers = sorted([ABILITIES[s]['tier'] for s in sigs]) if len(sigs) == 2 else []
    if tiers and tiers != [3, 4]:
        errors.append(f'{sc_id} sig tiers {tiers} != [3, 4]')

if errors:
    for e in errors[:20]:
        print(f'FAIL: {e}')
    print(f'Total errors: {len(errors)}')
    raise SystemExit(1)
else:
    print('PASS: All 330 abilities validated — structural integrity confirmed')
    # Summary stats
    pool_count = sum(1 for a in ABILITIES.values() if a['subclass_id'] is None)
    sig_count = sum(1 for a in ABILITIES.values() if a['subclass_id'] is not None)
    print(f'  Pool abilities: {pool_count} (expected 150)')
    print(f'  Signature abilities: {sig_count} (expected 180)')
    print(f'  Domains covered: {len(DOMAIN_ABILITIES)}')
    print(f'  Subclasses covered: {len(SUBCLASS_SIGNATURES)}')
"</automated>
  </verify>
  <done>
    - ABILITIES dict contains exactly 330 entries
    - All 10 domains have 15 pool abilities each
    - All 90 subclasses have exactly 2 signatures each (Tier 3 + Tier 4)
    - Every ability has all 16 required fields with valid values
    - Resource types match guild/fingerprint definitions
    - No duplicate ids, no stub descriptions
    - Validation script passes with zero errors
  </done>
</task>

</tasks>

<verification>
Full validation script in Task 1 verify block covers all structural checks.
Additionally:
- `python -c "from world.ability_registry import ABILITIES; print(len(ABILITIES))"` returns 330
- `evennia test --settings server.conf.settings tests/` passes (no import errors)
</verification>

<success_criteria>
- 330 abilities pass all 10 structural validation checks
- DOMAIN_ABILITIES covers all 10 domains with 15 abilities each
- SUBCLASS_SIGNATURES covers all 90 subclasses with 2 signatures each
- No errors remain after validation + fix cycle
</success_criteria>

<output>
After completion, create `.planning/phases/05b-ability-content-authoring/05b-06-SUMMARY.md`
</output>
