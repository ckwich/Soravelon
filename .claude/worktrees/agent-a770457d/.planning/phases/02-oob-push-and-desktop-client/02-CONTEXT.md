# Phase 2: OOB Push and Desktop Client - Context

**Gathered:** 2026-03-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the server-side OOB publisher module, room coordinate system with auto-layout fallback, zone world-map coordinates, and fog-of-war support. This phase is SERVER-SIDE ONLY — the Tauri desktop client is a separate project/phase (2.1). The OOB publisher defines the typed contract that any client consumes.

**Scope reduction from original roadmap:** CLI-01 through CLI-05 (Tauri client) are deferred to Phase 2.1 (separate repo). Phase 2 delivers CLI-06 (OOB publisher) and CLI-07 (room coordinates) plus the full message catalog, map data model, and auto-layout system.

</domain>

<decisions>
## Implementation Decisions

### Repo Scope
- **D-01:** Phase 2 is server-side only (OOB publisher + room coords + map data). The Tauri desktop client is a SEPARATE project bootstrapped in Phase 2.1.
- **D-02:** Tauri client repo does not exist yet — creation deferred to Phase 2.1.

### OOB Message Catalog
- **D-03:** Full comprehensive OOB catalog from day one — not minimal. The client should be as verbose and rich as the player wants.
- **D-04:** Message types: `status_update` (dimensions, domains, carried_scales, companion), `map_update` (zone graph, room position, exits, player marker), `node_event` (state transitions, zone-wide), `flight_progress` (leg timing, disembark availability), `combat_update` (HP, abilities, cooldowns, targets), `quest_update` (active quests, progress, objectives), `inventory_update` (items, equipment, encumbrance), `stat_update` (HP/resource bars, conditions).
- **D-05:** Auto-push on every change. No client subscription model. Client receives everything, renders what it wants, ignores the rest.
- **D-06:** Debounce per message type. Each type has a configurable minimum interval (e.g., combat_update max 4/sec, inventory_update max 1/sec). Last-value-wins during debounce window.

### Map Panel Data Model
- **D-07:** Room coordinates are zone-local with a world-level overlay. Each zone has its own (0,0) origin for room positions. Zones themselves have world-level positions for the world map.
- **D-08:** Server computes room layout (auto-layout fallback for zones without hand-placed coords). NO client-side layout computation — player client is a thin renderer.
- **D-09:** Auto-layout uses BFS-based grid algorithm on zone load for rooms without explicit coords. Builder-placed coords (from GUI builder, Phase 3) override auto-layout.
- **D-10:** Zone world positions stored on `zone_obj.db.world_x`, `zone_obj.db.world_y`, `zone_obj.db.world_radius`. Set by builder/admin.
- **D-11:** Fog of war is configurable per zone via `zone_obj.db.fog_of_war` boolean. Cities = no fog (full zone visible). Dungeons = fog (only visited rooms shown). Default: no fog.
- **D-12:** Room types have distinct icon + color per type on the map. Server sends `room_type` in `map_update`. Client maintains an icon registry keyed by room_type.

### Map Visual Features
- **D-13:** Node failure shown as color tint on affected rooms (green→yellow→orange→red) + boundary circle around node radius + status badge (Healthy/Stressed/Failing/Collapsed).
- **D-14:** Group members shown as small dot icons on the zone map. No strangers visible — group members only.
- **D-15:** Cross-zone exits shown as edge-of-map arrows with destination zone name label.

### WebSocket Protocol
- **D-16:** Use Evennia's native WebSocket protocol (built-in webclient). OOB messages sent via `character.msg(oob_type=data)`. Client parses Evennia's JSON array protocol `["cmdname", [args], {kwargs}]`.
- **D-17:** Mock client in tests — verify OOB messages using `character.msg()` call assertions. No real WebSocket in Phase 2 tests.

### Claude's Discretion
- Debounce interval values per message type (exact milliseconds)
- Auto-layout algorithm choice (BFS grid vs force-directed)
- OOB message JSON schema field names
- Room coordinate scale (integers, floats, pixel units)

</decisions>

<canonical_refs>
## Canonical References

### OOB / WebSocket
- Evennia webclient source: `evennia/server/portal/webclient.py` — JSON array protocol format
- `character.msg()` — Evennia's message routing to connected sessions
- `world/world_state.py:get_character_context_packet()` — existing status data aggregation (status_update source)

### Map Data
- `world/area_builder.py` — room creation, zone metadata, existing tag system
- `world/zone_registry.py` — zone lookup for world map
- `world/node_helpers.py:get_rooms_in_radius()` — BFS pattern reusable for auto-layout
- `typeclasses/rooms.py` — SoravelonRoom with zone_id, room_type tags

### Existing State Providers
- `world/world_state.py` — dimension scores, domain scores (status_update)
- `world/inventory_engine.py` — inventory state (inventory_update)
- `world/banking.py` — balance (stat_update)
- `world/scripts/node_script.py` — node state transitions (node_event)
- `world/scripts/flight_script.py` — flight leg progress (flight_progress)
- `world/group_engine.py` — group membership (map player markers)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `get_character_context_packet()` already aggregates most of `status_update` data
- `get_rooms_in_radius()` BFS can be adapted for auto-layout grid computation
- Zone registry + tag system provides all data needed for `map_update`
- NodeScript already tracks failure state — just needs to publish OOB on state change

### Integration Points
- Every system that mutates visible state needs an OOB publish call added
- `typeclasses/characters.py` hooks (puppet, unpuppet, move) are natural trigger points for `map_update`
- `world/scripts/node_script.py:at_repeat()` should publish `node_event` on state transitions
- `world/scripts/flight_script.py` should publish `flight_progress` on leg start/arrival

</code_context>

<deferred>
## Deferred Ideas

- CLI-01 through CLI-05 (Tauri client) → Phase 2.1 (separate project/repo)
- Combat OOB field details → Phase 6 when combat system is built (schema defined now, populated then)
- Quest OOB field details → when quest system is built (schema defined now, populated then)
- World map interactive features (click zone to zoom) → client-side Phase 2.1

</deferred>

---

*Phase: 02-oob-push-and-desktop-client*
*Context gathered: 2026-03-24*
