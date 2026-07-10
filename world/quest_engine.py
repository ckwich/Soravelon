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
    """Remove an owned delivery item or expose the exact failing gate."""
    from world.inventory_engine import destroy_owned_item

    return destroy_owned_item(character, item)


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

def _matching_objective_updates(quest_spec, objective_type, identifiers):
    """Return one capped increment for each matching authored objective."""
    updates = []
    for objective in quest_spec.get("objectives") or []:
        if objective.get("type") != objective_type:
            continue
        target = objective.get("target", "")
        if target not in identifiers:
            continue
        updates.append(
            {
                "key": _make_obj_key(objective_type, target),
                "amount": 1,
                "cap": objective.get("count", 1),
            }
        )
    return updates


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

    for cq in CharacterQuest.objects.filter(character=character, status="active"):
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue
        updates = _matching_objective_updates(quest_spec, "kill", identifiers)
        if updates:
            _advance_quest_objectives(character, cq.pk, quest_spec, updates)


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

    for cq in CharacterQuest.objects.filter(character=character, status="active"):
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue
        updates = _matching_objective_updates(quest_spec, "collect", identifiers)
        if updates:
            _advance_quest_objectives(character, cq.pk, quest_spec, updates)


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

    for cq in CharacterQuest.objects.filter(character=character, status="active"):
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue
        updates = _matching_objective_updates(
            quest_spec,
            "investigate",
            {room_id},
        )
        if updates:
            _advance_quest_objectives(character, cq.pk, quest_spec, updates)


def check_practice_objectives(character, opportunity_id):
    """
    Check active quests for practice objectives matching a completed opportunity.

    Called by practice_engine after a meaningful builder-authored practice
    interaction succeeds.
    """
    _ensure_model()

    for cq in CharacterQuest.objects.filter(character=character, status="active"):
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue
        updates = _matching_objective_updates(
            quest_spec,
            "practice",
            {opportunity_id},
        )
        if updates:
            _advance_quest_objectives(character, cq.pk, quest_spec, updates)


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

    for cq in CharacterQuest.objects.filter(character=character, status="active"):
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue
        updates = []
        delivery_items = []
        claimed_item_ids = set()
        for objective in quest_spec.get("objectives") or []:
            if (
                objective.get("type") != "deliver"
                or objective.get("target", "") != npc_id
            ):
                continue
            item_tag = objective.get("item_tag", "")
            if not item_tag:
                continue
            delivery_item = _find_carried_item_by_tag(character, item_tag)
            if not delivery_item or delivery_item.id in claimed_item_ids:
                continue
            claimed_item_ids.add(delivery_item.id)
            updates.append(
                {
                    "key": _make_obj_key("deliver", npc_id),
                    "amount": 1,
                    "cap": objective.get("count", 1),
                }
            )
            delivery_items.append(delivery_item)
        if updates:
            _advance_quest_objectives(
                character,
                cq.pk,
                quest_spec,
                updates,
                delivery_items=delivery_items,
            )


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

    for cq in CharacterQuest.objects.filter(character=character, status="active"):
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue
        updates = _matching_objective_updates(quest_spec, "talk_to", {npc_id})
        if updates:
            _advance_quest_objectives(character, cq.pk, quest_spec, updates)


# ---------------------------------------------------------------------------
# Completion and rewards
# ---------------------------------------------------------------------------

class _QuestMutationRejected(RuntimeError):
    """An expected objective mutation gate failed."""


class _QuestOutcomeRejected(RuntimeError):
    """A completion reward or consequence failed before commit."""

    def __init__(self, failure):
        super().__init__(failure["message"])
        self.failure = failure


def _quest_after_write(checkpoint):
    """Failure-injection seam for the atomic quest outcome."""


def _run_rollback_callbacks(callbacks):
    """Undo session-only mutations in reverse action order."""
    while callbacks:
        callbacks.pop()()


def _objectives_complete(progress, quest_spec):
    for objective in quest_spec.get("objectives") or []:
        key = _make_obj_key(objective["type"], objective["target"])
        if progress.get(key, 0) < objective.get("count", 1):
            return False
    return True


def _publish_quest_completion(character, quest_id, name, next_id, messages):
    """Expose completion only after every durable outcome write commits."""
    character.msg(f"|g[Quest Complete]|n {name}")
    for message in messages:
        character.msg(message)

    if next_id:
        next_spec = _get_quest_spec(next_id)
        if next_spec:
            character.ndb.pending_quest_offer = {
                "npc": None,
                "quest": next_spec,
            }

    try:
        from world.oob_publisher import push_quest_update

        push_quest_update(
            character,
            {
                "quest_id": quest_id,
                "status": "complete",
                "name": name,
            },
        )
    except Exception:
        import evennia

        evennia.logger.log_trace("Quest completion OOB publish failed")


def _validate_completed_quest_receipt(character, cq):
    from world.game_operations import get_operation_replay

    receipt = get_operation_replay(
        character=character,
        operation_id=cq.outcome_operation_id,
        operation_type="quest_completion",
        related_id=f"quest:{cq.quest_id}:{cq.pk}",
    )
    if not receipt:
        raise RuntimeError(
            f"Completed quest {cq.pk} has no durable completion receipt."
        )


def _complete_locked_quest(
    character,
    cq,
    quest_spec,
    deferred_messages,
    rollback_callbacks,
):
    """Complete one already-locked active quest inside its owning transaction."""
    progress = dict(cq.progress or {})
    if not _objectives_complete(progress, quest_spec):
        return False

    failures = _pay_rewards(
        character,
        quest_spec,
        operation_id=f"quest-reward:{cq.pk}",
        deferred_messages=deferred_messages,
        rollback_callbacks=rollback_callbacks,
    )
    if failures:
        raise _QuestOutcomeRejected(failures[0])

    from django.utils import timezone
    from world.game_operations import get_operation_replay, record_operation

    outcome_operation_id = f"quest-outcome:{cq.pk}"
    related_id = f"quest:{cq.quest_id}:{cq.pk}"
    if get_operation_replay(
        character=character,
        operation_id=outcome_operation_id,
        operation_type="quest_completion",
        related_id=related_id,
    ):
        raise RuntimeError(
            f"Active quest {cq.pk} already has a completion receipt."
        )

    result = {
        "status": "complete",
        "quest_id": cq.quest_id,
        "reward_count": len(quest_spec.get("rewards") or []),
    }
    cq.status = "complete"
    cq.completed_at = timezone.now()
    cq.outcome_operation_id = outcome_operation_id
    cq.outcome_result = result
    cq.save(
        update_fields=[
            "status",
            "completed_at",
            "outcome_operation_id",
            "outcome_result",
        ]
    )
    record_operation(
        character=character,
        operation_id=outcome_operation_id,
        operation_type="quest_completion",
        related_id=related_id,
        result=result,
    )
    _quest_after_write("completion_recorded")
    return True


def _advance_quest_objectives(
    character,
    quest_pk,
    quest_spec,
    updates,
    *,
    delivery_items=(),
):
    """Lock, advance, consume, reward, and complete as one transaction."""
    from django.db import transaction
    from evennia.objects.models import ObjectDB
    from world.atomic_state import atomic_evennia_state

    deferred_messages = []
    rollback_callbacks = []
    delivery_items = list(delivery_items)
    completed = False
    try:
        with atomic_evennia_state(character, *delivery_items) as tracker:
            locked_character = ObjectDB.objects.select_for_update().get(
                pk=character.id
            )
            tracker.track(locked_character, attributes=("carried_scales",))
            cq = CharacterQuest.objects.select_for_update().get(
                pk=quest_pk,
                character_id=locked_character.id,
            )
            if cq.status == "complete":
                _validate_completed_quest_receipt(locked_character, cq)
                return True
            if cq.status != "active":
                return False

            progress = dict(cq.progress or {})
            changed_update_indexes = []
            for index, update in enumerate(updates):
                key = update["key"]
                current = progress.get(key, 0)
                cap = update.get("cap")
                new_value = current + update.get("amount", 1)
                if cap is not None:
                    new_value = min(cap, new_value)
                if new_value <= current:
                    continue
                progress[key] = new_value
                changed_update_indexes.append(index)

            for index in changed_update_indexes:
                if index >= len(delivery_items):
                    continue
                delivery_item = delivery_items[index]
                tracker.track(delivery_item)
                consumed, message = _consume_delivery_item(
                    locked_character,
                    delivery_item,
                )
                if not consumed:
                    raise _QuestMutationRejected(message)

            if changed_update_indexes:
                cq.progress = progress
                cq.save(update_fields=["progress"])

            completed = _complete_locked_quest(
                locked_character,
                cq,
                quest_spec,
                deferred_messages,
                rollback_callbacks,
            )
            if completed:
                name = quest_spec.get("name") or cq.quest_id
                transaction.on_commit(
                    lambda: _publish_quest_completion(
                        character,
                        cq.quest_id,
                        name,
                        quest_spec.get("next_quest_id"),
                        tuple(deferred_messages),
                    )
                )
        return completed
    except _QuestOutcomeRejected as error:
        _run_rollback_callbacks(rollback_callbacks)
        character.msg(
            "|r[Reward Error]|n "
            f"{error.failure['action_type'] or 'unknown'} failed: "
            f"{error.failure['message']}"
        )
        return False
    except _QuestMutationRejected as error:
        _run_rollback_callbacks(rollback_callbacks)
        character.msg(f"|r[Quest Update Error]|n {error}")
        return False
    except Exception:
        _run_rollback_callbacks(rollback_callbacks)
        raise


def _check_quest_completion(character, cq, quest_spec):
    """Atomically complete a quest whose authored objectives are all met."""
    _ensure_model()
    completed = _advance_quest_objectives(
        character,
        cq.pk,
        quest_spec,
        [],
    )
    if getattr(cq, "pk", None):
        cq.refresh_from_db()
    return completed


class _RewardBatchRejected(RuntimeError):
    def __init__(self, failure):
        super().__init__(failure["message"])
        self.failure = failure


def _reward_after_write(checkpoint):
    """Failure-injection seam for exactly-once reward batches."""


def _pay_rewards_exactly_once(
    character,
    quest_spec,
    operation_id,
    *,
    deferred_messages=None,
    rollback_callbacks=None,
):
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
    owns_messages = deferred_messages is None
    deferred_messages = [] if deferred_messages is None else deferred_messages
    rollback_callbacks = [] if rollback_callbacks is None else rollback_callbacks
    context = {
        "character": character,
        "room": character.location,
        "_created_items": [],
        "_deferred_messages": deferred_messages,
        "_rollback_callbacks": rollback_callbacks,
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
        if owns_messages:
            from django.db import transaction

            transaction.on_commit(
                lambda: [character.msg(message) for message in deferred_messages]
            )
        return []
    except _RewardBatchRejected as error:
        _run_rollback_callbacks(rollback_callbacks)
        if owns_messages:
            character.msg(
                "|r[Reward Error]|n "
                f"{error.failure['action_type'] or 'unknown'} failed: "
                f"{error.failure['message']}"
            )
        return [error.failure]
    except Exception:
        _run_rollback_callbacks(rollback_callbacks)
        raise


def _pay_rewards(
    character,
    quest_spec,
    operation_id=None,
    *,
    deferred_messages=None,
    rollback_callbacks=None,
):
    """
    Execute all reward actions for a completed quest (D-20).

    Each reward is an action dict processed by execute_action().
    Returns a list of failed reward details.
    """
    if operation_id is not None:
        return _pay_rewards_exactly_once(
            character,
            quest_spec,
            operation_id,
            deferred_messages=deferred_messages,
            rollback_callbacks=rollback_callbacks,
        )

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

def get_available_quest_offers_for_npc(npc, character):
    """Return every currently valid authored and Social Web offer for an NPC."""
    _ensure_model()

    npc_id = getattr(npc.db, "npc_id", None) or ""
    if not npc_id:
        return ()

    all_specs = _get_all_quest_specs()

    # Get character's existing quest IDs by status
    existing = CharacterQuest.objects.filter(character=character)
    active_ids = set(existing.filter(status="active").values_list("quest_id", flat=True))
    complete_ids = set(existing.filter(status="complete").values_list("quest_id", flat=True))
    failed_ids = set(existing.filter(status="failed").values_list("quest_id", flat=True))

    offers = []
    offered_quest_ids = set()
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

        offers.append(spec)
        offered_quest_ids.add(qid)

    from world.social_quest_offers import get_social_quest_offers_for_npc

    social_offers = get_social_quest_offers_for_npc(
        npc,
        character,
        active_ids=active_ids,
        complete_ids=complete_ids,
        failed_ids=failed_ids,
    )
    offers.extend(
        offer
        for offer in social_offers
        if offer.get("quest_id") not in offered_quest_ids
    )
    return tuple(offers)


def get_available_quest_for_npc(npc, character):
    """Compatibility adapter returning the first eligible NPC offer, if any."""
    offers = get_available_quest_offers_for_npc(npc, character)
    return offers[0] if offers else None


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
