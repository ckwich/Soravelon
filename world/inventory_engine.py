"""
Inventory engine for Soravelon.

All item movement in and out of character inventory goes through
this module. Keeps Evennia containment and InventoryItem Django
records in sync.

- Scales (carried_scales) are NOT managed here — use banking system.
- Auto-stacking for stackable items on pickup.
- Keyring routing for SoravelonKeyringItem instances.
- Container capacity enforcement.
"""

import random
import evennia
from world.models import InventoryItem


# ---------------------------------------------------------------------------
# Container weight reduction rolling
# ---------------------------------------------------------------------------

CONTAINER_WEIGHT_RANGES = {
    "common":     (0,  10),
    "uncommon":   (10, 25),
    "rare":       (25, 50),
    "masterwork": (50, 75),
}


def roll_container_weight_reduction(rarity):
    """Roll weight reduction % for a container within its rarity band."""
    low, high = CONTAINER_WEIGHT_RANGES.get(rarity, (0, 10))
    return random.randint(low, high)


def initialize_container(container_obj, rarity):
    """Set weight_reduction on a new container based on rarity."""
    reduction = roll_container_weight_reduction(rarity)
    container_obj.db.weight_reduction = reduction
    container_obj.db.rarity = rarity
    return reduction


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_or_create_inventory_record(character, item, **defaults):
    record, created = InventoryItem.objects.get_or_create(
        character_id=character.id,
        item_id=item.id,
        defaults={"quantity": 1, **defaults}
    )
    return record, created


def _delete_inventory_record(character, item):
    InventoryItem.objects.filter(
        character_id=character.id,
        item_id=item.id
    ).delete()


def _find_existing_stack(character, item):
    """Find an existing stack of the same item type for auto-stacking."""
    from evennia.objects.models import ObjectDB

    if not bool(item.db.stackable):
        return None

    item_type = item.db.item_type

    existing_records = list(InventoryItem.objects.filter(
        character_id=character.id,
        is_quest_item=False,
        is_equipped=False
    ))

    if not existing_records:
        return None

    item_ids = [record.item_id for record in existing_records]
    item_lookup = {obj.id: obj for obj in ObjectDB.objects.filter(id__in=item_ids)}

    for record in existing_records:
        existing = item_lookup.get(record.item_id)
        if not existing:
            continue

        if (existing.key == item.key
                and existing.db.item_type == item_type
                and bool(existing.db.stackable)):
            return existing

    return None


def _get_container_contents_weight(character, container):
    """Calculate total effective weight of items in container."""
    from evennia.objects.models import ObjectDB

    records = list(InventoryItem.objects.filter(
        character_id=character.id,
        container_id=container.id
    ))

    if not records:
        return 0.0

    item_ids = [record.item_id for record in records]
    item_lookup = {obj.id: obj for obj in ObjectDB.objects.filter(id__in=item_ids)}

    total = 0.0
    for record in records:
        item_obj = item_lookup.get(record.item_id)
        if item_obj:
            unit_weight = (item_obj.db.weight or 0.1)
            effective = container.get_effective_weight_of(
                unit_weight, record.quantity
            )
            total += effective
    return total


# ---------------------------------------------------------------------------
# Pickup
# ---------------------------------------------------------------------------

def pick_up(character, item, container=None):
    """
    Pick up an item from a room (or from a container).
    Handles auto-stacking and keyring routing.
    Returns (success: bool, message: str).
    """
    from typeclasses.objects import SoravelonKeyringItem

    # Validate location
    if container:
        if item.location != container:
            return False, f"That's not in {container.key}."
    else:
        if item.location != character.location:
            return False, "You don't see that here."

    # Check for auto-stack
    existing_stack = _find_existing_stack(character, item)
    if existing_stack:
        record = InventoryItem.objects.get(
            character_id=character.id,
            item_id=existing_stack.id
        )
        qty_to_add = getattr(item.db, 'quantity', 1) or 1
        record.quantity += qty_to_add
        record.save()

        item_key = item.key
        item.delete()

        return True, (
            f"You pick up the {item_key}. "
            f"You now have {record.quantity}."
        )

    # Keyring routing
    is_keyring = isinstance(item, SoravelonKeyringItem)

    # Move item to character
    item.move_to(character, quiet=True)

    # Create InventoryItem record
    record, _ = _get_or_create_inventory_record(
        character, item,
        quantity=getattr(item.db, 'quantity', 1) or 1,
        container_id=None,
        is_quest_item=bool(item.db.is_quest_item),
        keyring=is_keyring,
    )

    return True, f"You pick up the {item.key}."


# ---------------------------------------------------------------------------
# Drop
# ---------------------------------------------------------------------------

def drop_item(character, item, quantity=None):
    """
    Drop an item from inventory to the current room.
    Returns (success: bool, message: str).
    """
    can, reason = item.can_drop(character)
    if not can:
        return False, reason

    record = item.get_inventory_record(character)
    if not record:
        return False, "You don't have that."

    if record.is_equipped:
        return False, f"Unequip {item.key} before dropping it."

    # Partial stack drop
    if quantity and record.quantity > quantity:
        from evennia import create_object

        dropped = create_object(
            item.__class__,
            key=item.key,
            location=character.location
        )
        for attr_name in (
            'weight', 'rarity', 'item_type', 'stackable',
            'value_scales', 'desc', 'lore_desc',
            'weight_reduction', 'weight_capacity',
        ):
            val = getattr(item.db, attr_name, None)
            if val is not None:
                setattr(dropped.db, attr_name, val)

        record.quantity -= quantity
        record.save()

        return True, f"You drop {quantity} {item.key}."

    # Full drop
    item.move_to(character.location, quiet=True)
    _delete_inventory_record(character, item)

    return True, f"You drop the {item.key}."


# ---------------------------------------------------------------------------
# Container operations
# ---------------------------------------------------------------------------

def put_in_container(character, item, container):
    """Move an item from direct carry into a container."""
    from typeclasses.objects import SoravelonContainer

    if not isinstance(container, SoravelonContainer):
        return False, f"{container.key} isn't a container."

    can_accept, reason = container.can_accept(item)
    if not can_accept:
        return False, reason

    record = item.get_inventory_record(character)
    if not record:
        return False, "You don't have that."
    if record.container_id:
        return False, f"{item.key} is already in a container."
    if record.is_equipped:
        return False, f"Unequip {item.key} before packing it."

    current_weight = _get_container_contents_weight(character, container)
    item_weight = container.get_effective_weight_of(
        item.db.weight, record.quantity
    )

    if current_weight + item_weight > container.db.weight_capacity:
        return False, (
            f"{container.key} is too full. "
            f"Capacity: {container.db.weight_capacity} kg."
        )

    record.container_id = container.id
    record.save()

    return True, f"You put the {item.key} in {container.key}."


def take_from_container(character, item, container=None):
    """Move an item from a container to direct carry."""
    record = item.get_inventory_record(character)
    if not record:
        return False, "You don't have that."

    if not record.container_id:
        return False, f"{item.key} isn't in a container."

    if container:
        if record.container_id != container.id:
            return False, f"{item.key} isn't in {container.key}."

    record.container_id = None
    record.save()

    return True, f"You take the {item.key} out."


# ---------------------------------------------------------------------------
# Equip / Unequip
# ---------------------------------------------------------------------------

def equip_item(character, item):
    """Equip an item to its designated slot."""
    can, reason = item.can_equip(character)
    if not can:
        return False, reason

    record = item.get_inventory_record(character)
    if not record:
        return False, "You don't have that."

    if record.container_id:
        return False, f"Take {item.key} out of your container first."

    slot = item.db.equipment_slot
    record.is_equipped = True
    record.equipment_slot = slot
    record.save()

    return True, f"You equip the {item.key}."


def unequip_item(character, item):
    """Unequip an item, returning it to direct carry."""
    record = item.get_inventory_record(character)
    if not record:
        return False, "You don't have that."

    if not record.is_equipped:
        return False, f"{item.key} isn't equipped."

    record.is_equipped = False
    record.equipment_slot = None
    record.save()

    return True, f"You unequip the {item.key}."


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def get_inventory_display_data(character):
    """Return structured inventory data for the i command renderer."""
    from world.inventory_helpers import get_carry_state

    BASE_CAPACITY = 10
    base_stats = character.db.base_stats or {}
    strength = base_stats.get("strength", 10) or 10
    carry_capacity = BASE_CAPACITY + (strength * 5)

    records = InventoryItem.objects.filter(
        character_id=character.id
    ).order_by('acquired_at')

    result = {
        "equipped": [],
        "containers": {},
        "carried": [],
        "keyring": [],
        "carried_scales": (character.db.carried_scales or 0),
        "carry_state": get_carry_state(character),
        "carry_weight": 0.0,
        "carry_capacity": carry_capacity,
    }

    from evennia.objects.models import ObjectDB

    # Batch fetch all item and container objects in one query
    all_ids = set()
    for record in records:
        all_ids.add(record.item_id)
        if record.container_id:
            all_ids.add(record.container_id)

    item_lookup = {obj.id: obj for obj in ObjectDB.objects.filter(id__in=all_ids)}

    total_weight = 0.0

    for record in records:
        item = item_lookup.get(record.item_id)
        if not item:
            continue

        if not record.keyring:
            unit_weight = (item.db.weight or 0.1)
            if record.container_id:
                cont = item_lookup.get(record.container_id)
                if cont:
                    reduction = getattr(
                        cont.db, 'weight_reduction', 0
                    ) / 100
                    total_weight += unit_weight * record.quantity * (1 - reduction)
            else:
                total_weight += unit_weight * record.quantity

        if record.keyring:
            result["keyring"].append((item, record))
        elif record.is_equipped:
            result["equipped"].append((item, record))
        elif record.container_id:
            cont = item_lookup.get(record.container_id)
            if cont:
                if cont not in result["containers"]:
                    result["containers"][cont] = []
                result["containers"][cont].append((item, record))
        else:
            result["carried"].append((item, record))

    result["carry_weight"] = round(total_weight, 2)
    return result


def get_filtered_inventory(character, filter_str):
    """Return inventory items matching filter_str in name or item_type."""
    from evennia.objects.models import ObjectDB

    filter_lower = filter_str.lower()
    records = list(InventoryItem.objects.filter(character_id=character.id))
    matches = []

    if not records:
        return matches

    item_ids = [record.item_id for record in records]
    item_lookup = {obj.id: obj for obj in ObjectDB.objects.filter(id__in=item_ids)}

    for record in records:
        item = item_lookup.get(record.item_id)
        if not item:
            continue

        if (filter_lower in item.key.lower()
                or filter_lower in (
                    getattr(item.db, 'item_type', '') or ''
                ).lower()):
            matches.append((item, record))

    return matches


def get_equipped_items(character):
    """Return all currently equipped items for combat stat calculation."""
    from evennia.objects.models import ObjectDB

    records = list(InventoryItem.objects.filter(
        character_id=character.id,
        is_equipped=True
    ))

    if not records:
        return []

    item_ids = [record.item_id for record in records]
    item_lookup = {obj.id: obj for obj in ObjectDB.objects.filter(id__in=item_ids)}

    result = []
    for record in records:
        item = item_lookup.get(record.item_id)
        if item:
            result.append((item, record))
    return result
