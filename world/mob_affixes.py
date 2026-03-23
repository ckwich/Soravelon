"""
Mob affix definitions — single source of truth.

Each affix has:
  - tag: string stored in category="mob_affix" on the mob
  - display_name: shown to player on reveal
  - category: offensive/defensive/disruption/elemental/immunity
  - combat_modifiers: dict of stat modifiers (read by combat system)
  - on_hit_effect: status effect applied on hit (or None)
  - per_round_effect: fires each combat round (or None)
  - reveal_message: shown on first relevant interaction ({mob_name} placeholder)
"""

MOB_AFFIXES = {
    # OFFENSIVE
    "enraged": {
        "tag": "enraged",
        "display_name": "Enraged",
        "category": "offensive",
        "combat_modifiers": {"damage_multiplier": 1.30},
        "on_hit_effect": None,
        "per_round_effect": None,
        "reveal_message": "{mob_name} is enraged — hits land harder than expected.",
    },
    "vampiric": {
        "tag": "vampiric",
        "display_name": "Vampiric",
        "category": "offensive",
        "combat_modifiers": {"lifesteal_pct": 0.15},
        "on_hit_effect": None,
        "per_round_effect": None,
        "reveal_message": "{mob_name} heals as it strikes you.",
    },
    "echoing": {
        "tag": "echoing",
        "display_name": "Echoing",
        "category": "offensive",
        "combat_modifiers": {"echo_chance": 1.0, "echo_magnitude": 0.50},
        "on_hit_effect": None,
        "per_round_effect": None,
        "reveal_message": "{mob_name}'s strike reverberates — the blow lands twice.",
    },
    "frenzied": {
        "tag": "frenzied",
        "display_name": "Frenzied",
        "category": "offensive",
        "combat_modifiers": {"action_budget_bonus": 1},
        "on_hit_effect": None,
        "per_round_effect": None,
        "reveal_message": "{mob_name} moves with unnatural speed.",
    },
    # DEFENSIVE
    "armored": {
        "tag": "armored",
        "display_name": "Armored",
        "category": "defensive",
        "combat_modifiers": {"damage_reduction_flat": 0.25},
        "on_hit_effect": None,
        "per_round_effect": None,
        "reveal_message": "{mob_name}'s hide turns the blow — it's heavily armored.",
    },
    "regenerating": {
        "tag": "regenerating",
        "display_name": "Regenerating",
        "category": "defensive",
        "combat_modifiers": {"regen_pct_per_round": 0.03},
        "on_hit_effect": None,
        "per_round_effect": "heal_self",
        "reveal_message": "{mob_name}'s wounds close as quickly as you open them.",
    },
    "warding": {
        "tag": "warding",
        "display_name": "Warding",
        "category": "defensive",
        "combat_modifiers": {"status_duration_multiplier": 0.50},
        "on_hit_effect": None,
        "per_round_effect": None,
        "reveal_message": "{mob_name} shakes off the effect — it resists status conditions.",
    },
    "evasive": {
        "tag": "evasive",
        "display_name": "Evasive",
        "category": "defensive",
        "combat_modifiers": {"dodge_bonus": 0.20},
        "on_hit_effect": None,
        "per_round_effect": None,
        "reveal_message": "{mob_name} moves before the strike lands.",
    },
    # DISRUPTION
    "slowing": {
        "tag": "slowing",
        "display_name": "Slowing",
        "category": "disruption",
        "combat_modifiers": {},
        "on_hit_effect": "slow",
        "per_round_effect": None,
        "reveal_message": "{mob_name}'s strike drags at you — you feel slowed.",
    },
    "draining": {
        "tag": "draining",
        "display_name": "Draining",
        "category": "disruption",
        "combat_modifiers": {"resource_drain_pct": 0.10},
        "on_hit_effect": "drain_resource",
        "per_round_effect": None,
        "reveal_message": "{mob_name}'s strike costs you more than HP.",
    },
    "blinding": {
        "tag": "blinding",
        "display_name": "Blinding",
        "category": "disruption",
        "combat_modifiers": {"blind_chance": 0.20},
        "on_hit_effect": "blind",
        "per_round_effect": None,
        "reveal_message": "{mob_name}'s strike clouds your vision.",
    },
    "rooting": {
        "tag": "rooting",
        "display_name": "Rooting",
        "category": "disruption",
        "combat_modifiers": {"root_interval": 3},
        "on_hit_effect": None,
        "per_round_effect": "periodic_root",
        "reveal_message": "{mob_name} pins you in place.",
    },
    # ELEMENTAL
    "fire_touched": {
        "tag": "fire_touched",
        "display_name": "Fire-Touched",
        "category": "elemental",
        "combat_modifiers": {},
        "on_hit_effect": "burn",
        "per_round_effect": None,
        "reveal_message": "{mob_name}'s strikes carry heat.",
    },
    "venom_touched": {
        "tag": "venom_touched",
        "display_name": "Venom-Touched",
        "category": "elemental",
        "combat_modifiers": {},
        "on_hit_effect": "poison",
        "per_round_effect": None,
        "reveal_message": "{mob_name}'s strikes carry venom.",
    },
    "storm_touched": {
        "tag": "storm_touched",
        "display_name": "Storm-Touched",
        "category": "elemental",
        "combat_modifiers": {},
        "on_hit_effect": "wet",
        "per_round_effect": None,
        "reveal_message": "{mob_name}'s strikes carry the storm.",
    },
    "ancient": {
        "tag": "ancient",
        "display_name": "Ancient",
        "category": "elemental",
        "combat_modifiers": {"damage_reduction_flat": 0.15},
        "on_hit_effect": None,
        "per_round_effect": None,
        "reveal_message": "Something old in {mob_name} resists your strikes.",
    },
    # IMMUNITIES
    "fire_immune": {
        "tag": "fire_immune",
        "display_name": "Fire Immune",
        "category": "immunity",
        "combat_modifiers": {},
        "on_hit_effect": None,
        "per_round_effect": None,
        "reveal_message": "{mob_name} is immune to fire effects.",
    },
    "poison_immune": {
        "tag": "poison_immune",
        "display_name": "Poison Immune",
        "category": "immunity",
        "combat_modifiers": {},
        "on_hit_effect": None,
        "per_round_effect": None,
        "reveal_message": "{mob_name} is immune to poison.",
    },
    "stun_immune": {
        "tag": "stun_immune",
        "display_name": "Stun Immune",
        "category": "immunity",
        "combat_modifiers": {},
        "on_hit_effect": None,
        "per_round_effect": None,
        "reveal_message": "{mob_name} cannot be stunned.",
    },
    "root_immune": {
        "tag": "root_immune",
        "display_name": "Root Immune",
        "category": "immunity",
        "combat_modifiers": {},
        "on_hit_effect": None,
        "per_round_effect": None,
        "reveal_message": "{mob_name} cannot be rooted.",
    },
}

# Node-type weighted affix pools
NODE_AFFIX_POOLS = {
    "resonance": ["ancient", "warding", "regenerating", "armored", "evasive"],
    "thermal": ["fire_touched", "fire_immune", "enraged", "armored", "frenzied"],
    "cognitive": ["echoing", "frenzied", "evasive", "warding", "rooting"],
    "gravity": ["slowing", "rooting", "armored", "enraged", "ancient"],
    "temporal": ["echoing", "draining", "blinding", "warding", "evasive"],
}

GENERAL_AFFIX_POOL = [
    "enraged", "armored", "vampiric", "slowing",
    "regenerating", "evasive", "draining", "blinding",
    "frenzied", "warding", "rooting",
]

FORBIDDEN_COMBINATIONS = [
    {"stun_immune", "root_immune"},
    {"regenerating", "vampiric"},
    {"armored", "ancient"},
]

DEFENSIVE_LIMIT = 1
DEFENSIVE_AFFIXES = {"armored", "regenerating", "warding", "evasive"}

RARITY_WEIGHTS = {
    "normal": 850,
    "magic": 120,
    "rare": 25,
    "legendary": 5,
}

PACK_SIZES = {
    "magic": (1, 2),
    "rare": (2, 3),
    "legendary": (3, 4),
}


# --- Interface hooks (stubs — combat system reads these) ---

def check_mob_damage_modifiers(mob):
    """STUB — called by combat system when calculating damage."""
    return mob.get_combat_modifiers() if hasattr(mob, 'get_combat_modifiers') else {}


def check_mob_on_hit_effects(mob, target):
    """STUB — called by combat system after a hit lands."""
    effects = []
    for affix_tag in (mob.db.affix_list or []):
        affix_def = MOB_AFFIXES.get(affix_tag, {})
        on_hit = affix_def.get("on_hit_effect")
        if on_hit:
            effects.append((on_hit, 1))
    return effects


def check_mob_per_round_effects(mob):
    """STUB — called by combat system at round end."""
    effects = []
    for affix_tag in (mob.db.affix_list or []):
        affix_def = MOB_AFFIXES.get(affix_tag, {})
        per_round = affix_def.get("per_round_effect")
        if per_round:
            effects.append(per_round)
    return effects
