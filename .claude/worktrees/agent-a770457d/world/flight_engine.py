"""
Flight engine — fare calculation and flight booking for Dragon Courier.

Exports:
    fare_for_route(character, legs) -> int
    book_flight(character, origin_point_id, destination_point_id) -> (bool, str)
"""

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


def book_flight(character, origin_point_id, destination_point_id):
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
    from world.banking import withdraw, get_balance

    # 1. Validate both points exist
    origin = FlightRegistry.get_point(origin_point_id)
    destination = FlightRegistry.get_point(destination_point_id)
    if not origin:
        return False, f"Unknown flight point: {origin_point_id}"
    if not destination:
        return False, f"Unknown flight point: {destination_point_id}"

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

    # 5. Deduct fare atomically (before script creation — Pitfall 6)
    ok, msg = withdraw(character, fare)
    if not ok:
        return False, f"Payment failed: {msg}"

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

    # 6. Create FlightScript and start journey
    from world.scripts.flight_script import FlightScript
    script = character.scripts.add(FlightScript, key="flight_script", persistent=True)
    script.db.legs = leg_data
    script.db.current_leg = 0
    script.db.in_transit = True
    script.db.fare_paid = True   # Pitfall 6: fare already deducted — no double-deduct on reload
    script.start_journey()
    return True, ""
