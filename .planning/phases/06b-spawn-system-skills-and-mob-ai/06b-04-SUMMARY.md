---
phase: 06b-spawn-system-skills-and-mob-ai
plan: 04
subsystem: combat
tags: [mob-ai, casting-time, conditions, pathfinding, bfs, combat-script]

requires:
  - phase: 06a-base-attributes-and-combat
    provides: "combat_ai.py with weight-based ability selection, combat_script.py with CombatScript"
provides:
  - "Casting time mechanic with telegraph + delayed resolution + stun/root interrupt"
  - "6 additional D-13 condition vocabulary keys for mob ability conditions"
  - "is_hunter BFS chase behavior for mobs pursuing fleeing players"
  - "CombatScript pending_mob_casts tracking and round-start resolution"
affects: [mob-templates, zone-content, combat-encounters]

tech-stack:
  added: []
  patterns:
    - "Pending mob cast state on ndb.pending_mob_casts dict keyed by mob_id"
    - "Cast interruption via status effect check at resolution time"
    - "is_hunter uses existing patrol_engine.find_path() BFS for chase"

key-files:
  created: []
  modified:
    - world/combat_ai.py
    - world/combat_script.py

key-decisions:
  - "Cast telegraph emote defaults to generic message if ability has no custom emote"
  - "Pending casts resolve at round start (after end_round increments round number)"
  - "is_hunter flag checked defensively with `mob.db.is_hunter or False` -- no mobs.py modification needed"

patterns-established:
  - "Cast time pattern: select_mob_action returns cast_start -> start_mob_cast registers -> resolve_pending_casts resolves N rounds later"
  - "Condition vocabulary additions follow same lambda(mob, target, ch) -> bool signature"

requirements-completed: [CMB-04]

duration: 4min
completed: 2026-03-26
---

# Phase 06b Plan 04: Mob AI Casting Time, Conditions & Hunter Chase Summary

**Mob casting time with telegraph/interrupt mechanic, 6 vault-spec D-13 conditions, and BFS-pathfinding is_hunter chase behavior**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-26T23:25:33Z
- **Completed:** 2026-03-26T23:29:48Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Added 6 missing D-13 condition keys (pack_present, hp_below_50, hp_below_25, target_rooted, target_blinded, no_target_dot) to CONDITION_CHECKS
- Built full casting time mechanic: cast_start action from select_mob_action, start_mob_cast() registration, resolve_pending_casts() with stun/root interrupt check
- Added is_hunter BFS chase via patrol_engine.find_path() within configurable detection range
- Integrated pending mob cast resolution into CombatScript round progression with proper cleanup on death/combat-end

## Task Commits

Each task was committed atomically:

1. **Task 1: Missing conditions + casting time in combat_ai.py** - `aeea6de` (feat)
2. **Task 2: CombatScript cast resolution integration** - `0f16fda` (feat)

## Files Created/Modified
- `world/combat_ai.py` - Added 6 D-13 conditions, casting time (start_mob_cast, resolve_pending_casts), is_hunter chase (attempt_hunter_chase), updated process_mob_turn for cast_start
- `world/combat_script.py` - Added pending_mob_casts ndb init, cast resolution at round start, _dispatch_resolved_cast method, cast_start action handling, cleanup on death/end

## Decisions Made
- Cast telegraph emote defaults to generic "{mob.key} begins casting a spell..." if ability data has no custom emote
- Pending casts resolve at the start of each new round (after end_round increments round_number and notifies players)
- is_hunter flag checked defensively (`mob.db.is_hunter or False`) so no modification to mobs.py is needed -- flag is set by spawn definitions at spawn time
- _resolve_combatant helper iterates combat_handler._resolve_combatants() rather than doing fresh DB search

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Git worktree index corruption**
- **Found during:** Task 2 commit
- **Issue:** Sparse checkout corruption caused `git add` to fail with "unable to read" errors on .gitattributes and other blobs
- **Fix:** Used `git read-tree HEAD` to rebuild index from last good commit, then re-staged
- **Files modified:** None (git infrastructure fix)
- **Verification:** Commit succeeded after index rebuild

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Git infrastructure fix only, no code impact.

## Issues Encountered
- Worktree had corrupt git objects (missing blobs for .gitattributes and other files). Resolved by rebuilding index from HEAD with `git read-tree HEAD`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Combat AI now has full condition vocabulary, casting time mechanics, and hunter chase
- Mob templates can use cast_time field on abilities for telegraphed spells
- is_hunter flag can be set on spawn definitions for chase-capable mobs
- CombatScript correctly tracks and resolves all pending mob casts

## Self-Check: PASSED

- world/combat_ai.py: FOUND
- world/combat_script.py: FOUND
- 06b-04-SUMMARY.md: FOUND
- Commit aeea6de: FOUND
- Commit 0f16fda: FOUND

---
*Phase: 06b-spawn-system-skills-and-mob-ai*
*Completed: 2026-03-26*
