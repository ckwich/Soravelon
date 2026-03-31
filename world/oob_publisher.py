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


def _get_zone_obj(room):
    """Resolve the zone object for a room, if available."""
    if not room or not hasattr(room, "db"):
        return None
    try:
        from world.zone_scaling import get_zone_obj_for_room
        return get_zone_obj_for_room(room)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Combat OOB helpers
# ---------------------------------------------------------------------------

def _resolve_combatant(cid):
    """Resolve a single combatant by database ID. Returns obj or None."""
    if cid is None:
        return None
    try:
        from evennia import search_object
        results = search_object(str(cid), exact=False, use_dbref="#" + str(cid))
        if results:
            return results[0]
    except Exception:
        pass
    return None


def _safe_ndb_value(holder, attr, default=None):
    """Read an ndb attribute without leaking MagicMock placeholders into payloads."""
    try:
        value = getattr(holder.ndb, attr, default)
    except Exception:
        return default
    if type(value).__module__.startswith("unittest.mock"):
        return default
    return value


def _safe_value(value, default=None):
    """Collapse MagicMock placeholder values to a default."""
    if type(value).__module__.startswith("unittest.mock"):
        return default
    return value


def _get_available_abilities(character):
    """
    Return list of {id, name, on_cooldown} dicts for the character's known abilities.

    Checks per-encounter cooldowns (ndb.ability_cooldowns) to mark availability.
    """
    try:
        from world.ability_registry import ABILITIES
        from world.models import CharacterAbility

        known_ids = list(
            CharacterAbility.objects.filter(
                character=character
            ).values_list("ability_id", flat=True)
        )
    except Exception:
        return []

    cooldowns = character.ndb.ability_cooldowns or {}
    available = []
    for aid in known_ids:
        ability = ABILITIES.get(aid)
        if not ability:
            continue
        on_cd = cooldowns.get(aid, 0) > 0
        available.append({
            "id": aid,
            "name": ability["name"],
            "on_cooldown": on_cd,
        })
    return available


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
    Push HP, stamina, domain resource, and active conditions.

    Sent on login, after damage/healing, and on status effect changes.
    """
    from world.base_attributes import derive_max_hp, derive_max_stamina
    from world.ability_engine import get_domain_resource

    resource = get_domain_resource(character)
    data = {
        "hp": _safe_ndb_value(character, "hp"),
        "hp_max": _safe_value(derive_max_hp(character)),
        "stamina": _safe_ndb_value(character, "stamina"),
        "stamina_max": _safe_value(derive_max_stamina(character)),
        "domain_resource": resource,
        "conditions": [
            f"{e['type']}_{e.get('stacks', 1)}"
            for e in (_safe_ndb_value(character, "active_effects", []) or [])
        ],
    }
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
    zone_obj = _get_zone_obj(room)
    if zone_obj and hasattr(zone_obj, "db"):
        fog_of_war = bool(zone_obj.db.fog_of_war)
    else:
        fog_of_war = bool(room.db.fog_of_war if hasattr(room, "db") else False)

    # Collect all objects tagged with this zone_id, filter to rooms only
    candidates = evennia.search_tag(zone_id, category="zone_id")
    rooms_data = []
    for r in candidates:
        # Filter: only room typeclasses (Pitfall 3 — avoids exits/zone objects/mobs)
        if not r.db_typeclass_path or "rooms." not in r.db_typeclass_path:
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


def push_combat_update(character, data=None):
    """
    Push structured combat state to the character.

    If data is passed (from CombatScript._build_combat_oob), sends it directly.
    If data is None, builds the payload from the character's combat_handler.

    Payload includes: combat state, round, turn status, actions remaining,
    combatant list with HP percentages and effects, available abilities,
    and current target.
    """
    if data is not None:
        # Legacy / direct passthrough from CombatScript
        _send(character, "combat_update", data)
        return

    handler = character.ndb.combat_handler
    if not handler:
        return

    # Build combatants list
    combatants = []
    for cid in (handler.db.combatant_ids or []):
        obj = _resolve_combatant(cid)
        if not obj:
            continue
        is_mob = not (
            hasattr(obj, "tags")
            and obj.tags.has("player_character", category="character_type")
        )
        if is_mob:
            hp_max = obj.db.hp_max or 1
        else:
            from world.base_attributes import derive_max_hp
            hp_max = derive_max_hp(obj) or 1
        hp_pct = (obj.ndb.hp or 0) / max(1, hp_max)
        effects = [e["type"] for e in (obj.ndb.active_effects or [])]
        current_idx = handler.db.current_turn_index or 0
        ids = handler.db.combatant_ids or []
        is_current = (
            current_idx < len(ids)
            and ids[current_idx] == cid
        )
        combatants.append({
            "id": cid,
            "name": obj.key,
            "hp_pct": round(hp_pct, 2),
            "is_mob": is_mob,
            "effects": effects,
            "is_current": is_current,
        })

    # Build available abilities
    available = _get_available_abilities(character)

    payload = {
        "state": "active",
        "round": handler.db.round_number or 1,
        "your_turn": (
            handler.get_current_combatant() == character
            if hasattr(handler, "get_current_combatant") else False
        ),
        "actions_remaining": character.ndb.actions_remaining or 0,
        "combatants": combatants,
        "available_abilities": available,
        "target_id": character.ndb.combat_target_id,
    }
    _send(character, "combat_update", payload)


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
