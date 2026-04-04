---
phase: 13-gathering-and-refining
verified: 2026-04-03T22:00:00Z
status: passed
score: 8/8 must-haves verified
re_verification: false
---

# Phase 13: Gathering and Refining Verification Report

**Phase Goal:** Resource gathering nodes spawn stochastically in flagged rooms with zone-wide pool limits, players use skill-specific commands (mine, harvest, chop, forage, fish, butcher) to extract raw materials, processing recipes convert raw materials into crafting ingredients (ore->ingot, fiber->thread->cloth), a fishing mini-game and idle mode exist, tools with durability are required, and a scalable 5-tier MATERIAL_REGISTRY organizes all materials
**Verified:** 2026-04-03
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Gathering nodes spawn randomly in eligible rooms per zone-level gathering_pool() definitions with max_active limits; depleted nodes respawn in different eligible rooms | VERIFIED | `world/gathering_engine.py` (555 lines): `spawn_gathering_pool()` creates `GatheringPoolScript` on zone objects, `spawn_node_in_pool()` picks random eligible rooms, `_prune_and_refill()` enforces max_active, `deplete_node()` schedules respawn via `evennia.utils.delay()` excluding depleted room. `world/area_builder.py` line 952: `gathering_pool()` DSL method stores pool defs on zone, line 1056: `initialize_zone_gathering()` called from `build()`. |
| 2 | Players use mine/harvest/chop/forage/fish/butcher commands with required tools; gathering delay varies by tier and is reduced by skill (min 40% of base) | VERIFIED | `commands/cmd_gathering.py` (342 lines): `_BaseGatherCmd` with tool check (`_find_tool` via item_tag), delay calculation `max(base_delay * 0.4, base_delay * (1 - reduction))`, 5 concrete commands (CmdMine, CmdHarvest, CmdChop, CmdForage, CmdButcher). All registered in `commands/default_cmdsets.py` lines 112-125. |
| 3 | Processing recipes in RECIPE_REGISTRY convert raw materials to crafting ingredients with skill-based conversion ratios (3:1->2:1->1:1) and quality propagation | VERIFIED | `world/crafting_definitions.py`: 15+ processing recipes with `recipe_type: "processing"` and `conversion_ratio: {"thresholds": [30, 60, 85], "quantities": [3, 2, 1]}`. `world/crafting_engine.py` line 179: `get_conversion_quantity()` reads ratio, line 235: called from `_check_ingredients()`, line 204: `calculate_processing_quality()` handles quality propagation. |
| 4 | MATERIAL_REGISTRY in world/material_definitions.py defines all materials with 5 expandable tiers, categories, and skill mappings | VERIFIED | `world/material_definitions.py` (286 lines): `MATERIAL_TIERS` (5 tiers), `GATHERING_CATEGORIES` (6 categories: ore, herb, wood, forage, fish, hide), `MATERIAL_REGISTRY` with 18 materials across all categories and tiers 1-3, each with required keys (display_name, category, tier, raw_form, processed_form, gathering_skill, processing_skill, processing_station, visibility). |
| 5 | Fishing has an active mini-game (cast->bite->reel) with full rewards and an idle mode with diminished returns | VERIFIED | `commands/cmd_fishing.py` (332 lines): `CmdFish` with active mode state machine (cast -> `_on_bite` with 5-15s timer -> `_on_reel` within 4s window), idle mode via `_start_idle_fishing` with 15-30s intervals, `_catch_fish` with `quality_multiplier` (1.0 active, 0.5 idle drops quality by one tier). `CmdReel` delegates to `CmdFish._on_reel`. Bait improves timers and quality. |
| 6 | Tools degrade with use and are repairable via smithing; no tool = cannot gather | VERIFIED | `_BaseGatherCmd._find_tool()` checks item_tag, returns None if missing -> blocks gather. Durability decremented in `_gather_callback` line 149. `CmdRepair` in `commands/cmd_prospect.py` line 95: requires workbench station, uses smithing skill, repair amount scales with skill (10 + smithing/5). `TOOL_DURABILITY` dict in material_definitions.py defines max_durability per tool type. |
| 7 | Prospect/survey reveals nodes in straight lines with directional indicators; Sense gives vague hints; tiered visibility gates mid/high-tier nodes by skill | VERIFIED | `CmdProspect` in `commands/cmd_prospect.py` (167 lines): calls `prospect_scan()` which walks cardinal exits in straight lines. Output shows direction, distance, material, tier, richness. `GatheringNode.get_display_name()` in objects.py line 279: checks `VISIBILITY_THRESHOLDS` vs player skill, returns None for hidden nodes. `CmdSense` in cmd_sense.py reads gathering flags from SENSE_DISPLAY (mineral_deposits, rich_soil, dense_foliage, water_source). |
| 8 | Mob loot drops (hides, bones, silk) feed into the processing pipeline as raw materials | VERIFIED | `world/gathering_engine.py` line 513: `BUTCHER_YIELDS` maps mob types (boar, ash_wolf, spider, drake) to material drops (hides, bones, silk, meat). `get_butcher_yields()` with fallback to generic yields. `CmdButcher._gather_callback` creates items via `item_spawner.create_item_from_template`. `CorpseContainer.can_butcher()` in objects.py line 159 gates access. Mob `at_death` stores `mob_key` on corpse. |

**Score:** 8/8 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `world/material_definitions.py` | MATERIAL_REGISTRY, tiers, categories, delays, visibility | VERIFIED | 286 lines, all exports present |
| `world/gathering_engine.py` | spawn/deplete/gather/prospect functions, pool script | VERIFIED | 555 lines, full lifecycle engine |
| `typeclasses/objects.py` | GatheringNode typeclass | VERIFIED | Lines 260-290, skill-gated visibility |
| `world/area_builder.py` | gathering_pool() DSL | VERIFIED | Line 952, stores on zone, build() calls initialize |
| `world/crafting_definitions.py` | Processing recipes with conversion_ratio | VERIFIED | 15+ processing recipes with recipe_type and conversion_ratio |
| `world/crafting_engine.py` | get_conversion_quantity, quality propagation | VERIFIED | Lines 179-199 (conversion), 204-220 (quality), wired into _check_ingredients |
| `commands/cmd_gathering.py` | _BaseGatherCmd + 5 concrete commands | VERIFIED | 342 lines, all 5 commands with tool/skill/delay logic |
| `commands/cmd_fishing.py` | CmdFish (active + idle) + CmdReel | VERIFIED | 332 lines, full state machine |
| `commands/cmd_prospect.py` | CmdProspect, CmdRepair | VERIFIED | 167 lines, straight-line scan + tool repair |
| `commands/cmd_sense.py` | Gathering hints in Sense output | VERIFIED | 63 lines, reads SENSE_DISPLAY for gathering flags |
| `commands/default_cmdsets.py` | All commands registered | VERIFIED | Lines 112-125: all 10 commands registered |
| `world/room_state.py` | Gathering flags in FLAG_VOCABULARY | VERIFIED | mineral_deposits, rich_soil, dense_foliage, water_source + SENSE_DISPLAY entries |
| `world/item_spawner.py` | item_tag on created items | VERIFIED | Line 75: tags.add(item_id, category="item_tag") |
| `world/skill_definitions.py` | mining, woodcutting, skinning skills | VERIFIED | Lines 353, 367, 381 |
| `tests/test_gathering.py` | Tests for SC-1 through SC-8 | VERIFIED | 607 lines, 41 test methods |
| `tests/test_fishing.py` | Tests for fishing modes | VERIFIED | 335 lines, 18 test methods |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| gathering_engine.py | material_definitions.py | MATERIAL_REGISTRY import | WIRED | `from world.material_definitions import` at line 141 |
| area_builder.py | gathering_engine.py | initialize_zone_gathering() | WIRED | Line 1056: import + call from build() |
| gathering_engine.py | typeclasses/objects.py | creates GatheringNode | WIRED | Line 186: `from typeclasses.objects import GatheringNode` |
| cmd_gathering.py | gathering_engine.py | gather_from_node() | WIRED | Line 102: import + call in _gather_callback |
| cmd_gathering.py | material_definitions.py | GATHERING_CATEGORIES | WIRED | Line 64: import GATHER_DELAY_BY_TIER, line 74: MATERIAL_REGISTRY |
| cmd_gathering.py | item_spawner.py | create_item_from_template | WIRED | Line 114: import + call to create gathered items |
| cmd_fishing.py | gathering_engine.py | gather_from_node | WIRED | Line 228: import + call in _catch_fish |
| cmd_fishing.py | material_definitions.py | MATERIAL_REGISTRY | WIRED | Line 229: import in _catch_fish |
| cmd_prospect.py | gathering_engine.py | prospect_scan | WIRED | Line 50: import + call |
| crafting_engine.py | crafting_definitions.py | conversion_ratio | WIRED | Line 235: get_conversion_quantity called from _check_ingredients |
| default_cmdsets.py | all gathering commands | import + add | WIRED | Lines 112-125: all 10 commands imported and added |
| tests/test_gathering.py | gathering_engine.py | import tested functions | WIRED | Tests import and exercise spawn, gather, prospect functions |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| GatheringNode | material_id, tier, gathers_remaining | MATERIAL_REGISTRY via spawn_node_in_pool | Yes -- random material from pool, random gathers 2-6 | FLOWING |
| cmd_gathering.py | gathered items | gather_from_node -> item_spawner | Yes -- creates real items with quality/value | FLOWING |
| cmd_fishing.py | caught fish items | gather_from_node -> item_spawner | Yes -- creates items with quality tiers | FLOWING |
| cmd_prospect.py | scan results | prospect_scan straight-line walk | Yes -- returns real node objects with direction/distance | FLOWING |
| crafting_engine.py | conversion_quantity | get_conversion_quantity from recipe | Yes -- skill-based threshold lookup (3/2/1) | FLOWING |

### Behavioral Spot-Checks

Step 7b: SKIPPED (Evennia server not running; requires full Django/Twisted stack for typeclass resolution)

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| SC-1 | 13-02, 13-07 | Gathering nodes spawn randomly with pool limits, depleted respawn different room | SATISFIED | gathering_engine.py full lifecycle |
| SC-2 | 13-04, 13-07 | mine/harvest/chop/forage/fish/butcher with tools, skill-based delay | SATISFIED | cmd_gathering.py 5 commands + cmd_fishing.py |
| SC-3 | 13-03, 13-07 | Processing recipes with conversion ratios (3:1->2:1->1:1) | SATISFIED | crafting_definitions.py recipes + crafting_engine.py get_conversion_quantity |
| SC-4 | 13-01, 13-07 | MATERIAL_REGISTRY with 5 tiers, categories, skill mappings | SATISFIED | material_definitions.py 286 lines, 18 materials |
| SC-5 | 13-05, 13-07 | Fishing active mini-game + idle mode with diminished returns | SATISFIED | cmd_fishing.py state machine, quality_multiplier 0.5 for idle |
| SC-6 | 13-04, 13-06, 13-07 | Tool durability + repair via smithing | SATISFIED | _BaseGatherCmd durability deduction + CmdRepair |
| SC-7 | 13-06, 13-07 | Prospect/survey straight-line scan + Sense hints + visibility gates | SATISFIED | CmdProspect + prospect_scan + GatheringNode.get_display_name + SENSE_DISPLAY |
| SC-8 | 13-01, 13-07 | Mob loot drops feed processing pipeline | SATISFIED | BUTCHER_YIELDS + CmdButcher + CorpseContainer.can_butcher |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| None | - | No TODO/FIXME/placeholder patterns found | - | - |

### Human Verification Required

### 1. Gathering Command Flow

**Test:** Start server, create a pickaxe item with item_tag "pickaxe", spawn an ore GatheringNode in the room, run `mine`, wait for delay, verify item appears in inventory.
**Expected:** "You begin to mine Iron Ore..." then after delay "You gather [quality] Iron Ore." Item in inventory with item_tag.
**Why human:** Requires running Evennia server with full typeclass resolution and delay() system.

### 2. Fishing Active Mode Flow

**Test:** Equip fishing rod, go to room with fish GatheringNode, run `fish`, wait for bite message, type `reel`.
**Expected:** Cast message, bite notification within 5-15s, successful catch on reel, fish item in inventory.
**Why human:** Requires real-time timer interaction and server event loop.

### 3. Prospect Scan Output

**Test:** Place gathering nodes in adjacent rooms connected by cardinal exits, run `prospect`.
**Expected:** Directional indicators with distance, material name, tier, and richness for each detected node.
**Why human:** Requires multi-room setup with exits and live node objects.

### Gaps Summary

No gaps found. All 8 success criteria are satisfied with substantive, wired implementations. The gathering system is fully built:

- Material data layer (286 lines) with 18 materials across 6 categories and 5 tiers
- Gathering engine (555 lines) with stochastic spawning, pool lifecycle, and prospect scanning
- 7 player commands (mine, harvest, chop, forage, butcher, fish, reel) plus prospect/survey and repair
- Processing pipeline with 15+ conversion recipes and skill-based ratios
- Tool durability system with repair at workbenches
- Skill-gated node visibility (low/mid/high thresholds)
- Sense integration with gathering room state flags
- Butcher system connected to mob corpses
- 59 automated tests across 2 test files (607 + 335 lines)
- All commands registered in CharacterCmdSet

---

_Verified: 2026-04-03_
_Verifier: Claude (gsd-verifier)_
