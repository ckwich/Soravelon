# Phase 1: Patrol, Commands, and Flight Paths - Context

**Gathered:** 2026-03-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Complete all server-side Milestone 0 systems: patrol mobs walking authored routes with disposition-based combat engagement, a shared action vocabulary powering dynamic commands and triggers on rooms/mobs/items, command prefix matching with player alias support, and the Dragon Courier multi-leg flight transit system.

</domain>

<decisions>
## Implementation Decisions

### Patrol Behavior
- **D-01:** Patrol encounter delay is builder-configurable per patrol definition (`encounter_delay` field). Some mobs check disposition instantly on arrival, others emote first then check.
- **D-02:** Patrol mobs check disposition in BOTH directions — when mob arrives in a room with players AND when a player enters a room containing a patrol mob. Continuous threat awareness.
- **D-03:** Combat engagement is configurable per mob via `combat_enabled` flag. Caldenmere and other invulnerable mobs set this to false. Guard patrols set it to true.
- **D-04:** Patrol echo radius is configurable per patrol definition (`echo_radius` field). Uses BFS from mob's current room.

### Action Vocabulary
- **D-05:** Implement all action handlers that have backing systems NOW (give_item, take_item via inventory_engine; modify_standing via world_state; log_world_event via WorldEventLog). Only stub actions whose systems don't exist yet (set_quest_flag, open_dialogue, spawn_mob).
- **D-06:** Add `modify_attunement` action type to the vocabulary — zone attunement changes from triggers (node events, lore discoveries). Uses existing `update_zone_attunement()`.
- **D-07:** Total action vocabulary: teleport, teleport_to_mob, echo, give_item, take_item, set_quest_flag (stub), modify_standing, spawn_mob (stub), despawn_self, open_dialogue (stub), log_world_event, modify_attunement.

### Flight Paths
- **D-08:** Flight points discovered by visiting the room (auto-discover on enter) AND talking to the Dragon Courier NPC to register. Discovery unlocks the point; NPC interaction is required to book flights.
- **D-09:** Pricing is base fare per leg + Standing discount (Consortium faction). Higher Standing = cheaper flights. Discount tiers TBD by planner.
- **D-10:** Flights are MULTI-LEG real-time traversal, NOT instant teleport. Each leg takes 30+ seconds with timed echo messages describing geography passing beneath the player. Cost increases per leg.
- **D-11:** Player can `disembark` at any stop along the route. They are NOT locked to the final destination.
- **D-12:** During flight, player has full command access except movement commands. Can chat, check inventory, use abilities, read messages — but cannot walk/move.
- **D-13:** Flight network is a graph with explicit edges defined by builders via `area.flight_point()` (marks a room as a stop) and `area.flight_route()` (defines connection between stops with cost and leg echoes).

### Command Prefix Resolution
- **D-14:** Ambiguous prefixes return an error with the match list: "Did you mean: attack, attune?" Player must type more characters. No silent auto-resolution.
- **D-15:** Player aliases stored in `character.db.aliases` — persistent across sessions and server restarts.
- **D-16:** Aliases support chaining up to 3 commands via semicolons (e.g., `buff` = `cast shield; cast haste; cast blessing`).
- **D-17:** Aliases NEVER override system commands.

### Trigger System
- **D-18:** Multiple triggers on the same event fire in definition order (list index in `room.db.triggers`). Builder controls priority.
- **D-19:** Trigger chaining is depth-limited to 3 levels. A teleport trigger can fire on_enter in the destination, but recursion beyond 3 is blocked.

### Custom Command Discoverability
- **D-20:** Mob/item descriptions naturally hint at available interactions (builder writes the hints).
- **D-21:** Custom commands that act as exits/teleports have a `visible_in_exits` boolean. When true, they appear in the room's exit list. When false, they're hidden (quest-gated or discovery-based).

### Patrol Mob Spawning
- **D-22:** Tests use `create_object(SoravelonMob)` + attach PatrolScript directly. Architecture must be clean enough that the future spawn system can adopt the same PatrolScript attachment pattern seamlessly.

### Claude's Discretion
- Flight path echo text content and timing (30s minimum per leg, specific messages are creative work)
- Exact Standing discount percentages for flight pricing
- PatrolScript tick interval optimization (currently 1s per the Session 10 prompt — may tune)
- Trigger depth-limit error messaging

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Patrol System
- `world/node_helpers.py` — Contains `get_rooms_in_radius()` BFS pattern to reuse for `find_path()`
- `world/mob_disposition.py` — `get_mob_behavior(mob, character)` returns behavior string for disposition checks
- `typeclasses/mobs.py` — `SoravelonMob` typeclass with affix/disposition integration

### Area Builder
- `world/area_builder.py` — Existing AreaBuilder with 11 methods; this phase adds `patrol()`, `custom_command()`, `trigger()`, `flight_point()`, `flight_route()`

### Action Vocabulary Backing Systems
- `world/inventory_engine.py` — `pick_up()`, `drop_item()` for give_item/take_item actions
- `world/world_state.py` — `modify_standing()`, `update_zone_attunement()`, `log_world_event()` for standing/attunement/event actions
- `world/banking.py` — May be needed for flight path fare deduction

### Triggers
- `typeclasses/rooms.py` — `SoravelonRoom` with existing `at_object_receive()` hook to extend
- `typeclasses/mobs.py` — `SoravelonMob` with existing lifecycle hooks

### Existing Architecture Docs
- `C:\Obsidian\brain\Soravelon\soravelon-architecture.md` — ADRs, Scripts vs TickerHandler matrix
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md` — Disposition system, behavior vocabulary
- `C:\Obsidian\brain\Soravelon\soravelon-areaspec.md` — AreaBuilder pattern, zone field reference
- `C:\Obsidian\brain\Soravelon\soravelon-builder.md` — Builder permissions model
- `C:\Obsidian\brain\Soravelon\soravelon-commands.md` — Command system design

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `world/node_helpers.py:get_rooms_in_radius()` — BFS over room exits, same pattern for `find_path()`
- `world/mob_disposition.py:get_mob_behavior()` — Returns "aggressive"/"territorial"/"passive"/"friendly" — used directly by PatrolScript
- `world/area_builder.py` — Idempotent zone loading pattern reusable for flight point registration
- `world/world_state.py:log_world_event()` — Ready-to-use for action vocabulary's log_world_event action

### Established Patterns
- `(bool, str)` return tuples from all engine functions
- SaverDict copy pattern for list attribute mutations (copy → mutate → assign)
- Tag-based lookups for zone/room/mob identification
- Lazy imports inside methods to avoid circular dependencies

### Integration Points
- `server/conf/at_server_startstop.py` — May need flight path registry initialization
- `typeclasses/rooms.py:at_object_receive()` — Extend for trigger firing
- `typeclasses/mobs.py:at_death()` — Extend for on_mob_death triggers
- `typeclasses/characters.py:at_object_creation()` — Add visited_rooms, fired_triggers, discovered_flight_points

</code_context>

<specifics>
## Specific Ideas

- Caldenmere (the walking golem city) is just a patrol mob with `combat_enabled=False`, `echo_radius` set to the full zone, and custom commands (`climb leg`, `climb down`) attached via `custom_command()`. No special-cased code.
- Flight path echoes should describe the geography passing beneath — forests, mountains, plains, cities visible from the air. These are authored per-route by builders.
- The `visible_in_exits` boolean on custom commands enables quest-gated exits that appear only after a trigger fires to set a flag.

</specifics>

<deferred>
## Deferred Ideas

- Time of day system (on_time_of_day triggers stored but cannot fire until time system exists)
- Quest flag checking in conditions (set_quest_flag action is stubbed)
- NPC dialogue integration (open_dialogue action is stubbed)
- Mob spawn runtime system (spawn_mob action is stubbed; patrol mobs created manually for now)

None — discussion stayed within phase scope otherwise.

</deferred>

---

*Phase: 01-patrol-commands-and-flight-paths*
*Context gathered: 2026-03-24*
