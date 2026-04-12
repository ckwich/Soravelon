---
phase: 17-area-reconciliation-and-test-env
plan: 03
subsystem: area-builder-reconciliation-tests
tags: [testing, reconciliation, area-builder, tdd]
dependency_graph:
  requires: [17-01, 17-02]
  provides: [reconciliation-test-coverage]
  affects: [world/area_builder.py, tests/test_area_builder.py]
tech_stack:
  added: []
  patterns: [AreaBuilderTestBase, EvenniaTest, reconciliation-rebuild-pattern]
key_files:
  created: []
  modified:
    - tests/test_area_builder.py
    - world/area_builder.py
decisions:
  - "Used rebuild-pattern for reconciliation tests: build zone, then rebuild with modified spec and assert deletions"
  - "Fixed 3 bugs in _reconcile_stale_objects discovered by test execution"
metrics:
  duration: "34 minutes"
  completed: "2026-04-12"
  tasks_completed: 1
  tasks_total: 1
  files_modified: 2
---

# Phase 17 Plan 03: Reconciliation Test Suite Summary

Add 10 reconciliation test methods to tests/test_area_builder.py covering all decision points (D-01 through D-06) plus runtime mob exemption and on_examine trigger validation. Fixed 3 bugs in _reconcile_stale_objects discovered during test execution.

## Tasks Completed

### Task 1: Reconciliation test suite

Added `TestReconciliation` class with 10 test methods to `tests/test_area_builder.py`:

| Test Method | Decision | What It Verifies |
|---|---|---|
| `test_orphan_room_deleted_on_rebuild` | D-01 | Room removed from spec is hard-deleted |
| `test_player_evicted_from_deleted_room` | D-01 | Player moved to respawn_point with message |
| `test_orphan_exit_deleted_on_rebuild` | D-02 | Exit removed from spec is hard-deleted |
| `test_orphan_npc_deleted_on_rebuild` | D-03 | NPC removed from spec is hard-deleted |
| `test_builder_mob_deleted_on_rebuild` | D-03 | Builder mob() object removed from spec is deleted |
| `test_runtime_mob_preserved_on_rebuild` | D-04 | Runtime-spawned mob (MOB_INSTANCE_TAG_CATEGORY) preserved |
| `test_crafting_station_tag_cleared_on_rebuild` | D-05 | Crafting station tags cleared on room rebuild |
| `test_exit_attr_reset_on_rebuild` | D-06 | Exit requires_ancestry reset to None when removed from spec |
| `test_build_report_contains_reconciled_key` | - | build() return dict includes reconciled counts |
| `test_on_examine_trigger_accepted` | - | on_examine event passes validation |

**Commit:** `ce00b27`

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] DEFAULT_HOME '#N' format causes ValueError in _reconcile_stale_objects**
- **Found during:** Task 1 (all build() tests failing)
- **Issue:** `django_settings.DEFAULT_HOME` is `'#2'` (Evennia dbref format) but code passed it directly to `ObjectDB.objects.get(id=fallback_id)` which expects an integer
- **Fix:** Strip '#' prefix and convert to int with try/except for ValueError/TypeError
- **Files modified:** world/area_builder.py
- **Commit:** ce00b27

**2. [Rule 1 - Bug] hasattr(obj, 'destination') crashes on stale objects**
- **Found during:** Task 1 (all build() tests failing)
- **Issue:** `hasattr(obj, 'destination')` triggers Evennia's lazy FK resolution which raises `ObjectDoesNotExist` for objects whose destination has been deleted, causing the entire reconciliation sweep to abort
- **Fix:** Use `isinstance(obj, SoravelonExit)` as primary check, with try/except fallback for destination access
- **Files modified:** world/area_builder.py
- **Commit:** ce00b27

**3. [Rule 1 - Bug] mob() method missing zone_id tag**
- **Found during:** Task 1 (test_builder_mob_deleted_on_rebuild failing)
- **Issue:** `mob()` sets `mob_obj.db.zone_id` but never adds the `zone_id` tag via `tags.add()`. Since `_reconcile_stale_objects` finds zone objects via `search_tag(zone_id, category="zone_id")`, builder mobs were invisible to the reconciliation sweep
- **Fix:** Added `mob_obj.tags.add(self._zone_id, category="zone_id")` to `mob()` method
- **Files modified:** world/area_builder.py
- **Commit:** ce00b27

## Test Results

- `evennia test --settings settings tests.test_area_builder.TestReconciliation`: **10 tests, 0 failures, 0 errors**
- `evennia test --settings settings tests.test_area_builder`: **72 tests, 1 pre-existing error** (test_second_pass_resolves_cross_zone_exit uses `__new__` without `__init__`, missing `_exit_ids` attr from Plan 17-01)
- Full suite (`tests/`): 447 errors are pre-existing Evennia harness issues (documented in 17-CONTEXT.md as D-07/D-08 scope for Plan 17-02)

## Deferred Issues

- `test_second_pass_resolves_cross_zone_exit` broken by Plan 17-01's addition of `_exit_ids` tracking to `_create_exit_object`. The test creates a raw AreaBuilder via `__new__` without `__init__`, so `_exit_ids` is missing. Fix: either initialize `_exit_ids` in `_create_exit_object` or update the test to use proper initialization.

## Self-Check: PASSED

- FOUND: tests/test_area_builder.py (contains TestReconciliation with 10 test methods)
- FOUND: world/area_builder.py (3 bug fixes applied)
- FOUND: ce00b27 (commit exists)
