---
phase: 13-gathering-and-refining
plan: 05
subsystem: gathering
tags: [fishing, state-machine, timers, gathering, idle-mode]

requires:
  - phase: 13-01
    provides: MATERIAL_REGISTRY with fish entries and GATHERING_CATEGORIES
  - phase: 13-02
    provides: gather_from_node, GatheringPoolScript, GatheringNode typeclass

provides:
  - CmdFish with active mini-game (cast/bite/reel) and idle auto-fishing mode
  - CmdReel time-sensitive command for active fishing bite window
  - Movement interrupt for fishing state in Character.at_after_move

affects: [13-06, 13-07, phase-14]

tech-stack:
  added: []
  patterns: [dual-mode state machine on ndb, timer-based mini-game with deferred callbacks]

key-files:
  created: [commands/cmd_fishing.py]
  modified: [typeclasses/characters.py]

key-decisions:
  - "CmdReel delegates to CmdFish()._on_reel for single state machine owner"
  - "Fishing state stored on character.ndb.fishing_state dict with mode/phase/timers"
  - "Movement interrupt added to Character.at_after_move (not at_pre_move) for consistency with existing patterns"

patterns-established:
  - "Timer-based mini-game: deferred callbacks with phase tracking on ndb state dict"
  - "Idle vs active mode: same command, different quality multipliers and timer intervals"

requirements-completed: [SC-5]

duration: 2min
completed: 2026-04-04
---

# Phase 13 Plan 05: Fishing System Summary

**Dual-mode fishing command with active cast/bite/reel mini-game and idle auto-fishing at diminished returns, bait quality bonuses, tool durability, and movement interrupt**

## Performance

- **Duration:** 2 min
- **Started:** 2026-04-04T02:56:37Z
- **Completed:** 2026-04-04T02:58:14Z
- **Tasks:** 1
- **Files modified:** 2

## Accomplishments
- Active fishing mini-game: cast line, wait 5-15s for bite, 4s reel window, full quality rewards
- Idle fishing mode: auto-catches every 15-40s with -1 quality tier penalty
- Bait system: optional +1 quality tier, consumed per catch, reduces timer by 20-30%
- Movement interrupt: Character.at_after_move cancels all fishing timers and clears state

## Task Commits

Each task was committed atomically:

1. **Task 1: Create commands/cmd_fishing.py with active and idle fishing modes** - `a5afb22` (feat)

## Files Created/Modified
- `commands/cmd_fishing.py` - CmdFish (active + idle modes, state machine, bait, quality) and CmdReel (bite-phase reel delegate)
- `typeclasses/characters.py` - Added fishing state cleanup in at_after_move (Pitfall 6 prevention)

## Decisions Made
- CmdReel delegates to CmdFish()._on_reel to keep the state machine in a single class
- Fishing state stored on character.ndb.fishing_state dict (volatile, cleared on disconnect/move)
- Movement interrupt placed in at_after_move (consistent with existing OOB/combat patterns in that hook)
- Active mode auto-restarts cast after successful catch (continuous fishing until node depleted or stopped)
- Idle mode schedules next catch after each catch (20-40s interval, bait reduces by 20%)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Fishing command ready for CmdSet registration (Phase 13-06 or character cmdset wiring)
- Fish materials (river_trout, cave_eel, shadow_bass) already in MATERIAL_REGISTRY from Plan 01
- Gathering pool system from Plan 02 handles fish spot spawning

---
*Phase: 13-gathering-and-refining*
*Completed: 2026-04-04*
