# Varath Prime Hub 4 Design

**Date:** 2026-04-20

## Goal
Build a Hub 4 capital-region content pack centered on a single large `varath_prime` city zone plus four connected exterior land-based zones, all authored in a strict `AreaBuilder`-compatible format so the Soravelon builder app can import, edit, validate, and re-export them without lossy translation.

## Hard Constraints

### Narrative
- Nothing in this pack may hint that dragons are intelligent behind the curse.
- Dragon-adjacent content may be brutal, bureaucratic, superstitious, tragic, uncanny, or politically loaded.
- History must be rich, cohesive, and trackable across all five zones.
- The capital region should emphasize ancient infrastructure, inherited wounds, Imperial revisionism, and layered public/private history.

### AreaBuilder / Builder App Compatibility
- All authored content must use the `AreaBuilder` pattern used by existing zone files.
- No raw Evennia DB calls or ad hoc content bootstrapping may appear inside authored area files.
- Zone structure must remain compatible with the builder app contract documented in:
  - `C:\Obsidian\brain\Soravelon\soravelon-builder.md`
  - `C:\Obsidian\brain\Soravelon\soravelon-areaspec.md`
  - `world/zone_serializer.py`
  - `C:\Dev\Sora_builder\sidecar\area_parser.py`
  - `C:\Dev\Sora_builder\sidecar\area_serializer.py`
- Authoring must remain round-trippable through the builder ecosystem:
  - zone metadata in `area.zone(...)`
  - rooms in `area.room(...)`
  - local and cross-zone exits in `area.exit(...)`
  - spawns in `area.spawn(...)`
  - NPCs in `area.npc(...)`
  - named mobs in `area.named_mob(...)`
  - direct mob placements in `area.mob(...)`
  - cataloged items in `area.item(...)`
  - optional node config in `area.node(...)`
  - quests in `area.quest(...)`
  - materials in `area.material(...)`
  - gathering loops in `area.gathering_pool(...)`
  - lore fragments in `area.lore_fragment(...)`
  - flight stop config in `area.flight_point(...)`
  - flight routes in `area.flight_route(...)`
- Authored payloads should stay JSON-serializable in spirit and avoid opaque runtime objects stored inside custom data blobs.
- Repeated room patterns should still be expanded into explicit `area.room(...)` declarations rather than hidden behind custom code generation helpers that the builder app cannot safely parse.

### Parser-Safe Authoring Rules
- `zone_id` must be a literal snake_case string passed directly to `AreaBuilder(...)`.
- Use the conventional `area = AreaBuilder("zone_id")` pattern inside `build()`.
- Rooms should be assigned directly to local variables via `room_var = area.room("room_id", ...)` so the parser can resolve later references.
- Inter-entity references should use direct room variables or literal room-id / zone-id strings in the established DSL pattern.
- Do not generate entity calls through helper functions, loops, comprehensions, decorators, wrappers, factories, or indirect dispatch.
- Do not hide room creation inside reusable abstractions the AST parser cannot evaluate.
- Prefer canonical direct `area.method(...)` calls in source order matching the serializer’s expectations.
- Zone IDs and room IDs should remain stable and human-auditable because the builder app keys layouts and references off those identifiers.

## Recommended Zone Lineup

### Core Hub Zone
- `varath_prime`

### Exterior Zones
- `crownroad_north`
- `old_causeway`
- `ironvein_escarpment`
- `stagcrown_preserve`

These replace the vault’s more literal Hub 4 roster with a stronger capital-region package while staying faithful to the same thematic territory.

## Narrative Spine
This pack should feel like entering the center of Imperial power and discovering that the capital was built on older roads, older sites, older scars, and older lies than the state will admit.

Every zone should express three simultaneous history layers:

1. **Ancient / pre-Imperial layer**
   Older roads, shrine sites, ruins, patterned stone, drainage works, terraces, markers, and node scars that predate current Imperial ownership.

2. **Imperial consolidation layer**
   Survey markers, checkpoints, quarry works, charters, district walls, Corps compounds, hunting boundaries, and official renaming campaigns.

3. **Current fracture layer**
   Smuggling, resistance, clerical disappearance, poaching, labor brutality, salvage economies, hidden shrines, and local memory that contradicts public inscription.

## Pack Identity
This is an **ancient capital, ancient wounds** region.

- `varath_prime` shows power, ritualized order, privilege, and surveillance.
- `crownroad_north` shows the Empire as traffic, control, and logistics.
- `old_causeway` shows that the Empire inherited corridors it does not understand.
- `ironvein_escarpment` shows extraction and desecration in plain view.
- `stagcrown_preserve` shows elite leisure built on enclosure, corruption, and controlled violence.

## Zone Specifications

### 1. `varath_prime`

**Role:** Hub city zone for Hub 4.
**Target size:** `150-180` rooms.
**Primary feel:** polished intimidation, class division, ceremonial power, hidden dissent.
**Services:** full hub-city service suite, city flight platform, trainers, guild contacts, bank, medic, market, transport, lodging.

#### District Plan
- **Crown Approach**
  Arrival roads, processional gate, customs, road checkpoints, courier traffic, first visual impression of the capital.
- **Outer Commons**
  Markets, boarding houses, labor alleys, food lines, cheap taverns, street preachers, minor officials.
- **Ministry Ward**
  Archives, tax offices, permit halls, public records, sealed clerical buildings, decree walls.
- **Martial Quarter**
  Barracks, drill fields, armories, officer taverns, logistics courts, military chapels.
- **Dragon Corps Enclave**
  Handler courts, tack stores, feed depots, training rings, observation galleries, restricted holding structures, flight platform.
- **Circle District**
  Walled magical quarter, observatories, sanctioned laboratories, lecture halls, magical commerce under seal.
- **Noble Heights**
  Villas, high courts, salons, patronage houses, diplomatic gardens, private guards.
- **Hidden Warrens**
  Basements, service tunnels, concealed courtyards, illicit print cells, smugglers, covert resistance paths, hidden Veilcraft access.

#### Content Targets
- `45-60` static/service/story NPCs
- `20-30` ambient or patrol NPCs
- `3-5` hostile or restricted pockets
- `3+` faction quest hubs
- ancestry-sensitive city reactions
- public inscriptions and decrees that can be contradicted elsewhere

#### Narrative Duties
- Present the official Imperial story first.
- Introduce the region’s key institutions:
  - Human Empire
  - Imperial Dragon Corps
  - Circle of Wizards
  - Accord
  - Ironblood
  - Warcraft
- Seed hidden history through records, damaged plaques, sealed doors, confiscated ledgers, and whispered testimony.

### 2. `crownroad_north`

**Role:** Main overland approach to the capital.
**Target size:** `110-125` rooms.
**Primary feel:** too-clean Imperial order over an older corridor.
**Gameplay focus:** patrol combat, escort/disruption, travelers, checkpoint politics, documents, overland farming.

#### Subregions
- Outer milestone road
- Toll and checkpoint stations
- Relay hostel and courier yards
- Shrine pull-offs and dead camps
- Caravan sidings
- Survey field boundary zone

#### Content Targets
- `6-8` base mob families
- `2` elite variants
- `1-2` named encounters
- `10-14` field/story NPCs
- `6-8` patrol or traveler spawn sets

#### History Hooks
- roadbeds that do not match modern Imperial geometry
- re-cut milestones with erased prior text
- traveler registries that reveal disappearances
- old shrines folded into road maintenance sites

### 3. `old_causeway`

**Role:** Older corridor near the capital that the Empire repurposed rather than built.
**Target size:** `110-130` rooms.
**Primary feel:** unease, inheritance, repeating forms, ruin under repair.
**Gameplay focus:** salvage, secret routes, lore recovery, node-scar exploration, ambushes, hidden shrines.

#### Subregions
- broken paved segments
- collapsed arches and underpasses
- ruined waystations
- overgrown branch routes
- drained cistern or reservoir complex
- old boundary court or survey circle

#### Content Targets
- `6-7` base mob families
- `2-3` elite variants
- `2` named encounters
- `8-12` field/story NPCs
- hidden lore-heavy subareas

#### History Hooks
- plaques rewritten by later regimes
- repeated numeric/architectural patterns
- evidence of older state control predating the Empire
- node scars every few segments
- archival links back to Ministry Ward and Circle surveys

### 4. `ironvein_escarpment`

**Role:** The industrialized Imperial face of the Reth near the capital.
**Target size:** `115-130` rooms.
**Primary feel:** quarry violence, harsh ascent, extraction over sanctity.
**Gameplay focus:** ore farming, camp clearing, hard combat, labor politics, industrial hazards, shrine desecration.

#### Subregions
- switchback quarry road
- lower cut terraces
- lift towers and haul lines
- spoil fields and slag runoff
- prison labor encampments
- stripped mountain shrine belt

#### Content Targets
- `7-8` base mob families
- `2-3` elite variants
- `2` named encounters
- `10-15` field/story NPCs
- robust mining/gathering loops

#### History Hooks
- stone marked with removed shrine iconography
- quarry stamps and ministry requisitions
- records tying mountain extraction to capital building campaigns
- memorials to cave-ins or labor revolts
- evidence that sacred sites were intentionally repurposed

### 5. `stagcrown_preserve`

**Role:** Imperial hunting preserve and elite leisure forest outside the capital.
**Target size:** `110-130` rooms.
**Primary feel:** curated beauty masking cruelty and illicit trade.
**Gameplay focus:** hunting, hides, herbs, fishing pockets, ranger conflict, poacher traffic, noble questlines.

#### Subregions
- formal hunting gates
- managed game trails
- lodge grounds and noble camps
- poacher blinds and hidden meat lines
- lake or reservoir basin with fishing nodes
- old forest shrine or stone circle under preserve ownership

#### Content Targets
- `6-8` base mob families
- `2-3` elite variants
- `1-2` named encounters
- `10-16` field/story NPCs
- mixed legal/illegal resource loops

#### History Hooks
- preserve markers superimposed over older sacred boundaries
- hunting charter revisions tied to noble families
- poachers exposing what the official preserve story hides
- lake works that re-channel older water systems
- official ranger logs contradicting black-market trophy traffic

## History Tracking Framework

To make the history cohesive and followable across the whole pack, the same recurring systems should appear in all five zones.

### Repeating Institutions
- one major ministry cluster
- one or two noble houses with visible regional control
- one Dragon Corps command chain
- one extraction or contracting syndicate
- one hidden resistance logistics thread

### Repeating Physical Markers
- mile markers
- quarry stamps
- charter seals
- preserve boundary stones
- wardstones or sanctioned Circle markers
- bridge plates and culvert carvings

### Repeating Historical Events
- road rebuilding decrees
- quarry expansions
- hunting charter reforms
- district “restoration” campaigns
- labor suppressions or disappearances

### Contradictory Record Sources
- public monument text
- official ledger or registry
- local oral testimony
- contraband notes or smuggled copies

The same names, years, decrees, and houses should recur so the player can build a real mental model of the region.

## Quest and Narrative Density Contract

Every zone should contain:
- `1` major local questline
- `1` faction thread tied back to `varath_prime`
- `1` history chain that crosses at least one additional zone
- `1` smaller human-scale story cluster

### Suggested Cross-Zone Threads
- **Imperial Revision**
  Renaming, rebuilding, and claiming older sites.
- **Administrative Violence**
  Harm enacted through law, permits, quotas, transport, and custody.
- **Private Splendor / Public Rot**
  Elite comfort sustained by extraction and hidden coercion.
- **Inherited Ruin**
  The capital’s wealth rests on structures whose original meaning is obscured.

## Flight and Connectivity

### Flight
- `varath_prime` should contain the Hub 4 Dragon Courier platform.
- Exterior zones should not each receive courier stops in the first pass.
- The city should function as the single aerial hub for this pack.

### Overland Connectivity
- `varath_prime` connects directly to all four exterior zones.
- Exterior zones may also interconnect where geography supports it, but the city remains the central navigation and service node.
- Hidden or faction-gated exits are encouraged where supported by `AreaBuilder`.

## Builder-Safe Authoring Guidelines

### Required Authoring Shape
- explicit room declarations
- explicit exits
- explicit spawn declarations
- explicit mob placements where patrols or scripted ambient populations require them
- explicit NPC placement
- explicit gathering pool declarations for harvest/fishing loops
- explicit item declarations for any zone-local catalog additions
- explicit lore fragment placement
- explicit materials and quest declarations

### Avoid
- inline custom helper generators that emit content invisibly
- bespoke runtime-only data structures not mirrored in serializer expectations
- hidden content generation loops that the builder app cannot reconstruct
- narrative encoded only in comments instead of content objects
- helper wrappers around `area.room(...)`, `area.exit(...)`, `area.spawn(...)`, and other DSL methods
- computed `zone_id` or computed `room_id` values
- abstractions that prevent the AST parser from seeing literal DSL method calls and their arguments

### Preferred Pattern
Large zones may still use section comments and district-based grouping, matching the existing authored style in:
- `world/areas/vaels_crossing.py`
- `world/areas/cantera_edge.py`

## Zone Naming and Identity Summary

| Zone ID | Function | Identity |
|---|---|---|
| `varath_prime` | hub city | imperial capital built over older scars |
| `crownroad_north` | overland artery | logistics, checkpoints, disappearance by paperwork |
| `old_causeway` | ancient corridor | inherited roadwork, repeating forms, salvage and unease |
| `ironvein_escarpment` | mountain extraction zone | quarry violence, shrine stripping, industrial control |
| `stagcrown_preserve` | hunting forest zone | elite leisure, poaching, enclosure, lake-side resource play |

## Success Criteria

The pack is successful when:
- `varath_prime` can support long-form city play without feeling like a corridor hub.
- each exterior zone feels mechanically and narratively distinct.
- players can track coherent regional history across all five zones.
- the capital region clearly expresses Imperial power without collapsing into one-note militarism.
- dragon-adjacent content stays within the no-hint rule.
- authored files remain cleanly compatible with the AreaBuilder/builder app workflow.

## Implementation Notes for the Future Plan
- Build the city zone first because it defines institutions, exits, and the history vocabulary the exterior zones should echo.
- Author the exterior zones in the order that best establishes the region’s historical lexicon:
  1. `varath_prime`
  2. `crownroad_north`
  3. `old_causeway`
  4. `ironvein_escarpment`
  5. `stagcrown_preserve`
- Add the Hub 4 flight point in the city zone once the city layout is stable enough to define a permanent courier platform room.
