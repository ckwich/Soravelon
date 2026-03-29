# Phase 7: Milestone 1 Content - Context

**Gathered:** 2026-03-29
**Status:** Ready for planning

<domain>
## Phase Boundary

Author Soravelon's first playable slice: Vael's Crossing (100+ room hub city on Varath) with all services, 4 starter zones (100+ rooms each) with mobs/NPCs/materials, one zone with an active node and Layer 1 rooms, a 50+ item equipment catalog with material tiers, and vendor/crafting/loot item sources. All content authored as AreaBuilder DSL zone spec files in `world/areas/`.

</domain>

<decisions>
## Implementation Decisions

### Hub City — Vael's Crossing
- **D-01:** 100+ rooms. Dark frontier outpost aesthetic — gritty, worn, practical. On the eastern continent (Varath). NOT the western continent despite vault World Bible saying "Hub 1 — Western continent frontier town" — user override.
- **D-02:** "Vael's Crossing" is the final name.
- **D-03:** Bustling metropolis feel — 50+ NPCs with quest stub threads everywhere. Rich atmosphere designed for future propagation via builder client.
- **D-04:** Districts designed by Claude — aim for 6-8 districts (~15-25 rooms each) covering all services. Must include: guild quarter (all 10 domain halls), market, residential, dock/gate area.
- **D-05:** Unsafe edges — core city is safe, outskirts/sewers/back alleys have low-level threats (rats, thugs). Hidden underworld district with shady NPCs, debt collectors, black market, AND mob spawns (thugs, smugglers).
- **D-06:** Thematic named paths connect to starter zones (e.g., "The Ashway", "Harbor Road"). Not cardinal gates.
- **D-07:** Single Dragon Courier flight point in the city. Full Consortium bank branch.
- **D-08:** All 10 guild halls present (temporary — will redistribute when more hub cities exist).
- **D-09:** Empire + Consortium + Wardens faction presence in the city. Other factions via NPCs but no formal offices.
- **D-10:** 3-5 atmospheric landmarks designed by Claude (watchtower, old temple, memorial, etc.).
- **D-11:** New player onboarding: arrive at a specific room with a greeter NPC who points to services.
- **D-12:** One crafting station of each type (cooking fire, smithing forge, alchemy bench).
- **D-13:** Trainers populated — skill trainer NPCs for the Phase 6b TRAINER_REGISTRY.
- **D-14:** Medic building serves as death respawn point.
- **D-15:** City vendors sell basic starter weapons/armor AND basic consumable potions.
- **D-16:** All content invented fresh (no existing vault lore for Vael's Crossing), but scan ALL vault files for naming conventions, continent geography, faction details before creating anything.

### Starter Zones (4 total)
- **D-17:** 100+ rooms per zone. 4 distinct biomes designed by Claude using Varath geography (Ashreach plains, The Reth mountains, northeastern coast, Cantera Forest as references).
- **D-18:** NO LEVELS — zone scaling makes all content appropriate for all players. Never reference level ranges.
- **D-19:** Moderate mob density — 1-2 spawns per 2 rooms.
- **D-20:** One named mob (mini-boss) per zone with unique loot and zone-wide respawn announcement.
- **D-21:** Mob rarity through affix system (random modifications on base templates), NOT separate spawn definitions for uncommon/rare mobs. Exploration rewarded copiously.
- **D-22:** 1-3 field NPCs per zone (ranger outpost, hermit, patrol captain) with dialogue and quest hook stubs.
- **D-23:** Quest stubs only — NPCs reference quests in dialogue but quest system stays stubbed. Stubs must be viewable/editable in future builder client.
- **D-24:** Both crafting materials AND lore fragments in each zone.
- **D-25:** Connected network — zones connect to city AND to each other.
- **D-26:** Flight points in city only for M1 — players walk to zones.
- **D-27:** Some mobs wander (random movement, not fixed patrol routes). If a wandering mob system doesn't exist, it needs implementation.
- **D-28:** 1-2 is_hunter mobs per zone (BFS chase within detection range). Sparingly.
- **D-29:** Zone attunement active from start — players gain attunement as they explore/fight.
- **D-30:** Some room state flags alter descriptions (visible), others discoverable by domain Sense ability.
- **D-31:** 3-5 base mob types per zone, themed to biome. Variety comes through affix system.

### Equipment Catalog
- **D-32:** Large catalog (50+ items). Ranged weapons are flavor only — no cross-room combat system yet.
- **D-33:** Soft stat requirements — weapons work for anyone but scale better with matching stats.
- **D-34:** Three sources: city vendors (basics), mob drops (zone-themed), crafting (quality variants).
- **D-35:** 2-3 material tiers with scaling stats (iron → steel → mithril or similar). Zone drops themed by material.
- **D-36:** Ignore equipment weight for M1 — no encumbrance friction.
- **D-37:** 13 equipment slots: head, face, chest, back (cloak), hands, wrists (bracers), legs, feet, main hand, off hand, ring ×2, amulet.
- **D-38:** Two-handed weapons exist (greatswords, staves, greataxes) — use both hand slots, higher damage.
- **D-39:** Shields are passive armor in off-hand (no active block mechanic for M1).
- **D-40:** Equipment provides small stat bonuses (+2 Strength on gauntlets, etc.).
- **D-41:** Equipment is permanent — no durability/degradation system for M1.
- **D-42:** Weapon damage per vault spec: damage_min/damage_max + stat scaling + zone scaling multiplier.
- **D-43:** No set bonuses for M1. No procedural affixes (CON-04).
- **D-44:** Vendor consumables (basic healing potions) alongside crafting outputs.

### Node Zone
- **D-45:** Claude picks which of the 4 zones gets the active node — choose theme that best fits corruption/magical instability.
- **D-46:** Complete transformation when node collapses — Layer 1 rooms are fundamentally different, almost unrecognizable.
- **D-47:** Partial overlay — only rooms near the node center get Layer 1 versions. Edge rooms stay normal.
- **D-48:** Unique corrupted mob variants spawn only in Layer 1 (collapsed state).
- **D-49:** Node failure follows existing NodeScript tick-driven progression: healthy → stressed → failing → collapsed.
- **D-50:** Layer 1 has exclusive lore fragments for Remnance/Echoes domain.
- **D-51:** Interactive stabilization mechanic — players can attempt to stabilize/repair the node, slowing or reversing failure.
- **D-52:** Claude picks node type from VALID_NODE_TYPES based on zone theme.

### Claude's Discretion
- District names and internal layout of Vael's Crossing
- Zone names, biome themes, and geographic placement on Varath
- Specific NPC names, dialogue content, and quest stub descriptions
- Mob type designs (species, abilities, behavior) per zone theme
- Equipment item names, stat values, and material tier progression
- Landmark designs and placement in the city
- Node zone selection and Layer 1 room design
- Number of rooms in Layer 1 overlay (subset of the 100+ L0 rooms)
- Wandering mob implementation approach

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### World Lore (scan ALL before inventing content)
- `C:\Obsidian\brain\Soravelon\Soravelon_World_Bible.md` — Creation myth, twin continents (Varath/Sorath), hub city descriptions, naming conventions, faction lore, geography
- `C:\Obsidian\brain\Soravelon\soravelon-factions.md` — Faction details for Empire, Consortium, Wardens, Kau'roran, Resistance
- `C:\Obsidian\brain\Soravelon\soravelon-ancestries.md` — Ancestry lore affecting NPC diversity
- `C:\Obsidian\brain\Soravelon\soravelon.md` — Core game overview

### Existing Systems
- `world/area_builder.py` — DSL for authoring zones (zone, room, exit, spawn, npc, named_mob, quest, material, lore_fragment, flight_point, node, item)
- `world/area_validator.py` — VALID_ZONE_TYPES, VALID_CONTINENTS, VALID_NODE_TYPES, VALID_ROOM_TYPES, VALID_DIRECTIONS
- `world/ability_registry.py` — 330 abilities for mob ability assignment
- `world/mob_spawner.py` — SpawnRecord system, respawn timers
- `world/dialogue_engine.py` — NPC dialogue with standing-tier variation
- `world/crafting_definitions.py` — Existing 8 recipes (cooking, smithing, alchemy)
- `world/crafting_engine.py` — Crafting quality system
- `world/loot_tables.py` — Loot drop framework
- `world/skill_definitions.py` — 21 skills + TRAINER_REGISTRY (empty, needs populating)
- `world/zone_scaling.py` — Per-player scaling (NO LEVELS)
- `world/scripts/node_script.py` — NodeScript tick-driven failure progression
- `world/combat_ai.py` — Mob AI with ability selection, conditions, casting, hunter chase
- `world/base_attributes.py` — 7 stats, point-buy, descriptors

### Item System
- `typeclasses/objects.py` — SoravelonItem, Equipment, Container typeclasses
- `world/inventory_engine.py` — Item lifecycle (pickup, drop, equip)
- `.claude/skills/item-typeclasses/skill.md` — Item typeclass reference
- `.claude/skills/inventory-engine/skill.md` — Inventory engine reference

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `world/area_builder.py` — Full DSL ready for zone authoring. All methods (zone, room, exit, spawn, npc, named_mob, quest, material, lore_fragment, flight_point, node, item) tested and idempotent.
- `world/mob_spawner.py` — SpawnRecord system handles respawn from death, initialize_spawn_records at startup.
- `world/dialogue_engine.py` — Standing-tier dialogue with 8 tiers, hints, ambient echoes.
- `world/crafting_definitions.py` — 8 recipes ready; RECIPE_REGISTRY extensible.
- `world/skill_definitions.py` — TRAINER_REGISTRY ready to populate with NPC keys.
- `typeclasses/objects.py:Equipment` — Equipment typeclass exists but needs slot/stat_bonus fields.

### Established Patterns
- Zone files in `world/areas/*.py` define `build()` functions imported at server start.
- Mobs get abilities from `db.abilities` list — no CharacterAbility unlock needed.
- NPC objects created via `area.npc()` with is_npc=True, dialogue kwargs.
- Items defined via `area.item()` stored on zone_obj.db.item_definitions.

### Integration Points
- `server/conf/at_server_startstop.py:_load_all_zones()` — imports all world/areas/*.py
- `world/skill_definitions.py:TRAINER_REGISTRY` — needs NPC key → skill mapping
- `typeclasses/objects.py:Equipment` — needs equip slot, stat bonuses, damage range fields
- `world/loot_tables.py` — needs actual drop table data for zone mobs
- Character creation flow — needs to place new characters in Vael's Crossing greeter room

</code_context>

<specifics>
## Specific Ideas

- City should feel like a bustling metropolis with threads and roots of numerous quest starters everywhere — rich atmosphere for future propagation via builder client
- Exploration should be rewarded copiously — mob rarity through affixes, lore fragments, materials, hidden areas
- Ranged weapons are purely flavor in a MUD environment — no cross-room combat system
- Quest stubs must be viewable and editable when the builder client is built
- Wandering mobs (random movement) are wanted — if no system exists, implement one
- Some room state flags alter descriptions (visible to all), others discoverable by domain Sense ability only

</specifics>

<deferred>
## Deferred Ideas

- Active shield block mechanic — stored in Engram TODO
- Equipment durability/degradation system — stored in Engram TODO
- Equipment set bonuses (matching gear combo effects) — future content
- Cross-room ranged combat system — future milestone
- Full quest system implementation — future milestone (M1 has stubs only)
- Western continent (Sorath) hub cities and zones — separate design pass
- PvP combat — not in scope
- Procedural equipment affixes — explicitly excluded by CON-04 for M1

</deferred>

---

*Phase: 07-milestone-1-content*
*Context gathered: 2026-03-29*
