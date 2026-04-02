---
created: 2026-04-02T19:48:27.331Z
title: Refactor equipment catalog out of areas folder
area: architecture
files:
  - world/areas/equipment_catalog.py
  - world/item_spawner.py
  - world/area_builder.py
---

## Problem

`world/areas/equipment_catalog.py` is a data registry pretending to be a zone — it creates a ZoneObject with no rooms and stuffs 76 item definitions into `zone_obj.db.item_definitions`. It lives in `world/areas/` only because `_load_all_zones()` auto-discovers `.py` files there, which is a side-effect dependency.

This causes several issues:
- The builder app would show "Equipment Catalog" as a zone with 0 rooms and 76 items
- Item definitions use `equip_slot` field name but the DB attribute is `equipment_slot` (Phase 8 fixed the write side but not the definition source)
- `item_spawner.create_item_from_template()` searches ALL zone objects to find item definitions — scanning game zones for what is really catalog data
- Mixing catalog data with zone specs makes the areas/ directory confusing

## Solution

1. Move to `world/item_catalog.py` as a proper Python module with a dict-based registry (like `RECIPE_REGISTRY` or `MOB_TEMPLATES`)
2. Change `item_spawner.create_item_from_template()` to look up from the new registry instead of scanning `zone_obj.db.item_definitions`
3. Keep `area.item()` functional for zone-specific items (quest items, unique drops) but the global equipment catalog should be a standalone module
4. Normalize all `equip_slot` references in definitions to `equipment_slot` for consistency
5. Update zone_serializer if it handles item defs (it does — check the `item()` pathway)
6. Update builder app schema to reflect the split: zone items vs catalog items
