---
phase: 06a-base-attributes-and-combat
plan: 02
subsystem: combat
tags: [status-effects, dot, compounds, stacking, crowd-control]

# Dependency graph
requires:
  - phase: 06a-base-attributes-and-combat
    provides: "Combat context decisions D-23 through D-25"
provides:
  - "world/status_effects.py with apply_effect, remove_effect, tick_effects, check_compound_triggers, get_effect_modifiers, clear_all_effects"
  - "STACKABLE_EFFECTS, NON_STACKABLE_EFFECTS, COMPOUND_MATRIX constants"
affects: [combat-engine, ability-engine, mob-ai]

# Tech tracking
tech-stack:
  added: []
  patterns: ["ndb.active_effects volatile list for combat status state", "SaverDict copy pattern for effect mutations", "bidirectional compound matrix for O(1) pair lookup"]

key-files:
  created: ["world/status_effects.py"]
  modified: []

key-decisions:
  - "Compound duration defaults to 3 rounds; petrify gets +2 from extended_duration spec"
  - "Immunity checked via both ndb.immunities (volatile) and db.immunities (persistent mob config)"
  - "Compound result types treated as non-stackable for replacement logic"

patterns-established:
  - "Effect entry schema: {type, stacks, duration, magnitude, source_id, max_stacks, is_compound}"
  - "Bidirectional compound matrix: store (a,b) and (b,a) for O(1) lookup"

requirements-completed: [CMB-01]

# Metrics
duration: 2min
completed: 2026-03-26
---

# Phase 06a Plan 02: Status Effects Summary

**Complete status effect system with 5 stackable and 7 non-stackable effects, 4 compound triggers (additive and consuming), diminishing DoT damage tables, and per-round tick processing**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-26T18:46:55Z
- **Completed:** 2026-03-26T18:49:01Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments
- Stackable effects (poison/bleed/burn/weaken/drain) with max stacks and diminishing damage arrays
- Non-stackable effects (slow/root/blind/stun/charm/haste/wet) with stronger-replaces-weaker logic
- 4 compound triggers: venom_lag (additive), corruption (additive), petrify (additive), steam (consuming)
- tick_effects processes DoT damage, drain stamina, duration decay, and petrify-breaks-on-damage
- get_effect_modifiers aggregates action budget, miss chance, skip turn, flee prevention for combat engine

## Task Commits

Each task was committed atomically:

1. **Task 1: Create world/status_effects.py with effect constants and application logic** - `ec4fa13` (feat)

**Plan metadata:** pending (docs: complete plan)

## Files Created/Modified
- `world/status_effects.py` - Full status effect system: constants, apply/remove/tick/compound/modifier functions

## Decisions Made
- Compound duration defaults to 3 rounds; petrify extended_duration adds 2 more for total of 5
- Immunity support via both ndb.immunities (session-volatile) and db.immunities (persistent mob config)
- Compound result types (venom_lag, corruption, petrify, steam) treated as non-stackable for apply logic
- Petrify compound grants both prevents_flee and skip_turn modifiers

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Known Stubs
None - all functions are fully implemented with real logic.

## Next Phase Readiness
- Status effect system ready for combat engine integration (06a-04 CombatScript)
- tick_effects designed to be called at round end per D-11
- get_effect_modifiers ready for action budget computation in combat turns

---
*Phase: 06a-base-attributes-and-combat*
*Completed: 2026-03-26*
