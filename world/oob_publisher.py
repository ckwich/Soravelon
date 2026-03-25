"""
OOB publisher — single hub for all server-to-client push data.

All game systems import and call push_* functions here. Never call
character.msg() for OOB directly from game logic.

Message types and debounce intervals (DEBOUNCE_INTERVALS):
  status_update   — dimension/domain scores, currency, companion
  map_update      — zone room graph, player position, fog-of-war
  node_event      — zone node state transition (no debounce)
  flight_progress — Dragon Courier leg tracking
  combat_update   — combat state (Phase 6 placeholder)
  quest_update    — quest state (future placeholder)
  inventory_update — carried items + encumbrance
  stat_update     — HP / resource bars (Phase 6 placeholder)

Wire format (Evennia native):
  character.msg(status_update={"key": "val"})
  → WebSocket frame: ["status_update", [], {"key": "val"}]
"""

import time

# ---------------------------------------------------------------------------
# Debounce configuration — minimum seconds between sends per message type.
# Interval <= 0 means no debounce (always send).
# ---------------------------------------------------------------------------
DEBOUNCE_INTERVALS = {
    "status_update": 2.0,      # dimension/domain scores change slowly
    "map_update": 0.5,          # room movement
    "node_event": 0.0,          # state transitions are rare — must not drop
    "flight_progress": 1.0,     # 1/sec during flight
    "combat_update": 0.25,      # 4/sec max
    "quest_update": 5.0,        # low frequency
    "inventory_update": 1.0,    # 1/sec max
    "stat_update": 0.5,         # HP bars
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _should_send(character, msg_type):
    """Return True if the debounce window for this message type has passed."""
    debounce = character.ndb.oob_debounce or {}
    interval = DEBOUNCE_INTERVALS.get(msg_type, 1.0)
    if interval <= 0:
        return True
    last_sent = debounce.get(msg_type, 0.0)
    return (time.monotonic() - last_sent) >= interval


def _mark_sent(character, msg_type):
    """Record current time as the last-sent timestamp for msg_type (SaverDict copy pattern)."""
    debounce = dict(character.ndb.oob_debounce or {})
    debounce[msg_type] = time.monotonic()
    character.ndb.oob_debounce = debounce


def _send(character, msg_type, data):
    """
    Send an OOB message to the character if connected and debounce allows.

    Checks character.sessions.all() before sending — silently skips if not
    connected (Pitfall 2). Runs debounce gate before calling character.msg().
    """
    if not character.sessions.all():
        return
    if not _should_send(character, msg_type):
        return
    character.msg(**{msg_type: data})
    _mark_sent(character, msg_type)


# ---------------------------------------------------------------------------
# Group position helper
# ---------------------------------------------------------------------------

def _get_group_positions(character):
    """
    Return a list of {room_id, member_name} for group members in the same
    zone as the character (excluding self).

    Returns [] if character is not in a group or has no location.
    """
    from world.group_engine import get_group_state  # lazy import (circular guard)

    room = character.location
    if not room:
        return []
    zone_id = room.db.zone_id
    if not zone_id:
        return []

    group_state = get_group_state(character)
    if not group_state:
        return []

    members = group_state.get("members", [])
    markers = []
    for member_id in members:
        if member_id == character.id:
            continue
        from evennia import search_object  # lazy import
        results = search_object("#%d" % member_id)
        if not results:
            continue
        member = results[0]
        if not member.location:
            continue
        member_zone = member.location.db.zone_id
        if member_zone != zone_id:
            continue
        room_id = member.location.tags.get(category="room_id")
        if room_id:
            markers.append({"room_id": room_id, "member_name": member.key})

    return markers


# ---------------------------------------------------------------------------
# Public push functions
# ---------------------------------------------------------------------------

def push_status_update(character):
    """
    Push dimension scores, domain scores, currency, and companion info.

    Reads character state via get_character_context_packet from world_state.
    Sent on login and whenever dimension/domain scores change.
    """
    from world.world_state import get_character_context_packet  # lazy import

    packet = get_character_context_packet(character)
    data = {
        "dimensions": {
            "reputation": packet.get("reputation") or 0.0,
            "network": packet.get("network") or 0.0,
            "bond": packet.get("bond") or 0.0,
            "legacy": packet.get("legacy") or 0.0,
            "attunement": packet.get("attunement") or 0.0,
        },
        "domains": character.db.domain_scores or {},
        "carried_scales": character.db.carried_scales or 0,
        "companion": {
            "id": character.db.companion_id,
            "type": character.db.companion_type,
            "tier": character.db.companion_tier,
        },
    }
    _send(character, "status_update", data)


def push_stat_update(character):
    """
    Push HP and resource bar state (Phase 6 placeholder).

    The schema is live; the combat system populates hp/hp_max in Phase 6.
    """
    data = {"hp": None, "hp_max": None, "conditions": []}
    _send(character, "stat_update", data)


def push_map_update(character):
    """
    Push the full zone room graph for the character's current zone.

    Includes: room IDs, names, coords, room types, node states, exits,
    fog-of-war visited flags, and group member markers.

    Only rooms tagged with the current zone_id and having SoravelonRoom
    typeclass are included (Pitfall 3 — avoids exits/zone objects/mobs).
    """
    import evennia  # lazy import

    room = character.location
    if not room:
        return
    zone_id = room.db.zone_id
    if not zone_id:
        return

    visited_ids = set(character.db.visited_room_ids or set())
    fog_of_war = bool(room.db.fog_of_war if hasattr(room, "db") else False)

    # Collect all objects tagged with this zone_id, filter to rooms only
    candidates = evennia.search_tag(zone_id, category="zone_id")
    rooms_data = []
    for r in candidates:
        # Filter: only SoravelonRoom instances (Pitfall 3)
        if not r.db_typeclass_path or not r.db_typeclass_path.endswith("rooms.SoravelonRoom"):
            continue

        room_id = r.tags.get(category="room_id")
        node_state = r.tags.get(category="node_state")

        exits_data = []
        if hasattr(r, "exits"):
            for ex in r.exits:
                dest = ex.destination
                dest_zone = dest.db.zone_id if dest and hasattr(dest, "db") else None
                exits_data.append({
                    "direction": ex.key,
                    "destination_zone": dest_zone,
                    "cross_zone": (dest_zone != zone_id) if dest_zone is not None else False,
                })

        rooms_data.append({
            "room_id": room_id,
            "name": r.key,
            "x": r.db.grid_x,
            "y": r.db.grid_y,
            "room_type": r.db.room_type or "generic",
            "node_state": node_state,
            "exits": exits_data,
            "visited": room_id in visited_ids if room_id else False,
        })

    player_room_id = room.tags.get(category="room_id")
    group_markers = _get_group_positions(character)

    data = {
        "zone_id": zone_id,
        "player_room_id": player_room_id,
        "fog_of_war": fog_of_war,
        "rooms": rooms_data,
        "group_markers": group_markers,
    }
    _send(character, "map_update", data)


def push_node_event(character, zone_id, old_state, new_state):
    """
    Push a node state transition event to the character.

    No debounce — state transitions are infrequent and must not be dropped.
    """
    data = {
        "zone_id": zone_id,
        "old_state": old_state,
        "new_state": new_state,
    }
    _send(character, "node_event", data)


def push_flight_progress(character, leg_index, total_legs, destination_name, disembark_available):
    """
    Push Dragon Courier flight leg progress to the character.

    Called by FlightScript on each leg start and arrival.
    """
    data = {
        "leg_index": leg_index,
        "total_legs": total_legs,
        "destination_name": destination_name,
        "disembark_available": disembark_available,
    }
    _send(character, "flight_progress", data)


def push_combat_update(character, data):
    """
    Push combat state to the character (Phase 6 placeholder passthrough).

    Combat field schema is TBD in Phase 6. Callers assemble and pass data dict.
    """
    _send(character, "combat_update", data)


def push_quest_update(character, data):
    """
    Push quest state to the character (placeholder passthrough).

    Quest field schema is TBD when the quest system is built.
    """
    _send(character, "quest_update", data)


def push_inventory_update(character):
    """
    Push inventory state to the character.

    Items list is a stub — full item enumeration via inventory_engine in Phase 6.
    Encumbrance state from inventory_helpers.get_carry_state is live now.
    """
    from world.inventory_helpers import get_carry_state  # lazy import

    data = {
        "items": [],  # stub: Phase 6 will populate via inventory_engine query
        "encumbrance": get_carry_state(character),
    }
    _send(character, "inventory_update", data)
