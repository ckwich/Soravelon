"""Canonical runtime interpretation of authored ancestry traits."""

from __future__ import annotations

from collections.abc import Mapping
import math
from numbers import Real


BASE_STAT_NAMES = frozenset(
    {
        "strength",
        "agility",
        "endurance",
        "mana",
        "acuity",
        "presence",
        "resonance",
    }
)


def _finite_number(value, *, trait_name: str) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, Real)
        or not math.isfinite(float(value))
    ):
        raise ValueError(f"Ancestry {trait_name} must be a finite number.")
    return float(value)


def _positive_multiplier(value, *, trait_name: str) -> float:
    multiplier = _finite_number(value, trait_name=trait_name)
    if multiplier <= 0:
        raise ValueError(f"Ancestry {trait_name} must be positive.")
    return multiplier


def apply_effective_stat_traits(character, effective_stats: Mapping) -> dict:
    """Return one ancestry-adjusted copy of already-effective base stats.

    Equipment is resolved before this boundary. Percentage traits describe
    total stat effectiveness, so they scale that complete effective value.
    Intrinsic ``db.base_stats`` and the supplied mapping are never mutated.
    """

    from world.ancestry_engine import get_ancestry_trait

    adjusted = dict(effective_stats)

    attribute_bonus = _finite_number(
        get_ancestry_trait(character, "attribute_bonus", 0),
        trait_name="attribute_bonus",
    )
    if attribute_bonus:
        for stat_name in BASE_STAT_NAMES.intersection(adjusted):
            adjusted[stat_name] += attribute_bonus

    multipliers = {
        "strength": get_ancestry_trait(character, "strength_scaling", 1.0),
        "agility": get_ancestry_trait(character, "agility_scaling", 1.0),
    }

    coat_traits = get_ancestry_trait(character, "coat_traits", {})
    coat = getattr(character.db, "selvar_coat", None)
    if isinstance(coat_traits, Mapping) and coat in coat_traits:
        selected_coat = coat_traits[coat]
        if not isinstance(selected_coat, Mapping):
            raise ValueError(f"Ancestry coat_traits[{coat!r}] must be a mapping.")
        if coat == "summer":
            agility_bonus = _finite_number(
                selected_coat.get("agility_bonus", 0),
                trait_name="coat_traits.summer.agility_bonus",
            )
            multipliers["agility"] *= 1.0 + agility_bonus
        elif coat == "winter":
            endurance_bonus = _finite_number(
                selected_coat.get("endurance_bonus", 0),
                trait_name="coat_traits.winter.endurance_bonus",
            )
            multipliers["endurance"] = 1.0 + endurance_bonus

    for stat_name, raw_multiplier in multipliers.items():
        if stat_name not in adjusted:
            continue
        multiplier = _positive_multiplier(
            raw_multiplier,
            trait_name=f"{stat_name}_effectiveness",
        )
        adjusted[stat_name] *= multiplier

    return adjusted


def maximum_health_multiplier(character) -> float:
    """Return the ancestry multiplier applied to derived maximum health."""

    from world.ancestry_engine import get_ancestry_trait

    return _positive_multiplier(
        get_ancestry_trait(character, "hp_bonus", 1.0),
        trait_name="hp_bonus",
    )
