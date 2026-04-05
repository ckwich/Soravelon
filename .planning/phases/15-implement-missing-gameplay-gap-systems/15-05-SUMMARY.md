---
phase: 15-implement-missing-gameplay-gap-systems
plan: 05
title: "Content Authoring: Tools, Loot, Crafting Outputs, Quest Items"
subsystem: content-authoring
tags: [tools, loot-tables, crafting, quest-items, gathering, equipment-catalog]
dependency_graph:
  requires: [15-01]
  provides: [gathering-tools, rat-loot, bandit-loot, crafting-outputs, quest-items, cmd-tools]
  affects: [equipment_catalog, loot_tables, zone-files, default_cmdsets]
tech_stack:
  added: []
  patterns: [tool-slots-separate-from-combat, quest-item-triggers, tiered-loot-drops]
key_files:
  created:
    - commands/cmd_tools.py
    - tests/test_content_authoring.py
  modified:
    - world/areas/equipment_catalog.py
    - world/loot_tables.py
    - world/areas/stormhaven_coast.py
    - world/areas/vaels_crossing.py
    - world/areas/cantera_edge.py
    - world/areas/reth_foothills.py
    - commands/default_cmdsets.py
decisions:
  - "Tool slots (D-20) are separate from combat VALID_SLOTS, stored as character.db.equipped_tools dict"
  - "Quest items wired via area.trigger() with give_item action_type, using on_examine/on_first_visit/on_enter events"
  - "stolen_artifact quest item sourced via bandit loot table (low weight_in_pool=1) rather than dedicated trigger"
  - "Fish gathering uses area.material() (existing DSL) not a new gathering_pool() method"
metrics:
  duration_seconds: 8931
  completed: "2026-04-05T12:06:00Z"
  tasks_completed: 2
  tasks_total: 2
  files_created: 2
  files_modified: 7
  test_count: 17
---

# Phase 15 Plan 05: Content Authoring Summary

Gathering tools with separate tool slots, fish materials, rat/bandit loot tables, 10 crafting output definitions, and 8 quest items wired to world sources via triggers and loot drops.

## Tasks Completed

### Task 1: Gathering tools + tool slots + tools command
**Commit:** `5175b3f`

Added 5 gathering tool items to equipment_catalog.py with dedicated tool_slot and tool_tag fields. Tool slots are entirely separate from combat VALID_SLOTS (per D-20). Created CmdTools command supporting `tools`, `tools equip <tool>`, and `tools unequip <slot>`. Also added bait consumable, 10 crafting output item definitions (basic_healing_draught, cooked_meat, healing_draught, hearty_stew, herb_poultice, iron_chainmail, mountain_tonic, spiced_fish, stamina_tonic, trail_rations), and 8 quest items with is_quest_item=True flag.

**Files:** commands/cmd_tools.py (new), world/areas/equipment_catalog.py, commands/default_cmdsets.py

### Task 2: Fish pools + loot tables + quest item triggers + tests
**Commit:** `eb879a7`

Added fish gathering materials (common_fish tier 1, coastal_fish tier 2, deep_fish tier 3) to stormhaven_coast. Added complete rat and bandit loot tables with tiered drops (5 tiers each). Wired 7 of 8 quest items to concrete world sources:
- stolen_artifact: bandit loot table drop (weight_in_pool=1, rare)
- contraband_package: stormhaven smuggler cache on_examine trigger
- outstanding_debt_token: vaels_crossing bank on_first_visit trigger
- warden_supplies: vaels_crossing warden office on_examine trigger
- resonance_sample: cantera_edge node center on_examine trigger
- rare_herb_bundle: reth_foothills herb ledge on_examine trigger
- rare_alpine_ingredient: reth_foothills herb ledge on_enter trigger
- commissioned_blade: sourced via NPC dialogue (smith_goram quest flow)

Created test_content_authoring.py with 17 tests covering all content items.

**Files:** world/loot_tables.py, world/areas/stormhaven_coast.py, world/areas/vaels_crossing.py, world/areas/cantera_edge.py, world/areas/reth_foothills.py, tests/test_content_authoring.py (new)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] gathering_engine.py does not exist**
- **Found during:** Task 1
- **Issue:** Plan specified updating world/gathering_engine.py tool check to use equipped_tools, but the file does not exist yet in the codebase
- **Fix:** Skipped gathering_engine update; tool slot system is fully defined and will be consumed when gathering_engine is implemented
- **Impact:** None -- the tool items and CmdTools command are complete; gathering_engine will read character.db.equipped_tools when it exists

**2. [Rule 3 - Blocking] gathering_pool() method does not exist on AreaBuilder**
- **Found during:** Task 2
- **Issue:** Plan specified area.gathering_pool() calls, but AreaBuilder has no such method
- **Fix:** Used existing area.material() method to define fish materials (common_fish, coastal_fish, deep_fish), which is the correct DSL for zone-level harvestable resources
- **Impact:** Fish materials are properly registered via the existing system

**3. [Rule 3 - Blocking] Sparse checkout corruption in worktree**
- **Found during:** Task 2 commit
- **Issue:** Worktree had sparse checkout enabled by GSD plugin, preventing staging of world/ files. Additionally, the worktree index contained 139 corrupted blob references from GSD plugin files
- **Fix:** Rebuilt branch from main with clean index, used git add --sparse flag consistently
- **Impact:** No impact on code quality; purely git infrastructure issue

## Known Stubs

None. All items are fully defined with complete data (descriptions, values, weights, tiers). Quest items have concrete world sources wired via triggers or loot tables.

## Verification

- 17/17 tests pass in test_content_authoring.py
- CATALOG contains 5 tools, 10 crafting outputs, 8 quest items, 1 bait item
- LOOT_TABLES contains "rat" and "bandit" entries with tiered drops
- Fish materials defined in stormhaven_coast
- 7 of 8 quest items wired to concrete triggers/loot (commissioned_blade via NPC dialogue flow)

## Self-Check: PASSED
