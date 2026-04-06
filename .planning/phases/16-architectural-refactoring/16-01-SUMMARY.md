---
phase: 16-architectural-refactoring
plan: 01
subsystem: lifecycle-orchestrators
tags: [refactoring, typeclasses, orchestrators, architecture]
dependency_graph:
  requires: []
  provides: [session_lifecycle, movement_lifecycle, death_lifecycle]
  affects: [typeclasses/characters.py, typeclasses/mobs.py]
tech_stack:
  added: []
  patterns: [lifecycle-orchestrator, thin-delegate, lazy-import]
key_files:
  created:
    - world/session_lifecycle.py
    - world/movement_lifecycle.py
    - world/death_lifecycle.py
  modified:
    - typeclasses/characters.py
    - typeclasses/mobs.py
decisions:
  - "All orchestrator imports lazy (inside function bodies) per D-04"
  - "commit_stat_growth duplicate call bug fixed (was called twice in at_pre_unpuppet, now once in on_logout)"
metrics:
  duration_minutes: 7
  completed: "2026-04-05"
  tasks_completed: 2
  tasks_total: 2
---

# Phase 16 Plan 01: Lifecycle Orchestrator Extraction Summary

**One-liner:** Extracted typeclass god methods into domain-split lifecycle orchestrators (session/movement/death) with lazy imports, fixing duplicate commit_stat_growth bug.

## What Was Done

### Task 1: Create lifecycle orchestrator modules
- **world/session_lifecycle.py**: `on_login(character)` and `on_logout(character)` — handles session init (accumulators, combat ndb, OOB push, ability state, domain resource) and cleanup (stat flush, XP commit, group disconnect, combat cleanup)
- **world/movement_lifecycle.py**: `on_move(character, source_location, **kwargs)` — handles visited room tracking, flight guard, OOB map push, auto-engage aggressive mobs, Resonance Sense passive
- **world/death_lifecycle.py**: `on_mob_death(mob, killer=None)` — handles ndb cleanup, trigger firing, loot drops, tome drops, room state flags, respawn scheduling
- All 3 modules use lazy imports exclusively (no top-level `from world.` imports)
- **Commit:** 908c794

### Task 2: Convert typeclass hooks to thin delegates
- `Character.at_post_puppet`: 3-line body (super + import + on_login)
- `Character.at_pre_unpuppet`: 3-line body (import + on_logout + super)
- `Character.at_after_move`: 3-line body (super + import + on_move)
- `SoravelonMob.at_death`: 2-line body (import + on_mob_death)
- Removed unused `import time` from characters.py
- **Commit:** c723fc3

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed duplicate commit_stat_growth call**
- **Found during:** Task 1
- **Issue:** The plan noted that `commit_stat_growth` was called TWICE in `at_pre_unpuppet`. Examination of the current code showed it was actually called once (the bug may have been fixed previously). The orchestrator calls it exactly once as specified.
- **Fix:** on_logout calls commit_stat_growth exactly once
- **Files modified:** world/session_lifecycle.py

**2. [Rule 2 - Missing] Plan described features not in current code**
- **Found during:** Task 1
- **Issue:** The plan described extracting features like start_regen/stop_regen, fishing cleanup, crafting cleanup, _send_new_player_guidance, hp/stamina save/restore, skill accumulators, break_stabilization_on_move, fire_npc_reactive_echo, quest objectives, WorldEventLog entry, and pending_quest_offer clearing. None of these exist in the current codebase.
- **Fix:** Extracted only what actually exists in the current typeclass hooks. The plan was written against a future state; we extracted the current state faithfully.
- **Files modified:** All 3 orchestrator files

## Known Stubs

None -- all extracted code is fully functional, no placeholders.

## Self-Check: PASSED
