---
phase: 02-oob-push-and-desktop-client
plan: 03
subsystem: oob
tags: [evennia, oob, websocket, flight, node, xp]

# Dependency graph
requires:
  - phase: 02-01
    provides: oob_publisher.py with push_node_event, push_flight_progress, push_map_update, push_status_update
provides:
  - NodeScript._on_state_transition pushes node_event to all connected zone players
  - FlightScript._begin_leg pushes flight_progress on leg start (disembark_available=False)
  - FlightScript._arrive_at_stop pushes flight_progress on intermediate arrival (disembark_available=True)
  - FlightScript._arrive_final pushes flight_progress (complete) and map_update on landing
  - commit_session_xp pushes status_update after XP is written to DB
affects: [02-04, desktop-client]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Lazy import of oob_publisher inside methods to avoid circular imports"
    - "Append-only OOB hooks — all existing method logic unchanged, pushes added at end"
    - "Pitfall 6 mitigation: explicit push_map_update in _arrive_final so at_after_move suppression during flight is safe"

key-files:
  created: []
  modified:
    - world/scripts/node_script.py
    - world/scripts/flight_script.py
    - world/world_state.py

key-decisions:
  - "Intermediate stop uses leg index (current-1) after counter increment — leg was already advanced before disembark OOB push"
  - "Final landing push_flight_progress uses leg_index=total_legs (sentinel value) to signal completion to client"

patterns-established:
  - "OOB push at end of state-transition methods — never in the middle of existing logic"
  - "FlightRegistry import inside _arrive_at_stop is lazy (inside the else block), not duplicating module-level import"

requirements-completed: [CLI-06]

# Metrics
duration: 15min
completed: 2026-03-25
---

# Phase 02 Plan 03: OOB Hook Wiring Summary

**Wired OOB publisher into NodeScript state transitions, FlightScript leg traversal, and commit_session_xp — 3 files, 4 push call sites added.**

## Performance

- **Duration:** ~15 min
- **Started:** 2026-03-25T06:30:00Z
- **Completed:** 2026-03-25T06:45:00Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- NodeScript._on_state_transition now enumerates all connected zone players via `evennia.search_tag` and calls `push_node_event` for each at the end of the method
- FlightScript wired at all three leg events: `_begin_leg` (in-transit, disembark=False), `_arrive_at_stop` (intermediate, disembark=True), `_arrive_final` (complete + map refresh)
- `commit_session_xp` pushes `status_update` after all domain scores are written — client receives updated dimension/domain state automatically after each XP flush

## Task Commits

1. **Task 1: Wire node_event OOB push into NodeScript._on_state_transition()** - `9be29b1` (feat)
2. **Task 2: Wire flight_progress, map_update, and status_update OOB pushes** - `0b52f26` (feat)

## Files Created/Modified

- `world/scripts/node_script.py` - Added push_node_event call at end of _on_state_transition; iterates zone players via search_tag
- `world/scripts/flight_script.py` - Added push_flight_progress in _begin_leg and _arrive_at_stop; added push_flight_progress + push_map_update in _arrive_final
- `world/world_state.py` - Added push_status_update at end of commit_session_xp after all DB writes complete

## Decisions Made

- Intermediate stop uses `leg_index = current - 1` because `self.db.current_leg` is already incremented before the OOB push in `_arrive_at_stop`. The push reflects the leg that was just completed.
- Final landing sends `leg_index=total_legs` (equal to total_legs) as a sentinel value to signal journey completion to the client — this is intentional, not an off-by-one.
- `from world.flight_registry import FlightRegistry` import in `_arrive_at_stop` is placed inside the `else` block (intermediate stop path only) — avoids double-import since the final stop path does not need it.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- All three event-driven game systems now emit OOB messages to connected clients
- Plan 02-04 (desktop client protocol) can now define client-side handlers for `node_event`, `flight_progress`, `map_update`, and `status_update` knowing they will fire at the correct game moments
- No blockers

---
*Phase: 02-oob-push-and-desktop-client*
*Completed: 2026-03-25*
