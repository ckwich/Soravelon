"""
Vendor economy engine for Soravelon.

Handles buy/sell/appraise/list/view operations for NPC vendors.
Vendors use carried_scales (character.db.carried_scales), NOT bank balance.
All functions return (bool, str) tuples per project convention.
"""

import copy
import math

from world.atomic_state import atomic_evennia_state
from world.game_operations import (
    get_operation_replay,
    normalize_operation_id,
    record_operation,
)
from world.item_catalog import CATALOG
from world.inventory_engine import destroy_owned_item
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
    "weapon_family",
)


def _normalize_player_stock_quantity(entry):
    """Return a safe integer quantity for a player-stock entry."""
    quantity = entry.get("stock_quantity", 1)
    if not isinstance(quantity, int) or quantity < 1:
        return 1
    return quantity


def _safe_copy_db_value(value):
    """Copy a non-empty durable item attribute into vendor stock."""
    if value is None:
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


def _after_write(checkpoint):
    """Failure-injection seam for composite rollback tests."""


def _lock_object_rows(*objects):
    from evennia.objects.models import ObjectDB

    ids = sorted({obj.id for obj in objects})
    locked = ObjectDB.objects.select_for_update().in_bulk(ids)
    if len(locked) != len(ids):
        raise RuntimeError("A vendor transaction actor no longer exists.")
    return locked


def buy_item(character, vendor_npc, item_id, *, operation_id=None):
    """
    Buy item from vendor. Deducts carried_scales and creates item.

    Args:
        character: Buying character.
        vendor_npc: Vendor mob.
        item_id: String ID of item to buy.

    Returns:
        (bool, str): Success flag and message.
    """
    operation_id = normalize_operation_id(operation_id)
    related_id = f"vendor:{vendor_npc.id}:buy:{item_id}"

    with atomic_evennia_state(character, vendor_npc) as tracker:
        locked = _lock_object_rows(character, vendor_npc)
        locked_character = locked[character.id]
        locked_vendor = locked[vendor_npc.id]
        tracker.track(locked_character, attributes=("carried_scales",))
        tracker.track(locked_vendor, attributes=("player_stock",))

        replay = get_operation_replay(
            character=locked_character,
            operation_id=operation_id,
            operation_type="vendor_buy",
            related_id=related_id,
        )
        if replay:
            return True, replay.result["message"]

        stock = get_vendor_stock(locked_vendor)
        item_def = stock.get(item_id)
        if not item_def:
            return False, "That item is not available here."

        price = get_vendor_price(locked_vendor, item_def, locked_character)
        carried = locked_character.db.carried_scales or 0
        if carried < price:
            return False, f"You need {price} Scales but only have {carried}."

        locked_character.db.carried_scales = carried - price
        _after_write("scales_debited")

        player_stock = copy.deepcopy(locked_vendor.db.player_stock or {})
        if item_id in player_stock and item_id not in CATALOG:
            quantity = _normalize_player_stock_quantity(player_stock[item_id])
            if quantity > 1:
                player_stock[item_id]["stock_quantity"] = quantity - 1
            else:
                del player_stock[item_id]
            locked_vendor.db.player_stock = player_stock
            _after_write("vendor_stock_decremented")

        spawned_item_def = copy.deepcopy(item_def)
        spawned_item_def.pop("stock_quantity", None)
        item = create_item_from_template(
            spawned_item_def,
            location=locked_character,
        )
        tracker.track(item)
        _after_write("purchase_item_spawned")
        message = f"You purchase {item.key} for {price} Scales."
        record_operation(
            character=locked_character,
            operation_id=operation_id,
            operation_type="vendor_buy",
            related_id=related_id,
            result={
                "message": message,
                "price": price,
                "item_object_id": item.id,
            },
        )
        _after_write("operation_recorded")
        return True, message


def sell_item(character, vendor_npc, item, *, operation_id=None):
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
    operation_id = normalize_operation_id(operation_id)
    item_object_id = getattr(item, "id", None)
    related_id = f"vendor:{vendor_npc.id}:sell:{item_object_id}"

    with atomic_evennia_state(character, vendor_npc) as tracker:
        locked = _lock_object_rows(character, vendor_npc)
        locked_character = locked[character.id]
        locked_vendor = locked[vendor_npc.id]
        tracker.track(locked_character, attributes=("carried_scales",))
        tracker.track(locked_vendor, attributes=("player_stock",))

        replay = get_operation_replay(
            character=locked_character,
            operation_id=operation_id,
            operation_type="vendor_sell",
            related_id=related_id,
        )
        if replay:
            return True, replay.result["message"]

        from evennia.objects.models import ObjectDB

        locked_item = ObjectDB.objects.select_for_update().filter(
            pk=item_object_id,
        ).first()
        if not locked_item or locked_item.db_location_id != locked_character.id:
            return False, "You don't have that."
        tracker.track(locked_item)

        accepts = locked_vendor.db.vendor_accepts or []
        item_type = locked_item.db.item_type or "item"
        if item_type not in accepts:
            return False, f"This vendor doesn't deal in {item_type} items."
        allowed, message = locked_item.can_be_sold(locked_character)
        if not allowed:
            return False, message

        value = locked_item.db.value_scales or 0
        sell_price = max(1, math.floor(value * SELL_RATIO))
        item_key = locked_item.key

        locked_character.db.carried_scales = (
            locked_character.db.carried_scales or 0
        ) + sell_price
        _after_write("scales_credited")

        player_stock = copy.deepcopy(locked_vendor.db.player_stock or {})
        base_item_id = (
            locked_item.tags.get(category="item_tag")
            or item_key.lower().replace(" ", "_")
        )
        stock_item_id = _next_player_stock_id(base_item_id, player_stock)
        stock_entry = _build_player_stock_entry(locked_item, stock_item_id)
        stock_signature = _player_stock_signature(stock_entry)

        for existing_id, existing_entry in player_stock.items():
            if _player_stock_signature(existing_entry) == stock_signature:
                player_stock[existing_id]["stock_quantity"] = (
                    _normalize_player_stock_quantity(existing_entry) + 1
                )
                break
        else:
            player_stock[stock_item_id] = stock_entry
        locked_vendor.db.player_stock = player_stock
        _after_write("vendor_stock_credited")

        destroyed, destroy_message = destroy_owned_item(
            locked_character,
            locked_item,
        )
        if not destroyed:
            raise RuntimeError(destroy_message)
        _after_write("sale_item_destroyed")

        result_message = f"You sell {item_key} for {sell_price} Scales."
        record_operation(
            character=locked_character,
            operation_id=operation_id,
            operation_type="vendor_sell",
            related_id=related_id,
            result={"message": result_message, "price": sell_price},
        )
        _after_write("operation_recorded")
        return True, result_message


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
