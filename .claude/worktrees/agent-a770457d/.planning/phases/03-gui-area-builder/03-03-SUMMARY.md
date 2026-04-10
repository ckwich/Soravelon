---
phase: 03-gui-area-builder
plan: "03"
subsystem: zone-loading
tags: [json, area-builder, zone-serializer, evennia, django-orm]

requires:
  - phase: 03-01
    provides: "area_validator.py with validate_zone() and AreaBuilderValidationError"
  - phase: 03-02
    provides: "_UNRESOLVED_EXITS_REGISTRY, two-pass _load_all_zones(), .zone.json elif branch"

provides:
  - "world/zone_serializer.py — load_zone_from_json() JSON→AreaBuilder adapter"
  - "20 tests covering all 16 JSON section types, validation gating, and idempotency"

affects:
  - soravelon-builder (sidecar can call load_zone_from_json for server-side loading)
  - 03-04 (live-edit hooks use this function as the entry point)
  - content phases (zone JSON files loaded via this adapter at server start)

tech-stack:
  added: []
  patterns:
    - "JSON section keys mirror AreaBuilder method kwargs exactly (thin adapter pattern)"
    - "Validate-before-build: validate_zone() gates DB writes; error-severity raises, warnings pass"
    - "rooms_lookup dict for local room resolution; colon-separated string for cross-zone exits"

key-files:
  created:
    - world/zone_serializer.py
    - tests/test_zone_serializer.py
  modified: []

key-decisions:
  - "Task 2 (extend _load_all_zones) was pre-implemented in 03-02 — verified and accepted as-is; no duplicate modification needed"
  - "rooms_lookup dict (not DB search) for local exit/spawn/npc resolution — matches AreaBuilder's own _rooms pattern"
  - "Missing optional sections default to empty list via .get() — all sections except 'zone' are optional"
  - "Idempotency test uses room_id tag category search (not zone_id) to filter individual rooms precisely"

patterns-established:
  - "Thin adapter pattern: load_zone_from_json is 120 lines that call AreaBuilder — no logic duplication"
  - "Section ordering matches AreaBuilder dependency order: zone → rooms → exits → spawns → ... → build()"

requirements-completed:
  - BLD-02

duration: 8min
completed: "2026-03-25"
---

# Phase 03 Plan 03: Zone Serializer Summary

**JSON→AreaBuilder adapter load_zone_from_json() maps all 16 zone JSON section types to AreaBuilder calls with validate-before-build gating and cross-zone exit string passthrough**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-25T19:34:11Z
- **Completed:** 2026-03-25T19:42:02Z
- **Tasks:** 2 (1 implemented, 1 pre-existing)
- **Files modified:** 2 created

## Accomplishments

- Created `world/zone_serializer.py` with `load_zone_from_json()` — validates via `validate_zone()` before touching DB, then maps all 16 JSON sections to AreaBuilder method calls in correct dependency order
- 20 new tests covering: import, validation gating (error vs warning severity), zone/rooms/exits section mapping, cross-zone exit string passthrough, optional sections defaulting, materials, and idempotency
- Confirmed `at_server_startstop.py` already has the `.zone.json` branch from 03-02 — no duplicate modification needed

## Task Commits

1. **Task 1 (RED): Failing tests for zone_serializer** - `4b3c436` (test)
2. **Task 1 (GREEN): Implement zone_serializer** - `8d11eb6` (feat)
3. **Task 2: Pre-existing in 03-02** — no commit needed (deviation documented)

**Plan metadata:** (pending docs commit)

_Note: TDD tasks have RED then GREEN commits. Task 2 was a pre-existing implementation._

## Files Created/Modified

- `world/zone_serializer.py` — load_zone_from_json(): validates, builds rooms_lookup, calls all 16 AreaBuilder section methods, returns build() report
- `tests/test_zone_serializer.py` — 20 tests: import, validation gating, section mapping, optional sections, cross-zone exits, idempotency

## Decisions Made

- Task 2 (`_load_all_zones()` `.zone.json` branch) was already implemented in 03-02. Verified correctness and skipped re-implementation to avoid duplicate modification.
- Used `rooms_lookup` dict (room_id → room_obj) built during room creation phase for local exit/spawn/npc resolution. This mirrors AreaBuilder's own `_rooms` dict pattern — no extra DB queries.
- Missing optional sections use `.get(key, [])` — all sections except `"zone"` are optional, consistent with plan spec.

## Deviations from Plan

### Pre-existing Implementation

**1. Task 2 already completed in 03-02**
- **Found during:** Task 2 start — verified `at_server_startstop.py` before any modification
- **Issue:** Important context note in prompt stated `.zone.json` branch was added during 03-02; confirmed with grep
- **Action:** Skipped Task 2 modification entirely — branch already correct with `load_zone_from_json` import, `json.load()`, error handling with `traceback.print_exc()`
- **Verification:** `grep -n "zone.json|load_zone_from_json" server/conf/at_server_startstop.py` confirms lines 104, 130, 133, 136

---

**Total deviations:** 1 (pre-existing task — no action needed)
**Impact on plan:** Task 2 goal fully satisfied by 03-02. Zero scope change.

## Issues Encountered

- Idempotency test initially used `evennia.search_tag(zone_id, category="zone_id")` + `hasattr(r, "exits")` filter — this matched 5 objects (ZoneObject, exits, rooms) not 2. Fixed by searching with `room_id` tag category instead, which uniquely identifies individual rooms.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `load_zone_from_json()` is the server-side entry point for `.zone.json` files produced by the GUI builder
- `_load_all_zones()` processes `.zone.json` files alongside `.py` files in sorted order — server is now a native JSON zone consumer
- BLD-02 (partial) satisfied: server can load JSON zone files the builder produces
- Phase 03-04 (live-edit hooks) can use `load_zone_from_json()` as its WebSocket payload handler

---
*Phase: 03-gui-area-builder*
*Completed: 2026-03-25*
