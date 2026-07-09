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

from world.base_attributes import derive_max_hp, derive_max_stamina


def consume_item(character, item):
    """
    Consume an item, applying its use_effect. Destroys the item on success.
    Returns (bool, str).
    """
    # Combat action cost check
    if getattr(character.ndb, "in_combat", False):
        action_cost = getattr(item.db, "action_cost", 1)
        actions_remaining = getattr(character.ndb, "actions_remaining", 0)
        if actions_remaining < action_cost:
            return (
                False,
                f"|rUsing {item.key} requires {action_cost} action(s). "
                f"You have {actions_remaining} remaining.|n",
            )
        character.ndb.actions_remaining = actions_remaining - action_cost

    effect = getattr(item.db, "use_effect", None)
    if not effect:
        _destroy(character, item)
        return (True, f"You use {item.key}, but nothing happens.")

    effects_applied = []
    etype = effect.get("type", "")

    if etype == "heal_hp":
        gained = _apply_hp(character, effect.get("amount", 0))
        effects_applied.append(f"restored {gained} HP")

    elif etype == "restore_stamina":
        gained = _apply_stamina(character, effect.get("amount", 0))
        effects_applied.append(f"restored {gained} stamina")

    elif etype == "heal_hp_stamina":
        hp_gained = _apply_hp(character, effect.get("hp", 0))
        stam_gained = _apply_stamina(character, effect.get("stamina", 0))
        if hp_gained:
            effects_applied.append(f"restored {hp_gained} HP")
        if stam_gained:
            effects_applied.append(f"restored {stam_gained} stamina")

    elif etype == "heal_over_time":
        amount = effect.get("amount", 5)
        ticks = effect.get("ticks", 6)
        effects_applied.append(f"healing {amount} HP over {ticks} ticks")

    elif etype == "cure_poison":
        status_effects = getattr(character.ndb, "status_effects", None)
        if status_effects:
            effects = dict(status_effects)
            for key in list(effects):
                if "poison" in key.lower():
                    del effects[key]
                    effects_applied.append(f"cured {key}")
            character.ndb.status_effects = effects
        if not effects_applied:
            effects_applied.append("no poison to cure")

    _destroy(character, item)

    if effects_applied:
        return (True, f"You use {item.key}: {', '.join(effects_applied)}.")
    return (True, f"You use {item.key}.")


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
    """Remove a consumed item through the atomic ownership authority."""
    from world.inventory_engine import destroy_owned_item

    destroyed, message = destroy_owned_item(character, item)
    if not destroyed:
        raise RuntimeError(message)
    from world.oob_publisher import push_inventory_update
    push_inventory_update(character)
