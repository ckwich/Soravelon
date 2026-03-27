---
phase: 06c-npc-dialogue-and-crafting
verified: 2026-03-26T21:00:00Z
status: gaps_found
score: 3/4 must-haves verified
gaps:
  - truth: "Ambient NPC echoes fire on timer with variance, creating lived-in atmosphere"
    status: failed
    reason: "Tag category mismatch: ambient_npc_tick() searches search_tag('npc', category='object_type') but area_builder tags NPCs with category='character_type' and category='mob_type'. The ticker finds zero NPCs and never fires."
    artifacts:
      - path: "world/dialogue_engine.py"
        issue: "Line 408: search_tag('npc', category='object_type') -- should be category='character_type' or category='mob_type'"
      - path: "world/area_builder.py"
        issue: "Lines 531-532: tags NPC as ('npc', 'character_type') and ('npc', 'mob_type') but NOT ('npc', 'object_type')"
    missing:
      - "Fix tag category in ambient_npc_tick() to match area_builder tagging (use 'character_type' or 'mob_type')"
---

# Phase 06c: NPC Dialogue and Crafting Verification Report

**Phase Goal:** NPC dialogue system with Standing-tier greetings, keyword topics, dynamic hints, ambient behavior; crafting framework with recipe registry, quality variance, and basic output for Cooking/Smithing/Alchemy
**Verified:** 2026-03-26T21:00:00Z
**Status:** gaps_found
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths (Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | An NPC gives different dialogue to a player with high vs. low standing, or to a Kau'roran vs. a Human ancestry -- the context packet drives the variation | VERIFIED | `get_standing_tier()` maps disposition float through 8 tiers including betrayal; `resolve_greeting()` selects tier-specific text; `resolve_topic_response()` uses RESPONSE_PRIORITY with `_check_condition()` evaluating standing, ancestry, class, dimensions; `_build_dialogue_context()` calls `get_character_context_packet()` from world_state; 531-line test suite covers all tier mappings |
| 2 | Dynamic hints show relevant topics based on Standing tier, active quests, and world-state dimensions | VERIFIED | `get_npc_hints()` collects from base_hints, tier_hints (filtered by standing tier), network_hints (threshold 40), scholar_hints, warden_hints; filters already-known via KnownTopicRecord with context_hash re-surfacing; caps at MAX_HINTS_DISPLAYED=4; CmdTalk displays hints after greeting |
| 3 | Crafting a recipe with ingredients produces an item; quality varies based on skill level -- higher skill = better results | VERIFIED | `craft_item()` validates recipe knowledge, station, ingredients, then calls `calculate_craft_quality(skill_value, difficulty)` with gap-based tier mapping + random variance; `_create_crafted_item()` creates SoravelonObject with quality metadata; test suite confirms high-skill produces masterwork, low-skill produces flawed; 9 recipes across 3 professions (cooking/smithing/alchemy) |
| 4 | Ambient NPC echoes fire on timer with variance, creating lived-in atmosphere | FAILED | `ambient_npc_tick()` at line 408 uses `search_tag("npc", category="object_type")` but area_builder tags NPCs as `("npc", category="character_type")`. Tag mismatch means the ticker finds zero NPCs. The logic is correct -- interval, variance, player-presence check, random echo selection -- but wiring is broken by this category mismatch. |

**Score:** 3/4 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `world/dialogue_definitions.py` | Standing tier thresholds, response priority, synonyms | VERIFIED | 69 lines; exports STANDING_TIER_THRESHOLDS (7 thresholds for 8 tiers), RESPONSE_PRIORITY (16 conditions), TOPIC_SYNONYMS (9 entries), MAX_HINTS_DISPLAYED, threshold constants |
| `world/dialogue_engine.py` | Core dialogue logic: greetings, topics, hints, keyword extraction, ambient | VERIFIED (wiring bug) | 471 lines; all 8 public functions implemented. `ambient_npc_tick` has tag category mismatch. |
| `world/crafting_definitions.py` | Recipe registry, quality tiers, station requirements | VERIFIED | 222 lines; RECIPE_REGISTRY with 9 recipes (3 cooking, 2 smithing, 3 alchemy), QUALITY_TIERS (5), QUALITY_MULTIPLIERS, STATION_REQUIREMENTS (4), SKILL_TO_COMMAND mapping |
| `world/crafting_engine.py` | Crafting logic: quality calc, validation, execution, discovery | VERIFIED | 346 lines; `craft_item()`, `calculate_craft_quality()`, `check_station()`, `learn_recipe()`, `get_known_recipes()`, `_check_ingredients()`, `_create_crafted_item()` all substantive |
| `commands/cmd_dialogue.py` | CmdTalk, CmdAsk, CmdSay, CmdTell, CmdAccept, CmdDecline | VERIFIED | 450 lines; all 6 commands implemented with NPC lookup, engine dispatch, error handling |
| `commands/cmd_crafting.py` | CmdCraft, CmdCook, CmdSmith, CmdBrew, CmdRecipes | VERIFIED | 234 lines; _BaseCraftCmd with delay, cancellation on move; CmdRecipes with skill filter and grouped display |
| `commands/default_cmdsets.py` | All commands registered | VERIFIED | Both cmd_dialogue (6 commands) and cmd_crafting (5 commands) imported and added to CharacterCmdSet |
| `typeclasses/characters.py` | pending_quest_offer init and clearing | VERIFIED | ndb.pending_quest_offer initialized to None; cleared in at_after_move; reactive echo fires on room enter |
| `world/models.py` | KnownTopicRecord, CharacterRecipe models | VERIFIED | Both models defined with proper ForeignKeys to ObjectDB, unique_together constraints |
| `world/migrations/0006_knowntopicrecord_characterrecipe.py` | Migration for new models | VERIFIED | Migration exists (numbered 0006 not 0005 as planned; 0005 was used by a different migration) |
| `world/area_builder.py` | npc() method with dialogue/ambient kwargs | VERIFIED | npc() creates SoravelonMob with is_npc=True, sets all 12 dialogue/ambient db attributes from kwargs |
| `server/conf/at_server_startstop.py` | Ambient ticker registered | VERIFIED | TICKER_HANDLER.add(interval=15, callback="world.dialogue_engine.ambient_npc_tick") registered at server start |
| `world/action_vocabulary.py` | open_dialogue handler | VERIFIED | _handle_open_dialogue finds NPC by tag/key, dispatches greeting or topic response |
| `tests/test_dialogue.py` | Dialogue tests (min 150 lines) | VERIFIED | 531 lines; covers tier mapping (all 8), topic priority, keyword extraction (4 stages), context packet, hints, topic learning |
| `tests/test_crafting.py` | Crafting tests (min 100 lines) | VERIFIED | 346 lines; covers quality gradient, station check, recipe discovery, quality modifiers |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| dialogue_engine.py | world_state.py | get_character_context_packet | WIRED | Lazy import in _build_dialogue_context(), function exists at line 320 of world_state.py |
| dialogue_engine.py | mob_disposition.py | get_mob_disposition | WIRED | Lazy import in get_standing_tier() |
| dialogue_engine.py | dialogue_definitions.py | RESPONSE_PRIORITY, TOPIC_SYNONYMS, STANDING_TIER_THRESHOLDS | WIRED | Top-level import at line 27 |
| crafting_engine.py | skill_engine.py | get_skill_value | WIRED | Lazy import in craft_item(), function exists at line 65 of skill_engine.py |
| crafting_engine.py | models.py | CharacterRecipe | WIRED | Lazy imports in get_known_recipes, learn_recipe, _ensure_default_recipes |
| cmd_dialogue.py | dialogue_engine.py | resolve_greeting, resolve_topic_response, get_npc_hints, extract_topic | WIRED | Lazy imports in each command's func() |
| cmd_crafting.py | crafting_engine.py | craft_item, get_known_recipes | WIRED | Lazy imports in _BaseCraftCmd.func() and CmdRecipes.func() |
| default_cmdsets.py | cmd_dialogue.py, cmd_crafting.py | import and add to CharacterCmdSet | WIRED | Both imported and all 11 commands added |
| at_server_startstop.py | dialogue_engine.py | TICKER_HANDLER -> ambient_npc_tick | WIRED (callback string) | Callback registered as string path; function exists; BUT tag mismatch prevents finding NPCs |
| area_builder.py | typeclasses/mobs.py | Creates SoravelonMob with is_npc=True | WIRED | create_object with SoravelonMob typeclass, db.is_npc=True |
| characters.py | dialogue_engine.py | fire_npc_reactive_echo on room enter | WIRED | Lazy import at line 216; called in at_after_move |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| dialogue_engine.py | npc.db.dialogue_greeting_tiers | area_builder.npc() kwargs | Yes, set from dialogue dict | FLOWING |
| dialogue_engine.py | disposition float | mob_disposition.get_mob_disposition() | Yes, computed from DB | FLOWING |
| crafting_engine.py | skill_value | skill_engine.get_skill_value() | Yes, reads from DB | FLOWING |
| dialogue_engine.py (ambient) | npc_objects | search_tag("npc", "object_type") | No, wrong tag category | DISCONNECTED |

### Behavioral Spot-Checks

Step 7b: SKIPPED (no runnable entry points -- Evennia server not running, tests require Django setup)

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| NPC-01 | 06c-01, 06c-03 | NPC template system injects world-state variables into dialogue | SATISFIED | get_character_context_packet() builds context; _build_dialogue_context() augments with standing tier; all condition checks reference context dict |
| NPC-02 | 06c-01, 06c-03, 06c-04 | NPCs respond differently based on character standing, ancestry, reputation | SATISFIED | Standing tier from disposition; RESPONSE_PRIORITY evaluates tier conditions; greeting_tiers selects per-tier text; tests confirm all 8 tiers |
| NPC-03 | 06c-01, 06c-04, 06c-05 | Context packet feeds NPC templates (same interface as future LLM consumer) | SATISFIED | _build_dialogue_context() returns dict with standing_tier, ancestry, domains, guild, dimensions, quest stubs -- documented as NPC-03 LLM interface |
| SKL-03 | 06c-02 | Crafting skill track with quality variance | SATISFIED | 3 craft skills (cooking/smithing/alchemy) with recipes; quality calc uses skill_value from skill_engine; 5 quality tiers with multipliers |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| world/dialogue_engine.py | 408 | `search_tag("npc", category="object_type")` -- wrong tag category | BLOCKER | Ambient ticker finds 0 NPCs; success criterion 4 fails |
| world/dialogue_engine.py | 117-119 | Quest state stubs (active/completed/failed = []) | Info | Expected -- quest system not yet built; interface ready |
| world/dialogue_engine.py | 378-385 | has_available_quest/get_quest_offer stubs | Info | Expected -- quest system not yet built |
| world/area_builder.py | N/A | npc_name and npc_id not set as db attributes | Warning | Commands fall back to npc.key which works, but KnownTopicRecord uses npc.key as fallback for npc_id which could cause collisions across zones |

### Human Verification Required

### 1. Dialogue Variation by Ancestry/Standing

**Test:** Create two characters with different ancestries and standings, talk to the same NPC
**Expected:** Different greeting text and different available hints based on standing tier and context conditions
**Why human:** Requires running Evennia server with zone loaded, multiple character sessions

### 2. Crafting with Delay and Movement Cancel

**Test:** Start crafting a recipe, then move to another room before craft_time completes
**Expected:** Crafting is cancelled with "You moved and lost your crafting progress"
**Why human:** Requires Evennia delay system running in Twisted reactor

### 3. Ambient Echo Timing and Variance

**Test:** Stand in a room with an NPC that has idle echoes configured, wait for echoes
**Expected:** Echoes appear at interval +/- variance, only when players present
**Why human:** Requires running ticker, real-time observation (also blocked by tag bug)

### Gaps Summary

One gap blocks full goal achievement:

**Ambient NPC ticker tag mismatch** -- The `ambient_npc_tick()` function in `world/dialogue_engine.py` line 408 searches for NPCs using `search_tag("npc", category="object_type")`, but `world/area_builder.py` tags NPC objects with `("npc", category="character_type")` and `("npc", category="mob_type")`. The category never matches, so the ticker finds zero NPCs and never fires any ambient echoes. This is a one-line fix: change `category="object_type"` to `category="character_type"` (or `"mob_type"`).

All other systems -- dialogue greetings, topic resolution, dynamic hints, keyword extraction, crafting quality, recipe registry, commands, tests -- are fully implemented and properly wired.

---

_Verified: 2026-03-26T21:00:00Z_
_Verifier: Claude (gsd-verifier)_
