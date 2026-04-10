"""
Loot table system for Soravelon.

Drop quality is SKILL-BASED: killer's relevant domain score (0-100) drives
material tier (1-5) via get_material_tier() from zone_scaling.

DO NOT use mob level or zone level for drop quality — the crafting design
explicitly uses killer skill, not level. See soravelon-crafting.md D-34.

LOOT_TABLES is a module-level dict keyed by mob_type. Zones can override
per mob_type via zone_obj.db.loot_table_overrides.

Public API:
    roll_loot(mob, killer) -> list[dict]  — item_def dicts, may be empty
    get_loot_modifiers(mob) -> dict       — rarity modifiers (preserved from stub)
"""

import random


# ---------------------------------------------------------------------------
# Zone scaling imports — wrapped at module level so tests can patch them here.
# Lazy to avoid circular imports at load time.
# ---------------------------------------------------------------------------

def get_zone_obj_for_room(room):
    """Thin wrapper — patchable in tests. Delegates to world.zone_scaling."""
    from world.zone_scaling import get_zone_obj_for_room as _fn
    return _fn(room)


def get_material_tier(skill_score):
    """Thin wrapper — patchable in tests. Delegates to world.zone_scaling."""
    from world.zone_scaling import get_material_tier as _fn
    return _fn(skill_score)


# ---------------------------------------------------------------------------
# Rarity modifiers (stub values — preserved)
# ---------------------------------------------------------------------------

LOOT_TIER_MODIFIERS = {
    "normal":    {"extra_rolls": 0, "tome_chance": 0.00, "ancient_chance": 0.00},
    "magic":     {"extra_rolls": 1, "tome_chance": 0.00, "ancient_chance": 0.00},
    "rare":      {"extra_rolls": 1, "tome_chance": 0.05, "ancient_chance": 0.00},
    "legendary": {"extra_rolls": 2, "tome_chance": 0.15, "ancient_chance": 0.02},
}


def get_loot_modifiers(mob):
    """Return loot modifiers for a mob based on its rarity."""
    rarity = (mob.db.rarity or "normal")
    return LOOT_TIER_MODIFIERS.get(rarity, LOOT_TIER_MODIFIERS["normal"])


# ---------------------------------------------------------------------------
# Loot tables (data-driven, zone-overridable)
# ---------------------------------------------------------------------------

LOOT_TABLES = {
    # Template entry. Real mob_type keys added as content is authored in Phase 7.
    # Each entry: mob_type, relevant_skill, base_drop_chance, drops list.
    # drops list: each entry has item_id, key, item_type, weight,
    #   value_by_tier [t1..t5], rarity_by_tier [t1..t5],
    #   desc_by_tier [t1..t5], weight_in_pool.
    "wolf": {
        "mob_type": "wolf",
        "relevant_skill": "combat",
        "base_drop_chance": 0.70,
        "drops": [
            {
                "item_id": "wolf_pelt",
                "key": "wolf pelt",
                "item_type": "item",
                "weight": 0.8,
                "weight_in_pool": 10,
                "value_by_tier":  [2, 5, 10, 20, 40],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A rough, matted wolf pelt.",
                    "A standard wolf pelt with intact fur.",
                    "A quality wolf pelt, dense and clean.",
                    "A refined wolf pelt with rich, dark color.",
                    "An exceptional wolf pelt, flawless and vibrant.",
                ],
            },
        ],
    },
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _resolve_loot_table(mob):
    """Return loot table entry for mob, checking zone overrides first."""
    mob_type = mob.db.mob_type
    if not mob_type:
        return None

    # Check zone override
    room = mob.location
    if room:
        zone_obj = get_zone_obj_for_room(room)
        if zone_obj and zone_obj.db.loot_table_overrides:
            override = zone_obj.db.loot_table_overrides.get(mob_type)
            if override:
                return override

    return LOOT_TABLES.get(mob_type)


def _pick_drop(drops, count=1):
    """Weighted random selection of `count` drops from drops list."""
    if not drops:
        return []
    total_weight = sum(d.get("weight_in_pool", 1) for d in drops)
    selected = []
    for _ in range(count):
        r = random.uniform(0, total_weight)
        cumulative = 0
        for drop in drops:
            cumulative += drop.get("weight_in_pool", 1)
            if r <= cumulative:
                selected.append(drop)
                break
    return selected


def _build_item_def(drop, tier):
    """Build an item_def dict from a drop entry at a given tier (1-5)."""
    idx = max(0, min(4, tier - 1))
    return {
        "item_id":   drop["item_id"],
        "key":       drop["key"],
        "item_type": drop.get("item_type", "item"),
        "weight":    drop.get("weight", 0.5),
        "rarity":    drop["rarity_by_tier"][idx],
        "value":     drop["value_by_tier"][idx],
        "desc":      drop["desc_by_tier"][idx],
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def roll_loot(mob, killer):
    """
    Resolve loot drops for a mob kill.

    Drop quality is determined by killer's relevant domain skill score
    (D-34 — NOT mob level, NOT zone level).

    Args:
        mob: SoravelonMob that died.
        killer: Character who landed the kill.

    Returns:
        list[dict]: item_def dicts to create via item_spawner. May be empty.
    """
    table = _resolve_loot_table(mob)
    if not table:
        return []

    # Base drop chance
    if random.random() > table.get("base_drop_chance", 0.7):
        return []

    # Skill-based tier (D-34 — skill score, not level)
    relevant_skill = table.get("relevant_skill", "combat")
    domain_scores = (killer.db.domain_scores or {}) if killer else {}
    skill_score = domain_scores.get(relevant_skill, 0)

    tier = get_material_tier(skill_score)

    # Base roll: 1 drop
    drops = table.get("drops", [])
    selected = _pick_drop(drops, count=1)

    # Extra rolls from rarity modifier
    rarity_mods = get_loot_modifiers(mob)
    extra = rarity_mods.get("extra_rolls", 0)
    if extra:
        selected.extend(_pick_drop(drops, count=extra))

    return [_build_item_def(drop, tier) for drop in selected]
