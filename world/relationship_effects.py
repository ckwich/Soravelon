"""Pure validation and cache-tracking rules for authored world-state effects."""

import re
from numbers import Integral, Real


AUTHORED_DIMENSIONS = frozenset({"reputation", "network", "bond", "legacy"})
RELATIONSHIP_EFFECT_ACTIONS = frozenset(
    {
        "modify_dimension",
        "modify_attunement",
        "modify_trust",
        "set_betrayal",
    }
)

_EFFECT_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_.:-]{0,79}$")
_ZONE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_]{0,63}$")


def is_valid_effect_id(value):
    """Return whether a replay identity is stable and safe to compose."""
    return isinstance(value, str) and bool(_EFFECT_ID_PATTERN.fullmatch(value))


def is_valid_effect_delta(value):
    """Return whether a 0-100 relationship track change is bounded and real."""
    return (
        isinstance(value, Real)
        and not isinstance(value, bool)
        and value != 0
        and abs(value) <= 100
    )


def is_valid_trust_delta(value):
    """Return whether a Trust change preserves the integer 0-100 contract."""
    return (
        isinstance(value, Integral)
        and not isinstance(value, bool)
        and value != 0
        and abs(value) <= 100
    )


def is_valid_zone_id(value):
    """Return whether a zone ID is canonical before registry resolution."""
    return isinstance(value, str) and bool(_ZONE_ID_PATTERN.fullmatch(value))


def tracked_relationship_attributes(actions):
    """Return Evennia Attributes that an action batch may mutate."""
    names = set()
    for action in actions or ():
        if not isinstance(action, dict):
            continue
        action_type = action.get("action_type")
        if action_type == "modify_dimension":
            dimension = action.get("dimension")
            if dimension in AUTHORED_DIMENSIONS:
                names.add(f"{dimension}_score")
        elif action_type == "modify_attunement":
            names.add("attunement_score")
    return tuple(sorted(names))
