---
name: wander-system
description: Wandering mob movement — stochastic zone-bounded random movement for mobs with db.wander=True, driven by global ticker
---

## Activation

This skill triggers when editing these files:
- `world/wander_system.py`
- `tests/test_wander_system.py`

Keywords: wander, wandering, wander_mob, wander_tick, wanderer tag, mob movement, random movement

---

You are working on **the wandering mob system** (`world/wander_system.py`) — stochastic random movement for mobs within their zone.

## Key Files
- `world/wander_system.py` — `wander_mob()` (single mob move) + `wander_tick()` (batch tick for all wanderers)
- `world/mob_templates.py` — Templates define `wander: True/False`; `apply_mob_template()` sets `mob.db.wander`
- `world/mob_spawner.py` — `spawn_single_mob()` adds `wanderer` tag (category `mob_behavior`) when `mob.db.wander` is True
- `server/conf/at_server_startstop.py` — Registers `wander_tick` as periodic callback (60s interval)
- `tests/test_wander_system.py` — Unit tests (unittest.TestCase + MagicMock, no Evennia DB)

## Key Concepts
- **Stochastic per-tick chance:** `WANDER_CHANCE = 0.4` (40%) per tick — mobs move on average once per 2.5 minutes
- **Zone-bounded movement:** Mobs only move to exits whose destination has the same `db.zone_id`. Never crosses zone boundaries
- **Guard chain:** Skips if `db.wander` not True, in combat (`ndb.combat_script`), has active `PatrolScript`, is dead (`db.is_dead`), or no valid exits
- **Patrol priority:** Active PatrolScript takes precedence over wandering — checked via `mob.scripts.get("patrol_script")`
- **Room filtering:** Destinations with `no_mobs` tag (category `room_flag`) are excluded from valid exits
- **Quiet movement:** `mob.move_to(destination, quiet=True)` suppresses default Evennia move messages; arrival echo sent manually via `destination.msg_contents()`
- **Tag-based lookup:** `wander_tick()` finds all wanderers via `evennia.search_tag("wanderer", category="mob_behavior")` — O(1) indexed query

## Critical Rules
1. **Wanderer tag set at spawn, not in wander_system** — `mob_spawner.py` adds the tag; `wander_system.py` only queries it
2. **Patrol always wins** — if a mob has both `db.wander=True` and an active PatrolScript, patrol takes priority
3. **Zone boundary is hard** — never allow cross-zone wandering. Check `dest.db.zone_id == current_zone`
4. **Global ticker, not per-mob script** — `wander_tick()` is registered as a single server periodic callback, NOT a per-mob script. This is different from PatrolScript (per-mob, self-ticking)
5. **`quiet=True` on move** — always use quiet movement to avoid spamming default Evennia enter/leave messages

## References
- **Mob Templates:** `world/mob_templates.py` — `wander` field in template definitions
- **Mob Spawner:** `world/mob_spawner.py` — tags mobs as `wanderer` at spawn
- **Patrol System:** `world/scripts/patrol_script.py` — takes priority over wandering
- **Server Hooks:** `server/conf/at_server_startstop.py` — ticker registration

---
**Last Updated:** 2026-03-29
