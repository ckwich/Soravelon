---
phase: 02-oob-push-and-desktop-client
plan: "01"
subsystem: oob-publisher
tags: [oob, websocket, map, fog-of-war, debounce]
dependency_graph:
  requires:
    - world/world_state.py (get_character_context_packet)
    - world/inventory_helpers.py (get_carry_state)
    - world/group_engine.py (get_group_state)
    - typeclasses/characters.py (existing hooks)
  provides:
    - world/oob_publisher.py (8 push_* functions + debounce gate)
    - character.db.visited_room_ids (fog-of-war tracking)
    - character.ndb.oob_debounce (debounce timestamps)
    - at_after_move hook (map_update trigger on movement)
    - at_post_puppet OOB init (full initial state on login)
  affects:
    - typeclasses/characters.py (3 changes)
tech_stack:
  added: []
  patterns:
    - "OOB via character.msg(**{msg_type: data}) — Evennia native WebSocket JSON array protocol"
    - "Debounce via ndb timestamps (time.monotonic) — ndb resets naturally on disconnect"
    - "SaverDict copy pattern for ndb dict mutations"
    - "Lazy imports inside all push_* functions to prevent circular imports"
    - "evennia.search_tag + typeclass_path filter for zone room enumeration (Pitfall 3)"
key_files:
  created:
    - world/oob_publisher.py
  modified:
    - typeclasses/characters.py
decisions:
  - "Used get_character_context_packet keys (reputation/network/bond/legacy/attunement) directly — not *_score suffixed keys, as the function returns renamed fields"
  - "push_inventory_update items list is an intentional stub (empty []) — full item query deferred to Phase 6 per plan spec"
  - "at_after_move placed before at_before_move in class body per plan spec"
  - "fog_of_war reads room.db.fog_of_war (not zone_obj.db.fog_of_war) — aligns with map_update assembly from current room context"
metrics:
  duration: "2 minutes"
  completed_date: "2026-03-25"
  tasks_completed: 2
  files_changed: 2
---

# Phase 02 Plan 01: OOB Publisher Hub Summary

OOB publisher hub with Evennia-native WebSocket OOB dispatch, debounce gate via ndb timestamps, all 8 typed message types, and character typeclass wiring for login push and movement-triggered map updates.

## Tasks Completed

| # | Name | Commit | Files |
|---|------|--------|-------|
| 1 | Create world/oob_publisher.py — all 8 message types with debounce | 3c2a1d6 | world/oob_publisher.py (new) |
| 2 | Wire OOB hooks into typeclasses/characters.py | ff45647 | typeclasses/characters.py |

## What Was Built

### world/oob_publisher.py (new)

Single OOB hub module. All 8 message types defined:

- `push_status_update` — dimensions (reputation/network/bond/legacy/attunement), domain_scores, carried_scales, companion info
- `push_stat_update` — HP/conditions placeholder (Phase 6 populates)
- `push_map_update` — full zone room graph: room_id, name, grid_x/y, room_type, node_state, exits (with cross_zone flag), visited flag, group markers
- `push_node_event` — zone state transition (no debounce)
- `push_flight_progress` — leg_index, total_legs, destination_name, disembark_available
- `push_combat_update` — passthrough placeholder
- `push_quest_update` — passthrough placeholder
- `push_inventory_update` — encumbrance state live; items list stub

Internal helpers:
- `_should_send(character, msg_type)` — checks ndb debounce timestamps
- `_mark_sent(character, msg_type)` — SaverDict copy pattern write-back
- `_send(character, msg_type, data)` — session guard + debounce gate + msg dispatch
- `_get_group_positions(character)` — group member room_id markers for same zone

`DEBOUNCE_INTERVALS` constant with all 8 types.

### typeclasses/characters.py (3 changes)

1. `at_object_creation`: `self.db.visited_room_ids = set()` for fog-of-war tracking
2. `at_post_puppet`: `self.ndb.oob_debounce = {}` init + 4 push calls (status, stat, map, inventory)
3. `at_after_move` (new method): tracks visited rooms via room_id tags, pushes map_update unless `ndb.in_flight`

## Deviations from Plan

### Minor Adjustment

**get_character_context_packet key names**
- **Found during:** Task 1 implementation
- **Issue:** Plan's action block referenced `packet.get("reputation_score")` style keys, but `get_character_context_packet` returns `"reputation"`, `"network"`, etc. (without `_score` suffix) — the function renames the fields.
- **Fix:** Used `packet.get("reputation")` etc. directly, matching the function's actual return contract.
- **Files modified:** world/oob_publisher.py
- **Commit:** 3c2a1d6

## Known Stubs

| Stub | File | Reason |
|------|------|--------|
| `"items": []` in push_inventory_update | world/oob_publisher.py:258 | Full item enumeration via inventory_engine deferred to Phase 6 per plan spec (D-03 schema live, data TBD) |
| `{"hp": None, "hp_max": None, "conditions": []}` in push_stat_update | world/oob_publisher.py:152 | Combat system (HP/resources) deferred to Phase 6 — schema is live so client can wire the message type now |

These stubs are intentional per plan spec. Phase 6 (combat system) will populate both.

## Self-Check: PASSED

- world/oob_publisher.py: FOUND
- typeclasses/characters.py: FOUND (3 changes verified)
- Commit 3c2a1d6: FOUND
- Commit ff45647: FOUND
- All 8 push_* functions defined in oob_publisher.py: VERIFIED
- DEBOUNCE_INTERVALS with 8 keys: VERIFIED
- visited_room_ids in at_object_creation: VERIFIED (line 74)
- visited_room_ids in at_after_move: VERIFIED (lines 122, 125)
- oob_debounce init in at_post_puppet: VERIFIED (line 96)
- 4 push calls in at_post_puppet: VERIFIED (lines 99-102)
- at_after_move method present: VERIFIED (lines 115-130)
- push_map_update guarded by ndb.in_flight: VERIFIED (line 127)
