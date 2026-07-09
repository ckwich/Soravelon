# Social Explainability Dialogue Implementation Plan

**Date:** 2026-07-08
**Repo:** `/Users/ckwichman/Documents/Projects/soravelon`

## Goal

Add the first player-facing Social Web explanation surface through dialogue:
`ask <npc> about me` and narrow `why` phrases.

The feature should make NPC social reactions more legible without exposing a
numeric reputation dashboard, raw Social Web internals, or LLM-authored truth.

## Binding Contract

- Keep the surface diegetic and non-numeric.
- Use the existing `CmdAsk` flow instead of adding a parallel command.
- Use `_build_dialogue_context()` so Social Web knowledge still comes from
  `query_social_context()`.
- Prefer `social_quest_context.offer_explainability` from a pending quest offer
  when the offer belongs to the same NPC.
- Fall back to current Social Web fact/claim summaries from the dialogue
  context packet.
- Filter raw fact keys, claim keys, node keys, traces, confidence scores,
  prompts, model output, and withheld authoring implications.
- Do not mutate Social Web state, quest state, standing, or reputation.
- Do not call an LLM; this remains deterministic renderer input.

## Implementation Tasks

### Task 1: Add Red Tests

Prove:

- `ask <npc> about me` enters the social explanation surface and skips normal
  topic extraction/recording.
- social explanation topic matching is narrow enough not to steal ordinary
  topics such as `why wolves`.
- pending quest offer explainability can produce a safe answer.
- current Social Web context can produce a safe answer when no pending offer is
  relevant.
- missing safe summaries produce a fair fallback.
- raw Social Web/internal/provider fields are filtered from player-facing text.
- multi-word NPC `why` asks resolve the correct NPC.
- specific topics such as `why wolves` remain normal authored topic asks.
- private/admin/hidden visibility and raw-looking summary/channel text are
  rejected instead of rendered.

### Task 2: Implement Dialogue Engine Helpers

Add deterministic helpers in `world.dialogue_engine`:

- `is_social_explanation_topic()`
- `resolve_social_explanation()`
- small private formatters for safe evidence and pending-offer matching

### Task 3: Wire CmdAsk

Before normal topic extraction, detect social explanation topics, build the
existing dialogue context, pass any pending offer, and render the NPC response.

For ask input without explicit `about`, resolve the longest NPC-name prefix so
`ask Agent Calloway why` works while `ask Maren why wolves` still sends
`why wolves` through normal topic matching.

### Task 4: Validate

Run:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_cmd_dialogue.TestCmdAsk tests.test_dialogue.TestSocialExplanationSurface
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_cmd_dialogue tests.test_dialogue tests.test_social_quest_offers
uv run --python 3.12 --with-requirements requirements.txt python scripts/smoke_start.py
```

## Next Slice After This

Add social explanation coverage for one live Warden flow so manual play can
show: complete Warden report, talk to Calloway, receive the Social Web-gated
offer, then `ask Calloway why` and get a grounded in-world reason.
