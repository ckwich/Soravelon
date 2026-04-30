"""
Reusable equipment archetypes and affixes for generated gear drops.

Loot tables stay builder-safe literal dicts. They may reference an
``equipment_archetype`` plus an ``affix_profile``; this module expands that
small authoring payload into a full item_def for item_spawner.
"""

from __future__ import annotations

import copy
import random


class EquipmentArchetypeError(ValueError):
    """Raised when authored equipment generation data is invalid."""


RARITY_ORDER = ["normal", "magic", "rare", "legendary", "ancient"]


EQUIPMENT_ARCHETYPES = {
    "agile_blade": {
        "key": "blade",
        "equip_slot": "main_hand",
        "scaling_stat": "agility",
        "weight": 1.5,
        "tags": ["weapon", "blade", "light"],
        "material_tier_by_tier": [1, 1, 2, 2, 3],
        "damage_min_by_tier": [5, 6, 8, 10, 13],
        "damage_max_by_tier": [10, 12, 15, 18, 22],
        "stat_bonuses_by_tier": [
            {},
            {},
            {"agility": 1},
            {"agility": 1},
            {"agility": 2},
        ],
        "desc_fragment": "It favors speed, balance, and precise handwork.",
    },
    "cleaving_axe": {
        "key": "boarding axe",
        "equip_slot": "main_hand",
        "scaling_stat": "strength",
        "weight": 2.1,
        "tags": ["weapon", "axe", "heavy"],
        "material_tier_by_tier": [1, 1, 2, 2, 3],
        "damage_min_by_tier": [7, 9, 11, 14, 17],
        "damage_max_by_tier": [13, 16, 20, 24, 29],
        "stat_bonuses_by_tier": [
            {},
            {"strength": 1},
            {"strength": 1},
            {"strength": 2},
            {"strength": 2},
        ],
        "desc_fragment": "It is weighted for hard commitments and brutal follow-through.",
    },
    "guarded_mail": {
        "key": "mail coat",
        "equip_slot": "chest",
        "scaling_stat": "endurance",
        "weight": 7.0,
        "tags": ["armor", "mail", "medium"],
        "material_tier_by_tier": [1, 1, 2, 2, 3],
        "armor_value_by_tier": [4, 6, 8, 11, 15],
        "stat_bonuses_by_tier": [
            {},
            {},
            {"endurance": 1},
            {"endurance": 1},
            {"endurance": 2},
        ],
        "desc_fragment": "The rings are set to spread force instead of merely catching it.",
    },
    "beast_talisman": {
        "key": "talisman",
        "equip_slot": "amulet",
        "scaling_stat": "resonance",
        "weight": 0.2,
        "tags": ["accessory", "trophy", "beast"],
        "material_tier_by_tier": [1, 1, 2, 2, 3],
        "stat_bonuses_by_tier": [
            {"presence": 1},
            {"presence": 1},
            {"presence": 1, "resonance": 1},
            {"presence": 2, "resonance": 1},
            {"presence": 2, "resonance": 2},
        ],
        "desc_fragment": "It keeps the memory of a living thing close to the skin.",
    },
}


EQUIPMENT_AFFIXES = {
    "balanced": {
        "name": "Balanced",
        "name_prefix": "Balanced",
        "allowed_tags": ["weapon"],
        "stat_bonuses_by_tier": [
            {"agility": 1},
            {"agility": 1},
            {"agility": 1},
            {"agility": 2},
            {"agility": 2},
        ],
        "damage_max_by_tier": [1, 1, 2, 2, 3],
        "value_multiplier": 1.15,
        "desc_fragment": "Its balance invites quick follow-up strikes.",
    },
    "keen": {
        "name": "Keen",
        "name_prefix": "Keen",
        "allowed_tags": ["weapon"],
        "damage_min_by_tier": [1, 1, 1, 2, 2],
        "damage_max_by_tier": [1, 2, 2, 3, 3],
        "value_multiplier": 1.18,
        "desc_fragment": "The edge bites sooner than its plain shape suggests.",
    },
    "hewing": {
        "name": "Hewing",
        "name_prefix": "Hewing",
        "allowed_tags": ["weapon", "heavy"],
        "stat_bonuses_by_tier": [
            {"strength": 1},
            {"strength": 1},
            {"strength": 1},
            {"strength": 2},
            {"strength": 2},
        ],
        "damage_min_by_tier": [1, 1, 2, 2, 3],
        "value_multiplier": 1.16,
        "desc_fragment": "Its weight wants to finish what the swing begins.",
    },
    "guarded": {
        "name": "Guarded",
        "name_prefix": "Guarded",
        "allowed_tags": ["armor"],
        "armor_value_by_tier": [1, 1, 2, 2, 3],
        "stat_bonuses_by_tier": [
            {"endurance": 1},
            {"endurance": 1},
            {"endurance": 1},
            {"endurance": 2},
            {"endurance": 2},
        ],
        "value_multiplier": 1.17,
        "desc_fragment": "Its reinforcement protects without turning clumsy.",
    },
    "resilient": {
        "name": "Resilient",
        "name_prefix": "Resilient",
        "allowed_tags": ["armor", "accessory"],
        "armor_value_by_tier": [1, 1, 1, 2, 2],
        "stat_bonuses_by_tier": [
            {"endurance": 1},
            {"endurance": 1},
            {"endurance": 1},
            {"endurance": 1},
            {"endurance": 2},
        ],
        "value_multiplier": 1.12,
        "desc_fragment": "It seems made for someone who expects to get back up.",
    },
    "precise": {
        "name": "Precise",
        "name_prefix": "Precise",
        "allowed_tags": ["weapon", "accessory"],
        "stat_bonuses_by_tier": [
            {"acuity": 1},
            {"acuity": 1},
            {"acuity": 1},
            {"acuity": 2},
            {"acuity": 2},
        ],
        "value_multiplier": 1.14,
        "desc_fragment": "Small details in the work reward careful timing.",
    },
    "commanding": {
        "name": "Commanding",
        "name_prefix": "Commanding",
        "allowed_tags": ["accessory", "armor"],
        "stat_bonuses_by_tier": [
            {"presence": 1},
            {"presence": 1},
            {"presence": 1},
            {"presence": 2},
            {"presence": 2},
        ],
        "value_multiplier": 1.12,
        "desc_fragment": "It has the quiet confidence of something meant to be seen.",
    },
}


EQUIPMENT_AFFIX_PROFILES = {
    "bandit_weapon": {
        "affixes": [
            {"id": "balanced", "weight": 4},
            {"id": "keen", "weight": 3},
            {"id": "precise", "weight": 1},
        ],
    },
    "raider_weapon": {
        "affixes": [
            {"id": "balanced", "weight": 3},
            {"id": "keen", "weight": 3},
            {"id": "hewing", "weight": 2},
        ],
    },
    "frontier_armor": {
        "affixes": [
            {"id": "guarded", "weight": 4},
            {"id": "resilient", "weight": 3},
            {"id": "commanding", "weight": 1},
        ],
    },
    "beast_trophy": {
        "affixes": [
            {"id": "resilient", "weight": 2},
            {"id": "commanding", "weight": 2},
            {"id": "precise", "weight": 1},
        ],
    },
}


_CONFIG_KEYS = {
    "affix_profile",
    "affix_count",
    "affix_count_by_tier",
    "weight_in_pool",
    "value_by_tier",
    "rarity_by_tier",
    "desc_by_tier",
    "material_tier_by_tier",
    "damage_min_by_tier",
    "damage_max_by_tier",
    "armor_value_by_tier",
    "stat_bonuses_by_tier",
}

_PASSTHROUGH_KEYS = {
    "stackable",
    "tool_slot",
    "tool_tag",
    "two_handed",
    "use_effect",
    "lore_tags",
    "source_tags",
}


def _tier_index(tier):
    return max(0, min(4, int(tier) - 1))


def _tiered_value(data, base_key, idx, default=None):
    tiered_key = f"{base_key}_by_tier"
    if tiered_key in data:
        values = data[tiered_key]
        if len(values) != 5:
            raise EquipmentArchetypeError(
                f"{tiered_key} must contain exactly five tier values"
            )
        return copy.deepcopy(values[idx])
    if base_key in data:
        return copy.deepcopy(data[base_key])
    return copy.deepcopy(default)


def _merge_stat_bonuses(left, right):
    merged = dict(left or {})
    for stat, value in (right or {}).items():
        merged[stat] = merged.get(stat, 0) + value
    return {stat: value for stat, value in merged.items() if value}


def _tags_match(affix, archetype):
    allowed_tags = set(affix.get("allowed_tags", []))
    if not allowed_tags:
        return True
    archetype_tags = set(archetype.get("tags", []))
    return bool(allowed_tags & archetype_tags)


def _slot_matches(affix, slot):
    allowed_slots = set(affix.get("allowed_slots", []))
    return not allowed_slots or slot in allowed_slots


def _tier_matches(affix, tier):
    min_tier = affix.get("min_tier", 1)
    max_tier = affix.get("max_tier", 5)
    return min_tier <= tier <= max_tier


def _eligible_affix_weights(profile, archetype, tier, slot):
    combined = {}
    for entry in profile.get("affixes", []):
        affix_id = entry.get("id")
        affix = EQUIPMENT_AFFIXES.get(affix_id)
        if not affix:
            raise EquipmentArchetypeError(f"Unknown equipment affix '{affix_id}'")
        if not _tags_match(affix, archetype):
            continue
        if not _slot_matches(affix, slot):
            continue
        if not _tier_matches(affix, tier):
            continue
        combined[affix_id] = combined.get(affix_id, 0) + entry.get("weight", 1)
    return combined


def _weighted_pick_without_replacement(candidates, count, rng):
    selected = []
    remaining = dict(candidates)
    for _ in range(min(count, len(remaining))):
        total = sum(max(0, weight) for weight in remaining.values())
        if total <= 0:
            break
        roll = rng.uniform(0, total)
        cumulative = 0
        for affix_id, weight in list(remaining.items()):
            cumulative += max(0, weight)
            if roll <= cumulative:
                selected.append(affix_id)
                del remaining[affix_id]
                break
    return selected


def _affix_count_for_tier(drop, profile, idx):
    if "affix_count_by_tier" in drop:
        values = drop["affix_count_by_tier"]
        if len(values) != 5:
            raise EquipmentArchetypeError(
                "affix_count_by_tier must contain exactly five tier values"
            )
        return values[idx]
    if "affix_count" in drop:
        return drop["affix_count"]
    if "affix_count_by_tier" in profile:
        values = profile["affix_count_by_tier"]
        if len(values) != 5:
            raise EquipmentArchetypeError(
                "profile affix_count_by_tier must contain exactly five tier values"
            )
        return values[idx]
    return profile.get("affix_count", 0)


def _source_provenance(source):
    if not source:
        return None
    source_name = source.get("mob_key") or source.get("mob_type")
    provenance = {
        "source_type": source.get("source_type", "mob_drop"),
        "source_name": str(source_name) if source_name else "unknown",
    }
    for key in ("mob_type", "loot_table", "zone_id"):
        value = source.get(key)
        if value:
            provenance[key] = str(value)
    return provenance


def _increase_rarity(rarity, steps):
    if not steps:
        return rarity
    try:
        idx = RARITY_ORDER.index(rarity)
    except ValueError:
        idx = 0
    idx = min(len(RARITY_ORDER) - 1, idx + steps)
    return RARITY_ORDER[idx]


def _apply_affix(item_def, affix_id, tier, idx):
    affix = EQUIPMENT_AFFIXES[affix_id]
    stat_bonus = _tiered_value(affix, "stat_bonuses", idx, {})
    damage_min_bonus = _tiered_value(affix, "damage_min", idx, 0) or 0
    damage_max_bonus = _tiered_value(affix, "damage_max", idx, 0) or 0
    armor_bonus = _tiered_value(affix, "armor_value", idx, 0) or 0

    item_def["stat_bonuses"] = _merge_stat_bonuses(
        item_def.get("stat_bonuses"), stat_bonus
    )
    if damage_min_bonus:
        item_def["damage_min"] = item_def.get("damage_min", 0) + damage_min_bonus
    if damage_max_bonus:
        item_def["damage_max"] = item_def.get("damage_max", 0) + damage_max_bonus
    if armor_bonus:
        item_def["armor_value"] = item_def.get("armor_value", 0) + armor_bonus

    if affix.get("value_multiplier"):
        item_def["value"] = int(round(item_def.get("value", 0) * affix["value_multiplier"]))
    if affix.get("value_bonus"):
        item_def["value"] = item_def.get("value", 0) + affix["value_bonus"]

    item_def["rarity"] = _increase_rarity(item_def.get("rarity", "normal"),
                                          affix.get("rarity_step", 0))

    return {
        "id": affix_id,
        "name": affix["name"],
        "tier": tier,
        "stat_bonuses": stat_bonus,
        "damage_min_bonus": damage_min_bonus,
        "damage_max_bonus": damage_max_bonus,
        "armor_value_bonus": armor_bonus,
    }


def build_equipment_from_archetype(drop, tier, rng=None, source=None):
    """Expand an archetype-backed loot drop into an item_spawner item_def."""
    archetype_id = drop.get("equipment_archetype")
    archetype = EQUIPMENT_ARCHETYPES.get(archetype_id)
    if not archetype:
        raise EquipmentArchetypeError(f"Unknown equipment archetype '{archetype_id}'")

    idx = _tier_index(tier)
    rng = rng or random
    slot = drop.get("equip_slot", archetype["equip_slot"])

    item_def = {
        "item_id": drop["item_id"],
        "key": drop.get("key", archetype.get("key", drop["item_id"])),
        "item_type": "equipment",
        "weight": drop.get("weight", archetype.get("weight", 0.5)),
        "rarity": _tiered_value(drop, "rarity", idx, "normal"),
        "value": _tiered_value(drop, "value", idx, 0),
        "desc": _tiered_value(drop, "desc", idx, ""),
        "equip_slot": slot,
        "scaling_stat": drop.get("scaling_stat", archetype.get("scaling_stat")),
        "material_tier": _tiered_value(drop, "material_tier", idx, None),
    }
    if item_def["material_tier"] is None:
        item_def["material_tier"] = _tiered_value(archetype, "material_tier", idx, 0)

    for stat_key in ("damage_min", "damage_max", "armor_value"):
        value = _tiered_value(drop, stat_key, idx, None)
        if value is None:
            value = _tiered_value(archetype, stat_key, idx, 0)
        if value:
            item_def[stat_key] = value

    item_def["stat_bonuses"] = _merge_stat_bonuses(
        _tiered_value(archetype, "stat_bonuses", idx, {}),
        _tiered_value(drop, "stat_bonuses", idx, {}),
    )

    for field_name in _PASSTHROUGH_KEYS:
        if field_name in drop:
            item_def[field_name] = copy.deepcopy(drop[field_name])

    profile_id = drop.get("affix_profile")
    profile = EQUIPMENT_AFFIX_PROFILES.get(profile_id, {}) if profile_id else {}
    if profile_id and not profile:
        raise EquipmentArchetypeError(f"Unknown equipment affix profile '{profile_id}'")

    affix_count = _affix_count_for_tier(drop, profile, idx) if profile else 0
    candidates = _eligible_affix_weights(profile, archetype, tier, slot) if profile else {}
    affix_ids = _weighted_pick_without_replacement(candidates, affix_count, rng)

    applied_affixes = []
    name_prefixes = []
    desc_fragments = []
    for affix_id in affix_ids:
        affix = EQUIPMENT_AFFIXES[affix_id]
        applied_affixes.append(_apply_affix(item_def, affix_id, tier, idx))
        if affix.get("name_prefix"):
            name_prefixes.append(affix["name_prefix"])
        if affix.get("desc_fragment"):
            desc_fragments.append(affix["desc_fragment"])

    if name_prefixes:
        item_def["key"] = f"{' '.join(name_prefixes)} {item_def['key']}"

    desc_parts = [part for part in (item_def.get("desc"), archetype.get("desc_fragment"))
                  if part]
    desc_parts.extend(desc_fragments)
    item_def["desc"] = " ".join(desc_parts)

    item_def["equipment_archetype"] = archetype_id
    item_def["equipment_affixes"] = applied_affixes
    provenance = _source_provenance(source) or drop.get("drop_provenance")
    if provenance:
        item_def["drop_provenance"] = provenance

    # Avoid leaking authoring-only fields if a caller passed an item_def-like dict.
    for key in _CONFIG_KEYS:
        item_def.pop(key, None)

    return item_def
