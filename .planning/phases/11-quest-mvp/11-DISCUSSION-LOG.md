# Phase 11: Quest MVP - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.

**Date:** 2026-04-03
**Phase:** 11-quest-mvp
**Areas discussed:** Quest data model, Objective types, Rewards, Player commands

---

## Quest Data Model

| Option | Description | Selected |
|--------|-------------|----------|
| Unlimited active | No cap | |
| Soft cap with warning | Warn at 5-10 | |
| Hard cap (5) | Max 5 active, must abandon to accept | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Always re-acceptable | Reset progress, no lockout | |
| Cooldown | Wait before re-accept | |
| One attempt only | Failed = locked | |
| Mostly re-acceptable + one_chance flag (user) | Builder sets per-quest | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Succeed, abandon, and fail | Three distinct terminal states | ✓ |
| Succeed and abandon only | No failure state | |

---

## Objective Types

Selected for MVP: kill, collect, investigate (skill-gated), deliver, talk_to (for quest chains)
User added: talk_to for quest chains, investigate tied to investigation skill

---

## Quest Chains

| Option | Description | Selected |
|--------|-------------|----------|
| next_quest_id field | Linear chain, auto-offer on completion | ✓ |
| Prerequisite list | Branching paths | |
| Both | Maximum flexibility | |

---

## Quest Rewards

Selected: All 4 core types + user additions
- Scales, Items, Standing, Recipes (core)
- Skill XP, Teleport/area access, Boss/mob spawn, Node progress (user additions)
- Format: Action dict list reusing action_vocabulary pattern

---

## Player Commands

| Option | Description | Selected |
|--------|-------------|----------|
| quest (list) + quest <name> (detail) | Subcommand pattern | ✓ |
| Separate commands | quests, objectives, abandon | |
| Combined with existing | Extend dialogue commands | |

---

## Claude's Discretion

- Progress notification format
- investigate search check requirements
- Failure condition implementation
- Quest sharing mechanics
- quest_type as mechanical vs cosmetic

## Deferred Ideas

- Quest timers
- Quest sharing between group members
- LLM-generated content
- Branching prerequisites
- Quest map markers
