"""
Recovery commands: rest, sleep, wake, and medic blessings.

Thin dispatchers to world/recovery_engine.py.
No game logic lives in this file.
"""

from commands.command import Command


class CmdRest(Command):
    """
    Sit down and rest to recover faster.

    Usage:
        rest
        sit

    Resting accelerates HP and stamina regeneration (3% per tick vs 1% passive).
    Interrupted by combat or movement.
    """

    key = "rest"
    aliases = ["sit"]
    locks = "cmd:all()"
    help_category = "Recovery"

    def func(self):
        from world.recovery_engine import set_recovery_state
        ok, msg = set_recovery_state(self.caller, "resting")
        self.caller.msg(msg)


class CmdSleep(Command):
    """
    Lie down and sleep to recover quickly.

    Usage:
        sleep

    Sleep regenerates HP and stamina at 6% per tick (10% if a bed is present).
    While sleeping you cannot see room events. Interrupted by combat or movement.
    """

    key = "sleep"
    locks = "cmd:all()"
    help_category = "Recovery"

    def func(self):
        from world.recovery_engine import set_recovery_state
        ok, msg = set_recovery_state(self.caller, "sleeping")
        self.caller.msg(msg)


class CmdWake(Command):
    """
    Wake up or stand from resting.

    Usage:
        wake
        stand
    """

    key = "wake"
    aliases = ["stand"]
    locks = "cmd:all()"
    help_category = "Recovery"

    def func(self):
        from world.recovery_engine import cancel_recovery
        ok, msg = cancel_recovery(self.caller)
        self.caller.msg(msg)


class CmdBlessing(Command):
    """
    Request a blessing from a medic NPC.

    Usage:
        blessing                - list available blessings
        blessing <type>         - request a specific blessing
        bless <type>

    Blessings cost Scales and have cooldowns. Types:
        heal    - Restore HP to full (20 Scales, 2min cooldown)
        fortify - Defense buff (30 Scales, 2min cooldown)
        vigor   - Offense buff (30 Scales, 2min cooldown)
        purify  - Cleanse all negative effects (40 Scales, 1min cooldown)

    You must be in the same room as a medic NPC.
    """

    key = "blessing"
    aliases = ["bless"]
    locks = "cmd:all()"
    help_category = "Recovery"

    def func(self):
        from world.recovery_engine import apply_blessing, BLESSINGS

        # Find medic NPC in room
        medic = None
        if self.caller.location:
            for obj in self.caller.location.contents:
                if getattr(obj.db, "is_medic", False):
                    medic = obj
                    break

        if not medic:
            self.caller.msg("There is no medic here.")
            return

        blessing_id = self.args.strip().lower() if self.args else ""

        if not blessing_id:
            # List available blessings
            lines = ["|wAvailable Blessings:|n"]
            for bid, bdata in BLESSINGS.items():
                lines.append(
                    f"  |w{bid:<8}|n - {bdata['desc']} "
                    f"({bdata['cost']} Scales, {bdata['cooldown']}s cooldown)"
                )
            lines.append("\nUsage: |wblessing <type>|n")
            self.caller.msg("\n".join(lines))
            return

        ok, msg = apply_blessing(self.caller, medic, blessing_id)
        self.caller.msg(msg)
