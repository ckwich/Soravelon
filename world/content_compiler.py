"""Pure, mutation-free authority checks for literal AreaBuilder source."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
import json
from numbers import Integral, Real
from pathlib import Path
from typing import Mapping

from world.area_validator import VALID_DIRECTIONS
from world.action_vocabulary import ACTION_HANDLERS
from world.faction_registry import FactionIdentityError, canonicalize_faction_id
from world.item_catalog import CATALOG
from world.material_definitions import MATERIAL_REGISTRY
from world.mob_templates import MOB_TEMPLATES
from world.quest_engine import OBJECTIVE_TYPES, OBJECTIVE_TYPE_ALIASES
from world.skill_definitions import SKILL_DEFINITIONS
from world.social_taxonomy import EDGE_TYPES, NODE_TYPES

SUPPORTED_AREA_OPERATIONS = frozenset(
    {
        "build",
        "custom_command",
        "exit",
        "flight_point",
        "flight_route",
        "gathering_pool",
        "initial_room_state",
        "item",
        "loot_table_override",
        "lore_fragment",
        "material",
        "medic",
        "mob",
        "named_mob",
        "node",
        "npc",
        "patrol",
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
)
FORBIDDEN_RUNTIME_HANDLERS = frozenset({"attributes", "db", "scripts", "tags"})


@dataclass(frozen=True)
class SourceLocation:
    source_path: str
    line: int
    column: int


@dataclass(frozen=True)
class SymbolicReference:
    kind: str
    key: str


@dataclass(frozen=True)
class FrozenMap:
    entries: tuple[tuple[object, object], ...]


@dataclass(frozen=True)
class AreaOperation(SourceLocation):
    method: str
    arguments: tuple[object, ...] = ()
    keyword_arguments: FrozenMap = FrozenMap(())


@dataclass(frozen=True)
class CompilationDiagnostic(SourceLocation):
    code: str
    message: str


@dataclass(frozen=True)
class ZoneSourceDefinition:
    source_path: str
    zone_id: str
    operations: tuple[AreaOperation, ...]


@dataclass(frozen=True)
class AreaCompilationResult:
    definition: ZoneSourceDefinition | None
    diagnostics: tuple[CompilationDiagnostic, ...]


@dataclass(frozen=True)
class AreaSourceAudit:
    definitions: tuple[ZoneSourceDefinition, ...]
    diagnostics: tuple[CompilationDiagnostic, ...]


@dataclass(frozen=True)
class WorldManifest:
    schema_version: str
    zones: tuple[ZoneSourceDefinition, ...]
    manifest_hash: str


@dataclass(frozen=True)
class WorldManifestCompilation:
    manifest: WorldManifest | None
    diagnostics: tuple[CompilationDiagnostic, ...]


@dataclass(frozen=True)
class WorldContentChange:
    action: str
    zone_id: str
    entity_type: str
    entity_id: str
    before: AreaOperation | None
    after: AreaOperation | None
    destructive: bool
    player_impact: tuple[str, ...]


@dataclass(frozen=True)
class WorldChangePlan:
    previous_manifest_hash: str
    target_manifest_hash: str
    changes: tuple[WorldContentChange, ...]


@dataclass(frozen=True)
class WorldChangePlanningResult:
    plan: WorldChangePlan | None
    diagnostics: tuple[CompilationDiagnostic, ...]


class ManifestIntegrityError(ValueError):
    """Raised when durable manifest evidence does not match its semantic hash."""


def _frozen_map_get(mapping: FrozenMap, key: str, default: object = None) -> object:
    return dict(mapping.entries).get(key, default)


def _thaw(value: object) -> object:
    if isinstance(value, FrozenMap):
        return {key: _thaw(item) for key, item in value.entries}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


def _operation_value(
    operation: AreaOperation,
    position: int,
    keyword: str,
    default: object = None,
) -> object:
    if len(operation.arguments) > position:
        return operation.arguments[position]
    return _frozen_map_get(operation.keyword_arguments, keyword, default)


def _diagnostic(
    operation: AreaOperation, code: str, message: str
) -> CompilationDiagnostic:
    return CompilationDiagnostic(
        source_path=operation.source_path,
        line=operation.line,
        column=operation.column,
        code=code,
        message=message,
    )


def _validate_relationship_faction(
    operation: AreaOperation,
    faction_id: object,
    diagnostics: list[CompilationDiagnostic],
) -> None:
    """Require canonical, registered IDs in relationship-bearing source."""
    if faction_id in (None, ""):
        return
    try:
        canonical = canonicalize_faction_id(faction_id)
    except FactionIdentityError as exc:
        diagnostics.append(
            _diagnostic(operation, "unknown-faction-id", str(exc))
        )
        return
    if canonical != faction_id:
        diagnostics.append(
            _diagnostic(
                operation,
                "noncanonical-faction-id",
                f"Faction relationship ID '{faction_id}' must be '{canonical}'.",
            )
        )


def _attribute_chain(node: ast.AST) -> tuple[str, ...]:
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return tuple(reversed(parts))


class _NonLiteralAreaValue(ValueError):
    pass


class _AreaAuthorityVisitor(ast.NodeVisitor):
    def __init__(self, source_path: str):
        self.source_path = source_path
        self.builder_names: set[str] = set()
        self.builder_nodes: list[ast.Call] = []
        self.zone_ids: list[str] = []
        self.literal_bindings: dict[str, object] = {}
        self.symbolic_bindings: dict[str, SymbolicReference] = {}
        self.operations: list[AreaOperation] = []
        self.diagnostics: list[CompilationDiagnostic] = []
        self._reported_nodes: set[int] = set()

    def _location(self, node: ast.AST) -> dict[str, object]:
        return {
            "source_path": self.source_path,
            "line": node.lineno,
            "column": node.col_offset + 1,
        }

    def _report_forbidden(self, node: ast.AST, chain: tuple[str, ...]) -> None:
        if id(node) in self._reported_nodes:
            return
        self._reported_nodes.add(id(node))
        handler = next(part for part in chain if part in FORBIDDEN_RUNTIME_HANDLERS)
        self.diagnostics.append(
            CompilationDiagnostic(
                **self._location(node),
                code="forbidden-runtime-mutation",
                message=(
                    f"Direct '.{handler}' mutation is outside the literal AreaBuilder "
                    "authority contract. Add or use a supported area operation."
                ),
            )
        )

    def _check_mutation_target(self, node: ast.AST) -> None:
        chain = _attribute_chain(node)
        if FORBIDDEN_RUNTIME_HANDLERS.intersection(chain):
            self._report_forbidden(node, chain)

    def _freeze_literal(self, value: object) -> object:
        if isinstance(value, dict):
            return FrozenMap(
                tuple(
                    (self._freeze_literal(key), self._freeze_literal(item))
                    for key, item in value.items()
                )
            )
        if isinstance(value, (list, tuple)):
            return tuple(self._freeze_literal(item) for item in value)
        if isinstance(value, (set, frozenset)):
            return tuple(
                sorted(
                    (self._freeze_literal(item) for item in value),
                    key=repr,
                )
            )
        if value is None or isinstance(value, (bool, float, int, str)):
            return value
        raise _NonLiteralAreaValue(f"unsupported literal value {type(value).__name__}")

    def _compile_value(self, node: ast.AST) -> object:
        if isinstance(node, ast.Name):
            if node.id in self.symbolic_bindings:
                return self.symbolic_bindings[node.id]
            if node.id in self.literal_bindings:
                return self.literal_bindings[node.id]
            raise _NonLiteralAreaValue(f"unresolved name '{node.id}'")
        try:
            return self._freeze_literal(ast.literal_eval(node))
        except (ValueError, TypeError) as exc:
            raise _NonLiteralAreaValue(
                f"{type(node).__name__} is not a literal or symbolic reference"
            ) from exc

    def _builder_method(self, node: ast.AST) -> str | None:
        if not isinstance(node, ast.Call):
            return None
        chain = _attribute_chain(node.func)
        if len(chain) == 2 and chain[0] in self.builder_names:
            return chain[1]
        return None

    def _register_builder_result(self, node: ast.Assign) -> None:
        method = self._builder_method(node.value)
        if method not in {"mob", "npc", "room"} or not isinstance(node.value, ast.Call):
            return
        target = next(
            (target for target in node.targets if isinstance(target, ast.Name)),
            None,
        )
        if target is None:
            return
        key_index = 1 if method == "npc" else 0
        if len(node.value.args) <= key_index:
            return
        try:
            key = self._compile_value(node.value.args[key_index])
        except _NonLiteralAreaValue:
            return
        if isinstance(key, str) and key:
            self.symbolic_bindings[target.id] = SymbolicReference(method, key)

    def visit_Assign(self, node: ast.Assign) -> None:
        if (
            isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "AreaBuilder"
        ):
            self.builder_nodes.append(node.value)
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.builder_names.add(target.id)
            if node.value.args:
                try:
                    zone_id = self._compile_value(node.value.args[0])
                except _NonLiteralAreaValue:
                    zone_id = None
                if isinstance(zone_id, str) and zone_id:
                    self.zone_ids.append(zone_id)
        elif len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                literal = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                literal = None
            if literal is not None:
                self.literal_bindings[node.targets[0].id] = self._freeze_literal(
                    literal
                )
            self._register_builder_result(node)
        for target in node.targets:
            self._check_mutation_target(target)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self._check_mutation_target(node.target)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self._check_mutation_target(node.target)
        self.generic_visit(node)

    def visit_Delete(self, node: ast.Delete) -> None:
        for target in node.targets:
            self._check_mutation_target(target)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        chain = _attribute_chain(node.func)
        if FORBIDDEN_RUNTIME_HANDLERS.intersection(chain):
            self._report_forbidden(node, chain)
        elif len(chain) == 2 and chain[0] in self.builder_names:
            method = chain[1]
            if method not in SUPPORTED_AREA_OPERATIONS:
                self.diagnostics.append(
                    CompilationDiagnostic(
                        **self._location(node),
                        code="unsupported-area-operation",
                        message=f"Unsupported AreaBuilder operation 'area.{method}()'.",
                    )
                )
            else:
                try:
                    arguments = tuple(self._compile_value(arg) for arg in node.args)
                    if any(keyword.arg is None for keyword in node.keywords):
                        raise _NonLiteralAreaValue("keyword unpacking is not supported")
                    keyword_arguments = FrozenMap(
                        tuple(
                            sorted(
                                (
                                    (keyword.arg, self._compile_value(keyword.value))
                                    for keyword in node.keywords
                                    if keyword.arg is not None
                                ),
                                key=lambda item: item[0],
                            )
                        )
                    )
                except _NonLiteralAreaValue as exc:
                    self.diagnostics.append(
                        CompilationDiagnostic(
                            **self._location(node),
                            code="nonliteral-area-argument",
                            message=f"area.{method}() cannot compile: {exc}.",
                        )
                    )
                else:
                    self.operations.append(
                        AreaOperation(
                            **self._location(node),
                            method=method,
                            arguments=arguments,
                            keyword_arguments=keyword_arguments,
                        )
                    )
        self.generic_visit(node)


def compile_area_source(source: str, *, source_path: str) -> AreaCompilationResult:
    """Inventory literal operations without importing source or touching persistence."""

    try:
        tree = ast.parse(source, filename=source_path)
    except SyntaxError as exc:
        diagnostic = CompilationDiagnostic(
            source_path=source_path,
            line=exc.lineno or 1,
            column=exc.offset or 1,
            code="syntax-error",
            message=exc.msg,
        )
        return AreaCompilationResult(definition=None, diagnostics=(diagnostic,))

    visitor = _AreaAuthorityVisitor(source_path)
    visitor.visit(tree)
    if not visitor.zone_ids:
        builder_node = visitor.builder_nodes[0] if visitor.builder_nodes else tree
        visitor.diagnostics.append(
            CompilationDiagnostic(
                source_path=source_path,
                line=getattr(builder_node, "lineno", 1),
                column=getattr(builder_node, "col_offset", 0) + 1,
                code="missing-zone-id",
                message="AreaBuilder requires one non-empty literal zone_id.",
            )
        )
    diagnostics = tuple(
        sorted(
            visitor.diagnostics, key=lambda item: (item.line, item.column, item.code)
        )
    )
    definition = None
    if not diagnostics:
        definition = ZoneSourceDefinition(
            source_path=source_path,
            zone_id=visitor.zone_ids[0],
            operations=tuple(visitor.operations),
        )
    return AreaCompilationResult(definition=definition, diagnostics=diagnostics)


def audit_area_sources(areas_dir: Path) -> AreaSourceAudit:
    """Compile every tracked-style Python area source in deterministic path order."""

    definitions: list[ZoneSourceDefinition] = []
    diagnostics: list[CompilationDiagnostic] = []
    project_root = areas_dir.parents[1]
    for path in sorted(areas_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        source_path = path.relative_to(project_root).as_posix()
        result = compile_area_source(path.read_text(), source_path=source_path)
        if result.definition is not None:
            definitions.append(result.definition)
        diagnostics.extend(result.diagnostics)
    return AreaSourceAudit(
        definitions=tuple(definitions),
        diagnostics=tuple(diagnostics),
    )


def _canonical_manifest_value(value: object) -> object:
    if isinstance(value, SymbolicReference):
        return {"$ref": {"kind": value.kind, "key": value.key}}
    if isinstance(value, FrozenMap):
        return {
            str(key): _canonical_manifest_value(item) for key, item in value.entries
        }
    if isinstance(value, tuple):
        return [_canonical_manifest_value(item) for item in value]
    if value is None or isinstance(value, (bool, float, int, str)):
        return value
    raise TypeError(f"Unsupported manifest value: {type(value).__name__}")


def _semantic_manifest_payload(
    definitions: tuple[ZoneSourceDefinition, ...],
) -> dict[str, object]:
    zones: list[dict[str, object]] = []
    for definition in definitions:
        operations = []
        for operation in definition.operations:
            if operation.method == "build":
                continue
            operations.append(
                {
                    "method": operation.method,
                    "arguments": _canonical_manifest_value(operation.arguments),
                    "keyword_arguments": _canonical_manifest_value(
                        operation.keyword_arguments
                    ),
                }
            )
        zones.append(
            {
                "source_path": definition.source_path,
                "zone_id": definition.zone_id,
                "operations": operations,
            }
        )
    return {
        "schema_version": "soravelon.world-content.v1",
        "zones": zones,
    }


def _validate_world_definitions(
    definitions: tuple[ZoneSourceDefinition, ...],
) -> tuple[CompilationDiagnostic, ...]:
    diagnostics: list[CompilationDiagnostic] = []
    rooms_by_zone: dict[str, set[str]] = {}
    social_node_keys: set[str] = set()
    authored_exits: set[tuple[str, str, str]] = set()
    npc_ids: set[str] = set()
    quest_ids: set[str] = set()
    authored_item_ids: set[str] = set()
    practice_ids: set[str] = set()
    stable_id_owners: dict[tuple[str, str], str] = {}
    inverse_directions = {
        "north": "south",
        "south": "north",
        "east": "west",
        "west": "east",
        "northeast": "southwest",
        "southwest": "northeast",
        "northwest": "southeast",
        "southeast": "northwest",
        "up": "down",
        "down": "up",
        "in": "out",
        "out": "in",
    }

    for definition in definitions:
        room_ids = {
            operation.arguments[0]
            for operation in definition.operations
            if operation.method == "room"
            and operation.arguments
            and isinstance(operation.arguments[0], str)
        }
        rooms_by_zone[definition.zone_id] = room_ids
        for operation in definition.operations:
            stable_id_specs = {
                "npc": (1, "duplicate-npc-id"),
                "quest": (0, "duplicate-quest-id"),
                "item": (0, "duplicate-item-id"),
                "named_mob": (0, "duplicate-named-mob-id"),
                "flight_point": (1, "duplicate-flight-point-id"),
            }
            stable_spec = stable_id_specs.get(operation.method)
            if stable_spec is not None:
                position, duplicate_code = stable_spec
                if len(operation.arguments) > position:
                    stable_id = operation.arguments[position]
                    if isinstance(stable_id, str):
                        if stable_id != stable_id.casefold():
                            diagnostics.append(
                                _diagnostic(
                                    operation,
                                    "noncanonical-identifier",
                                    f"Runtime identity '{stable_id}' must use canonical lowercase.",
                                )
                            )
                        owner_key = (operation.method, stable_id)
                        previous_source = stable_id_owners.get(owner_key)
                        if previous_source is not None:
                            diagnostics.append(
                                _diagnostic(
                                    operation,
                                    duplicate_code,
                                    f"{operation.method} ID '{stable_id}' is already authored by {previous_source}.",
                                )
                            )
                        else:
                            stable_id_owners[owner_key] = operation.source_path
            if operation.method == "room" and operation.arguments:
                room_id = operation.arguments[0]
                if isinstance(room_id, str) and room_id != room_id.casefold():
                    diagnostics.append(
                        _diagnostic(
                            operation,
                            "noncanonical-identifier",
                            f"Runtime identity '{room_id}' must use canonical lowercase.",
                        )
                    )
            if operation.method == "npc" and len(operation.arguments) > 1:
                npc_id = operation.arguments[1]
                if isinstance(npc_id, str):
                    npc_ids.add(npc_id)
            elif operation.method == "quest" and operation.arguments:
                quest_id = operation.arguments[0]
                if isinstance(quest_id, str):
                    quest_ids.add(quest_id)
            elif operation.method == "item" and operation.arguments:
                item_id = operation.arguments[0]
                if isinstance(item_id, str):
                    authored_item_ids.add(item_id)
            elif operation.method == "practice_opportunity" and operation.arguments:
                practice_id = operation.arguments[0]
                if isinstance(practice_id, str):
                    practice_ids.add(practice_id)
            if operation.method == "exit" and len(operation.arguments) >= 3:
                source, destination, direction = operation.arguments[:3]
                if isinstance(source, SymbolicReference) and isinstance(direction, str):
                    source_key = f"{definition.zone_id}:{source.key}"
                    destination_key = (
                        f"{definition.zone_id}:{destination.key}"
                        if isinstance(destination, SymbolicReference)
                        else destination
                    )
                    if isinstance(destination_key, str):
                        authored_exits.add((source_key, destination_key, direction))
            if operation.method != "social_node" or len(operation.arguments) < 2:
                continue
            node_type, identifier = operation.arguments[:2]
            if node_type not in NODE_TYPES:
                diagnostics.append(
                    _diagnostic(
                        operation,
                        "unsupported-social-node-type",
                        f"Social node type '{node_type}' is not in the approved taxonomy.",
                    )
                )
            if isinstance(node_type, str) and isinstance(identifier, str):
                social_node_keys.add(f"{node_type}:{identifier}")

    all_room_ids = set().union(*rooms_by_zone.values()) if rooms_by_zone else set()
    objective_targets = {
        "kill": set(MOB_TEMPLATES),
        "collect": set(CATALOG) | authored_item_ids | set(MATERIAL_REGISTRY),
        "investigate": all_room_ids,
        "deliver": npc_ids | all_room_ids,
        "talk_to": npc_ids,
        "practice": practice_ids,
    }

    for definition in definitions:
        room_ids = rooms_by_zone[definition.zone_id]
        exit_destinations: dict[tuple[str, str], object] = {}
        zone_operation = next(
            operation
            for operation in definition.operations
            if operation.method == "zone"
        )
        zone_kwargs = _frozen_map_get(
            zone_operation.keyword_arguments, "has_node", False
        )
        for operation in definition.operations:
            if operation.method in {"npc", "vendor"}:
                _validate_relationship_faction(
                    operation,
                    _frozen_map_get(operation.keyword_arguments, "faction"),
                    diagnostics,
                )

            if operation.method == "node" and not zone_kwargs:
                diagnostics.append(
                    _diagnostic(
                        operation,
                        "inactive-node-operation",
                        "area.node() requires zone(has_node=True) so runtime materializes it.",
                    )
                )
            if operation.method in {"spawn", "named_mob"}:
                mob_position = 1 if operation.method == "spawn" else 0
                mob_id = _operation_value(operation, mob_position, "mob")
                if mob_id not in MOB_TEMPLATES:
                    diagnostics.append(
                        _diagnostic(
                            operation,
                            "unknown-mob-template",
                            f"Mob template '{mob_id}' is not registered.",
                        )
                    )

            if operation.method == "vendor":
                for field_name in ("item_ids", "exclude_item_ids"):
                    item_ids = _frozen_map_get(
                        operation.keyword_arguments, field_name, ()
                    )
                    for item_id in item_ids if isinstance(item_ids, tuple) else ():
                        if item_id not in CATALOG:
                            diagnostics.append(
                                _diagnostic(
                                    operation,
                                    "unknown-item-id",
                                    f"Vendor item '{item_id}' is not in the canonical catalog.",
                                )
                            )

            if operation.method == "material" and operation.arguments:
                material_id = operation.arguments[0]
                if material_id not in MATERIAL_REGISTRY:
                    diagnostics.append(
                        _diagnostic(
                            operation,
                            "unknown-material-id",
                            f"Material '{material_id}' is not registered.",
                        )
                    )
                else:
                    material = MATERIAL_REGISTRY[material_id]
                    tier = _frozen_map_get(
                        operation.keyword_arguments,
                        "tier",
                        1,
                    )
                    if tier != material["tier"]:
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "material-tier-mismatch",
                                f"Material '{material_id}' is tier {material['tier']}, not {tier}.",
                            )
                        )
                    absorbed_property = _frozen_map_get(
                        operation.keyword_arguments,
                        "absorbed_property",
                    )
                    if absorbed_property is not None and (
                        not isinstance(absorbed_property, str)
                        or not absorbed_property.strip()
                    ):
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "invalid-material-property",
                                "Absorbed material properties must be non-empty identifiers.",
                            )
                        )
                    profession_bonus = _thaw(
                        _frozen_map_get(
                            operation.keyword_arguments,
                            "profession_bonus",
                            FrozenMap(()),
                        )
                    )
                    if not isinstance(profession_bonus, dict):
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "invalid-material-profession-bonus",
                                "Material profession_bonus must be a literal map.",
                            )
                        )
                    else:
                        for skill_id, bonus in profession_bonus.items():
                            if skill_id not in SKILL_DEFINITIONS:
                                diagnostics.append(
                                    _diagnostic(
                                        operation,
                                        "unknown-material-profession",
                                        f"Material bonus skill '{skill_id}' is not registered.",
                                    )
                                )
                            if (
                                not isinstance(bonus, Real)
                                or isinstance(bonus, bool)
                                or not 0 < bonus <= 0.25
                            ):
                                diagnostics.append(
                                    _diagnostic(
                                        operation,
                                        "invalid-material-profession-bonus",
                                        "Material profession bonuses must be greater than 0 and at most 0.25.",
                                    )
                                )

            if operation.method == "exit" and len(operation.arguments) >= 3:
                source, destination, direction = operation.arguments[:3]
                if direction not in VALID_DIRECTIONS:
                    diagnostics.append(
                        _diagnostic(
                            operation,
                            "unsupported-exit-direction",
                            f"Exit direction '{direction}' is not supported.",
                        )
                    )
                if isinstance(source, SymbolicReference):
                    key = (source.key, str(direction))
                    previous = exit_destinations.get(key)
                    if previous is not None and previous != destination:
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "duplicate-exit-direction",
                                f"Room '{source.key}' has multiple '{direction}' destinations.",
                            )
                        )
                    exit_destinations[key] = destination
                if isinstance(destination, str):
                    parts = destination.split(":", 1)
                    target_rooms = (
                        rooms_by_zone.get(parts[0]) if len(parts) == 2 else None
                    )
                    if target_rooms is None or parts[1] not in target_rooms:
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "unresolved-cross-zone-room",
                                f"Cross-zone room '{destination}' is not authored in this manifest.",
                            )
                        )

                if (
                    isinstance(source, SymbolicReference)
                    and isinstance(direction, str)
                    and not _frozen_map_get(
                        operation.keyword_arguments, "one_way", False
                    )
                ):
                    source_key = f"{definition.zone_id}:{source.key}"
                    destination_key = (
                        f"{definition.zone_id}:{destination.key}"
                        if isinstance(destination, SymbolicReference)
                        else destination
                    )
                    inverse = inverse_directions.get(direction)
                    if (
                        isinstance(destination_key, str)
                        and inverse is not None
                        and (destination_key, source_key, inverse) not in authored_exits
                    ):
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "missing-reciprocal-intent",
                                "Exit has no inverse edge; declare one_way=True if this is intentional.",
                            )
                        )

            if operation.method == "gathering_pool":
                authored_rooms = _frozen_map_get(
                    operation.keyword_arguments, "rooms", ()
                )
                for room_id in (
                    authored_rooms if isinstance(authored_rooms, tuple) else ()
                ):
                    if room_id not in room_ids:
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "unresolved-local-room",
                                f"Room '{room_id}' is not authored in zone '{definition.zone_id}'.",
                            )
                        )
                materials = _operation_value(operation, 2, "materials", ())
                for material_id in materials if isinstance(materials, tuple) else ():
                    if material_id not in MATERIAL_REGISTRY:
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "unknown-material-id",
                                f"Gathering material '{material_id}' is not registered.",
                            )
                        )

            if operation.method == "quest":
                quest_giver = _frozen_map_get(
                    operation.keyword_arguments, "quest_giver"
                )
                if quest_giver not in npc_ids:
                    diagnostics.append(
                        _diagnostic(
                            operation,
                            "unresolved-quest-giver",
                            f"Quest giver '{quest_giver}' is not authored in this manifest.",
                        )
                    )
                referenced_quests = list(
                    _frozen_map_get(
                        operation.keyword_arguments, "prerequisite_quests", ()
                    )
                )
                next_quest_id = _frozen_map_get(
                    operation.keyword_arguments, "next_quest_id"
                )
                if next_quest_id:
                    referenced_quests.append(next_quest_id)
                for quest_id in referenced_quests:
                    if quest_id not in quest_ids:
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "unresolved-quest-id",
                                f"Quest reference '{quest_id}' is not authored in this manifest.",
                            )
                        )
                objectives = _thaw(
                    _frozen_map_get(operation.keyword_arguments, "objectives", ())
                )
                if not objectives:
                    objectives = [
                        {
                            "type": _frozen_map_get(
                                operation.keyword_arguments, "objective_type"
                            ),
                            "target": _frozen_map_get(
                                operation.keyword_arguments, "objective_target"
                            ),
                        }
                    ]
                for objective in objectives if isinstance(objectives, list) else ():
                    if not isinstance(objective, dict):
                        continue
                    authored_type = objective.get("type")
                    objective_type = OBJECTIVE_TYPE_ALIASES.get(
                        authored_type, authored_type
                    )
                    if objective_type not in OBJECTIVE_TYPES | {"practice"}:
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "unknown-objective-type",
                                f"Objective type '{authored_type}' has no runtime progress path.",
                            )
                        )
                        continue
                    allowed_targets = objective_targets.get(objective_type)
                    target = objective.get("target")
                    if allowed_targets is not None and target not in allowed_targets:
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "unresolved-objective-target",
                                f"Objective target '{target}' does not resolve for type '{authored_type}'.",
                            )
                        )

            actions: object = ()
            if operation.method == "quest":
                actions = _frozen_map_get(operation.keyword_arguments, "rewards", ())
            elif operation.method == "trigger":
                actions = _operation_value(operation, 2, "actions", ())
            elif operation.method == "custom_command":
                action = _operation_value(operation, 2, "action_dict")
                actions = (action,) if action is not None else ()
            for action in actions if isinstance(actions, tuple) else ():
                action_dict = _thaw(action)
                if not isinstance(action_dict, dict):
                    continue
                action_type = action_dict.get("action_type")
                if action_type not in ACTION_HANDLERS:
                    diagnostics.append(
                        _diagnostic(
                            operation,
                            "unknown-action-type",
                            f"Action type '{action_type}' is not registered.",
                        )
                    )
                elif action_type == "give_skill_xp":
                    if action_dict.get("skill_id") not in SKILL_DEFINITIONS:
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "unknown-skill-id",
                                f"Skill '{action_dict.get('skill_id')}' is not registered.",
                            )
                        )
                    count = action_dict.get("count", 1)
                    if (
                        isinstance(count, bool)
                        or not isinstance(count, Integral)
                        or count <= 0
                    ):
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "invalid-skill-award-count",
                                "Quest skill award count must be a positive integer.",
                            )
                        )
                elif action_type == "modify_standing":
                    _validate_relationship_faction(
                        operation,
                        action_dict.get("faction_id"),
                        diagnostics,
                    )

            if operation.method == "social_edge" and len(operation.arguments) >= 2:
                source_key, target_key = operation.arguments[:2]
                edge_type = _frozen_map_get(operation.keyword_arguments, "edge_type")
                if edge_type not in EDGE_TYPES:
                    diagnostics.append(
                        _diagnostic(
                            operation,
                            "unsupported-social-edge-type",
                            f"Social edge type '{edge_type}' is not in the approved taxonomy.",
                        )
                    )
                for node_key in (source_key, target_key):
                    if node_key not in social_node_keys:
                        diagnostics.append(
                            _diagnostic(
                                operation,
                                "unresolved-social-node",
                                f"Social node '{node_key}' is not authored in this manifest.",
                            )
                        )

    return tuple(
        sorted(
            diagnostics,
            key=lambda item: (item.source_path, item.line, item.column, item.code),
        )
    )


def compile_world_sources(
    sources: Mapping[str, str],
) -> WorldManifestCompilation:
    """Compile deterministic source text into one immutable semantic manifest."""

    definitions: list[ZoneSourceDefinition] = []
    diagnostics: list[CompilationDiagnostic] = []
    zone_sources: dict[str, str] = {}
    for source_path, source in sorted(sources.items()):
        result = compile_area_source(source, source_path=source_path)
        diagnostics.extend(result.diagnostics)
        if result.definition is None:
            continue
        previous_source = zone_sources.get(result.definition.zone_id)
        if previous_source is not None:
            diagnostics.append(
                CompilationDiagnostic(
                    source_path=source_path,
                    line=1,
                    column=1,
                    code="duplicate-zone-id",
                    message=(
                        f"zone_id '{result.definition.zone_id}' is already owned by "
                        f"{previous_source}."
                    ),
                )
            )
            continue
        zone_sources[result.definition.zone_id] = source_path
        definitions.append(result.definition)

    ordered_diagnostics = tuple(
        sorted(
            diagnostics,
            key=lambda item: (item.source_path, item.line, item.column, item.code),
        )
    )
    if ordered_diagnostics:
        return WorldManifestCompilation(manifest=None, diagnostics=ordered_diagnostics)

    frozen_definitions = tuple(definitions)
    semantic_diagnostics = _validate_world_definitions(frozen_definitions)
    if semantic_diagnostics:
        return WorldManifestCompilation(manifest=None, diagnostics=semantic_diagnostics)
    payload = _semantic_manifest_payload(frozen_definitions)
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    manifest = WorldManifest(
        schema_version="soravelon.world-content.v1",
        zones=frozen_definitions,
        manifest_hash=hashlib.sha256(canonical).hexdigest(),
    )
    return WorldManifestCompilation(manifest=manifest, diagnostics=())


def compile_world_manifest(areas_dir: Path) -> WorldManifestCompilation:
    """Compile every literal Python zone source under one directory."""

    project_root = areas_dir.parents[1]
    sources = {
        path.relative_to(project_root).as_posix(): path.read_text()
        for path in sorted(areas_dir.glob("*.py"))
        if not path.name.startswith("_")
    }
    return compile_world_sources(sources)


def _reference_key(value: object) -> str | None:
    if isinstance(value, SymbolicReference):
        return value.key
    if isinstance(value, str):
        return value
    return None


def _operation_identity(operation: AreaOperation) -> tuple[str, str] | None:
    if operation.method == "build":
        return ("build", "build")
    direct_id_positions = {
        "flight_point": 1,
        "item": 0,
        "lore_fragment": 0,
        "material": 0,
        "mob": 0,
        "named_mob": 0,
        "npc": 1,
        "practice_opportunity": 0,
        "quest": 0,
        "room": 0,
    }
    position = direct_id_positions.get(operation.method)
    if position is not None and len(operation.arguments) > position:
        value = operation.arguments[position]
        if isinstance(value, str):
            return (operation.method, value)

    if operation.method in {"node", "zone"}:
        return (operation.method, operation.method)
    if operation.method == "exit" and len(operation.arguments) >= 3:
        source = _reference_key(operation.arguments[0])
        direction = operation.arguments[2]
        if source and isinstance(direction, str):
            return ("exit", f"{source}:{direction}")
    if operation.method == "spawn" and len(operation.arguments) >= 2:
        room = _reference_key(operation.arguments[0])
        mob = operation.arguments[1]
        if room and isinstance(mob, str):
            return ("spawn", f"{room}:{mob}")
    if operation.method in {"initial_room_state", "medic", "vendor"}:
        target = _reference_key(_operation_value(operation, 0, "target"))
        if target:
            return (operation.method, target)
    if operation.method == "room_role" and len(operation.arguments) >= 2:
        room = _reference_key(operation.arguments[0])
        role = operation.arguments[1]
        if room and isinstance(role, str):
            return ("room_role", f"{room}:{role}")
    if operation.method == "loot_table_override":
        mob_type = _operation_value(operation, 0, "mob_type")
        if isinstance(mob_type, str):
            return ("loot_table_override", mob_type)
    if operation.method == "patrol":
        mob_key = _operation_value(operation, 0, "mob_key")
        if isinstance(mob_key, str):
            return ("patrol", mob_key)
    if operation.method == "trigger":
        trigger_id = _frozen_map_get(operation.keyword_arguments, "trigger_id")
        if isinstance(trigger_id, str) and trigger_id:
            return ("trigger", trigger_id)
    if operation.method == "custom_command" and len(operation.arguments) >= 2:
        target = _reference_key(operation.arguments[0])
        key = operation.arguments[1]
        if target and isinstance(key, str):
            return ("custom_command", f"{target}:{key}")
    if operation.method == "gathering_pool":
        pool_type = _operation_value(operation, 0, "pool_type")
        if isinstance(pool_type, str):
            return ("gathering_pool", pool_type)
    if operation.method == "flight_route" and len(operation.arguments) >= 2:
        first, second = operation.arguments[:2]
        if isinstance(first, str) and isinstance(second, str):
            return ("flight_route", f"{first}:{second}")
    if operation.method == "social_node" and len(operation.arguments) >= 2:
        node_type, identifier = operation.arguments[:2]
        if isinstance(node_type, str) and isinstance(identifier, str):
            return ("social_node", f"{node_type}:{identifier}")
    if operation.method == "social_edge" and len(operation.arguments) >= 2:
        source, target = operation.arguments[:2]
        edge_type = _frozen_map_get(operation.keyword_arguments, "edge_type")
        if all(isinstance(value, str) for value in (source, target, edge_type)):
            return ("social_edge", f"{source}->{target}:{edge_type}")
    return None


def _operation_semantic_value(operation: AreaOperation) -> tuple[object, ...]:
    return (
        operation.method,
        operation.arguments,
        operation.keyword_arguments,
    )


def _change_impact(entity_type: str, action: str) -> tuple[bool, tuple[str, ...]]:
    if action == "move":
        impacts = {
            "flight_point": ("travel-discovery",),
            "mob": ("encounter-location",),
            "named_mob": (
                "encounter-location",
                "prestige-target",
            ),
            "npc": ("npc-location", "quest-dialogue-routing"),
        }
        return False, impacts.get(entity_type, ("authored-location",))
    if action != "delete":
        return False, ()
    impacts = {
        "exit": ("connected-navigation",),
        "flight_point": ("travel-discovery",),
        "item": ("item-source", "inventory-expectations"),
        "named_mob": ("encounter", "prestige-target"),
        "npc": ("relationship-memory", "quest-dialogue-routing"),
        "quest": ("active-quest-progress",),
        "room": ("occupied-room", "contained-objects", "connected-navigation"),
        "social_edge": ("rumor-routing",),
        "social_node": ("relationship-memory", "rumor-routing"),
        "zone": ("world-region", "all-zone-content"),
    }
    return True, impacts.get(entity_type, ("authored-runtime-state",))


def _manifest_operation_index(
    manifest: WorldManifest,
) -> tuple[
    dict[tuple[str, str, str], AreaOperation],
    tuple[CompilationDiagnostic, ...],
]:
    index: dict[tuple[str, str, str], AreaOperation] = {}
    diagnostics: list[CompilationDiagnostic] = []
    for definition in manifest.zones:
        for operation in definition.operations:
            if operation.method == "build":
                continue
            identity = _operation_identity(operation)
            if identity is None:
                diagnostics.append(
                    _diagnostic(
                        operation,
                        "unmodelled-change-identity",
                        f"area.{operation.method}() has no stable change identity.",
                    )
                )
                continue
            entity_type, entity_id = identity
            key = (definition.zone_id, entity_type, entity_id)
            if key in index:
                diagnostics.append(
                    _diagnostic(
                        operation,
                        "duplicate-change-identity",
                        f"Change identity '{entity_type}:{entity_id}' is duplicated in zone '{definition.zone_id}'.",
                    )
                )
                continue
            index[key] = operation
    return index, tuple(
        sorted(
            diagnostics,
            key=lambda item: (item.source_path, item.line, item.column, item.code),
        )
    )


def plan_world_changes(
    previous: WorldManifest, target: WorldManifest
) -> WorldChangePlanningResult:
    """Build a pure, immutable and fail-closed semantic change plan."""

    previous_index, previous_diagnostics = _manifest_operation_index(previous)
    target_index, target_diagnostics = _manifest_operation_index(target)
    diagnostics = tuple(
        sorted(
            previous_diagnostics + target_diagnostics,
            key=lambda item: (item.source_path, item.line, item.column, item.code),
        )
    )
    if diagnostics:
        return WorldChangePlanningResult(plan=None, diagnostics=diagnostics)

    changes: list[WorldContentChange] = []
    for key in sorted(set(previous_index) | set(target_index)):
        zone_id, entity_type, entity_id = key
        before = previous_index.get(key)
        after = target_index.get(key)
        if before is None:
            action = "create"
        elif after is None:
            action = "delete"
        elif _operation_semantic_value(before) == _operation_semantic_value(after):
            continue
        else:
            move_positions = {
                "flight_point": 0,
                "mob": 1,
                "named_mob": 1,
                "npc": 0,
            }
            move_position = move_positions.get(entity_type)
            action = "update"
            if (
                move_position is not None
                and len(before.arguments) > move_position
                and len(after.arguments) > move_position
                and before.arguments[move_position] != after.arguments[move_position]
            ):
                action = "move"
        destructive, player_impact = _change_impact(entity_type, action)
        changes.append(
            WorldContentChange(
                action=action,
                zone_id=zone_id,
                entity_type=entity_type,
                entity_id=entity_id,
                before=before,
                after=after,
                destructive=destructive,
                player_impact=player_impact,
            )
        )
    return WorldChangePlanningResult(
        plan=WorldChangePlan(
            previous_manifest_hash=previous.manifest_hash,
            target_manifest_hash=target.manifest_hash,
            changes=tuple(changes),
        ),
        diagnostics=(),
    )


def _encode_stored_value(value: object) -> object:
    if isinstance(value, SymbolicReference):
        return {"type": "reference", "kind": value.kind, "key": value.key}
    if isinstance(value, FrozenMap):
        return {
            "type": "map",
            "entries": [
                [_encode_stored_value(key), _encode_stored_value(item)]
                for key, item in value.entries
            ],
        }
    if isinstance(value, tuple):
        return {
            "type": "tuple",
            "items": [_encode_stored_value(item) for item in value],
        }
    if value is None or isinstance(value, (bool, float, int, str)):
        return value
    raise TypeError(f"Unsupported stored manifest value: {type(value).__name__}")


def _decode_stored_value(value: object) -> object:
    if not isinstance(value, dict):
        return value
    value_type = value.get("type")
    if value_type == "reference":
        return SymbolicReference(kind=value["kind"], key=value["key"])
    if value_type == "map":
        return FrozenMap(
            tuple(
                (
                    _decode_stored_value(entry[0]),
                    _decode_stored_value(entry[1]),
                )
                for entry in value["entries"]
            )
        )
    if value_type == "tuple":
        return tuple(_decode_stored_value(item) for item in value["items"])
    raise ManifestIntegrityError("Stored manifest contains an unknown value encoding.")


def serialize_world_manifest(manifest: WorldManifest) -> dict[str, object]:
    """Serialize a manifest losslessly for durable JSON storage."""

    return {
        "schema_version": manifest.schema_version,
        "manifest_hash": manifest.manifest_hash,
        "zones": [
            {
                "source_path": definition.source_path,
                "zone_id": definition.zone_id,
                "operations": [
                    {
                        "source_path": operation.source_path,
                        "line": operation.line,
                        "column": operation.column,
                        "method": operation.method,
                        "arguments": _encode_stored_value(operation.arguments),
                        "keyword_arguments": _encode_stored_value(
                            operation.keyword_arguments
                        ),
                    }
                    for operation in definition.operations
                ],
            }
            for definition in manifest.zones
        ],
    }


def deserialize_world_manifest(payload: Mapping[str, object]) -> WorldManifest:
    """Restore durable manifest evidence and verify its semantic integrity."""

    try:
        definitions = tuple(
            ZoneSourceDefinition(
                source_path=zone["source_path"],
                zone_id=zone["zone_id"],
                operations=tuple(
                    AreaOperation(
                        source_path=operation["source_path"],
                        line=operation["line"],
                        column=operation["column"],
                        method=operation["method"],
                        arguments=_decode_stored_value(operation["arguments"]),
                        keyword_arguments=_decode_stored_value(
                            operation["keyword_arguments"]
                        ),
                    )
                    for operation in zone["operations"]
                ),
            )
            for zone in payload["zones"]
        )
        schema_version = payload["schema_version"]
        stored_hash = payload["manifest_hash"]
    except (KeyError, TypeError, ValueError) as exc:
        raise ManifestIntegrityError(
            "Stored manifest has an invalid structure."
        ) from exc
    canonical = json.dumps(
        _semantic_manifest_payload(definitions),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    calculated_hash = hashlib.sha256(canonical).hexdigest()
    if calculated_hash != stored_hash:
        raise ManifestIntegrityError(
            "Stored manifest integrity hash does not match its semantic content."
        )
    if schema_version != "soravelon.world-content.v1":
        raise ManifestIntegrityError(
            f"Stored manifest schema '{schema_version}' is not supported."
        )
    return WorldManifest(
        schema_version=schema_version,
        zones=definitions,
        manifest_hash=stored_hash,
    )
