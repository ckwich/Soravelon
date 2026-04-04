# Phase 13: Gathering and Refining - Context

**Gathered:** 2026-04-03
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the resource gathering and material refining systems: gathering nodes spawn stochastically in flagged rooms with zone-wide pool limits, players use skill-specific commands (mine, harvest, chop, forage, fish, butcher) to extract raw materials, and processing recipes in the existing crafting system convert raw materials into crafting ingredients (ore to ingot, fiber to thread to cloth). Includes a fishing mini-game, tool requirements with durability, prospect/survey discovery mechanics, and a scalable 5-tier material registry.

</domain>

<decisions>
## Implementation Decisions

### Gathering Node Design
- **D-01: Stochastic node spawning** -- Rooms flagged as eligible for gathering types. Nodes spawn as Evennia objects randomly across eligible rooms, managed by a zone-wide pool. E.g., 5 meadow rooms share a pool of max 3 herb nodes that appear randomly among them. Anti-bot: no fixed farming routes.
- **D-02: AreaBuilder DSL** -- `area.gathering_pool('herb', rooms=['meadow_1','meadow_2','meadow_3'], materials=['wild_herb','thornroot'], max_active=3, respawn_minutes=15)`. Zone-level declaration, pool manages random room placement. Mirrors mob `spawn_definitions` pattern.
- **D-03: Shared depletion** -- Nodes have a random use count (2-6 per node) visible to all players. Once depleted, the node disappears and a new one spawns in a different eligible room after a delay. Creates real scarcity and competition.
- **D-04: Skill affects quality AND quantity** -- Higher gathering skill yields more items per gather AND better quality raw materials. Quality uses the existing flawed/standard/fine/superior/masterwork tier system.

### Processing Chains
- **D-05: Two-step max depth** -- Raw -> Processed (ore -> ingot, hide -> leather_strip, herb -> extract). Fiber -> thread -> cloth is the deepest chain. No deeper than 2 processing steps before a material becomes a final crafting ingredient.
- **D-06: Existing crafting system** -- Processing recipes go into RECIPE_REGISTRY alongside crafting recipes. `smith iron_ingot` at a forge smelts ore. Reuses station checks, skill quality, delay, and the entire _BaseCraftCmd pipeline. No new engine needed.
- **D-07: Quality propagation** -- Raw material quality carries through processing. Fine iron ore + skilled smithing = better chance of fine iron ingot. Raw quality sets a floor/ceiling, processing skill adjusts within that range.
- **D-08: Skill-based conversion ratio** -- Low skill: 3 raw -> 1 processed. Medium skill: 2 raw -> 1 processed. High skill: 1 raw -> 1 processed (1:1). Master gatherers need less material and get better quality. Strong progression loop.

### Material Taxonomy
- **D-09: MATERIAL_REGISTRY** -- Central Python dict in new `world/material_definitions.py`. Each material: id, display_name, category (ore/fiber/herb/hide/wood/fish), tier, raw_form, processed_form, gathering_skill, processing_skill. New materials = add dict entry.
- **D-10: 5 material tiers** -- Expandable tier system (not locked to equipment's current 3 tiers). Tiers 1-5 with room for future expansion. Zone difficulty influences tier range but is not the sole gate.
- **D-11: Mob drops feed processing pipeline** -- Existing mob loot items (boar_hide, spider_silk_thread, ash_wolf_pelt) become raw crafting materials. Process wolf hide into leather strip at workbench. 50+ existing loot items gain crafting utility.

### Gathering Commands
- **D-12: Skill-specific commands** -- `mine` (mining), `harvest` (herbalism), `chop` (woodcutting), `forage` (foraging), `fish` (fishing), `butcher` (skinning). Each wired to its skill. Matches crafting pattern (cook, smith, brew, craft).
- **D-13: 6 gathering skills** -- Mining (NEW), Herbalism (exists), Woodcutting (NEW), Foraging (exists), Fishing (exists), Skinning (NEW). Full skill split for a deep MUD with 90 subclass combinations.
- **D-14: Variable delay with skill reduction** -- Gathering delay varies by node tier. Skill reduces delay, but never below 40% of the original timer. Cancelled by movement (same as crafting).
- **D-15: Butcher targets corpses** -- `butcher <corpse>` extracts hides, bones, meat from mob corpses. Skinning skill determines quality and quantity. Corpse consumed or marked as butchered.

### Fishing System
- **D-16: Active + idle fishing modes** -- Active: cast -> wait for random bite timer -> 'reel' within window -> catch. Better rewards. Idle: `fish` starts auto-fishing with periodic catches at significantly diminished returns. Rewards engagement without punishing casual play.
- **D-17: Fishing spots via gathering pools** -- Water-tagged rooms eligible for fishing spot spawning. Uses same `area.gathering_pool()` system. Fish types configurable per room/zone, builder-app friendly.
- **D-18: Optional bait system** -- Can fish without bait. Bait items (from foraging or vendors) improve catch rate, quality, or unlock rare fish. Bait consumed per cast.

### Tool Requirements
- **D-19: Required tools per skill** -- Mining needs pickaxe, woodcutting needs hatchet, fishing needs rod, herbalism needs sickle/shears. No tool = can't gather. Tools are equipment items. Creates item progression and economic sink.
- **D-20: Tool durability with repair** -- Tools have durability, lose points per use, break when depleted. Repairable at workbench via smithing skill. Creates ongoing material demand -- smiths make tools for gatherers, gatherers feed materials to smiths.

### Node Discovery & Visibility
- **D-21: Tiered visibility** -- Low-tier nodes visible to everyone in room descriptions. Mid-tier nodes require minimum skill to spot. High-tier nodes hidden until discovered via prospect/survey.
- **D-22: Prospect/survey command** -- Reveals gathering nodes within N rooms in straight lines from the player (line-of-sight, not BFS through corners). Directional indicators ("Iron deposits to the north, 2 rooms away"). Skill improves range but never scans entire zone.
- **D-23: Sense integration** -- Existing Sense command gives vague environmental hints ("mineral deposits nearby"). Prospect/survey gives specifics ("Iron ore vein, tier 2, 4 gathers remaining"). Different detail levels.

### Zone Material Distribution
- **D-24: Common materials everywhere, rare exclusives per zone** -- Most common gathering nodes available across zones with similar biomes. Each zone has 1-2 unique rare materials in pockets (e.g., Ashreach has volcanic glass, Cantera has heartwood resin). Maximizes both zone identity and player experience.
- **D-25: Zone difficulty influences tier range** -- Starter zones spawn mostly tier 1-2. Mid zones spawn tier 2-3. Advanced zones spawn tier 3-5. Each zone has a tier floor and ceiling configured in gathering_pool().

### Claude's Discretion
- Exact gathering delay values per node tier (base seconds)
- Skill threshold breakpoints for tiered visibility
- Prospect/survey max range values and scaling formula
- Tool durability values and repair cost formula
- Fishing bite timer ranges (active mode)
- Idle fishing catch interval and diminished return multiplier
- Specific bait items and their bonus effects
- Processing recipe difficulty values
- Quality propagation formula (how raw quality + skill combine)
- GatheringNode typeclass implementation details
- Pool respawn timer randomization range
- Zone-exclusive material names for each existing zone

### Folded Todos
None.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Crafting System (extend, don't replace)
- `world/crafting_engine.py` -- Core engine with quality tiers, station checks, ingredient matching, skill integration
- `world/crafting_definitions.py` -- RECIPE_REGISTRY (27 recipes), QUALITY_TIERS, STATION_REQUIREMENTS, COMMAND_TO_SKILL mappings
- `commands/cmd_crafting.py` -- _BaseCraftCmd pattern (delay, move-cancel, station check) that gathering commands should mirror

### Item & Loot Infrastructure
- `world/item_spawner.py` -- `create_item_from_template()` for creating gathered material items
- `world/loot_tables.py` -- LOOT_TABLES with 50+ mob drops that will feed into processing pipeline
- `world/areas/equipment_catalog.py` -- 69 item templates across 3 material tiers (iron/steel/mithril)

### Skill Definitions
- `world/skill_definitions.py` -- Existing herbalism (#84), foraging (#210), fishing (#252) skill definitions with thresholds. New skills (mining, woodcutting, skinning) need adding.

### Zone & Mob Systems
- `world/area_builder.py` -- AreaBuilder DSL for `gathering_pool()` extension
- `world/mob_spawner.py` -- Spawn pool pattern (zone-level management, random room placement) that gathering node spawning should mirror

### Models
- `world/models.py` -- CharacterRecipe model for recipe tracking. May need GatheringNode tracking model.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **_BaseCraftCmd (commands/cmd_crafting.py):** Shared command base with delay, move-cancel, station check. Gathering commands can follow same pattern with `_BaseGatherCmd`.
- **Quality tier system (crafting_definitions.py):** flawed/standard/fine/superior/masterwork with multipliers. Reusable for gathered material quality.
- **Skill integration (skill_engine.py):** `get_skill_value()`, `accumulate_skill_use()` already wired for crafting. Same functions for gathering.
- **mob_spawner.py pool pattern:** `spawn_zone()` manages zone-wide mob pools with room assignment. Gathering node spawning can mirror this architecture.
- **item_spawner.py:** `create_item_from_template()` creates items from definition dicts. Gathered materials use same pathway.
- **Tag-based ingredient matching:** `obj.tags.has(tag, category="item_tag")` already used by crafting engine for ingredient lookup.

### Established Patterns
- **AreaBuilder DSL:** `area.spawn()`, `area.item()`, `area.flight_point()` -- `area.gathering_pool()` follows same declarative pattern
- **Tick-driven scripts:** NodeScript, PatrolScript, FlightScript use Evennia's TickerHandler. GatheringPoolScript would follow same pattern for respawn management.
- **Room state flags (room_state.py):** FLAG_VOCABULARY for volatile room state. Could add gathering-related flags.

### Integration Points
- **_load_all_zones() (area_builder.py):** Where gathering pools would be initialized after zone load
- **Mob at_death (typeclasses/mobs.py):** Where butcher-eligible corpse state gets set
- **Character cmdset:** Where gathering commands get registered
- **OOB publisher:** For gathering-related client push (node discovered, gather complete, etc.)

</code_context>

<specifics>
## Specific Ideas

- "I don't want players to have a farming route that they can just script/bot out" -- Anti-bot is a core design goal. Stochastic spawning, variable depletion, and prospect-based discovery all serve this.
- "We're running a deep and rich MUD with 90 subclass combinations, having a large bank of skills makes sense" -- Full 6-skill split is justified by game depth.
- "Maximize zone identity while also maximizing player experience" -- Zone exclusives for identity, common materials everywhere for accessibility.
- Processing conversion ratio (3:1 -> 2:1 -> 1:1) makes gathering skill progression feel deeply rewarding -- less waste and better quality.
- Fishing has both active mini-game AND idle mode -- rewards engagement without punishing casual play.
- Tool durability creates smith-gatherer economic loop -- smiths make tools, gatherers feed materials to smiths.
- Prospect/survey uses straight-line scanning with directional indicators, NOT BFS pathfinding -- intentional design choice for exploration feel.

</specifics>

<deferred>
## Deferred Ideas

None -- discussion stayed within phase scope.

</deferred>

---

*Phase: 13-gathering-and-refining*
*Context gathered: 2026-04-03*
