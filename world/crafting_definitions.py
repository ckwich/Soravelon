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
            "template_id": "antidote_potion",
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

    # ---------------------------------------------------------------
    # Processing Recipes (Phase 13 — raw material -> crafting ingredient)
    # recipe_type: "processing" distinguishes from crafting recipes.
    # conversion_ratio: dynamic ingredient quantity based on skill level (D-08).
    # Output uses item_id/key/item_type dict for create_item_from_template.
    # ---------------------------------------------------------------

    # ===== Ore Processing (smithing, forge) =====

    "iron_ingot": {
        "name": "Iron Ingot",
        "skill": "smithing",
        "difficulty": 10,
        "station": "forge",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "iron_ore", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "iron_ingot",
            "key": "Iron Ingot",
            "item_type": "item",
            "weight": 1.0,
            "desc": "A bar of refined iron, ready for smithing.",
            "value": 15,
        },
        "default_known": True,
        "command": "smith",
        "craft_time": 4,
        "craft_echo": "You heat the ore in the forge and hammer out impurities...",
    },
    "steel_ingot": {
        "name": "Steel Ingot",
        "skill": "smithing",
        "difficulty": 30,
        "station": "forge",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "steel_ore", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "steel_ingot",
            "key": "Steel Ingot",
            "item_type": "item",
            "weight": 1.0,
            "desc": "A bar of tempered steel, strong and versatile.",
            "value": 35,
        },
        "default_known": True,
        "command": "smith",
        "craft_time": 6,
        "craft_echo": "You fold and temper the steel ore into a gleaming ingot...",
    },
    "mithril_ingot": {
        "name": "Mithril Ingot",
        "skill": "smithing",
        "difficulty": 55,
        "station": "forge",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "mithril_ore", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "mithril_ingot",
            "key": "Mithril Ingot",
            "item_type": "item",
            "weight": 0.5,
            "desc": "A luminous bar of mithril, light as air and strong as steel.",
            "value": 80,
        },
        "default_known": True,
        "command": "smith",
        "craft_time": 8,
        "craft_echo": "The mithril ore shimmers as you work it into a lightweight ingot...",
    },

    # ===== Herb Processing (alchemy, alchemy_bench) =====

    "herb_extract": {
        "name": "Herb Extract",
        "skill": "alchemy",
        "difficulty": 10,
        "station": "alchemy_bench",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "wild_herb", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "herb_extract",
            "key": "Herb Extract",
            "item_type": "item",
            "weight": 0.2,
            "desc": "A concentrated herbal extract, useful in alchemy.",
            "value": 10,
        },
        "default_known": True,
        "command": "brew",
        "craft_time": 3,
        "craft_echo": "You crush and distill the herbs into a concentrated extract...",
    },
    "thornroot_extract": {
        "name": "Thornroot Extract",
        "skill": "alchemy",
        "difficulty": 30,
        "station": "alchemy_bench",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "thornroot", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "thornroot_extract",
            "key": "Thornroot Extract",
            "item_type": "item",
            "weight": 0.2,
            "desc": "A potent thornroot concentrate with healing properties.",
            "value": 25,
        },
        "default_known": True,
        "command": "brew",
        "craft_time": 5,
        "craft_echo": "Careful work extracts the potent essence from the thorny roots...",
    },
    "moonpetal_essence": {
        "name": "Moonpetal Essence",
        "skill": "alchemy",
        "difficulty": 55,
        "station": "alchemy_bench",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "moonpetal", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "moonpetal_essence",
            "key": "Moonpetal Essence",
            "item_type": "item",
            "weight": 0.1,
            "desc": "A shimmering essence distilled from rare moonpetals.",
            "value": 75,
        },
        "default_known": True,
        "command": "brew",
        "craft_time": 7,
        "craft_echo": "The moonpetals dissolve into a luminous, silvery essence...",
    },

    # ===== Wood Processing (engineering, workbench) =====

    "pine_plank": {
        "name": "Pine Plank",
        "skill": "engineering",
        "difficulty": 10,
        "station": "workbench",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "pine_log", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "pine_plank",
            "key": "Pine Plank",
            "item_type": "item",
            "weight": 1.5,
            "desc": "A smooth plank of pine, suitable for construction.",
            "value": 8,
        },
        "default_known": True,
        "command": "craft",
        "craft_time": 4,
        "craft_echo": "You saw and plane the pine logs into smooth planks...",
    },
    "oak_plank": {
        "name": "Oak Plank",
        "skill": "engineering",
        "difficulty": 30,
        "station": "workbench",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "oak_log", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "oak_plank",
            "key": "Oak Plank",
            "item_type": "item",
            "weight": 2.0,
            "desc": "A dense plank of oak, strong and durable.",
            "value": 20,
        },
        "default_known": True,
        "command": "craft",
        "craft_time": 5,
        "craft_echo": "You carefully work the dense oak into even planks...",
    },
    "ironwood_plank": {
        "name": "Ironwood Plank",
        "skill": "engineering",
        "difficulty": 55,
        "station": "workbench",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "ironwood_log", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "ironwood_plank",
            "key": "Ironwood Plank",
            "item_type": "item",
            "weight": 2.5,
            "desc": "An incredibly hard plank of ironwood, nearly unbreakable.",
            "value": 70,
        },
        "default_known": True,
        "command": "craft",
        "craft_time": 7,
        "craft_echo": "The ironwood resists every cut, but you shape it into a solid plank...",
    },

    # ===== Forage Processing (cooking/alchemy) =====

    "dried_mushroom": {
        "name": "Dried Mushroom",
        "skill": "cooking",
        "difficulty": 10,
        "station": "campfire",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "wild_mushroom", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "dried_mushroom",
            "key": "Dried Mushroom",
            "item_type": "item",
            "weight": 0.1,
            "desc": "Sun-dried mushrooms, a nutritious cooking ingredient.",
            "value": 5,
        },
        "default_known": True,
        "command": "cook",
        "craft_time": 3,
        "craft_echo": "You dry the mushrooms slowly over the fire...",
    },
    "moss_paste": {
        "name": "Moss Paste",
        "skill": "alchemy",
        "difficulty": 25,
        "station": "alchemy_bench",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "cave_moss", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "moss_paste",
            "key": "Moss Paste",
            "item_type": "item",
            "weight": 0.2,
            "desc": "A thick paste ground from cave moss, useful in poultices.",
            "value": 15,
        },
        "default_known": True,
        "command": "brew",
        "craft_time": 4,
        "craft_echo": "You grind the cave moss into a thick, pungent paste...",
    },
    "starbloom_powder": {
        "name": "Starbloom Powder",
        "skill": "alchemy",
        "difficulty": 55,
        "station": "alchemy_bench",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "starbloom", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "starbloom_powder",
            "key": "Starbloom Powder",
            "item_type": "item",
            "weight": 0.1,
            "desc": "A faintly glowing powder with potent alchemical properties.",
            "value": 70,
        },
        "default_known": True,
        "command": "brew",
        "craft_time": 6,
        "craft_echo": "You carefully grind the starbloom into a luminous powder...",
    },

    # ===== Fish Processing (cooking, campfire) =====

    "raw_fish": {
        "name": "Raw Fish Fillet",
        "skill": "cooking",
        "difficulty": 5,
        "station": "campfire",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "river_trout", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "raw_fish",
            "key": "Raw Fish Fillet",
            "item_type": "item",
            "weight": 0.3,
            "desc": "A cleaned and filleted fish, ready for cooking.",
            "value": 5,
        },
        "default_known": True,
        "command": "cook",
        "craft_time": 2,
        "craft_echo": "You gut and fillet the trout with practiced hands...",
    },
    "eel_fillet": {
        "name": "Eel Fillet",
        "skill": "cooking",
        "difficulty": 20,
        "station": "campfire",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "cave_eel", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "eel_fillet",
            "key": "Eel Fillet",
            "item_type": "item",
            "weight": 0.3,
            "desc": "A slippery eel fillet, prized for its rich flavor.",
            "value": 15,
        },
        "default_known": True,
        "command": "cook",
        "craft_time": 3,
        "craft_echo": "You carefully slice and debone the cave eel...",
    },
    "shadow_bass_fillet": {
        "name": "Shadow Bass Fillet",
        "skill": "cooking",
        "difficulty": 40,
        "station": "campfire",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "shadow_bass", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "shadow_bass_fillet",
            "key": "Shadow Bass Fillet",
            "item_type": "item",
            "weight": 0.4,
            "desc": "A dark, oily fillet from the elusive shadow bass.",
            "value": 40,
        },
        "default_known": True,
        "command": "cook",
        "craft_time": 4,
        "craft_echo": "The shadow bass yields a dark, richly flavored fillet...",
    },

    # ===== Hide Processing (smithing, workbench) =====

    "leather_strip": {
        "name": "Leather Strip",
        "skill": "smithing",
        "difficulty": 15,
        "station": "workbench",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "boar_hide", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "leather_strip",
            "key": "Leather Strip",
            "item_type": "item",
            "weight": 0.3,
            "desc": "A supple strip of tanned leather.",
            "value": 12,
        },
        "default_known": True,
        "command": "smith",
        "craft_time": 4,
        "craft_echo": "You scrape and tan the hide into supple leather strips...",
    },
    "cured_pelt": {
        "name": "Cured Pelt",
        "skill": "smithing",
        "difficulty": 35,
        "station": "workbench",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "ash_wolf_pelt", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "cured_pelt",
            "key": "Cured Pelt",
            "item_type": "item",
            "weight": 0.5,
            "desc": "A properly cured wolf pelt, soft yet durable.",
            "value": 30,
        },
        "default_known": True,
        "command": "smith",
        "craft_time": 6,
        "craft_echo": "You salt and stretch the wolf pelt until it cures properly...",
    },
    "treated_scale": {
        "name": "Treated Scale",
        "skill": "smithing",
        "difficulty": 55,
        "station": "workbench",
        "recipe_type": "processing",
        "ingredients": [{"item_tag": "drake_scale", "quantity": 3}],
        "conversion_ratio": {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]},
        "output": {
            "item_id": "treated_scale",
            "key": "Treated Scale",
            "item_type": "item",
            "weight": 0.4,
            "desc": "A drake scale treated with oils and heat, hard as iron.",
            "value": 75,
        },
        "default_known": True,
        "command": "smith",
        "craft_time": 8,
        "craft_echo": "You treat the drake scale with oils and careful heat until it gleams...",
    },

    # ===== Quest-Reward Alchemy Recipes =====

    "healing_draught": {
        "name": "Healing Draught",
        "skill": "alchemy",
        "difficulty": 25,
        "station": "alchemy_bench",
        "ingredients": [
            {"item_tag": "wild_herb", "quantity": 2},
            {"item_tag": "thornroot", "quantity": 1},
            {"item_tag": "clean_water", "quantity": 1},
        ],
        "output": {
            "template_id": "healing_draught",
            "base_item_type": "consumable",
            "quality_affects": "effect_amount",
        },
        "default_known": False,
        "command": "brew",
        "craft_time": 5,
        "craft_echo": "You blend the herbs into a poultice, then steep them in warmed water...",
    },
    "mountain_tonic": {
        "name": "Mountain Tonic",
        "skill": "alchemy",
        "difficulty": 40,
        "station": "alchemy_bench",
        "ingredients": [
            {"item_tag": "mountain_herb", "quantity": 2},
            {"item_tag": "clean_water", "quantity": 1},
            {"item_tag": "wild_mushroom", "quantity": 1},
        ],
        "output": {
            "template_id": "mountain_tonic",
            "base_item_type": "consumable",
            "quality_affects": "effect_amount",
        },
        "default_known": False,
        "command": "brew",
        "craft_time": 6,
        "craft_echo": "You follow the old formula, grinding the mountain herbs with mortar and stone...",
    },
}
