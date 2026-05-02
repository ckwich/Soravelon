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
    get_loot_modifiers(mob) -> dict       — rarity modifiers
"""

import copy
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
# Rarity modifiers
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
    # --- Stormhaven Coast mob loot (07-08) ---
    "shore_crab": {
        "mob_type": "shore_crab",
        "relevant_skill": "combat",
        "base_drop_chance": 0.60,
        "drops": [
            {
                "item_id": "crab_shell",
                "key": "crab shell",
                "item_type": "item",
                "weight": 0.3,
                "weight_in_pool": 10,
                "value_by_tier":  [1, 3, 6, 12, 25],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A cracked crab shell. Barely useful.",
                    "A sturdy crab shell, intact enough for crafting.",
                    "A quality crab shell with good coloring.",
                    "A thick, iridescent crab shell.",
                    "A flawless crab shell, impossibly hard and gleaming.",
                ],
            },
            {
                "item_id": "crab_claw",
                "key": "crab claw",
                "item_type": "item",
                "weight": 0.4,
                "weight_in_pool": 5,
                "value_by_tier":  [1, 2, 5, 10, 20],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A small crab claw. Could be ground into powder.",
                    "A decent crab claw, suitable for alchemy.",
                    "A large crab claw with sharp edges.",
                    "A massive claw, dense and razor-edged.",
                    "An enormous claw that could serve as a weapon.",
                ],
            },
        ],
    },
    "sea_serpent": {
        "mob_type": "sea_serpent",
        "relevant_skill": "combat",
        "base_drop_chance": 0.85,
        "drops": [
            {
                "item_id": "serpent_scale",
                "key": "sea serpent scale",
                "item_type": "item",
                "weight": 0.2,
                "weight_in_pool": 8,
                "value_by_tier":  [5, 12, 25, 50, 100],
                "rarity_by_tier": ["normal", "normal", "magic", "rare", "rare"],
                "desc_by_tier": [
                    "A dull serpent scale, flaking at the edges.",
                    "A sea serpent scale with a metallic sheen.",
                    "A dense, iron-colored serpent scale.",
                    "A pristine scale that shimmers with deep-water iridescence.",
                    "A perfect serpent scale, hard as steel and beautiful.",
                ],
            },
            {
                "item_id": "serpent_venom_sac",
                "key": "serpent venom sac",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 4,
                "value_by_tier":  [8, 18, 35, 70, 140],
                "rarity_by_tier": ["normal", "normal", "magic", "rare", "legendary"],
                "desc_by_tier": [
                    "A ruptured venom sac, mostly empty.",
                    "A venom sac with some potency remaining.",
                    "An intact venom sac, potent and dangerous.",
                    "A swollen venom sac radiating heat.",
                    "A perfectly preserved venom sac of extraordinary potency.",
                ],
            },
            {
                "item_id": "serpent_fang",
                "key": "sea serpent fang",
                "item_type": "item",
                "weight": 0.3,
                "weight_in_pool": 6,
                "value_by_tier":  [4, 10, 20, 40, 80],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A chipped serpent fang.",
                    "A serpent fang, yellowed but intact.",
                    "A sharp serpent fang with traces of venom.",
                    "A gleaming fang as long as a dagger.",
                    "A massive, venom-dripping fang of extraordinary size.",
                ],
            },
        ],
    },
    "coastal_raider": {
        "mob_type": "coastal_raider",
        "relevant_skill": "combat",
        "base_drop_chance": 0.75,
        "drops": [
            {
                "item_id": "raider_cutlass",
                "key": "raider's cutlass",
                "item_type": "equipment",
                "equip_slot": "main_hand",
                "scaling_stat": "agility",
                "material_tier_by_tier": [1, 1, 2, 2, 3],
                "damage_min_by_tier": [7, 9, 11, 13, 15],
                "damage_max_by_tier": [13, 15, 18, 21, 24],
                "stat_bonuses_by_tier": [
                    {"agility": 1},
                    {"agility": 1},
                    {"agility": 2},
                    {"agility": 2},
                    {"agility": 3},
                ],
                "weight": 1.5,
                "weight_in_pool": 4,
                "value_by_tier":  [8, 18, 35, 70, 140],
                "rarity_by_tier": ["normal", "normal", "magic", "rare", "rare"],
                "desc_by_tier": [
                    "A battered cutlass, nicked and salt-pitted.",
                    "A serviceable cutlass with a worn leather grip.",
                    "A well-maintained cutlass with good balance.",
                    "A fine cutlass, oiled and deadly sharp.",
                    "An exceptional cutlass, light and perfectly balanced.",
                ],
            },
            {
                "item_id": "raider_coin_pouch",
                "key": "raider's coin pouch",
                "item_type": "item",
                "weight": 0.2,
                "weight_in_pool": 8,
                "value_by_tier":  [3, 8, 15, 30, 60],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A nearly empty coin pouch with a few coppers.",
                    "A leather pouch with some mixed coins.",
                    "A pouch jingling with silver.",
                    "A heavy pouch of assorted currency.",
                    "A bulging pouch of gold and foreign coins.",
                ],
            },
            {
                "item_id": "salt_stained_leather",
                "key": "salt-stained leather",
                "item_type": "item",
                "weight": 0.8,
                "weight_in_pool": 6,
                "value_by_tier":  [2, 5, 10, 20, 40],
                "rarity_by_tier": ["normal", "normal", "normal", "normal", "magic"],
                "desc_by_tier": [
                    "Scraps of salt-ruined leather.",
                    "Pieces of tough, salt-cured leather.",
                    "Quality leather hardened by salt exposure.",
                    "Dense, waterproof leather of raider make.",
                    "Supple, salt-treated leather of exceptional quality.",
                ],
            },
        ],
    },
    "cliff_harpy": {
        "mob_type": "cliff_harpy",
        "relevant_skill": "combat",
        "base_drop_chance": 0.70,
        "drops": [
            {
                "item_id": "harpy_feather",
                "key": "harpy feather",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 10,
                "value_by_tier":  [2, 5, 10, 20, 40],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A ragged grey feather, dirty and bent.",
                    "A long harpy feather with a grey sheen.",
                    "A clean harpy feather, surprisingly soft.",
                    "A storm-grey feather crackling with static.",
                    "A perfect feather that hums faintly in the wind.",
                ],
            },
            {
                "item_id": "harpy_talon",
                "key": "harpy talon",
                "item_type": "item",
                "weight": 0.2,
                "weight_in_pool": 6,
                "value_by_tier":  [3, 7, 14, 28, 55],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A broken harpy talon.",
                    "A harpy talon, curved and sharp.",
                    "A large talon with dried blood still visible.",
                    "A wickedly curved talon, razor-sharp.",
                    "A massive talon, dense as iron and gleaming.",
                ],
            },
        ],
    },
    "salt_lurker": {
        "mob_type": "salt_lurker",
        "relevant_skill": "combat",
        "base_drop_chance": 0.65,
        "drops": [
            {
                "item_id": "salt_crystal",
                "key": "crystallized salt deposit",
                "item_type": "item",
                "weight": 0.5,
                "weight_in_pool": 8,
                "value_by_tier":  [2, 5, 10, 20, 40],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A chunk of impure salt crystal.",
                    "A salt crystal with decent clarity.",
                    "A large, translucent salt crystal.",
                    "A perfectly formed salt crystal with inner glow.",
                    "An enormous crystal of impossible purity.",
                ],
            },
            {
                "item_id": "lurker_brine",
                "key": "lurker brine",
                "item_type": "item",
                "weight": 0.3,
                "weight_in_pool": 6,
                "value_by_tier":  [3, 7, 15, 30, 60],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A vial of weak, brackish brine.",
                    "A vial of concentrated brine.",
                    "A vial of potent lurker brine.",
                    "A flask of hyper-concentrated brine that burns skin.",
                    "A sealed flask of pure lurker essence.",
                ],
            },
        ],
    },
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
                "equip_slot": "main_hand",
                "scaling_stat": "agility",
                "material_tier_by_tier": [1, 1, 1, 2, 2],
                "damage_min_by_tier": [6, 7, 9, 11, 13],
                "damage_max_by_tier": [12, 14, 16, 19, 22],
                "stat_bonuses_by_tier": [
                    {"agility": 1},
                    {"agility": 1},
                    {"agility": 2},
                    {"agility": 2},
                    {"agility": 3},
                ],
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
                "equip_slot": "amulet",
                "material_tier_by_tier": [2, 2, 3, 3, 3],
                "stat_bonuses_by_tier": [
                    {"presence": 1},
                    {"presence": 1, "resonance": 1},
                    {"presence": 2, "resonance": 1},
                    {"presence": 2, "resonance": 2},
                    {"presence": 3, "resonance": 2},
                ],
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
    # --- Cantera Edge loot tables (07-07) ---
    "forest_spider": {
        "mob_type": "forest_spider",
        "relevant_skill": "combat",
        "base_drop_chance": 0.65,
        "drops": [
            {
                "item_id": "spider_fang",
                "key": "spider fang",
                "item_type": "item",
                "weight": 0.3,
                "weight_in_pool": 8,
                "value_by_tier":  [2, 4, 8, 16, 32],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A cracked spider fang, still dripping venom.",
                    "A spider fang with a sharp, clean point.",
                    "A large spider fang, venom sac intact.",
                    "A pristine fang with potent venom residue.",
                    "An enormous fang from an ancient spider, pulsing with toxin.",
                ],
            },
            {
                "item_id": "raw_spider_silk",
                "key": "raw spider silk",
                "item_type": "item",
                "weight": 0.2,
                "weight_in_pool": 6,
                "value_by_tier":  [3, 6, 12, 24, 48],
                "rarity_by_tier": ["normal", "normal", "magic", "magic", "rare"],
                "desc_by_tier": [
                    "A tangled clump of sticky spider silk.",
                    "A skein of spider silk, roughly cleaned.",
                    "Clean spider silk, surprisingly strong.",
                    "Fine spider silk with an iridescent sheen.",
                    "Flawless spider silk, stronger than steel wire.",
                ],
            },
        ],
    },
    "wild_boar": {
        "mob_type": "wild_boar",
        "relevant_skill": "combat",
        "base_drop_chance": 0.70,
        "drops": [
            {
                "item_id": "boar_tusk",
                "key": "boar tusk",
                "item_type": "item",
                "weight": 0.4,
                "weight_in_pool": 8,
                "value_by_tier":  [2, 5, 10, 20, 40],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A chipped boar tusk, yellowed with age.",
                    "A solid boar tusk with a sharp curve.",
                    "A large boar tusk, polished by use.",
                    "A massive tusk from a veteran boar.",
                    "A perfect ivory tusk, dense and gleaming.",
                ],
            },
            {
                "item_id": "boar_hide",
                "key": "boar hide",
                "item_type": "item",
                "weight": 1.0,
                "weight_in_pool": 6,
                "value_by_tier":  [3, 6, 12, 24, 48],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A rough boar hide, scarred and stiff.",
                    "A serviceable boar hide with thick bristle.",
                    "A quality hide, dense and pliable.",
                    "A prime boar hide, supple and unmarred.",
                    "An extraordinary hide from an ancient boar.",
                ],
            },
        ],
    },
    "cantera_wolf": {
        "mob_type": "cantera_wolf",
        "relevant_skill": "combat",
        "base_drop_chance": 0.70,
        "drops": [
            {
                "item_id": "cantera_wolf_pelt",
                "key": "cantera wolf pelt",
                "item_type": "item",
                "weight": 0.8,
                "weight_in_pool": 10,
                "value_by_tier":  [3, 6, 12, 24, 48],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A dark wolf pelt with amber-tipped fur.",
                    "A cantera wolf pelt, thick and well-furred.",
                    "A quality pelt with distinctive amber markings.",
                    "A prime cantera wolf pelt with luminous fur tips.",
                    "A flawless pelt that seems to glow faintly in shadow.",
                ],
            },
        ],
    },
    "vine_creeper": {
        "mob_type": "vine_creeper",
        "relevant_skill": "combat",
        "base_drop_chance": 0.55,
        "drops": [
            {
                "item_id": "thorn_vine",
                "key": "thorn vine",
                "item_type": "item",
                "weight": 0.3,
                "weight_in_pool": 8,
                "value_by_tier":  [1, 3, 6, 12, 24],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A dried thorn vine, brittle and sharp.",
                    "A flexible thorn vine, still green.",
                    "A strong thorn vine with intact barbs.",
                    "A resilient vine that coils on its own.",
                    "A living vine fragment, thorns gleaming.",
                ],
            },
            {
                "item_id": "creeper_sap",
                "key": "creeper sap",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 4,
                "value_by_tier":  [2, 5, 10, 20, 40],
                "rarity_by_tier": ["normal", "normal", "magic", "magic", "rare"],
                "desc_by_tier": [
                    "A vial of murky green sap.",
                    "A vial of creeper sap, slightly viscous.",
                    "Clear creeper sap with a sharp herbal scent.",
                    "Concentrated creeper sap, potent and pure.",
                    "Distilled creeper essence, almost luminous.",
                ],
            },
        ],
    },
    "forest_bandit": {
        "mob_type": "forest_bandit",
        "relevant_skill": "combat",
        "base_drop_chance": 0.75,
        "drops": [
            {
                "item_id": "bandit_coin_pouch",
                "key": "coin pouch",
                "item_type": "item",
                "weight": 0.2,
                "weight_in_pool": 8,
                "value_by_tier":  [5, 10, 20, 40, 80],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A small pouch with a few tarnished coins.",
                    "A leather pouch jingling with mixed coin.",
                    "A well-stuffed pouch of silver and copper.",
                    "A heavy pouch of assorted currency.",
                    "A fat purse bulging with gold and silver.",
                ],
            },
            {
                "item_id": "bandit_lockpick",
                "key": "crude lockpick",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 3,
                "value_by_tier":  [2, 4, 8, 16, 32],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A bent wire shaped into a crude lockpick.",
                    "A basic lockpick, roughly fashioned.",
                    "A serviceable lockpick with a comfortable grip.",
                    "A well-made lockpick of tempered steel.",
                    "A masterwork lockpick, nearly invisible.",
                ],
            },
        ],
    },
    # --- Cantera Edge L1 corrupted mob loot (07-07) ---
    "corrupted_treant": {
        "mob_type": "corrupted_treant",
        "relevant_skill": "combat",
        "base_drop_chance": 0.80,
        "drops": [
            {
                "item_id": "corrupted_heartwood",
                "key": "corrupted heartwood",
                "item_type": "item",
                "weight": 0.5,
                "weight_in_pool": 8,
                "value_by_tier":  [5, 10, 20, 40, 80],
                "rarity_by_tier": ["normal", "magic", "magic", "rare", "rare"],
                "desc_by_tier": [
                    "A chunk of blackened wood veined with amber.",
                    "Corrupted heartwood, warm to the touch.",
                    "Dense heartwood pulsing with faint energy.",
                    "Resonant heartwood that hums when held.",
                    "Living heartwood that glows from within.",
                ],
            },
            {
                "item_id": "burning_sap",
                "key": "burning sap",
                "item_type": "item",
                "weight": 0.2,
                "weight_in_pool": 5,
                "value_by_tier":  [4, 8, 16, 32, 64],
                "rarity_by_tier": ["normal", "magic", "magic", "rare", "legendary"],
                "desc_by_tier": [
                    "A vial of amber sap that is warm to hold.",
                    "Burning sap sealed in a heat-resistant vial.",
                    "Concentrated burning sap, glowing steadily.",
                    "Pure burning sap, painfully hot through the vial.",
                    "Liquid resonance in sap form, nearly alive.",
                ],
            },
        ],
    },
    "void_wisp": {
        "mob_type": "void_wisp",
        "relevant_skill": "combat",
        "base_drop_chance": 0.60,
        "drops": [
            {
                "item_id": "resonance_mote",
                "key": "resonance mote",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 10,
                "value_by_tier":  [5, 10, 20, 40, 80],
                "rarity_by_tier": ["magic", "magic", "rare", "rare", "legendary"],
                "desc_by_tier": [
                    "A flickering mote of unstable energy.",
                    "A stabilized resonance mote, humming softly.",
                    "A bright mote that pulses in a steady rhythm.",
                    "A potent mote radiating visible energy.",
                    "A brilliant mote containing a fragment of pure resonance.",
                ],
            },
        ],
    },
    "blighted_stag": {
        "mob_type": "blighted_stag",
        "relevant_skill": "combat",
        "base_drop_chance": 0.70,
        "drops": [
            {
                "item_id": "crystal_antler",
                "key": "crystal antler",
                "item_type": "item",
                "weight": 0.4,
                "weight_in_pool": 8,
                "value_by_tier":  [4, 8, 16, 32, 64],
                "rarity_by_tier": ["normal", "magic", "magic", "rare", "rare"],
                "desc_by_tier": [
                    "A broken antler tip, partially crystallized.",
                    "A crystal antler fragment, amber-hued.",
                    "A complete crystal antler, glowing at the tips.",
                    "A pristine crystal antler resonating with energy.",
                    "A perfect crystal antler, singing with harmonics.",
                ],
            },
            {
                "item_id": "blighted_hide",
                "key": "blighted hide",
                "item_type": "item",
                "weight": 0.6,
                "weight_in_pool": 6,
                "value_by_tier":  [3, 6, 12, 24, 48],
                "rarity_by_tier": ["normal", "normal", "magic", "magic", "rare"],
                "desc_by_tier": [
                    "A patch of mottled, luminous hide.",
                    "Blighted stag hide, grey patches glowing faintly.",
                    "Quality blighted hide with full bioluminescence.",
                    "Prime blighted hide, patterns shifting in the light.",
                    "Extraordinary blighted hide, alive with inner light.",
                ],
            },
        ],
    },
    # --- Cantera Edge named mob loot (07-07) ---
    "heartwood_ancient": {
        "mob_type": "heartwood_ancient",
        "relevant_skill": "combat",
        "base_drop_chance": 1.0,
        "drops": [
            {
                "item_id": "heartwood_core",
                "key": "heartwood core",
                "item_type": "item",
                "weight": 1.0,
                "weight_in_pool": 10,
                "value_by_tier":  [15, 30, 60, 120, 240],
                "rarity_by_tier": ["magic", "rare", "rare", "legendary", "legendary"],
                "desc_by_tier": [
                    "A dense core of amber heartwood, warm and heavy.",
                    "An ancient heartwood core, pulsing with stored energy.",
                    "A resonant heartwood core, centuries of power within.",
                    "A living heartwood core, the tree's essence distilled.",
                    "The Ancient's heartwood -- millennia of accumulated resonance.",
                ],
            },
            {
                "item_id": "ancient_bark_plate",
                "key": "ancient bark plate",
                "item_type": "item",
                "weight": 1.5,
                "weight_in_pool": 6,
                "value_by_tier":  [10, 20, 40, 80, 160],
                "rarity_by_tier": ["normal", "magic", "rare", "rare", "legendary"],
                "desc_by_tier": [
                    "A thick plate of ancient bark, dense as stone.",
                    "An ancient bark plate with natural reinforcement.",
                    "A prime bark plate, centuries of growth compressed.",
                    "A legendary bark plate, harder than forged steel.",
                    "Living bark from the Ancient itself, still growing.",
                ],
            },
        ],
    },

    # --- Reth Foothills: mountain_troll (elite) ---
    "mountain_troll": {
        "mob_type": "mountain_troll",
        "relevant_skill": "combat",
        "base_drop_chance": 0.85,
        "drops": [
            {
                "item_id": "mountain_troll_hide",
                "key": "mountain troll hide",
                "item_type": "item",
                "weight": 2.0,
                "weight_in_pool": 8,
                "value_by_tier":  [8, 18, 35, 70, 140],
                "rarity_by_tier": ["normal", "normal", "magic", "magic", "rare"],
                "desc_by_tier": [
                    "A slab of blue-grey troll hide, tough but poorly cut.",
                    "A section of mountain troll hide, dense and cold to the touch.",
                    "Quality mountain troll hide with natural frost-resistance.",
                    "Superior hide with a faint blue sheen — dense as boiled plate.",
                    "Flawless mountain troll hide, nearly impervious. Frost clings to it.",
                ],
            },
            {
                "item_id": "frost_shard",
                "key": "frost shard",
                "item_type": "item",
                "weight": 0.3,
                "weight_in_pool": 5,
                "value_by_tier":  [5, 12, 25, 50, 100],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A cloudy sliver of ice that refuses to melt.",
                    "A translucent frost shard, cold enough to numb fingers.",
                    "A clear frost shard that radiates chill in a small radius.",
                    "A brilliant frost shard — the air crackles with cold near it.",
                    "A perfect frost shard, ancient ice compressed to crystal hardness.",
                ],
            },
            {
                "item_id": "mountain_troll_tusk",
                "key": "mountain troll tusk",
                "item_type": "item",
                "weight": 0.5,
                "weight_in_pool": 6,
                "value_by_tier":  [4, 10, 20, 40, 80],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A broken troll tusk, cracked from the cold.",
                    "A thick tusk with faint blue veining.",
                    "A solid mountain troll tusk, heavy as a mace head.",
                    "A pristine tusk with mineral deposits along the root.",
                    "A massive, ice-blue tusk — could anchor a weapon or talisman.",
                ],
            },
        ],
    },

    # --- Stormhaven Coast: sea_raider (solo) ---
    "sea_raider": {
        "mob_type": "sea_raider",
        "relevant_skill": "combat",
        "base_drop_chance": 0.80,
        "drops": [
            {
                "item_id": "raider_boarding_axe",
                "key": "raider's boarding axe",
                "item_type": "equipment",
                "equipment_archetype": "cleaving_axe",
                "affix_profile": "raider_weapon",
                "affix_count_by_tier": [0, 0, 1, 1, 1],
                "equip_slot": "main_hand",
                "scaling_stat": "strength",
                "material_tier_by_tier": [1, 1, 2, 2, 3],
                "damage_min_by_tier": [9, 11, 13, 16, 19],
                "damage_max_by_tier": [15, 18, 21, 25, 29],
                "stat_bonuses_by_tier": [
                    {"strength": 1},
                    {"strength": 1},
                    {"strength": 2},
                    {"strength": 2},
                    {"strength": 3},
                ],
                "weight": 2.0,
                "weight_in_pool": 4,
                "value_by_tier":  [10, 22, 45, 90, 180],
                "rarity_by_tier": ["normal", "normal", "magic", "rare", "rare"],
                "desc_by_tier": [
                    "A chipped boarding axe, salt-crusted and dull.",
                    "A serviceable boarding axe with a leather-wrapped haft.",
                    "A well-honed boarding axe, balanced for quick work.",
                    "A fine boarding axe with a razor edge and iron-capped haft.",
                    "A masterwork boarding axe — light, fast, and wickedly sharp.",
                ],
            },
            {
                "item_id": "plunder_pouch",
                "key": "plunder pouch",
                "item_type": "item",
                "weight": 0.3,
                "weight_in_pool": 8,
                "value_by_tier":  [4, 10, 20, 40, 80],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A meager pouch of stolen coppers.",
                    "A pouch with mixed foreign coins.",
                    "A heavy pouch jingling with silver and brass.",
                    "A fat pouch of gold coins bearing distant crests.",
                    "A bulging pouch of rare coins, gems, and a signet ring.",
                ],
            },
            {
                "item_id": "sea_raider_leather",
                "key": "sea raider's leather",
                "item_type": "item",
                "weight": 0.8,
                "weight_in_pool": 6,
                "value_by_tier":  [3, 7, 15, 30, 60],
                "rarity_by_tier": ["normal", "normal", "normal", "normal", "magic"],
                "desc_by_tier": [
                    "Scraps of salt-hardened leather, barely usable.",
                    "Strips of tough raider leather, stiff from brine.",
                    "Quality sea-treated leather with natural waterproofing.",
                    "Dense, oiled leather from a veteran raider's kit.",
                    "Exceptional brine-cured leather, supple yet hard as shell.",
                ],
            },
        ],
    },
    # --- Rat loot (D-22) ---
    "rat": {
        "mob_type": "rat",
        "relevant_skill": "combat",
        "base_drop_chance": 0.40,
        "drops": [
            {
                "item_id": "rat_hide",
                "key": "rat hide",
                "item_type": "item",
                "weight": 0.2,
                "weight_in_pool": 10,
                "value_by_tier":  [1, 2, 4, 8, 15],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A scrap of matted rat fur.",
                    "A small rat hide, barely usable.",
                    "A decent rat pelt with thick fur.",
                    "A large, unusually clean rat hide.",
                    "A pristine hide from an enormous rat.",
                ],
            },
            {
                "item_id": "rat_tail",
                "key": "rat tail",
                "item_type": "item",
                "weight": 0.1,
                "weight_in_pool": 5,
                "value_by_tier":  [1, 1, 3, 6, 12],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A thin, wiry rat tail.",
                    "A rat tail, occasionally used in folk remedies.",
                    "A thick rat tail, prized by alchemists.",
                    "An unusually long tail with alchemical properties.",
                    "A perfectly preserved tail, pulsing with strange energy.",
                ],
            },
        ],
    },
    # --- Bandit loot (D-22) ---
    "bandit": {
        "mob_type": "bandit",
        "relevant_skill": "combat",
        "base_drop_chance": 0.65,
        "drops": [
            {
                "item_id": "stolen_coin_pouch",
                "key": "stolen coin pouch",
                "item_type": "item",
                "weight": 0.3,
                "weight_in_pool": 10,
                "value_by_tier":  [5, 12, 25, 50, 100],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "A threadbare pouch with a few Scales inside.",
                    "A pouch containing a modest haul of stolen Scales.",
                    "A well-stuffed pouch of pilfered coins.",
                    "A heavy pouch bulging with stolen wealth.",
                    "A masterwork purse overflowing with Scales.",
                ],
            },
            {
                "item_id": "bandit_blade",
                "key": "notched blade",
                "item_type": "equipment",
                "equipment_archetype": "agile_blade",
                "affix_profile": "bandit_weapon",
                "affix_count_by_tier": [0, 0, 1, 1, 1],
                "equip_slot": "main_hand",
                "scaling_stat": "agility",
                "material_tier_by_tier": [1, 1, 2, 2, 3],
                "damage_min_by_tier": [4, 5, 7, 9, 12],
                "damage_max_by_tier": [8, 10, 13, 16, 20],
                "stat_bonuses_by_tier": [
                    {},
                    {},
                    {"agility": 1},
                    {"agility": 1},
                    {"agility": 2},
                ],
                "weight": 1.5,
                "weight_in_pool": 5,
                "value_by_tier":  [8, 18, 35, 70, 140],
                "rarity_by_tier": ["normal", "normal", "magic", "rare", "rare"],
                "desc_by_tier": [
                    "A rusty, notched blade. Barely sharp.",
                    "A worn shortsword taken from a bandit.",
                    "A serviceable blade, well-maintained despite its owner.",
                    "A keen-edged blade with a leather-wrapped grip.",
                    "A fine blade with a hidden maker's mark — stolen from someone important.",
                ],
            },
            {
                "item_id": "bandit_leather",
                "key": "bandit leather",
                "item_type": "item",
                "weight": 1.0,
                "weight_in_pool": 4,
                "value_by_tier":  [3, 8, 16, 32, 65],
                "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
                "desc_by_tier": [
                    "Scraps of worn leather armor.",
                    "Rough leather patches, repairable.",
                    "Decent bandit leathers, still functional.",
                    "Reinforced leather with hidden pockets.",
                    "Masterwork leather armor, suspiciously fine for a bandit.",
                ],
            },
        ],
    },
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _loot_table_keys_for_mob(mob):
    """Return explicit loot table key first, then legacy mob_type fallback."""
    keys = []
    for raw_key in (
            getattr(mob.db, "loot_table", None),
            getattr(mob.db, "mob_type", None)):
        if isinstance(raw_key, str) and raw_key and raw_key not in keys:
            keys.append(raw_key)
    return keys


def _resolve_loot_table(mob):
    """Return loot table entry for mob, checking zone overrides first."""
    table_keys = _loot_table_keys_for_mob(mob)
    if not table_keys:
        return None

    # Check zone override
    room = mob.location
    if room:
        zone_obj = get_zone_obj_for_room(room)
        if zone_obj and zone_obj.db.loot_table_overrides:
            for table_key in table_keys:
                override = zone_obj.db.loot_table_overrides.get(table_key)
                if override:
                    return override

    for table_key in table_keys:
        table = LOOT_TABLES.get(table_key)
        if table:
            return table
    return None


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


def _loot_source_for_mob(mob):
    """Build lightweight provenance for generated item defs."""
    if not mob:
        return None
    source = {
        "source_type": "mob_drop",
        "mob_key": getattr(mob, "key", None),
    }
    for attr_name in ("mob_type", "loot_table"):
        value = getattr(mob.db, attr_name, None)
        if value:
            source[attr_name] = value
    room = getattr(mob, "location", None)
    if room:
        zone_id = getattr(room.db, "zone_id", None)
        if zone_id:
            source["zone_id"] = zone_id
    return source


def _build_item_def(drop, tier, mob=None):
    """Build an item_def dict from a drop entry at a given tier (1-5)."""
    if drop.get("equipment_archetype"):
        from world.equipment_archetypes import build_equipment_from_archetype
        return build_equipment_from_archetype(
            drop,
            tier,
            source=_loot_source_for_mob(mob),
        )

    idx = max(0, min(4, tier - 1))
    item_def = {
        "item_id":   drop["item_id"],
        "key":       drop["key"],
        "item_type": drop.get("item_type", "item"),
        "weight":    drop.get("weight", 0.5),
        "rarity":    drop["rarity_by_tier"][idx],
        "value":     drop["value_by_tier"][idx],
        "desc":      drop["desc_by_tier"][idx],
    }
    if "material_tier_by_tier" in drop:
        item_def["material_tier"] = drop["material_tier_by_tier"][idx]
    elif "material_tier" in drop:
        item_def["material_tier"] = drop["material_tier"]

    for source_key, target_key in (
        ("damage_min_by_tier", "damage_min"),
        ("damage_max_by_tier", "damage_max"),
        ("armor_value_by_tier", "armor_value"),
        ("stat_bonuses_by_tier", "stat_bonuses"),
    ):
        if source_key in drop:
            item_def[target_key] = copy.deepcopy(drop[source_key][idx])

    for field_name in (
        "equip_slot",
        "scaling_stat",
        "two_handed",
        "stackable",
        "tool_slot",
        "tool_tag",
        "use_effect",
        "weapon_family",
    ):
        if field_name in drop:
            item_def[field_name] = copy.deepcopy(drop[field_name])

    return item_def


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

    return [_build_item_def(drop, tier, mob=mob) for drop in selected]
