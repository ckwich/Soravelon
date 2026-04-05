"""
Vendor economy engine for Soravelon.

Handles buy/sell/appraise/list/view operations for NPC vendors.
Vendors use carried_scales (character.db.carried_scales), NOT bank balance.
All functions return (bool, str) tuples per project convention.
"""

import math
from world.areas.equipment_catalog import CATALOG
from world.item_spawner import create_item_from_template

SELL_RATIO = 0.33  # Players get 33% of item value when selling


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
    base_stock = {k: v for k, v in CATALOG.items() if v.get("item_type") in accepts}
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
    player_stock = vendor_npc.db.player_stock or {}
    if item_id in player_stock and item_id not in CATALOG:
        del player_stock[item_id]
        vendor_npc.db.player_stock = player_stock

    item = create_item_from_template(item_def, location=character)
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
    item_id = item.db.item_id or item_key.lower().replace(" ", "_")
    player_stock[item_id] = {
        "item_id": item_id,
        "key": item_key,
        "item_type": item_type,
        "value": value,
        "desc": item.db.desc or "",
        "rarity": item.db.rarity or "common",
        "equip_slot": item.db.equipment_slot,
        "stat_bonuses": item.db.stat_bonuses or {},
        "damage_min": item.db.damage_min or 0,
        "damage_max": item.db.damage_max or 0,
        "armor_value": item.db.armor_value or 0,
        "weight": item.db.weight or 0,
    }
    vendor_npc.db.player_stock = player_stock

    # Remove item from character
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
    lines.append(f"  Value: {item_def.get('value', 0)} Scales")
    return True, "\n".join(lines)
