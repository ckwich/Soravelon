---
phase: 13-gathering-and-refining
plan: 03
subsystem: crafting
tags: [crafting, processing, recipes, conversion-ratio, quality-propagation]

requires:
  - phase: 13-01
    provides: "MATERIAL_REGISTRY with 18 materials, tiers, processing metadata"
provides:
  - "18 processing recipes in RECIPE_REGISTRY converting raw materials to crafting ingredients"
  - "get_conversion_quantity() for skill-based 3:1/2:1/1:1 conversion (D-08)"
  - "calculate_processing_quality() for raw quality propagation (D-07)"
  - "Processing branch in craft_item() using inline output dicts"
affects: [crafting-system, gathering-commands, item-economy]

tech-stack:
  added: []
  patterns:
    - "Processing recipes use recipe_type='processing' and item_id-based output dicts"
    - "conversion_ratio field with thresholds/quantities arrays for skill-gated efficiency"

key-files:
  created: []
  modified:
    - world/crafting_definitions.py
    - world/crafting_engine.py

key-decisions:
  - "Extended all 18 MATERIAL_REGISTRY materials (not just minimum 8) for complete pipeline coverage"
  - "Processing output uses item_id-based dict (not template_id) to distinguish from standard crafting recipes"
  - "Processing items tagged with item_id in item_tag category for downstream recipe ingredient matching"

patterns-established:
  - "Processing recipes: recipe_type='processing' + conversion_ratio + item_id output dict"
  - "Quality propagation: average of raw material index and skill-based index (D-07)"

requirements-completed: [SC-3]

duration: 3min
completed: 2026-04-04
---

# Phase 13 Plan 03: Processing Recipes and Conversion Ratios Summary

**18 processing recipes spanning all 6 material categories with skill-based conversion ratios (3:1/2:1/1:1) and quality propagation through the existing crafting pipeline**

## Performance

- **Duration:** 3 min
- **Started:** 2026-04-04T02:49:14Z
- **Completed:** 2026-04-04T02:52:27Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Added 18 processing recipes to RECIPE_REGISTRY covering ore, herb, wood, forage, fish, and hide categories
- Implemented skill-based conversion ratio system (D-08): low skill needs 3 raw materials, mid needs 2, high needs 1
- Added quality propagation for processing (D-07): raw material quality averaged with skill-based quality
- Extended craft_item with processing branch that creates items via create_item_from_template with inline output dicts

## Task Commits

Each task was committed atomically:

1. **Task 1: Add processing recipes to RECIPE_REGISTRY** - `4b8571d` (feat)
2. **Task 2: Extend crafting engine for conversion ratios and processing output** - `9f1c61c` (feat)

## Files Created/Modified
- `world/crafting_definitions.py` - Added 18 processing recipes with recipe_type, conversion_ratio, and output dicts
- `world/crafting_engine.py` - Added get_conversion_quantity(), calculate_processing_quality(), extended _check_ingredients and craft_item

## Decisions Made
- Extended all 18 MATERIAL_REGISTRY materials into processing recipes (plan minimum was 8-10) for complete raw-to-processed pipeline coverage across all gathering categories
- Processing output uses `item_id` key in output dict to distinguish from standard crafting recipes that use `template_id` -- the `recipe_type == "processing"` check gates the new craft_item branch
- Processing items receive an `item_tag` matching their `item_id` so downstream crafting recipes (e.g., iron_sword requiring iron_ingot) find them via the same tag-based ingredient matching

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Known Stubs
None - all processing recipes have complete output definitions and the crafting engine handles them end-to-end.

## Next Phase Readiness
- Processing recipes ready for gathering commands (future plans) to feed raw materials
- Existing crafting commands (smith, brew, cook, craft) work for processing without modification
- Quality propagation wired -- raw material quality influences processing output quality

---
*Phase: 13-gathering-and-refining*
*Completed: 2026-04-04*
