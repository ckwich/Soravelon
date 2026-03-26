---
phase: 06b-spawn-system-skills-and-mob-ai
plan: 01
subsystem: spawn-system
tags: [django-orm, ticker, spawn-record, mob-respawn, worldeventlog]

# Dependency graph
requires:
  - phase: 03.1-mob-spawn-runtime
    provides: mob_spawner.py spawn functions, SoravelonMob typeclass, spawn_definitions DSL
provides:
  - SpawnRecord Django model for persistent mob spawn state
  - WorldEventLog class body (was missing from models.py)
  - spawn_tick() global 60s ticker for crash-safe respawns
  - initialize_spawn_records() idempotent server-start wiring
  - schedule_respawn_from_death() replacing callLater
  - Named mob death WorldEventLog entries
  - Named mob zone-wide respawn announcements
affects: [06b-03-mob-ability-ai, 06b-04-casting-time-hunter-chase, content-zones]

# Tech tracking
tech-stack:
  added: []
  patterns: [SpawnRecord DB-backed respawn replaces Twisted callLater]

key-files:
  created: [world/migrations/0006_spawnrecord.py]
  modified: [world/models.py, world/mob_spawner.py, typeclasses/mobs.py, server/conf/at_server_startstop.py]

key-decisions:
  - "SpawnRecord uses mob.db.spawn_record_id for direct FK lookup on death (avoids JSONField __contains query)"
  - "Named mob respawn detection via WorldEventLog query (not flag on SpawnRecord)"
  - "Zone-wide respawn announcement uses vague text per vault spec"

patterns-established:
  - "SpawnRecord-backed ticker: DB query for due records, spawn, update, save -- crash-safe respawn pattern"

requirements-completed: [CMB-04]

# Metrics
duration: 7min
completed: 2026-03-26
---

# Phase 06b Plan 01: Spawn Record System Summary

**SpawnRecord Django model + 60s global ticker replacing Twisted callLater for crash-safe mob respawns with named mob death logging**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-26T23:33:47Z
- **Completed:** 2026-03-26T23:40:30Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- SpawnRecord model tracks live state per spawn slot (room_id, spawn_index, active_mob_ids, respawn_at)
- Global 60s ticker (spawn_tick) processes due SpawnRecords -- survives server restarts
- Death hook rewritten to use SpawnRecord instead of callLater -- no more lost respawns on crash
- Named mob deaths write WorldEventLog entries for respawn announcement tracking
- WorldEventLog class body added to models.py (was missing despite migration 0003 existing)

## Task Commits

Each task was committed atomically:

1. **Task 1: WorldEventLog fix + SpawnRecord model + migration** - `d0753ba` (feat)
2. **Task 2: Spawn ticker + death hook rewrite + server start wiring** - `fbb4e53` (feat)

## Files Created/Modified
- `world/models.py` - Added WorldEventLog class body + SpawnRecord model
- `world/migrations/0006_spawnrecord.py` - Migration for SpawnRecord table
- `world/mob_spawner.py` - Added spawn_tick(), initialize_spawn_records(), schedule_respawn_from_death(); removed _schedule_respawn() and _get_reactor()
- `typeclasses/mobs.py` - Rewritten at_death() to use SpawnRecord path + WorldEventLog for named mobs; added spawn_record_id db attribute
- `server/conf/at_server_startstop.py` - Added spawn_tick ticker (5th TICKER_HANDLER) + initialize_spawn_records() call after _load_all_zones()

## Decisions Made
- SpawnRecord uses mob.db.spawn_record_id for direct FK lookup on death -- avoids JSONField __contains query that fails on SQLite (D-06)
- Named mob respawn detection queries WorldEventLog for prior "named_mob_death" entries rather than storing a flag on SpawnRecord
- Zone-wide respawn announcement uses vague text ("Something stirs in the distance.") per vault spec
- _is_respawn() for normal mobs always returns False (only named mobs get respawn announcements)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Worktree had corrupted git objects (invalid .gitattributes reference) -- switched to committing directly in main repo

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- SpawnRecord system is foundation for all future mob population management
- spawn_tick processes respawns every 60s -- content zones will automatically use this system
- Named mob death tracking feeds into future quest system and respawn announcements

## Self-Check: PASSED

- All 5 files found on disk
- Both commits (d0753ba, fbb4e53) verified in git log
- All 13 functions present in mob_spawner.py
- No _schedule_respawn references in mobs.py
- 5 TICKER_HANDLER.add calls in at_server_startstop.py

---
*Phase: 06b-spawn-system-skills-and-mob-ai*
*Completed: 2026-03-26*
