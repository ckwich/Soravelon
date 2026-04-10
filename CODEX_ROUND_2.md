# Repository Health Check Report

## 1. Executive Summary
- Overall assessment: structurally ambitious, partially disciplined, not production-ready in its current worktree state.
- Top risks: broken NPC/quest wiring, scripted movement blocked by character movement guards, reconnect/logout state exploits, builder reload non-idempotence, and stale persistence assumptions.
- Top strengths: explicit command registration, clear engine-oriented module split, broad unit-test presence, and consistent use of lazy imports to keep Evennia/Django circularity under control.
- Production-readiness judgment: fail. There are multiple confirmed runtime-path defects in core player-facing systems.
- Coherence judgment: mixed. The repo has a coherent intended architecture, but the implementation is drifting in important seams: commands vs builder DSL, persistent models vs ndb session state, and authored content vs actual runtime wiring.

The repo also has a dirty worktree in core files. This report audits the current workspace state, not a clean committed baseline.

## 2. System Map
- `server/conf/`: Evennia/Django configuration, startup hooks, ticker registration, initial load.
- `commands/`: primary player command surface. `commands/default_cmdsets.py` is the main registration point.
- `typeclasses/`: account, character, room, exit, object, mob, and script behavior.
- `world/`: almost all gameplay engines and registries.
- `world/areas/`: authored content DSL using `AreaBuilder`.
- `world/models.py`: persistent relational state for standings, skills, quests, bank, spawn records, recipes, dialogue topics.
- `tests/`: broad unit-heavy test suite, mostly mock-driven.
- `web/`: mostly scaffold-level web code, not materially integrated into current gameplay architecture.

Intended interaction model:
- Content authors build zones via `AreaBuilder`.
- Startup loads every area file in `at_server_start`.
- Rooms, NPCs, mobs, exits, nodes, flight points, quests, and gathering pools are wired from authored zone specs.
- Commands dispatch into `world/*_engine.py` service modules.
- Transient combat/session state lives mostly in `ndb`.
- Durable progression/state lives in Django models and selected `db` attrs.
- OOB updates are pushed centrally through `world/oob_publisher.py`.

Important architectural observations:
- The repo is trying to use a service/engine style rather than thick typeclasses. That is good.
- The repo is simultaneously carrying legacy and current systems in several places: mob spawning, quest formats, compatibility classes, action handlers, and placeholder AI hooks.
- The biggest failures are not in isolated functions. They are at system boundaries: builder to runtime, forced movement to character hooks, `db` vs `ndb`, and tests vs actual area-built objects.

## 3. Critical Findings

### F1. NPC quest/dialogue wiring is broken at the builder boundary
- Severity: Critical
- Confidence: Confirmed
- Area: Area builder, dialogue, quests
- Files: `world/area_builder.py`, `world/quest_engine.py`, `world/dialogue_engine.py`, `commands/cmd_dialogue.py`
- Explanation: `AreaBuilder.npc()` tags NPCs with `npc_id` but never assigns `npc_obj.db.npc_id`. Runtime quest/dialogue code reads `npc.db.npc_id` directly for quest offering, hint tracking, and topic learning.
- Why it matters: Area-authored NPC quest offers can silently fail even though the content is present and tests look green.
- Recommended fix: Set `npc_obj.db.npc_id = npc_id` in `AreaBuilder.npc()`. Add an integration test that builds an area NPC and verifies `talk` can surface an authored quest.

### F2. Chain quest acceptance crashes on the happy path
- Severity: High
- Confidence: Confirmed
- Area: Dialogue / quest UX
- Files: `world/quest_engine.py`, `commands/cmd_dialogue.py`
- Explanation: Quest completion sets `character.ndb.pending_quest_offer = {"npc": None, ...}` for chain offers. `CmdAccept` explicitly allows `npc is None` for validation, then immediately dereferences `npc.db.npc_name`.
- Why it matters: A completed quest chain can hard-fail when the player tries to accept the next quest.
- Recommended fix: Handle `npc is None` end-to-end in `CmdAccept` and `_build_quest_oob_payload`, with a generic acceptance message and OOB payload.

### F3. Scripted travel and forced transport are being blocked by player movement guards
- Severity: Critical
- Confidence: Confirmed
- Area: Movement lifecycle, flight, respawn, teleport, node transitions
- Files: `typeclasses/characters.py`, `world/scripts/flight_script.py`, `world/combat_engine.py`, `world/action_vocabulary.py`, `world/scripts/node_script.py`
- Explanation: `Character.at_before_move()` blocks movement while `ndb.in_flight` or when overloaded. Multiple systems use normal `move_to()` with hooks enabled. Evennia `move_to()` calls `at_pre_move` by default. That means:
  - Flight script tries to move players while `ndb.in_flight` is still true.
  - Respawn uses normal `move_to()`, so overload can block respawn.
  - Teleports and node-layer swaps are subject to player movement restrictions.
- Why it matters: This is a systemic runtime break. The Dragon Courier path is especially likely to deadlock.
- Recommended fix: Use `move_hooks=False` or a dedicated force-move path for system-driven transport, or distinguish player-issued movement from scripted movement in `at_before_move`.

### F4. Disconnect/reconnect resets combat and survival state and can be exploited
- Severity: Critical
- Confidence: Confirmed
- Area: Character lifecycle, persistence
- Files: `typeclasses/characters.py`
- Explanation: `at_post_puppet()` resets `ndb.hp`, `ndb.stamina`, `ndb.active_effects`, cooldowns, and resources. `at_pre_unpuppet()` removes the player from combat. This lets players disconnect to escape combat and return with restored core volatile state.
- Why it matters: This is a production-breaking exploit. It undermines combat, attrition, and encounter integrity.
- Recommended fix: Decide which state must persist across reconnects and restore it from durable storage or combat scripts. At minimum, do not reset HP/stamina/effects/resources blindly on reconnect.

### F5. Death penalty code no longer targets the state the repo actually uses
- Severity: High
- Confidence: Confirmed
- Area: Death handling, progression persistence
- Files: `world/banking.py`, `world/world_state.py`, `world/skill_engine.py`, `world/base_attributes.py`
- Explanation: `on_character_death()` claims to wipe uncommitted XP but only clears `character.ndb.session_xp`, which is not the live accumulator mechanism. Domain XP uses `ndb.domain_xp_*`, skills use `ndb.skill_use_*`, and stat growth uses `ndb.stat_xp_accumulators`.
- Why it matters: Death penalties are materially weaker than the code/comments claim. Players keep progression that the design says should be lost.
- Recommended fix: Either implement real accumulator clearing for all live progression buckets or remove the claim from code/comments/tests and redesign the death penalty honestly.

### F6. Logout persistence is inconsistent and loses some live progression
- Severity: High
- Confidence: Confirmed
- Area: Session persistence
- Files: `typeclasses/characters.py`, `world/skill_engine.py`, `world/world_state.py`, `typeclasses/scripts.py`
- Explanation:
  - Logout commits domain XP and stat growth.
  - Logout does not commit skill accumulators.
  - Safety flush commits domain XP and skill accumulators.
  - Safety flush does not commit stat growth.
- Why it matters: What survives depends on how the session ends. Clean logout, crash, and timer flush produce different outcomes.
- Recommended fix: Standardize one persistence contract. Commit domain XP, skill accumulators, and stat growth together on logout and in safety flushes.

### F7. Ability post-processing treats message strings as success flags
- Severity: High
- Confidence: Confirmed
- Area: Ability engine / combat correctness
- Files: `world/ability_engine.py`, `world/combat_engine.py`
- Explanation: Effect handlers mostly return strings, not `(success, message)`. `_post_ability_resource_hook()` uses the handler return value as truthiness for builder/resource logic. Misses and resisted effects still produce non-empty strings, so they can incorrectly trigger resource generation and follow-up behavior.
- Why it matters: Core combat math and domain resource behavior are wrong under failure conditions.
- Recommended fix: Normalize effect handlers to return structured success results and thread that through `use_ability()`.

### F8. Builder reload is not idempotent for triggers, custom commands, or patrol scripts
- Severity: High
- Confidence: Confirmed
- Area: Area loading / startup coherence
- Files: `world/area_builder.py`, `server/conf/at_server_startstop.py`
- Explanation:
  - `_set_room_attrs()` resets some authored lists but not `db.triggers` or `db.custom_commands`.
  - `trigger()` appends to existing triggers.
  - `custom_command()` replaces by key only if the key is re-authored; removed commands persist.
  - `_finalize_patrols()` adds `PatrolScript` every build without checking for an existing script.
- Why it matters: Rebuilds can accumulate duplicate behavior and preserve deleted behavior. That is classic architecture drift at runtime.
- Recommended fix: Explicitly reset or reconcile authored behavior lists on every build and dedupe persistent scripts by stable ownership key.

### F9. Several action-vocabulary handlers are hard broken by invalid Evennia search API usage
- Severity: High
- Confidence: Confirmed
- Area: Action vocabulary
- Files: `world/action_vocabulary.py`
- Explanation: Handlers call `evennia.search_object(dbref=...)`. Evennia’s manager does not accept a `dbref` keyword. Those paths raise `TypeError`.
- Why it matters: `teleport`, `give_item` by existing object ID, and `take_item` by existing object ID are not safe code paths.
- Recommended fix: Use `search_object("#<id>")` or `search_object(searchdata, use_dbref=True)` consistently. Add direct unit tests against the actual Evennia search API contract.

### F10. Dialogue hint conditions encode the wrong game model
- Severity: Medium
- Confidence: Confirmed
- Area: Dialogue engine
- Files: `world/dialogue_engine.py`, `world/guild_engine.py`
- Explanation:
  - `scholar_present` checks `primary_domain == "scholar"` or `"scholar" in subclass`.
  - `warden_present` checks `guild == "wardens"`.
  - The repo’s actual guild/domain model uses domain IDs like `naturalism` and guild IDs like `verdance`, `ironblood`, etc.
- Why it matters: Scholar and Warden-specific hint paths are effectively dead or misrouted.
- Recommended fix: Rebase these conditions on actual domain/guild/subclass IDs used by `guild_engine.py`.

### F11. `on_examine` is authored as a supported trigger event but is never emitted
- Severity: Medium
- Confidence: Confirmed
- Area: Trigger system
- Files: `world/area_builder.py`, `world/trigger_engine.py`
- Explanation: `trigger()` advertises `on_examine` as valid, but no command or typeclass path calls `fire_triggers(..., "on_examine", ...)`.
- Why it matters: Content authors can define behavior that never fires, and there is no visible warning.
- Recommended fix: Either wire `on_examine` into the actual inspection command path or remove it from the supported trigger surface.

### F12. Compound status effects are only partially implemented
- Severity: Medium
- Confidence: Confirmed
- Area: Status effects / combat
- Files: `world/status_effects.py`
- Explanation:
  - `steam` and `discharge` explicitly have `pass` in tick handling where burst behavior is described.
  - `petrify` is supposed to break on damage, but live combat code never sets `target.ndb.took_damage_this_round`.
- Why it matters: The combat system advertises compound interactions that are incomplete or nonfunctional.
- Recommended fix: Either implement the missing behavior or downgrade the design/docs/tests to match reality.

### F13. Test strategy is masking real integration failures
- Severity: High
- Confidence: Confirmed
- Area: Test architecture
- Files: `tests/test_dialogue.py`, `tests/test_quest_engine.py`, `tests/test_content_integration.py`
- Explanation: Dialogue and quest tests manually assign `npc.db.npc_id` on mocks. They do not validate that area-built NPCs actually expose the fields runtime systems require.
- Why it matters: The test suite gives false confidence on the builder-to-runtime seam.
- Recommended fix: Add content-integration tests that create NPCs through `AreaBuilder.npc()` and then exercise `get_available_quest_for_npc`, `talk`, and `ask`.

### F14. The migration state is not clean
- Severity: Medium
- Confidence: Confirmed
- Area: ORM / deployment hygiene
- Files: `world/models.py`, `world/migrations/*`
- Explanation: `makemigrations --check --dry-run` produces a new migration (`0008_...`) for index renames and `AutoField`/`BigAutoField` drift.
- Why it matters: The schema is not in a clean committed state, which is a deployment risk and a sign of model/migration drift.
- Recommended fix: Reconcile model field types and committed migrations, then keep `makemigrations --check` green in CI.

## 4. Integration / Wiring Audit
Correctly wired:
- Custom typeclass defaults are configured in `server/conf/settings.py`.
- Core command surface is explicitly registered in `commands/default_cmdsets.py`.
- Startup hook wires global tickers for world state, banking, spawn records, wandering, and ambient NPC behavior.
- `FILE_HELP_ENTRY_MODULES` points at `world.help_entries`.
- `INSTALLED_APPS` includes `world`.
- Area files are actually loaded at startup, with second-pass unresolved cross-zone exit handling.
- SpawnRecord runtime is wired into startup via `initialize_spawn_records()`.
- OOB messages are centralized instead of being scattered through game logic.

Disconnected, partially connected, or incorrectly connected:
- Area-built NPCs are not fully wired to quest/dialogue runtime because `db.npc_id` is missing.
- Chain quest offers are partially wired in `quest_engine` but not safely handled in `CmdAccept`.
- `on_examine` trigger support exists on paper but not in runtime dispatch.
- LLM/AI quest system exists only as character attrs and comments. There is no real integration layer, service, model, or command path.
- Scripted travel/respawn/teleport paths are not coherently integrated with movement restrictions.
- Builder reload logic does not fully reconcile authored state, so runtime objects drift away from authored content.
- Death handling comments and behavior no longer match the actual accumulator architecture.

## 5. Dead Code / Drift Audit
- Top-level `README.md`, `world/README.md`, `typeclasses/README.md`, `server/README.md`, and `web/README.md` are mostly stock Evennia scaffolding and do not describe the real system.
- `typeclasses.objects.Object`, `typeclasses.rooms.Room`, and similar compatibility wrappers are mostly legacy scaffolding.
- `world/mob_spawner.py` still carries legacy bootstrap paths alongside the SpawnRecord path. That is architectural duplication.
- `world/action_vocabulary.py` carries handlers that appear unused in content (`open_dialogue`, `teleport`, `teleport_to_mob`, `take_item`).
- AI-related character fields (`questline_choices`, `active_llm_quest_id`) are placeholders with no live subsystem behind them.
- `server/conf/server_services_plugins.py` and `portal_services_plugins.py` are empty stubs.
- `tests/test_content_integration.py` is mostly string/import validation and does not function as true runtime integration coverage.
- Comments in `world/node_helpers.py` still say scholar/stabilizer tracking is deferred even though the function now returns counts.
- Status-effect comments describe burst and break-on-damage logic that the implementation does not carry through.
- The repo already contains prior health-check markdown files at the root, which suggests review output is accumulating as artifacts rather than being folded into maintained docs.

## 6. Refactor Opportunities
1. High impact / low-medium risk: Introduce a single forced-move helper for system-driven transport.
   Payoff: fixes flight, respawn, node swaps, teleports, and future scripted travel in one place.
2. High impact / medium risk: Make `AreaBuilder` explicitly reconcile authored state instead of append/update-in-place.
   Payoff: removes reload drift and duplicate scripts/triggers/cmdsets.
3. High impact / medium risk: Formalize a session-state persistence contract.
   Payoff: eliminates reconnect exploits and inconsistent logout/crash behavior.
4. High impact / medium risk: Normalize engine return contracts, especially abilities and actions.
   Payoff: removes truthiness bugs and clarifies combat correctness.
5. Medium impact / low risk: Add a typed NPC runtime schema helper instead of raw `db` field assumptions.
   Payoff: prevents more builder/runtime field mismatches.
6. Medium impact / low risk: Split legacy mob spawn helpers from the authoritative SpawnRecord runtime.
   Payoff: less architectural ambiguity and easier maintenance.
7. Medium impact / low risk: Replace stock scaffold docs with actual subsystem docs.
   Payoff: better onboarding and lower architecture drift.

## 7. Testing Gaps
- Highest-priority missing tests:
  - Area-built NPC can offer an authored quest through real dialogue flow.
  - Chain quest accept path with `npc=None`.
  - Dragon Courier full journey moves a player between stops under real character hooks.
  - Respawn while overloaded.
  - Reconnect/logout does not reset or erase prohibited state.
  - Builder reload does not duplicate triggers/custom commands/patrol scripts.
  - Action vocabulary handlers using actual Evennia search APIs.
  - Death penalty actually affects the real uncommitted progression buckets.
  - Compound status effects with live combat damage and break conditions.

- Weak tests:
  - Quest/dialogue tests are too mock-heavy and hand-author fields the builder is supposed to provide.
  - Content integration tests validate imports and source text, not runtime behavior.
  - Status-effect tests cover presence/modifiers more than end-to-end combat integration.

- Critical systems under-tested:
  - Command registration under real Evennia cmdset resolution.
  - Rebuild/restart idempotence.
  - Character reconnect lifecycle.
  - Forced transport paths.
  - Persistent model migration cleanliness.

## 8. Risk Register
1. Core NPC quest content can be authored successfully but fail at runtime.
2. Players can likely bypass or reset combat/survival state through disconnect/reconnect.
3. Flight and other scripted movement paths are at risk of hard failure due to hook misuse.
4. Repeated server starts can drift runtime content away from authored content.
5. Combat resource behavior is incorrect under failed/resisted abilities.
6. Death and logout persistence semantics are internally inconsistent.
7. Schema drift is present and not being kept migration-clean.
8. The test suite is broad but not trustworthy on the most integration-sensitive seams.

## 9. Recommended Action Plan
Immediate:
1. Fix `AreaBuilder.npc()` to write `db.npc_id`.
2. Fix `CmdAccept` and quest OOB helpers to tolerate `npc=None`.
3. Introduce a force-move path and patch flight/respawn/teleport/node transitions to use it.
4. Stop resetting combat/survival state blindly on reconnect.
5. Fix `search_object(dbref=...)` calls in `world/action_vocabulary.py`.

Short-term cleanup:
1. Commit skill accumulators and stat growth consistently on logout and safety flush.
2. Fix death penalty logic to target real accumulator state.
3. Reconcile `AreaBuilder` reload behavior for triggers/custom commands/patrol scripts.
4. Correct dialogue condition model checks for scholar/warden hints.
5. Add migration-cleanliness enforcement.

Medium-term architectural improvements:
1. Remove or isolate legacy spawn paths.
2. Replace stock scaffolding docs with real subsystem docs.
3. Decide whether AI/LLM questing is real roadmap or dead placeholder and either build it or delete the surface area.
4. Expand integration tests around area-built content and Evennia lifecycle hooks.

Suggested order:
1. Runtime blockers and exploits.
2. Builder/runtime wiring.
3. Persistence correctness.
4. Reload/idempotence.
5. Test and migration hygiene.

## 10. Appendix
Notable patterns:
- Good: explicit command registration, central OOB publisher, modular engine layout, heavy use of lazy imports.
- Bad: heavy dependence on untyped `db`/`ndb` contracts, append-heavy builder mutation, and comments that claim behaviors not implemented anymore.

Runtime verification performed:
- `compileall` over `commands server tests typeclasses web world`: passed.
- Django `check`: passed.
- `makemigrations world --check --dry-run`: failed with pending migration drift.
- Full `pytest` run was not possible from the available repo environment because the local venv did not have `pytest` installed.

Open questions:
- Are disconnects during combat intended to be allowed, or should they be treated as forfeits/deaths?
- Is group state intentionally session-only for production, or is persistence expected later?
- Is the LLM quest system still on the roadmap, or is it stale placeholder surface?

Areas requiring manual runtime testing:
- Dragon Courier booking, leg transitions, and disembark path.
- Respawn while overloaded.
- NPC quest offering from real area-built NPCs.
- Builder reload after removing a trigger/custom command/patrol from authored content.
- Reconnect behavior mid-combat and after status effects/resources are active.

## Top 10 Concrete Fixes
1. Set `npc_obj.db.npc_id` in `AreaBuilder.npc()`.
2. Guard `CmdAccept` and `_build_quest_oob_payload` for `npc=None`.
3. Add a forced-move helper and use it for flight, respawn, node swaps, teleports, and scripted flee movement.
4. Stop resetting HP/stamina/effects/resources on every puppet event.
5. Replace `search_object(dbref=...)` calls with valid Evennia search usage.
6. Commit skill accumulators on logout and stat growth in safety flushes.
7. Rework death penalty to clear actual live progression accumulators.
8. Reconcile `AreaBuilder` authored state on rebuild, including triggers/custom commands/patrol scripts.
9. Fix dialogue condition checks to use real guild/domain/subclass identifiers.
10. Add integration tests for builder-built NPC quest flow and flight traversal.

## Top 10 Suspected Dead-Code Candidates
1. `typeclasses/characters.py` LLM quest placeholders: `questline_choices`, `active_llm_quest_id`, `SeerQuest` comments.
2. `world/action_vocabulary.py` `open_dialogue` handler.
3. `world/action_vocabulary.py` `teleport` handler.
4. `world/action_vocabulary.py` `teleport_to_mob` handler.
5. `world/action_vocabulary.py` `take_item` handler.
6. `world/mob_spawner.py` `_schedule_respawn()` legacy path.
7. `world/mob_spawner.py` `spawn_zone()` / `spawn_room_mobs()` legacy bootstrap path.
8. `typeclasses/objects.py:Object` compatibility wrapper.
9. `typeclasses/rooms.py:Room` compatibility wrapper.
10. Empty plugin stubs in `server/conf/server_services_plugins.py` and `server/conf/portal_services_plugins.py`.

## Top 10 Files/Modules I Should Inspect First
1. `typeclasses/characters.py`
2. `world/area_builder.py`
3. `commands/cmd_dialogue.py`
4. `world/quest_engine.py`
5. `world/action_vocabulary.py`
6. `world/scripts/flight_script.py`
7. `world/ability_engine.py`
8. `world/status_effects.py`
9. `world/banking.py`
10. `server/conf/at_server_startstop.py`

## Fastest Path To Materially Improve Repo Health In 1-2 Days
1. Fix NPC ID wiring, chain quest accept, and invalid `search_object` calls.
2. Introduce one safe forced-move path and patch flight/respawn/node/teleport callers.
3. Remove the reconnect exploit by preserving or reloading survival/combat state instead of resetting it.
4. Make logout and safety flush persist all live progression buckets consistently.
5. Make `AreaBuilder` idempotent for triggers/custom commands/patrol scripts.
6. Add 5 integration tests: area-built NPC quest offer, chain accept, flight traversal, reconnect state, rebuild idempotence.
7. Re-run `makemigrations --check`, reconcile drift, and make it part of CI.
