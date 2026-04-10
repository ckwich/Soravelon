# Phase 6c: NPC Dialogue & Crafting - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the NPC dialogue system (keyword-based topic dialogue, Standing-tier greetings, dynamic hints, keyword extraction, ambient NPC behavior) and the crafting framework (recipe registry with discovery, quality variance from skill level, basic crafting output for Cooking/Smithing/Alchemy). NPCs become interactive world inhabitants, and players can produce useful items through trade skills.

</domain>

<decisions>
## Implementation Decisions

### NPC Dialogue System
- **D-01:** Keyword-based topic dialogue per vault spec. Player commands: talk/greet (greeting + hints), ask about <topic> (topic query), say (freeform broadcast, keyword extraction), tell <npc> (directed say). accept/decline for quest offers.
- **D-02:** Standing-tier greetings: hostile, unfriendly, neutral, acknowledged, friendly, honored, exalted, betrayal. Template system selects tier from Standing + Trust. Dialogue system provides text at that tier.
- **D-03:** Topic response nodes with priority stack: quest_complete > quest_failed > quest_active > betrayal > exalted > honored > ... > scholar_present > warden_present > dragon_present > network_high > reputation_high > default. First match wins. Every topic MUST have a default response.
- **D-04:** Dynamic hint system. After every greeting, available hints display in brackets. Hints are dynamic per player (filtered by Standing tier, active quests, world-state dimensions, class/profession). Only non-zero skills shown. Capped at readable number (research determines 3-5).
- **D-05:** Keyword extraction: direct topic match → synonym matching (TOPIC_SYNONYMS static dict) → partial match → generic fallback showing available topics.
- **D-06:** Quest offers appear inline with dialogue. accept/decline commands. Quest offer trigger: NPC has quest available + player doesn't have it active + meets prerequisites + appropriate Standing tier.
- **D-07:** Build exactly as documented in vault. Interesting additions from Claude are welcome.

### NPC Ambient Behavior
- **D-08:** Idle echoes: minimum 4 per NPC, fired on timer with variance (base ± variance seconds). Per vault spec.
- **D-09:** Reactive echoes: fire from zone state change hooks (combat_nearby, node_active, quest_complete, player_enters, etc.).
- **D-10:** Ambient architecture: Claude decides between single global ambient ticker vs per-NPC TickerHandler subscriptions based on performance analysis.

### NPC Data Model
- **D-11:** NPCDialogueDefinition: greeting_tiers dict, topics dict (topic_key → {condition: text}), base_hints, tier_hints, quest_hints, network_hints, scholar_hints, warden_hints.
- **D-12:** NPCAmbientDefinition: idle_echoes list, idle_interval, idle_variance, reactive_echoes dict.
- **D-13:** KnownTopicRecord: Django model tracking which topics each character has learned from each NPC (for hint suppression).
- **D-14:** TOPIC_SYNONYMS: static Python dict, authored globally (not per NPC). "wolf" maps to "wolves" for every NPC.

### Crafting System
- **D-15:** Recipe system with quality variance from skill level. Recipes define required ingredients + skill level + output item. Quality/success based on skill check — even with the recipe you can still fail ("burn the food").
- **D-16:** Static recipe registry + discovery. Some recipes known by default (basic cooking). Others require finding recipe items in world or learning from trainers. CharacterRecipe model tracks which recipes each character knows.
- **D-17:** Three crafting professions with basic output: Cooking (makes food — HP regen consumables), Smithing (repairs equipment, basic weapons/armor), Alchemy (craft) (makes potions, reagents).
- **D-18:** Engineering (craft) is SEPARATE from Engineering domain. Craft skill = gear repair, device building. Domain = combat companion, traps. Non-Engineers can repair their own gear.
- **D-19:** Crafting commands: craft <recipe>, cook <recipe>, smith <recipe>, brew <recipe>. Each requires appropriate station/location (campfire for cooking, forge for smithing, etc.).

### Claude's Discretion
- MAX_HINTS_DISPLAYED value (3-5)
- Known topic persistence strategy (persist vs session-reset)
- Ambient ticker architecture (global vs per-NPC)
- Multi-NPC room response behavior (how many NPCs respond to 'say')
- Recipe quality formula details
- Crafting station implementation (room tag? object in room?)
- Crafting time mechanic (instant? short delay?)

</decisions>

<specifics>
## Specific Ideas

- "Build it to the documentation but I welcome any interesting additions" — stick to vault spec but creative enhancements welcome
- Quest offers feel like conversation decisions, not UI clicks
- NPCs should feel like people in a place, not quest kiosks
- Say vs tell distinction: say broadcasts to room (multiple NPCs may respond), tell targets specific NPC
- Merchant dialogue integration: separate command set for buy/sell, but 'talk <merchant>' still works for lore/hints

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### NPC Dialogue
- `C:\Obsidian\brain\Soravelon\soravelon-dialogue.md` — COMPLETE dialogue system spec: player commands, greeting tiers, topic response nodes, priority stack, hint system, keyword extraction, quest offer integration, ambient behavior, data models, area builder reference

### NPC Behavior Context
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md` §Faction Territory Expression — How zones feel different based on faction control, ambient echo pools
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md` §Mob Disposition System — Standing/Trust/ancestry disposition computation that dialogue system uses for greeting tier

### Crafting Context
- `C:\Obsidian\brain\Soravelon\soravelon-skills.md` §General Proficiency Skill List — Cooking, Smithing, Alchemy (craft), Engineering (craft) skill definitions
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` §Domain Resources §Alchemy — Reagents as pre-crafted consumable stock (Alchemy crafting output)

### Existing Code
- `world/mob_disposition.py` — get_mob_disposition() returns float used for Standing tier in dialogue
- `world/world_state.py` — get_standing(), modify_standing() for faction standing queries
- `world/ancestry_engine.py` — ancestry traits for ancestry-driven dialogue variants
- `world/oob_publisher.py` — Push dialogue/quest state updates to client

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `world/mob_disposition.py:get_mob_disposition()` — Returns float. Dialogue system maps this to Standing tier for greeting selection.
- `world/world_state.py:get_standing()` — Direct faction standing query for tier-based topic responses.
- `world/oob_publisher.py` — Push quest accept/decline, dialogue state to client.
- `world/area_builder.py` — NPC definitions in area specs. Extend with dialogue and ambient definitions.
- `world/action_vocabulary.py` — Action handlers for quest consequences that modify NPC behavior.

### Established Patterns
- Keyword-based commands: existing command parser uses Evennia's cmdhandler. Dialogue commands follow same pattern.
- TickerHandler for periodic processing: ambient echoes follow same pattern as other tickers.
- Static Python registries: TOPIC_SYNONYMS follows same pattern as ABILITIES dict, ANCESTRY_DATA dict.
- Django models for relational data: KnownTopicRecord, CharacterRecipe follow existing model patterns.

### Integration Points
- `commands/default_cmdsets.py` — Register dialogue commands (talk, ask, say/tell override, accept, decline) and crafting commands
- `world/area_builder.py` — Extend for NPC dialogue definitions and ambient behavior definitions in area specs
- `server/conf/at_server_startstop.py` — Register ambient NPC ticker if using global approach
- Crafting output creates items via `world/inventory_engine.py:pick_up()` or direct creation

</code_context>

<deferred>
## Deferred Ideas

- LLM-driven NPC responses — future feature per vault doc
- NPC conversation memory — future feature (Standing/Trust provides implicit memory)
- NPC-to-NPC dialogue (ambient eavesdropping) — content phase
- Full recipe list — content authoring phase
- Advanced crafting (enchanting, upgrading, material quality) — dedicated crafting expansion
- Merchant buy/sell command set — separate economy phase or inline

</deferred>

---

*Phase: 06c-npc-dialogue-and-crafting*
*Context gathered: 2026-03-26*
