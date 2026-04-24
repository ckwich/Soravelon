"""
Vendor economy engine for Soravelon.

Handles buy/sell/appraise/list/view operations for NPC vendors.
Vendors use carried_scales (character.db.carried_scales), NOT bank balance.
All functions return (bool, str) tuples per project convention.
"""

import copy
import math
from world.areas.equipment_catalog import CATALOG
from world.inventory_engine import unregister_item_ownership
from world.item_spawner import create_item_from_template

SELL_RATIO = 0.33  # Players get 33% of item value when selling
_PLAYER_STOCK_OPTIONAL_ATTRS = (
    "damage_min",
    "damage_max",
    "armor_value",
    "stat_bonuses",
    "use_effect",
    "tool_slot",
    "tool_tag",
    "scaling_stat",
    "two_handed",
    "stackable",
    "material_tier",
)


def _normalize_player_stock_quantity(entry):
    """Return a safe integer quantity for a player-stock entry."""
    quantity = entry.get("stock_quantity", 1)
    if not isinstance(quantity, int) or quantity < 1:
        return 1
    return quantity


def _is_mock_value(value):
    """Ignore MagicMock placeholders from unit-test items."""
    return type(value).__module__.startswith("unittest.mock")


def _safe_copy_db_value(value):
    """Copy item db values while ignoring empty or mock placeholders."""
    if value is None or _is_mock_value(value):
        return None
    if value in ({}, []):
        return None
    return copy.deepcopy(value)


def _build_player_stock_entry(item, item_id):
    """Serialize a sellable item into a vendor stock template."""
    entry = {
        "item_id": item_id,
        "key": item.key,
        "item_type": item.db.item_type or "item",
        "value": item.db.value_scales or 0,
        "desc": item.db.desc or "",
        "rarity": item.db.rarity or "common",
        "weight": item.db.weight or 0,
        "stock_quantity": 1,
    }

    equip_slot = _safe_copy_db_value(getattr(item.db, "equipment_slot", None))
    if equip_slot is not None:
        entry["equip_slot"] = equip_slot

    for attr_name in _PLAYER_STOCK_OPTIONAL_ATTRS:
        value = _safe_copy_db_value(getattr(item.db, attr_name, None))
        if value is not None:
            entry[attr_name] = value

    return entry


def _player_stock_signature(entry):
    """Build a stable signature used to stack identical player-sold items."""
    comparable = {}
    for key, value in entry.items():
        if key in {"item_id", "stock_quantity"}:
            continue
        comparable[key] = value
    return repr(sorted(comparable.items()))


def _next_player_stock_id(base_item_id, player_stock):
    """Choose a stock id that does not collide with authored catalog items."""
    candidate = base_item_id
    if candidate in CATALOG:
        candidate = f"used_{base_item_id}"
    suffix = 2
    while candidate in player_stock or candidate in CATALOG:
        candidate = f"used_{base_item_id}_{suffix}"
        suffix += 1
    return candidate


def _find_vendor_in_room(character):
    """Find a vendor NPC in character's current room. Returns mob or None."""
    if not character.location:
        return None
    for obj in character.location.contents:
        if obj.db.is_vendor:
            return obj
    return None


def get_vendor_stock(vendor_npc):
    """
    Return combined stock dict: CATALOG base filtered by vendor_accepts
    plus player-sold items.

    Args:
        vendor_npc: SoravelonMob with db.vendor_accepts list.

    Returns:
        dict: {item_id: item_def_dict, ...}
    """
    accepts = vendor_npc.db.vendor_accepts or []
    allowed_ids = set(vendor_npc.db.vendor_item_ids or [])
    excluded_ids = set(vendor_npc.db.vendor_exclude_item_ids or [])

    base_stock = {
        k: v
        for k, v in CATALOG.items()
        if v.get("item_type") in accepts
        and not v.get("is_quest_item")
        and (not allowed_ids or k in allowed_ids)
        and k not in excluded_ids
    }
    player_stock = vendor_npc.db.player_stock or {}
    return {**base_stock, **player_stock}


def get_vendor_price(vendor_npc, item_def, character):
    """
    Return buy price for an item. Base = item value.
    Faction-affiliated vendors adjust by standing (max 20% discount).

    Args:
        vendor_npc: Vendor mob.
        item_def: Item definition dict with 'value' key.
        character: Buying character.

    Returns:
        int: Final price in Scales.
    """
    base_price = item_def.get("value", 0)
    faction = vendor_npc.db.vendor_faction
    if faction:
        from world.world_state import get_standing
        standing = get_standing(character, faction)
        discount = min(0.20, standing * 0.002)  # max 20% discount at standing 100
        base_price = max(1, int(base_price * (1 - discount)))
    return base_price


def buy_item(character, vendor_npc, item_id):
    """
    Buy item from vendor. Deducts carried_scales and creates item.

    Args:
        character: Buying character.
        vendor_npc: Vendor mob.
        item_id: String ID of item to buy.

    Returns:
        (bool, str): Success flag and message.
    """
    stock = get_vendor_stock(vendor_npc)
    item_def = stock.get(item_id)
    if not item_def:
        return False, "That item is not available here."

    price = get_vendor_price(vendor_npc, item_def, character)
    carried = character.db.carried_scales or 0
    if carried < price:
        return False, f"You need {price} Scales but only have {carried}."

    character.db.carried_scales = carried - price

    # Remove from player_stock if it was player-sold (one copy)
    player_stock = dict(vendor_npc.db.player_stock or {})
    if item_id in player_stock and item_id not in CATALOG:
        quantity = _normalize_player_stock_quantity(player_stock[item_id])
        if quantity > 1:
            player_stock[item_id]["stock_quantity"] = quantity - 1
        else:
            del player_stock[item_id]
        vendor_npc.db.player_stock = player_stock

    spawned_item_def = copy.deepcopy(item_def)
    spawned_item_def.pop("stock_quantity", None)
    item = create_item_from_template(spawned_item_def, location=character)
    return True, f"You purchase {item.key} for {price} Scales."


def sell_item(character, vendor_npc, item):
    """
    Sell item to vendor. Character gains 33% of item value.
    Item is deleted and added to vendor's player_stock.

    Args:
        character: Selling character.
        vendor_npc: Vendor mob.
        item: SoravelonItem object to sell.

    Returns:
        (bool, str): Success flag and message.
    """
    accepts = vendor_npc.db.vendor_accepts or []
    item_type = item.db.item_type or "item"
    if item_type not in accepts:
        return False, f"This vendor doesn't deal in {item_type} items."

    ok, msg = item.can_be_sold(character)
    if not ok:
        return False, msg

    value = item.db.value_scales or 0
    sell_price = max(1, math.floor(value * SELL_RATIO))

    # Capture item name before deletion
    item_key = item.key

    # Transfer Scales to character
    character.db.carried_scales = (character.db.carried_scales or 0) + sell_price

    # Add to vendor player_stock at full price
    player_stock = dict(vendor_npc.db.player_stock or {})
    base_item_id = item.db.item_id or item_key.lower().replace(" ", "_")
    stock_item_id = _next_player_stock_id(base_item_id, player_stock)
    stock_entry = _build_player_stock_entry(item, stock_item_id)
    stock_signature = _player_stock_signature(stock_entry)

    for existing_id, existing_entry in player_stock.items():
        if _player_stock_signature(existing_entry) == stock_signature:
            player_stock[existing_id]["stock_quantity"] = (
                _normalize_player_stock_quantity(existing_entry) + 1
            )
            break
    else:
        player_stock[stock_item_id] = stock_entry
    vendor_npc.db.player_stock = player_stock

    # Remove item from character
    unregister_item_ownership(character, item)
    item.delete()

    return True, f"You sell {item_key} for {sell_price} Scales."


def appraise_item(character, vendor_npc, item):
    """
    Show what vendor would pay for an item.

    Args:
        character: Character requesting appraisal.
        vendor_npc: Vendor mob.
        item: SoravelonItem to appraise.

    Returns:
        (bool, str): Success flag and message.
    """
    accepts = vendor_npc.db.vendor_accepts or []
    item_type = item.db.item_type or "item"
    if item_type not in accepts:
        return False, f"This vendor doesn't deal in {item_type} items."
    ok, msg = item.can_be_sold(character)
    if not ok:
        return False, msg
    value = item.db.value_scales or 0
    sell_price = max(1, math.floor(value * SELL_RATIO))
    return True, f"The vendor would pay {sell_price} Scales for {item.key}."


def view_item(vendor_npc, item_id):
    """
    Show full item stats from vendor stock. No appraisal check needed
    -- vendors know their own stock.

    Args:
        vendor_npc: Vendor mob.
        item_id: String ID of item to view.

    Returns:
        (bool, str): Success flag and formatted stat display.
    """
    stock = get_vendor_stock(vendor_npc)
    item_def = stock.get(item_id)
    if not item_def:
        return False, "That item is not in the vendor's stock."
    lines = [f"|w{item_def.get('key', item_id)}|n"]
    if item_def.get("desc"):
        lines.append(item_def["desc"])
    if item_def.get("damage_min"):
        lines.append(f"  Damage: {item_def['damage_min']}-{item_def['damage_max']}")
    if item_def.get("armor_value"):
        lines.append(f"  Armor: {item_def['armor_value']}")
    if item_def.get("stat_bonuses"):
        bonuses = ", ".join(f"{k} +{v}" for k, v in item_def["stat_bonuses"].items())
        lines.append(f"  Bonuses: {bonuses}")
    if item_def.get("rarity") and item_def["rarity"] != "normal":
        lines.append(f"  Rarity: {item_def['rarity']}")
    quantity = _normalize_player_stock_quantity(item_def)
    if quantity > 1:
        lines.append(f"  Stock: {quantity}")
    lines.append(f"  Value: {item_def.get('value', 0)} Scales")
    return True, "\n".join(lines)
