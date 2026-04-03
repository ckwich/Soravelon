---
phase: 12-launch-polish-help
plan: 01
subsystem: onboarding
tags: [connection-screen, starter-kits, ancestry, new-player-guidance, ansi]

# Dependency graph
requires:
  - phase: 05-ancestry-engine-and-ability-system
    provides: ancestry_engine.py, set_ancestry(), ANCESTRY_TRAITS
  - phase: 03.1-mob-spawn-runtime
    provides: item_spawner.py, create_item_from_template()
provides:
  - Dark fantasy connection screen with Soravelon branding
  - Ancestry-based starter kits (weapons, armor, potions, currency)
  - New player guidance prompts (ancestry, guild, quest hints)
affects: [12-02, 12-03, future-content]

# Tech tracking
tech-stack:
  added: []
  patterns: [starter-kit-inline-defs, guidance-method-pattern]

key-files:
  modified:
    - server/conf/connection_screens.py
    - world/ancestry_engine.py
    - typeclasses/characters.py

key-decisions:
  - "All starter items defined inline in ancestry_engine.py (no equipment_catalog dependency)"
  - "Guidance gated by backend_level > 1 or 2+ domain_scores as experience heuristic"
  - "Starter kit grants 50 Scales currency via character.db.carried_scales"

patterns-established:
  - "_grant_starter_kit pattern: ancestry engine creates items via item_spawner after standings"
  - "_send_new_player_guidance pattern: private method on Character called at end of at_post_puppet"

requirements-completed: [D-01, D-02, D-09, D-10, D-11]

# Metrics
duration: 3min
completed: 2026-03-31
---

# Phase 12 Plan 01: Connection Screen and New Player Onboarding Summary

**Dark fantasy connection screen, 4 ancestry-specific starter kits with weapons/armor/potions, and tiered new player guidance prompts**

## Performance

- **Duration:** 3 min
- **Started:** 2026-04-03T22:33:53Z
- **Completed:** 2026-04-03T22:37:11Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Replaced default Evennia connection screen with atmospheric dark fantasy text featuring Soravelon branding and lore excerpt
- Added STARTER_KITS dict with ancestry-specific gear: Human (sword/leather), Kau'roran (spear/hide), Veth (2x dagger/leather/lockpick), Selvar (staff/robes) plus healing potions and 50 Scales for all
- Wired _grant_starter_kit into set_ancestry() to create items via item_spawner on ancestry choice
- Added _send_new_player_guidance() with 3-tier hints: ancestry prompt, guild exploration hint, NPC conversation hint

## Task Commits

Each task was committed atomically:

1. **Task 1: Connection screen + starter kit in set_ancestry** - `30ed9f7` (feat)
2. **Task 2: New player guidance prompts in at_post_puppet** - `35f8a54` (feat)

## Files Created/Modified
- `server/conf/connection_screens.py` - Dark fantasy connection screen with Soravelon lore and ANSI colors
- `world/ancestry_engine.py` - STARTER_KITS dict (4 ancestries), _grant_starter_kit() function, inline item defs
- `typeclasses/characters.py` - _send_new_player_guidance() method with ancestry/guild/quest checks

## Decisions Made
- All starter items defined inline in ancestry_engine.py rather than depending on equipment_catalog (which does not exist) -- avoids runtime dependency on zone loading
- Experience heuristic uses backend_level > 1 OR 2+ domain_scores to suppress guidance for returning players
- Starter kit grants 50 Scales via direct db.carried_scales assignment (consistent with at_object_creation init)
- Items created with error handling per-item so one failure does not block entire kit

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Equipment catalog does not exist**
- **Found during:** Task 1
- **Issue:** Plan referenced world/areas/equipment_catalog.py and search_tag lookup for zone_obj, but this file does not exist in the codebase
- **Fix:** Defined all starter items inline in ancestry_engine.py as template dicts, removed equipment_catalog dependency entirely
- **Files modified:** world/ancestry_engine.py
- **Committed in:** 30ed9f7

**2. [Rule 3 - Blocking] apply_ancestry_skill_seeds does not exist**
- **Found during:** Task 1
- **Issue:** Plan mentioned adding starter kit after apply_ancestry_skill_seeds call, but this function does not exist
- **Fix:** Added _grant_starter_kit call after _apply_starting_standings (the last existing call in set_ancestry)
- **Files modified:** world/ancestry_engine.py
- **Committed in:** 30ed9f7

---

**Total deviations:** 2 auto-fixed (2 blocking)
**Impact on plan:** Both fixes necessary because referenced code did not exist. Inline definitions are simpler and avoid runtime zone-loading dependency.

## Issues Encountered
- Git worktree had corrupted index with missing blobs from GSD plugin sparse checkout. Fixed by resetting index via git read-tree HEAD before committing Task 2.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Connection screen ready for players
- Starter kits will create items when ancestry is chosen
- Guidance prompts active on login for new characters
- Plans 12-02 and 12-03 (help system and lore journal) already merged into main

## Self-Check: PASSED

All 3 files found. All 2 commits verified.

---
*Phase: 12-launch-polish-help*
*Completed: 2026-03-31*
