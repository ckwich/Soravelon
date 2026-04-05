---
phase: 16
slug: architectural-refactoring
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-05
---

# Phase 16 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Evennia test runner (Django-based) + unittest.TestCase |
| **Config file** | `server/conf/settings.py` |
| **Quick run command** | `evennia test --settings server.conf.settings tests/` |
| **Full suite command** | `evennia test --settings server.conf.settings tests/` |
| **Estimated runtime** | ~45 seconds |

---

## Sampling Rate

- **After every task commit:** Run full test suite
- **After every plan wave:** Run full test suite
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 45 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 16-01-xx | 01 | 1 | D-01/D-03 | unit | `pytest tests/test_session_lifecycle.py -x` | ❌ W0 | ⬜ pending |
| 16-01-xx | 01 | 1 | D-01/D-03 | unit | `pytest tests/test_movement_lifecycle.py -x` | ❌ W0 | ⬜ pending |
| 16-01-xx | 01 | 1 | D-01/D-03 | unit | `pytest tests/test_death_lifecycle.py -x` | ❌ W0 | ⬜ pending |
| 16-02-xx | 02 | 1 | D-05/D-06 | unit | `pytest tests/test_gathering.py -x` | ✅ (update) | ⬜ pending |
| 16-03-xx | 03 | 1 | D-09 | unit | `pytest tests/test_combat_engine.py -x` | ✅ (update) | ⬜ pending |
| 16-04-xx | 04 | 2 | D-11/D-12 | smoke | grep-based zero old-name verification | Manual | ⬜ pending |
| 16-05-xx | 05 | 2 | D-13/D-15 | audit | grep-based sweep + import check | Manual | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_session_lifecycle.py` — stubs for D-01/D-02/D-03 login/logout orchestrator
- [ ] `tests/test_movement_lifecycle.py` — stubs for D-01/D-02/D-03 movement orchestrator
- [ ] `tests/test_death_lifecycle.py` — stubs for D-01/D-02/D-03 mob death orchestrator

*Existing test files to update: test_gathering.py, test_combat_engine.py, test_status_effects.py*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Naming rename completeness | D-11/D-12 | Need grep across entire codebase | `grep -r "mob_template\b" world/ typeclasses/ commands/ tests/` returns 0 hits for old names |
| SaverDict compliance | D-13/D-14 | Pattern analysis not automatable | `grep -rn "\.db\.\w*\[" world/ typeclasses/` — verify all hits use copy pattern |
| Import hygiene | D-17/D-19 | Circular import detection needs runtime check | `python -c "import typeclasses.characters; import typeclasses.mobs"` succeeds |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 45s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
