"""Pure playable-connectivity audit for compiled world-content manifests."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass

from world.content_compiler import SymbolicReference, WorldManifest

FRESH_START_ROOM = "vaels_crossing:hg_arrival"


@dataclass(frozen=True)
class ConnectivityDiagnostic:
    code: str
    entity_id: str
    message: str


@dataclass(frozen=True)
class ConnectivityAudit:
    start_room: str
    reachable_rooms: frozenset[str]
    unreachable_rooms: frozenset[str]
    unreachable_zones: frozenset[str]
    diagnostics: tuple[ConnectivityDiagnostic, ...]

    @property
    def passed(self) -> bool:
        return not self.diagnostics


def _room_key(zone_id: str, value: object) -> str | None:
    if isinstance(value, SymbolicReference):
        return f"{zone_id}:{value.key}"
    if isinstance(value, str):
        return value if ":" in value else f"{zone_id}:{value}"
    return None


def audit_world_connectivity(
    manifest: WorldManifest,
    *,
    start_room: str = FRESH_START_ROOM,
) -> ConnectivityAudit:
    """Audit walking plus authored bidirectional flight reachability."""

    rooms: set[str] = set()
    adjacency: dict[str, set[str]] = defaultdict(set)
    flight_points: dict[str, str] = {}
    flight_routes: list[tuple[str, str]] = []
    diagnostics: list[ConnectivityDiagnostic] = []

    for definition in manifest.zones:
        zone_id = definition.zone_id
        for operation in definition.operations:
            if operation.method == "room":
                room = _room_key(zone_id, operation.arguments[0])
                if room:
                    rooms.add(room)
            elif operation.method == "exit":
                source = _room_key(zone_id, operation.arguments[0])
                destination = _room_key(zone_id, operation.arguments[1])
                if source and destination:
                    adjacency[source].add(destination)
            elif operation.method == "flight_point":
                room = _room_key(zone_id, operation.arguments[0])
                point_id = str(operation.arguments[1])
                if room:
                    flight_points[point_id] = room
            elif operation.method == "flight_route":
                flight_routes.append(
                    (str(operation.arguments[0]), str(operation.arguments[1]))
                )

    for first, second in flight_routes:
        missing = [point for point in (first, second) if point not in flight_points]
        if missing:
            diagnostics.append(
                ConnectivityDiagnostic(
                    code="unknown-flight-point",
                    entity_id=f"{first}:{second}",
                    message=f"Flight route references missing points: {', '.join(missing)}.",
                )
            )
            continue
        first_room = flight_points[first]
        second_room = flight_points[second]
        adjacency[first_room].add(second_room)
        adjacency[second_room].add(first_room)

    if start_room not in rooms:
        diagnostics.append(
            ConnectivityDiagnostic(
                code="missing-fresh-start",
                entity_id=start_room,
                message="The configured fresh-character start room is absent.",
            )
        )
        reachable: set[str] = set()
    else:
        reachable = {start_room}
        frontier = deque([start_room])
        while frontier:
            current = frontier.popleft()
            for neighbor in adjacency.get(current, ()):
                if neighbor in rooms and neighbor not in reachable:
                    reachable.add(neighbor)
                    frontier.append(neighbor)

    unreachable_rooms = rooms - reachable
    all_zones = {definition.zone_id for definition in manifest.zones}
    reachable_zones = {room.partition(":")[0] for room in reachable}
    unreachable_zones = all_zones - reachable_zones
    for zone_id in sorted(unreachable_zones):
        diagnostics.append(
            ConnectivityDiagnostic(
                code="unreachable-zone",
                entity_id=zone_id,
                message=f"No room in zone '{zone_id}' is reachable from {start_room}.",
            )
        )

    return ConnectivityAudit(
        start_room=start_room,
        reachable_rooms=frozenset(reachable),
        unreachable_rooms=frozenset(unreachable_rooms),
        unreachable_zones=frozenset(unreachable_zones),
        diagnostics=tuple(
            sorted(diagnostics, key=lambda item: (item.code, item.entity_id))
        ),
    )
