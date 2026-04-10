---
name: patrol-system
description: Tick-driven mob patrol routing with BFS pathfinding, disposition-based encounter checks, and combat interrupt handling
---

## Activation

This skill triggers when editing these files:
- `world/scripts/patrol_script.py`
- `world/patrol_engine.py`
- `world/trigger_engine.py`
- `typeclasses/mobs.py`
- `typeclasses/rooms.py`

Keywords: patrol, patrol script, encounter, trigger, fire_triggers, combat_enabled, interrupt mode, echo radius, patrol route

---

You are working on **the patrol system** — tick-driven mob movement along predefined routes with disposition-based encounter checks.

## Key Files
- `world/scripts/patrol_script.py` — `PatrolScript`: self-ticking script (5s default) attached to patrol mobs, manages route advancement and combat interrupts
- `world/patrol_engine.py` — Stateless engine: `find_path()` BFS, `next_patrol_step()`, `check_patrol_encounter()`, `echo_to_radius()`
- `typeclasses/mobs.py` — Patrol attrs (`db.patrol`, `db.combat_enabled`, `db.triggers`), trigger firing in `at_death()`
- `typeclasses/rooms.py` — `at_object_receive()` fires on_enter/on_first_visit triggers + patrol encounter checks; `at_object_leave()` fires on_exit triggers

## Key Concepts
- **PatrolScript is self-ticking** — unlike NodeScript (interval=0, externally driven), PatrolScript ticks at `self.interval` (default 5s). One script per patrol mob.
- **Route as dbref list:** `db.route_ids` is a list of room dbref integers. `next_patrol_step()` wraps around at the end.
- **Disposition-driven encounters:** `check_patrol_encounter()` calls `get_mob_behavior()` — engages only if behavior is `"aggressive"` or `"territorial"`. Respects `db.combat_enabled` (D-03: False = invulnerable/non-combat mobs).
- **Encounter delay (D-01):** `patrol_def.encounter_delay` seconds before disposition check after arrival. Uses `evennia.utils.utils.delay()`.
- **Room arrival checks (D-02):** `SoravelonRoom.at_object_receive()` checks patrol mobs already in the room when a player enters, with optional encounter_delay.
- **Combat interrupt:** `db.interrupted = True` pauses route advancement. `on_combat_end(outcome)` resumes based on `interrupt_mode`: `resume` (default), `reset_to_start`, or `abandon`.
- **Echo broadcasts (D-04):** `echo_to_radius()` uses BFS from `node_helpers.get_rooms_in_radius()` to announce patrol movement to nearby rooms.
- **Trigger hooks:** Rooms and mobs store `db.triggers` lists. `fire_triggers()` from `world/trigger_engine` handles event dispatch (on_enter, on_exit, on_first_visit, on_mob_death).

## Critical Rules
1. **Pitfall 2 guard required** — always check `if not mob or not mob.pk` before acting on a mob reference in delayed callbacks or script ticks. Scripts may tick after mob deletion.
2. **Player-character guard (Pitfall 7)** — room trigger/encounter hooks check `hasattr(obj, 'account') and obj.account` to avoid firing for NPCs/mobs.
3. **PatrolScript is self-ticking** — do NOT set `interval=0`. This is different from NodeScript which is externally driven by `node_failure_tick`.
4. **`db.patrol` on mob vs `db.patrol_def` on script** — mob's `db.patrol` is the patrol definition dict (None = not a patrol mob); script's `db.patrol_def` is the operational copy.
5. **Encounter uses disposition, never hardcoded** — always go through `check_patrol_encounter()` → `get_mob_behavior()`. Never hardcode friend/foe.
6. **SaverDict caution** — copy `self.db.patrol_def` to plain dict before `.get()` calls (line 70 of patrol_script.py).

## References
- **Mob Disposition:** `world/mob_disposition.py` — behavior thresholds that drive encounter decisions
- **Node Helpers BFS:** `world/node_helpers.py` — `get_rooms_in_radius()` used by echo broadcasts
- **Area Builder:** `world/area_builder.py` — defines patrol routes via `area.patrol()` DSL

---
**Last Updated:** 2026-03-24
