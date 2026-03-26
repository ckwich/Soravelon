---
phase: 06b-spawn-system-skills-and-mob-ai
plan: 02
type: execute
wave: 1
depends_on: []
files_modified:
  - world/skill_definitions.py
  - world/skill_engine.py
autonomous: true
requirements: [SKL-01, SKL-02, SKL-03, SKL-04]

must_haves:
  truths:
    - "General proficiency skills (0-100) with passive use accumulation and deliberate practice"
    - "Diminishing returns by tier match vault spec (0-25 full, 26-50 75%, 51-75 40%, 76-90 10%, 91-100 2%)"
    - "Practice has rolling 24hr per-skill cooldown (not global reset)"
    - "Skill progression is independent of domain/guild system"
    - "Trainer sessions raise gain ceiling (framework ready for NPC wiring)"
  artifacts:
    - path: "world/skill_definitions.py"
      provides: "SKILL_DEFINITIONS registry (20+ skills), ANCESTRY_SKILL_SEEDS, TRAINER_REGISTRY, DIMINISHING_BRACKETS"
      contains: "SKILL_DEFINITIONS"
    - path: "world/skill_engine.py"
      provides: "accumulate_skill_use, commit_skill_accumulators, practice_skill, train_with_trainer, get_skill_value, check_discoveries"
      exports: ["accumulate_skill_use", "commit_skill_accumulators", "practice_skill", "get_skill_value"]
  key_links:
    - from: "world/skill_engine.py"
      to: "world/models.py"
      via: "CharacterSkill.objects.get_or_create for lazy record creation"
      pattern: "CharacterSkill.objects"
    - from: "world/skill_engine.py"
      to: "world/skill_definitions.py"
      via: "SKILL_DEFINITIONS lookup for skill metadata"
      pattern: "from world.skill_definitions import"
---

<objective>
Skill definitions registry and core skill engine with all three improvement methods (passive use, deliberate practice, trainer sessions) and discovery framework.

Purpose: SKL-01 through SKL-04 require a full general proficiency system independent of the domain/guild system. This plan creates the static data registry (20+ skills per vault spec) and the engine that handles accumulation, practice, training, and diminishing returns. The discovery framework provides the hook for hidden lore triggers based on skill combinations.

Output: world/skill_definitions.py (data), world/skill_engine.py (logic).
</objective>

<execution_context>
@C:\Users\colek\.claude\get-shit-done\workflows\execute-plan.md
@C:\Users\colek\.claude\get-shit-done\templates\summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md

@C:\Obsidian\brain\Soravelon\soravelon-skills.md

@world/models.py
@world/world_state.py
</context>

<interfaces>
<!-- Existing CharacterSkill model this plan writes to -->

From world/models.py:
```python
class CharacterSkill(models.Model):
    SKILL_TYPES = [
        ("general", "General Proficiency"),
        ("zone_attunement", "Zone Attunement"),
        ("node_attunement", "Node Attunement"),
        ("creature_attunement", "Creature Attunement"),
    ]
    character = models.ForeignKey("objects.ObjectDB", on_delete=models.CASCADE, related_name="skills")
    skill_id = models.CharField(max_length=128)
    skill_type = models.CharField(max_length=32, choices=SKILL_TYPES)
    value = models.FloatField(default=0.0)
    last_practiced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("character", "skill_id")
        indexes = [models.Index(fields=["character", "skill_type"])]
```

<!-- Pattern to follow from world/world_state.py -->
From world/world_state.py (accumulator pattern):
```python
# ndb session accumulators: character.ndb.domain_xp_combat etc.
# batch-committed to DB via commit_session_xp() at breakpoints
```
</interfaces>

<tasks>

<task type="auto">
  <name>Task 1: Skill definitions registry</name>
  <files>world/skill_definitions.py</files>
  <action>
Create `world/skill_definitions.py` as a pure-data Python module (same pattern as ability_registry.py). Per D-16 through D-25.

**SKILL_DEFINITIONS** dict with 21+ entries per D-16. Each entry:
```python
"lockpicking": {
    "name": "Lockpicking",
    "skill_type": "general",
    "description": "Pick locks and bypass mechanical security.",
    "domain_bonus": "subterfuge",  # faster passive gain with this domain
    "thresholds": {
        25: "Basic locks opened without tools",
        50: "Complex locks, some magical wards",
        75: "Master locks, warded containers",
        90: "Dragon-era locks, ancient mechanisms",
        100: "Any lock in the known world",
    },
    "trainer_required_above": 50,
},
```

Full list from D-16: lockpicking, animal_handling, beast_training, herbalism, tracking, climbing, persuasion, intimidation, swimming, first_aid, appraisal, stealth, foraging, node_reading, navigation, fishing, engineering, cooking, smithing, alchemy, reflexes.

For each, set appropriate domain_bonus from vault (soravelon-skills.md Domain Bonus column), trainer_required_above (50 for most, 75 for advanced), and thresholds.

**ANCESTRY_SKILL_SEEDS** dict per D-20:
```python
ANCESTRY_SKILL_SEEDS = {
    "human": {},
    "kauroran": {"swimming": 30, "fishing": 25, "beast_training": 20, "persuasion": 15},
    "veth": {"stealth": 20, "navigation": 25, "lockpicking": 10, "tracking": 25},
    "selvar_north": {"tracking": 20, "climbing": 15, "intimidation": 10},
    "selvar_south": {"lockpicking": 15, "appraisal": 15, "persuasion": 10, "navigation": 20},
}
```

NOTE per Pitfall 7: Selvar coat->lineage mapping: winter=North, summer=South. Document this in a SELVAR_COAT_TO_LINEAGE dict:
```python
SELVAR_COAT_TO_LINEAGE = {"winter": "selvar_north", "summer": "selvar_south"}
```

**TRAINER_REGISTRY** dict (Claude's Discretion -- static Python dicts, stub for now):
```python
TRAINER_REGISTRY = {
    # Populated during content phase. Framework ready.
    # "marveth_locksmith": {
    #     "name": "Marveth",
    #     "trainer_quality": "journeyman",
    #     "skills_taught": ["lockpicking", "appraisal"],
    #     "cost_per_session": 80,
    # },
}
```

**DIMINISHING_BRACKETS** per D-19 (same curve as domain XP):
```python
DIMINISHING_BRACKETS = [
    (0, 25, 1.0),    # full rate
    (26, 50, 0.75),
    (51, 75, 0.40),
    (76, 90, 0.10),
    (91, 100, 0.02),
]
```

**PRACTICE_GAINS** per vault spec:
```python
PRACTICE_GAINS = [
    (0, 25, 3.0, 5.0),    # (min_skill, max_skill, min_gain, max_gain)
    (26, 50, 2.0, 4.0),
    (51, 75, 1.0, 3.0),
    (76, 90, 0.5, 1.0),
    (91, 100, 0.1, 0.3),
]
```

**ATTUNEMENT_THRESHOLDS** per D-23:
```python
ATTUNEMENT_THRESHOLDS = {
    25: "sensory_detail",
    50: "hidden_reveal",
    75: "mob_patterns",
    90: "enhanced_magic",
    100: "lore_fragment",
}
```

**DISCOVERY_TRIGGERS** per D-24 (framework with one example entry):
```python
DISCOVERY_TRIGGERS = [
    {
        "id": "cantera_cognitive_wolves",
        "conditions": {"cognitive_node": 90, "forest_wolf": 90, "cantera_forest_old_path": 75},
        "lore_fragment": "lore_cantera_cognitive_001",
        "message": "You notice something about the wolves near this stone...",
    },
]
```

**PASSIVE_ACCUMULATOR_THRESHOLD** = 10 (10 successful uses = +0.1 skill value per vault).
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "from world.skill_definitions import SKILL_DEFINITIONS, ANCESTRY_SKILL_SEEDS, DIMINISHING_BRACKETS, PRACTICE_GAINS, DISCOVERY_TRIGGERS, SELVAR_COAT_TO_LINEAGE; assert len(SKILL_DEFINITIONS) >= 21, f'Expected 21+ skills, got {len(SKILL_DEFINITIONS)}'; assert 'reflexes' in SKILL_DEFINITIONS; assert 'cooking' in SKILL_DEFINITIONS; assert len(ANCESTRY_SKILL_SEEDS) == 5; print('OK')"</automated>
  </verify>
  <done>SKILL_DEFINITIONS has 21+ entries covering all D-16 skills. ANCESTRY_SKILL_SEEDS maps 5 ancestry variants (human, kauroran, veth, selvar_north, selvar_south) with SELVAR_COAT_TO_LINEAGE for coat-to-lineage mapping. DIMINISHING_BRACKETS and PRACTICE_GAINS match vault spec exactly.</done>
</task>

<task type="auto">
  <name>Task 2: Skill engine -- accumulation, practice, training, discovery</name>
  <files>world/skill_engine.py</files>
  <action>
Create `world/skill_engine.py` with the following public functions. Follow the (bool, str) return tuple pattern for all mutation functions per project convention.

**get_skill_value(character, skill_id) -> float:**
- CharacterSkill.objects.filter(character=character, skill_id=skill_id).first()
- Return record.value if exists, else 0.0

**get_skills_by_type(character, skill_type) -> list[dict]:**
- Query CharacterSkill records for character filtered by skill_type
- Return list of {"skill_id": ..., "name": ..., "value": ..., "last_practiced_at": ...}
- Only return non-zero skills per D-21

**accumulate_skill_use(character, skill_id, count=1):**
- Increment ndb accumulator: `key = f"skill_use_{skill_id}"`
- `current = getattr(character.ndb, key, 0) or 0`
- `setattr(character.ndb, key, current + count)`
- No DB write per Pitfall 2 in research (anti-pattern: per-use DB writes)

**commit_skill_accumulators(character):**
- Iterate all SKILL_DEFINITIONS keys
- For each, check `getattr(character.ndb, f"skill_use_{skill_id}", 0)`
- If accumulated >= PASSIVE_ACCUMULATOR_THRESHOLD (10): apply passive gain
- Passive gain: 0.1 * diminishing_rate_for_current_value (use _get_diminishing_rate helper)
- Use `CharacterSkill.objects.get_or_create()` for lazy record creation
- `record.value = min(100.0, record.value + gain)`; `record.save()`
- Reset ndb accumulator to remainder (accumulated % threshold)
- After applying gains, call `check_discoveries(character, skill_id, new_value)` if value crossed a threshold

**practice_skill(character, skill_id) -> (bool, str):**
- Validate skill_id exists in SKILL_DEFINITIONS
- get_or_create CharacterSkill record
- Rolling 24hr cooldown check per D-18/Pitfall 4: `timezone.now() - record.last_practiced_at >= timedelta(hours=24)`
- Calculate gain from PRACTICE_GAINS table using `random.uniform(min_gain, max_gain)` for current tier
- Apply diminishing rate multiplier
- Check trainer_required_above: if record.value > threshold and no recent trainer session, cap gain at 50% (trainer_quality modifier TBD -- for now just note in message)
- `record.value = min(100.0, record.value + gain)`
- `record.last_practiced_at = timezone.now()`; `record.save()`
- Call `check_discoveries(character, skill_id, record.value)` if value crossed threshold
- Return (True, f"[{defn['name']}: {old_value:.0f} -> {record.value:.0f}]\n[Next practice available in 24 hours]")

**train_with_trainer(character, skill_id, trainer_id) -> (bool, str):**
- Look up trainer in TRAINER_REGISTRY
- Validate trainer teaches this skill
- Check character has enough Scales (use banking.get_balance or character.db.carried_scales)
- Deduct cost
- Apply trainer bonus: set `character.ndb.trainer_bonus_{skill_id} = trainer_quality_multiplier`
- This bonus is consumed on next practice_skill() call (multiplies gain)
- Return (True, f"[{trainer_name} coached you on {skill_name}. Next practice will be enhanced.]")

**apply_ancestry_skill_seeds(character, ancestry_id, coat=None):**
- Look up seeds from ANCESTRY_SKILL_SEEDS
- For Selvar: use SELVAR_COAT_TO_LINEAGE[coat] to get the right seed set
- For each seed: `CharacterSkill.objects.get_or_create(character=character, skill_id=skill_id, defaults={"skill_type": "general", "value": seed_value})`
- If record already exists (shouldn't at creation, but defensive): only set value if current < seed_value

**check_discoveries(character, changed_skill_id, new_value):**
- Per D-24: only check on threshold crossings (25/50/75/90/100)
- For each DISCOVERY_TRIGGER: check if ALL conditions met (query CharacterSkill for each required skill_id >= threshold)
- Track discovered discoveries on `character.db.discoveries` (set of discovery IDs)
- If new discovery: send lore message to character, add to discoveries set
- Use SaverDict copy pattern for the set mutation

**_get_diminishing_rate(current_value) -> float:**
- Look up DIMINISHING_BRACKETS for the tier containing current_value
- Return the rate multiplier
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "from world.skill_engine import accumulate_skill_use, commit_skill_accumulators, practice_skill, get_skill_value, apply_ancestry_skill_seeds, check_discoveries, train_with_trainer, get_skills_by_type; print('All exports OK')"</automated>
  </verify>
  <done>skill_engine.py provides all three improvement methods: passive use (ndb accumulator + batch commit), deliberate practice (24hr rolling cooldown, tier-based gains), and trainer sessions (cost Scales, enhance next practice). Discovery framework checks skill combos on threshold crossings. All mutation functions return (bool, str) per project convention.</done>
</task>

</tasks>

<verification>
- All 21+ skills defined in SKILL_DEFINITIONS with correct skill_type, domain_bonus, thresholds
- ANCESTRY_SKILL_SEEDS covers human (empty), kauroran, veth, selvar_north, selvar_south
- practice_skill() respects 24hr rolling cooldown per skill (not global)
- Diminishing returns match vault: full/75%/40%/10%/2% at tier boundaries
- get_skill_value() returns 0.0 for unlearned skills (lazy creation)
- check_discoveries() only fires on threshold crossings
</verification>

<success_criteria>
A character can accumulate skill use passively (ndb accumulators batched to DB), practice skills with 24hr cooldown and tier-based diminishing returns, and train with NPCs to enhance practice gains. The skill system is entirely independent of the domain/guild system (SKL-04). All 20+ general proficiency skills from D-16 are defined. Discovery framework is wired and ready for content.
</success_criteria>

<output>
After completion, create `.planning/phases/06b-spawn-system-skills-and-mob-ai/06b-02-SUMMARY.md`
</output>
