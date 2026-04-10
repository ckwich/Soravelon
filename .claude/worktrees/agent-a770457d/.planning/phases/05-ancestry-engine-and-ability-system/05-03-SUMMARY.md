---
phase: 05-ancestry-engine-and-ability-system
plan: 03
subsystem: abilities
tags: [ability-engine, effect-dispatch, cooldowns, domain-resources, resonance-sense]

requires:
  - phase: 05-ancestry-engine-and-ability-system/05-01
    provides: "room_state.py with flags, get_dominant_flag, SENSE_DISPLAY, add_room_flag"
  - phase: 05-ancestry-engine-and-ability-system/05-02
    provides: "ability_registry.py with ABILITIES dict, ABILITY_TIERS, EFFECT_TYPES, get_ability"
  - phase: 04-domain-fingerprints-guild-engine
    provides: "guild_engine.py with GUILDS, FINGERPRINTS, get_guild_tier, CharacterGuild model"
provides:
  - "world/ability_engine.py with use_ability(), effect dispatch, cooldown/resource management"
  - "clear_encounter_cooldowns() for combat encounter end"
  - "initialize_domain_resource() for guild member resource setup"
  - "Character ndb volatile state for abilities (cooldowns, ancestry_ability_used, domain_resource)"
  - "Resonance Sense passive hook in at_after_move"
  - "Room activity timestamp tracking for still flag decay"
affects: [05-04-ability-commands, 06-combat-system, ability-engine]

tech-stack:
  added: []
  patterns:
    - "Effect-type dispatch: EFFECT_HANDLERS dict maps effect_type string to handler function"
    - "ndb volatile state pattern: ability_cooldowns, ancestry_ability_used, domain_resource on character.ndb"
    - "Domain resource dict pattern: {type, current, max} on ndb"

key-files:
  created:
    - world/ability_engine.py
  modified:
    - typeclasses/characters.py

key-decisions:
  - "Effect handlers are stubs returning descriptive text; Phase 6 wires real combat effects"
  - "Domain resource initialized at login (not just encounter start) for utility/social abilities"
  - "FINGERPRINTS has no resource_max field; initialize_domain_resource defaults to 100"

patterns-established:
  - "Effect-type dispatch: all abilities route through EFFECT_HANDLERS[effect_type], no per-ability callables"
  - "Cooldown tracking: ndb.ability_cooldowns dict with ability_id -> rounds remaining"
  - "Resource management: build/spend/get/initialize pattern with (bool, str) returns"

requirements-completed: [ABL-02, ABL-03, ABL-05]

duration: 4min
completed: 2026-03-26
---

# Phase 05 Plan 03: Ability Engine Summary

**Ability execution engine with effect-type dispatch, per-encounter cooldown tracking, domain resource management, and Resonance Sense passive hook**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-26T05:49:19Z
- **Completed:** 2026-03-26T05:54:02Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Ability engine with use_ability() dispatching through 10 effect-type handlers
- Cooldown and resource management with CharacterAbility-based access checks
- Character typeclass wired with ndb volatile state init, Sense hook, and room activity tracking

## Task Commits

Each task was committed atomically:

1. **Task 1: Create world/ability_engine.py with use_ability() and effect dispatch** - `f8270bd` (feat)
2. **Task 2: Add Character ndb inits, Sense hook, room activity tracking, and db fields** - `c80a078` (feat)

## Files Created/Modified
- `world/ability_engine.py` - Ability execution engine: use_ability(), 10 effect handlers, cooldown/resource management, access checks
- `typeclasses/characters.py` - Added db fields (remnance_discovered, active_loadout), ndb inits (ability_cooldowns, ancestry_ability_used, domain_resource), at_after_move Sense hook and room activity timestamp

## Decisions Made
- Effect handlers are stubs returning descriptive text -- Phase 6 wires real combat effects
- Domain resource initialized at login (not just encounter start) so utility/social abilities have resources available outside combat
- FINGERPRINTS dict has no resource_max field; initialize_domain_resource uses default of 100

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

- `world/ability_engine.py` lines 23-67: All 10 effect handlers (_handle_damage, _handle_dot, etc.) return descriptive text strings. Phase 6 combat system will wire real combat effects. This is intentional per plan -- stubs validate the dispatch pattern.

## Issues Encountered
- Worktree had corrupted git objects preventing commits; resolved by committing directly to main repo with changes applied to the full (up-to-date) characters.py

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- ability_engine.py ready for Plan 04 to build CmdUseAbility command that calls use_ability()
- Phase 6 combat system can replace stub handlers with real effect implementations
- Resonance Sense passive fires correctly for resonance-primary guild members

---
*Phase: 05-ancestry-engine-and-ability-system*
*Completed: 2026-03-26*
