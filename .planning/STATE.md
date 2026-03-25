---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: Ready to execute
stopped_at: Completed 03-03-PLAN.md
last_updated: "2026-03-25T19:43:17.228Z"
progress:
  total_phases: 7
  completed_phases: 2
  total_plans: 14
  completed_plans: 11
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-24)

**Core value:** Character identity must feel mechanically distinct — 90 subclasses play differently, not just look different
**Current focus:** Phase 03 — gui-area-builder

## Current Position

Phase: 03 (gui-area-builder) — EXECUTING
Plan: 2 of 4

## Performance Metrics

**Velocity:**

- Total plans completed: 0
- Average duration: -
- Total execution time: 0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| - | - | - | - |

**Recent Trend:**

- Last 5 plans: none yet
- Trend: -

*Updated after each plan completion*
| Phase 01 P03 | 7 | 2 tasks | 5 files |
| Phase 01 P02 | 7 | 2 tasks | 5 files |
| Phase 01 P01 | 25 | 2 tasks | 4 files |
| Phase 01 P04 | 3 | 3 tasks | 4 files |
| Phase 01 P05 | 5 | 2 tasks | 7 files |
| Phase 02 P01 | 2 | 2 tasks | 2 files |
| Phase 02 P02 | 35 | 2 tasks | 2 files |
| Phase 02 P03 | 15 | 2 tasks | 3 files |
| Phase 02 P04 | 25 | 2 tasks | 2 files |
| Phase 03 P03 | 8 | 2 tasks | 2 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Roadmap: Phase 4 (fingerprints) gates Phase 5 (abilities) — no ability can be authored before all 10 domain mechanical verbs are locked in a design document
- Roadmap: Phase 3 (GUI builder) gates Phase 7 (content) — all zone content authored through builder, not hand-coded
- Roadmap: Phase 2 (OOB publisher) gates Phase 3 (desktop client) — typed envelope protocol defined before any client event handler is written
- Research: Use single CmdUseAbility dispatcher for all 360+ abilities; never per-ability Cmd classes
- Research: Two-pass area loading fix (BLD-06) must ship in Phase 3 before any cross-zone content is authored
- [Phase 01]: Used commands.command.Command (local base) instead of evennia.Command — lazy init prevents static class definition before server start
- [Phase 01]: Used unittest.TestCase for preprocessor tests (not EvenniaTest) — pure-logic modules with MagicMock need no Evennia DB setup
- [Phase 01]: get_mob_behavior imported at patrol_engine module level (not lazy) to enable test patching
- [Phase 01]: trigger_engine calls in mobs.py/rooms.py guarded by if self.db.triggers — safe no-op until plan 01-01 delivers the module
- [Phase 01]: Used unittest.TestCase for trigger_engine tests (pure-logic MagicMock modules need no Evennia DB setup)
- [Phase 01]: fire_triggers returns None (void) — errors logged not raised; non-character guard via account attribute check
- [Phase 01]: Added mob() method to AreaBuilder — required for _mobs dict that patrol() uses to look up mob objects in build() finalization
- [Phase 01]: Used evennia.commands.cmdset.CmdSet directly in cmd_dynamic.py — evennia.CmdSet returns None before full Evennia init
- [Phase 01]: sys.modules injection for flight tests — world.world_state imports Django at module level; inject stubs before import to keep pure unittest.TestCase approach
- [Phase 01]: D-08 NPC booking gate deferred — discovery alone unlocks Dragon Courier booking for Phase 01; NPC gate wires in during content phase
- [Phase 02]: Used get_character_context_packet keys (reputation/network/bond/legacy/attunement) directly — not *_score suffixed keys
- [Phase 02]: push_inventory_update items list is an intentional stub — full item query deferred to Phase 6 per plan spec
- [Phase 02]: BFS collision nudge shifts east (nx += 1) for up/down/in/out exits that map to (0,0) offset — deterministic, simple
- [Phase 02]: auto_layout_zone is a module-level function (not a method) in area_builder.py; called at build() step 3.5 after _finalize_patrols
- [Phase 02]: Intermediate stop uses leg index (current-1) after counter increment — leg was already advanced before disembark OOB push
- [Phase 02]: Final landing push_flight_progress uses leg_index=total_legs (sentinel) to signal completion to client
- [Phase 02]: Used unittest.TestCase + django.setup() (not EvenniaTest) for test_oob_publisher — all characters are MagicMock so no DB objects needed; EvenniaTest.setUp hits SQLite under lock from running server
- [Phase 03]: Task 2 (_load_all_zones .zone.json branch) was pre-implemented in 03-02 — verified correct and skipped re-implementation
- [Phase 03]: load_zone_from_json uses rooms_lookup dict (not DB search) for local exit/spawn/npc resolution — mirrors AreaBuilder's _rooms pattern, no extra DB queries

### Pending Todos

None yet.

### Blockers/Concerns

- Phase 5 risk: 90 subclass ability authoring is a creative design task (not pure engineering) — fingerprint document from Phase 4 is the only guard rail; budget extra time
- Phase 6 risk: Evennia contrib cooldowns persistence across disconnects is unverified — confirm during Phase 6 planning before combat is designed around it
- Phase 2 risk: Full Evennia OOB outputfunc catalog is MEDIUM-confidence — verify against webclient.py source before locking the typed protocol in Phase 2

## Session Continuity

Last session: 2026-03-25T19:43:17.226Z
Stopped at: Completed 03-03-PLAN.md
Resume file: None
