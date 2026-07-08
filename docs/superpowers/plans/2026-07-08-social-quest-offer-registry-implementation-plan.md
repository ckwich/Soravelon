# Social Quest Offer Registry Implementation Plan

**Date:** 2026-07-08
**Repo:** `/Users/ckwichman/Documents/Projects/soravelon`

## Goal

Turn the first live Social Web quest offer into a scalable, data-driven
registry while preserving the current Warden-memory behavior.

The slice should also carry forward the browser-review synthesis: future
player-facing explainability and contest/repair gameplay need metadata now, but
they must not become LLM-owned or freeform mutation paths.

## Binding Contract

- The offer registry is data, not dialogue command logic.
- `query_social_context()` remains the live source for what an NPC knows.
- `compile_quest_spec()` remains the deterministic quest compiler.
- The LLM remains renderer-only and disabled in compiled quest context.
- The Warden follow-up quest must still require the real
  `vc_q_warden_report:delivered` Social Web fact.
- Dynamic quest specs must remain retrievable by quest id for progress and
  completion.
- Explainability metadata must be player-safe and non-numeric.
- Contest/repair hooks are metadata only in this slice.
- Do not add schedules, romance, property, employment, or broad NPC simulation.

## Implementation Tasks

### Task 1: Add Registry Contract Tests

Write failing tests proving:

- the Warden offer rule is available through a registry API by NPC id and quest
  id
- registry callers receive copies, not mutable shared rule data
- the live offer carries player-safe explainability metadata derived from real
  Social Web context
- the live offer carries future contest/repair hook metadata
- existing active/completed/failed quest-state gating still applies

### Task 2: Extract Data-Driven Offer Rules

Create a small registry module that owns offer rule data and lookup helpers.
Move Warden-specific rule data out of `world.social_quest_offers` into the
registry.

The service module should keep runtime behavior:

- identify the NPC and player social nodes
- query Social Web context once
- validate required grounding
- compile the deterministic quest spec
- attach explainability and repair metadata

### Task 3: Update Spec And Validation

Update the Social Quest Grammar spec with the offer registry, explainability,
and repair metadata contract.

Validate with:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_social_quest_offers tests.test_social_quest_grammar tests.test_dialogue.TestQuestOfferAcceptance
uv run --python 3.12 --with-requirements requirements.txt python scripts/smoke_start.py
```

## Next Slice After This

Add a player-safe Social Web explainability surface, likely starting with a
diegetic `ask <npc> about me` path that uses the explanation packet and
`query_social_context()` traces without exposing numeric debug state.
