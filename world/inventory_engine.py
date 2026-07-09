"""Soravelon's weight-based inventory interface.

Durable ownership mutations are implemented by ``inventory_transactions``.
This module preserves the established caller interface and owns inventory
queries plus container initialization.
"""

import random

from world.inventory_transactions import (
    _get_container_contents_weight as _get_container_contents_weight,
    destroy_owned_item as destroy_owned_item,
    drop_item as drop_item,
    equip_item as equip_item,
    move_owned_items_to_world_container as move_owned_items_to_world_container,
    pick_up as pick_up,
    put_in_container as put_in_container,
    register_item_ownership as register_item_ownership,
    take_from_container as take_from_container,
    transfer_item as transfer_item,
    unequip_item as unequip_item,
    unregister_item_ownership as unregister_item_ownership,
)
from world.models import InventoryItem


CONTAINER_WEIGHT_RANGES = {
    "common": (0, 10),
    "uncommon": (10, 25),
    "rare": (25, 50),
    "masterwork": (50, 75),
}


def roll_container_weight_reduction(rarity):
    """Roll weight reduction percentage within the authored rarity band."""

    low, high = CONTAINER_WEIGHT_RANGES.get(rarity, (0, 10))
    return random.randint(low, high)


def initialize_container(container_obj, rarity):
    """Initialize one container's rolled weight reduction."""

    reduction = roll_container_weight_reduction(rarity)
    container_obj.db.weight_reduction = reduction
    container_obj.db.rarity = rarity
    return reduction


def equip_items_in_empty_slots(character, items):
    """Equip eligible items without displacing existing gear."""

    for item in items:
        slot = item.db.equipment_slot
        if not slot:
            continue

        occupied_slots = {slot}
        if slot == "ring1":
            occupied_slots.add("ring2")
        if InventoryItem.objects.filter(
            character_id=character.id,
            is_equipped=True,
            equipment_slot__in=occupied_slots,
        ).count() == len(occupied_slots):
            continue

        if (
            slot == "main_hand"
            and bool(item.db.two_handed)
            and InventoryItem.objects.filter(
                character_id=character.id,
                is_equipped=True,
                equipment_slot="off_hand",
            ).exists()
        ):
            continue

        equipped, message = equip_item(character, item)
        if not equipped:
            return False, message

    return True, ""


def get_inventory_display_data(character):
    """Return structured inventory data for CLI and OOB renderers."""

    from world.inventory_helpers import get_carry_state
    from world.equipment_effects import get_effective_stats

    base_capacity = 10
    effective_stats = get_effective_stats(character)
    strength = effective_stats.get("strength", 10) or 10
    carry_capacity = base_capacity + (strength * 5)

    records = list(
        InventoryItem.objects.filter(character_id=character.id).order_by(
            "acquired_at"
        )
    )
    result = {
        "equipped": [],
        "containers": {},
        "carried": [],
        "keyring": [],
        "carried_scales": character.db.carried_scales or 0,
        "carry_state": get_carry_state(
            character,
            effective_stats=effective_stats,
        ),
        "carry_weight": 0.0,
        "carry_capacity": carry_capacity,
    }

    from evennia.objects.models import ObjectDB

    all_ids = set()
    for record in records:
        all_ids.add(record.item_id)
        if record.container_id:
            all_ids.add(record.container_id)
    item_lookup = ObjectDB.objects.in_bulk(all_ids)

    total_weight = 0.0
    for record in records:
        item = item_lookup.get(record.item_id)
        if not item:
            continue

        if not record.keyring:
            unit_weight = item.db.weight or 0.1
            if record.container_id:
                container = item_lookup.get(record.container_id)
                if container:
                    reduction = (container.db.weight_reduction or 0) / 100
                    total_weight += (
                        unit_weight * record.quantity * (1 - reduction)
                    )
            else:
                total_weight += unit_weight * record.quantity

        if record.keyring:
            result["keyring"].append((item, record))
        elif record.is_equipped:
            result["equipped"].append((item, record))
        elif record.container_id:
            container = item_lookup.get(record.container_id)
            if container:
                result["containers"].setdefault(container, []).append(
                    (item, record)
                )
        else:
            result["carried"].append((item, record))

    result["carry_weight"] = round(total_weight, 2)
    return result


def get_filtered_inventory(character, filter_str):
    """Return owned items matching a case-insensitive name or item type."""

    from evennia.objects.models import ObjectDB

    filter_lower = filter_str.lower()
    records = list(InventoryItem.objects.filter(character_id=character.id))
    if not records:
        return []
    item_lookup = ObjectDB.objects.in_bulk(record.item_id for record in records)

    matches = []
    for record in records:
        item = item_lookup.get(record.item_id)
        if not item:
            continue
        item_type = getattr(item.db, "item_type", "") or ""
        if filter_lower in item.key.lower() or filter_lower in item_type.lower():
            matches.append((item, record))
    return matches


def get_equipped_items(character):
    """Return the character's current equipped-object/metadata pairs."""

    from evennia.objects.models import ObjectDB

    records = list(
        InventoryItem.objects.filter(
            character_id=character.id,
            is_equipped=True,
        )
    )
    if not records:
        return []
    item_lookup = ObjectDB.objects.in_bulk(record.item_id for record in records)
    return [
        (item_lookup[record.item_id], record)
        for record in records
        if record.item_id in item_lookup
    ]
