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
