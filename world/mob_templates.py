"""
Mob template registry for Soravelon.

Defines MOB_TEMPLATES dict mapping template_key -> stat/behavior dicts.
Zone content plans expand these templates; this module provides the
starter set and the apply function.

Public API:
    get_mob_template(template_key) -> dict or None
    apply_mob_template(mob, template_key) -> None
"""

import logging

logger = logging.getLogger("world.mob_templates")


# ---------------------------------------------------------------------------
# Template registry
# ---------------------------------------------------------------------------
# Each template defines the full stat block for a mob type.
# Zone content plans (07-03 through 07-10) will add entries here.
#
# Field reference:
#   key             - Display name for the mob
#   mob_type        - Lookup key for loot tables and combat AI
#   desc            - Description shown on look
#   base_aggression - passive / cautious / aggressive / hostile
#   hp_min, hp_max  - HP range (zone scaling applied on top)
#   damage_min, damage_max - Base damage range
#   speed           - Attack speed multiplier (1.0 = normal)
#   abilities       - List of ability dicts for combat AI
#   faction         - Faction affiliation string or None
#   is_hunter       - If True, mob uses BFS chase behavior
#   detection_range - Rooms away mob can detect players (for hunters)
#   flee_threshold  - HP percentage at which mob attempts to flee
#   wander          - If True, mob moves randomly between rooms
#   loot_table      - Key into LOOT_TABLES for drop resolution

MOB_TEMPLATES = {
    "rat": {
        "key": "rat",
        "mob_type": "rat",
        "desc": "A mangy brown rat with beady eyes and matted fur. It skitters nervously, looking for scraps.",
        "base_aggression": "passive",
        "hp_min": 20,
        "hp_max": 35,
        "damage_min": 2,
        "damage_max": 5,
        "speed": 1.2,
        "abilities": [],
        "faction": None,
        "is_hunter": False,
        "detection_range": 0,
        "flee_threshold": 50,
        "wander": True,
        "loot_table": "rat",
    },
    "wolf": {
        "key": "wolf",
        "mob_type": "wolf",
        "desc": "A lean grey wolf with piercing amber eyes. Its hackles are raised, and a low growl rumbles in its throat.",
        "base_aggression": "aggressive",
        "hp_min": 60,
        "hp_max": 90,
        "damage_min": 8,
        "damage_max": 14,
        "speed": 1.1,
        "abilities": [
            {
                "ability_id": "wolf_bite",
                "weight": 3,
                "element": "physical",
                "damage_base": 12,
                "cooldown": 2,
                "condition": None,
                "status_effect": "bleed",
                "effect_duration": 3,
                "effect_magnitude": 3,
                "application_chance": 0.3,
            },
        ],
        "faction": None,
        "is_hunter": True,
        "detection_range": 3,
        "flee_threshold": 15,
        "wander": False,
        "loot_table": "wolf",
    },
    "bandit": {
        "key": "bandit",
        "mob_type": "bandit",
        "desc": "A rough-looking figure in patched leather, with a scarred face and a blade held low and ready.",
        "base_aggression": "cautious",
        "hp_min": 70,
        "hp_max": 100,
        "damage_min": 7,
        "damage_max": 13,
        "speed": 1.0,
        "abilities": [
            {
                "ability_id": "bandit_slash",
                "weight": 2,
                "element": "physical",
                "damage_base": 10,
                "cooldown": 1,
                "condition": None,
                "status_effect": None,
                "effect_duration": 0,
                "effect_magnitude": 0,
                "application_chance": 0.0,
            },
            {
                "ability_id": "bandit_intimidate",
                "weight": 1,
                "element": "shadow",
                "damage_base": 0,
                "cooldown": 4,
                "condition": "target_below_50hp",
                "status_effect": "slow",
                "effect_duration": 2,
                "effect_magnitude": 1,
                "application_chance": 0.5,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 2,
        "flee_threshold": 25,
        "wander": False,
        "loot_table": "bandit",
    },
    # --- Vael's Crossing city mobs (07-04) ---
    "sewer_rat": {
        "key": "sewer rat",
        "mob_type": "sewer_rat",
        "desc": (
            "An oversized rat with matted grey fur and yellowed teeth. "
            "It hisses from the darkness, eyes reflecting torchlight "
            "like dull coins."
        ),
        "base_aggression": "passive",
        "hp_min": 15,
        "hp_max": 25,
        "damage_min": 2,
        "damage_max": 4,
        "speed": 1.3,
        "abilities": [
            {
                "ability_id": "rat_bite",
                "weight": 3,
                "element": "physical",
                "damage_base": 4,
                "cooldown": 1,
                "condition": None,
                "status_effect": "disease",
                "effect_duration": 4,
                "effect_magnitude": 1,
                "application_chance": 0.15,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 0,
        "flee_threshold": 60,
        "wander": True,
        "loot_table": "rat",
    },
    "thug": {
        "key": "street thug",
        "mob_type": "thug",
        "desc": (
            "A heavyset figure in stained clothes, hands wrapped in "
            "dirty rags. A crude cudgel hangs from a belt loop. "
            "The look in their eyes says they have nothing to lose."
        ),
        "base_aggression": "cautious",
        "hp_min": 60,
        "hp_max": 85,
        "damage_min": 6,
        "damage_max": 12,
        "speed": 0.9,
        "abilities": [
            {
                "ability_id": "thug_bludgeon",
                "weight": 3,
                "element": "physical",
                "damage_base": 10,
                "cooldown": 2,
                "condition": None,
                "status_effect": "stun",
                "effect_duration": 1,
                "effect_magnitude": 1,
                "application_chance": 0.2,
            },
            {
                "ability_id": "thug_shakedown",
                "weight": 1,
                "element": "shadow",
                "damage_base": 0,
                "cooldown": 5,
                "condition": "target_below_50hp",
                "status_effect": "slow",
                "effect_duration": 2,
                "effect_magnitude": 1,
                "application_chance": 0.4,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 1,
        "flee_threshold": 30,
        "wander": False,
        "loot_table": "bandit",
    },
    "smuggler": {
        "key": "smuggler",
        "mob_type": "smuggler",
        "desc": (
            "A wiry figure in a dark cloak, moving with the alertness "
            "of someone who expects trouble. A short blade is visible "
            "at the hip. Their eyes dart to every exit."
        ),
        "base_aggression": "aggressive",
        "hp_min": 55,
        "hp_max": 80,
        "damage_min": 7,
        "damage_max": 13,
        "speed": 1.1,
        "abilities": [
            {
                "ability_id": "smuggler_backstab",
                "weight": 2,
                "element": "physical",
                "damage_base": 14,
                "cooldown": 3,
                "condition": None,
                "status_effect": "bleed",
                "effect_duration": 3,
                "effect_magnitude": 2,
                "application_chance": 0.3,
            },
            {
                "ability_id": "smuggler_smoke_bomb",
                "weight": 1,
                "element": "shadow",
                "damage_base": 0,
                "cooldown": 6,
                "condition": "self_below_40hp",
                "status_effect": "blind",
                "effect_duration": 2,
                "effect_magnitude": 1,
                "application_chance": 0.6,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 2,
        "flee_threshold": 35,
        "wander": False,
        "loot_table": "bandit",
    },
    "pickpocket": {
        "key": "pickpocket",
        "mob_type": "pickpocket",
        "desc": (
            "A slight figure who blends into the crowd. Quick hands, "
            "quicker feet. If caught, they fight dirty -- but they "
            "prefer running."
        ),
        "base_aggression": "passive",
        "hp_min": 30,
        "hp_max": 50,
        "damage_min": 3,
        "damage_max": 7,
        "speed": 1.4,
        "abilities": [
            {
                "ability_id": "pickpocket_slash",
                "weight": 2,
                "element": "physical",
                "damage_base": 6,
                "cooldown": 1,
                "condition": None,
                "status_effect": None,
                "effect_duration": 0,
                "effect_magnitude": 0,
                "application_chance": 0.0,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 0,
        "flee_threshold": 50,
        "wander": True,
        "loot_table": "bandit",
    },
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_mob_template(template_key):
    """
    Return template dict for given key, or None if not found.

    Args:
        template_key (str): Key into MOB_TEMPLATES.

    Returns:
        dict or None: Template definition, or None.
    """
    return MOB_TEMPLATES.get(template_key)


def apply_mob_template(mob, template_key):
    """
    Apply all template fields to a mob's db attributes.

    If template_key is not found in MOB_TEMPLATES, logs a warning and
    returns without modifying the mob. This keeps backward compatibility
    for mobs spawned without a template.

    Does NOT override base_disposition or trust_sensitive -- those come
    from spawn_def, not template.

    Args:
        mob: SoravelonMob instance.
        template_key (str): Key into MOB_TEMPLATES.
    """
    template = MOB_TEMPLATES.get(template_key)
    if template is None:
        logger.warning(
            "Unknown mob template '%s' — mob will use defaults.", template_key
        )
        return

    # Display
    mob.key = template["key"]
    mob.db.desc = template["desc"]

    # Identity
    mob.db.mob_type = template["mob_type"]

    # Stats
    mob.db.hp_min = template["hp_min"]
    mob.db.hp_max = template["hp_max"]
    mob.db.damage_min = template["damage_min"]
    mob.db.damage_max = template["damage_max"]
    mob.db.speed = template["speed"]

    # Behavior
    mob.db.base_aggression = template["base_aggression"]
    mob.db.is_hunter = template["is_hunter"]
    mob.db.detection_range = template["detection_range"]
    mob.db.wander = template["wander"]
    mob.db.flee_threshold = template["flee_threshold"]

    # Combat
    mob.db.abilities = list(template["abilities"])  # copy to avoid shared mutation

    # Faction
    mob.db.faction = template["faction"]

    # Loot
    mob.db.loot_table = template["loot_table"]
