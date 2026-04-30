"""
zone_serializer — JSON zone data → AreaBuilder adapter.

Accepts parsed .zone.json data (a Python dict) and calls
AreaBuilder methods to build the zone into Evennia DB objects.

JSON schema mirrors AreaBuilder method kwargs exactly.
Single source of truth for the JSON↔AreaBuilder mapping.

Usage::

    import json
    from world.zone_serializer import load_zone_from_json

    with open("world/areas/vaels_crossing.zone.json") as f:
        zone_data = json.load(f)
    report = load_zone_from_json(zone_data)
"""

from world.area_builder import AreaBuilder, AreaBuilderValidationError
from world.area_validator import validate_zone


def load_zone_from_json(zone_data: dict) -> dict:
    """
    Parse JSON zone data and call AreaBuilder methods to build the zone.

    Args:
        zone_data: Parsed dict from a .zone.json file. Expected top-level keys:
            zone (dict, required), rooms (list), exits (list), spawns (list),
            npcs (list), named_mobs (list), patrols (list), triggers (list),
            custom_commands (list), practice_opportunities (list),
            flight_points (list), flight_routes (list), node (dict or None),
            quests (list), materials (list), loot_table_overrides (list),
            lore_fragments (list)

    Returns:
        build() report dict: {zone_id, rooms_created, exits_created, warnings, unresolved_exits}

    Raises:
        AreaBuilderValidationError: if validate_zone() finds error-severity issues
        KeyError: if required "zone" key or "zone_id" field is missing
    """
    # 1. Validate before touching the DB
    errors = validate_zone(zone_data)
    error_msgs = [f"{e.field_path}: {e.message}" for e in errors if e.severity == "error"]
    if error_msgs:
        raise AreaBuilderValidationError(
            f"zone_serializer: {len(error_msgs)} validation error(s):\n"
            + "\n".join(f"  - {m}" for m in error_msgs)
        )

    zone_meta = zone_data["zone"]
    zone_id = zone_meta["zone_id"]
    area = AreaBuilder(zone_id)

    # 2. zone() — pass all zone_meta kwargs except zone_id (AreaBuilder takes zone_id in __init__)
    zone_kwargs = {k: v for k, v in zone_meta.items() if k != "zone_id"}
    area.zone(**zone_kwargs)

    # 3. loot_table_overrides — zone-owned drop tables keyed by mob/loot table id
    for override_def in zone_data.get("loot_table_overrides", []):
        mob_type = override_def["mob_type"]
        override_kwargs = {
            k: v for k, v in override_def.items()
            if k != "mob_type"
        }
        area.loot_table_override(mob_type, **override_kwargs)

    # 4. rooms — build local lookup dict {room_id: room_obj}
    rooms_lookup = {}
    for room_def in zone_data.get("rooms", []):
        room_id = room_def["room_id"]
        room_kwargs = {k: v for k, v in room_def.items() if k != "room_id"}
        room_obj = area.room(room_id, **room_kwargs)
        rooms_lookup[room_id] = room_obj

    # 5. exits
    for exit_def in zone_data.get("exits", []):
        from_room_id = exit_def["from_room"]
        to_room = exit_def["to"]
        direction = exit_def["direction"]
        exit_kwargs = {k: v for k, v in exit_def.items()
                       if k not in ("from_room", "to", "direction")}

        from_room = rooms_lookup.get(from_room_id)
        if not from_room:
            # from_room not found — skip with warning added to builder
            area._build_warnings.append(
                f"exit: from_room '{from_room_id}' not in this zone's rooms"
            )
            continue

        # to_room: "zone_id:room_id" string = cross-zone, else local lookup
        if isinstance(to_room, str) and ":" in to_room:
            area.exit(from_room, to_room, direction, **exit_kwargs)
        else:
            to_room_obj = rooms_lookup.get(to_room)
            if not to_room_obj:
                area._build_warnings.append(
                    f"exit: to_room '{to_room}' not in this zone's rooms"
                )
                continue
            area.exit(from_room, to_room_obj, direction, **exit_kwargs)

    # 6. spawns
    for spawn_def in zone_data.get("spawns", []):
        room_id = spawn_def["room"]
        mob = spawn_def["mob"]
        room_obj = rooms_lookup.get(room_id)
        if not room_obj:
            area._build_warnings.append(f"spawn: room '{room_id}' not found")
            continue
        spawn_kwargs = {k: v for k, v in spawn_def.items() if k not in ("room", "mob")}
        area.spawn(room_obj, mob, **spawn_kwargs)

    # 7. npcs
    for npc_def in zone_data.get("npcs", []):
        room_id = npc_def["room"]
        npc_id = npc_def["npc_id"]
        room_obj = rooms_lookup.get(room_id)
        if not room_obj:
            area._build_warnings.append(f"npc: room '{room_id}' not found")
            continue
        npc_kwargs = {k: v for k, v in npc_def.items() if k not in ("room", "npc_id")}
        area.npc(room_obj, npc_id, **npc_kwargs)

    # 8. named_mobs
    for nm_def in zone_data.get("named_mobs", []):
        mob_instance_id = nm_def["mob_instance_id"]
        room_id = nm_def["room"]
        room_obj = rooms_lookup.get(room_id)
        if not room_obj:
            area._build_warnings.append(f"named_mob: room '{room_id}' not found")
            continue
        nm_kwargs = {k: v for k, v in nm_def.items() if k not in ("mob_instance_id", "room")}
        area.named_mob(mob_instance_id, room_obj, **nm_kwargs)

    # 9. patrols (mob_key + optional mob placement)
    for patrol_def in zone_data.get("patrols", []):
        mob_key = patrol_def["mob_key"]
        mob_room_id = patrol_def.get("mob_room")
        route_room_ids = patrol_def.get("route_room_ids", [])

        # Place the mob if mob_room is provided
        if mob_room_id:
            mob_room = rooms_lookup.get(mob_room_id)
            if mob_room:
                mob_attrs = patrol_def.get("mob_attrs", {})
                area.mob(mob_key, mob_room, **mob_attrs)

        patrol_kwargs = {k: v for k, v in patrol_def.items()
                         if k not in ("mob_key", "mob_room", "mob_attrs")}
        area.patrol(mob_key, route_room_ids, **patrol_kwargs)

    # 10. triggers — source is a room_id string, area.trigger() resolves it internally
    for trig_def in zone_data.get("triggers", []):
        source_id = trig_def["source"]
        event = trig_def["event"]
        actions = trig_def["actions"]
        trig_kwargs = {k: v for k, v in trig_def.items()
                       if k not in ("source", "event", "actions")}
        area.trigger(source_id, event, actions, **trig_kwargs)

    # 11. custom_commands — target is a room_id string, area.custom_command() resolves it
    for cmd_def in zone_data.get("custom_commands", []):
        target_id = cmd_def["target"]
        key = cmd_def["key"]
        action_dict = cmd_def["action_dict"]
        cmd_kwargs = {k: v for k, v in cmd_def.items()
                      if k not in ("target", "key", "action_dict")}
        area.custom_command(target_id, key, action_dict, **cmd_kwargs)

    # 12. practice_opportunities
    for practice_def in zone_data.get("practice_opportunities", []):
        room_id = practice_def["room"]
        opportunity_id = practice_def["opportunity_id"]
        practice_kwargs = {
            k: v for k, v in practice_def.items()
            if k not in ("room", "opportunity_id")
        }
        area.practice_opportunity(opportunity_id, room_id, **practice_kwargs)

    # 13. flight_points
    for fp_def in zone_data.get("flight_points", []):
        room_id = fp_def["room"]
        point_id = fp_def["point_id"]
        room_obj = rooms_lookup.get(room_id)
        if not room_obj:
            area._build_warnings.append(f"flight_point: room '{room_id}' not found")
            continue
        fp_kwargs = {k: v for k, v in fp_def.items() if k not in ("room", "point_id")}
        area.flight_point(room_obj, point_id, **fp_kwargs)

    # 14. flight_routes
    for fr_def in zone_data.get("flight_routes", []):
        area.flight_route(
            fr_def["point_a_id"],
            fr_def["point_b_id"],
            fr_def["base_fare"],
            fr_def.get("leg_duration", 30),
            fr_def.get("echoes", []),
        )

    # 15. node
    node_def = zone_data.get("node")
    if node_def:
        center_room_id = node_def["center_room"]
        radius = node_def["radius"]
        center_room = rooms_lookup.get(center_room_id)
        if center_room:
            node_kwargs = {k: v for k, v in node_def.items()
                           if k not in ("center_room", "radius")}
            area.node(center_room, radius, **node_kwargs)
        else:
            area._build_warnings.append(f"node: center_room '{center_room_id}' not found")

    # 16. quests
    for quest_def in zone_data.get("quests", []):
        quest_id = quest_def["quest_id"]
        quest_kwargs = {k: v for k, v in quest_def.items() if k != "quest_id"}
        area.quest(quest_id, **quest_kwargs)

    # 17. materials
    for mat_def in zone_data.get("materials", []):
        material = mat_def["material"]
        mat_kwargs = {k: v for k, v in mat_def.items() if k != "material"}
        area.material(material, **mat_kwargs)

    # 18. lore_fragments
    for lf_def in zone_data.get("lore_fragments", []):
        fragment_id = lf_def["fragment_id"]
        room_id = lf_def["room"]
        room_obj = rooms_lookup.get(room_id)
        if not room_obj:
            area._build_warnings.append(f"lore_fragment: room '{room_id}' not found")
            continue
        lf_kwargs = {k: v for k, v in lf_def.items() if k not in ("fragment_id", "room")}
        area.lore_fragment(fragment_id, room_obj, **lf_kwargs)

    return area.build()
