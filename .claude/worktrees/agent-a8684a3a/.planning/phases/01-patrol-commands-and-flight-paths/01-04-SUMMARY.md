---
phase: 01-patrol-commands-and-flight-paths
plan: "04"
subsystem: area-builder
tags:
  - area-builder
  - patrol
  - triggers
  - custom-commands
  - flight-registry
  - rooms
dependency_graph:
  requires:
    - 01-01  # action_vocabulary, trigger_engine, patrol_engine, patrol_script
    - 01-02  # command_preprocessor, cmd_alias; rooms/mobs/characters extended with patrol/trigger attrs
  provides:
    - AreaBuilder.patrol() — attaches PatrolScript to mob at build time
    - AreaBuilder.trigger() — appends trigger dict to room/mob db.triggers
    - AreaBuilder.custom_command() — attaches DynamicAreaCmdSet to any object
    - AreaBuilder.flight_point() — registers room as Dragon Courier stop
    - AreaBuilder.flight_route() — registers bidirectional route in FlightRegistry
    - SoravelonRoom.return_appearance() — renders visible custom commands in exit list
    - FlightRegistry — module-level singleton for flight network graph with BFS routing
  affects:
    - world/area_builder.py (extended with 6 new methods)
    - typeclasses/rooms.py (return_appearance override)
    - world/flight_registry.py (new module)
    - commands/cmd_dynamic.py (new module)
tech_stack:
  added:
    - world/flight_registry.py (module-level singleton, same pattern as zone_registry)
    - commands/cmd_dynamic.py (DynamicAreaCommand + DynamicAreaCmdSet + build_dynamic_cmdset)
  patterns:
    - Deferred execution in build() for patrol attachment (mob/room objects must exist first)
    - SaverDict copy pattern for db.triggers and db.custom_commands list mutations
    - Lazy imports inside methods to break circular dependencies (PatrolScript, FlightRegistry)
    - BFS for shortest multi-leg flight path in FlightRegistry.find_route_legs()
key_files:
  created:
    - world/flight_registry.py
    - commands/cmd_dynamic.py
  modified:
    - world/area_builder.py
    - typeclasses/rooms.py
decisions:
  - "Added mob() method to AreaBuilder to create named patrol mobs — required for _mobs dict that patrol() uses to look up mob objects in build() finalization"
  - "Used evennia.commands.cmdset.CmdSet directly (not evennia.CmdSet) in cmd_dynamic.py — evennia.CmdSet returns None before full Evennia init, direct import works at Django setup time"
metrics:
  duration: "3 minutes"
  completed_date: "2026-03-24"
  tasks_completed: 3
  files_modified: 4
---

# Phase 01 Plan 04: AreaBuilder Extension (patrol, trigger, custom_command, flight_point, flight_route) Summary

AreaBuilder extended with 5 authoring methods plus FlightRegistry singleton and DynamicAreaCommand infrastructure, completing the zone DSL surface for all Phase 1 dynamic content.

## What Was Built

**Task 1: patrol(), trigger(), custom_command() + DynamicAreaCommand infrastructure**

- `AreaBuilder.mob(mob_key, room, **kwargs)` — creates/retrieves a SoravelonMob, registers in `self._mobs` for patrol lookup. Added to support `patrol()` which needs actual mob objects.
- `AreaBuilder.patrol(mob_key, route_room_ids, ...)` — validates interrupt_mode, defers to `build()` finalization. `_finalize_patrols()` called from `build()` attaches PatrolScript with `db.route_ids`, `db.route_index`, `db.patrol_def`.
- `AreaBuilder.trigger(source, event, actions, ...)` — validates event against 5 valid events, appends trigger dict to `source_obj.db.triggers` using SaverDict copy pattern. Auto-generates trigger_id if not provided.
- `AreaBuilder.custom_command(target, key, action_dict, ...)` — stores cmd_def in `target.db.custom_commands`, calls `build_dynamic_cmdset()` and attaches via `target.cmdset.add()`.
- `commands/cmd_dynamic.py` — `DynamicAreaCommand` delegates to `execute_action()`, `DynamicAreaCmdSet` (Union merge), `build_dynamic_cmdset()` factory function.

**Task 2: flight_point() + flight_route() + FlightRegistry**

- `world/flight_registry.py` — `_FlightRegistry` class with `register_point()`, `register_route()` (bidirectional), `get_point()`, `get_route()`, `connected_points()`, `find_route_legs()` (BFS), `clear()`. Module-level `FlightRegistry` singleton.
- `AreaBuilder.flight_point(room_or_id, point_id, name=None)` — registers room in FlightRegistry, tags room with `"flight_point"` category `"travel"`, sets `room.db.flight_point_id`.
- `AreaBuilder.flight_route(point_a_id, point_b_id, base_fare, leg_duration=30, echoes=None)` — validates `leg_duration >= 30`, registers bidirectional in FlightRegistry.

**Task 3: SoravelonRoom.return_appearance()**

- Overrides Evennia's default to append visible custom commands (D-21) after standard exit list.
- Filters `self.db.custom_commands` for `visible_in_exits=True`.
- Renders as `|wkey|n - desc` or `|wkey|n` using Evennia color codes.
- No-op if no visible commands — returns unchanged appearance.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical Functionality] Added mob() method**
- **Found during:** Task 1
- **Issue:** Plan's patrol() finalization in build() references `self._mobs.get(patrol_def["mob_key"])`, but AreaBuilder had no `mob()` method and no `_mobs` dict. Without `mob()`, zone authors have no way to create patrol mobs with a named key.
- **Fix:** Added `mob(mob_key, room, **kwargs)` method that creates SoravelonMob objects and registers them in `self._mobs`. Also added `_mobs = {}` and `_deferred_patrols = []` to `__init__`.
- **Files modified:** world/area_builder.py
- **Commit:** 99292e6

**2. [Rule 3 - Blocking Import] Used direct CmdSet import instead of evennia.CmdSet**
- **Found during:** Task 1 verification
- **Issue:** `from evennia import CmdSet` returns `None` at module import time before full Evennia/Django initialization. `class DynamicAreaCmdSet(CmdSet)` raised `TypeError: NoneType takes no arguments`.
- **Fix:** Changed to `from evennia.commands.cmdset import CmdSet` — direct path works at Django setup time, consistent with how `commands/command.py` imports from Evennia directly.
- **Files modified:** commands/cmd_dynamic.py
- **Commit:** 99292e6

## Known Stubs

None — all methods are fully implemented and wired.

## Self-Check: PASSED

- world/area_builder.py: FOUND (all 5 methods + mob() + _finalize_patrols())
- world/flight_registry.py: FOUND
- commands/cmd_dynamic.py: FOUND
- typeclasses/rooms.py return_appearance: FOUND
- Commits: 99292e6, 663896a, 0712745 all present in git log
