"""Literal AreaBuilder Social Web topology with safe cross-zone reconciliation."""

from __future__ import annotations

from django.db import transaction
from django.db.models import Q

from world.social_taxonomy import EDGE_TYPES, NODE_TYPES, normalize_tags


_REGISTERED_ZONE_TOPOLOGY = {}
_DIRECTIONALITIES = {"one_way", "two_way", "broadcast", "gatekept"}


def social_edge_key(source_node_key, target_node_key, edge_type):
    return f"edge:{source_node_key}:{target_node_key}:{edge_type}"


def _typed_node_key(value):
    value = str(value or "").strip()
    if ":" not in value:
        return ""
    node_type, identifier = value.split(":", 1)
    if node_type not in NODE_TYPES or not identifier:
        return ""
    return value


def validate_social_node_definition(node_type, identifier, **_kwargs):
    if node_type not in NODE_TYPES:
        raise ValueError(f"unsupported social node_type: {node_type}")
    if not isinstance(identifier, str) or not identifier.strip() or ":" in identifier:
        raise ValueError("social node identifier must be a non-empty untyped identifier")


def validate_social_edge_definition(source_node_key, target_node_key, *, edge_type, **kwargs):
    if not _typed_node_key(source_node_key) or not _typed_node_key(target_node_key):
        raise ValueError("social edges require typed source_node_key and target_node_key")
    if edge_type not in EDGE_TYPES:
        raise ValueError(f"unsupported social edge_type: {edge_type}")
    directionality = kwargs.get("directionality", "one_way")
    if directionality not in _DIRECTIONALITIES:
        raise ValueError(f"unsupported social directionality: {directionality}")
    if directionality == "gatekept" and not normalize_tags(
        kwargs.get("required_tags") or kwargs.get("blockers") or []
    ):
        raise ValueError("gatekept social edges require required_tags")


def clear_registered_social_topology():
    """Reset only the in-process registry before AreaBuilder reloads every zone."""
    _REGISTERED_ZONE_TOPOLOGY.clear()


def register_zone_social_topology(zone_id, *, nodes, edges):
    """Register one literal zone specification and materialize what is resolvable."""
    _REGISTERED_ZONE_TOPOLOGY[zone_id] = {
        "nodes": tuple(dict(node) for node in nodes),
        "edges": tuple(dict(edge) for edge in edges),
    }
    return materialize_registered_social_topology(finalize=False)


def _bind(zone_id, kind, object_key):
    from world.models import SocialTopologyBinding

    SocialTopologyBinding.objects.get_or_create(
        zone_id=zone_id,
        kind=kind,
        object_key=object_key,
    )


def _node_has_runtime_references(node):
    from world.models import (
        SocialClaim,
        SocialEdge,
        SocialFact,
        SocialKnowledge,
        SocialTrace,
    )

    return any(
        queryset.exists()
        for queryset in (
            SocialEdge.objects.filter(Q(source_node=node) | Q(target_node=node)),
            SocialFact.objects.filter(
                Q(subject_node=node) | Q(actor_node=node) | Q(scope_node=node)
            ),
            SocialClaim.objects.filter(
                Q(speaker_node=node) | Q(subject_node=node)
            ),
            SocialKnowledge.objects.filter(
                Q(node=node) | Q(source_node=node)
            ),
            SocialTrace.objects.filter(Q(from_node=node) | Q(to_node=node)),
        )
    )


def _remove_unowned_object(kind, object_key):
    from world.models import SocialEdge, SocialNode, SocialTopologyBinding

    if SocialTopologyBinding.objects.filter(kind=kind, object_key=object_key).exists():
        return
    if kind == "edge":
        SocialEdge.objects.filter(edge_key=object_key).delete()
        return
    node = SocialNode.objects.filter(node_key=object_key).first()
    if node and not _node_has_runtime_references(node):
        node.delete()


def _reconcile_zone_bindings(zone_id, desired):
    from world.models import SocialTopologyBinding

    stale_bindings = list(SocialTopologyBinding.objects.filter(zone_id=zone_id))
    for binding in stale_bindings:
        if (binding.kind, binding.object_key) in desired:
            continue
        kind = binding.kind
        object_key = binding.object_key
        binding.delete()
        _remove_unowned_object(kind, object_key)


def materialize_registered_social_topology(*, finalize=False):
    """Materialize all registered nodes, then resolve edges after node creation.

    ``finalize=True`` is called after AreaBuilder has loaded every zone. It is
    the only point at which stale builder bindings are removed, ensuring a
    cross-zone edge is not mistaken for stale merely because its target zone
    loaded later in the first pass.
    """
    from world.social_engine import connect_social_nodes, ensure_social_node

    desired_by_zone = {
        zone_id: set() for zone_id in _REGISTERED_ZONE_TOPOLOGY
    }
    unresolved_edges = []
    materialized_nodes = 0
    materialized_edges = 0

    with transaction.atomic():
        for zone_id, topology in sorted(_REGISTERED_ZONE_TOPOLOGY.items()):
            for node_def in topology["nodes"]:
                node = ensure_social_node(
                    node_def["node_type"],
                    node_def["identifier"],
                    display_name=node_def.get("display_name", ""),
                    zone_id=node_def.get("zone_id", zone_id),
                    settlement_id=node_def.get("settlement_id", ""),
                    faction_id=node_def.get("faction_id", ""),
                    metadata=node_def.get("metadata") or {},
                )
                _bind(zone_id, "node", node.node_key)
                desired_by_zone[zone_id].add(("node", node.node_key))
                materialized_nodes += 1

        for zone_id, topology in sorted(_REGISTERED_ZONE_TOPOLOGY.items()):
            for edge_def in topology["edges"]:
                ok, message, edge = connect_social_nodes(
                    edge_def["source_node_key"],
                    edge_def["target_node_key"],
                    edge_type=edge_def["edge_type"],
                    directionality=edge_def.get("directionality", "one_way"),
                    trust=edge_def.get("trust", 0.5),
                    latency_seconds=edge_def.get("latency_seconds", 0),
                    bandwidth=edge_def.get("bandwidth", 3),
                    secrecy=edge_def.get("secrecy", ""),
                    distortion=edge_def.get("distortion", ""),
                    scope_tags=edge_def.get("scope_tags") or [],
                    blockers=edge_def.get("blockers") or [],
                    required_tags=edge_def.get("required_tags"),
                    blocked_tags=edge_def.get("blocked_tags"),
                )
                if not ok:
                    unresolved_edges.append(
                        {
                            "zone_id": zone_id,
                            "source_node_key": edge_def["source_node_key"],
                            "target_node_key": edge_def["target_node_key"],
                            "edge_type": edge_def["edge_type"],
                            "message": message,
                        }
                    )
                    continue
                _bind(zone_id, "edge", edge.edge_key)
                desired_by_zone[zone_id].add(("edge", edge.edge_key))
                materialized_edges += 1

        if finalize:
            for zone_id, desired in desired_by_zone.items():
                _reconcile_zone_bindings(zone_id, desired)

    return {
        "materialized_nodes": materialized_nodes,
        "materialized_edges": materialized_edges,
        "unresolved_edges": unresolved_edges,
    }
