"""
Flight engine — fare calculation and flight booking for Dragon Courier.

Exports:
    fare_for_route(character, legs) -> int
    book_flight(character, origin_point_id, destination_point_id) -> (bool, str)
"""

import logging

from django.db import transaction

from world.game_operations import (
    get_operation_replay,
    normalize_operation_id,
    record_operation,
)


logger = logging.getLogger("evennia")

# Consortium Standing discount tiers (D-09).
# Checked in descending threshold order — first match wins.
STANDING_DISCOUNT_TIERS = [
    (75, 0.30),   # Standing 75-100: 30% off
    (50, 0.20),   # Standing 50-74: 20% off
    (25, 0.10),   # Standing 25-49: 10% off
    (0,  0.00),   # Standing 0-24: no discount
]

CONSORTIUM_FACTION_ID = "consortium"


def fare_for_route(character, legs):
    """
    Calculate total fare for a multi-leg route with Consortium Standing discount.

    Sums base_fare across all legs, then applies a Standing-based percentage
    discount. Result is floored to int (rounds down). Never negative.

    Args:
        character: the travelling Character
        legs: list of (from_point_id, to_point_id) tuples

    Returns:
        int — total fare in scales after Standing discount
    """
    from world.flight_registry import FlightRegistry
    from world.world_state import get_standing

    base_total = 0
    for from_id, to_id in legs:
        route = FlightRegistry.get_route(from_id, to_id)
        if route:
            base_total += route["base_fare"]

    standing = get_standing(character, CONSORTIUM_FACTION_ID)
    discount = 0.0
    for threshold, disc in STANDING_DISCOUNT_TIERS:
        if standing >= threshold:
            discount = disc
            break

    discounted = int(base_total * (1.0 - discount))
    return max(0, discounted)


def _after_write(checkpoint):
    """Failure-injection seam for composite flight rollback tests."""


def _clean_failed_script(character, script):
    """Clear volatile/script cache state after transactional setup failure."""

    if script is not None:
        try:
            script.delete()
        except Exception:
            script.flush_from_cache(force=True)
    character.ndb.in_flight = False


def _commit_flight_booking(
    character,
    *,
    origin_point_id,
    destination_point_id,
    leg_data,
    fare,
    operation_id,
):
    """Commit fare, persistent script, receipt, and initial journey together."""

    from evennia.objects.models import ObjectDB
    from world.banking import deduct_from_bank

    related_id = f"flight:{origin_point_id}:{destination_point_id}"
    script = None
    try:
        with transaction.atomic():
            locked_character = ObjectDB.objects.select_for_update().get(
                pk=character.id
            )
            replay = get_operation_replay(
                character=locked_character,
                operation_id=operation_id,
                operation_type="flight_booking",
                related_id=related_id,
            )
            if replay:
                if replay.result.get("status") == "booked":
                    return True, replay.result.get("message", "")
                return False, replay.result.get(
                    "message",
                    "That booking did not complete.",
                )

            paid, payment_message = deduct_from_bank(
                locked_character,
                fare,
                "flight_fare",
                description=(
                    f"Flight: {origin_point_id} -> {destination_point_id}"
                ),
                related_id=related_id,
                operation_id=operation_id,
            )
            if not paid:
                return False, f"Payment failed: {payment_message}"
            _after_write("flight_fare_deducted")

            from world.scripts.flight_script import FlightScript

            script = locked_character.scripts.add(
                FlightScript,
                key="flight_script",
            )
            script.db.legs = leg_data
            script.db.current_leg = 0
            script.db.in_transit = True
            script.db.fare_paid = True
            script.db.booking_operation_id = operation_id
            _after_write("flight_script_configured")

            record_operation(
                character=locked_character,
                operation_id=operation_id,
                operation_type="flight_booking",
                related_id=related_id,
                result={
                    "status": "booked",
                    "message": "",
                    "fare": fare,
                    "script_id": script.id,
                },
            )
            _after_write("operation_recorded")
            script.start_journey()
            _after_write("journey_started")
        return True, ""
    except Exception:
        logger.exception(
            "flight_engine: booking operation %s failed",
            operation_id,
        )
        _clean_failed_script(character, script)
        return False, "Flight setup failed; no fare was charged."


def book_flight(
    character,
    origin_point_id,
    destination_point_id,
    *,
    operation_id=None,
):
    """
    Validate and start a Dragon Courier flight from origin to destination.

    Validation order:
      1. Origin and destination points must exist in FlightRegistry
      2. A route must exist between them
      3. Destination must be in character.db.discovered_flight_points (D-08)
      4. Character must have sufficient banked balance
      5. Deduct fare atomically via banking.withdraw()
      6. Create FlightScript and call start_journey()

    fare_paid is set on the script BEFORE start_journey() is called so that
    a server reload mid-flight does not double-deduct (Pitfall 6).

    Args:
        character: the travelling Character
        origin_point_id: ID of departure flight point
        destination_point_id: ID of arrival flight point

    Returns:
        (bool, str) — (True, "") on success; (False, reason) on failure
    """
    from world.flight_registry import FlightRegistry
    from world.banking import get_balance

    # 1. Validate both points exist
    origin = FlightRegistry.get_point(origin_point_id)
    destination = FlightRegistry.get_point(destination_point_id)
    if not origin:
        return False, f"Unknown flight point: {origin_point_id}"
    if not destination:
        return False, f"Unknown flight point: {destination_point_id}"
    current_room = getattr(character, "location", None)
    current_room_id = getattr(current_room, "id", None)
    if current_room_id != origin["room_id"]:
        return False, "You must be at that Dragon Courier stop to depart from it."

    # 2. Find route legs via BFS
    legs = FlightRegistry.find_route_legs(origin_point_id, destination_point_id)
    if not legs:
        return False, "No route found to that destination."

    # 3. Discovery gate (D-08): NPC booking gate deferred to content phase
    discovered = character.db.discovered_flight_points or set()
    if destination_point_id not in discovered:
        return False, "You have not discovered that flight point yet."

    # 4. Calculate fare and check balance
    fare = fare_for_route(character, legs)
    balance = get_balance(character)
    if balance < fare:
        return False, f"Insufficient funds: need {fare} scales, have {balance}."

    # Build leg data for FlightScript persistence
    leg_data = []
    for from_id, to_id in legs:
        route = FlightRegistry.get_route(from_id, to_id)
        to_point = FlightRegistry.get_point(to_id)
        leg_data.append({
            "from_point_id": from_id,
            "to_point_id": to_id,
            "to_room_id": to_point["room_id"],
            "duration": route["leg_duration"],
            "echoes": route.get("echoes", []),
        })

    return _commit_flight_booking(
        character,
        origin_point_id=origin_point_id,
        destination_point_id=destination_point_id,
        leg_data=leg_data,
        fare=fare,
        operation_id=normalize_operation_id(operation_id),
    )
