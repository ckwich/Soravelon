"""
Inventory weight calculation helpers.
"""


ENCUMBRANCE_MOVEMENT_STAMINA_COSTS = {
    "encumbered": 2,
    "heavy": 5,
}


def get_movement_stamina_cost(carry_state):
    """Return the per-room stamina cost for a computed carry state."""

    return ENCUMBRANCE_MOVEMENT_STAMINA_COSTS.get(carry_state, 0)


def get_carry_state(character, effective_stats=None):
    """
    Compute character's current carry state.
    Returns: "normal" / "encumbered" / "heavy" / "overloaded"
    """
    from world.models import InventoryItem
    from evennia.objects.models import ObjectDB

    BASE_CAPACITY = 10
    if effective_stats is None:
        from world.equipment_effects import get_effective_stats

        effective_stats = get_effective_stats(character)
    strength = effective_stats.get("strength", 10)
    capacity = BASE_CAPACITY + (strength * 5)

    records = list(InventoryItem.objects.filter(
        character_id=character.id
    ))

    if not records:
        return "normal"

    # Batch fetch all item objects in one query
    all_item_ids = set()
    for record in records:
        all_item_ids.add(record.item_id)
        if record.container_id:
            all_item_ids.add(record.container_id)

    item_lookup = {}
    for obj in ObjectDB.objects.filter(id__in=all_item_ids):
        item_lookup[obj.id] = obj

    # Build container reduction lookup
    container_reduction = {}
    for record in records:
        if record.container_id and record.container_id not in container_reduction:
            container_obj = item_lookup.get(record.container_id)
            if container_obj:
                wr = container_obj.db.weight_reduction
                container_reduction[record.container_id] = wr if wr is not None else 0
            else:
                container_reduction[record.container_id] = 0

    total_weight = 0.0
    for record in records:
        item_obj = item_lookup.get(record.item_id)
        if not item_obj:
            continue
        unit_weight = item_obj.db.weight
        unit_weight = unit_weight if unit_weight is not None else 0.1
        quantity = record.quantity or 1

        if record.container_id:
            reduction = container_reduction.get(record.container_id, 0) / 100
            total_weight += unit_weight * quantity * (1 - reduction)
        else:
            total_weight += unit_weight * quantity

    ratio = total_weight / capacity if capacity > 0 else 999

    if ratio <= 1.0:
        return "normal"
    if ratio <= 1.3:
        return "encumbered"
    if ratio <= 1.6:
        return "heavy"
    return "overloaded"
