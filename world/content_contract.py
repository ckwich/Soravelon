"""Versioned offline contract generated from Soravelon content authority."""

from __future__ import annotations

import inspect
import json
from pathlib import Path

from world.action_vocabulary import ACTION_HANDLERS
from world.area_builder import AreaBuilder
from world.area_validator import (
    VALID_CONTINENTS,
    VALID_DIRECTIONS,
    VALID_FACTION_TERRITORIES,
    VALID_NODE_TYPES,
    VALID_ROOM_TYPES,
    VALID_ZONE_TYPES,
)
from world.content_compiler import (
    FORBIDDEN_RUNTIME_HANDLERS,
    SUPPORTED_AREA_OPERATIONS,
)
from world.item_catalog import CATALOG
from world.material_definitions import MATERIAL_REGISTRY
from world.mob_templates import MOB_TEMPLATES
from world.quest_engine import OBJECTIVE_TYPE_ALIASES, OBJECTIVE_TYPES
from world.skill_definitions import SKILL_DEFINITIONS
from world.social_taxonomy import EDGE_TYPES, NODE_TYPES

CONTRACT_VERSION = "1.0.0"
CONTRACT_SCHEMA = "soravelon.area-content-contract.v1"
DEFAULT_ARTIFACT_PATH = (
    Path(__file__).resolve().parents[1]
    / "contracts"
    / "soravelon-content-contract.v1.json"
)


def _json_default(value):
    if value is inspect.Parameter.empty:
        return None
    if value is None or isinstance(value, (bool, float, int, str)):
        return value
    if isinstance(value, (list, tuple)):
        return list(value)
    return repr(value)


def _operation_signature(method_name: str) -> dict[str, object]:
    signature = inspect.signature(getattr(AreaBuilder, method_name))
    parameters = []
    for parameter in signature.parameters.values():
        if parameter.name == "self":
            continue
        entry = {
            "name": parameter.name,
            "kind": parameter.kind.name.lower(),
            "required": parameter.default is inspect.Parameter.empty
            and parameter.kind
            not in {
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            },
        }
        if parameter.default is not inspect.Parameter.empty:
            entry["default"] = _json_default(parameter.default)
        parameters.append(entry)
    return {"parameters": parameters}


def build_content_contract() -> dict[str, object]:
    """Return the deterministic offline contract from live server authority."""

    operations = {
        method: _operation_signature(method)
        for method in sorted(SUPPORTED_AREA_OPERATIONS)
    }
    return {
        "contract_version": CONTRACT_VERSION,
        "schema": CONTRACT_SCHEMA,
        "grammar": {
            "builder_class": "world.area_builder.AreaBuilder",
            "supported_operations": operations,
            "forbidden_runtime_handlers": sorted(FORBIDDEN_RUNTIME_HANDLERS),
            "symbolic_reference_kinds": ["mob", "npc", "room"],
            "literal_value_schema": {
                "one_of": [
                    "null",
                    "boolean",
                    "number",
                    "string",
                    "literal-list",
                    "literal-map",
                    "symbolic-reference",
                ],
                "maps_require_literal_keys": True,
                "keyword_unpacking": False,
            },
            "source_call_schema": {
                "required": [
                    "method",
                    "arguments",
                    "keyword_arguments",
                    "source_path",
                    "line",
                    "column",
                ],
                "additional_properties": False,
            },
        },
        "enums": {
            "action_types": sorted(ACTION_HANDLERS),
            "continents": sorted(VALID_CONTINENTS),
            "directions": sorted(VALID_DIRECTIONS),
            "faction_territories": sorted(VALID_FACTION_TERRITORIES),
            "node_types": sorted(VALID_NODE_TYPES),
            "objective_type_aliases": dict(sorted(OBJECTIVE_TYPE_ALIASES.items())),
            "objective_types": sorted(OBJECTIVE_TYPES),
            "room_types": sorted(VALID_ROOM_TYPES),
            "social_edge_types": sorted(EDGE_TYPES),
            "social_node_types": sorted(NODE_TYPES),
            "zone_types": sorted(VALID_ZONE_TYPES),
        },
        "stable_ids": {
            "items": sorted(CATALOG),
            "materials": sorted(MATERIAL_REGISTRY),
            "mob_templates": sorted(MOB_TEMPLATES),
            "skills": sorted(SKILL_DEFINITIONS),
        },
        "validation_rules": {
            "runtime_identifier_pattern": "^[a-z0-9][a-z0-9_]*$",
            "cross_zone_room_reference_pattern": (
                "^[a-z0-9][a-z0-9_]*:[a-z0-9][a-z0-9_]*$"
            ),
            "unknown_operation_policy": "reject-file-read-only",
            "unknown_identifier_policy": "reject-with-source-location",
            "model_mutation_authority": "none",
            "network_required": False,
        },
    }


def render_content_contract() -> str:
    return json.dumps(build_content_contract(), indent=2, sort_keys=True) + "\n"


def contract_artifact_is_current(path: Path = DEFAULT_ARTIFACT_PATH) -> bool:
    try:
        return path.read_text() == render_content_contract()
    except FileNotFoundError:
        return False
