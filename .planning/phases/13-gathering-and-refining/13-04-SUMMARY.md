---
phase: 13-gathering-and-refining
plan: 04
subsystem: commands
tags: [gathering, mining, herbalism, woodcutting, foraging, skinning, butcher, tool-durability]

requires:
  - phase: 13-01
    provides: "MATERIAL_REGISTRY, GATHERING_CATEGORIES, GATHER_DELAY_BY_TIER, TOOL_DURABILITY"
  - phase: 13-02
    provides: "GatheringNode typeclass, gather_from_node(), deplete_node(), GatheringPoolScript"
provides:
  - "CmdMine, CmdHarvest, CmdChop, CmdForage, CmdButcher gathering commands"
  - "_BaseGatherCmd base class with tool checks, skill delay, durability loss"
  - "get_butcher_yields() for mob-type-specific material extraction"
  - "CorpseContainer.can_butcher() guard method"
affects: [13-05, 13-06, 13-07, content-phases]

tech-stack:
  added: []
  patterns: ["_BaseGatherCmd mirrors _BaseCraftCmd delay/move-cancel pattern", "butcher overrides _find_node and _gather_callback for corpse targeting"]

key-files:
  created: ["commands/cmd_gathering.py"]
  modified: ["world/gathering_engine.py", "typeclasses/objects.py", "world/combat_engine.py"]

key-decisions:
  - "Butcher uses can_butcher() (not can_loot()) for corpse eligibility -- adds butchered and decay guards"
  - "Bonus quantity at skill 50+ (25%) and 80+ (50%) for high-skill reward curve"
  - "BUTCHER_YIELDS fallback gives generic raw_meat + bone_fragment for undefined mob types"

patterns-established:
  - "_BaseGatherCmd pattern: tool check, node find, skill delay, delayed callback with move-cancel"
  - "Butcher override pattern: subclass overrides _find_node and _gather_callback for non-node targets"

requirements-completed: [SC-2, SC-6]

duration: 2min
completed: 2026-04-04
---

# Phase 13 Plan 04: Gathering Commands Summary

**Five gathering commands (mine/harvest/chop/forage/butcher) with tool requirements, skill-based delay reduction, durability loss, and corpse butchering integration**

## Performance

- **Duration:** 2 min
- **Started:** 2026-04-04T02:56:12Z
- **Completed:** 2026-04-04T02:58:35Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- _BaseGatherCmd base class with tool check, node lookup, skill-reduced delay (min 40% of base), quality calculation, bonus quantity, durability loss, and skill XP
- 5 concrete commands: CmdMine (mining/pickaxe/ore), CmdHarvest (herbalism/sickle/herb), CmdChop (woodcutting/hatchet/wood), CmdForage (foraging/no tool/forage), CmdButcher (skinning/skinning_knife/corpses)
- CmdButcher overrides to target CorpseContainer corpses with mob-specific yield tables
- CorpseContainer.can_butcher() prevents double-butchering and respects decay phase

## Task Commits

Each task was committed atomically:

1. **Task 1: Create cmd_gathering.py with _BaseGatherCmd and 5 gathering commands** - `d1a725a` (feat)
2. **Task 2: Mark mob corpses as butcherable and add butcher check** - `a7b1e0e` (feat)

## Files Created/Modified
- `commands/cmd_gathering.py` - New file with _BaseGatherCmd base class and CmdMine, CmdHarvest, CmdChop, CmdForage, CmdButcher
- `world/gathering_engine.py` - Added BUTCHER_YIELDS dict and get_butcher_yields() function
- `typeclasses/objects.py` - Added can_butcher() method and butcherable/butchered flags to CorpseContainer
- `world/combat_engine.py` - Added butcherable/butchered flag initialization in spawn_corpse()

## Decisions Made
- Butcher uses can_butcher() (not can_loot()) for corpse eligibility -- adds butchered-flag and decay guards on top of loot phase checks
- Bonus quantity at skill 50+ (25% chance) and 80+ (50% chance) for rewarding skill investment
- BUTCHER_YIELDS fallback gives generic raw_meat + bone_fragment for undefined mob types -- ensures all corpses yield something
- Butcher delay uses tier_difficulty=15 (fixed) since corpses have no tier attribute

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Gathering commands ready for CmdSet registration (Phase 13-05 or similar)
- Butcher yields integrate with processing pipeline from Plan 13-03
- All 5 commands follow the same delay/move-cancel pattern as crafting commands

---
*Phase: 13-gathering-and-refining*
*Completed: 2026-04-04*
