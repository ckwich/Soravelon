"""
Base Attribute System for Soravelon.

Seven stats govern all combat math, resource derivation, and character identity.
Stats are displayed via descriptors only -- numeric values are never shown to players.
Stats grow through action-specific use with diminishing returns.

HP derived from Endurance + backend level.
Stamina derived from Endurance.
Action budget derived from Agility.
Initiative derived from Agility (characters) or speed (mobs).
"""

import math
import random

# ---------------------------------------------------------------------------
# Stat definitions
# ---------------------------------------------------------------------------

STAT_NAMES = (
    "strength",
    "agility",
    "endurance",
    "mana",
    "acuity",
    "presence",
    "resonance",
)

STAT_GOVERNS = {
    "strength": "Melee damage, carry capacity, physical power",
    "agility": "Speed, dodge chance, stealth, action budget",
    "endurance": "HP pool, stamina pool, damage resistance",
    "mana": "Spell power, mana pool, magical potency",
    "acuity": "Critical chance, cooldown reduction, perception",
    "presence": "Social ability power, charm, intimidation",
    "resonance": "Node interaction, attunement gain, resonance ability power",
}


# ---------------------------------------------------------------------------
# Descriptor tables (7 stats x 10 tiers = 70 unique descriptors)
# Tiers: 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80-89, 90-100
# ---------------------------------------------------------------------------

STAT_DESCRIPTORS = {
    "strength": [
        (0, "Feeble"),
        (10, "Frail"),
        (20, "Average"),
        (30, "Sturdy"),
        (40, "Strong"),
        (50, "Powerful"),
        (60, "Mighty"),
        (70, "Formidable"),
        (80, "Colossal"),
        (90, "Prodigious"),
    ],
    "agility": [
        (0, "Sluggish"),
        (10, "Clumsy"),
        (20, "Steady"),
        (30, "Nimble"),
        (40, "Quick"),
        (50, "Deft"),
        (60, "Swift"),
        (70, "Fleet"),
        (80, "Blinding"),
        (90, "Ethereal"),
    ],
    "endurance": [
        (0, "Fragile"),
        (10, "Delicate"),
        (20, "Hardy"),
        (30, "Tough"),
        (40, "Resilient"),
        (50, "Stout"),
        (60, "Stalwart"),
        (70, "Unyielding"),
        (80, "Ironforged"),
        (90, "Indomitable"),
    ],
    "mana": [
        (0, "Inert"),
        (10, "Dim"),
        (20, "Flickering"),
        (30, "Luminous"),
        (40, "Radiant"),
        (50, "Brilliant"),
        (60, "Blazing"),
        (70, "Incandescent"),
        (80, "Resplendent"),
        (90, "Transcendent"),
    ],
    "acuity": [
        (0, "Dull"),
        (10, "Unfocused"),
        (20, "Attentive"),
        (30, "Sharp"),
        (40, "Keen"),
        (50, "Precise"),
        (60, "Insightful"),
        (70, "Piercing"),
        (80, "Prescient"),
        (90, "Omniscient"),
    ],
    "presence": [
        (0, "Invisible"),
        (10, "Meek"),
        (20, "Noticeable"),
        (30, "Engaging"),
        (40, "Commanding"),
        (50, "Imposing"),
        (60, "Magnetic"),
        (70, "Sovereign"),
        (80, "Overwhelming"),
        (90, "Legendary"),
    ],
    "resonance": [
        (0, "Deaf"),
        (10, "Faint"),
        (20, "Attuned"),
        (30, "Receptive"),
        (40, "Sensitive"),
        (50, "Harmonic"),
        (60, "Resonant"),
        (70, "Reverberant"),
        (80, "Symphonic"),
        (90, "Primordial"),
    ],
}


def get_stat_descriptor(stat_name, value):
    """
    Return the descriptor word for a stat at a given value (0-100).

    Tiers: 0-9, 10-19, ..., 90-100. Value is clamped to 0-100.
    """
    tiers = STAT_DESCRIPTORS.get(stat_name)
    if not tiers:
        return "Unknown"
    clamped = max(0, min(100, int(value)))
    descriptor = tiers[0][1]  # default to lowest
    for threshold, word in tiers:
        if clamped >= threshold:
            descriptor = word
        else:
            break
    return descriptor


# ---------------------------------------------------------------------------
# Point-buy allocation
# ---------------------------------------------------------------------------

POINT_BUY_CONFIG = {
    "base": 10,
    "bonus_points": 20,
    "per_stat_max": 25,
    "per_stat_min": 5,
}


def validate_point_buy(allocations):
    """
    Validate a point-buy allocation dict.

    Each stat must be present and within per_stat_min..per_stat_max.
    Total points spent (sum of allocations - 7*base) must equal bonus_points
    plus any points freed by reducing stats below base.

    Returns (bool, str).
    """
    base = POINT_BUY_CONFIG["base"]
    bonus = POINT_BUY_CONFIG["bonus_points"]
    stat_max = POINT_BUY_CONFIG["per_stat_max"]
    stat_min = POINT_BUY_CONFIG["per_stat_min"]

    # Check all 7 stats present
    for stat in STAT_NAMES:
        if stat not in allocations:
            return False, f"Missing stat: {stat}"

    if len(allocations) != len(STAT_NAMES):
        return False, f"Expected {len(STAT_NAMES)} stats, got {len(allocations)}"

    # Check per-stat bounds
    for stat, val in allocations.items():
        if stat not in STAT_NAMES:
            return False, f"Unknown stat: {stat}"
        if not isinstance(val, (int, float)):
            return False, f"Stat {stat} must be a number"
        if val < stat_min:
            return False, f"{stat} below minimum ({stat_min})"
        if val > stat_max:
            return False, f"{stat} above maximum ({stat_max})"

    # Check total budget: each stat starts at base. Player can redistribute.
    # Total pool = 7 * base + bonus_points
    total_pool = len(STAT_NAMES) * base + bonus
    total_allocated = sum(int(v) for v in allocations.values())

    if total_allocated != total_pool:
        return False, (
            f"Point total {total_allocated} != {total_pool} "
            f"(7x{base} base + {bonus} bonus)"
        )

    return True, "Valid allocation"


def apply_point_buy(character, allocations):
    """
    Validate and apply point-buy allocation to character.db.base_stats.

    Returns (bool, str).
    """
    ok, msg = validate_point_buy(allocations)
    if not ok:
        return False, msg

    stats = {stat: int(allocations[stat]) for stat in STAT_NAMES}
    character.db.base_stats = stats
    return True, "Stats allocated successfully."


# ---------------------------------------------------------------------------
# HP and Stamina derivation
# ---------------------------------------------------------------------------

BASE_HP = 50
HP_PER_ENDURANCE = 5
HP_PER_LEVEL = 10

BASE_STAMINA = 30
STAMINA_PER_ENDURANCE = 2


def derive_max_hp(character, effective_stats=None):
    """
    Derive maximum HP from Endurance stat and backend level.

    Formula: base_hp(50) + endurance*5 + backend_level*10
    """
    if effective_stats is None:
        from world.equipment_effects import get_effective_stats

        effective_stats = get_effective_stats(character)
    stats = effective_stats
    endurance = stats.get("endurance", 10)
    backend_level = character.db.backend_level or 1
    base_value = BASE_HP + (endurance * HP_PER_ENDURANCE) + (
        backend_level * HP_PER_LEVEL
    )
    from world.ancestry_effects import maximum_health_multiplier

    return round(base_value * maximum_health_multiplier(character))


def derive_max_stamina(character, effective_stats=None):
    """
    Derive maximum stamina from Endurance stat.

    Formula: base_stamina(30) + endurance*2
    """
    if effective_stats is None:
        from world.equipment_effects import get_effective_stats

        effective_stats = get_effective_stats(character)
    stats = effective_stats
    endurance = stats.get("endurance", 10)
    return BASE_STAMINA + (endurance * STAMINA_PER_ENDURANCE)


def derive_hp(character):
    """Return current HP. Uses ndb cache if available, otherwise max HP."""
    hp = character.ndb.hp
    if hp is not None:
        return hp
    return derive_max_hp(character)


def derive_stamina(character):
    """Return current stamina. Uses ndb cache if available, otherwise max."""
    stamina = character.ndb.stamina
    if stamina is not None:
        return stamina
    return derive_max_stamina(character)


# ---------------------------------------------------------------------------
# Action budget
# ---------------------------------------------------------------------------

def get_actions_per_turn(character):
    """
    Derive actions per turn from Agility stat.

    Formula: floor(1 + agility / 30). Min 1, practical max 4.
    """
    from world.equipment_effects import get_effective_stats

    stats = get_effective_stats(character)
    agility = stats.get("agility", 10)
    actions = int(1 + agility / 30)
    return max(1, min(4, actions))


def get_damage_modifier(actions_per_turn):
    """
    Per-action damage modifier for multi-action builds.

    Formula: 1.0 / sqrt(actions_per_turn).
    More actions = less damage per action, preserving overall DPS balance.
    """
    return 1.0 / math.sqrt(max(1, actions_per_turn))


# ---------------------------------------------------------------------------
# Initiative
# ---------------------------------------------------------------------------

def get_initiative(combatant):
    """
    Calculate initiative for a combatant. Fixed for entire encounter.

    Characters: agility_stat + randint(1, 20)
    Mobs: (speed or 1.0) * 10 + randint(1, 20)
    """
    # Check if this is a character (has base_stats) or a mob (has speed)
    base_stats = combatant.db.base_stats
    if base_stats:
        from world.equipment_effects import get_effective_stats

        agility = get_effective_stats(combatant).get("agility", 10)
        return agility + random.randint(1, 20)
    else:
        # Mob: use speed attribute
        speed = combatant.db.speed or 1.0
        return int(speed * 10) + random.randint(1, 20)


# ---------------------------------------------------------------------------
# Stat growth through use
# ---------------------------------------------------------------------------

STAT_GROWTH_ACTIONS = {
    "melee_hit": "strength",
    "dodge_success": "agility",
    "damage_taken": "endurance",
    "spell_cast": "mana",
    "cooldown_reduced": "acuity",
    "social_ability": "presence",
    "resonance_ability": "resonance",
}

# Diminishing returns brackets for stat growth XP gain
STAT_GROWTH_RATES = [
    (0, 25, 1.0),      # stat 0-25: full rate
    (25, 50, 0.75),     # stat 25-50: 75%
    (50, 75, 0.40),     # stat 50-75: 40%
    (75, 90, 0.10),     # stat 75-90: 10%
    (90, 100, 0.02),    # stat 90-100: 2%
]

# Base XP per use action
STAT_XP_PER_USE = 0.5


def _get_stat_growth_rate(current_value):
    """Return the XP gain rate multiplier for a stat at the given value."""
    for low, high, rate in STAT_GROWTH_RATES:
        if low <= current_value < high:
            return rate
    # At 100 — effectively no growth
    return 0.0


def record_stat_use(character, action_type, amount=1):
    """
    Accumulate stat XP on ndb.stat_xp_accumulators for the given action.

    Applies diminishing returns based on the stat's current value.
    Does nothing if action_type is unknown or accumulators not initialized.
    """
    stat_name = STAT_GROWTH_ACTIONS.get(action_type)
    if not stat_name:
        return

    accumulators = character.ndb.stat_xp_accumulators
    if not accumulators:
        return

    # Get current stat value for diminishing returns
    stats = character.db.base_stats or {}
    current_value = stats.get(stat_name, 10)
    rate = _get_stat_growth_rate(current_value)

    xp_gain = STAT_XP_PER_USE * amount * rate
    accumulators[stat_name] = accumulators.get(stat_name, 0.0) + xp_gain


def commit_stat_growth(character):
    """
    Read ndb stat XP accumulators, convert to stat points, update
    character.db.base_stats using SaverDict copy pattern.

    Called alongside domain XP flush (session commit, logout, safety tick).
    """
    accumulators = character.ndb.stat_xp_accumulators
    if not accumulators:
        return

    # SaverDict copy pattern
    stats = dict(character.db.base_stats or {stat: 10 for stat in STAT_NAMES})
    changed = False

    for stat_name in STAT_NAMES:
        accumulated = accumulators.get(stat_name, 0.0)
        if accumulated <= 0:
            continue

        current = stats.get(stat_name, 10)
        # Each full point of XP = 1 stat point (fractional accumulates)
        persistent_xp = character.db.stat_xp or {}
        total_xp = persistent_xp.get(stat_name, 0.0) + accumulated

        # Convert XP to stat points: every 10 XP = 1 stat point
        new_points = int(total_xp / 10)
        remainder = total_xp - (new_points * 10)

        if new_points > 0:
            new_value = min(100, current + new_points)
            stats[stat_name] = new_value
            changed = True

        # Store remainder back to persistent XP
        persistent_xp = dict(character.db.stat_xp or {})
        persistent_xp[stat_name] = remainder
        character.db.stat_xp = persistent_xp

        # Reset accumulator
        accumulators[stat_name] = 0.0

    if changed:
        character.db.base_stats = stats
