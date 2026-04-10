# Repository Gameplay Health Check Report

## 1. Executive Summary

Overall gameplay health is poor. The repo has a lot of authored content, but multiple core play loops are either broken, incomplete, or only cosmetically present. This is not "missing polish." Several systems that make the game feel playable on paper do not actually function end to end.

Top risks:

- Core progression loops are broken: gathering tools are not authored, fishing has no usable world nodes, hide gathering pools are dead, and multiple crafting loops lack real item outputs or ingredient sources.
- Quest content is materially unreliable: several quest objective handlers cannot satisfy the authored quest specs, making a non-trivial slice of quest content impossible to complete.
- Combat progression is misleading: equipment can be equipped and displayed, but the active player basic-attack path does not use equipped weapons, and armor/stat bonuses appear disconnected from live combat math.
- Economy is mostly fictional: the world heavily implies merchants and trade, but there is no actual buy/sell/vendor loop, which collapses value flow, loot conversion, and item progression.

Top strengths:

- There is significant authored content density: areas, mobs, loot tables, recipes, quests, and command surfaces exist in volume.
- System intent is legible. The repo clearly aims for layered gameplay loops rather than a toy MUD.
- Several subsystems are internally structured well enough to be salvageable without a rewrite.

Production-playability judgment:

- Not completely playable.
- A player can move around, fight some mobs, and invoke commands, but the full game loop advertised by the content is not deliverable as written.

Coherence judgment:

- Conceptually ambitious, operationally fragmented.
- The codebase knows what game it wants to be. The gameplay wiring does not yet cash that check.

## 2. System Map

Major gameplay subsystems:

- Combat: `world/combat_script.py`, `world/combat_engine.py`, `world/combat_ai.py`, `commands/combat_commands.py`
- Equipment and inventory: `typeclasses/objects.py`, `world/inventory_engine.py`, `commands/cmd_equipment.py`
- Loot and rewards: `world/loot_tables.py`, `world/mob_templates.py`, `typeclasses/mobs.py`, `world/item_spawner.py`
- Gathering and fishing: `commands/cmd_gathering.py`, `commands/cmd_fishing.py`, `world/gathering_engine.py`, `world/material_definitions.py`
- Crafting: `world/crafting_engine.py`, `world/crafting_definitions.py`, authored item defs in area modules and `world/areas/equipment_catalog.py`
- Quests: `world/quest_engine.py`, quest definitions in `world/areas/*.py`
- Economy and banking: `world/banking.py`, `commands/cmd_bank.py`
- Content authoring: `world/area_builder.py`, `world/areas/*.py`, `world/action_vocabulary.py`

Intended interaction model:

- World content authors rooms, mobs, gathering pools, quests, vendors, and items through area-builder modules.
- Players gather resources, craft gear and consumables, kill mobs for loot, complete quests, improve skills, buy/sell through vendors, and recycle value through banking.
- Combat and equipment are intended to support progression pressure through weapon upgrades, armor scaling, consumables, and corpse/loot rules.

Important architectural observation:

- The content layer is ahead of the engine layer. Many authored areas assume systems exist that either do not exist at all or only partially exist.

## 3. Critical Findings

### 3.1 Economy loop is missing

- Severity: Critical
- Confidence: Confirmed
- Area: Economy / vendors / progression loop
- Files: `commands/default_cmdsets.py`, `world/help_entries.py`, `world/areas/vaels_crossing.py`, `world/areas/ashreach_plains.py`
- Issue:
  - The world is full of vendor/shop content and the help text explicitly promises trade with NPCs.
  - There is no implemented `buy`, `sell`, merchant, vendor inventory, or transaction command path.
  - `commands/default_cmdsets.py` registers bank commands but no merchant/trade command surface.
- Why it matters:
  - This removes the economic sink/source loop.
  - Loot value becomes mostly decorative.
  - Crafted goods have no clear conversion path.
  - Shop-heavy content in Vael's Crossing is mostly staging, not gameplay.
- Recommended fix:
  - Implement a minimal merchant system immediately: `list`, `buy`, `sell`, vendor stock definitions, quest-item sale protection, and price sourcing from authored item defs.

### 3.2 Consumables are effectively unusable

- Severity: Critical
- Confidence: Confirmed
- Area: Consumables / survival / sustain
- Files: `commands/cmd_abilities.py`, `world/areas/equipment_catalog.py`, `world/areas/vaels_crossing.py`, `world/ancestry_engine.py`, `world/item_spawner.py`
- Issue:
  - The use-item path in `commands/cmd_abilities.py` only recognizes items with `item.db.consumable == True`.
  - Authored consumables are created with `item_type="consumable"` plus `use_effect`, or with `effect` / `magnitude`, not `db.consumable`.
  - The consumer logic expects `heal_amount`, `stamina_amount`, or `cure_effect`, not `use_effect` or `effect`.
  - Starter healing items from ancestry definitions use `heal_amount` but are authored as `item_type="item"`, so they also miss the consumable gate.
- Why it matters:
  - Potions, antidotes, bandages, and starter healing items do not reliably work.
  - Sustain, recovery, and preparation loops are broken.
- Recommended fix:
  - Standardize one consumable schema.
  - Make `item_type=="consumable"` sufficient for use.
  - Normalize authored consumable payloads at spawn time or in the use path.

### 3.3 Fishing is not playable

- Severity: Critical
- Confidence: Confirmed
- Area: Gathering / fishing
- Files: `commands/cmd_fishing.py`, `world/material_definitions.py`, `world/areas/*.py`
- Issue:
  - `CmdFish` requires a `GatheringNode` with `node_type == "fish"`.
  - No authored area module defines a `gathering_pool("fish", ...)`.
  - The command also expects `fishing_rod` and optional `bait` items, but no authored item path for those tools was found.
- Why it matters:
  - Fishing is exposed as a command surface but has no world support.
  - Any recipes or loops depending on fish are functionally dead.
- Recommended fix:
  - Add real fish pools in coastal/water areas.
  - Author rods and bait as actual obtainable items.
  - Add tests that at least one fish node exists in shipped content.

### 3.4 Gathering tools are missing, making multiple professions unusable

- Severity: Critical
- Confidence: Confirmed
- Area: Gathering / crafting input loop
- Files: `world/material_definitions.py`, `commands/cmd_gathering.py`, `commands/cmd_fishing.py`, authored area/item content
- Issue:
  - Mining, herbalism, woodcutting, skinning, and fishing all require tool items (`pickaxe`, `sickle`, `hatchet`, `skinning_knife`, `fishing_rod`).
  - These tool identifiers exist in system metadata, not as authored obtainable items.
- Why it matters:
  - Large portions of gathering are blocked before the player can even start.
  - Crafting loses its material supply loop.
- Recommended fix:
  - Author starter/basic versions of all gathering tools and place them in the world, starter loadouts, or vendors.

### 3.5 Hide gathering pools are authored but unreachable

- Severity: High
- Confidence: Confirmed
- Area: Gathering content wiring
- Files: `world/areas/vaels_crossing.py`, `world/areas/cantera_edge.py`, `commands/cmd_gathering.py`
- Issue:
  - Area content defines `gathering_pool("hide", ...)`.
  - The gather command path for hides is `butcher`, and `CmdButcher` only searches for `CorpseContainer`, not `GatheringNode`.
  - Result: authored hide pools cannot ever be harvested.
- Why it matters:
  - Authored content is lying to the game.
  - Skinning/hide supply is split between two incompatible systems.
- Recommended fix:
  - Decide whether hide comes from corpses only or from hide nodes too.
  - Then delete the losing path or wire both properly.

### 3.6 Multiple quests are impossible due to objective-handler bugs

- Severity: Critical
- Confidence: Confirmed
- Area: Quest progression
- Files: `world/quest_engine.py`, `world/areas/ashreach_plains.py`, `world/areas/reth_foothills.py`, `world/areas/vaels_crossing.py`, `world/areas/stormhaven_coast.py`, `world/areas/cantera_edge.py`
- Issue:
  - `check_investigate_objectives()` only ever advances investigate progress to `1`, so authored investigate objectives with `count > 1` cannot complete.
  - `check_deliver_objectives()` requires `item_tag` on objective entries, but explicit enriched `objectives=[...]` deliver quests do not auto-fill it.
  - `check_deliver_objectives()` also only advances deliver progress to `1`, so deliver objectives with `count > 1` cannot complete.
  - Some enriched kill targets do not match real mob ids/templates:
    - `sea_raider` quest target vs spawned `coastal_raider`
    - `mountain_troll` quest target vs spawned `rock_troll`
- Why it matters:
  - This is not edge-case quest polish. It makes shipped quest content unwinnable.
- Recommended fix:
  - Fix objective progression logic first.
  - Add a repo-wide quest validation pass that checks every target against actual mobs, rooms, NPC ids, and item tags.

### 3.7 Several quest item targets appear to have no source

- Severity: High
- Confidence: Likely
- Area: Quest content completeness
- Files: quest definitions across `world/areas/*.py`, `world/action_vocabulary.py`, `world/loot_tables.py`, `world/crafting_definitions.py`
- Issue:
  - Objective targets such as `outstanding_debt_token`, `commissioned_blade`, `stolen_artifact`, `rare_herb_bundle`, `rare_alpine_ingredient`, `resonance_sample`, `contraband_package`, and `warden_supplies` were found in quests but no clear generation path was found in loot, crafting, dialogue reward, or authored item content.
- Why it matters:
  - Even after fixing quest engine math, some quests may still be impossible because the required items do not enter the world.
- Recommended fix:
  - Add a static validator for quest collectible/delivery targets and prove each has at least one production path.

### 3.8 Equipment progression is largely disconnected from combat

- Severity: Critical
- Confidence: Confirmed for weapons, Likely for armor/stat bonuses
- Area: Combat / equipment / progression
- Files: `world/combat_script.py`, `world/combat_engine.py`, `world/inventory_engine.py`, `typeclasses/objects.py`, `commands/cmd_equipment.py`
- Issue:
  - Player basic attacks call `resolve_basic_attack(character, target)` with no weapon argument in `world/combat_script.py`.
  - The helper `world/inventory_engine.get_equipped_items()` exists but is not used in the active combat path.
  - I found no live combat path applying equipped weapon damage to player basic attacks.
  - I also found no clear path applying `armor_value` or `stat_bonuses` from equipped gear into incoming damage, derived stats, or combat mitigation.
- Why it matters:
  - Equipping a sword appears not to matter for basic attacks.
  - Armor and stat-bearing gear may be mostly fake progression.
  - This guts the entire loot/equipment incentive structure.
- Recommended fix:
  - Make combat read the equipped main-hand item on every basic attack.
  - Define a single authoritative place where equipped stat bonuses and armor contribute to derived combat numbers.

### 3.9 Group loot modes exist as UI/state only

- Severity: High
- Confidence: Confirmed
- Area: Group play / loot distribution
- Files: `world/group_engine.py`, `commands/cmd_group.py`, loot/corpse code
- Issue:
  - Group loot modes `personal`, `ffa`, `round_robin`, and `need_pass` are supported as state values.
  - I found no distribution logic using those modes in corpse generation, item assignment, or loot rolling.
- Why it matters:
  - Multiplayer reward rules are promised but not enforced.
  - Group progression and fairness are undefined in practice.
- Recommended fix:
  - Either implement real distribution semantics or cut the fake modes and ship only one real rule.

### 3.10 Some spawned mobs have no real loot tables

- Severity: High
- Confidence: Confirmed
- Area: Reward loop / combat payoff
- Files: `world/mob_templates.py`, `world/loot_tables.py`
- Issue:
  - Mobs reference `loot_table: "rat"` and `loot_table: "bandit"`.
  - Those keys are referenced in templates but not defined in `LOOT_TABLES`.
- Why it matters:
  - Relevant mobs can die and drop nothing because the loot-table mapping is incomplete.
  - That makes early/mid-game content feel broken or stingy for the wrong reasons.
- Recommended fix:
  - Either add the missing table entries or update all templates to reference real tables.

### 3.11 Crafting outputs and ingredient loops are incomplete

- Severity: High
- Confidence: Confirmed
- Area: Crafting / content completeness
- Files: `world/crafting_definitions.py`, `world/crafting_engine.py`, `world/areas/equipment_catalog.py`, area item defs
- Issue:
  - Multiple recipe outputs do not have authored item definitions, including `basic_healing_draught`, `cooked_meat`, `healing_draught`, `hearty_stew`, `herb_poultice`, `iron_chainmail`, `mountain_tonic`, `spiced_fish`, `stamina_tonic`, and `trail_rations`.
  - This means crafting falls back to generic objects instead of intended items/effects.
  - Several recipe ingredients rely on shaky or absent source loops, especially where fishing/tools are missing.
- Why it matters:
  - Crafting does not reliably produce meaningful or balanced rewards.
  - Recipe trees are wider than the implemented item catalog.
- Recommended fix:
  - Add a static recipe-to-item and recipe-to-ingredient validator and make it part of CI.

### 3.12 Corpse and loot access rules appear under-enforced in actual play

- Severity: Medium
- Confidence: Likely
- Area: Looting / corpse interaction
- Files: `typeclasses/objects.py`, `world/combat_engine.py`, `world/inventory_engine.py`, command surface
- Issue:
  - `CorpseContainer.can_loot()` exists and corpse objects are locked against direct `get`.
  - I did not find a custom loot/open-corpse command that enforces corpse claim rules while allowing controlled item retrieval.
  - The broader item loop appears to rely heavily on default Evennia get/drop behavior, which does not know about `InventoryItem` syncing or corpse claim logic.
- Why it matters:
  - Corpse looting may be awkward, impossible, or bypass gameplay-specific rules depending on default Evennia behavior.
- Recommended fix:
  - Add an explicit corpse-loot command layer and stop relying on generic object interactions for a model-backed inventory system.

## 4. Integration / Wiring Audit

### Correctly wired or mostly coherent

- Combat command registration is explicit and broad in `commands/default_cmdsets.py`.
- Combat encounters do start through `commands/combat_commands.py` and route into `world/combat_script.py`.
- Corpse spawning exists for both mobs and players in `world/combat_engine.py`.
- Equipment can be equipped and tracked at the model layer through `world/inventory_engine.py`.
- Quest definitions are numerous and structurally consistent enough to audit.
- Area content is extensive and generally follows a consistent authoring style.

### Disconnected / partially connected / incorrectly connected

- Vendors, shops, and merchant NPCs are authored but not backed by trade mechanics.
- Consumable item authoring does not match the consumable execution path.
- Fishing command exists without fish nodes or rods.
- Hide gathering pools exist without a command path that can target them.
- Group loot mode state exists without corresponding loot behavior.
- Crafted outputs often do not map to authored items.
- Quest definitions assume objective-handler behavior that the engine does not implement.
- Equipment metadata exists without convincing live combat integration.

## 5. Dead Code / Drift Audit

Likely drift / dead gameplay paths:

- `world/inventory_engine.get_equipped_items()` looks like intended combat integration that never got finished.
- `armor_value` and many `stat_bonuses` definitions in equipment content look largely decorative right now.
- Group loot modes beyond maybe a future `personal` path look like speculative scaffolding.
- Fish and hide support in material/category metadata overstate actual shipped gameplay.
- Vendor-rich area content in Vael's Crossing is far ahead of the systems that would make it interactive.
- Consumable schemas are duplicated and incompatible:
  - `use_effect`
  - `effect` / `magnitude`
  - `heal_amount` / `stamina_amount` / `cure_effect`

Documentation/content drift:

- Help text claims trading and selling crafted goods.
- The world presentation strongly implies a functioning merchant economy.
- The actual command surface and systems do not deliver that promise.

## 6. Refactor Opportunities

### 1. Unify item schemas

- Impact: Very high
- Risk: Medium
- Payoff:
  - Fixes consumables, tools, quest items, crafting outputs, merchant inventory, and loot in one move.

### 2. Build a static gameplay integrity validator

- Impact: Very high
- Risk: Low
- Payoff:
  - Catches missing loot tables, quest target mismatches, missing item outputs, missing tool sources, and dead gathering pools before runtime.

### 3. Centralize equipment contribution to combat stats

- Impact: Very high
- Risk: Medium
- Payoff:
  - Converts gear from theater into progression.

### 4. Collapse gathering definitions into one authoritative source

- Impact: High
- Risk: Medium
- Payoff:
  - Prevents the current split where categories exist in metadata but not in actual area content or command support.

### 5. Replace fake group loot modes with one real implementation

- Impact: Medium
- Risk: Low
- Payoff:
  - Removes misleading multiplayer complexity and reduces unfinished branching logic.

### 6. Split authored-content validation from runtime systems

- Impact: High
- Risk: Low
- Payoff:
  - Large area files become less dangerous if CI proves their references are valid.

## 7. Testing Gaps

Missing or weak tests:

- No repo-level test proving every exposed gathering command has at least one corresponding authored node and obtainable tool.
- No test proving every quest objective target is satisfiable by actual rooms, mobs, NPCs, item tags, or delivery items.
- No test proving every recipe output maps to a real authored item with expected gameplay effects.
- No test proving equipped weapons affect player attack damage in the live combat path.
- No test proving armor/stat bonuses affect survivability or derived stats.
- No test proving merchant/shop gameplay exists even though content strongly implies it.
- No test proving group loot modes affect anything beyond state storage.
- Corpse-loot tests appear to focus on isolated logic, not on actual player-command interaction.

Highest-priority new tests:

- A full quest integrity test over all area-authored quests.
- A full gameplay-content integrity test over tools, gathering pools, fish pools, and craftable outputs.
- A combat integration test proving equipped weapon changes basic-attack damage.
- A merchant smoke test once trade exists.

## 8. Risk Register

1. Quest content is partially unwinnable.
2. Equipment progression may be mostly fake.
3. Economy loop does not exist despite world design depending on it.
4. Gathering/crafting progression is blocked by missing tools and dead node types.
5. Fishing is exposed but not playable.
6. Reward loops are inconsistent because some mobs have no real loot tables.
7. Content authoring velocity is exceeding engine validation, which will keep increasing drift.

## 9. Recommended Action Plan

### Immediate fixes

1. Fix quest objective progression bugs for `investigate` and `deliver`.
2. Standardize consumable item handling and make all authored consumables usable.
3. Wire equipped weapon damage into the live basic-attack path.
4. Add the missing loot tables or retarget affected mobs.

### Short-term cleanup

1. Add obtainable gathering tools.
2. Add fish pools or remove/disable fishing until it is real.
3. Resolve hide gathering duplication: corpse-only or node-supported, not both half-done.
4. Author missing recipe outputs and verify ingredient sourcing.

### Medium-term architectural improvements

1. Implement a minimum viable merchant system.
2. Add static validation for quests, recipes, loot tables, gathering pools, and item ids.
3. Define one authoritative item/equipment schema and normalize all authored content to it.
4. Either implement real group loot modes or cut back to one honest rule.

### Suggested order of operations

1. Fix impossible quests.
2. Fix fake consumables and fake equipment progression.
3. Restore gathering/crafting input loops.
4. Restore reward/economy output loops.
5. Add validation so the repo stops regressing in the same ways.

## 10. Appendix

### Notable patterns

- The repo repeatedly has the same failure mode: strong content intent, weak end-to-end wiring.
- Systems are often built in metadata first, then not fully connected to commands or authored content.
- Content breadth is outpacing gameplay validation.

### Open questions

- Whether any hidden/default Evennia command behavior is currently compensating for the absence of a custom loot command layer.
- Whether armor/stat bonuses affect derived stats indirectly somewhere outside the combat path I traced. I did not find convincing evidence that they do.
- Whether some quest items are spawned only through dialogue or trigger paths not surfaced by straightforward static inspection. If so, they are still too opaque.

### Areas requiring runtime verification

- Corpse looting UX and rule enforcement under real player commands.
- Actual player damage delta between unarmed and equipped attacks.
- Any hidden production path for missing quest items.
- Balance tuning once broken loops are made real, especially consumables, loot value, and recipe payoff.

## Top 10 Concrete Gameplay Fixes

1. Make equipped weapons affect `attack`.
2. Make authored consumables actually consumable.
3. Fix `investigate` objectives with `count > 1`.
4. Fix `deliver` objectives to support enriched objective specs and counts above 1.
5. Add a real merchant buy/sell loop.
6. Add obtainable gathering tools for all required professions.
7. Add fish nodes and rod/bait content or disable fishing.
8. Either support hide nodes or remove them and keep skinning corpse-only.
9. Add missing `rat` and `bandit` loot-table coverage.
10. Author real item defs for all recipe outputs currently falling back to generic items.

## Top 10 Suspected Dead/Unplayable Gameplay Content Candidates

1. Fishing command flow as currently shipped.
2. Hide gathering pools in authored areas.
3. Vendor/shop rooms as actual gameplay spaces rather than scenery.
4. Group loot modes other than future intent/state.
5. `use_effect` consumables in `world/areas/equipment_catalog.py`.
6. `effect` / `magnitude` consumables in `world/areas/vaels_crossing.py`.
7. Multi-count investigate quests.
8. Multi-count deliver quests.
9. Quest targets requiring `sea_raider` or `mountain_troll`.
10. Crafting outputs with no authored item definitions.

## Top 10 Files/Modules To Inspect First

1. `world/quest_engine.py`
2. `world/combat_script.py`
3. `world/combat_engine.py`
4. `commands/cmd_abilities.py`
5. `world/inventory_engine.py`
6. `commands/cmd_fishing.py`
7. `commands/cmd_gathering.py`
8. `world/crafting_definitions.py`
9. `world/loot_tables.py`
10. `world/areas/vaels_crossing.py`

## Fastest Path To Materially Improve Playability In 1-2 Days

1. Patch quest objective logic so authored quests stop being impossible.
2. Patch consumable handling so healing/stamina/antidote items actually work.
3. Wire equipped weapon lookup into basic attacks.
4. Add starter/basic gathering tools and at least one fish pool plus rod access.
5. Add missing loot-table coverage for referenced mob archetypes.
6. Ship one minimal merchant command path for buy/sell against authored vendor stock.
7. Add one static audit test file that fails on:
   - missing quest targets
   - missing loot tables
   - missing recipe outputs
   - gathering commands without nodes/tools

