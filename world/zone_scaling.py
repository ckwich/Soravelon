"""
Per-player logarithmic mob scaling for Soravelon.

No zone level floors or caps. Every zone valid at every progression.
Mob HP rolled once at spawn (shared pool). Scaling operates on combat
math (damage dealt/received), not mob HP. Scaling locked per-player at
first hit, cached on mob.ndb.combat_scales[character.id].

Backend level is INTERNAL ONLY — never expose to players.
"""

import math
import random

REFERENCE_LEVEL = 10
SCALE_FLOOR = 0.5

RARITY_MULTIPLIERS = {
    "normal":    1.0,
    "magic":     1.4,
    "rare":      1.8,
    "legendary": 2.5,
}


# ---------------------------------------------------------------------------
# Mob initialization (called at spawn — once per mob lifetime)
# ---------------------------------------------------------------------------

def initialize_mob_combat_stats(mob):
    """
    Roll and store mob HP and damage at spawn time.
    Applies rarity and prestige multipliers.
    """
    rarity   = mob.db.rarity or "normal"
    prestige = mob.db.prestige_modifier or 1.0
    mult     = RARITY_MULTIPLIERS.get(rarity, 1.0) * prestige

    hp_min  = mob.db.hp_min  or 80
    hp_max  = mob.db.hp_max  or 120
    dmg_min = mob.db.damage_min or 8
    dmg_max = mob.db.damage_max or 14

    rolled_hp = random.randint(hp_min, hp_max)

    mob.db.hp           = int(rolled_hp * mult)
    mob.db.hp_max       = int(rolled_hp * mult)
    mob.db.ref_damage_min = int(dmg_min * mult)
    mob.db.ref_damage_max = int(dmg_max * mult)


# ---------------------------------------------------------------------------
# Per-player scaling (called at encounter start — once per character)
# ---------------------------------------------------------------------------

def get_scale_factor(backend_level):
    """
    Logarithmic scale factor. Returns float >= SCALE_FLOOR.
    At backend 10: 1.0 (reference). At backend 50: ~1.83.
    """
    raw = math.log(backend_level + 1) / math.log(REFERENCE_LEVEL + 1)
    return max(SCALE_FLOOR, raw)


def get_combat_scale(mob, character):
    """
    Return cached combat scale for character vs mob.
    Computes and caches on first call.
    """
    if not hasattr(mob.ndb, 'combat_scales') or mob.ndb.combat_scales is None:
        mob.ndb.combat_scales = {}

    if character.id not in mob.ndb.combat_scales:
        backend = character.db.backend_level or 1
        mob.ndb.combat_scales[character.id] = get_scale_factor(backend)

    return mob.ndb.combat_scales[character.id]


def get_mob_damage_for_player(mob, character):
    """Return (min_damage, max_damage) this mob deals to this character."""
    scale   = get_combat_scale(mob, character)
    dmg_min = int((mob.db.ref_damage_min or 8)  * scale)
    dmg_max = int((mob.db.ref_damage_max or 14) * scale)
    return dmg_min, dmg_max


def get_player_damage_to_mob(base_player_damage, mob, character):
    """Scale player damage against this mob."""
    scale = get_combat_scale(mob, character)
    return max(1, int(base_player_damage * scale))


def apply_resistance(damage, element, target):
    """Apply elemental resistance. Minimum 1 damage."""
    resistances = target.db.resistances or {}
    resistance  = resistances.get(element, 0.0)
    return max(1, int(damage * (1 - resistance)))


# ---------------------------------------------------------------------------
# Loot quality (skill-based, not level-based)
# ---------------------------------------------------------------------------

MATERIAL_TIER_BY_SKILL = [
    (0,  25,  1),
    (26, 50,  2),
    (51, 75,  3),
    (76, 90,  4),
    (91, 100, 5),
]


def get_material_tier(skill_score):
    """Return material drop tier (1-5) based on skill score, not zone."""
    for low, high, tier in MATERIAL_TIER_BY_SKILL:
        if low <= (skill_score or 0) <= high:
            return tier
    return 1


# ---------------------------------------------------------------------------
# Zone object lookup
# ---------------------------------------------------------------------------

def get_zone_obj_for_room(room):
    """Find the ZoneObject for a room. Returns None if not found."""
    zone_id = room.db.zone_id
    if not zone_id:
        return None
    # Search by zone_id tag first (O(1) indexed), fall back to scan
    import evennia
    tagged = evennia.search_tag(zone_id, category="zone_id")
    for obj in tagged:
        if obj.tags.get("zone_object", category="object_type"):
            return obj
    return None
