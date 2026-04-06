"""
Trigger Engine for Soravelon.

Dispatches trigger events attached to rooms, mobs, and items.
Enforces once-per-character and cooldown constraints on trigger firing.

Key behaviors:
- fire_triggers(source_obj, event_name, character) iterates source_obj.db.triggers
  and executes all matching trigger actions via world.action_vocabulary.execute_action.
- Triggers fire in definition order (D-18).
- once_per_character triggers are blocked if already seen by this character.
- cooldown_seconds triggers are blocked if fired within the cooldown window.
- Non-Character objects (no .account) are silently rejected (Pitfall 7).
- Depth is propagated to execute_action to enforce chaining limit (D-19).
- Returns None — errors are logged, not raised.

Storage on character:
  character.db.fired_triggers   — set of trigger_ids that fired once-per-char
  character.db.trigger_cooldowns — dict of trigger_id -> datetime of last fire
Both use the SaverDict copy pattern on mutation.
"""

from datetime import datetime, timedelta

import evennia


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _check_once_per(character, trigger_id, trigger):
    """
    Return True (skip) if trigger has once_per_character=True and has already fired.

    Initializes character.db.fired_triggers as an empty set if not set.
    """
    if not trigger.get("once_per_character"):
        return False
    fired = character.db.fired_triggers
    if fired is None:
        fired = set()
        character.db.fired_triggers = fired
    return trigger_id in fired


def _check_cooldown(character, trigger_id, trigger):
    """
    Return True (skip) if trigger has cooldown_seconds > 0 and is still within the window.

    Initializes character.db.trigger_cooldowns as an empty dict if not set.
    """
    cooldown_seconds = trigger.get("cooldown_seconds", 0)
    if not cooldown_seconds:
        return False
    cooldowns = character.db.trigger_cooldowns
    if cooldowns is None:
        cooldowns = {}
        character.db.trigger_cooldowns = cooldowns
    if trigger_id not in cooldowns:
        return False
    last_fire = cooldowns[trigger_id]
    return datetime.utcnow() < last_fire + timedelta(seconds=cooldown_seconds)


def _record_fired(character, trigger_id, trigger):
    """
    Record that this trigger fired for this character.

    Uses SaverDict copy pattern for both fired_triggers (set) and
    trigger_cooldowns (dict) to ensure Evennia persists the changes.
    """
    if trigger.get("once_per_character"):
        # SaverDict copy pattern for set mutations
        fired = character.db.fired_triggers
        if fired is None:
            fired = set()
        fired_copy = set(fired)
        fired_copy.add(trigger_id)
        character.db.fired_triggers = fired_copy

    if trigger.get("cooldown_seconds", 0):
        # SaverDict copy pattern for dict mutations
        cooldowns = character.db.trigger_cooldowns
        if cooldowns is None:
            cooldowns = {}
        cooldowns_copy = dict(cooldowns)
        cooldowns_copy[trigger_id] = datetime.utcnow()
        character.db.trigger_cooldowns = cooldowns_copy


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def fire_triggers(source_obj, event_name, character, context=None, _depth=0):
    """
    Fire all triggers on source_obj matching event_name for character.

    source_obj: room, mob, or item with db.triggers list.
    event_name: "on_enter", "on_exit", "on_first_visit", "on_mob_death", "on_examine"
    character: the Character triggering the event (must have .account to proceed).
    context: optional additional context dict (merged with standard keys).
    _depth: recursion counter for D-19 chaining limit (passed to execute_action).

    Returns None (void). Errors are logged to Evennia logger, not raised.
    """
    # Guard: only fire for actual player characters (Pitfall 7)
    if not hasattr(character, "account") or not character.account:
        return

    triggers = list(source_obj.db.triggers or [])
    if not triggers:
        return

    # Build context dict
    ctx = dict(context) if context else {}
    ctx.update({
        "character": character,
        "room": character.location,
    })

    for trigger in triggers:
        if trigger.get("event") != event_name:
            continue

        trigger_id = trigger.get("trigger_id", "")

        if _check_once_per(character, trigger_id, trigger):
            continue

        if _check_cooldown(character, trigger_id, trigger):
            continue

        # Execute each action in the trigger's action list
        for action in trigger.get("actions", []):
            from world.action_vocabulary import execute_action
            success, msg = execute_action(action, ctx, _depth=_depth)
            if not success:
                try:
                    from evennia.utils import logger
                    logger.log_warn(
                        f"trigger_engine: action failed in trigger "
                        f"'{trigger_id}': {action.get('action_type', '?')} — {msg}"
                    )
                except Exception:
                    pass  # Logging unavailable (e.g., unit test without Django)

        _record_fired(character, trigger_id, trigger)
