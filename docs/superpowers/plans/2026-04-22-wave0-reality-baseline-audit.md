# Soravelon Wave 0 Reality Baseline Audit

**Date:** 2026-04-22
**Depends on:** `docs/superpowers/plans/2026-04-22-deep-gameplay-code-health-audit-plan.md`

## Scope
Wave 0 establishes current repo reality before deeper audit waves begin. This pass focused on:

- active runtime surfaces
- command and content availability
- current test and smoke harnesses
- drift between live code and older internal codebase-analysis docs

## Evidence Reviewed

- `README.md`
- `commands/default_cmdsets.py`
- `server/conf/at_server_startstop.py`
- `world/areas/*`
- `tests/test_*.py`
- `.planning/codebase/CONCERNS.md`
- `.planning/codebase/STRUCTURE.md`
- `.planning/codebase/ARCHITECTURE.md`
- `python scripts/smoke_start.py`

## Current-State Baseline

### Repo surface
- `world/`: `87` Python files
- `commands/`: `34` Python files
- `tests/`: `59` `test_*.py` modules (`60` Python files total including package init)

### Authored world content
- `world/areas/` contains `10` authored zone files:
  - `ashreach_plains`
  - `cantera_edge`
  - `crownroad_north`
  - `ironvein_escarpment`
  - `old_causeway`
  - `reth_foothills`
  - `stagcrown_preserve`
  - `stormhaven_coast`
  - `vaels_crossing`
  - `varath_prime`
- `world/areas/equipment_catalog.py` is shared item data, not a zone.

### Player-facing command surface
- `CharacterCmdSet` in `commands/default_cmdsets.py` currently registers `66` command additions/overrides.
- The live surface spans aliases, flight, ancestry, guilds, domains, abilities, combat, skills, dialogue, crafting, equipment, banking, groups, loadouts, map/search, quests, help, lore, vendors, social, inspection, gathering, fishing, prospecting, recovery, loot, and tools.

### Server bootstrap surface
- `at_server_start()` currently registers `7` persistent ticker callbacks:
  - world-state decay
  - session XP safety flush
  - node failure tick
  - banking payment tick
  - mob spawn tick
  - wandering tick
  - ambient NPC tick
- Startup also:
  - recovers Layer 1 node pool state
  - reloads all zones from `world/areas/`
  - initializes spawn records

### Verification harness
- The current README accurately points operators toward:
  - `python scripts/run_tests.py`
  - `python scripts/smoke_start.py`
- `python scripts/smoke_start.py` passed during this audit wave.
- Content regression coverage is non-trivial, including:
  - `5` `test_*layout.py` files
  - `4` `test_*contract.py` files
  - broader content/system tests such as `test_content_authoring.py`, `test_content_integration.py`, and `test_hub1_contracts.py`

## Findings

### High-Value Fix
- `.planning/codebase/CONCERNS.md` is materially stale and no longer safe as a current-state source. It still claims there are no custom commands, no area spec files, no mob spawn system, no combat system, no NPC system, and no quest system. Those statements conflict with the live code in `commands/default_cmdsets.py`, `server/conf/at_server_startstop.py`, and the authored `world/areas/` pack.

### High-Value Fix
- `.planning/codebase/STRUCTURE.md` is also behind repo reality. It still describes `commands/` as "currently using Evennia defaults" and shows `world/areas/` as effectively empty except for future spec placement. That is no longer true.

### Improvement Opportunity
- `.planning/codebase/ARCHITECTURE.md` is still partially useful at the pattern level, but several concrete enumerations are stale. One example: it says server start registers `4` tickers, while the live startup path now registers `7`, plus zone load and spawn initialization.

### Already Strong
- `README.md` is much closer to current repo truth than the older codebase-analysis docs. It correctly presents Soravelon as a server-first launch build with authored zones, combat, progression, crafting, gathering, banking, social systems, custom help, a canonical test runner, and a smoke gate.

### Already Strong
- The baseline runtime story is coherent enough to continue the audit. The smoke pass succeeded, the server bootstrap file reflects active systems, and the content surface is substantial rather than skeletal.

### Improvement Opportunity
- The repo has a broad test suite, but there is no single up-to-date "current-state inventory" document tying together command surface, world systems, content pack count, and verification layers. Creating or refreshing that inventory would reduce future audit drift.

## Blocker Assessment

- **No Wave 0 stop-ship runtime blocker was found.**
- The biggest Wave 0 problem is **process/documentation drift**, not evidence that the shipped game surface is absent.
- That drift is still important because it can misdirect future audits, onboarding, and launch readiness judgments.

## Recommended Next Actions

1. Treat `.planning/codebase/CONCERNS.md` and `.planning/codebase/STRUCTURE.md` as historical snapshots until refreshed.
2. Use live code plus `README.md` as the baseline truth source for the rest of the audit.
3. Continue directly into Wave 1: boot, session, character lifecycle, and persistence safety.
4. After the deeper audit waves, either refresh the old codebase-analysis docs or replace them with a fresh current-state baseline document.

## Useful Anchors

- `commands/default_cmdsets.py`
- `server/conf/at_server_startstop.py`
- `README.md`
- `.planning/codebase/CONCERNS.md`
- `.planning/codebase/STRUCTURE.md`
- `.planning/codebase/ARCHITECTURE.md`
