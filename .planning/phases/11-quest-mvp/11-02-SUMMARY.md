---
phase: 11-quest-mvp
plan: 02
subsystem: quest-infrastructure
tags: [action-vocabulary, area-builder, quest-dsl, scales, skill-xp, node-failure]

# Dependency graph
requires:
  - phase: 01-patrol-commands-and-flight-paths
    provides: action_vocabulary.py dispatch framework
  - phase: 03.1-mob-spawn-runtime
    provides: skill_engine.accumulate_skill_use, node_script interface
provides:
  - 3 new ACTION_HANDLERS (give_scales, give_skill_xp, modify_node_failure)
  - Enriched quest() DSL accepting objectives, rewards, next_quest_id, one_chance
affects: [11-quest-mvp, zone-content, quest-engine]

# Tech tracking
tech-stack:
  added: []
  patterns: [lazy-import action handlers, idempotent quest replace-by-id]

key-files:
  created: []
  modified:
    - world/action_vocabulary.py
    - world/area_builder.py

key-decisions:
  - "Keep set_quest_flag stub for backward compat with legacy triggers"
  - "quest() uses replace-by-quest_id for idempotent reload behavior"
  - "Legacy flat quest fields preserved alongside enriched fields"

patterns-established:
  - "Action handlers use lazy imports for cross-module dependencies"
  - "Quest DSL stores both legacy and enriched fields; quest_engine normalizes at runtime"

requirements-completed: [D-13, D-14, D-21, D-22, D-12]

# Metrics
duration: 3min
completed: 2026-04-03
---

# Phase 11 Plan 02: Action Handlers and Quest DSL Summary

**Three new reward action handlers (give_scales, give_skill_xp, modify_node_failure) and enriched area.quest() DSL with objectives list, rewards list, chain support, and one_chance flag**

## Performance

- **Duration:** 3 min
- **Started:** 2026-04-03T19:15:40Z
- **Completed:** 2026-04-03T19:18:35Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Added give_scales handler that awards Scales to character.db.carried_scales with amount validation
- Added give_skill_xp handler that calls accumulate_skill_use via lazy import from skill_engine
- Added modify_node_failure handler that finds zone via search_tag, adjusts NodeScript failure%, calls _update_state
- Updated area.quest() DSL to accept enriched schema (name, description, objectives, rewards, next_quest_id, one_chance) while preserving all legacy flat fields
- Added idempotent replace-by-quest_id behavior to quest() to prevent duplicate entries on reload

## Task Commits

Each task was committed atomically:

1. **Task 1: Three new action vocabulary handlers** - `63ab94a` (feat)
2. **Task 2: Update area.quest() DSL for enriched schema** - `bbee77e` (feat)

## Files Created/Modified
- `world/action_vocabulary.py` - Added 3 new handlers (_handle_give_scales, _handle_give_skill_xp, _handle_modify_node_failure) and registered in ACTION_HANDLERS dict (now 16 entries)
- `world/area_builder.py` - Updated quest() method with enriched fields and idempotent replace logic

## Decisions Made
- Kept `set_quest_flag: _stub_handler` for backward compatibility with any existing triggers that reference it
- quest() uses replace-by-quest_id to prevent duplicate entries when zone reloads call quest() again with same quest_id
- All legacy flat fields (objective_type, objective_target, objective_count, reward_tiers, etc.) preserved alongside new enriched fields -- quest_engine._normalize_quest_spec() handles conversion at runtime

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Git worktree had corrupted blob objects (missing .gitattributes, .gitignore blobs) -- resolved by resetting index via `git read-tree HEAD` before staging Task 2 changes

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Action vocabulary now supports all quest reward types needed by quest_engine.py
- area.quest() DSL stores the enriched schema needed for full quest specs
- Zone content files can be updated with objectives/rewards lists in subsequent plans
- quest_engine.py (Plan 01) can dispatch rewards via execute_action()

## Self-Check: PASSED

- world/action_vocabulary.py: FOUND
- world/area_builder.py: FOUND
- 11-02-SUMMARY.md: FOUND
- Commit 63ab94a: FOUND
- Commit bbee77e: FOUND

---
*Phase: 11-quest-mvp*
*Completed: 2026-04-03*
