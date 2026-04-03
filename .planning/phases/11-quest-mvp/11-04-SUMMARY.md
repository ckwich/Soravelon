---
phase: 11-quest-mvp
plan: 04
subsystem: content
tags: [quest-specs, area-builder, dsl, dark-fantasy, creative-authoring]

# Dependency graph
requires:
  - phase: 11-quest-mvp plan 01
    provides: quest_engine.py with CharacterQuest model and state machine
  - phase: 11-quest-mvp plan 02
    provides: enriched area.quest() DSL signature with objectives/rewards fields
  - phase: 11-quest-mvp plan 03
    provides: quest progress hooks (kill, collect, investigate, deliver, talk_to)
provides:
  - 20 enriched quest specs across 5 zones with names, descriptions, objectives, and rewards
  - Wolf->bandit quest chain connection in Ashreach Plains
  - Node failure mitigation reward in Cantera Edge
  - All 5 MVP objective types exercised (kill, collect, investigate, deliver, talk_to)
affects: [11-quest-mvp plan 05, zone-content, quest-testing]

# Tech tracking
tech-stack:
  added: []
  patterns: [enriched quest spec format with objectives list and rewards list alongside legacy flat fields]

key-files:
  modified:
    - world/areas/vaels_crossing.py
    - world/areas/ashreach_plains.py
    - world/areas/reth_foothills.py
    - world/areas/cantera_edge.py
    - world/areas/stormhaven_coast.py

key-decisions:
  - "Preserved all legacy flat fields (objective_type, objective_target, objective_count, reward_tiers, consequence_*) alongside new enriched fields for backward compatibility"
  - "Reward amounts scaled by zone danger: city quests 50-120 scales, wilderness 60-120 scales"
  - "Every quest includes an echo reward for narrative flavor text from the quest giver"

patterns-established:
  - "Quest enrichment pattern: objectives list + rewards list + legacy fields coexist in area.quest() calls"
  - "Non-MVP objective type mapping: gather->collect, recover->collect, discover->investigate, craft->collect, escort->talk_to"

requirements-completed: [D-07, D-08, D-09, D-10, D-11, D-12, D-13, D-21, D-22]

# Metrics
duration: 7min
completed: 2026-04-03
---

# Phase 11 Plan 04: Enrich Quest Specs Summary

**20 enriched quest specs across 5 zones with dark-fantasy names, narrative descriptions, typed objectives, and multi-reward action lists**

## Performance

- **Duration:** 7 min
- **Started:** 2026-04-03T19:37:58Z
- **Completed:** 2026-04-03T19:45:24Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- All 20 quest stubs transformed into fully playable quest specs with creative names, descriptions, objectives, and rewards
- All 5 MVP objective types exercised: kill (4 quests), collect (6 quests), investigate (5 quests), deliver (4 quests), talk_to (1 quest)
- Quest chain connected: ashreach_wolf_overpopulation -> ashreach_bandit_problem via next_quest_id
- 7 distinct reward action types used: give_scales, modify_standing, give_skill_xp, learn_recipe, echo, modify_node_failure
- Legacy flat fields preserved on all 20 quests for backward compatibility

## Task Commits

Each task was committed atomically:

1. **Task 1: Enrich Vael's Crossing quest specs (8 quests)** - `6132754` (feat)
2. **Task 2: Enrich wilderness zone quest specs (12 quests across 4 zones)** - `29fa3c3` (feat)

## Files Modified
- `world/areas/vaels_crossing.py` - 8 enriched quests: Missing Shipment, Cellar Menace, Warden's Dispatch, Outstanding Debts, Goram's Commission, Shadow Market Recovery, Echoes of the Tower, Ystra's Remedy
- `world/areas/ashreach_plains.py` - 3 enriched quests: Wolf Cull, Ashway Brigands, Voices in the Dust (with wolf->bandit chain)
- `world/areas/reth_foothills.py` - 3 enriched quests: Lost in the Deep, Troll Country, Mountain Remedies
- `world/areas/cantera_edge.py` - 3 enriched quests: Warden Resupply, The Lost Traveler, Node Resonance Samples (with modify_node_failure reward)
- `world/areas/stormhaven_coast.py` - 3 enriched quests: Coastal Bounty, Whispers from the Deep, Quiet Cargo

## Decisions Made
- Preserved all legacy flat fields alongside new enriched fields for backward compatibility with existing code
- Scaled reward amounts by zone danger level: city quests 50-120 scales, wilderness 60-120 scales
- Every quest includes a narrative echo reward from the quest giver for immersion
- Non-MVP objective types mapped to closest MVP equivalents: gather->collect, recover->collect, discover->investigate, craft->collect, escort->talk_to

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Worktree had sparse checkout and object corruption issues; switched to committing directly in the main repo where all zone files were available

## Known Stubs

None - all 20 quest specs are fully enriched with real content. No placeholder data remains.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- All 20 quest specs now have objectives and rewards, making the quest engine fully functional for testing
- Plan 05 (validation/testing) can verify that all quest specs parse correctly and wire to the quest engine
- The quest chain (wolf->bandit) provides a testable multi-quest flow

## Self-Check: PASSED

- All 5 zone files exist and parse without syntax errors
- 20 objectives= found (8+3+3+3+3), 20 rewards= found (8+3+3+3+3)
- All 20 legacy objective_type= fields preserved
- Commits 6132754 and 29fa3c3 verified in git log
- SUMMARY.md created at expected path

---
*Phase: 11-quest-mvp*
*Completed: 2026-04-03*
