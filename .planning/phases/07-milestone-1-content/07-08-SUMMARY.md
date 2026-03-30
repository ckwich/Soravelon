---
phase: 07-milestone-1-content
plan: 08
subsystem: content
tags: [area-builder, coastal, zone-spec, mob-templates, loot-tables]

requires:
  - phase: 07-01
    provides: AreaBuilder DSL for zone authoring
  - phase: 07-02
    provides: mob_templates and loot_tables framework
  - phase: 07-03
    provides: area_validator constants (VALID_ZONE_TYPES etc.)
provides:
  - Stormhaven Coast starter zone (107 rooms, coastal biome)
  - 5 coastal mob types with templates and loot tables
  - Named mob Captain Wrack with unique respawn
  - 3 field NPCs with quest stubs
  - Cross-zone exits connecting to Vael's Crossing and Ashreach Expanse
affects: [07-09, 07-10, equipment-catalog, node-zone]

tech-stack:
  added: []
  patterns: [coastal zone layout with 10 sub-areas, sea cave underground network]

key-files:
  created:
    - world/areas/stormhaven_coast.py
  modified:
    - world/mob_templates.py
    - world/loot_tables.py

key-decisions:
  - "Captain Wrack (raider captain) chosen as named mob over Tidecaller (sea serpent) for better narrative integration with smuggler's cove sub-area"
  - "10 sub-areas for geographic variety: harbor road, cliff paths (N/S), village, tidal flats, sea caves, smuggler's cove, lighthouse, shipwreck, storm bluffs"
  - "Salt lurker designed as eyeless cave ambusher -- passive aggression with high burst damage on disturbance"

patterns-established:
  - "Coastal zone pattern: mix of surface path/clearing rooms with underground cave network"
  - "Smuggler's cove pattern: hidden trail entrance, escape tunnel exit, weapons cache"

requirements-completed: [CON-02]

duration: 9min
completed: 2026-03-30
---

# Phase 7 Plan 08: Stormhaven Coast Summary

**107-room jagged coastal starter zone with sea caves, smuggler's cove, lighthouse, shipwreck, 5 mob types, and named mob Captain Wrack**

## Performance

- **Duration:** 9 min
- **Started:** 2026-03-30T00:21:11Z
- **Completed:** 2026-03-30T00:30:30Z
- **Tasks:** 1
- **Files modified:** 3

## Accomplishments
- Stormhaven Coast zone spec with 107 rooms across 10 sub-areas (harbor road approach, cliff path north, village, tidal flats, sea caves, smuggler's cove, lighthouse point, wreck of the Seaspray, cliff path south, storm bluffs)
- 5 mob types with full stat blocks, abilities, and loot tables: shore_crab, sea_serpent, coastal_raider, cliff_harpy, salt_lurker
- Named mob Captain Wrack (infamous raider captain, 120-min respawn) in smuggler's captain cabin
- 51 spawn definitions maintaining moderate mob density (D-19), 1 is_hunter cliff harpy (D-28)
- 3 field NPCs, 5 lore fragments (maritime history, dragon-era cairns, standing stones), 4 materials, 3 quest stubs

## Task Commits

Each task was committed atomically:

1. **Task 1: Author Stormhaven Coast zone spec with mob templates and loot tables** - `f048fe0` (feat)

## Files Created/Modified
- `world/areas/stormhaven_coast.py` - Complete coastal starter zone spec with 107 rooms, 51 spawns, named mob, NPCs, materials, lore
- `world/mob_templates.py` - Added 5 coastal mob templates (shore_crab, sea_serpent, coastal_raider, cliff_harpy, salt_lurker)
- `world/loot_tables.py` - Added 5 loot tables with tier-scaled drops for all coastal mob types

## Decisions Made
- Captain Wrack chosen as named mob (raider captain in smuggler's cove) rather than Tidecaller (sea serpent in deep pool) -- better narrative integration with the smuggler sub-area and existing raider spawns
- 10 sub-areas designed for geographic diversity: surface paths, underground caves, settlement, ruins, and high-altitude bluffs
- Salt lurker designed as eyeless cave-dwelling ambusher with passive aggression but high burst damage -- fits the deep cave ecosystem
- Lore fragments connect to existing dragon-era symbol threading from Vael's Crossing (cairns, standing stones, fossil wall)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Known Stubs
None - all data structures are fully populated with real content.

## Next Phase Readiness
- Stormhaven Coast completes the 4-zone starter region surrounding Vael's Crossing
- Cross-zone exit to ashreach_expanse defined (will resolve when that zone loads)
- Ready for equipment catalog (07-09) and node zone (07-10) integration

---
*Phase: 07-milestone-1-content*
*Completed: 2026-03-30*
