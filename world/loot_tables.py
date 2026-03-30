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
    # --- Ashreach Plains loot tables (07-05) ---
    "ash_wolf": {
        "mob_type": "ash_wolf",
        "relevant_skill": "combat",
        "base_drop_chance": 0.70,
        "drops": [
            {
                "item_id": "ash_wolf_pelt",
                "key": "ash wolf pelt",
                "item_type": "item",
                "weight": 0.8,
                "weight_in_pool": 10,
                "value_by_tier":  [3, 6, 12, 24, 48],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A rough pelt of ash-grey fur, torn in places.",
                    "A standard ash wolf pelt with intact fur.",
                    "A quality ash wolf pelt, dense and warm.",
                    "A fine ash wolf pelt with a silvery sheen.",
                    "A flawless ash wolf pelt, soft as silk.",
                ],
            },
            {
                "item_id": "ash_wolf_fang",
                "key": "wolf fang",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 6,
                "value_by_tier":  [1, 3, 7, 15, 30],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A cracked wolf fang, barely usable.",
                    "A wolf fang, slightly yellowed.",
                    "A clean, sharp wolf fang.",
                    "A large wolf fang, perfect for crafting.",
                    "A pristine wolf fang with an unusual dark sheen.",
                ],
            },
            {
                "item_id": "raw_wolf_meat",
                "key": "raw wolf meat",
                "item_type": "item",
                "weight": 1.0,
                "weight_in_pool": 8,
                "value_by_tier":  [1, 2, 4, 8, 16],
                "rarity_by_tier": ["normal", "normal", "normal", "normal", "normal"],
                "desc_by_tier": [
                    "Stringy, tough wolf meat. Barely edible.",
                    "A cut of wolf meat, gamey but serviceable.",
                    "A decent cut of wolf haunch.",
                    "Quality wolf meat, lean and red.",
                    "Prime wolf loin, surprisingly tender.",
                ],
            },
        ],
    },
    "plains_viper": {
        "mob_type": "plains_viper",
        "relevant_skill": "combat",
        "base_drop_chance": 0.65,
        "drops": [
            {
                "item_id": "venom_sac",
                "key": "venom sac",
                "item_type": "item",
                "weight": 0.2,
                "weight_in_pool": 7,
                "value_by_tier":  [4, 8, 16, 32, 64],
                "rarity_by_tier": ["normal", "normal", "magic", "magic", "rare"],
                "desc_by_tier": [
                    "A small, partially ruptured venom sac.",
                    "A venom sac, still moist with toxin.",
                    "A full venom sac, carefully extracted.",
                    "A potent venom sac, glowing faintly green.",
                    "A pristine venom sac of extraordinary potency.",
                ],
            },
            {
                "item_id": "snake_skin",
                "key": "snake skin",
                "item_type": "item",
                "weight": 0.3,
                "weight_in_pool": 10,
                "value_by_tier":  [2, 4, 8, 16, 32],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A torn section of viper skin.",
                    "A shed viper skin in fair condition.",
                    "A quality snake skin with intact scales.",
                    "A supple snake skin with a golden pattern.",
                    "A flawless snake skin, scales shimmering.",
                ],
            },
        ],
    },
    "ashreach_bandit": {
        "mob_type": "ashreach_bandit",
        "relevant_skill": "subterfuge",
        "base_drop_chance": 0.75,
        "drops": [
            {
                "item_id": "bandit_coins",
                "key": "handful of coins",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 12,
                "value_by_tier":  [3, 7, 14, 28, 56],
                "rarity_by_tier": ["normal", "normal", "normal", "normal", "normal"],
                "desc_by_tier": [
                    "A few bent copper coins.",
                    "A small handful of mixed coins.",
                    "A decent pile of copper and silver.",
                    "A fat purse of silver coins.",
                    "A heavy pouch of silver and gold.",
                ],
            },
            {
                "item_id": "iron_shortsword",
                "key": "iron shortsword",
                "item_type": "equipment",
                "weight": 1.5,
                "weight_in_pool": 4,
                "value_by_tier":  [5, 10, 20, 40, 80],
                "rarity_by_tier": ["normal", "normal", "magic", "magic", "rare"],
                "desc_by_tier": [
                    "A battered iron shortsword with a notched edge.",
                    "A serviceable iron shortsword.",
                    "A well-maintained iron shortsword.",
                    "A sharp iron shortsword with a leather grip.",
                    "A finely balanced iron shortsword.",
                ],
            },
            {
                "item_id": "linen_bandage",
                "key": "linen bandage",
                "item_type": "item",
                "weight": 0.2,
                "weight_in_pool": 8,
                "value_by_tier":  [1, 2, 4, 8, 16],
                "rarity_by_tier": ["normal", "normal", "normal", "normal", "normal"],
                "desc_by_tier": [
                    "A dirty strip of linen, barely sterile.",
                    "A basic linen bandage, slightly stained.",
                    "A clean linen bandage.",
                    "A quality linen bandage, neatly rolled.",
                    "A fine linen bandage with herbal salve.",
                ],
            },
        ],
    },
    "dust_beetle": {
        "mob_type": "dust_beetle",
        "relevant_skill": "naturalism",
        "base_drop_chance": 0.60,
        "drops": [
            {
                "item_id": "chitin_plate",
                "key": "chitin plate",
                "item_type": "item",
                "weight": 0.5,
                "weight_in_pool": 10,
                "value_by_tier":  [1, 3, 6, 12, 24],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A cracked piece of beetle carapace.",
                    "A section of beetle chitin, slightly chipped.",
                    "A solid chitin plate with a dull sheen.",
                    "A sturdy chitin plate, ash-grey and tough.",
                    "A perfect chitin plate, hard as iron.",
                ],
            },
            {
                "item_id": "beetle_ichor",
                "key": "beetle ichor",
                "item_type": "item",
                "weight": 0.3,
                "weight_in_pool": 6,
                "value_by_tier":  [1, 2, 5, 10, 20],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A smear of cloudy beetle fluid.",
                    "A small vial of beetle ichor.",
                    "A vial of clear beetle ichor.",
                    "Concentrated beetle ichor with a sharp smell.",
                    "Potent beetle ichor, practically luminous.",
                ],
            },
        ],
    },
    "steppe_hawk": {
        "mob_type": "steppe_hawk",
        "relevant_skill": "combat",
        "base_drop_chance": 0.60,
        "drops": [
            {
                "item_id": "hawk_feathers",
                "key": "hawk feathers",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 10,
                "value_by_tier":  [1, 3, 6, 12, 24],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A handful of broken feathers.",
                    "Several steppe hawk feathers, slightly bent.",
                    "Clean hawk feathers in good condition.",
                    "Long, perfect hawk feathers with dark bands.",
                    "Pristine hawk feathers, dark as midnight.",
                ],
            },
            {
                "item_id": "hawk_talons",
                "key": "hawk talons",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 5,
                "value_by_tier":  [2, 4, 8, 16, 32],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "Dull, chipped hawk talons.",
                    "A pair of hawk talons, serviceable.",
                    "Sharp hawk talons, still keen.",
                    "Razor-sharp hawk talons, perfect for fletching.",
                    "Pristine talons with an unnatural sharpness.",
                ],
            },
        ],
    },
    "alpha_ash_wolf": {
        "mob_type": "alpha_ash_wolf",
        "relevant_skill": "combat",
        "base_drop_chance": 1.0,
        "drops": [
            {
                "item_id": "alpha_wolf_pelt",
                "key": "alpha ash wolf pelt",
                "item_type": "item",
                "weight": 1.2,
                "weight_in_pool": 6,
                "value_by_tier":  [15, 30, 60, 120, 240],
                "rarity_by_tier": ["magic", "magic", "rare", "rare", "legendary"],
                "desc_by_tier": [
                    "A scarred but impressive wolf pelt, dark as soot.",
                    "A large dark wolf pelt with thick, coarse fur.",
                    "A magnificent dark pelt with a silver undercoat.",
                    "A legendary alpha pelt, nearly black, shot with silver.",
                    "The pelt of the Ashreach Alpha -- unmistakable and priceless.",
                ],
            },
            {
                "item_id": "alpha_fang_necklace",
                "key": "alpha fang necklace",
                "item_type": "equipment",
                "weight": 0.2,
                "weight_in_pool": 3,
                "value_by_tier":  [20, 40, 80, 160, 320],
                "rarity_by_tier": ["magic", "rare", "rare", "legendary", "legendary"],
                "desc_by_tier": [
                    "A cord strung with the Alpha's broken fangs.",
                    "A necklace of polished alpha wolf fangs.",
                    "A striking necklace of dark, gleaming fangs.",
                    "A powerful necklace radiating primal menace.",
                    "The Alpha's Maw -- every fang perfect, thrumming with presence.",
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
