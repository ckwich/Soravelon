---
phase: "01"
plan: "05"
subsystem: flight-system
tags:
  - flight
  - dragon-courier
  - fast-travel
  - commands
  - tdd
dependency_graph:
  requires:
    - "01-03: flight_registry.py + AreaBuilder flight_point()/flight_route()"
    - "01-04: FlightRegistry singleton with register_point, find_route_legs, get_route"
    - "world/banking.py: withdraw(), get_balance()"
    - "world/world_state.py: get_standing()"
    - "typeclasses/characters.py: db.discovered_flight_points, ndb.in_flight"
  provides:
    - "world/flight_engine.py: fare_for_route(), book_flight()"
    - "world/scripts/flight_script.py: FlightScript per-player state machine"
    - "commands/cmd_fly.py: CmdFly, CmdDisembark, CmdFlightRoutes"
    - "typeclasses/characters.py: at_before_move() flight block (D-12)"
    - "typeclasses/rooms.py: auto-discovery on room enter (D-08)"
  affects:
    - "commands/default_cmdsets.py: CharacterCmdSet gains 3 flight commands"
    - "typeclasses/rooms.py: at_object_receive extended with flight discovery"
    - "typeclasses/rooms.py: at_object_creation initializes db.flight_point_id"
tech_stack:
  added:
    - "evennia.utils.utils.delay() — all leg timers in FlightScript"
  patterns:
    - "(bool, str) return tuple on all engine functions"
    - "Lazy import inside functions to avoid circular deps (flight_engine, flight_script)"
    - "sys.modules injection for pure-logic tests (no Evennia/Django DB setup)"
    - "SaverDict copy pattern for discovered_flight_points set mutation"
key_files:
  created:
    - "world/flight_engine.py"
    - "world/scripts/flight_script.py"
    - "commands/cmd_fly.py"
    - "tests/test_flight_engine.py"
  modified:
    - "commands/default_cmdsets.py"
    - "typeclasses/characters.py"
    - "typeclasses/rooms.py"
decisions:
  - "sys.modules injection used for flight tests (same approach as command_preprocessor tests) — world.world_state and world.banking can't be patched via string path without Django setup; inject stubs into sys.modules before module-level import"
  - "D-08 NPC booking gate deferred to content phase — discovery alone unlocks flight booking for this phase"
  - "db.flight_point_id added to SoravelonRoom.at_object_creation (Rule 2 auto-add) — plan comment specified initialization but at_object_creation lacked the attribute"
metrics:
  duration: "5 minutes"
  completed_date: "2026-03-24T23:21:25Z"
  tasks_completed: 2
  files_changed: 7
---

# Phase 01 Plan 05: Dragon Courier Flight System Summary

**One-liner:** Delay-based multi-leg Dragon Courier with 4-tier Consortium Standing discount, fare_paid reload guard, and auto-discovery on room enter.

## What Was Built

The Dragon Courier flight system is Soravelon's primary fast-travel mechanic — multi-leg timed traversal with Standing-based pricing and mid-journey disembark.

### Task 1: Flight Engine + FlightScript (TDD)

**world/flight_engine.py:**
- `fare_for_route(character, legs)` — sums `base_fare` across legs, applies Consortium Standing discount (0-24=0%, 25-49=10%, 50-74=20%, 75-100=30%), floors to int, never negative
- `book_flight(character, origin_id, dest_id)` — validates points exist, finds BFS route, checks discovery gate (D-08), checks/deducts balance via `banking.withdraw()`, creates FlightScript, calls `start_journey()`, returns `(bool, str)`

**world/scripts/flight_script.py:**
- `FlightScript(SoravelonScript)` — persistent, interval=0 (not self-ticking), uses `evennia.utils.utils.delay()` for all timers
- `at_script_creation()` — `db.fare_paid = False` (Pitfall 6: no double-deduction on server reload)
- `start_journey()` — sets `ndb.in_flight = True`, sends departure message, begins first leg
- `_begin_leg()` — sends destination announcement, schedules mid-leg echo delays, schedules `_arrive_at_stop` via `delay(leg_duration, ...)`
- `_arrive_at_stop()` — moves player via `move_to()`, at intermediate stops gives 10-second disembark window via `delay(10, _check_continue)` (D-11)
- `_arrive_final()` — clears `ndb.in_flight`, sends landing message, calls `self.stop()`
- `do_disembark()` — called by CmdDisembark; clears `ndb.in_flight`, stops script

### Task 2: Flight Commands + Character/Room Wiring

**commands/cmd_fly.py:**
- `CmdFly` — checks `ndb.in_flight` and `here.db.flight_point_id` directly (no getattr); with no args lists reachable discovered destinations with fare estimates; with arg books flight to named destination via prefix match
- `CmdDisembark` — finds `flight_script` on character, calls `do_disembark()`; graceful cleanup if script gone
- `CmdFlightRoutes` (alias: `flightroutes`) — lists all discovered stops

**commands/default_cmdsets.py:** CharacterCmdSet now includes CmdFly, CmdDisembark, CmdFlightRoutes.

**typeclasses/characters.py:** `at_before_move()` now checks `ndb.in_flight` first — returns False with "You cannot move while aboard the Dragon Courier." message (D-12). Then falls through to existing overloaded inventory check.

**typeclasses/rooms.py:**
- `at_object_creation()` — now initializes `db.flight_point_id = None`
- `at_object_receive()` — after trigger firing, checks `self.db.flight_point_id`; if truthy and not already discovered, adds to `character.db.discovered_flight_points` set (SaverDict copy pattern) and sends discovery notification (D-08)

## Tests

21 tests in `tests/test_flight_engine.py`:
- `TestFareForRoute` (11 tests): all 4 discount tiers, multi-leg sum before discount, rounding, negative-zero guard
- `TestBookFlight` (8 tests): origin/destination validation, discovery gate, balance check, withdraw call, payment failure
- `TestFlightScriptImportable` (2 tests): importability, required method presence

Test approach: `sys.modules` injection to stub `world.world_state` and `world.banking` before import (avoids Django setup). Same pattern as `test_command_preprocessor.py`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Init] Added db.flight_point_id to SoravelonRoom.at_object_creation**
- **Found during:** Task 2
- **Issue:** Plan comment stated "db.flight_point_id initialized None in at_object_creation" but the attribute was missing from SoravelonRoom.at_object_creation
- **Fix:** Added `self.db.flight_point_id = None` with explanatory comment
- **Files modified:** typeclasses/rooms.py
- **Commit:** 706a0f8

**2. [Rule 2 - Test Approach] sys.modules injection for pure-logic tests**
- **Found during:** Task 1 RED phase
- **Issue:** Plan's TDD tests used `patch("world.world_state.get_standing", ...)` but `world.world_state` imports Django models at module level, requiring Django setup. Pure unittest.TestCase can't trigger Django setup.
- **Fix:** Inject stubs into `sys.modules` before any import of `world.flight_engine` or `world.scripts.flight_script`. Same pattern proven in other pure-logic test modules.
- **Files modified:** tests/test_flight_engine.py
- **Commit:** 528add5

### Deferred Items (from plan frontmatter)

**D-08 NPC Booking Gate:** NPC interaction requirement deferred to content phase. Discovery alone unlocks flight booking. Dragon Courier NPC will wire in during NPC dialogue (open_dialogue action) implementation.

## Known Stubs

None — all exported functions are fully implemented. Discovery set is properly persisted via SaverDict copy. fare_paid flag prevents double-deduction across server reloads.

## Self-Check

Verified files exist:
- world/flight_engine.py: created
- world/scripts/flight_script.py: created
- commands/cmd_fly.py: created
- tests/test_flight_engine.py: created (21 tests passing)
- commands/default_cmdsets.py: modified
- typeclasses/characters.py: modified
- typeclasses/rooms.py: modified

Verified commits:
- 06ec123: test(01-05) — RED tests
- 528add5: feat(01-05) — flight_engine.py + flight_script.py
- 706a0f8: feat(01-05) — cmd_fly.py + wiring
