"""
Crafting definitions registry for Soravelon.

Pure-data module defining all recipe data, quality tiers, station requirements,
and skill-to-command mappings for the crafting system. No Django imports.

Recipes are static data — CharacterRecipe model tracks which recipes each
character has discovered. Recipes with default_known=True are auto-learned.
"""

# --- Quality Tiers (lowest to highest) ---

QUALITY_TIERS = ["flawed", "standard", "fine", "superior", "masterwork"]

# --- Quality Display Names (with color codes) ---

QUALITY_DISPLAY = {
    "flawed": "|x[Flawed]|n",
    "standard": "|w[Standard]|n",
    "fine": "|g[Fine]|n",
    "superior": "|c[Superior]|n",
    "masterwork": "|y[Masterwork]|n",
}

# --- Quality Multipliers ---
# Applied to effect amounts (heal, regen, buff, damage, armor, etc.)

QUALITY_MULTIPLIERS = {
    "flawed": 0.6,
    "standard": 1.0,
    "fine": 1.3,
    "superior": 1.6,
    "masterwork": 2.0,
}

# --- Station Requirements ---
# Maps station type key to a human-readable description for error messages.

STATION_REQUIREMENTS = {
    "campfire": "a campfire or cooking hearth",
    "forge": "a smithing forge",
    "alchemy_bench": "an alchemist's workbench",
    "workbench": "an engineering workbench",
}

# --- Skill-to-Command Mapping ---
# Maps the general proficiency skill_id to the crafting command verb.
# Per D-18: engineering skill is SEPARATE from engineering domain.

SKILL_TO_COMMAND = {
    "cooking": "cook",
    "smithing": "smith",
    "alchemy": "brew",
    "engineering": "craft",
}

COMMAND_TO_SKILL = {v: k for k, v in SKILL_TO_COMMAND.items()}

# --- Recipe Registry ---
# Keyed by recipe_id. Each entry defines ingredients, skill requirement,
# station, output, and whether it's known by default.

RECIPE_REGISTRY = {
    # ===== Cooking (campfire, cooking skill) =====
    "trail_rations": {
        "name": "Trail Rations",
        "skill": "cooking",
        "difficulty": 10,
        "station": "campfire",
        "ingredients": [
            {"item_tag": "raw_meat", "quantity": 1},
            {"item_tag": "wild_herb", "quantity": 1},
        ],
        "output": {
            "template_id": "trail_rations",
            "base_item_type": "consumable",
            "quality_affects": "effect_amount",
        },
        "default_known": True,
        "command": "cook",
        "craft_time": 3,
        "craft_echo": "You tend the fire, turning the food carefully...",
    },
    "hearty_stew": {
        "name": "Hearty Stew",
        "skill": "cooking",
        "difficulty": 25,
        "station": "campfire",
        "ingredients": [
            {"item_tag": "raw_meat", "quantity": 2},
            {"item_tag": "root_vegetable", "quantity": 1},
            {"item_tag": "clean_water", "quantity": 1},
        ],
        "output": {
            "template_id": "hearty_stew",
            "base_item_type": "consumable",
            "quality_affects": "effect_amount",
        },
        "default_known": True,
        "command": "cook",
        "craft_time": 5,
        "craft_echo": "You stir the pot, the aroma of stew filling the air...",
    },
    "spiced_fish": {
        "name": "Spiced Fish",
        "skill": "cooking",
        "difficulty": 40,
        "station": "campfire",
        "ingredients": [
            {"item_tag": "raw_fish", "quantity": 1},
            {"item_tag": "wild_herb", "quantity": 1},
            {"item_tag": "spice", "quantity": 1},
        ],
        "output": {
            "template_id": "spiced_fish",
            "base_item_type": "consumable",
            "quality_affects": "effect_amount",
        },
        "default_known": False,
        "command": "cook",
        "craft_time": 4,
        "craft_echo": "You season the fish and place it over the flames...",
    },
    # ===== Smithing (forge, smithing skill) =====
    "iron_dagger": {
        "name": "Iron Dagger",
        "skill": "smithing",
        "difficulty": 20,
        "station": "forge",
        "ingredients": [
            {"item_tag": "iron_ingot", "quantity": 2},
        ],
        "output": {
            "template_id": "iron_dagger",
            "base_item_type": "weapon",
            "quality_affects": "damage",
        },
        "default_known": True,
        "command": "smith",
        "craft_time": 6,
        "craft_echo": "You heat the iron and hammer it into shape...",
    },
    "iron_chainmail": {
        "name": "Iron Chainmail",
        "skill": "smithing",
        "difficulty": 40,
        "station": "forge",
        "ingredients": [
            {"item_tag": "iron_ingot", "quantity": 4},
            {"item_tag": "leather_strip", "quantity": 2},
        ],
        "output": {
            "template_id": "iron_chainmail",
            "base_item_type": "armor",
            "quality_affects": "armor_value",
        },
        "default_known": False,
        "command": "smith",
        "craft_time": 8,
        "craft_echo": "You link iron rings together, testing each joint...",
    },
    # ===== Alchemy (alchemy_bench, alchemy skill) =====
    "basic_healing_draught": {
        "name": "Basic Healing Draught",
        "skill": "alchemy",
        "difficulty": 20,
        "station": "alchemy_bench",
        "ingredients": [
            {"item_tag": "thornroot", "quantity": 2},
            {"item_tag": "clean_water", "quantity": 1},
        ],
        "output": {
            "template_id": "basic_healing_draught",
            "base_item_type": "consumable",
            "quality_affects": "effect_amount",
        },
        "default_known": True,
        "command": "brew",
        "craft_time": 4,
        "craft_echo": "You crush the thornroot and mix it into the water...",
    },
    "antidote": {
        "name": "Antidote",
        "skill": "alchemy",
        "difficulty": 30,
        "station": "alchemy_bench",
        "ingredients": [
            {"item_tag": "thornroot", "quantity": 1},
            {"item_tag": "nightpetal", "quantity": 1},
            {"item_tag": "clean_water", "quantity": 1},
        ],
        "output": {
            "template_id": "antidote",
            "base_item_type": "consumable",
            "quality_affects": "effect_amount",
        },
        "default_known": False,
        "command": "brew",
        "craft_time": 5,
        "craft_echo": "You carefully distill the nightpetal essence...",
    },
    "stamina_tonic": {
        "name": "Stamina Tonic",
        "skill": "alchemy",
        "difficulty": 35,
        "station": "alchemy_bench",
        "ingredients": [
            {"item_tag": "ironbark_sap", "quantity": 1},
            {"item_tag": "clean_water", "quantity": 1},
            {"item_tag": "spice", "quantity": 1},
        ],
        "output": {
            "template_id": "stamina_tonic",
            "base_item_type": "consumable",
            "quality_affects": "effect_amount",
        },
        "default_known": False,
        "command": "brew",
        "craft_time": 5,
        "craft_echo": "You mix the ironbark sap with spiced water, heating slowly...",
    },

    # ===== M1 Equipment Recipes — Smithing =====

    "iron_sword": {
        "name": "Iron Sword",
        "skill": "smithing",
        "difficulty": 25,
        "station": "forge",
        "ingredients": [
            {"item_tag": "iron_ingot", "quantity": 3},
        ],
        "output": {
            "template_id": "iron_sword",
            "base_item_type": "weapon",
            "quality_affects": "damage",
        },
        "default_known": True,
        "command": "smith",
        "craft_time": 7,
        "craft_echo": "You fold the iron, hammering the blade into a keen edge...",
    },
    "iron_mace": {
        "name": "Iron Mace",
        "skill": "smithing",
        "difficulty": 25,
        "station": "forge",
        "ingredients": [
            {"item_tag": "iron_ingot", "quantity": 3},
        ],
        "output": {
            "template_id": "iron_mace",
            "base_item_type": "weapon",
            "quality_affects": "damage",
        },
        "default_known": True,
        "command": "smith",
        "craft_time": 7,
        "craft_echo": "You shape the flanged head and fit it to the haft...",
    },
    "steel_sword": {
        "name": "Steel Sword",
        "skill": "smithing",
        "difficulty": 45,
        "station": "forge",
        "ingredients": [
            {"item_tag": "steel_ingot", "quantity": 3},
        ],
        "output": {
            "template_id": "steel_sword",
            "base_item_type": "weapon",
            "quality_affects": "damage",
        },
        "default_known": False,
        "command": "smith",
        "craft_time": 8,
        "craft_echo": "You work the steel carefully, folding and quenching for a superior edge...",
    },
    "iron_buckler": {
        "name": "Iron Buckler",
        "skill": "smithing",
        "difficulty": 30,
        "station": "forge",
        "ingredients": [
            {"item_tag": "iron_ingot", "quantity": 4},
        ],
        "output": {
            "template_id": "iron_buckler",
            "base_item_type": "armor",
            "quality_affects": "armor_value",
        },
        "default_known": True,
        "command": "smith",
        "craft_time": 6,
        "craft_echo": "You hammer the iron into a round disc, raising the boss...",
    },
    "iron_helm": {
        "name": "Iron Helm",
        "skill": "smithing",
        "difficulty": 30,
        "station": "forge",
        "ingredients": [
            {"item_tag": "iron_ingot", "quantity": 2},
        ],
        "output": {
            "template_id": "iron_helm",
            "base_item_type": "armor",
            "quality_affects": "armor_value",
        },
        "default_known": True,
        "command": "smith",
        "craft_time": 6,
        "craft_echo": "You raise the dome of the helm, shaping the nose guard...",
    },
    "iron_breastplate": {
        "name": "Iron Breastplate",
        "skill": "smithing",
        "difficulty": 50,
        "station": "forge",
        "ingredients": [
            {"item_tag": "iron_ingot", "quantity": 5},
            {"item_tag": "leather_strip", "quantity": 2},
        ],
        "output": {
            "template_id": "iron_breastplate",
            "base_item_type": "armor",
            "quality_affects": "armor_value",
        },
        "default_known": False,
        "command": "smith",
        "craft_time": 10,
        "craft_echo": "You shape the breastplate over the anvil, fitting straps and buckles...",
    },
    "steel_greatsword": {
        "name": "Steel Greatsword",
        "skill": "smithing",
        "difficulty": 55,
        "station": "forge",
        "ingredients": [
            {"item_tag": "steel_ingot", "quantity": 5},
            {"item_tag": "leather_strip", "quantity": 1},
        ],
        "output": {
            "template_id": "steel_greatsword",
            "base_item_type": "weapon",
            "quality_affects": "damage",
        },
        "default_known": False,
        "command": "smith",
        "craft_time": 10,
        "craft_echo": "You draw out the steel into a massive blade, wire-wrapping the grip...",
    },

    # ===== M1 Equipment Recipes — Alchemy =====

    "minor_healing_potion": {
        "name": "Minor Healing Potion",
        "skill": "alchemy",
        "difficulty": 15,
        "station": "alchemy_bench",
        "ingredients": [
            {"item_tag": "thornroot", "quantity": 1},
            {"item_tag": "clean_water", "quantity": 1},
        ],
        "output": {
            "template_id": "minor_healing_potion",
            "base_item_type": "consumable",
            "quality_affects": "effect_amount",
        },
        "default_known": True,
        "command": "brew",
        "craft_time": 3,
        "craft_echo": "You steep the thornroot in water, producing a ruddy liquid...",
    },
    "minor_stamina_potion": {
        "name": "Minor Stamina Potion",
        "skill": "alchemy",
        "difficulty": 20,
        "station": "alchemy_bench",
        "ingredients": [
            {"item_tag": "ironbark_sap", "quantity": 1},
            {"item_tag": "clean_water", "quantity": 1},
        ],
        "output": {
            "template_id": "minor_stamina_potion",
            "base_item_type": "consumable",
            "quality_affects": "effect_amount",
        },
        "default_known": True,
        "command": "brew",
        "craft_time": 3,
        "craft_echo": "You dissolve the ironbark sap into a fizzing green tonic...",
    },

    # ===== M1 Equipment Recipes — Cooking =====

    "cooked_meat": {
        "name": "Cooked Meat",
        "skill": "cooking",
        "difficulty": 5,
        "station": "campfire",
        "ingredients": [
            {"item_tag": "raw_meat", "quantity": 1},
        ],
        "output": {
            "template_id": "cooked_meat",
            "base_item_type": "consumable",
            "quality_affects": "effect_amount",
        },
        "default_known": True,
        "command": "cook",
        "craft_time": 2,
        "craft_echo": "You turn the meat over the flames until it sizzles...",
    },
    "herb_poultice": {
        "name": "Herb Poultice",
        "skill": "cooking",
        "difficulty": 15,
        "station": "campfire",
        "ingredients": [
            {"item_tag": "wild_herb", "quantity": 2},
            {"item_tag": "clean_water", "quantity": 1},
        ],
        "output": {
            "template_id": "herb_poultice",
            "base_item_type": "consumable",
            "quality_affects": "effect_amount",
        },
        "default_known": True,
        "command": "cook",
        "craft_time": 3,
        "craft_echo": "You mash the herbs and bind them into a damp poultice...",
    },
}
