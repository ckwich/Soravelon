"""Pure playable-connectivity audit for compiled world-content manifests."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass

from world.content_compiler import (
    SymbolicReference,
    WorldManifest,
    thaw_compiled_value,
)

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
    """Audit walking plus flight reachability under the live discovery gate."""

    rooms: set[str] = set()
    adjacency: dict[str, set[str]] = defaultdict(set)
    flight_points: dict[str, str] = {}
    flight_routes: list[tuple[str, str]] = []
    authored_flight_grants_by_zone: dict[str, set[str]] = defaultdict(set)
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
            elif operation.method == "quest":
                kwargs = thaw_compiled_value(operation.keyword_arguments)
                for reward in kwargs.get("rewards", []) if isinstance(kwargs, dict) else []:
                    if not isinstance(reward, dict):
                        continue
                    if reward.get("action_type") == "discover_flight_point":
                        point_id = reward.get("point_id")
                        if isinstance(point_id, str) and point_id:
                            authored_flight_grants_by_zone[zone_id].add(point_id)

    valid_flight_routes: list[tuple[str, str]] = []
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
        valid_flight_routes.append((first, second))

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

    def expand_walking(seed_rooms: set[str]) -> None:
        frontier = deque(seed_rooms)
        while frontier:
            current = frontier.popleft()
            for neighbor in adjacency.get(current, ()):
                if neighbor in rooms and neighbor not in reachable:
                    reachable.add(neighbor)
                    frontier.append(neighbor)

    while True:
        reachable_zones = {room.partition(":")[0] for room in reachable}
        discovered_flight_points = {
            point_id for point_id, room in flight_points.items() if room in reachable
        }
        for zone_id in reachable_zones:
            discovered_flight_points.update(
                authored_flight_grants_by_zone.get(zone_id, set())
            )
        newly_reachable = set()
        for first, second in valid_flight_routes:
            first_room = flight_points[first]
            second_room = flight_points[second]
            if first_room in reachable and second in discovered_flight_points:
                newly_reachable.add(second_room)
            if second_room in reachable and first in discovered_flight_points:
                newly_reachable.add(first_room)
        newly_reachable -= reachable
        if not newly_reachable:
            break
        reachable.update(newly_reachable)
        expand_walking(newly_reachable)

    for first, second in valid_flight_routes:
        first_reachable = flight_points[first] in reachable
        second_reachable = flight_points[second] in reachable
        if first_reachable == second_reachable:
            continue
        origin, blocked_destination = (
            (first, second) if first_reachable else (second, first)
        )
        diagnostics.append(
            ConnectivityDiagnostic(
                code="circular-flight-discovery",
                entity_id=f"{origin}:{blocked_destination}",
                message=(
                    f"Fresh players can reach '{origin}', but booking to "
                    f"'{blocked_destination}' requires discovering that inaccessible "
                    "destination first."
                ),
            )
        )

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
