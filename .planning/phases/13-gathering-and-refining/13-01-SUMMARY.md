---
phase: 13-gathering-and-refining
plan: 01
subsystem: world-data
tags: [gathering, materials, skills, room-state, item-spawner, pure-data]

# Dependency graph
requires:
  - phase: 06c-crafting
    provides: crafting_definitions.py quality tiers, RECIPE_REGISTRY pattern
  - phase: 05-skills
    provides: skill_definitions.py skill entry format, skill_engine
provides:
  - MATERIAL_REGISTRY with 18 materials across 6 categories and 3 tiers
  - MATERIAL_TIERS, GATHERING_CATEGORIES, GATHER_DELAY_BY_TIER, VISIBILITY_THRESHOLDS constants
  - TOOL_DURABILITY specifications for 5 gathering tools
  - 3 new gathering skills (mining, woodcutting, skinning) in SKILL_DEFINITIONS
  - 4 gathering-related flags in FLAG_VOCABULARY (mineral_deposits, rich_soil, dense_foliage, water_source)
  - item_tag fix on item_spawner enabling crafting ingredient matching for all spawned items
affects: [13-02, 13-03, 13-04, 13-05, 13-06, 13-07, crafting-system]

# Tech tracking
tech-stack:
  added: []
  patterns: [pure-data registry module pattern for material taxonomy]

key-files:
  created: [world/material_definitions.py]
  modified: [world/skill_definitions.py, world/room_state.py, world/item_spawner.py]

key-decisions:
  - "Hide processing station is workbench (not forge) -- leather working is a separate craft from metal smithing"
  - "Gathering flags use typical_duration=None (persistent) since they are set during zone build, not volatile"
  - "Gathering flags placed low in SENSE_PRIORITY (below combat/node flags) since they are ambient, not urgent"

patterns-established:
  - "Pure-data material registry: all material definitions in one dict, no scattered constants"
  - "Gathering category-to-skill-to-tool-to-command mapping via GATHERING_CATEGORIES dict"

requirements-completed: [SC-4, SC-8]

# Metrics
duration: 2min
completed: 2026-04-04
---

# Phase 13 Plan 01: Material Definitions and Data Foundation Summary

**18-material MATERIAL_REGISTRY across 6 gathering categories with gathering skills, room state flags, and item_tag crafting fix**

## Performance

- **Duration:** 2 min
- **Started:** 2026-04-04T02:45:18Z
- **Completed:** 2026-04-04T02:47:20Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Created world/material_definitions.py as single source of truth for all material data (SC-4)
- Added 3 new gathering skills (mining, woodcutting, skinning) to SKILL_DEFINITIONS for Phase 13 commands
- Added 4 gathering flags to FLAG_VOCABULARY enabling Sense integration for gathering hints
- Fixed item_spawner to set item_tag on all created items, enabling mob loot as crafting ingredients (SC-8)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create world/material_definitions.py** - `c87b5b5` (feat)
2. **Task 2: Add gathering skills + room state flags + fix item_spawner** - `7ef8933` (feat)

## Files Created/Modified
- `world/material_definitions.py` - Pure-data registry: MATERIAL_REGISTRY (18 materials), MATERIAL_TIERS, GATHERING_CATEGORIES, GATHER_DELAY_BY_TIER, VISIBILITY_THRESHOLDS, TOOL_DURABILITY
- `world/skill_definitions.py` - Added mining, woodcutting, skinning skill entries
- `world/room_state.py` - Added mineral_deposits, rich_soil, dense_foliage, water_source flags with Sense display text
- `world/item_spawner.py` - Added item_tag setting via tags.add(item_id, category="item_tag")

## Decisions Made
- Hide processing uses workbench station (leather working separate from metal smithing at forge)
- Gathering room state flags are persistent (typical_duration=None) since set at zone build time
- Gathering Sense display text placed below combat/node flags in priority order (ambient, not urgent)

## Deviations from Plan

None -- plan executed exactly as written.

## Issues Encountered
None.

## Known Stubs
None -- all data is complete and functional. No placeholder values.

## User Setup Required
None -- no external service configuration required.

## Next Phase Readiness
- MATERIAL_REGISTRY ready for consumption by gathering_engine (Plan 02)
- Gathering skills registered for skill_engine queries
- Room state flags ready for gathering pool zone build integration
- item_tag fix enables mob loot processing pipeline (Plan 05)

---
*Phase: 13-gathering-and-refining*
*Completed: 2026-04-04*
