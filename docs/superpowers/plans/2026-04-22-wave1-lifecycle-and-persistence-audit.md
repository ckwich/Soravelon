# Soravelon Wave 1 Lifecycle and Persistence Audit

**Date:** 2026-04-22
**Depends on:** `docs/superpowers/plans/2026-04-22-deep-gameplay-code-health-audit-plan.md`
**Follows:** `docs/superpowers/plans/2026-04-22-wave0-reality-baseline-audit.md`

## Scope
Wave 1 audited the player-state safety path:

- character login and logout
- volatile versus persistent state boundaries
- combat/disconnect interactions
- death and respawn flow
- adjacent verification coverage

## Evidence Reviewed

- `typeclasses/characters.py`
- `world/session_lifecycle.py`
- `world/movement_lifecycle.py`
- `world/world_state.py`
- `world/ability_engine.py`
- `world/status_effects.py`
- `world/combat_engine.py`
- `world/group_engine.py`
- `world/recovery_engine.py`
- `typeclasses/scripts.py`
- `world/areas/vaels_crossing.py`
- `world/areas/varath_prime.py`
- `tests/test_world_state.py`
- `tests/test_group_engine.py`
- `tests/test_recovery_engine.py`
- `tests/test_combat_engine.py`
- `tests/test_content_integration.py`

## Validation Run

- `python scripts/run_tests.py tests.test_world_state tests.test_group_engine tests.test_recovery_engine tests.test_combat_engine tests.test_content_integration`
- Result: `98` tests passed

This confirms adjacent systems are stable under their current tests, but it does **not** prove the full login/logout/reconnect lifecycle is safe.

## Findings

### Blocker
- **Logout/reconnect currently functions as a combat and state reset exploit.**
  - `world/session_lifecycle.py` resets `combat_handler`, `active_effects`, `hp`, `stamina`, `ability_cooldowns`, and guild resource state on login.
  - `world/status_effects.py` explicitly stores all active effects on `ndb`.
  - `world/ability_engine.py` reinitializes guild resources from guild fingerprint defaults, including full-start or default-start pools for several resource types.
  - Combined effect: a player can disconnect and reconnect to drop combat, clear status effects, restore HP/stamina, clear cooldowns, and refresh at least some ability-economy state.
  - This is a launch blocker because it undermines combat fairness, death pressure, and resource management.

### High-Value Fix
- **Respawn routing is now globally ambiguous.**
  - `world/combat_engine.py` resolves respawn by calling `search_tag("respawn_point", category="spawn_point")` and picking the first room returned.
  - There are already at least two live respawn points:
    - `world/areas/vaels_crossing.py`
    - `world/areas/varath_prime.py`
  - Impact: player death routing can become dependent on search ordering instead of zone, region, or intended hometown logic.
  - This became a real gameplay bug once Hub 4 added a second city infirmary.

### High-Value Fix
- **Respawn bypasses movement lifecycle and does not explicitly refresh client state.**
  - `_respawn_player()` uses `move_to(..., move_hooks=False)`.
  - It restores HP/stamina and sends a flavor message, but it does not call movement lifecycle hooks or explicitly push map/status updates afterward.
  - Likely impact: fog-of-war, room-derived map state, and OOB HUD state may lag behind the actual respawn until the next player action.

### Improvement Opportunity
- **Lifecycle orchestration is centralized well enough to fix safely.**
  - `typeclasses/characters.py` delegates login/logout/move work into lifecycle modules.
  - `world/session_lifecycle.py`, `world/movement_lifecycle.py`, and `world/death_lifecycle.py` keep cross-system coordination out of the typeclasses.
  - This is good architecture and lowers remediation risk.

### Improvement Opportunity
- **The current test suite covers adjacent engines, not the real lifecycle path.**
  - `tests/test_world_state.py` validates domain XP commit behavior.
  - `tests/test_group_engine.py` validates `on_member_disconnect()` directly.
  - `tests/test_combat_engine.py` validates corpse handling, but patches out `world.banking.on_character_death`.
  - `tests/test_content_integration.py` only verifies that respawn logic references the `respawn_point` tag string.
  - There is no direct login/logout/reconnect coverage for:
    - `Character.at_post_puppet()`
    - `Character.at_pre_unpuppet()`
    - `world.session_lifecycle.on_login()`
    - `world.session_lifecycle.on_logout()`
    - reconnect during combat
    - reconnect preserving or intentionally resolving combat state

## Recommended Fix Directions

### For the reconnect exploit
- Preserve or explicitly reconcile combat-critical state across reconnects instead of reinitializing it blindly.
- Do not full-heal or clear cooldowns/effects/resources on ordinary reconnect.
- If disconnecting during combat should count as surrender/defeat, resolve that explicitly instead of granting a clean reset.
- Add regression tests for:
  - reconnect during combat
  - reconnect with active effects
  - reconnect with ability cooldowns
  - reconnect with partially spent guild resource pools

### For respawn routing
- Replace “first tagged room” logic with explicit routing:
  - home city
  - zone-family fallback
  - nearest valid medic point
  - or an authored region mapping table
- Add tests for multiple simultaneous respawn points.

### For post-respawn client consistency
- Push explicit status/map updates after respawn, or route respawn through a controlled hook path that preserves intended side effects.
- Add a regression test around death -> respawn -> client-visible state refresh.

## Wave 1 Verdict

- **Wave 1 is not launch-clean yet.**
- The reconnect reset path is a real blocker.
- Respawn routing is already underdefined for the current multi-hub content footprint.
- The surrounding architecture is strong enough that these problems look fixable without major structural churn.
