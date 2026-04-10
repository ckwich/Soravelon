---
phase: 05-ancestry-engine-and-ability-system
plan: 05
subsystem: test-suite
tags: [testing, ancestry, abilities, room-state, tdd]
dependency_graph:
  requires: [05-01, 05-02, 05-03, 05-04]
  provides: [phase-5a-test-coverage]
  affects: []
tech_stack:
  added: []
  patterns: [unittest-mock-pure-logic, patch-at-import-target]
key_files:
  created:
    - tests/test_ancestry_engine.py
    - tests/test_ability_engine.py
    - tests/test_room_state.py
  modified: []
decisions:
  - "Patched modify_standing at world.world_state (lazy import target) not world.ancestry_engine"
  - "Patched CharacterAbility at world.models (lazy import in _check_ability_access)"
  - "Used SimpleNamespace for db/ndb mock attributes for clean attribute assignment"
metrics:
  duration_minutes: 9
  completed: "2026-03-26T06:09:00Z"
---

# Phase 05 Plan 05: Test Suite for Ancestry, Ability, and Room State Summary

**49 tests across 3 files covering all Phase 5a systems: ancestry engine (15), ability engine (22), room state (12)**

## What Was Built

### tests/test_ancestry_engine.py (15 tests)
- **TestHumanAncestry**: sets ancestry, applies Empire +10k standing
- **TestKauroranAncestry**: 3 faction standings (kauroran +20k, wardens +10k, empire -15k)
- **TestVethAncestry**: Consortium +7500 standing
- **TestSelvarAncestry**: coat required, summer/winter coat, -5k penalty to 4 factions + guild offset
- **TestAncestryRejection**: rejects duplicate ancestry, rejects unknown ancestry
- **TestGetAncestryTrait**: returns trait value, returns default when no ancestry, returns default for missing trait

### tests/test_ability_engine.py (22 tests)
- **TestAbilityRegistryStructure**: 16 required fields, 10+ domains, subclass signatures, all effect types covered, get_ability, tier thresholds
- **TestUseAbilityDispatch**: damage dispatch, unknown ability rejection, unlock gating
- **TestCooldowns**: blocks when on cooldown, sets cooldown after use, decrement removes expired, clear_encounter resets all
- **TestResourceManagement**: spend success/insufficient, build capped at max, initialize from guild, no-guild returns None, get_domain_resource, build with no resource
- **TestAbilityTierGating**: CharacterAbility record required for access

### tests/test_room_state.py (12 tests)
- **TestGetRoomFlags**: empty when no state, returns flags when current, lazy decay (3 rounds), expired flags removed, persistent flag no decay
- **TestAddRoomFlag**: add new flag, refresh takes max duration, refresh keeps existing if longer, unknown flag logs warning
- **TestRemoveRoomFlag**: removes existing flag
- **TestGetDominantFlag**: priority order (void_touched > blood_soaked), still when no flags, None when recent activity
- **TestFlagVocabularyCompleteness**: 21 flags, SENSE_PRIORITY covers all

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Patch target for modify_standing**
- **Found during:** Task 1
- **Issue:** Plan suggested `@patch("world.ancestry_engine.modify_standing")` but modify_standing is a lazy import inside `_apply_starting_standings`, not a module-level attribute
- **Fix:** Patched at `world.world_state.modify_standing` (the actual source module)
- **Files modified:** tests/test_ancestry_engine.py
- **Commit:** 9c434e9

**2. [Rule 1 - Bug] Patch target for CharacterAbility**
- **Found during:** Task 2
- **Issue:** Plan suggested `@patch("world.ability_engine.CharacterAbility")` but CharacterAbility is lazily imported inside `_check_ability_access`
- **Fix:** Patched at `world.models.CharacterAbility` (the actual source module)
- **Files modified:** tests/test_ability_engine.py
- **Commit:** e76cc0f

**3. [Rule 3 - Blocking] Git worktree index corruption**
- **Found during:** Task 2 commit
- **Issue:** Worktree index contained corrupted entries from another repo's object store (`.claude-plugin/marketplace.json`, `.gitattributes`, etc.)
- **Fix:** Rebuilt index from HEAD via `git read-tree`, staged new file via `git hash-object` + `git update-index`
- **Commit:** e76cc0f

## Decisions Made

1. Used `world.world_state.modify_standing` as patch target (not `world.ancestry_engine.modify_standing`) because the import is lazy inside `_apply_starting_standings`
2. Used `world.models.CharacterAbility` as patch target (not `world.ability_engine.CharacterAbility`) because the import is lazy inside `_check_ability_access`
3. Used `SimpleNamespace` for db/ndb mock attributes instead of `MagicMock()` -- cleaner attribute assignment without PropertyMock

## Known Stubs

None -- these are test files, no stubs.

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| 1 | 9c434e9 | test(05-05): add ancestry engine and room state test suites |
| 2 | e76cc0f | test(05-05): add ability engine and registry test suite |
