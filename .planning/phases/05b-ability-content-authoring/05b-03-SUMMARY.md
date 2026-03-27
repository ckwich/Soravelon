---
phase: 05b-ability-content-authoring
plan: 03
subsystem: abilities
tags: [arcana, resonance, mana, attunement, spellcasting, builder-spender, attuned-variants]

# Dependency graph
requires:
  - phase: 05b-ability-content-authoring plan 01
    provides: Combat + Tactics pool and signature abilities
  - phase: 05b-ability-content-authoring plan 02
    provides: Subterfuge + Diplomacy pool and signature abilities
provides:
  - 15 Arcana domain pool abilities (T1-T4, mana resource)
  - 15 Resonance domain pool abilities (T1-T4, resonance resource with attuned_variants)
  - 18 Arcana-primary subclass signatures (9 subclasses x 2)
  - 18 Resonance-primary subclass signatures (9 subclasses x 2, all with attuned_variants)
affects: [05b-04, 05b-05, 05b-06, ability-engine, combat-engine]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Charged abilities (charge_turns 1-2) dominant in caster domains"
    - "Builder/spender pattern: 0-cost builders generate resource, 60-100 cost spenders consume it"
    - "Attuned variants: room flag keyed dict with extra_effect and extra_cost per variant"

key-files:
  created: []
  modified:
    - world/ability_registry.py

key-decisions:
  - "Arcana mana costs 15-70 range to support cross-encounter rationing (pool ~200)"
  - "Resonance builders all cost 0 resonance, generating 15-20 per use; spenders require 60-100"
  - "All 15 Resonance pool abilities have attuned_variants (not just signatures)"
  - "Resonance T4 capstones cost full 100 resonance for maximum payoff feel"
  - "Arcana T4 capstones all require charge_turns=2 for dramatic channel feel"
  - "Sealwright Seal Break = highest single-target damage in Resonance guild at base 250"
  - "Sealreader Truth Unbound = most dangerous ability narratively, corrupted_death +100% damage variant"

patterns-established:
  - "Caster domain pool: T1 cheap instant/quick, T2 moderate channeled, T3 expensive channeled, T4 devastating 2-turn channels"
  - "Builder/spender pool: T1 all builders (0 cost, generate resource), T2 mix (builders + first spenders at 60), T3 powerful spenders at 80, T4 full-100 spenders"
  - "Subclass signature naming: {subclass_id}_{ability_snake_name} for unique ID"

requirements-completed: [ABL-04]

# Metrics
duration: 6min
completed: 2026-03-27
---

# Phase 05b Plan 03: Arcana + Resonance Abilities Summary

**66 ability definitions for Arcana (mana-based caster) and Resonance (builder/spender with attuned room-flag variants) domains, including 36 subclass signatures**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-27T19:55:56Z
- **Completed:** 2026-03-27T20:01:38Z
- **Tasks:** 2 (1 auto + 1 auto-approved checkpoint)
- **Files modified:** 1

## Accomplishments
- Authored 15 Arcana pool abilities spanning fire/ice/lightning elements with meaningful mana costs for cross-encounter rationing
- Authored 15 Resonance pool abilities with full builder/spender pattern: 0-cost builders and 60-100 cost spenders, every ability having attuned_variants
- Authored 18 Arcana-primary subclass signatures covering battlemage, mistveil, stormweaver, spellseeker, enchantvoice, fusewright, wardcaller, runewright, voidscribe
- Authored 18 Resonance-primary subclass signatures covering runebreaker, greymantle, thornweald, sealwright, lorekeeper, corroder, nodecaller, arcanist, sealreader -- all with attuned_variants matching their documented room flags
- Removed 3 arcana/resonance stubs (arcane_bolt, pulse_attune, resonance_ward) and replaced with full definitions

## Task Commits

Each task was committed atomically:

1. **Task 1: Author 66 Arcana + Resonance ability definitions** - `b3f3ff1` (feat)
2. **Task 2: User review** - auto-approved in auto mode

## Files Created/Modified
- `world/ability_registry.py` - Added 66 ability entries (+1771 lines), removed 3 stubs

## Decisions Made
- Arcana pool uses charge_turns extensively (20 charged abilities) to reinforce caster identity per D-08
- Resonance pool splits cleanly: T1 = pure builders (0 cost, +15-20 res), T2 = first spenders (60 threshold), T3 = powerful spenders (80), T4 = full 100 spenders
- All Resonance pool abilities (not just signatures) have attuned_variants to reinforce the ATTUNE fingerprint throughout progression
- Sealwright gets highest burst (Seal Break base 250 with +80% in resonant rooms = effective 450) as documented in vault
- Arcana T4s all require charge_turns=2 with costs 60-70 mana -- represents significant resource investment across encounters
- Voidscribe Firstform Casting uses resistance bypass as its unique mechanic, reflecting pre-cursor spellforms

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Known Stubs
None. All 66 abilities have concrete effect_params, descriptions, and values.

## Next Phase Readiness
- Arcana and Resonance domains fully authored, ready for next domain pair (Naturalism + Alchemy in 05b-04)
- 6 of 10 domains now have full ability content (Combat, Tactics, Subterfuge, Diplomacy, Arcana, Resonance)
- 4 domains remaining: Naturalism, Alchemy, Engineering, Remnance

---
*Phase: 05b-ability-content-authoring*
*Completed: 2026-03-27*
