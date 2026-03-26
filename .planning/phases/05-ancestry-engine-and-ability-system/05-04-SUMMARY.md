---
phase: 05-ancestry-engine-and-ability-system
plan: 04
subsystem: commands
tags: [commands, ancestry, guild, domains, abilities, dispatcher]

requires:
  - phase: 05-01
    provides: ancestry_engine.py with set_ancestry() and ANCESTRY_TRAITS
  - phase: 05-02
    provides: ability_registry.py with ABILITIES dict and get_ability()
  - phase: 04-01
    provides: guild_engine.py with GUILDS, SUBCLASSES, check_guild_eligibility, join_guild
provides:
  - CmdSetAncestry command for permanent ancestry selection
  - CmdJoinGuild command for guild membership with secondary domain choice
  - CmdDomains command showing proficiency descriptors with hidden Remnance
  - CmdAbilities command showing known abilities and loadout
  - CmdUseAbility single dispatcher with ambiguous prefix disambiguation
  - Guild discovery hook in commit_session_xp (D-17)
affects: [ability-engine, combat-system, content-authoring]

tech-stack:
  added: []
  patterns:
    - "Single dispatcher CmdUseAbility for all 360+ abilities (no per-ability Cmd classes)"
    - "Ambiguous prefix match lists options instead of silently picking first"
    - "Guild discovery as fire-and-forget notification wrapped in try/except"

key-files:
  created:
    - commands/cmd_ancestry.py
    - commands/cmd_guild.py
    - commands/cmd_domains.py
    - commands/cmd_abilities.py
  modified:
    - world/world_state.py
    - commands/default_cmdsets.py

key-decisions:
  - "CmdJoinGuild requires full syntax (joinguild <guild> <secondary>) instead of yield-based interactive prompt -- simpler, no Evennia yield dependency"
  - "Guild discovery sends guild-flavored RP message rather than system notification -- fits dark-fantasy tone"
  - "CmdUseAbility resolves ability names by trying progressively longer word matches before falling back to prefix search"

patterns-established:
  - "Command pattern: lazy imports inside func() for engine modules (follows cmd_fly.py precedent)"
  - "Ambiguous match pattern: list all matches and return without executing when >1 prefix match found"

requirements-completed: [ANC-01, ANC-02, ANC-03, ANC-04, ABL-02, ABL-03]

duration: 4min
completed: 2026-03-26
---

# Phase 5 Plan 4: Player Commands and Guild Discovery Summary

**5 player-facing commands (ancestry, guild, domains, abilities, use) with guild discovery hook wired into commit_session_xp**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-26T05:49:27Z
- **Completed:** 2026-03-26T05:53:50Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments
- CmdSetAncestry accepts 4 ancestries with Selvar coat variant, delegates to set_ancestry()
- CmdDomains displays domain proficiency descriptors, hides Remnance until discovered (D-25)
- CmdAbilities/CmdUseAbility: single dispatcher with ambiguous prefix match disambiguation (ABL-02)
- CmdJoinGuild presents eligible guilds with secondary domain selection
- Guild discovery fires safely in commit_session_xp after domain score reaches threshold (D-17)
- All 5 commands registered in CharacterCmdSet

## Task Commits

Each task was committed atomically:

1. **Task 1: Create command modules** - `c07c8bb` (feat)
2. **Task 2: Wire guild discovery hook and register commands** - `f7dbe1e` (feat)

## Files Created/Modified
- `commands/cmd_ancestry.py` - CmdSetAncestry: permanent ancestry selection from 4 choices
- `commands/cmd_guild.py` - CmdJoinGuild: guild eligibility check with secondary domain selection
- `commands/cmd_domains.py` - CmdDomains: domain scores as proficiency descriptors, hidden Remnance
- `commands/cmd_abilities.py` - CmdAbilities (display) and CmdUseAbility (single dispatcher)
- `world/world_state.py` - Added _check_guild_discovery() hook in commit_session_xp
- `commands/default_cmdsets.py` - Registered all 5 new commands in CharacterCmdSet

## Decisions Made
- CmdJoinGuild uses full syntax rather than interactive yield prompts -- simpler and avoids Evennia yield dependency
- Guild discovery sends RP-flavored message ("a messenger approaches...") instead of system notification
- CmdUseAbility name resolution: progressively longer word matches first, then prefix search with disambiguation

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None that prevent plan goals. CmdUseAbility delegates to `world.ability_engine.use_ability()` which is implemented in plan 05-03 (same wave). The attuned variant prompt in CmdUseAbility is informational text only per plan spec (D-23 stub -- full y/n prompt deferred).

## Issues Encountered
- Git worktree had corrupt sparse-checkout index entries from `.claude-plugin/` and `.codex/` directories with missing objects. Fixed by running `git read-tree HEAD` to reset the index before staging.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- All player-facing commands ready for integration testing
- ability_engine.use_ability() must exist (plan 05-03) for CmdUseAbility to function end-to-end
- Commands ready for Phase 6 combat system to wire in resource/cooldown mechanics

---
*Phase: 05-ancestry-engine-and-ability-system*
*Completed: 2026-03-26*
