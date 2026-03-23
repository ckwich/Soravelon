---
name: item-typeclasses
description: Item typeclass hierarchy — SoravelonItem, Container, Equipment, KeyringItem in typeclasses/objects.py
---

## Activation

This skill triggers when editing these files:
- `typeclasses/objects.py`

Keywords: item, container, equipment, keyring, inventory, loot, weight, equip, slot

---

You are working on **item typeclasses** in `typeclasses/objects.py`.

## Hierarchy
```
ObjectParent (mixin) + DefaultObject
  └─ SoravelonObject (base non-char/non-room)
       └─ SoravelonItem (pickupable items)
            ├─ SoravelonContainer (bags with weight reduction)
            ├─ SoravelonEquipment (slot-based gear)
            └─ SoravelonKeyringItem (credentials, zero weight, undropable)
```

## Key Patterns
- **Metadata split:** `db.weight`, `db.rarity`, `db.item_type` live on typeclass; quantity, equip state, quest flag live in `world.models.InventoryItem` Django model
- **`(bool, str)` return convention:** `can_drop()`, `can_equip()`, `can_accept()`, `can_be_sold()` all return `(False, "reason")` or `(True, None)`
- **Lazy import:** All `world.models` imports are inside methods to avoid circular imports
- **`get_inventory_record(character)`:** Fetches the `InventoryItem` row; returns `None` if missing (lazy creation pattern)

## Critical Rules
1. **Never manipulate items directly** — all item operations go through `world/inventory_engine.py`
2. **Containers cannot nest** — `SoravelonContainer.can_accept()` rejects other containers via `isinstance` check
3. **Equipment slots are fixed:** `head`, `body`, `hands`, `feet`, `right_hand`, `left_hand`, `accessory` — adding slots requires updating `VALID_SLOTS`
4. **KeyringItem.at_get()** auto-creates/updates `InventoryItem` with `keyring=True` on pickup — this is the only typeclass that writes to Django on get
5. **KeyringItem blocks `can_drop()`** — removal requires a separate `discard` command, not normal drop
6. **Equipment is never stackable** — `stackable = False` is enforced at creation

## References
- **Inventory Engine:** `world/inventory_engine.py`
- **Django Models:** `world/models.py` (InventoryItem, etc.)
- **Tests:** `tests/test_typeclasses.py`, `tests/test_inventory_engine.py`

---
**Last Updated:** 2026-03-23
