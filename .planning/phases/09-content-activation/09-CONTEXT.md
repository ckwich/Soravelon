# Phase 9: Content Activation and Travel Network - Context

**Gathered:** 2026-04-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Make existing authored content reachable by players — wire trainers to NPCs, make recipes learnable, add triggers to zone specs, improve wilderness NPC density organically, and add crafting stations where missing. Flight network and Remnance discovery are explicitly deferred.

</domain>

<decisions>
## Implementation Decisions

### Flight Network
- **D-01:** Flight routes only connect hub cities. Wilderness zones are walk-only. Since v1.0 has only one hub (Vael's Crossing), the flight network is effectively dormant.
- **D-02:** Flight point and route expansion deferred to Phase 12 or future milestone. No flight work in Phase 9.

### Trainer Placement
- **D-03:** Hybrid placement: Vael's Crossing guild quarters get general trainers (3-4 skills each). Wilderness zones get 1-2 specialist trainers in thematically appropriate locations (fishing near coast, climbing in foothills, herbalism in forest).
- **D-04:** Training cost is tiered: low-skill training costs Scales only. High-skill training costs Scales AND hard-to-find materials. The trainer's skill level and the player's current level determine the cost tier.
- **D-05:** Wire trainer_id to existing NPCs where thematically appropriate. Also create new trainer NPCs for wilderness zones.

### Remnance Domain
- **D-06:** Remnance stays completely hidden for v1.0. Do NOT implement any unlock mechanism. The discovery will be gated behind future LLM-driven quests and world events, not a mechanical trigger. Remove Remnance discovery from Phase 9 scope entirely.

### Wilderness NPC Density
- **D-07:** No fixed NPC-per-zone quota. Placement must be organic and driven by zone flavor, not formulaic.
- **D-08:** Merchants appear only where traffic or loot naturally accumulates (e.g., near dungeon exits, crossroads).
- **D-09:** Trainers are thematically matched to zone terrain and biome. Not every zone needs every skill trainer.
- **D-10:** Faction scouts/agents are sparse and selective — NOT in every zone. In future milestones they may track players instead of being stationary.
- **D-11:** Rest camps are occasional, not guaranteed per zone. Only where it makes geographic/narrative sense.
- **D-12:** NEVER remove existing NPCs from any zone. Only add new ones. User must authorize any NPC removal.

### Recipe Learning
- **D-13:** Wire learn_recipe() to trainer interactions and quest rewards. Non-default recipes must become acquirable in gameplay.

### Triggers
- **D-14:** Add area.trigger() calls to zone specs for on_enter and on_first_visit events — starter quest hooks, discovery moments, zone-entry flavor text.

### Crafting Stations
- **D-15:** Add engineering workbench to Vael's Crossing (currently missing). Add basic fire pits to wilderness zones where camps exist.

### Claude's Discretion
- Specific trainer-to-NPC assignments (which existing NPC gets which trainer_id)
- Specific new NPC names, descriptions, and placement room choices
- Trigger text content and placement
- Number of new NPCs per zone (guided by D-07 through D-12)
- Training cost formulas (Scales amounts, material requirements)
- Which recipes are learned from which trainers vs quest rewards

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Skill and Training System
- `world/skill_definitions.py` — SKILL_DEFINITIONS (21+ skills), TRAINER_REGISTRY
- `world/skill_engine.py` — trainer_session(), get_skill_value()
- `commands/skill_commands.py` — CmdTrain implementation

### Crafting and Recipes
- `world/crafting_engine.py` — learn_recipe(), RECIPE_REGISTRY
- `world/crafting_definitions.py` — Recipe definitions, STATION_REQUIREMENTS
- `world/models.py` — CharacterRecipe model

### Area Builder (for zone edits)
- `world/area_builder.py` — npc() with trainer_id, trigger(), material()
- `world/areas/vaels_crossing.py` — Hub city (54 NPCs, 6 crafting stations)
- `world/areas/ashreach_plains.py` — Plains zone (3 NPCs, 2 stations)
- `world/areas/reth_foothills.py` — Mountain zone (3 NPCs, 0 stations)
- `world/areas/cantera_edge.py` — Forest zone (3 NPCs, 1 station)
- `world/areas/stormhaven_coast.py` — Coastal zone (3 NPCs, 1 station)

### Trigger System
- `world/trigger_engine.py` — fire_triggers(), supported events
- `world/action_vocabulary.py` — Available trigger actions (13 types)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `world/area_builder.py:npc()` — accepts trainer_id kwarg, stores on npc_obj.db.trainer_id + adds tag
- `world/area_builder.py:trigger()` — stores trigger dicts on room.db.triggers
- `world/crafting_engine.py:learn_recipe()` — creates CharacterRecipe record, ready to call
- `world/skill_definitions.py:TRAINER_REGISTRY` — maps trainer_id to skill + quality config

### Established Patterns
- NPCs created via area.npc() with faction, dialogue attrs, ambient echoes
- Triggers fire in definition order with once-per-character and cooldown support
- Crafting stations tagged via room.tags.add("crafting_{station}", category="crafting_station")

### Integration Points
- Zone spec files are the primary edit targets — add npc(), trigger(), and station tags
- TRAINER_REGISTRY in skill_definitions.py needs entries for new trainers
- RECIPE_REGISTRY in crafting_definitions.py may need entries for trainer-taught recipes

</code_context>

<specifics>
## Specific Ideas

- Ashreach Plains: fishing trainer near river/lake area, herbalism for grassland plants
- Reth Foothills: climbing trainer in mountain terrain, mining skill trainer near cave
- Cantera Edge: tracking trainer in deep forest, foraging trainer
- Stormhaven Coast: swimming trainer, navigation trainer near docks
- Vael's Crossing guild quarters: 2-3 general trainers covering combat, subterfuge, diplomacy skills
- Engineering workbench needed in Vael's Crossing (currently only forge, campfire, alchemy bench)

</specifics>

<deferred>
## Deferred Ideas

- Flight network expansion — deferred to Phase 12 or future milestone (D-02)
- Remnance discovery mechanism — deferred to LLM-quest milestone (D-06)
- Faction agents that track players — future milestone mechanic (D-10)
- Vendor buy/sell commands — Phase 12 or future (no buy/sell economy yet)

</deferred>

---

*Phase: 09-content-activation*
*Context gathered: 2026-04-01*
