---
name: zone-attunement
description: Per-zone attunement tracking (0-100) with dual representation — Django model rows feed aggregate dimension score on character
---

## Activation

This skill triggers when editing these files:
- `world/world_state.py`
- `world/models.py`
- `world/zone_scaling.py`
- `world/zone_object.py`
- `tests/test_world_state.py`

Keywords: attunement, zone attunement, zone score, attunement aggregate, ZoneAttunement

---

You are working on **zone attunement** — the system tracking a character's familiarity with each zone (0-100 per zone), aggregated into the `attunement` world-state dimension.

## Key Files
- `world/models.py:55-74` — `ZoneAttunement` Django model (character FK, zone_id, score, last_visited)
- `world/world_state.py:109-133` — `update_zone_attunement()` and `recalculate_attunement_aggregate()`
- `world/world_state.py:275-284` — `get_zone_attunement()` (read helper, returns 0.0 for missing record)
- `world/zone_scaling.py:126-137` — `get_zone_obj_for_room()` (tag-based O(1) zone lookup)
- `typeclasses/characters.py` — `db.attunement_score` initialized to 0.0 (computed aggregate, never set directly)
- `tests/test_world_state.py` — `TestAttunementDualRepresentation` validates aggregate recalculation

## Dual Representation Pattern
Zone attunement uses a **dual representation**:
1. **Per-zone rows** in `ZoneAttunement` model — source of truth, one row per (character, zone_id)
2. **Aggregate score** in `character.db.attunement_score` — derived via `Avg("score")` across all zone rows

The aggregate is recalculated by `recalculate_attunement_aggregate()`, called inside `commit_session_xp()`.

## Critical Rules
1. **Never set `attunement_score` directly** — always go through `update_zone_attunement()` + `recalculate_attunement_aggregate()`
2. **Scores clamped 0-100** — both per-zone and aggregate enforce this via `max(0.0, min(100.0, ...))`
3. **Lazy record creation** — missing `ZoneAttunement` row means 0.0 attunement, not an error
4. **Attunement does NOT decay globally** — `DECAY_RATES["attunement"] = 0.0`; decay is per-zone if implemented
5. **`get_zone_attunement()` accepts room or string** — resolves `zone.db.zone_id` if object, else `str(zone)`
6. **Zone lookup uses tags** — `evennia.search_tag(zone_id, category="zone_id")` for O(1) indexed lookup, not queryset scan
7. **Aggregate feeds context packet** — `get_character_context_packet()` includes both aggregate `attunement` and per-zone `zone_attunement`

## References
- **World State Engine:** `world/world_state.py`
- **Models:** `world/models.py`
- **Zone Scaling:** `world/zone_scaling.py`
- **Tests:** `tests/test_world_state.py`

---
**Last Updated:** 2026-03-23
