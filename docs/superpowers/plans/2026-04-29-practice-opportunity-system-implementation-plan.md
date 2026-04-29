# Practice Opportunity System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a builder-safe practice opportunity system that awards hidden skill and domain progression from meaningful in-world actions while keeping Remnance non-player-facing in current-era content.

**Architecture:** Add one runtime engine, one action-vocabulary action, one `AreaBuilder` DSL method, one quest objective checker, and one Remnance visibility helper. Do not add area-authoring abstractions that the builder cannot round-trip.

**Tech Stack:** Python, Evennia commands, Django test runner through `scripts/run_tests.py`, Soravelon `AreaBuilder` DSL.

---

## File Map

- `world/practice_engine.py`: validates and resolves builder-authored practice payloads.
- `world/remnance_visibility.py`: centralizes current-era Remnance and Vaelborn visibility rules.
- `world/action_vocabulary.py`: dispatches `grant_practice`.
- `commands/cmd_dynamic.py`: passes raw player command args into action context.
- `world/area_builder.py`: adds literal `area.practice_opportunity(...)`.
- `world/quest_engine.py`: adds `practice` objective progress.
- `world/zone_serializer.py`: loads serialized `practice_opportunities`.
- `commands/cmd_quest.py`: previews practice rewards without XP numbers.
- `commands/cmd_help.py`, `commands/cmd_domains.py`, `commands/cmd_guild.py`, `commands/cmd_status.py`, `commands/cmd_abilities.py`, `commands/cmd_loadout.py`, `world/session_lifecycle.py`, `world/world_state.py`: hide current-era Remnance from player-facing command surfaces.
- `world/help_entries.py`, `world/areas/vaels_crossing.py`, `world/areas/reth_foothills.py`, `world/areas/stormhaven_coast.py`, `world/lore_registry.py`: remove or lock public Remnance references.
- `tests/test_practice_engine.py`: behavior coverage for practice resolution.
- `tests/test_dynamic_commands.py`: command argument passthrough coverage.
- `tests/test_remnance_visibility.py`: current-era Remnance blackout coverage.
- Existing focused test files: action vocabulary, quest engine, area builder, quest command, help, guild, session lifecycle.

## Completed Task Record

### Task 1: Practice Runtime

- [x] **Step 1: Write failing runtime tests**

Tests covered skill/domain accumulation, target matching, once-per-character behavior, quest objective notification, and Remnance rejection.

- [x] **Step 2: Verify red**

`python scripts/run_tests.py tests.test_practice_engine`

Expected failure was missing `world.practice_engine`.

- [x] **Step 3: Implement runtime**

Created `world/practice_engine.py` with `validate_practice_payload` and `resolve_practice_opportunity`.

- [x] **Step 4: Verify green**

`python scripts/run_tests.py tests.test_practice_engine`

Result: 4 tests passed.

### Task 2: Shared Action And Dynamic Args

- [x] **Step 1: Write failing action/command tests**

Tests covered a new `grant_practice` action and raw dynamic command args in action context.

- [x] **Step 2: Verify red**

`python scripts/run_tests.py tests.test_action_vocabulary` and
`python scripts/run_tests.py tests.test_dynamic_commands`

Expected failures were missing `grant_practice` and missing `context["args"]`.

- [x] **Step 3: Implement dispatcher and context passthrough**

Added `_handle_grant_practice` and passed `self.args` from dynamic commands.

- [x] **Step 4: Verify green**

`python scripts/run_tests.py tests.test_action_vocabulary tests.test_dynamic_commands`

Result: tests passed in the later combined focused run.

### Task 3: Builder DSL And Serialized Area Support

- [x] **Step 1: Write failing builder tests**

Tests covered `area.practice_opportunity(...)`, room metadata, generated dynamic command, and hidden-domain rejection.

- [x] **Step 2: Verify red**

`python scripts/run_tests.py tests.test_area_builder.TestPracticeOpportunity`

Expected failure was missing `AreaBuilder.practice_opportunity`.

- [x] **Step 3: Implement literal DSL**

Added a strict builder-safe method that stores `room.db.practice_opportunities` and compiles to a dynamic command.

- [x] **Step 4: Verify green**

`python scripts/run_tests.py tests.test_area_builder.TestPracticeOpportunity`

Result: 2 tests passed.

### Task 4: Quest Objective Integration

- [x] **Step 1: Write failing quest tests**

Tests covered `practice` objectives incrementing only for matching opportunity IDs and capping at required count.

- [x] **Step 2: Verify red**

`python scripts/run_tests.py tests.test_quest_engine`

Expected failure was missing `check_practice_objectives`.

- [x] **Step 3: Implement objective checker**

Added `check_practice_objectives(character, opportunity_id)` to `world/quest_engine.py`.

- [x] **Step 4: Verify green**

`python scripts/run_tests.py tests.test_quest_engine`

Result: 66 tests passed in the prior focused run.

### Task 5: Player-Facing Quest Reward Text

- [x] **Step 1: Write failing quest-command test**

Test covered `grant_practice` rewards rendering as meaningful practice instead of XP.

- [x] **Step 2: Implement reward preview**

Added `grant_practice` formatting in `commands/cmd_quest.py`.

- [x] **Step 3: Verify green**

`python scripts/run_tests.py tests.test_cmd_quest`

Result: included in the 152-test focused run.

### Task 6: Current-Era Remnance Blackout

- [x] **Step 1: Write failing visibility tests**

Tests covered public help, dynamic ability help, `domains`, `joinguild`, login guidance, automatic guild discovery, and area/lore string constants.

- [x] **Step 2: Verify red**

`python scripts/run_tests.py tests.test_remnance_visibility`

Expected failures named public help leaks, command leaks, area/lore leaks, and the hidden guild messenger.

- [x] **Step 3: Implement central visibility helper**

Added `world/remnance_visibility.py` and routed command/help surfaces through it.

- [x] **Step 4: Remove public prose leaks**

Rewrote current-era area/lore/help prose so public content no longer names Remnance or Vaelborn. Kept internal future-event data intact.

- [x] **Step 5: Verify green**

`python scripts/run_tests.py tests.test_remnance_visibility`

Result: 7 tests passed.

## Validation Checklist

- [x] `python scripts/run_tests.py tests.test_practice_engine tests.test_action_vocabulary tests.test_quest_engine tests.test_cmd_quest tests.test_dynamic_commands tests.test_remnance_visibility tests.test_help_entries tests.test_help_command tests.test_cmd_guild tests.test_session_lifecycle`
- [ ] `python scripts/run_tests.py tests.test_area_builder.TestPracticeOpportunity`
- [ ] `python -m py_compile` on touched runtime modules
- [ ] `python scripts/smoke_start.py`
- [ ] Engram closeout memory
- [ ] Scoped git commit

## Notes For Future Work

- Builder UI/parser support is documented separately in `docs/superpowers/plans/2026-04-29-sora-builder-practice-opportunities-handoff.md`.
- Remnance should remain internal until a deliberate world-event unlock sets a future visibility flag. Do not reintroduce the old `remnance_discovered` flag as player-facing authority.
