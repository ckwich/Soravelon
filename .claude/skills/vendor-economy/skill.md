---
name: vendor-economy
description: Vendor engine — buy/sell/appraise/view with CATALOG-sourced stock, type-restricted NPC vendors, faction price discounts, and player-sold item resale
---

## Activation

This skill triggers when editing these files:
- `world/vendor_engine.py`
- `commands/cmd_vendor.py`
- `world/areas/equipment_catalog.py`
- `tests/test_vendor_engine.py`

Keywords: vendor, buy, sell, appraise, shop, commerce, vendor stock, CATALOG, equipment catalog, vendor_accepts, carried_scales, sell ratio

---

You are working on **the vendor economy system** (`world/vendor_engine.py`) — NPC vendor buy/sell/appraise/view with CATALOG-sourced stock.

## Key Files
- `world/vendor_engine.py` — All vendor logic: `buy_item()`, `sell_item()`, `appraise_item()`, `view_item()`, `get_vendor_stock()`, `get_vendor_price()`, `_find_vendor_in_room()`
- `commands/cmd_vendor.py` — 5 commands: CmdList, CmdBuy, CmdSell, CmdAppraise, CmdView (all Commerce category)
- `world/areas/equipment_catalog.py` — `CATALOG` dict (single source of truth), `build()` iterates CATALOG to register via AreaBuilder
- `tests/test_vendor_engine.py` — unittest.TestCase + MagicMock (no Evennia DB)
- `commands/default_cmdsets.py` — All 5 vendor commands registered in `CharacterCmdSet`

## Key Concepts
- **CATALOG is single source of truth:** `world/areas/equipment_catalog.py` defines all item defs in a `CATALOG` dict. `build()` iterates it. Vendor engine imports and filters it
- **CATALOG item types:** equipment, consumable, ingredient, item, material, tool. Tools have `tool_slot` and `tool_tag` fields. Quest items have `is_quest_item: True`. Consumables use a `use_effect` dict with `type` key (`heal_hp`, `restore_stamina`, `heal_hp_stamina`, `heal_over_time`, `cure_poison`) and type-specific params (`amount`, `hp`, `stamina`, `ticks`)
- **Vendor stock = CATALOG filtered + player-sold:** `get_vendor_stock()` filters CATALOG by `vendor_npc.db.vendor_accepts` list, then merges `vendor_npc.db.player_stock`
- **Carried Scales, not bank:** All transactions use `character.db.carried_scales` directly. NOT the banking system's `BankAccount`
- **33% sell-back ratio:** `SELL_RATIO = 0.33`. Minimum 1 Scale via `max(1, floor(value * 0.33))`
- **Type restrictions:** Each vendor NPC has `db.vendor_accepts` list (e.g. `["equipment"]`, `["consumable", "ingredient"]`). Sell rejected if item type not in list
- **Faction price discounts:** `get_vendor_price()` checks `vendor_npc.db.vendor_faction`. Standing maps to max 20% discount (`standing * 0.002`)
- **Player-sold items resold:** Sold items stored in `vendor_npc.db.player_stock` dict at full value. Removed from player_stock on re-purchase (if not in CATALOG)
- **Item creation via item_spawner:** `buy_item()` calls `create_item_from_template(item_def, location=character)` to create the purchased object
- **Commands are thin dispatchers:** All 5 commands delegate to `vendor_engine.py` functions. Sell/appraise use partial name matching on inventory

## Vendor NPC Attributes
- `db.is_vendor = True` — identifies NPC as vendor (searched by `_find_vendor_in_room()`)
- `db.vendor_accepts` — list of accepted item_type strings
- `db.vendor_faction` — optional faction ID for price discounts
- `db.player_stock` — dict of player-sold items available for resale

## Vaels Crossing Vendors
- npc_weaponsmith_brenna: `["equipment"]`
- npc_armorsmith_derik: `["equipment"]`
- npc_apothecary_ystra: `["consumable", "ingredient"]`
- npc_shopkeep_haldric: `["item", "material"]`
- npc_tanner_blackhide: `["hide"]`

## Critical Rules
1. **All functions return `(bool, str)` tuples** — follows repo-wide convention
2. **Use `carried_scales`, never bank balance** — vendor transactions are immediate cash, not banking
3. **`can_be_sold()` gate** — `sell_item()` and `appraise_item()` call `item.can_be_sold(character)` to block quest items (`is_quest_item: True`)
4. **Lazy import of `get_standing`** — inside `get_vendor_price()` to avoid circular deps
5. **CATALOG items persist in stock** — only player-sold items are removed from `player_stock` on re-purchase
6. **SaverDict copy for player_stock** — both `buy_item()` and `sell_item()` copy `vendor_npc.db.player_stock` to plain dict before mutation, then reassign
7. **New items go in CATALOG dict** — add entries to `world/areas/equipment_catalog.py` as zones introduce new equipment
8. **Consumables must use `use_effect` dict** — never use flat `heal_amount`/`stamina_amount`/`cure_effect` attrs. Consumable dispatch lives in `world/item_effects.py` (`consume_item()`), called from `CmdUseAbility._consume_item()`

## References
- **Item Spawner:** `world/item_spawner.py` — `create_item_from_template()` creates purchased items
- **World State:** `world/world_state.py` — `get_standing()` for faction price discounts
- **Inventory Engine:** `world/inventory_engine.py` — `can_be_sold()` on item typeclasses
- **Item Effects Engine:** `world/item_effects.py` — `consume_item()` dispatches consumable `use_effect` dicts (heal, stamina, cure, HoT)
- **Tests:** `tests/test_vendor_engine.py`

---
**Last Updated:** 2026-04-05
