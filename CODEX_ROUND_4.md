# Repository Health Check Report

## 1. Executive Summary

Overall assessment: this repo is directionally strong but operationally uneven. It has a recognizable architecture, several good subsystem boundaries, and a serious attempt at Evennia-native world simulation. It is not cleanly production-ready in its current state because multiple core runtime paths have drifted out of sync with the model layer and with the repo's own stated design.

Top risks:

- Real player-death flow is broken by a stale import in the banking/death path.
- Mob spawning is carrying stale field names across both persistence and runtime counting.
- Recovery/rest stabilization systems exist mostly as isolated modules, not as end-to-end game lifecycle behavior.
- Combat persistence claims are stronger than the implementation appears to support.
- Tests are materially behind the code and are not trustworthy as a readiness signal.

Top strengths:

- The codebase does have a coherent intended shape: `commands` for interface, `typeclasses` for Evennia integration, `world` for gameplay/services.
- Lazy imports are used aggressively and mostly correctly to contain circular dependency risk.
- Several systems are conceptually well-factored: abilities, inventory, guilds, quests, dialogue, world state, zone building.
- Startup orchestration is centralized instead of being scattered across random modules.

Production-readiness judgment: not ready for confident deployment without a focused stabilization pass.

Coherence judgment: more coherent than fragmented at the macro level, but badly affected by architecture drift and stale wiring at the subsystem seams.

## 2. System Map

Major subsystems:

- `server/conf/*`: Evennia and Django configuration, startup hooks, optional plugin hooks, session/search/parser extension points.
- `commands/*`: static command sets plus dynamic command generation for area content.
- `typeclasses/*`: Evennia-facing object model for accounts, characters, rooms, exits, objects, mobs, scripts, and channels.
- `world/*`: gameplay engines and services: combat, guilds, quests, dialogue, banking, spawning, recovery, movement, death, triggers, OOB updates, area loading.
- `world/models.py`: persistent data for recipes, quests, spawn records, topic knowledge, and other game state.
- `tests/*`: mostly unit-style tests, many mock-heavy, limited evidence of true Evennia integration testing.

Intended interaction model:

- Evennia settings point command/typeclass entry points into this repo.
- Character/account/session lifecycle hooks delegate into `world` services.
- Startup hooks load areas, initialize spawn state, and start recurring background behavior.
- Commands mutate character/world state through `world` engines rather than embedding all logic directly in command classes.
- Persistent models back long-lived world state while `db`/`ndb` attrs handle live runtime state.

Important architectural observations:

- The repo is trying to be a service-oriented Evennia game, not a pile of ad hoc commands. That is the right direction.
- The weakest point is not structure, it is integration discipline. Too many systems are implemented as modules with comments implying lifecycle behavior, but without the final hook-up that makes them actually authoritative.
- There is visible drift between old field names, old compatibility assumptions, and current model/typeclass behavior.
- There are multiple placeholder extension points still present in live code, which increases ambiguity about what is actually active.

## 3. Critical Findings

### 1. Broken player death path

- Severity: Critical
- Confidence: Confirmed
- Area / subsystem: Death lifecycle, banking, combat
- File(s) involved: `world/banking.py:286`, `world/banking.py:310`, `world/combat_engine.py:509`, `world/world_state.py:19`
- Explanation: `world.combat_engine.handle_player_death` calls `world.banking.on_character_death`. That function imports `DOMAIN_NAMES` from `world.world_state`, but `world.world_state` defines `ALL_DOMAINS`, not `DOMAIN_NAMES`.
- Why it matters: A real player death can raise at runtime inside a critical state transition. That is not a cosmetic defect. It means character death handling is not trustworthy.
- Recommended fix: Replace the stale constant import with the actual canonical domain list, then add an integration test that kills a player through the real combat/death path.

### 2. SpawnRecord persistence is out of sync with the model

- Severity: Critical
- Confidence: Confirmed
- Area / subsystem: Spawning, persistence, startup
- File(s) involved: `world/models.py:419`, `world/migrations/0008_rename_mob_template_key.py:11`, `world/mob_spawner.py:472`
- Explanation: The persistent model field is `mob_template_key`, and migration `0008` explicitly renamed the old field. `world.mop_spawner.initialize_spawn_records` still tries to populate `mob_template`.
- Why it matters: Spawn record creation and startup reconciliation are working from stale schema assumptions. This can break initialization or silently corrupt spawn bookkeeping.
- Recommended fix: Remove all remaining runtime references to `mob_template`, standardize on `mob_template_key`, and add a test that initializes spawn records against a real test database.

### 3. Mob counting still uses the old attribute name

- Severity: High
- Confidence: Confirmed
- Area / subsystem: Spawning, live room population accounting
- File(s) involved: `world/mob_spawner.py:129`, `world/mob_templates.py:1657`
- Explanation: Spawn counting checks `obj.db.mob_template`, while template application writes `mob.db.mob_template_key`.
- Why it matters: The spawner can undercount already-existing mobs and overspawn duplicates. This is a direct world-consistency bug.
- Recommended fix: Rename the runtime attribute check to `mob_template_key` and add an end-to-end test covering restart/reconciliation behavior.

### 4. Recovery system is implemented but not lifecycle-wired

- Severity: High
- Confidence: Confirmed
- Area / subsystem: Recovery, rest, regeneration
- File(s) involved: `world/recovery_engine.py:147`, `world/recovery_engine.py:155`, `world/recovery_engine.py:193`, `commands/cmd_recovery.py:70`
- Explanation: `start_regen`, `stop_regen`, and `cancel_recovery` exist, but runtime references only show the manual cancel path from `cmd_recovery`. I found no lifecycle hooks invoking regen start/stop on login/logout, movement, combat transitions, or wake/sleep transitions.
- Why it matters: This is not a complete gameplay system. It is a command-side fragment with state helpers behind it. Regeneration behavior is likely dormant, inconsistent, or dependent on manual edge flows only.
- Recommended fix: Define the authoritative recovery lifecycle and wire it in one place: login/logout, movement interruption, combat interruption, sleep/rest state changes.

### 5. Stabilization-break-on-move is dead runtime logic

- Severity: High
- Confidence: Confirmed
- Area / subsystem: Node / concentration / movement integration
- File(s) involved: `world/node_helpers.py:164`, `tests/test_node_system.py:782`
- Explanation: `break_stabilization_on_move` exists and is tested, but I found no runtime call sites outside tests.
- Why it matters: A system that exists only in tests is not a system. If movement is supposed to break stabilization, current gameplay behavior does not enforce it.
- Recommended fix: Hook this into the actual movement lifecycle, likely through the character movement hook path or the existing movement lifecycle module.

### 6. Combat script persistence story is likely unsound

- Severity: High
- Confidence: Likely
- Area / subsystem: Combat, script persistence, reload behavior
- File(s) involved: `world/combat_script.py:24`, `world/combat_script.py:43`, `world/combat_script.py:979`
- Explanation: The module-level `CombatScript` is a plain class. `_get_script_class` dynamically creates a new Evennia script subclass by copying that class dict into a generated type. The code claims `self.persistent = True`, but the persistent import path for a reloaded server will point at `world.combat_script.CombatScript`, which is not obviously the generated subclass. That is a fragile design.
- Why it matters: Combat encounters surviving reloads is exactly the sort of stateful behavior that fails in production if the typeclass path is not stable.
- Recommended fix: Replace the dynamic-class pattern with a real top-level Evennia `DefaultScript` subclass and test actual reload persistence, not mocked behavior.

### 7. Group loot mode behavior contradicts its own documentation

- Severity: Medium
- Confidence: Confirmed
- Area / subsystem: Groups, loot permissions
- File(s) involved: `world/group_engine.py:317`, `world/group_engine.py:354`
- Explanation: The docstring says `need_pass` is not implemented and should be treated as personal. The actual fallback is `return None`, which behaves like free-for-all.
- Why it matters: This is a correctness and trust problem. The code lies about game rules.
- Recommended fix: Either implement `need_pass` correctly or make the fallback match the documented semantics. Then test every loot mode.

### 8. Migration state is not clean

- Severity: Medium
- Confidence: Confirmed
- Area / subsystem: Django models, schema management
- File(s) involved: `world/migrations/*`, `world/models.py`
- Explanation: `makemigrations world --check --dry-run` proposes a new migration. The app also already contains parallel `0006` migrations plus a merge migration.
- Why it matters: A non-clean migration state means the code and schema history are drifting. That is manageable in a hobby branch; it is not acceptable for disciplined production deployment.
- Recommended fix: Generate and review the pending migration, reconcile naming/index drift, and make migration cleanliness a CI gate.

### 9. Test suite is stale and not a reliable guardrail

- Severity: Medium
- Confidence: Confirmed
- Area / subsystem: Verification
- File(s) involved: `tests/test_content_integration.py:168`, `tests/test_typeclasses.py:283`, `tests/test_social.py:37`, `tests/test_combat_script.py:74`
- Explanation: There are tests asserting behavior that no longer matches the code. Example: `test_content_integration` expects `Character.at_object_creation` to reference `greeter_room`, which it does not. `test_typeclasses` expects `acct.db.command_aliases == {}`, which the account typeclass does not initialize. Social tests still build around `guild_name` even though the repo otherwise uses `guild_id`.
- Why it matters: Stale tests create false confidence and false failures at the same time. They actively obscure repo health.
- Recommended fix: Triage the test suite into current-contract tests, obsolete tests, and missing integration tests. Remove or rewrite the obsolete ones immediately.

### 10. Repo hygiene is poor enough to hide real problems

- Severity: Medium
- Confidence: Confirmed
- Area / subsystem: Repository operations, deployment hygiene
- File(s) involved: repo root, `server/`, cache directories
- Explanation: The worktree includes SQLite DB artifacts, logs, static output, Python caches, pytest cache directories, and prior AI-generated reports.
- Why it matters: This is how configuration drift, accidental commits, and environment-coupled bugs survive. It also makes audits harder because signal is buried in generated noise.
- Recommended fix: Clean `.gitignore`, remove generated state from the tracked working set, and separate runtime artifacts from source control.

### 11. Several extension points exist but are not actually active

- Severity: Low
- Confidence: Confirmed
- Area / subsystem: Evennia wiring
- File(s) involved: `server/conf/settings.py`, `server/conf/cmdparser.py`, `server/conf/at_search.py`, `server/conf/serversession.py`, `server/conf/server_services_plugins.py`, `server/conf/portal_services_plugins.py`
- Explanation: The repo contains custom parser, search hook, session class, and plugin hook modules, but the effective settings still use Evennia defaults for parser, search result handling, and session class. The service plugin modules are placeholders.
- Why it matters: Unused extension points are architecture noise. They make it harder to tell what the runtime actually is.
- Recommended fix: Either wire them for real or delete them. Placeholder modules should not live indefinitely in production code.

### 12. Social display code is drifting from canonical guild state

- Severity: Low
- Confidence: Confirmed
- Area / subsystem: Social commands, guild presentation
- File(s) involved: `commands/cmd_social.py:51`, `tests/test_social.py:37`
- Explanation: `cmd_social` reads `char.db.guild_name`, while the broader guild system appears to treat `guild_id` plus guild metadata lookup as canonical.
- Why it matters: This is not catastrophic, but it is classic data-model drift. Presentation code is depending on a field that is not clearly authoritative.
- Recommended fix: Standardize guild presentation on a single source of truth and remove `guild_name` as a pseudo-cache unless it is explicitly maintained.

## 4. Integration / Wiring Audit

Correctly wired or plausibly healthy:

- Custom typeclass bases are configured in `server/conf/settings.py`.
- Evennia command cmdset defaults resolve to this repo's `commands/default_cmdsets.py`, so the custom command layer is actually live.
- The command layer is broadly organized and registered through explicit cmdsets rather than ad hoc monkeypatching.
- Startup uses `AT_SERVER_STARTSTOP_MODULE = "server.conf.at_server_startstop"`, which gives the repo a real place to initialize world systems.
- The `world` package is treated as the service layer and is referenced from typeclasses and commands instead of burying all logic directly in one class.
- Lazy import patterns are used consistently to limit circular import damage.

Disconnected, partially connected, or incorrectly connected:

- Recovery/regeneration exists as a module but is not wired into the actual lifecycle.
- Movement does not appear to invoke node stabilization break logic.
- Domain chat typeclass exists, but default channel configuration only wires `OOCChannel`; domain channel behavior is effectively unused.
- Custom parser, search result hook, and custom session class exist but are not enabled.
- Service plugin modules exist as placeholders with no substantive behavior.
- Combat script persistence is conceptually wired but likely not stable across reloads because the typeclass definition strategy is shaky.
- Social display code still references `guild_name`, which does not look like the canonical guild state representation.
- Spawn initialization/runtime counting are still split between old and new field names.
- Tests cover several isolated helpers but often fail to prove that the real Evennia wiring works end to end.

## 5. Dead Code / Drift Audit

Strong dead-code or drift candidates:

- `server/conf/cmdparser.py`: present but not enabled.
- `server/conf/at_search.py`: present but not enabled.
- `server/conf/serversession.py`: present but not enabled.
- `server/conf/server_services_plugins.py`: placeholder.
- `server/conf/portal_services_plugins.py`: placeholder.
- `server/conf/at_initial_setup.py`: effectively a pass-through placeholder.
- `typeclasses/channels.DomainChannel`: implemented and tested, but not wired into channel creation.
- `world/node_helpers.break_stabilization_on_move`: tested helper with no runtime call site.
- `world/recovery_engine.start_regen` and `stop_regen`: implemented but not actually invoked by lifecycle code.
- Test expectations around `greeter_room`, `command_aliases`, and `guild_name`: stale contracts that no longer reflect the codebase.

Duplicate or overlapping systems:

- Guild representation appears split between `guild_id`, resolved metadata, and `guild_name` display assumptions.
- Combat script behavior is split between a plain class and a generated subclass, which is a design-level duplication of identity.
- Spawn template naming exists in both old (`mob_template`) and new (`mob_template_key`) forms.

Documentation or architecture drift:

- `need_pass` behavior in groups does not match the inline documentation.
- Recovery and stabilization helpers imply integrated gameplay behavior that does not exist in the runtime path.
- The repo advertises several custom Evennia extension points that are not actually active.

## 6. Refactor Opportunities

Ranked by engineering value versus implementation risk:

### 1. Collapse stale field aliases and schema drift

- Impact: High
- Risk: Low
- Rationale: Unify `mob_template` and `mob_template_key`, remove old branches, and make persistence and runtime naming identical.
- Expected payoff: Immediate reduction in spawn bugs and startup ambiguity.

### 2. Replace dynamic combat script class generation with a real typeclass

- Impact: High
- Risk: Medium
- Rationale: The current pattern is clever and brittle. Persistence-sensitive Evennia code should not depend on runtime-generated class identity.
- Expected payoff: Safer reload behavior and simpler reasoning about combat lifecycle.

### 3. Introduce a single authoritative lifecycle integration layer

- Impact: High
- Risk: Medium
- Rationale: Recovery, movement interruption, node stabilization, OOB updates, and death cleanup are spread across modules but not governed centrally.
- Expected payoff: Fewer orphaned systems and much clearer state transitions.

### 4. Standardize canonical character state fields

- Impact: Medium
- Risk: Low
- Rationale: Decide what is authoritative for guilds, group state, recovery state, combat state, and domain accumulators.
- Expected payoff: Less presentation drift, fewer stale attribute bugs, easier testing.

### 5. Remove or wire placeholder Evennia extension modules

- Impact: Medium
- Risk: Low
- Rationale: Dead extension points create confusion for every future maintainer.
- Expected payoff: Lower mental overhead and fewer false assumptions about runtime behavior.

### 6. Split runtime artifacts from source tree discipline

- Impact: Medium
- Risk: Low
- Rationale: The repo currently mixes source, runtime state, generated assets, and audit artifacts.
- Expected payoff: Cleaner diffs, safer deployment, less accidental drift.

### 7. Replace mock-heavy tests with true integration tests for key flows

- Impact: High
- Risk: Medium
- Rationale: The current suite validates many assumptions in isolation but does not sufficiently prove Evennia lifecycle behavior.
- Expected payoff: A realistic production-readiness signal.

## 7. Testing Gaps

Missing or weak coverage:

- Real character death through combat into banking/death cleanup.
- Spawn record initialization against the actual Django model and migration state.
- Spawn reconciliation after reboot/reload with existing mobs already in rooms.
- Combat script survival or graceful cleanup across server reload.
- Recovery lifecycle across login, logout, movement, sleep/rest, and combat interruption.
- Group loot behavior for every loot mode, especially `need_pass`.
- Command registration verification that the intended commands are actually attached to the right cmdsets in-game.
- Typeclass wiring verification that newly created accounts, characters, rooms, exits, mobs, and scripts get the expected behavior.
- Domain channel creation and permission behavior, if that feature is intended to exist.
- Session/account/character interaction tests covering puppet/unpuppet, reconnect, and persistence restoration.

Highest-priority new tests:

1. End-to-end death test from combat damage to post-death state cleanup.
2. Spawn initialization test that creates `SpawnRecord` rows and validates the `mob_template_key` contract.
3. Reboot/reconciliation test that confirms spawner counts existing mobs correctly.
4. Combat reload persistence test using the real Evennia script system.
5. Recovery lifecycle integration test covering movement and logout interruption.
6. Cmdset registration test that asserts the expected command classes are live for a character session.

Verification weakness worth calling out:

- `pytest` was not installed in the provided venv, so I could not execute the suite as-is. That is itself a repo readiness problem.
- `django check` passed and `compileall` succeeded, which only proves baseline import/syntax health, not system correctness.

## 8. Risk Register

1. Death/combat/banking path can fail at runtime due to stale constant wiring.
2. Spawn system can create invalid records or overspawn due to old field names still in active logic.
3. Stateful combat persistence may not survive reload safely.
4. Recovery and stabilization systems are conceptually present but operationally incomplete.
5. Schema migration state is drifting and not being actively policed.
6. Test suite is stale enough to mislead rather than protect.
7. Repo hygiene is weak, increasing accidental config/runtime drift risk.
8. Canonical state ownership is not consistently defined across social/guild/group systems.

## 9. Recommended Action Plan

Immediate fixes:

1. Fix the death-path constant mismatch in `world/banking.py`.
2. Replace all active `mob_template` references with `mob_template_key`.
3. Correct `need_pass` fallback behavior or disable the mode until implemented.
4. Clean the migration drift and generate the pending migration intentionally.
5. Remove or quarantine stale tests that assert obsolete contracts.

Short-term cleanup:

1. Wire recovery and stabilization into the actual lifecycle or explicitly remove those features from the active design.
2. Decide whether domain chat is a real feature; if not, remove `DomainChannel`.
3. Remove unused Evennia extension modules or explicitly enable and test them.
4. Clean `.gitignore` and purge runtime/generated artifacts from the normal repo workflow.

Medium-term architectural improvements:

1. Replace the dynamic combat script generation pattern with a stable top-level Evennia script typeclass.
2. Introduce a documented lifecycle matrix for login, logout, movement, combat start/end, sleep/rest, death, and reload.
3. Define canonical ownership for core character state and remove redundant cached fields.
4. Build a small integration test harness for Evennia flows instead of relying mostly on mocks.

Suggested order of operations:

1. Fix confirmed runtime breakages.
2. Reconcile persistence/schema naming drift.
3. Rebuild the test baseline around actual current behavior.
4. Remove dead wiring and placeholders.
5. Then attack deeper architectural cleanup such as combat script persistence and lifecycle consolidation.

## 10. Appendix

Notable patterns:

- The repo often has the right idea one layer early. The service/helper exists, but the final hook-up is missing.
- Comments and docstrings are not consistently trustworthy. Several describe intended behavior rather than actual behavior.
- The architecture is strong enough to salvage without a rewrite. The right move is disciplined consolidation, not reinvention.

Open questions:

- Is domain chat an intended near-term feature or abandoned work?
- Is combat supposed to survive server reloads, or is that merely aspirational?
- Is recovery meant to be passive ambient regen, explicit rest-only behavior, or both?
- Are group memberships intentionally `ndb`-heavy and session-scoped, or is persistence still planned?

Areas requiring runtime verification or manual testing:

- Real Evennia reload with active combat encounters.
- Character reconnect/logout during recovery and during corpse/loot grace periods.
- Zone bootstrap on a non-empty database with existing spawn records and live mobs.
- Session puppet/unpuppet interactions with account permissions, channels, and OOB publishing.
- New character/account creation flow through actual cmdset/typeclass initialization.

## Top 10 Concrete Fixes

1. Fix `world/banking.py` to use `ALL_DOMAINS` instead of `DOMAIN_NAMES`.
2. Replace `mob_template` with `mob_template_key` everywhere in `world/mob_spawner.py`.
3. Add a real death-path integration test covering combat to post-death cleanup.
4. Add a real spawn initialization test against the Django model layer.
5. Make `need_pass` match its documented fallback or remove it from valid loot modes.
6. Wire recovery start/stop/cancel into actual lifecycle hooks.
7. Wire movement to break stabilization if that mechanic is intended.
8. Replace dynamic combat script type creation with a stable top-level script class.
9. Generate and review the pending migration, then make migration cleanliness mandatory.
10. Remove or rewrite stale tests that no longer describe current behavior.

## Top 10 Suspected Dead-Code Candidates

1. `server/conf/cmdparser.py`
2. `server/conf/at_search.py`
3. `server/conf/serversession.py`
4. `server/conf/server_services_plugins.py`
5. `server/conf/portal_services_plugins.py`
6. `server/conf/at_initial_setup.py`
7. `typeclasses/channels.py::DomainChannel`
8. `world/node_helpers.py::break_stabilization_on_move`
9. `world/recovery_engine.py::start_regen`
10. Test expectations built around `greeter_room`, `command_aliases`, and `guild_name`

## Top 10 Files/Modules I Should Inspect First

1. `world/mob_spawner.py`
2. `world/banking.py`
3. `world/combat_engine.py`
4. `world/combat_script.py`
5. `world/recovery_engine.py`
6. `world/movement_lifecycle.py`
7. `world/session_lifecycle.py`
8. `world/models.py`
9. `commands/default_cmdsets.py`
10. `server/conf/settings.py`

## Fastest Path To Materially Improve Repo Health In 1-2 Days

1. Fix the two confirmed runtime breakages: death constant mismatch and spawn field-name drift.
2. Clean migration drift and ensure the database schema matches the current model code.
3. Delete or disable obviously inactive extension points so the runtime surface area is honest.
4. Triage stale tests into keep, rewrite, or delete; then restore a runnable minimal test baseline.
5. Wire recovery and stabilization into actual lifecycle hooks, or explicitly cut them from the active feature set.
6. Clean repo hygiene so generated state stops obscuring source-level changes.

