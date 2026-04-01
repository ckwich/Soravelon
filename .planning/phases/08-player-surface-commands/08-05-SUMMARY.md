---
phase: 08-player-surface-commands
plan: 05
subsystem: player-commands
tags: [loadout, map, commands, fog-of-war, ability-management]
dependency_graph:
  requires: [ability_registry, ability_engine, area_builder]
  provides: [CmdLoadout, CmdMap]
  affects: [default_cmdsets, CharacterCmdSet]
tech_stack:
  added: []
  patterns: [SaverDict-copy, lazy-import, prefix-matching, fog-of-war]
key_files:
  created:
    - commands/cmd_loadout.py
    - commands/cmd_map.py
  modified:
    - commands/default_cmdsets.py
decisions:
  - "Loadout preset slots are integer-keyed (1-5) stored in char.db.loadout_presets dict"
  - "Map trims empty rows for cleaner display; uses Evennia color tags for current/visited markers"
metrics:
  duration_minutes: 3
  completed: "2026-04-01T20:33:00Z"
---

# Phase 08 Plan 05: Loadout Management and ASCII Map Summary

CmdLoadout with 5-preset ability loadout management and CmdMap with fog-of-war ASCII zone rendering.

## Task Results

### Task 1: CmdLoadout -- ability loadout management with presets

| Aspect | Detail |
|--------|--------|
| Commit | `7cda5b4` |
| Files | `commands/cmd_loadout.py` (created) |
| Status | Complete |

Created `CmdLoadout` with subcommands: view (no args), add, remove, clear, save, and numeric preset swap. Loadout capped at 8 abilities (`MAX_LOADOUT_SIZE`), with up to 5 presets (`MAX_PRESETS`). Ability name matching uses case-insensitive prefix search with disambiguation for multiple matches. All list mutations use the SaverDict copy pattern (copy to Python list, mutate, assign back). Imports `get_ability` from `world.ability_registry` and `_check_ability_access` from `world.ability_engine` lazily inside `func()`.

### Task 2: CmdMap -- ASCII text map with fog-of-war + command registration

| Aspect | Detail |
|--------|--------|
| Commit | `eace442` |
| Files | `commands/cmd_map.py` (created), `commands/default_cmdsets.py` (modified) |
| Status | Complete |

Created `CmdMap` with a 10-tile radius ASCII grid centered on the player. Uses `room.db.grid_x`/`grid_y` for coordinates and `room.tags.get(category="zone_id")` to scope to current zone. Fog-of-war filters rooms via `char.db.visited_room_ids` -- only visited rooms render as `#`, current position as `@`. Empty rows are trimmed from top/bottom for clean output. Both `CmdLoadout` and `CmdMap` registered in `CharacterCmdSet` via `commands/default_cmdsets.py`.

## Deviations from Plan

None -- plan executed exactly as written.

## Known Stubs

None -- both commands are fully functional against existing ability_registry and room coordinate systems.

## Verification Results

- `commands/cmd_loadout.py` passes AST parse; exports CmdLoadout with key="loadout"
- `commands/cmd_map.py` passes AST parse; exports CmdMap with key="map"
- `commands/default_cmdsets.py` contains both `self.add(CmdLoadout())` and `self.add(CmdMap())`

## Self-Check: PASSED

All created files exist. All commit hashes verified in git log.
