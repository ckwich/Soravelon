---
name: zone-scaling
description: Per-player logarithmic combat scaling, mob HP initialization, damage math, and skill-based loot tiers
---

## Activation

This skill triggers when editing these files:
- `world/zone_scaling.py`
- `world/zone_object.py`
- `tests/test_zone_scaling.py`

Keywords: zone scaling, combat scaling, mob damage, scale factor, material tier, loot tier, rarity multiplier

---

You are working on **zone scaling** — the per-player combat math and mob initialization system.

## Key Files
- `world/zone_scaling.py` — All scaling functions (stateless module, no DB models)
- `world/zone_object.py` — ZoneObject init and node system setup
- `typeclasses/mobs.py` — Calls `initialize_mob_combat_stats` at spawn via `initialize_for_spawn()`
- `world/mob_affix_roller.py` — Also calls `initialize_mob_combat_stats` for pack mobs
- `tests/test_zone_scaling.py` — Comprehensive unit tests

## Key Concepts
- **No zone level caps:** Every zone is valid at every player progression level. Scaling is purely per-player, not per-zone.
- **Mob HP rolled once at spawn:** `initialize_mob_combat_stats()` rolls HP from `hp_min`/`hp_max`, applies rarity + prestige multipliers, stores final values in `db.*`. This is a one-time operation.
- **Damage scaling locked at first hit:** `get_combat_scale()` computes and caches scale factor in `mob.ndb.combat_scales[character.id]` on first call. Subsequent calls return cached value — scale never changes mid-fight.
- **Logarithmic curve:** `get_scale_factor()` uses `log(level+1)/log(REFERENCE_LEVEL+1)` with floor of `SCALE_FLOOR` (0.5). Reference level 10 = factor 1.0.
- **Loot is skill-based:** `get_material_tier()` maps skill score (0-100) to tier (1-5). Not level-based, not zone-based.
- **Zone lookup uses tags:** `get_zone_obj_for_room()` searches by `zone_id` tag (indexed O(1)), not room scanning.

## Critical Rules
1. **`ndb` for combat cache, `db` for rolled stats** — `combat_scales` is volatile (`ndb`), rolled HP/damage are persistent (`db`). Never swap these.
2. **Call `initialize_mob_combat_stats` AFTER setting rarity/prestige** — it reads `mob.db.rarity` and `mob.db.prestige_modifier` to compute multipliers. Setting them after init produces wrong stats.
3. **Scale factor has a floor** — `SCALE_FLOOR = 0.5` prevents low-level scaling from zeroing out damage. Never bypass this minimum.
4. **Minimum 1 damage everywhere** — both `get_player_damage_to_mob` and `apply_resistance` enforce `max(1, ...)`. Maintain this invariant in any new damage path.
5. **Stateless module** — `zone_scaling.py` has no imports from `world/models.py`. It operates on object attributes only. Keep it that way.
6. **Rarity keys are lowercase strings** — `"normal"`, `"magic"`, `"rare"`, `"legendary"`. Must match `RARITY_MULTIPLIERS` dict keys exactly.

## References
- **Mob typeclasses:** `typeclasses/mobs.py`
- **Affix system:** `world/mob_affixes.py`, `world/mob_affix_roller.py`
- **Tests:** `tests/test_zone_scaling.py`

---
**Last Updated:** 2026-03-23
