"""
Quest engine for Soravelon.

Stateless service module following the established engine pattern (banking.py,
inventory_engine.py). All functions take a character + context and return
(bool, str) tuples where applicable.

Quest definitions are stored on zone objects as db.quest_definitions (list of
dicts), authored via area.quest() DSL. This module reads specs at runtime and
manages quest state via the CharacterQuest Django model.

Lazy imports throughout to avoid circular dependencies (project convention).
"""

import datetime

# ---------------------------------------------------------------------------
# Lazy model accessor — avoids import-time Django resolution
# ---------------------------------------------------------------------------

CharacterQuest = None


def _ensure_model():
    """Lazily import CharacterQuest model on first use."""
    global CharacterQuest
    if CharacterQuest is None:
        from world.models import CharacterQuest as _CQ
        CharacterQuest = _CQ


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_ACTIVE_QUESTS = 5  # D-02

OBJECTIVE_TYPES = {"kill", "collect", "investigate", "deliver", "talk_to"}

# Map non-MVP objective types to their MVP equivalents
_OBJECTIVE_TYPE_ALIASES = {
    "gather": "collect",
    "recover": "collect",
    "craft": "collect",       # crafting objectives treated as collect for MVP
    "discover": "investigate",
    "escort": "deliver",      # escort → deliver for MVP simplicity
}


# ---------------------------------------------------------------------------
# Quest spec helpers
# ---------------------------------------------------------------------------

def _get_quest_spec(quest_id):
    """
    Find a quest spec by ID across all loaded zones.

    Searches zone objects tagged 'zone_object' for quest_definitions
    containing the given quest_id.
    """
    import evennia

    zone_objs = evennia.search_tag("zone_object", category="object_type")
    for zo in zone_objs:
        for qdef in (zo.db.quest_definitions or []):
            if qdef.get("quest_id") == quest_id:
                return _normalize_quest_spec(qdef)
    return None


def _get_all_quest_specs():
    """
    Return all quest specs from all loaded zones.

    Used by get_available_quest_for_npc to search for quests by NPC.
    """
    import evennia

    specs = []
    zone_objs = evennia.search_tag("zone_object", category="object_type")
    for zo in zone_objs:
        for qdef in (zo.db.quest_definitions or []):
            specs.append(_normalize_quest_spec(qdef))
    return specs


def _normalize_quest_spec(quest_spec):
    """
    Convert flat quest format to objectives-list format.

    Flat format: {objective_type, objective_target, objective_count}
    New format: {objectives: [{type, target, count}, ...]}

    If spec already has 'objectives' key, returns as-is.
    Non-MVP types (gather, discover, escort, etc.) are mapped to MVP types.
    """
    spec = dict(quest_spec)  # shallow copy

    if "objectives" in spec and spec["objectives"]:
        # Already in new format — just normalize objective types
        normalized = []
        for obj in spec["objectives"]:
            obj = dict(obj)
            obj_type = obj.get("type", "")
            obj["type"] = _OBJECTIVE_TYPE_ALIASES.get(obj_type, obj_type)
            normalized.append(obj)
        spec["objectives"] = normalized
        return spec

    # Convert flat format to objectives list
    obj_type = spec.get("objective_type", "")
    obj_type = _OBJECTIVE_TYPE_ALIASES.get(obj_type, obj_type)
    target = spec.get("objective_target", "")
    count = spec.get("objective_count", 1)

    obj = {"type": obj_type, "target": target, "count": count}

    # For deliver objectives, also store the item_tag (same as target in
    # flat format since flat format only has one target field)
    if obj_type == "deliver":
        obj["item_tag"] = spec.get("flagged_drop") or target

    spec["objectives"] = [obj]
    return spec


def _make_obj_key(obj_type, target):
    """Build the progress dict key for an objective."""
    return f"{obj_type}_{target}"


# ---------------------------------------------------------------------------
# Core quest functions
# ---------------------------------------------------------------------------

def accept_quest(character, quest_id, quest_spec):
    """
    Accept a quest. Creates a CharacterQuest record.

    Per D-01: stores character, quest_id, status=active, progress={}.
    Per D-02: rejects if 5 active quests exist.
    Per D-03: rejects one_chance quest already failed.

    Returns (bool, str).
    """
    _ensure_model()

    # Check active quest cap (D-02)
    active_count = CharacterQuest.objects.filter(
        character=character, status="active"
    ).count()
    if active_count >= MAX_ACTIVE_QUESTS:
        return False, f"You already have {MAX_ACTIVE_QUESTS} active quests. Abandon one first."

    # Check one_chance lock (D-03)
    if quest_spec.get("one_chance"):
        if CharacterQuest.objects.filter(
            character=character, quest_id=quest_id, status="failed"
        ).exists():
            return False, "This quest is no longer available to you."

    # Check not already active
    if CharacterQuest.objects.filter(
        character=character, quest_id=quest_id, status="active"
    ).exists():
        return False, "You already have this quest."

    # Initialize progress dict with zero values for all objectives
    spec = _normalize_quest_spec(quest_spec)
    progress = {}
    for obj in (spec.get("objectives") or []):
        key = _make_obj_key(obj["type"], obj["target"])
        progress[key] = 0

    CharacterQuest.objects.create(
        character=character,
        quest_id=quest_id,
        status="active",
        progress=progress,
    )

    name = quest_spec.get("name") or quest_id
    return True, f"Quest accepted: {name}"


def abandon_quest(character, quest_id):
    """
    Abandon an active quest (D-04).

    Sets status to 'abandoned'. Player-triggered terminal state.
    Returns (bool, str).
    """
    _ensure_model()

    cq = CharacterQuest.objects.filter(
        character=character, quest_id=quest_id, status="active"
    ).first()

    if not cq:
        return False, "You don't have that quest."

    cq.status = "abandoned"
    cq.save(update_fields=["status"])
    return True, f"Quest abandoned: {quest_id}"


# ---------------------------------------------------------------------------
# Objective check functions
# ---------------------------------------------------------------------------

def check_kill_objectives(character, mob):
    """
    Check active quests for kill objectives matching this mob (D-07/D-19).

    Called from typeclasses/mobs.py at_death().
    Matches on mob.db.mob_template or mob.db.mob_id.
    """
    _ensure_model()

    mob_template = mob.db.mob_template or ""
    mob_id = mob.db.mob_id or ""
    identifiers = {id for id in (mob_template, mob_id) if id}

    if not identifiers:
        return

    active_quests = CharacterQuest.objects.filter(
        character=character, status="active"
    )
    for cq in active_quests:
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue

        updated = False
        for obj in (quest_spec.get("objectives") or []):
            if obj.get("type") != "kill":
                continue
            target = obj.get("target", "")
            if target not in identifiers:
                continue

            key = _make_obj_key("kill", target)
            cq.refresh_from_db()
            progress = dict(cq.progress or {})
            progress[key] = progress.get(key, 0) + 1
            cq.progress = progress
            cq.save(update_fields=["progress"])
            updated = True

        if updated:
            _check_quest_completion(character, cq, quest_spec)


def check_collect_objectives(character, item):
    """
    Check active quests for collect objectives matching this item (D-08).

    Called when an item is picked up. Matches on item.db.item_tag
    or item tag with category 'item_tag'.
    """
    _ensure_model()

    item_tag = getattr(item.db, "item_tag", None) or ""
    # Also check Evennia tags
    tag_val = item.tags.get(category="item_tag") if hasattr(item, "tags") else None
    identifiers = {id for id in (item_tag, tag_val) if id}

    if not identifiers:
        return

    active_quests = CharacterQuest.objects.filter(
        character=character, status="active"
    )
    for cq in active_quests:
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue

        updated = False
        for obj in (quest_spec.get("objectives") or []):
            if obj.get("type") != "collect":
                continue
            target = obj.get("target", "")
            if target not in identifiers:
                continue

            key = _make_obj_key("collect", target)
            cq.refresh_from_db()
            progress = dict(cq.progress or {})
            progress[key] = progress.get(key, 0) + 1
            cq.progress = progress
            cq.save(update_fields=["progress"])
            updated = True

        if updated:
            _check_quest_completion(character, cq, quest_spec)


def check_investigate_objectives(character, room):
    """
    Check active quests for investigate objectives matching this room (D-09).

    Called on room entry. Room visit alone completes for MVP simplicity.
    Matches on room.db.room_id.
    """
    _ensure_model()

    room_id = getattr(room.db, "room_id", None) or ""
    if not room_id:
        return

    active_quests = CharacterQuest.objects.filter(
        character=character, status="active"
    )
    for cq in active_quests:
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue

        updated = False
        for obj in (quest_spec.get("objectives") or []):
            if obj.get("type") != "investigate":
                continue
            target = obj.get("target", "")
            if target != room_id:
                continue

            key = _make_obj_key("investigate", target)
            cq.refresh_from_db()
            progress = dict(cq.progress or {})
            if progress.get(key, 0) < 1:
                progress[key] = 1
                cq.progress = progress
                cq.save(update_fields=["progress"])
                updated = True

        if updated:
            _check_quest_completion(character, cq, quest_spec)


def check_deliver_objectives(character, npc):
    """
    Check active quests for deliver objectives matching this NPC (D-10).

    Delivery requires: character carries item with matching item_tag AND
    talks to target NPC. Called from talk command.
    """
    _ensure_model()

    npc_id = getattr(npc.db, "npc_id", None) or ""
    if not npc_id:
        return

    active_quests = CharacterQuest.objects.filter(
        character=character, status="active"
    )
    for cq in active_quests:
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue

        updated = False
        for obj in (quest_spec.get("objectives") or []):
            if obj.get("type") != "deliver":
                continue
            target = obj.get("target", "")
            if target != npc_id:
                continue

            # Check if character has the delivery item
            item_tag = obj.get("item_tag", "")
            if not item_tag:
                continue

            has_item = any(
                getattr(getattr(c, "db", None), "item_tag", None) == item_tag
                for c in (character.contents or [])
            )
            if not has_item:
                continue

            key = _make_obj_key("deliver", target)
            cq.refresh_from_db()
            progress = dict(cq.progress or {})
            if progress.get(key, 0) < 1:
                progress[key] = 1
                cq.progress = progress
                cq.save(update_fields=["progress"])
                updated = True

        if updated:
            _check_quest_completion(character, cq, quest_spec)


def check_talk_to_objectives(character, npc):
    """
    Check active quests for talk_to objectives matching this NPC (D-11).

    Called from talk command. Simple NPC ID match.
    """
    _ensure_model()

    npc_id = getattr(npc.db, "npc_id", None) or ""
    if not npc_id:
        return

    active_quests = CharacterQuest.objects.filter(
        character=character, status="active"
    )
    for cq in active_quests:
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue

        updated = False
        for obj in (quest_spec.get("objectives") or []):
            if obj.get("type") != "talk_to":
                continue
            target = obj.get("target", "")
            if target != npc_id:
                continue

            key = _make_obj_key("talk_to", target)
            cq.refresh_from_db()
            progress = dict(cq.progress or {})
            if progress.get(key, 0) < 1:
                progress[key] = 1
                cq.progress = progress
                cq.save(update_fields=["progress"])
                updated = True

        if updated:
            _check_quest_completion(character, cq, quest_spec)


# ---------------------------------------------------------------------------
# Completion and rewards
# ---------------------------------------------------------------------------

def _check_quest_completion(character, cq, quest_spec):
    """
    Check if all objectives are met and complete the quest if so.

    On completion: sets status='complete', completed_at=now, pays rewards
    via execute_action (D-20), and if next_quest_id exists, sets
    character.ndb.pending_quest_offer for chain auto-offer (D-05).
    """
    objectives = quest_spec.get("objectives") or []
    progress = dict(cq.progress or {})

    for obj in objectives:
        key = _make_obj_key(obj["type"], obj["target"])
        required = obj.get("count", 1)
        current = progress.get(key, 0)
        if current < required:
            return  # Not all objectives met

    # All objectives met — complete the quest
    cq.status = "complete"
    try:
        from django.utils import timezone as _tz
        cq.completed_at = _tz.now()
    except Exception:
        cq.completed_at = datetime.datetime.now(datetime.timezone.utc)
    cq.save(update_fields=["status", "completed_at"])

    # Notify player
    name = quest_spec.get("name") or cq.quest_id
    character.msg(f"|g[Quest Complete]|n {name}")

    # Pay rewards (D-20)
    _pay_rewards(character, quest_spec)

    # Chain auto-offer (D-05)
    next_id = quest_spec.get("next_quest_id")
    if next_id:
        character.ndb.pending_quest_offer = next_id

    # Push OOB update if available
    try:
        from world.oob_publisher import push_quest_update
        push_quest_update(character, {
            "quest_id": cq.quest_id,
            "status": "complete",
            "name": name,
        })
    except Exception:
        pass  # OOB not yet wired or character is mock — safe to skip


def _pay_rewards(character, quest_spec):
    """
    Execute all reward actions for a completed quest (D-20).

    Each reward is an action dict processed by execute_action().
    """
    from world.action_vocabulary import execute_action

    context = {"character": character, "room": character.location}
    rewards = quest_spec.get("rewards") or []

    for reward in rewards:
        execute_action(reward, context)


# ---------------------------------------------------------------------------
# Query functions
# ---------------------------------------------------------------------------

def get_available_quest_for_npc(npc, character):
    """
    Find a quest this NPC can offer to this character (D-18).

    Searches all quest_definitions for quest_giver matching npc's npc_id.
    Filters out: already active, already complete (if one_chance),
    one_chance + failed.

    Returns the first available quest spec dict, or None.
    """
    _ensure_model()

    npc_id = getattr(npc.db, "npc_id", None) or ""
    if not npc_id:
        return None

    all_specs = _get_all_quest_specs()

    # Get character's existing quest IDs by status
    existing = CharacterQuest.objects.filter(character=character)
    active_ids = set(existing.filter(status="active").values_list("quest_id", flat=True))
    complete_ids = set(existing.filter(status="complete").values_list("quest_id", flat=True))
    failed_ids = set(existing.filter(status="failed").values_list("quest_id", flat=True))

    for spec in all_specs:
        if spec.get("quest_giver") != npc_id:
            continue

        qid = spec.get("quest_id")

        # Skip if already active
        if qid in active_ids:
            continue

        # Skip if already complete
        if qid in complete_ids:
            continue

        # Skip if one_chance and failed
        if spec.get("one_chance") and qid in failed_ids:
            continue

        return spec

    return None


def get_active_quests(character):
    """
    Return queryset of active CharacterQuest records for a character.
    """
    _ensure_model()
    return CharacterQuest.objects.filter(
        character=character, status="active"
    )


def get_quest_detail(character, quest_id):
    """
    Return a dict with formatted quest info for display (D-16).

    Returns: {name, description, quest_id, objectives: [{type, target, count,
    progress}], rewards: [...]} or None if quest not found.
    """
    _ensure_model()

    cq = CharacterQuest.objects.filter(
        character=character, quest_id=quest_id
    ).first()
    if not cq:
        return None

    quest_spec = _get_quest_spec(quest_id)
    if not quest_spec:
        return None

    progress = dict(cq.progress or {})
    objectives = []
    for obj in (quest_spec.get("objectives") or []):
        key = _make_obj_key(obj["type"], obj["target"])
        objectives.append({
            "type": obj["type"],
            "target": obj["target"],
            "count": obj.get("count", 1),
            "progress": progress.get(key, 0),
        })

    return {
        "quest_id": quest_id,
        "name": quest_spec.get("name") or quest_id,
        "description": quest_spec.get("description") or "",
        "status": cq.status,
        "objectives": objectives,
        "rewards": quest_spec.get("rewards") or [],
        "quest_giver": quest_spec.get("quest_giver") or "",
    }
