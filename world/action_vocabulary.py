"""
Action Vocabulary for Soravelon.

Shared dispatch module for all trigger-driven and command-driven game events.
Every action type in the game routes through execute_action().

12 action types (D-07):
  Implemented: teleport, teleport_to_mob, echo, give_item, take_item,
               modify_standing, modify_attunement, log_world_event, despawn_self
  Stubs (D-05): set_quest_flag, open_dialogue, spawn_mob

All handlers use lazy imports to avoid circular dependencies (Pitfall 3).
execute_action() enforces a trigger chain depth limit of 3 (D-19).
"""


# ---------------------------------------------------------------------------
# Depth limit constant
# ---------------------------------------------------------------------------

TRIGGER_CHAIN_DEPTH_LIMIT = 3


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

def _handle_echo(action_dict, context, _depth):
    """Send a message to the character in context."""
    character = context.get("character")
    if not character:
        return False, "No character in context"
    msg = action_dict.get("message", "")
    character.msg(msg)
    return True, ""


def _handle_teleport(action_dict, context, _depth):
    """Move character to a specific room by DB id."""
    character = context.get("character")
    if not character:
        return False, "No character in context"
    target_room_id = action_dict.get("target_room_id")
    if target_room_id is None:
        return False, "teleport: missing target_room_id"
    import evennia
    results = evennia.search_object(dbref=target_room_id)
    if not results:
        return False, f"teleport: room not found (id={target_room_id})"
    target_room = results[0]
    character.move_to(target_room, quiet=False)
    return True, ""


def _handle_teleport_to_mob(action_dict, context, _depth):
    """Move character to a named mob's current location."""
    character = context.get("character")
    if not character:
        return False, "No character in context"
    mob_key = action_dict.get("mob_key")
    if not mob_key:
        return False, "teleport_to_mob: missing mob_key"
    import evennia
    results = evennia.search_object(mob_key)
    if not results:
        return False, f"teleport_to_mob: mob not found (key={mob_key})"
    mob_obj = results[0]
    target_room = mob_obj.location
    if not target_room:
        return False, f"teleport_to_mob: mob '{mob_key}' has no location"
    character.move_to(target_room, quiet=False)
    return True, ""


def _handle_give_item(action_dict, context, _depth):
    """Give an item to the character (by item id)."""
    character = context.get("character")
    if not character:
        return False, "No character in context"
    item_id = action_dict.get("item_id")
    if item_id is None:
        return False, "give_item: missing item_id"
    import evennia
    results = evennia.search_object(dbref=item_id)
    if not results:
        return False, f"give_item: item not found (id={item_id})"
    item = results[0]
    from world.inventory_engine import pick_up
    return pick_up(character, item)


def _handle_take_item(action_dict, context, _depth):
    """Take an item from the character's inventory (by item id)."""
    character = context.get("character")
    if not character:
        return False, "No character in context"
    item_id = action_dict.get("item_id")
    if item_id is None:
        return False, "take_item: missing item_id"
    import evennia
    results = evennia.search_object(dbref=item_id)
    if not results:
        return False, f"take_item: item not found (id={item_id})"
    item = results[0]
    from world.inventory_engine import drop_item
    return drop_item(character, item)


def _handle_modify_standing(action_dict, context, _depth):
    """Adjust faction standing for the character."""
    character = context.get("character")
    if not character:
        return False, "No character in context"
    faction_id = action_dict.get("faction_id")
    delta = action_dict.get("delta", 0)
    if not faction_id:
        return False, "modify_standing: missing faction_id"
    from world.world_state import modify_standing
    modify_standing(character, faction_id, delta, "trigger_action")
    return True, ""


def _handle_modify_attunement(action_dict, context, _depth):
    """Adjust zone attunement for the character."""
    character = context.get("character")
    if not character:
        return False, "No character in context"
    zone_id = action_dict.get("zone_id")
    delta = action_dict.get("delta", 0)
    if not zone_id:
        return False, "modify_attunement: missing zone_id"
    from world.world_state import update_zone_attunement
    update_zone_attunement(character, zone_id, delta)
    return True, ""


def _handle_log_world_event(action_dict, context, _depth):
    """Record a world event to the WorldEventLog."""
    character = context.get("character")
    event_type = action_dict.get("event_type", "trigger_event")
    data = action_dict.get("data") or {}
    zone_id = action_dict.get("zone_id", "")
    character_id = character.id if character else None
    from world.world_state import log_world_event
    log_world_event(
        event_type=event_type,
        description=f"Trigger-fired event: {event_type}",
        zone_id=zone_id,
        character_id=character_id,
        data=data,
    )
    return True, ""


def _handle_despawn_self(action_dict, context, _depth):
    """Delete the mob object from the game world."""
    mob = context.get("mob")
    if not mob:
        return False, "despawn_self: no mob in context"
    mob.delete()
    return True, ""


def _stub_handler(action_dict, context, _depth):
    """Placeholder for not-yet-implemented actions."""
    action_type = action_dict.get("action_type", "unknown")
    return False, f"Action '{action_type}' not yet implemented."


# ---------------------------------------------------------------------------
# Dispatch registry
# ---------------------------------------------------------------------------

ACTION_HANDLERS = {
    "echo": _handle_echo,
    "teleport": _handle_teleport,
    "teleport_to_mob": _handle_teleport_to_mob,
    "give_item": _handle_give_item,
    "take_item": _handle_take_item,
    "modify_standing": _handle_modify_standing,
    "modify_attunement": _handle_modify_attunement,
    "log_world_event": _handle_log_world_event,
    "despawn_self": _handle_despawn_self,
    "set_quest_flag": _stub_handler,
    "open_dialogue": _stub_handler,
    "spawn_mob": _stub_handler,
}


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def execute_action(action_dict, context, _depth=0):
    """
    Execute one action from the shared vocabulary.

    context keys: character, room, mob, item (all optional — relevant handler
    will validate its requirements).
    _depth: recursion depth for trigger chaining — blocked at >= 3 (D-19).

    Returns (bool, str).
    """
    if _depth >= TRIGGER_CHAIN_DEPTH_LIMIT:
        return False, "Trigger chain depth limit reached."
    action_type = action_dict.get("action_type")
    handler = ACTION_HANDLERS.get(action_type)
    if not handler:
        return False, f"Unknown action type: {action_type}"
    return handler(action_dict, context, _depth)
