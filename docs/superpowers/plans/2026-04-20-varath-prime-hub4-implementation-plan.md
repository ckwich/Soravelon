# Varath Prime Hub 4 Implementation Plan

**Date:** 2026-04-20
**Depends on:** `docs/superpowers/specs/2026-04-20-varath-prime-hub4-design.md`

## Goal
Author a complete Hub 4 capital-region content pack in builder-safe `AreaBuilder` format:

- `varath_prime` as one unified city zone with all districts inside the same area file
- four exterior land-based zones connected to the city:
  - `crownroad_north`
  - `old_causeway`
  - `ironvein_escarpment`
  - `stagcrown_preserve`

The pack must be rich enough to feel like a real regional hub on first ship:

- city zone: `150-180` rooms
- each exterior zone: `110-130` rooms
- strong service coverage, quest density, mob density, and gathering loops
- no narrative hints that dragons are intelligent behind the curse
- full compatibility with the Soravelon builder app and the strict sidecar AST parser

## Primary Deliverables

### New area files
- `world/areas/varath_prime.py`
- `world/areas/crownroad_north.py`
- `world/areas/old_causeway.py`
- `world/areas/ironvein_escarpment.py`
- `world/areas/stagcrown_preserve.py`

### Likely supporting file changes
- `world/mob_templates.py`
  - add new hostile families, elite variants, and named encounters used by the five Hub 4 zones
- `world/areas/equipment_catalog.py`
  - only if we decide shared reusable gear belongs in the central catalog instead of zone-local `area.item(...)`
- `tests/test_content_integration.py`
  - add import/callability coverage for the five new zone files
- `tests/test_area_builder.py`
  - add focused smoke coverage for new flight wiring and selected cross-zone exit expectations if needed

### Runtime content targets
- one new Hub 4 flight stop in `varath_prime`
- at least one real Dragon Courier route connecting `varath_prime` to the existing `vaels_crossing_courier` stop
- city services, spawn tags, gathering pools, named mobs, lore fragments, and quest chains all present in first pass

## Hard Authoring Rules

### Builder / parser safety
- Use `area = AreaBuilder("zone_id")` with a literal snake_case zone id.
- Use direct local assignments for rooms: `room_var = area.room("room_id", ...)`.
- Use direct `area.method(...)` calls for all DSL authoring.
- Do not hide room/exits/spawns/NPCs behind helpers, wrappers, loops, or factories.
- Keep room IDs stable, short, and district/subregion-prefixed.
- Use direct room variables or literal `"zone_id:room_id"` strings for exits.
- Keep payloads literal and JSON-like in spirit so the builder sidecar can parse and reserialize them.

### Runtime / validator safety
- Use only valid `zone_type`, `continent`, `room_type`, and exit direction values supported by `world/area_validator.py`.
- Do not use unsupported `spawn_condition` strings.
- Keep city districts in one zone file. No intra-city districts split across multiple areas.
- Reserve `mob()` for authored persistent mob objects where patrols or set-piece placement need them.
- Use `spawn()` for ordinary runtime-managed hostile population.
- Use `gathering_pool()` for harvest/fishing loops.
- Add `greeter_room` / `respawn_point` tags manually where needed.

### Narrative safety
- Nothing implies dragons are secretly lucid, remembering, plotting, or communicating behind the curse.
- Uncanniness should attach to institutions, ruins, roads, geometry, bureaucracy, state violence, and inherited sites.
- Every zone must expose the same regional history from a different angle.

## Shared Content Spine

Before room-by-room authoring starts, lock a small recurring regional vocabulary and reuse it across all five zones.

### Shared institutions
- one roads/logistics ministry office and its field bureaucracy
- one records/charter office and its archival paper trail
- one Dragon Corps regional command chain
- one Circle survey/containment presence
- one extraction contractor or haul syndicate
- one hidden resistance logistics network

### Shared historical traces
- reused decree years
- repeated quarry or charter seals
- repeating milestone or culvert markings
- identical survey phrasing on plaques and ledgers
- contradictory public inscription versus private records

### Shared naming packet
This should be authored first and then reused consistently:

- `2` major noble houses
- `1` ministry title
- `1` contractor/syndicate name
- `1` resistance cell name
- `1` Dragon Corps command banner / command title

If a name is introduced in `varath_prime`, it should reappear in at least `2` exterior zones.

## Room ID and Layout Conventions

Use stable prefixes so the builder and future editors can navigate the files quickly.

### City convention
- `ca_` Crown Approach
- `oc_` Outer Commons
- `mw_` Ministry Ward
- `mq_` Martial Quarter
- `dc_` Dragon Corps Enclave
- `cd_` Circle District
- `nh_` Noble Heights
- `hw_` Hidden Warrens

### Exterior convention
- each zone gets `4-6` subregion prefixes
- each subregion gets a main spine, side loops, hidden pocket, and service/story anchor rooms

### Exit discipline
- keep the main traversal graph readable
- prefer clear spines with lateral loops over dense maze design
- hidden exits should be rare and intentional
- cross-zone exits should cluster at obvious boundary rooms and named gates/roads

## Zone-by-Zone Build Plan

## 1. `varath_prime`

### Zone role
Hub city for Hub 4. It defines the region’s institutional language, flight access, service economy, and the public version of history.

### Target budget
- `160` rooms target
- `45-60` static/service/story NPCs
- `20-30` ambient or patrol NPCs
- `3-5` hostile pockets
- `3-4` major quest hubs

### District room budgets
- Crown Approach: `18`
- Outer Commons: `26`
- Ministry Ward: `22`
- Martial Quarter: `20`
- Dragon Corps Enclave: `18`
- Circle District: `18`
- Noble Heights: `20`
- Hidden Warrens: `18`

### Required city anchors
- city arrival / gate complex
- greeter room
- respawn-safe room
- bank
- medic
- inn / lodging
- vendor cluster
- crafting cluster
- faction/guild touchpoints
- Dragon Courier platform
- at least `4` overland gate exits, one toward each exterior zone

### City service and faction placement
- Outer Commons: practical services, lower-cost lodging, public commerce
- Ministry Ward: records, permits, seal offices, confiscation/archive quest hooks
- Martial Quarter: guard, logistics, officer chains, training grounds
- Dragon Corps Enclave: courier platform, handlers, tack depots, restricted holding spaces
- Circle District: magical services, sanctioned labs, sealed archives, research quests
- Noble Heights: patron quests, private guards, preserve and quarry patronage
- Hidden Warrens: smugglers, resistance cells, illicit fixers, hostile dens

### City hostile pockets
- sealed Ministry cellar or records vault
- Hidden Warrens gang pocket
- restricted Dragon Corps service tunnels or holding pens
- Circle undercroft or abandoned laboratory wing

### City quest hubs
- Ministry records / disappearance-by-paperwork questline
- Corps logistics / courier clearance questline
- Noble patronage / preserve charter questline
- Hidden Warrens resistance / contraband ledgers questline

### City lore duties
- introduce the official state narrative
- seed contradictions through plaques, ledgers, seal walls, confiscation records, and whispered accounts
- establish the repeated dates, families, offices, and decrees used by the whole pack

### Flight content
- add a Hub 4 city flight point, likely in the Dragon Corps Enclave
- add a route between the new city stop and `vaels_crossing_courier`
- do not add separate exterior flight stops in first pass

## 2. `crownroad_north`

### Zone role
The capital’s overland artery: logistics, checkpoints, relays, document traffic, and controlled movement.

### Target budget
- `116` rooms target
- `6-8` hostile families
- `2` elite variants
- `1-2` named encounters
- `10-14` field/story NPCs
- `6-8` patrol/traveler spawn sets

### Subregion room budgets
- outer milestones: `22`
- checkpoint chain: `20`
- relay hostel yards: `18`
- shrine pull-offs and dead camps: `18`
- caravan sidings: `18`
- survey fields / boundary strip: `20`

### Core play loops
- escort disruption
- checkpoint bribery and permit recovery
- early farming against roadbandits, carrion beasts, and deserter pockets
- document chain quests that tie directly back to Ministry Ward

### Hostile population plan
- roadside brigands
- deserter cells
- dust hounds or road scavengers
- carrion birds / pack hunters
- toll extortionists or rogue levy crews
- shrine scavengers

### Named encounter slots
- a checkpoint captain running a private extraction racket
- a roadbandit leader or “missing” registrar whose records do not match the official story

### Gathering plan
- roadside herbs
- milestone scrap / salvage
- limited skinning or scavenger hides

### Narrative duties
- show administrative violence through transit law
- expose disappearances via traveler logs, manifests, and registry books
- repeat the same decrees and seal language seen in the city

## 3. `old_causeway`

### Zone role
The older corridor the Empire renamed but did not truly author. This is the pack’s strongest “inherited ruin” zone.

### Target budget
- `118` rooms target
- `6-7` hostile families
- `2-3` elite variants
- `2` named encounters
- `8-12` field/story NPCs
- multiple hidden subareas and lore pockets

### Subregion room budgets
- broken causeway spine: `24`
- collapsed arches: `20`
- ruined waystations: `18`
- overgrown branch routes: `20`
- drained reservoir / cistern works: `18`
- survey circle / old court: `18`

### Core play loops
- salvage routes
- hidden-path navigation
- lore fragment discovery
- ambush pockets and side-path elites
- archival follow-up from Ministry Ward and Circle District

### Hostile population plan
- causeway scavengers
- culvert lurkers
- swarm or nest enemies in collapsed masonry
- salvager cutthroats
- feral beasts nesting in old chambers
- shrine or culvert guardians if the tone supports them

### Named encounter slots
- a vanished surveyor or archivist who became the zone’s trackable mystery
- a hidden-route set-piece guardian in the reservoir or arch complex

### Gathering plan
- salvage stone / broken fittings
- wet-grown herbs
- rare mineral residue in reservoir chambers

### Narrative duties
- make repeating geometry and numbering feel deliberate
- prove the Empire inherited, revised, and partially misunderstood the corridor
- tie records back to both Ministry Ward and Circle District

## 4. `ironvein_escarpment`

### Zone role
Capital-adjacent extraction zone where the city’s wealth becomes visibly violent.

### Target budget
- `120` rooms target
- `7-8` hostile families
- `2-3` elite variants
- `2` named encounters
- `10-15` field/story NPCs
- strongest ore / stone loop in the pack

### Subregion room budgets
- switchback approach road: `20`
- lower cut terraces: `22`
- lift towers and haul lines: `18`
- spoil fields / runoff: `18`
- labor encampments: `20`
- stripped shrine belt: `22`

### Core play loops
- ore and stone gathering
- hard combat farming
- camp clearing
- labor records and memorial discovery
- shrine desecration narrative chain

### Hostile population plan
- quarry thugs
- forced-labor overseers
- cliff predators or scavengers
- slag hounds / quarry beasts
- tunnel or cut-face nest enemies
- shrine scavengers / relic raiders

### Named encounter slots
- a quarry foreman or contractor enforcer tied to the capital’s noble or ministry interests
- a shrine-belt elite guarding a scarred sacred site

### Gathering plan
- ore
- stone
- industrial salvage
- sparse herbs in runoff or cliff edge niches

### Narrative duties
- connect capital building campaigns directly to quarry extraction
- show memorialization, erasure, and labor suppression side by side
- reuse named houses, offices, requisition years, and seal language from the city

## 5. `stagcrown_preserve`

### Zone role
Elite preserve outside the capital where leisure, enclosure, trophy culture, poaching, and class hypocrisy collide.

### Target budget
- `118` rooms target
- `6-8` hostile families
- `2-3` elite variants
- `1-2` named encounters
- `10-16` field/story NPCs
- mixed hunting, herb, and fishing loops

### Subregion room budgets
- formal hunting gates: `18`
- managed game trails: `24`
- lodge grounds and noble camps: `18`
- poacher blinds and hidden meat lines: `20`
- lake basin / reservoir edge: `18`
- stone-circle woods: `20`

### Core play loops
- hides and skins
- herbal gathering
- fishing around the lake basin
- ranger versus poacher quest chains
- noble patronage and trophy paperwork

### Hostile population plan
- preserve wolves or hounds
- boars / dangerous game
- poacher crews
- trophy hunters or illegal camp guards
- ambush predators near the lake or woods
- ranger-aligned or poacher-aligned conflict pockets

### Named encounter slots
- a preserve alpha beast or legendary stag
- a poacher chief, trophy broker, or disgraced ranger

### Gathering plan
- hides
- herbs
- fish
- trophy salvage or rare preserve materials

### Narrative duties
- show preserve law as class privilege
- place charter stones over older sacred or communal boundaries
- connect noble leisure directly to city politics and black-market traffic

## Shared Content Production Plan

## A. Naming and continuity packet
Create first and keep beside the implementation work:

- recurring houses
- offices
- decrees
- survey years
- contractor markings
- resistance code phrases

This packet prevents late-stage drift and keeps the history trackable.

## B. Mob template expansion
Before or during zone authoring, add the hostile families needed across the pack.

### Recommended template counts
- `5-7` city-specific hostile or restricted templates
- `6-8` templates per exterior zone
- `1-2` named templates or named encounter definitions per exterior zone

### Authoring split
- reusable creature or humanoid archetypes belong in `world/mob_templates.py`
- exact placement and distribution live in the owning area file

## C. Item and material strategy
- shared reusable gear/consumables can live in `equipment_catalog.py`
- zone-specific trophies, paperwork props, preserve loot, or quest items can live in the owning area file with `area.item(...)`
- avoid scattering near-identical reusable equipment across multiple zone files

## D. Quest structure
Every zone should ship with:
- `1` main local questline
- `1` faction/institution line that reaches back to `varath_prime`
- `1` history thread crossing at least one adjacent zone
- `1` small human story cluster

## Execution Sequence

## Wave 0: continuity prework
- finalize recurring names, decree years, and institutions
- define room-id prefix map for all five zones
- define city flight point ID and exact route target to `vaels_crossing_courier`
- decide which shared items belong in `equipment_catalog.py` versus zone-local item defs
- decide which mob families can be shared across multiple Hub 4 zones

## Wave 1: `varath_prime` structural skeleton
- create zone metadata and all district blocks
- build main arteries and district anchors first
- wire greeter/respawn tags
- wire the `4` exterior exits
- add city flight point and Vael route
- add service NPC anchors and first pass lore anchors

### Wave 1 gate
- file imports cleanly
- build function callable
- no validator-invalid room types or directions
- no unresolved intra-pack exit targets once companion zones exist

## Wave 2: `varath_prime` content fill
- finish district side loops and hidden pockets
- add faction quest hubs
- add patrol-capable `mob()` placements only where needed
- add lore fragments, ledgers, plaques, decree walls, and hidden testimony threads
- add city hostile pockets

## Wave 3: `crownroad_north`
- establish the approach spine from city gate to far boundary
- add checkpoints, relay yards, shrine pull-offs, and survey field boundary
- add population mix, gathering pools, named encounter, and registry quests

## Wave 4: `old_causeway`
- establish the broken corridor backbone
- add branch loops, arches, cistern/reservoir, and hidden survey spaces
- add salvage routes, lore fragments, and deeper contradiction records

## Wave 5: `ironvein_escarpment`
- establish switchback road and terrace progression
- add quarry extraction loops, labor sites, and shrine belt
- add the harshest farming and industrial storytelling in the pack

## Wave 6: `stagcrown_preserve`
- establish preserve access law, game trails, lodge cluster, poacher lines, and lake basin
- add hunting, herb, and fishing loops
- add noble charter and black-market contradiction content

## Wave 7: pack polish
- tighten cross-zone continuity
- verify repeated names/dates/offices appear intentionally across zones
- rebalance any zone that over-indexes on one enemy family or one type of story beat
- ensure each exterior zone feels mechanically distinct from the others

## Verification Plan

### During authoring
- import each zone module after creation
- keep each zone file parser-safe for the builder sidecar
- validate no unsupported `spawn_condition` strings are introduced
- keep room IDs and exit targets stable as soon as they are referenced by another zone

### Repo tests to update or add
- extend `tests/test_content_integration.py` to import the five new zone modules
- add callable `build()` coverage for each new file
- add at least one focused flight integration test or smoke assertion for the new Hub 4 stop/route
- add any area-builder smoke assertions needed for major cross-zone exits

### Runtime verification after implementation
- `python scripts/smoke_start.py`
- focused canonical tests for content integration and area builder
- server startup with all new zones loaded
- second-pass cross-zone exit reconciliation reports zero unresolved exits inside the Hub 4 pack
- `fly` lists the new city route once the player has discovered the stops

### Builder verification
After each zone file is authored, parse it through the builder sidecar parser in `C:\\Dev\\Sora_builder\\sidecar\\area_parser.py`.

Success criteria for parser verification:
- no `UnsupportedAreaConstructError`
- zone model includes all expected rooms/exits/spawns/NPCs/flight data
- file can be reserialized without structural loss

## Risks and Mitigations

### Risk: city scope balloons
Mitigation:
- ship the city from district anchors outward
- keep each district to its room budget
- do not add new districts beyond the approved eight

### Risk: exterior zones become mechanically redundant
Mitigation:
- lock one primary farming identity per zone
- lock one primary narrative identity per zone
- review enemy families for overlap before authoring named encounters

### Risk: builder round-trip breaks
Mitigation:
- keep source strictly literal and parser-visible
- validate with the sidecar parser after each file, not at the end

### Risk: history becomes broad but untrackable
Mitigation:
- reuse the same names, dates, and decrees across multiple zones
- maintain a continuity sheet during authoring

## Definition of Done

This plan is complete when:

- all five area files exist and load cleanly
- the city is one coherent zone, not split across files
- each exterior zone exceeds `100` rooms and has distinct combat/gathering/narrative identity
- the Hub 4 city flight stop exists and connects into the live courier network
- shared history is visible and trackable across all five zones
- builder parser validation succeeds for every new area file
- startup/test smoke passes with the new content in place
