"""Canonical identifiers for durable faction relationships."""


class FactionIdentityError(ValueError):
    """Raised when a relationship writer receives an unknown faction ID."""


FACTION_NAMES = {
    "circle": "Circle",
    "consortium": "Consortium",
    "empire": "Empire",
    "guilds": "Guilds",
    "ironblood": "Ironblood",
    "kauroran": "Kau'roran",
    "resistance": "Resistance",
    "resonance": "Resonance",
    "verdance": "Verdance",
    "wardens": "Wardens",
    "western_arcana": "Western Arcana",
}

CANONICAL_FACTION_IDS = frozenset(FACTION_NAMES)

FACTION_ID_ALIASES = {
    "warden": "wardens",
}


def canonicalize_faction_id(faction_id):
    """Return one validated relationship ID, accepting declared aliases."""
    if not isinstance(faction_id, str):
        raise FactionIdentityError("Faction ID must be a string.")
    normalized = faction_id.strip().lower()
    canonical = FACTION_ID_ALIASES.get(normalized, normalized)
    if canonical not in CANONICAL_FACTION_IDS:
        raise FactionIdentityError(f"Unknown faction relationship ID: {faction_id!r}")
    return canonical


def is_canonical_faction_id(faction_id):
    """Return whether a value is already a canonical relationship ID."""
    return isinstance(faction_id, str) and faction_id in CANONICAL_FACTION_IDS
