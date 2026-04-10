---
name: inventory-engine
description: Item lifecycle engine — pickup, drop, equip, containers, stacking, keyring, encumbrance
---

## Activation

This skill triggers when editing inventory-related files:
- `world/inventory_engine.py`
- `world/inventory_helpers.py`
- `typeclasses/objects.py`
- `world/models.py`

Keywords: inventory, item, pickup, drop, equip, unequip, container, keyring, encumbrance, carry weight, stacking

---

You are working on **soravelon's inventory engine** — stateless service functions that manage all item movement.

## Key Files
- `world/inventory_engine.py` — All item ops: pick_up, drop_item, put_in_container, take_from_container, equip/unequip, query helpers
- `world/inventory_helpers.py` — `get_carry_state()` weight/encumbrance calculation
- `typeclasses/objects.py` — Item typeclasses: `SoravelonItem`, `SoravelonContainer`, `SoravelonEquipment`, `SoravelonKeyringItem`
- `world/models.py` — `InventoryItem` Django model (the source of truth for quantity, equip state, container assignment, keyring flag)

## Key Concepts
- **Dual-record system:** Evennia object holds intrinsic props (`weight`, `rarity`, `item_type`); `InventoryItem` model holds relational state (`quantity`, `is_equipped`, `container_id`, `keyring`)
- **Auto-stacking:** On pickup, stackable items merge into existing stack (same `key` + `item_type` + `stackable=True`). Merged item object is **deleted**
- **Partial stack drop:** Splits stack by cloning the object and copying attrs, then adjusting record quantity
- **Keyring routing:** `SoravelonKeyringItem` instances get `keyring=True` on their record. Zero weight, cannot be dropped
- **Container weight reduction:** Rolled per-container by rarity band (`CONTAINER_WEIGHT_RANGES`). Stored as `db.weight_reduction` (integer 0-75, applied as `/100`)
- **Encumbrance thresholds:** capacity = `10 + (strength * 5)` kg. Ratio ≤1.0 normal, ≤1.3 encumbered, ≤1.6 heavy, >1.6 overloaded
- **Equipment slots:** `head`, `body`, `hands`, `feet`, `right_hand`, `left_hand`, `accessory` — one item per slot enforced in `can_equip()`

## Critical Rules
1. **All item ops go through `inventory_engine.py`** — never move items by setting `location` directly without updating the `InventoryItem` record
2. **Containers cannot nest** — `SoravelonContainer.can_accept()` rejects other containers
3. **Must unequip before drop or container pack** — checked in `drop_item()` and `put_in_container()`
4. **Quest items cannot be dropped or sold** — enforced in `can_drop()` and `can_be_sold()`
5. **Batch-fetch pattern required** — collect IDs → single `filter(id__in=ids)` → dict lookup. All query helpers already follow this; new queries must too
6. **`item_id` is unique** — one `InventoryItem` record per Evennia object, not per character. Stacking merges into existing record and deletes the picked-up object
7. **Scales are NOT inventory** — `carried_scales` is managed by the banking system, not inventory engine

## References
- **Model definitions:** `world/models.py`
- **Item typeclasses:** `typeclasses/objects.py`
- **Tests:** `tests/test_inventory_engine.py`

---
**Last Updated:** 2026-03-23
