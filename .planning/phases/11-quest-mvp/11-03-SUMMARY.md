---
phase: 11-quest-mvp
plan: 03
subsystem: quest-system
tags: [quest-hooks, dialogue-integration, quest-progress, commands]

# Dependency graph
requires:
  - phase: 11-quest-mvp plan 01
    provides: quest_engine.py with check_*_objectives, accept_quest, get_active_quests
  - phase: 11-quest-mvp plan 02
    provides: action_vocabulary handlers and enriched quest DSL
  - phase: 06c-npc-dialogue-and-crafting
    provides: dialogue_engine.py, cmd_dialogue.py with CmdTalk/CmdAccept stubs
provides:
  - 4 quest progress hooks wired (kill, collect, investigate, talk_to/deliver)
  - CmdAccept creates CharacterQuest via accept_quest (D-17)
  - dialogue_engine stubs replaced with real quest_engine delegation (D-18)
  - CmdQuest command with list/detail/abandon subcommands (D-15, D-16)
affects: [11-quest-mvp plan 04, 11-quest-mvp plan 05, content authoring]

# Tech tracking
tech-stack:
  added: []
  patterns: [lazy quest_engine imports in all hook points, progress bar rendering with # and . chars]

key-files:
  created: [commands/cmd_quest.py]
  modified: [typeclasses/mobs.py, typeclasses/rooms.py, world/inventory_engine.py, commands/cmd_dialogue.py, world/dialogue_engine.py, commands/default_cmdsets.py]

key-decisions:
  - "Quest progress hooks placed after existing game logic (triggers, loot, flight) but before infrastructure (SpawnRecord, patrol checks)"
  - "All quest_engine imports are lazy (inside function bodies) per project convention to avoid circular deps"

patterns-established:
  - "Quest hook pattern: lazy import + single function call at the right lifecycle point"
  - "CmdQuest subcommand dispatch: args.startswith('abandon ') for subcommands, else list/detail"

requirements-completed: [D-07, D-08, D-09, D-10, D-11, D-15, D-16, D-17, D-18, D-19, D-05]

# Metrics
duration: 4min
completed: 2026-04-03
---

# Phase 11 Plan 03: Quest Hooks and CmdQuest Summary

**Wired 4 quest progress hooks into mob death/item pickup/room entry/dialogue and created CmdQuest with list/detail/abandon subcommands**

## Performance

- **Duration:** 4 min
- **Started:** 2026-04-03T19:31:43Z
- **Completed:** 2026-04-03T19:35:33Z
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments
- Wired kill objectives into mobs.py at_death (fires when player kills a mob)
- Wired investigate objectives into rooms.py at_object_receive (fires on room entry)
- Wired collect objectives into inventory_engine.py pick_up (fires on item pickup)
- Wired talk_to and deliver objectives into CmdTalk (fires on NPC dialogue)
- Replaced CmdAccept stub with real accept_quest() call creating CharacterQuest records
- Replaced dialogue_engine has_available_quest/get_quest_offer stubs with real quest_engine delegation
- Created CmdQuest with progress bar list view, detailed objective view with rewards preview, and abandon subcommand

## Task Commits

Each task was committed atomically:

1. **Task 1: Wire 4 progress hooks + CmdAccept/CmdTalk + dialogue_engine stubs** - `04de16e` (feat)
2. **Task 2: CmdQuest command + cmdset registration** - `7aea888` (feat)

## Files Created/Modified
- `typeclasses/mobs.py` - Added check_kill_objectives hook in at_death()
- `typeclasses/rooms.py` - Added check_investigate_objectives hook in at_object_receive()
- `world/inventory_engine.py` - Added check_collect_objectives hook in pick_up()
- `commands/cmd_dialogue.py` - Wired CmdAccept to accept_quest(), added talk_to/deliver hooks in CmdTalk
- `world/dialogue_engine.py` - Replaced quest stubs with real quest_engine calls
- `commands/cmd_quest.py` - NEW: CmdQuest with list/detail/abandon subcommands
- `commands/default_cmdsets.py` - Registered CmdQuest in CharacterCmdSet

## Decisions Made
- Quest progress hooks placed after existing game logic (triggers, loot, flight discovery) but before infrastructure (SpawnRecord scheduling, patrol checks) to maintain correct execution order
- All quest_engine imports are lazy (inside function bodies) per project convention to avoid circular dependencies
- CmdQuest uses partial case-insensitive matching for quest names (same UX pattern as dialogue commands)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Git worktree had corrupted index entries (stale .md files and .gitattributes with missing blobs) - resolved by resetting index with git read-tree HEAD before committing Task 2

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All quest hooks are live: mob death, item pickup, room entry, and NPC dialogue fire progress checks
- CmdQuest gives players full quest management UI
- Ready for Plan 04 (quest test suite) and Plan 05 (Ashreach Plains quest content)
- Chain auto-offer (D-05) works via pending_quest_offer set by quest completion in quest_engine

## Self-Check: PASSED

- All 7 files verified present on disk
- Commit 04de16e (Task 1) found in git log
- Commit 7aea888 (Task 2) found in git log

---
*Phase: 11-quest-mvp*
*Completed: 2026-04-03*
