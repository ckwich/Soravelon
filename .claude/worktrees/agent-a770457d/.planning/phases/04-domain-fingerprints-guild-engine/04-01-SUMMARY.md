---
phase: 04-domain-fingerprints-guild-engine
plan: 01
subsystem: game-engine
tags: [guilds, subclasses, fingerprints, gts, domain-progression, django-model]

# Dependency graph
requires:
  - phase: 03.1-mob-spawn-runtime
    provides: "world/models.py base with existing Django models"
provides:
  - "FINGERPRINTS constant registry (10 domain mechanical identities)"
  - "GUILDS constant registry (10 guild definitions)"
  - "SUBCLASSES constant registry (90 subclass definitions)"
  - "GTS computation engine (calculate_guild_tier_score, get_guild_tier, get_guild_tier_label)"
  - "Guild eligibility check (check_guild_eligibility at threshold 30)"
  - "CharacterGuild Django model with migration"
  - "DOMAIN_FINGERPRINTS.md consolidated design document"
affects: [05-ability-authoring, guild-commands, combat-system, phase-5]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Python constant registries for static game data (GUILDS, SUBCLASSES, FINGERPRINTS)"
    - "On-the-fly GTS computation (never cached/stored)"
    - "Module-level lookup indexes built at import (_DOMAIN_TO_GUILD, _DOMAIN_PAIR_TO_SUBCLASS)"
    - "Module-level validation assertions at import time"

key-files:
  created:
    - "world/guild_engine.py"
    - "world/migrations/0004_characterguild.py"
    - ".planning/phases/04-domain-fingerprints-guild-engine/DOMAIN_FINGERPRINTS.md"
  modified:
    - "world/models.py"

key-decisions:
  - "Runewright name collision: used 'runewright' for Arcane+Engineering (arcane guild) and 'runewright_forge' for Engineering+Resonance (forge guild) to avoid duplicate subclass_id keys"
  - "Vaelborn tier 1 label is empty string (not None or placeholder text)"
  - "Migration numbered 0004 to sequence after existing 0003_worldeventlog"

patterns-established:
  - "guild_engine.py as authoritative constant registry for all guild/subclass/fingerprint data"
  - "GTS always computed fresh from character.db.domain_scores -- never stored"
  - "CharacterGuild OneToOneField enforces single guild record per character at DB level"

requirements-completed: [DOM-01, DOM-02, DOM-03, DOM-04, DOM-05]

# Metrics
duration: 10min
completed: 2026-03-25
---

# Phase 04 Plan 01: Domain Fingerprints and Guild Engine Summary

**10 domain fingerprints, 10 guilds, 90 subclasses as Python constant registries with GTS computation engine and CharacterGuild Django model**

## Performance

- **Duration:** 10 min
- **Started:** 2026-03-26T00:52:06Z
- **Completed:** 2026-03-26T01:02:37Z
- **Tasks:** 3
- **Files modified:** 4

## Accomplishments
- Consolidated vault creative content into DOMAIN_FINGERPRINTS.md design document (10 fingerprints, 10 guilds, 90 subclasses, tier labels, GTS formula, proficiency descriptors)
- Created world/guild_engine.py with 1628 lines: constant registries, lookup indexes, GTS computation, guild eligibility, proficiency labels, and import-time validation assertions
- Added CharacterGuild Django model with OneToOneField to ObjectDB and migration 0004

## Task Commits

Each task was committed atomically:

1. **Task 1: Consolidate vault sources into DOMAIN_FINGERPRINTS.md** - `a312554` (docs)
2. **Task 2 + Task 3: guild_engine.py + CharacterGuild model + migration** - `f34a641` (feat)

Note: Tasks 2 and 3 were combined into a single commit due to git worktree corruption preventing separate commits for the worktree branch. All deliverables are present.

## Files Created/Modified
- `.planning/phases/04-domain-fingerprints-guild-engine/DOMAIN_FINGERPRINTS.md` - Consolidated design document from vault sources
- `world/guild_engine.py` - Constant registries (GUILDS, SUBCLASSES, FINGERPRINTS, GUILD_TIER_LABELS, DOMAIN_PROFICIENCY_LABELS) + GTS computation functions + guild eligibility check
- `world/models.py` - Added CharacterGuild model (OneToOneField to ObjectDB)
- `world/migrations/0004_characterguild.py` - Django migration creating CharacterGuild table

## Decisions Made
- Runewright subclass name collision between Arcane guild (arcana+engineering) and Forge guild (engineering+resonance): used `runewright` as subclass_id for Arcane guild version and `runewright_forge` for Forge guild version. Both have display name "Runewright" but distinct IDs.
- Vaelborn tier 1 label stored as empty string `""` per research recommendation. Display logic handles the hidden state.
- Migration numbered 0004 (not 0003) because 0003_worldeventlog already exists from prior phase work.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Runewright subclass_id collision**
- **Found during:** Task 2 (guild_engine.py creation)
- **Issue:** Both Arcane+Engineering and Engineering+Resonance subclasses are named "Runewright" in the vault, causing duplicate key in SUBCLASSES dict
- **Fix:** Used `runewright` for Arcane guild version and `runewright_forge` for Forge guild version
- **Files modified:** world/guild_engine.py, DOMAIN_FINGERPRINTS.md
- **Verification:** len(SUBCLASSES) == 90, all domain pair lookups resolve correctly
- **Committed in:** f34a641

**2. [Rule 3 - Blocking] Migration number collision with 0003_worldeventlog**
- **Found during:** Task 3 (migration generation)
- **Issue:** 0003_worldeventlog.py already exists from prior phase; creating 0003_characterguild.py would collide
- **Fix:** Numbered migration as 0004 with dependency on 0003_worldeventlog
- **Files modified:** world/migrations/0004_characterguild.py
- **Verification:** Migration file exists with correct dependency chain
- **Committed in:** f34a641

**3. [Rule 3 - Blocking] Git worktree corruption preventing separate commits**
- **Found during:** Task 3 (committing)
- **Issue:** Worktree had corrupted .claude-plugin objects preventing any new commits
- **Fix:** Committed Tasks 2 and 3 together from main repo instead of worktree
- **Impact:** Tasks 2 and 3 share a single commit instead of separate atomic commits

---

**Total deviations:** 3 auto-fixed (3 blocking)
**Impact on plan:** All auto-fixes necessary for correct operation. No scope creep. Combined commit is a cosmetic deviation only.

## Issues Encountered
- Git worktree had corrupted objects in .claude-plugin/ directory preventing all commits. Resolved by committing from main repo.

## User Setup Required
None - no external service configuration required.

## Known Stubs
None - all data is fully populated. 90 subclasses, 10 guilds, 10 fingerprints all have complete entries.

## Next Phase Readiness
- guild_engine.py provides all constant registries and computation functions needed for Phase 5 ability authoring
- CharacterGuild model ready for join_guild() wiring in Phase 5
- DOMAIN_FINGERPRINTS.md serves as design reference for downstream ability work
- GTS computation verified at threshold boundaries (0, 20, 50, 85, 99)

## Self-Check: PASSED

All files verified present:
- DOMAIN_FINGERPRINTS.md: FOUND
- world/guild_engine.py: FOUND
- world/models.py: FOUND
- world/migrations/0004_characterguild.py: FOUND
- 04-01-SUMMARY.md: FOUND
- Commit a312554: FOUND
- Commit f34a641: FOUND

---
*Phase: 04-domain-fingerprints-guild-engine*
*Completed: 2026-03-25*
