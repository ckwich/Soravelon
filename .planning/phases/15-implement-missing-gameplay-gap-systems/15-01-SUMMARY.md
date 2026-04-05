---
phase: 15-implement-missing-gameplay-gap-systems
plan: 01
subsystem: vendor-economy
tags: [vendor, economy, commerce, NPC, equipment]
dependency_graph:
  requires: [equipment_catalog, item_spawner, inventory_engine, banking]
  provides: [vendor_engine, cmd_vendor, vendor_npc_wiring]
  affects: [vaels_crossing, default_cmdsets]
tech_stack:
  added: []
  patterns: [engine-command-dispatch, catalog-dict-source-of-truth]
key_files:
  created:
    - world/vendor_engine.py
    - commands/cmd_vendor.py
    - tests/test_vendor_engine.py
  modified:
    - world/areas/equipment_catalog.py
    - world/areas/vaels_crossing.py
    - commands/default_cmdsets.py
decisions:
  - CATALOG dict is the single source of truth for item defs; build() iterates it
  - Vendors use carried_scales, not bank balance
  - 33% sell-back ratio (SELL_RATIO = 0.33)
  - Vendor type restrictions via db.vendor_accepts list
  - Added npc_tanner_blackhide NPC to mk_tanner room (was missing)
metrics:
  duration_seconds: 634
  completed: "2026-04-05T06:57:32Z"
  tasks_completed: 2
  tasks_total: 2
  tests_passed: 11
  files_created: 3
  files_modified: 3
---

# Phase 15 Plan 01: Vendor Economy System Summary

Vendor/shop economy system with buy/sell/appraise/list/view commands, type-restricted NPC vendors, and CATALOG-based stock management.

## Task Results

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Vendor engine + CATALOG extraction | f2d70bb | world/vendor_engine.py, world/areas/equipment_catalog.py, tests/test_vendor_engine.py |
| 2 | Vendor commands + NPC wiring | 9bcbe5e | commands/cmd_vendor.py, commands/default_cmdsets.py, world/areas/vaels_crossing.py |

## What Was Built

### world/vendor_engine.py
- `buy_item(character, vendor, item_id)` -- deducts carried_scales, creates item via item_spawner
- `sell_item(character, vendor, item)` -- pays 33% of value, adds to vendor player_stock, deletes item
- `appraise_item(character, vendor, item)` -- returns sell price without transaction
- `view_item(vendor, item_id)` -- full stat display from vendor stock
- `get_vendor_stock(vendor)` -- CATALOG base filtered by vendor_accepts + player-sold items
- `get_vendor_price(vendor, item_def, character)` -- faction-based price discounts (max 20%)
- `_find_vendor_in_room(character)` -- locates vendor NPC in room

### world/areas/equipment_catalog.py
- Refactored from inline `area.item()` calls to CATALOG dict as single source of truth
- 75 items defined: 71 equipment + 4 consumables across 3 material tiers
- `build()` now iterates CATALOG to register items via AreaBuilder

### commands/cmd_vendor.py
- CmdList, CmdBuy, CmdSell, CmdAppraise, CmdView -- all Commerce category
- Thin dispatchers to vendor_engine functions
- Partial name matching for sell/appraise (inventory search)

### Vaels Crossing Vendor NPCs
- npc_weaponsmith_brenna: vendor_accepts=["equipment"]
- npc_armorsmith_derik: vendor_accepts=["equipment"]
- npc_apothecary_ystra: vendor_accepts=["consumable", "ingredient"]
- npc_shopkeep_haldric: vendor_accepts=["item", "material"]
- npc_tanner_blackhide: vendor_accepts=["hide"] (new NPC added)

## Deviations from Plan

### Auto-added Missing Functionality

**1. [Rule 2] Added npc_tanner_blackhide NPC**
- **Found during:** Task 2
- **Issue:** Plan referenced "mk_tanner NPC" but mk_tanner was a room with no NPC
- **Fix:** Created npc_tanner_blackhide in mk_tanner room with vendor attributes
- **Files modified:** world/areas/vaels_crossing.py

**2. [Rule 3] Fixed UTF-8 encoding in equipment_catalog.py**
- **Found during:** Task 1
- **Issue:** Generated CATALOG file had cp1252 em dash bytes (0x97)
- **Fix:** Re-encoded file as UTF-8, replaced em dashes with --
- **Files modified:** world/areas/equipment_catalog.py

## Known Stubs

None -- all vendor functions are fully wired to real data sources.

## Self-Check: PASSED
