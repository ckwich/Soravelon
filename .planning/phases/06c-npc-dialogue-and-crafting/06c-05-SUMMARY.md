---
phase: 06c-npc-dialogue-and-crafting
plan: 05
subsystem: testing
tags: [dialogue, crafting, npc, standing-tiers, recipe-discovery, quality-variance]

requires:
  - phase: 06c-01
    provides: dialogue_definitions, standing tier thresholds, topic synonyms
  - phase: 06c-02
    provides: dialogue_engine functions, crafting_engine functions
  - phase: 06c-03
    provides: KnownTopicRecord, CharacterRecipe models
  - phase: 06c-04
    provides: dialogue and crafting commands

provides:
  - Comprehensive test suite for NPC dialogue system (30 tests)
  - Comprehensive test suite for crafting system (31 tests)
  - Regression guard for context packet interface (NPC-03)

affects: [phase-07-content, quest-system]

tech-stack:
  added: []
  patterns: [lazy-import-patch-at-source for unittest.mock]

key-files:
  created:
    - tests/test_dialogue.py
    - tests/test_crafting.py
  modified: []

key-decisions:
  - "Patch lazy imports at source module (world.mob_disposition, world.world_state) not at consumer module (world.dialogue_engine) -- consistent with Phase 05 decision"
  - "Used statistical assertions for quality variance tests (50+ iterations) to handle random.choices variance"
  - "Used unittest.TestCase for pure-logic tests, EvenniaTest only for model-backed operations (KnownTopicRecord, CharacterRecipe, room tags)"

patterns-established:
  - "Dialogue test pattern: mock get_mob_disposition at world.mob_disposition, mock get_betrayal at world.world_state"
  - "Context packet regression guard: explicit required_keys set checked via issubset"

requirements-completed: [NPC-01, NPC-02, NPC-03]

duration: 10min
completed: 2026-03-27
---

# Phase 06c Plan 05: NPC Dialogue and Crafting Tests Summary

**61 tests covering all dialogue requirements (NPC-01/02/03, D-04/D-05) and crafting requirements (D-15/16/17) with standing tier mapping, keyword extraction, quality variance, and recipe discovery validation**

## Performance

- **Duration:** 10 min
- **Started:** 2026-03-27T03:09:08Z
- **Completed:** 2026-03-27T03:18:42Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- 6 dialogue test classes covering standing tier mapping (all 8 tiers + betrayal), greeting resolution, topic priority stack, keyword extraction (4 stages), dynamic hints, and context packet interface stability
- 5 crafting test classes covering quality variance across skill/difficulty ranges, quality modifiers, recipe discovery lifecycle, registry data integrity, and station checks
- Regression guard for NPC-03: explicit key set validation ensures LLM context packet interface stability

## Task Commits

Each task was committed atomically:

1. **Task 1: Dialogue system tests** - `0b8202c` (test) -- 30 tests in 6 classes
2. **Task 2: Crafting system tests** - `0b8202c` (test) -- 31 tests in 5 classes

Note: Both tasks committed together due to worktree git object issues requiring branch-based commit from main repo.

## Files Created/Modified
- `tests/test_dialogue.py` - NPC dialogue system tests (NPC-01, NPC-02, NPC-03, D-04, D-05)
- `tests/test_crafting.py` - Crafting system tests (D-15, D-16, D-17)

## Decisions Made
- Patched lazy imports at source module per Phase 05 convention: `world.mob_disposition.get_mob_disposition` and `world.world_state.get_betrayal` instead of at `world.dialogue_engine`
- Used statistical assertions (50-100 iterations) for quality variance tests to handle `random.choices` variance while maintaining test reliability
- Mixed unittest.TestCase (pure logic) and EvenniaTest (model-backed) per project convention

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed unfriendly tier test threshold**
- **Found during:** Task 1 (Dialogue system tests)
- **Issue:** Test used disposition -0.5 expecting "unfriendly" tier, but threshold table maps -0.5 to "hostile" (unfriendly requires >= -0.4)
- **Fix:** Changed test value from -0.5 to -0.3 to match actual STANDING_TIER_THRESHOLDS behavior
- **Files modified:** tests/test_dialogue.py
- **Verification:** All 30 dialogue tests pass
- **Committed in:** 0b8202c

---

**Total deviations:** 1 auto-fixed (1 bug in test data)
**Impact on plan:** Test data correction only, no scope creep.

## Issues Encountered
- Worktree had corrupted git objects (missing blobs from concurrent worktree operations). Worked around by committing from main repo branch instead of worktree.
- Migration conflict between 0006_knowntopicrecord_characterrecipe and 0006_spawnrecord required merge migration (0007_merge) before test DB creation.

## Known Stubs
None -- all tests validate real production code, no stubs introduced.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All NPC dialogue and crafting systems fully tested and validated
- Phase 06c complete -- all 5 plans executed with test coverage
- Ready for content authoring phases

---
*Phase: 06c-npc-dialogue-and-crafting*
*Completed: 2026-03-27*
