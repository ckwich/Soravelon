# Phase 16: Architectural Refactoring - Research

**Researched:** 2026-04-05
**Domain:** Code structure, naming consistency, Evennia SaverDict safety, Python import hygiene
**Confidence:** HIGH

## Summary

This phase is a pure refactoring pass -- no new features, no behavior changes. The scope breaks into 7 independent work streams that can mostly be parallelized: lifecycle orchestrator extraction, command logic extraction, duplicate consolidation, naming renames, SaverDict audit, return type enforcement, and import cleanup.

The codebase is in good shape for refactoring. Most SaverDict mutations already follow copy-mutate-assign (grep found zero in-place mutations in world/ or typeclasses/). The naming renames (D-11, D-12) are the riskiest items because `mob_id` is used as an Evennia tag **category** stored in the database and `mob_template` is a Django model field on `SpawnRecord` -- both require careful handling to avoid breaking existing stored data. Typeclass god methods are well-understood: at_post_puppet is ~65 lines, at_pre_unpuppet is ~50 lines, at_after_move is ~80 lines, at_death is ~75 lines. All follow the same pattern of importing world/ modules and calling functions sequentially.

**Primary recommendation:** Execute as 7 independent work plans (one per scope item), with the naming rename plan (D-11/D-12) requiring the most care due to stored data implications. Lifecycle orchestrators and command extraction are the highest-value items.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- D-01: Create domain-split lifecycle orchestrator files: `world/session_lifecycle.py` (login/logout), `world/movement_lifecycle.py` (move), `world/death_lifecycle.py` (mob death).
- D-02: Each orchestrator exposes a single entry point (e.g., `on_login(character)`, `on_move(character, source, dest)`) that coordinates all the individual system calls internally.
- D-03: Typeclass hooks become thin 3-line delegates: call the orchestrator, nothing else. Example: `at_post_puppet` calls `session_lifecycle.on_login(self)`.
- D-04: Orchestrators import world modules lazily (inside functions) to avoid circular imports.
- D-05: Move `cmd_fishing._catch_fish()` logic into `world/gathering_engine.py` as a `catch_fish()` function.
- D-06: Move `cmd_gathering._gather_callback()` logic into `world/gathering_engine.py` as an expanded `gather_from_node()` or new `complete_gather()` function.
- D-07: Commands retain only: argument parsing, user messages, calling the engine. No game state mutation.
- D-08: Extract only when the SAME computation appears in 2+ places with identical logic. No premature abstractions.
- D-09: Specific targets: weapon damage fallback (combat_engine.py two branches), effect list search (status_effects.py two loops), threshold-checking patterns.
- D-10: New helpers go in their owning module (e.g., `_find_effect()` in status_effects.py), not a separate utils file.
- D-11: Rename `mob_template` -> `mob_template_key` and `mob_id` -> `mob_instance_id` across all modules to make the distinction explicit.
- D-12: Update all references in world/*.py, typeclasses/*.py, commands/*.py, and tests/*.py. This is a breaking rename -- must be done atomically.
- D-13: Systematic sweep of all `db.*` dict/set/list mutations. Every mutation must use copy-mutate-assign pattern.
- D-14: Key targets: any `del db.foo[key]`, `db.foo.append()`, `db.foo.add()`, `db.foo[key] = val` without prior `dict(db.foo)` copy.
- D-15: Every public function in `world/*.py` engine modules must return `(bool, str)` tuples per project convention.
- D-16: Internal/private functions (prefixed with `_`) are exempt from tuple returns.
- D-17: Move heavy top-level imports in typeclasses/ to lazy (inside methods) where they import from world/.
- D-18: Remove all unused imports.
- D-19: Verify no circular import paths exist between typeclasses/ and world/ modules.

### Claude's Discretion
- Exact helper function names and signatures for extracted duplicates
- Whether to inline small orchestrator calls vs function references
- Import ordering within files

### Deferred Ideas (OUT OF SCOPE)
- Serializable game data format for companion apps
- Equipment query caching (can_equip() optimization)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| D-01 | Create lifecycle orchestrator files | Typeclass hook analysis complete -- at_post_puppet, at_pre_unpuppet, at_after_move, at_death all documented |
| D-02 | Single entry point per orchestrator | Hook call sequences mapped for all 4 targets |
| D-03 | Thin typeclass delegates | Current hook sizes measured (65-80 lines each), extraction pattern verified |
| D-04 | Lazy imports in orchestrators | Existing lazy import pattern confirmed throughout codebase |
| D-05 | Extract _catch_fish to gathering_engine | Full logic analyzed (lines 226-303 of cmd_fishing.py) |
| D-06 | Extract _gather_callback to gathering_engine | Full logic analyzed (lines 87-154 of cmd_gathering.py) |
| D-07 | Commands as thin arg-parse + message layers | item_effects.py extraction from cmd_abilities is the reference pattern |
| D-08 | No premature abstractions | Duplicate targets verified as genuinely duplicated |
| D-09 | Weapon damage + effect lookup consolidation | combat_engine.py lines 151-168 and status_effects.py lines 197-233 analyzed |
| D-10 | Helpers in owning module | Confirmed: no utils.py exists, pattern is module-local privates |
| D-11 | Rename mob_template -> mob_template_key | CRITICAL: `mob_template` is a Django model field on SpawnRecord AND a db.* attribute -- needs migration |
| D-12 | Rename mob_id -> mob_instance_id atomically | CRITICAL: `mob_id` is an Evennia tag category stored in DB -- needs data consideration |
| D-13 | SaverDict mutation sweep | Audit complete: zero in-place violations found in production code |
| D-14 | Key mutation targets | Tests have read-only db indexing; production code is clean |
| D-15 | Return type (bool, str) enforcement | 13 bare return/return None sites found in world/*.py for review |
| D-16 | Private function exemption | Pattern clear: _ prefix = exempt |
| D-17 | Lazy imports in typeclasses | Only 2 top-level world/ imports found (both in mobs.py) |
| D-18 | Remove unused imports | Requires per-file sweep |
| D-19 | No circular imports | Current architecture is clean: typeclasses -> world/ (one direction) |
</phase_requirements>

## Architecture Patterns

### Lifecycle Orchestrator Pattern

The current typeclass hooks are sequential call lists. The orchestrator pattern extracts these into world/ modules:

**Before (typeclasses/characters.py at_post_puppet, ~65 lines):**
```python
def at_post_puppet(self, **kwargs):
    super().at_post_puppet(**kwargs)
    from world.world_state import init_session_accumulators
    from world.base_attributes import STAT_NAMES, derive_max_hp, derive_max_stamina
    init_session_accumulators(self)
    self.ndb.stat_xp_accumulators = {stat: 0.0 for stat in STAT_NAMES}
    # ... 60 more lines of init ...
```

**After (thin delegate):**
```python
def at_post_puppet(self, **kwargs):
    super().at_post_puppet(**kwargs)
    from world.session_lifecycle import on_login
    on_login(self)
```

**Orchestrator structure (world/session_lifecycle.py):**
```python
def on_login(character):
    """Coordinate all systems at login. Called from Character.at_post_puppet."""
    from world.world_state import init_session_accumulators
    from world.base_attributes import STAT_NAMES, derive_max_hp, derive_max_stamina
    # ... all the logic currently in at_post_puppet ...

def on_logout(character):
    """Coordinate all systems at logout. Called from Character.at_pre_unpuppet."""
    from world.world_state import commit_session_xp
    # ... all the logic currently in at_pre_unpuppet ...
```

### Target Orchestrators

| File | Entry Points | Source Hook(s) |
|------|-------------|----------------|
| `world/session_lifecycle.py` | `on_login(character)`, `on_logout(character)` | `Character.at_post_puppet`, `Character.at_pre_unpuppet` |
| `world/movement_lifecycle.py` | `on_move(character, source_location)` | `Character.at_after_move` |
| `world/death_lifecycle.py` | `on_mob_death(mob, killer)` | `SoravelonMob.at_death` |

### Room Hook Note

`SoravelonRoom.at_object_receive` (lines 96-148) is also a god method but was NOT listed in the decisions. It remains as-is for this phase.

### Command Logic Extraction Pattern

Reference: `world/item_effects.py` was extracted from `commands/cmd_abilities.py` in a prior phase. Same pattern applies.

**Before (in command):**
```python
def _catch_fish(self, character, state, quality_multiplier=1.0):
    # 80 lines of game logic
```

**After (in world/gathering_engine.py):**
```python
def catch_fish(character, node, tool, bait, quality_multiplier=1.0):
    """Process a fish catch. Returns (bool, str)."""
    # Same logic, returns (bool, str) + item reference
```

**Command becomes:**
```python
def _catch_fish(self, character, state, quality_multiplier=1.0):
    from world.gathering_engine import catch_fish
    success, msg = catch_fish(character, state["node"], state["tool"], state.get("bait"), quality_multiplier)
    character.msg(msg)
    if not success:
        self._stop_fishing(character)
```

### Anti-Patterns to Avoid
- **Creating a utils.py:** All helpers go in their owning module per D-10
- **Changing behavior during refactoring:** This is a structure-only change. All game logic must produce identical results
- **Renaming DB-stored strings without migration:** Tag categories and model fields live in the database

## Naming Rename: Critical Stored Data Analysis

### mob_template -> mob_template_key

| Location | Type | Migration Needed |
|----------|------|-----------------|
| `SpawnRecord.mob_template` (Django model field) | DB column | YES -- Django migration to rename column |
| `mob.db.mob_template` (Evennia db attribute) | Pickled in AttributeDB | Code-only -- read old value, write new key at creation time. Existing mobs get destroyed/recreated by spawner on reload |
| `mob_templates.py` dict keys | Code-only | No |
| `action_vocabulary.py` references | Code-only | No |
| `quest_engine.py` references | Code-only | No |

### mob_id -> mob_instance_id

| Location | Type | Migration Needed |
|----------|------|-----------------|
| Evennia tag `category="mob_id"` | Stored in `django_tags` table | DECISION NEEDED: rename tag category requires `Tag.objects.filter(db_category="mob_id").update(db_category="mob_instance_id")` OR keep old category string as constant |
| `combat_ai.py` local variable `mob_id` | Code-only (holds integer .id) | No -- this is a different concept (DB primary key), rename to `combatant_db_id` or leave as-is |
| `combat_script.py` dict key `"mob_id"` | In-memory dict | Code-only |
| `quest_engine.py` references | Code-only | No |
| `zone_serializer.py` dict key | Code-only (zone JSON schema) | No, but zone.json files need update |
| `test_world_state.py` data dict | Code-only | No |

**Recommendation:** For the tag category `"mob_id"`, use a two-step approach:
1. Define `MOB_INSTANCE_TAG_CATEGORY = "mob_instance_id"` constant
2. Add a data migration that updates existing tags
3. Update all code to use the constant

For the `SpawnRecord.mob_template` field, create a standard Django `RenameField` migration.

## Duplicate Logic Consolidation Targets

### 1. Weapon Damage Fallback (combat_engine.py lines 151-168)

Two branches compute damage: character-attacking and mob-attacking. Both follow: get min/max -> randint -> apply strength modifier. The duplicate is the fallback to BARE_HANDS constants. This is a small consolidation -- extract `_compute_raw_damage(attacker, weapon)`.

### 2. Effect List Search (status_effects.py lines 192-233)

`_apply_stackable` and `_apply_non_stackable` both iterate `effects` list looking for matching `entry["type"]`. Extract: `_find_effect(effects, effect_type) -> (entry, index)`.

### 3. Threshold Patterns

These need to be identified during implementation. The audit flagged "threshold-checking patterns" generically. Implementer should grep for repeated if/elif chains comparing numeric ranges.

## SaverDict Audit Results

**Finding: Production code is already clean.** A systematic grep for in-place mutations on `.db.*` collections found:
- **world/*.py:** 0 violations
- **typeclasses/*.py:** 0 violations
- **commands/*.py:** 0 violations
- **tests/*.py:** Read-only indexing only (assertEqual assertions)

The copy-mutate-assign pattern has been consistently applied throughout. The SaverDict audit (D-13/D-14) should still do a manual review, but expect minimal or zero fixes needed.

## Return Type Enforcement Audit

Bare `return` or `return None` sites found in world/*.py (13 total):
- `command_preprocessor.py`: 2 sites (lines 94, 175) -- these are parser functions, may be intentionally non-tuple
- `patrol_engine.py`: 1 site (line 155) -- fire-and-forget tick handler
- `node_helpers.py`: 1 site (line 22) -- lookup function returning None for "not found"
- `nodes/node_effects.py`: 1 site (line 19) -- tick handler
- `zone_registry.py`: 1 site (line 20) -- lookup returning None
- `scripts/patrol_script.py`: 7 sites -- Script.at_repeat internal (not public API)

**Assessment:** Most of these are internal/script functions that are exempt per D-16. The public API functions to fix are likely few. The implementer should check each site for public vs private status.

## Import Hygiene Assessment

### Top-Level world/ Imports in Typeclasses

Only **2 top-level imports** from world/ found in typeclasses/:
```python
# typeclasses/mobs.py lines 9-10
from world.mob_affix_roller import apply_affixes_to_mob, get_star_prefix
from world.mob_affixes import MOB_AFFIXES
```

These are used in `at_object_creation` -- moving them lazy requires importing inside the method.

### Circular Import Risk

Current architecture is clean: `typeclasses/ -> world/` is one-directional. No world/ module imports from typeclasses/. The new lifecycle orchestrators maintain this direction (world/ modules called by typeclasses/, never importing from typeclasses/).

### Unused Imports

Requires per-file automated scan. Recommended approach: use `pyflakes` or manual grep. No automated tool is installed in the project currently.

## Common Pitfalls

### Pitfall 1: Renaming DB-Stored Strings Without Migration
**What goes wrong:** Code renames `"mob_id"` tag category to `"mob_instance_id"` but existing mobs in the database still have tags with category `"mob_id"`. Tag lookups silently return nothing.
**Why it happens:** Evennia tags are stored as strings in Django's tag table. Code changes don't update stored data.
**How to avoid:** Either (a) add a data migration, or (b) keep the old string as a constant and only rename variables.
**Warning signs:** Named mob detection breaks after rename (at_death line 189 checks this tag).

### Pitfall 2: Breaking Test Mock Paths During Extraction
**What goes wrong:** Moving `_catch_fish` logic to `gathering_engine.catch_fish` breaks any test that patches `commands.cmd_fishing.CmdFish._catch_fish`.
**Why it happens:** Tests mock at the import path. Moving code changes the path.
**How to avoid:** Update mock paths in test files atomically with the extraction.
**Warning signs:** Tests that passed before fail with "object has no attribute" errors.

### Pitfall 3: Orchestrator Swallowing Exceptions
**What goes wrong:** Wrapping 65 lines of at_post_puppet in a single orchestrator function. If any line raises, the entire login flow aborts.
**Why it happens:** The original code in the typeclass hook had implicit error isolation (Evennia catches exceptions in hooks). The orchestrator is now a plain function call.
**How to avoid:** Keep the same error handling semantics. If the original code had no try/except, the orchestrator should not add one either -- Evennia's hook runner handles it.

### Pitfall 4: Incomplete Atomic Rename
**What goes wrong:** Renaming `mob_template` in 9 out of 10 files. The missed file causes a KeyError at runtime.
**Why it happens:** Grep misses string literals, dict keys, or test fixtures.
**How to avoid:** Search for both the variable pattern AND the string literal pattern. Verify zero remaining occurrences after rename.
**Warning signs:** Any grep hit for the old name after the rename plan completes.

### Pitfall 5: Django Migration for SpawnRecord Field
**What goes wrong:** Renaming the `mob_template` field on `SpawnRecord` without a proper `RenameField` migration.
**Why it happens:** Developer creates a new migration with `RemoveField` + `AddField` instead of `RenameField`, losing data.
**How to avoid:** Use `evennia makemigrations world` after the model change. Verify the auto-generated migration uses `RenameField`. If it generates Remove+Add, manually edit to `RenameField`.

## Code Examples

### Lifecycle Orchestrator Template
```python
# world/session_lifecycle.py
"""
Session lifecycle orchestrator.
Coordinates all system calls for login/logout.
"""


def on_login(character):
    """
    Called from Character.at_post_puppet after super().
    Initializes all volatile state and pushes initial OOB.
    """
    from world.world_state import init_session_accumulators
    from world.base_attributes import STAT_NAMES, derive_max_hp, derive_max_stamina

    init_session_accumulators(character)

    # Stat growth session accumulators (volatile)
    character.ndb.stat_xp_accumulators = {stat: 0.0 for stat in STAT_NAMES}

    # Combat-relevant ndb state
    character.ndb.combat_handler = None
    # ... etc -- exact copy of at_post_puppet body ...
```

### Django RenameField Migration
```python
# world/migrations/XXXX_rename_mob_template_key.py
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('world', '0007_merge_20260326_2012'),
    ]
    operations = [
        migrations.RenameField(
            model_name='spawnrecord',
            old_name='mob_template',
            new_name='mob_template_key',
        ),
    ]
```

### Tag Category Data Migration
```python
# world/migrations/XXXX_rename_mob_id_tag.py
from django.db import migrations

def rename_mob_id_tags(apps, schema_editor):
    Tag = apps.get_model('typeclasses', 'Tag')  # Evennia's tag model
    Tag.objects.filter(db_category="mob_id").update(db_category="mob_instance_id")

def reverse_rename(apps, schema_editor):
    Tag = apps.get_model('typeclasses', 'Tag')
    Tag.objects.filter(db_category="mob_instance_id").update(db_category="mob_id")

class Migration(migrations.Migration):
    dependencies = [
        ('world', '0007_merge_20260326_2012'),
    ]
    operations = [
        migrations.RunPython(rename_mob_id_tags, reverse_rename),
    ]
```

**Note:** The Evennia Tag model may be in a different app (`typeclasses` or `objects`). Verify the actual model location before writing the migration.

### Effect Helper Extraction
```python
# In world/status_effects.py
def _find_effect(effects, effect_type):
    """Find an effect entry by type. Returns (entry, index) or (None, -1)."""
    for idx, entry in enumerate(effects):
        if entry["type"] == effect_type:
            return entry, idx
    return None, -1
```

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Evennia test runner (Django-based) + unittest.TestCase |
| Config file | `server/conf/settings.py` |
| Quick run command | `evennia test --settings server.conf.settings tests/` |
| Full suite command | `evennia test --settings server.conf.settings tests/` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| D-01/D-03 | Orchestrators called from typeclasses | unit | `evennia test --settings server.conf.settings tests/test_typeclasses.py -x` | Yes (extend) |
| D-05/D-06 | Extracted gathering functions | unit | `evennia test --settings server.conf.settings tests/test_gathering.py -x` | Yes (extend) |
| D-09 | Consolidated helpers | unit | `evennia test --settings server.conf.settings tests/test_combat_engine.py tests/test_status_effects.py -x` | Yes (extend) |
| D-11/D-12 | Naming rename completeness | smoke | grep-based verification (zero old-name hits) | Manual |
| D-13/D-14 | SaverDict compliance | manual-only | grep-based audit | Manual |
| D-15 | Return type enforcement | unit | Per-module existing tests | Yes (existing) |
| D-17/D-18/D-19 | Import hygiene | smoke | `python -c "import typeclasses.characters"` | Manual |

### Sampling Rate
- **Per task commit:** `evennia test --settings server.conf.settings tests/`
- **Per wave merge:** Full suite
- **Phase gate:** Full suite green before verify

### Wave 0 Gaps
- [ ] `tests/test_session_lifecycle.py` -- covers D-01/D-02/D-03 for login/logout orchestrator
- [ ] `tests/test_movement_lifecycle.py` -- covers D-01/D-02/D-03 for movement orchestrator
- [ ] `tests/test_death_lifecycle.py` -- covers D-01/D-02/D-03 for mob death orchestrator

## Project Constraints (from CLAUDE.md)

- Store game state on `db` attributes (persisted) or `ndb` (volatile). Never raw Django fields on typeclasses.
- Custom Django models go in `world/models.py`; register the `world` app for migrations.
- All game logic lives in `world/` modules; typeclasses call into them. (This phase enforces this rule more strictly.)
- Tests use Evennia's `EvenniaTestCase` or `EvenniaCommandTestMixin`.
- Return `(bool, str)` tuples from game logic. (D-15 enforces this.)
- SaverDict copy pattern -- copy `db.*` dict to plain dict, mutate, assign once. (D-13/D-14 audits this.)

## Scope Sizing

| Work Stream | Files Touched | Estimated Complexity | Risk |
|-------------|---------------|---------------------|------|
| Lifecycle orchestrators (D-01 to D-04) | 6 new + 3 modified | Medium | Low |
| Command extraction (D-05 to D-07) | 3 modified | Medium | Low |
| Duplicate consolidation (D-08 to D-10) | 2-3 modified | Low | Low |
| Naming rename (D-11 to D-12) | 12+ modified + 2 migrations | High | HIGH |
| SaverDict audit (D-13 to D-14) | 0-5 modified | Low (likely no fixes) | Low |
| Return type enforcement (D-15 to D-16) | 3-5 modified | Low | Low |
| Import hygiene (D-17 to D-19) | 5-10 modified | Low | Low |

## Sources

### Primary (HIGH confidence)
- Direct codebase analysis of all target files
- Grep-based audits for SaverDict mutations, mob_id/mob_template usage, import patterns
- Line-by-line reading of typeclass hooks, command methods, status_effects.py

### Secondary (MEDIUM confidence)
- Evennia Tag model location for data migration (need to verify actual app label at implementation time)

## Metadata

**Confidence breakdown:**
- Architecture patterns: HIGH -- direct code analysis, extraction pattern proven by item_effects.py precedent
- Naming renames: HIGH -- all stored data locations identified, migration requirements documented
- SaverDict audit: HIGH -- comprehensive grep found zero violations
- Return types: HIGH -- all bare returns enumerated
- Import hygiene: MEDIUM -- unused import detection requires per-file manual or tool-based scan

**Research date:** 2026-04-05
**Valid until:** 2026-05-05 (stable -- internal refactoring, no external dependencies)
