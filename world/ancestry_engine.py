"""
Ancestry engine for Soravelon.

Four playable ancestries at launch: Human, Kau'roran, Veth, Selvar.
Each ancestry provides innate traits, a starting ability, domain interaction
modifiers, and starting faction standings applied at character creation.

set_ancestry() is called once during character creation. It sets
character.db.ancestry, optionally character.db.selvar_coat, and applies
starting faction standings via modify_standing().

Ancestry traits are static data -- no DB models, pure Python constants.
"""

# ---------------------------------------------------------------------------
# Ancestry trait definitions
# ---------------------------------------------------------------------------

ANCESTRY_TRAITS = {
    "human": {
        "name": "Human",
        "attribute_bonus": 1,
        "reputation_generation": 1.15,
        "status_duration_reduction": 0.10,
        "starting_ability": "second_wind",
        "domain_modifiers": {
            "combat": {"reputation_from_kills_scale": 1.2},
            "naturalism": {"attunement_any_zone": True},
            "subterfuge": {"network_from_jobs_scale": 1.2},
        },
    },
    "kauroran": {
        "name": "Kau'roran",
        "hp_bonus": 1.30,
        "strength_scaling": 1.20,
        "trust_build_rate": 1.20,
        "starting_ability": "immovable",
        "domain_modifiers": {
            "combat": {"strength_scaling_extra": True},
            "naturalism": {"aoe_magnitude_bonus": True},
            "subterfuge": {"focus_on_hit": True},
        },
    },
    "veth": {
        "name": "Veth",
        "agility_scaling": 1.25,
        "speed_bonus": 1.15,
        "guard_aggro_threshold": 1.30,
        "warren_sense": True,
        "starting_ability": "vanish",
        "domain_modifiers": {
            "combat": {"momentum_from_misses": True},
            "naturalism": {"underground_attunement_double": True},
            "subterfuge": {"network_gains_double": True},
        },
    },
    "selvar": {
        "name": "Selvar",
        "reckless_momentum_bonus": 0.20,
        "starting_ability": "audacity",
        "coat_traits": {
            "summer": {"agility_bonus": 0.10, "focus_generation_bonus": 0.05},
            "winter": {"endurance_bonus": 0.10, "status_resist_bonus": 0.05},
        },
        "domain_modifiers": {
            "combat": {"momentum_no_decay": True},
            "naturalism": {"mana_regen_on_status": True},
            "subterfuge": {"focus_on_status": True},
        },
    },
}

# ---------------------------------------------------------------------------
# Starting faction standings applied at character creation
# ---------------------------------------------------------------------------

ANCESTRY_STARTING_STANDING = {
    "human": {"empire": 10000},
    "kauroran": {"kauroran": 20000, "wardens": 10000, "empire": -15000},
    "veth": {"consortium": 7500},
    "selvar": {},  # handled specially via SELVAR_ALL_FACTIONS_PENALTY
}

SELVAR_ALL_FACTIONS_PENALTY = -5000
SELVAR_GUILD_OFFSET = 2500

# Factions known to the world at character creation.
# Resistance excluded -- applied silently via hidden standing system later.
KNOWN_FACTIONS_AT_CREATION = ["empire", "wardens", "kauroran", "consortium"]

VALID_ANCESTRIES = tuple(ANCESTRY_TRAITS.keys())
VALID_COATS = ("summer", "winter")


# ---------------------------------------------------------------------------
# Starter kits -- items granted when ancestry is chosen
# ---------------------------------------------------------------------------

_HEALING_POTION = {
    "item_id": "healing_potion",
    "key": "Healing Potion",
    "item_type": "item",
    "weight": 0.3,
    "rarity": "normal",
    "value": 10,
    "desc": "A small vial of crimson liquid that restores health.",
    "heal_amount": 30,
}

_LOCKPICK = {
    "item_id": "lockpick",
    "key": "Lockpick",
    "item_type": "item",
    "weight": 0.1,
    "rarity": "normal",
    "value": 5,
    "desc": "A slender tool for working locks.",
}

_IRON_SWORD = {
    "item_id": "iron_sword",
    "key": "Iron Sword",
    "item_type": "equipment",
    "equip_slot": "main_hand",
    "weight": 3.0,
    "rarity": "normal",
    "value": 25,
    "desc": "A simple but sturdy iron blade.",
    "damage_min": 4,
    "damage_max": 8,
}

_IRON_SPEAR = {
    "item_id": "iron_spear",
    "key": "Iron Spear",
    "item_type": "equipment",
    "equip_slot": "main_hand",
    "weight": 4.0,
    "rarity": "normal",
    "value": 25,
    "desc": "A long iron-tipped spear favored by the Kau'roran.",
    "damage_min": 5,
    "damage_max": 9,
}

_IRON_DAGGER = {
    "item_id": "iron_dagger",
    "key": "Iron Dagger",
    "item_type": "equipment",
    "equip_slot": "main_hand",
    "weight": 1.0,
    "rarity": "normal",
    "value": 15,
    "desc": "A keen iron dagger, balanced for quick strikes.",
    "damage_min": 3,
    "damage_max": 6,
}

_IRON_STAFF = {
    "item_id": "iron_staff",
    "key": "Iron Staff",
    "item_type": "equipment",
    "equip_slot": "main_hand",
    "weight": 3.5,
    "rarity": "normal",
    "value": 25,
    "desc": "An iron-shod staff etched with faint warding runes.",
    "damage_min": 3,
    "damage_max": 7,
    "stat_bonuses": {"intellect": 1},
}

_LEATHER_ARMOR = {
    "item_id": "leather_armor",
    "key": "Leather Armor",
    "item_type": "equipment",
    "equip_slot": "chest",
    "weight": 5.0,
    "rarity": "normal",
    "value": 30,
    "desc": "Cured leather armor offering modest protection.",
    "armor": 3,
}

_HIDE_ARMOR = {
    "item_id": "hide_armor",
    "key": "Hide Armor",
    "item_type": "equipment",
    "equip_slot": "chest",
    "weight": 7.0,
    "rarity": "normal",
    "value": 35,
    "desc": "Thick hide plates stitched over heavy leather. Sturdy.",
    "armor": 4,
}

_CLOTH_ROBES = {
    "item_id": "cloth_robes",
    "key": "Cloth Robes",
    "item_type": "equipment",
    "equip_slot": "chest",
    "weight": 2.0,
    "rarity": "normal",
    "value": 20,
    "desc": "Simple robes of woven cloth, light and unencumbering.",
    "armor": 1,
    "stat_bonuses": {"intellect": 1},
}

STARTER_KITS = {
    "human": [_IRON_SWORD, _LEATHER_ARMOR, _HEALING_POTION, _HEALING_POTION],
    "kauroran": [_IRON_SPEAR, _HIDE_ARMOR, _HEALING_POTION, _HEALING_POTION],
    "veth": [
        _IRON_DAGGER, _IRON_DAGGER, _LEATHER_ARMOR,
        _HEALING_POTION, _HEALING_POTION, _LOCKPICK,
    ],
    "selvar": [_IRON_STAFF, _CLOTH_ROBES, _HEALING_POTION, _HEALING_POTION],
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def set_ancestry(character, ancestry_id, coat=None):
    """
    Set ancestry for a character during character creation.

    Returns (bool, str). Rejects if ancestry already chosen.
    For selvar, coat must be provided ("summer" or "winter").
    """
    if character.db.ancestry:
        return False, "Ancestry already chosen."

    if ancestry_id not in ANCESTRY_TRAITS:
        return False, f"Unknown ancestry: {ancestry_id}"

    if ancestry_id == "selvar":
        if coat not in VALID_COATS:
            return False, f"Selvar ancestry requires a coat choice: {VALID_COATS}"
        character.db.selvar_coat = coat

    character.db.ancestry = ancestry_id
    _apply_starting_standings(character, ancestry_id)
    _grant_starter_kit(character, ancestry_id)

    # Apply ancestry skill seeds (D-20)
    from world.skill_engine import apply_ancestry_skill_seeds
    apply_ancestry_skill_seeds(character, ancestry_id, coat=coat)

    from world.ability_engine import sync_character_ability_unlocks
    sync_character_ability_unlocks(character)

    display_name = ANCESTRY_TRAITS[ancestry_id]["name"]
    if ancestry_id == "selvar" and coat:
        return True, f"Ancestry set to {display_name} ({coat} coat)."
    return True, f"Ancestry set to {display_name}."


def get_ancestry_trait(character, trait_name, default=None):
    """
    Look up a specific trait value for the character's ancestry.

    Convenience function for other modules that need ancestry data
    without importing the full ANCESTRY_TRAITS dict.
    """
    ancestry_id = character.db.ancestry
    if not ancestry_id:
        return default
    traits = ANCESTRY_TRAITS.get(ancestry_id)
    if not traits:
        return default
    return traits.get(trait_name, default)


# ---------------------------------------------------------------------------
# Internal
# ---------------------------------------------------------------------------

def _grant_starter_kit(character, ancestry_id):
    """Create starter items for the chosen ancestry and place them in character inventory."""
    import logging
    logger = logging.getLogger("evennia")

    kit = STARTER_KITS.get(ancestry_id, [])
    if not kit:
        return

    try:
        from world.item_spawner import create_item_from_template
    except ImportError:
        logger.warning("ancestry_engine: item_spawner not available, skipping starter kit")
        return

    for item_def in kit:
        try:
            create_item_from_template(item_def, location=character)
        except Exception as err:
            logger.warning("ancestry_engine: failed to create starter item %s: %s",
                           item_def.get("item_id", "unknown"), err)

    # Grant starting currency
    character.db.carried_scales = 50


def _apply_starting_standings(character, ancestry_id):
    """Apply starting faction standings for the chosen ancestry."""
    from world.world_state import modify_standing

    # Standard standings from the table
    for faction_id, amount in ANCESTRY_STARTING_STANDING.get(ancestry_id, {}).items():
        modify_standing(character, faction_id, amount, "ancestry_starting")

    # Selvar special case: penalty to all known factions + guild offset
    if ancestry_id == "selvar":
        for faction_id in KNOWN_FACTIONS_AT_CREATION:
            modify_standing(character, faction_id, SELVAR_ALL_FACTIONS_PENALTY, "ancestry_starting")
        modify_standing(character, "guilds", SELVAR_GUILD_OFFSET, "ancestry_starting")
