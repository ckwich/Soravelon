---
phase: 06c-npc-dialogue-and-crafting
plan: 01
subsystem: dialogue
tags: [npc, dialogue, keyword-extraction, standing-tier, ambient-echo, crafting-recipes]

# Dependency graph
requires:
  - phase: 04-domain-fingerprints-guild-engine
    provides: "CharacterGuild model, guild/subclass identity on character"
  - phase: 06a-base-attributes-and-combat
    provides: "Combat system, base attributes"
provides:
  - "KnownTopicRecord Django model for per-character/NPC topic tracking"
  - "CharacterRecipe Django model for recipe discovery tracking"
  - "dialogue_definitions.py with STANDING_TIER_THRESHOLDS, RESPONSE_PRIORITY, TOPIC_SYNONYMS, MAX_HINTS_DISPLAYED"
  - "dialogue_engine.py with 12 functions: greeting, topic response, hints, keyword extraction, ambient tick, reactive echo"
affects: [06c-02, 06c-03, 06c-04, 06c-05]

# Tech tracking
tech-stack:
  added: []
  patterns: ["context-hash hint re-surfacing", "4-stage keyword extraction pipeline", "global ambient NPC ticker"]

key-files:
  created:
    - world/dialogue_definitions.py
    - world/dialogue_engine.py
    - world/migrations/0006_knowntopicrecord_characterrecipe.py
  modified:
    - world/models.py

key-decisions:
  - "MAX_HINTS_DISPLAYED = 4 (balances info vs clutter)"
  - "Context hash uses MD5 truncated to 16 chars for hint re-surfacing"
  - "Migration 0006 hand-crafted to avoid auto-migration picking up unrelated WorldEventLog drift"
  - "Global ambient ticker approach (not per-NPC TickerHandler) per D-10"

patterns-established:
  - "NPC db attribute naming: npc.db.dialogue_greeting_tiers, npc.db.dialogue_topics, etc."
  - "Standing tier derived from get_mob_disposition() float, not raw standing integer"
  - "Dialogue context built from get_character_context_packet() with quest stubs appended"

requirements-completed: [NPC-01, NPC-02, NPC-03]

# Metrics
duration: 4min
completed: 2026-03-27
---

# Phase 06c Plan 01: Dialogue Data Layer Summary

**NPC dialogue engine with Standing-tier greetings, priority-stack topic responses, context-aware hint system, 4-stage keyword extraction, and ambient echo ticker**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-27T02:49:13Z
- **Completed:** 2026-03-27T02:53:30Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- KnownTopicRecord and CharacterRecipe Django models with migration 0006
- dialogue_definitions.py with all static data (tier thresholds, response priority stack, synonym dict, dimension thresholds)
- dialogue_engine.py with 12 functions covering the full dialogue pipeline: greetings, topics, hints, keyword extraction, ambient behavior, quest stubs

## Task Commits

Each task was committed atomically:

1. **Task 1: Django models + migration** - `824f3ed` (feat)
2. **Task 2: Dialogue definitions + dialogue engine** - `b099c65` (feat)

## Files Created/Modified
- `world/models.py` - Added KnownTopicRecord and CharacterRecipe models
- `world/migrations/0006_knowntopicrecord_characterrecipe.py` - Migration for new models
- `world/dialogue_definitions.py` - Static data: tier thresholds, priority stack, synonyms, constants
- `world/dialogue_engine.py` - Core dialogue logic: 12 functions with lazy imports

## Decisions Made
- MAX_HINTS_DISPLAYED set to 4 per plan recommendation
- Context hash for hint re-surfacing uses MD5 truncated to 16 chars (lightweight, collision-resistant enough for hint suppression)
- Hand-crafted migration 0006 instead of auto-generated to avoid picking up unrelated model drift (WorldEventLog missing from models.py but present in migration 0003)
- Global ambient ticker approach (single callback iterating all NPCs) rather than per-NPC TickerHandler subscriptions, per D-10

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Migration number corrected from 0005 to 0006**
- **Found during:** Task 1 (Django models + migration)
- **Issue:** Plan specified migration 0005 but 0005_characterability already exists
- **Fix:** Used correct sequence number 0006 with dependency on 0005_characterability
- **Files modified:** world/migrations/0006_knowntopicrecord_characterrecipe.py
- **Verification:** Migration file created with correct dependency chain

**2. [Rule 3 - Blocking] Hand-crafted migration to avoid WorldEventLog deletion**
- **Found during:** Task 1 (Django models + migration)
- **Issue:** Auto-generated migration tried to delete WorldEventLog model and rename indexes from other models (pre-existing drift between models.py and migration state)
- **Fix:** Wrote hand-crafted migration that only creates the two new models
- **Files modified:** world/migrations/0006_knowntopicrecord_characterrecipe.py
- **Verification:** Models importable, migration only contains CreateModel operations

---

**Total deviations:** 2 auto-fixed (2 blocking)
**Impact on plan:** Both fixes necessary for correct migration. No scope creep.

## Issues Encountered
- Git worktree corruption (missing blobs) forced switching to main repo for commits. Parallel agent contention likely cause. Work completed successfully in main repo.

## Known Stubs
- `has_available_quest()` returns False (quest system not yet built, documented in plan)
- `get_quest_offer()` returns None (quest system not yet built, documented in plan)
- Quest conditions in `_check_condition()` always return False (no active/completed/failed quests yet)

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Dialogue engine ready for Plan 02 (dialogue commands: talk, ask, say, tell)
- NPC db attribute naming convention established for AreaBuilder extensions
- Ambient ticker ready for registration in at_server_startstop.py

## Self-Check: PASSED

All 4 files verified on disk. Both task commits (824f3ed, b099c65) found in git log.

---
*Phase: 06c-npc-dialogue-and-crafting*
*Completed: 2026-03-27*
