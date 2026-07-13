"""
NPC dialogue commands.

CmdTalk     -- greet an NPC, see Standing-tier greeting + dynamic hints
CmdAsk      -- ask an NPC about a specific topic
CmdSay      -- room broadcast + NPC keyword extraction (overrides Evennia default)
CmdTell     -- directed speech to a specific NPC or private tell to a player
CmdAccept   -- accept a pending quest offer
CmdDecline  -- decline a pending quest offer

All commands are thin dispatchers to world/dialogue_engine.py.
No dialogue text lives in this file (anti-pattern per research).
"""

import evennia

from commands.command import Command


# ---------------------------------------------------------------------------
# NPC lookup helper (shared by all commands)
# ---------------------------------------------------------------------------

MAX_DIALOGUE_LENGTH = 500  # Cap player dialogue input to prevent spam/DOS


def _split_ask_target_and_topic(character, args):
    """Resolve an ask target and topic, allowing multi-word NPC names."""
    if " about " in args:
        parts = args.split(" about ", 1)
        npc_name = parts[0].strip()
        topic_text = parts[1].strip()
        if not npc_name or not topic_text:
            return (None, topic_text)
        return (_find_npc_in_room(character, npc_name), topic_text)

    words = args.split()
    if len(words) < 2:
        return (None, "")

    for split_index in range(len(words) - 1, 0, -1):
        npc_name = " ".join(words[:split_index])
        topic_text = " ".join(words[split_index:]).strip()
        npc = _find_npc_in_room(character, npc_name)
        if npc:
            return (npc, topic_text)

    return (None, " ".join(words[1:]).strip())


def _find_npc_in_room(character, npc_name):
    """
    Search room.contents for an NPC matching npc_name.

    Validates typeclass (SoravelonMob with is_npc flag). Case-insensitive,
    partial match accepted (startswith). Returns first match or None.
    """
    if not character.location or not npc_name:
        return None

    from typeclasses.mobs import SoravelonMob

    npc_name_lower = npc_name.strip().lower()

    prefix_match = None
    token_match = None

    for obj in character.location.contents:
        if not isinstance(obj, SoravelonMob) or not obj.db.is_npc:
            continue
        obj_names = [
            (obj.db.npc_name or "").lower(),
            (obj.key or "").lower(),
        ]
        obj_names = [name for name in obj_names if name]

        if any(name == npc_name_lower for name in obj_names):
            return obj
        if prefix_match is None and any(
            name.startswith(npc_name_lower)
            for name in obj_names
        ):
            prefix_match = obj
        if token_match is None and any(
            token.startswith(npc_name_lower)
            for name in obj_names
            for token in name.split()
        ):
            token_match = obj

    return prefix_match or token_match


def _is_tellable_player(target):
    """Return True only for an online player character target."""
    if not target or getattr(getattr(target, "db", None), "is_npc", False):
        return False
    sessions = getattr(target, "sessions", None)
    if not sessions:
        return False
    try:
        return sessions.count() > 0
    except Exception:
        return False


def _find_online_player(player_name):
    """
    Find an online player character by exact or prefix match.

    The search is session-backed so `tell` can reach players outside the room
    without overlapping with NPC lookup rules.
    """
    if not player_name:
        return None

    player_name_lower = player_name.strip().lower()
    sessions = evennia.SESSION_HANDLER.get_sessions()
    seen_ids = set()
    prefix_match = None

    for session in sessions:
        puppet = session.get_puppet()
        if not puppet or puppet.id in seen_ids or not _is_tellable_player(puppet):
            continue

        seen_ids.add(puppet.id)
        player_key = (getattr(puppet, "key", "") or "").lower()
        if player_key == player_name_lower:
            return puppet
        if not prefix_match and player_key.startswith(player_name_lower):
            prefix_match = puppet

    return prefix_match


def _build_quest_oob_payload(npc, quest_data):
    """Build a stable quest payload for OOB updates from dialogue commands."""
    quest_data = quest_data or {}
    npc_db = getattr(npc, "db", None)
    fallback_npc = quest_data.get("quest_giver", "")
    return {
        "event": "accepted",
        "quest_id": quest_data.get("quest_id") or quest_data.get("id") or "",
        "quest_name": quest_data.get("name", "a task"),
        "npc_id": (
            (getattr(npc_db, "npc_id", None) if npc_db else None)
            or getattr(npc, "key", "")
            or fallback_npc
        ),
        "npc_name": (
            (getattr(npc_db, "npc_name", None) if npc_db else None)
            or getattr(npc, "key", "")
            or fallback_npc
        ),
        "description": quest_data.get("description", ""),
        "objectives": quest_data.get("objectives", []),
    }


# ---------------------------------------------------------------------------
# CmdTalk / greet
# ---------------------------------------------------------------------------


def _quest_offer_display_text(quest_data):
    """Use the bounded renderer result, retaining authored prose as fallback."""
    social_context = (quest_data or {}).get("social_quest_context") or {}
    rendered_offer = social_context.get("rendered_offer") or {}
    speech = rendered_offer.get("speech") if isinstance(rendered_offer, dict) else ""
    if isinstance(speech, str) and speech.strip():
        return speech.strip()
    return (quest_data or {}).get("description", "A mysterious request.")

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
            get_quest_offers,
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

        # Guild recruitment is a local conversation, reconstructed from its
        # durable invitation rather than a remote numeric join screen.
        from world.guild_engine import (
            GUILDS,
            get_recruitment_for_contact,
            get_recruitment_secondary_choices,
        )

        recruitment = get_recruitment_for_contact(character, npc)
        if recruitment:
            guild = GUILDS[recruitment.guild_id]
            choices = get_recruitment_secondary_choices(character, recruitment)
            scores = character.db.domain_scores or {}
            recommended = max(
                choices,
                key=lambda domain: float(scores.get(domain, 0.0)),
                default=None,
            )
            choice_lines = []
            for domain in choices:
                note = " |g(your strongest second path)|n" if domain == recommended else ""
                choice_lines.append(f"  |w{domain}|n{note}")
            character.msg(
                f"\n|y{npc_display} opens the sealed invitation from "
                f"{guild['name']}. The guild recognized what you have done, "
                "but your second path must be named here, face to face.|n\n"
                + "\n".join(choice_lines)
                + "\n|x[Type |waccept <secondary_domain>|x to enter the induction, "
                "or |wdecline|x to leave the invitation open.]|n"
            )
            character.ndb.pending_guild_recruitment = {
                "npc": npc,
                "recruitment_id": recruitment.id,
            }
            return

        # Quest offer
        quest_offers = tuple(get_quest_offers(npc, character) or ())
        if quest_offers:
            quest_data = quest_offers[0]
            pending_offer = {
                "npc": npc,
                "quest": quest_data,
            }
            if len(quest_offers) > 1:
                pending_offer["quests"] = quest_offers
                offer_lines = []
                for index, offer in enumerate(quest_offers, start=1):
                    offer_lines.append(
                        f"|y[{index}] {offer.get('name', 'A task')}|n — "
                        f"{_quest_offer_display_text(offer)}"
                    )
                character.msg(
                    f"\n|y{npc_display} has several leads for you:|n\n"
                    + "\n".join(offer_lines)
                )
                character.msg(
                    "|x[Type |waccept <number>|x to choose a lead or "
                    "|wdecline|x to pass for now]|n"
                )
                character.ndb.pending_quest_offer = pending_offer
                return
            character.msg(
                f"\n|y{npc_display} has a task for you:|n "
                f"{_quest_offer_display_text(quest_data)}"
            )
            character.msg("|x[Type |waccept|x or |wdecline|x]|n")
            character.ndb.pending_quest_offer = pending_offer


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
            is_social_explanation_topic,
            record_topic_learned,
            resolve_social_explanation,
            resolve_topic_response,
            _build_dialogue_context,
        )

        character = self.caller
        args = self.args.strip()[:MAX_DIALOGUE_LENGTH]

        if not args:
            character.msg("|yAsk whom about what? Usage: ask <npc> about <topic>|n")
            return

        npc, topic_text = _split_ask_target_and_topic(character, args)

        if not topic_text:
            character.msg("|yAsk about what? Usage: ask <npc> about <topic>|n")
            return

        if not npc:
            character.msg("|rYou don't see anyone by that name here.|n")
            return

        npc_display = npc.db.npc_name or npc.key

        if is_social_explanation_topic(topic_text):
            context = _build_dialogue_context(npc, character)
            pending_offer = getattr(
                getattr(character, "ndb", None),
                "pending_quest_offer",
                None,
            )
            text = resolve_social_explanation(
                npc,
                character,
                context=context,
                pending_offer=pending_offer,
            )
            character.msg(f"|w{npc_display}|n says, \"{text}\"")
            return

        # Normalize topic via extract_topic for synonym/partial matching
        from world.dialogue_engine import extract_topic
        available_topics = list((npc.db.dialogue_topics or {}).keys())
        topic_key = extract_topic(topic_text, available_topics)

        if topic_key:
            context = _build_dialogue_context(npc, character)
            text, condition = resolve_topic_response(
                npc,
                character,
                topic_key,
                context=context,
            )
            if text:
                character.msg(f"|w{npc_display}|n says, \"{text}\"")
                # Record learned topic
                npc_id = npc.db.npc_id or npc.key or ""
                record_topic_learned(character, npc_id, topic_key, context)
                from world.quest_engine import check_social_interaction_objectives

                check_social_interaction_objectives(
                    character,
                    npc,
                    verb="ask",
                    topic=topic_text,
                )
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
        text = self.args.strip()[:MAX_DIALOGUE_LENGTH]

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

            context = _build_dialogue_context(npc, character)
            response_text, condition = resolve_topic_response(
                npc,
                character,
                topic_key,
                context=context,
            )
            if response_text:
                npc_display = npc.db.npc_name or npc.key
                character.msg(f"\n|w{npc_display}|n responds, \"{response_text}\"")
                # Record learned
                npc_id = npc.db.npc_id or npc.key or ""
                record_topic_learned(character, npc_id, topic_key, context)
                responses += 1


# ---------------------------------------------------------------------------
# CmdTell
# ---------------------------------------------------------------------------

class CmdTell(Command):
    """
    Speak directly to a specific NPC or privately message a player.

    Usage:
      tell <npc> <text>
      tell <player> <message>
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
            character.msg("|yTell whom? Usage: tell <npc|player> <text>|n")
            return

        args = args[:MAX_DIALOGUE_LENGTH]
        parts = args.split(None, 1)
        target_name = parts[0]
        text = parts[1].strip() if len(parts) > 1 else ""

        if not text:
            character.msg("|yTell whom what? Usage: tell <npc|player> <text>|n")
            return

        npc = _find_npc_in_room(character, target_name)
        if npc:
            npc_display = npc.db.npc_name or npc.key

            # Broadcast the tell
            character.msg(f'You tell {npc_display}, "{text}"')

            # Extract topic from speech
            available_topics = list((npc.db.dialogue_topics or {}).keys())
            topic_key = extract_topic(text, available_topics)

            if topic_key:
                context = _build_dialogue_context(npc, character)
                response_text, condition = resolve_topic_response(
                    npc,
                    character,
                    topic_key,
                    context=context,
                )
                if response_text:
                    character.msg(f"|w{npc_display}|n says, \"{response_text}\"")
                    npc_id = npc.db.npc_id or npc.key or ""
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
            return

        player = _find_online_player(target_name)
        if player:
            if player == character:
                character.msg("|yYou mutter to yourself.|n")
                return

            character.msg(f'|mYou tell {player.key}, "{text}"|n')
            player.msg(f'|m{character.key} tells you, "{text}"|n')
            return

        character.msg(
            "|rYou don't see anyone by that name here, and no online player "
            "matches it.|n"
        )


# ---------------------------------------------------------------------------
# CmdAccept
# ---------------------------------------------------------------------------

class CmdAccept(Command):
    """
    Accept a pending quest offer from an NPC.

    Usage:
      accept [number]
    """

    key = "accept"
    locks = "cmd:all()"
    help_category = "Dialogue"

    def func(self):
        character = self.caller
        guild_offer = getattr(character.ndb, "pending_guild_recruitment", None)
        if guild_offer:
            npc = guild_offer.get("npc")
            if npc is None or npc.location != character.location:
                character.msg(
                    "|rThe guild contact is no longer here. Speak with them again in person.|n"
                )
                character.ndb.pending_guild_recruitment = None
                return
            secondary_domain = self.args.strip().lower()
            if not secondary_domain:
                character.msg(
                    "|yName your second path with |waccept <secondary_domain>|y.|n"
                )
                return

            from world.guild_engine import complete_recruitment_induction
            from world.models import GuildRecruitment

            try:
                recruitment = GuildRecruitment.objects.get(
                    pk=guild_offer.get("recruitment_id"),
                    character=character,
                )
            except GuildRecruitment.DoesNotExist:
                character.msg("|rThat invitation is no longer available.|n")
                character.ndb.pending_guild_recruitment = None
                return

            success, message = complete_recruitment_induction(
                character,
                recruitment,
                secondary_domain,
                npc,
            )
            if not success:
                character.msg(f"|y{message}|n")
                return

            from world.guild_engine import GUILDS, SUBCLASSES

            guild = GUILDS[recruitment.guild_id]
            subclass = SUBCLASSES.get(character.db.subclass_id, {})
            npc_display = npc.db.npc_name or npc.key
            character.msg(
                f"|g{npc_display} witnesses your induction into {guild['name']}. "
                f"Your joined path is {subclass.get('name', character.db.subclass_id)}. "
                "The choice is recorded here, and the guild now answers you in kind.|n"
            )
            character.ndb.pending_guild_recruitment = None
            return

        offer = character.ndb.pending_quest_offer

        if not offer:
            character.msg("|yThere's nothing to accept right now.|n")
            return

        npc = offer.get("npc")
        quest_data = offer.get("quest")
        quest_options = offer.get("quests")
        if isinstance(quest_options, (list, tuple)) and quest_options:
            if len(quest_options) == 1:
                quest_data = quest_options[0]
            else:
                choice_text = self.args.strip()
                if not choice_text:
                    character.msg(
                        "|yChoose a lead with |waccept <number>|y, or "
                        "|wdecline|y to pass for now.|n"
                    )
                    return
                try:
                    choice = int(choice_text)
                except ValueError:
                    choice = 0
                if choice < 1 or choice > len(quest_options):
                    character.msg("|yThat is not one of the available leads.|n")
                    return
                quest_data = quest_options[choice - 1]

        # Validate NPC still in same room (Pitfall 4)
        # Chain offers from quest completion may have npc=None — skip room check
        if npc is not None and npc.location != character.location:
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

        quest_name = quest_data.get("name", "a task") if quest_data else "a task"
        if npc is not None:
            npc_display = npc.db.npc_name or npc.key
            character.msg(
                f"|g{npc_display} nods. "
                f"\"Then it's settled. I'm counting on you.\"|n\n"
                f"|g[Quest accepted: {quest_name}]|n"
            )
        else:
            character.msg(
                "|gThe next lead is yours before the trail goes cold.|n\n"
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
        guild_offer = getattr(character.ndb, "pending_guild_recruitment", None)
        if guild_offer:
            npc = guild_offer.get("npc")
            npc_display = "The contact" if not npc else (npc.db.npc_name or npc.key)
            character.msg(
                f"|y{npc_display} closes the letter without tearing it. "
                "The invitation remains open; return when you are ready to choose.|n"
            )
            character.ndb.pending_guild_recruitment = None
            return

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
