---
name: loot-tables
description: Loot system — skill-based drop tiers, weighted drop pools, zone overrides, rarity modifiers, and group loot modes
---

## Activation

This skill triggers when editing these files:
- `world/loot_tables.py`
- `world/group_engine.py`
- `world/zone_scaling.py`

Keywords: loot, drops, rarity, loot table, loot mode, roll_loot, drop chance, material tier

---

You are working on **soravelon's loot system** — skill-based tiered drops resolved via `world/loot_tables.py`.

## Key Files
- `world/loot_tables.py` — `LOOT_TABLES` dict, `LOOT_TIER_MODIFIERS`, `roll_loot()`, `get_loot_modifiers()`, zone override resolution
- `world/group_engine.py` — Group loot mode logic (personal/ffa/round_robin/need_pass)
- `world/zone_scaling.py` — `MATERIAL_TIER_BY_SKILL` + `get_material_tier()` — skill-based loot quality
- `typeclasses/mobs.py` — `Mob.get_loot_tier()` returns `db.rarity` (normal/magic/rare/legendary)

## Key Concepts
- **Skill-based quality, NOT level-based:** Killer's relevant domain skill score (0-100) maps to material tier (1-5) via `get_material_tier()`. Never use mob level or zone level for drop quality
- **Rarity tiers:** normal → magic → rare → legendary. Stored in `mob.db.rarity`, default "normal"
- **Loot modifiers:** `LOOT_TIER_MODIFIERS` maps rarity to `extra_rolls`, `tome_chance`, `ancient_chance`. Extra rolls add weighted random picks from the same drop pool
- **LOOT_TABLES structure:** Keyed by `mob_type`. Each entry has `relevant_skill`, `base_drop_chance`, and `drops` list. Each drop has `item_id`, `key`, `item_type`, `weight`, `weight_in_pool`, plus `value_by_tier`, `rarity_by_tier`, `desc_by_tier` arrays (5 entries each, indexed by tier 1-5)
- **Zone overrides:** `_resolve_loot_table()` checks `zone_obj.db.loot_table_overrides` first (keyed by mob_type), falling back to module-level `LOOT_TABLES`
- **Weighted random selection:** `_pick_drop()` uses `weight_in_pool` for weighted random among drops in a table
- **Item def output:** `_build_item_def()` produces a dict with `item_id`, `key`, `item_type`, `weight`, `rarity`, `value`, `desc` — ready for `item_spawner.create_item_from_template()`
- **Registered tables:** shore_crab, sea_serpent, coastal_raider, cliff_harpy, salt_lurker, wolf, ash_wolf, plains_viper, ashreach_bandit, dust_beetle, steppe_hawk, alpha_ash_wolf
- **Loot modes:** Group loot defaults to "personal". Quest drops and Scales are ALWAYS personal regardless of mode
- **Groups are session-only (`ndb`)** — loot mode dissolves when leader disconnects

## Critical Rules
1. **Quest drops and Scales bypass loot mode** — always personal, never shared/rolled
2. **Loot quality scales with skill score, not character level** — use `get_material_tier()`
3. **Rarity fallback** — always default to "normal" if `mob.db.rarity` is missing/unknown
4. **Zone overrides take precedence** — `_resolve_loot_table()` checks zone object first
5. **Lazy imports for zone_scaling** — `get_zone_obj_for_room` and `get_material_tier` are thin wrappers with deferred imports, patchable in tests
6. **Follow `(bool, str)` return convention** from base skill for any new functions (note: `roll_loot` returns `list[dict]` as its established API)
7. **New mob_type loot tables go in LOOT_TABLES dict** — add entries as zones are authored

## References
- **Mob Affixes:** `world/mob_affixes.py` — rarity tier definitions that feed loot modifiers
- **Group Engine:** `world/group_engine.py` — loot distribution modes
- **Zone Scaling:** `world/zone_scaling.py` — material tier tables
- **Item Spawner:** `world/item_spawner.py` — `create_item_from_template()` consumes item_def dicts

---
**Last Updated:** 2026-03-30
