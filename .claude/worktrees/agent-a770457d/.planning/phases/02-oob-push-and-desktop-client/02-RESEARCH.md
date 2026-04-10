# Phase 2: OOB Push and Desktop Client — Research

**Researched:** 2026-03-24
**Domain:** Evennia OOB protocol, server-side map data, BFS auto-layout, debounce
**Confidence:** HIGH (verified from Evennia source + existing project code)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**D-01:** Phase 2 is server-side only (OOB publisher + room coords + map data). Tauri client deferred to Phase 2.1.
**D-02:** Tauri client repo does not exist — creation deferred to Phase 2.1.
**D-03:** Full comprehensive OOB catalog from day one — not minimal.
**D-04:** Message types: `status_update`, `map_update`, `node_event`, `flight_progress`, `combat_update`, `quest_update`, `inventory_update`, `stat_update`.
**D-05:** Auto-push on every change. No client subscription model. Client receives everything, ignores what it wants.
**D-06:** Debounce per message type. Each type has configurable minimum interval. Last-value-wins during debounce window.
**D-07:** Room coordinates are zone-local with world-level overlay. Each zone has its own (0,0) origin. Zones have world-level positions for world map.
**D-08:** Server computes room layout. NO client-side layout computation. Client is a thin renderer.
**D-09:** Auto-layout uses BFS-based grid algorithm on zone load for rooms without explicit coords. Builder-placed coords override auto-layout.
**D-10:** Zone world positions stored on `zone_obj.db.world_x`, `zone_obj.db.world_y`, `zone_obj.db.world_radius`. Set by builder/admin.
**D-11:** Fog of war configurable per zone via `zone_obj.db.fog_of_war` boolean. Cities = no fog. Dungeons = fog (only visited rooms). Default: no fog.
**D-12:** Room types have distinct icon + color on map. Server sends `room_type` in `map_update`. Client maintains icon registry keyed by room_type.
**D-13:** Node failure shown as color tint on affected rooms (green→yellow→orange→red) + boundary circle + status badge.
**D-14:** Group members shown as small dot icons on zone map. No strangers — group members only.
**D-15:** Cross-zone exits shown as edge-of-map arrows with destination zone name label.
**D-16:** Use Evennia's native WebSocket protocol (built-in webclient). OOB messages sent via `character.msg(oob_type=data)`. Client parses Evennia's JSON array protocol `["cmdname", [args], {kwargs}]`.
**D-17:** Mock client in tests — verify OOB messages using `character.msg()` call assertions. No real WebSocket in Phase 2 tests.

### Claude's Discretion

- Debounce interval values per message type (exact milliseconds)
- Auto-layout algorithm choice (BFS grid vs force-directed)
- OOB message JSON schema field names
- Room coordinate scale (integers, floats, pixel units)

### Deferred Ideas (OUT OF SCOPE)

- CLI-01 through CLI-05 (Tauri client) → Phase 2.1 (separate project/repo)
- Combat OOB field details → Phase 6 when combat system is built (schema defined now, populated then)
- Quest OOB field details → when quest system is built (schema defined now, populated then)
- World map interactive features (click zone to zoom) → client-side Phase 2.1
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CLI-06 | OOB publisher module provides typed contract for all server→client push data | Evennia `character.msg(**kwargs)` routes arbitrary kwargs as OOB via `send_default`. `world/oob_publisher.py` is the right location. Debounce via `ndb` timestamps. |
| CLI-07 | Room coordinates stored in AreaBuilder for map rendering | `_set_room_attrs()` in AreaBuilder already sets all room db attrs. Add `grid_x`, `grid_y` to that set. Auto-layout BFS fills gaps. Zone world coords on `zone_obj.db.*`. |
</phase_requirements>

---

## Summary

Phase 2 delivers the server-side OOB infrastructure: a typed publisher module (`world/oob_publisher.py`) and a coordinate system grafted onto existing rooms and zones. The Tauri client is explicitly out of scope.

**The Evennia OOB mechanism is simpler than it looks.** Calling `character.msg(status_update={"key": "val"})` is all that is needed. Evennia routes any kwarg that is not `text` or `options` through `send_default()` on the WebSocket session, which emits `["status_update", [], {"key": "val"}]` as JSON. The webclient (and any future Tauri client) receives this array and dispatches on the first element. No custom protocol code, no GMCP, no MSDP — the native Evennia WebSocket already supports arbitrary OOB commands out of the box.

**The map data model is a two-level coordinate system.** Zone-local coords (`room.db.grid_x`, `room.db.grid_y`) are computed by the BFS auto-layout algorithm at zone load time (unless a builder has placed explicit coords). World-level coords (`zone_obj.db.world_x`, `zone_obj.db.world_y`, `zone_obj.db.world_radius`) are set manually by the admin/builder. Both levels are stored on Evennia `db` attributes and pushed to the client in `map_update`.

**Debounce lives in `ndb`.** Each character holds a dict `ndb.oob_debounce` mapping message type → last-sent timestamp. The publisher checks elapsed time before each send. `ndb` is volatile (resets on disconnect), which is correct: debounce windows that span disconnects are irrelevant.

**Primary recommendation:** Build `world/oob_publisher.py` as the single OOB hub. All game systems import and call it. It owns debounce, message assembly, and the send call. Never call `character.msg()` directly for OOB from game logic.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Evennia (installed) | 6.0.0 | `character.msg(**kwargs)` → OOB dispatch | Native WebSocket JSON array protocol, no extra dependencies |
| `evennia.utils.utils.delay` | 6.0.0 | Twisted-safe async timer | Same pattern used by `FlightScript` — proven in codebase |
| Django ORM | 6.0.3 | `room.db.*` / `zone_obj.db.*` attribute storage | Project standard for persistent state |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `collections.deque` (stdlib) | 3.12 | BFS frontier queue in auto-layout | Faster than list for popleft |
| `time.monotonic` (stdlib) | 3.12 | Debounce timestamp comparison | No drift, no tzinfo complexity |
| `unittest.mock.MagicMock` | 3.12 | Mock `character.msg` in tests | Standard for pure-logic module testing in this project |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `ndb` debounce timestamps | Script-based timer | ndb is simpler, no script lifecycle to manage |
| BFS grid auto-layout | Force-directed layout | BFS grid is deterministic (reproducible coords), force-directed needs physics loop |
| `character.msg(**kwargs)` | Custom GMCP/MSDP | Native path requires zero protocol code; GMCP/MSDP is Telnet-specific and adds complexity |

**Installation:** No new packages required. All dependencies are already present in the Evennia + Python 3.12 environment.

---

## Architecture Patterns

### Recommended Project Structure

```
world/
├── oob_publisher.py          # OOB hub — assemble and send all message types
world/scripts/
├── (no new scripts needed)   # Debounce is ndb-based, not script-based
typeclasses/
├── characters.py             # Add at_after_move() hook for map_update trigger
tests/
├── test_oob_publisher.py     # unittest.TestCase with MagicMock msg
```

Coordinate storage is grafted directly onto existing room and zone objects via `db` attributes — no new models, no new files for coords alone.

### Pattern 1: Evennia OOB Send Mechanism

**What:** Any kwarg passed to `character.msg()` that is not `text` or `options` becomes an OOB command. The WebSocket session calls `send_default(cmdname, *args, **kwargs)` which emits `["cmdname", [], {data}]` as JSON.

**When to use:** Every OOB push in the publisher calls this.

```python
# Source: evennia/server/portal/webclient.py:325, evennia/objects/objects.py:970
# character.msg() → session.data_out(**kwargs) → send_default(cmdname, ...)
# Wire format: ["status_update", [], {"dimensions": {...}, "domains": {...}}]

def push_status_update(character, data):
    character.msg(status_update=data)

# Multi-message: all kwargs are sent as separate OOB commands in one call
character.msg(status_update=status_data, stat_update=stat_data)
```

**Key verified fact (HIGH confidence):** The `WebSocketClient.protocol_flags["OOB"] = True` is set in `onOpen()`. The `send_default` method fires for any kwarg not named `text` or `options`. The wire format is `json.dumps([cmdname, args, kwargs])` where cmdname is the kwarg key and the data value flows through as kwargs.

### Pattern 2: Debounce via `ndb` Timestamps

**What:** Per-character, per-message-type last-sent timestamp stored in `ndb`. Publisher checks elapsed time before sending. Last value queued during the window replaces the prior pending value; the queued value fires after the window expires.

**When to use:** Every OOB push goes through the debounce gate in `oob_publisher.py`.

```python
# Source: project pattern (ndb usage in typeclasses/characters.py)
import time

# Debounce intervals per message type (Claude's Discretion — recommended values)
DEBOUNCE_INTERVALS = {
    "status_update":    2.0,   # 0.5/sec — low-frequency state
    "map_update":       0.5,   # 2/sec — room movement
    "node_event":       0.0,   # no debounce — state transitions are infrequent
    "flight_progress":  1.0,   # 1/sec during flight
    "combat_update":    0.25,  # 4/sec max — D-06 explicit
    "quest_update":     5.0,   # low frequency
    "inventory_update": 1.0,   # 1/sec max — D-06 explicit
    "stat_update":      0.5,   # HP bars
}

def _should_send(character, msg_type):
    """Returns True if the debounce window for this message type has passed."""
    debounce = character.ndb.oob_debounce or {}
    interval = DEBOUNCE_INTERVALS.get(msg_type, 1.0)
    if interval <= 0:
        return True
    last_sent = debounce.get(msg_type, 0.0)
    return (time.monotonic() - last_sent) >= interval

def _mark_sent(character, msg_type):
    debounce = dict(character.ndb.oob_debounce or {})
    debounce[msg_type] = time.monotonic()
    character.ndb.oob_debounce = debounce
```

**Recommended debounce values (Claude's Discretion):**
- `combat_update`: 0.25s (4/sec max, per D-06)
- `inventory_update`: 1.0s (1/sec max, per D-06)
- `map_update`: 0.5s (room movement bursts during flight)
- `status_update`: 2.0s (dimension/domain scores change slowly)
- `node_event`: 0.0s (no debounce — state transitions are rare, must not be dropped)
- `flight_progress`: 1.0s
- `stat_update`: 0.5s
- `quest_update`: 5.0s

### Pattern 3: BFS Grid Auto-Layout

**What:** Assign integer grid coordinates to all rooms in a zone using BFS from an arbitrary start room. Coords are zone-local integers; the client scales to pixels. This is the same BFS pattern used by `node_helpers.get_rooms_in_radius()`.

**When to use:** `build()` in AreaBuilder, after all rooms and exits are created, for any room without explicit `grid_x`/`grid_y`.

```python
# Source: adapted from world/node_helpers.py:get_rooms_in_radius()
from collections import deque

DIRECTION_OFFSETS = {
    "north":     (0,  1),
    "south":     (0, -1),
    "east":      (1,  0),
    "west":      (-1, 0),
    "northeast": (1,  1),
    "northwest": (-1, 1),
    "southeast": (1, -1),
    "southwest": (-1,-1),
    "up":        (0,  0),  # same cell, different layer — no 2D offset
    "down":      (0,  0),
    "in":        (0,  0),
    "out":       (0,  0),
}

def auto_layout_zone(rooms_dict):
    """
    Assign grid_x, grid_y to rooms without explicit coords.
    rooms_dict: {room_id: room_obj}
    Does NOT overwrite rooms where db.grid_x is already set.
    """
    # Pick first room as origin
    room_list = list(rooms_dict.values())
    if not room_list:
        return

    # Find a root: prefer one with no exits going "south/west" to anchor top-left
    root = room_list[0]
    if root.db.grid_x is not None:
        return  # all coords already set by builder; skip auto-layout

    occupied = {}   # (x, y) -> room_obj
    queue = deque()
    root.db.grid_x = 0
    root.db.grid_y = 0
    occupied[(0, 0)] = root
    queue.append((root, 0, 0))

    while queue:
        room, cx, cy = queue.popleft()
        for exit_obj in room.exits:
            dest = exit_obj.destination
            if not dest or dest.db.grid_x is not None:
                continue
            dx, dy = DIRECTION_OFFSETS.get(exit_obj.key, (0, 0))
            nx, ny = cx + dx, cy + dy
            # Collision: nudge until free
            while (nx, ny) in occupied:
                nx += 1
            dest.db.grid_x = nx
            dest.db.grid_y = ny
            occupied[(nx, ny)] = dest
            queue.append((dest, nx, ny))
```

**Coordinate scale recommendation (Claude's Discretion):** Use integer grid units. Each unit = 1 cell. The client multiplies by a pixel scale factor it controls. This keeps server data simple and lets the client zoom freely.

### Pattern 4: Map Update Assembly

**What:** When a character moves (or the zone state changes), assemble and push `map_update`. This is the largest message — contains full zone graph, not just current room.

```python
# Source: world/zone_registry.py, world/node_helpers.py, typeclasses/rooms.py
def build_map_update(character):
    """
    Build the map_update payload for the character's current zone.
    Returns dict suitable for character.msg(map_update=...).
    """
    room = character.location
    if not room:
        return None
    zone_id = room.db.zone_id

    # Collect all rooms in zone via tag search
    import evennia
    zone_rooms = evennia.search_tag(zone_id, category="zone_id")

    rooms_data = []
    for r in zone_rooms:
        if not hasattr(r, "exits"):  # skip non-rooms (exits, zone objects)
            continue
        rooms_data.append({
            "room_id": r.tags.get("room_id", category="room_id"),
            "name": r.key,
            "x": r.db.grid_x,
            "y": r.db.grid_y,
            "room_type": r.db.room_type or "generic",
            "node_state": r.tags.get(category="node_state"),
            "exits": [
                {
                    "direction": ex.key,
                    "destination_zone": ex.destination.db.zone_id if ex.destination else None,
                    "cross_zone": (ex.destination.db.zone_id != zone_id) if ex.destination else False,
                }
                for ex in r.exits
            ],
            "visited": _room_visited(character, r),
        })

    # Group member positions
    group_positions = _get_group_positions(character)

    return {
        "zone_id": zone_id,
        "player_room_id": room.tags.get("room_id", category="room_id"),
        "fog_of_war": bool(character.location.db.fog_of_war
                          if hasattr(character.location, "db") else False),
        "rooms": rooms_data,
        "group_markers": group_positions,
    }
```

### Pattern 5: Integration Hook Placement

The following existing locations need a single `oob_publisher.push_X(character)` call added — no structural changes required:

| Location | Event | OOB message |
|----------|-------|-------------|
| `typeclasses/characters.py:at_after_move()` | room change | `map_update`, `node_event` (if node zone) |
| `typeclasses/characters.py:at_post_puppet()` | login | all 8 message types (full initial state) |
| `world/scripts/node_script.py:_on_state_transition()` | state change | `node_event` for all players in zone |
| `world/scripts/flight_script.py:_begin_leg()` | leg start | `flight_progress` |
| `world/scripts/flight_script.py:_arrive_at_stop()` | leg arrival | `flight_progress`, `map_update` |
| `world/scripts/flight_script.py:_arrive_final()` | landing | `flight_progress`, `map_update` |
| `world/world_state.py:commit_session_xp()` | XP commit | `status_update` |

### Anti-Patterns to Avoid

- **Direct `character.msg(status_update=...)` in game logic modules:** All OOB pushes must route through `oob_publisher.py`. Never scatter OOB calls across banking.py, inventory_engine.py, etc.
- **Storing debounce in `db` (persisted):** `db` persists across disconnects. Use `ndb` — debounce windows that span disconnects are meaningless and `ndb` resets naturally.
- **Sending `map_update` on every tick:** Map update should only fire on: move, zone state change, or explicit request. Not on every node tick.
- **Computing layout on every `map_update` send:** Auto-layout runs once during `build()` and stores coords. `map_update` reads stored `grid_x`/`grid_y` — never recomputes.
- **Cross-zone room inclusion in `map_update`:** Only rooms in the current zone are sent. Cross-zone exits are indicated with `cross_zone: true` + destination zone name, not the destination rooms.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| WebSocket OOB dispatch | Custom protocol layer | `character.msg(**kwargs)` | Already routed by Evennia's session layer; `send_default` handles any kwarg key |
| Async timers for debounce | `time.sleep()` or Twisted `LoopingCall` | `ndb` timestamps + check-on-push | Twisted is single-threaded; sleep blocks; LoopingCall adds unnecessary lifecycle management for what is a simple gate check |
| Zone room enumeration | Custom DB query | `evennia.search_tag(zone_id, category="zone_id")` | Already the pattern for zone-scoped lookups in `node_helpers.py` |
| BFS traversal | Custom graph library | Adapt `node_helpers.get_rooms_in_radius()` | Already proven, same zone-scoping logic needed |

**Key insight:** The Evennia OOB protocol requires no custom infrastructure. The `character.msg(**kwargs)` path already terminates in `send_default()` which emits any kwarg as a JSON array OOB command. The only new code is the message assembly and debounce logic.

---

## Common Pitfalls

### Pitfall 1: `ndb` Attribute Init

**What goes wrong:** `character.ndb.oob_debounce` is `None` on first access (not an empty dict). Code that does `character.ndb.oob_debounce["key"]` raises `TypeError`.

**Why it happens:** Evennia `ndb` returns `None` for any unset attribute, never raising `AttributeError`.

**How to avoid:** Always access with `character.ndb.oob_debounce or {}`. Initialize to `{}` at `at_post_puppet()` time.

**Warning signs:** `TypeError: 'NoneType' object is not subscriptable` on first login.

### Pitfall 2: `character.msg()` with No Sessions

**What goes wrong:** `character.msg(status_update=data)` silently does nothing if the character has no connected session. This is correct behavior — but watch for missed pushes in tests that don't mock sessions.

**Why it happens:** `character.msg()` iterates `self.sessions.all()` which is empty for an unconnected character.

**How to avoid:** In tests, use `unittest.mock.MagicMock` on `character.msg`, then assert `character.msg.assert_called_with(status_update=...)`. The project already uses this pattern (see `test_flight_engine.py`).

### Pitfall 3: Zone Tag Search Returns Non-Room Objects

**What goes wrong:** `evennia.search_tag(zone_id, category="zone_id")` returns exits, zone objects, and mobs with the tag — not just rooms.

**Why it happens:** `area_builder.py:_create_exit_object()` tags exits with `zone_id` (line 315). The zone object itself also has the tag (line 145).

**How to avoid:** Filter results by checking `hasattr(r, "exits")` or `r.db_typeclass_path.endswith("rooms.SoravelonRoom")`. For map assembly, the safest check is `isinstance(r.typeclass, SoravelonRoom)` or check for `grid_x` attribute existence.

### Pitfall 4: Auto-Layout Collision on Non-Cardinal Exits

**What goes wrong:** Two rooms that are connected via "up/down/in/out" exits both get assigned (0, 0) and collide.

**Why it happens:** `DIRECTION_OFFSETS` maps "up/down/in/out" to (0, 0) since they have no 2D spatial meaning.

**How to avoid:** After placing a node at `(nx, ny)`, check `occupied` dict and nudge `nx += 1` until the slot is free. The nudge is visible in Pattern 3 above.

### Pitfall 5: Fog of War Scope

**What goes wrong:** Fog-of-war sends `visited: False` for all rooms, blocking the client from rendering any map at all in dungeon zones.

**Why it happens:** `character.db.discovered_exits` tracks discovered exits (for the flight system), not visited rooms. No visited-room tracking exists yet.

**How to avoid:** Add `character.db.visited_rooms` as a set of room dbrefs (or room_id tags). Initialize in `at_object_creation()`. Set in `at_after_move()`. The `map_update` builder reads this set to compute `visited` per room.

### Pitfall 6: `map_update` sent during flight room moves

**What goes wrong:** `FlightScript._arrive_at_stop()` calls `character.move_to(stop_rooms[0], quiet=True)`. This triggers `at_after_move()`, which if naively wired, will push `map_update`. During flight, the player position is moving rapidly and the map panel shouldn't thrash.

**Why it happens:** `at_after_move()` fires for all moves, including script-driven ones.

**How to avoid:** Gate `map_update` in `at_after_move()` with `if character.ndb.in_flight: return`. The `flight_progress` message covers flight state. Push `map_update` explicitly in `_arrive_final()` instead.

---

## Code Examples

Verified patterns from official sources:

### OOB Send (core pattern)

```python
# Source: evennia/objects/objects.py:970 (msg), evennia/server/portal/webclient.py:325 (send_default)
# Any kwarg to character.msg() that is not "text" or "options" becomes OOB.

# Single message type
character.msg(status_update={"dimensions": {"reputation": 45.2}})
# Wire: ["status_update", [], {"dimensions": {"reputation": 45.2}}]

# Multiple message types in one call (batched, same WebSocket frame)
character.msg(
    status_update={"dimensions": {...}},
    stat_update={"hp": 100, "hp_max": 100},
)
# Wire: two separate OOB commands
```

### Session presence check (avoid null sends)

```python
# Source: evennia/objects/objects.py:1023
# character.sessions.all() is the authoritative check
def push_oob(character, msg_type, data):
    if not character.sessions.all():
        return  # Not connected — skip
    # ... debounce check ...
    character.msg(**{msg_type: data})
```

### BFS zone room collection

```python
# Source: adapted from world/node_helpers.py:get_rooms_in_radius()
# Zone rooms via tag search — the project-standard pattern
import evennia
from typeclasses.rooms import SoravelonRoom

def get_zone_rooms(zone_id):
    """Return only SoravelonRoom objects tagged with this zone_id."""
    candidates = evennia.search_tag(zone_id, category="zone_id")
    return [obj for obj in candidates if isinstance(obj.typeclass, SoravelonRoom)]
```

### Test pattern (MagicMock msg)

```python
# Source: project convention (unittest.TestCase + MagicMock, as in test_flight_engine.py)
from unittest.mock import MagicMock, patch
import unittest

class TestOobPublisherStatusUpdate(unittest.TestCase):
    def setUp(self):
        self.char = MagicMock()
        self.char.ndb.oob_debounce = None
        self.char.sessions.all.return_value = [MagicMock()]  # "connected"
        self.char.db.reputation_score = 42.0
        # ... other db attrs

    def test_status_update_sends_dimensions(self):
        from world.oob_publisher import push_status_update
        push_status_update(self.char)
        self.char.msg.assert_called_once()
        call_kwargs = self.char.msg.call_args.kwargs
        self.assertIn("status_update", call_kwargs)
        dims = call_kwargs["status_update"]["dimensions"]
        self.assertEqual(dims["reputation"], 42.0)
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| GMCP/MSDP for Telnet OOB | Native WebSocket JSON array via `send_default` | Evennia WebSocket addition | WebSocket clients use kwarg-based OOB natively; no Telnet negotiation needed |
| Per-room level gating | Zone-level tier without level numbers | This project (CLAUDE.md) | No `level_floor`/`level_cap` on zones — removed from design |

**Deprecated/outdated:**
- GMCP/MSDP: Telnet-era OOB protocols. Evennia supports them but WebSocket clients use the simpler JSON array path. Do not implement GMCP for Phase 2.

---

## Open Questions

1. **Fog-of-war visited-room tracking field name**
   - What we know: `character.db.discovered_flight_points` exists (set of dbrefs). `character.db.discovered_exits` exists (for other uses).
   - What's unclear: Should visited rooms be tracked as dbrefs (int) or room_id strings (tag)?
   - Recommendation: Use `character.db.visited_room_ids` as a set of `room_id` tag strings (not dbrefs). Room_ids are stable across server restarts; dbrefs are stable too but the `room_id` tag is what `map_update` sends as the identifier anyway. Initialize as empty set in `at_object_creation()`. Update in `at_after_move()`.

2. **`node_event` zone-wide broadcast scope**
   - What we know: `NodeScript._on_state_transition()` doesn't currently iterate zone players.
   - What's unclear: How to efficiently find all connected players in a zone.
   - Recommendation: `count_zone_actors()` in `node_helpers.py` already does a single tag-scan pass. A variant that returns player *objects* (not counts) is a small addition. Alternatively, use `evennia.search_tag(zone_id, category="zone_id")`, filter for characters with `sessions.all()`.

3. **`status_update` vs `stat_update` separation**
   - What we know: D-04 lists both `status_update` (dimensions, domains, carried_scales, companion) and `stat_update` (HP, resource bars, conditions).
   - What's unclear: HP/resource bars don't exist yet (combat system is Phase 6). `stat_update` fields will be mostly empty/null.
   - Recommendation: Emit `stat_update` with placeholder `{"hp": null, "hp_max": null, "conditions": []}` now. The schema is defined; the combat system populates it in Phase 6.

---

## Environment Availability

Step 2.6: SKIPPED — Phase 2 is purely server-side Python code additions. No external tools, services, CLIs, databases, or runtimes beyond those already used by the project (Python 3.12, Evennia 6.0, Django ORM, SQLite). All dependencies are already installed and verified.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest via `evennia test --settings server.conf.settings tests/` |
| Config file | none — test discovery via directory |
| Quick run command | `evennia test --settings server.conf.settings tests/test_oob_publisher.py` |
| Full suite command | `evennia test --settings server.conf.settings tests/` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CLI-06 | OOB publisher sends all 8 message types with correct keys | unit | `evennia test --settings server.conf.settings tests/test_oob_publisher.py` | ❌ Wave 0 |
| CLI-06 | Debounce prevents send within window | unit | same | ❌ Wave 0 |
| CLI-06 | Debounce allows send after window | unit | same | ❌ Wave 0 |
| CLI-06 | No send when character has no session | unit | same | ❌ Wave 0 |
| CLI-07 | Auto-layout assigns non-overlapping coords to all zone rooms | unit | `evennia test --settings server.conf.settings tests/test_oob_publisher.py` or `tests/test_area_builder.py` | ❌ Wave 0 |
| CLI-07 | Builder-placed coords are not overwritten by auto-layout | unit | same | ❌ Wave 0 |
| CLI-07 | `map_update` payload contains `grid_x`/`grid_y` for every room | unit | same | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** `evennia test --settings server.conf.settings tests/test_oob_publisher.py`
- **Per wave merge:** `evennia test --settings server.conf.settings tests/`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_oob_publisher.py` — covers CLI-06 (all message types, debounce, session guard)
- [ ] Coordinate tests can be added to `tests/test_area_builder.py` (file exists) — covers CLI-07

*(No framework gaps — pytest + Evennia test utilities already operational)*

---

## Sources

### Primary (HIGH confidence)

- `evennia/server/portal/webclient.py` (installed at `/c/Users/colek/AppData/Local/Programs/Python/Python312/Lib/site-packages/evennia/server/portal/webclient.py`) — Verified: `send_default` dispatches any OOB kwarg as JSON array; `protocol_flags["OOB"] = True` set on WebSocket connect
- `evennia/objects/objects.py` (same install) — Verified: `character.msg(**kwargs)` routes all non-`text`/non-`options` kwargs to `session.data_out(**kwargs)` which terminates in `send_default`
- `evennia/server/serversession.py` (same install) — Verified: `data_out(**kwargs)` → `sessionhandler.data_out(self, **kwargs)`
- `evennia/utils/utils.py` (same install) — Verified: `delay(timedelay, callback)` wraps `TASK_HANDLER.add()`, same mechanism as `FlightScript`
- `world/node_helpers.py` — BFS pattern for zone traversal (direct read)
- `world/area_builder.py` — Room attribute setter `_set_room_attrs()`, exit creation, zone object structure (direct read)
- `typeclasses/characters.py` — Existing hooks: `at_post_puppet`, `at_pre_unpuppet`, `at_before_move`, `at_object_creation` (direct read)
- `world/scripts/node_script.py` — `_on_state_transition()` hook location (direct read)
- `world/scripts/flight_script.py` — `_begin_leg()`, `_arrive_at_stop()`, `_arrive_final()` hook locations (direct read)

### Secondary (MEDIUM confidence)

- Project tests (`tests/test_flight_engine.py` pattern) — MagicMock + `sys.modules` injection for pure unittest.TestCase — confirmed viable for `oob_publisher` tests

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — verified from installed Evennia source files
- Architecture (OOB protocol): HIGH — traced `character.msg()` → `send_default()` → WebSocket JSON through actual source
- Architecture (BFS layout): HIGH — direct adaptation of existing `get_rooms_in_radius()` in codebase
- Pitfalls: HIGH — each pitfall traced to actual code paths (ndb None behavior, zone tag search returns exits, flight move triggers)
- Debounce intervals: MEDIUM — values are Claude's Discretion; calibrated to game feel, not verified against production benchmarks

**Research date:** 2026-03-24
**Valid until:** 2026-05-24 (Evennia 6.0 stable — 60 days)
