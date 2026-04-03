---
phase: 12-launch-polish-help
plan: 02
subsystem: help-system
tags: [help, commands, abilities, guilds, ancestries, lore]
dependency_graph:
  requires: [ability_registry, guild_engine, ancestry_engine]
  provides: [dynamic_ability_help, comprehensive_help_entries]
  affects: [default_cmdsets, help_entries]
tech_stack:
  added: []
  patterns: [lazy-import-in-func, evennia-cmdhelp-override]
key_files:
  created:
    - commands/cmd_help.py
  modified:
    - commands/default_cmdsets.py
    - world/help_entries.py
decisions:
  - "CmdHelp overrides Evennia default via same key='help' in CharacterCmdSet"
  - "ABILITIES import is lazy (inside func()) to avoid import-time Evennia init issues"
  - "92 entries across 8 categories covers all registered commands, systems, ancestries, guilds, skills, and world lore"
metrics:
  duration_seconds: 493
  completed: "2026-04-03T22:29:12Z"
  tasks_completed: 2
  tasks_total: 2
  files_created: 1
  files_modified: 2
---

# Phase 12 Plan 02: Comprehensive Help System Summary

92 help entries across 8 categories + CmdHelp override for dynamic ability lookup from ABILITIES registry.

## What Was Built

### Task 1: Custom CmdHelp with Dynamic Ability Lookup (11429f9)

Created `commands/cmd_help.py` with `CmdHelp` extending Evennia's default help command. When a player types `help <ability_name>`, the command checks the ABILITIES registry for a match by ability_id or display name. If found, it renders formatted ability info (tier, domain, effect type, resource cost, cooldown, scaling). If no ability match, falls through to standard Evennia help.

Registered CmdHelp in CharacterCmdSet, overriding the default. Also synced default_cmdsets.py with the main repo's full command registration list.

### Task 2: 92 Hand-Written Help Entries (a2643fa)

Expanded `world/help_entries.py` from 1 entry to 92 entries across 8 categories:

| Category | Count | Coverage |
|----------|-------|----------|
| New Player | 5 | Getting started, character creation, combat basics, exploration, currency |
| Systems | 15 | Combat, guilds, domains, abilities, ancestry, crafting, banking, equipment, skills, quests, factions, encumbrance, death, attunement, scaling |
| Commands | 40 | All custom commands with usage, description, examples |
| Ancestries | 4 | Human, Kau'roran, Veth, Selvar with lore and mechanical traits |
| Guilds | 10 | All 10 guilds with motto, domain, resource, subclass list |
| Skills | 8 | Investigation, lockpicking, cooking, smithing, alchemy, herbalism, mining, survival |
| World Lore | 6 | Dragon curse, nodes, courier, empire, consortium, wardens |
| General | 1 | Evennia (dev-locked) |

Writing style: second person, concise, in-world flavor, Evennia ANSI colors for emphasis.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Synced default_cmdsets.py with main repo**
- **Found during:** Task 1
- **Issue:** Worktree's default_cmdsets.py was behind main repo (missing skill_commands, dialogue, crafting, equipment, bank, group, loadout, map, search, quest registrations)
- **Fix:** Copied full command registration list from main repo, added CmdHelp at top
- **Files modified:** commands/default_cmdsets.py

**2. [Rule 3 - Blocking] Fixed corrupted git index in worktree**
- **Found during:** Task 2 commit
- **Issue:** Sparse checkout left invalid object references in the index, preventing commits
- **Fix:** Used `git read-tree HEAD` to rebuild index from last known good state, then added files with `--sparse` flag

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| 1 | 11429f9 | Custom CmdHelp with dynamic ability lookup |
| 2 | a2643fa | 92 hand-written help entries across 8 categories |

## Known Stubs

None -- all help entries contain substantive text. Ability descriptions in the registry itself still have `[STUB - Phase 5b]` prefixes, which will appear in dynamic help output, but those are owned by the ability_registry module (not this plan).

## Self-Check: PASSED
