---
phase: 4
slug: domain-fingerprints-guild-engine
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-03-25
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | unittest (via `evennia test --settings settings tests/`) |
| **Config file** | None (Evennia test runner) |
| **Quick run command** | `evennia test --settings settings tests/test_guild_engine.py` |
| **Full suite command** | `evennia test --settings settings tests/` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `evennia test --settings settings tests/test_guild_engine.py`
- **After every plan wave:** Run `evennia test --settings settings tests/`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | DOM-05 | unit | `evennia test --settings settings tests/test_guild_engine.py::TestFingerprintRegistry` | ❌ W0 | ⬜ pending |
| 04-01-02 | 01 | 1 | DOM-01 | unit | `evennia test --settings settings tests/test_guild_engine.py::TestGuildSubclassRegistry` | ❌ W0 | ⬜ pending |
| 04-02-01 | 02 | 2 | DOM-02, DOM-03 | unit+Django | `evennia test --settings settings tests/test_guild_engine.py::TestJoinGuild` | ❌ W0 | ⬜ pending |
| 04-02-02 | 02 | 2 | DOM-02, DOM-03, DOM-04, DOM-05 | unit | `evennia test --settings settings tests/test_guild_engine.py` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_guild_engine.py` — stubs for DOM-01 through DOM-05
- [ ] No conftest needed (unittest.TestCase pattern, not pytest fixtures)
- [ ] No framework install needed (Evennia test runner already available)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Design doc has 10 distinct non-overlapping verbs | DOM-05 | Creative review | Read .planning/ design doc, verify each domain has unique verb |

---

## Test Pattern Decision

- Pure computation tests (GTS, tiers, eligibility, registry validation): `unittest.TestCase` + MagicMock
- Model mutation tests (join_guild, complete_induction): `EvenniaTest` or Django `TestCase`

Follows established pattern from Phase 1 (patrol_engine, trigger_engine, flight_engine tests all use unittest.TestCase with MagicMock).

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
