# Repository Health Check Report — Soravelon MUD
**Date:** 2026-03-27
**Auditor:** Claude Opus 4.6 (automated deep audit)
**Scope:** Full codebase audit of `C:\Dev\Evennia\soravelon`

---

## 1. Executive Summary

**Overall Health: GOOD with one critical blocker and several medium-priority issues.**

Soravelon is a well-structured, disciplined Evennia 6.0 MUD codebase with ~33K lines of code (15K engine, 2.5K commands, 1.1K typeclasses, 14K tests). The architecture is clean — thin typeclasses delegate to stateless world/ engine modules, Django models handle relational data, and ndb handles volatile session state. Established patterns are followed consistently across most of the codebase.

**Top Risks:**
1. **CRITICAL:** Two Django model classes (WorldEventLog, SpawnRecord) have migrations but no class bodies in models.py — the server will crash on any code path that imports these models
2. **HIGH:** 18 instances of the `getattr(obj.db, ...)` anti-pattern that contradicts Evennia's AttributeHandler behavior and the project's own documented conventions
3. **MEDIUM:** Many direct `character.msg()` calls in combat_script.py bypass the OOB publisher, creating inconsistency for future client integration

**Top Strengths:**
- Extremely consistent architectural patterns across 40+ world/ modules
- Strong test coverage (35 test files, ~14K lines) — test/code ratio near 1:1
- Clean separation of concerns: typeclasses → world engines → Django models
- All 6 TickerHandler registrations verified correct
- All 25+ command classes verified correctly registered
- CombatCmdSet dynamic add/remove is properly wired through CombatScript

**Production Readiness:** Not yet — the missing model classes are a hard blocker. After fixing that critical issue plus the getattr patterns, the systems layer is architecturally sound for Phase 7 content authoring.

**Coherence:** The repo is coherent, not fragmented. All systems were built in dependency order (phases 1-6c) and share consistent patterns. The rapid build pace (7 phases in 3 days) means some rough edges exist but the architectural skeleton is solid.

---

## 2. System Map

### Major Subsystems (by layer)

**Layer 1: Typeclasses** (1,126 lines)
- `characters.py` — Character with 30+ db attributes, 10+ ndb slots, stat/combat/skill integration
- `mobs.py` — SoravelonMob with affix system, disposition, spawn record, death handling
- `objects.py` — SoravelonItem, Container, Equipment, KeyringItem, CorpseContainer
- `rooms.py` — SoravelonRoom with dual-layer node support
- `exits.py` — SoravelonExit with locked/hidden exit support
- `scripts.py` — SoravelonScript base

**Layer 2: World Engines** (14,846 lines across 30+ modules)
- **Core Progression:** world_state.py, base_attributes.py, guild_engine.py, ancestry_engine.py
- **Combat:** combat_engine.py, combat_script.py, combat_ai.py, ability_engine.py, ability_registry.py, status_effects.py
- **Skills:** skill_engine.py, skill_definitions.py
- **NPC/Dialogue:** dialogue_engine.py, dialogue_definitions.py, crafting_engine.py, crafting_definitions.py
- **Economy:** banking.py, inventory_engine.py, loot_tables.py
- **World Sim:** mob_spawner.py, mob_affix_roller.py, mob_affixes.py, mob_disposition.py, zone_scaling.py, room_state.py, node_helpers.py
- **Infrastructure:** area_builder.py, oob_publisher.py, flight_engine.py, patrol_engine.py, trigger_engine.py, action_vocabulary.py, group_engine.py

**Layer 3: Commands** (2,497 lines)
- 11 command modules with 25+ command classes
- CombatCmdSet dynamically added/removed during combat
- default_cmdsets.py as central registration point

**Layer 4: Server Configuration** (872 lines)
- 6 ticker registrations in at_server_startstop.py
- Zone loading and spawn initialization on startup

**Layer 5: Django Models** (369 lines, 13 models)
- FactionStanding, ZoneAttunement, CharacterSkill, NodeEventLog
- InventoryItem, BankAccount, BankTransaction, RecurringPayment, DebtRecord
- CharacterGuild, CharacterAbility, KnownTopicRecord, CharacterRecipe
- **MISSING:** WorldEventLog, SpawnRecord (migrations exist, class bodies do not)

### Interaction Flow
```
Player Input → Evennia CmdHandler → commands/*.py
  → world/*.py engine functions (stateless)
    → world/models.py (Django ORM, relational data)
    → typeclasses/*.py (db/ndb attribute mutations)
    → world/oob_publisher.py (client push)

Server Tickers (6 registered):
  → world_state_decay_tick (86400s)
  → session_xp_safety_flush (600s) → also flushes skill accumulators
  → node_failure_tick (30s)
  → banking_payment_tick (86400s)
  → spawn_tick (60s)
  → ambient_npc_tick (15s)

Combat Flow:
  Player enters room → auto-engage check → CombatScript created on room
  → CombatCmdSet added to players → turn loop (initiative-ordered)
  → mob AI via combat_ai.py → damage via combat_engine.py
  → status effects via status_effects.py → death → corpse + respawn scheduling
```

---

## 3. Critical Findings

### FINDING-01: Missing Django Model Classes
- **Severity:** Critical
- **Confidence:** Confirmed
- **Area:** Data layer
- **Files:** `world/models.py`, `world/migrations/0003_worldeventlog.py`, `world/migrations/0006_spawnrecord.py`
- **Explanation:** WorldEventLog and SpawnRecord have Django migrations that create their database tables, but the Python class definitions are completely absent from `world/models.py`. The file ends at line 369 with CharacterRecipe. Any import of `from world.models import WorldEventLog` or `from world.models import SpawnRecord` will raise `ImportError`.
- **Why it matters:**
  - `world/mob_spawner.py` imports SpawnRecord on 6 lines (302, 313, 338, 341, 449, 456)
  - `world/mob_spawner.py` imports WorldEventLog on 2 lines (409, 415)
  - `world/world_state.py` imports and creates WorldEventLog on lines 382-390
  - `tests/test_spawn_record.py` will fail on import
  - The spawn_tick() registered in at_server_startstop will crash on first invocation
  - Any mob death will crash when at_death() calls schedule_respawn_from_death()
- **Fix:** Add both class bodies to `world/models.py`. WorldEventLog fields can be derived from migration 0003. SpawnRecord fields from migration 0006. This is a ~40-line addition.

### FINDING-02: getattr(obj.db, ...) Anti-Pattern (18 instances)
- **Severity:** High
- **Confidence:** Confirmed
- **Area:** Cross-cutting (7 modules)
- **Files:** `world/banking.py`, `world/combat_ai.py`, `world/combat_script.py`, `world/inventory_engine.py`, `world/mob_affix_roller.py`, `world/mob_disposition.py`, `world/node_helpers.py`, `world/world_state.py`, `typeclasses/exits.py`
- **Explanation:** Evennia's `AttributeHandler.__getattr__` intercepts attribute access on `obj.db` and returns `None` for missing attributes — Python's `getattr()` default parameter is never reached because `AttributeError` is never raised. Code like `getattr(character.db, 'carried_scales', 0)` will return `None` (not `0`) if the attribute doesn't exist, leading to silent `TypeError` when used in arithmetic.
- **Why it matters:** Banking balance calculations (`getattr(character.db, 'carried_scales', 0)`) will silently get `None` instead of `0` for characters without the attribute, causing `TypeError: unsupported operand type(s)` in arithmetic operations. This is the project's own documented trap (CLAUDE.md rule).
- **Fix:** Replace all 18 instances with `obj.db.attr or fallback` pattern. Most are simple: `character.db.carried_scales or 0`.

### FINDING-03: Parallel Migration Numbering
- **Severity:** Medium
- **Confidence:** Confirmed
- **Area:** Data layer
- **Files:** `world/migrations/0006_knowntopicrecord_characterrecipe.py`, `world/migrations/0006_spawnrecord.py`, `world/migrations/0007_merge_20260326_2012.py`
- **Explanation:** Two migration files share number 0006 (created by parallel worktree agents). A merge migration 0007 exists to reconcile them. This is valid Django behavior but indicates the parallel execution model sometimes creates migration conflicts.
- **Why it matters:** Future migrations must be created on the main branch after merge, not in parallel worktrees. The merge migration is functional but adds noise.
- **Fix:** No action needed — the merge migration handles it. Document the pattern for future awareness.

---

## 4. Integration / Wiring Audit

### Correctly Wired (Verified)

| Connection | Status |
|------------|--------|
| 6 TickerHandler registrations in at_server_startstop.py | All callbacks exist and match expected signatures |
| 25+ commands in CharacterCmdSet | All imported classes exist, all files verified |
| CombatCmdSet dynamic add/remove via CombatScript | Properly wired through _add_combat_cmdset/_remove_combat_cmdset |
| ability_engine.py → combat_engine.py + status_effects.py | 10 effect handlers use lazy imports to real resolution functions |
| combat_script.py → combat_engine.py + combat_ai.py + status_effects.py | 20+ lazy import points verified |
| ancestry_engine.py → skill_engine.py (seed wiring) | set_ancestry() calls apply_ancestry_skill_seeds() at line 121 |
| world_state.py → skill_engine.py (flush wiring) | session_xp_safety_flush() calls commit_skill_accumulators() at line 416-417 |
| area_builder.py → zone_registry.py | register_zone() called in build() |
| mobs.py at_death() → mob_spawner.py | schedule_respawn_from_death() called (line 206) |
| mobs.py at_death() → room_state.py | add_room_flag() for blood_soaked/fading_life/power_vacuum |
| mobs.py at_death() → WorldEventLog | Named mob death logging (line 180-187) |
| dialogue action_vocabulary handler → dialogue_engine.py | open_dialogue wired to resolve_greeting/resolve_topic_response |
| Characters auto-engage → combat_script.start_combat() | at_after_move() checks aggressive mobs (line 189-206) |

### Disconnected or Partially Connected

| Issue | Status |
|-------|--------|
| WorldEventLog model class missing from models.py | **BROKEN** — all imports will fail |
| SpawnRecord model class missing from models.py | **BROKEN** — spawn_tick and at_death will crash |
| named_mob_registry.py exists but is never imported | **ORPHANED** — file exists as untracked, never used |
| world/prototypes.py exists but is never imported | **ORPHANED** — superseded by AreaBuilder pattern |
| world/help_entries.py exists but is never imported | **ORPHANED** — empty or unused |
| combat_script.py direct msg() calls (17 instances) bypass oob_publisher | **PARTIAL** — works but inconsistent with OOB architecture |
| oob_publisher.py has combat_update as a stub type | **PARTIAL** — push_combat_update exists but may not match combat_script's output format |

---

## 5. Dead Code / Drift Audit

### Orphaned Files
| File | Status | Action |
|------|--------|--------|
| `world/named_mob_registry.py` | Untracked, never imported anywhere | Delete or integrate |
| `world/prototypes.py` | Never imported — superseded by area_builder.py mob templates | Delete |
| `world/help_entries.py` | Never imported | Delete or implement |
| `world/apps.py` | Standard Django app config — not orphaned, just auto-generated | Keep |

### Documentation Drift
| Area | Issue |
|------|-------|
| CLAUDE.md says "16 files" in tests/ | Actually 35 test files now |
| CLAUDE.md lists "11 Django models" | Actually 13 models defined (plus 2 missing) |
| Base skill says "16 files" test suite | Stale — should say 35 |
| Several skills reference old line numbers | Line numbers shift as files grow — inherent drift |

### Intentional Stubs (Not Dead Code)
These are explicitly documented for future phases and are NOT issues:
- `mob_spawner.py` quest_complete/time_of_day condition stubs
- `action_vocabulary.py` set_quest_flag stub handler
- `dialogue_engine.py` quest state checking stubs
- `oob_publisher.py` quest_update placeholder
- `loot_tables.py` rarity modifier stub values

---

## 6. Refactor Opportunities

### Priority 1: Fix Missing Models (Immediate, Low Risk)
- **Impact:** Unblocks the entire spawn and event logging system
- **Risk:** Very low — just adding class bodies matching existing migrations
- **LOE:** 30 minutes

### Priority 2: Replace getattr(obj.db, ...) Pattern (Immediate, Low Risk)
- **Impact:** Prevents silent None-instead-of-default bugs in banking, combat, inventory
- **Risk:** Very low — mechanical replacement, each instance is independent
- **LOE:** 1 hour across 7 files, 18 instances

### Priority 3: Consolidate OOB Combat Messages (Medium-term, Medium Risk)
- **Impact:** Ensures combat state is consistently pushed to desktop client
- **Risk:** Medium — requires understanding what the client expects
- **Payoff:** When the proprietary client is built (Milestone 2+), combat data will already flow through the correct channel
- **LOE:** 2-3 hours to route combat_script.py messages through push_combat_update

### Priority 4: Clean Up Orphaned Files (Low Priority, Low Risk)
- **Impact:** Reduces confusion for new contributors
- **Risk:** Very low
- **LOE:** 15 minutes

### Priority 5: Update CLAUDE.md Metrics (Low Priority, Low Risk)
- **Impact:** Prevents stale documentation misleading agents
- **LOE:** 15 minutes

---

## 7. Testing Gaps

### Missing Test Files
| Module | Test File | Priority |
|--------|-----------|----------|
| `world/dialogue_engine.py` | `tests/test_dialogue_engine.py` | LOW — covered by `test_dialogue.py` (30 tests) |
| `world/crafting_engine.py` | `tests/test_crafting_engine.py` | LOW — covered by `test_crafting.py` (31 tests) |
| `world/ability_registry.py` | `tests/test_ability_registry.py` | MEDIUM — registry structure validation |
| `world/node_helpers.py` | `tests/test_node_helpers.py` | LOW — covered by `test_node_system.py` |
| `world/skill_definitions.py` | `tests/test_skill_definitions.py` | LOW — static data, tested via skill_engine tests |
| `world/dialogue_definitions.py` | None | LOW — static data |
| `world/crafting_definitions.py` | None | LOW — static data |

Note: The "missing" test files for dialogue/crafting engines are naming convention differences — the tests exist under alternate names (test_dialogue.py, test_crafting.py). Real gaps are:
- **ability_registry.py** — no structural validation tests for the 14 ability stubs
- **Integration tests** — no end-to-end combat flow test (start combat → turns → death → corpse → respawn)

### Highest Priority Tests to Add
1. **Integration: Full combat lifecycle** — player enters room, mob auto-engages, combat runs 3 rounds, mob dies, corpse spawns, SpawnRecord schedules respawn
2. **Integration: Skill accumulation pipeline** — player uses ability, passive skill XP accumulates on ndb, safety flush commits to DB
3. **Smoke test: Server startup** — verify all 6 tickers register without import errors (would catch the missing model issue)

---

## 8. Risk Register

| # | Risk | Severity | Likelihood | Mitigation |
|---|------|----------|------------|------------|
| 1 | Missing WorldEventLog/SpawnRecord models crash server on mob death or spawn tick | Critical | Certain | Add model class bodies |
| 2 | getattr(obj.db, ...) returns None instead of default, causing arithmetic TypeError in banking | High | Likely | Replace with `or` pattern |
| 3 | Combat msg() bypass means future client won't receive structured combat data | Medium | Future | Route through oob_publisher |
| 4 | Parallel worktree execution creates migration conflicts | Medium | Recurring | Create migrations on main only |
| 5 | No server startup smoke test — import errors only caught at runtime | Medium | Recurring | Add startup test |
| 6 | 35 test files can't run from Git Bash (Evennia path issue) | Low | Known | Test from Windows terminal or CI |

---

## 9. Recommended Action Plan

### Immediate (Before Any Further Development)
1. **Add WorldEventLog and SpawnRecord class bodies to world/models.py** — derive from migration files
2. **Replace all 18 getattr(obj.db, ...) instances** — mechanical find-and-replace

### Short-Term (Before Phase 7 Content)
3. Delete orphaned files: `world/named_mob_registry.py`, `world/prototypes.py`, `world/help_entries.py`
4. Update CLAUDE.md metrics (test file count, model count)
5. Add a server startup smoke test that imports all world/ modules

### Medium-Term (Before Milestone 2 Client)
6. Route combat_script.py messages through oob_publisher for structured client push
7. Add integration tests for full combat lifecycle and skill accumulation pipeline
8. Review bare `except Exception:` handlers — add logging or narrow exception types

---

## 10. Appendix

### Notable Positive Patterns
- **Consistent (bool, str) return tuples** across all engine modules — very clean error handling interface
- **Lazy imports inside functions** used consistently to break circular dependencies between world/ modules — correct Evennia pattern
- **SaverDict copy pattern** documented and mostly followed for db dict mutations
- **F() expressions** used correctly in banking.py for atomic balance updates
- **ndb for volatile state** — combat state, skill accumulators, group membership all correctly on ndb
- **Tag-based lookups** used consistently instead of scanning all objects
- **TickerHandler for bulk periodic work** — correct choice over per-object Scripts for spawn, ambient, decay

### Open Questions Requiring Runtime Verification
- Does the ambient_npc_tick correctly find NPCs after the tag category fix (object_type → character_type)?
- Does CombatScript survive server reload (db_persistent=True) and correctly resume?
- Do the 8 crafting recipes produce functional items that can be picked up via inventory_engine?
- Does the skill discovery framework fire correctly when skill thresholds are crossed?

### Codebase Metrics
| Metric | Value |
|--------|-------|
| Total Python files (excl. migrations, cache) | ~80 |
| World engine modules | 30+ |
| Command files | 11 |
| Typeclass files | 9 |
| Test files | 35 |
| Django models (defined) | 13 |
| Django models (migrated but missing) | 2 |
| TickerHandler registrations | 6 |
| Command classes | 25+ |
| Lines: World engines | 14,846 |
| Lines: Commands | 2,497 |
| Lines: Typeclasses | 1,126 |
| Lines: Tests | 13,696 |
| Lines: Server conf | 872 |
| Test/Code ratio | ~0.93:1 |
