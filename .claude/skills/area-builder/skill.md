---
name: area-builder
description: Declarative zone DSL — rooms, exits, spawns, NPCs, quests, materials, patrols, flights, nodes, gathering pools, grid coords, and world position
---

## Activation

This skill triggers when editing these files:
- `world/area_builder.py`
- `world/area_validator.py`
- `world/areas/*.py`
- `world/zone_registry.py`
- `world/named_mob_registry.py`
- `tests/test_area_builder.py`

Keywords: area builder, zone, room, area, build, grid, world position, auto layout, flight point, flight route, cross-zone exit, spawn, named mob, patrol, trigger, quest, material, gathering pool, lore fragment, validate zone, area validator, item definition, spawn point, greeter room, respawn point

---

You are working on **the AreaBuilder** (`world/area_builder.py`) — the declarative Python DSL that translates zone spec files into Evennia DB objects.

## Key Files
- `world/area_builder.py` — DSL class: `zone()`, `room()`, `exit()`, `spawn()`, `named_mob()`, `npc()`, `mob()`, `item()`, `patrol()`, `trigger()`, `custom_command()`, `flight_point()`, `flight_route()`, `node()`, `quest()`, `material()`, `gathering_pool()`, `lore_fragment()`, `build()`
- `world/area_validator.py` — Pure-Python validation (no Django/Evennia imports). `AreaBuilderValidationError`, `ValidationError` dataclass, `validate_zone()`, and all validation constants (`VALID_ZONE_TYPES`, `VALID_CONTINENTS`, `VALID_NODE_TYPES`, `VALID_DIRECTIONS`, `VALID_ROOM_TYPES`, `VALID_FACTION_TERRITORIES`)
- `world/material_definitions.py` — `MATERIAL_REGISTRY` taxonomy consumed by `material()` and `gathering_pool()` DSL methods
- `world/gathering_engine.py` — `initialize_zone_gathering()` called from `build()` to spawn initial gathering nodes
- `world/areas/*.py` — Zone spec files that import AreaBuilder and define `build()` functions
- `world/zone_registry.py` — Module-level singleton; zones registered in `build()`
- `world/named_mob_registry.py` — Module-level singleton; named mobs registered in `build()`
- `server/conf/at_server_startstop.py` — `_load_all_zones()` imports and runs all `world/areas/*.py` at server start
- `tests/test_area_builder.py` — Comprehensive test suite with `AreaBuilderTestBase`

## Key Concepts
- **Idempotent builds:** Rooms and zone objects are found by tag lookup (`room_id`, `zone_id` categories). Re-running `build()` updates in place, never duplicates.
- **Cross-zone exits deferred:** `exit(r1, "other_zone:room_id", "south")` stores in `_deferred_exits`, resolved in `build()` by tag lookup. Warns if target zone not loaded yet.
- **Grid coordinates:** `room()` accepts optional `grid_x`/`grid_y`. Rooms without explicit coords get auto-assigned by `auto_layout_zone()` (BFS from first unassigned room, using `DIRECTION_OFFSETS`). Collision on zero-offset exits (up/down/in/out) resolved by nudging `x += 1`.
- **Zone world position:** `zone()` accepts `world_x`, `world_y`, `world_radius` for continent-level map placement. Stored on ZoneObject `db.*`.
- **Spawn definitions are data, not objects:** `spawn()` stores definition dicts on `room.db.spawn_definitions`. `named_mob()` also stores on `room.db.spawn_definitions` (with `is_named=True`, `count_min=1`, `count_max=1`). Actual mob creation happens at runtime.
- **Item definitions:** `item()` stores item definition dicts on `zone_obj.db.item_definitions`. Requires `zone()` first. Returns `self` for chaining. Extra kwargs (e.g. `damage_min`) are preserved in the stored dict.
- **Gathering pools:** `gathering_pool()` stores pool definition dicts on `zone_obj.db.gathering_pools`. `build()` calls `initialize_zone_gathering()` which spawns `GatheringPoolScript` per pool and creates initial `GatheringNode` objects in eligible rooms.
- **Material placement:** `material()` DSL method wires material IDs from `MATERIAL_REGISTRY` to room gathering nodes. Material IDs must exist in the registry.
- **Patrol wiring:** `patrol()` defers to `build()` → `_finalize_patrols()` which attaches `PatrolScript` to mob objects registered via `mob()`.
- **Spawn point tags:** Zone specs tag special rooms directly (not via DSL methods): `greeter_room` (category `spawn_point`) for new character spawn, `respawn_point` (category `spawn_point`) for death respawn. These are consumed by `Character.at_object_creation()` and `combat_engine._respawn_player()` via `search_tag`.
- **Validation split:** Constants and `validate_zone()` live in `world/area_validator.py` (pure Python, no server deps). `area_builder.py` imports them. The validator can be bundled into external tools (GUI builder sidecar) without Evennia.
- **`validate_zone()` returns `list[ValidationError]`** — dataclass with `severity`, `field_path`, `message`. Empty list = valid. Validates zone name, zone_type, continent, node_type, faction_territory, room_types, and exit directions.

## Critical Rules
1. **SaverDict copy pattern everywhere** — all list appends use `list(room.db.X or [])`, mutate, reassign. Never `.append()` directly on `db.*`
2. **No level gates** — `requires_level` is silently stripped from exits. Design has no visible levels
3. **Zone objects searched by tag** — `_get_or_create_zone_object()` uses `search_tag("zone_object", category="object_type")`, not queryset scan
4. **`build()` order matters** — cross-zone exits → node init → gathering pool init → patrols → auto_layout → named mob registry → zone registry → list attr init
5. **Flight route minimum 30s** — enforced in `flight_route()`, raises `AreaBuilderValidationError` if `leg_duration < 30`
6. **Node init deferred** — `node()` stores config; `build()` calls `initialize_node()` after all rooms exist
7. **`auto_layout_zone()` never overwrites explicit coords** — rooms with `grid_x is not None` are skipped
8. **Validation constants live in `area_validator.py`** — single source of truth. Do not duplicate these sets in `area_builder.py` or elsewhere
9. **`named_mob()` uses spawn_definitions, not named_mob_definitions** — stored on `room.db.spawn_definitions` with `is_named=True`. The old `named_mob_definitions` attr is not used.
10. **Spawn point tags are manual** — `greeter_room` and `respawn_point` tags (category `spawn_point`) are added directly in zone spec `build()` functions via `room.tags.add()`, not through a DSL method

## References
- **Zone specs:** `world/areas/*.py`
- **Validator:** `world/area_validator.py`
- **Material Registry:** `world/material_definitions.py` — `MATERIAL_REGISTRY` for gathering node validation
- **Gathering Engine:** `world/gathering_engine.py` — `initialize_zone_gathering()` called from `build()`
- **Node system:** `world/zone_object.py` — `initialize_node()`
- **Flight registry:** `world/flight_registry.py`
- **Patrol script:** `world/scripts/patrol_script.py`
- **Tests:** `tests/test_area_builder.py`

---
**Last Updated:** 2026-04-04
