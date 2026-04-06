---
name: node-system
description: Zone node failure state machine — Layer 0/1 room swapping, node types, stabilization, and tick-driven failure progression
---

## Activation

This skill triggers when editing node-system-related files:
- `world/scripts/node_script.py`
- `world/node_helpers.py`
- `world/nodes/node_effects.py`
- `world/zone_object.py`
- `typeclasses/rooms.py`

Keywords: node, layer1, layer0, failure, stabiliz, zone_object, node_effect, node_script

---

You are working on the **node failure system** — a zone-level state machine that transforms rooms when player activity destabilizes a zone.

## Key Files
- `world/scripts/node_script.py` — `NodeScript`: state machine (dormant→awakening→active→critical) driven by failure 0–100
- `world/node_helpers.py` — Global tick (`node_failure_tick`), BFS radius search, zone actor counting, server-start recovery, `break_stabilization_on_move()`
- `world/nodes/node_effects.py` — `NODE_TYPE_TAGS` dict maps 5 node types to room effect tags (interface contract for combat/mob systems)
- `world/zone_object.py` — `initialize_node()`: creates Layer 1 rooms and attaches NodeScript to a ZoneObject
- `typeclasses/rooms.py` — `SoravelonRoom` (L0) and `Layer1Room` (L1, starts tagged `inactive`)

## Key Concepts
- **Failure thresholds:** dormant <30, awakening <60, active <60–90, critical ≥90
- **Layer swap:** At `active` state, players in L0 rooms are `move_to()` into pre-created L1 rooms. Deactivation reverses via `obj.db.layer0_room_id` breadcrumb
- **External tick:** `NodeScript.interval=0` — driven by global `node_failure_tick()` every 30s via TickerHandler, NOT self-ticking
- **Session cap:** Each tick caps failure contribution at 5.0 per session (`db.session_failure_added`), reset on deactivation
- **Node types:** resonance, thermal, cognitive, gravity, temporal — effects are room tags in `node_effect` category
- **BFS radius:** `get_rooms_in_radius()` respects zone boundaries (`zone_id` match only)
- **Stabilization breaks on move:** `Character.at_after_move()` calls `break_stabilization_on_move()` from `world/node_helpers.py` — moving rooms cancels any in-progress node stabilization attempt

## Critical Rules
1. **Never make NodeScript self-ticking** — `interval` must stay 0. The global `node_failure_tick` is the single driver
2. **Node effects are tags, not logic** — other systems read `node_effect` category tags. Don't embed combat/mob logic here
3. **L1 rooms are real DB objects** created at init, toggled via `active`/`inactive` tags in `node_layer` category
4. **Always store `layer0_room_id` on player before `move_to()`** — this is the only way back when L1 deactivates
5. **`initialize_node_pool()` must be idempotent** — called on every server start to recover orphaned active L1 rooms
6. **One NodeScript per zone** — attached to ZoneObject, found via `script_type` tag search, never by scanning all objects
7. **Gravity node type sets `db.action_budget_penalty = -1`** on room — the only type that writes to `db.*` (others are tag-only)

## References
- **Room typeclasses:** `typeclasses/rooms.py`
- **Node effects contract:** `world/nodes/node_effects.py` (`NODE_TYPE_TAGS` dict)
- **Zone init:** `world/zone_object.py` (`initialize_node()`)
- **Character hooks:** `typeclasses/characters.py` — `at_after_move()` calls `break_stabilization_on_move()`

---
**Last Updated:** 2026-04-05
