"""
Mob disposition system.

Computes a float (-1.0 to +1.0) representing a mob's disposition
toward a specific character. Behavior emerges from this float.

Standing and ancestry are ALWAYS additive — personal achievement
modifies institutional prejudice, it does not erase it.

PERFORMANCE: get_mob_disposition() makes up to 2 DB reads. The combat
system should cache get_mob_behavior() per encounter in character.ndb.
"""

from world.world_state import get_standing, get_trust

# --- Ancestry × Faction modifier table ---

ANCESTRY_FACTION_MODIFIERS = {
    ("human",    "empire"):      +0.10,
    ("human",    "wardens"):      0.00,
    ("human",    "resistance"):  -0.20,
    ("human",    "consortium"):   0.00,
    ("human",    "kauroran"):     0.00,
    ("kauroran", "empire"):      -0.20,
    ("kauroran", "wardens"):     +0.15,
    ("kauroran", "kauroran"):    +0.20,
    ("kauroran", "consortium"):   0.00,
    ("kauroran", "resistance"):  +0.05,
    ("veth",     "empire"):      -0.05,
    ("veth",     "wardens"):      0.00,
    ("veth",     "kauroran"):    +0.05,
    ("veth",     "consortium"):  +0.10,
    ("veth",     "resistance"):  +0.10,
    ("selvar",   "empire"):      -0.15,
    ("selvar",   "wardens"):     -0.05,
    ("selvar",   "kauroran"):    +0.05,
    ("selvar",   "consortium"):  +0.05,
    ("selvar",   "resistance"):   0.00,
}

# Behavior thresholds
FRIENDLY_THRESHOLD = 0.6
PASSIVE_THRESHOLD = 0.2
NEUTRAL_LOW = -0.2
ELEVATED_LOW = -0.6


def get_ancestry_modifier(ancestry, faction_id):
    """Return ancestry × faction disposition modifier. 0.0 for unlisted."""
    if not ancestry or not faction_id:
        return 0.0
    return ANCESTRY_FACTION_MODIFIERS.get(
        (ancestry.lower(), faction_id.lower()), 0.0
    )


def get_standing_modifier(character, faction_id):
    """Map Standing (-100,000 to +100,000) → modifier (-0.6 to +0.6)."""
    if not faction_id:
        return 0.0
    standing = get_standing(character, faction_id)
    return (standing / 100_000) * 0.6


def get_reputation_modifier(character):
    """Map Reputation (0-100) → modifier (0 to +0.2). Always non-negative."""
    reputation = float(getattr(character.db, 'reputation_score', 0.0) or 0.0)
    return (max(0.0, reputation) / 100) * 0.2


def get_trust_modifier(character, faction_id, pre_trust_disposition):
    """
    Trust modifier for trust_sensitive (elite) mobs only.

    Trust 0-24: reduces positive disposition proportionally.
    Trust 25-75: no effect.
    Trust 76+: +0.1 bonus.

    Only affects positive pre-trust disposition. Negative is untouched.
    """
    if not faction_id:
        return 0.0

    trust = get_trust(character, faction_id)

    if trust < 25 and pre_trust_disposition > 0:
        reduction_factor = trust / 25
        return pre_trust_disposition * (reduction_factor - 1)

    elif trust > 75:
        return +0.1

    return 0.0


def get_quest_modifier(character, quest_modifier_id):
    """
    Return disposition modifier from active quests referencing this modifier ID.

    Searches the character's active quests for a quest spec containing
    a 'disposition_modifier' field keyed by quest_modifier_id. Returns
    the float value if found, otherwise 0.0.
    """
    from world.quest_engine import get_active_quests, _get_quest_spec

    for cq in get_active_quests(character):
        spec = _get_quest_spec(cq.quest_id)
        if not spec:
            continue
        modifier = spec.get("disposition_modifier")
        if isinstance(modifier, dict):
            # Dict keyed by modifier_id -> float
            val = modifier.get(quest_modifier_id)
            if val is not None:
                return float(val)
        elif isinstance(modifier, (int, float)):
            # Single modifier applies if quest_modifier_id matches quest_id
            if cq.quest_id == quest_modifier_id:
                return float(modifier)
    return 0.0


def get_mob_disposition(mob, character):
    """
    Compute mob's disposition toward character. Returns float -1.0 to +1.0.
    Computed fresh each call — not cached here.
    """
    disposition = float(mob.db.base_disposition or 0.0)

    # Standing modifier
    if mob.db.faction:
        disposition += get_standing_modifier(character, mob.db.faction)

    # Reputation modifier
    disposition += get_reputation_modifier(character)

    # Ancestry modifier (additive with Standing — never overrides)
    if mob.db.faction:
        ancestry = getattr(character.db, 'ancestry', None)
        if ancestry:
            disposition += get_ancestry_modifier(ancestry, mob.db.faction)

    # Trust modifier (elite mobs only, applied after Standing+ancestry)
    if mob.db.faction and bool(mob.db.trust_sensitive):
        disposition += get_trust_modifier(
            character, mob.db.faction, disposition
        )

    # Quest modifier — reads from active quests via quest_engine
    if getattr(mob.db, 'quest_modifier', None):
        disposition += get_quest_modifier(
            character, mob.db.quest_modifier
        )

    return max(-1.0, min(1.0, disposition))


def get_mob_behavior(mob, character):
    """
    Translate disposition to behavior string.

    Returns one of:
      "friendly", "passive", base_aggression, "territorial", "aggressive"
    """
    disposition = get_mob_disposition(mob, character)
    base = (mob.db.base_aggression or 'passive')

    if disposition >= FRIENDLY_THRESHOLD:
        return "friendly"
    elif disposition >= PASSIVE_THRESHOLD:
        return "passive"
    elif disposition >= NEUTRAL_LOW:
        return base
    elif disposition >= ELEVATED_LOW:
        if base == "passive":
            return "territorial"
        return "aggressive"
    else:
        return "aggressive"
