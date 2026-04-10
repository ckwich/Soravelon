# Architecture

**Analysis Date:** 2026-03-24

## Pattern Overview

**Overall:** Three-layer architecture on top of Evennia 6.0 (Django + Twisted)

**Key Characteristics:**
- Typeclasses are thin wrappers that delegate all logic to `world/` engine modules
- Django ORM models in `world/models.py` store relational data (faction standings, inventory, banking)
- Intrinsic character state stored on Evennia `db` attributes (dimension scores, domain progression)
- Session-volatile state stored on `ndb` attributes (group membership, XP accumulators, combat scales)
- Tick-driven systems use Evennia's `TICKER_HANDLER` for periodic processing (node failure, XP flush, decay, payments)
- Area definitions are Python files in `world/areas/` loaded at server start via `AreaBuilder`

## Layers

**Layer 1 - Typeclasses (Interface Layer):**
- Purpose: Define game objects with Evennia hooks, delegate to world engines
- Location: `typeclasses/`
- Contains: Character, Room, Exit, Object/Item, Mob, Script, Account typeclasses
- Depends on: `world/` engine modules (imported lazily in methods)
- Used by: Evennia core (command dispatch, object creation, session management)

**Layer 2 - World Engines (Business Logic):**
- Purpose: All game logic — progression, combat math, inventory management, banking, mob behavior
- Location: `world/` (top-level .py files)
- Contains: Pure-logic modules with no typeclass inheritance
- Depends on: `world/models.py` (Django ORM), Evennia search/create APIs
- Used by: Typeclasses (via lazy imports), TickerHandler callbacks, AreaBuilder

**Layer 3 - Django Models (Persistence):**
- Purpose: Store relational data that describes entity relationships
- Location: `world/models.py`
- Contains: 9 Django models (FactionStanding, ZoneAttunement, CharacterSkill, NodeEventLog, InventoryItem, BankAccount, BankTransaction, RecurringPayment, DebtRecord, WorldEventLog)
- Depends on: Django ORM, Evennia's `objects.ObjectDB` (ForeignKey target)
- Used by: World engine modules exclusively

## Data Flow

**Command Execution Flow:**

1. Player input arrives via Evennia's Twisted protocol
2. `commands/default_cmdsets.py` routes to command class
3. Command's `func()` calls world engine function (e.g., `world.inventory_engine.pick_up()`)
4. Engine function reads/writes Django models and Evennia `db`/`ndb` attributes
5. Engine returns `(success: bool, message: str)` tuple
6. Command sends message to player via `character.msg()`

**Character Login Flow:**

1. `Character.at_post_puppet()` fires (`typeclasses/characters.py:68`)
2. Calls `world.world_state.init_session_accumulators()` to initialize ndb XP accumulators
3. Creates `SessionCommitScript` (persistent=False, interval=600s) for periodic XP flush and debt countdown

**Character Logout Flow:**

1. `Character.at_pre_unpuppet()` fires (`typeclasses/characters.py:84`)
2. Calls `world.world_state.commit_session_xp()` to batch-write accumulated domain XP
3. Calls `world.group_engine.on_member_disconnect()` to remove from group

**Domain XP Accumulation:**

1. Game actions call `world.world_state.accumulate_domain_xp(character, domain, raw_xp)` -- writes to `ndb` only
2. Every 10 minutes, `SessionCommitScript.at_repeat()` calls `commit_session_xp()` -- batch writes `ndb` to `db`
3. On logout, `at_pre_unpuppet()` calls `commit_session_xp()` for final flush
4. Global safety flush via TickerHandler every 600s catches any missed characters

**State Management:**
- Persistent intrinsic state: `character.db.*` attributes (scores, levels, currency, ancestry)
- Persistent relational state: Django models in `world/models.py` (faction standings, inventory records, bank accounts)
- Session-volatile state: `character.ndb.*` (XP accumulators, group state, combat scales, gravity penalties)
- In-memory registries: `world/zone_registry.py` and `world/named_mob_registry.py` (rebuilt on every server start)

## Key Abstractions

**World-State Dimensions:**
- Purpose: Five aggregate scores (0-100) that describe character progression
- Dimensions: Reputation, Network, Bond, Legacy, Attunement
- Location: `world/world_state.py`
- Storage: `character.db.*_score` (fast read), with Attunement backed by `ZoneAttunement` model records

**Domain Scores:**
- Purpose: 10 skill domains (combat, subterfuge, naturalism, resonance, arcana, diplomacy, alchemy, tactics, engineering, remnance)
- Location: `world/world_state.py`
- Storage: `character.db.domain_scores` dict (0-100 per domain)
- Drives: Backend level calculation (hidden from players), diminishing returns on XP gain

**Backend Level:**
- Purpose: Internal power metric (1-50) derived from weighted domain scores
- Location: `world/world_state.py:calculate_backend_level()`
- NEVER exposed to players
- Used by: Zone scaling (`world/zone_scaling.py`) for per-player combat math

**Mob Disposition:**
- Purpose: Computed float (-1.0 to +1.0) determining mob behavior toward a character
- Location: `world/mob_disposition.py`
- Inputs: base_disposition, faction standing, ancestry, reputation, trust (for elites)
- Outputs: behavior string (friendly, passive, base, territorial, aggressive)
- Pattern: Always computed fresh, never hardcoded

**Node System:**
- Purpose: Zone-level failure state machine (dormant -> awakening -> active -> critical)
- Location: `world/scripts/node_script.py`, `world/node_helpers.py`, `world/nodes/node_effects.py`
- Pattern: Global 30s tick drives all node scripts; Layer 0/1 room swap on activation
- State machine: failure float 0-100 maps to states at thresholds 30/60/90

**AreaBuilder:**
- Purpose: Declarative Python DSL for defining zones (rooms, exits, mobs, quests, materials)
- Location: `world/area_builder.py`
- Pattern: Area spec files in `world/areas/` define `build()` functions; loaded at server start
- Creates: Evennia Room/Exit/ZoneObject DB objects; registers zones and named mobs in memory registries

## Entry Points

**Server Start:**
- Location: `server/conf/at_server_startstop.py:at_server_start()`
- Registers 4 TickerHandler callbacks (decay, XP flush, node tick, banking)
- Calls `initialize_node_pool()` to recover orphaned Layer 1 rooms
- Calls `_load_all_zones()` to import all `world/areas/*.py` and run their `build()` functions

**Character Creation:**
- Location: `typeclasses/characters.py:Character.at_object_creation()`
- Initializes all dimension scores, domain scores, currency, companion, quest state
- Tags character as `player_character` for queryset filtering

**Mob Spawn:**
- Location: `typeclasses/mobs.py:SoravelonMob.initialize_for_spawn()`
- Calls `world.mob_affix_roller.apply_affixes_to_mob()` for rarity/affix rolling
- Calls `world.zone_scaling.initialize_mob_combat_stats()` for HP/damage setup

## Module Dependency Graph

```
typeclasses/characters.py
  -> world/world_state.py (login/logout XP management)
  -> world/group_engine.py (disconnect handling)
  -> world/inventory_helpers.py (encumbrance check on move)
  -> world/banking.py (banked_scales property)

typeclasses/mobs.py
  -> world/mob_affix_roller.py (spawn affixes)
  -> world/mob_affixes.py (affix definitions)
  -> world/mob_disposition.py (behavior computation)
  -> world/zone_scaling.py (combat stat init)

typeclasses/objects.py
  -> world/models.py (InventoryItem lookups)

typeclasses/exits.py
  -> world/models.py (keyring check for LockedExit)

typeclasses/scripts.py
  -> world/world_state.py (session XP commit)
  -> world/banking.py (debt timer)

world/world_state.py
  -> world/models.py (FactionStanding, ZoneAttunement, WorldEventLog)

world/banking.py
  -> world/models.py (BankAccount, BankTransaction, RecurringPayment, DebtRecord)

world/inventory_engine.py
  -> world/models.py (InventoryItem)
  -> world/inventory_helpers.py (carry state)

world/mob_disposition.py
  -> world/world_state.py (standing, trust lookups)

world/mob_affix_roller.py
  -> world/mob_affixes.py (affix pools, weights, forbidden combos)

world/zone_scaling.py (no world/ dependencies — standalone math)

world/node_helpers.py
  -> world/nodes/node_effects.py (cleanup on recovery)

world/scripts/node_script.py
  -> world/node_helpers.py (room radius, effects)
  -> world/nodes/node_effects.py (apply/remove effects)

world/area_builder.py
  -> world/zone_registry.py (register zone)
  -> world/named_mob_registry.py (register named mobs)
  -> world/zone_object.py (node initialization)
  -> typeclasses/rooms.py (room creation)
  -> typeclasses/exits.py (exit creation)
  -> typeclasses/objects.py (zone object creation)

server/conf/at_server_startstop.py
  -> world/world_state.py (decay tick, XP flush)
  -> world/node_helpers.py (node tick, pool init)
  -> world/banking.py (payment tick)
  -> world/zone_registry.py (clear on start)
  -> world/named_mob_registry.py (clear on start)
  -> world/areas/*.py (dynamic import + build)
```

## Error Handling

**Strategy:** Return-tuple pattern for user-facing operations

**Patterns:**
- All engine functions that can fail return `(success: bool, message: str)` tuples
- Callers check success before proceeding; message is sent to player on failure
- Examples: `world/banking.py:deposit()`, `world/inventory_engine.py:pick_up()`, `world/group_engine.py:send_group_invite()`
- Django model lookups use `try/except DoesNotExist` with sensible defaults (0, None, False)
- Atomic DB updates use `F()` expressions and `filter().update()` for concurrency safety (banking, faction standing)

## Cross-Cutting Concerns

**Logging:** World events recorded via `world.world_state.log_world_event()` into `WorldEventLog` model. No structured application logging beyond Evennia defaults.

**Validation:** AreaBuilder validates zone_type, continent, direction, room_type against constant sets. Raises `AreaBuilderValidationError` on invalid specs.

**Authentication:** Handled entirely by Evennia's account/session system. Custom `SoravelonAccount` adds preference attributes only.

**Tick System:** Four global tickers registered in `at_server_start()`:
- World-state decay: 86400s (24h) -- `world.world_state.world_state_decay_tick`
- Session XP flush: 600s (10min) -- `world.world_state.session_xp_safety_flush`
- Node failure: 30s -- `world.node_helpers.node_failure_tick`
- Banking payments: 86400s (24h) -- `world.banking.banking_payment_tick`

Plus per-character `SessionCommitScript` (600s, non-persistent) created on login.

---

*Architecture analysis: 2026-03-24*
