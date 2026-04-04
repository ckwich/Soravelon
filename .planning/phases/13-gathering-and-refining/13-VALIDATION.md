---
phase: 13
slug: gathering-and-refining
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-03
---

# Phase 13 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Evennia EvenniaTestCase (Django TestCase) + pytest |
| **Config file** | server/conf/settings.py |
| **Quick run command** | `evennia test --settings server.conf.settings tests/test_gathering.py` |
| **Full suite command** | `evennia test --settings server.conf.settings tests/` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `evennia test --settings server.conf.settings tests/test_gathering.py`
- **After every plan wave:** Run `evennia test --settings server.conf.settings tests/`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| TBD | TBD | TBD | SC-1 (node spawning) | integration | `evennia test tests/test_gathering.py` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | SC-2 (gather commands) | unit+integration | `evennia test tests/test_gathering.py` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | SC-3 (processing recipes) | unit | `evennia test tests/test_crafting.py` | ✅ | ⬜ pending |
| TBD | TBD | TBD | SC-4 (material registry) | unit | `evennia test tests/test_gathering.py` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | SC-5 (fishing) | integration | `evennia test tests/test_fishing.py` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | SC-6 (tools/durability) | unit | `evennia test tests/test_gathering.py` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | SC-7 (prospect/survey) | integration | `evennia test tests/test_gathering.py` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | SC-8 (mob loot→processing) | integration | `evennia test tests/test_loot_tables.py` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_gathering.py` — stubs for gathering engine, node spawning, commands, tools, prospect
- [ ] `tests/test_fishing.py` — stubs for fishing mini-game and idle mode
- [ ] Shared fixtures: mock rooms with gathering pool data, mock characters with skills/tools

*Existing `tests/test_crafting.py` and `tests/test_loot_tables.py` cover processing recipe and mob loot integration.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Fishing mini-game timing | SC-5 | Real-time bite/reel window timing | Connect to server, fish at water room, verify bite prompt appears, reel within window |
| Node stochastic spawning distribution | SC-1 | Statistical distribution needs many samples | Run gathering pool ticker 100+ times, verify nodes don't always spawn in same room |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
