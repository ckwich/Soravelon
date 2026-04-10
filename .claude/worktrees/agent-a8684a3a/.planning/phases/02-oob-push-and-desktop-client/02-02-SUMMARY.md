---
phase: 02-oob-push-and-desktop-client
plan: 02
subsystem: area-builder
tags: [area_builder, grid_coords, bfs_layout, zone_coords, fog_of_war]

# Dependency graph
requires:
  - phase: 01-foundation
    provides: AreaBuilder with room/exit/zone DSL, idempotent build(), zone/named_mob registries
provides:
  - "room.db.grid_x / room.db.grid_y — zone-local integer grid coordinates on every room after build()"
  - "zone_obj.db.world_x / world_y / world_radius — world-level zone position attributes"
  - "zone_obj.db.fog_of_war — per-zone boolean, default False"
  - "auto_layout_zone() — BFS function assigning coords to rooms without explicit placement"
  - "DIRECTION_OFFSETS — cardinal/diagonal/vertical offset table for BFS traversal"
affects:
  - "02-03-oob-publisher (map_update reads grid_x/grid_y from rooms)"
  - "02-04-oob-integration (at_after_move sends map_update with pre-computed coords)"
  - "03-gui-builder (GUI builder reads/writes grid_x/grid_y via area spec DSL)"

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "BFS grid auto-layout: traverse zone room graph via exit objects, assign integer coords, nudge collisions east"
    - "Explicit builder coords preserved: grid_x/grid_y set in area.room() kwargs bypass auto_layout_zone BFS"
    - "World coords as optional zone attributes: world_x/world_y/world_radius set via area.zone() kwargs"

key-files:
  created:
    - "tests/test_area_builder.py — 33-test suite covering all AreaBuilder functionality including 8 new coord tests"
  modified:
    - "world/area_builder.py — DIRECTION_OFFSETS, auto_layout_zone(), _set_room_attrs grid_x/grid_y, zone() world coords, build() 3.5 call"

key-decisions:
  - "Collision nudge shifts east (nx += 1) for up/down/in/out exits that map to (0,0) offset — deterministic, simple, matches research recommendation"
  - "auto_layout_zone finds first room without grid_x as BFS root — if all rooms have explicit coords it returns immediately (no-op)"
  - "DIRECTION_OFFSETS defined at module level as UPPER_SNAKE_CASE constant per project conventions"

patterns-established:
  - "BFS coordinate assignment: rooms_dict -> deque BFS -> occupied set -> nudge on collision"
  - "Optional zone attrs: zone() kwargs with defaults (None for coords, False for fog_of_war)"

requirements-completed: [CLI-07]

# Metrics
duration: 35min
completed: 2026-03-25
---

# Phase 02 Plan 02: AreaBuilder Room Coordinates and BFS Auto-Layout Summary

**BFS grid auto-layout grafted onto AreaBuilder: every room gets zone-local (grid_x, grid_y) integer coords after build(), with zone-level world position and fog-of-war attrs for the Tauri map panel**

## Performance

- **Duration:** 35 min
- **Started:** 2026-03-25T05:51:46Z
- **Completed:** 2026-03-25T06:27:23Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- `_set_room_attrs()` stores `grid_x`/`grid_y` from kwargs; rooms without explicit coords get None until auto-layout fills them
- `zone()` stores `world_x`, `world_y`, `world_radius`, `fog_of_war` on `zone_obj.db` (defaults None/None/None/False)
- `auto_layout_zone(rooms_dict)` BFS function assigns integer coords, preserves builder-placed coords, and nudges east on collision (handles up/down/in/out (0,0) offset)
- `build()` calls `auto_layout_zone(self._rooms)` at step 3.5 (after `_finalize_patrols`, before named mob registration)
- 8 new tests covering: explicit coords, None defaults, world coord storage, auto-layout fill, north-chain coords (0,0)→(0,1)→(0,2), preservation of explicit coords, no collision

## Task Commits

Each task was committed atomically:

1. **Task 1+2: grid coords, world coords, DIRECTION_OFFSETS, auto_layout_zone, build() wiring** - `b83f27b` (feat)

## Files Created/Modified

- `world/area_builder.py` — DIRECTION_OFFSETS constant, auto_layout_zone() function, _set_room_attrs grid_x/grid_y lines, zone() world coord lines, build() step 3.5 call
- `tests/test_area_builder.py` — created (was untracked); full 33-test suite covering all AreaBuilder functionality

## Decisions Made

- Collision nudge uses `nx += 1` (east) for (0,0)-offset exits — simple, deterministic, no random walk
- BFS root is first room in `rooms_dict` without `grid_x is None`; if all rooms have explicit coords, function returns immediately (no-op)
- Tasks 1 and 2 combined into a single commit because they form a single atomic unit (coords storage is meaningless without the layout function)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- `evennia test --settings server.conf.settings tests/test_area_builder.py` format fails (path to file not supported by Django test runner). Used `python -m evennia test --settings settings tests.test_area_builder` (dotted module path) instead. All 33 tests pass.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Room coords are pre-computed at zone load time — `map_update` in Plan 02-03 can read `room.db.grid_x`/`room.db.grid_y` directly
- Zone world position is available for world map rendering in the Tauri client
- Fog-of-war flag is set per zone; visited-room tracking (Pitfall 5 in RESEARCH.md) still needed in Plan 02-04

---
*Phase: 02-oob-push-and-desktop-client*
*Completed: 2026-03-25*
