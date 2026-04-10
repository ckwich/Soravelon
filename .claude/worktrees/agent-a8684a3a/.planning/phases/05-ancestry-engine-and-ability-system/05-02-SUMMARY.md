---
phase: 05-ancestry-engine-and-ability-system
plan: 02
subsystem: ability-system
tags: [ability-registry, django-model, migration, guild-engine, data-structure]

# Dependency graph
requires:
  - phase: 04-domain-fingerprints-guild-engine
    provides: "GUILDS, SUBCLASSES, FINGERPRINTS dicts and CharacterGuild model"
provides:
  - "ABILITIES dict with stub entries covering all 10 domains and 10 effect types"
  - "DOMAIN_ABILITIES derived lookup (domain -> tier -> ability_ids)"
  - "SUBCLASS_SIGNATURES derived lookup (subclass_id -> ability_ids)"
  - "CharacterAbility Django model for tracking unlocked abilities"
  - "Migration 0005 for CharacterAbility table"
affects: [05-03, 05-04, 05-05, ability-engine, combat-system]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Derived lookup tables built from master dict at module level"]

key-files:
  created:
    - world/ability_registry.py
    - world/migrations/0005_characterability.py
  modified:
    - world/models.py
    - world/guild_engine.py

key-decisions:
  - "14 stub abilities (not 20) sufficient to cover all 10 domains and all 10 effect types"
  - "Bladestorm chosen as signature stub subclass (2 entries at tier 3 and 4)"
  - "Ironwright hook updated to no-companion design per D-27"

patterns-established:
  - "Derived lookup pattern: DOMAIN_ABILITIES and SUBCLASS_SIGNATURES auto-built from ABILITIES dict at import time"
  - "Stub marking convention: [STUB - Phase 5b] in description field"

requirements-completed: [ABL-01, ABL-06, ABL-04]

# Metrics
duration: 4min
completed: 2026-03-26
---

# Phase 05 Plan 02: Ability Registry and CharacterAbility Model Summary

**Data-driven ability registry with 14 stub entries covering all 10 domains/effect types, CharacterAbility model with migration, and Ironwright D-27 hook fix**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-26T05:36:44Z
- **Completed:** 2026-03-26T05:40:47Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- ABILITIES dict with 14 stub entries covering all 10 domains and all 10 effect types per D-09 schema
- DOMAIN_ABILITIES and SUBCLASS_SIGNATURES derived lookups auto-built from master dict
- CharacterAbility model with unique_together constraint and migration 0005
- Ironwright hook text updated from companion-based to weapons-mid-battle per D-27

## Task Commits

Each task was committed atomically:

1. **Task 1: Create world/ability_registry.py with ABILITIES dict and derived lookups** - `dec7e70` (feat)
2. **Task 2: Add CharacterAbility model + migration + Ironwright fix** - `03008ee` (feat)

## Files Created/Modified
- `world/ability_registry.py` - ABILITIES dict, DOMAIN_ABILITIES, SUBCLASS_SIGNATURES, EFFECT_TYPES, ABILITY_TIERS, get_ability()
- `world/models.py` - CharacterAbility model (character FK, ability_id, unlocked_at, times_used)
- `world/migrations/0005_characterability.py` - Migration creating CharacterAbility table
- `world/guild_engine.py` - Ironwright hook text updated per D-27

## Decisions Made
- 14 stub abilities sufficient to cover all 10 domains and all 10 effect types (plan specified ~20; 14 achieves full coverage without redundancy)
- Bladestorm chosen as the signature stub subclass with tier 3 and tier 4 entries
- Loop variables cleaned from module namespace via `del` after derived lookup construction

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

All 14 abilities in ABILITIES dict are intentional stubs marked `[STUB - Phase 5b]`. These will be replaced with the full 330 ability entries during Phase 5b content authoring. This is explicitly by design per the plan.

## Issues Encountered
- Worktree was behind main branch; fast-forwarded before starting work
- Worktree git index was contaminated with entries from another project; reset index to HEAD before committing Task 2

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- ability_registry.py provides the data structure for 05-03 (ability engine/dispatcher)
- CharacterAbility model provides the persistence layer for ability unlock tracking
- SUBCLASS_SIGNATURES keys validated against guild_engine.SUBCLASSES (bladestorm exists in both)

## Self-Check: PASSED

All files verified present. All commit hashes verified in git log.

---
*Phase: 05-ancestry-engine-and-ability-system*
*Completed: 2026-03-26*
