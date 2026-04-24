# Soravelon Wave 10 Test Architecture and Verification Remediation

**Date:** 2026-04-22
**Fixes:** `docs/superpowers/plans/2026-04-22-wave10-test-architecture-and-verification-audit.md`

## Summary
Wave 10 remediation strengthened Soravelon's safety net where the audit found the highest leverage gaps: direct command coverage, semantic integration checks, and lightweight registry-contract protection.

## What Changed

### Replaced brittle source-text checks with semantic assertions
- `tests/test_content_integration.py`
  - Replaced the raw-string `greeter_room` check with an AST-based assertion that `world/areas/vaels_crossing.py` really authors a `greeter_room` tag in the `spawn_point` category.
  - Replaced the `_respawn_player` source-text check with a behavior-level test that proves respawn falls back to globally tagged `respawn_point` rooms when no local route exists.
  - Replaced the `CmdStabilize` cmdset registration string check with a real `CharacterCmdSet.at_cmdset_creation()` assertion that confirms the `stabilize` command is actually added.

### Added direct command-surface coverage
- `tests/test_cmd_guild.py`
  - covers already-guilded rejection
  - covers visible invite listing and hidden guild filtering
  - covers secondary-domain prompting
  - covers successful join dispatch and subclass welcome messaging
- `tests/test_cmd_vendor.py`
  - covers `list`, `buy`, `sell`, `appraise`, and `view`
  - verifies usage errors, no-vendor failures, grouped stock rendering, item lookup, and engine-message passthrough
- `tests/test_cmd_quest.py`
  - covers empty quest journal behavior
  - covers active quest progress rendering
  - covers quest detail output for objectives and rewards
  - covers partial-name quest abandonment dispatch

### Added direct registry coverage
- `tests/test_flight_registry.py`
  - verifies bidirectional route registration
  - verifies shortest multi-leg route finding
  - verifies `clear()` fully resets registry state

## Why This Matters

- The suite now tests more of the literal commands players type instead of assuming engine coverage is enough.
- The critical spawn/respawn checks now validate semantics rather than mere text presence.
- One of the pure-data registries called out in the audit now has its own fast contract coverage instead of only being exercised transitively.

## Validation

- `python -m py_compile tests/test_content_integration.py tests/test_cmd_guild.py tests/test_cmd_vendor.py tests/test_cmd_quest.py tests/test_flight_registry.py`
  - Result: passed
- `python scripts/run_tests.py tests.test_content_integration tests.test_cmd_guild tests.test_cmd_vendor tests.test_cmd_quest tests.test_flight_registry tests.test_help_command tests.test_command_preprocessor`
  - Result: `66` tests passed
- `python scripts/smoke_start.py`
  - Result: passed

## Remaining Wave 10 Opportunities

- Command coverage is meaningfully better, but still not comprehensive. Good next targets are:
  - `abilities`
  - `group`
  - `loot`
  - `rest` / `sleep` / `wake`
  - `status`
  - `map`
  - `search`
  - `loadout`
- More registry-contract passes are still worthwhile for:
  - `dialogue_definitions`
  - `material_definitions`
  - `lore_registry`
  - selected authored help/data cross-links
- The biggest remaining verification gap after this remediation is still golden-path play coverage across multiple systems in sequence.
