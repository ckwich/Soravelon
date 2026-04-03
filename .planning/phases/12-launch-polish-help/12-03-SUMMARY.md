---
phase: 12-launch-polish-help
plan: 03
subsystem: lore-journal
tags: [commands, lore, journal, search-bugfix]
dependency_graph:
  requires: [area_builder, cmd_search]
  provides: [cmd_lore, lore_registry]
  affects: [default_cmdsets, cmd_search]
tech_stack:
  added: []
  patterns: [static-registry-pattern, zone-grouped-fragments]
key_files:
  created:
    - commands/cmd_lore.py
    - world/lore_registry.py
  modified:
    - commands/cmd_search.py
    - commands/default_cmdsets.py
decisions:
  - Included all 32 lore fragments from 5 zones (not just cantera_edge 13) for complete registry
metrics:
  duration_seconds: 275
  completed: "2026-04-03T22:25:37Z"
---

# Phase 12 Plan 03: Lore Journal Command Summary

CmdLore journal with zone-grouped fragment display and static lore registry containing all 32 fragments across 5 zones.

## What Was Built

### Task 1: Lore Registry + cmd_search Bug Fix
**Commit:** `7dd466c`

- Created `world/lore_registry.py` with `LORE_FRAGMENTS` dict mapping 32 fragment_ids to metadata (zone, title, text)
- Populated from all 5 area files: Cantera Edge (13), Stormhaven Coast (5), Reth Foothills (5), Ashreach Plains (5), Vael's Crossing (4)
- Helper functions: `get_zone_fragments(zone_id)`, `get_all_zones()`, `get_fragment(fragment_id)`
- Fixed pre-existing bug in `commands/cmd_search.py`: `frag.get("id")` changed to `frag.get("fragment_id")` to match area_builder's stored key

### Task 2: CmdLore Command + CmdSet Registration
**Commit:** `bea4c8a`

- Created `commands/cmd_lore.py` with `CmdLore` command (key="lore", aliases=["journal", "lore journal"])
- `lore` (no args): Shows zone overview with collected/total fragment counts
- `lore <zone>`: Shows collected fragment text for that zone with titles
- Partial zone name matching (case-insensitive)
- Empty state messages for no fragments collected and no zones discovered
- Registered in `CharacterCmdSet` in `commands/default_cmdsets.py`

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical Functionality] Included all zone fragments**
- **Found during:** Task 1
- **Issue:** Plan specified only 13 cantera_edge fragments, but 4 other zones also had lore fragments (19 additional)
- **Fix:** Populated registry with all 32 fragments from all 5 zones for a complete journal experience
- **Files modified:** world/lore_registry.py

**2. [Rule 3 - Blocking Issue] Corrupt git index from worktree sparse-checkout**
- **Found during:** Task 2 commit
- **Issue:** Worktree index contained corrupt blob references from another repository's sparse-checkout
- **Fix:** Used `git read-tree HEAD` to reset index to match HEAD tree, then re-staged files
- **Files modified:** None (git infrastructure)

## Known Stubs

None -- all data is fully wired from area files to the registry.

## Verification Results

- Lore registry: 32 fragments in 5 zones
- CmdLore class found with correct key ("lore") and aliases (["journal", "lore journal"])
- CmdLore registered in default_cmdsets.py (2 occurrences: import + add)
- cmd_search.py uses corrected "fragment_id" key
