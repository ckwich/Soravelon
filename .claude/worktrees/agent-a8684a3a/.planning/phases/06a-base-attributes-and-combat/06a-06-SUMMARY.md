---
phase: 06a-base-attributes-and-combat
plan: 06
subsystem: combat
tags: [combat-commands, cmdset, oob, auto-engage, flee, targeting]

# Dependency graph
requires:
  - phase: 06a-05
    provides: CombatScript, start_combat, join_combat, process_player_action
provides:
  - CmdAttack, CmdFlee, CmdTarget, CmdPass combat commands
  - CombatCmdSet (Replace priority 10) for combat-mode command restriction
  - Auto-engage on room entry for aggressive mobs (same-room only)
  - push_combat_update with structured combatant/ability payload
  - push_stat_update with HP/stamina/domain-resource/conditions
affects: [06a-07, 06b, phase-7-content]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "CombatCmdSet Replace+priority 10 blocks exits during combat"
    - "Auto-engage in at_after_move checks get_behavior_toward for aggressive mobs"
    - "push_combat_update builds payload internally when called without data arg"

key-files:
  created:
    - commands/combat_commands.py
  modified:
    - commands/default_cmdsets.py
    - world/combat_script.py
    - typeclasses/characters.py
    - world/oob_publisher.py

key-decisions:
  - "CombatCmdSet import moved from cmd_abilities to combat_commands (Rule 3 fix)"
  - "push_combat_update accepts optional data arg for backward compat with CombatScript direct calls"
  - "Auto-engage joins all aggressive mobs into same combat (not separate encounters)"

patterns-established:
  - "Combat commands delegate all action logic to combat_script.process_player_action"
  - "OOB combat helpers (_resolve_combatant, _get_available_abilities) kept in oob_publisher"

requirements-completed: [CMB-01, CMB-04]

# Metrics
duration: 6min
completed: 2026-03-26
---

# Phase 06a Plan 06: Combat Commands Summary

**CmdAttack/CmdFlee/CmdTarget/CmdPass with CombatCmdSet, auto-engage on room entry, and structured OOB combat/stat publishers**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-26T19:17:14Z
- **Completed:** 2026-03-26T19:23:16Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- Combat commands handle all player input types: attack initiation, basic attacks, flee with speed check, target switching, and turn passing
- CombatCmdSet (Replace, priority 10, no_exits) restricts commands during combat while preserving look and ability usage
- Auto-engage fires when player enters room with aggressive mobs (same-room only; is_hunter BFS deferred to Phase 6b)
- push_combat_update delivers full structured payload: combatant HP%, effects, abilities, turn state
- push_stat_update sends HP, stamina, domain resource, and active condition strings

## Task Commits

Each task was committed atomically:

1. **Task 1: Create combat commands and CombatCmdSet** - `5c50e53` (feat)
2. **Task 2: Wire auto-engage, OOB publishers, and combat cleanup hooks** - `0176957` (feat)

## Files Created/Modified
- `commands/combat_commands.py` - CmdAttack, CmdFlee, CmdTarget, CmdPass, CombatCmdSet
- `commands/default_cmdsets.py` - CmdAttack registered in CharacterCmdSet for out-of-combat initiation
- `world/combat_script.py` - CombatCmdSet import path updated to combat_commands
- `typeclasses/characters.py` - Auto-engage logic in at_after_move
- `world/oob_publisher.py` - Full push_combat_update and push_stat_update implementations with helpers

## Decisions Made
- CombatCmdSet moved to its own module (combat_commands.py) rather than living in cmd_abilities.py -- cleaner separation of concerns and avoids combat_script importing from a non-combat module
- push_combat_update accepts optional data kwarg for backward compatibility with CombatScript's _build_combat_oob direct-call pattern
- All aggressive mobs in room join the same combat encounter rather than creating separate encounters per mob

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Updated CombatCmdSet import path in combat_script.py**
- **Found during:** Task 1 (combat commands creation)
- **Issue:** combat_script.py imported CombatCmdSet from commands.cmd_abilities, but CombatCmdSet is now in commands.combat_commands
- **Fix:** Changed both _add_combat_cmdset and _remove_combat_cmdset to import from commands.combat_commands
- **Files modified:** world/combat_script.py
- **Verification:** Import chain verified via python -c test
- **Committed in:** 5c50e53 (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Essential for correctness -- old import path would cause ImportError. No scope creep.

## Issues Encountered
- Git worktree had corrupted objects preventing commits; resolved by committing directly to main repo instead

## User Setup Required
None - no external service configuration required.

## Known Stubs
None - all functions are fully implemented with real logic.

## Next Phase Readiness
- All combat commands, auto-engage, and OOB publishers are wired
- Ready for 06a-07 test suite (final plan in Phase 6a)
- is_hunter BFS aggro deferred to Phase 6b per plan specification

---
*Phase: 06a-base-attributes-and-combat*
*Completed: 2026-03-26*
