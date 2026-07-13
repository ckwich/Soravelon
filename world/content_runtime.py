"""Read-only proof that legacy runtime state exactly reflects a manifest."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass

from world.content_compiler import (
    AreaOperation,
    FrozenMap,
    SymbolicReference,
    WorldManifest,
    _operation_value,
    _thaw,
)
from world.tag_search import search_objects_by_exact_tag


@dataclass(frozen=True)
class RuntimeManifestDiagnostic:
    source_path: str
    line: int
    column: int
    zone_id: str
    entity_id: str
    code: str
    message: str


@dataclass(frozen=True)
class RuntimeManifestVerification:
    verified_manifest_hash: str | None
    diagnostics: tuple[RuntimeManifestDiagnostic, ...]


def hydrate_runtime_registries(manifest: WorldManifest) -> None:
    """Rebuild process-local lookup registries from existing verified objects."""

    from world import zone_registry
    from world.flight_registry import FlightRegistry

    zone_registry.clear()
    FlightRegistry.clear()
    for definition in manifest.zones:
        zone_obj = next(
            (
                obj
                for obj in search_objects_by_exact_tag("zone_object", "object_type")
                if (obj.db.zone_id or "") == definition.zone_id
            ),
            None,
        )
        if zone_obj is None:
            raise RuntimeError(
                f"Cannot hydrate missing runtime zone '{definition.zone_id}'."
            )
        zone_registry.register_zone(definition.zone_id, zone_obj)
        for operation in definition.operations:
            if operation.method == "flight_point":
                room_id = _ref_key(operation.arguments[0])
                point_id = operation.arguments[1]
                room = next(
                    (
                        candidate
                        for candidate in search_objects_by_exact_tag(room_id, "room_id")
                        if (candidate.db.zone_id or "") == definition.zone_id
                    ),
                    None,
                )
                if room is None:
                    raise RuntimeError(
                        f"Cannot hydrate flight point '{point_id}': room missing."
                    )
                FlightRegistry.register_point(
                    point_id,
                    room,
                    name=_operation_value(operation, 2, "name"),
                )
            elif operation.method == "flight_route":
                first, second, fare = operation.arguments[:3]
                FlightRegistry.register_route(
                    first,
                    second,
                    fare,
                    _operation_value(operation, 3, "leg_duration", 30),
                    _operation_value(operation, 4, "echoes", ()) or [],
                )


def _plain(value):
    if isinstance(value, FrozenMap):
        return {str(key): _plain(item) for key, item in value.entries}
    if isinstance(value, SymbolicReference):
        return {"kind": value.kind, "key": value.key}
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if isinstance(value, set):
        return sorted(_plain(item) for item in value)
    return value


def _kwargs(operation: AreaOperation) -> dict[str, object]:
    value = _thaw(operation.keyword_arguments)
    return value if isinstance(value, dict) else {}


def _ref_key(value: object) -> str | None:
    if isinstance(value, SymbolicReference):
        return value.key
    if isinstance(value, str):
        return value
    return None


class _RuntimeVerifier:
    def __init__(self, manifest: WorldManifest):
        self.manifest = manifest
        self.diagnostics: list[RuntimeManifestDiagnostic] = []
        self._load_runtime_snapshot()

    def _load_runtime_snapshot(self) -> None:
        """Load authored object, attribute, tag, and social state in bounded queries."""

        from evennia.objects.models import ObjectDB
        from django.db.models import Q
        from world.models import SocialEdge, SocialNode, SocialTopologyBinding

        tag_links = ObjectDB.db_tags.through.objects
        authored_object_ids = tag_links.filter(
            tag__db_category="zone_id",
            tag__db_tagtype__isnull=True,
        ).values("objectdb_id")
        identified_object_ids = tag_links.filter(
            Q(tag__db_category__in=("room_id", "npc_id"))
            | Q(tag__db_category="object_type", tag__db_key="zone_object"),
            tag__db_tagtype__isnull=True,
        ).values("objectdb_id")
        objects = list(
            ObjectDB.objects.filter(
                Q(id__in=identified_object_ids)
                | Q(id__in=authored_object_ids, db_destination__isnull=False)
            )
            .select_related("db_location", "db_destination")
            .distinct()
        )
        object_ids = [obj.id for obj in objects]
        self.objects = {obj.id: obj for obj in objects}
        self.tags: dict[int, dict[str | None, list[str]]] = defaultdict(
            lambda: defaultdict(list)
        )
        runtime_tag_links = (
            ObjectDB.db_tags.through.objects.filter(
                objectdb_id__in=object_ids,
                tag__db_tagtype__isnull=True,
            )
            .select_related("tag")
            .order_by("id")
        )
        for link in runtime_tag_links:
            self.tags[link.objectdb_id][link.tag.db_category].append(link.tag.db_key)
        zone_object_ids = {
            obj.id
            for obj in objects
            if "zone_object" in self.tags[obj.id].get("object_type", [])
        }
        room_object_ids = {
            obj.id for obj in objects if self.tags[obj.id].get("room_id")
        }
        npc_object_ids = {obj.id for obj in objects if self.tags[obj.id].get("npc_id")}
        exit_object_ids = {
            obj.id for obj in objects if obj.db_destination_id is not None
        }
        common_attribute_keys = {"zone_id"}
        zone_attribute_keys = {
            "gathering_pools",
            "item_definitions",
            "layer_1_overrides",
            "material_definitions",
            "name",
            "node_lore_fragments",
            "quest_definitions",
        }
        room_attribute_keys = {
            "ambient_echoes",
            "ambient_interval",
            "ambient_variance",
            "desc",
            "flags",
            "grid_x",
            "grid_y",
            "indoor",
            "initial_room_flags",
            "is_layer1",
            "lore_fragments",
            "practice_opportunities",
            "room_type",
            "spawn_definitions",
            "terrain",
            "time_echoes",
            "triggers",
        }
        npc_attribute_keys = {
            "dialogue_base_hints",
            "dialogue_greeting_tiers",
            "dialogue_network_hints",
            "dialogue_quest_hints",
            "dialogue_scholar_hints",
            "dialogue_tier_hints",
            "dialogue_topics",
            "dialogue_warden_hints",
            "faction",
            "is_medic",
            "is_vendor",
            "social_edges",
            "social_profile",
            "trainer_id",
            "vendor_accepts",
            "vendor_exclude_item_ids",
            "vendor_faction",
            "vendor_item_ids",
        }
        exit_attribute_keys = {
            "desc",
            "hidden",
            "lock_tag",
            "requires_ancestry",
            "requires_quest",
            "requires_standing",
        }
        for definition in self.manifest.zones:
            zone_operation = next(
                operation
                for operation in definition.operations
                if operation.method == "zone"
            )
            zone_attribute_keys.update(_kwargs(zone_operation))
        self.attributes: dict[int, dict[str, object]] = defaultdict(dict)
        attribute_scope = Q(
            objectdb_id__in=object_ids,
            attribute__db_key__in=common_attribute_keys,
        )
        for ids, keys in (
            (zone_object_ids, zone_attribute_keys),
            (room_object_ids, room_attribute_keys),
            (npc_object_ids, npc_attribute_keys),
            (exit_object_ids, exit_attribute_keys),
        ):
            attribute_scope |= Q(objectdb_id__in=ids, attribute__db_key__in=keys)
        attribute_links = (
            ObjectDB.db_attributes.through.objects.filter(attribute_scope)
            .filter(
                attribute__db_category__isnull=True,
                attribute__db_attrtype__isnull=True,
            )
            .select_related("attribute")
        )
        for link in attribute_links:
            self.attributes[link.objectdb_id][
                link.attribute.db_key
            ] = link.attribute.value
        self.owned_by_zone: dict[str, list[object]] = defaultdict(list)
        for obj in objects:
            zone_ids = self.tags[obj.id].get("zone_id", [])
            if zone_ids:
                self.owned_by_zone[zone_ids[0]].append(obj)
        self.room_identity_by_pk = {
            obj.id: (self.attr(obj, "zone_id"), room_ids[0])
            for obj in objects
            if (room_ids := self.tags[obj.id].get("room_id", []))
        }
        self.social_nodes = {node.node_key: node for node in SocialNode.objects.all()}
        self.social_edges = {
            edge.edge_key: edge
            for edge in SocialEdge.objects.select_related("source_node", "target_node")
        }
        self.social_bindings_by_zone: dict[str, set[tuple[str, str]]] = defaultdict(set)
        for zone_id, kind, object_key in SocialTopologyBinding.objects.values_list(
            "zone_id", "kind", "object_key"
        ):
            self.social_bindings_by_zone[zone_id].add((kind, object_key))

    def attr(self, obj, key: str, default=None):
        return self.attributes.get(obj.id, {}).get(key, default)

    def tag_values(self, obj, category: str) -> list[str]:
        return self.tags.get(obj.id, {}).get(category, [])

    def tag_value(self, obj, category: str):
        values = self.tag_values(obj, category)
        return values[0] if values else None

    def has_tag(self, obj, key: str, category: str) -> bool:
        return key in self.tag_values(obj, category)

    def report(
        self,
        operation: AreaOperation,
        zone_id: str,
        entity_id: str,
        code: str,
        message: str,
    ) -> None:
        self.diagnostics.append(
            RuntimeManifestDiagnostic(
                source_path=operation.source_path,
                line=operation.line,
                column=operation.column,
                zone_id=zone_id,
                entity_id=entity_id,
                code=code,
                message=message,
            )
        )

    def compare(
        self,
        operation: AreaOperation,
        zone_id: str,
        entity_id: str,
        expected: object,
        actual: object,
    ) -> None:
        if _plain(expected) != _plain(actual):
            self.report(
                operation,
                zone_id,
                entity_id,
                "runtime-value-mismatch",
                f"Expected {_plain(expected)!r}; found {_plain(actual)!r}.",
            )

    def verify(self) -> RuntimeManifestVerification:
        expected_zone_ids = {definition.zone_id for definition in self.manifest.zones}
        zone_objects = {
            str(zone_id): obj
            for obj in self.objects.values()
            if self.has_tag(obj, "zone_object", "object_type")
            and (zone_id := self.attr(obj, "zone_id"))
        }
        actual_zone_ids = set(zone_objects)
        for definition in self.manifest.zones:
            zone_operation = next(
                operation
                for operation in definition.operations
                if operation.method == "zone"
            )
            if definition.zone_id not in actual_zone_ids:
                self.report(
                    zone_operation,
                    definition.zone_id,
                    definition.zone_id,
                    "missing-runtime-zone",
                    "Manifest zone has no runtime ZoneObject.",
                )
                continue
            self.verify_zone(definition, zone_objects[definition.zone_id])
        for zone_id in sorted(actual_zone_ids - expected_zone_ids):
            zone_obj = zone_objects[zone_id]
            self.diagnostics.append(
                RuntimeManifestDiagnostic(
                    source_path="<runtime>",
                    line=1,
                    column=1,
                    zone_id=zone_id,
                    entity_id=zone_id,
                    code="unexpected-runtime-zone",
                    message=f"Runtime ZoneObject #{zone_obj.id} is not manifest-owned.",
                )
            )
        ordered = tuple(
            sorted(
                self.diagnostics,
                key=lambda item: (
                    item.source_path,
                    item.line,
                    item.column,
                    item.code,
                    item.entity_id,
                ),
            )
        )
        return RuntimeManifestVerification(
            verified_manifest_hash=None if ordered else self.manifest.manifest_hash,
            diagnostics=ordered,
        )

    def verify_zone(self, definition, zone_obj) -> None:
        zone_id = definition.zone_id
        operations = tuple(
            operation
            for operation in definition.operations
            if operation.method != "build"
        )
        by_method: dict[str, list[AreaOperation]] = {}
        for operation in operations:
            by_method.setdefault(operation.method, []).append(operation)

        zone_operation = by_method["zone"][0]
        for field, expected in _kwargs(zone_operation).items():
            actual = (
                self.attr(zone_obj, "name")
                if field == "name"
                else self.attr(zone_obj, field)
            )
            self.compare(
                zone_operation, zone_id, f"{zone_id}.{field}", expected, actual
            )

        owned = self.owned_by_zone.get(zone_id, [])
        rooms = {
            str(room_id): obj
            for obj in owned
            if (room_id := self.tag_value(obj, "room_id"))
            and not self.attr(obj, "is_layer1", False)
        }
        expected_rooms = {
            str(operation.arguments[0]): operation
            for operation in by_method.get("room", [])
        }
        self.compare_identity_sets(
            zone_operation,
            zone_id,
            "room",
            set(expected_rooms),
            set(rooms),
        )
        for room_id in sorted(set(expected_rooms) & set(rooms)):
            self.verify_room(zone_id, expected_rooms[room_id], rooms[room_id])

        npcs = {
            str(npc_id): obj
            for obj in owned
            if (npc_id := self.tag_value(obj, "npc_id"))
        }
        expected_npcs = {
            str(operation.arguments[1]): operation
            for operation in by_method.get("npc", [])
        }
        self.compare_identity_sets(
            zone_operation,
            zone_id,
            "npc",
            set(expected_npcs),
            set(npcs),
        )
        for npc_id in sorted(set(expected_npcs) & set(npcs)):
            operation = expected_npcs[npc_id]
            npc = npcs[npc_id]
            room_id = _ref_key(operation.arguments[0])
            actual_room_id = (
                self.tag_value(npc.location, "room_id") if npc.location else None
            )
            self.compare(
                operation, zone_id, f"{npc_id}.location", room_id, actual_room_id
            )
            kwargs = _kwargs(operation)
            field_map = {
                "name": "key",
                "faction": "faction",
                "trainer_id": "trainer_id",
                "social_profile": "social_profile",
                "social_edges": "social_edges",
            }
            for authored, runtime in field_map.items():
                if authored not in kwargs:
                    continue
                actual = npc.key if runtime == "key" else self.attr(npc, runtime)
                self.compare(
                    operation, zone_id, f"{npc_id}.{authored}", kwargs[authored], actual
                )
            self.verify_npc_dialogue(operation, zone_id, npc_id, npc, kwargs)

        self.verify_exits(
            zone_id, zone_operation, by_method.get("exit", []), rooms, owned
        )
        self.verify_zone_definitions(zone_id, zone_obj, by_method)
        self.verify_room_definitions(zone_id, rooms, by_method)
        self.verify_runtime_flags(zone_id, rooms, npcs, by_method)
        self.verify_flight(zone_id, by_method)
        self.verify_social(zone_id, by_method)
        self.verify_node(zone_id, zone_obj, rooms, by_method)

        supported = {
            "build",
            "exit",
            "flight_point",
            "flight_route",
            "gathering_pool",
            "initial_room_state",
            "item",
            "lore_fragment",
            "material",
            "medic",
            "named_mob",
            "node",
            "npc",
            "practice_opportunity",
            "quest",
            "room",
            "room_role",
            "social_edge",
            "social_node",
            "spawn",
            "trigger",
            "vendor",
            "zone",
        }
        for operation in operations:
            if operation.method not in supported:
                self.report(
                    operation,
                    zone_id,
                    operation.method,
                    "unsupported-runtime-verification",
                    f"area.{operation.method}() has no bootstrap verifier.",
                )

    def compare_identity_sets(
        self, operation, zone_id, entity_type, expected, actual
    ) -> None:
        for entity_id in sorted(expected - actual):
            self.report(
                operation,
                zone_id,
                entity_id,
                f"missing-runtime-{entity_type}",
                f"Manifest {entity_type} is absent from runtime state.",
            )
        for entity_id in sorted(actual - expected):
            self.report(
                operation,
                zone_id,
                entity_id,
                f"unexpected-runtime-{entity_type}",
                f"Runtime {entity_type} is not manifest-owned.",
            )

    def verify_room(self, zone_id, operation, room) -> None:
        room_id = str(operation.arguments[0])
        kwargs = _kwargs(operation)
        defaults = {
            "name": room_id,
            "desc": "",
            "room_type": "generic",
            "indoor": False,
            "terrain": "none",
            "flags": [],
            "ambient_echoes": [],
            "ambient_interval": 60,
            "ambient_variance": 30,
            "time_echoes": {},
        }
        for field, default in defaults.items():
            expected = kwargs.get(field, default)
            actual = room.key if field == "name" else self.attr(room, field)
            self.compare(operation, zone_id, f"{room_id}.{field}", expected, actual)
        for field in ("grid_x", "grid_y"):
            if field in kwargs:
                self.compare(
                    operation,
                    zone_id,
                    f"{room_id}.{field}",
                    kwargs[field],
                    self.attr(room, field),
                )
        if "crafting_stations" in kwargs:
            actual = [
                str(tag).removeprefix("crafting_")
                for tag in self.tag_values(room, "crafting_station")
            ]
            self.compare(
                operation,
                zone_id,
                f"{room_id}.crafting_stations",
                kwargs["crafting_stations"],
                actual,
            )

    def verify_npc_dialogue(self, operation, zone_id, npc_id, npc, kwargs) -> None:
        dialogue = kwargs.get("dialogue", {})
        expected_greeting_tiers = dict(dialogue.get("greeting_tiers", {}))
        if dialogue.get("greeting") and "neutral" not in expected_greeting_tiers:
            expected_greeting_tiers["neutral"] = dialogue["greeting"]
        dialogue_fields = {
            "greeting_tiers": "dialogue_greeting_tiers",
            "topics": "dialogue_topics",
            "base_hints": "dialogue_base_hints",
            "tier_hints": "dialogue_tier_hints",
            "quest_hints": "dialogue_quest_hints",
            "network_hints": "dialogue_network_hints",
            "scholar_hints": "dialogue_scholar_hints",
            "warden_hints": "dialogue_warden_hints",
        }
        dict_fields = {"greeting_tiers", "topics", "tier_hints", "quest_hints"}
        for authored, runtime in dialogue_fields.items():
            expected = (
                expected_greeting_tiers
                if authored == "greeting_tiers"
                else dialogue.get(authored, {} if authored in dict_fields else [])
            )
            self.compare(
                operation,
                zone_id,
                f"{npc_id}.dialogue.{authored}",
                expected,
                self.attr(npc, runtime),
            )

    def verify_exits(self, zone_id, zone_operation, operations, rooms, owned) -> None:
        expected = {}
        for operation in operations:
            source = _ref_key(operation.arguments[0])
            destination = operation.arguments[1]
            direction = operation.arguments[2]
            expected[(source, direction)] = (operation, destination)
        actual = {}
        room_ids_by_pk = {room.id: room_id for room_id, room in rooms.items()}
        for exit_obj in owned:
            if exit_obj.db_location_id in room_ids_by_pk and exit_obj.db_destination_id:
                actual[(room_ids_by_pk[exit_obj.db_location_id], exit_obj.key)] = (
                    exit_obj
                )
        self.compare_identity_sets(
            zone_operation, zone_id, "exit", set(expected), set(actual)
        )
        for identity in sorted(set(expected) & set(actual)):
            operation, destination = expected[identity]
            exit_obj = actual[identity]
            if isinstance(destination, SymbolicReference):
                expected_destination = f"{zone_id}:{destination.key}"
            else:
                expected_destination = destination
            actual_destination = None
            if exit_obj.destination:
                destination_identity = self.room_identity_by_pk.get(
                    exit_obj.db_destination_id
                )
                if destination_identity:
                    actual_destination = (
                        f"{destination_identity[0]}:{destination_identity[1]}"
                    )
            self.compare(
                operation,
                zone_id,
                f"{identity[0]}.{identity[1]}.destination",
                expected_destination,
                actual_destination,
            )
            kwargs = _kwargs(operation)
            defaults = {
                "desc": "",
                "hidden": False,
                "locked": False,
                "requires_ancestry": None,
                "requires_standing": None,
                "requires_quest": None,
            }
            for field, default in defaults.items():
                expected_value = kwargs.get(field, default)
                if field == "locked":
                    actual_value = bool(self.attr(exit_obj, "lock_tag"))
                else:
                    actual_value = self.attr(exit_obj, field)
                self.compare(
                    operation,
                    zone_id,
                    f"{identity[0]}.{identity[1]}.{field}",
                    expected_value,
                    actual_value,
                )

    def verify_zone_definitions(self, zone_id, zone_obj, by_method) -> None:
        expected_items = [
            {"item_id": operation.arguments[0], **_kwargs(operation)}
            for operation in by_method.get("item", [])
        ]
        self.compare_collection(
            zone_id,
            by_method,
            "item",
            expected_items,
            self.attr(zone_obj, "item_definitions", []) or [],
        )
        expected_materials = [
            {
                "material": operation.arguments[0],
                "tier": _kwargs(operation).get("tier", 1),
                "terrain": _kwargs(operation).get("terrain"),
                "absorbed_property": _kwargs(operation).get("absorbed_property"),
                "profession_bonus": _kwargs(operation).get("profession_bonus", {}),
            }
            for operation in by_method.get("material", [])
        ]
        self.compare_collection(
            zone_id,
            by_method,
            "material",
            expected_materials,
            self.attr(zone_obj, "material_definitions", []) or [],
        )
        expected_quests = [
            self.expected_quest(operation) for operation in by_method.get("quest", [])
        ]
        self.compare_collection(
            zone_id,
            by_method,
            "quest",
            expected_quests,
            self.attr(zone_obj, "quest_definitions", []) or [],
        )
        expected_pools = [
            self.expected_gathering_pool(operation)
            for operation in by_method.get("gathering_pool", [])
        ]
        self.compare_collection(
            zone_id,
            by_method,
            "gathering_pool",
            expected_pools,
            self.attr(zone_obj, "gathering_pools", []) or [],
        )

    def compare_collection(self, zone_id, by_method, method, expected, actual) -> None:
        operation = (by_method.get(method) or by_method["zone"])[0]
        self.compare(operation, zone_id, f"{zone_id}.{method}", expected, actual)

    def expected_quest(self, operation) -> dict[str, object]:
        kwargs = _kwargs(operation)
        quest_id = operation.arguments[0]
        return {
            "quest_id": quest_id,
            "name": kwargs.get("name", quest_id),
            "description": kwargs.get("description", ""),
            "quest_type": kwargs.get("quest_type"),
            "quest_giver": kwargs.get("quest_giver"),
            "objectives": kwargs.get("objectives", []),
            "rewards": kwargs.get("rewards", []),
            "next_quest_id": kwargs.get("next_quest_id"),
            "prerequisite_quests": kwargs.get("prerequisite_quests", []),
            "one_chance": kwargs.get("one_chance", False),
            "incident_seed": kwargs.get("incident_seed"),
            "quest_archetype": kwargs.get("quest_archetype"),
            "social_quest_context": kwargs.get("social_quest_context"),
            "can_share": kwargs.get("can_share", False),
            "share_radius": kwargs.get("share_radius", 1),
            "share_cap": kwargs.get("share_cap", 6),
            "objective_type": kwargs.get("objective_type"),
            "objective_target": kwargs.get("objective_target"),
            "objective_count": kwargs.get("objective_count", 1),
            "flagged_drop": kwargs.get("flagged_drop"),
            "reward_tiers": kwargs.get("reward_tiers", {}),
            "world_expression": kwargs.get("world_expression", {}),
            "consequence_small": kwargs.get("consequence_small"),
            "consequence_medium": kwargs.get("consequence_medium"),
        }

    def expected_gathering_pool(self, operation) -> dict[str, object]:
        kwargs = _kwargs(operation)
        return {
            "pool_type": _operation_value(operation, 0, "pool_type"),
            "room_ids": _operation_value(operation, 1, "rooms"),
            "materials": _operation_value(operation, 2, "materials"),
            "max_active": kwargs.get("max_active", 3),
            "respawn_minutes": kwargs.get("respawn_minutes", 15),
            "respawn_variance": kwargs.get("respawn_variance", 5),
            "tier_floor": kwargs.get("tier_floor", 1),
            "tier_ceiling": kwargs.get("tier_ceiling", 3),
        }

    def verify_room_definitions(self, zone_id, rooms, by_method) -> None:
        expected_spawns: dict[str, list[dict[str, object]]] = {
            room_id: [] for room_id in rooms
        }
        for operation in by_method.get("spawn", []):
            expected_spawns[_ref_key(operation.arguments[0])].append(
                self.expected_spawn(operation, named=False)
            )
        for operation in by_method.get("named_mob", []):
            expected_spawns[_ref_key(operation.arguments[1])].append(
                self.expected_spawn(operation, named=True)
            )
        expected_lore: dict[str, list[dict[str, object]]] = {
            room_id: [] for room_id in rooms
        }
        for operation in by_method.get("lore_fragment", []):
            kwargs = _kwargs(operation)
            expected_lore[_ref_key(operation.arguments[1])].append(
                {
                    "fragment_id": operation.arguments[0],
                    "discovery_method": kwargs.get("discovery_method", "search"),
                    "scholar_path": kwargs.get("scholar_path"),
                    "text": kwargs.get("text", ""),
                    "insight_gain": kwargs.get("insight_gain", 0),
                }
            )
        expected_triggers: dict[str, list[dict[str, object]]] = {
            room_id: [] for room_id in rooms
        }
        for operation in by_method.get("trigger", []):
            room_id = _ref_key(operation.arguments[0])
            kwargs = _kwargs(operation)
            expected_triggers[room_id].append(
                {
                    "trigger_id": kwargs.get("trigger_id"),
                    "event": operation.arguments[1],
                    "actions": _operation_value(operation, 2, "actions"),
                    "once_per_character": kwargs.get("once_per_character", False),
                    "cooldown_seconds": kwargs.get("cooldown_seconds", 0),
                }
            )
        expected_practice: dict[str, list[dict[str, object]]] = {
            room_id: [] for room_id in rooms
        }
        for operation in by_method.get("practice_opportunity", []):
            room_id = _ref_key(operation.arguments[1])
            kwargs = _kwargs(operation)
            expected_practice[room_id].append(
                {
                    "opportunity_id": operation.arguments[0],
                    "verb": kwargs.get("verb"),
                    "target": kwargs.get("target", ""),
                    "skill_awards": kwargs.get("skill_awards", {}),
                    "domain_awards": kwargs.get("domain_awards", {}),
                    "success_text": kwargs.get("success_text", ""),
                    "failure_text": kwargs.get("failure_text", ""),
                    "once_per_character": kwargs.get("once_per_character", True),
                    "cooldown_seconds": kwargs.get("cooldown_seconds", 0),
                }
            )
        for room_id, room in rooms.items():
            room_operation = next(
                operation
                for operation in by_method.get("room", [])
                if operation.arguments[0] == room_id
            )
            for label, expected, actual in (
                (
                    "spawns",
                    expected_spawns[room_id],
                    self.attr(room, "spawn_definitions", []) or [],
                ),
                (
                    "lore",
                    expected_lore[room_id],
                    self.attr(room, "lore_fragments", []) or [],
                ),
                (
                    "triggers",
                    expected_triggers[room_id],
                    self.attr(room, "triggers", []) or [],
                ),
                (
                    "practice",
                    expected_practice[room_id],
                    self.attr(room, "practice_opportunities", []) or [],
                ),
            ):
                self.compare(
                    room_operation,
                    zone_id,
                    f"{room_id}.{label}",
                    expected,
                    actual,
                )

    def expected_spawn(self, operation, *, named: bool) -> dict[str, object]:
        kwargs = _kwargs(operation)
        mob = operation.arguments[0] if named else operation.arguments[1]
        return {
            "mob": mob,
            "behavior": kwargs.get("behavior", []),
            "flee_threshold": kwargs.get("flee_threshold", 20),
            "count_min": 1 if named else kwargs.get("count_min", 1),
            "count_max": 1 if named else kwargs.get("count_max", 1),
            "respawn_minutes": kwargs.get("respawn_minutes", 120 if named else 15),
            "respawn_variance": kwargs.get("respawn_variance", 30 if named else 5),
            "standing_check": None if named else kwargs.get("standing_check"),
            "base_disposition": kwargs.get("base_disposition", 0.0),
            "trust_sensitive": False if named else kwargs.get("trust_sensitive", False),
            "is_named": named,
            "prestige_modifier": kwargs.get("prestige_modifier", 1.0),
            "tome_drop": kwargs.get("tome_drop"),
            "spawn_condition": kwargs.get("spawn_condition"),
            "sequence": kwargs.get("sequence", []),
        }

    def verify_runtime_flags(self, zone_id, rooms, npcs, by_method) -> None:
        for operation in by_method.get("room_role", []):
            room_id = _ref_key(operation.arguments[0])
            role = operation.arguments[1]
            tag = {"greeter": "greeter_room", "respawn": "respawn_point"}[role]
            self.compare(
                operation,
                zone_id,
                f"{room_id}.role.{role}",
                True,
                self.has_tag(rooms[room_id], tag, "spawn_point"),
            )
        for operation in by_method.get("initial_room_state", []):
            room_id = _ref_key(operation.arguments[0])
            self.compare(
                operation,
                zone_id,
                f"{room_id}.initial_room_state",
                operation.arguments[1],
                self.attr(rooms[room_id], "initial_room_flags"),
            )
        for operation in by_method.get("vendor", []):
            npc_id = _ref_key(operation.arguments[0])
            kwargs = _kwargs(operation)
            npc = npcs[npc_id]
            self.compare(
                operation,
                zone_id,
                f"{npc_id}.is_vendor",
                True,
                self.attr(npc, "is_vendor"),
            )
            for authored, runtime in (
                ("accepts", "vendor_accepts"),
                ("item_ids", "vendor_item_ids"),
                ("exclude_item_ids", "vendor_exclude_item_ids"),
                ("faction", "vendor_faction"),
            ):
                if authored in kwargs or authored == "faction":
                    self.compare(
                        operation,
                        zone_id,
                        f"{npc_id}.{authored}",
                        kwargs.get(authored),
                        self.attr(npc, runtime),
                    )
        for operation in by_method.get("medic", []):
            npc_id = _ref_key(operation.arguments[0])
            self.compare(
                operation,
                zone_id,
                f"{npc_id}.is_medic",
                True,
                self.attr(npcs[npc_id], "is_medic"),
            )

    def verify_flight(self, zone_id, by_method) -> None:
        from world.flight_registry import FlightRegistry

        for operation in by_method.get("flight_point", []):
            room_id = _ref_key(operation.arguments[0])
            point_id = operation.arguments[1]
            point = FlightRegistry.get_point(point_id)
            actual_room = None
            if point:
                identity = self.room_identity_by_pk.get(point.get("room_id"))
                if identity:
                    actual_room = identity[1]
            self.compare(
                operation,
                zone_id,
                f"flight_point.{point_id}.room",
                (zone_id, room_id),
                (point.get("zone_id"), actual_room) if point else None,
            )
        for operation in by_method.get("flight_route", []):
            first, second, fare = operation.arguments[:3]
            kwargs = _kwargs(operation)
            self.compare(
                operation,
                zone_id,
                f"flight_route.{first}.{second}",
                {
                    "base_fare": fare,
                    "leg_duration": kwargs.get("leg_duration", 30),
                    "echoes": kwargs.get("echoes", []),
                },
                FlightRegistry.get_route(first, second),
            )

    def verify_social(self, zone_id, by_method) -> None:
        from world.social_topology import social_edge_key

        expected_bindings = set()
        for operation in by_method.get("social_node", []):
            node_key = f"{operation.arguments[0]}:{operation.arguments[1]}"
            expected_bindings.add(("node", node_key))
            node = self.social_nodes.get(node_key)
            if node is None:
                self.report(
                    operation,
                    zone_id,
                    node_key,
                    "missing-runtime-social-node",
                    "Social node is absent.",
                )
            else:
                kwargs = _kwargs(operation)
                expected = {
                    "node_type": operation.arguments[0],
                    "display_name": kwargs.get("display_name", ""),
                    "zone_id": kwargs.get("zone_id") or zone_id,
                    "settlement_id": kwargs.get("settlement_id", ""),
                    "faction_id": kwargs.get("faction_id", ""),
                    "metadata": kwargs.get("metadata", {}),
                }
                actual = {field: getattr(node, field) for field in expected}
                self.compare(operation, zone_id, node_key, expected, actual)
        for operation in by_method.get("social_edge", []):
            kwargs = _kwargs(operation)
            edge_key = social_edge_key(
                operation.arguments[0], operation.arguments[1], kwargs.get("edge_type")
            )
            expected_bindings.add(("edge", edge_key))
            edge = self.social_edges.get(edge_key)
            if edge is None:
                self.report(
                    operation,
                    zone_id,
                    edge_key,
                    "missing-runtime-social-edge",
                    "Social edge is absent.",
                )
            else:
                from world.social_taxonomy import normalize_tags

                expected = {
                    "source_node": operation.arguments[0],
                    "target_node": operation.arguments[1],
                    "edge_type": kwargs.get("edge_type"),
                    "directionality": kwargs.get("directionality", "one_way"),
                    "trust": kwargs.get("trust", 0.5),
                    "latency_seconds": kwargs.get("latency_seconds", 0),
                    "bandwidth": kwargs.get("bandwidth", 3),
                    "secrecy": kwargs.get("secrecy", ""),
                    "distortion": kwargs.get("distortion", ""),
                    "scope_tags": normalize_tags(kwargs.get("scope_tags", [])),
                    "blockers": normalize_tags(kwargs.get("blockers", [])),
                    "required_tags": normalize_tags(
                        kwargs.get("required_tags")
                        if kwargs.get("required_tags") is not None
                        else kwargs.get("blockers", [])
                    ),
                    "blocked_tags": normalize_tags(kwargs.get("blocked_tags", [])),
                }
                actual = {
                    "source_node": edge.source_node.node_key,
                    "target_node": edge.target_node.node_key,
                    **{
                        field: getattr(edge, field)
                        for field in expected
                        if field not in {"source_node", "target_node"}
                    },
                }
                self.compare(operation, zone_id, edge_key, expected, actual)
        actual_bindings = self.social_bindings_by_zone.get(zone_id, set())
        operation = (
            by_method.get("social_node")
            or by_method.get("social_edge")
            or by_method["zone"]
        )[0]
        self.compare(
            operation,
            zone_id,
            f"{zone_id}.social_bindings",
            sorted(expected_bindings),
            sorted(actual_bindings),
        )

    def verify_node(self, zone_id, zone_obj, rooms, by_method) -> None:
        for operation in by_method.get("node", []):
            center_room_id = _ref_key(operation.arguments[0])
            scripts = zone_obj.scripts.get("node_script")
            script = scripts[0] if scripts else None
            self.compare(
                operation,
                zone_id,
                f"{zone_id}.node.center",
                rooms[center_room_id].id,
                script.db.center_room_id if script else None,
            )
            self.compare(
                operation,
                zone_id,
                f"{zone_id}.node.radius",
                (
                    operation.arguments[1]
                    if len(operation.arguments) > 1
                    else _kwargs(operation).get("radius")
                ),
                script.db.node_radius if script else None,
            )
            overrides = _kwargs(operation).get("layer_1_overrides", {})
            self.compare(
                operation,
                zone_id,
                f"{zone_id}.node.layer_1_overrides",
                overrides,
                self.attr(zone_obj, "layer_1_overrides", {}) or {},
            )
            self.compare(
                operation,
                zone_id,
                f"{zone_id}.node.lore_fragments",
                _kwargs(operation).get("lore_fragments", []),
                self.attr(zone_obj, "node_lore_fragments", []) or [],
            )


def verify_runtime_manifest(manifest: WorldManifest) -> RuntimeManifestVerification:
    """Verify exact manifest ownership and authored values without any writes."""

    return _RuntimeVerifier(manifest).verify()
