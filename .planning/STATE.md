---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: Ready to plan
stopped_at: Completed 16-02-PLAN.md
last_updated: "2026-03-26T22:33:50.301Z"
progress:
  total_phases: 10
  completed_phases: 6
  total_plans: 33
  completed_plans: 31
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-24)

**Core value:** Character identity must feel mechanically distinct — 90 subclasses play differently, not just look different
**Current focus:** Phase 16 — architectural-refactoring

## Current Position

Phase: 16-architectural-refactoring
Plan: 02 of 5 (complete)

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
| Phase 03.1 P02 | 5 | 2 tasks | 6 files |
| Phase 03.1 P01 | 18 | 1 tasks | 2 files |
| Phase 03.1 P03 | 10 | 2 tasks | 4 files |
| Phase 03.1 P04 | 3 | 1 tasks | 2 files |
| Phase 03.1 P05 | 10 | 2 tasks | 1 files |
| Phase 04 P01 | 10 | 3 tasks | 4 files |
| Phase 04 P02 | 28 | 2 tasks | 2 files |
| Phase 05 P02 | 4 | 2 tasks | 4 files |
| Phase 05 P04 | 4 | 2 tasks | 6 files |
| Phase 05 P03 | 4 | 2 tasks | 2 files |
| Phase 05 P05 | 9 | 2 tasks | 3 files |
| Phase 06a P02 | 2 | 1 tasks | 1 files |
| Phase 06a P01 | 5 | 2 tasks | 2 files |
| Phase 06a P04 | 123 | 1 tasks | 1 files |
| Phase 06a P05 | 5 | 2 tasks | 1 files |
| Phase 06a P06 | 6 | 2 tasks | 5 files |

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
- [Phase 03.1]: Item typeclass selected via string map; unknown item_type defaults to SoravelonItem
- [Phase 03.1]: named_mob() delegates to spawn() with is_named=True, count_min=1, count_max=1 — named mobs merged into unified spawn_definitions schema (D-13/D-14)
- [Phase 03.1]: Named mobs merged into spawn_definitions (no separate registry) — mob_id tag enables search_tag reload detection
- [Phase 03.1]: _schedule_respawn called from at_death only (not initial spawn) — keeps mob_spawner as pure creation engine
- [Phase 03.1]: spawn_zone called inline after each zone build (both .py and .zone.json branches) using tag search for zone_obj
- [Phase 03.1]: Action-spawned mobs use respawn_minutes=0 — event-driven, not area-managed; only at_death triggers respawn for area-defined mobs
- [Phase 03.1]: tome_drop initialized in at_object_creation to avoid getattr trap on db attributes (project convention)
- [Phase 03.1]: Exposed get_zone_obj_for_room and get_material_tier as module-level wrappers in loot_tables.py — avoids lazy-import patching trap in tests
- [Phase 03.1]: area_builder tests require evennia test --settings settings runner (not plain pytest) due to EvenniaTest session requirement
- [Phase 04]: Runewright subclass_id collision: 'runewright' for Arcane guild, 'runewright_forge' for Forge guild
- [Phase 04]: Vaelborn tier 1 label is empty string, not None or placeholder
- [Phase 04]: CharacterGuild migration numbered 0004 (after existing 0003_worldeventlog)
- [Phase 04]: Used EvenniaTest for model mutation tests and unittest.TestCase+MagicMock for pure computation tests
- [Phase 04]: Included missing 0003_worldeventlog migration to fix dependency chain for EvenniaTest DB setup
- [Phase 05]: 14 stub abilities cover all 10 domains and 10 effect types; bladestorm chosen as signature stub subclass
- [Phase 05]: Ironwright hook updated to no-companion weapons-mid-battle design per D-27
- [Phase 05]: CmdJoinGuild uses full syntax (not interactive yield) for simplicity
- [Phase 05]: Guild discovery sends RP-flavored message instead of system notification
- [Phase 05]: CmdUseAbility uses progressive word matching then prefix search with disambiguation
- [Phase 05]: Effect handlers are stubs returning descriptive text; Phase 6 wires real combat effects
- [Phase 05]: Domain resource initialized at login (not just encounter start) for utility/social abilities
- [Phase 05]: FINGERPRINTS has no resource_max; initialize_domain_resource defaults to 100
- [Phase 05]: Patch lazy imports at source module (world.world_state, world.models) not at consumer module
- [Phase 06a]: Compound duration defaults to 3 rounds; petrify gets +2 from extended_duration spec
- [Phase 06a]: Immunity checked via both ndb.immunities (volatile) and db.immunities (persistent mob config)
- [Phase 06a]: Point-buy: 7x10 base + 20 bonus = 90 total, min 5 max 25 per stat
- [Phase 06a]: HP formula: 50 + endurance*5 + backend_level*10; Stamina: 30 + endurance*2
- [Phase 06a]: Action budget: floor(1 + agility/30) capped at 4; damage modifier 1/sqrt(actions)
- [Phase 06a]: Stat growth: 0.5 XP per use, 10 XP = 1 stat point, diminishing returns curve
- [Phase 06a]: Mob AI uses lambda dict for condition vocabulary (9 checks); weight-based random.choices for ability selection; fire-once trigger set for scripted sequences
- [Phase 06a]: CombatScript uses dynamic type() subclassing to avoid Evennia import-time typeclass resolution
- [Phase 06a]: Timer cancellation uses deferred.cancel() from Evennia delay() return value
- [Phase 06a]: CombatCmdSet import moved from cmd_abilities to combat_commands (cleaner separation)
- [Phase 06a]: push_combat_update accepts optional data arg for backward compat with CombatScript direct calls
- [Phase 06a]: Auto-engage joins all aggressive mobs into same combat encounter (not separate)

### Pending Todos

None yet.

### Blockers/Concerns

- Phase 5 risk: 90 subclass ability authoring is a creative design task (not pure engineering) — fingerprint document from Phase 4 is the only guard rail; budget extra time
- Phase 6 risk: Evennia contrib cooldowns persistence across disconnects is unverified — confirm during Phase 6 planning before combat is designed around it
- Phase 2 risk: Full Evennia OOB outputfunc catalog is MEDIUM-confidence — verify against webclient.py source before locking the typed protocol in Phase 2

## Session Continuity

Last session: 2026-03-26T19:24:34.441Z
Stopped at: Completed 06a-06-PLAN.md
Resume file: None
