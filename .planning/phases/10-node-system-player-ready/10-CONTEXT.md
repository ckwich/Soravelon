# Phase 10: Node System Player-Ready - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Make the node system deliver its intended player experience — Layer 1 rooms are navigable with mirrored exits, override descriptions are applied, all 5 node effect types function mechanically, stabilization has proper stamina-based limits, and players receive atmospheric warnings before dimensional shifts.

</domain>

<decisions>
## Implementation Decisions

### Layer 1 Exit Topology
- **D-01:** Mirror L0 exits exactly into L1. Same directions, same connections. Players navigate the shadow dimension with their existing mental map.
- **D-02:** Create exits at build time in `initialize_node()`, not dynamically at activation. Exits exist permanently on L1 rooms (tagged inactive). This allows the game editor to create and edit L1 exits.
- **D-03:** For each L0 exit between two rooms in the node radius, create an equivalent exit between their corresponding L1 rooms. Use the L0→L1 room mapping already stored in `layer0_room.db.layer1_room_id`.

### Layer 1 Override Application
- **D-04:** Apply `layer_1_overrides` (name + desc) from `zone_obj.db.layer_1_overrides` to L1 rooms during `_activate_layer1()`. Restore original names on `_deactivate_layer1()`.
- **D-05:** L1 room descriptions should be the override desc when active, generic "[Node Active]" suffix name when no override exists for that room.

### Node Effect Implementation
- **D-06:** Thermal (wet_suppressed + burn_enhanced): DUAL AXIS — fire damage +30% AND burn DoT ticks for double. Water/ice damage -30% AND wet status application blocked. Checked in `combat_engine.apply_resistance()` and `status_effects.tick_effects()`.
- **D-07:** Cognitive (mob_coordination): Mobs in same room focus the same target instead of splitting. `combat_ai.get_mob_target()` checks for `mob_coordination` tag and copies first mob's target for all mobs in the encounter.
- **D-08:** Temporal (dot_tick_variance): DoT damage rolls 50%-150% of normal per tick instead of flat amount. Same average DPS but unpredictable. Checked in `status_effects.tick_effects()` before applying DoT damage.

### Stabilization Limits
- **D-09:** Stabilization drains stamina over time (5 per tick / 30 seconds). Stops automatically when stamina hits 0.
- **D-10:** Stabilization breaks on combat entry OR room movement. Pure focus mechanic — stand still and commit.
- **D-11:** 5-minute cooldown between stabilization attempts remains (existing CmdStabilize behavior).
- **D-12:** Player gets message when stabilization ends: "Your concentration wavers. The stabilization fades." (stamina) or "Your focus breaks." (combat/movement).

### Player Transition Experience
- **D-13:** Warning messages during awakening stage (30-59% failure). Every tick, players in zone get atmospheric echoes. At ~55% (pre-active threshold), direct warning: "The dimensional barrier is weakening. Prepare yourself."
- **D-14:** The atmospheric changes during awakening ARE the primary warning. Players who use `sense` or pay attention to room descriptions can anticipate the shift.

### Claude's Discretion
- Exact atmospheric warning message text during awakening ticks
- How L1 room names display when no override exists (e.g., "[Distorted] room_name" vs "room_name [Node Active]")
- Whether to apply node_state tags to L1 rooms as well as L0 (recommended: yes, for consistency)
- Stamina drain rate tuning (5/tick suggested, planner can adjust)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Node System Core
- `world/scripts/node_script.py` — NodeScript state machine, _activate_layer1(), _deactivate_layer1(), receive_tick()
- `world/zone_object.py` — initialize_node() creates L1 rooms and NodeScript
- `world/node_helpers.py` — node_failure_tick(), get_rooms_in_radius(), attempt_stabilization(), stop_stabilization(), count_zone_actors()
- `world/nodes/node_effects.py` — NODE_TYPE_TAGS, apply_node_effects(), remove_node_effects()
- `world/node_commands.py` — CmdStabilize

### Combat Integration (for node effects)
- `world/combat_engine.py` — apply_resistance() for thermal damage modifiers
- `world/combat_ai.py` — get_mob_target() for cognitive coordination
- `world/status_effects.py` — tick_effects() for thermal DoT and temporal variance

### Content (Cantera Edge overrides)
- `world/areas/cantera_edge.py` — area.node() call with layer_1_overrides dict (~24 rooms)

### Rooms
- `typeclasses/rooms.py` — SoravelonRoom, Layer1Room, get_display_desc()

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `initialize_node()` already creates L1 rooms and links them via `layer0_room.db.layer1_room_id` — exits just need to mirror this mapping
- `get_rooms_in_radius()` BFS already used by _activate/_deactivate — same function for finding affected rooms
- `apply_node_effects()` / `remove_node_effects()` already handle tag application — just need consumers
- `_activate_layer1()` already teleports players — just needs override application added

### Established Patterns
- Tags as contracts: node effects set tags, combat/AI/status systems check them
- Room tags use category-based namespacing (node_state, node_effect, node_layer)
- Stabilization tracked on ndb.stabilizing_zones (volatile, per-session)

### Integration Points
- `world/zone_object.py:initialize_node()` — add exit cloning here
- `world/scripts/node_script.py:_activate_layer1()` — add override application here
- `world/scripts/node_script.py:_on_state_transition()` — add awakening warnings here
- `world/combat_engine.py:apply_resistance()` — add thermal modifier check
- `world/combat_ai.py:get_mob_target()` — add coordination check
- `world/status_effects.py:tick_effects()` — add thermal DoT and temporal variance

</code_context>

<specifics>
## Specific Ideas

- Exit cloning in initialize_node(): iterate L0 rooms, for each exit where both source and destination have L1 counterparts, create_object(SoravelonExit) linking L1 source → L1 destination with same key/direction
- Override application: read zone_obj.db.layer_1_overrides dict, key is room_id string, value is {name, desc}. Match against L0 room tags to find the corresponding L1 room.
- Stamina drain: modify count_zone_actors() or create a separate stabilization tick that checks ndb.stamina and calls stop_stabilization() when depleted

</specifics>

<deferred>
## Deferred Ideas

- Node system for zones beyond Cantera Edge — future content phases
- L1-specific mob spawns (node_active spawn_condition mobs exist but L1 spawn wiring is content, not engine work)
- Distorted exit topology (D-01 chose mirror; distortion could be a future node type or critical-state feature)

</deferred>

---

*Phase: 10-node-system-player-ready*
*Context gathered: 2026-04-02*
