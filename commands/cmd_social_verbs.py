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


def _find_social_npc(character, npc_name):
    from commands.cmd_dialogue import _find_npc_in_room

    npc = _find_npc_in_room(character, npc_name)
    if not npc:
        character.msg("|rYou don't see anyone by that name here.|n")
    return npc


def _split_npc_about(character, args, usage):
    if " about " not in args:
        character.msg(f"|yUsage: {usage}|n")
        return None, ""
    npc_name, topic = args.split(" about ", 1)
    npc_name = npc_name.strip()
    topic = topic.strip()
    if not npc_name or not topic:
        character.msg(f"|yUsage: {usage}|n")
        return None, ""
    return _find_social_npc(character, npc_name), topic


def _respond_to_social_topic(character, npc, topic):
    """Require an authored NPC topic before an interaction can advance."""
    from world.dialogue_engine import (
        _build_dialogue_context,
        extract_topic,
        resolve_topic_response,
    )

    available_topics = list((npc.db.dialogue_topics or {}).keys())
    topic_key = extract_topic(topic, available_topics)
    if not topic_key:
        return False
    context = _build_dialogue_context(npc, character)
    text, _condition = resolve_topic_response(
        npc,
        character,
        topic_key,
        context=context,
    )
    if not text:
        return False
    npc_display = npc.db.npc_name or npc.key
    character.msg(f"|w{npc_display}|n says, \"{text}\"")
    return True


class CmdProtect(Command):
    """Make a visible protection action for an NPC in the room.

    Usage:
      protect <npc>
    """

    key = "protect"
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        from world.quest_engine import check_social_interaction_objectives

        npc_name = (self.args or "").strip()
        if not npc_name:
            self.caller.msg("|yUsage: protect <npc>|n")
            return
        npc = _find_social_npc(self.caller, npc_name)
        if not npc:
            return
        matched = check_social_interaction_objectives(
            self.caller,
            npc,
            verb="protect",
        )
        npc_display = npc.db.npc_name or npc.key
        if matched:
            self.caller.msg(
                f"|wYou make your protection of {npc_display} visible.|n"
            )
        else:
            self.caller.msg(
                f"|yThere is no immediate protection action for {npc_display}.|n"
            )


class CmdConfront(Command):
    """Confront an NPC about an authored Social Web topic.

    Usage:
      confront <npc> about <topic>
    """

    key = "confront"
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        from world.quest_engine import check_social_interaction_objectives

        npc, topic = _split_npc_about(
            self.caller,
            (self.args or "").strip(),
            "confront <npc> about <topic>",
        )
        if not npc:
            return
        if not _respond_to_social_topic(self.caller, npc, topic):
            self.caller.msg("|yThey have no answer to that confrontation.|n")
            return
        check_social_interaction_objectives(
            self.caller,
            npc,
            verb="confront",
            topic=topic,
        )


class CmdReport(Command):
    """Report authored evidence to an NPC who can act on it.

    Usage:
      report <npc> about <evidence>
    """

    key = "report"
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        from world.quest_engine import check_social_interaction_objectives

        npc, evidence = _split_npc_about(
            self.caller,
            (self.args or "").strip(),
            "report <npc> about <evidence>",
        )
        if not npc:
            return
        if not _respond_to_social_topic(self.caller, npc, evidence):
            self.caller.msg("|yThey have no record to receive on that subject.|n")
            return
        check_social_interaction_objectives(
            self.caller,
            npc,
            verb="report",
            evidence=evidence,
        )
