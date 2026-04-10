---
phase: 06a-base-attributes-and-combat
plan: 01
subsystem: character-stats
tags: [base-attributes, point-buy, descriptors, hp-derivation, stat-growth, combat-prep]

# Dependency graph
requires:
  - phase: 05-ability-system
    provides: "Character typeclass with domain progression, guild system"
provides:
  - "7-stat base attribute system (strength, agility, endurance, mana, acuity, presence, resonance)"
  - "70 unique stat descriptors (10 tiers per stat)"
  - "Point-buy allocation with validation"
  - "Ancestry stat modifiers for 4 ancestries"
  - "HP/stamina derivation formulas"
  - "Action budget and damage modifier from agility"
  - "Initiative calculation for characters and mobs"
  - "Use-driven stat growth with diminishing returns"
  - "Combat ndb slots initialized on character login"
affects: [06a-02, 06a-03, 06a-04, 06a-05, 06a-06, 06a-07]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Stat descriptors replace numeric display for player-facing stats"
    - "Use-driven stat growth via ndb accumulators with diminishing returns"
    - "Combat ndb slots initialized at login, cleaned up at logout"

key-files:
  created:
    - world/base_attributes.py
  modified:
    - typeclasses/characters.py

key-decisions:
  - "Point-buy: 7x10 base + 20 bonus = 90 total pool, min 5 max 25 per stat"
  - "Stat growth: 0.5 XP per use action, 10 XP = 1 stat point, diminishing returns curve"
  - "HP formula: 50 + endurance*5 + backend_level*10"
  - "Stamina formula: 30 + endurance*2"
  - "Action budget: floor(1 + agility/30), capped at 4"

patterns-established:
  - "Stat descriptors: STAT_DESCRIPTORS dict with (threshold, word) tuples per stat"
  - "Combat ndb slots: hp, stamina, combat_handler, active_effects, etc. initialized at login"
  - "Stat growth accumulators: ndb.stat_xp_accumulators flushed at logout alongside domain XP"

requirements-completed: [CMB-01]

# Metrics
duration: 5min
completed: 2026-03-26
---

# Phase 06a Plan 01: Base Attributes Summary

**7-stat attribute system with 70 descriptors, point-buy allocation, HP/stamina derivation, action budget, and use-driven growth**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-26T18:46:54Z
- **Completed:** 2026-03-26T18:51:39Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Created world/base_attributes.py with complete 7-stat system, 70 unique descriptors, point-buy validation, ancestry modifiers, HP/stamina derivation, action budget, initiative, and stat growth
- Extended Character typeclass with base_stats initialization, combat ndb slots, stat growth accumulator flush, and combat cleanup on disconnect

## Task Commits

Each task was committed atomically:

1. **Task 1: Create world/base_attributes.py** - `a449498` (feat)
2. **Task 2: Wire base stats into Character typeclass** - `f57178d` (feat)

## Files Created/Modified
- `world/base_attributes.py` - Full base attribute system: 7 stats, 70 descriptors, point-buy, ancestry modifiers, HP/stamina derivation, action budget, initiative, stat growth
- `typeclasses/characters.py` - Extended with base_stats/stat_xp init, combat ndb slots, stat growth flush, combat cleanup

## Decisions Made
- Point-buy budget: 7 stats at base 10 + 20 bonus points = 90 total; min 5, max 25 per stat
- Stat growth rate: 0.5 XP per use action, 10 accumulated XP = 1 stat point; diminishing returns reuse domain XP bracket pattern
- HP: 50 + endurance*5 + backend_level*10 (endurance=10, level=1 = 110 HP)
- Stamina: 30 + endurance*2 (no level scaling -- stamina is endurance-gated only)
- Action budget: floor(1 + agility/30), hard cap at 4 actions; damage modifier = 1/sqrt(actions)
- Ancestry modifiers: Human (+2 pre, +1 acu), Kau'roran (+3 str, +2 end, -2 acu), Veth (+2 acu, +2 agi, -1 str), Selvar (+2 res, +1 pre, +1 agi, -1 end)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Worktree index had corrupt entries from another project (sparse checkout pollution). Fixed by resetting index with `git read-tree HEAD` before staging Task 2.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Base attributes ready for combat system (06a-02+): all derivation formulas, stat growth, and combat ndb slots in place
- Character typeclass now initializes HP, stamina, and combat state at login
- Action budget and initiative formulas ready for CombatScript integration

---
*Phase: 06a-base-attributes-and-combat*
*Completed: 2026-03-26*
