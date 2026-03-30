---
phase: 07-milestone-1-content
plan: "07"
subsystem: cantera-edge-zone
tags: [zone, content, node-system, layer-1, forest, mobs, loot]
dependency_graph:
  requires: ["07-01", "07-02", "07-03"]
  provides: ["cantera_edge zone spec", "forest mob templates", "forest loot tables", "node zone with L1"]
  affects: ["world/areas/cantera_edge.py", "world/mob_templates.py", "world/loot_tables.py"]
tech_stack:
  added: []
  patterns: ["AreaBuilder DSL zone spec", "node() with layer_1_overrides", "spawn_condition=node_active for L1 mobs"]
key_files:
  created:
    - world/areas/cantera_edge.py
  modified:
    - world/mob_templates.py
    - world/loot_tables.py
decisions:
  - "Resonance node type chosen for forest biome — ancient magic humming through roots/stones"
  - "5 regions: Forest Edge, Deep Cantera, Bone Hollows, Root Caves, The Resonance"
  - "21 Layer 1 room overrides in the Resonance region — complete transformations per D-46"
  - "Pala trees used as key atmospheric element — bone-white branches, amber heartwood, orange sap"
  - "Base-8 mathematical patterns threaded through lore fragments for dragon infrastructure discovery"
  - "The Heartwood Ancient placed at rs_root_throne as named mob"
metrics:
  duration_minutes: 12
  completed: "2026-03-30T00:34:00Z"
---

# Phase 07 Plan 07: Cantera Edge Zone Summary

Dense ancient forest starter zone with active resonance node and Layer 1 corrupted room transformations, 101 rooms across 5 biome regions, 8 mob types (5 base + 3 corrupted L1 variants), named mini-boss, 3 field NPCs with dialogue, and dragon-era lore threading.

## What Was Built

### Zone Structure (101 rooms)

1. **Forest Edge** (~23 rooms) — Transition from plains, Cantera Trail entrance, lighter woods with ferns, birch, and wildlife. Contains Warden's Watch Post and lost traveler camp.

2. **Deep Cantera** (~25 rooms) — Dense old-growth forest. Spider territory, bandit camps, and the first signs of the forest's strangeness (silent pool, twisted paths, amber seep).

3. **The Bone Hollows** (~17 rooms) — Pala tree groves with bone-white branches, amber heartwood, orange sap. Shrine stones with base-8 symbol patterns. Druid hermit camp.

4. **Root Caves** (~15 rooms) — Underground passages beneath ancient trees. Fungal caverns, crystal veins, sap rivers. Exit north to Reth foothills.

5. **The Resonance** (~21 rooms) — Node center. Eight standing stones, warped groves, crystal gardens, stabilization ring. All 21 rooms have Layer 1 overrides.

### Node System

- Node type: `resonance` — ancient magic infrastructure humming through root systems
- Center room: `rs_node_center` ("The Resonance Heart")
- Radius: 5 (affects ~21 rooms in The Resonance region)
- 21 Layer 1 overrides with complete visual transformations:
  - "The Resonance Heart" -> "The Shattered Lens"
  - "Standing Stones" -> "The Singing Pillars"
  - "Crystal Garden" -> "Crystal Eruption"
  - "Warped Grove" -> "The Petrified Spiral"
  - etc.
- Stabilization mechanic: `rs_stabilization_ring` room with sap channel system

### Mob Types (8 total)

**Base mobs (5):**
- `forest_spider` — aggressive, web/bite, poison/slow effects
- `wild_boar` — cautious, high HP, charge/gore, stun/bleed
- `cantera_wolf` — aggressive hunter, BFS chase, bleed
- `vine_creeper` — passive until disturbed, entangle/constrict
- `forest_bandit` — cautious humanoid, bow/sword, bleed

**Corrupted L1 variants (3, spawn_condition="node_active"):**
- `corrupted_treant` — hostile, high HP, root slam/sap spray/bark shield
- `void_wisp` — fast, erratic, resonance pulse/phase shift, arcane damage
- `blighted_stag` — aggressive, crystal antlers, resonance bellow

**Named mob:**
- `heartwood_ancient` — "The Heartwood Ancient", 250-350 HP, 120-min respawn, unique loot (heartwood core, ancient bark plate)

### NPCs (3)

1. **Thaelen** (Druid Hermit) — Studies node instability, topics: node, corruption, stabilization, pala trees
2. **Kaelen** (Warden Ranger) — Tracks corruption spread, quest hook for resupply
3. **Mirren** (Lost Traveler) — Quest hook for escort back to trailhead

### Lore and Materials

- 10 lore fragments total (3 L1 exclusive for Remnance/Echoes domain)
- Base-8 patterns threaded throughout (eight stones, eight symbols, four strokes each)
- 8 harvestable materials: cantera_timber, nightcap_mushroom, bramble_berry, cantera_amber, shelf_fungus, spider_silk, pala_bark, pala_sap, cave_mushroom, resonance_crystal

### Cross-Zone Exits

- East to `vaels_crossing:hg_west_road` (city approach)
- South to `ashreach_expanse:ae_north_treeline` (plains)
- North to `reth_foothills:rf_south_cave` (mountains)

### Loot Tables

- Complete loot tables for all 9 mob types (5 base + 3 corrupted + 1 named)
- L1 corrupted drops are higher value/rarity (resonance motes, corrupted heartwood, crystal antlers)
- Named mob has guaranteed drops with high-tier rare/legendary items

## Deviations from Plan

None - plan executed exactly as written.

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| 1 | dad3933 | feat(07-07): author Cantera Edge forest zone with node system and Layer 1 |

## Self-Check: PASSED

- world/areas/cantera_edge.py: FOUND
- world/mob_templates.py: FOUND
- world/loot_tables.py: FOUND
- Commit dad3933: FOUND
