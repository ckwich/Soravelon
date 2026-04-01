---
phase: 08-player-surface-commands
plan: 01
subsystem: item-spawner, oob-publisher, skill-definitions, area-content
tags: [bugfix, equipment, oob, skills]
dependency_graph:
  requires: [item_spawner, oob_publisher, inventory_engine, skill_definitions, vaels_crossing]
  provides: [fixed_equip_slot, real_inventory_oob, investigation_skill]
  affects: [equipment_system, client_inventory, search_command]
tech_stack:
  added: []
  patterns: [lazy-import-in-oob, equipment_slot-canonical-name]
key_files:
  created: []
  modified:
    - world/item_spawner.py
    - world/areas/vaels_crossing.py
    - world/oob_publisher.py
    - world/skill_definitions.py
decisions:
  - "D-15: item_spawner writes db.equipment_slot (not db.equip_slot) to match SoravelonEquipment.can_equip"
  - "D-16: greatswords use equip_slot='main_hand' + two_handed=True (not 'two_hand')"
  - "D-17: OOB push_inventory_update calls get_inventory_display_data for real item data"
  - "D-11: investigation skill uses remnance domain_bonus, trainer_required_above=50"
metrics:
  duration_seconds: 243
  completed: "2026-04-01T20:34:19Z"
  tasks_completed: 3
  tasks_total: 3
---

# Phase 08 Plan 01: Foundation Fixes and Investigation Skill Summary

Fixed equip_slot schema drift, greatsword slot names, OOB inventory stub, and added investigation skill definition for search command.

## What Was Done

### Task 1: Fix equip_slot schema drift and greatsword slots (D-15, D-16)
- Changed `item.db.equip_slot` to `item.db.equipment_slot` in item_spawner.py line 65, matching what SoravelonEquipment.can_equip() reads
- Changed iron_greatsword and iron_greataxe from `equip_slot="two_hand"` to `equip_slot="main_hand", two_handed=True` in vaels_crossing.py
- **Commit:** 10020c2

### Task 2: Wire OOB push_inventory_update to real data (D-17)
- Replaced empty `{"items": []}` stub with call to `get_inventory_display_data(character)`
- Now sends equipped, carried, containers, keyring, carried_scales, encumbrance, carry_weight, carry_capacity
- **Commit:** b5c46ad

### Task 3: Add investigation skill to SKILL_DEFINITIONS (D-11)
- Added "investigation" general proficiency skill with remnance domain_bonus
- 5 threshold tiers: 25/50/75/90/100 from hidden doors to dragon-era vaults
- trainer_required_above=50 matches other general skills
- **Commit:** 8852e23

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None - all changes are complete implementations.

## Commits

| Task | Commit  | Message |
|------|---------|---------|
| 1    | 10020c2 | fix(08-01): fix equip_slot schema drift and greatsword slot names |
| 2    | b5c46ad | fix(08-01): wire OOB push_inventory_update to real inventory data |
| 3    | 8852e23 | feat(08-01): add investigation skill to SKILL_DEFINITIONS registry |

## Self-Check: PASSED
