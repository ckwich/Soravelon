---
phase: 05c-ability-polish-and-resource-engine
plan: 02
subsystem: combat
tags: [resource-system, ability-engine, combat-lifecycle, domain-resources]

# Dependency graph
requires:
  - phase: 05-ancestry-engine-and-ability-system
    provides: "ability_engine.py with generic resource functions"
  - phase: 06a-base-attributes-and-combat
    provides: "combat_script.py and combat_engine.py with lifecycle hooks"
provides:
  - "10 type-aware resource handlers with RESOURCE_HANDLERS dispatch table"
  - "Type-aware initialize_domain_resource (Focus=5 cap, Balance=50 start, Mana full, Influence from Reputation)"
  - "Post-ability resource hooks for builders/spenders/consumers"
  - "Combat lifecycle integration: per-round decay, encounter-end resets"
  - "Exported helpers: handle_focus_miss, get_balance_modifier, build_momentum_on_damage"
affects: [combat-system, ability-engine, 5c-03-test-suite]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Resource handler dispatch table pattern", "Post-ability hook pattern for builder/spender systems"]

key-files:
  created: []
  modified:
    - world/ability_engine.py
    - world/combat_script.py
    - world/combat_engine.py

key-decisions:
  - "Resource handlers use function dispatch table (not class hierarchy or if/elif chain)"
  - "Balance scaling uses linear interpolation: 1.0 at center, 1.5x at extremes"
  - "Momentum builds on both attacker hit (+10) and target damage taken (+5)"
  - "Focus miss handling added via status effect miss_chance check in resolve_ability_damage"

patterns-established:
  - "RESOURCE_HANDLERS dict maps resource_type string to handler function"
  - "_post_ability_resource_hook called after every ability for builder/consumer effects"
  - "on_round_end_resources and on_encounter_end_resources for lifecycle integration"

requirements-completed: [ABL-04]

# Metrics
duration: 6min
completed: 2026-03-27
---

# Phase 5c Plan 02: Resource Engine Summary

**10 domain resource handlers with type-aware dispatch, combat lifecycle hooks for decay/build/reset, and Balance/Focus/Momentum combat integration**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-27T16:43:07Z
- **Completed:** 2026-03-27T16:49:00Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Implemented all 10 resource handler functions (momentum, focus, balance, resonance, mana, influence, reagents, command, components, echoes) with RESOURCE_HANDLERS dispatch table
- Made initialize_domain_resource type-aware: Focus cap=5, Balance start=50/max=100, Mana starts full, Influence from Reputation score, Echoes with investigation bonus, Reagents/Components from persistent stock
- Wired combat lifecycle: Resonance decays -10/round, Focus resets on skipped turn or miss, Command builds from ally actions, Momentum builds on hit/damage, Mana recovers 15% at encounter end

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement resource handler dispatch table and type-aware initialization** - `6870b64` (feat)
2. **Task 2: Wire resource lifecycle hooks into combat_script and combat_engine** - `ad7757a` (feat)

## Files Created/Modified
- `world/ability_engine.py` - 10 resource handlers, dispatch table, post-ability hooks, lifecycle functions, Balance/Focus/Momentum helpers
- `world/combat_script.py` - on_round_end_resources in end_round, on_encounter_end_resources in end_combat, ally_action_count tracking
- `world/combat_engine.py` - build_momentum_on_damage in basic attack, handle_focus_miss on ability miss, get_balance_modifier scaling in damage/heal

## Decisions Made
- Resource handlers use function dispatch table (RESOURCE_HANDLERS dict) rather than class hierarchy -- simpler, matches EFFECT_HANDLERS pattern already established
- Balance scaling is linear interpolation: position 0 (Feral) = 1.5x damage, position 100 (Calm) = 1.5x heal, position 50 = 1.0x both
- Momentum builds on both attacker hit (+10) and target damage taken (+5) per D-04
- Added miss_chance check to resolve_ability_damage (matching resolve_basic_attack pattern) to enable Focus miss reset

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Added miss check to resolve_ability_damage**
- **Found during:** Task 2 (combat_engine wiring)
- **Issue:** resolve_ability_damage had no miss_chance check from status effects, but handle_focus_miss needs to trigger on ability miss
- **Fix:** Added get_effect_modifiers miss_chance check at the top of resolve_ability_damage (matching the pattern already in resolve_basic_attack)
- **Files modified:** world/combat_engine.py
- **Verification:** Import resolves, function signature preserved
- **Committed in:** ad7757a (Task 2 commit)

**2. [Rule 1 - Bug] Removed duplicate get_effect_modifiers import in resolve_ability_damage**
- **Found during:** Task 2 (combat_engine wiring)
- **Issue:** After adding the miss check import at the top of the function, the original import on line 319 was redundant
- **Fix:** Removed the duplicate `from world.status_effects import get_effect_modifiers` and reused the variable from the earlier import
- **Files modified:** world/combat_engine.py
- **Committed in:** ad7757a (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (2 bugs)
**Impact on plan:** Both fixes necessary for correctness. The miss check ensures Focus reset triggers properly. No scope creep.

## Issues Encountered
- Git worktree had corrupted sparse-checkout config blocking commits for files outside sparse set. Resolved by disabling sparse checkout and rebuilding the index. Required `--sparse` flag on git add for the second commit.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Resource engine complete, all 10 domains have mechanically distinct resource behavior
- Ready for Plan 03 (test suite) to verify resource handlers and lifecycle hooks
- Balance tuning will happen during Phase 7+ playtesting

---
## Self-Check: PASSED

All 3 files exist. Both commit hashes (6870b64, ad7757a) verified in git log.

---
*Phase: 05c-ability-polish-and-resource-engine*
*Completed: 2026-03-27*
