---
name: flight-system
description: Dragon Courier flight network — fare calculation with Consortium Standing discounts, multi-leg BFS routing, and delay-driven FlightScript
---

## Activation

This skill triggers when editing these files:
- `world/flight_engine.py`
- `world/flight_registry.py`
- `world/scripts/flight_script.py`
- `tests/test_flight_engine.py`

Keywords: flight, flight point, flight route, fare, dragon courier, disembark, FlightScript, FlightRegistry

---

You are working on **the Dragon Courier flight system** — fare-gated fast travel between registered flight points.

## Key Files
- `world/flight_engine.py` — `fare_for_route()` (Standing discount) + `book_flight()` (validation → withdraw → create script)
- `world/flight_registry.py` — Module-level singleton graph: flight points + bidirectional routes, BFS `find_route_legs()`
- `world/scripts/flight_script.py` — `FlightScript`: delay-driven per-player state machine (leg traversal, echoes, disembark window)
- `world/area_builder.py` — `flight_point()` and `flight_route()` DSL methods populate FlightRegistry at zone build time
- `tests/test_flight_engine.py` — EvenniaTest-based tests using `unittest.mock.patch` for world engine dependencies

## Key Concepts
- **Flight network is a graph:** Points (rooms) and routes (edges with fare + duration) stored in `FlightRegistry` singleton. Rebuilt on every server start from area files (same as ZoneRegistry).
- **BFS routing:** `find_route_legs()` returns shortest path as `[(from_id, to_id), ...]`. Returns `[]` for same-origin-destination or unreachable.
- **Consortium Standing discounts (D-09):** Fare tiers checked descending — standing ≥75 → 30% off, ≥50 → 20%, ≥25 → 10%, else 0%. Multi-leg fares sum base_fare THEN discount.
- **Discovery gate (D-08):** `character.db.discovered_flight_points` (set) must contain destination. NPC booking gate deferred to content phase.
- **FlightScript uses `delay()`, NOT self-ticking:** `interval=0`. Leg timing and disembark windows use `evennia.utils.utils.delay()`. This is different from both NodeScript (externally ticked) and PatrolScript (self-ticking).
- **Fare-paid guard (Pitfall 6):** `book_flight()` deducts fare BEFORE creating script, then sets `db.fare_paid=True`. `at_script_creation()` initializes it `False`. Prevents double-deduction on server reload.
- **Disembark window (D-11):** At intermediate stops, player gets 10s to type `disembark`. If not, `_check_continue()` auto-advances to next leg.
- **Mid-leg echoes:** Route definitions include `echoes` list of `{"delay": N, "message": "..."}` for atmospheric narration during flight.

## Critical Rules
1. **`fare_paid` is set in `book_flight()`, never in `at_script_creation()`** — Pitfall 6: script creation must NOT deduct fare
2. **Minimum leg duration is 30s (D-10)** — enforced in `AreaBuilder.flight_route()`, not in the engine
3. **Always check `character.pk` in delayed callbacks** — character may disconnect mid-flight; `_begin_leg()` and `_arrive_at_stop()` guard with `if not character or not character.pk`
4. **`ndb.in_flight` is the player-visible flight state** — set True in `start_journey()`, cleared in `_arrive_final()` and `do_disembark()`. Other systems should check this before allowing actions
5. **Routes are bidirectional** — `register_route()` stores both `(a,b)` and `(b,a)` entries
6. **Follows `(bool, str)` return convention** — `book_flight()` returns `(True, "")` on success, `(False, reason)` on failure

## References
- **Banking:** `world/banking.py` — `withdraw()`, `get_balance()` used for fare deduction
- **Standing:** `world/world_state.py` — `get_standing()` for Consortium discount tiers
- **Area Builder:** `world/area_builder.py` — `flight_point()`, `flight_route()` DSL
- **Tests:** `tests/test_flight_engine.py`

---
**Last Updated:** 2026-03-25
