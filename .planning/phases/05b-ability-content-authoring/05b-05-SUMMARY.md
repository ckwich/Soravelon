---
phase: 05b-ability-content-authoring
plan: 05
subsystem: game-content
tags: [abilities, engineering, remnance, companion, echoes, components]

# Dependency graph
requires:
  - phase: 05b-ability-content-authoring (plans 01-04)
    provides: "264 abilities across 8 domains (combat, tactics, subterfuge, diplomacy, arcana, resonance, naturalism, alchemy)"
provides:
  - "66 Engineering + Remnance ability definitions completing all 330 abilities"
  - "15 companion-centric Engineering pool abilities with fuel system"
  - "15 investigation-as-power Remnance pool abilities"
  - "18 Engineering-primary subclass signatures reflecting companion chassis"
  - "18 Remnance-primary subclass signatures with hidden domain identity"
affects: [ability-engine, combat-engine, phase-06]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Companion-centric ability design (Engineering pool abilities reference mechanical companion)"
    - "Investigation bonus mechanic (Remnance abilities scale with accumulated echoes)"
    - "Base-8 resonance pattern for Bucketborn (accidental correctness theme)"

key-files:
  created: []
  modified:
    - "world/ability_registry.py"

key-decisions:
  - "Engineering companion commands (deploy_sentry, companion_intercept, companion_overdrive) form the backbone of the pool -- the companion IS the Engineering identity"
  - "Remnance abilities use excavation/memory language exclusively -- no 'spell' or 'cast' terminology, reinforcing the hidden domain's pre-magic identity"
  - "Sealbreaker Curse Break has charge_turns=2 (longest in game) and damage_base=250 (highest) -- genuinely the most dangerous ability"
  - "Bucketborn Base-8 Resonance includes ancient_effect flag for future Gidget lore integration"
  - "runewright_forge subclass key (not runewright) used for Engineering+Resonance signatures, matching guild_engine.py SUBCLASSES dict"

patterns-established:
  - "Companion ability naming: verb + companion role (Deploy Sentry, Companion Intercept, Companion Overdrive)"
  - "Remnance ability naming: excavation verbs and memory nouns (Memory Strike, Echo Excavation, Void Excavation)"
  - "Room flags: Engineering writes 'fortified', 'trapped', 'mechanized'; Remnance writes 'ancient_presence', 'void_touched', 'corrupted_death', 'excavated'"

requirements-completed: [ABL-04]

# Metrics
duration: 6min
completed: 2026-03-27
---

# Phase 5b Plan 05: Engineering + Remnance Abilities Summary

**66 abilities authored: companion-centric Engineering (components/fuel system) and investigation-as-power Remnance (echoes/pre-curse knowledge) completing all 330 game abilities across 10 domains**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-27T20:13:27Z
- **Completed:** 2026-03-27T20:19:34Z
- **Tasks:** 2 (1 auto + 1 auto-approved checkpoint)
- **Files modified:** 1

## Accomplishments
- 15 Engineering pool abilities with companion commands, device deployment, fuel system (Standard/Enhanced/Overcharge)
- 15 Remnance pool abilities with excavation theme, investigation bonus scaling, pre-curse power language
- 18 Engineering subclass signatures reflecting 9 distinct companion chassis (Ironsmith combat, Gearhand scout, Growsmith living wood, Runewright rune-slotted, Sparkshaper magical, Dealsmith economic, Siegewright heavy, Fumehand chemical, Bucketborn accidental base-8)
- 18 Remnance subclass signatures reflecting hidden domain identity (Dragonkin physical transformation, Truthshadow armor-ignoring truth, Worldroot nature-ancient hybrid, Sealbreaker curse-breaking danger, Firstform pre-school spellcraft, Ancientvoice authority debuff, Rootpoison dragon-origin toxin, Firstblade forgotten tactics, Dragonwright drake engine summon)
- All 330 abilities complete across all 10 domains. Zero stubs remain in the entire registry.

## Task Commits

1. **Task 1: Author 66 Engineering + Remnance ability definitions** - `598927b` (feat)
2. **Task 2: User review (auto-approved)** - N/A (checkpoint)

## Files Created/Modified
- `world/ability_registry.py` - Added 66 Engineering + Remnance abilities, removed deploy_turret and echo_probe stubs (+1745 -42 lines)

## Decisions Made
- Engineering companion as pool identity: Deploy Sentry, Companion Intercept, Reinforce Chassis, Companion Overdrive, etc. are all companion-centric. The companion IS the Engineering domain.
- Remnance avoids all magical terminology: "remember", "excavate", "uncover" instead of "cast", "spell", "enchant". Reinforces hidden domain mystery.
- Sealbreaker Curse Break: charge_turns=2, damage_base=250, 0.85 application_chance. The most dangerous ability in the game per vault design. World_effect flag for future world-state integration.
- Bucketborn abilities include random_bonus and ancient_effect flags for future "happy accident" randomization system.
- Used runewright_forge key (not runewright) for Engineering+Resonance subclass -- runewright is Arcana+Engineering in guild_engine.py.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Corrected runewright subclass key to runewright_forge**
- **Found during:** Task 1 (ability authoring)
- **Issue:** Plan referenced "runewright" for Engineering+Resonance, but guild_engine.py uses "runewright_forge" (runewright is Arcana+Engineering)
- **Fix:** Used runewright_forge as subclass_id for both Engineering+Resonance signatures
- **Files modified:** world/ability_registry.py
- **Verification:** Verification script passes with dynamic subclass key lookup
- **Committed in:** 598927b

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Key correction to match actual guild_engine.py data. No scope creep.

## Issues Encountered
None beyond the runewright/runewright_forge key resolution.

## Known Stubs
None -- all 330 abilities have concrete descriptions, effect_params, and values.

## Next Phase Readiness
- All 330 abilities are authored. Phase 5b ability content authoring is complete.
- Ready for Phase 5b Plan 06 (final validation pass) or Phase 6 progression.

---
*Phase: 05b-ability-content-authoring*
*Completed: 2026-03-27*
