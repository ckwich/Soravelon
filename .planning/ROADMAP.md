# Roadmap: Soravelon

## Overview

Soravelon has 12 foundation systems built and passing tests. This roadmap covers the remaining Milestone 0 work (patrol, commands, flight paths, desktop client, GUI builder) then delivers Milestone 1 (domain/guild engine, 90-subclass ability system, ancestries, combat, skills, NPC templates, and the first playable zone content). Phases follow the strict dependency chain: server-side completions first, then client tooling, then design-gated ability work, then combat and content integration. The GUI builder must ship before any zone content is authored.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Patrol, Commands, and Flight Paths** - Complete Milestone 0 server-side systems: patrol mobs, command prefix/alias, Dragon Courier flight paths
- [ ] **Phase 2: OOB Push and Desktop Client** - OOB publisher infrastructure and Tauri desktop client with terminal, status, and map panels
- [ ] **Phase 3: GUI Area Builder** - Tauri visual zone editor writing AreaBuilder .py files; two-pass loading fix prerequisite
- [ ] **Phase 4: Domain Fingerprints and Guild Engine** - 10 domain mechanical fingerprints + guild/GTS computation engine (design gate for all ability work)
- [ ] **Phase 5: Ancestry Engine and Ability System** - 4 playable ancestries and all 90 subclasses with 360+ ability definitions
- [ ] **Phase 6: Combat, Skills, and NPC Templates** - Ability-driven combat engine, proficiency skill tracks, and world-state NPC dialogue system
- [ ] **Phase 7: Milestone 1 Content** - Hub City 1, 4 starter zones (3 Layer 0 + 1 Layer 1), and basic equipment authored via GUI builder
- [x] **Phase 13: Gathering and Refining** - Resource gathering nodes, material processing pipeline, fishing system, tool requirements, and scalable 5-tier material registry (completed 2026-04-04)

## Phase Details

### Phase 1: Patrol, Commands, and Flight Paths
**Goal**: Server-side Milestone 0 is complete — patrol mobs walk cities, players can use command prefixes and personal aliases, and the Dragon Courier flight system moves players between discovered nodes
**Depends on**: Nothing (extends existing AreaBuilder and typeclass foundations)
**Requirements**: IWA-01, IWA-02, IWA-03, IWA-04, IWA-05, IWA-06, IWA-07, IWA-08, FLT-01, FLT-02, FLT-03, FLT-04, CMD-01, CMD-02, CMD-03, CMD-04, CMD-05
**Success Criteria** (what must be TRUE):
  1. A patrol mob placed in an area walks a BFS-computed route, stops to fight any player it arrives near, and resumes/resets/abandons per its configured interruption mode
  2. Custom commands attached to rooms or mobs via AreaBuilder fire their shared action vocabulary (teleport, echo, modify_standing, spawn_mob) when invoked
  3. Triggers fire on room enter, exit, first visit, mob death, and examine, with once-per-character and cooldown constraints enforced
  4. A player can type `at` and have it resolve to `attack` without ambiguity; `n` resolves to `north` in contexts where only one match exists
  5. A player alias `kill $1` expands correctly and never overrides built-in system commands
  6. A player boards the Dragon Courier, selects a discovered destination, and arrives at the correct location with Standing-based fare applied
**Plans**: 6 plans

Plans:
- [x] 01-01-PLAN.md — Action vocabulary (execute_action dispatch) + trigger engine
- [x] 01-02-PLAN.md — Patrol engine BFS + PatrolScript + mob/room hooks
- [x] 01-03-PLAN.md — Command prefix resolution + player alias system
- [x] 01-04-PLAN.md — AreaBuilder extensions: patrol(), trigger(), custom_command(), flight_point(), flight_route()
- [x] 01-05-PLAN.md — Flight engine, FlightScript, CmdFly/CmdDisembark, character/room wiring
- [x] 01-06-PLAN.md — Test suite: patrol, trigger, command prefix, flight system

### Phase 2: OOB Push and Desktop Client
**Goal**: Server-side OOB publisher delivers a typed contract for all server→client push data; room coordinates computed and stored for map rendering; Tauri desktop client deferred to Phase 2.1
**Depends on**: Phase 1 (room coordinates added in IWA/AreaBuilder work)
**Requirements**: CLI-06, CLI-07
**Note**: CLI-01 through CLI-05 (Tauri client) deferred to Phase 2.1 per CONTEXT.md D-01/D-02.
**Success Criteria** (what must be TRUE):
  1. The server pushes all structured state through oob_publisher.py with a typed envelope contract covering 8 message types
  2. Debounce prevents message flooding per message type; combat_update max 4/sec, inventory_update max 1/sec
  3. Every room in every zone has non-None grid_x/grid_y integer coords after build(); builder-placed coords are preserved
  4. Zone objects store world_x, world_y, world_radius, fog_of_war for world map rendering
**Plans**: 4 plans

Plans:
- [x] 02-01-PLAN.md — OOB publisher (world/oob_publisher.py) + character hooks (at_after_move, visited_room_ids, at_post_puppet wiring)
- [x] 02-02-PLAN.md — Room coordinates and BFS auto-layout (AreaBuilder grid_x/grid_y + auto_layout_zone + zone world coords)
- [x] 02-03-PLAN.md — Integration hooks (NodeScript node_event, FlightScript flight_progress, commit_session_xp status_update)
- [x] 02-04-PLAN.md — Test suite: test_oob_publisher.py (CLI-06) + coordinate tests in test_area_builder.py (CLI-07)

### Phase 3: GUI Area Builder
**Goal**: Server-side JSON zone loading infrastructure is complete — the server loads .zone.json files natively, cross-zone exits resolve correctly regardless of load order, and a pure-Python validation module provides a shared schema contract for the builder app
**Depends on**: Phase 2 (AreaBuilder spec schema stabilized)
**Requirements**: BLD-02, BLD-05, BLD-06
**Note**: BLD-01, BLD-03, BLD-04 (Tauri app) deferred to separate soravelon-builder project per CONTEXT.md D-01/D-02.
**Success Criteria** (what must be TRUE):
  1. Cross-zone exits defined in any load order resolve correctly on server reload — no silent skips (two-pass fix)
  2. Server loads .zone.json files from world/areas/ alongside .py files in sorted order
  3. load_zone_from_json() validates then produces identical DB objects to an equivalent .py zone file
  4. world/area_validator.py is importable without Django setup (pure Python sidecar-ready)
**Plans**: 4 plans

Plans:
- [x] 03-01-PLAN.md — world/area_validator.py (pure-Python validation module, constants extracted from area_builder)
- [x] 03-02-PLAN.md — Two-pass cross-zone exit fix (AreaBuilder._UNRESOLVED_EXITS_REGISTRY + _load_all_zones() second pass)
- [x] 03-03-PLAN.md — world/zone_serializer.py (JSON→AreaBuilder adapter) + _load_all_zones() .zone.json support
- [x] 03-04-PLAN.md — Test suite: test_area_validator.py + test_zone_serializer.py + two-pass registry tests

### Phase 03.1: Mob Spawn Runtime (INSERTED)

**Goal:** Mobs appear in zones at runtime -- spawn definitions on rooms produce SoravelonMob instances with affixes, patrol scripts attach automatically, named mobs are merged into spawn_definitions (no separate registry), dead mobs respawn on timers, and skill-based loot drops on death
**Requirements**: SPAWN-01 through SPAWN-14 (added as infrastructure prerequisite for Phase 6 combat and Phase 7 content)
**Depends on:** Phase 3 (AreaBuilder stores spawn/patrol definitions), Phase 1 (mob_affix_roller, PatrolScript, zone_scaling)
**Success Criteria** (what must be TRUE):
  1. When a zone loads, rooms with spawn_definitions produce the correct count of SoravelonMob instances with rarity-rolled affixes and combat stats
  2. Named mobs are spawn_definitions with is_named=True -- named_mob_registry.py is deleted; area.named_mob() wraps area.spawn()
  3. Patrol definitions automatically attach PatrolScript to spawned mobs with the correct route; find_path() skips no_mobs rooms
  4. Dead mobs respawn after respawn_minutes +/- respawn_variance without duplicating (Twisted callLater)
  5. Count management enforces count_min/count_max per spawn definition; server reload preserves existing mobs
  6. roll_loot() uses killer's skill score (not level) for material tier; items created via item_spawner and placed in room
**Plans:** 5/5 plans complete

Plans:
- [x] 03.1-01-PLAN.md -- world/mob_spawner.py: spawn_zone, spawn_room_mobs, spawn_single_mob, spawn_named_mob, _maybe_attach_patrol, _schedule_respawn
- [x] 03.1-02-PLAN.md -- world/item_spawner.py (create_item_from_template) + AreaBuilder refactor (item() method, named_mob() wrapper, remove named_mob_registry)
- [x] 03.1-03-PLAN.md -- Integration wiring: spawn_zone in _load_all_zones, at_death respawn/loot/tome, patrol no_mobs filter, action_vocabulary spawn_mob + give_item template_id
- [x] 03.1-04-PLAN.md -- world/loot_tables.py: extend stub to full roll_loot() + skill-based LOOT_TABLES; zone override support
- [x] 03.1-05-PLAN.md -- Test suite: test_mob_spawner.py + test_item_spawner.py + test_loot_tables.py + area_builder regression tests

### Phase 4: Domain Fingerprints and Guild Engine
**Goal**: The mechanical identity of all 10 domains is locked in a design document and enforced by the guild/GTS engine — no ability will be authored without a fingerprint to validate against
**Depends on**: Phase 1 (domain score tracking already exists; this formalizes it with GTS computation)
**Requirements**: DOM-01, DOM-02, DOM-03, DOM-04, DOM-05
**Success Criteria** (what must be TRUE):
  1. A design document specifies the exclusive mechanical gameplay verb for each of the 10 domains (e.g., "Combat: force-movement", "Subterfuge: information asymmetry") — all 10 are distinct and non-overlapping
  2. Guild Tier Score computes correctly as (primary x 0.66) + (secondary x 0.33) and returns the correct tier label at thresholds 0/20/50/85
  3. A guild organically discovers a player when their domain score reaches the Practiced threshold (~30) without explicit player action
  4. Domain scores display the correct GTS tier label to the player with no numeric level shown
  5. CharacterGuild Django model exists with correct migration (CharacterAbility deferred to Phase 5 per D-16)
**Plans**: 2 plans

Plans:
- [x] 04-01-PLAN.md — Design doc consolidation + guild_engine.py constants/computation + CharacterGuild model + migration
- [x] 04-02-PLAN.md — join_guild/complete_induction mutation functions + test suite (test_guild_engine.py)

### Phase 5: Ancestry Engine and Ability System
**Goal**: Phase 5a builds the ancestry engine, ability framework, room state system, and all structural infrastructure. Phase 5b (separate) authors all 330 ability definitions collaboratively.
**Depends on**: Phase 4 (domain fingerprints and GTS engine must exist before ability authoring begins)
**Requirements**: ANC-01, ANC-02, ANC-03, ANC-04, ANC-05, ABL-01, ABL-02, ABL-03, ABL-04, ABL-05, ABL-06
**Note**: ABL-04 (full 330 ability content) deferred to Phase 5b per CONTEXT.md D-01. Phase 5a delivers stub abilities only.
**Success Criteria** (what must be TRUE):
  1. Each of the 4 ancestries applies its mechanical trait at character creation (e.g., Kau'roran size modifier, Veth tunnel shortcuts) and the traits feed into mob disposition calculations
  2. A player with a Duskblade (Combat+Subterfuge) subclass has access to abilities that could not be mistaken for a Thornguard (Combat+Naturalism) — each subclass's Tier 1 ability set is mechanically distinct
  3. The `use <ability>` dispatcher handles all 360+ abilities through a single CmdUseAbility command — no per-ability Cmd classes exist
  4. Ability tier gating unlocks correctly at GTS thresholds 0/20/50/85; attempting a locked ability returns a clear feedback message
  5. Ability cooldowns tracked per-encounter on character.ndb reset correctly between encounters
**Plans**: 5 plans

Plans:
- [x] 05-01-PLAN.md — Ancestry engine (world/ancestry_engine.py) + room state (world/room_state.py) + mob death flag writers + action vocabulary handler
- [x] 05-02-PLAN.md — Ability registry (world/ability_registry.py) + CharacterAbility model + migration + Ironwright fix
- [x] 05-03-PLAN.md — Ability engine (world/ability_engine.py) + Character ndb/db inits + Sense hook
- [x] 05-04-PLAN.md — Commands (CmdSetAncestry, CmdJoinGuild, CmdDomains, CmdAbilities, CmdUseAbility) + guild discovery wiring + cmdset registration
- [x] 05-05-PLAN.md — Test suite: test_ancestry_engine.py + test_ability_engine.py + test_room_state.py

### Phase 6a: Base Attributes & Combat System
**Goal**: Character base attribute system (7 stats, point-buy, descriptor display, stat growth) and full turn-based combat (CombatScript, initiative, action budget, damage formula, status effects with compounds, corpse containers, flee)
**Depends on**: Phase 5 (ability system must exist before combat can dispatch ability effects)
**Requirements**: CMB-01, CMB-02, CMB-03, CMB-04
**Success Criteria** (what must be TRUE):
  1. A player uses an ability in combat and the correct damage, status effect, or positional change resolves against a mob; zone-scaling logarithmic math applies to that mob's stats
  2. Group combat correctly distributes loot using the existing group engine's loot modes
  3. Status effect compounds (Burn+Wet=Steam, Poison+Slow=Venom Lag) trigger correctly in combat
  4. Base attributes display as descriptors only (no numbers visible to players); attributes grow through action-specific use
**Plans**: 7 plans

Plans:
- [x] 06a-01-PLAN.md — Base attributes: 7 stats, 70 descriptors, point-buy, stat growth, HP/stamina/action-budget derivation
- [x] 06a-02-PLAN.md — Status effects: stackable/non-stackable effects, compound matrix, tick logic
- [x] 06a-03-PLAN.md — Combat engine: damage resolution, ability handler wiring, corpse containers, death handling
- [x] 06a-04-PLAN.md — Combat AI: mob ability selection, targeting, condition vocabulary, scripted sequences
- [x] 06a-05-PLAN.md — CombatScript: room-attached turn manager, initiative, round progression, group timeout
- [x] 06a-06-PLAN.md — Combat commands: CmdAttack/CmdFlee/CmdTarget/CmdPass, CombatCmdSet, auto-engage, OOB publishers
- [ ] 06a-07-PLAN.md — Test suite: test_base_attributes + test_status_effects + test_combat_engine + test_combat_ai + test_combat_script

### Phase 6b: Spawn System, Skills & Mob AI
**Goal**: Mob spawn/respawn runtime with SpawnRecord model, mob ability AI with weighted priority selection, and full general proficiency + attunement skill system with discovery framework
**Depends on**: Phase 6a (combat system required for mob abilities and spawn integration)
**Requirements**: CMB-04, SKL-01, SKL-02, SKL-03, SKL-04
**Success Criteria** (what must be TRUE):
  1. Mobs respawn on timer after death via SpawnRecord + global ticker; named mobs announce to zone on respawn
  2. Mob abilities fire based on weight and cooldown conditions during combat turns
  3. A general proficiency skill (e.g., Lockpicking) increases through passive use and deliberate practice independently of the domain system
  4. Ancestry skill seeds are applied via set_ancestry(); attunement skills track per-zone and per-creature progress
**Plans**: TBD

### Phase 6c: NPC Dialogue & Crafting
**Goal**: NPC dialogue system with Standing-tier greetings, keyword topics, dynamic hints, ambient behavior; crafting framework with recipe registry, quality variance, and basic output for Cooking/Smithing/Alchemy
**Depends on**: Phase 6b (skill system required for crafting proficiencies and trainer interactions)
**Requirements**: NPC-01, NPC-02, NPC-03, SKL-03
**Success Criteria** (what must be TRUE):
  1. An NPC gives different dialogue to a player with high vs. low standing, or to a Kau'roran vs. a Human ancestry — the context packet drives the variation
  2. Dynamic hints show relevant topics based on Standing tier, active quests, and world-state dimensions
  3. Crafting a recipe with ingredients produces an item; quality varies based on skill level — higher skill = better results
  4. Ambient NPC echoes fire on timer with variance, creating lived-in atmosphere
**Plans**: TBD

### Phase 7: Milestone 1 Content
**Goal**: Soravelon's first playable slice is live — Vael's Crossing is navigable, 4 starter zones are populated with mobs and NPCs, one zone has an active node with Layer 1 rooms, and basic weapons and armor exist
**Depends on**: Phase 3 (GUI builder required to author content), Phase 6c (combat, NPC, and skill systems required for meaningful play)
**Requirements**: CON-01, CON-02, CON-03, CON-04
**Success Criteria** (what must be TRUE):
  1. A new player arrives in Vael's Crossing, can navigate to bank, guild, and services, and the city feels inhabited with NPCs and ambient content
  2. Three starter zones have rooms, mobs, NPCs, and basic quests playable from character creation; mob encounters use the ability-driven combat system
  3. One starter zone's active node transitions through its failure states (healthy → stressed → failing → collapsed), swapping Layer 0 rooms for Layer 1 rooms correctly
  4. Basic weapons and armor are obtainable from zone loot and city vendors with no procedural affixes
**Plans**: TBD

### Phase 13: Gathering and Refining
**Goal**: Resource gathering nodes spawn stochastically in flagged rooms with zone-wide pool limits, players use skill-specific commands (mine, harvest, chop, forage, fish, butcher) to extract raw materials, processing recipes convert raw materials into crafting ingredients (ore->ingot, fiber->thread->cloth), a fishing mini-game and idle mode exist, tools with durability are required, and a scalable 5-tier MATERIAL_REGISTRY organizes all materials
**Depends on**: Phase 6c (crafting system must exist), Phase 9 (trainers and zone content must be wired)
**Requirements**: SC-1, SC-2, SC-3, SC-4, SC-5, SC-6, SC-7, SC-8
**Success Criteria** (what must be TRUE):
  1. Gathering nodes spawn randomly in eligible rooms per zone-level gathering_pool() definitions with max_active limits; depleted nodes respawn in different eligible rooms
  2. Players use mine/harvest/chop/forage/fish/butcher commands with required tools; gathering delay varies by tier and is reduced by skill (min 40% of base)
  3. Processing recipes in RECIPE_REGISTRY convert raw materials to crafting ingredients with skill-based conversion ratios (3:1->2:1->1:1) and quality propagation
  4. MATERIAL_REGISTRY in world/material_definitions.py defines all materials with 5 expandable tiers, categories, and skill mappings
  5. Fishing has an active mini-game (cast->bite->reel) with full rewards and an idle mode with diminished returns
  6. Tools degrade with use and are repairable via smithing; no tool = cannot gather
  7. Prospect/survey reveals nodes in straight lines with directional indicators; Sense gives vague hints; tiered visibility gates mid/high-tier nodes by skill
  8. Mob loot drops (hides, bones, silk) feed into the processing pipeline as raw materials
**Plans**: 7 plans

Plans:
- [x] 13-01-PLAN.md — Material registry + new gathering skills + room state flags + item_tag fix
- [x] 13-02-PLAN.md — GatheringNode typeclass + gathering_engine.py + GatheringPoolScript + AreaBuilder DSL
- [x] 13-03-PLAN.md — Processing recipes in RECIPE_REGISTRY + crafting engine conversion ratio extension
- [x] 13-04-PLAN.md — Gathering commands (_BaseGatherCmd + mine/harvest/chop/forage/butcher) + corpse butcher
- [x] 13-05-PLAN.md — Fishing system (CmdFish active + idle modes, CmdReel)
- [x] 13-06-PLAN.md — Prospect/survey + Sense gathering hints + tool repair + command registration
- [x] 13-07-PLAN.md — Test suite: test_gathering.py + test_fishing.py

**Canonical refs**: world/crafting_engine.py, world/crafting_definitions.py, commands/cmd_crafting.py, world/item_spawner.py, world/loot_tables.py, world/mob_spawner.py, world/skill_definitions.py

### Phase 14: All TBD/TODOs Implemented
**Goal**: Implement all stub functions and placeholder handlers left by Phases 1-13: death penalty (20% Scales drop on corpse + uncommitted XP loss), combat affix hooks (rarity damage multipliers + status effect mapping), quest stub wiring to Phase 11's quest engine, WorldEventScript behavior, Lore help entry, OOB quest_update payload, attuned variant text, and zone tier reference cleanup
**Depends on**: Phase 13 (gathering system complete), Phase 11 (quest engine exists)
**Requirements**: SC-1, SC-2, SC-3, SC-4, SC-5, SC-6, SC-7, SC-8
**Success Criteria** (what must be TRUE):
  1. on_character_death() drops 20% of carried Scales into the player's corpse container and wipes uncommitted session XP
  2. check_mob_damage_modifiers() returns rarity-based multipliers (1.0/1.15/1.3/1.5); check_mob_on_hit_effects() and check_mob_per_round_effects() apply status effects from affix definitions
  3. set_quest_flag and open_dialogue action handlers call into quest_engine instead of _stub_handler
  4. Dialogue engine pulls active quest hints instead of returning empty stubs
  5. WorldEventScript has real event tracking behavior; Lore help entry has real content
  6. quest_update OOB message has a defined payload shape with quest progress data
  7. No TODO/STUB/placeholder comments remain in production source (excluding tests)
  8. No references to "zone tier" as a game concept remain in source code
**Plans**: 4 plans

Plans:
- [x] 14-01-PLAN.md — Death penalty (Scales drop + XP loss) + combat affix hooks (rarity multipliers + status effects)
- [x] 14-02-PLAN.md — Quest stub wiring (action vocabulary + dialogue hints + OOB payload + mob disposition)
- [x] 14-03-PLAN.md — WorldEventScript + Lore help entry + attuned variant text
- [x] 14-04-PLAN.md — Final sweep: STUB/placeholder cleanup + zone tier removal + test updates

### Phase 15: Implement Missing Gameplay Gap Systems
**Goal**: Game is fully playable end-to-end — vendor economy closes the Scales loop, HP/stamina recovery enables between-fight healing, item inspection gives stat visibility, social commands enable multiplayer communication, combat bugs are fixed, and all missing content (tools, loot tables, crafting outputs, quest items) is authored
**Depends on**: Phase 14 (all stubs implemented)
**Requirements**: D-01, D-02, D-03, D-04, D-05, D-06, D-07, D-08, D-09, D-10, D-11, D-12, D-13, D-14, D-15, D-16, D-17, D-18, D-19, D-20, D-21, D-22, D-23, D-24, D-25, D-26, D-27, D-28
**Success Criteria** (what must be TRUE):
  1. Players can buy/sell items at vendor NPCs with type restrictions, 33% sell-back, and faction price adjustments
  2. HP/stamina regenerates passively out of combat; rest/sleep accelerates recovery; medic blessings heal for Scales
  3. All ability effect handlers return (bool, str) tuples; compound effects (steam/discharge/petrify) work correctly
  4. Custom loot command respects corpse phase checks; group loot distributes per mode
  5. Players can see who's online, shout zone-wide, whisper privately, and use OOC/domain channels
  6. Item inspection gated by appraisal skill; compare shows side-by-side stats
  7. 5 gathering tools equippable in separate tool slots; fish pools in coastal zones
  8. Rat/bandit loot tables, 10 crafting output definitions, and 8 quest items with sources all authored
**Plans**: 5 plans

Plans:
- [ ] 15-01-PLAN.md — Vendor engine + CATALOG extraction + vendor commands + NPC wiring
- [x] 15-02-PLAN.md — Recovery engine (regen ticks, rest/sleep, medic blessings) + commands + character wiring
- [ ] 15-03-PLAN.md — Combat fixes (ability return normalization, compound effects, corpse loot, group loot)
- [ ] 15-04-PLAN.md — Social systems (who/shout/whisper, OOC/domain channels) + item inspection/compare
- [ ] 15-05-PLAN.md — Missing content (gathering tools, fish pools, loot tables, crafting outputs, quest items)

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 3.1 -> 4 -> 5 -> 6a -> 6b -> 6c -> 7

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Patrol, Commands, and Flight Paths | 6/6 | Complete | 2026-03-24 |
| 2. OOB Push and Desktop Client | 4/4 | Complete | 2026-03-25 |
| 3. GUI Area Builder | 4/4 | Complete | 2026-03-25 |
| 3.1 Mob Spawn Runtime (INSERTED) | 5/5 | Complete | 2026-03-25 |
| 4. Domain Fingerprints and Guild Engine | 0/2 | Not started | - |
| 5. Ancestry Engine and Ability System | 0/5 | Not started | - |
| 6a. Base Attributes & Combat System | 0/7 | Not started | - |
| 6b. Spawn System, Skills & Mob AI | 0/TBD | Not started | - |
| 6c. NPC Dialogue & Crafting | 0/TBD | Not started | - |
| 7. Milestone 1 Content | 0/TBD | Not started | - |
| 12. Launch Polish and Help | 1/3 | Complete    | 2026-04-03 |
| 13. Gathering and Refining | 7/7 | Complete    | 2026-04-04 |
| 14. All TBD/TODOs Implemented | 4/4 | Complete    | 2026-04-04 |
| 15. Implement Missing Gameplay Gap Systems | 1/5 | In Progress|  |
