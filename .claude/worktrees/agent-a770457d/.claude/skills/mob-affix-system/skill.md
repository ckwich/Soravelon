---
name: mob-affix-system
description: Rarity-tiered mob affixes with weighted pools, forbidden combos, pack spawning, and progressive reveal
---

## Activation

This skill triggers when editing these files:
- `world/mob_affixes.py`
- `world/mob_affix_roller.py`
- `typeclasses/mobs.py`

Keywords: affix, rarity, mob spawn, pack, combat modifier, immunity, reveal

---

You are working on **the mob affix system** — rarity tiers, affix rolling, pack spawning, and combat integration.

## Key Files
- `world/mob_affixes.py` — Affix definitions (20 affixes), pools, forbidden combos, combat hook stubs
- `world/mob_affix_roller.py` — Rarity roll, affix selection, `apply_affixes_to_mob()`, `spawn_mob_with_pack()`
- `typeclasses/mobs.py` — `SoravelonMob` typeclass: display, reveal, modifier merging, immunity checks

## Key Concepts
- **Rarity tiers:** normal(850)/magic(120)/rare(25)/legendary(5) weights. Normal = 0 affixes, magic=1, rare=2, legendary=3
- **Affix pools:** Node-type pools (`NODE_AFFIX_POOLS`) used when room has `mob_affixes_active` tag (category `node_effect`) + matching `db.node_type`. Falls back to `GENERAL_AFFIX_POOL`
- **Forbidden combos:** Sets in `FORBIDDEN_COMBINATIONS` — if candidate set is superset, affix rejected
- **Defensive limit:** Max 1 defensive affix per mob (`DEFENSIVE_LIMIT`). Defensive set: armored, regenerating, warding, evasive
- **Pack spawning:** Non-normal mobs spawn with packs (magic 1-2, rare 2-3, legendary 3-4). Pack mobs are always normal rarity with no affixes
- **Progressive reveal:** Affixes hidden until first combat interaction. Revealed state in `ndb.revealed_affixes` (volatile set). `reveal_affix()` returns message once, then `None`
- **Combat modifiers merge additively:** `get_combat_modifiers()` sums values for duplicate keys across affixes

## Critical Rules
1. **Assign `db.affix_list` once** — list assigned atomically to avoid SaverList N-append repickle (line 110 of roller)
2. **Affixes stored as both tags AND list** — tags (`category="mob_affix"`) for queries, `db.affix_list` for iteration. Keep in sync
3. **Spawn entry point is `initialize_for_spawn(room)`** — rolls affixes AND combat stats. `spawn_with_affixes()` is legacy compat only
4. **Pack mobs skip `initialize_for_spawn()`** — they call `initialize_mob_combat_stats()` directly (from `world/zone_scaling`) with hardcoded normal rarity
5. **`has_immunity()` returns `(bool, str|None)` tuple** — follows project convention of `(bool, str)` returns
6. **Combat hook stubs exist but are not wired** — `check_mob_damage_modifiers`, `check_mob_on_hit_effects`, `check_mob_per_round_effects` in `mob_affixes.py` are stubs for future combat system
7. **`ndb.revealed_affixes` reset on death** — `at_death()` clears it so re-spawned mob starts fresh

## References
- **Affix Definitions:** `world/mob_affixes.py`
- **Zone Scaling:** `world/zone_scaling.py`
- **Mob Disposition:** `world/mob_disposition.py`

---
**Last Updated:** 2026-03-23
