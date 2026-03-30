---
phase: 07-milestone-1-content
plan: 09
subsystem: equipment-catalog
tags: [equipment, items, crafting, consumables, material-tiers]
dependency_graph:
  requires: [07-01, 07-02]
  provides: [equipment-catalog, m1-crafting-recipes]
  affects: [loot-tables, vendors, item-spawner]
tech_stack:
  added: []
  patterns: [area-builder-item-dsl, recipe-registry]
key_files:
  created:
    - world/areas/equipment_catalog.py
  modified:
    - world/crafting_definitions.py
decisions:
  - "3 material tiers: iron (base), steel (~1.5x), mithril (~2x rare)"
  - "Light armor = leather/shadowsilk (agility), heavy armor = iron/steel/mithril plate (strength)"
  - "Rings defined as ring1 with auto-fill to ring2 per existing can_equip() logic"
  - "Consumable potions use use_effect dict for future effect implementation"
  - "Smithing recipes default_known for iron tier, discovered for steel/iron_breastplate"
metrics:
  duration_minutes: 5
  completed: "2026-03-30T00:27:00Z"
  tasks_completed: 2
  tasks_total: 2
---

# Phase 7 Plan 9: Equipment Catalog Summary

76 equipment items across 3 material tiers (iron/steel/mithril) covering all 13 slots, plus 11 new crafting recipes for smithing, alchemy, and cooking.

## What Was Built

### Task 1: Equipment Catalog (76 items)

Created `world/areas/equipment_catalog.py` as a utility zone spec defining all M1 equipment via `area.item()`.

**Weapons (21 items, 7 types x 3 tiers):**
- Sword, Dagger, Mace (one-handed) -- strength/agility scaling
- Staff, Greatsword, Greataxe, Bow (two-handed) -- higher damage, both hand slots
- All weapons have damage_min/damage_max + scaling_stat + stat_bonuses

**Shields (6 items, 2 types x 3 tiers):**
- Buckler (light, small armor_value) and Kite Shield (heavy, larger armor_value)
- Passive off_hand armor per D-39

**Armor (30 items, 2 sets x 5 slots x 3 tiers):**
- Light set: leather/hardened/shadowsilk -- agility-friendly stat bonuses
- Heavy set: iron/steel/mithril plate -- strength/endurance bonuses

**Accessories (15 items):**
- 3 cloaks (back), 2 bracers (wrists), 4 rings (ring1), 3 amulets, 2 face items

**Consumables (4 items):**
- Minor Healing Potion, Minor Stamina Potion, Antidote, Linen Bandage
- Each with use_effect dict for future effect system wiring

### Task 2: Extended Crafting Recipes (11 new, 19 total)

Extended `world/crafting_definitions.py` RECIPE_REGISTRY:
- **7 smithing:** iron sword, iron mace, steel sword, iron buckler, iron helm, iron breastplate, steel greatsword
- **2 alchemy:** minor healing potion, minor stamina potion
- **2 cooking:** cooked meat, herb poultice
- All output template_ids reference equipment catalog item IDs

## Stat Scaling by Tier

| Tier | Material | Stat Bonus | Damage Mult | Rarity |
|------|----------|-----------|-------------|--------|
| 1 | Iron/Leather | +1 | 1.0x | normal |
| 2 | Steel/Hardened | +2 | ~1.5x | normal |
| 3 | Mithril/Shadowsilk | +3 to +5 | ~2.0x | rare |

## Deviations from Plan

None -- plan executed exactly as written.

## Known Stubs

- `use_effect` on consumables is a data dict only; no consumption/effect handler wired yet (future plan scope)
- Equipment `scaling_stat` field is defined but scaling formula lives in combat engine (already implemented in Phase 6a)

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| 1 | 18f5896 | Equipment catalog with 76 items across 3 material tiers |
| 2 | da5e86d | Extended RECIPE_REGISTRY with 11 M1 equipment recipes |

## Self-Check: PASSED

- FOUND: world/areas/equipment_catalog.py
- FOUND: world/crafting_definitions.py
- FOUND: commit 18f5896
- FOUND: commit da5e86d
