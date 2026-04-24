# Soravelon Wave 1 Lifecycle Remediation

**Date:** 2026-04-22
**Depends on:** `docs/superpowers/plans/2026-04-22-wave1-lifecycle-and-persistence-audit.md`

## Scope
This pass implemented and verified the four Wave 1 fixes:

- reconnect/login no longer wipes combat-critical runtime state
- logout no longer force-removes a player from live combat
- respawn no longer picks an arbitrary global `respawn_point`
- lifecycle behavior now has direct regression coverage

## Files Changed

- `world/session_lifecycle.py`
- `world/combat_engine.py`
- `tests/test_session_lifecycle.py`
- `tests/test_combat_engine.py`

## What Changed

### Reconnect no longer resets live runtime state
- `world/session_lifecycle.py` now validates whether an existing `combat_handler` is still active before using it.
- Login now restores existing `ndb` runtime state when it already exists instead of blindly resetting:
  - `hp`
  - `stamina`
  - `active_effects`
  - `ability_cooldowns`
  - `combat_target_id`
  - `actions_remaining`
  - `ability_used_this_turn`
  - `charged_ability`
  - `ancestry_ability_used`
  - `domain_resource`
- This closes the disconnect/reconnect exploit where players could clear pressure, wipe cooldowns, and refresh ability economy by reconnecting.

### Reconnect during combat now rehydrates the player surface
- If a player reconnects while still owned by an active `combat_handler`, login now:
  - re-adds the combat cmdset
  - re-sends the turn prompt if it is their turn
  - pushes a fresh `combat_update`
- This makes reconnect behavior match live encounter reality instead of pretending the encounter ended.

### Logout preserves combat membership instead of dodging the encounter
- `world/session_lifecycle.py` no longer calls `remove_combatant()` during ordinary disconnect.
- When disconnect happens during active combat, the current effect list is copied into `combat_handler.db.active_effects_db` so combat-owned effect recovery remains truthful.
- This lines up with `world/combat_script.py`, which already skips disconnected combatants instead of requiring them to be removed from the encounter.

### Respawn now chooses the nearest reachable recovery point
- `world/combat_engine.py` now performs a room-graph breadth-first search from the death room to find the nearest reachable room tagged `respawn_point`.
- Fallback order is now:
  1. nearest reachable respawn room
  2. `character.home`
  3. first globally tagged respawn room
- This removes global search-order ambiguity once multiple city infirmaries exist.

### Respawn now refreshes player-visible state
- Respawn now:
  - marks the destination room as visited for fog-of-war
  - clears OOB debounce state
  - pushes fresh `status_update`, `stat_update`, `map_update`, and `inventory_update`
- This closes the stale-client-state gap created by `move_hooks=False`.

## Validation

- `python -m py_compile world/session_lifecycle.py world/combat_engine.py tests/test_session_lifecycle.py tests/test_combat_engine.py`
- `python scripts/run_tests.py tests.test_session_lifecycle tests.test_combat_engine tests.test_world_state tests.test_group_engine tests.test_recovery_engine tests.test_content_integration`
- Result: `103` tests passed
- `python scripts/smoke_start.py`
- Result: passed

## Regression Coverage Added

### `tests/test_session_lifecycle.py`
- fresh login initializes missing runtime state
- reconnect preserves active combat state instead of wiping it
- reconnect to active combat re-adds the combat surface
- logout during combat preserves encounter membership and effect snapshots

### `tests/test_combat_engine.py`
- respawn prefers the nearest reachable respawn room instead of first global tag match
- respawn refreshes player-visible state and marks the destination as visited

## Residual Notes

- This remediation fixes the audited disconnect/reconnect exploit path and the multi-hub respawn ambiguity.
- I did **not** run a full DB-backed `area.build()` pass during this remediation.
- I also did **not** treat this as a full restart-persistence redesign; the fix is targeted at the live login/logout lifecycle and active-combat truthfulness audited in Wave 1.

## Wave 1 Verdict After Remediation

- **Wave 1 is now materially healthier and no longer blocked by the original reconnect exploit.**
- The fixed lifecycle path is now directly tested rather than inferred through adjacent engine tests.
- Audit can continue into player-legibility and onboarding without building on a broken state model.
