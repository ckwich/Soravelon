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
