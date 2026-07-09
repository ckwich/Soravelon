# Social Explainability Warden Proof Plan

**Date:** 2026-07-08
**Repo:** `/Users/ckwichman/Documents/Projects/soravelon`

## Goal

Prove the player-facing Social Web explanation surface works on the live Warden
route, not just pure formatter fixtures.

The proof should show that real quest rewards create the Social Web knowledge
Calloway uses, `talk Calloway` can surface the Social Web-gated follow-up, and
`ask Calloway why` explains the offer without raw Social Web internals. Whistle
must stay ignorant unless actual Social Web propagation gives Whistle knowledge.

## Binding Contract

- The test may pay the authored Warden-report reward directly, but must also
  mark `vc_q_warden_report` complete before checking the follow-up offer.
- The test must assert real Social Web knowledge exists for Calloway and Harven.
- The test must assert Whistle has no edge or knowledge path for this payload.
- The command path should use real `CmdTalk` and `CmdAsk` calls.
- NPC lookup should preserve exact and prefix matching, with token fallback only
  after those higher-confidence matches.
- Player-facing explanation output must include safe Warden context while
  excluding raw keys, node ids, trace fields, confidence values, provider/prompt
  fields, and `warden_report` implementation vocabulary.

## Implementation Tasks

### Task 1: Add Red Route Proof

Add an integration test to `tests/test_social_web_warden_route.py` proving:

- paying `vc_q_warden_report` creates Calloway and Harven Social Web knowledge
- Whistle has no Social Web edge or context for the Warden-report payload
- `talk Calloway` creates pending quest `vc_sq_under_seal_dustwalkers_rest`
- `ask Calloway why` returns the safe grounded reason
- `ask Whistle why` returns the fair fallback

### Task 2: Tighten NPC Lookup

Let `_find_npc_in_room()` match a token inside an NPC display name only after
exact and full-name prefix matching. This makes `Calloway` resolve `Agent
Calloway` without stealing more specific matches first.

### Task 3: Validate

Run:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_social_web_warden_route
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_social_web_warden_route tests.test_dialogue tests.test_cmd_dialogue tests.test_social_quest_offers tests.test_social_web_kernel tests.test_socialmemory_command tests.test_action_vocabulary tests.test_content_authoring tests.test_quest_engine
uv run --python 3.12 --with-requirements requirements.txt python scripts/smoke_start.py
```

## Next Slice After This

Add positive propagation gameplay for a non-Warden NPC: create a real Social Web
route that gives Whistle or another local anchor a safe rumor/report reason,
then prove their `ask why` answer changes only after that route exists.
