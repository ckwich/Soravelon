---
name: group-system
description: Session-only party system with invite flow, leadership transfer, loot modes, and zone proximity queries
---

## Activation

This skill triggers when editing these files:
- `world/group_engine.py`
- `tests/test_group_engine.py`
- `commands/*group*`

Keywords: group, party, invite, loot mode, group engine, kick, leadership

---

You are working on **the group/party system** in soravelon.

## Key Files
- `world/group_engine.py` — All group logic (formation, loot, proximity)
- `tests/test_group_engine.py` — 17 test classes using `EvenniaTest` + `GroupTestBase`
- `typeclasses/characters.py` — Calls `on_member_disconnect()` in `at_pre_unpuppet()`

## Key Concepts
- **Session-only state:** Groups live entirely in `ndb` (volatile). No Django models. Groups dissolve on disconnect.
- **Leader-centric storage:** `group_state` dict lives on `leader.ndb`; members only store `ndb.group_leader_id` pointing to leader's `.id`.
- **Leadership transfer:** When leader leaves, `_transfer_leadership_internal()` moves `group_state` to next member and updates all `group_leader_id` refs.
- **Invite flow:** `send_group_invite` → stores `target.ndb.pending_group_invite` → `accept_group_invite` creates group on first accept (lazy creation).
- **Loot modes:** `personal` (default), `ffa`, `round_robin`, `need_pass`. Quest drops and Scales are ALWAYS personal regardless of mode.
- **Proximity via BFS:** `get_members_in_proximity()` imports `node_helpers.get_rooms_in_radius()` for same-zone BFS traversal (default radius=3).

## Critical Rules
1. **All functions return `(bool, str)` tuples** — follows repo-wide convention
2. **Max 6 members** — `MAX_GROUP_SIZE = 6`, enforced at both invite and accept
3. **SaverDict copy pattern required** — `ndb.group_state` is a SaverDict; read→mutate→reassign (e.g., `state["members"].append(id); leader.ndb.group_state = state`)
4. **Member validation on every read** — `_get_group_members()` prunes stale IDs (disconnected players) automatically
5. **Disconnect cleanup is mandatory** — `on_member_disconnect()` must be called from `at_pre_unpuppet()`; forgetting this leaks ghost members
6. **Zone queries need `room.db.zone_id`** — `get_members_in_zone()` checks member locations against zone_id string

## References
- **Node/BFS helpers:** `world/node_helpers.py`
- **Character hooks:** `typeclasses/characters.py`

---
**Last Updated:** 2026-03-23
