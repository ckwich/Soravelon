# Soravelon Wave 10 Test Architecture and Verification Audit

**Date:** 2026-04-22
**Depends on:** `docs/superpowers/plans/2026-04-22-deep-gameplay-code-health-audit-plan.md`
**Follows:** `docs/superpowers/plans/2026-04-22-wave9-social-group-coop-audit.md`

## Scope
Wave 10 audited the quality of Soravelon's verification story rather than the game systems themselves. This pass focused on:

- which runtime areas have direct tests versus indirect or incidental coverage
- where the suite catches regressions versus merely proving imports
- whether the current safety net matches launch-readiness needs
- the difference between content-contract coverage and runtime behavior coverage

## Evidence Reviewed

- `tests/` directory inventory
- `tests/test_content_integration.py`
- `tests/test_help_entries.py`
- `tests/test_group_engine.py`
- `tests/test_social.py`
- `tests/test_session_lifecycle.py`
- top-level `world/` and `commands/` module inventory

## Validation Run

- `python scripts/run_tests.py tests.test_group_engine tests.test_social tests.test_help_entries tests.test_session_lifecycle tests.test_content_integration tests.test_help_command`
- Result: `77` tests passed

## Current-State Snapshot

- `tests/` currently contains `61` `test_*.py` files.
- `world/` currently contains `58` top-level Python modules.
- `commands/` currently contains `34` top-level Python modules.
- The repo has strong engine coverage in several core areas: combat, abilities, loot, vendors, quests, area contracts, and major authored hubs.
- Coverage symmetry is still uneven, especially across command modules, definition registries, lifecycle helpers, and runtime/content integration semantics.

## Findings

### High-Value Fix
- **Direct command-level coverage is much thinner than the player-facing command surface.**
  - Only a small subset of command modules has obvious direct tests by command family, while many high-traffic commands still lack focused command tests.
  - Missing or weakly-covered command surfaces include important launch paths like guild joining, abilities, vendors, loot, recovery, quest journal usage, group command dispatch, map/search/status, and loadout ergonomics.
  - Player-facing impact: a lot of the UX surface is protected mainly by engine tests and smoke imports, not by command-behavior tests that validate syntax, messaging, and error paths.
  - Recommended fix direction: add a command-surface wave focused on the highest-frequency commands first rather than trying to cover every command equally.
  - Verification needed: command-level tests for the actual parser paths players type, including failure messaging.

### High-Value Fix
- **Several integration tests still prove source-text presence rather than runtime truth.**
  - `tests/test_content_integration.py:200-205` checks for `greeter_room` by looking for a string in source.
  - `tests/test_content_integration.py:207-212` verifies respawn logic by checking that `_respawn_player` source contains the string `respawn_point`.
  - These tests are useful as cheap sentries, but they can pass while behavior is semantically broken.
  - Player-facing impact: the suite can create false confidence around critical authored/runtime glue.
  - Recommended fix direction: replace the highest-value string-presence tests with behavior-level assertions where practical, starting with spawn/respawn and greeter-room expectations.
  - Verification needed: runtime or AST-based tests that validate semantics rather than raw string presence.

### High-Value Fix
- **Registry and definition modules are not protected as strongly as the engines consuming them.**
  - Definition-heavy modules such as `ability_registry`, `dialogue_definitions`, `material_definitions`, `skill_definitions`, `lore_registry`, and `flight_registry` have limited direct invariant testing compared to execution engines.
  - Some of these surfaces are exercised transitively, but there are still too few tests that assert authored-data contracts in a targeted way.
  - Player-facing impact: data drift can survive until runtime, especially when new content is added quickly.
  - Recommended fix direction: add lightweight contract tests for registries and authored data shapes, similar to the strong zone contract tests now used for areas.
  - Verification needed: fast, pure-Python registry audits that validate ids, references, unlock sources, help hooks, and data shape invariants.

### Improvement Opportunity
- **Filename-based coverage symmetry understates real protection, but the asymmetry is still a useful warning.**
  - Some important systems are tested under broader names rather than matching module names one-to-one, such as dialogue and crafting.
  - Even so, the mismatch itself signals maintainability risk: it is harder to know what protects what, especially for new contributors or late-stage launch work.
  - Recommended fix direction: maintain a small coverage matrix doc or a meta-test that maps runtime modules to their protecting suites.

### Improvement Opportunity
- **The suite is strong on focused engine behavior and authored area contracts, but thinner on end-to-end flows.**
  - The codebase now has very good focused tests for many isolated systems and zone authoring rules.
  - What is still scarce are multi-step player journeys that traverse onboarding, guilding, quests, vendors, travel, combat, death, and recovery as a continuous play session.
  - Player-facing impact: cross-system regressions can still hide in the seams between individually-tested engines.
  - Recommended fix direction: add a small set of “golden path” integration tests for first-session play, early questing, basic commerce, and grouped combat.

### Improvement Opportunity
- **Launch verification still leans heavily on smoke and focused suites rather than full runtime build validation.**
  - `python scripts/smoke_start.py` is a valuable guardrail, and the area contract tests are strong.
  - But the remaining launch risk sits in the zones between pure importability and a full DB-backed runtime pass, especially for authored content.
  - Recommended fix direction: add a reproducible build-validation routine for the most important authored areas and critical startup systems.

### Already Strong / Protect With Regression Coverage
- **The repo has matured into a real test-bearing game codebase, not a prototype with token tests.**
  - `61` test files is a meaningful base.
  - Recent audit/remediation waves have materially improved the safety net around lifecycle, help, abilities, economy, travel, and content authoring.
  - The zone contract/layout model is especially strong and worth reusing elsewhere.

## Recommended Next Verification Work

1. Add direct command tests for the most-used player commands:
   - `joinguild`, `abilities`, `quest`, `buy`, `sell`, `group`, `loot`, `rest`, `sleep`, `wake`, `map`, `search`, `status`
2. Replace the highest-value string-presence integration tests with semantic checks.
3. Add contract tests for high-value registries and definition modules.
4. Create a small golden-path suite for first-session play and early co-op play.
5. Add a documented launch verification checklist that names the exact smoke/build/test passes expected before host/go-live.

## Wave 10 Verdict

- **The safety net is solid enough to keep moving, but not yet fully commensurate with launch ambitions.**
- Soravelon now has many strong local tests, but the remaining risk is in command UX, registry drift, semantic integration checks, and multi-system player journeys.
