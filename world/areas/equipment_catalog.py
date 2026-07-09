"""
Equipment Catalog — master item definitions for Soravelon M1.

Defines 77 equipment items across 3 material tiers (iron/steel/mithril)
covering all 13 equipment slots, plus basic consumable potions.

This is a utility zone spec — no rooms, just item definitions registered
via area.item() for use by vendors, loot tables, and crafting outputs.

Per CON-04: No procedural affixes. All items are static definitions.
Per D-41: No durability system.
Per D-36: Weight values are cosmetic (no encumbrance enforcement).
Per D-33: Soft stat requirements via scaling_stat (no hard checks).
Per D-42: Weapons have damage_min/damage_max + stat scaling.
Per D-39: Shields are passive off_hand armor.
Per D-38: Two-handed weapons use both hand slots.

``world.item_catalog.CATALOG`` is the single source of truth for all item
definitions. Tool templates there retain their ``tool_slot`` and ``tool_tag``
fields. This module only registers canonical copies through AreaBuilder.
"""

from world.area_builder import AreaBuilder
from world.item_catalog import CATALOG


# ==================================================================
# CATALOG compatibility re-export; canonical data lives in world.item_catalog
# ==================================================================
# Each entry: item_id -> {item_id, key, item_type, equip_slot, ...}
# Used here only to register canonical templates with AreaBuilder.

def build():
    area = AreaBuilder("equipment_catalog")
    area.zone(
        name="Equipment Catalog",
        zone_type="frontier",
        continent="varath",
    )

    for item_id, item_def in CATALOG.items():
        # Pass all fields except item_id as kwargs to area.item()
        kwargs = {k: v for k, v in item_def.items() if k != "item_id"}
        area.item(item_id, **kwargs)

    return area.build()
