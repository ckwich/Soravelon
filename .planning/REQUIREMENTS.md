# Requirements: Soravelon

**Defined:** 2026-03-24
**Core Value:** Character identity must feel mechanically distinct — 90 subclasses play differently, not just look different.

## v1 Requirements

Requirements for Milestone 0 completion + Milestone 1 playable skeleton.

### Interactive World Authoring

- [x] **IWA-01**: Patrol system with BFS pathfinding drives mob route-following behavior
- [x] **IWA-02**: Patrol mobs check disposition against players on room arrival and break for combat
- [x] **IWA-03**: Patrol interruption modes work correctly (resume / reset_to_start / abandon)
- [x] **IWA-04**: Custom commands can be attached to rooms, mobs, and items via AreaBuilder
- [x] **IWA-05**: Shared action vocabulary executes teleport, echo, modify_standing, spawn_mob, and other actions
- [x] **IWA-06**: Trigger system fires on room enter, exit, first visit, mob death, and examine events
- [x] **IWA-07**: Triggers support once-per-character and cooldown constraints
- [x] **IWA-08**: AreaBuilder exposes patrol(), custom_command(), and trigger() methods

### Flight Paths

- [x] **FLT-01**: Dragon Courier Service provides instant transit between discovered flight points
- [x] **FLT-02**: Flight points are discovery-gated (must visit the location first)
- [x] **FLT-03**: Multi-leg booking supported for indirect routes
- [x] **FLT-04**: Standing-based pricing with faction discounts

### Commands

- [x] **CMD-01**: Command prefix matching resolves shortest unambiguous prefix
- [x] **CMD-02**: Context-sensitive CmdSet scope narrows ambiguity automatically
- [x] **CMD-03**: Player aliases support up to 3 commands per alias with semicolons
- [x] **CMD-04**: Argument tokens ($1, $2, $*, $@) expand correctly in aliases
- [x] **CMD-05**: Aliases never override system commands

### Desktop Client

- [ ] **CLI-01**: Tauri 2.0 desktop client connects to Evennia via WebSocket
- [ ] **CLI-02**: Terminal pane renders MUD text output with ANSI color support
- [ ] **CLI-03**: Status panel displays character dimensions, domain scores, and companion status
- [ ] **CLI-04**: Map panel renders zone layout with room nodes and exit edges
- [ ] **CLI-05**: Map panel shows node activity state (color-coded failure slider)
- [x] **CLI-06**: OOB publisher module provides typed contract for all server→client push data
- [x] **CLI-07**: Room coordinates stored in AreaBuilder for map rendering

### GUI Area Builder

- [ ] **BLD-01**: Tauri 2.0 app with @xyflow/react canvas for visual zone editing
- [x] **BLD-02**: Builder outputs valid AreaBuilder .py files
- [ ] **BLD-03**: Owner mode has full access to all zone IDs and type definitions
- [ ] **BLD-04**: Contributor mode works from reference bundle with restricted scope
- [ ] **BLD-05**: Mob ability composer allows data-driven ability design without code
- [ ] **BLD-06**: Two-pass area loading fix resolves cross-zone exit load-order bug

### Domain & Guild System

- [x] **DOM-01**: 10 domains tracked with 0-100 scores and diminishing returns
- [x] **DOM-02**: Guild Tier Score computed as (primary × 0.66) + (secondary × 0.33)
- [x] **DOM-03**: Guild discovers player organically at Practiced proficiency (~30 domain score)
- [x] **DOM-04**: GTS tier labels provide non-numeric progression feedback to players
- [x] **DOM-05**: 10 domain mechanical fingerprints designed (distinct gameplay verb per domain)

### Ability System

- [x] **ABL-01**: Global data-driven ability registry (not per-character instances)
- [x] **ABL-02**: CmdUseAbility dispatcher handles all 360+ abilities through one command
- [x] **ABL-03**: Ability tier gating unlocks at Guild Tier Score 0/20/50/85
- [x] **ABL-04**: All 90 subclasses have mechanically distinct ability sets (4 tiers each)
- [x] **ABL-05**: Ability cooldowns tracked per-encounter on mob.ndb
- [x] **ABL-06**: Subclass engine derives identity from primary + secondary domain pair

### Combat

- [ ] **CMB-01**: Combat system integrates ability effects with damage, status, and targeting
- [ ] **CMB-02**: Zone scaling applies per-player logarithmic factors during combat
- [ ] **CMB-03**: Mob abilities fire based on weight, cooldown, and condition vocabulary
- [ ] **CMB-04**: Group combat uses existing group engine for proximity and loot

### Skills & Professions

- [ ] **SKL-01**: General proficiency skills (0-100) with learn-by-use progression
- [ ] **SKL-02**: 4 profession tracks: Cooking, Smithing, Alchemy, Scholarly Research
- [ ] **SKL-03**: Animal Handling skill track (0-100) with Dragon Handling unlock at 100
- [ ] **SKL-04**: Profession progression is independent of domain/guild system

### Ancestries

- [x] **ANC-01**: Human ancestry with Empire Standing bonus and world-reaction traits
- [x] **ANC-02**: Kau'roran ancestry with size, cultural traits, and kiai ceremony access
- [x] **ANC-03**: Veth ancestry with size modifiers, tunnel shortcuts, and information networks
- [x] **ANC-04**: Selvar ancestry with seasonal coat variation and social perception modifiers
- [ ] **ANC-05**: Ancestry modifiers feed into mob disposition calculation (additive, not override)

### Content

- [ ] **CON-01**: Hub City 1 (Vael's Crossing) authored via GUI builder with full services
- [ ] **CON-02**: 3 starter zones with Layer 0 content (rooms, mobs, NPCs, quests)
- [ ] **CON-03**: 1 starter zone with active node and Layer 1 implementation
- [ ] **CON-04**: Basic equipment (weapons/armor) available without procedural affixes

### NPC System

- [ ] **NPC-01**: NPC template system injects world-state variables into dialogue
- [ ] **NPC-02**: NPCs respond differently based on character standing, ancestry, and reputation
- [ ] **NPC-03**: Context packet feeds NPC templates (same interface as future LLM consumer)

## v2 Requirements

### Companion System (Milestone 2)

- **CMP-01**: Animal Handling skill progression unlocks companion tiers (Familiar/Companion/Bonded)
- **CMP-02**: Dragon bonding requires AH 100 + Warding 75+ or kiai ceremony
- **CMP-03**: Dragon growth stages (Hatchling → Juvenile → Adult → Elder)
- **CMP-04**: Mount system with saddlebag containers and mounted combat

### Content Push (Milestone 4)

- **CTN-01**: Procedural equipment affixes
- **CTN-02**: Zones 1-20 complete
- **CTN-03**: Hub City 2: Caldenmere (walking golem city)

### Economy (Future)

- **ECO-01**: Auction House (local hub AHs, then Wandering Exchange)
- **ECO-02**: Tome system + Loremaster NPC framework

## Out of Scope

| Feature | Reason |
|---------|--------|
| Companion/mount/dragon system | Milestone 2 — requires domain mastery first |
| Procedural equipment affixes | Milestone 4 content push |
| LLM quest generation | Post-M2 — data collection started, infrastructure deferred |
| Auction House / Wandering Exchange | Future milestone — banking ready as dependency |
| Day/night cycle runtime | Triggers stored but not fired until time system built |
| Mobile client | No plans — desktop client only |
| Zones beyond starter region | Milestone 4+ content push |
| Visible level numbers | Anti-feature — contradicts core design (no visible levels) |
| Stamina/mana resource pools | Design TBD — not decided, don't build speculatively |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| IWA-01 | Phase 1 | Complete |
| IWA-02 | Phase 1 | Complete |
| IWA-03 | Phase 1 | Complete |
| IWA-04 | Phase 1 | Complete |
| IWA-05 | Phase 1 | Complete |
| IWA-06 | Phase 1 | Complete |
| IWA-07 | Phase 1 | Complete |
| IWA-08 | Phase 1 | Complete |
| FLT-01 | Phase 1 | Complete |
| FLT-02 | Phase 1 | Complete |
| FLT-03 | Phase 1 | Complete |
| FLT-04 | Phase 1 | Complete |
| CMD-01 | Phase 1 | Complete |
| CMD-02 | Phase 1 | Complete |
| CMD-03 | Phase 1 | Complete |
| CMD-04 | Phase 1 | Complete |
| CMD-05 | Phase 1 | Complete |
| CLI-01 | Phase 2 | Pending |
| CLI-02 | Phase 2 | Pending |
| CLI-03 | Phase 2 | Pending |
| CLI-04 | Phase 2 | Pending |
| CLI-05 | Phase 2 | Pending |
| CLI-06 | Phase 2 | Complete |
| CLI-07 | Phase 2 | Complete |
| BLD-01 | Phase 3 | Pending |
| BLD-02 | Phase 3 | Complete |
| BLD-03 | Phase 3 | Pending |
| BLD-04 | Phase 3 | Pending |
| BLD-05 | Phase 3 | Pending |
| BLD-06 | Phase 3 | Pending |
| DOM-01 | Phase 4 | Complete |
| DOM-02 | Phase 4 | Complete |
| DOM-03 | Phase 4 | Complete |
| DOM-04 | Phase 4 | Complete |
| DOM-05 | Phase 4 | Complete |
| ANC-01 | Phase 5 | Complete |
| ANC-02 | Phase 5 | Complete |
| ANC-03 | Phase 5 | Complete |
| ANC-04 | Phase 5 | Complete |
| ANC-05 | Phase 5 | Pending |
| ABL-01 | Phase 5 | Complete |
| ABL-02 | Phase 5 | Complete |
| ABL-03 | Phase 5 | Complete |
| ABL-04 | Phase 5 | Complete |
| ABL-05 | Phase 5 | Complete |
| ABL-06 | Phase 5 | Complete |
| CMB-01 | Phase 6 | Pending |
| CMB-02 | Phase 6 | Pending |
| CMB-03 | Phase 6 | Pending |
| CMB-04 | Phase 6 | Pending |
| SKL-01 | Phase 6 | Pending |
| SKL-02 | Phase 6 | Pending |
| SKL-03 | Phase 6 | Pending |
| SKL-04 | Phase 6 | Pending |
| NPC-01 | Phase 6 | Pending |
| NPC-02 | Phase 6 | Pending |
| NPC-03 | Phase 6 | Pending |
| CON-01 | Phase 7 | Pending |
| CON-02 | Phase 7 | Pending |
| CON-03 | Phase 7 | Pending |
| CON-04 | Phase 7 | Pending |

**Coverage:**
- v1 requirements: 61 total
- Mapped to phases: 61
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-24*
*Last updated: 2026-03-24 after roadmap creation*
