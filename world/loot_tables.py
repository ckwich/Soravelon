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
    # --- Reth Foothills loot tables (07-06) ---
    "rock_troll": {
        "mob_type": "rock_troll",
        "relevant_skill": "combat",
        "base_drop_chance": 0.75,
        "drops": [
            {
                "item_id": "troll_hide",
                "key": "troll hide",
                "item_type": "item",
                "weight": 1.5,
                "weight_in_pool": 10,
                "value_by_tier":  [5, 12, 25, 50, 100],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A rough slab of troll hide, stinking and coarse.",
                    "A section of troll hide, thick and durable.",
                    "A quality troll hide, dense as boiled leather.",
                    "A superior troll hide with natural stone-grey sheen.",
                    "An exceptional troll hide, nearly impervious to cuts.",
                ],
            },
            {
                "item_id": "troll_tooth",
                "key": "troll tooth",
                "item_type": "item",
                "weight": 0.3,
                "weight_in_pool": 6,
                "value_by_tier":  [3, 8, 16, 32, 65],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A cracked, yellowed troll tooth.",
                    "A troll tooth, chipped but solid.",
                    "A troll tooth in good condition, sharp and heavy.",
                    "A pristine troll tusk with a faint mineral gleam.",
                    "A flawless troll tusk, hard as iron.",
                ],
            },
        ],
    },
    "mountain_cat": {
        "mob_type": "mountain_cat",
        "relevant_skill": "combat",
        "base_drop_chance": 0.70,
        "drops": [
            {
                "item_id": "mountain_cat_pelt",
                "key": "mountain cat pelt",
                "item_type": "item",
                "weight": 0.6,
                "weight_in_pool": 10,
                "value_by_tier":  [4, 10, 20, 40, 80],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A torn mountain cat pelt with matted fur.",
                    "A mountain cat pelt with tawny-grey markings.",
                    "A quality mountain cat pelt, soft and supple.",
                    "A fine mountain cat pelt with striking patterns.",
                    "A flawless mountain cat pelt, luxuriously soft.",
                ],
            },
            {
                "item_id": "mountain_cat_claw",
                "key": "mountain cat claw",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 5,
                "value_by_tier":  [2, 6, 12, 24, 50],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A chipped mountain cat claw.",
                    "A mountain cat claw, curved and sharp.",
                    "A keen mountain cat claw with intact sheath.",
                    "A razor-sharp mountain cat talon.",
                    "A pristine mountain cat talon, wickedly curved.",
                ],
            },
        ],
    },
    "cave_spider": {
        "mob_type": "cave_spider",
        "relevant_skill": "combat",
        "base_drop_chance": 0.65,
        "drops": [
            {
                "item_id": "spider_silk_thread",
                "key": "spider silk thread",
                "item_type": "item",
                "weight": 0.2,
                "weight_in_pool": 10,
                "value_by_tier":  [2, 5, 10, 22, 45],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A tangled wad of sticky spider silk.",
                    "A bundle of spider silk, partially cleaned.",
                    "A spool of cave spider silk, surprisingly strong.",
                    "Fine-spun spider silk thread, stronger than cord.",
                    "Exceptional spider silk, translucent and unbreakable.",
                ],
            },
            {
                "item_id": "spider_venom_sac",
                "key": "spider venom sac",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 5,
                "value_by_tier":  [3, 8, 15, 30, 60],
                "rarity_by_tier": ["normal", "normal", "magic", "magic", "rare"],
                "desc_by_tier": [
                    "A ruptured venom sac, mostly empty.",
                    "A spider venom sac, partially intact.",
                    "An intact spider venom sac, contents potent.",
                    "A full spider venom sac, carefully extracted.",
                    "A pristine venom sac, the contents virtually pure.",
                ],
            },
        ],
    },
    "stone_golem_fragment": {
        "mob_type": "stone_golem_fragment",
        "relevant_skill": "combat",
        "base_drop_chance": 0.80,
        "drops": [
            {
                "item_id": "golem_stone_shard",
                "key": "golem stone shard",
                "item_type": "item",
                "weight": 1.0,
                "weight_in_pool": 10,
                "value_by_tier":  [6, 15, 30, 60, 120],
                "rarity_by_tier": ["normal", "normal", "magic", "magic", "rare"],
                "desc_by_tier": [
                    "A rough chunk of golem stone, cracked.",
                    "A golem stone fragment with faint carvings.",
                    "A golem stone shard with intact rune-work.",
                    "A resonant golem stone, warm to the touch.",
                    "A perfect golem core shard, humming with residual energy.",
                ],
            },
        ],
    },
    "reth_eagle": {
        "mob_type": "reth_eagle",
        "relevant_skill": "combat",
        "base_drop_chance": 0.65,
        "drops": [
            {
                "item_id": "eagle_feather",
                "key": "Reth eagle feather",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 10,
                "value_by_tier":  [2, 5, 12, 25, 50],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A battered eagle feather, bent and dull.",
                    "A Reth eagle feather, brown and tawny.",
                    "A fine eagle feather with rich coloring.",
                    "A magnificent eagle plume, two feet long.",
                    "A flawless Reth eagle plume, iridescent at the tip.",
                ],
            },
            {
                "item_id": "eagle_talon",
                "key": "Reth eagle talon",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 4,
                "value_by_tier":  [3, 7, 14, 28, 55],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A cracked eagle talon.",
                    "A Reth eagle talon, curved and sharp.",
                    "A keen eagle talon with a wicked curve.",
                    "A razor-edged eagle talon, polished dark.",
                    "A perfect eagle talon, hard as forged steel.",
                ],
            },
        ],
    },
    "grandmother_spider": {
        "mob_type": "grandmother_spider",
        "relevant_skill": "combat",
        "base_drop_chance": 1.0,
        "drops": [
            {
                "item_id": "grandmother_silk_bolt",
                "key": "bolt of ancient silk",
                "item_type": "item",
                "weight": 0.5,
                "weight_in_pool": 8,
                "value_by_tier":  [20, 50, 100, 200, 400],
                "rarity_by_tier": ["magic", "magic", "rare", "rare", "legendary"],
                "desc_by_tier": [
                    "A bolt of ancient spider silk, centuries old.",
                    "A bolt of Grandmother's silk, strong as steel.",
                    "A rare bolt of Grandmother's silk, luminous.",
                    "An extraordinary bolt of ancient silk, nearly alive.",
                    "A legendary bolt of Grandmother's silk, thrumming with power.",
                ],
            },
            {
                "item_id": "grandmother_fang",
                "key": "Grandmother's fang",
                "item_type": "item",
                "weight": 0.3,
                "weight_in_pool": 4,
                "value_by_tier":  [15, 40, 80, 160, 320],
                "rarity_by_tier": ["magic", "magic", "rare", "rare", "legendary"],
                "desc_by_tier": [
                    "A massive spider fang, dark and curved.",
                    "Grandmother Spider's fang, dripping with venom.",
                    "A rare fang from the ancient spider, pulsing faintly.",
                    "An extraordinary fang, the venom still potent.",
                    "A legendary fang of Grandmother Spider, warm and alive.",
                ],
            },
            {
                "item_id": "grandmother_eye",
                "key": "Grandmother's eye",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 2,
                "value_by_tier":  [25, 60, 120, 250, 500],
                "rarity_by_tier": ["rare", "rare", "rare", "legendary", "legendary"],
                "desc_by_tier": [
                    "A glassy spider eye, still reflecting light.",
                    "One of Grandmother's eyes, unnervingly aware.",
                    "A rare specimen -- the eye seems to watch you.",
                    "An extraordinary eye that sees in all spectra.",
                    "A legendary eye of Grandmother Spider, omniscient and terrible.",
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
