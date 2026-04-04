"""
Material definitions registry for Soravelon.

Pure-data module -- no Django or Evennia imports. Consumed by gathering_engine,
cmd_gathering, cmd_fishing, and crafting_definitions.

Defines the MATERIAL_REGISTRY taxonomy, material tiers, gathering categories,
gathering delay constants, visibility thresholds, and tool durability specs.
"""

# --- Material Tiers (D-10: 5 expandable tiers) ---

MATERIAL_TIERS = {
    1: "Common",
    2: "Uncommon",
    3: "Rare",
    4: "Exceptional",
    5: "Legendary",
}

# --- Gathering Categories (D-12, D-13, D-19) ---
# Maps category string to the skill, required tool, and command verb.

GATHERING_CATEGORIES = {
    "ore": {"skill": "mining", "tool": "pickaxe", "command": "mine"},
    "herb": {"skill": "herbalism", "tool": "sickle", "command": "harvest"},
    "wood": {"skill": "woodcutting", "tool": "hatchet", "command": "chop"},
    "forage": {"skill": "foraging", "tool": None, "command": "forage"},
    "fish": {"skill": "fishing", "tool": "fishing_rod", "command": "fish"},
    "hide": {"skill": "skinning", "tool": "skinning_knife", "command": "butcher"},
}

# --- Gathering Delay by Tier (base seconds, D-14) ---
# Skill reduces delay but never below 40% of these values.

GATHER_DELAY_BY_TIER = {
    1: 4,
    2: 6,
    3: 8,
    4: 12,
    5: 16,
}

# --- Visibility Thresholds (D-21) ---
# Minimum gathering skill required to see nodes at each visibility level.

VISIBILITY_THRESHOLDS = {
    "low": 0,
    "mid": 30,
    "high": 60,
}

# --- Tool Durability (D-19, D-20) ---
# max_durability = uses before breaking, repair_cost = Scales per repair.

TOOL_DURABILITY = {
    "pickaxe": {"max_durability": 50, "repair_cost": 5},
    "sickle": {"max_durability": 40, "repair_cost": 4},
    "hatchet": {"max_durability": 50, "repair_cost": 5},
    "skinning_knife": {"max_durability": 30, "repair_cost": 3},
    "fishing_rod": {"max_durability": 60, "repair_cost": 6},
}

# --- Material Registry (D-09, D-24, D-25) ---
# Central source of truth for all materials. Keyed by material_id.
# Each entry defines display name, category, tier, raw/processed forms,
# gathering/processing skill and station, and visibility level.

MATERIAL_REGISTRY = {

    # ===== Ores (mining) =====

    "iron_ore": {
        "display_name": "Iron Ore",
        "category": "ore",
        "tier": 1,
        "raw_form": "iron_ore",
        "processed_form": "iron_ingot",
        "gathering_skill": "mining",
        "processing_skill": "smithing",
        "processing_station": "forge",
        "visibility": "low",
    },
    "steel_ore": {
        "display_name": "Steel Ore",
        "category": "ore",
        "tier": 2,
        "raw_form": "steel_ore",
        "processed_form": "steel_ingot",
        "gathering_skill": "mining",
        "processing_skill": "smithing",
        "processing_station": "forge",
        "visibility": "mid",
    },
    "mithril_ore": {
        "display_name": "Mithril Ore",
        "category": "ore",
        "tier": 3,
        "raw_form": "mithril_ore",
        "processed_form": "mithril_ingot",
        "gathering_skill": "mining",
        "processing_skill": "smithing",
        "processing_station": "forge",
        "visibility": "high",
    },

    # ===== Herbs (herbalism) =====

    "wild_herb": {
        "display_name": "Wild Herb",
        "category": "herb",
        "tier": 1,
        "raw_form": "wild_herb",
        "processed_form": "herb_extract",
        "gathering_skill": "herbalism",
        "processing_skill": "alchemy",
        "processing_station": "alchemy_bench",
        "visibility": "low",
    },
    "thornroot": {
        "display_name": "Thornroot",
        "category": "herb",
        "tier": 2,
        "raw_form": "thornroot",
        "processed_form": "thornroot_extract",
        "gathering_skill": "herbalism",
        "processing_skill": "alchemy",
        "processing_station": "alchemy_bench",
        "visibility": "mid",
    },
    "moonpetal": {
        "display_name": "Moonpetal",
        "category": "herb",
        "tier": 3,
        "raw_form": "moonpetal",
        "processed_form": "moonpetal_essence",
        "gathering_skill": "herbalism",
        "processing_skill": "alchemy",
        "processing_station": "alchemy_bench",
        "visibility": "high",
    },

    # ===== Wood (woodcutting) =====

    "pine_log": {
        "display_name": "Pine Log",
        "category": "wood",
        "tier": 1,
        "raw_form": "pine_log",
        "processed_form": "pine_plank",
        "gathering_skill": "woodcutting",
        "processing_skill": "engineering",
        "processing_station": "workbench",
        "visibility": "low",
    },
    "oak_log": {
        "display_name": "Oak Log",
        "category": "wood",
        "tier": 2,
        "raw_form": "oak_log",
        "processed_form": "oak_plank",
        "gathering_skill": "woodcutting",
        "processing_skill": "engineering",
        "processing_station": "workbench",
        "visibility": "mid",
    },
    "ironwood_log": {
        "display_name": "Ironwood Log",
        "category": "wood",
        "tier": 3,
        "raw_form": "ironwood_log",
        "processed_form": "ironwood_plank",
        "gathering_skill": "woodcutting",
        "processing_skill": "engineering",
        "processing_station": "workbench",
        "visibility": "high",
    },

    # ===== Forage (foraging) =====

    "wild_mushroom": {
        "display_name": "Wild Mushroom",
        "category": "forage",
        "tier": 1,
        "raw_form": "wild_mushroom",
        "processed_form": "dried_mushroom",
        "gathering_skill": "foraging",
        "processing_skill": "cooking",
        "processing_station": "campfire",
        "visibility": "low",
    },
    "cave_moss": {
        "display_name": "Cave Moss",
        "category": "forage",
        "tier": 2,
        "raw_form": "cave_moss",
        "processed_form": "moss_paste",
        "gathering_skill": "foraging",
        "processing_skill": "alchemy",
        "processing_station": "alchemy_bench",
        "visibility": "mid",
    },
    "starbloom": {
        "display_name": "Starbloom",
        "category": "forage",
        "tier": 3,
        "raw_form": "starbloom",
        "processed_form": "starbloom_powder",
        "gathering_skill": "foraging",
        "processing_skill": "alchemy",
        "processing_station": "alchemy_bench",
        "visibility": "high",
    },

    # ===== Fish (fishing) =====

    "river_trout": {
        "display_name": "River Trout",
        "category": "fish",
        "tier": 1,
        "raw_form": "river_trout",
        "processed_form": "raw_fish",
        "gathering_skill": "fishing",
        "processing_skill": "cooking",
        "processing_station": "campfire",
        "visibility": "low",
    },
    "cave_eel": {
        "display_name": "Cave Eel",
        "category": "fish",
        "tier": 2,
        "raw_form": "cave_eel",
        "processed_form": "eel_fillet",
        "gathering_skill": "fishing",
        "processing_skill": "cooking",
        "processing_station": "campfire",
        "visibility": "mid",
    },
    "shadow_bass": {
        "display_name": "Shadow Bass",
        "category": "fish",
        "tier": 3,
        "raw_form": "shadow_bass",
        "processed_form": "shadow_bass_fillet",
        "gathering_skill": "fishing",
        "processing_skill": "cooking",
        "processing_station": "campfire",
        "visibility": "high",
    },

    # ===== Hides (skinning) =====

    "boar_hide": {
        "display_name": "Boar Hide",
        "category": "hide",
        "tier": 1,
        "raw_form": "boar_hide",
        "processed_form": "leather_strip",
        "gathering_skill": "skinning",
        "processing_skill": "smithing",
        "processing_station": "workbench",
        "visibility": "low",
    },
    "ash_wolf_pelt": {
        "display_name": "Ash Wolf Pelt",
        "category": "hide",
        "tier": 2,
        "raw_form": "ash_wolf_pelt",
        "processed_form": "cured_pelt",
        "gathering_skill": "skinning",
        "processing_skill": "smithing",
        "processing_station": "workbench",
        "visibility": "mid",
    },
    "drake_scale": {
        "display_name": "Drake Scale",
        "category": "hide",
        "tier": 3,
        "raw_form": "drake_scale",
        "processed_form": "treated_scale",
        "gathering_skill": "skinning",
        "processing_skill": "smithing",
        "processing_station": "workbench",
        "visibility": "high",
    },
}
