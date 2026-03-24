---
phase: 01-patrol-commands-and-flight-paths
plan: "03"
subsystem: command-preprocessor
tags: [commands, alias-system, prefix-matching, character-input]
dependency_graph:
  requires: []
  provides: [command_preprocessor, alias_system, execute_cmd_override]
  affects: [typeclasses/characters.py, commands/default_cmdsets.py]
tech_stack:
  added: []
  patterns:
    - preprocess-input hook via Character.execute_cmd() override
    - SaverDict copy pattern for alias dict mutation
    - unittest.TestCase (not EvenniaTest) for pure-logic module tests
key_files:
  created:
    - world/command_preprocessor.py
    - commands/cmd_alias.py
    - tests/test_command_preprocessor.py
  modified:
    - commands/default_cmdsets.py
    - typeclasses/characters.py
decisions:
  - "Used commands.command.Command (local base) instead of evennia.Command import — evennia lazy-init prevents static class def with bare django.setup()"
  - "Used unittest.TestCase for preprocessor tests (not EvenniaTest) — pure-logic module with MagicMock needs no Evennia DB"
metrics:
  duration: "7 minutes"
  completed: "2026-03-24T23:00:54Z"
  tasks_completed: 2
  files_changed: 5
requirements_addressed: [CMD-01, CMD-02, CMD-03, CMD-04, CMD-05]
---

# Phase 01 Plan 03: Command Preprocessor and Alias System Summary

**One-liner:** Player input routed through prefix resolver and alias expander before Evennia cmdhandler, with persistent per-character alias macros supporting $1/$2/$*/$@ token substitution and 3-command chain cap.

## Tasks Completed

| Task | Description | Commit |
|------|-------------|--------|
| 1 (TDD) | world/command_preprocessor.py — resolve_prefix, expand_alias, preprocess_input | ddc12f5 |
| 2 | commands/cmd_alias.py, default_cmdsets.py update, characters.py execute_cmd + state init | f2fee64 |

## What Was Built

### world/command_preprocessor.py

Three public functions:

- **`resolve_prefix(raw_word, all_cmd_keys)`** — Exact match returns immediately; unique prefix returns expanded key; ambiguous prefix returns `(None, sorted_matches)`; no match returns `(None, [])`.
- **`expand_alias(character, alias_key, raw_args)`** — Looks up `character.db.aliases`, splits expansion by `;`, caps at 3 (D-16), substitutes `$1`/`$2`/`$*`/`$@` tokens. Returns `None` if alias not found.
- **`preprocess_input(character, raw_string)`** — Orchestrates the full pipeline: exact system command match (pass through), alias lookup, prefix resolution, ambiguity error (D-14), no-match pass-through. Returns `str | list[str] | None`.

### commands/cmd_alias.py

`CmdAlias` and `CmdUnalias` commands:
- `CmdAlias` with no args lists current aliases. With `name = expansion` syntax, validates against `SYSTEM_COMMAND_KEYS` (D-17), warns if expansion has >3 chains, stores using SaverDict copy pattern.
- `CmdUnalias` removes a named alias.

### commands/default_cmdsets.py

`CharacterCmdSet.at_cmdset_creation()` now imports and registers `CmdAlias()` and `CmdUnalias()`.

### typeclasses/characters.py

Two additions:

1. **`at_object_creation()`** initializes four new `db` attributes:
   - `db.aliases = {}` — persistent alias storage
   - `db.fired_triggers = set()` — once-per-char trigger tracking
   - `db.trigger_cooldowns = {}` — trigger cooldown timestamps
   - `db.discovered_flight_points = set()` — Dragon Courier discovered stops

2. **`execute_cmd()`** override routes every player command through `preprocess_input()`, handling `None` (abort), `list` (chained alias), and `str` (pass-through) return types.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `from evennia import Command` returns None at import time**
- **Found during:** Task 2 verification
- **Issue:** `evennia.Command` is lazily initialized and returns `None` before the Evennia server is fully started. Using it as a class base in a module-level class definition raises `TypeError: NoneType takes no arguments`.
- **Fix:** Changed import to `from commands.command import Command` — the project's own local `Command` base class which wraps `evennia.commands.command.Command` directly, always available.
- **Files modified:** `commands/cmd_alias.py`
- **Commit:** f2fee64

**2. [Rule 1 - Bug] Tests used EvenniaTest but needed unittest.TestCase**
- **Found during:** Task 1 TDD RED verification
- **Issue:** `EvenniaTest.setUp()` tries to create a DB account with `typeclasses.accounts.Account` — fails when not using project settings. Preprocessor tests use only `MagicMock`, not Evennia DB.
- **Fix:** Switched all test classes from `EvenniaTest` to `unittest.TestCase`.
- **Files modified:** `tests/test_command_preprocessor.py`
- **Commit:** ddc12f5

## Test Results

- 24 tests written and passing (all green)
- Test file: `tests/test_command_preprocessor.py`
- Runner: `evennia test tests.test_command_preprocessor` → `Ran 24 tests in 0.005s OK`
- Covers: resolve_prefix (5 tests), expand_alias (9 tests), preprocess_input (10 tests)

## Known Stubs

None — all functionality is fully wired.

## Self-Check: PASSED
