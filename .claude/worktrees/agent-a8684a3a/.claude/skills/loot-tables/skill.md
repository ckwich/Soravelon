---
name: loot-tables
description: Loot system stubs, rarity-based drop modifiers, group loot modes, and material tier scaling
---

## Activation

This skill triggers when editing these files:
- `world/loot_tables.py`
- `world/group_engine.py`
- `world/zone_scaling.py`

Keywords: loot, drops, rarity, loot table, loot mode

---

You are working on **soravelon's loot system** — currently a stub awaiting full implementation.

## Key Files
- `world/loot_tables.py` — Rarity-tier modifier dict + `get_loot_modifiers(mob)` (stub)
- `world/group_engine.py` — Group loot mode logic (personal/ffa/round_robin/need_pass)
- `world/zone_scaling.py` — `MATERIAL_TIER_BY_SKILL` + `get_material_tier()` — skill-based loot quality
- `typeclasses/mobs.py` — `Mob.get_loot_tier()` returns `db.rarity` (normal/magic/rare/legendary)

## Key Concepts
- **Rarity tiers:** normal → magic → rare → legendary. Stored in `mob.db.rarity`, default "normal"
- **Loot modifiers:** `LOOT_TIER_MODIFIERS` maps rarity to `extra_rolls`, `tome_chance`, `ancient_chance`
- **Material tiers:** Loot quality is skill-based (1-5), NOT level-based — see `zone_scaling.py`
- **Loot modes:** Group loot defaults to "personal". Quest drops and Scales are ALWAYS personal regardless of mode
- **Groups are session-only (`ndb`)** — loot mode dissolves when leader disconnects

## Critical Rules
1. **Quest drops and Scales bypass loot mode** — always personal, never shared/rolled
2. **Loot quality scales with skill score, not character level** — use `get_material_tier()`
3. **`loot_tables.py` is a stub** — actual drop tables not yet implemented. New loot logic goes here
4. **Rarity fallback** — always default to "normal" if `mob.db.rarity` is missing/unknown
5. **Follow `(bool, str)` return convention** from base skill for any new loot functions

## References
- **Mob Affixes:** `world/mob_affixes.py` — rarity tier definitions that feed loot modifiers
- **Group Engine:** `world/group_engine.py` — loot distribution modes
- **Zone Scaling:** `world/zone_scaling.py` — material tier tables

---
**Last Updated:** 2026-03-23
