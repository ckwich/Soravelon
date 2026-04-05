---
phase: 16-architectural-refactoring
plan: 03
subsystem: combat
tags: [refactoring, combat-engine, status-effects, helper-extraction]

# Dependency graph
requires:
  - phase: 06a-base-attributes-and-combat
    provides: "combat_engine.py and status_effects.py with inline duplicate logic"
provides:
  - "_compute_raw_damage helper consolidating weapon/mob damage branches"
  - "_find_effect helper consolidating effect list search loops"
affects: [combat-system, status-effects]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Private helper extraction into owning module (no utils.py)", "Unified return tuples for damage (int, str) and effect search (entry, idx)"]

key-files:
  created: []
  modified: [world/combat_engine.py, world/status_effects.py]

key-decisions:
  - "No threshold patterns duplicated across modules (D-09 scan clean) -- each if/elif chain is unique to its domain"
  - "Helpers are underscore-prefixed private functions in owning modules per D-10"

patterns-established:
  - "Private helper extraction: duplicate branches become single helper with tuple return"

requirements-completed: [D-08, D-09, D-10]

# Metrics
duration: 2min
completed: 2026-04-05
---

# Phase 16 Plan 03: Consolidate Duplicate Logic Summary

**Extracted _compute_raw_damage and _find_effect private helpers to eliminate inline duplicate branches in combat_engine.py and status_effects.py**

## Performance

- **Duration:** 2 min
- **Started:** 2026-04-05T17:52:37Z
- **Completed:** 2026-04-05T17:54:41Z
- **Tasks:** 1
- **Files modified:** 2

## Accomplishments
- Consolidated character vs mob weapon damage computation into `_compute_raw_damage(attacker, weapon)` returning `(raw_damage, element)` tuple
- Consolidated effect list search into `_find_effect(effects, effect_type)` returning `(entry, index)` tuple
- Replaced inline loops in `_apply_stackable` and `_apply_non_stackable` with `_find_effect` calls
- Replaced inline damage branches in `resolve_basic_attack` with `_compute_raw_damage` call
- Scanned all `world/*.py` for duplicated threshold patterns (D-09); none found -- each is unique to its domain

## Task Commits

Each task was committed atomically:

1. **Task 1: Consolidate weapon damage fallback and effect list search** - `05d2ce3` (refactor)

## Files Created/Modified
- `world/combat_engine.py` - Added `_compute_raw_damage` helper, replaced inline branches in `resolve_basic_attack`
- `world/status_effects.py` - Added `_find_effect` helper, replaced inline loops in `_apply_stackable` and `_apply_non_stackable`

## Decisions Made
- No threshold patterns found duplicated across modules (D-09 scan: only `mob_disposition.py` has a trust threshold chain, unique to that domain) -- no extraction needed
- Helpers stay as private underscore-prefixed functions in their owning module per D-10; no utils.py created

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- 6 pre-existing test failures in `test_status_effects.py` (compound trigger and DoT tests) confirmed present on unmodified main branch; not caused by this refactoring

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- combat_engine.py and status_effects.py are cleaner with consolidated helpers
- No behavioral changes; all existing callers work identically

## Self-Check: PASSED

- FOUND: world/combat_engine.py
- FOUND: world/status_effects.py
- FOUND: commit 05d2ce3
- CONFIRMED: _compute_raw_damage defined 1x in combat_engine.py
- CONFIRMED: _find_effect defined 1x in status_effects.py
- CONFIRMED: no world/utils.py

---
*Phase: 16-architectural-refactoring*
*Completed: 2026-04-05*
