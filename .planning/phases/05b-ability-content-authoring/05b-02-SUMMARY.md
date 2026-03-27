---
phase: 05b-ability-content-authoring
plan: 02
subsystem: abilities
tags: [subterfuge, diplomacy, focus, influence, veilcraft, accord, abilities, combat-data]

requires:
  - phase: 05a-ability-framework
    provides: "ability_registry.py schema, ability_engine.py dispatcher, combat_engine integration"
provides:
  - "33 Subterfuge abilities (15 pool + 18 subclass signatures)"
  - "33 Diplomacy abilities (15 pool + 18 subclass signatures)"
  - "Complete Veilcraft guild ability coverage"
  - "Complete Accord guild ability coverage"
affects: [05b-03, 05b-04, 05b-05, 05b-06, ability-balance-tuning]

tech-stack:
  added: []
  patterns:
    - "Subterfuge abilities use focus resource with instant charge_turns (READ fingerprint)"
    - "Diplomacy abilities use influence resource with mostly instant, some 1-round charges (LEVERAGE fingerprint)"
    - "Pool abilities use single-domain scaling; signatures use primary+secondary domain scaling"

key-files:
  created: []
  modified:
    - "world/ability_registry.py"

key-decisions:
  - "Subterfuge pool focuses on debuff stacking (weaken, blind, slow, poison) with damage payoffs for chains"
  - "Diplomacy pool balances solo damage with group buff utility (haste, warding) per D-11"
  - "Subterfuge Tier 4 capstones split between chain-payoff damage and guaranteed-crit execution"
  - "Diplomacy Tier 4 capstones include AoE charm, massive damage, and AoE weaken+slow"
  - "Wayfinder signatures use heal effect_type for empathic healing niche"
  - "Silkpoison signatures use delayed poison delivery through social interaction"

patterns-established:
  - "Subterfuge room flags: shadow_marked, exposed, scouted"
  - "Diplomacy room flags: intimidated, inspired, ordered"
  - "Cross-domain subclass signatures blend both domain identities in descriptions and mechanics"

requirements-completed: [ABL-04]

duration: 4min
completed: 2026-03-27
---

# Phase 05b Plan 02: Subterfuge + Diplomacy Abilities Summary

**66 abilities for Subterfuge (READ/Focus) and Diplomacy (LEVERAGE/Influence) domains with concrete effect_params, covering 18 subclass signatures across both guilds**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-27T19:48:11Z
- **Completed:** 2026-03-27T19:52:49Z
- **Tasks:** 2 (1 auto + 1 auto-approved checkpoint)
- **Files modified:** 1

## Accomplishments
- 15 Subterfuge pool abilities across tiers 1-4 with burst/debuff/chain identity
- 15 Diplomacy pool abilities across tiers 1-4 with solo-viable social combat identity
- 18 Subterfuge-primary subclass signatures (grimwarden through hollowseen)
- 18 Diplomacy-primary subclass signatures (civicguard through truthwarden)
- Removed shadow_read and diplomatic_leverage stubs
- All 66 abilities have concrete effect_params (damage_base, buff/debuff types, durations, magnitudes)

## Task Commits

Each task was committed atomically:

1. **Task 1: Author 66 Subterfuge + Diplomacy ability definitions** - `24f1813` (feat)

## Files Created/Modified
- `world/ability_registry.py` - Added 66 ability entries, removed 2 stubs (+1622/-36 lines)

## Decisions Made
- Subterfuge charge_turns=0 throughout (instant physical domain per D-08)
- Diplomacy mostly charge_turns=0 with select 1-round charges for dramatic pronouncements (words_of_authority, voice_of_ages, binding_deal, truth_revealed)
- Subterfuge damage values follow T1:30-35, T2:50-60, T3:80-100, T4:180-220 range
- Diplomacy damage values follow same tier ranges, presence-scaled
- Blackthorn signatures have highest poison magnitudes (10/12) per vault lore
- Wayfinder uses heal effect_type (unique among Diplomacy subclasses)
- Tally Agent T4 (Double Agent) is a buff-redirect sideways mechanic per D-14

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## Known Stubs
None - all 66 abilities have complete descriptions and effect_params.

## Next Phase Readiness
- Subterfuge and Diplomacy domains fully populated
- Ready for 05b-03 (Arcana + Resonance) to continue the domain authoring sequence
- Cross-domain subclass interactions (e.g., Tally Agent bridging both domains) are documented in signatures

---
*Phase: 05b-ability-content-authoring*
*Completed: 2026-03-27*
