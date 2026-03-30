"""
Node interaction commands.

CmdStabilize (D-51): allows players to slow or reverse node failure
by interacting at node_center rooms.
"""

import time

from commands.command import Command
from evennia.utils.search import search_tag


class CmdStabilize(Command):
    """
    Attempt to stabilize an unstable node.

    Usage:
        stabilize

    Works only in rooms marked as node_center. Reduces the node's
    failure value, slowing or reversing the failure progression.
    The amount of stabilization scales with your Echoes or Remnance
    domain score.

    Has a 5-minute cooldown between uses.
    """

    key = "stabilize"
    help_category = "Node"

    # Cooldown in seconds (5 minutes)
    COOLDOWN_SECONDS = 300

    # Base and max failure reduction
    BASE_REDUCTION = 5.0
    MAX_REDUCTION = 15.0

    def func(self):
        caller = self.caller
        room = caller.location

        if not room:
            caller.msg("You are nowhere.")
            return

        # Check room is a node center
        if not room.tags.has("node_center", category="room_type"):
            caller.msg(
                "There is no node to stabilize here. "
                "You must be at a node center."
            )
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
        zone_id = room.db.zone_id
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

        # Calculate reduction based on domain scores
        reduction = self.BASE_REDUCTION
        domain_scores = caller.db.domain_scores or {}
        echoes_score = domain_scores.get("echoes", 0)
        remnance_score = domain_scores.get("remnance", 0)
        best_score = max(echoes_score, remnance_score)

        # Scale: every 10 points of domain score adds 1 point of reduction
        reduction += min(best_score / 10.0, self.MAX_REDUCTION - self.BASE_REDUCTION)

        # Apply reduction
        old_failure = node_script.db.failure
        node_script.db.failure = max(0.0, old_failure - reduction)
        actual_reduction = old_failure - node_script.db.failure

        # Set cooldown
        caller.ndb.stabilize_cooldown = time.time() + self.COOLDOWN_SECONDS

        # Feedback
        caller.msg(
            f"|cYou focus your will on the node, pushing back against "
            f"the instability. The failure eases by "
            f"{actual_reduction:.1f} points.|n"
        )

        # Notify others in the room
        if room:
            room.msg_contents(
                f"|c{caller.key} channels energy into the node, "
                f"and the air steadies briefly.|n",
                exclude=[caller],
            )
