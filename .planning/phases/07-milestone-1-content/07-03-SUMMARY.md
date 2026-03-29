---
phase: 07-milestone-1-content
plan: 03
subsystem: mob-ai
tags: [wander, mob-movement, ticker, stochastic]

# Dependency graph
requires:
  - phase: 03.1-mob-spawn-runtime
    provides: "mob_spawner spawn_single_mob, SoravelonMob typeclass"
provides:
  - "wander_system.py with wander_mob() and wander_tick()"
  - "wanderer tag on mobs with db.wander=True for efficient lookup"
  - "TICKER_HANDLER registration for 60s wander tick"
affects: [zone-content, mob-templates, starter-zones]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Tag-based mob lookup for batch tick processing", "Stochastic tick chance (40%) for organic movement"]

key-files:
  created:
    - world/wander_system.py
    - tests/test_wander_system.py
  modified:
    - server/conf/at_server_startstop.py
    - world/mob_spawner.py

key-decisions:
  - "Used wanderer tag (category=mob_behavior) for efficient search_tag lookup instead of iterating all mobs"
  - "40% stochastic chance per 60s tick = average movement every 2.5 minutes"
  - "Patrol script takes priority over wandering -- mob cannot do both"

patterns-established:
  - "Mob behavior tags in mob_behavior category for batch tick queries"
  - "Guard chain pattern: wander flag -> combat -> patrol -> dead -> location -> valid exits"

requirements-completed: [CON-02]

# Metrics
duration: 3min
completed: 2026-03-29
---

# Phase 7 Plan 03: Wandering Mob System Summary

**Tick-driven wandering mob system with zone-boundary-aware random movement, 40% stochastic chance, and 5-guard skip chain**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-29T22:55:09Z
- **Completed:** 2026-03-29T22:58:00Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Wandering mob system that moves mobs with db.wander=True to random connected rooms
- Guard chain prevents movement during combat, patrol, death, or to invalid rooms (no_mobs, cross-zone)
- Wander tick registered in TICKER_HANDLER at 60s interval with 40% per-mob chance
- Wanderer tag added at spawn time for efficient batch lookup
- 15 unit tests (unittest.TestCase + MagicMock) all passing

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement wandering mob system (TDD)** - `97c2193` (feat)
2. **Task 2: Register wander tick in server startup** - `8d98ab3` (feat)

_Note: TDD RED+GREEN combined in single commit due to worktree corruption requiring repo switch_

## Files Created/Modified
- `world/wander_system.py` - wander_mob() single mob movement + wander_tick() batch tick function
- `tests/test_wander_system.py` - 15 unit tests covering all guard conditions and tick behavior
- `server/conf/at_server_startstop.py` - Added TICKER_HANDLER registration for wander_tick (60s)
- `world/mob_spawner.py` - Added wanderer tag in spawn_single_mob after apply_mob_template

## Decisions Made
- Used tag-based lookup (search_tag "wanderer") instead of iterating all mobs -- consistent with spawn system patterns
- 40% movement chance per tick creates organic feel without overwhelming movement
- Patrol scripts take strict priority over wandering -- a mob cannot do both simultaneously
- Used unittest.TestCase + MagicMock (not EvenniaTest) for pure-logic module with no DB dependency

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Worktree git corruption (invalid object errors) required switching to main repo for commits. No impact on code quality.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Wandering system ready for zone content authoring -- mobs with db.wander=True will automatically wander
- Mob template registry (07-02) can set wander=True in template definitions
- Zone content plans can use wander flag in spawn definitions

---
*Phase: 07-milestone-1-content*
*Completed: 2026-03-29*
