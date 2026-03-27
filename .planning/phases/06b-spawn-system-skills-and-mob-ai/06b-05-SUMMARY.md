---
phase: 06b-spawn-system-skills-and-mob-ai
plan: 05
subsystem: testing
tags: [unittest, mock, spawn-record, skill-engine, combat-ai, casting-time, hunter-chase]

requires:
  - phase: 06b-01
    provides: SpawnRecord model, spawn_tick, schedule_respawn_from_death
  - phase: 06b-02
    provides: Skill definitions, skill engine (accumulate, practice, train, discover)
  - phase: 06b-04
    provides: Combat AI casting time, new conditions, is_hunter chase
provides:
  - Automated test coverage for SpawnRecord lifecycle
  - Automated test coverage for skill engine (SKL-01 through SKL-04)
  - Automated test coverage for combat AI extensions (CMB-04)
affects: [regression-prevention, future-combat-changes, future-skill-changes]

tech-stack:
  added: []
  patterns: [patch-at-source-model for lazy Django imports, django.setup() in test modules]

key-files:
  created:
    - tests/test_spawn_record.py
    - tests/test_skill_engine.py
  modified:
    - tests/test_combat_ai.py

key-decisions:
  - "Patch Django model managers at world.models.X.objects (not world.module.X) for lazy-imported models"
  - "django.setup() required at module level in test files that touch real Django model metaclass"
  - "Fixed pre-existing test_condition_checked bug (missing abilities arg to _make_mob)"

patterns-established:
  - "Lazy import patching: patch at world.models.ModelName.objects for functions using from world.models import X"
  - "NdbProxy class pattern for MagicMock character ndb that supports setattr/getattr correctly"

requirements-completed: [SKL-01, SKL-02, SKL-03, SKL-04, CMB-04]

duration: 18min
completed: 2026-03-26
---

# Phase 06b Plan 05: Test Suite Summary

**75 automated tests covering SpawnRecord lifecycle, skill engine (passive/practice/diminishing/seeds), and combat AI (casting time, 6 new conditions, hunter chase)**

## Performance

- **Duration:** 18 min
- **Started:** 2026-03-26T23:52:26Z
- **Completed:** 2026-03-27T00:10:07Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- test_spawn_record.py: 14 tests covering death hook (mob removal, respawn scheduling, noop guard), spawn_tick (due processing, error resilience), _process_spawn_record (spawn + update, condition reschedule, missing room), initialize_spawn_records (per-def creation, idempotency), named mob death, and model field/constraint validation
- test_skill_engine.py: 30 tests covering get_skill_value (learned/unlearned), passive accumulation (ndb increment, no DB write), commit_skill_accumulators (gain applied, remainder preserved, threshold guard), diminishing returns (all 5 brackets + above-100), practice_skill (success, cooldown, 24hr reset, unknown skill), practice gains by tier, profession skills (SKL-02), animal handling (SKL-03), skill domain independence (SKL-04), ancestry seeds (human/kauroran/selvar winter/summer), discovery framework (trigger + no duplicate), and trainer sessions (cost/bonus/insufficient funds)
- test_combat_ai.py: Extended from 10 to 31 tests with new conditions (target_rooted, target_blinded, no_target_dot, pack_present, hp_below_50, hp_below_25), casting time (start, register, resolve, decrement), cast interrupt (stun + root), and hunter chase (BFS move, out-of-range, non-hunter guard)

## Task Commits

Each task was committed atomically:

1. **Task 1: SpawnRecord and skill engine tests** - `f7736d8` (test)
2. **Task 2: Combat AI extension tests** - `fa8eac4` (test)

## Files Created/Modified
- `tests/test_spawn_record.py` - 14 tests for SpawnRecord lifecycle
- `tests/test_skill_engine.py` - 30 tests for skill engine (all SKL requirements)
- `tests/test_combat_ai.py` - Extended with 21 new tests for casting time, conditions, hunter chase

## Decisions Made
- Patch Django model managers at `world.models.X.objects` for lazy-imported models (patching at consumer module fails because the import happens inside function bodies)
- Added `django.setup()` at module level in all three test files to allow Django model metaclass resolution (needed for `CharacterSkill.DoesNotExist`, `SpawnRecord._meta` introspection)
- Fixed pre-existing bug in test_condition_checked: `_make_mob()` was called without `abilities` arg, causing empty abilities list and always falling back to basic_attack

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed test_condition_checked pre-existing bug**
- **Found during:** Task 2 (combat AI extension tests)
- **Issue:** Existing test created abilities list but passed no argument to `_make_mob()`, so mob had empty abilities
- **Fix:** Added `abilities=abilities` argument to `_make_mob()` call
- **Files modified:** tests/test_combat_ai.py
- **Verification:** Test now passes — condition correctly gates execute ability
- **Committed in:** fa8eac4

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Pre-existing test bug fix, no scope creep.

## Issues Encountered
- Worktree git object store corrupted by sparse checkout of GSD tool files (`.claude-plugin/`, `.gitattributes`). Commits made on main branch directly. Tests verified from both worktree and main.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- All Phase 06b requirements have automated test coverage
- SpawnRecord lifecycle, skill engine, and combat AI extensions verified
- Phase 06b test suite complete — ready for phase transition

---
*Phase: 06b-spawn-system-skills-and-mob-ai*
*Completed: 2026-03-26*
