"""Pure, mutation-free authority checks for literal AreaBuilder source."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

SUPPORTED_AREA_OPERATIONS = frozenset(
    {
        "build",
        "custom_command",
        "exit",
        "flight_point",
        "flight_route",
        "gathering_pool",
        "item",
        "loot_table_override",
        "lore_fragment",
        "material",
        "mob",
        "named_mob",
        "node",
        "npc",
        "patrol",
        "practice_opportunity",
        "quest",
        "room",
        "social_edge",
        "social_node",
        "spawn",
        "trigger",
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
class AreaOperation(SourceLocation):
    method: str


@dataclass(frozen=True)
class CompilationDiagnostic(SourceLocation):
    code: str
    message: str


@dataclass(frozen=True)
class ZoneSourceDefinition:
    source_path: str
    operations: tuple[AreaOperation, ...]


@dataclass(frozen=True)
class AreaCompilationResult:
    definition: ZoneSourceDefinition | None
    diagnostics: tuple[CompilationDiagnostic, ...]


@dataclass(frozen=True)
class AreaSourceAudit:
    definitions: tuple[ZoneSourceDefinition, ...]
    diagnostics: tuple[CompilationDiagnostic, ...]


def _attribute_chain(node: ast.AST) -> tuple[str, ...]:
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return tuple(reversed(parts))


class _AreaAuthorityVisitor(ast.NodeVisitor):
    def __init__(self, source_path: str):
        self.source_path = source_path
        self.builder_names: set[str] = set()
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

    def visit_Assign(self, node: ast.Assign) -> None:
        if (
            isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "AreaBuilder"
        ):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.builder_names.add(target.id)
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
                self.operations.append(
                    AreaOperation(
                        **self._location(node),
                        method=method,
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
    diagnostics = tuple(
        sorted(
            visitor.diagnostics, key=lambda item: (item.line, item.column, item.code)
        )
    )
    definition = None
    if not diagnostics:
        definition = ZoneSourceDefinition(
            source_path=source_path,
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
