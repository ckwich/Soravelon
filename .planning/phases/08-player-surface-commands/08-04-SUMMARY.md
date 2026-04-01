---
phase: 08-player-surface-commands
plan: "04"
subsystem: commands
tags: [search, consumable, loadout, unified-use]
dependency_graph:
  requires: [skill_engine, ability_engine, inventory_engine, base_attributes]
  provides: [CmdSearch, consumable_item_use, loadout_gate]
  affects: [cmd_abilities.py, default_cmdsets.py]
tech_stack:
  added: []
  patterns: [unified-command-dispatcher, skill-check-vs-dc, per-room-cooldown]
key_files:
  created:
    - commands/cmd_search.py
  modified:
    - commands/cmd_abilities.py
    - commands/default_cmdsets.py
decisions:
  - "Loadout gate placed in ability branch of func() after ability_id resolution, before dispatch"
  - "Item consumption branch runs before ability resolution -- consumable items take priority"
  - "Empty loadout allows all abilities (backward compat)"
metrics:
  duration_seconds: 194
  completed: "2026-04-01T20:45:30Z"
  tasks_completed: 3
  tasks_total: 3
---

# Phase 08 Plan 04: Search Command and Unified Use Dispatcher Summary

CmdSearch rolls investigation+d20 vs room search_dc with 60s failure cooldown; CmdUseAbility extended as unified dispatcher routing consumable items to _consume_item and abilities through loadout gate.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | CmdSearch -- investigation skill vs search_dc | 4028ac5 | commands/cmd_search.py |
| 2 | Unified use dispatcher -- item consumption + ability routing | e184f06 | commands/cmd_abilities.py |
| 3 | Loadout enforcement gate + CmdSearch registration | 00e919a | commands/default_cmdsets.py |

## Implementation Details

### CmdSearch (commands/cmd_search.py)
- `search` / `investigate` command with investigation skill + d20 roll against room.db.search_dc
- Successful search reveals hidden exits (added to char.db.discovered_exits) and lore fragments (discovery_method == "search")
- Failed search applies 60-second per-room cooldown via char.ndb.search_cooldowns
- Skill XP accumulated on success via accumulate_skill_use

### Unified Use Dispatcher (commands/cmd_abilities.py)
- CmdUseAbility.func() now checks inventory for consumable items BEFORE ability resolution
- New _consume_item method handles heal_amount, stamina_amount, cure_effect from item.db attributes
- Items destroyed after consumption (both InventoryItem record and Evennia object)
- Combat action cost enforced when character is in combat (ndb.in_combat)
- push_inventory_update called after consumption for OOB sync

### Loadout Gate (PSC-06)
- After ability_id resolved, checks character.db.active_loadout
- Empty loadout = all abilities allowed (backward compat)
- Non-empty loadout requires ability_id to be in the list
- Clear error message directs player to use `loadout add` command

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Resolved merge conflicts and corrupt git objects**
- **Found during:** Pre-execution setup
- **Issue:** Branch was behind main; merging brought Wave 1 content but left a stale conflict marker in default_cmdsets.py. Sparse checkout had corrupt objects in index.
- **Fix:** Removed conflict marker, used git read-tree to reset index before staging
- **Files modified:** commands/default_cmdsets.py

## Decisions Made

1. Loadout gate placed in ability branch after ability_id resolution but before target resolution and dispatch
2. Item consumption branch runs first -- consumable items take priority over ability name matching
3. Empty loadout allows all abilities for backward compatibility

## Known Stubs

None -- all functionality is fully wired.
