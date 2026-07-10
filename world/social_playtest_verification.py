"""Live-runtime verification for the Vael's Crossing Social Web route."""

from __future__ import annotations

from collections import deque
from math import isclose


VAELS_CROSSING = "vaels_crossing"
ASHREACH_PLAINS = "ashreach_plains"
CALLOWAY_NODE_KEY = "npc:npc_warden_agent_calloway"
HARVEN_NODE_KEY = "npc:npc_warden_outpost_commander"
WHISTLE_NODE_KEY = "npc:npc_innkeeper_whistle"
TRAVELERS_NODE_KEY = "gathering:vc_inn_travelers"
RAITH_NODE_KEY = "npc:npc_debt_collector_raith"
RENN_NODE_KEY = "npc:npc_courier_agent_renn"
WARDEN_EDGE_KEY = (
    "edge:npc:npc_warden_agent_calloway:"
    "npc:npc_warden_outpost_commander:warden_report"
)
TRAVELER_EDGE_KEY = (
    "edge:gathering:vc_inn_travelers:"
    "npc:npc_innkeeper_whistle:inn_traveler"
)


class SocialWebRuntimeVerificationError(RuntimeError):
    """The live world does not satisfy the Social Web acceptance contract."""


def _require(condition, message):
    if not condition:
        raise SocialWebRuntimeVerificationError(message)


def _find_tagged_object(tag, category, zone_id):
    import evennia

    matches = [
        obj
        for obj in evennia.search_tag(tag, category=category)
        if (obj.db.zone_id or "") == zone_id
    ]
    _require(
        len(matches) == 1,
        f"expected one {category}={tag!r} in {zone_id}, found {len(matches)}",
    )
    return matches[0]


def _exit_between(source, destination, direction):
    matches = [
        exit_obj
        for exit_obj in source.exits
        if exit_obj.key.lower() == direction
        and exit_obj.destination
        and exit_obj.destination.id == destination.id
    ]
    _require(
        len(matches) == 1,
        (
            f"expected one {direction} exit from {source.key!r} "
            f"to {destination.key!r}, found {len(matches)}"
        ),
    )
    return matches[0]


def _shortest_route(source, destination):
    allowed_zones = {VAELS_CROSSING, ASHREACH_PLAINS}
    frontier = deque([(source, [])])
    seen = {source.id}
    while frontier:
        room, route = frontier.popleft()
        if room.id == destination.id:
            return route
        for exit_obj in room.exits:
            next_room = exit_obj.destination
            if (
                not next_room
                or next_room.id in seen
                or (next_room.db.zone_id or "") not in allowed_zones
            ):
                continue
            seen.add(next_room.id)
            frontier.append((next_room, [*route, exit_obj]))
    return []


def _verify_applied_migrations():
    from django.db import connection
    from django.db.migrations.executor import MigrationExecutor

    executor = MigrationExecutor(connection)
    world_leaves = executor.loader.graph.leaf_nodes("world")
    applied = executor.loader.applied_migrations
    pending = sorted(node for node in world_leaves if node not in applied)
    _require(not pending, f"world migrations pending: {pending}")
    return f"world migrations current ({len(world_leaves)} leaf migration(s))"


def _verify_materialized_topology():
    from world.models import SocialNode, SocialTopologyBinding

    expected_nodes = {
        CALLOWAY_NODE_KEY: VAELS_CROSSING,
        WHISTLE_NODE_KEY: VAELS_CROSSING,
        TRAVELERS_NODE_KEY: VAELS_CROSSING,
        RAITH_NODE_KEY: VAELS_CROSSING,
        RENN_NODE_KEY: VAELS_CROSSING,
        HARVEN_NODE_KEY: ASHREACH_PLAINS,
    }
    for node_key, zone_id in expected_nodes.items():
        node = SocialNode.objects.filter(node_key=node_key).first()
        _require(node is not None, f"missing materialized Social node {node_key}")
        _require(
            node.zone_id == zone_id,
            f"Social node {node_key} has zone {node.zone_id!r}, expected {zone_id!r}",
        )
        _require(
            SocialTopologyBinding.objects.filter(
                zone_id=zone_id,
                kind="node",
                object_key=node_key,
            ).exists(),
            f"Social node {node_key} is not bound to authored zone {zone_id}",
        )
    return f"{len(expected_nodes)} nodes bound to their authored zones"


def _verify_reciprocal_exits():
    vael_road = _find_tagged_object("hg_south_road", "room_id", VAELS_CROSSING)
    ash_road = _find_tagged_object("ash_road_01", "room_id", ASHREACH_PLAINS)
    _exit_between(vael_road, ash_road, "south")
    _exit_between(ash_road, vael_road, "north")
    return "hg_south_road south <-> ash_road_01 north"


def _verify_edge_policy():
    from world.models import SocialEdge, SocialTopologyBinding

    warden = SocialEdge.objects.filter(edge_key=WARDEN_EDGE_KEY).first()
    traveler = SocialEdge.objects.filter(edge_key=TRAVELER_EDGE_KEY).first()
    _require(warden is not None, "missing materialized Warden report edge")
    _require(traveler is not None, "missing materialized inn traveler edge")
    _require(
        SocialTopologyBinding.objects.filter(
            zone_id=VAELS_CROSSING,
            kind="edge",
            object_key=WARDEN_EDGE_KEY,
        ).exists(),
        "Warden report edge is not bound to Vael's Crossing",
    )
    _require(
        SocialTopologyBinding.objects.filter(
            zone_id=VAELS_CROSSING,
            kind="edge",
            object_key=TRAVELER_EDGE_KEY,
        ).exists(),
        "inn traveler edge is not bound to Vael's Crossing",
    )
    _require(
        (
            warden.active
            and warden.directionality == "one_way"
            and isclose(warden.trust, 0.95)
            and warden.latency_seconds == 0
            and set(warden.scope_tags) == {"warden", "report", "quest"}
        ),
        "Warden report edge policy does not match its authored contract",
    )
    _require(
        (
            traveler.active
            and traveler.directionality == "one_way"
            and isclose(traveler.trust, 0.75)
            and traveler.latency_seconds == 60
            and set(traveler.scope_tags)
            == {"public", "road_conduct", "traveler", "quest"}
        ),
        "inn traveler edge policy does not match its authored contract",
    )
    return "warden_report and inn_traveler policies are authored and active"


def _verify_route_state():
    calloway = _find_tagged_object(
        "npc_warden_agent_calloway",
        "npc_id",
        VAELS_CROSSING,
    )
    harven = _find_tagged_object(
        "npc_warden_outpost_commander",
        "npc_id",
        ASHREACH_PLAINS,
    )
    route = _shortest_route(calloway.location, harven.location)
    _require(route, "no materialized route from Calloway to Harven")
    crosses_zone = any(
        (exit_obj.location.db.zone_id or "")
        != (exit_obj.destination.db.zone_id or "")
        for exit_obj in route
    )
    _require(crosses_zone, "Calloway to Harven route never crosses zones")
    return f"Agent Calloway to Commander Harven traversable in {len(route)} exits"


def verify_social_web_runtime():
    """Return the verified live-runtime checks or raise one actionable error."""
    return {
        "applied migrations": _verify_applied_migrations(),
        "materialized topology": _verify_materialized_topology(),
        "reciprocal exits": _verify_reciprocal_exits(),
        "edge policy": _verify_edge_policy(),
        "route state": _verify_route_state(),
    }
