---
phase: 16-architectural-refactoring
plan: 04
subsystem: database, world-engine
tags: [django-migration, rename-field, mob-spawner, tag-category, naming-convention]

# Dependency graph
requires:
  - phase: 03.1-mob-spawn-runtime
    provides: SpawnRecord model, mob_spawner.py, named mob tag system
provides:
  - "SpawnRecord.mob_template_key (renamed from mob_template)"
  - "MOB_INSTANCE_TAG_CATEGORY constant for mob tag category"
  - "Django migration 0008 RenameField"
  - "combatant_db_id naming convention for combat integer IDs"
affects: [mob-spawner, combat-system, quest-engine, zone-serializer, area-builder]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "MOB_INSTANCE_TAG_CATEGORY constant in mob_spawner.py for tag category"
    - "combatant_db_id naming convention for integer DB primary keys in combat code"

key-files:
  created:
    - world/migrations/0008_rename_mob_template_key.py
  modified:
    - world/models.py
    - world/mob_templates.py
    - world/mob_spawner.py
    - world/quest_engine.py
    - world/action_vocabulary.py
    - world/combat_ai.py
    - world/combat_script.py
    - world/zone_serializer.py
    - world/area_builder.py
    - world/named_mob_registry.py
    - typeclasses/mobs.py
    - tests/test_mob_spawner.py
    - tests/test_quest_engine.py
    - tests/test_spawn_record.py
    - tests/test_world_state.py

key-decisions:
  - "mob.db.mob_template_key now set explicitly in apply_mob_template (was missing before)"
  - "combat_ai.py and combat_script.py local vars renamed to combatant_db_id (integer DB PK, different concept from tag category)"
  - "zone_serializer.py JSON key renamed from mob_id to mob_instance_id"
  - "Existing database tags with old category self-heal on zone reload (no data migration needed)"

patterns-established:
  - "MOB_INSTANCE_TAG_CATEGORY: always import from mob_spawner, never hardcode string"
  - "combatant_db_id: integer DB primary key for combat combatant tracking"

requirements-completed: [D-11, D-12]

# Metrics
duration: 15min
completed: 2026-04-05
---

# Phase 16 Plan 04: Mob Template Key and Instance ID Rename Summary

**Renamed mob_template -> mob_template_key and mob_id tag category -> mob_instance_id across 15+ files with Django RenameField migration**

## Performance

- **Duration:** 15 min
- **Started:** 2026-04-05T17:52:36Z
- **Completed:** 2026-04-05T18:07:00Z
- **Tasks:** 2
- **Files modified:** 15

## Accomplishments
- SpawnRecord.mob_template renamed to mob_template_key with data-preserving Django RenameField migration
- mob_id tag category replaced by MOB_INSTANCE_TAG_CATEGORY constant ("mob_instance_id") across all code
- combat_ai.py/combat_script.py local variables clarified as combatant_db_id to distinguish from tag category
- Zero old-name occurrences remain in production code (verified by grep)

## Task Commits

Each task was committed atomically:

1. **Task 1: Rename mob_template -> mob_template_key** - `78de768` (feat)
2. **Task 2: Rename mob_id tag category -> mob_instance_id** - `100e8e3` (feat)

## Files Created/Modified
- `world/migrations/0008_rename_mob_template_key.py` - Django RenameField migration for SpawnRecord
- `world/models.py` - SpawnRecord field renamed to mob_template_key
- `world/mob_templates.py` - Now sets mob.db.mob_template_key in apply_mob_template
- `world/mob_spawner.py` - MOB_INSTANCE_TAG_CATEGORY constant, all tag category refs updated
- `world/quest_engine.py` - Reads mob.db.mob_template_key and mob.db.mob_instance_id
- `world/action_vocabulary.py` - Local var renamed to mob_template_key
- `world/combat_ai.py` - Local vars renamed to combatant_db_id
- `world/combat_script.py` - Comment and key reference updated to combatant_db_id
- `world/zone_serializer.py` - JSON key mob_id -> mob_instance_id for named_mobs
- `world/area_builder.py` - named_mob() parameter renamed to mob_instance_id
- `world/named_mob_registry.py` - All parameter names updated to mob_instance_id
- `typeclasses/mobs.py` - Uses MOB_INSTANCE_TAG_CATEGORY for is_named check
- `tests/test_mob_spawner.py` - Tag category assertions updated
- `tests/test_quest_engine.py` - mob.db.mob_template_key and mob.db.mob_instance_id
- `tests/test_spawn_record.py` - Field name assertions updated
- `tests/test_world_state.py` - Event data key updated

## Decisions Made
- mob.db.mob_template_key is now explicitly set in apply_mob_template() -- this was previously missing (quest_engine read it but nothing wrote it)
- combat_ai.py/combat_script.py local vars holding integer DB primary keys renamed to combatant_db_id -- different semantic concept from the tag category mob_instance_id
- zone_serializer.py JSON key renamed from mob_id to mob_instance_id -- any existing .zone.json files must update this key
- Existing database tags with category="mob_id" become orphaned but self-heal when zones reload (mob_spawner destroys and recreates mobs)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Added mob.db.mob_template_key assignment in apply_mob_template**
- **Found during:** Task 1
- **Issue:** quest_engine.py reads mob.db.mob_template but apply_mob_template never set it
- **Fix:** Added `mob.db.mob_template_key = template_key` line in apply_mob_template()
- **Files modified:** world/mob_templates.py
- **Committed in:** 78de768 (Task 1 commit)

**2. [Rule 2 - Missing Critical] Updated named_mob_registry.py parameter names**
- **Found during:** Task 2
- **Issue:** named_mob_registry.py used mob_id parameter names matching the old convention
- **Fix:** Renamed all function parameters to mob_instance_id
- **Files modified:** world/named_mob_registry.py
- **Committed in:** 100e8e3 (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (2 missing critical)
**Impact on plan:** Both fixes necessary for consistency. No scope creep.

## Issues Encountered
- Git index corruption from merge with main (corrupted blob objects from upstream GSD tool repo) required index rebuild before Task 2 commit

## Known Stubs
None -- this plan is a mechanical rename with no new stubs.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All mob_template -> mob_template_key renames complete
- All mob_id tag -> mob_instance_id renames complete
- Django migration ready to apply on next `evennia migrate`
- Existing dev database tags self-heal on zone reload

---
*Phase: 16-architectural-refactoring*
*Completed: 2026-04-05*
