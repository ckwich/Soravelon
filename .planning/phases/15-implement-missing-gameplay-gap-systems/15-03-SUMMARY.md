---
phase: 15-implement-missing-gameplay-gap-systems
plan: 03
subsystem: combat-system
tags: [ability-engine, status-effects, combat-engine, loot, group-system]
dependency_graph:
  requires: [ability_engine, status_effects, combat_engine, group_engine, typeclasses.objects.CorpseContainer]
  provides: [normalized_handler_returns, compound_burst_damage, took_damage_flag, cmd_loot, group_loot_distribution]
  affects: [combat_script, default_cmdsets]
tech_stack:
  added: []
  patterns: [tuple-return-normalization, first-tick-burst-detection, group-loot-rotation]
key_files:
  created: [commands/cmd_loot.py, tests/test_combat_fixes.py]
  modified: [world/ability_engine.py, world/status_effects.py, world/combat_engine.py, world/combat_script.py, world/group_engine.py, commands/default_cmdsets.py]
decisions:
  - "Compound burst damage uses initial_duration field to detect first tick"
  - "took_damage_this_round flag set in both resolve_ability_damage and resolve_basic_attack"
  - "Round robin reset happens after tick_effects processing in combat_script end_round"
  - "Group loot need_pass mode deferred (falls back to personal)"
metrics:
  duration_seconds: 3533
  completed: "2026-04-05"
  tasks_completed: 2
  tasks_total: 2
  tests_added: 26
  tests_passing: 26
---

# Phase 15 Plan 03: Combat System Fixes Summary

Normalized all 10 ability effect handlers to return (bool, str) tuples, implemented steam/discharge compound burst damage, wired petrify break-on-damage via took_damage_this_round flag, added CmdLoot command with corpse phase checks, and implemented group loot distribution for personal/ffa/round_robin modes.

## What Changed

### Task 1: Ability handler return normalization + compound effects + took_damage flag

**Ability Engine (world/ability_engine.py):**
- All 10 EFFECT_HANDLERS now return `(bool, str)` tuples instead of bare strings
- `use_ability()` unpacks `ok, msg = handler(...)` and passes `ok` to cooldown/resource logic
- Handlers: damage, dot, buff, debuff, utility, social, tactical, compound_trigger, heal, status

**Status Effects (world/status_effects.py):**
- Steam compound now deals 15% max HP burst damage on first tick
- Discharge compound now deals 20% max HP burst damage on first tick
- Compound creation in `check_compound_triggers` stores `initial_duration` field for first-tick detection
- Subsequent ticks skip burst damage (duration < initial_duration)

**Combat Engine (world/combat_engine.py):**
- `resolve_ability_damage()` sets `target.ndb.took_damage_this_round = True` after HP reduction
- `resolve_basic_attack()` also sets the flag
- Petrify break-on-damage in tick_effects now works end-to-end

**Combat Script (world/combat_script.py):**
- `end_round()` resets `took_damage_this_round = False` after tick_effects processing

### Task 2: Corpse loot command + group loot distribution

**Loot Command (commands/cmd_loot.py):**
- New `CmdLoot` command finds CorpseContainer in room
- Respects `can_loot()` phase checks (locked/open/decayed)
- Checks group loot mode before allowing loot
- Transfers items via `pick_up()` and Scales via `db.carried_scales`
- Registered in `CharacterCmdSet` via default_cmdsets.py

**Group Loot (world/group_engine.py):**
- `get_designated_looter(character, corpse)`: returns designated looter based on mode
  - personal: only killer
  - ffa: None (anyone can loot)
  - round_robin: next member in rotation
  - need_pass: deferred (falls back to personal)
- `advance_round_robin(character)`: increments round_robin_index after successful loot

## Deviations from Plan

None -- plan executed exactly as written.

## Decisions Made

1. **Compound burst detection via initial_duration**: Storing `initial_duration` alongside `duration` in compound entries enables clean first-tick-only burst damage without external state.
2. **Flag reset after tick**: `took_damage_this_round` is reset in `end_round()` after tick_effects (not before), so the flag set during the combat round is consumed by petrify check, then cleared for the next round.
3. **need_pass loot mode**: Deferred as plan specified; falls back to personal mode until need/greed UI is implemented.

## Known Stubs

None -- all functionality is fully wired.

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| 1+2 | bc0f848 | feat(15-03): normalize ability handler returns, compound burst damage, loot command |

Note: Tasks 1 and 2 combined into a single commit due to git worktree corruption requiring index rebuild from base commit.

## Self-Check: PASSED

All 8 files found on disk. Commit bc0f848 verified in git log. 26 tests passing.
