# Phase 11: Quest MVP - Context

**Gathered:** 2026-04-03
**Status:** Ready for planning

<domain>
## Phase Boundary

Turn the 20 authored quest specs into a playable quest system — Django model for quest state, 5 objective types, quest chains, rich reward payout via action vocabulary, and player commands for viewing/managing quests. Must be editor-friendly (builder app already has quest editing UI in development).

</domain>

<decisions>
## Implementation Decisions

### Quest Data Model
- **D-01:** New `CharacterQuest` Django model: character FK, quest_id (str), status (active/complete/failed/abandoned), progress (int), started_at, completed_at. Migration required.
- **D-02:** Hard cap of 5 active quests per player. Must abandon one to accept a new one.
- **D-03:** Most quests re-acceptable after failure/abandonment. Builder sets optional `one_chance=True` flag per quest to permanently lock failed quests.
- **D-04:** Three terminal states: complete, failed, abandoned. Failed = system-triggered (timer, NPC death, wrong choice). Abandoned = player-triggered.

### Quest Chains
- **D-05:** Linear quest chains via `next_quest_id` field on quest spec. On completion, next quest auto-offers from same (or specified) NPC. Builder sets this in editor.
- **D-06:** No branching prerequisite system for MVP. Just linear chains. Branching can be added later.

### Objective Types (5 for MVP)
- **D-07:** `kill` — Track mob kills by template key or named_id. Progress: N/M killed. Fires on mob death event.
- **D-08:** `collect` — Track items with specific item_tag in inventory. Progress: N/M collected. Checked on item pickup.
- **D-09:** `investigate` — Visit a specific room. Tied to investigation skill — may require successful `search` check at the location. Progress: 0 or 1 (boolean).
- **D-10:** `deliver` — Carry a specific item to a specific NPC. Combines collect + talk_to. Progress: 0 or 1 (boolean).
- **D-11:** `talk_to` — Talk to a specific NPC (for quest chain transitions). Progress: 0 or 1. Fires when player uses `talk` command with the target NPC.

### Quest Rewards
- **D-12:** Rewards defined as action dict list, reusing the existing action_vocabulary pattern. Each reward = `{"action_type": "...", ...params}`. Builder already knows this from trigger authoring.
- **D-13:** Supported reward action types:
  - `give_scales` — Award N Scales to carried_scales
  - `give_item` — Spawn item by template_id into player inventory (existing handler)
  - `modify_standing` — Award +/- faction standing (existing handler)
  - `learn_recipe` — Teach a recipe (existing handler)
  - `give_skill_xp` — Award N skill XP via accumulate_skill_use()
  - `teleport` — Move player to a room (existing handler, for area access rewards)
  - `spawn_mob` — Spawn a boss/NPC/mob at a location (existing handler)
  - `modify_node_failure` — Adjust node failure % up or down (new handler needed)
  - `echo` — Display reward narrative text (existing handler)
- **D-14:** Most reward types already exist as action_vocabulary handlers. Only `give_scales`, `give_skill_xp`, and `modify_node_failure` need new handlers.

### Player Commands
- **D-15:** `quest` command with subcommands: `quest` (list all active), `quest <name>` (detail), `quest abandon <name>` (drop quest). Register in CharacterCmdSet.
- **D-16:** Quest list shows: quest name, progress bar, quest giver name. Detail shows: full description, objectives with progress, rewards preview.

### Quest Engine Integration
- **D-17:** Wire `CmdAccept` in dialogue to create CharacterQuest record (currently stubbed).
- **D-18:** Wire `has_available_quest()` to check quest specs against player state (completed quests, active quests, one_chance flags).
- **D-19:** Quest progress hooks fire from existing systems: mob death → kill objectives, item pickup → collect objectives, room enter → investigate objectives, talk command → talk_to objectives.
- **D-20:** Quest completion triggers reward payout via action_vocabulary.execute_action() for each reward dict.

### Editor Integration
- **D-21:** Quest specs authored via `area.quest()` DSL method (already exists). Builder editor writes these into zone JSON. The quest engine reads quest specs from room/zone db attrs at runtime.
- **D-22:** All quest fields must be serializable to JSON for the builder: quest_id, quest_type, quest_giver, objectives (list of dicts), rewards (list of action dicts), next_quest_id, one_chance, share settings.

### Claude's Discretion
- Quest progress notification text format
- Whether investigate objectives require search check or just room visit
- Failure condition implementation details (timers, NPC death detection)
- Quest sharing mechanics (can_share, share_radius, share_cap from existing quest specs)
- Whether to implement quest_type categories (investigation, kill, fetch) as mechanical or cosmetic

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Quest Infrastructure (existing)
- `world/area_builder.py` — area.quest() method (already exists, stores quest specs)
- `commands/cmd_dialogue.py` — CmdAccept/CmdDecline (acceptance currently stubbed)
- `world/dialogue_engine.py` — has_available_quest(), get_quest_offer() (currently stubs)
- `typeclasses/characters.py` — character.db.active_llm_quest_id, questline_choices (existing attrs)

### Action Vocabulary (reward execution)
- `world/action_vocabulary.py` — ACTION_HANDLERS dict, execute_action() dispatch
- `world/world_state.py` — modify_standing() for faction rewards
- `world/crafting_engine.py` — learn_recipe() for recipe rewards
- `world/skill_engine.py` — accumulate_skill_use() for skill XP rewards
- `world/item_spawner.py` — create_item_from_template() for item rewards

### Models (migration needed)
- `world/models.py` — Existing models pattern (FactionStanding, CharacterSkill, etc.)

### Quest Content
- `world/areas/vaels_crossing.py` — 8 quest specs
- `world/areas/ashreach_plains.py` — 3 quest specs
- `world/areas/reth_foothills.py` — 3 quest specs
- `world/areas/cantera_edge.py` — 3 quest specs
- `world/areas/stormhaven_coast.py` — 3 quest specs

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `action_vocabulary.execute_action()` — Reward payout can reuse the entire trigger action dispatch system
- `area.quest()` — Already stores quest spec dicts on zone/room db attrs
- `CmdAccept/CmdDecline` — Dialogue integration point already exists, just needs quest record creation
- `trigger_engine.fire_triggers()` — Quest progress hooks can piggyback on existing event system

### Established Patterns
- Django models follow: FK to ObjectDB, unique_together constraints, auto timestamps, lazy creation
- Commands follow: `from commands.command import Command`, locks `"cmd:all()"`, subcommand dispatch
- Engine functions return `(bool, str)` tuples

### Integration Points
- `typeclasses/mobs.py:at_death()` — Hook for kill objective progress
- `world/inventory_engine.py:pickup_item()` — Hook for collect objective progress
- `typeclasses/rooms.py:at_object_receive()` — Hook for investigate objective progress
- `commands/cmd_dialogue.py:CmdTalk` — Hook for talk_to objective progress
- `commands/default_cmdsets.py` — Register CmdQuest

</code_context>

<specifics>
## Specific Ideas

- Quest engine as `world/quest_engine.py` — centralized quest logic module following the stateless engine pattern
- Progress hooks use lightweight checks: on mob death, check if killer has active quest with kill objective matching mob template
- Quest completion auto-chains: on complete, if next_quest_id exists, auto-offer the next quest (set ndb.pending_quest_offer)
- 5 of 20 quests should be fully completable end-to-end as MVP verification targets

</specifics>

<deferred>
## Deferred Ideas

- Quest timers / time-limited quests — future milestone
- Quest sharing between group members (can_share fields exist in specs but sharing deferred)
- LLM-generated quest content — Milestone 2+
- Branching prerequisite chains (requires_quest list) — future enhancement to D-05
- Quest map markers / compass directions — future UI feature

</deferred>

---

*Phase: 11-quest-mvp*
*Context gathered: 2026-04-03*
