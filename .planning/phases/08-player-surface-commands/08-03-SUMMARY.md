---
phase: 08-player-surface-commands
plan: 03
subsystem: commands
tags: [banking, group, party, scales, commands]

# Dependency graph
requires:
  - phase: 01-patrol-commands-and-flight-paths
    provides: banking engine and group engine backends
provides:
  - CmdBank with deposit/withdraw/balance subcommands
  - CmdDeposit and CmdWithdraw flat aliases
  - CmdGroup with invite/accept/decline/leave/kick/lootmode subcommands
affects: [content-authoring, npc-interactions]

# Tech tracking
tech-stack:
  added: []
  patterns: [subcommand-dispatcher-pattern, flat-alias-pattern]

key-files:
  created: [commands/cmd_bank.py, commands/cmd_group.py]
  modified: [commands/default_cmdsets.py]

key-decisions:
  - "Used private _get_leader/_get_group_state imports in CmdGroup since no public get_group_state wrapper exists in group_engine"

patterns-established:
  - "Flat alias pattern: standalone CmdDeposit/CmdWithdraw commands delegate to same backend as CmdBank subcommands"

requirements-completed: [PSC-02, PSC-03]

# Metrics
duration: 3min
completed: 2026-03-31
---

# Phase 08 Plan 03: Bank and Group Commands Summary

**CmdBank with deposit/withdraw/balance plus CmdGroup with full party management, all delegating to existing backend engines**

## Performance

- **Duration:** 3 min
- **Started:** 2026-04-01T20:30:09Z
- **Completed:** 2026-04-01T20:33:10Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Bank commands (bank deposit/withdraw/balance) plus flat deposit/withdraw aliases wrapping world.banking engine
- Group commands (group invite/accept/decline/leave/kick/lootmode) wrapping world.group_engine
- All 4 command classes registered in CharacterCmdSet

## Task Commits

Each task was committed atomically:

1. **Task 1: Create CmdBank + flat aliases CmdDeposit/CmdWithdraw** - `2352458` (feat)
2. **Task 2: Create CmdGroup + register bank and group commands** - `d272589` (feat)

## Files Created/Modified
- `commands/cmd_bank.py` - CmdBank (subcommand dispatcher), CmdDeposit, CmdWithdraw (flat aliases)
- `commands/cmd_group.py` - CmdGroup with invite/accept/decline/leave/kick/lootmode/status subcommands
- `commands/default_cmdsets.py` - Registered all 4 new commands in CharacterCmdSet

## Decisions Made
- Used private `_get_leader` and `_get_group_state` from group_engine in CmdGroup since no public `get_group_state(character)` wrapper exists; the plan's interface listed it as public but the engine only has `_get_group_state(leader)` which requires finding the leader first

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Used private group_engine helpers for group status display**
- **Found during:** Task 2 (CmdGroup creation)
- **Issue:** Plan interface listed `get_group_state(character)` as public API but engine only has `_get_group_state(leader)` (private, takes leader not character)
- **Fix:** Imported `_get_leader` and `_get_group_state` from group_engine; CmdGroup resolves leader via `_get_leader(char)` then calls `_get_group_state(leader)`
- **Files modified:** commands/cmd_group.py
- **Verification:** Import succeeds, logic matches engine internals
- **Committed in:** d272589 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Necessary adaptation to actual engine API. No scope creep.

## Issues Encountered
- Worktree had corrupt git objects from sparse checkout; resolved by resetting index from HEAD via `git read-tree HEAD`

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Bank and group commands ready for player use
- All banking operations (deposit/withdraw/balance) accessible via both `bank <sub>` and flat aliases
- Party management fully wired to group_engine backend

---
*Phase: 08-player-surface-commands*
*Completed: 2026-03-31*
