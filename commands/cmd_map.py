"""
ASCII text map command with fog-of-war.

Renders a grid of the current zone centered on the player's position,
showing only rooms the player has previously visited.

Exports:
    CmdMap
"""

from commands.command import Command
from world.tag_search import search_objects_by_exact_tag


class CmdMap(Command):
    """
    Display an ASCII map of the current zone.

    Usage:
      map

    Shows a text grid centered on your current position. Only rooms you
    have previously visited are shown (fog-of-war). Your position is
    marked with |r@|n and visited rooms with |w#|n.
    """

    key = "map"
    locks = "cmd:all()"
    help_category = "General"

    MAP_RADIUS = 10  # show 10 rooms in each direction from current position

    def func(self):
        char = self.caller
        room = char.location
        if not room:
            char.msg("You can't see a map from here.")
            return

        grid_x = room.db.grid_x
        grid_y = room.db.grid_y
        if grid_x is None or grid_y is None:
            char.msg("This area has no mapped coordinates.")
            return

        zone_tag = room.tags.get(category="zone_id")
        if not zone_tag:
            char.msg("This area is unmapped.")
            return

        # Find all rooms in same zone
        zone_rooms = search_objects_by_exact_tag(zone_tag, "zone_id")

        visited = char.db.visited_room_ids or set()

        # Build coordinate map (fog-of-war: only visited rooms)
        coord_map = {}
        for r in zone_rooms:
            rx = r.db.grid_x
            ry = r.db.grid_y
            if rx is None or ry is None:
                continue
            room_tag = r.tags.get(category="room_id")
            if room_tag and room_tag in visited:
                coord_map[(rx, ry)] = r
            elif r == room:
                coord_map[(rx, ry)] = r  # always show current room

        if not coord_map:
            char.msg("No mapped rooms visible.")
            return

        # Determine render bounds centered on player
        radius = self.MAP_RADIUS
        min_x = grid_x - radius
        max_x = grid_x + radius
        min_y = grid_y - radius
        max_y = grid_y + radius

        # Render ASCII grid (y increases downward in display)
        lines = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                if (x, y) in coord_map:
                    r = coord_map[(x, y)]
                    if r == room:
                        row.append("|r@|n")  # current position
                    else:
                        row.append("|w#|n")  # visited room
                else:
                    row.append(" ")  # unknown/fog
            lines.append("".join(row))

        # Trim empty rows from top and bottom
        while lines and lines[0].replace(" ", "") == "":
            lines.pop(0)
        while lines and lines[-1].replace(" ", "") == "":
            lines.pop()

        header = f"|wMap: {zone_tag}|n  (|r@|n = you, |w#|n = visited)"
        char.msg(header + "\n" + "\n".join(lines))
