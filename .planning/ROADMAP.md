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
- [ ] 01-01-PLAN.md — Action vocabulary (execute_action dispatch) + trigger engine
- [ ] 01-02-PLAN.md — Patrol engine BFS + PatrolScript + mob/room hooks
- [x] 01-03-PLAN.md — Command prefix resolution + player alias system
- [ ] 01-04-PLAN.md — AreaBuilder extensions: patrol(), trigger(), custom_command(), flight_point(), flight_route()
- [ ] 01-05-PLAN.md — Flight engine, FlightScript, CmdFly/CmdDisembark, character/room wiring
- [ ] 01-06-PLAN.md — Test suite: patrol, trigger, command prefix, flight system

### Phase 2: OOB Push and Desktop Client
**Goal**: Players can connect to Soravelon via a dedicated Tauri desktop app that shows the MUD terminal, live character status, and a visual zone map; all server→client state flows through a typed OOB publisher
**Depends on**: Phase 1 (room coordinates added in IWA/AreaBuilder work)
**Requirements**: CLI-01, CLI-02, CLI-03, CLI-04, CLI-05, CLI-06, CLI-07
**Success Criteria** (what must be TRUE):
  1. The Tauri client connects to Evennia over WebSocket and renders MUD text with correct ANSI colors in a scrollable terminal pane (5000-line cap, no memory growth in 4-hour sessions)
  2. The status panel updates in real time showing current domain scores, dimension values, and companion status as they change
  3. The map panel renders the current zone's rooms as nodes and exits as edges, color-coded by node activity state
  4. The server pushes all structured state through oob_publisher.py with a typed envelope contract; the client handles unknown message types without crashing
**Plans**: TBD
**UI hint**: yes

### Phase 3: GUI Area Builder
**Goal**: Zone content can be authored visually — a Tauri app lets the owner create rooms, place exits, attach mobs, and save a valid AreaBuilder .py file to disk; cross-zone exits never silently fail on load
**Depends on**: Phase 2 (Tauri app foundation, AreaBuilder spec schema stabilized)
**Requirements**: BLD-01, BLD-02, BLD-03, BLD-04, BLD-05, BLD-06
**Success Criteria** (what must be TRUE):
  1. The owner can open the builder, create a zone with rooms and exits on a visual canvas, place mob templates, and save a .py file that the server loads correctly on reload
  2. Cross-zone exits defined in any order load correctly on server reload — no silent skips
  3. Contributor mode restricts editing to a provided reference bundle scope; owner mode has unrestricted access
  4. The mob ability composer lets a designer define mob ability data without writing Python
  5. The builder validates the AreaBuilder spec with Zod before writing to disk and surfaces errors to the user
**Plans**: TBD
**UI hint**: yes

### Phase 4: Domain Fingerprints and Guild Engine
**Goal**: The mechanical identity of all 10 domains is locked in a design document and enforced by the guild/GTS engine — no ability will be authored without a fingerprint to validate against
**Depends on**: Phase 1 (domain score tracking already exists; this formalizes it with GTS computation)
**Requirements**: DOM-01, DOM-02, DOM-03, DOM-04, DOM-05
**Success Criteria** (what must be TRUE):
  1. A design document specifies the exclusive mechanical gameplay verb for each of the 10 domains (e.g., "Combat: force-movement", "Subterfuge: information asymmetry") — all 10 are distinct and non-overlapping
  2. Guild Tier Score computes correctly as (primary × 0.66) + (secondary × 0.33) and returns the correct tier label at thresholds 0/20/50/85
  3. A guild organically discovers a player when their domain score reaches the Practiced threshold (~30) without explicit player action
  4. Domain scores display the correct GTS tier label to the player with no numeric level shown
  5. CharacterGuild and CharacterAbility Django models exist with correct migrations
**Plans**: TBD

### Phase 5: Ancestry Engine and Ability System
**Goal**: Players choose from 4 mechanically distinct ancestries at creation, and every one of 90 subclasses has a unique set of abilities across 4 tiers that express its domain-pair identity
**Depends on**: Phase 4 (domain fingerprints and GTS engine must exist before ability authoring begins)
**Requirements**: ANC-01, ANC-02, ANC-03, ANC-04, ANC-05, ABL-01, ABL-02, ABL-03, ABL-04, ABL-05, ABL-06
**Success Criteria** (what must be TRUE):
  1. Each of the 4 ancestries applies its mechanical trait at character creation (e.g., Kau'roran size modifier, Veth tunnel shortcuts) and the traits feed into mob disposition calculations
  2. A player with a Duskblade (Combat+Subterfuge) subclass has access to abilities that could not be mistaken for a Thornguard (Combat+Naturalism) — each subclass's Tier 1 ability set is mechanically distinct
  3. The `use <ability>` dispatcher handles all 360+ abilities through a single CmdUseAbility command — no per-ability Cmd classes exist
  4. Ability tier gating unlocks correctly at GTS thresholds 0/20/50/85; attempting a locked ability returns a clear feedback message
  5. Ability cooldowns tracked per-encounter on mob.ndb reset correctly between encounters
**Plans**: TBD

### Phase 6: Combat, Skills, and NPC Templates
**Goal**: Players can engage in ability-driven combat against zone-scaled mobs, develop proficiency skills through use, and NPCs respond with world-state-aware dialogue
**Depends on**: Phase 5 (ability system must exist before combat can dispatch ability effects)
**Requirements**: CMB-01, CMB-02, CMB-03, CMB-04, SKL-01, SKL-02, SKL-03, SKL-04, NPC-01, NPC-02, NPC-03
**Success Criteria** (what must be TRUE):
  1. A player uses an ability in combat and the correct damage, status effect, or positional change resolves against a mob; zone-scaling logarithmic math applies to that mob's stats
  2. Group combat correctly distributes loot using the existing group engine's loot modes; mob abilities fire based on weight and cooldown conditions
  3. A general proficiency skill (e.g., Lockpicking) increases through use and a profession track (Cooking) progresses independently of the domain system
  4. An NPC gives different dialogue to a player with high vs. low standing, or to a Kau'roran vs. a Human ancestry — the context packet drives the variation
**Plans**: TBD

### Phase 7: Milestone 1 Content
**Goal**: Soravelon's first playable slice is live — Vael's Crossing is navigable, 4 starter zones are populated with mobs and NPCs, one zone has an active node with Layer 1 rooms, and basic weapons and armor exist
**Depends on**: Phase 3 (GUI builder required to author content), Phase 6 (combat and NPC systems required for meaningful play)
**Requirements**: CON-01, CON-02, CON-03, CON-04
**Success Criteria** (what must be TRUE):
  1. A new player arrives in Vael's Crossing, can navigate to bank, guild, and services, and the city feels inhabited with NPCs and ambient content
  2. Three starter zones have rooms, mobs, NPCs, and basic quests playable from character creation; mob encounters use the ability-driven combat system
  3. One starter zone's active node transitions through its failure states (healthy → stressed → failing → collapsed), swapping Layer 0 rooms for Layer 1 rooms correctly
  4. Basic weapons and armor are obtainable from zone loot and city vendors with no procedural affixes
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Patrol, Commands, and Flight Paths | 1/6 | In Progress|  |
| 2. OOB Push and Desktop Client | 0/TBD | Not started | - |
| 3. GUI Area Builder | 0/TBD | Not started | - |
| 4. Domain Fingerprints and Guild Engine | 0/TBD | Not started | - |
| 5. Ancestry Engine and Ability System | 0/TBD | Not started | - |
| 6. Combat, Skills, and NPC Templates | 0/TBD | Not started | - |
| 7. Milestone 1 Content | 0/TBD | Not started | - |
