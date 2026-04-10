# Phase 6b: Spawn System, Skills & Mob AI - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the mob spawn/respawn runtime (SpawnRecord model, mob_spawner ticker, death→respawn scheduling), mob ability AI (weighted priority selection, casting, conditions), and the full general proficiency + attunement skill system (20+ skills, passive use accumulator, deliberate practice, trainer sessions, discovery framework). This phase makes the world feel alive with respawning mobs that use abilities and gives players a deep progression layer beyond domains.

</domain>

<decisions>
## Implementation Decisions

### Spawn System
- **D-01:** SpawnRecord Django model tracks live state per spawn slot (room_id, spawn_index, active_mob_ids, respawn_at). Per vault spec in soravelon-spawn-system.md.
- **D-02:** Single global TickerHandler (60s interval) processes all pending respawns in one indexed DB query. NOT per-mob Scripts. Same efficient pattern as existing tickers.
- **D-03:** Spawn condition vocabulary: None (always), node_failure_above_N, node_active, quest_complete:id (stub → False), time_of_day:period (stub → True), unknown (log warning, spawn anyway).
- **D-04:** Death hook schedules respawn: mob.at_death() finds SpawnRecord, removes mob from active_mob_ids, schedules respawn_at when all mobs in slot are dead.
- **D-05:** Named mob handling: prestige_modifier (1.5-3.0), long respawn (2-8 hours), zone-wide announcement on respawn (not first spawn), first-engage lore description. Death writes WorldEventLog entry.
- **D-06:** Store mob.db.spawn_record_id at creation time for direct SpawnRecord lookup on death (avoid JSONField __contains query that doesn't work in SQLite).
- **D-07:** Zone initialization on server start: initialize_spawn_records() creates SpawnRecord entries for all spawn definitions. Idempotent — existing records preserved across restarts.
- **D-08:** Call-for-help cap: max 3 additional mobs per combat encounter. Tracked on room.ndb.call_for_help_count, reset on combat end.

### Mob Ability AI
- **D-09:** Weighted priority list for ability selection. Each mob ability has a weight (0.0-1.0) and optional condition. Higher weight = more likely to fire when off cooldown. Abilities authored per-mob template as data dicts (NOT from shared registry).
- **D-10:** ALL mobs have at least 1-2 abilities, not just named/elite mobs. Normal mobs get simple abilities. Magic/Rare/Legendary get progressively more.
- **D-11:** Casting time mechanic: spells with cast_time > 0 telegraph (emote fires at cast start). Resolves on round N+cast_time. Players can interrupt via Stun or Root during cast window.
- **D-12:** Mob ability cooldowns tracked on mob.ndb.ability_cooldowns dict. Cleared on death. Decremented at round end.
- **D-13:** Condition vocabulary for mob abilities: null (no condition), pack_present, hp_below_50, hp_below_25, target_rooted, target_blinded, no_target_dot.
- **D-14:** Named mob scripted sequences: trigger types (combat_start, hp_below_X, round_N, target_flees, on_death). Action types (echo, ability, spawn, call_for_help, modify_behavior, zone_echo).
- **D-15:** is_hunter flag: mobs with this flag use BFS pathfinding to chase players across rooms within detection range. NOT all aggressive mobs — only explicitly flagged ones.

### Skill System — General Proficiencies
- **D-16:** Full 20+ general proficiency system. All skills from vault: Lockpicking, Animal Handling, Beast Training, Herbalism, Tracking, Climbing, Persuasion, Intimidation, Swimming, First Aid, Appraisal, Stealth, Foraging, Node Reading, Navigation, Fishing, Engineering (craft), Cooking, Smithing, Alchemy (craft), PLUS new "Reflexes" skill (passive combat speed factor).
- **D-17:** More passive-effect skills welcome (both combat + exploration). Combat passives provide MARGINAL mechanical effects (flavor-level, not competitive). The reason to train is CONTENT ACCESS — high skill levels unlock quest options and dialogue. Not power.
- **D-18:** Three improvement methods per vault: Passive use (session accumulator in ndb, batch-commit), Deliberate practice (24hr rolling cooldown per skill), Trainer sessions (cost Scales, raise gain ceiling).
- **D-19:** Diminishing returns by tier: 0-25 full rate, 26-50 75%, 51-75 40%, 76-90 10%, 91-100 2%. Same curve as domain XP.
- **D-20:** Ancestry skill seeds wire into ancestry_engine.py's set_ancestry(). Veth (formerly Rodentia): Stealth 20, Navigation 25, Lockpicking 10, Tracking (underground) 25. Kau'roran: Swimming 30, Fishing 25, Beast Training 20, Persuasion 15. Human: no seeds. Selvar North: Tracking 20, Climbing 15, Intimidation 10. Selvar South: Lockpicking 15, Appraisal 15, Persuasion 10, Navigation (coastal) 20.
- **D-21:** Skill display command filtered by category: 'skills' shows summary. 'skills general' shows general proficiencies. 'skills attunement' shows zone/node/creature. Only non-zero skills shown.

### Skill System — Attunement
- **D-22:** Zone attunement (one per zone, 50 at launch), Node attunement (one per node type, 5), Creature attunement (one per creature type, ~30). Total ~105 skills.
- **D-23:** Attunement threshold unlocks per vault: 25 (sensory detail), 50 (hidden exits/objects), 75 (mob patterns/stabilization), 90 (enhanced magic/early warning), 100 (unique lore fragment).

### Discovery Framework
- **D-24:** Build framework for hidden discovery triggers (skill combo conditions that unlock lore fragments). Framework exists even if no discoveries authored yet. Checks run when skills change thresholds.
- **D-25:** Quest system checks skill values at runtime for skill-gated content. Skills don't know about quests — clean separation.

### Claude's Discretion
- SpawnRecord migration details
- Ticker registration in at_server_start()
- Skill registry format (Python dicts like ability_registry.py vs YAML)
- Exact passive-effect skill list beyond Reflexes
- Trainer NPC data model details
- is_hunter detection range default value

</decisions>

<specifics>
## Specific Ideas

- "Rodentia" was renamed to "Veth" — update all references in vault and code
- Combat passives grow VERY slowly through use and need training with costs increasing at higher levels
- Discovery mechanic: "the first crack in the world's secret accessible outside the main questline"
- Skill-gated quests give people a reason to train — the reward is content, not power

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Spawn System
- `C:\Obsidian\brain\Soravelon\soravelon-spawn-system.md` — COMPLETE spawn system spec: SpawnRecord model, spawn_tick(), attempt_spawn(), condition evaluator, named mob handling, zone initialization, quest spawns
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md` §Mob Stats and Variance — HP/damage ranges, speed, accuracy, evasion, resistances authored per mob template

### Mob Ability AI
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md` §Mob Ability System — Full ability schema, element/status/targeting/condition vocabularies
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md` §Named Mob Scripted Sequences — Trigger types, action types, sequence examples
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md` §Behavior Vocabulary — Aggression states, combat behaviors, mobility behaviors

### Skill System
- `C:\Obsidian\brain\Soravelon\soravelon-skills.md` — COMPLETE skill system spec: 20 general proficiencies, attunement skills, three improvement methods, data models, practice commands, ancestry seeds, discovery mechanic, grind ceiling

### Status Effects (for mob abilities)
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` §Status Effect System — Stackable/non-stackable, compound triggers, node interactions

### Existing Code
- `world/mob_affix_roller.py` — Affix system that mob spawner integrates with
- `world/zone_scaling.py` — initialize_mob_combat_stats() called during spawn
- `typeclasses/mobs.py` — SoravelonMob.initialize_for_spawn() and at_death()
- `world/ancestry_engine.py` — set_ancestry() to wire skill seeds into
- `world/models.py:CharacterSkill` — Existing model, check if it matches vault spec

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `typeclasses/mobs.py:initialize_for_spawn()` — Called after mob creation. Applies affixes, combat stats. Spawn system calls this.
- `typeclasses/mobs.py:at_death()` — Already writes room flags. Extend for SpawnRecord respawn scheduling and corpse creation.
- `world/mob_affix_roller.py` — Applies rarity-based affixes at spawn time.
- `world/zone_scaling.py:initialize_mob_combat_stats()` — Sets mob HP/damage from scale factor.
- `world/ancestry_engine.py:set_ancestry()` — Returns (bool, str). Extend to create CharacterSkill seed records.
- `world/models.py:CharacterSkill` — Already exists. May need extension for vault spec fields.
- `world/models.py:WorldEventLog` — Already exists for named mob death logging.

### Established Patterns
- Global TickerHandler for periodic processing (node_failure_tick 30s, banking_payment_tick 86400s, session_xp_safety_flush 600s). Spawn tick at 60s follows this pattern.
- ndb session accumulators: domain XP uses ndb.domain_xp_combat etc., batch-committed. Skill use accumulator follows same pattern.
- Lazy record creation: CharacterSkill records created on first use, not at character creation (except ancestry seeds).

### Integration Points
- `server/conf/at_server_startstop.py:at_server_start()` — Register spawn_tick, initialize_spawn_records() after _load_all_zones()
- `world/area_builder.py:spawn()` — Already creates spawn_definitions on rooms. Spawn system reads these.
- CombatScript (from Phase 6a) — Mob ability AI fires during mob turns in combat. is_hunter engages via CombatScript creation.

</code_context>

<deferred>
## Deferred Ideas

- Full crafting system with materials/ingredients — Phase 6c (basic) or dedicated crafting phase
- Threat engine (taunt, aggro tables) — post-launch
- Quest spawn system — quest system not built yet, stub condition evaluator
- Time-of-day spawns — time system not built, stub returns True
- Full creature attunement list — depends on complete mob roster from content phase

</deferred>

---

*Phase: 06b-spawn-system-skills-and-mob-ai*
*Context gathered: 2026-03-26*
