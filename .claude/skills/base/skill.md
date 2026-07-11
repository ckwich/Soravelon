---
name: base
description: Core conventions, tech stack, and project structure for soravelon Evennia MUD
---

## Activation

This is a **base skill** that always loads when working in this repository.

---

You are working in **Soravelon**, an Evennia 6.1 MUD game.

## Tech Stack
Evennia 6.1.0 | Python 3.12+ | Django ORM | Twisted

## Commands
- `python scripts/run_tests.py [test_label ...]` — Canonical Django/Evennia test path
- `python scripts/smoke_start.py` — Bootstrap/import smoke gate
- `evennia start` / `evennia stop` / `evennia reload` — Server lifecycle (after activating `.venv`)
- `evennia test --settings settings.py <test_label>` — Focused launcher alternative; `--settings` is a filename, not `server.conf.settings`
- `evennia makemigrations world` / `evennia migrate` — DB migrations

## Architecture (3 layers)
- **Typeclasses** (`typeclasses/`) — Evennia entities (Character, Room, Object, Mob, Script) inheriting `Default*` via `ObjectParent` mixin
- **World engines** (`world/`) — Stateless service modules (world_state, banking, inventory_engine, mob_affixes, patrol_engine, flight_engine, oob_publisher) called from typeclasses
- **Django models** (`world/models.py`) — Relational state: FactionStanding, ZoneAttunement, CharacterSkill, InventoryItem, BankAccount, etc.

## Structure
- `typeclasses/` — Entity definitions (characters, rooms, objects, mobs, scripts)
- `world/` — Game logic engines, Django models, loot tables, node system
- `world/areas/` — Zone spec files (declarative Python DSL via AreaBuilder)
- `world/scripts/` — Tick-driven scripts (node_script, patrol_script, flight_script)
- `commands/` — Custom commands and cmdsets
- `server/conf/` — Settings, lifecycle hooks, connection screens, parsers
- `tests/` — Django/Evennia test suite
- `web/` — Django web frontend customization

## Critical Rules
1. **Return `(bool, str)` tuples** from game logic — no exceptions for normal flow
2. **Backend level is INTERNAL ONLY** — never expose to players
3. **Lazy record creation** — missing `world/models.py` record = default/neutral
4. **Session XP in `ndb`** — volatile until `commit_session_xp()`. Flush at logout, every 10m, and via safety ticker
5. **Item metadata in Django model** — weight/quantity/equip state live in `InventoryItem`, not on Evennia object. Use `inventory_engine.py` for all item ops
6. **Atomic balance updates** — always `F()` expressions, never read-modify-write
7. **SaverDict copy pattern** — copy `db.*` dict to plain dict, mutate, assign once (avoids N+1 repickle)
8. **Relational data in Django models** — faction standings, inventory, bank balances go in `world/models.py`, not `db.*`
9. **Batch-fetch pattern** — collect IDs, single `filter(id__in=ids)`, build lookup dict to prevent N+1
10. **Containers cannot nest** — `SoravelonContainer.can_accept()` rejects other containers
11. **OOB messages go through `oob_publisher`** — never call `character.msg()` for OOB directly from game logic

---
**Last Updated:** 2026-07-11
