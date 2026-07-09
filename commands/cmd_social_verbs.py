"""Player-facing Social Web verbs."""

from commands.command import Command


class CmdDeny(Command):
    """
    Contest a rumor or claim an NPC already knows about you.

    Usage:
      deny <npc> about me
    """

    key = "deny"
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        from commands.cmd_dialogue import _find_npc_in_room
        from world.social_claim_repair import deny_social_claim

        args = (self.args or "").strip()
        if " about " not in args:
            self.caller.msg("|yUsage: deny <npc> about me|n")
            return

        npc_name, topic_text = args.split(" about ", 1)
        npc_name = npc_name.strip()
        topic_text = topic_text.strip()
        if not npc_name or topic_text.lower() != "me":
            self.caller.msg("|yUsage: deny <npc> about me|n")
            return

        npc = _find_npc_in_room(self.caller, npc_name)
        if not npc:
            self.caller.msg("|rYou don't see anyone by that name here.|n")
            return

        result = deny_social_claim(self.caller, npc, topic_text=topic_text)
        npc_display = getattr(getattr(npc, "db", None), "npc_name", None) or npc.key
        if result.ok:
            self.caller.msg(f"|w{npc_display}|n {result.message}")
        else:
            self.caller.msg(f"|y{result.message}|n")
