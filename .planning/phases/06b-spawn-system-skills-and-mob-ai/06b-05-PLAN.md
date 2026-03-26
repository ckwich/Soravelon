---
phase: 06b-spawn-system-skills-and-mob-ai
plan: 05
type: execute
wave: 3
depends_on: ["06b-01", "06b-02", "06b-03", "06b-04"]
files_modified:
  - tests/test_spawn_record.py
  - tests/test_skill_engine.py
  - tests/test_combat_ai.py
autonomous: true
requirements: [SKL-01, SKL-02, SKL-03, SKL-04, CMB-04]

must_haves:
  truths:
    - "SpawnRecord lifecycle tested: creation, spawn_tick processing, death hook scheduling"
    - "Skill engine tested: passive accumulation, practice cooldown, diminishing returns, ancestry seeds"
    - "Combat AI casting time tested: cast start, resolution, interrupt"
    - "All requirement behaviors have automated test coverage"
  artifacts:
    - path: "tests/test_spawn_record.py"
      provides: "SpawnRecord model tests, spawn_tick tests, death hook tests"
      min_lines: 80
    - path: "tests/test_skill_engine.py"
      provides: "Skill progression tests, practice tests, ancestry seed tests, discovery tests"
      min_lines: 120
    - path: "tests/test_combat_ai.py"
      provides: "Extended with casting time, new conditions, is_hunter tests"
  key_links:
    - from: "tests/test_spawn_record.py"
      to: "world/mob_spawner.py"
      via: "Tests spawn_tick, schedule_respawn_from_death, initialize_spawn_records"
      pattern: "spawn_tick|schedule_respawn_from_death"
    - from: "tests/test_skill_engine.py"
      to: "world/skill_engine.py"
      via: "Tests accumulate, practice, train, discovery"
      pattern: "practice_skill|commit_skill_accumulators"
---

<objective>
Comprehensive test suite for all Phase 6b subsystems: SpawnRecord lifecycle, skill engine, and combat AI extensions.

Purpose: Automated verification that all requirements (CMB-04, SKL-01 through SKL-04) have test coverage. Tests catch regressions in spawn timing, skill progression math, practice cooldowns, and casting time interrupts.

Output: test_spawn_record.py (new), test_skill_engine.py (new), test_combat_ai.py (extended).
</objective>

<execution_context>
@C:\Users\colek\.claude\get-shit-done\workflows\execute-plan.md
@C:\Users\colek\.claude\get-shit-done\templates\summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/06b-spawn-system-skills-and-mob-ai/06b-01-SUMMARY.md
@.planning/phases/06b-spawn-system-skills-and-mob-ai/06b-02-SUMMARY.md
@.planning/phases/06b-spawn-system-skills-and-mob-ai/06b-03-SUMMARY.md
@.planning/phases/06b-spawn-system-skills-and-mob-ai/06b-04-SUMMARY.md

@world/mob_spawner.py
@world/skill_engine.py
@world/skill_definitions.py
@world/combat_ai.py
@tests/test_combat_ai.py
</context>

<tasks>

<task type="auto">
  <name>Task 1: SpawnRecord and skill engine tests</name>
  <files>tests/test_spawn_record.py, tests/test_skill_engine.py</files>
  <action>
**tests/test_spawn_record.py** -- Use unittest.TestCase with MagicMock (same pattern as Phase 03.1 tests per project decisions). Mock Evennia DB objects and Django ORM where needed.

Test cases:
- **TestSpawnRecordModel**: SpawnRecord creation with room_id, spawn_index, mob_template, active_mob_ids. Verify unique_together constraint (room_id + spawn_index).
- **TestScheduleRespawnFromDeath**: Mock mob with db.spawn_record_id. Call schedule_respawn_from_death(). Verify: mob.id removed from active_mob_ids (reassigned, not mutated in place). When all mobs dead, respawn_at is set to future time. When some mobs remain, respawn_at stays None.
- **TestSpawnTick**: Mock SpawnRecord queryset with due records. Call spawn_tick(). Verify: rooms resolved, spawn_def read, mob created, record.active_mob_ids updated, record.respawn_at set to None. Condition not met: verify record.respawn_at rescheduled to +5 minutes.
- **TestInitializeSpawnRecords**: Mock rooms with spawn_definitions. Call initialize_spawn_records(). Verify: SpawnRecord.objects.get_or_create called per definition. New records get respawn_at=now. Existing records preserved (idempotent).
- **TestNamedMobDeath**: Mock named mob death. Verify WorldEventLog.objects.create called with event_type="named_mob_death" and correct data dict.

**tests/test_skill_engine.py** -- Use unittest.TestCase with MagicMock.

Test cases covering all requirements:
- **TestGetSkillValue**: Returns 0.0 for unlearned skill. Returns correct value for learned skill.
- **TestAccumulateSkillUse** (SKL-01): accumulate_skill_use increments ndb counter. Does NOT write to DB.
- **TestCommitSkillAccumulators** (SKL-01): After 10+ uses, passive gain applied to CharacterSkill record. Gain multiplied by diminishing rate. Remainder preserved in ndb.
- **TestDiminishingReturns** (SKL-01): Verify _get_diminishing_rate returns 1.0 for 0-25, 0.75 for 26-50, 0.40 for 51-75, 0.10 for 76-90, 0.02 for 91-100.
- **TestPracticeSkill** (SKL-01): practice_skill returns (True, message) with value increase. Second immediate call returns (False, cooldown message). Call 24+ hours later succeeds.
- **TestPracticeGainsByTier**: Verify gain ranges match PRACTICE_GAINS table for each tier.
- **TestProfessionSkills** (SKL-02): Verify cooking, smithing, alchemy, engineering all present in SKILL_DEFINITIONS with skill_type="general".
- **TestAnimalHandling** (SKL-03): animal_handling skill exists, value range 0-100, at 100 a threshold check can confirm Dragon Handling eligibility.
- **TestSkillDomainIndependence** (SKL-04): Verify CharacterSkill has no FK to CharacterGuild. Skill operations don't require guild membership.
- **TestAncestrySkillSeeds**: apply_ancestry_skill_seeds for each ancestry creates correct CharacterSkill records with vault-spec seed values. Human creates none. Selvar winter -> North seeds, summer -> South seeds.
- **TestDiscoveryFramework**: Mock character with skills at discovery thresholds. Call check_discoveries. Verify discovery added to character.db.discoveries and message sent.
- **TestTrainWithTrainer**: Mock trainer in TRAINER_REGISTRY. Verify cost deducted, bonus applied to ndb.

Use `from unittest.mock import MagicMock, patch` for all DB and Evennia mocks. Patch at the module that imports (e.g., `world.skill_engine.CharacterSkill`) per Phase 05 decision.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -m pytest tests/test_spawn_record.py tests/test_skill_engine.py -x -v 2>&1 | tail -20</automated>
  </verify>
  <done>test_spawn_record.py covers SpawnRecord lifecycle (creation, spawn_tick, death hook, initialize, named mob WorldEventLog). test_skill_engine.py covers all SKL requirements: passive accumulation, practice cooldown, diminishing returns, profession skills, animal handling, domain independence, ancestry seeds, discovery framework.</done>
</task>

<task type="auto">
  <name>Task 2: Combat AI extension tests</name>
  <files>tests/test_combat_ai.py</files>
  <action>
Extend the existing tests/test_combat_ai.py (from Phase 6a) with new test cases. Read the existing file first to understand the test patterns and mocking approach already in use.

Add test cases:
- **TestNewConditions**: Verify target_rooted, target_blinded, no_target_dot, pack_present, hp_below_50, hp_below_25 all exist in CONDITION_CHECKS and return correct bool values.
  - target_rooted: True when target has "root" effect, False otherwise
  - target_blinded: True when target has "blind" effect, False otherwise
  - no_target_dot: True when target has no poison/bleed/burn, False when any present
  - pack_present: True when other mobs alive in combat, False when alone

- **TestCastingTimeStart**: Mock mob with ability that has cast_time=2. Call select_mob_action(). Verify returns dict with type="cast_start", cast_time=2, emote text.

- **TestStartMobCast**: Call start_mob_cast() with mock mob, ability, target, combat_handler. Verify combat_handler.ndb.pending_mob_casts has entry for mob.id with correct rounds_left.

- **TestResolvePendingCasts**: Create pending cast with rounds_left=1. Call resolve_pending_casts(). Verify: returns ability action dict. pending_mob_casts cleared for that mob. Verify rounds_left=2 decrements to 1, stays pending.

- **TestCastInterrupt**: Create pending cast with rounds_left=1 on a mob that has "stun" effect. Call resolve_pending_casts(). Verify: cast cancelled (not in resolved actions). Room gets interrupt message.

- **TestHunterChase**: Mock is_hunter mob with detection_range=3. Mock find_path returning a 2-room path. Call attempt_hunter_chase(). Verify mob.move_to called with next room. Verify False returned when target out of range (find_path returns empty).

Follow existing test file patterns for mocking (MagicMock for mob, target, combat_handler). Patch `world.combat_ai.has_effect` and `world.combat_ai.find_path` for clean isolation.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -m pytest tests/test_combat_ai.py -x -v 2>&1 | tail -20</automated>
  </verify>
  <done>test_combat_ai.py extended with tests for all 6 new condition keys, casting time start/resolve/interrupt, and is_hunter chase behavior. All tests pass alongside existing Phase 6a tests.</done>
</task>

</tasks>

<verification>
- `python -m pytest tests/test_spawn_record.py tests/test_skill_engine.py tests/test_combat_ai.py -x -v` all pass
- Every requirement ID has at least one test: CMB-04 (spawn creates combat-ready mobs), SKL-01 (passive + practice), SKL-02 (profession skills exist), SKL-03 (animal_handling to 100), SKL-04 (no guild FK)
</verification>

<success_criteria>
All three test files pass. SpawnRecord lifecycle is covered (creation, tick, death, initialize). Skill engine is covered (accumulation, practice, diminishing returns, seeds, discovery). Combat AI casting time is covered (start, resolve, interrupt). Hunter chase is covered. No test touches real DB -- all use MagicMock.
</success_criteria>

<output>
After completion, create `.planning/phases/06b-spawn-system-skills-and-mob-ai/06b-05-SUMMARY.md`
</output>
