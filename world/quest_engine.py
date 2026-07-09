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
    from world.social_quest_offers import get_social_quest_spec_by_id

    social_spec = get_social_quest_spec_by_id(quest_id)
    if social_spec:
        return _normalize_quest_spec(social_spec)
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
        flagged_drop = spec.get("flagged_drop") or ""
        for obj in spec["objectives"]:
            obj = dict(obj)
            obj_type = obj.get("type", "")
            obj["type"] = _OBJECTIVE_TYPE_ALIASES.get(obj_type, obj_type)
            if obj["type"] == "deliver" and not obj.get("item_tag") and flagged_drop:
                obj["item_tag"] = flagged_drop
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


def _get_prerequisite_quest_ids(quest_spec):
    """
    Return prerequisite quest IDs for a chain step.

    AreaBuilder stores the canonical field as prerequisite_quests. The small
    alias set lets older authored specs converge without player-facing drift.
    """
    raw = (
        quest_spec.get("prerequisite_quests")
        or quest_spec.get("required_quests")
        or quest_spec.get("requires_quests")
        or []
    )
    if isinstance(raw, str):
        return [raw]
    return [quest_id for quest_id in raw if quest_id]


def _make_obj_key(obj_type, target):
    """Build the progress dict key for an objective."""
    return f"{obj_type}_{target}"


def _find_carried_item_by_tag(character, item_tag):
    """Return the first carried item matching an item_tag."""
    if not item_tag:
        return None

    for item in (character.contents or []):
        db_tag = getattr(getattr(item, "db", None), "item_tag", None) or ""
        evennia_tag = item.tags.get(category="item_tag") if hasattr(item, "tags") else None
        if item_tag in {db_tag, evennia_tag}:
            return item
    return None


def _grant_delivery_items_on_accept(character, quest_spec):
    """
    Give deliver-quest handoff items to the player when a quest is accepted.

    This keeps authored delivery quests completable without inventing a second
    acquisition step outside the quest contract. Items are only granted when
    the player does not already carry the required tagged item.
    """
    context = {"character": character, "room": character.location}
    granted_tags = set()

    for obj in (quest_spec.get("objectives") or []):
        if obj.get("type") != "deliver":
            continue

        item_tag = obj.get("item_tag") or ""
        if not item_tag or item_tag in granted_tags:
            continue

        if _find_carried_item_by_tag(character, item_tag):
            granted_tags.add(item_tag)
            continue

        from world.action_vocabulary import execute_action
        success, msg = execute_action(
            {"action_type": "give_item", "template_id": item_tag},
            context,
        )
        if not success:
            return False, msg

        granted_tags.add(item_tag)

    return True, ""


def _consume_delivery_item(character, item):
    """Remove a delivered quest item from the player's inventory."""
    try:
        from world.inventory_engine import unregister_item_ownership
        unregister_item_ownership(character, item)
    except Exception:
        pass

    try:
        item.delete()
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Core quest functions
# ---------------------------------------------------------------------------

def accept_quest(character, quest_id, quest_spec):
    """
    Accept a quest. Creates a CharacterQuest record.

    Per D-01: stores character, quest_id, status=active, progress={}.
    Per D-02: rejects if 5 active quests exist.
    Per D-03: rejects one_chance quest already failed or completed.

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
        if CharacterQuest.objects.filter(
            character=character, quest_id=quest_id, status="complete"
        ).exists():
            return False, "You have already completed this quest."

    # Check not already active
    if CharacterQuest.objects.filter(
        character=character, quest_id=quest_id, status="active"
    ).exists():
        return False, "You already have this quest."

    prerequisite_ids = _get_prerequisite_quest_ids(quest_spec)
    if prerequisite_ids:
        complete_ids = set(
            CharacterQuest.objects.filter(
                character=character,
                status="complete",
                quest_id__in=prerequisite_ids,
            ).values_list("quest_id", flat=True)
        )
        missing = [quest_id for quest_id in prerequisite_ids if quest_id not in complete_ids]
        if missing:
            return False, "Complete the earlier quests in this chain first."

    # Initialize progress dict with zero values for all objectives
    spec = _normalize_quest_spec(quest_spec)
    progress = {}
    for obj in (spec.get("objectives") or []):
        key = _make_obj_key(obj["type"], obj["target"])
        progress[key] = 0

    cq = CharacterQuest.objects.create(
        character=character,
        quest_id=quest_id,
        status="active",
        progress=progress,
    )

    granted, grant_msg = _grant_delivery_items_on_accept(character, spec)
    if not granted:
        try:
            cq.delete()
        except Exception:
            pass
        return False, grant_msg

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
    Matches on mob.db.mob_template_key or mob.db.mob_instance_id.
    """
    _ensure_model()

    mob_template_key = mob.db.mob_template_key or ""
    mob_instance_id = mob.db.mob_instance_id or ""
    identifiers = {id for id in (mob_template_key, mob_instance_id) if id}

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

    room_id = room.tags.get(category="room_id") or ""
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
            required = obj.get("count", 1)
            cq.refresh_from_db()
            progress = dict(cq.progress or {})
            current = progress.get(key, 0)
            if current < required:
                progress[key] = current + 1
                cq.progress = progress
                cq.save(update_fields=["progress"])
                updated = True

        if updated:
            _check_quest_completion(character, cq, quest_spec)


def check_practice_objectives(character, opportunity_id):
    """
    Check active quests for practice objectives matching a completed opportunity.

    Called by practice_engine after a meaningful builder-authored practice
    interaction succeeds.
    """
    _ensure_model()

    active = CharacterQuest.objects.filter(character=character, status="active")
    for cq in active:
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue

        progress = dict(cq.progress or {})
        updated = False
        for obj in (quest_spec.get("objectives") or []):
            if obj.get("type") != "practice":
                continue
            target = obj.get("target", "")
            if target != opportunity_id:
                continue
            key = _make_obj_key("practice", target)
            required = obj.get("count", 1)
            current = progress.get(key, 0)
            if current >= required:
                continue
            progress[key] = min(required, current + 1)
            updated = True

        if updated:
            cq.progress = progress
            cq.save(update_fields=["progress"])
            _check_quest_completion(character, cq, quest_spec)


def check_deliver_objectives(character, npc):
    """
    Check active quests for deliver objectives matching this NPC (D-10).

    Delivery requires: character carries item with matching item_tag AND
    talks to target NPC. Called from talk command.
    """
    _ensure_model()

    npc_id = npc.tags.get(category="npc_id") if hasattr(npc, "tags") else ""
    npc_id = npc_id or ""
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

            delivery_item = _find_carried_item_by_tag(character, item_tag)
            if not delivery_item:
                continue

            key = _make_obj_key("deliver", target)
            required = obj.get("count", 1)
            cq.refresh_from_db()
            progress = dict(cq.progress or {})
            current = progress.get(key, 0)
            if current < required:
                progress[key] = current + 1
                cq.progress = progress
                cq.save(update_fields=["progress"])
                _consume_delivery_item(character, delivery_item)
                updated = True

        if updated:
            _check_quest_completion(character, cq, quest_spec)


def check_talk_to_objectives(character, npc):
    """
    Check active quests for talk_to objectives matching this NPC (D-11).

    Called from talk command. Simple NPC ID match.
    """
    _ensure_model()

    npc_id = npc.tags.get(category="npc_id") if hasattr(npc, "tags") else ""
    npc_id = npc_id or ""
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
        next_spec = _get_quest_spec(next_id)
        if next_spec:
            character.ndb.pending_quest_offer = {
                "npc": None,  # NPC not in scope at completion — CmdAccept handles gracefully
                "quest": next_spec,
            }

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


class _RewardBatchRejected(RuntimeError):
    def __init__(self, failure):
        super().__init__(failure["message"])
        self.failure = failure


def _reward_after_write(checkpoint):
    """Failure-injection seam for exactly-once reward batches."""


def _pay_rewards_exactly_once(character, quest_spec, operation_id):
    from evennia.objects.models import ObjectDB
    from world.action_vocabulary import execute_action
    from world.atomic_state import atomic_evennia_state
    from world.game_operations import (
        get_operation_replay,
        normalize_operation_id,
        record_operation,
    )

    operation_id = normalize_operation_id(operation_id)
    quest_id = quest_spec.get("quest_id") or quest_spec.get("name") or "anonymous"
    related_id = f"quest-rewards:{quest_id}"
    context = {
        "character": character,
        "room": character.location,
        "_created_items": [],
    }
    try:
        with atomic_evennia_state(character) as tracker:
            locked_character = ObjectDB.objects.select_for_update().get(
                pk=character.id
            )
            tracker.track(locked_character, attributes=("carried_scales",))
            context["character"] = locked_character
            context["room"] = locked_character.location
            replay = get_operation_replay(
                character=locked_character,
                operation_id=operation_id,
                operation_type="quest_rewards",
                related_id=related_id,
            )
            if replay:
                return []

            for index, reward in enumerate(quest_spec.get("rewards") or []):
                success, message = execute_action(reward, context)
                for item in context["_created_items"]:
                    tracker.track(item)
                if not success:
                    raise _RewardBatchRejected(
                        {
                            "index": index,
                            "action_type": reward.get("action_type"),
                            "message": message,
                        }
                    )
                _reward_after_write(f"reward_executed:{index}")

            record_operation(
                character=locked_character,
                operation_id=operation_id,
                operation_type="quest_rewards",
                related_id=related_id,
                result={"reward_count": len(quest_spec.get("rewards") or [])},
            )
            _reward_after_write("operation_recorded")
        return []
    except _RewardBatchRejected as error:
        character.msg(
            "|r[Reward Error]|n "
            f"{error.failure['action_type'] or 'unknown'} failed: "
            f"{error.failure['message']}"
        )
        return [error.failure]


def _pay_rewards(character, quest_spec, operation_id=None):
    """
    Execute all reward actions for a completed quest (D-20).

    Each reward is an action dict processed by execute_action().
    Returns a list of failed reward details.
    """
    if operation_id is not None:
        return _pay_rewards_exactly_once(character, quest_spec, operation_id)

    from world.action_vocabulary import execute_action

    context = {"character": character, "room": character.location}
    rewards = quest_spec.get("rewards") or []
    failures = []

    for index, reward in enumerate(rewards):
        success, msg = execute_action(reward, context)
        if success:
            continue
        failure = {
            "index": index,
            "action_type": reward.get("action_type"),
            "message": msg,
        }
        failures.append(failure)
        character.msg(
            "|r[Reward Error]|n "
            f"{failure['action_type'] or 'unknown'} failed: {msg}"
        )

    return failures


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

        # Skip if already complete AND one_chance (non-repeatable)
        if qid in complete_ids and spec.get("one_chance"):
            continue

        # Skip if one_chance and failed
        if spec.get("one_chance") and qid in failed_ids:
            continue

        prerequisites = _get_prerequisite_quest_ids(spec)
        if any(prerequisite not in complete_ids for prerequisite in prerequisites):
            continue

        return spec

    from world.social_quest_offers import get_social_quest_offer_for_npc

    return get_social_quest_offer_for_npc(
        npc,
        character,
        active_ids=active_ids,
        complete_ids=complete_ids,
        failed_ids=failed_ids,
    )


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
