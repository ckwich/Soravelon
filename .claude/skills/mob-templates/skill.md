---
name: mob-templates
description: Mob template registry — stat blocks, behavior defaults, and apply function consumed by mob_spawner at spawn time
---

## Activation

This skill triggers when editing these files:
- `world/mob_templates.py`
- `world/mob_spawner.py`
- `tests/test_mob_templates.py`

Keywords: mob template, mob spawn, spawn_single_mob, apply_mob_template, MOB_TEMPLATES, respawn, mob_spawner, template registry

---

You are working on **the mob template registry** (`world/mob_templates.py`) and **mob spawner** (`world/mob_spawner.py`) — template-driven mob creation and respawn scheduling.

## Key Files
- `world/mob_templates.py` — `MOB_TEMPLATES` dict, `get_mob_template()`, `apply_mob_template()`
- `world/mob_spawner.py` — `spawn_single_mob()`, `spawn_named_mob()`, `_schedule_respawn()`, zone spawn orchestration
- `tests/test_mob_templates.py` — Unit tests (unittest.TestCase + MagicMock, no Evennia DB)
- `world/area_builder.py` — `spawn()` / `named_mob()` store spawn_def dicts on `room.db.spawn_definitions`

## Key Concepts
- **Template as stat block:** Each `MOB_TEMPLATES` entry defines key, mob_type, desc, aggression, HP/damage ranges, speed, abilities, faction, hunter/wander/flee behavior, and loot_table
- **Registered templates:** Starter set (rat, wolf, bandit) + Vael's Crossing city mobs (sewer_rat, thug, smuggler, pickpocket) + Stormhaven Coast mobs (shore_crab, sea_serpent, coastal_raider, cliff_harpy, salt_lurker). Zone content plans add entries as zones are authored
- **Spawn flow:** `spawn_single_mob()` creates mob → sets zone_id/disposition/trust → calls `apply_mob_template(mob, spawn_def["mob"])` → then `mob.initialize_for_spawn(room)` (affixes + combat stats). Template provides base values; scaling applies on top
- **Wanderer tagging:** After `apply_mob_template()`, if `mob.db.wander` is True, `spawn_single_mob()` adds tag `wanderer` (category `mob_behavior`) for efficient lookup by `wander_tick()`
- **Sentinel override pattern:** `spawn_def.get("flee_threshold", _SENTINEL)` — if spawn_def explicitly sets flee_threshold, it overrides the template value. Otherwise template value is kept
- **Template does NOT set disposition/trust:** `base_disposition` and `trust_sensitive` come from spawn_def, not template — these are per-spawn-point, not per-mob-type
- **Respawn via callLater:** `_schedule_respawn()` uses `reactor.callLater(delay, _do_respawn)` with `respawn_minutes ± respawn_variance`, minimum 30s floor. NOT SpawnRecord-backed — no Django models for respawn tracking
- **Reactor accessor:** `_get_reactor()` defers Twisted import and enables test patching

## Template Field Reference
`key`, `mob_type`, `desc`, `base_aggression`, `hp_min`, `hp_max`, `damage_min`, `damage_max`, `speed`, `abilities` (list of ability dicts), `faction`, `is_hunter`, `detection_range`, `flee_threshold`, `wander`, `loot_table`

## Critical Rules
1. **Template key = spawn_def `mob` value** — `apply_mob_template(mob, spawn_def["mob"])` uses the mob type string as registry lookup
2. **Unknown templates log warning, don't crash** — `apply_mob_template()` returns without modification if key not found. Backward-compatible with templateless mobs
3. **Template applied BEFORE `initialize_for_spawn()`** — template sets hp_min/hp_max/damage_min/damage_max, then `initialize_for_spawn()` rolls actual HP and applies rarity/prestige multipliers
4. **Abilities are copied** — `list(template["abilities"])` prevents shared mutation across mob instances
5. **Spawn_def overrides template selectively** — only `flee_threshold` uses sentinel pattern currently. Other spawn_def fields (disposition, trust) are set before template apply and not touched by template
6. **Respawn checks count_max** — `_do_respawn()` callback only spawns if `_count_room_mobs(room, spawn_def) < count_max`
7. **No DB persistence for respawn** — callLater timers are lost on server restart. Initial zone spawn handles repopulation
8. **Wanderer tag is spawner's responsibility** — `mob_spawner.py` adds the `wanderer` tag after template apply, not the template itself

## References
- **Area Builder:** `world/area_builder.py` — `spawn()` and `named_mob()` create spawn_def dicts
- **Affix System:** `world/mob_affix_roller.py` — `initialize_for_spawn()` rolls affixes after template
- **Zone Scaling:** `world/zone_scaling.py` — `initialize_mob_combat_stats()` uses template-set hp_min/hp_max
- **Wander System:** `world/wander_system.py` — consumes `wanderer` tag for periodic random movement
- **Loot Tables:** `world/loot_tables.py` — `loot_table` field links to drop resolution
- **Tests:** `tests/test_mob_templates.py`

---
**Last Updated:** 2026-03-30
