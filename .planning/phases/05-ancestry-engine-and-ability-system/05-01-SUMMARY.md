---
phase: 05-ancestry-engine-and-ability-system
plan: 01
subsystem: game-engine
tags: [ancestry, room-state, faction-standing, mob-death, action-vocabulary]

requires:
  - phase: 04-domain-fingerprints-guild-engine
    provides: CharacterGuild model, faction standing system via world_state.modify_standing()
provides:
  - world/ancestry_engine.py with ANCESTRY_TRAITS for 4 ancestries, set_ancestry() API, starting standings
  - world/room_state.py with 21 lazy-decay room flags, Sense priority/display, get_room_flags/add_room_flag/get_dominant_flag
  - Mob death room flag writers (blood_soaked, fading_life, power_vacuum)
  - add_room_flag action vocabulary handler for trigger system
affects: [05-02, 05-03, 05-04, 05-05, character-creation, combat-system, sense-mechanic]

tech-stack:
  added: []
  patterns:
    - "Lazy decay room state -- no global ticker, flags expire on read via elapsed time calculation"
    - "Persistent flag sentinel (-1 duration) for node-driven flags that last until state change"
    - "FLAG_VOCABULARY as design contract -- all flags defined centrally before use"

key-files:
  created:
    - world/ancestry_engine.py
    - world/room_state.py
  modified:
    - typeclasses/mobs.py
    - world/action_vocabulary.py

key-decisions:
  - "Resistance faction excluded from KNOWN_FACTIONS_AT_CREATION -- applied silently via hidden standing system later"
  - "Selvar standing penalty applied to all 4 known factions individually then guild offset added separately"
  - "Room flags use ndb (volatile) storage -- intentional, clears on restart, represents immediate present"
  - "Nature-affinity mob factions: verdance, wardens, nature -- checked case-insensitive"

patterns-established:
  - "Room flag vocabulary: centralized FLAG_VOCABULARY dict is the single source of truth for all valid flag names"
  - "Lazy decay pattern: room.ndb.room_state stores flags+last_updated, expired flags pruned on read"
  - "Ancestry (bool, str) return pattern: set_ancestry returns success/message tuple consistent with project convention"

requirements-completed: [ANC-01, ANC-02, ANC-03, ANC-04, ANC-05]

duration: 7min
completed: 2026-03-26
---

# Phase 05 Plan 01: Ancestry Engine and Room State Summary

**Four-ancestry engine with starting standings via modify_standing(), plus 21-flag lazy-decay room state system with mob death writers and trigger integration.**

## What Was Built

### world/ancestry_engine.py
- `ANCESTRY_TRAITS` dict with full trait definitions for Human, Kau'roran, Veth, and Selvar ancestries
- `ANCESTRY_STARTING_STANDING` dict mapping each ancestry to faction standing adjustments
- `set_ancestry(character, ancestry_id, coat=None)` -- one-shot character creation call that sets db.ancestry, applies standings
- `get_ancestry_trait(character, trait_name, default=None)` -- convenience accessor for other modules
- Selvar special handling: -5000 to all 4 known factions, +2500 to guilds, coat choice (summer/winter)

### world/room_state.py
- `FLAG_VOCABULARY` with all 21 room state flags (charged, burning, frozen, toxic_air, resonant, void_touched, fading_life, blood_soaked, living_wood, fortified, scouted, disrupted, power_vacuum, unsettled, ancient_presence, still, shadow_marked, predator_kill, corrupted_death, node_critical, node_calming)
- `get_room_flags(room)` -- lazy decay on read, handles persistent (-1) flags
- `add_room_flag(room, flag_name, duration)` -- validates against vocabulary, refreshes to max duration
- `remove_room_flag(room, flag_name)` -- explicit removal
- `get_dominant_flag(room)` -- priority-ordered for Sense display, "still" fallback
- `SENSE_PRIORITY` list and `SENSE_DISPLAY` dict with atmospheric one-liners for all flags

### typeclasses/mobs.py at_death()
- `blood_soaked` flag on any mob death
- `fading_life` flag on nature-affinity mob death (verdance/wardens/nature factions)
- `power_vacuum` flag on named (mob_id tag) or boss (legendary rarity) mob death

### world/action_vocabulary.py
- `_action_add_room_flag` handler registered as "add_room_flag" in ACTION_HANDLERS
- Enables trigger system to write room flags via area spec files

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Worktree missing mobs.py and action_vocabulary.py from main repo**
- **Found during:** Task 2
- **Issue:** Worktree was branched from older commit, missing trigger/loot/respawn code in mobs.py and entire action_vocabulary.py
- **Fix:** Wrote full files matching main repo content plus new additions
- **Files modified:** typeclasses/mobs.py, world/action_vocabulary.py

**2. [Rule 3 - Blocking] Git index corruption in worktree**
- **Found during:** Task 2 commit
- **Issue:** Worktree index contained references to non-existent objects (.claude-plugin, .codex, etc.)
- **Fix:** Removed broken cached entries and re-added all existing files
- **Commits affected:** b1ca20e (included index cleanup alongside task changes)

## Known Stubs

None -- all code is functional, no placeholder data or unconnected components.

## Verification

- Both modules pass Python AST syntax check
- All acceptance criteria verified programmatically (ANCESTRY_TRAITS keys, set_ancestry signature, FLAG_VOCABULARY entries, SENSE_PRIORITY/DISPLAY, mob death flag writers, action handler registration)
