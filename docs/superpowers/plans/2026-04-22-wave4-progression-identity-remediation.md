# Soravelon Wave 4 Progression and Identity Remediation

**Date:** 2026-04-22
**Depends on:** `docs/superpowers/plans/2026-04-22-wave3-combat-abilities-audit.md`

## Scope
Wave 4 fixed progression and character-identity gaps that made the early game less trustworthy than the authored design. This pass focused on:

- ancestry starting-ability integrity
- ability unlock persistence and self-healing
- guild/domain unlock flow
- player-facing progression legibility

## Files Changed

- `world/ability_registry.py`
- `world/ability_engine.py`
- `world/ancestry_engine.py`
- `world/guild_engine.py`
- `world/world_state.py`
- `world/session_lifecycle.py`
- `commands/cmd_status.py`
- `world/help_entries.py`
- `tests/test_ability_engine.py`
- `tests/test_ancestry_engine.py`
- `tests/test_guild_engine.py`
- `tests/test_session_lifecycle.py`
- `tests/test_help_entries.py`

## What Changed

### Missing ancestry abilities are now fully authored
- Added real runtime entries for the four ancestry starter abilities that the ancestry system already referenced:
  - `second_wind`
  - `immovable`
  - `vanish`
  - `audacity`
- These are now part of the canonical registry instead of dangling references, so ancestry identity starts with a real mechanical hook instead of a missing unlock.

### Ancestry abilities stay out of the generic domain pool
- `world/ability_registry.py` now excludes `unlock_source == "ancestry"` from the derived domain tier pool.
- This keeps starting identity distinct from normal domain progression and prevents ancestry abilities from leaking into unrelated unlock paths.

### Ability unlocks now self-heal instead of silently drifting
- `world/ability_engine.py` now exposes:
  - `get_expected_unlocked_ability_ids(character)`
  - `sync_character_ability_unlocks(character)`
- The expected unlock set is derived from authored character state:
  - ancestry starter ability
  - primary-domain abilities up to current guild tier
  - subclass signature abilities when their tier threshold is met
- `_check_ability_access()` now backfills missing `CharacterAbility` rows when a character should legitimately know the requested ability.
- This closes the gap between authored progression and stored unlock records without forcing a destructive migration.

### Unlock sync now runs at the places players actually progress
- `set_ancestry()` now grants the starter identity package and syncs ability access in one pass.
- `join_guild()` now syncs abilities after initializing the guild/domain state.
- `commit_session_xp()` now re-syncs unlocks after recalculating level, guild tier, and attunement progress.
- `on_login()` now performs the same sync, which makes reconnects resilient if a legacy character record is missing unlock rows.

### Player-facing progression visibility is cleaner
- `status` now shows loadout ability display names instead of raw registry ids.
- `loadout` help was updated to match the live command surface:
  - `loadout add <ability>`
  - `loadout remove <ability>`
  - `loadout clear`
  - `loadout save <slot#>`
  - `loadout <slot#>`
- This removes a stale command-help mismatch at exactly the point where players manage their combat kit.

## Regression Coverage Added

### `tests/test_ability_engine.py`
- ancestry abilities are authored and excluded from the derived domain pool
- expected unlock calculation includes ancestry, domain tiers, and signature tiers
- sync grants missing ability rows additively

### `tests/test_guild_engine.py`
- joining a guild grants tier-one domain abilities
- higher guild-tier state grants the correct additional domain and signature unlocks

### `tests/test_session_lifecycle.py`
- login now triggers unlock sync during the session restore path

### `tests/test_ancestry_engine.py`
- ancestry tests now explicitly cover the new unlock-sync side effect

### `tests/test_help_entries.py`
- `loadout` help is pinned to the live command shape

## Validation

- `python -m py_compile world/ability_registry.py world/ability_engine.py world/ancestry_engine.py world/guild_engine.py world/world_state.py world/session_lifecycle.py commands/cmd_status.py world/help_entries.py tests/test_ability_engine.py tests/test_guild_engine.py tests/test_ancestry_engine.py tests/test_session_lifecycle.py tests/test_help_entries.py`
- `python scripts/run_tests.py tests.test_ability_engine tests.test_guild_engine tests.test_ancestry_engine tests.test_session_lifecycle tests.test_help_entries tests.test_world_state`
  - Result: `178` tests passed
- `python scripts/smoke_start.py`
  - Result: passed

## Wave 4 Verdict

- **Wave 4 is no longer carrying a progression-identity integrity gap.**
- Every ancestry now starts with a real authored ability, expected unlocks can be restored from authoritative character state, and the player-facing loadout surface is more legible.
- This makes the progression stack much safer for launch because missing unlock records now degrade into self-repair instead of invisible power loss.
