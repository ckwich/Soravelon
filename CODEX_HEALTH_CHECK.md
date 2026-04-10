# Repository Health Check Report

## 1. Executive Summary
Overall assessment: ambitious, partly coherent, not production-ready.

Top risks:
- World boot is not actually idempotent; node-enabled zones appear to create duplicate persistent artifacts on restart.
- Core state is split across Evennia `db`/`ndb`, Django models, and authored zone data without a consistently enforced source of truth.
- Several runtime paths that matter in play are broken right now: mob death cleanup, chain quest acceptance, mob-applied status effects, and regular mob spawn counting.
- Verification is weak enough that you cannot currently trust a green or red test run.

Top strengths:
- The intended architecture is legible: commands are mostly thin dispatchers, the `world/` package is the service layer, and typeclass defaults are explicitly configured in [server/conf/settings.py](/C:/Dev/Evennia/soravelon/server/conf/settings.py#L38C1).
- Command registration is explicit and broad in [commands/default_cmdsets.py](/C:/Dev/Evennia/soravelon/commands/default_cmdsets.py#L20C1).
- Dynamic area commands are genuinely wired into runtime cmdsets in [world/area_builder.py](/C:/Dev/Evennia/soravelon/world/area_builder.py#L738C1) and [commands/cmd_dynamic.py](/C:/Dev/Evennia/soravelon/commands/cmd_dynamic.py#L1C1).
- Help entries, custom typeclasses, and the `world` Django app are wired correctly in settings.

Production-readiness judgment: not ready. This repo can probably support local feature iteration, but it is not in a state where I would trust restart behavior, content rebuild correctness, or regression detection.

Coherence judgment: one strong intended architecture with real drift layered onto it. Not fragmented beyond repair, but definitely drifting.

## 2. System Map
Major subsystems:
- `typeclasses/`: runtime Evennia entities and lifecycle hooks.
- `commands/`: user command surface plus combat/dynamic command cmdsets.
- `world/`: service layer, content DSL, models, registries, scripts, combat, quests, inventory, gathering, node systems, patrols, OOB publishing.
- `server/conf/`: settings and startup lifecycle hooks.
- `tests/`: 43 test files, but the runner path is currently unreliable.

Intended interaction model:
- Commands dispatch into `world/*_engine.py` style modules.
- Typeclasses hold object identity and lifecycle hooks, then delegate behavior into `world/`.
- Area files build persistent world objects through `AreaBuilder`, and startup rebuilds zones from authored specs via [_load_all_zones()](/C:/Dev/Evennia/soravelon/server/conf/at_server_startstop.py#L104C1).
- Persistent relational state lives in [world/models.py](/C:/Dev/Evennia/soravelon/world/models.py#L1C1), while transient combat/session state lives in `ndb`.
- OOB/UI push behavior is centralized in `world/oob_publisher.py`.

Architectural observations:
- The codebase wants `world/` to be the authoritative game domain layer. It is close, but not consistent.
- Content authoring is split between Python DSL area files and JSON serializer input, but the two paths are not actually equivalent.
- There are multiple partial migrations in flight: inventory authority, equipment schema, node layering, quest UX, and future AI scaffolding.

## 3. Critical Findings

### 1. Non-idempotent node boot duplicates persistent room/script artifacts
- Severity: Critical
- Confidence: Confirmed
- Area: Startup, world boot, node system
- Files: [server/conf/at_server_startstop.py](/C:/Dev/Evennia/soravelon/server/conf/at_server_startstop.py#L91C1), [world/area_builder.py](/C:/Dev/Evennia/soravelon/world/area_builder.py#L1034C1), [world/zone_object.py](/C:/Dev/Evennia/soravelon/world/zone_object.py#L11C1), [world/node_helpers.py](/C:/Dev/Evennia/soravelon/world/node_helpers.py#L204C1)
- Issue: startup always calls `_load_all_zones()`, zone build always calls `_initialize_node()` when configured, and `initialize_node()` always creates new Layer 1 rooms and a new persistent `NodeScript`.
- Why it matters: restarts can accumulate duplicate Layer 1 rooms, duplicate node scripts, duplicate ticking behavior, and orphaned state.
- Recommended fix: make node initialization reconciliation-based, not create-only. Resolve an existing zone object and existing node script first, reuse/update existing Layer 1 rooms by `layer0_room_id`, and fail if duplicates already exist.

### 2. Mob death path does not remove the mob object
- Severity: Critical
- Confidence: Confirmed
- Area: Combat, lifecycle, persistence
- Files: [world/combat_engine.py](/C:/Dev/Evennia/soravelon/world/combat_engine.py#L423C1), [typeclasses/mobs.py](/C:/Dev/Evennia/soravelon/typeclasses/mobs.py#L142C1)
- Issue: `handle_mob_death()` calls `mob.at_death()`, spawns a corpse, moves loot, and returns. It never deletes, despawns, or tombstones the defeated mob.
- Why it matters: dead mobs can remain in-room, interact badly with wander/combat systems, and coexist with corpse/respawn outcomes.
- Recommended fix: define one authoritative death contract. Either delete the mob immediately after corpse/loot handling, or mark it dead and remove it from the room while all downstream systems honor that state.

### 3. Regular mob counting is wrong after templates are applied
- Severity: Critical
- Confidence: Confirmed
- Area: Spawning
- Files: [world/mob_spawner.py](/C:/Dev/Evennia/soravelon/world/mob_spawner.py#L117C1), [world/mob_templates.py](/C:/Dev/Evennia/soravelon/world/mob_templates.py#L1652C1)
- Issue: non-named spawn counting compares `obj.key == spawn_def["mob"]`, but template application overwrites `mob.key` with the display name.
- Why it matters: spawn caps are miscounted, so zone load and respawn behavior can over-spawn regular mobs.
- Recommended fix: count regular mobs by stable identity (`db.mob_template` or a tag), not display key.

### 4. Chain quest auto-offers can crash on `accept`
- Severity: High
- Confidence: Confirmed
- Area: Quests, dialogue commands
- Files: [world/quest_engine.py](/C:/Dev/Evennia/soravelon/world/quest_engine.py#L477C1), [commands/cmd_dialogue.py](/C:/Dev/Evennia/soravelon/commands/cmd_dialogue.py#L404C1)
- Issue: quest completion stores `pending_quest_offer = {"npc": None, ...}`, but `CmdAccept` later unconditionally dereferences `npc.db`.
- Why it matters: a normal chained quest flow can explode at player command time.
- Recommended fix: support NPC-less system offers explicitly in `CmdAccept` and OOB payload construction.

### 5. Mob ability status-effect application uses the wrong API
- Severity: High
- Confidence: Confirmed
- Area: Combat, status effects
- Files: [world/combat_script.py](/C:/Dev/Evennia/soravelon/world/combat_script.py#L376C1), [world/status_effects.py](/C:/Dev/Evennia/soravelon/world/status_effects.py#L142C1)
- Issue: `apply_effect()` is called with `source=` and `chance=` kwargs that the function does not accept.
- Why it matters: mob ability status application is broken.
- Recommended fix: normalize on one effect application API and keep probability handling outside `apply_effect()`.

### 6. Starter-kit items bypass the authoritative inventory model
- Severity: High
- Confidence: Confirmed
- Area: Inventory, character bootstrap
- Files: [world/ancestry_engine.py](/C:/Dev/Evennia/soravelon/world/ancestry_engine.py#L277C1), [world/item_spawner.py](/C:/Dev/Evennia/soravelon/world/item_spawner.py#L26C1), [world/inventory_engine.py](/C:/Dev/Evennia/soravelon/world/inventory_engine.py#L1C1)
- Issue: starter items are created directly into the character’s contents, but no `InventoryItem` rows are created.
- Why it matters: inventory state is split immediately for new characters; equip/drop/weight/query behavior can become inconsistent.
- Recommended fix: route all character inventory acquisition through `inventory_engine`, including starter kits, crafting output, and any other direct grants.

### 7. Zone rebuild is not a real sync; stale authored data persists
- Severity: High
- Confidence: Confirmed
- Area: Content pipeline
- Files: [world/area_builder.py](/C:/Dev/Evennia/soravelon/world/area_builder.py#L292C1), [world/area_builder.py](/C:/Dev/Evennia/soravelon/world/area_builder.py#L1047C1)
- Issue: room/zone list attributes are only initialized if falsy. Removing content from authored files does not remove stale DB data.
- Why it matters: world state drifts silently away from authored content over time.
- Recommended fix: rebuild author-owned lists as replacements, not append-only caches.

### 8. Zone load errors are swallowed and boot continues
- Severity: High
- Confidence: Confirmed
- Area: Startup robustness
- Files: [server/conf/at_server_startstop.py](/C:/Dev/Evennia/soravelon/server/conf/at_server_startstop.py#L133C1)
- Issue: zone load exceptions are printed and startup continues.
- Why it matters: you can boot a partially loaded world without an operational stop condition.
- Recommended fix: fail fast on build errors in production boot, or at minimum surface a hard degraded-state flag and abort player access.

### 9. Verification path is broken
- Severity: High
- Confidence: Confirmed
- Area: Testing, release readiness
- Files: [CLAUDE.md](/C:/Dev/Evennia/soravelon/CLAUDE.md#L24C1)
- Issue: `evennia test tests/` fails under default settings because the repo depends on custom settings; the documented runner `evennia test --settings server.conf.settings tests/` also failed during audit with an Evennia config import error.
- Why it matters: you do not currently have a trustworthy repo-level verification command.
- Recommended fix: define and document one canonical test entrypoint that actually runs in CI and locally, then prune or quarantine stale tests.

### 10. `on_first_visit` semantics are not enforced by the framework
- Severity: Medium
- Confidence: Confirmed
- Area: Triggers
- Files: [typeclasses/rooms.py](/C:/Dev/Evennia/soravelon/typeclasses/rooms.py#L96C1), [world/area_builder.py](/C:/Dev/Evennia/soravelon/world/area_builder.py#L707C1)
- Issue: room entry always fires `on_first_visit`; “first visit” is only approximated if authored triggers remembered to set `once_per_character=True`.
- Why it matters: the event name lies. Future content authors will get incorrect behavior by default.
- Recommended fix: encode first-visit logic in the trigger engine or rename the event to what it actually is.

### 11. Node layer-override lookup likely uses the wrong room key
- Severity: Medium
- Confidence: Likely
- Area: Node system
- Files: [world/scripts/node_script.py](/C:/Dev/Evennia/soravelon/world/scripts/node_script.py#L237C1)
- Issue: overrides are keyed using `layer0_room.db.room_id or layer0_room.key`, but room identity elsewhere is tag-based, not `db.room_id`.
- Why it matters: authored `layer_1_overrides` can fail to match and silently fall back.
- Recommended fix: use the room’s `room_id` tag as the canonical lookup key.

### 12. `modify_node_failure` can select the wrong object
- Severity: Medium
- Confidence: Confirmed
- Area: Action vocabulary
- Files: [world/action_vocabulary.py](/C:/Dev/Evennia/soravelon/world/action_vocabulary.py#L276C1)
- Issue: it resolves `zone_id` by grabbing the first object tagged with that zone, not the zone object.
- Why it matters: rooms, exits, mobs, and the zone object all share that tag namespace.
- Recommended fix: filter to `object_type=zone_object` before selecting.

### 13. JSON zone serializer is not feature-parity with `AreaBuilder`
- Severity: Medium
- Confidence: Confirmed
- Area: Content pipeline
- Files: [world/zone_serializer.py](/C:/Dev/Evennia/soravelon/world/zone_serializer.py#L1C1), [world/area_builder.py](/C:/Dev/Evennia/soravelon/world/area_builder.py#L580C1), [world/area_builder.py](/C:/Dev/Evennia/soravelon/world/area_builder.py#L952C1)
- Issue: the serializer claims the schema mirrors `AreaBuilder`, but it does not support `item()` or `gathering_pool()`.
- Why it matters: documented authoring parity is false.
- Recommended fix: either implement missing mappings or narrow the serializer’s claims.

### 14. Equipment authoring schema is drifting
- Severity: Medium
- Confidence: Confirmed
- Area: Items, content authoring
- Files: [world/areas/equipment_catalog.py](/C:/Dev/Evennia/soravelon/world/areas/equipment_catalog.py#L35C1), [world/areas/vaels_crossing.py](/C:/Dev/Evennia/soravelon/world/areas/vaels_crossing.py#L2146C1), [world/item_spawner.py](/C:/Dev/Evennia/soravelon/world/item_spawner.py#L59C1)
- Issue: current schema uses `armor_value` and `stat_bonuses`, but older content still uses `armor`, `stat_bonus`, and `stat_scaling`.
- Why it matters: portions of the content set almost certainly do not grant intended stats/armor.
- Recommended fix: pick one schema, migrate all authored content to it, and add validation.

### 15. Surviving mobs keep encounter status effects after combat
- Severity: Medium
- Confidence: Confirmed
- Area: Combat cleanup
- Files: [world/combat_script.py](/C:/Dev/Evennia/soravelon/world/combat_script.py#L782C1)
- Issue: end-of-combat cleanup clears effects for players only.
- Why it matters: mobs can carry encounter-scoped effects into later fights.
- Recommended fix: define which effects persist across encounters and clean all others on both players and mobs.

### 16. New-player guidance reads stale/non-authoritative quest state
- Severity: Medium
- Confidence: Confirmed
- Area: Character UX, quest state
- Files: [typeclasses/characters.py](/C:/Dev/Evennia/soravelon/typeclasses/characters.py#L156C1)
- Issue: guidance checks `self.db.active_quest_ids`, while the quest engine is model-backed via `CharacterQuest`.
- Why it matters: player hints can be wrong, and it signals leftover state-model drift.
- Recommended fix: query quest state through quest service functions only.

### 17. AI integration does not actually exist
- Severity: Low
- Confidence: Confirmed
- Area: AI/architecture
- Files: [typeclasses/characters.py](/C:/Dev/Evennia/soravelon/typeclasses/characters.py#L64C1), [world/dialogue_engine.py](/C:/Dev/Evennia/soravelon/world/dialogue_engine.py#L100C1)
- Issue: there is future-facing LLM scaffolding and comments, but I found no real model client, service integration, queue, or trust boundary implementation.
- Why it matters: if the repo is supposed to already have AI behavior, it doesn’t. If it is future work, the current code should say that more clearly.
- Recommended fix: either remove/cordon off the scaffolding or build a real AI service boundary with explicit failure handling and moderation policy.

## 4. Integration / Wiring Audit
Correctly wired:
- `world` app is registered in [server/conf/settings.py](/C:/Dev/Evennia/soravelon/server/conf/settings.py#L38C1).
- Custom base typeclasses are configured in [server/conf/settings.py](/C:/Dev/Evennia/soravelon/server/conf/settings.py#L41C1).
- Help entries are configured in [server/conf/settings.py](/C:/Dev/Evennia/soravelon/server/conf/settings.py#L54C1) and defined in [world/help_entries.py](/C:/Dev/Evennia/soravelon/world/help_entries.py#L1C1).
- Character command registration is explicit in [commands/default_cmdsets.py](/C:/Dev/Evennia/soravelon/commands/default_cmdsets.py#L20C1).
- Input preprocessing is actually wired through [typeclasses/characters.py](/C:/Dev/Evennia/soravelon/typeclasses/characters.py#L301C1) and [world/command_preprocessor.py](/C:/Dev/Evennia/soravelon/world/command_preprocessor.py#L127C1).
- Dynamic area commands are attached via persistent cmdsets in [world/area_builder.py](/C:/Dev/Evennia/soravelon/world/area_builder.py#L738C1).
- Startup tickers for world state, banking, spawn, wandering, and ambient NPC behavior are registered in [server/conf/at_server_startstop.py](/C:/Dev/Evennia/soravelon/server/conf/at_server_startstop.py#L33C1).

Disconnected / partial / incorrect:
- Node startup is declared idempotent but is not.
- JSON zone loading is marketed as equivalent to Python DSL authoring but is not.
- Starter inventory grants bypass inventory-model registration.
- Quest chain offers are only half-integrated.
- Mob ability status application path is wired to the wrong signature.
- `wander_system` relies on `db.is_dead`; I found test references but no convincing production path that sets it.
- AI systems are conceptual scaffolding, not an integrated subsystem.

## 5. Dead Code / Drift Audit
Dead or suspicious:
- Compatibility scaffolds: [typeclasses/objects.py](/C:/Dev/Evennia/soravelon/typeclasses/objects.py#L13C1) `ObjectParent`, `Object`, and [typeclasses/rooms.py](/C:/Dev/Evennia/soravelon/typeclasses/rooms.py#L28C1) `Room` look like template holdovers.
- [typeclasses/scripts.py](/C:/Dev/Evennia/soravelon/typeclasses/scripts.py#L40C1) `WorldEventScript` looks unintegrated.
- [server/conf/at_initial_setup.py](/C:/Dev/Evennia/soravelon/server/conf/at_initial_setup.py#L1C1), [server/conf/server_services_plugins.py](/C:/Dev/Evennia/soravelon/server/conf/server_services_plugins.py#L1C1), and sibling template plugin files are untouched scaffolds.
- LLM-related character fields are placeholder drift unless there is hidden out-of-repo integration.
- Top-level [README.md](/C:/Dev/Evennia/soravelon/README.md#L1C1) is still the generic Evennia scaffold and is misleading for this project.

Documentation drift:
- `CLAUDE.md` documents a test command that did not work during audit.
- The repo contains prior audit artifacts (`HEALTH_CHECK_REPORT.md`, `LAUNCH_READINESS_REPORT.md`) that are likely already stale unless they are treated as generated deliverables.

## 6. Refactor Opportunities
1. Unify state authority around services and models.
Payoff: high. Risk: medium. Inventory and quest state are the biggest wins.

2. Make area boot reconciliation-based instead of append/update-by-side-effect.
Payoff: high. Risk: medium. This will eliminate node duplication and content drift.

3. Consolidate item/equipment schema and add validation at authoring time.
Payoff: high. Risk: low.

4. Formalize lifecycle contracts for combat death, respawn, and despawn.
Payoff: high. Risk: medium.

5. Split “authored content cache” from “live mutable runtime state” on zone/room objects.
Payoff: medium-high. Risk: medium.

6. Remove or isolate scaffolding/placeholder systems that are not live.
Payoff: medium. Risk: low.

## 7. Testing Gaps
Missing or weak:
- No trustworthy end-to-end startup verification for zone loading, command registration, or typeclass settings.
- No strong integration test for inventory authority across starter gear, pickup, crafting, quest rewards, death, and corpse recovery.
- No restart/idempotency test for node-enabled zones.
- No test guaranteeing mob death actually removes or deactivates the mob.
- No regression test for chain quest acceptance when `npc=None`.
- No content-schema validation tests for authored item definitions.
- Several current tests are stale or mock-fragile, including [tests/test_item_spawner.py](/C:/Dev/Evennia/soravelon/tests/test_item_spawner.py#L159C1) and [tests/test_room_state.py](/C:/Dev/Evennia/soravelon/tests/test_room_state.py#L243C1).

Highest-priority new tests:
- Canonical repo test bootstrap with custom settings.
- Restart twice, assert node objects/scripts do not multiply.
- Kill mob, assert defeated mob is gone and respawn behavior is correct.
- Accept chain quest with `npc=None`.
- Starter character creation, assert `InventoryItem` rows exist for starter kit.
- Validate all authored `area.item()` definitions against current equipment schema.

## 8. Risk Register
- Restarting the server may silently corrupt runtime world shape.
- World content can drift away from authored truth without obvious symptoms.
- Combat lifecycle is not fully trustworthy.
- Inventory authority is inconsistent.
- Test/CI trust is too low for safe iteration speed.
- Content authoring standards are not enforced.
- Documentation does not accurately represent current operational reality.

## 9. Recommended Action Plan
Immediate:
- Fix node initialization idempotency.
- Fix mob death cleanup.
- Fix `CmdAccept` for chain offers.
- Fix status-effect API mismatch.
- Establish one working canonical test command.

Short-term:
- Route all item grants through inventory authority.
- Migrate item/equipment schemas and add validation.
- Make zone rebuild overwrite authored lists instead of preserving stale state.
- Change startup to fail hard on zone build errors in non-dev environments.

Medium-term:
- Reconcile “DB-authored cache” vs “live runtime mutable state”.
- Add restart/integration tests around world boot, command registration, and persistence recovery.
- Remove or isolate dead scaffolding and placeholder AI/world-event code.

Suggested order:
1. Verification path.
2. Startup idempotency.
3. Combat death correctness.
4. Inventory authority.
5. Content schema cleanup.
6. Architectural simplification.

## 10. Appendix
Notable patterns:
- Good: commands are generally thin and service-oriented.
- Bad: service boundaries exist, but the authoritative state model is not consistently respected.
- Good: dynamic command registration is explicit and real.
- Bad: content systems rely too heavily on mutable DB attributes that are treated as both authored truth and runtime cache.

Open questions:
- I did not start a live server to inspect an actual DB after multiple restarts; node duplication is confirmed by code path, not by live row count.
- I did not find real AI integration code. If it exists outside this repo, the repo should say so.
- I did not verify whether any external operational scripts compensate for the broken test runner.

Areas requiring runtime verification:
- Two consecutive boots on the same DB.
- Mob death in a real room with corpse and respawn timing.
- Character creation through the full Evennia path, including starter gear.
- Quest chain completion followed by `accept`.
- End-of-combat cleanup for mobs vs players.

## Top 10 concrete fixes
1. Make node initialization reconcile existing zone/node artifacts instead of blindly creating new ones.
2. Delete or fully despawn defeated mobs in `handle_mob_death()`.
3. Count spawned mobs by stable template/tag identity, not display key.
4. Fix `CmdAccept` to support `pending_quest_offer["npc"] is None`.
5. Fix mob status-effect application to use the real `apply_effect()` signature.
6. Route starter-kit grants through `inventory_engine`.
7. Replace append-only authored list behavior with authoritative rebuild behavior in `AreaBuilder`.
8. Fail startup on zone load errors outside local dev.
9. Create one working canonical test command and enforce it in CI.
10. Normalize item/equipment content to one schema and reject legacy fields at build time.

## Top 10 suspected dead-code candidates
1. [typeclasses/scripts.py](/C:/Dev/Evennia/soravelon/typeclasses/scripts.py#L40C1) `WorldEventScript`
2. [typeclasses/objects.py](/C:/Dev/Evennia/soravelon/typeclasses/objects.py#L21C1) `Object`
3. [typeclasses/objects.py](/C:/Dev/Evennia/soravelon/typeclasses/objects.py#L13C1) `ObjectParent`
4. [typeclasses/rooms.py](/C:/Dev/Evennia/soravelon/typeclasses/rooms.py#L28C1) `Room`
5. [server/conf/at_initial_setup.py](/C:/Dev/Evennia/soravelon/server/conf/at_initial_setup.py#L18C1)
6. [server/conf/server_services_plugins.py](/C:/Dev/Evennia/soravelon/server/conf/server_services_plugins.py#L18C1)
7. `server/conf/portal_services_plugins.py`
8. LLM placeholder fields in [typeclasses/characters.py](/C:/Dev/Evennia/soravelon/typeclasses/characters.py#L64C1)
9. `world_event_summary` placeholder path unless a real producer is added
10. Top-level stale audit artifacts if they are not regenerated as part of workflow

## Top 10 files/modules I should inspect first
1. [server/conf/at_server_startstop.py](/C:/Dev/Evennia/soravelon/server/conf/at_server_startstop.py#L1C1)
2. [world/area_builder.py](/C:/Dev/Evennia/soravelon/world/area_builder.py#L1C1)
3. [world/zone_object.py](/C:/Dev/Evennia/soravelon/world/zone_object.py#L1C1)
4. [world/combat_engine.py](/C:/Dev/Evennia/soravelon/world/combat_engine.py#L423C1)
5. [world/combat_script.py](/C:/Dev/Evennia/soravelon/world/combat_script.py#L376C1)
6. [world/mob_spawner.py](/C:/Dev/Evennia/soravelon/world/mob_spawner.py#L1C1)
7. [world/inventory_engine.py](/C:/Dev/Evennia/soravelon/world/inventory_engine.py#L1C1)
8. [world/ancestry_engine.py](/C:/Dev/Evennia/soravelon/world/ancestry_engine.py#L277C1)
9. [commands/cmd_dialogue.py](/C:/Dev/Evennia/soravelon/commands/cmd_dialogue.py#L404C1)
10. [world/zone_serializer.py](/C:/Dev/Evennia/soravelon/world/zone_serializer.py#L1C1)

## Fastest path to materially improve repo health in 1-2 days
1. Fix the canonical test runner and get one repeatable repo-wide command working.
2. Patch the four immediate runtime defects: node duplication, mob death cleanup, chain quest accept, status-effect API mismatch.
3. Add five regression tests for those exact defects.
4. Migrate starter-kit item grants onto inventory authority.
5. Add validation to reject legacy equipment fields during area build.
6. Change startup to stop on zone load failure.
7. Replace stale/generic top-level docs with one accurate operator/developer readme.

Verification note: I did not modify code. I did run the available test paths, and the current verification setup is broken enough to be a finding in its own right.
