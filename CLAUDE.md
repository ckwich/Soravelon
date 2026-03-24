# Soravelon

Evennia 6.0 MUD — dark-fantasy multiplayer text game with deep progression systems.

## Tech Stack

- **Engine:** Evennia 6.0 (Django + Twisted)
- **Language:** Python 3.11+
- **DB:** Django ORM (SQLite dev / PostgreSQL prod)
- **App:** `world` registered as custom Django app in `INSTALLED_APPS`

## Project Structure

```
typeclasses/     # Characters, rooms, exits, objects, mobs, scripts, accounts
commands/        # Command sets and custom commands
world/           # Game logic — models, engines, helpers, migrations
  scripts/       # Tick-driven scripts (node_script)
  nodes/         # Zone node effects
server/conf/     # Evennia settings, lifecycle hooks, connection screens
tests/           # Pytest test suite
web/             # Django web frontend (admin, API, webclient, website)
```

## Key Commands

```bash
evennia start            # Start server + portal
evennia stop             # Stop server
evennia reload           # Hot-reload without disconnecting players
evennia migrate          # Run Django migrations (world app has custom models)
evennia test --settings server.conf.settings tests/   # Run tests
```

## Custom Typeclasses (settings.py)

| Role       | Class                                  |
|------------|----------------------------------------|
| Object     | `typeclasses.objects.SoravelonObject`  |
| Character  | `typeclasses.characters.Character`     |
| Room       | `typeclasses.rooms.SoravelonRoom`      |
| Exit       | `typeclasses.exits.SoravelonExit`      |
| Script     | `typeclasses.scripts.SoravelonScript`  |
| Account    | `typeclasses.accounts.SoravelonAccount`|

## Skills Reference

Skills document the game's major systems. Invoke via Skill tool when working in that domain.

| Skill | Trigger | Path |
|-------|---------|------|
| **Base** | Any work in this repo | `.claude/skills/base/skill.md` |
| **World State Engine** | Character progression, domain XP, dimensions | `.claude/skills/world-state-engine/skill.md` |
| **Faction System** | Standings, trust, betrayal, subfactions | `.claude/skills/faction-system/skill.md` |
| **Zone Attunement** | Per-zone attunement (0-100), aggregate scores | `.claude/skills/zone-attunement/skill.md` |
| **Node System** | Zone nodes, Layer 0/1 rooms, failure states, ticks | `.claude/skills/node-system/skill.md` |
| **Mob Affix System** | Rarity tiers, weighted pools, forbidden combos | `.claude/skills/mob-affix-system/skill.md` |
| **Mob Disposition** | Computed disposition float, behavior modifiers | `.claude/skills/mob-disposition/skill.md` |
| **Zone Scaling** | Per-player scaling, mob HP, damage math, loot tiers | `.claude/skills/zone-scaling/skill.md` |
| **Banking** | Deposits, withdrawals, drafts, debt, payments | `.claude/skills/banking/skill.md` |
| **Inventory Engine** | Pickup, drop, equip, containers, encumbrance | `.claude/skills/inventory-engine/skill.md` |
| **Item Typeclasses** | SoravelonItem, Container, Equipment, KeyringItem | `.claude/skills/item-typeclasses/skill.md` |
| **Group System** | Party invite, leadership, loot modes, proximity | `.claude/skills/group-system/skill.md` |
| **Loot Tables** | Drop rates, rarity modifiers, material tiers | `.claude/skills/loot-tables/skill.md` |
| **Server Conf** | Lifecycle hooks, tickers, settings, connections | `.claude/skills/server-conf/skill.md` |

## Conventions

- Store game state on `db` attributes (persisted) or `ndb` (volatile). Never raw Django fields on typeclasses.
- Custom Django models go in `world/models.py`; register the `world` app for migrations.
- All game logic lives in `world/` modules; typeclasses call into them.
- Tests use Evennia's `EvenniaTestCase` or `EvenniaCommandTestMixin`.
- Mob behavior is driven by computed disposition — never hardcode friend/foe.
- Node failure uses a state machine (healthy → stressed → failing → collapsed) — respect the tick-driven progression.

<!-- GSD:project-start source:PROJECT.md -->
## Project

**Soravelon**

A dark-fantasy MUD built on Evennia 6.0, set in a world where ancient dragon-built magical infrastructure is failing. Players explore zones, fight mobs, build domain mastery across 10 disciplines, and develop character identity through 90 unique subclasses formed by domain combinations. The game is a passion project backed by an original novel trilogy — the world lore is deep and the design is pre-planned.

**Core Value:** **Character identity must feel mechanically distinct** — a Duskblade (Combat + Subterfuge) plays fundamentally differently from a Thornguard (Combat + Naturalism). If the 90 subclasses collapse into sameness, the game's central promise fails.

### Constraints

- **Tech stack**: Evennia 6.0 + Django ORM — cannot change, deeply embedded
- **Build order**: Strict dependency chain — systems must be built in documented sequence
- **No visible levels**: Backend level (1-50) is internal only — never exposed to players
- **Evennia patterns**: No `getattr(obj.db, 'attr', default)` — always `obj.db.attr or fallback`; SaverDict copy pattern for list mutations; F() expressions for balance updates
- **Solo developer**: Passion project — no team, no deadline, but production-grade discipline required
- **Client isolation**: Desktop client is a separate repo/project, not embedded in soravelon
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.12.10 - All game logic, typeclasses, commands, world engine
- HTML/CSS/JavaScript - Web frontend (`web/` directory: admin, webclient, website)
## Runtime
- Python 3.12.10
- Twisted 24.11.0 (async networking, telnet/websocket server)
- Django 6.0.3 (ORM, web framework, admin)
- pip (system-level install, no virtualenv detected)
- No lockfile (no `requirements.txt`, `pyproject.toml`, or `setup.cfg` present)
## Frameworks
- Evennia 6.0.0 - MUD engine providing typeclass system, command handler, session management, web client
- Django 6.0.3 - ORM, migrations, admin interface, URL routing
- Twisted 24.11.0 - Async event loop, telnet/SSL/websocket protocol handling
- pytest - Test runner (via `evennia test --settings server.conf.settings tests/`)
- Evennia test utilities (`EvenniaTestCase`, `EvenniaCommandTestMixin`)
- black 26.3.1 - Code formatter
- isort (bundled with Evennia) - Import sorting
## Key Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| evennia | 6.0.0 | MUD engine: typeclasses, commands, sessions, tickers |
| django | 6.0.3 | ORM, migrations, admin, URL routing, templates |
| twisted | 24.11.0 | Async networking: telnet, SSL, websocket protocols |
| autobahn | 20.12.3 | WebSocket protocol implementation (WAMP) |
| djangorestframework | 3.16.1 | REST API framework (Evennia web API) |
| Package | Version | Purpose |
|---------|---------|---------|
| django-sekizai | 2.0.0 | Django template block management |
| pyyaml | 6.0.3 | YAML parsing (config, data files) |
| lunr | 0.7.0.post1 | Full-text search indexing |
| simpleeval | 1.0.3 | Safe expression evaluation |
| black | 26.3.1 | Code formatting |
## Configuration
- `server/conf/settings.py` - Main Evennia/Django settings (imports `evennia.settings_default`)
- `server/conf/secret_settings.py` - Secret overrides (exists, not committed - contains sensitive config)
- Server name: `soravelon`
- Custom Django app: `world` registered in `INSTALLED_APPS`
- `BASE_OBJECT_TYPECLASS` = `typeclasses.objects.SoravelonObject`
- `BASE_CHARACTER_TYPECLASS` = `typeclasses.characters.Character`
- `BASE_ROOM_TYPECLASS` = `typeclasses.rooms.SoravelonRoom`
- `BASE_EXIT_TYPECLASS` = `typeclasses.exits.SoravelonExit`
- `BASE_SCRIPT_TYPECLASS` = `typeclasses.scripts.SoravelonScript`
- `BASE_ACCOUNT_TYPECLASS` = `typeclasses.accounts.SoravelonAccount`
- No build step required - Python source runs directly
- `evennia start` boots both Server (game logic) and Portal (connection handling)
- `evennia reload` hot-reloads server without dropping player connections
## Database
- SQLite3 - `server/evennia.db3`
- Django ORM with Evennia's built-in models + custom `world` app models
- PostgreSQL (configured via `secret_settings.py`)
## Platform Requirements
- Python 3.12+
- Evennia 6.0.0 installed (`pip install evennia`)
- No containerization (no Dockerfile/docker-compose detected)
- Python 3.12+
- PostgreSQL
- Twisted-compatible OS (Linux recommended)
## Ticker System
| Ticker | Interval | Callback |
|--------|----------|----------|
| World state decay | 86400s (24h) | `world.world_state.world_state_decay_tick` |
| Session XP flush | 600s (10m) | `world.world_state.session_xp_safety_flush` |
| Node failure tick | 30s | `world.node_helpers.node_failure_tick` |
| Banking payments | 86400s (24h) | `world.banking.banking_payment_tick` |
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- `snake_case.py` for all modules: `world_state.py`, `mob_disposition.py`, `inventory_engine.py`
- Test files: `test_<module_name>.py` — e.g., `tests/test_banking.py`
- Typeclasses: `<plural_noun>.py` — e.g., `typeclasses/characters.py`, `typeclasses/mobs.py`
- PascalCase with `Soravelon` prefix for game-specific typeclasses: `SoravelonRoom`, `SoravelonMob`, `SoravelonItem`, `SoravelonExit`
- PascalCase without prefix for Evennia compatibility stubs: `Room`, `Object`, `Character`
- Django models: PascalCase without prefix: `FactionStanding`, `BankTransaction`, `InventoryItem`
- Test classes: one class per test scenario, PascalCase describing the assertion: `TestDepositSuccess`, `TestStandingMaxMapsTo06`
- `snake_case` for all functions and methods
- Engine functions use verb-first: `deposit()`, `withdraw()`, `pick_up()`, `drop_item()`, `equip_item()`
- Getter functions: `get_balance()`, `get_mob_disposition()`, `get_carry_state()`
- Internal helpers: `_` prefix: `_record_transaction()`, `_get_group_state()`, `_find_existing_stack()`
- Callbacks: `at_` prefix per Evennia convention: `at_object_creation()`, `at_traverse()`, `at_death()`
- `snake_case` throughout
- Module-level constants: `UPPER_SNAKE_CASE` — `MAX_GROUP_SIZE`, `VALID_LOOT_MODES`, `ALL_DIMENSIONS`
- Data tables: `UPPER_SNAKE_CASE` dicts — `ANCESTRY_FACTION_MODIFIERS`, `CONTAINER_WEIGHT_RANGES`
- No Python enums used. Constants are tuples or dicts at module level.
- Rarity tiers are string constants: `"normal"`, `"magic"`, `"rare"`, `"legendary"`
- Node states are string constants: `"dormant"`, `"awakening"`, `"active"`, `"critical"`
## Code Style
- No formatter configuration detected (no `.prettierrc`, `pyproject.toml`, or `setup.cfg`)
- 4-space indentation (Python standard)
- Lines generally under 100 characters; long lines wrapped with parenthetical continuation
- Single blank line between functions within a module; double blank line between top-level classes
- No linter configuration detected
- Code follows PEP 8 consistently
- Imports at top of file; lazy imports inside functions when avoiding circular dependencies
- Module-level docstrings on every file describing purpose and key behaviors
- Function docstrings on public functions, one-liners for simple getters
- Performance notes in docstrings where relevant (e.g., `world/mob_disposition.py` line 12: "get_mob_disposition() makes up to 2 DB reads")
## Import Organization
- Use inside functions to break circular dependencies. This is the standard pattern:
- Examples: `world/banking.py` line 197 (lazy import of `create_object` inside `issue_draft`), `world/inventory_engine.py` line 136 (lazy import of `SoravelonKeyringItem`)
- None. All imports use full dotted paths.
## The `(bool, str)` Return Tuple Pattern
- `world/banking.py`: `deposit()`, `withdraw()`, `deduct_from_bank()`, `credit_to_bank()`, `issue_draft()`, `redeem_draft()`, `create_debt()`, `pay_debt()`
- `world/inventory_engine.py`: `pick_up()`, `drop_item()`, `put_in_container()`, `take_from_container()`, `equip_item()`, `unequip_item()`
- `world/group_engine.py`: `send_group_invite()`, `accept_group_invite()`, `decline_group_invite()`, `leave_group()`, `kick_from_group()`, `set_loot_mode()`
- `typeclasses/objects.py`: `can_drop()`, `can_equip()`, `can_accept()`, `can_be_sold()`
## The `(bool, str|None)` Reveal Pattern
## SaverDict Copy Pattern
## F() Expression Pattern for Atomic Updates
## Lazy Creation Pattern
- `world/banking.py`: `get_or_create_account()` — bank account created on first deposit
- `world/world_state.py`: `modify_standing()` — `FactionStanding` created on first interaction
- `world/world_state.py`: `update_zone_attunement()` — `ZoneAttunement` via `update_or_create()`
- `world/inventory_engine.py`: `_get_or_create_inventory_record()` — on pickup
## The `getattr` Trap on `db` Attributes
## Data Storage Patterns
- Intrinsic character state: `db.ancestry`, `db.carried_scales`, `db.reputation_score`
- Mob configuration: `db.rarity`, `db.base_disposition`, `db.faction`
- Room metadata: `db.zone_id`, `db.awakening_desc`
- All typeclass state initialized in `at_object_creation()`
- Session accumulators: `ndb.domain_xp_combat` (batch-committed periodically)
- Group state: `ndb.group_state`, `ndb.group_leader_id` (groups dissolve on disconnect)
- Combat caches: `ndb.combat_scales` (per-encounter, cleared on death)
- One-shot reveals: `ndb.revealed_affixes` (reset on mob death)
- Pending invites: `ndb.pending_group_invite`
- Relational data between entities: `FactionStanding`, `ZoneAttunement`
- Transaction logs (immutable): `BankTransaction`, `NodeEventLog`, `WorldEventLog`
- Inventory metadata: `InventoryItem` (links Evennia objects to character inventory)
- Financial state: `BankAccount`, `RecurringPayment`, `DebtRecord`
## Tags Pattern
- `zone_id` — zone membership for rooms
- `room_type` — room classification
- `room_id` — idempotent room lookup
- `node_layer` — `"active"` / `"inactive"` for Layer 1 rooms
- `node_effect` — active node effects on rooms
- `node_state` — current node phase on rooms
- `mob_affix` — active affixes on mobs
- `item_type` — item classification
- `script_type` — script classification
- `character_type` — `"player_character"` for queryset filtering
- `object_type` — `"zone_object"` for zone objects
## Module Organization
## Error Messages
- Player-facing messages use Evennia color codes: `|g` green, `|y` yellow, `|r` red, `|w` white, `|n` reset
- Error messages are descriptive and actionable: `"Unequip sword before dropping it."`, `"The way is locked. You need the right key."`
- Internal error returns use f-strings with context: `f"Insufficient funds. Banked balance: {account.balance} Scales."`
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern Overview
- Typeclasses are thin wrappers that delegate all logic to `world/` engine modules
- Django ORM models in `world/models.py` store relational data (faction standings, inventory, banking)
- Intrinsic character state stored on Evennia `db` attributes (dimension scores, domain progression)
- Session-volatile state stored on `ndb` attributes (group membership, XP accumulators, combat scales)
- Tick-driven systems use Evennia's `TICKER_HANDLER` for periodic processing (node failure, XP flush, decay, payments)
- Area definitions are Python files in `world/areas/` loaded at server start via `AreaBuilder`
## Layers
- Purpose: Define game objects with Evennia hooks, delegate to world engines
- Location: `typeclasses/`
- Contains: Character, Room, Exit, Object/Item, Mob, Script, Account typeclasses
- Depends on: `world/` engine modules (imported lazily in methods)
- Used by: Evennia core (command dispatch, object creation, session management)
- Purpose: All game logic — progression, combat math, inventory management, banking, mob behavior
- Location: `world/` (top-level .py files)
- Contains: Pure-logic modules with no typeclass inheritance
- Depends on: `world/models.py` (Django ORM), Evennia search/create APIs
- Used by: Typeclasses (via lazy imports), TickerHandler callbacks, AreaBuilder
- Purpose: Store relational data that describes entity relationships
- Location: `world/models.py`
- Contains: 9 Django models (FactionStanding, ZoneAttunement, CharacterSkill, NodeEventLog, InventoryItem, BankAccount, BankTransaction, RecurringPayment, DebtRecord, WorldEventLog)
- Depends on: Django ORM, Evennia's `objects.ObjectDB` (ForeignKey target)
- Used by: World engine modules exclusively
## Data Flow
- Persistent intrinsic state: `character.db.*` attributes (scores, levels, currency, ancestry)
- Persistent relational state: Django models in `world/models.py` (faction standings, inventory records, bank accounts)
- Session-volatile state: `character.ndb.*` (XP accumulators, group state, combat scales, gravity penalties)
- In-memory registries: `world/zone_registry.py` and `world/named_mob_registry.py` (rebuilt on every server start)
## Key Abstractions
- Purpose: Five aggregate scores (0-100) that describe character progression
- Dimensions: Reputation, Network, Bond, Legacy, Attunement
- Location: `world/world_state.py`
- Storage: `character.db.*_score` (fast read), with Attunement backed by `ZoneAttunement` model records
- Purpose: 10 skill domains (combat, subterfuge, naturalism, resonance, arcana, diplomacy, alchemy, tactics, engineering, remnance)
- Location: `world/world_state.py`
- Storage: `character.db.domain_scores` dict (0-100 per domain)
- Drives: Backend level calculation (hidden from players), diminishing returns on XP gain
- Purpose: Internal power metric (1-50) derived from weighted domain scores
- Location: `world/world_state.py:calculate_backend_level()`
- NEVER exposed to players
- Used by: Zone scaling (`world/zone_scaling.py`) for per-player combat math
- Purpose: Computed float (-1.0 to +1.0) determining mob behavior toward a character
- Location: `world/mob_disposition.py`
- Inputs: base_disposition, faction standing, ancestry, reputation, trust (for elites)
- Outputs: behavior string (friendly, passive, base, territorial, aggressive)
- Pattern: Always computed fresh, never hardcoded
- Purpose: Zone-level failure state machine (dormant -> awakening -> active -> critical)
- Location: `world/scripts/node_script.py`, `world/node_helpers.py`, `world/nodes/node_effects.py`
- Pattern: Global 30s tick drives all node scripts; Layer 0/1 room swap on activation
- State machine: failure float 0-100 maps to states at thresholds 30/60/90
- Purpose: Declarative Python DSL for defining zones (rooms, exits, mobs, quests, materials)
- Location: `world/area_builder.py`
- Pattern: Area spec files in `world/areas/` define `build()` functions; loaded at server start
- Creates: Evennia Room/Exit/ZoneObject DB objects; registers zones and named mobs in memory registries
## Entry Points
- Location: `server/conf/at_server_startstop.py:at_server_start()`
- Registers 4 TickerHandler callbacks (decay, XP flush, node tick, banking)
- Calls `initialize_node_pool()` to recover orphaned Layer 1 rooms
- Calls `_load_all_zones()` to import all `world/areas/*.py` and run their `build()` functions
- Location: `typeclasses/characters.py:Character.at_object_creation()`
- Initializes all dimension scores, domain scores, currency, companion, quest state
- Tags character as `player_character` for queryset filtering
- Location: `typeclasses/mobs.py:SoravelonMob.initialize_for_spawn()`
- Calls `world.mob_affix_roller.apply_affixes_to_mob()` for rarity/affix rolling
- Calls `world.zone_scaling.initialize_mob_combat_stats()` for HP/damage setup
## Module Dependency Graph
```
```
## Error Handling
- All engine functions that can fail return `(success: bool, message: str)` tuples
- Callers check success before proceeding; message is sent to player on failure
- Examples: `world/banking.py:deposit()`, `world/inventory_engine.py:pick_up()`, `world/group_engine.py:send_group_invite()`
- Django model lookups use `try/except DoesNotExist` with sensible defaults (0, None, False)
- Atomic DB updates use `F()` expressions and `filter().update()` for concurrency safety (banking, faction standing)
## Cross-Cutting Concerns
- World-state decay: 86400s (24h) -- `world.world_state.world_state_decay_tick`
- Session XP flush: 600s (10min) -- `world.world_state.session_xp_safety_flush`
- Node failure: 30s -- `world.node_helpers.node_failure_tick`
- Banking payments: 86400s (24h) -- `world.banking.banking_payment_tick`
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd:quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd:debug` for investigation and bug fixing
- `/gsd:execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd:profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
