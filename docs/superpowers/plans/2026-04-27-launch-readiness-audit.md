# Soravelon Launch Readiness Audit

Date: 2026-04-27
Repo: `C:\Dev\Evennia\soravelon`
Scope: current MUD runtime/content state after Tremen Hub 3 implementation.

## Verdict

Soravelon is much healthier than a prototype and has a serious amount of real test coverage, but I would not call it host/go-live ready yet.

The content corpus is in strong shape: all current area files parse through the Sora Builder sidecar with 0 errors and 0 warnings, all major hub contract suites pass, and the new Tremen pack is validated. The main launch blockers are now in live progression wiring and release verification reliability rather than basic content importability.

## Blockers

### 1. Guild discovery still lacks an obvious live domain-XP source

The intended design is correct: fresh characters should not receive an immediate guild invitation, and guilds should be worked toward. The current code still appears to be missing the live activity-to-domain-XP wiring that makes that happen naturally.

Evidence:

- `world.world_state.accumulate_domain_xp()` exists.
- `typeclasses/scripts.py` calls `commit_session_xp(character)`.
- `world.guild_engine.check_guild_eligibility()` is consulted by session guidance and guild commands.
- Current source search found `accumulate_domain_xp` call sites only in `world/world_state.py` and tests, not in live combat, quest, gathering, crafting, exploration, or command flows.

Impact:

Players can be told to practice toward guild discovery, but normal play may not actually advance them toward the Practiced threshold. This is a core progression promise and should be treated as the top launch blocker.

Recommended fix:

Wire domain XP awards into real activities with explicit design intent:

- combat ability use and combat outcomes
- quest completion by quest theme/domain
- gathering/crafting where domain-aligned
- exploration/investigation where authored

Add a golden-path integration test proving a fresh character can earn a guild invitation through ordinary play without a manual grant.

### 2. Chain quest acceptance can crash when the offer has no NPC

`commands/cmd_dialogue.py` explicitly allows chain offers from quest completion to have `npc=None`, then later uses `npc.db.npc_name` and passes `npc` into `_build_quest_oob_payload()`.

Evidence:

- `CmdAccept.func()` skips the room-location check when `npc is None`.
- The same function then computes `npc_display = npc.db.npc_name or npc.key`.
- Quest completion uses `ndb.pending_quest_offer` for chain auto-offers, and those can be detached from a live NPC.

Impact:

A player accepting an auto-offered chain quest can hit an AttributeError at exactly the moment the game is trying to make quest chains feel smooth.

Recommended fix:

Add a command-level regression test for accepting a chain offer with `npc=None`, then make `CmdAccept` use a safe fallback display name and OOB payload for detached chain offers.

### 3. The full release test command is not currently a reliable gate

`python scripts\run_tests.py` timed out after 10 minutes. The isolated `tests.test_area_builder` suite also timed out after 6 minutes.

Evidence:

- `python scripts\run_tests.py` timed out at 604 seconds.
- `python scripts\run_tests.py tests.test_area_builder` timed out at 364 seconds.
- `tests.test_area_validator` and `tests.test_zone_serializer` passed individually, isolating the non-completing behavior to the area-builder suite rather than all area tooling.

Impact:

Before hosting, the project needs a deterministic release gate. A suite that does not complete makes it harder to trust launch-readiness claims and harder to catch regressions quickly.

Recommended fix:

Isolate the slow/hanging `tests.test_area_builder` test case, split DB-heavy runtime build checks from fast unit checks, and add a documented release verification command that completes reliably.

## High Priority

### 4. Direct help coverage is still missing for core gathering commands

A current static command/help parity scan found 74 command-like keys and 126 help entries. After ignoring cmdset classes, the real direct-help gaps are:

- `butcher`
- `chop`
- `forage`
- `harvest`
- `mine`

Impact:

Gathering is a core Soravelon system and now appears throughout the hub content. Broad gathering help exists, but direct command help matters for player confidence and command discoverability.

Recommended fix:

Add direct help entries for those five commands and a parity test that excludes cmdset classes while requiring live player commands to have direct or alias help coverage.

### 5. Test logs still contain noisy unknown-template warnings

The combat/mob suite passes, but it prints unknown template warnings for `dire_wolf` and `bear`.

Impact:

The warnings do not currently fail tests, but noisy expected warnings make real missing-template warnings easier to miss during launch validation.

Recommended fix:

Either author explicit fixture templates for test-only names or adjust those tests to assert/log the expected warning in a controlled way.

### 6. SQLite test warning should be consciously accepted or removed

Several DB-backed chunks print:

`world.FactionStanding: SQLite does not support unique constraints with nulls distinct.`

Impact:

This may be acceptable if production uses a database that supports the intended constraint, but it should not remain as unexplained release noise.

Recommended fix:

Document the expected production database behavior, silence only if intentional, or adjust the test model constraint for SQLite compatibility.

## Strengths

- All 21 current `world/areas/*.py` files parse and validate through the Sora Builder sidecar with 0 errors and 0 warnings.
- Current area room counts are healthy: Vael's Crossing 108, Varath Prime 154, Korahei 100, Tremen 112, and all current exterior zones at 100+ rooms.
- Hub/area contract suites passed 108 tests across Hub 1, Hub 4, Hub 5, and Tremen Hub 3.
- Combat, ability, status, mob, and encounter behavior passed 348 tests.
- Command/help/social/guild surfaces passed 97 tests.
- Economy, inventory, equipment, crafting, gathering, fishing, vendors, loot, and banking passed 234 tests.
- World/lifecycle/guild/quest/flight/patrol/recovery/room-state/system coverage passed 500 tests.
- `python scripts\smoke_start.py` passed after the Tremen implementation.
- New-player onboarding copy now includes `help getting started`, inventory/gear/equip guidance, and `tell` correctly covers both NPCs and players.

## Validation Evidence

Passed:

- `python scripts\run_tests.py tests.test_ability_engine tests.test_combat_ai tests.test_combat_engine tests.test_combat_fixes tests.test_combat_script tests.test_status_effects tests.test_mob_affixes tests.test_mob_disposition tests.test_mob_spawner tests.test_mob_templates` - 348 tests OK.
- `python scripts\run_tests.py tests.test_cmd_dialogue tests.test_cmd_guild tests.test_cmd_quest tests.test_cmd_vendor tests.test_command_preprocessor tests.test_help_command tests.test_help_entries tests.test_social tests.test_group_engine` - 97 tests OK.
- `python scripts\run_tests.py tests.test_inventory_engine tests.test_equipment_slots tests.test_crafting tests.test_gathering tests.test_fishing tests.test_item_spawner tests.test_loot_tables tests.test_vendor_engine tests.test_banking` - 234 tests OK.
- `python scripts\run_tests.py tests.test_content_authoring tests.test_content_integration` - 48 tests OK.
- `python scripts\run_tests.py tests.test_area_gathering_contracts` - 4 tests OK.
- `python scripts\run_tests.py tests.test_area_validator` - 40 tests OK.
- `python scripts\run_tests.py tests.test_zone_serializer` - 20 tests OK.
- `python scripts\run_tests.py tests.test_ancestry_engine tests.test_base_attributes tests.test_equipment_slots tests.test_flight_engine tests.test_flight_registry tests.test_guild_engine tests.test_guild_engine_mutations tests.test_node_system tests.test_oob_publisher tests.test_patrol_engine tests.test_quest_engine tests.test_recovery_engine tests.test_room_state tests.test_session_lifecycle tests.test_skill_engine tests.test_spawn_record tests.test_trigger_engine tests.test_typeclasses tests.test_wander_system tests.test_world_state tests.test_zone_scaling` - 500 tests OK.
- `python scripts\run_tests.py tests.test_hub1_contracts tests.test_crownroad_north_contract tests.test_crownroad_north_layout tests.test_old_causeway_contract tests.test_old_causeway_layout tests.test_ironvein_escarpment_contract tests.test_ironvein_escarpment_layout tests.test_stagcrown_preserve_contract tests.test_stagcrown_preserve_layout tests.test_varath_prime_layout tests.test_varath_prime_quests_and_vendors tests.test_korahei_hub5_contracts tests.test_tremen_hub3_contracts` - 108 tests OK.
- `python scripts\smoke_start.py` - passed.
- Sora Builder sidecar parse/validate all `world/areas/*.py` files - 21 files checked, 0 errors, 0 warnings.

Did not complete:

- `python scripts\run_tests.py` - timed out after 604 seconds.
- `python scripts\run_tests.py tests.test_area_builder` - timed out after 364 seconds.

## Recommended Next Work

1. Wire live domain XP into ordinary play and prove guild invitations happen through play.
2. Fix `CmdAccept` for detached chain quest offers and add command-level regression coverage.
3. Repair or split `tests.test_area_builder` so the full release gate completes reliably.
4. Add direct help entries for the five gathering commands and protect command/help parity.
5. Clean up expected warning noise in test output.
6. Add a DB-backed runtime build pass for representative large areas once `tests.test_area_builder` is reliable.

