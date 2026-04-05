---
phase: 15-implement-missing-gameplay-gap-systems
plan: 04
subsystem: social
tags: [commands, channels, inspection, appraisal, communication]

requires:
  - phase: 06a-base-attributes-and-combat
    provides: stamina system for shout cost
provides:
  - CmdWho, CmdShout, CmdWhisper social commands
  - OOCChannel, DomainChannel typeclasses
  - CmdInspect, CmdCompare item inspection commands
  - Minimal skill_engine with get_skill_value and record_skill_use
affects: [skill-engine, crafting-system, item-typeclasses]

tech-stack:
  added: []
  patterns: [django-setup-in-tests, mock-spec-for-django-models, lazy-import-for-oob]

key-files:
  created:
    - commands/cmd_social.py
    - commands/cmd_inspect.py
    - world/skill_engine.py
    - tests/test_social.py
  modified:
    - typeclasses/channels.py
    - server/conf/settings.py
    - commands/default_cmdsets.py

key-decisions:
  - "Used at_pre_msg (not at_pre_channel_msg) for Evennia 6.0 DomainChannel hook"
  - "Created minimal skill_engine.py stub with get_skill_value/record_skill_use for appraisal"
  - "CLAUDE.md: replaced getattr(item.db, ...) with item.db.attr or fallback pattern"

patterns-established:
  - "Social command pattern: zone-wide via search_tag(zone_id), room-scope via location.contents"
  - "Channel domain gating: at_pre_msg checks primary domain from max(domain_scores)"

requirements-completed: [D-13, D-14, D-15, D-16, D-17, D-18, D-19]

duration: 10min
completed: 2026-04-05
---

# Phase 15 Plan 04: Social Commands and Item Inspection Summary

**Who/shout/whisper commands with zone-wide and room-scope communication, OOC/domain channels, and appraisal-gated item inspection with side-by-side comparison**

## Performance

- **Duration:** 10 min
- **Started:** 2026-04-05T06:46:19Z
- **Completed:** 2026-04-05T06:56:42Z
- **Tasks:** 2/2
- **Files modified:** 7

## Accomplishments

### Task 1: Social commands + channels
- CmdWho lists online players with name, ancestry, guild/domain, and zone
- CmdShout sends zone-wide in-character message, costs 10 stamina (via ndb.stamina deduction + push_stat_update)
- CmdWhisper delivers private in-room message; bystanders see notification without content
- OOCChannel with [OOC] prefix for server-wide out-of-character chat
- DomainChannel with at_pre_msg hook checking sender's primary domain matches channel
- OOC channel added to DEFAULT_CHANNELS in settings.py alongside Public and MudInfo

### Task 2: Item inspection + compare commands
- CmdInspect shows item mechanical stats gated by appraisal skill DC
- Appraisal DC formula: RARITY_DC[rarity] + (material_tier * 5) where normal=0, magic=15, rare=30, legendary=45
- CmdCompare shows side-by-side stat comparison for two items (both must pass appraisal check)
- record_skill_use called on successful inspection for passive skill advancement
- All 5 new commands registered in CharacterCmdSet

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed channel hook name for Evennia 6.0**
- **Found during:** Task 1
- **Issue:** Plan specified `at_pre_channel_msg` but Evennia 6.0 uses `at_pre_msg`
- **Fix:** Renamed all occurrences to `at_pre_msg`
- **Files modified:** typeclasses/channels.py, tests/test_social.py

**2. [Rule 3 - Blocking] Created skill_engine.py stub**
- **Found during:** Task 2
- **Issue:** cmd_inspect.py requires get_skill_value and record_skill_use from world/skill_engine.py which did not exist
- **Fix:** Created minimal skill_engine.py with get_skill_value (reads db.skills dict) and record_skill_use (increments db.skill_uses counter)
- **Files modified:** world/skill_engine.py

**3. [Rule 1 - Bug] Fixed getattr pattern per CLAUDE.md**
- **Found during:** Task 2
- **Issue:** Plan code used getattr(item.db, 'attr', default) which violates CLAUDE.md convention
- **Fix:** Changed to item.db.attr or fallback pattern throughout cmd_inspect.py
- **Files modified:** commands/cmd_inspect.py

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| 1+2 | 2b8604e | feat(15-04): implement social commands, channels, and item inspection |

## Known Stubs

- **world/skill_engine.py** (entire file): Minimal stub providing get_skill_value and record_skill_use. Full skill progression system (XP curves, practice, trainers, discovery) deferred to dedicated skill system plan. The stub is functional for appraisal checks.

## Self-Check: PASSED
