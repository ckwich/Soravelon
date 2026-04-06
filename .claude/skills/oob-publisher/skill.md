---
name: oob-publisher
description: Centralized OOB message hub — debounced server-to-client push for status, map, combat, inventory, flights, and node events
---

## Activation

This skill triggers when editing these files:
- `world/oob_publisher.py`

Keywords: oob, push, status_update, map_update, node_event, flight_progress, combat_update, inventory_update, stat_update, quest_update, debounce, oob_publisher

---

You are working on **the OOB publisher** (`world/oob_publisher.py`) — the single hub for all server-to-client push data.

## Key Files
- `world/oob_publisher.py` — All push functions, debounce logic, group position helper
- `tests/test_oob_publisher.py` — 28 tests (MagicMock characters, no DB needed)

## Key Concepts
- **Single entry point:** All game systems call `push_*` functions here. Never call `character.msg()` for OOB directly from game logic.
- **Wire format:** `character.msg(msg_type=data)` → WebSocket frame `["msg_type", [], {data}]` (Evennia native OOB).
- **Debounce per message type:** `DEBOUNCE_INTERVALS` dict controls min seconds between sends. Timestamps stored in `character.ndb.oob_debounce` (SaverDict copy pattern). Interval ≤0 means always send.
- **Session guard:** `_send()` checks `character.sessions.all()` before sending — silently skips disconnected characters.
- **8 message types:** `status_update` (2s), `map_update` (0.5s), `node_event` (0s), `flight_progress` (1s), `combat_update` (0.25s), `quest_update` (5s), `inventory_update` (1s), `stat_update` (0.5s).

## Message Types
- **`push_status_update`** — Reads `get_character_context_packet()` for dimensions/domains/currency/companion
- **`push_map_update`** — Full zone room graph with fog-of-war, exits, node states, group markers. Filters candidates to `SoravelonRoom` only (avoids exits/zone objects/mobs)
- **`push_node_event`** — Zone node state transition (no debounce — must not drop)
- **`push_flight_progress`** — Dragon Courier leg tracking (called by FlightScript)
- **`push_combat_update`** — Phase 6 placeholder passthrough
- **`push_quest_update`** — Merges event payload with `quest_engine.get_active_quests()` list. Sends `event`, `event_quest_id`, and full `active_quests` snapshot
- **`push_inventory_update`** — Items stub + live encumbrance via `get_carry_state()`
- **`push_stat_update`** — HP/resource bars including `hp`, `hp_max`, and `conditions`

## Critical Rules
1. **Never call `character.msg()` for OOB directly** — always go through `push_*` functions in this module
2. **SaverDict copy pattern for debounce** — `_mark_sent()` copies `ndb.oob_debounce` to plain dict, mutates, reassigns
3. **Session check before send** — `_send()` guards with `character.sessions.all()`. Never skip this
4. **Room filtering in map_update** — only include objects whose `db_typeclass_path` ends with `rooms.SoravelonRoom`. Zone tags match exits, zone objects, and mobs too
5. **Lazy imports throughout** — `world_state`, `group_engine`, `inventory_helpers`, `quest_engine`, `evennia` imported inside functions to avoid circular deps
6. **`node_event` has 0s debounce** — state transitions are rare and must never be dropped

## References
- **World State:** `world/world_state.py` — `get_character_context_packet()` feeds `push_status_update`
- **Group Engine:** `world/group_engine.py` — `get_group_state()` feeds map group markers
- **Inventory Helpers:** `world/inventory_helpers.py` — `get_carry_state()` feeds `push_inventory_update`
- **Quest Engine:** `world/quest_engine.py` — `get_active_quests()` feeds `push_quest_update`
- **Tests:** `tests/test_oob_publisher.py` — Full coverage with MagicMock characters

---
**Last Updated:** 2026-04-04
