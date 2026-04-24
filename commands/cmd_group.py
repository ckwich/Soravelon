"""
Group commands for Soravelon.

CmdGroup — subcommand dispatcher for party management.
"""

import evennia
from commands.command import Command
from world.group_engine import (
    send_group_invite,
    accept_group_invite,
    decline_group_invite,
    leave_group,
    kick_from_group,
    set_loot_mode,
    is_in_group,
    is_group_leader,
    VALID_LOOT_MODES,
    _get_leader,
    _get_group_state,
)


class CmdGroup(Command):
    """
    Manage your adventuring group.

    Usage:
      group                  - show group status
      group invite <player>  - invite a player to your group
      group accept           - accept a pending invite
      group decline          - decline a pending invite
      group leave            - leave your current group
      group kick <player>    - kick a member (leader only)
      group lootmode <mode>  - set loot mode (leader only)

    Valid loot modes: personal, ffa, round_robin
    Alias: party
    """

    key = "group"
    aliases = ["party"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        char = self.caller
        args = self.args.strip().split(None, 1)

        if not args or args[0].lower() == "status":
            self._show_status(char)
            return

        subcmd = args[0].lower()
        rest = args[1].strip() if len(args) > 1 else ""

        if subcmd == "invite":
            if not rest:
                char.msg("Usage: group invite <player>")
                return
            target = char.search(rest)
            if not target:
                return  # search() already msgs on failure
            success, msg = send_group_invite(char, target)
            if msg:
                char.msg(msg)

        elif subcmd == "accept":
            success, msg = accept_group_invite(char)
            if msg:
                char.msg(msg)

        elif subcmd == "decline":
            success, msg = decline_group_invite(char)
            if msg:
                char.msg(msg)

        elif subcmd == "leave":
            success, msg = leave_group(char)
            if msg:
                char.msg(msg)

        elif subcmd == "kick":
            if not rest:
                char.msg("Usage: group kick <player>")
                return
            target = char.search(rest)
            if not target:
                return
            success, msg = kick_from_group(char, target)
            if msg:
                char.msg(msg)

        elif subcmd == "lootmode":
            if not rest:
                char.msg(
                    f"Usage: group lootmode <mode>\n"
                    f"Valid modes: {', '.join(VALID_LOOT_MODES)}"
                )
                return
            success, msg = set_loot_mode(char, rest.lower())
            if msg:
                char.msg(msg)

        else:
            char.msg(
                "Usage: group [invite|accept|decline|leave|kick|lootmode]"
            )

    def _show_status(self, char):
        """Display current group state."""
        if not is_in_group(char):
            char.msg("You are not in a group.")
            return

        leader = _get_leader(char)
        if not leader:
            char.msg("You are not in a group.")
            return

        state = _get_group_state(leader)
        if not state:
            char.msg("You are not in a group.")
            return

        members_text = []
        for mid in state["members"]:
            obj = evennia.search_object("#" + str(mid))
            if obj:
                name = obj[0].key
                if mid == state["leader_id"]:
                    name += " |y(leader)|n"
                members_text.append(name)

        loot_mode = state.get("loot_mode", "personal")
        char.msg(
            f"|wGroup Members:|n {', '.join(members_text)}\n"
            f"|wLoot Mode:|n {loot_mode}"
        )
