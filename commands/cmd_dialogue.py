"""
NPC dialogue commands.

CmdTalk     -- greet an NPC, see Standing-tier greeting + dynamic hints
CmdAsk      -- ask an NPC about a specific topic
CmdSay      -- room broadcast + NPC keyword extraction (overrides Evennia default)
CmdTell     -- directed speech to a specific NPC
CmdAccept   -- accept a pending quest offer
CmdDecline  -- decline a pending quest offer

All commands are thin dispatchers to world/dialogue_engine.py.
No dialogue text lives in this file (anti-pattern per research).
"""

from commands.command import Command


# ---------------------------------------------------------------------------
# NPC lookup helper (shared by all commands)
# ---------------------------------------------------------------------------

def _find_npc_in_room(character, npc_name):
    """
    Search room.contents for an NPC matching npc_name.

    Looks for objects with db.is_npc == True. Case-insensitive,
    partial match accepted (startswith). Returns first match or None.
    """
    if not character.location or not npc_name:
        return None

    npc_name_lower = npc_name.strip().lower()

    for obj in character.location.contents:
        if not obj.db.is_npc:
            continue
        obj_name = (obj.db.npc_name or obj.key or "").lower()
        if obj_name == npc_name_lower:
            return obj
        if obj_name.startswith(npc_name_lower):
            return obj

    return None


def _build_quest_oob_payload(npc, quest_data):
    """Build a stable quest payload for OOB updates from dialogue commands."""
    quest_data = quest_data or {}
    return {
        "event": "accepted",
        "quest_id": quest_data.get("quest_id") or quest_data.get("id") or "",
        "quest_name": quest_data.get("name", "a task"),
        "npc_id": getattr(npc.db, "npc_id", None) or getattr(npc, "key", ""),
        "npc_name": getattr(npc.db, "npc_name", None) or getattr(npc, "key", ""),
        "description": quest_data.get("description", ""),
        "objectives": quest_data.get("objectives", []),
    }


# ---------------------------------------------------------------------------
# CmdTalk / greet
# ---------------------------------------------------------------------------

class CmdTalk(Command):
    """
    Greet an NPC and hear what they have to say.

    Usage:
      talk <npc>
      greet <npc>

    Shows a Standing-tier greeting and available conversation topics.
    """

    key = "talk"
    aliases = ["greet"]
    locks = "cmd:all()"
    help_category = "Dialogue"

    def func(self):
        from world.dialogue_engine import (
            get_npc_hints,
            get_quest_offer,
            has_available_quest,
            resolve_greeting,
        )

        character = self.caller
        npc_name = self.args.strip()

        if not npc_name:
            character.msg("|yTalk to whom? Usage: talk <npc>|n")
            return

        npc = _find_npc_in_room(character, npc_name)
        if not npc:
            character.msg("|rYou don't see anyone by that name here.|n")
            return

        # Greeting
        greeting_text, tier = resolve_greeting(npc, character)
        npc_display = npc.db.npc_name or npc.key
        character.msg(f"|w{npc_display}|n says, \"{greeting_text}\"")

        # Hints
        hints = get_npc_hints(npc, character)
        if hints:
            hint_parts = [f"ask about |w{h}|n" for h in hints]
            hint_str = "|x, ".join(hint_parts)
            character.msg(f"|x[Try: {hint_str}|x]|n")

        # Quest progress: talk_to and deliver objectives (D-11, D-10, D-19)
        from world.quest_engine import check_talk_to_objectives, check_deliver_objectives
        check_talk_to_objectives(character, npc)
        check_deliver_objectives(character, npc)

        # Quest offer
        if has_available_quest(npc, character):
            quest_data = get_quest_offer(npc, character)
            if quest_data:
                character.msg(
                    f"\n|y{npc_display} has a task for you:|n "
                    f"{quest_data.get('description', 'A mysterious request.')}"
                )
                character.msg("|x[Type |waccept|x or |wdecline|x]|n")
                character.ndb.pending_quest_offer = {
                    "npc": npc,
                    "quest": quest_data,
                }


# ---------------------------------------------------------------------------
# CmdAsk
# ---------------------------------------------------------------------------

class CmdAsk(Command):
    """
    Ask an NPC about a specific topic.

    Usage:
      ask <npc> about <topic>
      ask <npc> <topic>
    """

    key = "ask"
    locks = "cmd:all()"
    help_category = "Dialogue"

    def func(self):
        from world.dialogue_engine import (
            record_topic_learned,
            resolve_topic_response,
            _build_dialogue_context,
        )

        character = self.caller
        args = self.args.strip()

        if not args:
            character.msg("|yAsk whom about what? Usage: ask <npc> about <topic>|n")
            return

        # Parse: split on " about " first, then fall back to first_word rest
        if " about " in args:
            parts = args.split(" about ", 1)
            npc_name = parts[0].strip()
            topic_text = parts[1].strip()
        else:
            parts = args.split(None, 1)
            npc_name = parts[0]
            topic_text = parts[1].strip() if len(parts) > 1 else ""

        if not topic_text:
            character.msg("|yAsk about what? Usage: ask <npc> about <topic>|n")
            return

        npc = _find_npc_in_room(character, npc_name)
        if not npc:
            character.msg("|rYou don't see anyone by that name here.|n")
            return

        # Normalize topic via extract_topic for synonym/partial matching
        from world.dialogue_engine import extract_topic
        available_topics = list((npc.db.dialogue_topics or {}).keys())
        topic_key = extract_topic(topic_text, available_topics)

        npc_display = npc.db.npc_name or npc.key

        if topic_key:
            text, condition = resolve_topic_response(npc, character, topic_key)
            if text:
                character.msg(f"|w{npc_display}|n says, \"{text}\"")
                # Record learned topic
                npc_id = npc.db.npc_id or npc.key or ""
                context = _build_dialogue_context(npc, character)
                record_topic_learned(character, npc_id, topic_key, context)
                return

        # No topic match — show fallback with available topics
        if available_topics:
            topics_str = ", ".join(f"|w{t}|n" for t in available_topics[:6])
            character.msg(
                f"|y{npc_display} tilts their head. "
                f"\"I'm not sure what you mean.\"|n\n"
                f"|x[Available topics: {topics_str}|x]|n"
            )
        else:
            character.msg(
                f"|y{npc_display} tilts their head. "
                f"\"I'm not sure what you mean.\"|n"
            )


# ---------------------------------------------------------------------------
# CmdSay (overrides Evennia default)
# ---------------------------------------------------------------------------

class CmdSay(Command):
    """
    Speak to the room. NPCs may respond to keywords in your speech.

    Usage:
      say <text>
      '<text>
      "<text>
    """

    key = "say"
    aliases = ["'", '"']
    locks = "cmd:all()"
    help_category = "Dialogue"

    def func(self):
        from world.dialogue_engine import (
            extract_topic,
            get_standing_tier,
            record_topic_learned,
            resolve_topic_response,
            _build_dialogue_context,
        )

        character = self.caller
        text = self.args.strip()

        if not text:
            character.msg("|ySay what?|n")
            return

        # Normal room broadcast
        character.location.msg_contents(
            f'{character.key} says, "{text}"',
            exclude=[character],
        )
        character.msg(f'You say, "{text}"')

        # NPC keyword extraction — find NPCs in room
        if not character.location:
            return

        npcs = []
        for obj in character.location.contents:
            if obj.db.is_npc:
                npcs.append(obj)

        if not npcs:
            return

        # Sort by standing tier (friendlier first)
        tier_order = {
            "exalted": 0, "honored": 1, "friendly": 2,
            "acknowledged": 3, "neutral": 4, "unfriendly": 5,
            "hostile": 6, "betrayal": 7,
        }

        def _tier_sort_key(npc_obj):
            tier = get_standing_tier(character, npc_obj)
            return tier_order.get(tier, 4)

        npcs.sort(key=_tier_sort_key)

        # Cap at 2 responding NPCs
        responses = 0
        for npc in npcs:
            if responses >= 2:
                break

            available_topics = list((npc.db.dialogue_topics or {}).keys())
            if not available_topics:
                continue

            topic_key = extract_topic(text, available_topics)
            if not topic_key:
                continue

            response_text, condition = resolve_topic_response(
                npc, character, topic_key
            )
            if response_text:
                npc_display = npc.db.npc_name or npc.key
                character.msg(f"\n|w{npc_display}|n responds, \"{response_text}\"")
                # Record learned
                npc_id = npc.db.npc_id or npc.key or ""
                context = _build_dialogue_context(npc, character)
                record_topic_learned(character, npc_id, topic_key, context)
                responses += 1


# ---------------------------------------------------------------------------
# CmdTell
# ---------------------------------------------------------------------------

class CmdTell(Command):
    """
    Speak directly to a specific NPC.

    Usage:
      tell <npc> <text>
    """

    key = "tell"
    locks = "cmd:all()"
    help_category = "Dialogue"

    def func(self):
        from world.dialogue_engine import (
            extract_topic,
            record_topic_learned,
            resolve_topic_response,
            _build_dialogue_context,
        )

        character = self.caller
        args = self.args.strip()

        if not args:
            character.msg("|yTell whom? Usage: tell <npc> <text>|n")
            return

        parts = args.split(None, 1)
        npc_name = parts[0]
        text = parts[1].strip() if len(parts) > 1 else ""

        npc = _find_npc_in_room(character, npc_name)
        if not npc:
            character.msg("|rYou don't see anyone by that name here.|n")
            return

        npc_display = npc.db.npc_name or npc.key

        if not text:
            character.msg(f"|yTell {npc_display} what?|n")
            return

        # Broadcast the tell
        character.msg(f'You tell {npc_display}, "{text}"')

        # Extract topic from speech
        available_topics = list((npc.db.dialogue_topics or {}).keys())
        topic_key = extract_topic(text, available_topics)

        if topic_key:
            response_text, condition = resolve_topic_response(
                npc, character, topic_key
            )
            if response_text:
                character.msg(f"|w{npc_display}|n says, \"{response_text}\"")
                npc_id = npc.db.npc_id or npc.key or ""
                context = _build_dialogue_context(npc, character)
                record_topic_learned(character, npc_id, topic_key, context)
                return

        # No topic match — show fallback
        if available_topics:
            topics_str = ", ".join(f"|w{t}|n" for t in available_topics[:6])
            character.msg(
                f"|y{npc_display} tilts their head. "
                f"\"I'm not sure what you mean.\"|n\n"
                f"|x[Available topics: {topics_str}|x]|n"
            )
        else:
            character.msg(
                f"|y{npc_display} nods thoughtfully but says nothing.|n"
            )


# ---------------------------------------------------------------------------
# CmdAccept
# ---------------------------------------------------------------------------

class CmdAccept(Command):
    """
    Accept a pending quest offer from an NPC.

    Usage:
      accept
    """

    key = "accept"
    locks = "cmd:all()"
    help_category = "Dialogue"

    def func(self):
        character = self.caller
        offer = character.ndb.pending_quest_offer

        if not offer:
            character.msg("|yThere's nothing to accept right now.|n")
            return

        npc = offer.get("npc")
        quest_data = offer.get("quest")

        # Validate NPC still in same room (Pitfall 4)
        if not npc or npc.location != character.location:
            character.msg(
                "|rThe one who offered that quest is no longer here.|n"
            )
            character.ndb.pending_quest_offer = None
            return

        # Accept quest via quest engine (D-17)
        from world.quest_engine import accept_quest
        quest_id = quest_data.get("quest_id") if quest_data else None
        if not quest_id:
            character.msg("|rThat quest has no valid identifier.|n")
            character.ndb.pending_quest_offer = None
            return

        success, msg = accept_quest(character, quest_id, quest_data)
        if not success:
            character.msg(f"|r{msg}|n")
            character.ndb.pending_quest_offer = None
            return

        npc_display = npc.db.npc_name or npc.key
        quest_name = quest_data.get("name", "a task") if quest_data else "a task"
        character.msg(
            f"|g{npc_display} nods. "
            f"\"Then it's settled. I'm counting on you.\"|n\n"
            f"|g[Quest accepted: {quest_name}]|n"
        )

        # OOB push for quest accepted
        from world import oob_publisher
        oob_publisher.push_quest_update(
            character,
            _build_quest_oob_payload(npc, quest_data),
        )

        character.ndb.pending_quest_offer = None


# ---------------------------------------------------------------------------
# CmdDecline
# ---------------------------------------------------------------------------

class CmdDecline(Command):
    """
    Decline a pending quest offer from an NPC.

    Usage:
      decline
    """

    key = "decline"
    locks = "cmd:all()"
    help_category = "Dialogue"

    def func(self):
        character = self.caller
        offer = character.ndb.pending_quest_offer

        if not offer:
            character.msg("|yThere's nothing to decline right now.|n")
            return

        npc = offer.get("npc")
        npc_display = "They" if not npc else (npc.db.npc_name or npc.key)
        character.msg(
            f"|y{npc_display} nods slowly. "
            f"\"Perhaps another time, then.\"|n"
        )

        character.ndb.pending_quest_offer = None
