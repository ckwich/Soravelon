---
phase: 01-patrol-commands-and-flight-paths
plan: 01
subsystem: game-events
tags: [trigger-engine, action-vocabulary, dispatch, once-per-character, cooldown, depth-limit]

# Dependency graph
requires: []
provides:
  - "execute_action() dispatch dict with 12 action types (9 implemented, 3 stubs)"
  - "fire_triggers() event dispatcher with once-per and cooldown constraint enforcement"
  - "Shared action vocabulary all game commands and triggers route through"
affects:
  - 01-02-patrol-engine
  - 01-04-flight-paths
  - future trigger-driven mob/room/item events

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Dispatch dict (ACTION_HANDLERS) with handler functions — prefer over if/elif chains"
    - "Depth parameter (_depth) propagated through execute_action for chaining limit"
    - "SaverDict copy pattern for set/dict mutations on db attributes"
    - "Lazy import inside handler function body to avoid circular dependencies"
    - "once_per_character stored as set in character.db.fired_triggers"
    - "cooldown timestamps stored as dict in character.db.trigger_cooldowns"

key-files:
  created:
    - world/action_vocabulary.py
    - world/trigger_engine.py
    - tests/test_action_vocabulary.py
    - tests/test_trigger_engine.py
  modified: []

key-decisions:
  - "Used unittest.TestCase for trigger_engine tests (not EvenniaTest) — pure-logic module uses only MagicMock, no Evennia DB setup required"
  - "Trigger depth limit enforced at _depth >= 3, not > 3 — consistent with plan spec D-19"
  - "fire_triggers returns None (void) — errors are logged not raised"
  - "Guard on character.account (not hasattr check) — reject non-player objects silently"

patterns-established:
  - "Pattern: Action dispatch via dict — ACTION_HANDLERS[action_type](action_dict, context, _depth)"
  - "Pattern: Trigger constraints checked before execution, recorded after all actions run"
  - "Pattern: Once-per and cooldown state stored on character.db, not on the trigger itself"

requirements-completed:
  - IWA-05
  - IWA-06
  - IWA-07

# Metrics
duration: 25min
completed: 2026-03-24
---

# Phase 01 Plan 01: Action Vocabulary and Trigger Engine Summary

**execute_action() 12-type dispatch dict and fire_triggers() event dispatcher with once-per-character and cooldown constraint enforcement**

## Performance

- **Duration:** 25 min
- **Started:** 2026-03-24T23:10:00Z
- **Completed:** 2026-03-24T23:35:00Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- `world/action_vocabulary.py` with `execute_action()` dispatching to 12 action handlers: 9 implemented (echo, teleport, teleport_to_mob, give_item, take_item, modify_standing, modify_attunement, log_world_event, despawn_self) plus 3 stubs (set_quest_flag, open_dialogue, spawn_mob)
- Depth limit guard: `execute_action()` blocks at `_depth >= 3` with `(False, "Trigger chain depth limit reached.")`
- `world/trigger_engine.py` with `fire_triggers()` iterating triggers in definition order, enforcing once-per-character and cooldown constraints using SaverDict copy pattern
- 17 tests passing: basic dispatch, non-character guard, once-per, cooldown, depth propagation

## Task Commits

Each task was committed atomically:

1. **Task 1: Action Vocabulary Module (RED)** - `d5007d3` (test)
2. **Task 1: Action Vocabulary Module (GREEN)** - `fe4d051` (feat)
3. **Task 2: Trigger Engine Module (RED)** - `f4d4058` (test)
4. **Task 2: Trigger Engine Module (GREEN)** - `74dcf1d` (feat)

_TDD tasks committed as test (RED) then feat (GREEN) pairs._

## Files Created/Modified

- `world/action_vocabulary.py` - 12-action dispatch dict; execute_action() public entry point with depth guard; all handlers use lazy imports
- `world/trigger_engine.py` - fire_triggers() event dispatcher; _check_once_per/_check_cooldown/_record_fired helpers; SaverDict copy pattern for db mutations
- `tests/test_action_vocabulary.py` - 9 test classes, 16 tests (EvenniaTest — committed in prior attempt, d5007d3)
- `tests/test_trigger_engine.py` - 6 test classes, 17 tests (unittest.TestCase — pure mock)

## Decisions Made

- **unittest.TestCase vs EvenniaTest for trigger engine tests:** Trigger engine tests use only MagicMock — no Evennia DB objects needed. Following established project convention (same pattern as test_command_preprocessor.py).
- **depth limit at >= 3:** Plan spec D-19 states "blocked at >= 3" — TRIGGER_CHAIN_DEPTH_LIMIT constant set to 3 and guard is `_depth >= TRIGGER_CHAIN_DEPTH_LIMIT`.
- **fire_triggers guard uses `character.account`:** Checking `.account` attribute presence and truthiness matches Evennia's puppeted character semantics — NPC mobs and non-puppeted chars have None/missing account.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Previous attempt left `world/action_vocabulary.py` complete but uncommitted. Verified correctness before committing (12 handlers, clean import, depth limit working).
- `EvenniaTest` requires full Evennia SESSION_HANDLER initialization; trigger engine tests switched to `unittest.TestCase` per project convention for pure-logic modules.

## Known Stubs

The following stubs exist by design (D-05 per plan — future plans will implement):

| File | Action Type | Reason |
|------|-------------|--------|
| `world/action_vocabulary.py` | `set_quest_flag` | Quest system not yet designed |
| `world/action_vocabulary.py` | `open_dialogue` | Dialogue system not yet designed |
| `world/action_vocabulary.py` | `spawn_mob` | Mob spawn system not yet designed |

These stubs return `(False, "Action '{type}' not yet implemented.")` and are intentional. They do not prevent this plan's goals from being achieved.

## Next Phase Readiness

- `execute_action()` is ready to be called from patrol engine (01-02), flight path commands (01-04), and any future room/mob/item trigger hooks
- `fire_triggers()` is ready to be called from `SoravelonRoom.at_object_receive()` and mob death handlers
- Both modules have lazy imports so circular dependency risk with typeclasses is eliminated

## Self-Check: PASSED

All files verified present:
- world/action_vocabulary.py: FOUND
- world/trigger_engine.py: FOUND
- tests/test_action_vocabulary.py: FOUND
- tests/test_trigger_engine.py: FOUND
- .planning/phases/01-patrol-commands-and-flight-paths/01-01-SUMMARY.md: FOUND

All commits verified:
- d5007d3 test(01-01): add failing tests for action vocabulary module
- fe4d051 feat(01-01): implement action vocabulary with 12 action type dispatch
- f4d4058 test(01-01): add failing tests for trigger engine module
- 74dcf1d feat(01-01): implement trigger engine with once-per and cooldown constraints

---
*Phase: 01-patrol-commands-and-flight-paths*
*Completed: 2026-03-24*
