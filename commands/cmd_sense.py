"""
Room atmosphere display command.

CmdSense shows atmospheric text for active room state flags,
using SENSE_DISPLAY descriptions ordered by SENSE_PRIORITY.
"""

from commands.command import Command


class CmdSense(Command):
    """
    Perceive the atmosphere and lingering energies of your surroundings.

    Usage:
      sense
      perceive
      feel
    """

    key = "sense"
    aliases = ["perceive", "feel"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        from world.room_state import (
            get_room_flags,
            SENSE_DISPLAY,
            SENSE_PRIORITY,
            _room_qualifies_as_still,
        )

        room = self.caller.location
        if not room:
            self.caller.msg("You have no sense of your surroundings.")
            return

        flags = get_room_flags(room)

        if not flags:
            # Check if room qualifies as still (no recent activity)
            if _room_qualifies_as_still(room):
                text = SENSE_DISPLAY.get("still", "The room is quiet.")
                self.caller.msg(f"|c{text}|n")
            else:
                self.caller.msg("You sense nothing unusual here.")
            return

        # Show all active flags in SENSE_PRIORITY order, then remaining
        lines = []
        shown = set()
        for flag in SENSE_PRIORITY:
            if flag in flags:
                text = SENSE_DISPLAY.get(flag, f"You sense {flag}.")
                lines.append(f"|c{text}|n")
                shown.add(flag)
        for flag in sorted(flags.keys()):
            if flag not in shown:
                text = SENSE_DISPLAY.get(flag, f"You sense {flag}.")
                lines.append(f"|c{text}|n")

        self.caller.msg("\n".join(lines))
