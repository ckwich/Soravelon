---
phase: 06b-spawn-system-skills-and-mob-ai
plan: 02
subsystem: skills
tags: [proficiency, diminishing-returns, accumulator, practice, trainer, discovery]

requires:
  - phase: 04-domain-fingerprints-guild-engine
    provides: CharacterSkill model in world/models.py
provides:
  - SKILL_DEFINITIONS registry (21 general proficiency skills)
  - ANCESTRY_SKILL_SEEDS for 5 ancestry variants
  - Skill engine with passive accumulation, deliberate practice, trainer sessions
  - Discovery trigger framework for lore reveals on skill combos
affects: [06b-03, 06c-npc-dialogue-and-crafting, content-authoring]

tech-stack:
  added: []
  patterns: [ndb-accumulator-batch-commit, rolling-24hr-per-skill-cooldown, tier-based-diminishing-returns]

key-files:
  created:
    - world/skill_definitions.py
    - world/skill_engine.py
  modified: []

key-decisions:
  - "Skill system fully independent of domain/guild system (SKL-04)"
  - "Trainer bonus stored as ndb volatile — consumed on next practice, lost on disconnect (intentional friction)"
  - "Discovery check only on threshold crossings (25/50/75/90/100) to avoid per-use DB queries"

patterns-established:
  - "Skill accumulator pattern: ndb counter per skill_id, batch-commit at threshold via commit_skill_accumulators"
  - "Rolling cooldown pattern: per-record last_practiced_at with timedelta check, not global reset"

requirements-completed: [SKL-01, SKL-02, SKL-03, SKL-04]

duration: 3min
completed: 2026-03-26
---

# Phase 06b Plan 02: Skill Definitions and Engine Summary

**21 general proficiency skills with three improvement methods (passive use, deliberate practice, trainer sessions) and discovery trigger framework**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-26T23:33:43Z
- **Completed:** 2026-03-26T23:37:05Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- SKILL_DEFINITIONS registry with 21 entries covering all D-16 skills, each with domain_bonus, thresholds, and trainer gates
- ANCESTRY_SKILL_SEEDS for 5 ancestry variants (human, kauroran, veth, selvar_north, selvar_south) with SELVAR_COAT_TO_LINEAGE mapping
- Skill engine with all three improvement methods: passive ndb accumulation (10 uses = +0.1), deliberate practice (24hr rolling cooldown, tier-based gains), trainer sessions (NPC framework, Scales cost, enhances next practice)
- Discovery trigger framework that checks skill combos on threshold crossings

## Task Commits

Each task was committed atomically:

1. **Task 1: Skill definitions registry** - `75558a5` (feat)
2. **Task 2: Skill engine** - `5230359` (feat)

## Files Created/Modified
- `world/skill_definitions.py` - Pure-data registry: 21 skills, ancestry seeds, diminishing brackets, practice gains, trainer registry, discovery triggers
- `world/skill_engine.py` - Engine: accumulate_skill_use, commit_skill_accumulators, practice_skill, train_with_trainer, apply_ancestry_skill_seeds, check_discoveries

## Decisions Made
- Skill system fully independent of domain/guild system (SKL-04) — no imports from guild_engine or ability_engine
- Trainer bonus stored on ndb (volatile) — consumed on next practice, lost on disconnect; intentional friction to reward planning
- Discovery check fires only on threshold crossings (25/50/75/90/100) to avoid per-use DB queries for condition evaluation
- SELVAR_COAT_TO_LINEAGE mapping keeps coat-to-lineage logic in data layer, not engine logic

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Worktree sparse-checkout corruption prevented committing skill_engine.py from worktree; committed from main repo instead. Both commits are accessible.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Skill definitions and engine ready for integration with combat system (passive skill use accumulation)
- Trainer registry empty — populated during content phase when NPCs are authored
- Discovery triggers framework ready for content-phase lore entries

## Self-Check: PASSED

- [x] world/skill_definitions.py exists (92f8d06)
- [x] world/skill_engine.py exists (5230359)
- [x] Commit 75558a5 found (worktree, definitions)
- [x] Commit 92f8d06 found (main, definitions)
- [x] Commit 5230359 found (main, engine)
- [x] Commit 574240a found (docs)

---
*Phase: 06b-spawn-system-skills-and-mob-ai*
*Completed: 2026-03-26*
