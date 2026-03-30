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
    # --- Stormhaven Coast mobs (07-08) ---
    "shore_crab": {
        "key": "shore crab",
        "mob_type": "shore_crab",
        "desc": (
            "A large crab with a mottled grey-green shell, perfectly "
            "camouflaged against the coastal rocks. Its claws are "
            "disproportionately large, snapping open and shut with "
            "a sound like cracking knuckles."
        ),
        "base_aggression": "passive",
        "hp_min": 25,
        "hp_max": 40,
        "damage_min": 4,
        "damage_max": 8,
        "speed": 0.9,
        "abilities": [
            {
                "ability_id": "crab_pinch",
                "weight": 3,
                "element": "physical",
                "damage_base": 7,
                "cooldown": 1,
                "condition": None,
                "status_effect": "bleed",
                "effect_duration": 2,
                "effect_magnitude": 2,
                "application_chance": 0.2,
            },
            {
                "ability_id": "shell_guard",
                "weight": 1,
                "element": "physical",
                "damage_base": 0,
                "cooldown": 5,
                "condition": "self_below_40hp",
                "status_effect": None,
                "effect_duration": 0,
                "effect_magnitude": 0,
                "application_chance": 0.0,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 0,
        "flee_threshold": 40,
        "wander": True,
        "loot_table": "shore_crab",
    },
    "sea_serpent": {
        "key": "sea serpent",
        "mob_type": "sea_serpent",
        "desc": (
            "A sinuous creature of deep water, its scales the color of "
            "storm-tossed iron. It rises from the depths with unsettling "
            "silence, fangs bared, eyes like polished obsidian. The air "
            "around it smells of brine and something older."
        ),
        "base_aggression": "aggressive",
        "hp_min": 90,
        "hp_max": 140,
        "damage_min": 12,
        "damage_max": 20,
        "speed": 1.0,
        "abilities": [
            {
                "ability_id": "serpent_constrict",
                "weight": 2,
                "element": "physical",
                "damage_base": 16,
                "cooldown": 3,
                "condition": None,
                "status_effect": "slow",
                "effect_duration": 2,
                "effect_magnitude": 2,
                "application_chance": 0.4,
            },
            {
                "ability_id": "venom_spray",
                "weight": 1,
                "element": "nature",
                "damage_base": 10,
                "cooldown": 4,
                "condition": None,
                "status_effect": "poison",
                "effect_duration": 4,
                "effect_magnitude": 3,
                "application_chance": 0.5,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 2,
        "flee_threshold": 10,
        "wander": False,
        "loot_table": "sea_serpent",
    },
    "coastal_raider": {
        "key": "coastal raider",
        "mob_type": "coastal_raider",
        "desc": (
            "A weathered figure in salt-stained leathers, face half-hidden "
            "by a ragged scarf. A cutlass hangs at the hip, well-oiled "
            "and recently sharpened. The look in their eyes is calculating "
            "-- they are deciding whether you are worth the trouble."
        ),
        "base_aggression": "cautious",
        "hp_min": 65,
        "hp_max": 95,
        "damage_min": 8,
        "damage_max": 14,
        "speed": 1.0,
        "abilities": [
            {
                "ability_id": "cutlass_slash",
                "weight": 3,
                "element": "physical",
                "damage_base": 11,
                "cooldown": 1,
                "condition": None,
                "status_effect": "bleed",
                "effect_duration": 2,
                "effect_magnitude": 2,
                "application_chance": 0.25,
            },
            {
                "ability_id": "net_throw",
                "weight": 1,
                "element": "physical",
                "damage_base": 3,
                "cooldown": 5,
                "condition": None,
                "status_effect": "slow",
                "effect_duration": 3,
                "effect_magnitude": 2,
                "application_chance": 0.6,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 2,
        "flee_threshold": 25,
        "wander": False,
        "loot_table": "coastal_raider",
    },
    "cliff_harpy": {
        "key": "cliff harpy",
        "mob_type": "cliff_harpy",
        "desc": (
            "A gaunt, avian creature with ragged feathers the color of "
            "storm clouds. Its talons are hooked and crusted with dried "
            "blood. It perches on the cliff edge, head cocked, watching "
            "with unsettling intelligence. When it screams, the sound "
            "cuts through the wind like a blade."
        ),
        "base_aggression": "aggressive",
        "hp_min": 50,
        "hp_max": 75,
        "damage_min": 9,
        "damage_max": 15,
        "speed": 1.2,
        "abilities": [
            {
                "ability_id": "harpy_screech",
                "weight": 2,
                "element": "sonic",
                "damage_base": 5,
                "cooldown": 4,
                "condition": None,
                "status_effect": "stun",
                "effect_duration": 1,
                "effect_magnitude": 1,
                "application_chance": 0.35,
            },
            {
                "ability_id": "harpy_dive",
                "weight": 2,
                "element": "physical",
                "damage_base": 14,
                "cooldown": 3,
                "condition": None,
                "status_effect": None,
                "effect_duration": 0,
                "effect_magnitude": 0,
                "application_chance": 0.0,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 3,
        "flee_threshold": 20,
        "wander": False,
        "loot_table": "cliff_harpy",
    },
    "salt_lurker": {
        "key": "salt lurker",
        "mob_type": "salt_lurker",
        "desc": (
            "A pale, bloated creature that emerged from the brine-soaked "
            "depths of the sea caves. Its skin is crusted with salt "
            "crystals that crack and flake with each movement. Eyeless, "
            "it navigates by vibration and the taste of the air. When "
            "disturbed, it rears up with surprising speed."
        ),
        "base_aggression": "passive",
        "hp_min": 55,
        "hp_max": 80,
        "damage_min": 10,
        "damage_max": 16,
        "speed": 0.8,
        "abilities": [
            {
                "ability_id": "lurker_slam",
                "weight": 2,
                "element": "physical",
                "damage_base": 14,
                "cooldown": 2,
                "condition": None,
                "status_effect": "stun",
                "effect_duration": 1,
                "effect_magnitude": 1,
                "application_chance": 0.25,
            },
            {
                "ability_id": "spit_brine",
                "weight": 1,
                "element": "nature",
                "damage_base": 8,
                "cooldown": 4,
                "condition": None,
                "status_effect": "blind",
                "effect_duration": 2,
                "effect_magnitude": 1,
                "application_chance": 0.4,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 1,
        "flee_threshold": 15,
        "wander": False,
        "loot_table": "salt_lurker",
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
    # --- Ashreach Plains mobs (07-05) ---
    "ash_wolf": {
        "key": "ash wolf",
        "mob_type": "ash_wolf",
        "desc": (
            "A lean wolf with a dusty grey-brown coat, nearly invisible "
            "against the Ashreach grass. Its amber eyes are intelligent "
            "and watchful. Ash-colored fur gives the breed its name -- "
            "and its camouflage."
        ),
        "base_aggression": "aggressive",
        "hp_min": 55,
        "hp_max": 85,
        "damage_min": 7,
        "damage_max": 13,
        "speed": 1.1,
        "abilities": [
            {
                "ability_id": "ash_wolf_bite",
                "weight": 3,
                "element": "physical",
                "damage_base": 11,
                "cooldown": 2,
                "condition": None,
                "status_effect": "bleed",
                "effect_duration": 3,
                "effect_magnitude": 3,
                "application_chance": 0.3,
            },
            {
                "ability_id": "ash_wolf_howl",
                "weight": 1,
                "element": "shadow",
                "damage_base": 0,
                "cooldown": 6,
                "condition": "self_below_50hp",
                "status_effect": "slow",
                "effect_duration": 2,
                "effect_magnitude": 1,
                "application_chance": 0.5,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 2,
        "flee_threshold": 15,
        "wander": False,
        "loot_table": "ash_wolf",
    },
    "plains_viper": {
        "key": "plains viper",
        "mob_type": "plains_viper",
        "desc": (
            "A thick-bodied serpent coiled among the dry grass, its "
            "scales patterned in dusty brown and pale gold. It lies "
            "motionless until prey draws close, then strikes with "
            "terrifying speed."
        ),
        "base_aggression": "cautious",
        "hp_min": 30,
        "hp_max": 50,
        "damage_min": 10,
        "damage_max": 18,
        "speed": 1.3,
        "abilities": [
            {
                "ability_id": "viper_poison_bite",
                "weight": 3,
                "element": "nature",
                "damage_base": 14,
                "cooldown": 2,
                "condition": None,
                "status_effect": "poison",
                "effect_duration": 4,
                "effect_magnitude": 4,
                "application_chance": 0.5,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 1,
        "flee_threshold": 40,
        "wander": False,
        "loot_table": "plains_viper",
    },
    "ashreach_bandit": {
        "key": "Ashreach bandit",
        "mob_type": "ashreach_bandit",
        "desc": (
            "A weather-hardened figure in mismatched leather and stolen "
            "Imperial cloth. A notched blade hangs at the hip. The look "
            "of someone who chose the plains over prison -- or possibly "
            "both."
        ),
        "base_aggression": "cautious",
        "hp_min": 65,
        "hp_max": 95,
        "damage_min": 7,
        "damage_max": 12,
        "speed": 1.0,
        "abilities": [
            {
                "ability_id": "bandit_slash",
                "weight": 3,
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
                "ability_id": "bandit_dirty_kick",
                "weight": 1,
                "element": "physical",
                "damage_base": 5,
                "cooldown": 4,
                "condition": "target_below_50hp",
                "status_effect": "stun",
                "effect_duration": 1,
                "effect_magnitude": 1,
                "application_chance": 0.3,
            },
        ],
        "faction": None,
        "is_hunter": False,
        "detection_range": 2,
        "flee_threshold": 25,
        "wander": False,
        "loot_table": "ashreach_bandit",
    },
    "dust_beetle": {
        "key": "dust beetle",
        "mob_type": "dust_beetle",
        "desc": (
            "A beetle the size of a small dog, its carapace the same "
            "ash-grey as the plains soil. It trundles through the grass "
            "on stubby legs, mandibles working at whatever organic "
            "matter it finds. Harmless unless cornered."
        ),
        "base_aggression": "passive",
        "hp_min": 25,
        "hp_max": 40,
        "damage_min": 3,
        "damage_max": 7,
        "speed": 0.8,
        "abilities": [
            {
                "ability_id": "beetle_carapace_slam",
                "weight": 2,
                "element": "physical",
                "damage_base": 6,
                "cooldown": 3,
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
        "loot_table": "dust_beetle",
    },
    "steppe_hawk": {
        "key": "steppe hawk",
        "mob_type": "steppe_hawk",
        "desc": (
            "A large raptor with dark plumage and a wingspan wider than "
            "a person's outstretched arms. It circles overhead with "
            "patient menace, sharp eyes tracking movement below. When "
            "it stoops, it hits like a thrown stone."
        ),
        "base_aggression": "aggressive",
        "hp_min": 35,
        "hp_max": 55,
        "damage_min": 9,
        "damage_max": 16,
        "speed": 1.4,
        "abilities": [
            {
                "ability_id": "hawk_dive",
                "weight": 3,
                "element": "physical",
                "damage_base": 15,
                "cooldown": 3,
                "condition": None,
                "status_effect": None,
                "effect_duration": 0,
                "effect_magnitude": 0,
                "application_chance": 0.0,
            },
            {
                "ability_id": "hawk_screech",
                "weight": 1,
                "element": "shadow",
                "damage_base": 0,
                "cooldown": 5,
                "condition": None,
                "status_effect": "slow",
                "effect_duration": 2,
                "effect_magnitude": 1,
                "application_chance": 0.4,
            },
        ],
        "faction": None,
        "is_hunter": True,
        "detection_range": 4,
        "flee_threshold": 30,
        "wander": False,
        "loot_table": "steppe_hawk",
    },
    "alpha_ash_wolf": {
        "key": "Alpha Ash Wolf",
        "mob_type": "alpha_ash_wolf",
        "desc": (
            "A massive wolf, half again the size of its packmates, with "
            "a scarred muzzle and a coat so dark it looks burnt. Its eyes "
            "burn with feral intelligence. This is the apex predator of "
            "the Ashreach -- the pack lord, unchallenged. A low growl "
            "reverberates through the stone den."
        ),
        "base_aggression": "aggressive",
        "hp_min": 180,
        "hp_max": 250,
        "damage_min": 14,
        "damage_max": 22,
        "speed": 1.0,
        "abilities": [
            {
                "ability_id": "alpha_rending_bite",
                "weight": 3,
                "element": "physical",
                "damage_base": 20,
                "cooldown": 2,
                "condition": None,
                "status_effect": "bleed",
                "effect_duration": 4,
                "effect_magnitude": 5,
                "application_chance": 0.5,
            },
            {
                "ability_id": "alpha_rallying_howl",
                "weight": 1,
                "element": "shadow",
                "damage_base": 0,
                "cooldown": 8,
                "condition": "self_below_50hp",
                "status_effect": "slow",
                "effect_duration": 3,
                "effect_magnitude": 2,
                "application_chance": 0.7,
            },
            {
                "ability_id": "alpha_pounce",
                "weight": 2,
                "element": "physical",
                "damage_base": 16,
                "cooldown": 4,
                "condition": None,
                "status_effect": "stun",
                "effect_duration": 1,
                "effect_magnitude": 1,
                "application_chance": 0.3,
            },
        ],
        "faction": None,
        "is_hunter": True,
        "detection_range": 4,
        "flee_threshold": 5,
        "wander": False,
        "loot_table": "alpha_ash_wolf",
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
