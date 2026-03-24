"""
FlightRegistry — graph of Dragon Courier flight points and routes.

Module-level singleton. Populated by AreaBuilder at zone build time.
Queried by CmdFly for route planning and fare calculation.

flight_points: {point_id: {"room_id": int, "zone_id": str, "name": str}}
flight_routes: {(point_a_id, point_b_id): {"base_fare": int, "leg_duration": int, "echoes": list}}
               Both directions registered for bidirectional routes.
"""


class _FlightRegistry:
    """
    Singleton flight network graph.

    Populated at server start via AreaBuilder.flight_point() and
    AreaBuilder.flight_route(). Clears on server restart and is rebuilt
    from zone area files (same pattern as ZoneRegistry and NamedMobRegistry).
    """

    def __init__(self):
        self.flight_points = {}   # point_id -> dict
        self.flight_routes = {}   # (point_a, point_b) tuple -> route dict

    def register_point(self, point_id, room, name=None):
        """Register a room as a Dragon Courier stop."""
        self.flight_points[point_id] = {
            "room_id": room.id,
            "zone_id": room.db.zone_id,
            "name": name or room.key,
        }

    def register_route(self, point_a_id, point_b_id, base_fare, leg_duration, echoes=None):
        """Register a bidirectional route between two flight points."""
        route = {
            "base_fare": base_fare,
            "leg_duration": leg_duration,  # seconds per leg (D-10: minimum 30)
            "echoes": echoes or [],
        }
        self.flight_routes[(point_a_id, point_b_id)] = route
        self.flight_routes[(point_b_id, point_a_id)] = route  # bidirectional

    def get_point(self, point_id):
        """Return flight point dict or None."""
        return self.flight_points.get(point_id)

    def get_route(self, point_a_id, point_b_id):
        """Return route dict or None if no direct connection."""
        return self.flight_routes.get((point_a_id, point_b_id))

    def connected_points(self, point_id):
        """Return list of point_ids directly reachable from point_id."""
        return [b for (a, b) in self.flight_routes if a == point_id]

    def find_route_legs(self, origin_id, destination_id):
        """
        BFS to find the shortest multi-leg path between two points.

        Returns ordered list of (from_point_id, to_point_id) tuples
        or [] if unreachable or origin == destination.
        """
        if origin_id == destination_id:
            return []
        visited = {origin_id: None}  # point -> parent
        frontier = [origin_id]
        while frontier:
            next_frontier = []
            for current in frontier:
                for neighbor in self.connected_points(current):
                    if neighbor not in visited:
                        visited[neighbor] = current
                        if neighbor == destination_id:
                            # Backtrack to build leg list
                            legs = []
                            cur = destination_id
                            while visited[cur] is not None:
                                legs.append((visited[cur], cur))
                                cur = visited[cur]
                            return list(reversed(legs))
                        next_frontier.append(neighbor)
            frontier = next_frontier
        return []  # unreachable

    def clear(self):
        """Reset registry — used for testing."""
        self.flight_points.clear()
        self.flight_routes.clear()


# Module-level singleton
FlightRegistry = _FlightRegistry()
