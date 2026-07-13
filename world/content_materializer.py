"""Deterministic runtime materialization from validated world manifests."""

from __future__ import annotations

from dataclasses import dataclass

from world.content_compiler import FrozenMap, SymbolicReference, WorldManifest


class ContentMaterializationError(RuntimeError):
    """Raised when a validated manifest cannot materialize exactly."""


@dataclass(frozen=True)
class ContentMaterializationReport:
    zones: tuple[str, ...]
    removed_zones: tuple[str, ...]
    reconciled: dict[str, int]

    def __getitem__(self, key: str):
        return getattr(self, key)


def _resolve_value(value, references):
    if isinstance(value, SymbolicReference):
        try:
            return references[(value.kind, value.key)]
        except KeyError as exc:
            raise ContentMaterializationError(
                f"Unresolved {value.kind} reference '{value.key}'."
            ) from exc
    if isinstance(value, FrozenMap):
        return {
            _resolve_value(key, references): _resolve_value(item, references)
            for key, item in value.entries
        }
    if isinstance(value, tuple):
        return [_resolve_value(item, references) for item in value]
    return value


def _finalize_cross_zone_exits() -> None:
    from world.area_builder import AreaBuilder, get_unresolved_exits
    from world.tag_search import search_objects_by_exact_tag

    unresolved = []
    for exit_data in get_unresolved_exits():
        target_zone_id, target_room_id = exit_data["to"].split(":", 1)
        target = next(
            (
                room
                for room in search_objects_by_exact_tag(target_room_id, "room_id")
                if (room.db.zone_id or "") == target_zone_id
            ),
            None,
        )
        if target is None:
            unresolved.append(exit_data["to"])
            continue
        builder = AreaBuilder.__new__(AreaBuilder)
        builder._zone_id = exit_data["from_room"].db.zone_id or "unknown"
        builder._exits_created = 0
        kwargs = {
            key: value
            for key, value in exit_data.items()
            if key not in {"from_room", "to", "direction"}
        }
        builder._create_exit_object(
            exit_data["from_room"],
            target,
            exit_data["direction"],
            **kwargs,
        )
    if unresolved:
        raise ContentMaterializationError(
            "Cross-zone exits remain unresolved: " + ", ".join(sorted(unresolved))
        )


def _remove_retired_zones(
    previous_manifest: WorldManifest | None,
    target_manifest: WorldManifest,
    *,
    maintenance_approved: bool,
) -> tuple[str, ...]:
    if previous_manifest is None:
        return ()

    from django.conf import settings
    from evennia.objects.models import ObjectDB
    from typeclasses.characters import Character
    from world.tag_search import search_objects_by_exact_tag

    target_zone_ids = {zone.zone_id for zone in target_manifest.zones}
    removed_zone_ids = tuple(
        sorted(
            zone.zone_id
            for zone in previous_manifest.zones
            if zone.zone_id not in target_zone_ids
        )
    )
    for zone_id in removed_zone_ids:
        objects = list(search_objects_by_exact_tag(zone_id, "zone_id"))
        rooms = [obj for obj in objects if obj.tags.get(category="room_id")]
        occupants = [
            content
            for room in rooms
            for content in room.contents
            if isinstance(content, Character)
        ]
        if occupants and not maintenance_approved:
            raise ContentMaterializationError(
                f"Retired zone '{zone_id}' contains player characters and requires "
                "explicit maintenance approval."
            )
        if occupants:
            raw_home = str(getattr(settings, "DEFAULT_HOME", "")).lstrip("#")
            try:
                destination = ObjectDB.objects.get(id=int(raw_home))
            except (ObjectDB.DoesNotExist, TypeError, ValueError) as exc:
                raise ContentMaterializationError(
                    f"Retired zone '{zone_id}' has occupants but DEFAULT_HOME is invalid."
                ) from exc
            if (destination.db.zone_id or "") == zone_id:
                raise ContentMaterializationError(
                    f"Retired zone '{zone_id}' cannot evict occupants into itself."
                )
            for character in occupants:
                character.move_to(destination, quiet=True, move_hooks=False)

        exits = []
        for obj in objects:
            if not obj.pk:
                continue
            try:
                if obj.destination is not None:
                    exits.append(obj)
            except Exception:
                continue
        for obj in exits:
            obj.delete()
        for obj in objects:
            if obj.pk and obj not in rooms and obj not in exits:
                obj.delete()
        for room in rooms:
            if room.pk:
                room.delete()
    return removed_zone_ids


def materialize_world_manifest(
    manifest: WorldManifest,
    *,
    previous_manifest: WorldManifest | None = None,
    maintenance_approved: bool = False,
) -> ContentMaterializationReport:
    """Replay a validated manifest through AreaBuilder without source imports."""

    from world import zone_registry
    from world.area_builder import AreaBuilder, clear_unresolved_exits
    from world.flight_registry import FlightRegistry
    from world.social_topology import (
        clear_registered_social_topology,
        materialize_registered_social_topology,
    )

    zone_registry.clear()
    FlightRegistry.clear()
    clear_unresolved_exits()
    clear_registered_social_topology()

    removed_zones = _remove_retired_zones(
        previous_manifest,
        manifest,
        maintenance_approved=maintenance_approved,
    )

    zone_ids = []
    authored_rooms = []
    reconciliation = {
        "rooms_deleted": 0,
        "exits_deleted": 0,
        "npcs_deleted": 0,
        "mobs_deleted": 0,
        "players_evicted": 0,
    }
    for definition in manifest.zones:
        builder = AreaBuilder(definition.zone_id)
        references = {}
        report = None
        for operation in definition.operations:
            arguments = tuple(
                _resolve_value(value, references) for value in operation.arguments
            )
            keyword_arguments = _resolve_value(operation.keyword_arguments, references)
            result = getattr(builder, operation.method)(*arguments, **keyword_arguments)
            if operation.method in {"room", "mob"}:
                references[(operation.method, operation.arguments[0])] = result
                if operation.method == "room":
                    authored_rooms.append(result)
            elif operation.method == "npc":
                references[("npc", operation.arguments[1])] = result
            elif operation.method == "build":
                report = result
        if report is None:
            raise ContentMaterializationError(
                f"Zone '{definition.zone_id}' did not contain area.build()."
            )
        zone_ids.append(definition.zone_id)
        for key in reconciliation:
            reconciliation[key] += report["reconciled"][key]

    social_report = materialize_registered_social_topology(finalize=True)
    if social_report["unresolved_edges"]:
        identifiers = sorted(
            f"{edge['source_node_key']}->{edge['target_node_key']}"
            for edge in social_report["unresolved_edges"]
        )
        raise ContentMaterializationError(
            "Social topology edges remain unresolved: " + ", ".join(identifiers)
        )
    _finalize_cross_zone_exits()
    from world.mob_spawner import reconcile_spawn_records

    spawn_report = reconcile_spawn_records(authored_rooms)
    reconciliation.update(
        {
            f"spawn_records_{action}": count
            for action, count in spawn_report.items()
        }
    )
    return ContentMaterializationReport(
        zones=tuple(zone_ids),
        removed_zones=removed_zones,
        reconciled=reconciliation,
    )
