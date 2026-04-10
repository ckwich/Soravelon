"""
Helper functions for the node system.
Define these before implementing the NodeScript — several components depend on them.
"""

import evennia


def get_node_script(zone_id):
    """
    Retrieve the NodeScript for a given zone_id.
    Uses ScriptDB tag search — never scans all objects.
    """
    from evennia.scripts.models import ScriptDB

    scripts = ScriptDB.objects.get_by_tag(
        "node_script", category="script_type"
    )
    for script in scripts:
        if script.obj and script.obj.db.zone_id == zone_id:
            return script
    return None


def get_rooms_in_radius(center_room, radius):
    """
    BFS traversal to find all rooms within `radius` exits of center_room.
    Only traverses exits within the same zone (same zone_id).
    Does not cross zone boundaries.
    """
    if not center_room:
        return []

    visited = {center_room}
    frontier = [center_room]
    zone_id = center_room.db.zone_id

    for _ in range(radius):
        next_frontier = []
        for room in frontier:
            for exit_obj in room.exits:
                destination = exit_obj.destination
                if (destination
                        and destination not in visited
                        and getattr(destination.db, 'zone_id', None) == zone_id):
                    visited.add(destination)
                    next_frontier.append(destination)
        frontier = next_frontier
        if not frontier:
            break

    return list(visited)


def count_zone_actors(zone_id):
    """
    Single-pass count of players, scholars, and stabilizers in a zone.
    One tag search, one pass through room contents. Returns
    (player_count, scholar_count, stabilizer_count).
    Called every 30 seconds per zone — must be efficient.
    """
    rooms = evennia.search_tag(zone_id, category="zone_id")
    players = 0
    scholars = 0
    stabilizers = 0
    for room in rooms:
        for obj in room.contents:
            if not (hasattr(obj, 'account') and obj.account):
                continue
            players += 1
            if getattr(obj.ndb, 'studying_node', False):
                scholars += 1
            stab_zones = getattr(obj.ndb, 'stabilizing_zones', None)
            if stab_zones and zone_id in stab_zones:
                stabilizers += 1
    return players, scholars, stabilizers


# Legacy wrappers — kept for any external callers
def count_players_in_zone(zone_id):
    """Count characters currently in any room of this zone."""
    players, _, _ = count_zone_actors(zone_id)
    return players


def count_scholars_studying(zone_id):
    """STUB — Returns 0 until Milestone 2."""
    _, scholars, _ = count_zone_actors(zone_id)
    return scholars


def count_active_stabilizers(zone_id):
    """STUB — Returns 0 until Milestone 2."""
    _, _, stabilizers = count_zone_actors(zone_id)
    return stabilizers


def attempt_stabilization(character, zone_id):
    """
    Register character as active stabilizer. Hook for future abilities.
    """
    script = get_node_script(zone_id)
    if not script:
        return False
    if not hasattr(character.ndb, "stabilizing_zones"):
        character.ndb.stabilizing_zones = set()
    character.ndb.stabilizing_zones.add(zone_id)
    character.msg(
        "You focus on the patterns in the stone, working against "
        "the failure. The air resists."
    )
    return True


def stop_stabilization(character, zone_id):
    """Called when a character stops stabilizing."""
    if hasattr(character.ndb, "stabilizing_zones"):
        character.ndb.stabilizing_zones.discard(zone_id)


def node_failure_tick(*args, **kwargs):
    """
    Global 30-second tick for all node zones.
    One DB write per zone per tick.
    """
    from evennia.scripts.models import ScriptDB

    node_scripts = ScriptDB.objects.get_by_tag(
        "node_script", category="script_type"
    )
    for script in node_scripts:
        zone = script.obj
        if not zone or not zone.db.zone_id:
            continue
        zone_id = zone.db.zone_id
        players, scholars, stabilizers = count_zone_actors(zone_id)
        script.receive_tick(players, scholars, stabilizers)


def initialize_node_pool():
    """
    On server start, recover orphaned active Layer 1 rooms.
    Idempotent — safe to call on every server start.
    """
    orphaned = evennia.search_tag("active", category="node_layer")
    for room in orphaned:
        zone_id = room.db.zone_id
        script = get_node_script(zone_id)

        if not script or not script.db.layer1_active:
            for obj in list(room.contents):
                if hasattr(obj, 'account') and obj.account:
                    layer0_id = obj.db.layer0_room_id
                    if layer0_id:
                        layer0_objs = evennia.search_object(
                            "#" + str(layer0_id)
                        )
                        if layer0_objs:
                            obj.move_to(layer0_objs[0], quiet=True)
                            obj.msg(
                                "The node has quieted. "
                                "You find yourself back where you were."
                            )
                    else:
                        if obj.home:
                            obj.move_to(obj.home, quiet=True)
                    obj.db.layer0_room_id = None

            from world.nodes.node_effects import remove_node_effects
            remove_node_effects(room)
            room.tags.remove("active", category="node_layer")
            room.tags.add("inactive", category="node_layer")
