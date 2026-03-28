---
phase: 5c
slug: ability-polish-and-resource-engine
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-27
---

# Phase 5c — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | unittest + MagicMock (project standard for pure logic) |
| **Config file** | None (inline with `evennia test --settings settings tests/` or `pytest`) |
| **Quick run command** | `python -m pytest tests/test_ability_engine.py -x` |
| **Full suite command** | `python -m pytest tests/ -x` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_ability_engine.py -x`
- **After every plan wave:** Run `python -m pytest tests/ -x`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 5c-01-01 | 01 | 1 | ABL-04-R1 | unit | `pytest tests/test_ability_engine.py::TestAbilityRedundancy -x` | ❌ W0 | ⬜ pending |
| 5c-01-02 | 01 | 1 | ABL-04-R2 | unit | `pytest tests/test_ability_engine.py::TestResourceInitialization -x` | ❌ W0 | ⬜ pending |
| 5c-01-03 | 01 | 1 | ABL-04-R3 | unit | `pytest tests/test_ability_engine.py::TestFocusResource -x` | ❌ W0 | ⬜ pending |
| 5c-01-04 | 01 | 1 | ABL-04-R4 | unit | `pytest tests/test_ability_engine.py::TestBalanceResource -x` | ❌ W0 | ⬜ pending |
| 5c-01-05 | 01 | 1 | ABL-04-R5 | unit | `pytest tests/test_ability_engine.py::TestResonanceResource -x` | ❌ W0 | ⬜ pending |
| 5c-01-06 | 01 | 1 | ABL-04-R6 | unit | `pytest tests/test_ability_engine.py::TestInfluenceResource -x` | ❌ W0 | ⬜ pending |
| 5c-01-07 | 01 | 1 | ABL-04-R7 | unit | `pytest tests/test_ability_engine.py::TestMomentumResource -x` | ❌ W0 | ⬜ pending |
| 5c-01-08 | 01 | 1 | ABL-04-R8 | unit | `pytest tests/test_ability_engine.py::TestFiniteResources -x` | ❌ W0 | ⬜ pending |
| 5c-01-09 | 01 | 1 | ABL-04-R9 | unit | `pytest tests/test_ability_engine.py::TestCommandResource -x` | ❌ W0 | ⬜ pending |
| 5c-01-10 | 01 | 1 | ABL-04-R10 | unit | `pytest tests/test_ability_engine.py::TestEchoesResource -x` | ❌ W0 | ⬜ pending |
| 5c-01-11 | 01 | 1 | ABL-04-R11 | unit | `pytest tests/test_ability_engine.py::TestFocusScaling -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_ability_engine.py::TestResourceInitialization` — test all 10 resource types initialize with correct shape
- [ ] `tests/test_ability_engine.py::TestFocusResource` — Focus combo point lifecycle
- [ ] `tests/test_ability_engine.py::TestBalanceResource` — Balance pendulum mechanics
- [ ] `tests/test_ability_engine.py::TestResonanceResource` — Resonance decay
- [ ] `tests/test_ability_engine.py::TestInfluenceResource` — Influence from Reputation
- [ ] `tests/test_ability_engine.py::TestMomentumResource` — Momentum build triggers
- [ ] `tests/test_ability_engine.py::TestFiniteResources` — Reagents/Components depletion
- [ ] `tests/test_ability_engine.py::TestCommandResource` — Command ally-action build
- [ ] `tests/test_ability_engine.py::TestEchoesResource` — Echoes investigation bonus
- [ ] `tests/test_ability_engine.py::TestAbilityRedundancy` — structural uniqueness validation

*Existing infrastructure covers framework — only test stubs needed.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Ability loadout variety feels good | ABL-04 | Subjective game design judgment | Review all 8 domains, verify each tier has 2+ distinct ability archetypes |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
