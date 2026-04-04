---
phase: 13-gathering-and-refining
plan: 06
subsystem: commands
tags: [prospect, survey, repair, gathering, sense, room-state]

requires:
  - phase: 13-01
    provides: "Room state gathering flags (mineral_deposits, rich_soil, dense_foliage, water_source)"
  - phase: 13-02
    provides: "Gathering engine with GatheringNode, pool lifecycle"
  - phase: 13-04
    provides: "Processing recipes for gathered materials"
  - phase: 13-05
    provides: "Fishing commands (CmdFish, CmdReel)"
provides:
  - "CmdProspect/CmdSurvey for straight-line node discovery"
  - "CmdRepair for tool durability restoration at workbench"
  - "All 9 gathering commands registered in CharacterCmdSet"
  - "prospect_scan() function in gathering_engine.py"
affects: [phase-14, content-authoring]

tech-stack:
  added: []
  patterns: ["straight-line cardinal scanning (not BFS) for prospect"]

key-files:
  created: [commands/cmd_prospect.py]
  modified: [world/gathering_engine.py, commands/default_cmdsets.py]

key-decisions:
  - "Sense gathering hints already wired via SENSE_DISPLAY in room_state.py -- no cmd_sense.py changes needed"
  - "prospect_scan uses simple ex.key match for exit direction (consistent with area_builder pattern)"

patterns-established:
  - "Straight-line scanning pattern: walk exits by key match, not BFS"

requirements-completed: [SC-6, SC-7]

duration: 2min
completed: 2026-04-04
---

# Phase 13 Plan 06: Discovery Commands and Registration Summary

**Prospect/survey straight-line scanning, tool repair at workbench, and all 9 gathering commands registered in CharacterCmdSet**

## Performance

- **Duration:** 2 min
- **Started:** 2026-04-04T03:00:50Z
- **Completed:** 2026-04-04T03:02:32Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Created CmdProspect with survey alias that scans cardinal directions for gathering nodes with skill-based range (2-6 rooms)
- Created CmdRepair for tool durability restoration at workbench using smithing skill
- Added prospect_scan() to gathering_engine.py for straight-line node detection
- Registered all 9 Phase 13 commands: mine, harvest, chop, forage, butcher, fish, reel, prospect/survey, repair

## Task Commits

Each task was committed atomically:

1. **Task 1: Create cmd_prospect.py with straight-line scanning** - `6080511` (feat)
2. **Task 2: Extend Sense for gathering hints + register all commands** - `cb10941` (feat)

## Files Created/Modified
- `commands/cmd_prospect.py` - CmdProspect (prospect/survey) and CmdRepair commands
- `world/gathering_engine.py` - Added prospect_scan() and CARDINAL_DIRECTIONS
- `commands/default_cmdsets.py` - Registered 9 gathering commands in CharacterCmdSet

## Decisions Made
- Sense gathering hints were already fully wired via SENSE_DISPLAY dict in room_state.py (added in Plan 13-01), so no changes to cmd_sense.py were needed
- prospect_scan matches exit direction via ex.key.lower() == direction, consistent with area_builder exit creation pattern

## Deviations from Plan

None - plan executed exactly as written. The Sense hints referenced in Task 2 were already implemented by the room_state.py SENSE_DISPLAY architecture from Plan 13-01.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Known Stubs
None - all commands are fully functional with real engine calls.

## Next Phase Readiness
- All gathering commands accessible to players
- Phase 13 command surface complete (mine, harvest, chop, forage, butcher, fish, reel, prospect/survey, repair)
- Ready for Phase 13-07 (integration testing / zone content)

---
*Phase: 13-gathering-and-refining*
*Completed: 2026-04-04*
