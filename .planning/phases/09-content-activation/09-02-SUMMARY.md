---
phase: 09-content-activation
plan: 02
subsystem: zone-content-wiring
tags: [trainers, triggers, crafting-stations, zone-specs]
dependency_graph:
  requires: ["09-01"]
  provides: ["trainer-npc-wiring", "recipe-learn-paths", "zone-entry-triggers", "crafting-stations"]
  affects: ["world/areas/vaels_crossing.py", "world/areas/ashreach_plains.py", "world/areas/reth_foothills.py", "world/areas/cantera_edge.py", "world/areas/stormhaven_coast.py"]
tech_stack:
  added: []
  patterns: ["area.trigger() for on_first_visit events", "trainer_id kwarg on area.npc()", "crafting_stations kwarg on area.room()"]
key_files:
  created: []
  modified:
    - world/areas/vaels_crossing.py
    - world/areas/ashreach_plains.py
    - world/areas/reth_foothills.py
    - world/areas/cantera_edge.py
    - world/areas/stormhaven_coast.py
decisions:
  - "Placed Ashreach fishing trainer at stream crossing (outpost_03), herbalism trainer at shallow depression (grass_03)"
  - "Placed Reth climbing trainer at cliff face (wr_cliff_face), wired Halvek as smithing trainer"
  - "Wired Cantera Thaelen as foraging trainer, Kaelen as tracking trainer"
  - "Wired Stormhaven Korrin as navigation trainer, Aldren as swimming trainer"
  - "Spiced fish recipe has two learn paths: Malani in Vael's Crossing + Old Korrin at Stormhaven"
metrics:
  duration_minutes: 8
  completed: "2026-04-02T13:58:00Z"
  tasks_completed: 2
  tasks_total: 2
  files_modified: 5
---

# Phase 09 Plan 02: Zone Trainer Wiring and Content Activation Summary

Wired trainer_id to 18 NPCs across 5 zones, added 12 triggers (entry + recipe learning), 3 campfire stations, and 1 engineering workbench -- making trainers, recipes, and crafting reachable by players in authored content.

## Task Results

### Task 1: Wire trainer_id to Vael's Crossing NPCs + add engineering workbench

**Commit:** `9fadb7c`

- Added `trainer_id=` kwarg to 10 existing NPC calls (8 guild masters, herbalist Ystra, stablehand Korua)
- Added `crafting_stations=["workbench"]` to Gearworks engineering hall room
- Added 5 triggers: zone entry welcome (`vc_first_arrival`), iron chainmail recipe at forge, antidote and stamina tonic recipes at alchemy lab, spiced fish recipe at food stalls
- Zero NPCs removed (D-12 compliance)

### Task 2: Wire wilderness zones -- trainer NPCs, fire pits, triggers

**Commit:** `95f85ed`

**Ashreach Plains:**
- 2 new trainer NPCs: Neddra (fishing, at stream crossing) and Senna (herbalism, at grassland depression)
- Campfire crafting station at merchant campsite (ash_road_09)
- Entry trigger at northern approach (ash_road_01)

**Reth Foothills:**
- Wired trainer_id to existing Foreman Halvek (smithing)
- New climbing trainer NPC Grenn at cliff face (wr_cliff_face)
- Entry trigger at southern terminus (ra_road_south)
- 2 recipe triggers at foreman office: steel sword, iron breastplate

**Cantera Edge:**
- Wired trainer_id to existing Druid Thaelen (foraging) and Warden Kaelen (tracking)
- Campfire crafting station at hunter blind (fe_hunter_blind)
- Entry trigger at forest trailhead (fe_trailhead)

**Stormhaven Coast:**
- Wired trainer_id to existing Old Korrin (navigation) and Captain Aldren (swimming)
- Campfire crafting station at fisherman's rest (hr_fisherman_rest)
- Entry trigger at coastal junction (hr_junction)
- Spiced fish recipe trigger at harbor (sv_harbor)

## Verification Results

| Metric | Required | Actual |
|--------|----------|--------|
| trainer_id= assignments | 14+ | 18 |
| area.trigger() calls | 10+ | 12 |
| learn_recipe actions | 6+ | 7 |
| Engineering workbench | 1 | 1 |
| Campfire stations | 2+ | 3 |
| NPC removals | 0 | 0 |

**Recipe learn paths covered:** iron_chainmail (Vael's forge), antidote (Vael's alchemy), stamina_tonic (Vael's alchemy), spiced_fish (Vael's food stalls + Stormhaven harbor), steel_sword (Reth foreman), iron_breastplate (Reth foreman).

**Deferred:** steel_greatsword recipe has no learn path yet -- deferred to quest rewards in Phase 11 per plan note.

## Deviations from Plan

None -- plan executed exactly as written.

## Known Stubs

None -- all trainer_id values reference real TRAINER_REGISTRY keys from Plan 09-01. All triggers use valid action_type values.

## Self-Check: PASSED

- All 5 zone files exist on disk
- Commit 9fadb7c found (Task 1)
- Commit 95f85ed found (Task 2)
