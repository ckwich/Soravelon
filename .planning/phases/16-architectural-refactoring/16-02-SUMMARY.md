---
phase: 16-architectural-refactoring
plan: 02
subsystem: gathering
tags: [gathering, fishing, engine-extraction, command-thinning]

# Dependency graph
requires:
  - phase: 13-gathering-and-refining
    provides: gathering_engine.py, cmd_fishing.py, cmd_gathering.py
provides:
  - catch_fish() function in gathering_engine.py
  - complete_gather() function in gathering_engine.py
  - Thin command delegates for fishing and gathering
affects: [gathering-engine, fishing-commands, gathering-commands]

# Tech tracking
tech-stack:
  added: []
  patterns: [command-engine-separation, thin-command-pattern]

key-files:
  created: []
  modified:
    - world/gathering_engine.py
    - commands/cmd_fishing.py
    - commands/cmd_gathering.py

key-decisions:
  - "catch_fish returns 5-tuple (success, msg, item, bait_consumed, tool_broken) for command-layer state management"
  - "complete_gather accepts skill_name and skill_val as params since they were pre-calculated in command delay"

patterns-established:
  - "Engine function returns structured tuple with all mutation results; command reads tuple to decide UI flow"
  - "Move validation stays in command layer; all game state mutations move to world/ engine"

requirements-completed: [D-05, D-06, D-07]

# Metrics
duration: 8min
completed: 2026-04-04
---

# Phase 16 Plan 02: Gathering/Fishing Engine Extraction Summary

**Extracted catch_fish() and complete_gather() from command files into gathering_engine.py, enforcing D-07 thin-command pattern**

## Performance

- **Duration:** 8 min
- **Started:** 2026-04-04T10:53:00Z
- **Completed:** 2026-04-04T11:01:00Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Extracted all fish-catch game logic (quality calc, bait consumption, tool durability, skill XP, item creation) into gathering_engine.catch_fish()
- Extracted all gather-completion game logic (node depletion, quality calc, bonus quantity, tool durability, skill XP) into gathering_engine.complete_gather()
- Both command files now contain zero game state mutations in their delegate methods

## Task Commits

Each task was committed atomically:

1. **Task 1: Extract _catch_fish logic to gathering_engine.catch_fish** - `3ee6f02` (feat)
2. **Task 2: Extract _gather_callback logic to gathering_engine.complete_gather** - `2dfa434` (feat)

## Files Created/Modified
- `world/gathering_engine.py` - Added catch_fish() and complete_gather() public functions
- `commands/cmd_fishing.py` - Thinned _catch_fish to delegate to engine
- `commands/cmd_gathering.py` - Thinned _gather_callback to delegate to engine

## Decisions Made
- catch_fish() returns a 5-tuple (success, msg, item, bait_consumed, tool_broken) so the command can manage fishing state (clearing bait reference, stopping fishing on tool break) without touching game state
- complete_gather() takes skill_name and skill_val as explicit parameters since these were pre-calculated during the gather delay in the command; avoids re-querying skill engine
- Move validation and node-exists checks remain in the command layer as they are command-flow concerns, not game state mutations

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Git index corruption in worktree required index rebuild (rm + reset) before Task 2 commit
- Source files (cmd_fishing.py, cmd_gathering.py, gathering_engine.py) did not exist in worktree branch; checked out from worktree-agent-acdd6b3b branch
- Full Evennia test suite could not run due to missing dependencies in worktree (world.material_definitions etc.); verified syntax correctness via AST parsing

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- gathering_engine.py now exports catch_fish, complete_gather, gather_from_node as the complete gathering API
- CmdButcher._gather_callback still contains inline game logic (butcher yields) - candidate for future extraction if butcher system grows
- All files syntactically valid; full integration testing deferred to merge with complete codebase

## Self-Check: PASSED

- All 3 modified files exist on disk
- Both task commits (3ee6f02, 2dfa434) found in git log
- catch_fish() and complete_gather() both present in gathering_engine.py (1 each)

---
*Phase: 16-architectural-refactoring*
*Completed: 2026-04-04*
