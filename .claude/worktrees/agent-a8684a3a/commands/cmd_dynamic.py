"""
Dynamic command builder for AreaBuilder custom_command() definitions.

Provides DynamicAreaCommand and build_dynamic_cmdset() used by
AreaBuilder.custom_command() to attach one-off commands to rooms,
mobs, or items at zone build time.
"""

from commands.command import Command
from evennia.commands.cmdset import CmdSet


class DynamicAreaCommand(Command):
    """A runtime-built command executing an action vocabulary entry."""

    locks = "cmd:all()"
    help_category = "Zone"
    action_dict = {}  # set per-instance by build_dynamic_cmdset()

    def func(self):
        from world.action_vocabulary import execute_action
        context = {"character": self.caller, "room": self.caller.location}
        ok, msg = execute_action(self.action_dict, context)
        if not ok and msg:
            self.caller.msg(msg)


class DynamicAreaCmdSet(CmdSet):
    key = "DynamicAreaCmdSet"
    mergetype = "Union"
    no_exits = False
    no_objs = False


def build_dynamic_cmdset(cmd_def):
    """
    Build a CmdSet containing one DynamicAreaCommand from a cmd_def dict.

    Args:
        cmd_def: dict with keys: key, action_dict, aliases, visible_in_exits, desc

    Returns:
        A DynamicAreaCmdSet instance ready to be added via obj.cmdset.add()
    """
    cmd = DynamicAreaCommand()
    cmd.key = cmd_def["key"]
    cmd.aliases = list(cmd_def.get("aliases", []))
    cmd.action_dict = cmd_def["action_dict"]
    cmdset = DynamicAreaCmdSet()
    cmdset.add(cmd)
    return cmdset
