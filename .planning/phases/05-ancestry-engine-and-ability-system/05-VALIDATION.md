---
phase: 5
slug: ancestry-engine-and-ability-system
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-03-26
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | unittest via `evennia test --settings settings tests/` |
| **Config file** | None (Evennia test runner) |
| **Quick run command** | `evennia test --settings settings tests/test_ancestry_engine.py tests/test_ability_engine.py tests/test_room_state.py` |
| **Full suite command** | `evennia test --settings settings tests/` |
| **Estimated runtime** | ~20 seconds |

---

## Sampling Rate

- **After every task commit:** Run quick command (ancestry + ability + room_state tests)
- **After every plan wave:** Run full suite
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 20 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | ANC-01-04 | unit | `evennia test --settings settings tests/test_ancestry_engine.py` | W0 | pending |
| 05-01-02 | 01 | 1 | ANC-05 | unit | `evennia test --settings settings tests/test_mob_disposition.py` | Existing | pending |
| 05-02-01 | 02 | 1 | ABL-01 | unit | `evennia test --settings settings tests/test_ability_engine.py::TestAbilityRegistry` | W0 | pending |
| 05-02-02 | 02 | 1 | ABL-02 | unit | `evennia test --settings settings tests/test_ability_engine.py::TestUseAbility` | W0 | pending |
| 05-02-03 | 02 | 1 | ABL-03, ABL-05 | unit | `evennia test --settings settings tests/test_ability_engine.py::TestTierGating` | W0 | pending |
| 05-03-01 | 03 | 1 | D-21 | unit | `evennia test --settings settings tests/test_room_state.py` | W0 | pending |
| 05-04-01 | 04 | 2 | D-17, D-25 | unit | `evennia test --settings settings tests/test_guild_engine.py` | Extend | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_ancestry_engine.py` — stubs for ANC-01 through ANC-04
- [ ] `tests/test_ability_engine.py` — stubs for ABL-01, ABL-02, ABL-03, ABL-05
- [ ] `tests/test_room_state.py` — stubs for room state operations
- [ ] No conftest needed (unittest.TestCase pattern)
- [ ] No framework install needed (Evennia test runner available)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Sense display shows atmospheric text after move | D-22 | Requires connected client | Connect, move as Resonance-primary character, verify Sense line appears |

---

## Test Pattern Decision

- Ancestry engine (set_ancestry, apply_standings): `unittest.TestCase` + MagicMock
- Ability registry + dispatcher: `unittest.TestCase` + MagicMock
- Room state (lazy decay, flags): `unittest.TestCase` + MagicMock + time mocking
- CharacterAbility model: `EvenniaTest` (Django model operations)
- Commands (CmdSetAncestry, CmdDomains): `EvenniaCommandTestMixin`

---

## Validation Sign-Off

- [ ] All tasks have automated verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 20s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
