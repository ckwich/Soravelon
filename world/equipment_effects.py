"""Authoritative runtime effects for equipped Soravelon items.

InventoryItem rows decide what is equipped. This module translates those rows
into effective base attributes, armor, and weapon behavior without mutating a
character's intrinsic ``db.base_stats`` or consulting domain progression.
"""

from collections.abc import Mapping
from dataclasses import dataclass
import math
from numbers import Integral, Real


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

BARE_HANDS_MIN = 3
BARE_HANDS_MAX = 6
ARMOR_CURVE_SCALE = 50.0
MAX_ARMOR_MITIGATION = 0.75


@dataclass(frozen=True)
class WeaponDamageProfile:
    """Mechanically relevant weapon fields consumed by basic attacks."""

    minimum: int
    maximum: int
    scaling_stat: str
    element: str


def _has_player_stats(actor):
    stats = getattr(actor.db, "base_stats", None)
    return bool(stats)


def _is_player_character(actor):
    """Use the authoritative character tag with a legacy typeclass fallback."""
    if not _has_player_stats(actor):
        return False
    tags = getattr(actor, "tags", None)
    has_tag = getattr(tags, "has", None)
    if callable(has_tag):
        try:
            if has_tag(
                "player_character",
                category="character_type",
            ) is True:
                return True
        except (AttributeError, RuntimeError, TypeError):
            pass

    # Preserve equipment for legacy characters created before the identity tag.
    is_typeclass = getattr(actor, "is_typeclass", None)
    if callable(is_typeclass):
        try:
            return is_typeclass(
                "typeclasses.characters.Character",
                exact=False,
            ) is True
        except (AttributeError, RuntimeError, TypeError):
            pass
    return False


def _get_equipped_items(actor):
    """Return authoritative equipped rows only for a persisted player."""
    if not _is_player_character(actor):
        return []

    actor_id = getattr(actor, "id", None)
    if (
        isinstance(actor_id, bool)
        or not isinstance(actor_id, Integral)
        or actor_id <= 0
    ):
        return []

    from world.inventory_engine import get_equipped_items

    return get_equipped_items(actor)


def get_effective_stats(actor):
    """Return intrinsic, equipped, and ancestry-adjusted stats exactly once."""
    base_stats = getattr(actor.db, "base_stats", None)
    if not base_stats:
        return {}

    effective = dict(base_stats)
    for item, _record in _get_equipped_items(actor):
        bonuses = getattr(item.db, "stat_bonuses", None)
        if not isinstance(bonuses, Mapping):
            continue
        for stat_name, bonus in bonuses.items():
            if stat_name not in BASE_STAT_NAMES or stat_name not in effective:
                continue
            if (
                isinstance(bonus, bool)
                or not isinstance(bonus, Real)
                or not math.isfinite(float(bonus))
            ):
                continue
            effective[stat_name] += bonus
    if not _is_player_character(actor):
        return effective

    from world.ancestry_effects import apply_effective_stat_traits

    return apply_effective_stat_traits(actor, effective)


def get_total_equipped_armor(actor):
    """Return the non-negative armor rating of all equipped player items."""
    total = 0.0
    for item, _record in _get_equipped_items(actor):
        armor = getattr(item.db, "armor_value", 0) or 0
        if (
            isinstance(armor, bool)
            or not isinstance(armor, Real)
            or not math.isfinite(float(armor))
        ):
            continue
        total += max(0.0, float(armor))
    return int(total) if total.is_integer() else total


def clamp_current_resources_to_effective_caps(actor):
    """Prevent equipment changes from leaving HP or stamina above their caps."""

    if not _has_player_stats(actor):
        return

    from world.base_attributes import derive_max_hp, derive_max_stamina

    effective_stats = get_effective_stats(actor)
    current_hp = getattr(actor.ndb, "hp", None)
    current_stamina = getattr(actor.ndb, "stamina", None)
    if current_hp is not None:
        actor.ndb.hp = min(
            current_hp,
            derive_max_hp(actor, effective_stats=effective_stats),
        )
    if current_stamina is not None:
        actor.ndb.stamina = min(
            current_stamina,
            derive_max_stamina(actor, effective_stats=effective_stats),
        )


def _positive_damage(value, fallback):
    if (
        isinstance(value, bool)
        or not isinstance(value, Real)
        or not math.isfinite(float(value))
    ):
        return fallback
    return max(1, int(value))


def get_weapon_damage_profile(weapon):
    """Resolve authored weapon damage and base-stat scaling.

    Missing or invalid weapon data preserves the established unarmed/Strength
    fallback. Only the seven base attributes are valid scaling sources; domain
    scores are deliberately outside this contract.
    """
    if weapon is None:
        return WeaponDamageProfile(
            BARE_HANDS_MIN,
            BARE_HANDS_MAX,
            "strength",
            "physical",
        )

    minimum = _positive_damage(
        getattr(weapon.db, "damage_min", None),
        BARE_HANDS_MIN,
    )
    maximum = _positive_damage(
        getattr(weapon.db, "damage_max", None),
        BARE_HANDS_MAX,
    )
    maximum = max(minimum, maximum)

    scaling_stat = getattr(weapon.db, "scaling_stat", None)
    if scaling_stat not in BASE_STAT_NAMES:
        scaling_stat = "strength"

    element = getattr(weapon.db, "element", None)
    if not isinstance(element, str) or not element:
        element = "physical"

    return WeaponDamageProfile(minimum, maximum, scaling_stat, element)


def get_armor_mitigation(total_armor):
    """Convert armor rating to a capped, diminishing damage reduction."""
    if (
        isinstance(total_armor, bool)
        or not isinstance(total_armor, Real)
        or not math.isfinite(float(total_armor))
    ):
        return 0.0
    armor = max(0.0, float(total_armor))
    if armor == 0:
        return 0.0
    return min(
        MAX_ARMOR_MITIGATION,
        armor / (armor + ARMOR_CURVE_SCALE),
    )


def apply_armor_mitigation(damage, total_armor):
    """Apply the armor curve while preserving combat's one-damage floor."""
    if damage <= 0:
        return 0
    mitigation = get_armor_mitigation(total_armor)
    return max(1, round(damage * (1.0 - mitigation)))
