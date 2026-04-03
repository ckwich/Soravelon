---
phase: 12-launch-polish-help
verified: 2026-04-03T22:43:59Z
status: gaps_found
score: 5/7 must-haves verified
gaps:
  - truth: "Dynamic ability help from ABILITIES registry (help <ability_name> works)"
    status: failed
    reason: "CmdHelp exists in commands/cmd_help.py but is NOT registered in commands/default_cmdsets.py -- players will get default Evennia help, not dynamic ability lookup"
    artifacts:
      - path: "commands/cmd_help.py"
        issue: "File exists and is substantive but orphaned -- not imported or added in CharacterCmdSet"
      - path: "commands/default_cmdsets.py"
        issue: "Missing CmdHelp import and registration"
    missing:
      - "Add 'from commands.cmd_help import CmdHelp' and 'self.add(CmdHelp())' to CharacterCmdSet in default_cmdsets.py"
  - truth: "default_cmdsets.py regression -- 13 command registrations lost from main branch"
    status: failed
    reason: "Worktree Plan 12-01 overwrote default_cmdsets.py with stale version, dropping skill_commands, dialogue, crafting, and many other commands that exist on main"
    artifacts:
      - path: "commands/default_cmdsets.py"
        issue: "Worktree has 12 command registrations vs main's 25 -- lost CmdSkills, CmdPractice, CmdTrain, CmdTalk, CmdAsk, CmdSay, CmdTell, CmdAccept, CmdDecline, CmdCook, CmdSmith, CmdBrew, CmdCraft, CmdRecipes plus several more from phases 8-11"
    missing:
      - "Restore all command registrations from main branch AND add CmdHelp, CmdLore, and any other Phase 12 commands"
---

# Phase 12: Launch Polish & Help Verification Report

**Phase Goal:** New player experience smooth from connection to first combat; comprehensive help; lore journal; connection screen
**Verified:** 2026-04-03T22:43:59Z
**Status:** gaps_found
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Dark fantasy connection screen replaces Evennia default | VERIFIED | `server/conf/connection_screens.py` contains atmospheric text with Soravelon branding, ANSI colors, dragon lore excerpt, login instructions |
| 2 | Dynamic ability help from ABILITIES registry (help <ability_name> works) | FAILED | `commands/cmd_help.py` exists with correct logic but is NOT registered in `commands/default_cmdsets.py` -- orphaned |
| 3 | 90+ hand-written help entries covering systems, commands, ancestries, guilds, skills, recipes, factions | VERIFIED | 92 entries across 8 categories (New Player: 5, Systems: 15, Commands: 43, Ancestries: 4, Guilds: 10, Skills: 8, World Lore: 6, General: 1). Auto-loaded via Evennia's FILE_HELP_ENTRY_MODULES default |
| 4 | Lore journal command organized by zone with fragment counts | VERIFIED | `commands/cmd_lore.py` has zone overview with collected/total counts, partial name matching, fragment text display. Registered in worktree's default_cmdsets.py |
| 5 | Lore collection via search command with collected_lore tracking | VERIFIED | `commands/cmd_search.py` uses corrected `fragment_id` key (was `id`), populates `char.db.collected_lore_ids` on success |
| 6 | New player guided prompts (ancestry, guild, quest breadcrumbs) | VERIFIED | `_send_new_player_guidance()` in `typeclasses/characters.py` called at end of `at_post_puppet()`, 3-tier checks for ancestry/guild/quests with experience heuristic to suppress for returning players |
| 7 | Ancestry-based starter kit (different gear per ancestry) | VERIFIED | `STARTER_KITS` in `world/ancestry_engine.py` defines 4 ancestry-specific loadouts (Human: sword+leather, Kauroran: spear+hide, Veth: 2x dagger+leather+lockpick, Selvar: staff+robes), all get 2 healing potions + 50 Scales currency. `_grant_starter_kit()` wired into `set_ancestry()` via `create_item_from_template` |

**Score:** 5/7 truths verified (1 failed due to orphaned artifact, 1 regression)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `server/conf/connection_screens.py` | Dark fantasy connection screen | VERIFIED | 43 lines, CONNECTION_SCREEN variable with ANSI-colored atmospheric text |
| `commands/cmd_help.py` | Custom CmdHelp with dynamic ability lookup | ORPHANED | 85 lines, substantive implementation with ABILITIES registry lookup, name matching, formatted display -- but NOT registered in CharacterCmdSet |
| `world/help_entries.py` | 90+ help entries | VERIFIED | 1491 lines, 92 entries, all substantive (no short/stub entries found) |
| `commands/cmd_lore.py` | Lore journal command | VERIFIED | 128 lines, zone overview + zone detail views, partial name matching, empty state messages |
| `world/lore_registry.py` | Static lore fragment registry | VERIFIED | 446 lines, 32 fragments across 5 zones (Cantera Edge: 13, Stormhaven Coast: 5, Reth Foothills: 5, Ashreach Plains: 5, Vael's Crossing: 4) |
| `commands/cmd_search.py` | Search with fragment_id bug fix | VERIFIED | Uses `frag.get("fragment_id")` (corrected from `frag.get("id")`) |
| `world/ancestry_engine.py` | Starter kits in set_ancestry() | VERIFIED | STARTER_KITS dict, _grant_starter_kit() with per-item error handling, 50 Scales currency grant |
| `typeclasses/characters.py` | Guidance prompts in at_post_puppet() | VERIFIED | _send_new_player_guidance() with 3-tier checks, experience-based suppression |
| `commands/default_cmdsets.py` | All commands registered | REGRESSED | Only 12 registrations vs main's 25 -- lost skill_commands, dialogue, crafting, and more. CmdHelp missing entirely. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `commands/cmd_help.py` | `world/ability_registry.py` | Lazy import of ABILITIES | VERIFIED (internal) | Lazy import avoids init-time issues |
| `commands/default_cmdsets.py` | `commands/cmd_help.py` | CmdHelp import and add() | NOT_WIRED | No import or registration of CmdHelp exists in default_cmdsets.py |
| `commands/default_cmdsets.py` | `commands/cmd_lore.py` | CmdLore import and add() | WIRED | Lines 56-57 of worktree's default_cmdsets.py |
| `world/ancestry_engine.py` | `world/item_spawner.py` | create_item_from_template() | WIRED | Line 294: `create_item_from_template(item_def, location=character)` |
| `typeclasses/characters.py` | `_send_new_player_guidance` | Called in at_post_puppet | WIRED | Line 154: `self._send_new_player_guidance()` |
| `commands/cmd_lore.py` | `world/lore_registry.py` | get_all_zones, get_zone_fragments | WIRED | Line 30: lazy import of both functions |
| `commands/cmd_search.py` | `char.db.collected_lore_ids` | fragment_id tracking | WIRED | Lines 104-108: reads/appends collected_lore_ids |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `commands/cmd_help.py` | ABILITIES dict | `world/ability_registry.py` | Yes (registry populated in phase 5) | FLOWING (but orphaned -- never reached) |
| `commands/cmd_lore.py` | LORE_FRAGMENTS | `world/lore_registry.py` | Yes (32 static fragments) | FLOWING |
| `commands/cmd_lore.py` | collected_lore_ids | `char.db.collected_lore_ids` | Yes (populated by cmd_search) | FLOWING |
| `typeclasses/characters.py` | ancestry/guild/quest state | `char.db.*` | Yes (set by game systems) | FLOWING |

### Behavioral Spot-Checks

Step 7b: SKIPPED (no runnable entry points -- Evennia server not running)

### Requirements Coverage

No requirements from `.planning/REQUIREMENTS.md` are mapped to Phase 12. The D-01, D-02, D-05, D-09, D-10, D-11 referenced in plan frontmatter are internal design IDs used within this phase's context, not tracked in the top-level requirements file.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `commands/default_cmdsets.py` | - | Regression: 13 commands removed from main branch | BLOCKER | Players lose access to skill, dialogue, crafting commands when this branch merges |

No TODO/FIXME/PLACEHOLDER/STUB patterns found in any phase 12 files.

### Human Verification Required

### 1. Connection Screen Visual

**Test:** Connect to the game and observe the connection screen before login
**Expected:** Atmospheric dark fantasy text with "S O R A V E L O N" branding, dragon lore excerpt, ANSI colors rendering correctly
**Why human:** Visual presentation and ANSI color rendering cannot be verified programmatically

### 2. Starter Kit Functional Test

**Test:** Create a new character, choose each ancestry, check inventory
**Expected:** Each ancestry receives different gear (Human: Iron Sword + Leather Armor, Kauroran: Iron Spear + Hide Armor, Veth: 2x Iron Dagger + Leather + Lockpick, Selvar: Iron Staff + Cloth Robes), all get 2 Healing Potions and 50 Scales
**Why human:** Item creation through item_spawner requires running server with full DB context

### 3. Guidance Prompt Flow

**Test:** Log in as a brand-new character (no ancestry), observe prompts. Choose ancestry, relog, observe different prompt. Join guild, relog, observe quest hint.
**Expected:** Three-stage guidance: ancestry prompt -> guild exploration hint -> NPC conversation hint
**Why human:** Requires sequential game state changes across multiple logins

### Gaps Summary

Two gaps prevent full goal achievement:

1. **CmdHelp not registered (BLOCKER):** The dynamic ability help command exists as a complete, substantive implementation in `commands/cmd_help.py` but is never imported or registered in `commands/default_cmdsets.py`. The commit `11429f9` originally registered it, but the subsequent Plan 12-01 execution overwrote `default_cmdsets.py` with a stale version (the worktree had a corrupted git index and used `git read-tree HEAD` to recover, losing the 12-02 changes to this file).

2. **default_cmdsets.py regression (BLOCKER):** The worktree's `default_cmdsets.py` has only 12 command registrations versus main's 25. It lost CmdSkills, CmdPractice, CmdTrain, CmdTalk, CmdAsk, CmdSay, CmdTell, CmdAccept, CmdDecline, CmdCook, CmdSmith, CmdBrew, CmdCraft, CmdRecipes, and likely others from phases 8-11. This occurred because the Plan 12-01 worktree agent rebuilt the git index from HEAD (which was behind main) and wrote a minimal version. **When merging to main, this regression must be resolved** -- the fix should start from main's version and ADD the new Phase 12 commands (CmdHelp, CmdLore) rather than using the worktree's reduced version.

**Root cause for both gaps:** Git worktree index corruption during Plan 12-01 execution caused `default_cmdsets.py` to regress. Plans 12-02 and 12-03 ran first (and correctly registered commands), but Plan 12-01 ran last and overwrote the file.

---

_Verified: 2026-04-03T22:43:59Z_
_Verifier: Claude (gsd-verifier)_
