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

# Rarity-based damage multipliers (D-04)
RARITY_DAMAGE_MULTIPLIERS = {
    "normal": 1.0,
    "magic": 1.15,
    "rare": 1.3,
    "legendary": 1.5,
}

# Default status effect durations by category
_STACKABLE_DURATION = 3   # rounds for stackable effects (poison, bleed, burn, etc.)
_NON_STACKABLE_DURATION = 2  # rounds for non-stackable effects (slow, root, blind, etc.)


# --- Interface hooks (combat system reads these) ---

def check_mob_damage_modifiers(mob):
    """
    Compute merged combat modifiers from all mob affixes plus rarity multiplier.

    Merging rules:
    - damage_multiplier: multiplicative (product of all values)
    - damage_reduction_flat: additive (sum)
    - action_budget_bonus: additive (sum)
    - All other numeric modifiers: take max
    - rarity_damage_multiplier: from RARITY_DAMAGE_MULTIPLIERS lookup

    Args:
        mob: Mob object with db.affix_list and db.rarity.

    Returns:
        dict: Merged combat modifiers including rarity_damage_multiplier.
    """
    rarity = mob.db.rarity or "normal"
    modifiers = {"rarity_damage_multiplier": RARITY_DAMAGE_MULTIPLIERS.get(rarity, 1.0)}

    additive_keys = {"damage_reduction_flat", "action_budget_bonus", "dodge_bonus"}

    for affix_tag in (mob.db.affix_list or []):
        affix_def = MOB_AFFIXES.get(affix_tag, {})
        combat_mods = affix_def.get("combat_modifiers", {})
        for key, value in combat_mods.items():
            if key == "damage_multiplier":
                # Multiplicative stacking
                modifiers[key] = modifiers.get(key, 1.0) * value
            elif key in additive_keys:
                # Additive stacking
                modifiers[key] = modifiers.get(key, 0) + value
            else:
                # Take max for other numeric modifiers
                modifiers[key] = max(modifiers.get(key, 0), value)

    return modifiers


def check_mob_on_hit_effects(mob, target):
    """
    Apply on-hit status effects from mob affixes to the target.

    Checks target immunity before applying. Uses apply_effect from
    world.status_effects for actual application.

    Args:
        mob: Mob that landed the hit.
        target: Character or mob that was hit.

    Returns:
        list[tuple[str, bool]]: (effect_name, was_applied) for each affix on_hit.
    """
    from world.status_effects import apply_effect, STACKABLE_EFFECTS

    results = []
    for affix_tag in (mob.db.affix_list or []):
        affix_def = MOB_AFFIXES.get(affix_tag, {})
        on_hit = affix_def.get("on_hit_effect")
        if not on_hit:
            continue

        # Check immunity (volatile ndb or persistent db)
        immunities = set(target.ndb.immunities or []) | set(target.db.immunities or [])
        if on_hit in immunities:
            results.append((on_hit, False))
            continue

        # Determine duration based on effect category
        duration = _STACKABLE_DURATION if on_hit in STACKABLE_EFFECTS else _NON_STACKABLE_DURATION

        apply_effect(target, on_hit, duration, magnitude=1.0, source_id=mob.id)
        results.append((on_hit, True))

    return results


def check_mob_per_round_effects(mob):
    """
    Process per-round effects from mob affixes (heal_self, periodic_root, etc.).

    Args:
        mob: Mob whose per-round effects fire.

    Returns:
        list[dict]: Each dict has 'effect', 'applied' (bool), 'details' (str).
    """
    results = []
    for affix_tag in (mob.db.affix_list or []):
        affix_def = MOB_AFFIXES.get(affix_tag, {})
        per_round = affix_def.get("per_round_effect")
        if not per_round:
            continue

        combat_mods = affix_def.get("combat_modifiers", {})

        if per_round == "heal_self":
            # Regenerating affix: heal percentage of max HP per round
            regen_pct = combat_mods.get("regen_pct_per_round", 0.03)
            max_hp = mob.db.max_hp or 100
            heal_amount = int(regen_pct * max_hp)
            if heal_amount > 0:
                current_hp = mob.ndb.hp or 0
                mob.ndb.hp = min(max_hp, current_hp + heal_amount)
                results.append({
                    "effect": "heal_self",
                    "applied": True,
                    "details": f"{mob.key} regenerates {heal_amount} HP.",
                })
            else:
                results.append({
                    "effect": "heal_self",
                    "applied": False,
                    "details": "No regeneration amount.",
                })

        elif per_round == "periodic_root":
            # Rooting affix: apply root to combat targets on interval
            root_interval = combat_mods.get("root_interval", 3)
            combat_round = mob.ndb.combat_round or 0
            if root_interval > 0 and combat_round % root_interval == 0:
                from world.status_effects import apply_effect
                # Apply root to all targets in mob's current combat
                targets = mob.ndb.combat_targets or []
                for tgt in targets:
                    immunities = set(getattr(tgt.ndb, 'immunities', None) or []) | set(tgt.db.immunities or [])
                    if "root" not in immunities:
                        apply_effect(tgt, "root", _NON_STACKABLE_DURATION, magnitude=1.0, source_id=mob.id)
                results.append({
                    "effect": "periodic_root",
                    "applied": True,
                    "details": f"{mob.key} roots nearby enemies.",
                })
            else:
                results.append({
                    "effect": "periodic_root",
                    "applied": False,
                    "details": "Not on root interval this round.",
                })

        else:
            # Unknown per-round effect — log but don't crash
            results.append({
                "effect": per_round,
                "applied": False,
                "details": f"Unknown per-round effect: {per_round}.",
            })

    return results
