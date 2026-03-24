# Project Structure

**Analysis Date:** 2026-03-24

## Directory Layout

```
soravelon/
├── commands/                # Command sets and custom commands
│   ├── __init__.py
│   ├── command.py           # Base Command class (mostly Evennia scaffold)
│   └── default_cmdsets.py   # CharacterCmdSet, AccountCmdSet, etc.
├── server/
│   ├── conf/                # Evennia server configuration
│   │   ├── settings.py      # Typeclass overrides, INSTALLED_APPS
│   │   ├── at_server_startstop.py  # Ticker registration, zone loading
│   │   ├── at_initial_setup.py     # First-run setup
│   │   ├── connection_screens.py   # Login screen
│   │   ├── secret_settings.py      # Local secrets (gitignored)
│   │   └── ...              # Other Evennia hook files
│   ├── logs/                # Runtime logs
│   └── .static/             # Collected static files (generated)
├── tests/                   # Pytest test suite
│   ├── __init__.py
│   ├── test_area_builder.py
│   ├── test_banking.py
│   ├── test_group_engine.py
│   ├── test_inventory_engine.py
│   ├── test_mob_affixes.py
│   ├── test_mob_disposition.py
│   ├── test_node_system.py
│   ├── test_typeclasses.py
│   ├── test_world_state.py
│   └── test_zone_scaling.py
├── typeclasses/             # Evennia typeclass definitions
│   ├── __init__.py
│   ├── accounts.py          # SoravelonAccount (preferences)
│   ├── characters.py        # Character (dimensions, domains, login/logout)
│   ├── channels.py          # Default channel typeclass
│   ├── exits.py             # SoravelonExit, LockedExit, HiddenExit, NodeGravityExit
│   ├── mobs.py              # SoravelonMob (affixes, disposition, combat)
│   ├── objects.py           # SoravelonObject, SoravelonItem, Container, Equipment, KeyringItem
│   ├── rooms.py             # SoravelonRoom, Layer1Room
│   └── scripts.py           # SoravelonScript, SessionCommitScript, WorldEventScript
├── web/                     # Django web frontend
│   ├── admin/               # Admin URL overrides
│   ├── api/                 # REST API (empty — not yet implemented)
│   ├── static/              # Static assets (CSS, JS)
│   ├── templates/           # HTML templates
│   ├── webclient/           # Evennia webclient customization
│   ├── website/             # Website pages
│   └── urls.py              # URL routing
├── world/                   # Game logic — engines, models, data
│   ├── __init__.py
│   ├── apps.py              # Django app config for 'world'
│   ├── models.py            # Django models (9 models, 291 lines)
│   ├── area_builder.py      # AreaBuilder DSL for zone definitions (610 lines)
│   ├── areas/               # Zone spec files (loaded at server start)
│   │   └── __init__.py      # (area .py files go here)
│   ├── banking.py           # Banking engine (291 lines)
│   ├── group_engine.py      # Group/party system (298 lines)
│   ├── inventory_engine.py  # Inventory management (455 lines)
│   ├── inventory_helpers.py # Weight/carry state calculation (71 lines)
│   ├── loot_tables.py       # Loot tier modifiers (stub, 19 lines)
│   ├── mob_affix_roller.py  # Rarity rolling and affix application (164 lines)
│   ├── mob_affixes.py       # Affix definitions data (266 lines)
│   ├── mob_disposition.py   # Disposition computation (157 lines)
│   ├── named_mob_registry.py # In-memory named mob registry (35 lines)
│   ├── node_helpers.py      # Node system helpers and tick driver (172 lines)
│   ├── nodes/               # Node subsystem
│   │   ├── __init__.py
│   │   └── node_effects.py  # Node type effect tags (32 lines)
│   ├── prototypes.py        # Evennia prototype definitions (90 lines)
│   ├── scripts/             # Script typeclasses for game systems
│   │   ├── __init__.py
│   │   └── node_script.py   # NodeScript state machine (187 lines)
│   ├── world_state.py       # World-state engine — dimensions, domains, factions (383 lines)
│   ├── zone_object.py       # Zone initialization and Layer 1 room creation (65 lines)
│   ├── zone_registry.py     # In-memory zone registry (36 lines)
│   ├── zone_scaling.py      # Per-player scaling math (137 lines)
│   ├── help_entries.py      # In-game help text
│   ├── batch_cmds.ev        # Evennia batch command file
│   └── migrations/          # Django migrations for world app
├── .claude/                 # Claude skill files
│   └── skills/              # 14 skill directories for domain knowledge
├── .planning/               # Planning documents
│   └── codebase/            # Codebase analysis docs
├── CLAUDE.md                # Project instructions
└── README.md                # Project readme
```

## Key File Locations

**Entry Points:**
- `server/conf/settings.py`: Evennia settings, typeclass overrides, INSTALLED_APPS
- `server/conf/at_server_startstop.py`: Server lifecycle hooks, ticker registration, zone loading

**Configuration:**
- `server/conf/settings.py`: All Evennia settings (55 lines — minimal overrides)
- `server/conf/secret_settings.py`: Local secrets (exists, never read)
- `server/conf/connection_screens.py`: Login screen text

**Core Logic (world engines):**
- `world/world_state.py`: Dimension/domain/faction/attunement management (383 lines)
- `world/banking.py`: Full banking system with drafts, debt, recurring payments (291 lines)
- `world/inventory_engine.py`: Pickup, drop, equip, container operations (455 lines)
- `world/mob_disposition.py`: Computed disposition float from standing/ancestry/trust (157 lines)
- `world/zone_scaling.py`: Logarithmic per-player combat scaling (137 lines)
- `world/group_engine.py`: Party system with loot modes (298 lines)
- `world/area_builder.py`: Zone definition DSL (610 lines)

**Data Definitions:**
- `world/models.py`: All Django models (291 lines)
- `world/mob_affixes.py`: Affix data definitions and combat interface stubs (266 lines)
- `world/loot_tables.py`: Loot tier modifiers (stub, 19 lines)

**Typeclasses:**
- `typeclasses/characters.py`: Character with login/logout hooks (108 lines)
- `typeclasses/mobs.py`: Mob with affixes, disposition, combat interface (139 lines)
- `typeclasses/objects.py`: Item hierarchy — Item, Container, Equipment, KeyringItem (165 lines)
- `typeclasses/rooms.py`: SoravelonRoom and Layer1Room (50 lines)
- `typeclasses/exits.py`: Exit variants — Locked, Hidden, NodeGravity (99 lines)
- `typeclasses/scripts.py`: SessionCommitScript, WorldEventScript (47 lines)

**Testing:**
- `tests/test_world_state.py`: World-state engine tests (398 lines)
- `tests/test_banking.py`: Banking system tests (382 lines)
- `tests/test_inventory_engine.py`: Inventory tests (440 lines)
- `tests/test_node_system.py`: Node system tests (427 lines)
- `tests/test_area_builder.py`: AreaBuilder tests (491 lines)
- `tests/test_mob_disposition.py`: Disposition tests (382 lines)
- `tests/test_mob_affixes.py`: Affix system tests (293 lines)
- `tests/test_group_engine.py`: Group system tests (254 lines)
- `tests/test_zone_scaling.py`: Scaling tests (248 lines)
- `tests/test_typeclasses.py`: Typeclass tests (283 lines)

## Module Organization

Code is organized by **architectural layer**, not by feature/domain:

- `typeclasses/` = interface layer (one file per Evennia object type)
- `world/` = business logic layer (one file per game system/engine)
- `world/models.py` = persistence layer (all models in one file)
- `tests/` = flat test directory (one test file per engine/system)
- `commands/` = command dispatch (currently using Evennia defaults)

Within `world/`, each `.py` file is a self-contained engine module. Cross-engine calls use explicit imports. No barrel files or re-exports.

## Naming Conventions

**Files:**
- Typeclasses: plural noun matching Evennia convention (`characters.py`, `rooms.py`, `objects.py`)
- World engines: `snake_case` descriptive name (`world_state.py`, `mob_disposition.py`, `zone_scaling.py`)
- Tests: `test_` prefix matching engine name (`test_banking.py`, `test_world_state.py`)

**Directories:**
- Top-level: lowercase, no underscores (`typeclasses/`, `commands/`, `world/`, `tests/`)
- Sub-packages: lowercase, descriptive (`world/scripts/`, `world/nodes/`, `world/areas/`)

## Where to Add New Code

**New Game System/Engine:**
- Primary code: `world/{system_name}.py`
- Tests: `tests/test_{system_name}.py`
- If the system needs Django models: add to `world/models.py`, then `evennia migrate`
- If the system needs a typeclass: add to appropriate `typeclasses/*.py` file
- If the system needs a tick: register in `server/conf/at_server_startstop.py:at_server_start()`

**New Typeclass:**
- Add to existing file if it fits (e.g., new exit type goes in `typeclasses/exits.py`)
- Create new file in `typeclasses/` only for entirely new object categories
- Override in `server/conf/settings.py` if replacing a BASE_*_TYPECLASS

**New Command:**
- Command class: `commands/command.py` (or create a new file in `commands/`)
- Register in appropriate cmdset in `commands/default_cmdsets.py`

**New Zone/Area:**
- Create `world/areas/{zone_id}.py` with a `build()` function using `AreaBuilder`
- Will be auto-loaded on server start by `_load_all_zones()`

**New Script:**
- Simple scripts: add class to `typeclasses/scripts.py`
- Complex subsystem scripts: create `world/scripts/{name}.py` (like `node_script.py`)

**New Django Model:**
- Add to `world/models.py`
- Run `evennia migrate` to generate and apply migration

**Utilities/Helpers:**
- Small helpers for an engine: add to the engine's own file
- Shared helpers used by multiple engines: create `world/{topic}_helpers.py` (pattern: `inventory_helpers.py`)

## Special Directories

**`world/areas/`:**
- Purpose: Zone definition spec files (Python) loaded dynamically at server start
- Generated: No (authored by hand or builder tools)
- Committed: Yes
- Pattern: Each file exports a `build()` function that uses `AreaBuilder`

**`world/migrations/`:**
- Purpose: Django database migrations for the `world` app
- Generated: Yes (by `evennia migrate`)
- Committed: Yes

**`server/.static/`:**
- Purpose: Collected static files for Django admin and webclient
- Generated: Yes (by `collectstatic`)
- Committed: Yes (Evennia convention)

**`server/logs/`:**
- Purpose: Runtime server logs
- Generated: Yes
- Committed: No (gitignored)

**`.claude/skills/`:**
- Purpose: 14 skill files providing domain knowledge for Claude sessions
- Generated: No (authored)
- Committed: Yes

---

*Structure analysis: 2026-03-24*
