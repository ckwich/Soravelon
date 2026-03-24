"""
Dragon Courier flight commands.

CmdFly        — board and book Dragon Courier flights
CmdDisembark  — disembark at an intermediate stop
CmdFlightRoutes — list all discovered Dragon Courier stops
"""

from commands.command import Command


class CmdFly(Command):
    """
    Board the Dragon Courier and travel to a discovered destination.

    Usage:
      fly <destination name>
      fly                      (show available destinations from here)

    You must be at a Dragon Courier stop to book a flight.
    You must have previously discovered the destination stop.
    Fare is deducted before departure. Standing with the Consortium reduces fare.
    """

    key = "fly"
    locks = "cmd:all()"
    help_category = "Travel"

    def func(self):
        character = self.caller

        # Already in flight
        if character.ndb.in_flight:
            character.msg("You are already aboard a Dragon Courier.")
            return

        # Must be at a flight point
        here = character.location
        if not here or not here.db.flight_point_id:
            character.msg("There is no Dragon Courier stop here.")
            return

        origin_id = here.db.flight_point_id

        from world.flight_registry import FlightRegistry

        if not self.args:
            # List available destinations with fare estimates
            discovered = character.db.discovered_flight_points or set()
            reachable = FlightRegistry.connected_points(origin_id)
            available = [pid for pid in reachable if pid in discovered and pid != origin_id]
            if not available:
                character.msg("You have not discovered any destinations reachable from here.")
                return
            from world.flight_engine import fare_for_route
            lines = []
            for pid in sorted(available):
                point = FlightRegistry.get_point(pid)
                name = point["name"] if point else pid
                legs = FlightRegistry.find_route_legs(origin_id, pid)
                fare = fare_for_route(character, legs)
                lines.append(f"  {name:<30} {fare} scales")
            character.msg("Dragon Courier destinations from here:\n" + "\n".join(lines))
            return

        # Find destination by name prefix match (case-insensitive)
        dest_arg = self.args.strip().lower()
        discovered = character.db.discovered_flight_points or set()
        match = None
        for pid in FlightRegistry.flight_points:
            if pid not in discovered:
                continue
            point = FlightRegistry.get_point(pid)
            if point and point["name"].lower().startswith(dest_arg):
                match = pid
                break

        if not match:
            character.msg(
                f"Unknown destination '{self.args.strip()}'. "
                "Type 'fly' to see available destinations."
            )
            return

        from world.flight_engine import book_flight
        ok, msg = book_flight(character, origin_id, match)
        if not ok:
            character.msg(f"Cannot book flight: {msg}")


class CmdDisembark(Command):
    """
    Disembark from the Dragon Courier at the current stop.

    Usage:
      disembark

    Only available while in flight at a stop between legs.
    Ending your journey early forfeits your remaining fare.
    """

    key = "disembark"
    locks = "cmd:all()"
    help_category = "Travel"

    def func(self):
        character = self.caller

        if not character.ndb.in_flight:
            character.msg("You are not aboard a Dragon Courier.")
            return

        scripts = character.scripts.get("flight_script")
        if not scripts:
            # Script gone but flag set — clean up gracefully
            character.ndb.in_flight = False
            character.msg("You step off the courier.")
            return

        scripts[0].do_disembark()


class CmdFlightRoutes(Command):
    """
    Show all Dragon Courier stops you have discovered.

    Usage:
      routes
      flightroutes

    Lists all stops discovered through exploration. Visit a Dragon Courier
    stop to add it to your known network.
    """

    key = "routes"
    aliases = ["flightroutes"]
    locks = "cmd:all()"
    help_category = "Travel"

    def func(self):
        character = self.caller
        from world.flight_registry import FlightRegistry

        discovered = character.db.discovered_flight_points or set()
        if not discovered:
            character.msg("You have not discovered any Dragon Courier stops.")
            return

        lines = ["Dragon Courier stops you have discovered:"]
        for pid in sorted(discovered):
            point = FlightRegistry.get_point(pid)
            name = point["name"] if point else pid
            lines.append(f"  {name}")

        character.msg("\n".join(lines))
