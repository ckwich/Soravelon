---
phase: 06c-npc-dialogue-and-crafting
plan: 02
subsystem: crafting
tags: [crafting, recipes, quality-tiers, stations, cooking, smithing, alchemy]

requires:
  - phase: 06b-spawn-system-skills-and-mob-ai
    provides: "skill_engine.py get_skill_value/accumulate_skill_use, skill_definitions.py SKILL_DEFINITIONS"
provides:
  - "RECIPE_REGISTRY with 8 starter recipes across cooking/smithing/alchemy"
  - "QUALITY_TIERS and quality calculation with skill-difficulty gap + random variance"
  - "craft_item() main entry point for all crafting commands"
  - "learn_recipe()/get_known_recipes() for recipe discovery system"
  - "check_station() room tag validation for crafting stations"
affects: [06c-05-crafting-commands, content-authoring]

tech-stack:
  added: []
  patterns:
    - "Static recipe registry with CharacterRecipe model for discovery tracking"
    - "Quality tier system: flawed/standard/fine/superior/masterwork with multipliers"
    - "Room tag convention: crafting_{station} in category crafting_station"

key-files:
  created:
    - world/crafting_definitions.py
    - world/crafting_engine.py
  modified: []

key-decisions:
  - "Quality gap thresholds: <0=flawed, <15=standard, <30=fine, <50=superior, 50+=masterwork"
  - "Random variance +/-1 tier with 20/60/20 weighting (center-biased)"
  - "Station bonus adds +1 ceiling to quality roll"
  - "Fallback item creation via basic Evennia object when item_spawner unavailable"

patterns-established:
  - "Crafting station check: room.tags.has(crafting_{station}, category=crafting_station)"
  - "Ingredient check: obj.tags.has(item_tag, category=item_tag) on character.contents"
  - "Default recipes auto-learned via _ensure_default_recipes lazy idempotent creation"

requirements-completed: [SKL-03]

duration: 3min
completed: 2026-03-27
---

# Phase 6c Plan 02: Crafting Definitions & Engine Summary

**Static recipe registry with 8 recipes, quality tier system (flawed-to-masterwork), and full crafting engine with station/ingredient/skill validation**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-27T02:49:17Z
- **Completed:** 2026-03-27T02:52:39Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- RECIPE_REGISTRY with 8 starter recipes: 3 cooking, 2 smithing, 3 alchemy
- Quality calculation maps skill-difficulty gap to 5 tiers with random variance
- Full craft_item pipeline: recipe lookup, station check, ingredient validation, quality roll, item creation, skill accumulation

## Task Commits

Each task was committed atomically:

1. **Task 1: Crafting definitions registry** - `a480d5d` (feat)
2. **Task 2: Crafting engine** - `b530c6b` (feat)

## Files Created/Modified
- `world/crafting_definitions.py` - Pure-data module with RECIPE_REGISTRY, QUALITY_TIERS, STATION_REQUIREMENTS, SKILL_TO_COMMAND
- `world/crafting_engine.py` - Crafting logic: craft_item, calculate_craft_quality, check_station, learn_recipe, get_known_recipes, get_quality_modifier

## Decisions Made
- Quality gap thresholds: <0=flawed, <15=standard, <30=fine, <50=superior, 50+=masterwork
- Random variance uses random.choices with 20/60/20 weights for center-biased +/-1 tier shift
- Station bonus adds +1 to quality ceiling (not base)
- Fallback item creation uses basic SoravelonObject when item_spawner module not available
- _ensure_default_recipes is idempotent via get_or_create, called lazily on first craft/recipe check

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Git sparse-checkout and corrupt .gitattributes object blocked Task 2 commit; resolved by resetting index via git read-tree HEAD before staging

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Crafting definitions and engine ready for crafting commands (Plan 05)
- CharacterRecipe model (Plan 01) needed for recipe discovery persistence at runtime
- Item spawner integration is gracefully handled with fallback

## Self-Check: PASSED

- world/crafting_definitions.py: FOUND
- world/crafting_engine.py: FOUND
- 06c-02-SUMMARY.md: FOUND
- Commit a480d5d: FOUND
- Commit b530c6b: FOUND

---
*Phase: 06c-npc-dialogue-and-crafting*
*Completed: 2026-03-27*
