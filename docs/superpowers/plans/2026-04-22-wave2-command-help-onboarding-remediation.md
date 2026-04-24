# Soravelon Wave 2 Command, Help, and Onboarding Remediation

**Date:** 2026-04-22
**Depends on:** `docs/superpowers/plans/2026-04-22-wave2-command-help-onboarding-audit.md`

## Scope
This pass implemented the Wave 2 fixes for onboarding breadcrumbs, command/help parity, and help truthfulness.

## Files Changed

- `world/session_lifecycle.py`
- `typeclasses/characters.py`
- `commands/cmd_domains.py`
- `commands/cmd_help.py`
- `world/help_entries.py`
- `tests/test_help_entries.py`
- `tests/test_session_lifecycle.py`
- `tests/test_help_command.py`

## What Changed

### New-player guidance is live again
- `world/session_lifecycle.py` now exposes:
  - `get_new_player_guidance(character)`
  - `send_new_player_guidance(character)`
- The breadcrumb ladder now covers real early-session states:
  - no ancestry selected yet
  - ancestry selected but no guild invitation path chosen yet
  - guild-eligible but unguilded players
  - low-level players who need a first quest breadcrumb
- `on_login()` now sends that guidance when the player is not reconnecting into active combat.

### Character hooks expose the promised onboarding helper again
- `typeclasses/characters.py` now includes `_send_new_player_guidance()`.
- The helper delegates to the lifecycle layer instead of duplicating message logic in the typeclass.
- This realigns live code with older internal expectations without moving onboarding back into the typeclass.

### Alias drift was cleaned up
- `commands/cmd_domains.py` no longer claims the alias `skills`.
- This removes an unnecessary overlap with the real `skills` command and makes both command discovery and help lookups cleaner.

### Ability help now resolves the way players expect
- `commands/cmd_help.py` now uses `resolve_ability_help_query()` to support:
  - exact ability ids
  - spaced names
  - underscored names
  - unique prefixes
  - ambiguity prompts when a short prefix matches more than one ability
- This makes `help <ability>` meaningfully closer to `use <ability>` in player ergonomics.

### Command help now matches the live command surface
- `world/help_entries.py` now includes direct command topics for previously missing live commands, including:
  - `inspect`
  - `compare`
  - `fish`
  - `reel`
  - `loot`
  - `prospect`
  - `repair`
  - `rest`
  - `sleep`
  - `wake`
  - `blessing`
  - `who`
  - `shout`
  - `whisper`
  - `tools`
  - `list`
  - `buy`
  - `sell`
  - `appraise`
  - `view`
  - `charge`
- Core system topics were also re-keyed or enriched so the help names players naturally type now land on the useful page:
  - `abilities`
  - `ancestry`
  - `skills`
  - `guilds`
  - `quest`
  - `group`
  - `joinguild`

### Help text now tells the truth about runtime behavior
- `group` help now documents `group lootmode <mode>` instead of the stale `group loot <mode>` wording.
- `joinguild` help now documents the actual secondary-domain decision step.
- Command-help entries previously keyed under names like `domains command` and `quest command` were removed in favor of real player-facing keys.

## Regression Coverage Added

### `tests/test_session_lifecycle.py`
- missing-ancestry guidance
- guildless-but-eligible guidance
- low-level starter breadcrumb guidance
- suppression for states that no longer need onboarding noise

### `tests/test_help_command.py`
- exact spaced-name ability help resolution
- unique-prefix resolution
- ambiguity handling

### `tests/test_help_entries.py`
- command/help parity across the custom command surface
- direct key coverage for the main command and system topics
- truthfulness check for `group lootmode`
- regression guard ensuring `CmdDomains` no longer aliases `skills`

## Validation

- Static command/help parity scan
  - Result: no missing direct help coverage for the scanned custom command keys
- `python -m py_compile world/session_lifecycle.py typeclasses/characters.py commands/cmd_domains.py commands/cmd_help.py world/help_entries.py tests/test_help_entries.py tests/test_session_lifecycle.py tests/test_help_command.py`
- `python scripts/run_tests.py tests.test_help_entries tests.test_session_lifecycle tests.test_help_command tests.test_command_preprocessor tests.test_content_integration`
  - Result: `64` tests passed
- `python scripts/smoke_start.py`
  - Result: passed

## Wave 2 Verdict After Remediation

- **Wave 2 is materially healthier and much more player-legibility complete.**
- The largest onboarding gap is fixed, command/help parity is now directly enforced, and the most important help pages now match real command behavior.
- This closes the biggest “system exists but the player cannot reasonably discover or trust it” problems from the Wave 2 audit.
