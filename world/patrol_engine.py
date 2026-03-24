"""
Patrol engine for Soravelon.

Provides BFS pathfinding for patrol routes, route stepping with wrap-around,
patrol encounter checks against player characters, and zone-wide echo for
announcement of patrol mob movement.

Key functions:
    find_path(start_room, target_room, max_depth=20)
    next_patrol_step(mob, route_ids, current_index)
    check_patrol_encounter(mob, room)
    echo_to_radius(mob, message, radius)
"""

import evennia
from world.mob_disposition import get_mob_behavior  # noqa: F401 — imported here for test patching


def find_path(start_room, target_room, max_depth=20):
    """
    BFS from start_room to target_room, respecting zone boundaries.

    Returns a list of rooms from start_room to target_room (inclusive),
    or [] if no path exists within max_depth or across zone boundaries.

    Same BFS traversal as get_rooms_in_radius() in node_helpers, but with
    target termination and parent-pointer backtracking.

    Args:
        start_room: Evennia Room object to start from.
        target_room: Evennia Room object to reach.
        max_depth (int): Maximum BFS depth to search (default 20).

    Returns:
        list: Path from start_room to target_room, or [] if not found.
    """
    if start_room == target_room:
        return [start_room]

    zone_id = start_room.db.zone_id

    # parent dict: room → parent room (None for start)
    visited = {start_room: None}
    frontier = [start_room]

    for _ in range(max_depth):
        next_frontier = []
        for room in frontier:
            for exit_obj in room.exits:
                destination = exit_obj.destination
                if not destination or destination in visited:
                    continue
                # Zone boundary: only traverse within same zone_id
                dest_zone = destination.db.zone_id
                if dest_zone != zone_id:
                    continue
                visited[destination] = room
                if destination == target_room:
                    # Backtrack to reconstruct path
                    path = []
                    current = target_room
                    while current is not None:
                        path.append(current)
                        current = visited[current]
                    path.reverse()
                    return path
                next_frontier.append(destination)
        frontier = next_frontier
        if not frontier:
            break

    return []


def next_patrol_step(mob, route_ids, current_index):
    """
    Return the next room in the patrol route and its index.

    Wraps around: after the last room, returns route[0].

    Args:
        mob: The patrol mob (unused currently, reserved for future hooks).
        route_ids (list): List of room dbref integers (e.g., [123, 124, 125]).
        current_index (int): Current position in the route.

    Returns:
        tuple: (room_object, next_index) where room_object is the next room
               or None if route is empty or room not found.
    """
    if not route_ids:
        return (None, current_index)

    next_index = (current_index + 1) % len(route_ids)
    room_id = route_ids[next_index]

    results = evennia.search_object(f"#{room_id}", exact=True)
    if not results:
        return (None, current_index)

    return (results[0], next_index)


def check_patrol_encounter(mob, room):
    """
    Check if the patrol mob should engage any player character in the room.

    Returns True if combat should be initiated, False otherwise.

    Checks:
    1. If mob.db.combat_enabled is False → always False (D-03).
    2. If no player characters in room → False.
    3. For each player: if behavior is "aggressive" or "territorial" → True.
    4. If all players are "passive" or "friendly" → False.

    Args:
        mob: SoravelonMob object.
        room: Evennia Room object to check.

    Returns:
        bool: True if mob should initiate combat with any player.
    """
    if not mob.db.combat_enabled:
        return False

    for obj in room.contents:
        if not (hasattr(obj, 'account') and obj.account):
            continue
        behavior = get_mob_behavior(mob, obj)
        if behavior in ("aggressive", "territorial"):
            return True

    return False


def echo_to_radius(mob, message, radius):
    """
    Broadcast a message to all rooms within radius exits of mob's location.

    Uses BFS from mob's current room via get_rooms_in_radius().
    Used by PatrolScript for zone-wide patrol movement echoes (D-04).

    Args:
        mob: The mob whose location is the BFS center.
        message (str): Message to broadcast.
        radius (int): BFS radius in exits.
    """
    if not mob.location or radius <= 0:
        return

    from world.node_helpers import get_rooms_in_radius

    rooms = get_rooms_in_radius(mob.location, radius)
    for room in rooms:
        room.msg_contents(message)
