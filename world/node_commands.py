"""
Node interaction commands.

CmdStabilize (D-51): allows players to slow or reverse node failure
by continuously stabilizing at node_center rooms. Drains stamina over
time (D-09). Breaks on combat or movement (D-10). 5-minute cooldown
between attempts (D-11).
"""

import time

from commands.command import Command
from evennia.utils.search import search_tag


class CmdStabilize(Command):
    """
    Stabilize an unstable node.

    Usage:
        stabilize
        stabilize stop

    Works only in rooms marked as node_center. Begins a continuous
    stabilization that drains stamina over time. Use 'stabilize stop'
    to end stabilization early. Stabilization also breaks automatically
    if you enter combat or leave the room.

    Has a 5-minute cooldown between stabilization attempts.
    """

    key = "stabilize"
    help_category = "Node"

    # Cooldown in seconds (5 minutes) — D-11
    COOLDOWN_SECONDS = 300

    def func(self):
        caller = self.caller
        room = caller.location

        if not room:
            caller.msg("You are nowhere.")
            return

        # Handle "stabilize stop" subcommand
        args = self.args.strip().lower()
        if args == "stop":
            zones = getattr(caller.ndb, 'stabilizing_zones', None)
            if not zones:
                caller.msg("You are not stabilizing anything.")
                return
            from world.node_helpers import stop_stabilization
            for zone_id in list(zones):
                stop_stabilization(caller, zone_id)
            # Set cooldown after stopping (D-11)
            caller.ndb.stabilize_cooldown = (
                time.time() + self.COOLDOWN_SECONDS
            )
            caller.msg("You release your focus. The stabilization ends.")
            return

        # Check room is a node center
        if not room.tags.has("node_center", category="room_type"):
            caller.msg(
                "There is no node to stabilize here. "
                "You must be at a node center."
            )
            return

        # Check not already stabilizing
        stab_zones = getattr(caller.ndb, 'stabilizing_zones', None)
        zone_id = room.db.zone_id
        if stab_zones and zone_id in stab_zones:
            caller.msg("You are already stabilizing this node.")
            return

        # Check cooldown
        cooldown_until = caller.ndb.stabilize_cooldown
        if cooldown_until and time.time() < cooldown_until:
            remaining = int(cooldown_until - time.time())
            minutes = remaining // 60
            seconds = remaining % 60
            caller.msg(
                f"You have stabilized too recently. "
                f"Wait {minutes}m {seconds}s."
            )
            return

        # Find the zone's NodeScript
        if not zone_id:
            caller.msg("This area has no active node.")
            return

        zone_objs = search_tag(zone_id, category="zone_id")
        zone_obj = None
        for obj in zone_objs:
            if obj.tags.has("zone_object", category="object_type"):
                zone_obj = obj
                break

        if not zone_obj:
            caller.msg("This area has no active node.")
            return

        scripts = zone_obj.scripts.get("node_script")
        if not scripts:
            caller.msg("This area has no active node.")
            return

        node_script = scripts[0]

        if node_script.db.failure <= 0:
            caller.msg(
                "The node is already stable. There is nothing to do."
            )
            return

        # Start continuous stabilization
        from world.node_helpers import attempt_stabilization
        success = attempt_stabilization(caller, zone_id)
        if not success:
            return

        # Notify others in the room
        if room:
            room.msg_contents(
                f"|c{caller.key} focuses intently, channeling energy "
                f"into the node.|n",
                exclude=[caller],
            )
