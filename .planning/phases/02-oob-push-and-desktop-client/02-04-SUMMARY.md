---
phase: 02-oob-push-and-desktop-client
plan: "04"
subsystem: oob-tests
tags: [oob, tests, debounce, coordinates, cli-06, cli-07]
dependency_graph:
  requires:
    - world/oob_publisher.py (all 8 push_* functions, DEBOUNCE_INTERVALS, _should_send, _mark_sent)
    - world/area_builder.py (auto_layout_zone, DIRECTION_OFFSETS, grid_x/grid_y, world coords)
    - world/inventory_helpers.py (get_carry_state — patched in tests)
    - world/world_state.py (get_character_context_packet — patched in tests)
  provides:
    - tests/test_oob_publisher.py (28 tests for CLI-06: all 8 message types, debounce, session guard)
    - tests/test_area_builder.py (6 additional tests for CLI-07: explicit coords, auto-layout, world coords)
  affects:
    - Phase 2.1 Tauri client (tests document the OOB contract)
tech_stack:
  added: []
  patterns:
    - "unittest.TestCase with django.setup() at module level — avoids EvenniaTest DB overhead for pure-MagicMock tests"
    - "@patch on lazy-import paths (world.world_state.get_character_context_packet) — correct for oob_publisher's lazy import pattern"
    - "MagicMock character with sessions.all() and ndb.oob_debounce=None simulates connected player"
key_files:
  created:
    - tests/test_oob_publisher.py
  modified:
    - tests/test_area_builder.py
decisions:
  - "Used unittest.TestCase + django.setup() (not EvenniaTest) for test_oob_publisher — all characters are MagicMock so no DB objects needed; EvenniaTest.setUp hits SQLite under lock from running server"
  - "test_area_builder.py new classes use unique names (TestExplicitCoordsPreserved, TestAutoLayoutAllRoomsGetCoords, TestZoneWorldCoordsExtra) to avoid shadowing existing classes from plan 02-02"
  - "Plan's requested TestZoneWorldCoords and TestAutoLayoutAssignsCoords already existed from plan 02-02 execution; new classes cover the remaining test scenarios"
metrics:
  duration: "25 minutes"
  completed_date: "2026-03-25"
  tasks_completed: 2
  files_changed: 2
---

# Phase 02 Plan 04: OOB Publisher Test Suite Summary

Complete test suite for CLI-06 (OOB publisher) and CLI-07 (coordinate system): 28 tests for all 8 message types, debounce gate, and session guard in test_oob_publisher.py; 6 additional coordinate tests appended to test_area_builder.py.

## Tasks Completed

### Task 1: Create tests/test_oob_publisher.py — CLI-06 coverage

Created `tests/test_oob_publisher.py` with 28 tests organized into 9 test classes:

- **TestPushStatusUpdate** (5 tests): status_update kwarg present, dimensions dict, domains dict, no-send when disconnected, carried_scales
- **TestPushStatUpdate** (3 tests): stat_update kwarg, placeholder hp/conditions, session guard
- **TestPushNodeEvent** (2 tests): payload shape (zone_id/old_state/new_state), zero-interval sends twice
- **TestPushFlightProgress** (2 tests): leg_index/total_legs/destination, disembark_available True
- **TestPushCombatUpdate** (2 tests): passthrough payload, session guard
- **TestPushQuestUpdate** (1 test): passthrough payload
- **TestPushInventoryUpdate** (3 tests): items stub empty, encumbrance value, session guard
- **TestDebounceGate** (4 tests): first-call sends, within-window blocked, after-window allowed, node_event never debounced
- **TestSessionGuard** (2 tests): disconnected skips, connected sends
- **TestShouldSendHelper** (4 tests): None ndb returns True, within-window False, zero-interval True, after-expiry True

Commit: `ba47deb`

### Task 2: Add coordinate tests to tests/test_area_builder.py — CLI-07 coverage

Appended 3 new test classes (6 new tests) to `tests/test_area_builder.py`:

- **TestExplicitCoordsPreserved**: explicit coords preserved exactly after build(); mixed explicit+auto layout
- **TestAutoLayoutAllRoomsGetCoords**: all 5 rooms in a chain receive coords; up/down exits no collision
- **TestZoneWorldCoordsExtra**: fog_of_war defaults to False; world_x/world_y/world_radius/fog_of_war stored

Combined with the 8 coordinate tests added in plan 02-02, test_area_builder.py now has 14 coordinate-related tests total.

Commit: `106d0d0`

## Test Results

| File | Tests | Passed | Failed |
|------|-------|--------|--------|
| tests/test_oob_publisher.py | 28 | 28 | 0 |
| tests/test_area_builder.py (new tests only) | 6 | 6 | 0 |
| Combined (both files, evennia test runner) | 67 | 66 | 0* |

*1 pre-existing error: `test_named_mob_in_registry` fails with `OperationalError: database is locked` when Evennia server is running. Not introduced by this plan.

## Deviations from Plan

### Auto-fixed Issues

None — plan executed exactly as written, with minor adaptations:

**1. [Rule 2 - Missing functionality] Used unittest.TestCase instead of EvenniaTest for test_oob_publisher.py**
- **Found during:** Task 1 verification
- **Issue:** EvenniaTest.setUp tries to create real DB accounts/characters. With Evennia server running, SQLite is locked, causing setUp failures. All oob_publisher tests use MagicMock characters — no DB objects needed.
- **Fix:** Used `unittest.TestCase` with `django.setup()` at module level. `@patch` decorators work identically.
- **Files modified:** tests/test_oob_publisher.py
- **Impact:** Tests run via `pytest` directly (no evennia test runner required) for this file.

**2. [Rule 2 - Missing functionality] Used unique class names in test_area_builder.py to avoid shadowing**
- **Found during:** Task 2 implementation
- **Issue:** `TestAutoLayoutAssignsCoords` and `TestZoneWorldCoords` already existed in the file from plan 02-02 execution. Adding duplicate class names would silently shadow the existing classes.
- **Fix:** Used `TestExplicitCoordsPreserved`, `TestAutoLayoutAllRoomsGetCoords`, `TestZoneWorldCoordsExtra` as class names. Test scenarios are equivalent but non-duplicate.
- **Files modified:** tests/test_area_builder.py

## Known Stubs

None introduced in this plan.

## Self-Check: PASSED

Files verified:
- `tests/test_oob_publisher.py` — exists, 28 tests, all pass
- `tests/test_area_builder.py` — 3 new classes appended, 6 new tests, all pass

Commits verified:
- `ba47deb` — test(02-04): add CLI-06 test suite for oob_publisher — 28 tests
- `106d0d0` — test(02-04): add CLI-07 coordinate tests to test_area_builder — 6 new tests
