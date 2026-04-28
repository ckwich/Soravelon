# Tremen And The Tremeneth Hub 3 Design

Date: 2026-04-27

Status: approved direction, design spec before implementation planning

## Goal

Build a Hub 3 content pack centered on Tremen, the half-dwarf city carved into
the Tremeneth Mountains. The pack should match the quality bar established by
Hub 4 and Hub 5: rich history, meaningful quests, fair itemization, intentional
combat loops, practical gathering, and strict builder-safe AreaBuilder DSL.

The intended implementation boundary is one hub city plus four immediately
connected exterior zones, each at least 100 rooms:

- `tremen`
- `greyteeth_lower_passes`
- `tremeneth_high_passes`
- `tremeneth_deep_mines`
- `tremeneth_underhalls`

## Source Basis

This spec is based on:

- `AGENTS.md`
- `CLAUDE.md`
- `C:\Obsidian\brain\Soravelon\soravelon-areaspec.md`
- `C:\Obsidian\brain\Soravelon\Soravelon_World_Bible.md`
- `C:\Obsidian\brain\Soravelon\soravelon.md`
- `C:\Obsidian\brain\Soravelon\soravelon-crafting.md`
- `C:\Obsidian\brain\Soravelon\soravelon-guilds.md`
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md`
- `C:\Obsidian\brain\Soravelon\soravelon-quests.md`
- `C:\Obsidian\brain\Soravelon\soravelon-room-state.md`
- Existing live continuity in `world/areas/reth_foothills.py`
- Existing Hub 4 and Hub 5 area/spec/test patterns
- Engram context for Hub 5 validation and Tremen prep

## Geography Decision

There is a source conflict that must be resolved explicitly before authoring:

- `soravelon-areaspec.md` labels Hub 3 as "Korrath Mountains" and lists several
  `korrath_*` zone IDs.
- `Soravelon_World_Bible.md` says Tremen is in The Reth/Tremeneth Mountains on
  Varath, and says Korrath is a western Sorath mountain range.
- Existing live content in `reth_foothills.py` already supports the World Bible
  framing: The Reth is Varath's north-south mountain spine, the local peaks are
  the Greyteeth, and Tremen lies north in those peaks.

Binding decision for this pack:

- Tremen is in the Tremeneth Mountains, within the Reth/Greyteeth continuity.
- The Greyteeth is the local Tremen name for the surrounding range.
- Do not create new `korrath_*` zone IDs in this first implemented Tremen pack.
- If Korrath content is implemented later, treat it as Sorath/western-continent
  content unless the world bible is revised.

## Binding Guardrails

- Use strict literal AreaBuilder DSL only. No helper loops, factories, custom
  abstractions, or generated calls inside area files.
- No player-facing levels or level-gate language.
- No content may casually reveal or imply that dragons are intelligent beneath
  the curse.
- Node activity is visible and acknowledged in Hub 3, but nobody living truly
  understands how to repair nodes.
- Nodes are dramatic intensifiers, not the only source of interesting content.
- Basic quests may create NPC memory and character-scoped recognition, but not
  large permanent shared-world changes.
- Large world changes belong to later prerequisite-locked special event chains.
- Quests must carry meaning: story, relationship, exploration, world knowledge,
  play encouragement, or a practical route into new spaces.
- Delivery quests must guide players toward real places and discoveries.
- Combat loops must be grounded in local fiction, not random enemies wandering
  without reason.
- Half-dwarf culture should feel specific and lived-in without implementing a
  half-dwarf player ancestry unless that becomes an explicit separate scope.

## Pack Identity

This is the "old magic in worked stone" hub.

Tremen should contrast with both Varath Prime and Korahei:

- Varath Prime makes power official, polished, and surveilled.
- Korahei makes welcome communal, circular, and socially demanding.
- Tremen makes danger practical, old, and physically built into the mountain.

Tremeneth culture should feel like a civilization that stopped pretending the
mountain is ordinary generations ago. Residents do not treat node activity as a
rumor. They mark it, route around it, argue over it, mine near it, train for it,
and build traditions around not being surprised by it.

The pack should carry three history layers:

1. **Older-than-current-people stone**: patterned foundations, eightfold rooms,
   geometry that predates known Tremen construction, old node scars, and
   sealed underhall routes.
2. **Half-dwarf habitation and stewardship**: carved halls, watch-ledgers,
   patrol marks, forge law, resonance bells, family work-cords, and communal
   risk management.
3. **Imperial extraction and aftermath**: abandoned mine claims, broken
   requisition stamps, unsafe shafts, erased cave-in records, and unresolved
   political debt.

## Zone Lineup

### `tremen`

Role: Hub city.

Target size: 110-130 rooms.

Primary feel: carved dignity, practical caution, visible node discipline,
half-dwarf public life, old magic treated as daily infrastructure.

Core districts:

- Gate Teeth: main arrival ledges, weather checks, courier landing, and road
  notices from the lower passes.
- Bellcut Market: food, climbing gear, mining tools, lanterns, warm clothing,
  and pressure-cured mountain goods.
- Forgeheart: basic and advanced forge access, metalwork shops, repair halls,
  and masterwork aspiration without making drops worthless.
- Watch Houses: patrol boards, missing-route ledgers, rescue rosters, and
  practical mountain authority.
- Resonance Halls: node-watchers, Resonance guild contacts, bells that mark
  pressure shifts, and Scholar-friendly investigation hooks.
- Stone Commons: hearths, guest halls, family alcoves, and daily civic life.
- Underhall Gates: controlled entrances into lower stoneworks and older sealed
  passages.
- High Lift Courts: lift machinery, haul cages, winch crews, and routes toward
  high passes and mine approaches.

City services:

- Bank, inn/rest, healer, vendors, guild contacts, basic forge, advanced forge,
  alchemist bench, gathering tool vendors, mountain gear, and flight stop.
- Guild presence should include Resonance, Ironblood, Verdance, and Western
  Arcana, matching the Obsidian guild matrix.

City quest role:

- Teach Tremen etiquette and mountain safety.
- Route players to each exterior zone with fiction-backed reasons.
- Introduce node literacy without exposing dragon truths.
- Seed later long-form chains about underhall access, mine reclamation, and
  node stabilization.

### `greyteeth_lower_passes`

Role: First exterior approach and bridge from existing Reth Foothills
continuity.

Target size: 100-115 rooms.

Primary feel: cold road discipline, waystations, route markers, half-dwarf
warning signs, and the feeling that the mountain is already evaluating you.

Subregions:

- Rethward Arrival Track
- Lower Marker Road
- Bellpost Waystations
- Avalanche Shelters
- Goat Ledges
- Old Survey Pull-Offs
- Windcut Traverse
- Tremen Gate Approach

Gameplay focus:

- Travel literacy, weather danger, patrol assistance, rescue hooks, and early
  Tremen relationship building.
- Combat loops around ridge scavengers, coordinated predator packs, road
  bandits, and node-touched animals that make the route feel watched.
- Gathering should include herbs, stone, ore, hardy forage, and at least one
  fish pool where meltwater shelves or cold pools make fishing plausible.

Quest role:

- Primary outbound delivery/exploration route from Tremen.
- Delivery should make the player learn waystations, marker logic, and rescue
  etiquette, not just carry a parcel to a random NPC.

### `tremeneth_high_passes`

Role: Exposed patrol and ridge territory above the city.

Target size: 105-120 rooms.

Primary feel: brutal weather, disciplined patrols, old sites acknowledged but
guarded, and a sense of beauty that can kill the careless.

Subregions:

- Patrol Stair
- Storm Bells
- Ice-Shear Ridges
- Warden Cairns
- Druid-Guarded Stone
- Sky Bridges
- Thin-Air Shelters
- High Pass Overlook

Gameplay focus:

- Strong repeatable combat loops with local rationale: territorial ridge
  beasts, storm-driven migrations, loose constructs or echoes near old stone,
  and dangerous patrol rescues.
- Warden and Druid presence should be understandable but guarded. They protect
  old sites and node knowledge, but they do not flatten into exposition
  machines.
- Gathering should emphasize cold-infused durability materials, wind herbs,
  high stone, bird/feather drops, and snowmelt fishing only where geography
  supports it.

Quest role:

- Teach the player that visible node activity is not the same as safety or
  mastery.
- Provide a meaningful combat-practice route that feels like helping patrols
  and stabilizing travel rather than grinding mobs in a hallway.

### `tremeneth_deep_mines`

Role: Abandoned Imperial mines and contested resource zone.

Target size: 110-125 rooms.

Primary feel: pressure, debt, extraction scars, unsafe shafts, reclaimed
equipment, and something old that moved the mine layout out from under its
owners.

Subregions:

- Claim Gate
- Requisition Offices
- Lower Hoist
- Pressure Galleries
- Blackwater Sumps
- Broken Cart Runs
- Sealed Imperial Cut
- Old Resonance Seam

Gameplay focus:

- Mining-rich gathering and itemization.
- Repeatable combat loops around mine vermin, escaped constructs, salvage
  gangs, pressure-warped animals, and hazards left by Imperial abandonment.
- Mine-water fishing should exist in blackwater sump rooms or underground pools
  rather than being forced into every subregion.

Quest role:

- Tell a story about extraction, worker memory, half-dwarf reclamation, and
  whether old mine maps should be trusted.
- Route players into mining, salvage, pressure-material crafting, and the
  political memory of Empire without making the whole zone a lecture.

### `tremeneth_underhalls`

Role: Beneath-city cavern network and strongest mystery zone in the first pack.

Target size: 105-125 rooms.

Primary feel: familiar half-dwarf architecture gradually surrendering to older
stone, resonance phenomena, and carefully bounded awe.

Subregions:

- Underhall Gate
- Family Vault Walks
- Bell-Tuned Corridors
- Dry Cisterns
- Eightfold Junction
- Quiet Chasms
- Sealed Pattern Rooms
- Deep Listening Chamber

Gameplay focus:

- Exploration, lore fragments, node-adjacent mystery, and a combat loop rooted
  in guardians, cave ecology, and resonance-disturbed creatures.
- This zone may include a node center or node-adjacent configured site if the
  builder/runtime contract supports it cleanly.
- Fishing should exist only if water rooms make it believable, such as cisterns
  or underground streams.

Quest role:

- Seed a long prerequisite-locked chain about underhall access and old stone.
- The initial implementation should not permanently unlock a dungeon or make
  large world changes. It can mark the player as trusted, recover records, and
  open character-scoped narrative recognition.

## Quest Direction

The first pack should include roughly:

- 5-7 city quests in `tremen`
- 3-5 quests per exterior zone
- At least one multi-step chain with `next_quest_id` and
  `prerequisite_quests`
- No chain step should be startable mid-story

Recommended quest arcs:

1. **The Guest Bell**
   A city onboarding quest where the player learns Tremen guest protocol,
   weather boards, and how to read bell warnings. This should introduce
   `talk`, `ask`, and `tell` flows naturally.

2. **Waystation Marks**
   A delivery/exploration quest from Tremen into `greyteeth_lower_passes`.
   The delivery exists to teach route markers, shelters, and why Tremen people
   care about exact travel records.

3. **The Patrol That Counted Twice**
   A high-pass quest about an impossible patrol count during a node pulse. It
   should guide combat and investigation without stating hidden dragon truths.

4. **Requisition Dust**
   A mine quest about old Imperial paperwork that does not match the shafts.
   The player recovers records, tools, and testimony so Tremen NPCs remember
   what the Empire tried to make disappear.

5. **What The Bells Hear**
   A Resonance/Scholar-friendly underhall chain seed. The first steps should
   recover measurements and help a local watcher, not unlock a permanent shared
   dungeon.

6. **Stone Debt**
   A practical crafting/economy quest that introduces the advanced forge,
   pressure minerals, fair itemization, and material quality without turning
   masterwork gear into mandatory progression.

## Combat Direction

Every exterior zone should have dedicated repeatable combat loops that are easy
to find, fictionally justified, and not overcrowded.

Targets:

- City: mostly safe. If combat practice is included, it should be supervised,
  nonlethal training using passive/no-loot practice entities or a runtime-safe
  equivalent.
- Exterior zones: roughly 12-18 spawn anchors per 100 rooms, tuned by zone
  density and route shape.
- Named encounters: 1-2 per exterior zone where they support story.
- Hostiles should cluster around believable pressure points: avalanche paths,
  predator dens, abandoned shafts, salvage camps, old pattern rooms, and
  weather shelters.

No "random mobs for the sake of grind" rule:

- A creature should be present because it hunts there, nests there, was driven
  there, guards something, scavenges something, or has been affected by local
  node/world-state conditions.

## Gathering, Fishing, And Itemization

Every exterior zone should include material gathering. Fishing should be
included wherever water fiction supports it, including cold meltwater pools,
mine sumps, cistern streams, or underground lakes. Do not force fishing into
rooms where it reads absurdly.

Material identity:

- Mountain materials: dense, cold-infused, high durability.
- Underground materials: lightless, pressure-formed, high density.
- Node-enhanced materials: valuable risk/reward, not required for the zone to
  matter.
- Imperial mine salvage: useful, scarred, historically specific.

Likely material additions:

- `greyteeth_iron`
- `coldvein_stone`
- `pressure_quartz`
- `bellcap_mushroom`
- `windroot`
- `snowmelt_trout`
- `blackwater_char`
- `cavern_whitefish`
- `resonance_shard`
- `haul_rope_fiber`

Balancing principles:

- Hub 3 should introduce stronger durability/crafting identity without
  invalidating Hub 1, Hub 4, or Hub 5 materials.
- Masterwork gear remains slightly better than equivalent drops, not a runaway
  power tier.
- Vendor stock should be useful and zone-appropriate: climbing gear, cold
  weather supplies, mining tools, lanterns, repair kits, fishing rods, food,
  and practical weapons/armor appropriate to Tremen.

## NPC And Faction Direction

Tremen NPCs should feel direct, careful, and deeply used to the mountain. They
may be warm, but rarely ornamental. Their caution should feel earned.

Important NPC categories:

- Half-dwarf civic officials and watch captains
- Forge masters and repair clerks
- Bell-readers and resonance listeners
- Warden scouts
- Druid observers who choose words carefully
- Western Arcana contacts who study without Imperial posture
- Miners, lift crews, cooks, innkeepers, salvage witnesses, and traveling
  merchants

Faction posture:

- Resonance: at home here, practical and respected.
- Ironblood: credible in patrols, mine safety, and tactical protection.
- Verdance: present through Druid/Warden relationships, but not in control of
  the city.
- Western Arcana: scholarly, less Imperial than Varath Prime's Circle posture.
- Empire: present mostly as history, paperwork, debt, and mine scars, not as
  the controlling power of this first Tremen pack.

## Builder And Runtime Constraints

Area files must use explicit direct calls:

- `area.zone(...)`
- `area.room(...)`
- `area.exit(...)`
- `area.npc(...)`
- `area.quest(...)`
- `area.item(...)`
- `area.material(...)`
- `area.gathering_pool(...)`
- `area.spawn(...)`
- `area.named_mob(...)`
- `area.lore_fragment(...)`
- `area.flight_point(...)`
- `area.flight_route(...)`
- `area.node(...)` only where contract-safe

Do not use hidden helper loops or abstractions in authored area files. The
builder app must be able to parse and round-trip the content.

## Validation Expectations

Implementation should add focused tests before or alongside content:

- New `tests/test_tremen_hub3_contracts.py`
- Update `tests/test_area_gathering_contracts.py`
- Update `tests/test_content_integration.py`

The Tremen contract test should cover:

- Each zone imports and has callable `build()`.
- Each zone has at least 100 rooms.
- Required anchor rooms exist.
- Cross-zone exits are present and reciprocal.
- Exterior zones have adequate combat-loop density.
- Gathering pools reference registered materials and include fish pools where
  expected.
- Quest chains use `next_quest_id` plus matching `prerequisite_quests`.
- Quest consequences are specific, not generic copy/paste.
- Forbidden dragon-intelligence phrases do not appear.
- Player-facing text does not expose backend levels.
- Area files stay parser-safe with literal AreaBuilder DSL.

Recommended validation commands after implementation:

```powershell
python scripts/run_tests.py tests.test_tremen_hub3_contracts tests.test_area_gathering_contracts tests.test_content_integration.TestZoneImports tests.test_quest_engine tests.test_vendor_engine
python scripts/smoke_start.py
python -m py_compile world/areas/tremen.py world/areas/greyteeth_lower_passes.py world/areas/tremeneth_high_passes.py world/areas/tremeneth_deep_mines.py world/areas/tremeneth_underhalls.py
```

Also validate all five new files through the Sora Builder sidecar parse/validate
workflow before declaring the pack complete.

## Deferred Scope

Do not include these in the first overnight implementation unless explicitly
approved as a follow-up slice:

- Half-dwarf player ancestry implementation.
- Full permanent dungeon unlock.
- Major shared-world changes from routine quests.
- Korrath western-continent content.
- Caldenmere moving-city mechanics.
- New runtime node systems beyond contract-safe authored node metadata.

## Success Criteria

The pack is successful if:

- Tremen feels like a distinct Soravelon hub, not a generic dwarf city.
- The geography cleanly aligns with Reth/Tremeneth/Greyteeth continuity.
- Every quest has story, relationship, exploration, or gameplay purpose.
- Delivery quests guide players through meaningful spaces.
- Combat skill grinding is supported through believable local loops.
- Gathering and fishing are available where they make sense and are balanced
  against existing material tiers.
- The five zones are builder-safe, import-clean, contract-validated, and
  smoke-start clean.
