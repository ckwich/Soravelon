---
phase: 13-gathering-and-refining
plan: 02
subsystem: gathering-engine
tags: [gathering, nodes, pool-script, area-builder, typeclass]

# Dependency graph
requires:
  - phase: 13-gathering-and-refining
    plan: 01
    provides: MATERIAL_REGISTRY, GATHERING_CATEGORIES, VISIBILITY_THRESHOLDS
  - phase: 03-gui-area-builder
    provides: AreaBuilder DSL pattern, build() finalization
provides:
  - GatheringNode typeclass (skill-gated visibility, depletion hints)
  - GatheringPoolScript (tick-driven node lifecycle management)
  - spawn_gathering_pool(), deplete_node(), spawn_node_in_pool(), gather_from_node()
  - initialize_zone_gathering() for zone load integration
  - AreaBuilder.gathering_pool() DSL method
affects:
  - typeclasses/objects.py (new GatheringNode class)
  - world/area_builder.py (new gathering_pool method, build() integration)

# Tech stack
added: []
patterns:
  - Dynamic script subclass creation (mirrors CombatScript pattern)
  - SaverDict copy pattern for list mutations on zone object
  - Lazy imports inside all functions (no circular import risk)
  - Persistent room state flags (-1 duration) for Sense integration

# Key files
created:
  - world/gathering_engine.py
modified:
  - typeclasses/objects.py
  - world/area_builder.py

# Decisions
key-decisions:
  - "GatheringPoolScript uses dynamic type() subclass to avoid Evennia import-time typeclass resolution"
  - "Room state flags set with duration=-1 for persistent gathering hints"
  - "Pool ID generated as zone_id + pool_type for uniqueness"
  - "spawn_node_in_pool excludes both exclude_room_id param and last_depleted_room_id"

# Metrics
duration_minutes: 5
completed: "2026-04-04T02:52:00Z"
---

# Phase 13 Plan 02: Gathering Node Infrastructure Summary

GatheringNode typeclass with skill-gated visibility and GatheringPoolScript for stochastic zone-wide node lifecycle management via AreaBuilder DSL.

## What Was Built

### Task 1: GatheringNode Typeclass + gathering_engine.py

**GatheringNode** (typeclasses/objects.py) -- inherits SoravelonObject (not SoravelonItem since nodes cannot be picked up). Sets db.node_type, db.material_id, db.gathers_remaining (2-6), db.tier, db.zone_id, db.pool_id, db.visibility. Has `get:false()` lock. `get_display_name()` checks looker's gathering skill against VISIBILITY_THRESHOLDS for mid/high visibility nodes. `return_appearance()` shows depletion hints (rich/some/nearly exhausted).

**gathering_engine.py** (world/) -- five core functions:
- `spawn_node_in_pool()`: picks random eligible room (excluding last depleted), picks random material filtered by tier range, creates GatheringNode with random gathers_remaining
- `deplete_node()`: removes node, schedules respawn via `evennia.utils.delay()` in a different room
- `gather_from_node()`: decrements remaining, auto-depletes when empty, returns (bool, material_id)
- `spawn_gathering_pool()`: creates/configures GatheringPoolScript on zone object, spawns initial nodes, sets room state flags
- `initialize_zone_gathering()`: reads zone_obj.db.gathering_pools, calls spawn_gathering_pool for each

**GatheringPoolScript**: dynamic script subclass (avoiding import-time resolution). Tick interval 120s prunes dead nodes and spawns replacements when under max_active.

### Task 2: AreaBuilder DSL Extension

**gathering_pool()** method: `area.gathering_pool("ore", rooms=["mine_1", "mine_2"], materials=["iron_ore", "steel_ore"], max_active=3)`. Uses SaverDict copy pattern. Returns self for chaining. Raises AreaBuilderValidationError if called before zone().

**build()** integration: initializes `gathering_pools = []` on zone object alongside quest_definitions and material_definitions. Calls `initialize_zone_gathering()` after auto_layout and zone registry.

## Commits

| Task | Commit | Message |
|------|--------|---------|
| 1 | f2c5a98 | feat(13-02): GatheringNode typeclass and gathering_engine.py |
| 2 | ebcf753 | feat(13-02): AreaBuilder gathering_pool() DSL and build() integration |

## Deviations from Plan

None -- plan executed exactly as written.

## Known Stubs

None -- all functions are fully implemented with real logic.

## Verification Results

- GatheringNode typeclass importable: PASS
- gathering_engine 6 exports importable: PASS
- AreaBuilder.gathering_pool method exists: PASS
- build() source contains gathering_pools initialization: PASS
- build() source contains initialize_zone_gathering call: PASS
