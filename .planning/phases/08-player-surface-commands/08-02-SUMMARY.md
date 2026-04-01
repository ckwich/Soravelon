---
phase: 08-player-surface-commands
plan: 02
subsystem: commands
tags: [evennia, character-sheet, room-state, display-commands]

# Dependency graph
requires:
  - phase: 06a-base-attributes-and-combat
    provides: "base_attributes module with STAT_NAMES, get_stat_descriptor, derive_max_hp, derive_max_stamina"
  - phase: 04-domain-fingerprints-guild-engine
    provides: "guild_engine with GUILDS, SUBCLASSES, FINGERPRINTS, get_domain_proficiency_label, get_guild_tier_label"
provides:
  - "CmdStatus: full character sheet display (status/score/stats/sheet)"
  - "CmdSense: room atmosphere display (sense/perceive/feel)"
affects: [08-player-surface-commands, player-experience]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Lazy imports inside func() for Evennia commands", "Descriptor-only stat display (D-07)", "Proficiency-label-only domain display (D-08)"]

key-files:
  created:
    - commands/cmd_status.py
    - commands/cmd_sense.py
  modified:
    - commands/default_cmdsets.py

key-decisions:
  - "Used ndb.hp/ndb.stamina (correct codebase attribute names) instead of plan's ndb.current_hp/ndb.current_stamina"
  - "Domain resource displayed from ndb.domain_resource dict structure (type/current/max)"

patterns-established:
  - "Player surface commands use lazy imports inside func() and help_category='General'"
  - "Sense command shows all active flags in SENSE_PRIORITY order then remaining alphabetically"

requirements-completed: [PSC-01, PSC-10]

# Metrics
duration: 2min
completed: 2026-03-31
---

# Phase 08 Plan 02: Status and Sense Commands Summary

**CmdStatus character sheet with descriptor-only stats/proficiency-label domains, CmdSense room atmosphere from SENSE_DISPLAY flags**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-31T00:30:36Z
- **Completed:** 2026-03-31T00:33:06Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Full character sheet command (status/score/stats/sheet) displaying vitals, descriptor-only stats, dimensions, proficiency-label domains, guild/subclass, economy, loadout
- Room atmosphere command (sense/perceive/feel) surfacing SENSE_DISPLAY text for active room state flags in priority order
- Both commands registered in CharacterCmdSet

## Task Commits

Each task was committed atomically:

1. **Task 1: Create CmdStatus character sheet display** - `bf702d9` (feat)
2. **Task 2: Create CmdSense + register both commands** - `b829c58` (feat)

## Files Created/Modified
- `commands/cmd_status.py` - Full character sheet display with 6 sections (vitals, stats, dimensions, domains, economy, loadout)
- `commands/cmd_sense.py` - Room atmosphere from active flags using SENSE_DISPLAY and SENSE_PRIORITY
- `commands/default_cmdsets.py` - Registered CmdStatus and CmdSense in CharacterCmdSet

## Decisions Made
- Used `ndb.hp` and `ndb.stamina` instead of plan's `ndb.current_hp`/`ndb.current_stamina` -- matches actual codebase attribute names from characters.py and base_attributes.py
- Domain resource display reads `ndb.domain_resource` dict (type/current/max) from ability_engine.initialize_domain_resource

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Corrected ndb attribute names for HP/Stamina**
- **Found during:** Task 1 (CmdStatus implementation)
- **Issue:** Plan specified `char.ndb.current_hp` and `char.ndb.current_stamina` but codebase uses `char.ndb.hp` and `char.ndb.stamina`
- **Fix:** Used correct attribute names matching characters.py at_object_creation and base_attributes.py derive_hp/derive_stamina
- **Files modified:** commands/cmd_status.py
- **Verification:** Confirmed via grep of typeclasses/characters.py (lines 109-110)
- **Committed in:** bf702d9 (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Essential correctness fix. No scope creep.

## Issues Encountered
- Git worktree had corrupt objects in index from stale files (brainstorm.md, execute-plan.md, write-plan.md). Fixed with `git read-tree HEAD` to rebuild clean index from last commit.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Status and sense commands ready for player use
- Pattern established for additional Phase 8 surface commands

## Self-Check: PASSED

All files exist, all commits verified.

---
*Phase: 08-player-surface-commands*
*Completed: 2026-03-31*
