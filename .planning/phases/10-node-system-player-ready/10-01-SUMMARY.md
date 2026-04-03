---
phase: 10-node-system-player-ready
plan: 01
subsystem: node-system
tags: [node, layer1, exits, overrides, zone-object]
dependency_graph:
  requires: [initialize_node, NodeScript, SoravelonExit, Layer1Room]
  provides: [L1 exit topology, L1 override application, L1 exit activation]
  affects: [world/zone_object.py, world/scripts/node_script.py]
tech_stack:
  added: []
  patterns: [two-pass initialization, tag-based activation toggle]
key_files:
  created: []
  modified:
    - world/zone_object.py
    - world/scripts/node_script.py
decisions:
  - L1 exits created at build time in initialize_node(), tagged inactive until node activates (D-02)
  - Override lookup uses layer0_room.db.room_id falling back to layer0_room.key as dict key
  - State tags (_apply_state_tags/_remove_state_tags) extended to L1 rooms for consistency
metrics:
  duration_minutes: 3
  completed: "2026-04-03T17:54:00Z"
  tasks: 2
  files_modified: 2
---

# Phase 10 Plan 01: L1 Exit Topology and Override Application Summary

L1 rooms become navigable via cloned exit topology and display zone-specific override names/descriptions during node activation.

## What Was Done

### Task 1: Clone L0 exits into L1 rooms in initialize_node()
- Added `l0_to_l1` mapping dict built during L1 room creation pass
- Second pass iterates all L0 rooms, clones each exit where both source and destination have L1 counterparts (D-03)
- L1 exits created as SoravelonExit objects with `inactive` node_layer tag and zone_id tag
- Exits exist permanently on L1 rooms, toggled active/inactive by NodeScript

### Task 2: Apply and restore L1 overrides during activation/deactivation
- `_activate_layer1()` reads `layer_1_overrides` from zone_obj, applies name+desc per room
- Rooms without overrides get `[Distorted] original_name` prefix (D-05)
- Original names stored in `db.original_name` for restoration on deactivation
- L1 exits in each room toggled from inactive to active during activation, reversed on deactivation
- `_apply_state_tags` and `_remove_state_tags` extended to also tag L1 rooms (consistency)

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| 1 | 65fd09e | Clone L0 exit topology into L1 rooms at node initialization |
| 2 | 3d68144 | Apply L1 override names/descriptions and toggle exits on activation |

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None. All functionality is fully wired.
