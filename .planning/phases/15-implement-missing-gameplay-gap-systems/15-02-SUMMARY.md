---
phase: 15-implement-missing-gameplay-gap-systems
plan: 02
subsystem: recovery-engine
tags: [recovery, regen, rest, sleep, medic, blessings]
dependency_graph:
  requires: [base_attributes, oob_publisher, status_effects, combat_engine]
  provides: [recovery_engine, cmd_recovery, medic_npc_interaction]
  affects: [characters, vaels_crossing, default_cmdsets]
tech_stack:
  added: []
  patterns: [ndb_volatile_state, delayed_tick_scheduling, lazy_import]
key_files:
  created:
    - world/recovery_engine.py
    - commands/cmd_recovery.py
    - tests/test_recovery_engine.py
  modified:
    - world/status_effects.py
    - typeclasses/characters.py
    - commands/default_cmdsets.py
    - world/areas/vaels_crossing.py
decisions:
  - "Recovery state stored on ndb (volatile) -- clears on disconnect, consistent with combat state pattern"
  - "Bed detection checks room contents for db.is_bed attribute (no room_state flag needed)"
  - "Fortify/vigor added as non-stackable effects in status_effects.py for medic blessing buffs"
  - "Push stat update wrapper in recovery_engine for testability via module-level mock"
metrics:
  duration_seconds: 3487
  completed: "2026-04-05T07:44:40Z"
  tasks_completed: 2
  tasks_total: 2
  files_created: 3
  files_modified: 4
---

# Phase 15 Plan 02: HP/Stamina Recovery System Summary

**One-liner:** Four-tier regen system (1%/3%/6%/10% per 10s) with rest/sleep commands, sleep blindness, bed bonus, combat awareness, and medic NPC blessings for Scales.

## Task Results

### Task 1: Recovery engine with regen ticks and blessings (TDD)

**Commit:** 354c46e

Created `world/recovery_engine.py` with:
- `REGEN_RATES` dict: active (1%), resting (3%), sleeping (6%), sleeping_bed (10%)
- `BLESSINGS` dict: heal (20 Scales), fortify (30), vigor (30), purify (40) with cooldowns
- `_regen_tick()`: combat-aware tick that calculates HP/stamina gains, pushes OOB updates
- `start_regen()` / `stop_regen()`: tick lifecycle management
- `set_recovery_state()`: state transitions with combat blocking
- `cancel_recovery()`: return to active state
- `apply_blessing()`: cost checking, cooldown enforcement, effect application

Added "fortify" (15% damage reduction) and "vigor" (15% damage bonus) to `status_effects.py` NON_STACKABLE_EFFECTS and wired them into `get_effect_modifiers()`.

17 unit tests covering all regen tiers, combat skip, state management, blessings, cooldowns, and insufficient Scales.

### Task 2: Recovery commands + character wiring + medic NPC

**Commit:** 6e9f63c

Created `commands/cmd_recovery.py` with:
- `CmdRest` (rest/sit): sets resting state
- `CmdSleep` (sleep): sets sleeping state
- `CmdWake` (wake/stand): cancels recovery
- `CmdBlessing` (blessing/bless): medic NPC interaction with listing and application

Character wiring in `typeclasses/characters.py`:
- `at_post_puppet`: calls `start_regen()` on login
- `at_pre_unpuppet`: calls `stop_regen()` on disconnect
- `at_after_move`: calls `cancel_recovery()` if not in active state
- `at_look` override: returns blindness message when sleeping

Medic NPC: set `db.is_medic = True` on surgeon Adela in Vaels Crossing Imperial Medic Station.

Commands registered in `default_cmdsets.py`.

## Deviations from Plan

None -- plan executed exactly as written.

## Known Stubs

None -- all functionality is fully wired end-to-end.

## Self-Check: PASSED
