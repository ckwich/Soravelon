"""
Item effects engine — consumable use dispatch.

All consumable items use a use_effect dict:
  {"type": "heal_hp", "amount": 30}
  {"type": "restore_stamina", "amount": 20}
  {"type": "heal_hp_stamina", "hp": 10, "stamina": 15}
  {"type": "heal_over_time", "amount": 5, "ticks": 6}
  {"type": "cure_poison"}

Public API:
    consume_item(character, item) -> (bool, str)
"""

from collections.abc import Mapping
from copy import deepcopy

from world.base_attributes import derive_max_hp, derive_max_stamina


SUPPORTED_EFFECT_TYPES = {
    "heal_hp",
    "restore_stamina",
    "heal_hp_stamina",
    "heal_over_time",
    "cure_poison",
}


def _positive_number(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and value > 0
    )


def _validate_effect(effect):
    if not isinstance(effect, Mapping):
        return False, "That item cannot be used directly."
    effect_type = effect.get("type")
    if effect_type not in SUPPORTED_EFFECT_TYPES:
        return False, "That item's effect cannot be used safely."
    if effect_type in {"heal_hp", "restore_stamina"}:
        if not _positive_number(effect.get("amount")):
            return False, "That item's effect is invalid."
    elif effect_type == "heal_hp_stamina":
        if not any(_positive_number(effect.get(field)) for field in ("hp", "stamina")):
            return False, "That item's effect is invalid."
    elif effect_type == "heal_over_time":
        if not _positive_number(effect.get("amount")) or not (
            isinstance(effect.get("ticks"), int)
            and not isinstance(effect.get("ticks"), bool)
            and effect["ticks"] > 0
        ):
            return False, "That item's effect is invalid."
    return True, ""


def _snapshot_volatile_state(character):
    return {
        "hp": getattr(character.ndb, "hp", None),
        "stamina": getattr(character.ndb, "stamina", None),
        "active_effects": deepcopy(
            getattr(character.ndb, "active_effects", None)
        ),
        "actions_remaining": getattr(character.ndb, "actions_remaining", None),
    }


def _restore_volatile_state(character, snapshot):
    for field, value in snapshot.items():
        setattr(character.ndb, field, deepcopy(value))


def consume_item(character, item):
    """
    Consume an item, applying its use_effect. Destroys the item on success.
    Returns (bool, str).
    """
    effect = getattr(item.db, "use_effect", None)
    if not effect:
        item_name = str(getattr(item, "key", "item"))
        if "bait" in item_name.lower():
            return False, "Fishing bait is used through fishing, not by itself."
        return False, "That item cannot be used directly."
    valid, validation_message = _validate_effect(effect)
    if not valid:
        return False, validation_message

    action_cost = 0
    if getattr(character.ndb, "in_combat", False):
        action_cost = getattr(item.db, "action_cost", 1)
        actions_remaining = getattr(character.ndb, "actions_remaining", 0)
        if actions_remaining < action_cost:
            return (
                False,
                f"|rUsing {item.key} requires {action_cost} action(s). "
                f"You have {actions_remaining} remaining.|n",
            )

    snapshot = _snapshot_volatile_state(character)
    effects_applied = []
    etype = effect["type"]

    if etype == "heal_hp":
        gained = _apply_hp(character, effect.get("amount", 0))
        if gained <= 0:
            return False, "You are already at full health."
        effects_applied.append(f"restored {gained} HP")

    elif etype == "restore_stamina":
        gained = _apply_stamina(character, effect.get("amount", 0))
        if gained <= 0:
            return False, "Your stamina is already full."
        effects_applied.append(f"restored {gained} stamina")

    elif etype == "heal_hp_stamina":
        hp_gained = _apply_hp(character, effect.get("hp", 0))
        stam_gained = _apply_stamina(character, effect.get("stamina", 0))
        if hp_gained:
            effects_applied.append(f"restored {hp_gained} HP")
        if stam_gained:
            effects_applied.append(f"restored {stam_gained} stamina")
        if not effects_applied:
            return False, "Your health and stamina are already full."

    elif etype == "heal_over_time":
        amount = effect.get("amount", 5)
        ticks = effect.get("ticks", 6)
        from world.status_effects import apply_effect

        applied, message = apply_effect(
            character,
            "regeneration",
            duration=ticks,
            magnitude=amount,
            source_id=getattr(character, "id", None),
            data={"heal_per_round": amount},
        )
        if not applied:
            _restore_volatile_state(character, snapshot)
            return False, message
        effects_applied.append(f"healing {amount} HP over {ticks} ticks")

    elif etype == "cure_poison":
        from world.status_effects import has_effect, remove_effect

        if not has_effect(character, "poison"):
            return False, "You are not poisoned."
        remove_effect(character, "poison")
        effects_applied.append("cured poison")

    item_name = item.key
    try:
        _destroy(character, item)
    except Exception as error:
        _restore_volatile_state(character, snapshot)
        return False, str(error)

    if action_cost:
        character.ndb.actions_remaining -= action_cost

    if effects_applied:
        return (True, f"You use {item_name}: {', '.join(effects_applied)}.")
    return (True, f"You use {item_name}.")


def _apply_hp(character, amount):
    """Apply HP healing, return actual amount gained."""
    max_hp = derive_max_hp(character)
    current = character.ndb.hp if character.ndb.hp is not None else max_hp
    new_hp = min(current + amount, max_hp)
    character.ndb.hp = new_hp
    return new_hp - current


def _apply_stamina(character, amount):
    """Apply stamina restoration, return actual amount gained."""
    max_stam = derive_max_stamina(character)
    current = character.ndb.stamina if character.ndb.stamina is not None else max_stam
    new_stam = min(current + amount, max_stam)
    character.ndb.stamina = new_stam
    return new_stam - current


def _destroy(character, item):
    """Consume one owned quantity through the atomic inventory authority."""
    from world.inventory_engine import consume_owned_quantities

    consumed, message = consume_owned_quantities(
        character,
        [{"item": item, "quantity": 1}],
    )
    if not consumed:
        raise RuntimeError(message)
    from world.oob_publisher import push_inventory_update
    try:
        push_inventory_update(character)
    except Exception:
        import logging

        logging.getLogger("evennia").exception(
            "item_effects: inventory OOB update failed after consumption"
        )
