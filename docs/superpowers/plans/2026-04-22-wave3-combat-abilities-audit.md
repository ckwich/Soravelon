# Soravelon Wave 3 Combat, Abilities, and Encounter Loop Audit

**Date:** 2026-04-22
**Depends on:** `docs/superpowers/plans/2026-04-22-wave2-command-help-onboarding-remediation.md`

## Scope
Wave 3 reviewed whether combat remains truthful, fun, legible, and mechanically sound after the earlier runtime/ability alignment work. This pass focused on:

- combat turn flow
- charged-ability execution
- ability/runtime truthfulness
- status-effect interactions
- encounter scripting hooks and AI support

## Evidence Reviewed

- `world/ability_engine.py`
- `world/combat_engine.py`
- `world/combat_script.py`
- `world/status_effects.py`
- `world/combat_ai.py`
- `world/mob_templates.py`
- `tests/test_ability_engine.py`
- `tests/test_combat_engine.py`
- `tests/test_combat_script.py`
- `tests/test_status_effects.py`
- `tests/test_combat_ai.py`

## Current-State Validation

- `python scripts/run_tests.py tests.test_ability_engine tests.test_combat_script tests.test_combat_engine tests.test_status_effects tests.test_combat_ai`
  - Result: `208` tests passed
- `python scripts/smoke_start.py`
  - Result: passed

This confirms the combat surface is structurally stable after the latest fix pass, but the audit still surfaced meaningful design and code-health notes.

## Findings

### Blocker
- **Charged abilities could be fired instantly through the normal `use` path.**
  - `world/combat_script.py` correctly exposed a separate `charge` action, but `world/ability_engine.py` did not reject direct in-combat use of player abilities with `charge_turns > 0`.
  - Impact: authored charge-up abilities could bypass their channel time, which undermined both balance and combat fantasy.
  - This was fixed during the audit:
    - `use_ability()` now blocks direct player use of charged abilities during combat unless the runtime marks the call as an internal charged release.
    - `_prompt_player_turn()` now sets a temporary `resolving_charged_ability` flag only around the automatic release path.
    - turn prompts now show the charged ability's authored display name instead of only its raw id.

### Improvement Opportunity
- **Charging is still a very generous action-economy lane.**
  - Starting a charge currently does not consume the entire turn.
  - The eventual release also arrives without forcing a dedicated action commitment that round.
  - This may be intentionally fun, but it is still a balance lever worth reviewing because it can make charged abilities feel like upside-only setup buttons.

### Improvement Opportunity
- **Some group/AoE inference still leans on description heuristics rather than fully explicit authored flags.**
  - The combat runtime is much richer than it was earlier in the audit, but a few targeting decisions are still inferred from ability text patterns.
  - This is more of a code-health and future-authoring risk than an active launch blocker.
  - A later cleanup pass should prefer explicit targeting metadata over text-driven heuristics wherever practical.

### Already Strong / Protect With Regression Coverage
- **The encounter scripting surface is now meaningfully expressive.**
  - `world/combat_ai.py` supports trigger-driven sequencing and named encounter scripting that goes beyond plain stat inflation.
  - This is worth protecting because it gives authored bosses and named enemies room to feel distinct.

### Already Strong / Protect With Regression Coverage
- **Runtime alignment coverage is broad and improving.**
  - The ability/status/combat suites now meaningfully exercise:
    - AoE and group behavior
    - periodic effects
    - death cleanup
    - charge-release handling
    - status-effect modifiers

## Regression Coverage Added

### `tests/test_ability_engine.py`
- charged abilities reject direct in-combat `use`
- internal charged-release path still resolves successfully

### `tests/test_combat_script.py`
- automatic charged release marks the internal bypass flag only for the release path
- turn-prompt handling stays compatible with the charged-ability flow

## Wave 3 Verdict

- **Wave 3 is no longer blocked by the charged-ability bypass.**
- Combat is materially healthier than it was before the audit, and the biggest newly surfaced exploit path is closed.
- The remaining Wave 3 notes are mostly about balancing generosity and reducing future-authoring fragility rather than emergency launch breakage.
