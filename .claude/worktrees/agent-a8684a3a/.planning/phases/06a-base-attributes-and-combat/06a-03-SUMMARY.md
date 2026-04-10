---
phase: 06a-base-attributes-and-combat
plan: 03
subsystem: combat
tags: [damage-resolution, critical-hits, corpse-container, ability-wiring, zone-scaling]

requires:
  - phase: 06a-01
    provides: "7-stat system, HP/stamina derivation, stat growth, action budget"
  - phase: 06a-02
    provides: "Status effects, compound matrix, tick processing, effect modifiers"
  - phase: 05
    provides: "Ability registry with 14 stub abilities, ability engine dispatcher"
provides:
  - "Combat damage resolution: basic attacks, ability damage, healing"
  - "Critical hit system: Acuity-driven crit chance, 2.0x multiplier"
  - "Elite/boss scaling modifiers per vault spec (1.40x/1.80x incoming)"
  - "CorpseContainer typeclass with killer-locked loot phases"
  - "Death handling for mobs and players"
  - "DOMAIN_TO_STAT mapping (10 domains to 7 stats)"
  - "All 10 ability effect handlers wired to real combat resolution"
affects: [06a-04, 06a-05, 06a-06, 06a-07, 06b]

tech-stack:
  added: []
  patterns:
    - "Lazy import pattern in effect handlers for circular dependency avoidance"
    - "DOMAIN_TO_STAT mapping for ability scaling to base stat resolution"
    - "Corpse loot phase state machine: locked -> open -> decayed"
    - "delay() callbacks for corpse phase transitions"

key-files:
  created:
    - world/combat_engine.py
  modified:
    - typeclasses/objects.py
    - world/ability_engine.py

key-decisions:
  - "DOMAIN_TO_STAT validated against all ability_registry.py entries at execution time"
  - "Mob basic attack uses proportional scaling from ref damage range"
  - "Player corpses start in open phase immediately (no grace period)"
  - "_move_room_loot_to_corpse moves SoravelonItem instances from room to corpse"

patterns-established:
  - "Combat math chain: raw -> crit -> zone_scaling -> resistance -> elite/boss -> weaken reduction"
  - "Effect handlers return message strings; use_ability wraps in (bool, str) tuple"

requirements-completed: [CMB-01, CMB-02, CMB-04]

duration: 5min
completed: 2026-03-26
---

# Phase 06a Plan 03: Combat Engine Core Summary

**Damage resolution with zone scaling, Acuity-driven crits (2.0x), ability effect wiring, and killer-locked corpse containers**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-26T18:56:38Z
- **Completed:** 2026-03-26T19:01:47Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Combat engine with basic attack, ability damage, and heal resolution integrating zone scaling, elemental resistance, and critical hits
- CorpseContainer typeclass with 3-phase loot system (locked/open/decayed) and group-aware access control
- All 10 ability effect handlers replaced: stubs removed, wired to combat_engine and status_effects

## Task Commits

Each task was committed atomically:

1. **Task 1: Create combat_engine.py + CorpseContainer** - `39ca5e3` (feat)
2. **Task 2: Wire ability_engine.py handlers** - `91fc704` (feat)

## Files Created/Modified
- `world/combat_engine.py` - Damage resolution, crit system, death handling, corpse spawning, elite/boss scaling
- `typeclasses/objects.py` - Added CorpseContainer class with killer-locked loot phases
- `world/ability_engine.py` - Replaced all 10 stub handlers with real combat/status effect wiring

## Decisions Made
- DOMAIN_TO_STAT mapping covers all 10 domains: combat->strength, subterfuge->agility, naturalism->resonance, resonance->resonance, arcana->mana, diplomacy->presence, alchemy->acuity, tactics->acuity, engineering->acuity, remnance->mana
- Mob basic attack scales proportionally within the zone-scaled damage range rather than applying scale factor to raw
- Player corpses skip the grace period (start at "open" phase) since the player owns their own corpse
- _move_room_loot_to_corpse uses isinstance(obj, SoravelonItem) to identify loot items dropped by at_death

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Git worktree had corrupt objects (.gitattributes, .gitignore blobs missing) after merge from main. Fixed by removing corrupt .gitattributes from index and re-reading HEAD tree with git read-tree.

## Known Stubs

None - all stubs from ability_engine.py have been replaced with real implementations.

## Next Phase Readiness
- Combat engine ready for CombatScript (plan 06a-04) to orchestrate turn-based encounters
- resolve_basic_attack and resolve_ability_damage provide the damage pipeline
- CorpseContainer ready for loot commands and group loot mode integration

## Self-Check: PASSED

- FOUND: world/combat_engine.py
- FOUND: typeclasses/objects.py
- FOUND: world/ability_engine.py
- FOUND: .planning/phases/06a-base-attributes-and-combat/06a-03-SUMMARY.md
- FOUND: 39ca5e3
- FOUND: 91fc704

---
*Phase: 06a-base-attributes-and-combat*
*Completed: 2026-03-26*
