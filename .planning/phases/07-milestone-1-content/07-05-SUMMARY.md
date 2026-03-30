---
phase: "07"
plan: "05"
subsystem: ashreach-plains
tags: [zone-content, starter-zone, plains, mobs, loot]
dependency_graph:
  requires: [area-builder, mob-spawner, loot-tables, dialogue-engine]
  provides: [ashreach-plains-zone, plains-mob-templates, plains-loot-tables]
  affects: [zone-registry, named-mob-registry, at-server-startstop]
tech_stack:
  added: []
  patterns: [area-builder-dsl, mob-template-registry, loot-table-data]
key_files:
  created:
    - world/areas/ashreach_plains.py
  modified:
    - world/mob_templates.py
    - world/loot_tables.py
decisions:
  - "Used existing FLAG_VOCABULARY entries (resonant, ancient_presence) instead of inventing new flags per CLAUDE.md convention"
  - "Steppe hawk and alpha ash wolf are is_hunter mobs (D-28); dust beetle is wander mob (D-27)"
  - "Drystone Ruins lore fragments thread base-8 dragon connection without explicit revelation"
  - "Alpha Ash Wolf spawns in deep wolf den (ridge_09) with 120min respawn and unique necklace drop"
metrics:
  duration_seconds: 502
  completed: "2026-03-30T00:31:00Z"
  tasks_completed: 1
  tasks_total: 1
  files_created: 1
  files_modified: 2
---

# Phase 7 Plan 05: Ashreach Plains Summary

Windswept grassland starter zone with 102 rooms, 6 mob types (including named boss), 52 spawn definitions, and full loot/material/lore content using AreaBuilder DSL.

## What Was Built

### Zone Structure (102 rooms)
- **The Ashway Road** (18 rooms): Main route from Vael's Crossing south through the plains. Includes milestone markers, wayside rests, prairie dog colonies, and a crossroads hub.
- **Windswept Grasslands** (20 rooms): Open rolling plains with wolf territory markers, beetle grounds, snake runs, ash circles, and the lone thornwood tree.
- **Drystone Ruins** (15 rooms): Pre-Imperial structures with octagonal platforms, sunken chambers, wind channels, and 5 lore fragments hinting at base-8 dragon builders.
- **Wolf Den Ridge** (15 rooms): Rocky ridge with the Alpha Ash Wolf's den, pack gathering grounds, hidden spring, and gully system.
- **Bandit's Hollow** (18 rooms): Concealed ravine encampment with sentry posts, supply caches, prisoner pit, old mine, and escape route.
- **Warden Outpost** (16 rooms): Ranger station with barracks, watch tower, stable, hermit scholar's hut, and trails to adjacent zones.

### Mob Types (5 base + 1 named)
| Template | Aggression | HP Range | Key Ability | Loot Table |
|----------|-----------|----------|-------------|------------|
| ash_wolf | aggressive | 55-85 | bite (bleed), howl (slow) | pelt, fang, meat |
| plains_viper | cautious | 30-50 | poison_bite (poison) | venom sac, snake skin |
| ashreach_bandit | cautious | 65-95 | slash, dirty_kick (stun) | coins, iron sword, bandage |
| dust_beetle | passive | 25-40 | carapace_slam | chitin plate, beetle ichor |
| steppe_hawk | aggressive | 35-55 | dive, screech (slow) | feathers, talons |
| **Alpha Ash Wolf** | aggressive | 180-250 | rending_bite, rallying_howl, pounce | alpha pelt, fang necklace |

### Field NPCs (3)
1. **Warden Captain Ashwyn** (outpost commander office) -- quest hooks for wolf overpopulation and bandit problem
2. **Hermit Scholar Obed** (hermit's hut) -- quest hook for ruin investigation, lore about pre-Imperial civilization
3. **Merchant Reva** (Ashway merchant campsite) -- traveling Consortium trader

### Content Features
- **52 spawn definitions** across all regions (moderate density per D-19)
- **5 lore fragments** in Drystone Ruins (octagonal patterns, base-8 math, ash basin, wind channel acoustics, oversized seat with four-claw marks)
- **4 crafting materials**: iron_ore, wolfsbane, ashgrass_fiber, flint_shard (all tier 1)
- **3 quest stubs**: wolf cull, bandit clearance, ruin investigation
- **Cross-zone exits**: north to vaels_crossing, east to coastal_zone, west to cantera_forest
- **Hunter mobs**: steppe_hawk (detection_range=4), alpha_ash_wolf (detection_range=4)
- **Wandering mobs**: dust_beetle (wander=True in template)
- **Room state flags**: resonant and ancient_presence on key ruin rooms

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| 1 | e92c7f1 | Zone spec, mob templates, loot tables |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Convention] Used existing FLAG_VOCABULARY entries instead of plan-suggested flags**
- **Found during:** Task 1
- **Issue:** Plan suggested "scorched" and "buried_cache" room state flags, but CLAUDE.md convention requires all flags to be defined in FLAG_VOCABULARY before use. Neither flag exists.
- **Fix:** Used existing valid flags (resonant, ancient_presence) that fit the ruins thematic.
- **Files modified:** world/areas/ashreach_plains.py

## Known Stubs

None -- all data is fully wired to existing systems (AreaBuilder DSL, mob_templates registry, loot_tables registry).

## Self-Check: PASSED
