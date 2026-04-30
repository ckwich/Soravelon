"""
area_validator — pure-Python zone data validation.

No Django or Evennia imports at module level. Safe to import
in any Python 3.11+ environment without server setup.

Used by:
  - world/area_builder.py (imports constants)
  - world/zone_serializer.py (calls validate_zone before loading)
  - soravelon-builder sidecar (bundles this file for offline validation)
"""

from dataclasses import dataclass


class AreaBuilderValidationError(Exception):
    """Raised when an area spec contains invalid values."""
    pass


@dataclass
class ValidationError:
    severity: str    # "error" | "warning"
    field_path: str  # dot-notation path e.g. "zone.zone_type", "rooms[2].room_type"
    message: str


# ---------------------------------------------------------------------------
# Validation constants — authoritative source of truth.
# area_builder.py imports these rather than defining its own copies.
# ---------------------------------------------------------------------------

VALID_ZONE_TYPES = {
    "ancient_forest", "plains", "mountain", "coastal",
    "underground", "imperial_city", "frontier", "node_active",
}

VALID_CONTINENTS = {"varath", "sorath", "veluana"}

VALID_NODE_TYPES = {
    "resonance", "thermal", "gravity", "temporal", "cognitive",
}

VALID_FACTION_TERRITORIES = {
    "imperial", "neutral", "warden", "kauroran",
    "contested", "hidden",
}

VALID_DIRECTIONS = {
    "north", "south", "east", "west",
    "northeast", "northwest", "southeast", "southwest",
    "up", "down", "in", "out",
}

VALID_ROOM_TYPES = {
    "path", "clearing", "ruins", "cave", "building",
    "underground", "node_center", "generic",
}

SUPPORTED_SPAWN_CONDITIONS = (
    "node_active",
    "node_failure_above_N",
)

TIERED_LOOT_FIELDS = {
    "value_by_tier",
    "rarity_by_tier",
    "desc_by_tier",
    "material_tier_by_tier",
    "damage_min_by_tier",
    "damage_max_by_tier",
    "armor_value_by_tier",
    "stat_bonuses_by_tier",
}


def _append_error(errors: list, field_path: str, message: str):
    errors.append(ValidationError(
        severity="error",
        field_path=field_path,
        message=message,
    ))


def _validate_tiered_loot_field(errors: list, drop: dict, field_path: str, field_name: str):
    value = drop.get(field_name)
    if not isinstance(value, list) or len(value) != 5:
        _append_error(errors, field_path, f"{field_name} must be a list with one value for each tier 1-5")


def _validate_loot_table_overrides(errors: list, loot_table_overrides: list):
    if not isinstance(loot_table_overrides, list):
        _append_error(errors, "loot_table_overrides", "loot_table_overrides must be a list")
        return

    for table_idx, table in enumerate(loot_table_overrides):
        table_path = f"loot_table_overrides[{table_idx}]"
        if not isinstance(table, dict):
            _append_error(errors, table_path, "loot table override must be an object")
            continue

        mob_type = table.get("mob_type")
        if not isinstance(mob_type, str) or not mob_type:
            _append_error(errors, f"{table_path}.mob_type", "mob_type is required")

        relevant_skill = table.get("relevant_skill", "combat")
        if not isinstance(relevant_skill, str) or not relevant_skill:
            _append_error(errors, f"{table_path}.relevant_skill", "relevant_skill must be a skill/domain key")

        base_drop_chance = table.get("base_drop_chance", 0.7)
        if (
            not isinstance(base_drop_chance, (int, float))
            or isinstance(base_drop_chance, bool)
            or base_drop_chance < 0
            or base_drop_chance > 1
        ):
            _append_error(errors, f"{table_path}.base_drop_chance", "base_drop_chance must be a number from 0 to 1")

        drops = table.get("drops")
        if not isinstance(drops, list):
            _append_error(errors, f"{table_path}.drops", "drops must be a list")
            continue

        for drop_idx, drop in enumerate(drops):
            drop_path = f"{table_path}.drops[{drop_idx}]"
            if not isinstance(drop, dict):
                _append_error(errors, drop_path, "drop must be an object")
                continue

            for required_field in ["item_id", "key"]:
                if not isinstance(drop.get(required_field), str) or not drop.get(required_field):
                    _append_error(errors, f"{drop_path}.{required_field}", f"{required_field} is required")

            for required_tiered_field in ["value_by_tier", "rarity_by_tier", "desc_by_tier"]:
                _validate_tiered_loot_field(
                    errors,
                    drop,
                    f"{drop_path}.{required_tiered_field}",
                    required_tiered_field,
                )

            for optional_tiered_field in TIERED_LOOT_FIELDS - {"value_by_tier", "rarity_by_tier", "desc_by_tier"}:
                if optional_tiered_field in drop:
                    _validate_tiered_loot_field(
                        errors,
                        drop,
                        f"{drop_path}.{optional_tiered_field}",
                        optional_tiered_field,
                    )


# ---------------------------------------------------------------------------
# validate_zone
# ---------------------------------------------------------------------------

def validate_zone(zone_data: dict) -> list:
    """
    Validate a zone data dict (matching the .zone.json schema).

    Args:
        zone_data: dict with keys "zone" (dict), "rooms" (list), "exits" (list).

    Returns:
        list[ValidationError] — empty list if all valid.
    """
    errors = []

    zone = zone_data.get("zone") or {}
    rooms = zone_data.get("rooms") or []
    exits = zone_data.get("exits") or []
    loot_table_overrides = zone_data.get("loot_table_overrides") or []

    # zone.name — required and non-empty
    name = zone.get("name")
    if not name:
        errors.append(ValidationError(
            severity="error",
            field_path="zone.name",
            message="name is required",
        ))

    # zone.zone_type — optional; if present must be in VALID_ZONE_TYPES
    zone_type = zone.get("zone_type")
    if zone_type and zone_type not in VALID_ZONE_TYPES:
        errors.append(ValidationError(
            severity="error",
            field_path="zone.zone_type",
            message=f"invalid zone_type '{zone_type}'. Valid: {sorted(VALID_ZONE_TYPES)}",
        ))

    # zone.continent — optional; if present must be in VALID_CONTINENTS
    continent = zone.get("continent")
    if continent and continent not in VALID_CONTINENTS:
        errors.append(ValidationError(
            severity="error",
            field_path="zone.continent",
            message=f"invalid continent '{continent}'. Valid: {sorted(VALID_CONTINENTS)}",
        ))

    # zone.node_type — optional; if present must be in VALID_NODE_TYPES
    node_type = zone.get("node_type")
    if node_type and node_type not in VALID_NODE_TYPES:
        errors.append(ValidationError(
            severity="error",
            field_path="zone.node_type",
            message=f"invalid node_type '{node_type}'. Valid: {sorted(VALID_NODE_TYPES)}",
        ))

    # zone.faction_territory — defaults to "neutral"; if present must be valid
    faction_territory = zone.get("faction_territory")
    if faction_territory and faction_territory not in VALID_FACTION_TERRITORIES:
        errors.append(ValidationError(
            severity="error",
            field_path="zone.faction_territory",
            message=(
                f"invalid faction_territory '{faction_territory}'. "
                f"Valid: {sorted(VALID_FACTION_TERRITORIES)}"
            ),
        ))

    # rooms[N].room_type — optional per room; if present must be in VALID_ROOM_TYPES
    for idx, room in enumerate(rooms):
        room_type = room.get("room_type")
        if room_type and room_type not in VALID_ROOM_TYPES:
            errors.append(ValidationError(
                severity="error",
                field_path=f"rooms[{idx}].room_type",
                message=(
                    f"invalid room_type '{room_type}'. "
                    f"Valid: {sorted(VALID_ROOM_TYPES)}"
                ),
            ))

    # exits[N].direction — optional per exit; if present must be in VALID_DIRECTIONS
    for idx, exit_def in enumerate(exits):
        direction = exit_def.get("direction")
        if direction and direction not in VALID_DIRECTIONS:
            errors.append(ValidationError(
                severity="error",
                field_path=f"exits[{idx}].direction",
                message=(
                    f"invalid direction '{direction}'. "
                    f"Valid: {sorted(VALID_DIRECTIONS)}"
                ),
            ))

    _validate_loot_table_overrides(errors, loot_table_overrides)

    return errors


def validate_spawn_condition(condition_str: str):
    """
    Validate one authored spawn condition string.

    Supported formats:
      - node_active
      - node_failure_above_<integer>
    """
    if not condition_str:
        return None
    if condition_str == "node_active":
        return None
    prefix = "node_failure_above_"
    if condition_str.startswith(prefix):
        suffix = condition_str[len(prefix):]
        if suffix.isdigit():
            return None
    raise AreaBuilderValidationError(
        f"unsupported spawn_condition '{condition_str}'. "
        f"Supported: {', '.join(SUPPORTED_SPAWN_CONDITIONS)}"
    )
