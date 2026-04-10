---
name: material-registry
description: Material taxonomy — 18 materials across 6 gathering categories, 5 tiers, tool durability, visibility thresholds, and gathering delays
---

## Activation

This skill triggers when editing these files:
- `world/material_definitions.py`

Keywords: material, material registry, gathering, mining, herbalism, woodcutting, foraging, fishing, skinning, ore, herb, wood, hide, fish, forage, material tier, visibility, tool durability, gather delay

---

You are working on **the material registry** (`world/material_definitions.py`) — pure-data taxonomy consumed by gathering, crafting, and area builder systems.

## Key Files
- `world/material_definitions.py` — `MATERIAL_REGISTRY`, `MATERIAL_TIERS`, `GATHERING_CATEGORIES`, `GATHER_DELAY_BY_TIER`, `VISIBILITY_THRESHOLDS`, `TOOL_DURABILITY`

## Key Concepts
- **Pure Python constants, no Django imports:** Data-only module. No models, no Evennia deps. Safe to import anywhere
- **6 gathering categories:** ore (mining/pickaxe), herb (herbalism/sickle), wood (woodcutting/hatchet), forage (foraging/no tool), fish (fishing/fishing_rod), hide (skinning/skinning_knife)
- **5 material tiers:** Common (1), Uncommon (2), Rare (3), Exceptional (4), Legendary (5). Currently 3 materials per category (tiers 1-3), tiers 4-5 reserved for expansion
- **Material entry schema:** `display_name`, `category`, `tier`, `raw_form`, `processed_form`, `gathering_skill`, `processing_skill`, `processing_station`, `visibility`
- **Visibility gating:** `low` (skill 0+), `mid` (skill 30+), `high` (skill 60+) — minimum gathering skill to see nodes. Consumed by `GatheringNode.get_display_name()` for skill-gated visibility
- **Gather delay by tier:** 4s/6s/8s/12s/16s base delay. Skill reduces but never below 40% of base
- **Tool durability:** max_durability (uses before breaking) and repair_cost (Scales). Forage has no tool requirement
- **Processing stations:** forge (smithing), alchemy_bench (alchemy), workbench (engineering), campfire (cooking) — aligns with crafting system stations

## 18 Registered Materials
- **Ores:** iron_ore (T1), steel_ore (T2), mithril_ore (T3) → smithing at forge
- **Herbs:** wild_herb (T1), thornroot (T2), moonpetal (T3) → alchemy at alchemy_bench
- **Wood:** pine_log (T1), oak_log (T2), ironwood_log (T3) → engineering at workbench
- **Forage:** wild_mushroom (T1), cave_moss (T2), starbloom (T3) → cooking/alchemy
- **Fish:** river_trout (T1), cave_eel (T2), shadow_bass (T3) → cooking at campfire
- **Hides:** boar_hide (T1), ash_wolf_pelt (T2), drake_scale (T3) → smithing at workbench

## Critical Rules
1. **Material IDs are registry keys** — all lookups use the string key (e.g. `"iron_ore"`), not display name
2. **Category must match `GATHERING_CATEGORIES` keys** — ore, herb, wood, forage, fish, hide
3. **Tier must match `MATERIAL_TIERS` keys** — integer 1-5
4. **Visibility must match `VISIBILITY_THRESHOLDS` keys** — low, mid, high
5. **Processing stations must align with crafting system** — use existing `STATION_REQUIREMENTS` station names from `crafting_definitions.py`
6. **New materials go in `MATERIAL_REGISTRY`** — add entries as zones introduce new gathering nodes

## References
- **Gathering Engine:** `world/gathering_engine.py` — consumes `MATERIAL_REGISTRY` for node spawning, tier filtering, and visibility
- **Crafting System:** `world/crafting_definitions.py` — `STATION_REQUIREMENTS` defines valid stations
- **Area Builder:** `world/area_builder.py` — `material()` and `gathering_pool()` DSL methods wire materials to zone rooms
- **Skill Engine:** `world/skill_engine.py` — gathering skills (mining, herbalism, etc.) used for visibility and quality

---
**Last Updated:** 2026-04-04
