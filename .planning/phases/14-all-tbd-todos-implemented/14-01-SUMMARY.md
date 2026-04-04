---
phase: 14-all-tbd-todos-implemented
plan: 01
subsystem: combat, banking
tags: [death-penalty, mob-affixes, rarity-multipliers, status-effects, scales]

requires:
  - phase: 06a-combat-system
    provides: combat engine, status effects, base attributes
  - phase: 01-foundation
    provides: mob affix definitions, banking engine
provides:
  - Death penalty on player death (20% Scales drop + session XP wipe)
  - Rarity-based damage multipliers for mob combat
  - Real on-hit and per-round affix effect application
affects: [combat-system, mob-affixes, banking]

tech-stack:
  added: []
  patterns:
    - "Affix combat_modifiers merge: multiplicative for damage_multiplier, additive for flat/bonus, max for others"
    - "Death penalty placed on corpse via db.scales attribute for player loot"

key-files:
  created: []
  modified:
    - world/banking.py
    - world/mob_affixes.py
    - world/combat_engine.py

key-decisions:
  - "Corpse Scales stored as corpse.db.scales integer, lootable by other players"
  - "Session XP wipe uses ndb.session_xp = {} (volatile attribute, committed XP on db is safe)"
  - "Affix on-hit checks both ndb.immunities and db.immunities for immunity"
  - "Stackable effects default 3 rounds, non-stackable default 2 rounds for affix application"

patterns-established:
  - "Death penalty hook pattern: banking.on_character_death called from combat_engine.handle_player_death after corpse spawn, before respawn"
  - "Affix modifier merging: multiplicative/additive/max stacking rules for combat_modifiers dicts"

requirements-completed: [SC-1, SC-2]

duration: 4min
completed: 2026-04-04
---

# Phase 14 Plan 01: Death Penalty and Combat Affix Hooks Summary

**Death drops 20% carried Scales onto corpse and wipes session XP; mob affixes now apply real rarity multipliers and status effects via combat hooks**

## Performance

- **Duration:** 4 min
- **Started:** 2026-04-04T05:28:57Z
- **Completed:** 2026-04-04T05:33:00Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Replaced all STUB functions in banking.py with full death penalty logic (20% Scales drop to corpse, uncommitted XP wipe)
- Wired on_character_death into handle_player_death in combat_engine.py (after corpse spawn, before respawn)
- Added RARITY_DAMAGE_MULTIPLIERS constant and merged affix combat_modifiers with proper stacking rules
- Implemented real on_hit status effect application with immunity checks via apply_effect
- Implemented per_round effects: heal_self (regenerating) and periodic_root (rooting) with combat target iteration

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement death penalty in banking.py and wire into combat_engine.py** - `781359c` (feat)
2. **Task 2: Implement combat affix hooks with rarity multipliers and status effects** - `71cd4e7` (feat)

## Files Created/Modified
- `world/banking.py` - on_character_death and handle_carried_scales_on_death fully implemented
- `world/mob_affixes.py` - RARITY_DAMAGE_MULTIPLIERS, check_mob_damage_modifiers, check_mob_on_hit_effects, check_mob_per_round_effects all real implementations
- `world/combat_engine.py` - handle_player_death now calls on_character_death for death penalty

## Decisions Made
- Corpse Scales stored as `corpse.db.scales` integer on the player corpse object, lootable by other players
- Session XP wipe targets `ndb.session_xp` (volatile) so committed XP on `db` attributes remains safe
- Affix on-hit immunity checks both `ndb.immunities` (volatile) and `db.immunities` (persistent mob config)
- Default durations for affix-applied effects: 3 rounds stackable, 2 rounds non-stackable

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Known Stubs
None - all STUB markers removed from banking.py and mob_affixes.py.

## Next Phase Readiness
- Death penalty and affix hooks are complete and wired into combat
- Ready for plan 14-02 (next TBD/TODO batch)

## Self-Check: PASSED

- All 3 modified files exist on disk
- SUMMARY.md created at expected path
- Commit 781359c found in git history
- Commit 71cd4e7 found in git history

---
*Phase: 14-all-tbd-todos-implemented*
*Completed: 2026-04-04*
