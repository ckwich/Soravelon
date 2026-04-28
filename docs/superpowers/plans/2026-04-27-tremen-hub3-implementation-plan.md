# Tremen Hub 3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the approved Tremen/Tremeneth Hub 3 five-zone pack, verify each zone as it lands, polish the full pack, run a golden-path audit, then complete a full-MUD launch-readiness audit.

**Architecture:** Content is authored as strict literal AreaBuilder DSL in five new area files. Runtime registries provide the materials and mob templates used by those files. Tests enforce parser safety, room counts, graph connectivity, quest logic, gathering/fishing coverage, importability, and narrative guardrails.

**Tech Stack:** Python, Evennia, Soravelon `AreaBuilder`, unittest via `python scripts/run_tests.py`, Sora Builder sidecar parse/validate, Engram MCP.

---

## Approved Scope

Implement these five zones:

- `world/areas/tremen.py`
- `world/areas/greyteeth_lower_passes.py`
- `world/areas/tremeneth_high_passes.py`
- `world/areas/tremeneth_deep_mines.py`
- `world/areas/tremeneth_underhalls.py`

Each zone must have at least 100 rooms and remain round-trippable through the
builder parser. The area files must contain direct literal calls such as
`area.room(...)`, `area.exit(...)`, `area.npc(...)`, `area.quest(...)`,
`area.material(...)`, and `area.gathering_pool(...)`. Do not hide content inside
loops, helper functions, factories, or custom abstractions in the area files.

## Binding Decisions From The Spec

- Tremen is a Tremeneth/Greyteeth/Reth hub on Varath.
- Do not create new `korrath_*` zone IDs in this pack.
- Korrath remains deferred western-continent content unless the World Bible is revised.
- Node activity is visible and acknowledged, but nobody living truly repairs nodes.
- No text may reveal or imply intelligent dragons beneath the curse.
- Routine quests use NPC memory and character-scoped recognition, not permanent shared-world changes.
- Delivery quests must route players to real places and teach exploration.
- Combat loops must be fiction-anchored.
- Fishing appears where water geography supports it, including meltwater pools, mine sumps, and underhall cisterns.

## Files To Create

- `world/areas/tremen.py`: hub city, services, vendors, flight stop, city quests.
- `world/areas/greyteeth_lower_passes.py`: approach route, waystations, gathering, combat, route quests.
- `world/areas/tremeneth_high_passes.py`: exposed high-pass patrol zone, storm/ridge combat loops, Warden/Druid tension.
- `world/areas/tremeneth_deep_mines.py`: abandoned Imperial mines, mining economy, pressure/blackwater content.
- `world/areas/tremeneth_underhalls.py`: beneath-city underhalls, node-adjacent mystery, prerequisite chain seed.
- `tests/test_tremen_hub3_contracts.py`: focused Hub 3 pack contract test.
- `docs/superpowers/plans/2026-04-27-tremen-hub3-golden-path-audit.md`: final player-journey audit report.
- `docs/superpowers/plans/2026-04-27-launch-readiness-audit.md`: full-MUD launch-readiness audit report.

## Files To Modify

- `world/material_definitions.py`: add Tremeneth material registry entries.
- `world/mob_templates.py`: add Tremeneth mob templates and named encounter templates.
- `tests/test_area_gathering_contracts.py`: add new zones and expected fishing zones.
- `tests/test_content_integration.py`: add import coverage for five new area modules.

## Commit Boundaries

1. Plan commit: this implementation plan only.
2. Contract/registry commit: tests, material registry, mob templates.
3. One commit per completed and verified zone.
4. Whole-pack polish/audit commit.
5. Launch-readiness report commit.

If unrelated dirty files remain in the working tree, stage only the files owned
by the current boundary.

---

### Task 1: Commit This Implementation Plan

**Files:**
- Create: `docs/superpowers/plans/2026-04-27-tremen-hub3-implementation-plan.md`

- [ ] **Step 1: Review the plan file for placeholders**

Run:

```powershell
Select-String -Path docs/superpowers/plans/2026-04-27-tremen-hub3-implementation-plan.md -Pattern 'TBD|TODO|placeholder|fill in|later' -CaseSensitive:$false
```

Expected: no actionable placeholder text.

- [ ] **Step 2: Stage only this plan**

Run:

```powershell
git add docs/superpowers/plans/2026-04-27-tremen-hub3-implementation-plan.md
git diff --cached --name-only
```

Expected: only `docs/superpowers/plans/2026-04-27-tremen-hub3-implementation-plan.md`.

- [ ] **Step 3: Commit the plan**

Run:

```powershell
git commit -m "docs: plan tremen hub three implementation"
```

Expected: commit succeeds.

- [ ] **Step 4: Log the plan to Engram**

Store a concise Engram checkpoint with key
`soravelon_tremen_hub3_implementation_plan_2026_04_27`, including the repo path,
commit hash, approved zone list, validation approach, and the next step.

---

### Task 2: Add Tremen Pack Contract Tests

**Files:**
- Create: `tests/test_tremen_hub3_contracts.py`
- Modify: `tests/test_area_gathering_contracts.py`
- Modify: `tests/test_content_integration.py`

- [ ] **Step 1: Create focused failing contract coverage**

Create `tests/test_tremen_hub3_contracts.py` by adapting the Hub 5 contract
parser with these Tremen constants:

```python
ZONE_FILES = {
    "tremen": ROOT / "world" / "areas" / "tremen.py",
    "greyteeth_lower_passes": ROOT / "world" / "areas" / "greyteeth_lower_passes.py",
    "tremeneth_high_passes": ROOT / "world" / "areas" / "tremeneth_high_passes.py",
    "tremeneth_deep_mines": ROOT / "world" / "areas" / "tremeneth_deep_mines.py",
    "tremeneth_underhalls": ROOT / "world" / "areas" / "tremeneth_underhalls.py",
}

START_ROOMS = {
    "tremen": "gt_gate_teeth",
    "greyteeth_lower_passes": "ra_rethward_arrival",
    "tremeneth_high_passes": "ps_patrol_stair",
    "tremeneth_deep_mines": "cg_claim_gate",
    "tremeneth_underhalls": "ug_underhall_gate",
}
```

Use these required cross-zone exits:

```python
EXPECTED_CROSS_ZONE_EXITS = {
    ("tremen", "gt_lower_gate", "south", "greyteeth_lower_passes:ra_rethward_arrival"),
    ("greyteeth_lower_passes", "tg_tremen_gate", "north", "tremen:gt_lower_gate"),
    ("tremen", "hl_high_lift", "up", "tremeneth_high_passes:ps_patrol_stair"),
    ("tremeneth_high_passes", "ps_patrol_stair", "down", "tremen:hl_high_lift"),
    ("tremen", "fh_mine_lift", "down", "tremeneth_deep_mines:cg_claim_gate"),
    ("tremeneth_deep_mines", "cg_claim_gate", "up", "tremen:fh_mine_lift"),
    ("tremen", "ug_underhall_gate", "down", "tremeneth_underhalls:ug_underhall_gate"),
    ("tremeneth_underhalls", "ug_underhall_gate", "up", "tremen:ug_underhall_gate"),
}
```

Include tests for:

- area files exist
- each zone has at least 100 rooms
- each zone has at least five substantial room-prefix subregions
- local graph reachability
- reciprocal local exits
- required cross-zone exits
- quest givers/objectives/rewards resolve to known authored entities
- routine quests have empty or absent `world_expression`
- reward `action_type` values exist in `world.action_vocabulary.ACTION_HANDLERS`
- chained quests use `next_quest_id` plus matching `prerequisite_quests`
- exterior combat-loop density meets minimums
- city has vendor NPCs and curated stock
- gathering pools exist and include expected categories
- quest consequences are specific and not repeated generic filler
- forbidden dragon-intelligence phrases are absent
- player-facing level language is absent

- [ ] **Step 2: Add new zones to gathering contract coverage**

Modify `tests/test_area_gathering_contracts.py`:

```python
ZONE_FILES.update({
    "tremen": ROOT / "world" / "areas" / "tremen.py",
    "greyteeth_lower_passes": ROOT / "world" / "areas" / "greyteeth_lower_passes.py",
    "tremeneth_high_passes": ROOT / "world" / "areas" / "tremeneth_high_passes.py",
    "tremeneth_deep_mines": ROOT / "world" / "areas" / "tremeneth_deep_mines.py",
    "tremeneth_underhalls": ROOT / "world" / "areas" / "tremeneth_underhalls.py",
})
FISHING_EXPECTED_ZONES.update({
    "greyteeth_lower_passes",
    "tremeneth_high_passes",
    "tremeneth_deep_mines",
    "tremeneth_underhalls",
})
```

Do not require city fishing in `tremen`; the hub city can sell gear and teach
fishing without forcing a city fishing pool.

- [ ] **Step 3: Add import coverage**

Modify `tests/test_content_integration.py` by adding explicit import tests for:

```python
from world.areas import tremen
from world.areas import greyteeth_lower_passes
from world.areas import tremeneth_high_passes
from world.areas import tremeneth_deep_mines
from world.areas import tremeneth_underhalls
```

Also add those modules to `test_all_zones_have_callable_build`.

- [ ] **Step 4: Run focused tests and confirm expected failure**

Run:

```powershell
python scripts/run_tests.py tests.test_tremen_hub3_contracts tests.test_area_gathering_contracts tests.test_content_integration.TestZoneImports
```

Expected: failures caused by missing new area files/materials/imports, not parser
errors in existing zones.

---

### Task 3: Add Runtime Registry Entries

**Files:**
- Modify: `world/material_definitions.py`
- Modify: `world/mob_templates.py`

- [ ] **Step 1: Add Tremeneth materials**

Add a new `# ===== Zone-specific materials (Hub 3: Tremeneth) =====` section to
`MATERIAL_REGISTRY` before the Hub 5 section. Include these entries with
categories matching the gathering pools:

```python
"greyteeth_iron": {"category": "ore", "tier": 2, "gathering_skill": "mining"},
"coldvein_stone": {"category": "ore", "tier": 2, "gathering_skill": "mining"},
"pressure_quartz": {"category": "ore", "tier": 3, "gathering_skill": "mining"},
"resonance_shard": {"category": "ore", "tier": 3, "gathering_skill": "mining"},
"windroot": {"category": "herb", "tier": 2, "gathering_skill": "herbalism"},
"bellcap_mushroom": {"category": "forage", "tier": 2, "gathering_skill": "foraging"},
"haul_rope_fiber": {"category": "forage", "tier": 1, "gathering_skill": "foraging"},
"snowmelt_trout": {"category": "fish", "tier": 2, "gathering_skill": "fishing"},
"blackwater_char": {"category": "fish", "tier": 3, "gathering_skill": "fishing"},
"cavern_whitefish": {"category": "fish", "tier": 2, "gathering_skill": "fishing"},
"ridgecat_pelt": {"category": "hide", "tier": 2, "gathering_skill": "skinning"},
"minevermin_hide": {"category": "hide", "tier": 1, "gathering_skill": "skinning"},
```

Each entry must include the full existing registry shape:
`display_name`, `category`, `tier`, `raw_form`, `processed_form`,
`gathering_skill`, `processing_skill`, `processing_station`, and `visibility`.

- [ ] **Step 2: Add Tremeneth mob templates**

Add templates to `MOB_TEMPLATES` for:

- `greyteeth_scavenger`
- `marker_bandit`
- `ridgecat`
- `stormgoat`
- `windcut_eagle`
- `loose_oreling`
- `minevermin`
- `claim_jumper`
- `haul_construct`
- `blackwater_eel`
- `underhall_skitter`
- `bell_echo`
- `pattern_guardian`
- `stone_listening_frame`

Use existing ability schemas from nearby templates. Keep stats roughly Hub 3:
stronger than starter mobs, not a flat HP-sponge jump. Give each mob a
fictional reason to exist through `desc`, `base_aggression`, `wander`, and
`is_hunter`.

- [ ] **Step 3: Validate registry-only changes**

Run:

```powershell
python scripts/run_tests.py tests.test_mob_templates tests.test_area_gathering_contracts
```

Expected: material registry test may still fail until area files exist, but
`tests.test_mob_templates` should pass.

---

### Task 4: Implement `tremen`

**Files:**
- Create: `world/areas/tremen.py`
- Test: `tests/test_tremen_hub3_contracts.py`

- [ ] **Step 1: Author the city zone**

Create an explicit literal AreaBuilder file with:

- `area = AreaBuilder("tremen")`
- `area.zone(name="Tremen", zone_type="city", continent="varath", hub_city=True, faction_territory="warden", faction_presence=[...])`
- 110-130 rooms across these prefixes:
  - `gt`: Gate Teeth
  - `bm`: Bellcut Market
  - `fh`: Forgeheart
  - `wh`: Watch Houses
  - `rh`: Resonance Halls
  - `sc`: Stone Commons
  - `ug`: Underhall Gates
  - `hl`: High Lift Courts
- Required anchors:
  - `gt_gate_teeth`
  - `gt_lower_gate`
  - `hl_high_lift`
  - `fh_mine_lift`
  - `ug_underhall_gate`
  - `bm_bellcut_market`
  - `fh_advanced_forge`
  - `rh_listening_bells`

Use direct local variables:

```python
gt_gate_teeth = area.room("gt_gate_teeth", name="Gate Teeth", desc=(...), room_type="path", indoor=False)
```

Do not use room-generation loops.

- [ ] **Step 2: Add city NPCs and vendors**

Add at least 12 NPCs, including:

- arrival official
- market quartermaster
- forge master
- watch captain
- resonance listener
- underhall archivist
- lift forewoman
- healer
- innkeeper
- bank clerk
- Western Arcana scholar
- Warden scout

At least 4 vendor NPCs must have `vendor_item_ids` lists for mountain gear,
tools, food, medicine, and practical equipment.

- [ ] **Step 3: Add city quests**

Add 6 city quests:

- `tre_q_guest_bell`
- `tre_q_waystation_marks`
- `tre_q_stone_debt`
- `tre_q_bell_weather`
- `tre_q_underhall_measure`
- `tre_q_mine_reckoning`

Each quest must have a real giver, meaningful description, valid objectives,
specific consequence text, empty/absent `world_expression`, and rewards using
valid action vocabulary.

- [ ] **Step 4: Add city services and travel anchors**

Add `area.flight_point(...)` for Tremen and a route back to an existing major
hub where contract-safe. Cross-zone exits must connect from city anchors to the
four exterior zones using the expected tuples in Task 2.

- [ ] **Step 5: Verify city slice**

Run:

```powershell
python -m py_compile world/areas/tremen.py
python scripts/run_tests.py tests.test_tremen_hub3_contracts tests.test_content_integration.TestZoneImports
```

Expected: city-specific checks pass; missing exterior files may still fail if
the test suite expects all five files. If needed, run the exact failing test
names that only cover `tremen` until all five area files exist.

- [ ] **Step 6: Commit city slice**

Stage only `world/areas/tremen.py` plus test changes that are already needed
for the pack and commit:

```powershell
git commit -m "feat: add tremen hub city"
```

---

### Task 5: Implement `greyteeth_lower_passes`

**Files:**
- Create: `world/areas/greyteeth_lower_passes.py`
- Test: `tests/test_tremen_hub3_contracts.py`

- [ ] **Step 1: Author 100-115 rooms**

Use explicit room calls across:

- `ra`: Rethward Arrival Track
- `lm`: Lower Marker Road
- `bw`: Bellpost Waystations
- `as`: Avalanche Shelters
- `gl`: Goat Ledges
- `sp`: Survey Pull-Offs
- `wt`: Windcut Traverse
- `tg`: Tremen Gate Approach

Required anchors:

- `ra_rethward_arrival`
- `lm_first_marker`
- `bw_bellpost_waystation`
- `as_avalanche_shelter`
- `wt_windcut_turn`
- `tg_tremen_gate`

- [ ] **Step 2: Add combat and gathering**

Add 12-16 spawn anchors using `greyteeth_scavenger`, `marker_bandit`,
`ridgecat`, and `windcut_eagle`. Add gathering pools for ore, herb, forage,
hide, and fish. Fish rooms should be cold pools or meltwater shelves.

- [ ] **Step 3: Add quests**

Add 3-4 quests centered on waystation marks, missing travelers, marker repair,
and learning Tremen route etiquette. Ensure any delivery objective points to a
real waystation/marker/arrival NPC and teaches the route.

- [ ] **Step 4: Verify lower passes**

Run:

```powershell
python -m py_compile world/areas/greyteeth_lower_passes.py
python scripts/run_tests.py tests.test_tremen_hub3_contracts tests.test_area_gathering_contracts
```

Expected: lower-pass room, graph, combat, material, fishing, and quest checks
pass for this zone.

- [ ] **Step 5: Commit lower passes**

```powershell
git add world/areas/greyteeth_lower_passes.py tests/test_tremen_hub3_contracts.py tests/test_area_gathering_contracts.py tests/test_content_integration.py world/material_definitions.py world/mob_templates.py
git commit -m "feat: add greyteeth lower passes"
```

---

### Task 6: Implement `tremeneth_high_passes`

**Files:**
- Create: `world/areas/tremeneth_high_passes.py`

- [ ] **Step 1: Author 105-120 rooms**

Use explicit room calls across:

- `ps`: Patrol Stair
- `sb`: Storm Bells
- `ir`: Ice-Shear Ridges
- `wc`: Warden Cairns
- `dg`: Druid-Guarded Stone
- `sk`: Sky Bridges
- `ts`: Thin-Air Shelters
- `ho`: High Overlook

Required anchors:

- `ps_patrol_stair`
- `sb_storm_bells`
- `wc_warden_cairn`
- `dg_guarded_stone`
- `sk_sky_bridge`
- `ho_high_overlook`

- [ ] **Step 2: Add combat and gathering**

Add 12-18 spawn anchors using `ridgecat`, `stormgoat`, `windcut_eagle`,
`loose_oreling`, and `stone_listening_frame` where appropriate. Add ore, herb,
forage, hide, and fish pools. Fish pools should use snowmelt pools or storm-fed
basins, not dry ridge rooms.

- [ ] **Step 3: Add quests**

Add 3-5 quests about patrol counts, storm bells, Warden/Druid guarded sites,
and ridge rescue. At least one quest should route back to Tremen with a report
or measurements so city NPC memory deepens.

- [ ] **Step 4: Verify high passes**

Run:

```powershell
python -m py_compile world/areas/tremeneth_high_passes.py
python scripts/run_tests.py tests.test_tremen_hub3_contracts tests.test_area_gathering_contracts
```

Expected: high-pass checks pass.

- [ ] **Step 5: Commit high passes**

```powershell
git add world/areas/tremeneth_high_passes.py tests world/material_definitions.py world/mob_templates.py
git commit -m "feat: add tremeneth high passes"
```

---

### Task 7: Implement `tremeneth_deep_mines`

**Files:**
- Create: `world/areas/tremeneth_deep_mines.py`

- [ ] **Step 1: Author 110-125 rooms**

Use explicit room calls across:

- `cg`: Claim Gate
- `ro`: Requisition Offices
- `lh`: Lower Hoist
- `pg`: Pressure Galleries
- `bs`: Blackwater Sumps
- `bc`: Broken Cart Runs
- `si`: Sealed Imperial Cut
- `rs`: Old Resonance Seam

Required anchors:

- `cg_claim_gate`
- `ro_requisition_office`
- `lh_lower_hoist`
- `pg_pressure_gallery`
- `bs_blackwater_sump`
- `rs_resonance_seam`

- [ ] **Step 2: Add combat and gathering**

Add 14-18 spawn anchors using `minevermin`, `claim_jumper`,
`haul_construct`, `loose_oreling`, and `blackwater_eel`. Add strong ore pools,
forage pools, hide pools, and fish pools in sump/water rooms.

- [ ] **Step 3: Add quests**

Add 4-5 quests about old Imperial requisitions, mine safety, pressure material
crafting, salvage testimony, and a mine-to-underhall mystery seed. Ensure
political history comes through evidence and NPC memory rather than exposition
dumps.

- [ ] **Step 4: Verify deep mines**

Run:

```powershell
python -m py_compile world/areas/tremeneth_deep_mines.py
python scripts/run_tests.py tests.test_tremen_hub3_contracts tests.test_area_gathering_contracts
```

Expected: mine checks pass.

- [ ] **Step 5: Commit deep mines**

```powershell
git add world/areas/tremeneth_deep_mines.py tests world/material_definitions.py world/mob_templates.py
git commit -m "feat: add tremeneth deep mines"
```

---

### Task 8: Implement `tremeneth_underhalls`

**Files:**
- Create: `world/areas/tremeneth_underhalls.py`

- [ ] **Step 1: Author 105-125 rooms**

Use explicit room calls across:

- `ug`: Underhall Gate
- `fv`: Family Vault Walks
- `bc`: Bell-Tuned Corridors
- `dc`: Dry Cisterns
- `ej`: Eightfold Junction
- `qc`: Quiet Chasms
- `sp`: Sealed Pattern Rooms
- `dl`: Deep Listening Chamber

Required anchors:

- `ug_underhall_gate`
- `fv_family_vault_walk`
- `bc_bell_tuned_corridor`
- `dc_dry_cistern`
- `ej_eightfold_junction`
- `dl_deep_listening_chamber`

- [ ] **Step 2: Add combat, lore, gathering, and node-adjacent content**

Add 12-16 spawn anchors using `underhall_skitter`, `bell_echo`,
`pattern_guardian`, `loose_oreling`, and `stone_listening_frame`. Add lore
fragments that preserve mystery without revealing dragon intelligence. Add
ore, herb/forage, hide, and fish pools in cistern or underground stream rooms.
Only use `area.node(...)` if the runtime/builder contract remains clean.

- [ ] **Step 3: Add prerequisite-locked chain**

Add 4-5 quests. Include `tre_q_underhall_measure` follow-up logic using
`next_quest_id` and `prerequisite_quests`; do not create permanent dungeon
unlock or shared-world changes.

- [ ] **Step 4: Verify underhalls**

Run:

```powershell
python -m py_compile world/areas/tremeneth_underhalls.py
python scripts/run_tests.py tests.test_tremen_hub3_contracts tests.test_area_gathering_contracts
```

Expected: underhall checks pass.

- [ ] **Step 5: Commit underhalls**

```powershell
git add world/areas/tremeneth_underhalls.py tests world/material_definitions.py world/mob_templates.py
git commit -m "feat: add tremeneth underhalls"
```

---

### Task 9: Whole-Pack Validation And Builder Compatibility

**Files:**
- Modify any Tremen pack files needed to fix validation failures.

- [ ] **Step 1: Run full focused validation**

Run:

```powershell
python scripts/run_tests.py tests.test_tremen_hub3_contracts tests.test_area_gathering_contracts tests.test_content_integration.TestZoneImports tests.test_quest_engine tests.test_vendor_engine
```

Expected: PASS.

- [ ] **Step 2: Run smoke start**

Run:

```powershell
python scripts/smoke_start.py
```

Expected: PASS.

- [ ] **Step 3: Compile new area files**

Run:

```powershell
python -m py_compile world/areas/tremen.py world/areas/greyteeth_lower_passes.py world/areas/tremeneth_high_passes.py world/areas/tremeneth_deep_mines.py world/areas/tremeneth_underhalls.py
```

Expected: no output and exit code 0.

- [ ] **Step 4: Run Sora Builder sidecar validation**

Run the builder-side parser/validator for each new file using the current
sidecar commands available in `C:\Dev\Sora_builder`. At minimum, inspect each
file and run parse/validate if the sidecar exposes both paths.

Expected: zero parser/validator errors for all five files.

---

### Task 10: Narrative Richness, Fun, And Loose-End Polish

**Files:**
- Modify Tremen area files as needed.

- [ ] **Step 1: Audit the five-zone narrative spine**

Check that every zone expresses:

- older-than-current-people stone
- half-dwarf stewardship
- Imperial extraction aftermath
- visible-but-not-solved node activity
- distinct local gameplay purpose

- [ ] **Step 2: Audit quests**

For every quest, confirm it does at least one of:

- tells an engaging story
- guides exploration to a real place
- teaches a system or local practice
- deepens NPC relationship/memory
- encourages combat, gathering, crafting, travel, or investigation in a fun way

Rewrite any quest that is only an errand.

- [ ] **Step 3: Audit fun factors**

Confirm the pack has:

- discoverable route learning
- meaningful combat loops
- gathering/fishing that feels geographically grounded
- city services worth returning to
- underhall mystery
- at least one satisfying chain seed
- named or memorable local NPCs in every zone

- [ ] **Step 4: Re-run focused validation**

Run:

```powershell
python scripts/run_tests.py tests.test_tremen_hub3_contracts tests.test_area_gathering_contracts
```

Expected: PASS.

- [ ] **Step 5: Commit polish**

```powershell
git add world/areas/tremen.py world/areas/greyteeth_lower_passes.py world/areas/tremeneth_high_passes.py world/areas/tremeneth_deep_mines.py world/areas/tremeneth_underhalls.py tests
git commit -m "polish: enrich tremen hub three pack"
```

---

### Task 11: Tremen Golden-Path Audit

**Files:**
- Create: `docs/superpowers/plans/2026-04-27-tremen-hub3-golden-path-audit.md`

- [ ] **Step 1: Write the audit report**

Trace a player path:

1. Arrive in Tremen.
2. Learn guest bell/weather/route logic.
3. Visit Bellcut Market and Forgeheart.
4. Take `Waystation Marks` into `greyteeth_lower_passes`.
5. Return to Tremen with route understanding.
6. Take high-pass patrol content.
7. Take mine content and learn pressure-material value.
8. Enter underhall chain seed.
9. Return to Tremen with NPC recognition and next goals.

Report:

- what works well
- confusing steps
- missing guidance
- weak quest motivation
- unfair itemization
- weak combat loops
- missing help/onboarding mentions
- recommended follow-up improvements

- [ ] **Step 2: Commit the audit**

```powershell
git add docs/superpowers/plans/2026-04-27-tremen-hub3-golden-path-audit.md
git commit -m "docs: audit tremen golden path"
```

---

### Task 12: Full-MUD Launch-Readiness Audit

**Files:**
- Create: `docs/superpowers/plans/2026-04-27-launch-readiness-audit.md`

- [ ] **Step 1: Scan launch-critical sections**

Audit these areas with source-backed findings:

- Commands and aliases
- Help files and onboarding
- Abilities and status effects
- Combat and group behavior
- Inventory, equipment, items, vendors, and economy
- Gathering, fishing, crafting, and materials
- Quest logic, quest chains, world expression, and NPC memory
- Area imports, graph health, gathering coverage, and builder safety
- Mob templates, loot tables, spawns, named mobs, patrols
- Social/group/co-op systems
- Persistence/lifecycle/smoke start
- Tests and verification architecture

- [ ] **Step 2: Run broad validation**

Run:

```powershell
python scripts/run_tests.py
python scripts/smoke_start.py
```

If the full test suite is too slow or fails from unrelated known issues, record
the exact command, failure, and likely ownership in the audit.

- [ ] **Step 3: Write prioritized findings**

Use this severity model:

- `P0`: blocks hosting/go-live or can corrupt data
- `P1`: major gameplay/system break or misleading launch-critical content
- `P2`: meaningful quality, balance, onboarding, or coverage issue
- `P3`: polish/follow-up

Each finding should include:

- evidence path and line when possible
- observed behavior or code-backed risk
- why it matters for launch
- recommended fix

- [ ] **Step 4: Commit the audit**

```powershell
git add docs/superpowers/plans/2026-04-27-launch-readiness-audit.md
git commit -m "docs: audit mud launch readiness"
```

---

### Task 13: Final Closeout

**Files:**
- No required file edits unless validation fixes are needed.

- [ ] **Step 1: Final git status**

Run:

```powershell
git status --short
git log --oneline -8
```

Expected: only unrelated pre-existing `.claude/skills/...` dirt remains, unless
the user explicitly approved touching it.

- [ ] **Step 2: Final Engram memory**

Write an Engram closeout with:

- repo path
- commit list
- files changed
- validation commands and results
- Tremen pack audit summary
- launch-readiness audit summary
- remaining risks and next recommended step

- [ ] **Step 3: Final response**

Summarize:

- implementation completed
- validation results
- golden-path audit highlights
- full-MUD launch-readiness findings
- commits made
- Engram keys written
