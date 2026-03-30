---
phase: 07-milestone-1-content
plan: "06"
subsystem: content-zone-reth-foothills
tags: [zone, mountain, content, mobs, loot, npcs]
dependency_graph:
  requires: [area-builder, mob-templates, loot-tables, mob-spawner]
  provides: [reth-foothills-zone, mountain-mob-templates, mountain-loot-tables]
  affects: [zone-registry, named-mob-registry, cross-zone-exits]
tech_stack:
  added: []
  patterns: [area-builder-dsl, mob-template-registry, loot-table-data-driven]
key_files:
  created:
    - world/areas/reth_foothills.py
  modified:
    - world/mob_templates.py
    - world/loot_tables.py
decisions:
  - "Grandmother Spider chosen as named mob (ancient cave spider in deepest cave) over Ironhide rock troll"
  - "8 sub-areas for geographic variety: approach, switchbacks, mine, caves, ridge, overlooks, deepcavern, eastern descent"
  - "Dragon-era eight-fold notation lore threading across mine, overlooks, and deepcavern sub-areas"
metrics:
  duration_minutes: 11
  completed: "2026-03-30"
---

# Phase 7 Plan 06: Reth Foothills Zone Summary

Rugged mountain foothills zone with 102 rooms, cave networks, abandoned mine, 5 mob types, and Grandmother Spider named boss in the deepest cavern.

## Deviations from Plan

None - plan executed exactly as written.

## Task Completion

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Author Reth Foothills zone spec with mob templates and loot tables | 0580f11 | world/areas/reth_foothills.py, world/mob_templates.py, world/loot_tables.py |

## Key Decisions

1. **Named mob selection:** Grandmother Spider -- an ancient cave spider of unnatural intelligence, chosen over Ironhide rock troll because the deep cave system provides a more compelling boss encounter with vertical progression (surface -> caves -> deepcavern -> lair).

2. **Sub-area organization:** 8 distinct sub-areas provide geographic variety and natural exploration flow from plains transition (south) through switchbacks, mine, caves, and ridge to overlooks and eastern descent.

3. **Lore threading:** All 5 lore fragments reference the dragon-era eight-fold mathematical notation, connecting to the same pattern found in Vael's Crossing (Ashwatch Tower, Sunken Temple). The mine was unknowingly dug through a dormant node, and the ancient foundation on the overlooks may be a node resonance amplifier.

## Content Summary

### Zone Structure (102 rooms)
- **Rethward Approach** (12 rooms): Plains-to-foothills transition, warden camp
- **Lower Switchbacks** (14 rooms): Ascending paths, first mob encounters
- **Greystone Mine** (14 rooms): Underground mine shafts, iron/copper ore faces
- **Cave Networks** (16 rooms): Natural cave system, spider territories
- **Western Ridge** (12 rooms): High paths, eagle nesting, hermit cave
- **Mountain Overlooks** (10 rooms): Scenic viewpoints, golem ruins, summit
- **The Deepcavern** (12 rooms): Deep caves, Grandmother Spider's lair
- **Eastern Descent** (12 rooms): Lower slopes, connects to other zones

### Mob Types (5 base + 1 named)
| Mob | Aggression | HP Range | Speed | Key Abilities |
|-----|-----------|----------|-------|---------------|
| Rock Troll | aggressive | 120-180 | 0.7 | troll_slam (stun), throw_rock |
| Mountain Cat | cautious | 50-75 | 1.3 | cat_pounce (stun), cat_claw (bleed) |
| Cave Spider | aggressive | 30-50 | 1.2 | spider_web (slow), venomous_bite (poison) |
| Stone Golem Fragment | passive | 150-220 | 0.5 | golem_pound (stun) |
| Reth Eagle | aggressive | 45-70 | 1.2 | eagle_dive (bleed), wing_buffet (stun) |
| **Grandmother Spider** | aggressive | 300-400 | 0.9 | web_cage (slow), venomous_bite (poison), silk_storm (blind) |

### Field NPCs (3)
1. **Foreman Halvek** (Consortium) - Greystone Mine, quest about lost miners
2. **Warden Captain Serra** (Wardens) - Patrol camp, quest about troll activity
3. **Hermit Alchemist Old Renn** (neutral) - Western ridge cave, rare ingredients

### Cross-Zone Exits
- South to `vaels_crossing:hg_north_road`
- West to `cantera_approach:ca_mountain_trail`

## Known Stubs

None -- all data is fully wired. NPCs use stub dialogue (no dialogue dicts passed), which is the established pattern from vaels_crossing and will be populated in a dialogue content plan.

## Self-Check: PASSED
