---
phase: 06c-npc-dialogue-and-crafting
plan: 04
subsystem: commands
tags: [dialogue, crafting, npc, commands, evennia-cmdset]

# Dependency graph
requires:
  - phase: 06c-01
    provides: "dialogue_engine.py with greeting, topic, hint, and keyword extraction functions"
  - phase: 06c-02
    provides: "crafting_engine.py with craft_item, get_known_recipes; crafting_definitions.py with RECIPE_REGISTRY"
provides:
  - "6 dialogue commands: CmdTalk, CmdAsk, CmdSay (override), CmdTell, CmdAccept, CmdDecline"
  - "5 crafting commands: CmdCook, CmdSmith, CmdBrew, CmdCraft, CmdRecipes"
  - "All 11 commands registered in CharacterCmdSet"
  - "Pending quest offer state on character ndb with room-change clearing"
  - "NPC reactive echo on player_enters in at_after_move"
affects: [06c-05, quest-system, content-authoring]

# Tech tracking
tech-stack:
  added: []
  patterns: ["_BaseCraftCmd shared base class for crafting commands", "NPC keyword extraction piggybacked on CmdSay override"]

key-files:
  created:
    - commands/cmd_dialogue.py
    - commands/cmd_crafting.py
  modified:
    - commands/default_cmdsets.py
    - typeclasses/characters.py

key-decisions:
  - "CmdSay overrides Evennia default with same key/aliases; broadcasts then extracts NPC keywords"
  - "Crafting commands use evennia.utils.delay with room-change cancellation guard"
  - "NPC lookup uses case-insensitive partial match (startswith) on npc_name or key"
  - "Cap NPC say-responses at 2 per room, sorted by Standing tier (friendlier first)"

patterns-established:
  - "_BaseCraftCmd pattern: shared base class with craft_skill/craft_verb overrides for skill-specific commands"
  - "_find_npc_in_room helper: shared NPC lookup for all dialogue commands"

requirements-completed: [NPC-01, NPC-02, NPC-03]

# Metrics
duration: 6min
completed: 2026-03-27
---

# Phase 06c Plan 04: Dialogue and Crafting Commands Summary

**11 player-facing commands (6 dialogue + 5 crafting) dispatching to engine layer with CmdSay NPC keyword extraction override**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-27T02:57:35Z
- **Completed:** 2026-03-27T03:03:45Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- All 6 dialogue commands (talk, ask, say, tell, accept, decline) with Standing-tier greetings, topic resolution, and keyword extraction
- All 5 crafting commands (cook, smith, brew, craft, recipes) with shared base class, delay-based crafting, and recipe listing
- CmdSay properly overrides Evennia default with both room broadcast and NPC keyword extraction
- Pending quest offer lifecycle: set on talk, validated on accept (same-room check), cleared on room change

## Task Commits

Each task was committed atomically:

1. **Task 1: Dialogue commands** - `63cbfa9` (feat)
2. **Task 2: Crafting commands + cmdset registration** - `b4a4061` (feat)

## Files Created/Modified
- `commands/cmd_dialogue.py` - CmdTalk, CmdAsk, CmdSay, CmdTell, CmdAccept, CmdDecline + _find_npc_in_room helper
- `commands/cmd_crafting.py` - _BaseCraftCmd, CmdCook, CmdSmith, CmdBrew, CmdCraft, CmdRecipes
- `commands/default_cmdsets.py` - All 11 new commands registered in CharacterCmdSet
- `typeclasses/characters.py` - ndb.pending_quest_offer init + at_after_move clearing + reactive echo

## Decisions Made
- CmdSay overrides Evennia default with same key="say" and aliases=["'", '"'] so CharacterCmdSet.add() replaces it
- Crafting uses evennia.utils.delay() with ndb.crafting_in_progress flag and room comparison for move-cancellation
- NPC lookup is partial-match (startswith) case-insensitive on both npc_name db attr and key
- CmdSay caps NPC responses at 2 per say command, sorted by Standing tier (friendlier respond first)
- CmdAccept validates NPC is still in same room before accepting quest (Pitfall 4)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Worktree had corrupted sparse-checkout index entries from a plugin repo; resolved by staging only task-specific files without touching corrupted entries

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- All dialogue and crafting commands are wired and ready for testing (Plan 05)
- Quest accept/decline are stub-ready (has_available_quest returns False; wires in when quest system ships)
- NPC reactive echo fires on room entry; ambient tick registered separately at server start

---
*Phase: 06c-npc-dialogue-and-crafting*
*Completed: 2026-03-27*
