---
phase: 06a-base-attributes-and-combat
plan: 05
subsystem: combat
tags: [evennia-script, initiative, turn-based, combat-state-machine, charged-abilities]

requires:
  - phase: 06a-03
    provides: combat_engine damage resolution, crit system, death handling
  - phase: 06a-04
    provides: combat_ai mob turn AI, ability selection, targeting

provides:
  - CombatScript room-attached state machine with initiative-ordered turns
  - start_combat and join_combat module-level entry points
  - Round management with effect ticking and cooldown decrement
  - Charged ability lifecycle (declare, charge, auto-fire)
  - Group combat timeout with auto-attack fallback

affects: [06a-06, 06a-07, 06b, combat-commands]

tech-stack:
  added: []
  patterns:
    - "Dynamic typeclass construction to avoid import-time Evennia resolution"
    - "Event-driven script (interval=0) with persistent=True for reload survival"
    - "db.active_effects_db mirror for ndb effect persistence across reload"

key-files:
  created:
    - world/combat_script.py
  modified: []

key-decisions:
  - "CombatScript uses dynamic type() subclassing to avoid Evennia import-time typeclass resolution"
  - "Timer cancellation uses deferred.cancel() from Evennia delay() return value"
  - "Tasks 1 and 2 implemented atomically in single file (natural code boundary)"

patterns-established:
  - "Combat script pattern: interval=0 event-driven, persistent=True, db effects mirror"

requirements-completed: [CMB-01, CMB-04]

duration: 5min
completed: 2026-03-26
---

# Phase 06a Plan 05: Combat Script Summary

**Room-attached CombatScript orchestrates turn-based combat with initiative-ordered interleaving, charged abilities, group timeout, and reload-safe state persistence**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-26T19:07:35Z
- **Completed:** 2026-03-26T19:12:46Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- CombatScript manages full combat lifecycle: creation, turns, rounds, death, cleanup
- Initiative-ordered interleaved turns (D-15) with stun/charm skip logic
- Charged ability lifecycle: declare, auto-attack during charge, auto-fire on completion (D-10)
- Group combat round timeout with auto-attack fallback (D-18)
- Combat state survives server reload via db.active_effects_db mirror (Pitfall 1)

## Task Commits

Each task was committed atomically:

1. **Task 1: CombatScript lifecycle, state, and combatant management** - `0c74d3c` (feat)
2. **Task 2: Turn processing, round management, and charged abilities** - `b58fa4b` (feat)

## Files Created/Modified
- `world/combat_script.py` - CombatScript class with start_combat/join_combat module-level functions, full turn/round management

## Decisions Made
- CombatScript uses dynamic `type()` subclassing to avoid Evennia import-time typeclass resolution (same pattern as other world/ modules)
- Timer cancellation uses `deferred.cancel()` from Evennia `delay()` return value
- Both tasks implemented in single file creation pass since code is naturally cohesive

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Fixed worktree sparse-checkout corruption**
- **Found during:** Task 2 commit
- **Issue:** `git sparse-checkout disable` expanded index to include GSD plugin submodule objects that are not present in worktree
- **Fix:** Deleted corrupt index and regenerated via `git reset --mixed HEAD`
- **Files modified:** None (git infrastructure only)
- **Verification:** `git status --short` works correctly after reset

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Git infrastructure fix only. No scope creep.

## Issues Encountered
- Worktree sparse-checkout corruption required index rebuild -- resolved by deleting index file and running `git reset --mixed HEAD`

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- CombatScript ready for combat command integration (Plan 06)
- OOB combat_update push wired via oob_publisher
- Integrates combat_engine, combat_ai, status_effects, and ability_engine

---
*Phase: 06a-base-attributes-and-combat*
*Completed: 2026-03-26*
