---
phase: 06c-npc-dialogue-and-crafting
plan: 03
subsystem: npc-dialogue
tags: [area-builder, npc, dialogue, ambient-ticker, action-vocabulary]

requires:
  - phase: 06c-01
    provides: "Dialogue engine functions (resolve_greeting, resolve_topic_response, get_npc_hints, ambient_npc_tick)"
provides:
  - "AreaBuilder npc() creates SoravelonMob objects with dialogue/ambient db attributes"
  - "AreaBuilder room() supports crafting_stations kwarg for station tags"
  - "Global ambient NPC ticker registered at 15-second interval"
  - "open_dialogue action vocabulary handler (NPC lookup, greeting, topic)"
affects: [06c-04, 06c-05]

tech-stack:
  added: []
  patterns: ["NPC objects as SoravelonMob with is_npc=True, combat_enabled=False"]

key-files:
  modified:
    - world/area_builder.py
    - server/conf/at_server_startstop.py
    - world/action_vocabulary.py

key-decisions:
  - "NPC objects use npc_id tag category for idempotent lookup (parallel to room_id pattern)"
  - "NPC name defaults to npc_id title-cased with underscores replaced by spaces"

patterns-established:
  - "NPC creation pattern: SoravelonMob with is_npc=True, tagged npc/character_type and npc/mob_type"
  - "Crafting station tags: crafting_{station} in crafting_station category on rooms"

requirements-completed: [NPC-01, NPC-02]

duration: 4min
completed: 2026-03-26
---

# Phase 06c Plan 03: NPC Zone Wiring Summary

**AreaBuilder npc() creates NPC mob objects with dialogue/ambient db attributes, ambient ticker registered at 15s, open_dialogue action handler wired**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-26T22:17:56Z
- **Completed:** 2026-03-26T22:21:59Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- AreaBuilder npc() now creates SoravelonMob objects with is_npc=True during zone build, with full dialogue and ambient data on db attributes
- Global ambient NPC ticker registered at 15-second interval via TICKER_HANDLER
- open_dialogue action vocabulary handler implemented with NPC room lookup, greeting flow, and topic query support
- AreaBuilder room() supports crafting_stations kwarg for crafting station tags on rooms

## Task Commits

Each task was committed atomically:

1. **Task 1: AreaBuilder npc() extension + NPC object creation** - `5c72c3f` (feat)
2. **Task 2: Ambient ticker registration + open_dialogue handler** - `719a459` (feat)

## Files Created/Modified
- `world/area_builder.py` - Extended npc() to create NPC mobs with dialogue/ambient data; added crafting_stations to room()
- `server/conf/at_server_startstop.py` - Registered npc_ambient_tick at 15-second interval
- `world/action_vocabulary.py` - Implemented _handle_open_dialogue handler, replaced stub

## Decisions Made
- NPC objects use npc_id tag category for idempotent lookup, parallel to the existing room_id tag pattern
- NPC display name defaults to npc_id with underscores replaced by spaces and title-cased (e.g., "maren_warden" -> "Maren Warden")
- NPC tagged with both character_type=npc and mob_type=npc for queryset flexibility

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Worktree had corrupt git objects in index (.gitattributes, .gitignore blobs missing) - resolved by rebuilding index from HEAD via git read-tree before committing Task 2

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- NPC objects exist as interactable room contents for dialogue commands (Plan 04: CmdTalk/CmdAsk)
- Ambient ticker running for idle echoes once NPCs are defined in zone specs
- open_dialogue handler ready for trigger system integration
- Crafting station tags ready for CmdCraft station validation (Plan 04)

---
*Phase: 06c-npc-dialogue-and-crafting*
*Completed: 2026-03-26*
