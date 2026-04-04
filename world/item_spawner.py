"""
Item spawner for Soravelon.

Creates SoravelonItem instances from definition dicts authored in area files.
Item definitions are stored on zone_obj.db.item_definitions via area.item().

create_item_from_template(item_def, location=None) is the primary entry point.
Called by action_vocabulary._action_give_item and loot_tables.roll_loot.
"""

import evennia

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

    # Standard attrs — always set explicitly
    item.db.item_type  = item_type
    item.db.weight     = item_def.get("weight", 0.5)
    item.db.rarity     = item_def.get("rarity", "normal")
    item.db.desc       = item_def.get("desc", "")
    item.db.value      = item_def.get("value", 0)
    item.db.equipment_slot = item_def.get("equip_slot")  # None for non-equipment

    # Extra attrs — anything not in the reserved key set
    for k, v in item_def.items():
        if k not in _RESERVED_KEYS:
            setattr(item.db, k, v)

    # Set item_tag for crafting ingredient matching (Phase 13 requirement)
    item_id = item_def.get("item_id")
    if item_id:
        item.tags.add(item_id, category="item_tag")

    return item
