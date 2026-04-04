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
import time

from world.dialogue_definitions import (
    MAX_HINTS_DISPLAYED,
    NETWORK_HINT_THRESHOLD,
    REPUTATION_HINT_THRESHOLD,
    RESPONSE_PRIORITY,
    STANDING_TIER_THRESHOLDS,
    TOPIC_SYNONYMS,
)


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
    active_cqs = get_active_quests(character)
    context["active_quests"] = [cq.quest_id for cq in active_cqs]
    context["completed_quests"] = []
    context["failed_quests"] = []

    return context


def _check_condition(condition, context):
    """
    Evaluate a single condition string against the dialogue context.

    Returns True if the condition is met, False otherwise.
    """
    if condition == "default":
        return True

    if condition == "betrayal":
        return bool(context.get("betrayal_flag"))

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
        return primary == "scholar" or "scholar" in subclass

    if condition == "warden_present":
        guild = (context.get("guild") or "").lower()
        return guild == "wardens"

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

def resolve_topic_response(npc, character, topic_key):
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

    context = _build_dialogue_context(npc, character)

    for condition in RESPONSE_PRIORITY:
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
    return hashlib.md5(raw.encode()).hexdigest()[:16]


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
    from world.quest_engine import get_available_quest_for_npc
    return get_available_quest_for_npc(npc, character) is not None


def get_quest_offer(npc, character):
    """Get the quest offer data for display."""
    from world.quest_engine import get_available_quest_for_npc
    return get_available_quest_for_npc(npc, character)


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
