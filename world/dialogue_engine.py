"""
NPC dialogue engine.

Resolves greetings, topic responses, hints, and keyword extraction.
All functions use lazy imports to avoid circular dependencies (Pitfall 6).

NPC dialogue data is stored on db attributes set by AreaBuilder:
  npc.db.dialogue_greeting_tiers  -- dict {tier: text}
  npc.db.dialogue_topics          -- dict {topic_key: {condition: text}}
  npc.db.dialogue_base_hints      -- list of topic keys
  npc.db.dialogue_tier_hints      -- dict {tier: [topic_keys]}
  npc.db.dialogue_quest_hints     -- dict {quest_id: [topic_keys]}
  npc.db.dialogue_network_hints   -- list of topic keys
  npc.db.dialogue_scholar_hints   -- list of topic keys
  npc.db.dialogue_warden_hints    -- list of topic keys
  npc.db.ambient_idle_echoes      -- list of strings
  npc.db.ambient_idle_interval    -- int seconds
  npc.db.ambient_idle_variance    -- int seconds
  npc.db.ambient_reactive_echoes  -- dict {trigger: text}
  npc.db.is_npc                   -- True
  npc.db.faction                  -- faction id string
"""

import hashlib
import logging
import re
import time

from django.db import OperationalError, ProgrammingError

from world.dialogue_definitions import (
    MAX_HINTS_DISPLAYED,
    NETWORK_HINT_THRESHOLD,
    REPUTATION_HINT_THRESHOLD,
    RESPONSE_PRIORITY,
    SOCIAL_CONDITION_PREFIX_PRIORITY,
    STANDING_TIER_THRESHOLDS,
    TOPIC_SYNONYMS,
)


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Standing tier
# ---------------------------------------------------------------------------

def get_standing_tier(character, npc):
    """
    Map NPC disposition toward character to a Standing tier string.

    Checks betrayal first (returns "betrayal" tier). Then maps the
    disposition float from get_mob_disposition() through
    STANDING_TIER_THRESHOLDS. Returns one of 8 strings:
    exalted, honored, friendly, acknowledged, neutral, unfriendly,
    hostile, or betrayal.
    """
    from world.mob_disposition import get_mob_disposition
    from world.world_state import get_betrayal

    npc_faction = npc.db.faction if npc else None
    if npc_faction:
        if get_betrayal(character, npc_faction):
            return "betrayal"

    disposition = get_mob_disposition(npc, character)

    for threshold, tier in STANDING_TIER_THRESHOLDS:
        if disposition >= threshold:
            return tier

    return "hostile"


# ---------------------------------------------------------------------------
# Greeting resolution
# ---------------------------------------------------------------------------

def resolve_greeting(npc, character):
    """
    Select greeting text for NPC based on Standing tier.

    Returns (greeting_text, tier_used). Falls back to "neutral" then
    a generic fallback if the authored tier is missing.
    """
    tier = get_standing_tier(character, npc)
    greetings = npc.db.dialogue_greeting_tiers or {}

    text = greetings.get(tier)
    if text:
        return (text, tier)

    # Fallback: try neutral tier
    text = greetings.get("neutral")
    if text:
        return (text, "neutral")

    # Generic fallback
    npc_name = npc.db.npc_name or npc.key or "The stranger"
    return (f"{npc_name} regards you silently.", "default")


# ---------------------------------------------------------------------------
# Dialogue context
# ---------------------------------------------------------------------------

def _empty_social_context_packet():
    return {
        "viewer": {},
        "subject": {},
        "purpose": "dialogue",
        "facts": [],
        "claims": [],
    }


def _dialogue_node_identifier(value):
    if value is None or isinstance(value, bool):
        return ""
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value.strip()
    return ""


def _npc_social_node_key(npc):
    if not npc:
        return ""
    npc_db = getattr(npc, "db", None)
    npc_id = _dialogue_node_identifier(getattr(npc_db, "npc_id", None))
    if not npc_id:
        npc_id = _dialogue_node_identifier(getattr(npc, "key", None))
    return f"npc:{npc_id}" if npc_id else ""


def _character_social_node_key(character):
    character_id = _dialogue_node_identifier(getattr(character, "id", None))
    return f"player:{character_id}" if character_id else ""


def _build_social_dialogue_context(npc, character):
    viewer_node_key = _npc_social_node_key(npc)
    subject_node_key = _character_social_node_key(character)
    if not viewer_node_key or not subject_node_key:
        return _empty_social_context_packet()

    try:
        from world.social_engine import query_social_context

        return query_social_context(
            viewer_node_key=viewer_node_key,
            subject_node_key=subject_node_key,
            purpose="dialogue",
        )
    except (OperationalError, ProgrammingError):
        # Social Web schema/runtime can be absent during migrations or focused tests.
        logger.warning(
            "Social Web dialogue context unavailable; falling back to empty context.",
            exc_info=True,
        )
        return _empty_social_context_packet()


def _build_dialogue_context(npc, character):
    """
    Build the full context dict for condition evaluation.

    Lazy-imports get_character_context_packet to avoid circular deps.
    Adds quest state and standing tier for condition checks.
    This is the same interface future LLM will consume (NPC-03).
    """
    from world.world_state import get_character_context_packet

    zone = npc.db.zone_id if npc else None
    context = get_character_context_packet(character, npc=npc, zone=zone)

    # Standing tier for condition matching
    context["standing_tier"] = get_standing_tier(character, npc)

    # Quest state — pull from quest_engine
    from world.quest_engine import get_active_quests
    from world.models import CharacterQuest

    active_cqs = get_active_quests(character)
    context["active_quests"] = [cq.quest_id for cq in active_cqs]
    context["completed_quests"] = list(
        CharacterQuest.objects.filter(
            character=character, status="complete"
        ).values_list("quest_id", flat=True)
    )
    context["failed_quests"] = list(
        CharacterQuest.objects.filter(
            character=character, status="failed"
        ).values_list("quest_id", flat=True)
    )
    context["social_context"] = _build_social_dialogue_context(npc, character)
    try:
        from world.social_interpretation import build_social_interpretation

        context["social_interpretation"] = build_social_interpretation(
            _npc_identifier(npc),
            context["social_context"],
        )
    except Exception:
        logger.warning(
            "Social Web interpretation unavailable; falling back to empty packet.",
            exc_info=True,
        )
        context["social_interpretation"] = {}

    return context


def _normalize_social_condition_value(value):
    return str(value or "").strip().lower().replace(" ", "_")


def _social_condition_suffix(condition, prefix):
    return condition[len(prefix):].strip()


def _social_facts(social_context):
    return [
        item for item in (social_context or {}).get("facts", []) or []
        if isinstance(item, dict)
    ]


def _social_claims(social_context):
    return [
        item for item in (social_context or {}).get("claims", []) or []
        if isinstance(item, dict)
    ]


def _check_social_condition(condition, social_context):
    """
    Evaluate generic Social Web condition keys against a bounded packet.

    This intentionally inspects only exact packet fields. It does not scan
    summaries, infer fuzzy matches, call generators, or touch the database.
    """
    if condition.startswith("social_fact:"):
        fact_key = _social_condition_suffix(condition, "social_fact:")
        return any(
            str(fact.get("fact_key") or "") == fact_key
            for fact in _social_facts(social_context)
        )

    if condition.startswith("social_claim:"):
        claim_key = _social_condition_suffix(condition, "social_claim:")
        return any(
            str(claim.get("claim_key") or "") == claim_key
            for claim in _social_claims(social_context)
        )

    if condition.startswith("social_fact_tag:"):
        tag = _normalize_social_condition_value(
            _social_condition_suffix(condition, "social_fact_tag:")
        )
        return any(
            tag in {
                _normalize_social_condition_value(item)
                for item in (fact.get("tags") or [])
            }
            for fact in _social_facts(social_context)
        )

    if condition.startswith("social_fact_event:"):
        event_type = _normalize_social_condition_value(
            _social_condition_suffix(condition, "social_fact_event:")
        )
        return any(
            _normalize_social_condition_value(fact.get("event_type")) == event_type
            for fact in _social_facts(social_context)
        )

    if condition.startswith("social_claim_status:"):
        status = _normalize_social_condition_value(
            _social_condition_suffix(condition, "social_claim_status:")
        )
        return any(
            _normalize_social_condition_value(claim.get("status")) == status
            for claim in _social_claims(social_context)
        )

    if condition.startswith("social_claim_type:"):
        claim_type = _normalize_social_condition_value(
            _social_condition_suffix(condition, "social_claim_type:")
        )
        return any(
            _normalize_social_condition_value(claim.get("claim_type")) == claim_type
            for claim in _social_claims(social_context)
        )

    if condition.startswith("social_claim_trace_edge:"):
        edge_type = _normalize_social_condition_value(
            _social_condition_suffix(condition, "social_claim_trace_edge:")
        )
        for claim in _social_claims(social_context):
            for trace in claim.get("trace") or []:
                if not isinstance(trace, dict):
                    continue
                if _normalize_social_condition_value(trace.get("edge_type")) == edge_type:
                    return True
        return False

    return False


def _is_social_condition(condition):
    return any(
        condition.startswith(prefix)
        for prefix in SOCIAL_CONDITION_PREFIX_PRIORITY
    )


def _iter_social_conditions(topic_data):
    for prefix in SOCIAL_CONDITION_PREFIX_PRIORITY:
        for condition in sorted(
            key
            for key in topic_data
            if isinstance(key, str) and key.startswith(prefix)
        ):
            yield condition


def _resolve_social_topic_response(topic_data, context):
    social_context = (context or {}).get("social_context") or {}
    for condition in _iter_social_conditions(topic_data):
        if _check_social_condition(condition, social_context):
            return (topic_data[condition], condition)
    return (None, None)


SOCIAL_EXPLANATION_TOPICS = {
    "me",
    "myself",
    "why",
    "why me",
    "why trust me",
    "why do you trust me",
    "why are you asking me",
    "why did you ask me",
    "what have you heard about me",
    "what do you know about me",
}

UNSAFE_SOCIAL_TEXT_PATTERNS = (
    re.compile(r"\b(?:fact|claim|npc|player|edge|node):", re.IGNORECASE),
    re.compile(
        r"\b(?:fact_key|claim_key|node_key|edge_key|raw_prompt|model_output)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:provider|admin|hidden lore|confidence)\b", re.IGNORECASE),
    re.compile(r"\b0\.\d+\b"),
)

UNSAFE_SOCIAL_VISIBILITIES = {"private", "admin", "hidden", "secret"}


def _normalize_social_explanation_text(text):
    normalized = str(text or "").strip().lower().replace("?", " ")
    normalized = " ".join(normalized.split())
    if normalized.startswith("about "):
        normalized = normalized[len("about "):].strip()
    return normalized


def is_social_explanation_topic(text):
    """Return True when player input asks for NPC knowledge about the player."""
    return _normalize_social_explanation_text(text) in SOCIAL_EXPLANATION_TOPICS


def _humanize_social_channel(value):
    text = str(value or "").strip().replace("_", " ")
    return " ".join(text.split())


def _is_safe_social_text(value):
    text = str(value or "").strip()
    if not text:
        return False
    return not any(pattern.search(text) for pattern in UNSAFE_SOCIAL_TEXT_PATTERNS)


def _safe_social_text(value):
    text = str(value or "").strip()
    return text if _is_safe_social_text(text) else ""


def _safe_social_evidence(items, *, default_kind):
    evidence = []
    for item in items or []:
        if not isinstance(item, dict):
            continue
        visibility = _normalize_social_condition_value(item.get("visibility"))
        if visibility in UNSAFE_SOCIAL_VISIBILITIES:
            continue

        summary = _safe_social_text(item.get("summary"))
        if not summary:
            continue
        channel = _humanize_social_channel(item.get("channel"))
        if channel and not _is_safe_social_text(channel):
            continue
        evidence.append(
            {
                "kind": str(item.get("kind") or default_kind),
                "summary": summary,
                "channel": channel,
                "status": str(item.get("status") or "").strip(),
            }
        )
    return evidence


def _evidence_from_social_context(social_context):
    return (
        _safe_social_evidence((social_context or {}).get("facts"), default_kind="fact")
        + _safe_social_evidence(
            (social_context or {}).get("claims"),
            default_kind="claim",
        )
    )


def _npc_identifier(npc):
    npc_db = getattr(npc, "db", None)
    return (
        _dialogue_node_identifier(getattr(npc_db, "npc_id", None))
        or _dialogue_node_identifier(getattr(npc, "key", None))
    )


def _pending_offer_explainability_for_npc(npc, pending_offer):
    if not isinstance(pending_offer, dict):
        return {}

    quest = pending_offer.get("quest") or {}
    if not isinstance(quest, dict):
        return {}

    offer_npc = pending_offer.get("npc")
    quest_giver = _dialogue_node_identifier(quest.get("quest_giver"))
    if offer_npc is not npc and quest_giver != _npc_identifier(npc):
        return {}

    social_quest_context = quest.get("social_quest_context") or {}
    explainability = social_quest_context.get("offer_explainability") or {}
    return explainability if isinstance(explainability, dict) else {}


def _format_social_explanation(*, summary="", reason="", evidence=None):
    evidence = list(evidence or [])[:2]
    pieces = []
    summary = _safe_social_text(summary)
    reason = _safe_social_text(reason)

    if summary:
        pieces.append(summary)
    if reason and reason != summary:
        pieces.append(reason)

    if evidence:
        evidence_parts = []
        for item in evidence:
            item_summary = item.get("summary", "")
            channel = item.get("channel", "")
            if channel:
                evidence_parts.append(f"Through {channel}: {item_summary}")
            else:
                evidence_parts.append(item_summary)
        pieces.append("What I can point to is this: " + " ".join(evidence_parts))

    if not pieces:
        return "I have heard nothing I can fairly speak to."

    pieces.append("That shapes how I speak with you.")
    return " ".join(pieces)


def resolve_social_explanation(npc, character, *, context=None, pending_offer=None):
    """
    Build a player-safe explanation of what this NPC can say about the player.

    The response is diegetic and bounded to Social Web summaries/reasons. It
    intentionally omits raw fact keys, claim keys, node ids, traces, confidence
    scores, prompts, model output, and withheld implications.
    """
    if context is None:
        context = _build_dialogue_context(npc, character)

    offer_explainability = _pending_offer_explainability_for_npc(npc, pending_offer)
    if offer_explainability:
        return _format_social_explanation(
            summary=offer_explainability.get("summary", ""),
            reason=offer_explainability.get("npc_safe_reason", ""),
            evidence=_safe_social_evidence(
                offer_explainability.get("evidence"),
                default_kind="evidence",
            ),
        )

    social_context = (context or {}).get("social_context") or {}
    return _format_social_explanation(
        evidence=_evidence_from_social_context(social_context),
    )


def _check_condition(condition, context):
    """
    Evaluate a single condition string against the dialogue context.

    Returns True if the condition is met, False otherwise.
    """
    if condition == "default":
        return True

    if condition == "betrayal":
        return bool(context.get("betrayal_flag"))

    if _is_social_condition(condition):
        return _check_social_condition(condition, context.get("social_context") or {})

    # Standing tier conditions
    tier_conditions = {
        "exalted", "honored", "friendly", "acknowledged",
        "neutral", "suspicious", "unfriendly", "hostile",
    }
    if condition in tier_conditions:
        return context.get("standing_tier") == condition

    # Quest conditions (wired to quest_engine via context packet)
    if condition == "quest_active":
        return len(context.get("active_quests") or []) > 0
    if condition == "quest_complete":
        return len(context.get("completed_quests") or []) > 0
    if condition == "quest_failed":
        return len(context.get("failed_quests") or []) > 0

    # Class/companion presence conditions
    if condition == "scholar_present":
        primary = (context.get("primary_domain") or "").lower()
        subclass = (context.get("subclass") or "").lower()
        # Scholar maps to remnance domain; subclass names include "Scholar" variants
        return primary == "remnance" or "scholar" in subclass

    if condition == "warden_present":
        guild = (context.get("guild") or "").lower()
        subclass = (context.get("subclass") or "").lower()
        # Wardens map to warcraft guild; subclass names include "Warden" variants
        return guild == "warcraft" or "warden" in subclass

    if condition == "dragon_present":
        return (context.get("companion_type") or "").lower() == "dragon"

    # Dimension threshold conditions
    if condition == "network_high":
        return (context.get("network") or 0) > NETWORK_HINT_THRESHOLD

    if condition == "reputation_high":
        return (context.get("reputation") or 0) > REPUTATION_HINT_THRESHOLD

    return False


# ---------------------------------------------------------------------------
# Topic response
# ---------------------------------------------------------------------------

def resolve_topic_response(npc, character, topic_key, *, context=None):
    """
    Resolve the best response for a topic from an NPC.

    Reads npc.db.dialogue_topics, gets topic data, iterates
    RESPONSE_PRIORITY checking conditions. Returns (text, condition_key)
    or (None, None) if topic not found on this NPC.
    """
    topics = npc.db.dialogue_topics or {}
    topic_data = topics.get(topic_key)
    if not topic_data:
        return (None, None)

    if isinstance(topic_data, str):
        return (topic_data, "default")

    if context is None:
        context = _build_dialogue_context(npc, character)

    for condition in RESPONSE_PRIORITY:
        if condition == "social_context":
            text, social_condition = _resolve_social_topic_response(
                topic_data,
                context,
            )
            if social_condition:
                return (text, social_condition)
            continue

        if condition in topic_data:
            if _check_condition(condition, context):
                return (topic_data[condition], condition)

    # If no condition matched (shouldn't happen if "default" is authored)
    default_text = topic_data.get("default")
    if default_text:
        return (default_text, "default")

    return (None, None)


# ---------------------------------------------------------------------------
# Hint system
# ---------------------------------------------------------------------------

def get_npc_hints(npc, character):
    """
    Collect available dialogue hints for this character from this NPC.

    Gathers from base, tier, quest, network, scholar, and warden hint
    pools. Filters out already-known topics via KnownTopicRecord.
    Caps at MAX_HINTS_DISPLAYED. Returns list of topic key strings.
    """
    from world.models import KnownTopicRecord

    hints = []

    # Base hints — always available
    base_hints = npc.db.dialogue_base_hints or []
    hints.extend(base_hints)

    # Tier-specific hints
    tier = get_standing_tier(character, npc)
    tier_hints = npc.db.dialogue_tier_hints or {}
    hints.extend(tier_hints.get(tier, []))

    # Quest hints — show hints for active quests this NPC knows about
    from world.quest_engine import get_active_quests
    active_cqs = get_active_quests(character)
    active_quest_ids = [cq.quest_id for cq in active_cqs]
    quest_hints = npc.db.dialogue_quest_hints or {}
    for quest_id in active_quest_ids:
        hints.extend(quest_hints.get(quest_id, []))

    # Network hints — available when character has high Network dimension
    context = _build_dialogue_context(npc, character)
    if _check_condition("network_high", context):
        network_hints = npc.db.dialogue_network_hints or []
        hints.extend(network_hints)

    # Scholar hints — available when character has Scholar domain
    if _check_condition("scholar_present", context):
        scholar_hints = npc.db.dialogue_scholar_hints or []
        hints.extend(scholar_hints)

    # Warden hints — available when character is a Warden guild member
    if _check_condition("warden_present", context):
        warden_hints = npc.db.dialogue_warden_hints or []
        hints.extend(warden_hints)

    # Deduplicate while preserving order
    seen = set()
    unique_hints = []
    for h in hints:
        if h not in seen:
            seen.add(h)
            unique_hints.append(h)

    # Filter already-known topics (same context)
    npc_id = npc.db.npc_id or npc.key or ""
    known_records = KnownTopicRecord.objects.filter(
        character=character, npc_id=npc_id
    ).values_list("topic_key", "context_hash")
    known_map = {tk: ch for tk, ch in known_records}

    current_hash = _compute_context_hash(context)

    filtered = []
    for topic_key in unique_hints:
        stored_hash = known_map.get(topic_key)
        if stored_hash is None:
            # Never learned — show hint
            filtered.append(topic_key)
        elif stored_hash != current_hash:
            # Context changed since last learning — re-surface hint
            filtered.append(topic_key)
        # else: known in same context — suppress

    return filtered[:MAX_HINTS_DISPLAYED]


def _compute_context_hash(context):
    """
    Compute a short hash from context fields relevant to hint re-surfacing.

    When a character's standing tier, quest state, or dimension scores
    change significantly, the hash changes and previously-known topics
    re-appear as hints.
    """
    parts = [
        str(context.get("standing_tier", "")),
        str(int(context.get("reputation") or 0)),
        str(int(context.get("network") or 0)),
        str(context.get("guild") or ""),
        str(len(context.get("completed_quests") or [])),
    ]
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Topic learning
# ---------------------------------------------------------------------------

def record_topic_learned(character, npc_id, topic_key, context):
    """
    Create or update a KnownTopicRecord for this character/NPC/topic.

    Stores a context_hash so hints re-surface when context changes.
    """
    from world.models import KnownTopicRecord

    context_hash = _compute_context_hash(context)
    KnownTopicRecord.objects.update_or_create(
        character=character,
        npc_id=npc_id,
        topic_key=topic_key,
        defaults={"context_hash": context_hash},
    )


# ---------------------------------------------------------------------------
# Keyword extraction
# ---------------------------------------------------------------------------

def extract_topic(text, available_topics):
    """
    Extract a topic key from player input text.

    4-stage pipeline:
    1. Direct match — longest topic key first (underscores as spaces)
    2. Synonym match — via TOPIC_SYNONYMS
    3. Partial word match — words > 2 chars from underscore-split topic keys
    4. None — no match found

    Returns topic_key string or None.
    """
    if not text or not available_topics:
        return None

    normalized = text.strip().lower()
    topic_set = set(available_topics)

    # Stage 1: Direct match (longest first for multi-word topics)
    sorted_topics = sorted(topic_set, key=len, reverse=True)
    for topic in sorted_topics:
        # Match topic_key as-is or with underscores replaced by spaces
        topic_lower = topic.lower()
        topic_spaced = topic_lower.replace("_", " ")
        if topic_lower in normalized or topic_spaced in normalized:
            return topic

    # Stage 2: Synonym match
    for canonical, synonyms in TOPIC_SYNONYMS.items():
        if canonical not in topic_set:
            continue
        for syn in synonyms:
            if syn.lower() in normalized:
                return canonical

    # Stage 3: Partial word match
    input_words = set(normalized.split())
    for topic in sorted_topics:
        topic_words = topic.lower().replace("_", " ").split()
        for tw in topic_words:
            if len(tw) > 2 and tw in input_words:
                return topic

    # Stage 4: No match
    return None


# ---------------------------------------------------------------------------
# Quest integration
# ---------------------------------------------------------------------------

def has_available_quest(npc, character):
    """Check if NPC has a quest available for this character (D-18)."""
    return bool(get_quest_offers(npc, character))


def get_quest_offers(npc, character):
    """Return every currently offerable lead in the order dialogue should show."""
    from world.quest_engine import get_available_quest_offers_for_npc

    return get_available_quest_offers_for_npc(npc, character)


def get_quest_offer(npc, character):
    """Compatibility adapter returning the first available dialogue offer."""
    offers = get_quest_offers(npc, character)
    return offers[0] if offers else None


# ---------------------------------------------------------------------------
# Ambient NPC behavior
# ---------------------------------------------------------------------------

def ambient_npc_tick():
    """
    Global ambient ticker callback for NPC idle echoes.

    Iterates all rooms containing NPC objects with ambient data.
    For each NPC, checks ndb.next_echo_at timestamp. If elapsed,
    picks a random idle echo, sends to room (only if room has
    connected characters — Pitfall 5), and schedules next echo.

    Registered via TICKER_HANDLER at server start.
    """
    import random

    from evennia.utils.search import search_tag

    # Find all objects tagged as NPCs
    npc_objects = search_tag("npc", category="character_type")

    now = time.time()

    for npc in npc_objects:
        echoes = npc.db.ambient_idle_echoes or []
        if not echoes:
            continue

        interval = npc.db.ambient_idle_interval or 120
        variance = npc.db.ambient_idle_variance or 30

        next_echo = npc.ndb.next_echo_at or 0
        if now < next_echo:
            continue

        # Check if NPC's room has connected characters (Pitfall 5)
        room = npc.location
        if not room:
            continue

        has_players = False
        for obj in room.contents:
            if hasattr(obj, "has_account") and obj.has_account:
                has_players = True
                break

        if not has_players:
            # Skip — no one to see the echo. Schedule next check later.
            npc.ndb.next_echo_at = now + interval
            continue

        # Pick and send random echo
        echo_text = random.choice(echoes)
        room.msg_contents(echo_text)

        # Schedule next echo with variance
        next_interval = interval + random.randint(-variance, variance)
        next_interval = max(10, next_interval)  # minimum 10s between echoes
        npc.ndb.next_echo_at = now + next_interval


def fire_npc_reactive_echo(room, trigger_type):
    """
    Fire reactive echoes from NPCs in a room for a given trigger.

    Checks each NPC's npc.db.ambient_reactive_echoes dict for a
    matching trigger_type key. If found, sends the echo text to the room.

    Trigger types: combat_nearby, node_active, quest_complete,
    player_enters, player_leaves, etc.
    """
    if not room:
        return

    for obj in room.contents:
        if not (obj.db.is_npc):
            continue

        reactive = obj.db.ambient_reactive_echoes or {}
        echo_text = reactive.get(trigger_type)
        if echo_text:
            room.msg_contents(echo_text)
