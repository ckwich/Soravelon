---
phase: 01-patrol-commands-and-flight-paths
plan: 02
subsystem: patrol-engine
tags: [patrol, mobs, rooms, bfs, disposition, scripts]
dependency_graph:
  requires:
    - world/mob_disposition.py (get_mob_behavior)
    - world/node_helpers.py (get_rooms_in_radius)
    - typeclasses/scripts.py (SoravelonScript)
  provides:
    - world/patrol_engine.py (find_path, next_patrol_step, check_patrol_encounter, echo_to_radius)
    - world/scripts/patrol_script.py (PatrolScript)
    - typeclasses/mobs.py extended with patrol db attrs and at_death trigger hook
    - typeclasses/rooms.py extended with at_object_receive/at_object_leave trigger and patrol hooks
  affects:
    - world/trigger_engine.py (lazy import — will fail at runtime until plan 01-01 delivers it)
    - world/area_builder.py (patrol() method will attach PatrolScript and set db.patrol)
tech_stack:
  added: []
  patterns:
    - BFS with parent-pointer backtracking (same pattern as get_rooms_in_radius)
    - SaverDict copy pattern for route_ids and patrol_def mutation
    - Lazy import of get_mob_behavior at module-level for test patchability
    - Pitfall 2 guard: PatrolScript.at_repeat() stops self if mob is deleted
key_files:
  created:
    - world/patrol_engine.py
    - world/scripts/patrol_script.py
    - tests/test_patrol_engine.py
  modified:
    - typeclasses/mobs.py (added db.patrol, db.combat_enabled, db.triggers, extended at_death)
    - typeclasses/rooms.py (added db.triggers, db.custom_commands, at_object_receive, at_object_leave)
decisions:
  - get_mob_behavior imported at patrol_engine module level (not lazy) to enable test patching via patch("world.patrol_engine.get_mob_behavior")
  - trigger_engine calls in mobs.py and rooms.py guarded by if self.db.triggers — safe until plan 01-01 delivers the module
  - _check_mob_encounter_for_arrival is module-level helper (not class method) per plan spec
metrics:
  duration_minutes: 7
  completed_date: "2026-03-24"
  tasks_completed: 2
  tasks_total: 2
  files_created: 3
  files_modified: 2
---

# Phase 01 Plan 02: Patrol Engine + Script Hooks Summary

**One-liner:** BFS patrol pathfinder, tick-driven PatrolScript, and mob/room trigger hooks for city-life patrol mobs.

## What Was Built

### Task 1: Patrol Engine (TDD)

`world/patrol_engine.py` — four exports:

- `find_path(start, target, max_depth=20)`: BFS from start to target respecting zone_id boundaries. Uses parent-pointer dict for O(n) backtracking. Returns [] if target is unreachable, in a different zone, or beyond max_depth.
- `next_patrol_step(mob, route_ids, current_index)`: Advances route with wrap-around. Returns `(room, next_index)` or `(None, current_index)` on empty route / missing room.
- `check_patrol_encounter(mob, room)`: Returns True if any player in room triggers aggressive/territorial behavior. Respects `mob.db.combat_enabled = False` for invulnerable mobs (D-03, e.g., Caldenmere).
- `echo_to_radius(mob, message, radius)`: Broadcasts to all rooms within BFS radius of mob's location (D-04).

TDD: 15 tests written RED first, then GREEN. All 15 passing.

### Task 2: PatrolScript + Mob/Room Hooks

`world/scripts/patrol_script.py` — `PatrolScript(SoravelonScript)`:
- `at_script_creation()`: key=patrol_script, persistent=True, interval=5, repeats=0, tagged patrol_script
- `at_repeat()`: Guards deleted mob (Pitfall 2), skips when interrupted
- `_advance_route()`: Calls next_patrol_step, moves mob, optionally echoes, handles encounter_delay (D-01)
- `_initiate_combat()`: Sets interrupted=True, fires attack command on first hostile player
- `on_combat_end(outcome)`: Handles resume/reset_to_start/abandon interrupt modes

`typeclasses/mobs.py` extended:
- `at_object_creation()` adds: `db.patrol=None`, `db.combat_enabled=True`, `db.triggers=[]`
- `at_death()` now fires `on_mob_death` triggers when `db.triggers` is non-empty

`typeclasses/rooms.py` extended:
- `at_object_creation()` adds: `db.triggers=[]`, `db.custom_commands=[]`
- `at_object_receive()` fires `on_enter` + `on_first_visit` triggers for players; checks patrol mobs (D-02)
- `at_object_leave()` fires `on_exit` triggers for players
- Module-level `_check_mob_encounter_for_arrival()` helper for D-02 delayed encounter checks

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Test patching target for get_mob_behavior**
- **Found during:** Task 1 GREEN phase
- **Issue:** Tests used `patch("world.mob_disposition.get_mob_behavior")` but this forced import of `world.mob_disposition` which cascades to `world.models` and fails without full Django app registry under `evennia.settings_default`.
- **Fix:** Moved `get_mob_behavior` import to patrol_engine module level so tests can patch `world.patrol_engine.get_mob_behavior` without triggering the cascading import.
- **Files modified:** `world/patrol_engine.py`, `tests/test_patrol_engine.py`
- **Commit:** 3fe1211

## Known Stubs

- `fire_triggers` calls in `mobs.py` and `rooms.py` are guarded by `if self.db.triggers:` — safe no-ops until `world/trigger_engine.py` is delivered by plan 01-01. No stub text exposed to players.

## Self-Check: PASSED

Files created:
- world/patrol_engine.py — FOUND
- world/scripts/patrol_script.py — FOUND
- tests/test_patrol_engine.py — FOUND

Files modified:
- typeclasses/mobs.py — FOUND (at_death at line 140, db.patrol/combat_enabled/triggers added)
- typeclasses/rooms.py — FOUND (at_object_receive at line 57, db.triggers/custom_commands added)

Commits:
- 3e530cd: test(01-02): add failing tests (RED)
- 3fe1211: feat(01-02): patrol_engine implementation (GREEN)
- 3fa9057: feat(01-02): PatrolScript, SoravelonMob patrol attrs, SoravelonRoom trigger/patrol hooks
