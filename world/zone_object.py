"""
ZoneObject and zone initialization helpers.

The ZoneObject represents a zone in the game. It holds the NodeScript
and manages Layer 1 room creation.
"""

from evennia import create_object, create_script


def initialize_node(zone_obj, node_type, center_room, radius,
                    layer0_rooms, failure_start=0):
    """
    Set up the node system for a zone.
    Creates Layer 1 rooms as real DB objects.
    Returns the NodeScript.

    Args:
        zone_obj: the zone object to attach the script to
        node_type: "resonance"/"thermal"/"cognitive"/"gravity"/"temporal"
        center_room: SoravelonRoom at node center
        radius: int rooms from center affected
        layer0_rooms: list of SoravelonRoom objects needing Layer 1 equivalents
        failure_start: float starting failure % (0-100)
    """
    from typeclasses.rooms import Layer1Room
    from world.scripts.node_script import NodeScript

    zone_obj.db.has_node = True
    zone_obj.db.node_type = node_type

    # Tag zone object with its zone_id for indexed lookup
    if zone_obj.db.zone_id:
        zone_obj.tags.add(zone_obj.db.zone_id, category="zone_id")

    # First pass: create L1 rooms and build L0→L1 mapping
    l0_to_l1 = {}  # L0 room id → L1 room object
    layer1_ids = []
    for layer0_room in layer0_rooms:
        layer1_room = create_object(
            Layer1Room,
            key=f"{layer0_room.key} [Node Active]",
            location=None,
        )
        layer1_room.db.zone_id = zone_obj.db.zone_id
        layer1_room.db.layer0_room_id = layer0_room.id
        layer1_room.db.is_layer1 = True
        layer1_room.db.node_type = node_type
        if zone_obj.db.zone_id:
            layer1_room.tags.add(zone_obj.db.zone_id, category="zone_id")

        layer0_room.db.layer1_room_id = layer1_room.id
        layer1_ids.append(layer1_room.id)
        l0_to_l1[layer0_room.id] = layer1_room

    # Second pass: clone L0 exits into L1 rooms (D-02: created at build time)
    from typeclasses.exits import SoravelonExit
    for layer0_room in layer0_rooms:
        l1_source = l0_to_l1.get(layer0_room.id)
        if not l1_source:
            continue
        for exit_obj in layer0_room.exits:
            dest = exit_obj.destination
            if not dest or dest.id not in l0_to_l1:
                # Only clone exits where both endpoints have L1 counterparts (D-03)
                continue
            l1_dest = l0_to_l1[dest.id]
            l1_exit = create_object(
                SoravelonExit,
                key=exit_obj.key,
                location=l1_source,
                destination=l1_dest,
            )
            l1_exit.tags.add("inactive", category="node_layer")
            if zone_obj.db.zone_id:
                l1_exit.tags.add(zone_obj.db.zone_id, category="zone_id")

    script = create_script(
        NodeScript,
        obj=zone_obj,
        persistent=True,
    )
    script.db.node_type = node_type
    script.db.center_room_id = center_room.id
    script.db.node_radius = radius
    script.db.failure = float(failure_start)
    script.db.state = script._failure_to_state(failure_start)
    script.db.layer1_room_ids = layer1_ids

    return script
