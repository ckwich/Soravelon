---
phase: 05b-ability-content-authoring
plan: 04
subsystem: abilities
tags: [naturalism, alchemy, balance-spectrum, reagents, abilities, dot, poison, heal]

# Dependency graph
requires:
  - phase: 05a-ability-engine
    provides: "ability_registry.py schema, ability_engine.py dispatcher, combat_engine.py integration"
  - phase: 05b-01
    provides: "Combat + Tactics pool and signature abilities"
  - phase: 05b-02
    provides: "Subterfuge + Diplomacy pool and signature abilities"
  - phase: 05b-03
    provides: "Arcana + Resonance pool and signature abilities"
provides:
  - "15 Naturalism domain pool abilities (Balance spectrum resource)"
  - "15 Alchemy domain pool abilities (Reagents consumable resource)"
  - "18 Naturalism-primary subclass signatures (9 subclasses x 2)"
  - "18 Alchemy-primary subclass signatures (9 subclasses x 2)"
affects: [05b-05, 05b-06, ability-balance-tuning]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Balance spectrum resource -- abilities describe Feral/Calm push direction in descriptions"
    - "Reagents finite stock -- costs reflect consumable depletion (T1: 5-8, T2: 12-15, T3: 18-25, T4: 30-45)"

key-files:
  created: []
  modified:
    - "world/ability_registry.py"

key-decisions:
  - "Naturalism Balance costs are 10-55 (spectrum shifts, not pool expenditure)"
  - "Alchemy Reagent costs tier: T1 5-8, T2 12-15, T3 18-25, T4 30-45 to feel finite"
  - "Rotweald (naturalism+alchemy) focuses on organic decay/rot; Mireweald (alchemy+naturalism) focuses on distilled/weaponized decay"
  - "Naturalism T4 capstones require specific spectrum positions (Feral/Calm/Neutral)"
  - "Voidbrewer is only alchemy subclass with attuned_variants (resonant/charged flags)"

patterns-established:
  - "Spectrum resource pattern: Balance abilities describe push direction in description text"
  - "Finite resource pattern: Reagent costs lower than other resources to reflect permanent depletion"

requirements-completed: [ABL-04]

# Metrics
duration: 5min
completed: 2026-03-27
---

# Phase 5b Plan 04: Naturalism + Alchemy Abilities Summary

**66 abilities for Naturalism (Balance spectrum) and Alchemy (Reagents consumables) with distinct Rotweald vs Mireweald identity**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-27T20:05:01Z
- **Completed:** 2026-03-27T20:10:18Z
- **Tasks:** 2 (1 auto + 1 auto-approved checkpoint)
- **Files modified:** 1

## Accomplishments
- 15 Naturalism pool abilities with Feral/Calm spectrum push noted in every description
- 15 Alchemy pool abilities with finite Reagent costs (T1: 5-8, T2: 12-15, T3: 18-25, T4: 30-45)
- 18 Naturalism-primary subclass signatures covering all 9 subclasses
- 18 Alchemy-primary subclass signatures covering all 9 subclasses
- Rotweald (naturalism+alchemy) vs Mireweald (alchemy+naturalism) feel distinct despite shared domains
- Removed 3 stubs (wild_mend, reagent_toss, venom_coat) and replaced with full entries

## Task Commits

Each task was committed atomically:

1. **Task 1: Author 66 Naturalism + Alchemy ability definitions** - `e495480` (feat)
2. **Task 2: User review of ability definitions** - auto-approved (checkpoint)

## Files Created/Modified
- `world/ability_registry.py` - 66 new ability entries for naturalism and alchemy domains (1685 lines added, 55 removed)

## Decisions Made
- Naturalism Balance costs range 10-55 (representing spectrum shifts, not pool expenditure)
- Alchemy Reagent costs deliberately lower than other domain resources to reflect permanent stock depletion
- Naturalism T4 capstones tied to spectrum position: Primal Wrath (Feral), Ancient Restoration (Calm), Nature's Equilibrium (Neutral)
- Rotweald signatures use "organic decay" flavor (rot cloud, consuming decay); Mireweald uses "distilled/weaponized" flavor (swamp rot, mire zone)
- Voidbrewer is the only alchemy subclass with attuned_variants, leveraging resonant/charged room flags
- Stormcaller uses charge_turns=2 for Storm Call (longest naturalism charge), matching D-08 guidance for rare physical domain charges

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None - all 66 abilities have complete descriptions, effect_params, and concrete values.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- 8 of 10 domains now complete (Combat, Tactics, Subterfuge, Diplomacy, Arcana, Resonance, Naturalism, Alchemy)
- Ready for 05b-05 (Engineering + Remnance) to complete all 330 abilities

---
*Phase: 05b-ability-content-authoring*
*Completed: 2026-03-27*
