"""Canonical internal scale and pure helpers for faction standing."""

from numbers import Integral, Real


STANDING_MIN = -100_000
STANDING_MAX = 100_000
STANDING_AUTHORED_MIN_CHANGE = 1_000

STANDING_DISCOUNT_TIERS = (
    (75_000, 0.30),
    (50_000, 0.20),
    (25_000, 0.10),
    (0, 0.00),
)


def clamp_standing(value):
    """Clamp a numeric standing value to the documented internal range."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError("Standing must be numeric.")
    return max(STANDING_MIN, min(STANDING_MAX, value))


def standing_fraction(value):
    """Map canonical standing to a clamped -1.0 through +1.0 fraction."""
    return float(clamp_standing(value)) / STANDING_MAX


def standing_benefit_fraction(value):
    """Map only favorable standing to a clamped 0.0 through 1.0 fraction."""
    return max(0.0, standing_fraction(value))


def validate_authored_standing_delta(delta):
    """Return whether a content-authored change is meaningful on this scale."""
    return (
        isinstance(delta, Integral)
        and not isinstance(delta, bool)
        and STANDING_AUTHORED_MIN_CHANGE <= abs(delta) <= STANDING_MAX
    )
