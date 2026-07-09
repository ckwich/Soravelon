"""
Action Vocabulary for Soravelon.

Shared dispatch module for all trigger-driven and command-driven game events.
Every action type in the game routes through execute_action().

19 action types (D-07, D-24):
  Implemented: teleport, teleport_to_mob, echo, give_item, take_item,
               modify_standing, modify_attunement, log_world_event, despawn_self,
               spawn_mob, add_room_flag, give_scales, give_skill_xp,
               grant_practice, modify_node_failure, set_quest_flag,
               open_dialogue, learn_recipe, record_social_event

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
    results = evennia.search_object(f"#{target_room_id}")
    if not results:
        return False, f"teleport: room not found (id={target_room_id})"
    target_room = results[0]
    character.move_to(target_room, quiet=False, move_hooks=False)
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
    character.move_to(target_room, quiet=False, move_hooks=False)
    return True, ""


def _handle_give_item(action_dict, context, _depth):
    """Give an item to the character. Supports item_id (existing object) or
    template_id (create from zone item_definitions, D-24)."""
    character = context.get("character")
    if not character:
        return False, "No character in context"

    # Template-based creation (D-24)
    template_id = action_dict.get("template_id")
    if template_id:
        room = context.get("room") or (character.location if character else None)
        if not room:
            return False, "give_item: no room context for template lookup"
        import evennia
        zone_objs = evennia.search_tag("zone_object", category="object_type")
        zone_id = room.db.zone_id
        zone_obj = next((o for o in zone_objs if o.db.zone_id == zone_id), None)
        if not zone_obj:
            return False, f"give_item: zone object not found for zone '{zone_id}'"
        item_defs = zone_obj.db.item_definitions or []
        item_def = next((d for d in item_defs if d.get("item_id") == template_id), None)
        if not item_def:
            return False, f"give_item: template '{template_id}' not found in zone"
        from world.item_spawner import create_item_from_template
        item = create_item_from_template(item_def, location=room)
        from world.inventory_engine import pick_up
        return pick_up(character, item)

    # Existing object by dbref (original behavior)
    item_id = action_dict.get("item_id")
    if item_id is None:
        return False, "give_item: missing item_id or template_id"
    import evennia
    results = evennia.search_object(f"#{item_id}")
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
    results = evennia.search_object(f"#{item_id}")
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


def _handle_spawn_mob(action_dict, context, _depth):
    """Spawn a mob using a spawn_def dict or mob template string (D-26).

    action_dict keys:
        mob (str): mob template key (required)
        room_id (str, optional): tag room_id to spawn into; defaults to context room
        base_disposition (float, optional): base disposition override (default 0.0)
        flee_threshold (int, optional): flee HP threshold (default 20)
    """
    room = context.get("room")
    mob_template_key = action_dict.get("mob")
    if not mob_template_key:
        return False, "spawn_mob: missing 'mob' key"
    target_room = room
    room_id = action_dict.get("room_id")
    if room_id:
        import evennia
        results = evennia.search_tag(room_id, category="room_id")
        if results:
            target_room = results[0]
    if not target_room:
        return False, "spawn_mob: no target room"
    spawn_def = {
        "mob": mob_template_key,
        "count_min": 1,
        "count_max": 1,
        "is_named": False,
        "base_disposition": action_dict.get("base_disposition", 0.0),
        "flee_threshold": action_dict.get("flee_threshold", 20),
        "respawn_minutes": 0,   # action-spawned mobs don't auto-respawn
        "respawn_variance": 0,
        "trust_sensitive": False,
        "behavior": [],
        "standing_check": None,
        "prestige_modifier": 1.0,
        "tome_drop": None,
        "spawn_condition": None,
        "sequence": [],
    }
    from world.mob_spawner import spawn_single_mob
    mob = spawn_single_mob(spawn_def, target_room)
    if not mob:
        return False, "spawn_mob: failed to create mob"
    return True, f"Spawned {mob.key}"


def _action_add_room_flag(action_dict, context, _depth):
    """Write a room state flag to the character's current room. D-24."""
    flag = action_dict.get("flag", "")
    duration = action_dict.get("duration")
    character = context.get("character")
    if character and character.location and flag:
        from world.room_state import add_room_flag
        add_room_flag(character.location, flag, duration)
    return True, ""



def _handle_give_scales(action_dict, context, _depth):
    """Award Scales to character's carried_scales."""
    character = context.get("character")
    if not character:
        return False, "give_scales: no character in context"
    amount = action_dict.get("amount", 0)
    if amount <= 0:
        return False, "give_scales: invalid amount"
    current = character.db.carried_scales or 0
    character.db.carried_scales = current + amount
    character.msg(f"|y[+{amount} Scales]|n")
    return True, ""


def _handle_give_skill_xp(action_dict, context, _depth):
    """Award skill XP via the ndb accumulator pattern."""
    character = context.get("character")
    if not character:
        return False, "give_skill_xp: no character in context"
    skill_id = action_dict.get("skill_id")
    count = action_dict.get("count", 1)
    if not skill_id:
        return False, "give_skill_xp: missing skill_id"
    from world.skill_definitions import SKILL_DEFINITIONS
    if skill_id not in SKILL_DEFINITIONS:
        return False, f"give_skill_xp: unknown skill_id '{skill_id}'"
    from world.skill_engine import accumulate_skill_use
    accumulate_skill_use(character, skill_id, count)
    character.msg(f"|g[+{count} {skill_id.replace('_', ' ').title()} XP]|n")
    return True, ""


def _handle_grant_practice(action_dict, context, _depth):
    """Resolve a builder-authored practice opportunity."""
    from world.practice_engine import resolve_practice_opportunity
    return resolve_practice_opportunity(action_dict, context)


def _template_action_value(value, template_context):
    """Render action templates recursively without changing non-string values."""
    if isinstance(value, str):
        return value.format_map(template_context)
    if hasattr(value, "items"):
        return {
            key: _template_action_value(item, template_context)
            for key, item in dict(value.items()).items()
        }
    if isinstance(value, (bytes, bytearray)):
        return value
    try:
        return [_template_action_value(item, template_context) for item in value]
    except TypeError:
        pass
    return value


def _first_present(mapping, *keys, default=""):
    for key in keys:
        if key in mapping:
            return mapping[key]
    return default


def _resolve_social_node_key(value, node_refs, field_name):
    if not value:
        return False, f"record_social_event: missing {field_name}", ""
    node_key = node_refs.get(value, value)
    if not isinstance(node_key, str) or ":" not in node_key:
        return False, f"record_social_event: unknown node reference '{value}' for {field_name}", ""
    return True, "", node_key


def _action_sequence(value):
    if isinstance(value, (str, bytes, bytearray)) or hasattr(value, "items"):
        return None
    try:
        return list(value)
    except TypeError:
        return None


def _action_mapping(value):
    if not hasattr(value, "items"):
        return None
    return dict(value.items())


def _record_social_event_action(action_dict, character):
    from django.db import transaction

    template_context = {
        "character_id": str(character.id),
        "character_key": str(character.key),
    }

    try:
        rendered = _template_action_value(action_dict, template_context)
    except (KeyError, ValueError) as exc:
        return False, f"record_social_event: invalid template ({exc})"

    with transaction.atomic():
        success, message = _record_social_event_rendered(rendered)
        if not success:
            transaction.set_rollback(True)
        return success, message


def _record_social_event_rendered(rendered):
    from world.social_engine import (
        assert_social_claim,
        connect_social_nodes,
        ensure_social_node,
        mark_known,
        propagate_social_knowledge,
        record_social_fact,
    )

    node_defs = _action_sequence(rendered.get("nodes") or [])
    if not node_defs:
        return False, "record_social_event: nodes must be a non-empty list"

    node_refs = {}
    for index, node_def in enumerate(node_defs):
        node_def = _action_mapping(node_def)
        if node_def is None:
            return False, f"record_social_event: node {index} must be a dict"

        node_type = node_def.get("node_type")
        identifier = _first_present(node_def, "identifier_template", "identifier")
        if not node_type or not identifier:
            return False, f"record_social_event: node {index} missing node_type or identifier"

        try:
            node = ensure_social_node(
                node_type,
                identifier,
                display_name=_first_present(
                    node_def,
                    "display_template",
                    "display_name_template",
                    "display",
                    "display_name",
                ),
                zone_id=_first_present(node_def, "zone_template", "zone_id_template", "zone", "zone_id"),
                settlement_id=_first_present(
                    node_def,
                    "settlement_template",
                    "settlement_id_template",
                    "settlement",
                    "settlement_id",
                ),
                faction_id=_first_present(
                    node_def,
                    "faction_template",
                    "faction_id_template",
                    "faction",
                    "faction_id",
                ),
                metadata=node_def.get("metadata") or {},
            )
        except ValueError as exc:
            return False, f"record_social_event: {exc}"

        for ref in (node_def.get("ref"), node_def.get("key"), node.node_key):
            if ref:
                node_refs[ref] = node.node_key

    edge_defs = _action_sequence(rendered.get("edges") or [])
    if edge_defs is None:
        return False, "record_social_event: edges must be a list"
    for index, edge_def in enumerate(edge_defs):
        edge_def = _action_mapping(edge_def)
        if edge_def is None:
            return False, f"record_social_event: edge {index} must be a dict"

        ok, message, source_node_key = _resolve_social_node_key(
            _first_present(
                edge_def,
                "source_template",
                "source_node_template",
                "source_node_key_template",
                "source",
                "source_node",
                "source_node_key",
            ),
            node_refs,
            "edge source",
        )
        if not ok:
            return False, message
        ok, message, target_node_key = _resolve_social_node_key(
            _first_present(
                edge_def,
                "target_template",
                "target_node_template",
                "target_node_key_template",
                "target",
                "target_node",
                "target_node_key",
            ),
            node_refs,
            "edge target",
        )
        if not ok:
            return False, message

        ok, message, _edge = connect_social_nodes(
            source_node_key,
            target_node_key,
            edge_type=edge_def.get("edge_type"),
            directionality=edge_def.get("directionality", "one_way"),
            trust=edge_def.get("trust", 0.5),
            latency_seconds=edge_def.get("latency_seconds", 0),
            bandwidth=edge_def.get("bandwidth", 3),
            secrecy=edge_def.get("secrecy", ""),
            distortion=edge_def.get("distortion", ""),
            scope_tags=edge_def.get("scope_tags") or [],
            blockers=edge_def.get("blockers") or [],
        )
        if not ok:
            return False, f"record_social_event: {message}"

    fact_def = rendered.get("fact")
    fact_def = _action_mapping(fact_def)
    if fact_def is None:
        return False, "record_social_event: fact must be a dict"

    fact_key = _first_present(fact_def, "fact_key_template", "fact_key")
    if not fact_key or not fact_def.get("event_type") or not fact_def.get("summary"):
        return False, "record_social_event: fact missing fact_key, event_type, or summary"
    ok, message, subject_node_key = _resolve_social_node_key(
        _first_present(
            fact_def,
            "subject_template",
            "subject_node_template",
            "subject_node_key_template",
            "subject",
            "subject_node",
            "subject_node_key",
        ),
        node_refs,
        "fact subject",
    )
    if not ok:
        return False, message

    actor_node_key = ""
    actor_ref = _first_present(
        fact_def,
        "actor_template",
        "actor_node_template",
        "actor_node_key_template",
        "actor",
        "actor_node",
        "actor_node_key",
    )
    if actor_ref:
        ok, message, actor_node_key = _resolve_social_node_key(
            actor_ref,
            node_refs,
            "fact actor",
        )
        if not ok:
            return False, message

    scope_node_key = ""
    scope_ref = _first_present(
        fact_def,
        "scope_template",
        "scope_node_template",
        "scope_node_key_template",
        "scope",
        "scope_node",
        "scope_node_key",
    )
    if scope_ref:
        ok, message, scope_node_key = _resolve_social_node_key(
            scope_ref,
            node_refs,
            "fact scope",
        )
        if not ok:
            return False, message

    ok, message, fact = record_social_fact(
        fact_key=fact_key,
        subject_node_key=subject_node_key,
        actor_node_key=actor_node_key,
        scope_node_key=scope_node_key,
        event_type=fact_def.get("event_type"),
        summary=fact_def.get("summary"),
        tags=fact_def.get("tags") or [],
        visibility=fact_def.get("visibility", "local"),
        evidence=fact_def.get("evidence") or {},
        weight=fact_def.get("weight", 1.0),
        confidence=fact_def.get("confidence", 1.0),
        occurred_at=fact_def.get("occurred_at"),
        expires_at=fact_def.get("expires_at"),
    )
    if not ok:
        return False, f"record_social_event: {message}"

    claim = None
    claim_def = rendered.get("claim")
    if claim_def:
        claim_def = _action_mapping(claim_def)
        if claim_def is None:
            return False, "record_social_event: claim must be a dict"

        ok, message, speaker_node_key = _resolve_social_node_key(
            _first_present(
                claim_def,
                "speaker_template",
                "speaker_node_template",
                "speaker_node_key_template",
                "speaker",
                "speaker_node",
                "speaker_node_key",
            ),
            node_refs,
            "claim speaker",
        )
        if not ok:
            return False, message
        ok, message, claim_subject_node_key = _resolve_social_node_key(
            _first_present(
                claim_def,
                "subject_template",
                "subject_node_template",
                "subject_node_key_template",
                "subject",
                "subject_node",
                "subject_node_key",
            ),
            node_refs,
            "claim subject",
        )
        if not ok:
            return False, message

        claim_fact_key = _first_present(
            claim_def,
            "fact_key_template",
            "fact_key",
            default=fact.fact_key,
        )
        claim_key = _first_present(claim_def, "claim_key_template", "claim_key")
        if not claim_key or not claim_def.get("claim_type") or not claim_def.get("summary"):
            return False, "record_social_event: claim missing claim_key, claim_type, or summary"

        ok, message, claim = assert_social_claim(
            claim_key=claim_key,
            speaker_node_key=speaker_node_key,
            subject_node_key=claim_subject_node_key,
            fact_key=claim_fact_key,
            claim_type=claim_def.get("claim_type"),
            summary=claim_def.get("summary"),
            status=claim_def.get("status", "rumor"),
            intent=claim_def.get("intent", ""),
            bias_tags=claim_def.get("bias_tags") or [],
            confidence=claim_def.get("confidence", 0.5),
        )
        if not ok:
            return False, f"record_social_event: {message}"

    default_fact_key = fact.fact_key if fact else ""
    default_claim_key = claim.claim_key if claim else ""
    knowledge_defs = _action_sequence(rendered.get("knowledge") or [])
    if knowledge_defs is None:
        return False, "record_social_event: knowledge must be a list"

    for index, knowledge_def in enumerate(knowledge_defs):
        knowledge_def = _action_mapping(knowledge_def)
        if knowledge_def is None:
            return False, f"record_social_event: knowledge {index} must be a dict"

        ok, message, node_key = _resolve_social_node_key(
            _first_present(
                knowledge_def,
                "node_template",
                "node_key_template",
                "node",
                "node_key",
            ),
            node_refs,
            "knowledge node",
        )
        if not ok:
            return False, message

        source_node_key = ""
        source_ref = _first_present(
            knowledge_def,
            "source_template",
            "source_node_template",
            "source_node_key_template",
            "source",
            "source_node",
            "source_node_key",
        )
        if source_ref:
            ok, message, source_node_key = _resolve_social_node_key(
                source_ref,
                node_refs,
                "knowledge source",
            )
            if not ok:
                return False, message

        ok, message, _knowledge = mark_known(
            node_key=node_key,
            fact_key=_first_present(
                knowledge_def,
                "fact_key_template",
                "fact_key",
                default=default_fact_key,
            ),
            claim_key=_first_present(
                knowledge_def,
                "claim_key_template",
                "claim_key",
                default=default_claim_key,
            ),
            source_node_key=source_node_key,
            edge_key=knowledge_def.get("edge_key", ""),
            channel=knowledge_def.get("channel"),
            confidence=knowledge_def.get("confidence", 0.5),
            spreading=knowledge_def.get("spreading", False),
            available_after=knowledge_def.get("available_after"),
            evidence=knowledge_def.get("evidence") or {},
        )
        if not ok:
            return False, f"record_social_event: {message}"

    propagate_defs = rendered.get("propagate") or []
    if hasattr(propagate_defs, "items"):
        propagate_defs = [propagate_defs]
    else:
        propagate_defs = _action_sequence(propagate_defs)
    if propagate_defs is None:
        return False, "record_social_event: propagate must be a dict or list"

    for index, propagate_def in enumerate(propagate_defs):
        propagate_def = _action_mapping(propagate_def)
        if propagate_def is None:
            return False, f"record_social_event: propagate {index} must be a dict"
        ok, message, source_node_key = _resolve_social_node_key(
            _first_present(
                propagate_def,
                "source_template",
                "source_node_template",
                "source_node_key_template",
                "source",
                "source_node",
                "source_node_key",
            ),
            node_refs,
            "propagate source",
        )
        if not ok:
            return False, message
        propagated = propagate_social_knowledge(
            source_node_key=source_node_key,
            fact_key=_first_present(
                propagate_def,
                "fact_key_template",
                "fact_key",
                default=default_fact_key,
            ),
            claim_key=_first_present(
                propagate_def,
                "claim_key_template",
                "claim_key",
                default=default_claim_key,
            ),
            budget=propagate_def.get("budget", 10),
        )
        if propagate_def.get("required") and not propagated:
            return False, (
                "record_social_event: required propagation from "
                f"{source_node_key} carried no knowledge"
            )

    return True, "Social event recorded."


def _handle_record_social_event(action_dict, context, _depth):
    """Record a declarative Social Web event from a quest or trigger action."""
    character = context.get("character")
    if not character:
        return False, "record_social_event: no character in context"
    if getattr(character, "id", None) is None or not getattr(character, "key", None):
        return False, "record_social_event: invalid character context"
    return _record_social_event_action(action_dict, character)


def _handle_modify_node_failure(action_dict, context, _depth):
    """Adjust node failure percentage for a zone."""
    zone_id = action_dict.get("zone_id")
    delta = action_dict.get("delta", 0)
    if not zone_id:
        return False, "modify_node_failure: missing zone_id"
    import evennia
    zone_objs = evennia.search_tag(zone_id, category="zone_id")
    if not zone_objs:
        return False, f"modify_node_failure: zone '{zone_id}' not found"
    # Filter to actual zone object, not rooms/mobs that share the zone_id tag
    zone_obj = None
    for obj in zone_objs:
        if obj.tags.get("zone_object", category="object_type"):
            zone_obj = obj
            break
    if not zone_obj:
        return False, f"modify_node_failure: zone object for '{zone_id}' not found"
    scripts = zone_obj.scripts.get("node_script")
    if not scripts:
        return False, f"modify_node_failure: no node_script on zone '{zone_id}'"
    script = scripts[0]
    old_failure = script.db.failure
    new_failure = max(0.0, min(100.0, old_failure + delta))
    script.db.failure = new_failure
    script._update_state(old_failure, new_failure)
    return True, ""


def _handle_set_quest_flag(action_dict, context, _depth):
    """
    Set a quest flag for a character's active quest.

    action_dict keys:
        quest_id (str): ID of the quest to update
        flag_name (str): name of the flag to set

    If the flag represents an investigation milestone (flag_name starts with
    'investigate_'), delegates to check_investigate_objectives. Otherwise,
    sets the flag directly on the quest's progress dict.
    """
    character = context.get("character")
    if not character:
        return False, "No character in context"
    quest_id = action_dict.get("quest_id")
    flag_name = action_dict.get("flag_name")
    if not quest_id or not flag_name:
        return False, "set_quest_flag: missing quest_id or flag_name"

    from world.quest_engine import get_quest_detail

    detail = get_quest_detail(character, quest_id)
    if not detail or detail.get("status") != "active":
        return False, "No active quest found."

    # Investigation milestone delegation
    if flag_name.startswith("investigate_"):
        from world.quest_engine import check_investigate_objectives
        room = context.get("room") or (character.location if character else None)
        if room:
            check_investigate_objectives(character, room)
        return True, f"Quest flag '{flag_name}' set."

    # Generic flag — update progress dict directly via CharacterQuest model
    from world.quest_engine import get_active_quests
    for cq in get_active_quests(character):
        if cq.quest_id == quest_id:
            progress = dict(cq.progress or {})
            progress[flag_name] = 1
            cq.progress = progress
            cq.save(update_fields=["progress"])
            return True, f"Quest flag '{flag_name}' set."

    return False, "No active quest found."


def _handle_open_dialogue(action_dict, context, _depth):
    """
    Open dialogue with an NPC, checking for available quest offers.

    action_dict keys:
        npc (object, optional): the NPC to talk to (falls back to context)

    If the NPC has a quest available, auto-accepts it for the character.
    Sends the NPC greeting to the character regardless.
    """
    character = context.get("character")
    if not character:
        return False, "No character in context"

    npc = action_dict.get("npc") or context.get("mob") or context.get("npc")
    if not npc:
        return False, "open_dialogue: no NPC in context"

    from world.quest_engine import get_available_quest_for_npc, accept_quest
    from world.dialogue_engine import resolve_greeting

    # Check for quest offer
    quest_spec = get_available_quest_for_npc(npc, character)
    if quest_spec:
        quest_id = quest_spec.get("quest_id")
        success, msg = accept_quest(character, quest_id, quest_spec)
        if not success:
            character.msg(f"|y{msg}|n")

    # Send NPC greeting
    greeting_text, _tier = resolve_greeting(npc, character)
    character.msg(greeting_text)

    return True, "Dialogue opened."


def _handle_learn_recipe(action_dict, context, _depth):
    """
    Teach the character a crafting recipe.

    action_dict keys:
        recipe_id (str): ID of the recipe in RECIPE_REGISTRY
        learned_from (str, optional): Name of the NPC who taught it
        message (str, optional): Custom message to display
    """
    character = context.get("character")
    if not character:
        return False, "No character in context"

    recipe_id = action_dict.get("recipe_id")
    if not recipe_id:
        return False, "learn_recipe: no recipe_id"

    from world.models import CharacterRecipe

    _obj, created = CharacterRecipe.objects.get_or_create(
        character=character,
        recipe_id=recipe_id,
        defaults={"learned_from": action_dict.get("learned_from", "")},
    )

    if created:
        msg = action_dict.get("message") or f"|gYou learned the recipe: {recipe_id}.|n"
        character.msg(msg)
        return True, f"Learned recipe {recipe_id}"
    else:
        character.msg(f"|yYou already know the recipe: {recipe_id}.|n")
        return True, f"Already knew recipe {recipe_id}"


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
    "set_quest_flag": _handle_set_quest_flag,
    "open_dialogue": _handle_open_dialogue,
    "spawn_mob": _handle_spawn_mob,
    "add_room_flag": _action_add_room_flag,
    "give_scales": _handle_give_scales,
    "give_skill_xp": _handle_give_skill_xp,
    "grant_practice": _handle_grant_practice,
    "modify_node_failure": _handle_modify_node_failure,
    "learn_recipe": _handle_learn_recipe,
    "record_social_event": _handle_record_social_event,
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
