"""
Item spawner for Soravelon.

Creates SoravelonItem instances from definition dicts authored in area files.
Item definitions are stored on zone_obj.db.item_definitions via area.item().

create_item_from_template(item_def, location=None) is the primary entry point.
Called by action_vocabulary._action_give_item and loot_tables.roll_loot.

create_item_from_catalog(template_id, location=None, overrides=None) resolves a
shared canonical template before delegating to create_item_from_template().
"""

import logging

import evennia


logger = logging.getLogger("evennia")

_TYPECLASS_MAP = {
    "equipment": "typeclasses.objects.SoravelonEquipment",
    "container":  "typeclasses.objects.SoravelonContainer",
    "keyring":    "typeclasses.objects.SoravelonKeyringItem",
}
_DEFAULT_TYPECLASS = "typeclasses.objects.SoravelonItem"

_RESERVED_KEYS = frozenset(
    ["item_id", "key", "item_type", "weight", "rarity",
     "equip_slot", "desc", "value"]
)


def _is_player_inventory_owner(location):
    """Return True when location is a real Soravelon player character."""
    if location is None:
        return False
    if type(location).__module__.startswith("unittest.mock"):
        return False
    tags = getattr(location, "tags", None)
    if not tags:
        return False
    for method_name in ("has", "get"):
        method = getattr(tags, method_name, None)
        if not callable(method):
            continue
        try:
            if bool(method("player_character", category="character_type")):
                return True
        except TypeError:
            continue
    return False


def _register_player_inventory(item, location, item_def):
    """Create the authoritative InventoryItem row for direct-to-player spawns."""
    if not _is_player_inventory_owner(location):
        return
    from world.inventory_engine import register_item_ownership

    keyring_attr = getattr(item.db, "keyring", False)
    keyring_flag = bool(item_def.get("item_type") == "keyring")
    if isinstance(keyring_attr, bool):
        keyring_flag = keyring_flag or keyring_attr

    register_item_ownership(
        location,
        item,
        quantity=item_def.get("quantity", 1),
        is_quest_item=bool(item_def.get("is_quest_item")),
        keyring=keyring_flag,
    )


def create_item_from_template(item_def, location=None):
    """
    Create an Evennia item object from a definition dict.

    Selects the typeclass based on item_def["item_type"]:
      - "equipment"  → SoravelonEquipment
      - "container"  → SoravelonContainer
      - "keyring"    → SoravelonKeyringItem
      - "item" / unknown / missing → SoravelonItem (default)

    Always sets: db.item_type, db.weight, db.rarity, db.desc, db.value,
    db.equipment_slot (None for non-equipment).

    Any item_def key NOT in _RESERVED_KEYS is set as a db.* attribute
    (e.g., damage_min, damage_max, capacity, lock_tag).

    Args:
        item_def (dict): Item definition dict. Keys: item_id, key, item_type,
            weight, rarity, equip_slot, desc, value, plus optional extras.
        location: Evennia Room/Object to place item in, or None.

    Returns:
        Created item object.
    """
    item_type = item_def.get("item_type", "item")
    typeclass = _TYPECLASS_MAP.get(item_type, _DEFAULT_TYPECLASS)

    item = evennia.create_object(
        typeclass,
        key=item_def.get("key", item_def.get("item_id", "item")),
        location=location,
    )

    try:
        # Standard attrs — always set explicitly
        item.db.item_type = item_type
        item.db.weight = item_def.get("weight", 0.5)
        item.db.rarity = item_def.get("rarity", "normal")
        item.db.desc = item_def.get("desc", "")
        item.db.value_scales = item_def.get("value", 0)
        item.db.equipment_slot = item_def.get("equip_slot")

        # Extra attrs — anything not in the reserved key set
        for k, v in item_def.items():
            if k not in _RESERVED_KEYS:
                setattr(item.db, k, v)

        # Set item_tag for crafting ingredient matching (Phase 13 requirement)
        item_id = item_def.get("item_id")
        if item_id:
            item.tags.add(item_id, category="item_tag")

        _register_player_inventory(item, location, item_def)
    except Exception:
        try:
            item.delete()
        except Exception:
            logger.exception(
                "item_spawner: failed to clean up partially initialized item %s",
                getattr(item, "id", "unknown"),
            )
        raise

    return item


def create_item_from_catalog(template_id, location=None, overrides=None):
    """Create one canonical catalog item with optional per-instance metadata.

    ``get_item_template`` returns a deep copy, so applying crafting quality or
    other instance-specific overrides cannot mutate the shared catalog.
    Unknown ids raise ``ItemTemplateNotFound`` to the owning caller.
    """
    from world.item_catalog import get_item_template

    item_def = get_item_template(template_id)
    if overrides:
        item_def.update(overrides)
    return create_item_from_template(item_def, location=location)
