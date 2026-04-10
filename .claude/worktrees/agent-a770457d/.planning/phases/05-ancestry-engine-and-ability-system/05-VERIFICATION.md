---
phase: 05-ancestry-engine-and-ability-system
verified: 2026-03-25T20:00:00Z
status: passed
score: 5/5 must-haves verified
re_verification: false
human_verification:
  - test: "Run full test suite to confirm all tests pass"
    expected: "0 failures across test_ancestry_engine.py, test_ability_engine.py, test_room_state.py and full suite"
    why_human: "Cannot run evennia test from verification context (requires Django/Evennia bootstrap)"
  - test: "In-game: type 'ancestry human' and verify standings applied"
    expected: "Ancestry set, Empire +10,000 standing applied, confirmation message shown"
    why_human: "Requires running game server and logged-in character"
  - test: "In-game: type 'use momentum strike' with an unlocked ability"
    expected: "Dispatches to damage handler, shows combat stub text, sets cooldown if applicable"
    why_human: "Requires running game server with CharacterAbility DB record"
---

# Phase 5: Ancestry Engine and Ability System Verification Report

**Phase Goal:** Phase 5a builds the ancestry engine, ability framework, room state system, and all structural infrastructure. Phase 5b (separate) authors all 330 ability definitions collaboratively.
**Verified:** 2026-03-25
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Each of the 4 ancestries applies its mechanical trait at character creation and traits feed into mob disposition | VERIFIED | `world/ancestry_engine.py` (158 lines): ANCESTRY_TRAITS for human/kauroran/veth/selvar, set_ancestry() calls _apply_starting_standings() with correct amounts. mob_disposition.py already reads character.db.ancestry (pre-existing ANCESTRY_FACTION_MODIFIERS). |
| 2 | The `use <ability>` dispatcher handles all abilities through a single CmdUseAbility command | VERIFIED | `commands/cmd_abilities.py:91` has `key = "use"`, delegates to `world/ability_engine.py:use_ability()` which dispatches via EFFECT_HANDLERS dict (10 handlers). No per-ability Cmd classes exist. |
| 3 | Ability tier gating unlocks correctly at GTS thresholds 0/20/50/85; locked ability returns clear message | VERIFIED | `world/ability_engine.py:_check_ability_access()` queries CharacterAbility model. ABILITY_TIERS in registry defines thresholds {1:0, 2:20, 3:50, 4:85}. Denial returns "You have not unlocked {name}." |
| 4 | Ability cooldowns tracked per-encounter on character.ndb reset correctly between encounters | VERIFIED | `world/ability_engine.py:use_ability()` sets cooldown in ndb.ability_cooldowns after use. `decrement_cooldowns()` decrements per round. `clear_encounter_cooldowns()` resets both ability_cooldowns and ancestry_ability_used. Character ndb initialized at puppet time. |
| 5 | Phase 5a structural infrastructure complete (room state, registry, model, commands, guild discovery wiring) | VERIFIED | world/room_state.py (409 lines, 21 flags, lazy decay), world/ability_registry.py (14 ABILITIES stubs covering all 10 effect types, 10 domains), CharacterAbility model + migration 0005, 5 commands registered in CharacterCmdSet, guild discovery wired in commit_session_xp. |

**Score:** 5/5 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `world/ancestry_engine.py` | ANCESTRY_TRAITS, set_ancestry(), get_ancestry_trait() | VERIFIED (158 lines) | 4 ancestries with traits, standings, set_ancestry returns (bool, str), lazy import of modify_standing |
| `world/room_state.py` | FLAG_VOCABULARY, get_room_flags(), add_room_flag(), get_dominant_flag(), SENSE_DISPLAY | VERIFIED (409 lines) | 21 flags in FLAG_VOCABULARY, lazy decay via time-based round calc, SENSE_PRIORITY ordering, SENSE_DISPLAY atmospheric text |
| `world/ability_registry.py` | ABILITIES dict, DOMAIN_ABILITIES, SUBCLASS_SIGNATURES, get_ability() | VERIFIED (355 lines) | 14 stub abilities covering all 10 domains and all 10 effect_types, derived lookups built at module level |
| `world/ability_engine.py` | use_ability(), effect handlers, cooldown/resource management | VERIFIED (257 lines) | 10 effect handlers, access check via CharacterAbility, cooldown tracking, resource management, room flag writing |
| `world/models.py (CharacterAbility)` | CharacterAbility Django model | VERIFIED | ForeignKey to ObjectDB, ability_id CharField, unique_together constraint, times_used counter |
| `world/migrations/0005_characterability.py` | Migration creating CharacterAbility | VERIFIED | Dependencies on 0004_characterguild, creates model with correct fields and indexes |
| `commands/cmd_ancestry.py` | CmdSetAncestry | VERIFIED (83 lines) | key="ancestry", delegates to set_ancestry(), handles 4 ancestries + selvar coat |
| `commands/cmd_guild.py` | CmdJoinGuild | VERIFIED (156 lines) | key="joinguild", checks eligibility, secondary domain selection |
| `commands/cmd_domains.py` | CmdDomains | VERIFIED (65 lines) | key="domains", hides remnance until discovered, shows proficiency labels |
| `commands/cmd_abilities.py` | CmdAbilities, CmdUseAbility | VERIFIED (218 lines) | key="use", prefix matching with ambiguity disambiguation, target resolution |
| `tests/test_ancestry_engine.py` | Ancestry tests | VERIFIED (208 lines) | 6 test classes: Human, Kauroran, Veth, Selvar, Rejection, GetAncestryTrait |
| `tests/test_ability_engine.py` | Ability tests | VERIFIED (335 lines) | 5 test classes: RegistryStructure, UseAbilityDispatch, Cooldowns, ResourceManagement, TierGating |
| `tests/test_room_state.py` | Room state tests | VERIFIED (253 lines) | 5 test classes: GetRoomFlags, AddRoomFlag, RemoveRoomFlag, GetDominantFlag, FlagVocabularyCompleteness |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| world/ancestry_engine.py | world/world_state.py | `from world.world_state import modify_standing` (lazy, line 148) | WIRED | Called with 4 args including "ancestry_starting" reason |
| typeclasses/mobs.py | world/room_state.py | `from world.room_state import add_room_flag` in at_death (line 179) | WIRED | blood_soaked, fading_life, power_vacuum written on mob death |
| world/action_vocabulary.py | world/room_state.py | `_action_add_room_flag` handler (line 233, registered line 268) | WIRED | Handler fires from trigger system via ACTION_HANDLERS |
| world/ability_engine.py | world/ability_registry.py | `from world.ability_registry import ABILITIES` (line 167, 205) | WIRED | Lookups in _check_ability_access and use_ability |
| world/ability_engine.py | world/guild_engine.py | `from world.guild_engine import GUILDS, FINGERPRINTS` (line 125) | WIRED | Used in initialize_domain_resource |
| world/ability_engine.py | world/room_state.py | `from world.room_state import add_room_flag` (line 244) | WIRED | Room flag written after ability execution if room_flag_written set |
| typeclasses/characters.py | world/room_state.py | `from world.room_state import get_dominant_flag, SENSE_DISPLAY` (line 158) | WIRED | Sense hook in at_after_move for resonance guild members |
| commands/cmd_ancestry.py | world/ancestry_engine.py | `from world.ancestry_engine import` (lines 34, 40) | WIRED | set_ancestry called in func() |
| commands/cmd_abilities.py | world/ability_engine.py | `from world.ability_engine import use_ability` (line 134) | WIRED | Dispatches in func() |
| world/world_state.py | world/guild_engine.py | `from world.guild_engine import check_guild_eligibility` (line 211-212) | WIRED | _check_guild_discovery fires in commit_session_xp |
| commands/default_cmdsets.py | all command modules | imports and self.add() (lines 44-52) | WIRED | All 5 new commands registered: CmdSetAncestry, CmdJoinGuild, CmdDomains, CmdAbilities, CmdUseAbility |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|--------------|--------|--------------------|--------|
| world/ability_engine.py | ABILITIES lookup | world/ability_registry.py constant dict | Yes -- 14 stub entries with complete field schema | FLOWING (stubs are intentional Phase 5a scope) |
| world/ancestry_engine.py | ANCESTRY_TRAITS | Module constant dict | Yes -- all 4 ancestries with full trait data | FLOWING |
| world/room_state.py | room.ndb.room_state | Written by add_room_flag, mob death, abilities | Yes -- lazy decay reads real timestamps | FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| ability_registry imports | `python -c "from world.ability_registry import ABILITIES..."` | 14 abilities, 10 domains, all 10 effect types covered | PASS |
| ancestry_engine structure | File contains ANCESTRY_TRAITS with 4 keys, set_ancestry with (bool, str) return | Verified via file read | PASS |
| Room state flag count | FLAG_VOCABULARY has 21 entries (20 flags + still logic) | 21 flags confirmed in file | PASS |
| CmdUseAbility ambiguity | "Which ability did you mean?" message at line 211 | Present with comma-separated names | PASS |

Note: Cannot run `evennia test` or server commands from verification context. Test execution deferred to human verification.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-----------|-------------|--------|----------|
| ANC-01 | 05-01, 05-04 | Human ancestry with Empire Standing bonus | SATISFIED | ANCESTRY_STARTING_STANDING["human"] = {"empire": 10000}, CmdSetAncestry handles "human" |
| ANC-02 | 05-01, 05-04 | Kau'roran ancestry with traits and ceremony | SATISFIED | ANCESTRY_TRAITS["kauroran"] with hp_bonus, trust_build_rate; 3 starting standings |
| ANC-03 | 05-01, 05-04 | Veth ancestry with tunnel shortcuts and networks | SATISFIED | ANCESTRY_TRAITS["veth"] with warren_sense, speed_bonus; consortium +7500 |
| ANC-04 | 05-01, 05-04 | Selvar ancestry with coat variation | SATISFIED | coat_traits with summer/winter, SELVAR_ALL_FACTIONS_PENALTY, coat required |
| ANC-05 | 05-01 | Ancestry modifiers feed into mob disposition | SATISFIED | set_ancestry sets character.db.ancestry; mob_disposition.py ANCESTRY_FACTION_MODIFIERS reads it (pre-existing) |
| ABL-01 | 05-02 | Global data-driven ability registry | SATISFIED | world/ability_registry.py: ABILITIES dict with 14 stubs, DOMAIN_ABILITIES, SUBCLASS_SIGNATURES |
| ABL-02 | 05-03, 05-04 | CmdUseAbility dispatcher handles all abilities through one command | SATISFIED | commands/cmd_abilities.py CmdUseAbility key="use", dispatches via use_ability() |
| ABL-03 | 05-03 | Ability tier gating at GTS 0/20/50/85 | SATISFIED | ABILITY_TIERS defines thresholds, _check_ability_access queries CharacterAbility |
| ABL-04 | 05-02 | All 90 subclasses have distinct ability sets | SATISFIED (stub) | Per ROADMAP note: "ABL-04 (full 330 ability content) deferred to Phase 5b. Phase 5a delivers stub abilities only." 14 stubs present with [STUB - Phase 5b] markers. |
| ABL-05 | 05-03 | Ability cooldowns tracked per-encounter on ndb | SATISFIED | ndb.ability_cooldowns initialized at puppet, set in use_ability, cleared by clear_encounter_cooldowns |
| ABL-06 | 05-02 | Subclass engine derives identity from domain pair | SATISFIED | SUBCLASS_SIGNATURES derived from ABILITIES entries with subclass_id set; guild_engine.py SUBCLASSES maps 90 subclasses with primary+secondary domains |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| world/ability_registry.py | 74+ | "[STUB - Phase 5b]" in 14 descriptions | Info | Expected -- Phase 5a explicitly delivers stubs only per ROADMAP note |
| world/ability_engine.py | 20-63 | Effect handlers return "[Combat stub]" text | Info | Expected -- Phase 6 wires real combat effects |
| world/ability_registry.py | 301+ | `subclass_id: "bladestorm"` not in guild_engine.SUBCLASSES | Info | The actual subclass for combat+naturalism is "thornguard"; stub uses placeholder name. Will be fixed when Phase 5b populates real ability entries. |

### Human Verification Required

### 1. Full Test Suite Execution

**Test:** Run `evennia test --settings settings tests/ -x`
**Expected:** All tests pass with 0 failures, including test_ancestry_engine.py, test_ability_engine.py, test_room_state.py
**Why human:** Evennia test runner requires full Django/Twisted bootstrap not available in verification context

### 2. Ancestry Selection In-Game

**Test:** Connect to game server, create character, type `ancestry human`
**Expected:** "Ancestry set to Human." message, Empire standing at +10,000
**Why human:** Requires running server with real character object

### 3. Ability Use In-Game

**Test:** With a guild member character who has unlocked abilities, type `use momentum strike`
**Expected:** Dispatches to damage handler, shows stub text, cooldown set if applicable
**Why human:** Requires running server with CharacterAbility DB records

### 4. Guild Discovery Notification

**Test:** Accumulate domain XP past ~30 threshold via commit_session_xp
**Expected:** Character receives guild recruitment message mentioning appropriate guild name
**Why human:** Requires XP accumulation and session commit flow

### Gaps Summary

No blocking gaps found. All structural infrastructure for Phase 5a is in place:

- **Ancestry engine:** Complete with all 4 ancestries, standings, and trait system
- **Room state system:** Complete with 21 flags, lazy decay, Sense integration
- **Ability registry:** 14 stub entries covering all 10 domains and all 10 effect types (Phase 5b scope for full 330)
- **Ability engine:** Complete dispatch pipeline with cooldown, resource, access checks
- **CharacterAbility model:** Migrated with correct schema
- **Commands:** All 5 new commands registered and wired
- **Guild discovery:** Wired into commit_session_xp with safety wrapper
- **Tests:** 3 test files with comprehensive coverage (6+5+5 = 16 test classes)

One minor note: the "bladestorm" subclass_id in stub signature abilities does not match any real subclass in guild_engine.SUBCLASSES (the actual combat+naturalism subclass is "thornguard"). This is informational only -- Phase 5b will replace all stubs with real ability definitions using correct subclass IDs.

---

_Verified: 2026-03-25T20:00:00Z_
_Verifier: Claude (gsd-verifier)_
