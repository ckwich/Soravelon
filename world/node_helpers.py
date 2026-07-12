"""
Helper functions for the node system.
Define these before implementing the NodeScript — several components depend on them.
"""

import evennia

from world.tag_search import search_objects_by_exact_tag


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
    (player_count, scholar_count, stabilizer_count, stabilizer_list).
    Called every 30 seconds per zone — must be efficient.

    stabilizer_list contains the actual character objects for stabilization
    tick processing in node_failure_tick().
    """
    rooms = search_objects_by_exact_tag(zone_id, "zone_id")
    players = 0
    scholars = 0
    stabilizers = 0
    stabilizer_list = []
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
                stabilizer_list.append(obj)
    return players, scholars, stabilizers, stabilizer_list


# Legacy wrappers — kept for any external callers (use indices [0:3])
def count_players_in_zone(zone_id):
    """Count characters currently in any room of this zone."""
    players, _, _, _ = count_zone_actors(zone_id)
    return players


def count_scholars_studying(zone_id):
    """Returns 0. Scholar tracking deferred to Milestone 2."""
    _, scholars, _, _ = count_zone_actors(zone_id)
    return scholars


def count_active_stabilizers(zone_id):
    """Returns 0. Stabilizer tracking deferred to Milestone 2."""
    _, _, stabilizers, _ = count_zone_actors(zone_id)
    return stabilizers


def attempt_stabilization(character, zone_id):
    """
    Start continuous stabilization of a zone node.

    Requires stamina > 0 to begin. Drains 5 stamina per tick via
    stabilization_tick(). Stops automatically at 0 stamina.
    Breaks on combat entry or room movement (see break_stabilization_*).
    """
    # Check stamina requirement
    if (getattr(character.ndb, 'stamina', None) or 0) <= 0:
        character.msg("You lack the stamina to stabilize.")
        return False

    script = get_node_script(zone_id)
    if not script:
        return False
    if not hasattr(character.ndb, "stabilizing_zones"):
        character.ndb.stabilizing_zones = set()
    character.ndb.stabilizing_zones.add(zone_id)
    character.msg(
        "You focus on the patterns in the stone, working against "
        "the instability."
    )
    return True


def stop_stabilization(character, zone_id):
    """Called when a character stops stabilizing."""
    if hasattr(character.ndb, "stabilizing_zones"):
        character.ndb.stabilizing_zones.discard(zone_id)


def stabilization_tick(character, zone_id):
    """
    Per-tick stamina drain for active stabilizers. Called every 30s
    from node_failure_tick() for each stabilizer in the zone.

    Drains 5 stamina per tick. Auto-stops at 0 stamina (D-09/D-12).
    """
    current_stamina = getattr(character.ndb, 'stamina', None) or 0
    character.ndb.stamina = max(0, current_stamina - 5)
    if character.ndb.stamina <= 0:
        stop_stabilization(character, zone_id)
        character.msg("Your concentration wavers. The stabilization fades.")


def break_stabilization_on_combat(character):
    """
    Break all active stabilizations when combat begins (D-10).

    Integration point: called by Character typeclass or CombatScript
    when the character enters combat. The caller is responsible for
    invoking this function — this module only provides it.
    """
    zones = getattr(character.ndb, 'stabilizing_zones', None)
    if zones:
        for zone_id in list(zones):
            stop_stabilization(character, zone_id)
        character.msg("Your focus breaks as combat begins.")


def break_stabilization_on_move(character):
    """
    Break all active stabilizations when the character moves rooms (D-10).

    Integration point: called by Character.at_pre_move() or similar
    hook when the character changes rooms. The caller is responsible
    for invoking this function — this module only provides it.
    """
    zones = getattr(character.ndb, 'stabilizing_zones', None)
    if zones:
        for zone_id in list(zones):
            stop_stabilization(character, zone_id)
        character.msg("Your focus breaks.")


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
        players, scholars, stabilizers, stabilizer_list = count_zone_actors(
            zone_id
        )
        script.receive_tick(players, scholars, stabilizers)

        # Drain stamina for each active stabilizer (D-09)
        for stabilizer in stabilizer_list:
            stabilization_tick(stabilizer, zone_id)


def initialize_node_pool():
    """
    On server start, recover orphaned active Layer 1 rooms.
    Idempotent — safe to call on every server start.
    """
    orphaned = search_objects_by_exact_tag("active", "node_layer")
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
