"""
Loot table structure — stub for future loot system.
The affix system defines rarity tiers. The loot system (built later)
will implement the actual drop tables.
"""

LOOT_TIER_MODIFIERS = {
    "normal":    {"extra_rolls": 0, "tome_chance": 0.00, "ancient_chance": 0.00},
    "magic":     {"extra_rolls": 1, "tome_chance": 0.00, "ancient_chance": 0.00},
    "rare":      {"extra_rolls": 1, "tome_chance": 0.05, "ancient_chance": 0.00},
    "legendary": {"extra_rolls": 2, "tome_chance": 0.15, "ancient_chance": 0.02},
}


def get_loot_modifiers(mob):
    """Return loot modifiers for a mob based on its rarity."""
    rarity = (mob.db.rarity or 'normal')
    return LOOT_TIER_MODIFIERS.get(rarity, LOOT_TIER_MODIFIERS["normal"])
