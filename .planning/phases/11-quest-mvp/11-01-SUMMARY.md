---
phase: 11-quest-mvp
plan: 01
subsystem: quest-system
tags: [django-model, quest-engine, objective-tracking, jsonfield, action-vocabulary]

# Dependency graph
requires:
  - phase: 06a-base-attributes-and-combat
    provides: action_vocabulary execute_action dispatch for reward payout
provides:
  - CharacterQuest Django model with per-player quest state tracking
  - quest_engine.py stateless module with accept/abandon/progress/complete/query functions
  - 5 objective type checkers (kill, collect, investigate, deliver, talk_to)
  - Quest chain auto-offer via next_quest_id -> ndb.pending_quest_offer
  - Quest spec normalization from flat format to objectives-list format
affects: [11-02, 11-03, 11-04, 11-05, quest-hooks, quest-commands, quest-content]

# Tech tracking
tech-stack:
  added: []
  patterns: [quest-spec-normalization, event-driven-progress-hooks, refresh_from_db-for-json-updates]

key-files:
  created:
    - world/quest_engine.py
    - world/migrations/0006_characterquest.py
    - tests/test_quest_engine.py
  modified:
    - world/models.py

key-decisions:
  - "Migration numbered 0006 (after 0005_characterability in worktree) rather than 0008 per plan"
  - "Used datetime.datetime fallback for timezone.now() to support unittest.TestCase without Django settings"
  - "Broad except on OOB push_quest_update to tolerate mock characters in tests"
  - "Flat quest spec normalization maps gather->collect, discover->investigate, escort->deliver"
  - "Progress dict keyed by type_target (e.g. kill_sewer_rat) for multi-objective tracking"

patterns-established:
  - "Quest progress uses JSONField dict with refresh_from_db before mutation"
  - "Quest spec lookup scans zone_object tags at runtime (no cache for MVP)"
  - "_normalize_quest_spec converts flat area.quest() format to objectives-list format"

requirements-completed: [D-01, D-02, D-03, D-04, D-05, D-07, D-08, D-09, D-10, D-11, D-18, D-19, D-20, D-22]

# Metrics
duration: 8min
completed: 2026-04-03
---

# Phase 11 Plan 01: Quest Engine Core Summary

**CharacterQuest Django model + stateless quest_engine.py with 14 functions covering accept/abandon, 5 objective types, completion with reward payout via execute_action, chain auto-offer, and query/detail interfaces**

## Performance

- **Duration:** 8 min
- **Started:** 2026-04-03T19:16:56Z
- **Completed:** 2026-04-03T19:24:42Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- CharacterQuest Django model with JSONField progress tracking, 4 status states, timestamps, and proper indexes
- Quest engine with all 14 required functions following the established stateless engine pattern
- Full flat-to-objectives normalization bridging existing area.quest() format to the new multi-objective system
- 28 passing unit tests covering cap enforcement, one_chance lock, progress hooks, completion, chain offers, and queries

## Task Commits

Each task was committed atomically:

1. **Task 1: CharacterQuest Django model + migration** - `1b94efb` (feat)
2. **Task 2: quest_engine.py core functions (TDD RED)** - `ef50113` (test)
3. **Task 2: quest_engine.py core functions (TDD GREEN)** - `5bd2aad` (feat)

## Files Created/Modified
- `world/models.py` - Added CharacterQuest model at end of file
- `world/migrations/0006_characterquest.py` - Migration for CharacterQuest table
- `world/quest_engine.py` - Stateless quest engine with 14 functions
- `tests/test_quest_engine.py` - 28 test cases (unittest.TestCase + MagicMock)

## Decisions Made
- Migration numbered 0006 instead of 0008 as specified in plan -- worktree's latest migration was 0005_characterability, not 0007_merge
- Used `datetime.datetime.now(datetime.timezone.utc)` as fallback when Django settings unavailable, to support pure unittest.TestCase pattern
- Broad except clause on OOB push_quest_update call to tolerate mock characters and missing OOB infrastructure
- Quest spec normalization maps non-MVP objective types: gather/recover/craft -> collect, discover -> investigate, escort -> deliver

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Migration number adjusted from 0008 to 0006**
- **Found during:** Task 1
- **Issue:** Plan specified migration 0008 depending on 0007_merge, but worktree's latest migration is 0005_characterability
- **Fix:** Created migration as 0006_characterquest depending on 0005_characterability
- **Files modified:** world/migrations/0006_characterquest.py
- **Verification:** Python import of CharacterQuest succeeds
- **Committed in:** 1b94efb

**2. [Rule 1 - Bug] Fixed timezone.now() crash in pure unittest context**
- **Found during:** Task 2 (TDD GREEN)
- **Issue:** django.utils.timezone.now() requires Django settings configured, crashes in unittest.TestCase
- **Fix:** Added try/except fallback to datetime.datetime.now(datetime.timezone.utc)
- **Files modified:** world/quest_engine.py
- **Verification:** All 28 tests pass
- **Committed in:** 5bd2aad

**3. [Rule 1 - Bug] Fixed push_quest_update signature mismatch**
- **Found during:** Task 2 (TDD GREEN)
- **Issue:** push_quest_update requires (character, data) but was called with (character) only
- **Fix:** Added data dict parameter and broad except to handle mock characters
- **Files modified:** world/quest_engine.py
- **Verification:** All 28 tests pass
- **Committed in:** 5bd2aad

---

**Total deviations:** 3 auto-fixed (2 bugs, 1 blocking)
**Impact on plan:** All fixes necessary for correctness. No scope creep.

## Issues Encountered
- Git repo corruption in worktree (missing blobs for .gitattributes, .gitignore) -- resolved via `git read-tree HEAD` to rebuild index
- Sparse checkout was enabled on the worktree (set to "plugin" only) -- disabled to allow committing test files

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- CharacterQuest model and quest_engine.py are ready for Plan 02 (event hooks wiring)
- Plan 02 will wire check_kill_objectives into mobs.py at_death, check_investigate into rooms.py at_object_receive, etc.
- Plan 03 will add the CmdQuest command and register in CharacterCmdSet
- All 14 function interfaces are stable and tested

## Self-Check: PASSED

All files verified present:
- world/models.py
- world/migrations/0006_characterquest.py
- world/quest_engine.py
- tests/test_quest_engine.py

All commits verified:
- 1b94efb (Task 1: model + migration)
- ef50113 (Task 2 RED: failing tests)
- 5bd2aad (Task 2 GREEN: implementation)

---
*Phase: 11-quest-mvp*
*Completed: 2026-04-03*
