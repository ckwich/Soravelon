"""
Determines mob rarity and rolls affixes at spawn time.
Called by the spawn system when a mob is created.
"""

import random
from world.mob_affixes import (
    MOB_AFFIXES, NODE_AFFIX_POOLS, GENERAL_AFFIX_POOL,
    FORBIDDEN_COMBINATIONS, DEFENSIVE_LIMIT, DEFENSIVE_AFFIXES,
    RARITY_WEIGHTS, PACK_SIZES,
)

RARITY_AFFIX_COUNT = {
    "normal": 0,
    "magic": 1,
    "rare": 2,
    "legendary": 3,
}

RARITY_DISPLAY = {
    "magic": "|g\u2605|n",       # green star
    "rare": "|y\u2605\u2605|n",  # yellow two stars
    "legendary": "|r\u2605\u2605\u2605|n",  # red three stars
}


def roll_rarity():
    """Roll a rarity tier based on configured weights."""
    tiers = list(RARITY_WEIGHTS.keys())
    weights = [RARITY_WEIGHTS[t] for t in tiers]
    return random.choices(tiers, weights=weights, k=1)[0]


def get_affix_pool(room):
    """
    Get the appropriate affix pool for a room.
    Uses node type if room is in an active node zone.
    Falls back to general pool.
    """
    node_type = getattr(room.db, 'node_type', None)

    if (room.tags.get("mob_affixes_active", category="node_effect")
            and node_type
            and node_type in NODE_AFFIX_POOLS):
        return NODE_AFFIX_POOLS[node_type]

    return GENERAL_AFFIX_POOL


def roll_affixes(count, pool):
    """
    Roll `count` affixes from `pool`, enforcing:
    - No forbidden combinations
    - Maximum one defensive affix
    - No duplicates
    Returns list of affix tag strings.
    """
    if count == 0:
        return []

    available = list(pool)
    selected = []
    defensive_count = 0
    max_attempts = 50

    attempts = 0
    while len(selected) < count and available and attempts < max_attempts:
        attempts += 1
        choice = random.choice(available)
        available.remove(choice)

        if choice in DEFENSIVE_AFFIXES:
            if defensive_count >= DEFENSIVE_LIMIT:
                continue
            defensive_count += 1

        candidate_set = set(selected + [choice])
        forbidden = False
        for combo in FORBIDDEN_COMBINATIONS:
            if combo.issubset(candidate_set):
                forbidden = True
                break
        if forbidden:
            continue

        selected.append(choice)

    return selected


def apply_affixes_to_mob(mob, room):
    """
    Main entry point. Called at mob spawn time.
    Rolls rarity, rolls affixes, applies tags, stores rarity.
    Returns rarity string.
    """
    rarity = roll_rarity()
    affix_count = RARITY_AFFIX_COUNT[rarity]

    mob.db.rarity = rarity

    if affix_count > 0:
        pool = get_affix_pool(room)
        affixes = roll_affixes(affix_count, pool)

        for affix_tag in affixes:
            mob.tags.add(affix_tag, category="mob_affix")

        # Assign once — avoids SaverList N-append repickle
        mob.db.affix_list = affixes
    else:
        mob.db.affix_list = []

    return rarity


def get_pack_size(rarity):
    """Return (min, max) pack size for a rarity tier."""
    return PACK_SIZES.get(rarity, (0, 0))


def get_star_prefix(rarity):
    """Return ANSI star string for display, or empty string."""
    return RARITY_DISPLAY.get(rarity, "")


def spawn_mob_with_pack(mob_typeclass, key, room,
                        mob_type, zone_id, faction=None):
    """
    Spawn a mob with appropriate rarity and pack.
    Returns (affix_mob, [pack_mobs]) tuple.

    Pack companions are always normal rarity — no affixes.
    Uses initialize_for_spawn() which rolls affixes AND combat stats.
    """
    from evennia import create_object

    mob = create_object(mob_typeclass, key=key, location=room)
    mob.db.mob_type = mob_type
    mob.db.zone_id = zone_id
    mob.db.faction = faction

    mob.initialize_for_spawn(room)
    rarity = mob.db.rarity

    pack = []
    if rarity != "normal":
        min_pack, max_pack = get_pack_size(rarity)
        if min_pack > 0:
            pack_count = random.randint(min_pack, max_pack)
            for _ in range(pack_count):
                pack_mob = create_object(
                    mob_typeclass, key=key, location=room
                )
                pack_mob.db.mob_type = mob_type
                pack_mob.db.zone_id = zone_id
                pack_mob.db.faction = faction
                pack_mob.db.rarity = "normal"
                pack_mob.db.affix_list = []
                from world.zone_scaling import initialize_mob_combat_stats
                initialize_mob_combat_stats(pack_mob)
                pack.append(pack_mob)

    return mob, pack
