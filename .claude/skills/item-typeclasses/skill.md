---
name: item-typeclasses
description: Item typeclass hierarchy — SoravelonItem, Container, Equipment, KeyringItem in typeclasses/objects.py
---

## Activation

This skill triggers when editing these files:
- `typeclasses/objects.py`

Keywords: item, container, equipment, keyring, inventory, loot, weight, equip, slot, two-handed, ring

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

## Equipment Slots (13 total)
`head`, `face`, `chest`, `back`, `hands`, `wrists`, `legs`, `feet`, `main_hand`, `off_hand`, `ring1`, `ring2`, `amulet` — one item per slot enforced in `can_equip()`

## Equipment Attributes
- `db.equipment_slot` — target slot name
- `db.stat_bonuses` — dict of stat modifiers
- `db.two_handed` — bool, requires both main_hand and off_hand free
- `db.armor_value` — integer armor rating
- `db.damage_min` / `db.damage_max` — weapon damage range
- `db.material_tier` — integer tier for crafting/loot systems

## Equipment Logic in `can_equip()`
- **Two-handed check:** If `db.two_handed` and slot is `main_hand`, checks off_hand is empty. Blocks off_hand equip if main_hand holds a two-handed weapon
- **Ring auto-fill:** If `ring1` is occupied, automatically redirects to `ring2`. Fails only if both ring slots occupied
- **Standard slot check:** One item per slot via `InventoryItem` query

## Critical Rules
1. **Never manipulate items directly** — all item operations go through `world/inventory_engine.py`
2. **Containers cannot nest** — `SoravelonContainer.can_accept()` rejects other containers via `isinstance` check
3. **Equipment slots are fixed:** 13 slots in `VALID_SLOTS` — adding slots requires updating the set
4. **KeyringItem.at_get()** auto-creates/updates `InventoryItem` with `keyring=True` on pickup — this is the only typeclass that writes to Django on get
5. **KeyringItem blocks `can_drop()`** — removal requires a separate `discard` command, not normal drop
6. **Equipment is never stackable** — `stackable = False` is enforced at creation
7. **Ring auto-fill mutates `db.equipment_slot`** — `can_equip()` changes the slot from `ring1` to `ring2` in place when ring1 is occupied

## References
- **Inventory Engine:** `world/inventory_engine.py`
- **Django Models:** `world/models.py` (InventoryItem, etc.)
- **Tests:** `tests/test_typeclasses.py`, `tests/test_inventory_engine.py`, `tests/test_equipment_slots.py`

---
**Last Updated:** 2026-03-29
