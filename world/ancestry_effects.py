"""Canonical runtime interpretation of authored ancestry traits."""

from __future__ import annotations


def maximum_health_multiplier(character) -> float:
    """Return the ancestry multiplier applied to derived maximum health."""

    from world.ancestry_engine import get_ancestry_trait

    value = get_ancestry_trait(character, "hp_bonus", 1.0)
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
        raise ValueError("Ancestry hp_bonus must be a positive number.")
    return float(value)
