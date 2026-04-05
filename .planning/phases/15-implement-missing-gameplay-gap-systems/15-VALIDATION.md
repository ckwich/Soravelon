---
phase: 15
slug: implement-missing-gameplay-gap-systems
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-04
---

# Phase 15 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | unittest.TestCase + MagicMock (pure logic), EvenniaTestCase (DB-dependent) |
| **Config file** | `server/conf/settings.py` |
| **Quick run command** | `pytest tests/test_<module>.py -x` |
| **Full suite command** | `evennia test --settings server.conf.settings tests/` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_<changed_module>.py -x`
- **After every plan wave:** Run `evennia test --settings server.conf.settings tests/`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 15-01-xx | 01 | 1 | D-01/D-05 | unit | `pytest tests/test_vendor_engine.py -x` | ❌ W0 | ⬜ pending |
| 15-02-xx | 02 | 1 | D-06/D-10 | unit | `pytest tests/test_recovery_engine.py -x` | ❌ W0 | ⬜ pending |
| 15-02-xx | 02 | 1 | D-11/D-12 | unit | `pytest tests/test_recovery_engine.py -x` | ❌ W0 | ⬜ pending |
| 15-03-xx | 03 | 1 | D-13/D-14 | unit | `pytest tests/test_inspect.py -x` | ❌ W0 | ⬜ pending |
| 15-04-xx | 04 | 2 | D-15/D-18 | unit | `pytest tests/test_social.py -x` | ❌ W0 | ⬜ pending |
| 15-05-xx | 05 | 2 | D-25 | unit | `pytest tests/test_ability_engine.py -x` | ✅ (update) | ⬜ pending |
| 15-05-xx | 05 | 2 | D-26 | unit | `pytest tests/test_status_effects.py -x` | ✅ (update) | ⬜ pending |
| 15-06-xx | 06 | 2 | D-27 | unit | `pytest tests/test_loot.py -x` | ❌ W0 | ⬜ pending |
| 15-06-xx | 06 | 2 | D-28 | unit | `pytest tests/test_group_engine.py -x` | ✅ (update) | ⬜ pending |
| 15-07-xx | 07 | 3 | D-20/D-24 | unit | `pytest tests/test_gathering.py -x` | ✅ (update) | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_vendor_engine.py` — stubs for D-01 through D-05
- [ ] `tests/test_recovery_engine.py` — stubs for D-06 through D-12
- [ ] `tests/test_inspect.py` — stubs for D-13, D-14
- [ ] `tests/test_social.py` — stubs for D-15 through D-19
- [ ] `tests/test_loot.py` — stubs for D-27

*Existing test files to update: test_ability_engine.py, test_status_effects.py, test_group_engine.py, test_gathering.py*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Sleep blinds player from room events | D-08 | Requires visual verification of room event suppression | Enter room, sleep, have another character enter — verify no event shown |
| Vendor NPC interaction flow | D-02 | End-to-end flow with NPC targeting | Talk to vendor NPC, use list/buy/sell/appraise/view commands |
| Domain channel membership gating | D-18 | Requires two characters with different domains | Create two chars, verify correct channel access |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
