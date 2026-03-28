---
phase: 05c-ability-polish-and-resource-engine
plan: 01
subsystem: game-logic
tags: [abilities, ability-registry, combat-design, loadout-balance]

# Dependency graph
requires:
  - phase: 05b-ability-content-authoring
    provides: 330 authored abilities with effect_params
provides:
  - 17 redesigned abilities with unique mechanics (no redundant loadout slots)
  - New effect_params fields: piercing, is_multi_hit, aoe, heal_over_time, reflect_damage, bleed, applies_to_next_attack, resource_refund, echoes_generated, ignores_armor
affects: [05c-02, 06a, combat-system, ability-engine]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Ability differentiation via effect_params mechanics (not damage number bumps)"
    - "AoE flag pattern for multi-target abilities"

key-files:
  created: []
  modified:
    - world/ability_registry.py

key-decisions:
  - "Arcane bolt uses piercing (ignores resistance) at lower damage as anti-ward niche"
  - "Frost shard becomes T1 CC (slow status) rather than competing on damage"
  - "Absolute zero becomes hard CC (frozen 3 rounds) instead of damage competitor to arcane_cataclysm"
  - "Meteor strike gains AoE rather than more single-target damage"
  - "Harmonic shield gains damage reflection (25%) to make defense attractive"
  - "Remnance weaken progression already well-differentiated across tiers (T1: 2/0.10, T2: 3/0.12, T4: 4/0.20+slow)"

patterns-established:
  - "AoE abilities use effect_params aoe: True flag"
  - "Piercing abilities use piercing: True to bypass resistance"
  - "Multi-hit abilities use is_multi_hit/hit_count/damage_per_hit"
  - "HoT abilities use heal_over_time: True with hot_duration"
  - "Damage reflection uses reflect_damage: True with reflect_percent"

requirements-completed: []

# Metrics
duration: 4min
completed: 2026-03-28
---

# Phase 5c Plan 01: Ability Redundancy Fixes Summary

**17 redundant abilities across 8 domains redesigned with unique mechanics (AoE, piercing, multi-hit, bleed, reflection, CC) so every ability is loadout-worthy**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-28T01:02:29Z
- **Completed:** 2026-03-28T01:06:36Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments
- All 17 identified redundant abilities now have unique effect_params mechanics
- No ability's damage_base was simply increased -- each fix adds a qualitative differentiator
- Total ability count remains exactly 330 (no abilities added or removed)
- Remnance weaken debuff tier progression reviewed and confirmed already well-differentiated

## Task Commits

Each task was committed atomically:

1. **Task 1: Redesign ~18 redundant abilities with unique mechanics** - `837e123` (feat)

## Files Created/Modified
- `world/ability_registry.py` - Updated 17 ability definitions with new effect_params and descriptions

## Decisions Made
- Arcane bolt: piercing flag at 28 base damage (lower than spark_jolt's 40 but ignores all resistance)
- Frost shard: changed from damage to status effect_type (slow 0.7 for 2 rounds with 20 base damage)
- Absolute zero: changed from damage to status effect_type (frozen 1.0 for 3 rounds with 140 base damage)
- Meteor strike: kept burn status but added AoE with secondary 120 aoe_damage_base
- Death of a thousand reads: kept consumes_all_focus but added multi-hit (5x40) for per-hit proc differentiation
- Harmonic shield: kept warding buff but added reflect_damage/reflect_percent for retaliation niche
- Pre_curse_strike: increased damage_base from 95 to 110 AND added weaken status (damage+debuff combo)
- Remnance weaken differentiation: confirmed T1 (dur 2, mag 0.10), T2 (dur 3, mag 0.12), T4 (dur 4, mag 0.20 + slow) -- already clear progression, no changes needed

## Deviations from Plan

None - plan executed exactly as written. The plan listed ~18 abilities but 17 were unique entries (the Remnance weaken differentiation review item confirmed existing progression is adequate, requiring no additional changes).

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All abilities are now loadout-worthy with unique mechanics
- Ready for 5c-02 (resource engine implementation) which will wire resource-type-aware handlers
- New effect_params fields (aoe, piercing, multi-hit, etc.) will need combat engine support in future phases

---
*Phase: 05c-ability-polish-and-resource-engine*
*Completed: 2026-03-28*
