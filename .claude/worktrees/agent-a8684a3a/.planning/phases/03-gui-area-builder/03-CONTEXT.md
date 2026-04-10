# Phase 3: GUI Area Builder - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 3 in soravelon is SERVER-SIDE ONLY. It delivers the JSON zone schema, server-side JSON loader, cross-zone exit fix, shared validation module, and live-edit hook interfaces. The actual Tauri builder app is a SEPARATE project at `C:\Dev\Evennia\soravelon-builder` with its own GSD project.

**Requirements covered by this phase:**
- BLD-02 (partially — server can load .zone.json files that the builder produces)
- BLD-06 (cross-zone exit two-pass fix)
- BLD-05 (partially — shared validation module enables the builder's validator sidecar)

**Requirements deferred to builder app project:**
- BLD-01 (Tauri app with @xyflow canvas)
- BLD-03 (owner mode)
- BLD-04 (contributor mode — post-v1.0)

</domain>

<decisions>
## Implementation Decisions

### Scope Split
- **D-01:** Phase 3 in soravelon = server-side only. Builder app = separate GSD project at `C:\Dev\Evennia\soravelon-builder`.
- **D-02:** Builder app gets `/gsd:new-project` in its own repo with independent planning.

### JSON Zone Format
- **D-03:** JSON is the CANONICAL zone format. Server loads `.zone.json` natively. `.py` files are generated on export for version control/backup, not the primary loading mechanism.
- **D-04:** JSON schema mirrors AreaBuilder method signatures exactly. JSON has `zone{}`, `rooms[]`, `exits[]`, `spawns[]`, `npcs[]`, `quests[]`, etc. Each maps 1:1 to an AreaBuilder method call. The schema IS the API contract.
- **D-05:** Server-side JSON loader (`load_zone_from_json()`) is a thin adapter that parses JSON and calls AreaBuilder methods. One code path for both .py and .json. Validation, idempotency, cross-zone exits all inherited from AreaBuilder.
- **D-06:** `_load_all_zones()` updated to load both `.py` and `.zone.json` files from `world/areas/`. JSON files processed alongside Python files in sorted order.

### Cross-Zone Exit Fix (BLD-06)
- **D-07:** Two-pass loading. First pass: all zones load normally (some cross-zone exits may fail). Second pass: retry all unresolved cross-zone exits. Currently, `_load_all_zones()` does one pass and silently fails unresolved exits.
- **D-08:** Implementation: after all zone `build()` calls complete, iterate all zones and re-resolve any exits that were added to `_build_warnings` as unresolved. The AreaBuilder needs to track unresolved exits separately from general warnings.

### Shared Validation Module
- **D-09:** Extract validation logic from AreaBuilder into a standalone Python module (`world/area_validator.py`). Both server-side AreaBuilder and the Tauri sidecar import this module. Single source of truth for validation rules.
- **D-10:** Validation module is pure Python with no Django/Evennia dependencies. It validates JSON zone data against the schema and returns structured error objects. AreaBuilder calls into it; sidecar bundles it.

### Live-Edit Hooks
- **D-11:** Phase 3 defines the JSON zone schema + serializer + loader. The actual WebSocket live-edit API is a FUTURE phase. Builder starts offline-first.
- **D-12:** The eventual flow: builder sends JSON over WebSocket → server calls `load_zone_from_json()` → objects created/updated in DB → OOB push to connected players. This requires the same AreaBuilder idempotency that already exists.
- **D-13:** Live-edit will eventually support production for world events and unique quests (owner only). This means the JSON loader must be safe to call on a live server with players connected.

### Builder App Design (for reference — implemented in separate project)
- **D-14:** Strict grid canvas for room placement. Context menu + direction palette for exit creation.
- **D-15:** Right side panel for room properties, with tabs: Properties | Spawns | NPCs | Triggers | Lore.
- **D-16:** Drag-from-palette for quick mob/NPC/item placement + right panel for detailed editing.
- **D-17:** Node visualization: shaded rooms within radius + boundary circle + status badge.
- **D-18:** Patrol route editor: visual waypoint overlay on canvas + patrol config in right panel.
- **D-19:** Flight points are a room flag in the room editor + flight_master mob required.
- **D-20:** Materials and lore fragments are tabs on the room property panel.
- **D-21:** Real-time inline validation (red borders, error panel). Save blocked until resolved.
- **D-22:** Full mob authoring: stats, data-driven abilities (melee/spell type, damage range, cooldown, element, on-hit effects, conditions, combat emote). Custom triggers for boss scripting.
- **D-23:** Full quest authoring: type, objectives, rewards, world expressions, consequences.
- **D-24:** NPC dialogue tree editor: visual branching tree with condition-gated edges.
- **D-25:** Item + loot table editor in v1.0.
- **D-26:** Contributor mode and live-edit staging connection are post-v1.0.

### Claude's Discretion
- JSON schema exact field names and types (must mirror AreaBuilder kwargs)
- Validation error format (structured objects with severity, field path, message)
- Auto-layout fallback algorithm details for zones loaded from JSON without coords
- Two-pass retry mechanism specifics (how unresolved exits are tracked and retried)

</decisions>

<canonical_refs>
## Canonical References

### Cross-Zone Exit Bug
- `world/area_builder.py:_resolve_cross_zone_exits()` — current one-pass resolution with silent warning
- `server/conf/at_server_startstop.py:_load_all_zones()` — single-pass zone loading, no retry

### AreaBuilder Methods (JSON schema source)
- `world/area_builder.py` — zone(), room(), exit(), spawn(), named_mob(), npc(), node(), quest(), material(), lore_fragment(), patrol(), trigger(), custom_command(), flight_point(), flight_route(), mob()

### Validation Constants
- `world/area_builder.py` — VALID_ZONE_TYPES, VALID_CONTINENTS, VALID_NODE_TYPES, VALID_DIRECTIONS, VALID_FACTION_TERRITORIES, AreaBuilderValidationError

### Vault Design Doc
- `C:\Obsidian\brain\Soravelon\soravelon-builder.md` — Full builder design: permission model, reference bundles, mob ability composer fields, validation report format, staging commands

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- AreaBuilder is already idempotent — JSON loader gets this for free by calling AreaBuilder methods
- Validation constants already defined in area_builder.py — extract to shared module
- `_load_all_zones()` already processes sorted file list — extend to include .zone.json

### Integration Points
- `server/conf/at_server_startstop.py:_load_all_zones()` — needs two-pass and .json support
- `world/area_builder.py` — needs to expose unresolved exits for retry mechanism
- New `world/area_validator.py` — extracted validation, no Django deps
- New `world/zone_serializer.py` — JSON→AreaBuilder adapter

</code_context>

<specifics>
## Specific Ideas

- The JSON zone schema should use the same key names as AreaBuilder method kwargs (e.g., `room_id`, `zone_type`, `room_type`). This makes the adapter trivially thin: `area.room(**room_json)`.
- The two-pass cross-zone exit fix could store unresolved exits in a module-level list that `_load_all_zones()` retries after all builds complete.
- The shared validation module should be importable with `python -c "from world.area_validator import validate_zone"` — no Django setup required. This enables the Tauri sidecar to bundle it directly.

</specifics>

<deferred>
## Deferred Ideas

- Tauri builder app scaffolding → separate GSD project
- Canvas interaction, editors, dialogue trees → builder project
- Contributor mode and reference bundles → builder v2.0
- Live-edit WebSocket API → future phase (hooks defined here)
- Staging server setup and commands → future phase
- .py codegen from JSON export → builder project
- Import .py into JSON (AST parsing) → builder project

</deferred>

---

*Phase: 03-gui-area-builder*
*Context gathered: 2026-03-25*
