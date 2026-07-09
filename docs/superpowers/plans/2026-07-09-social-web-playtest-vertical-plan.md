# Social Web Playtest Vertical Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the full eight-slice Vael's Crossing Social Web vertical so a playtester can see NPC knowledge move through real contact edges, receive personal quest offers, complete the first social quest lifecycle, contest a social claim, and observe deterministic LLM-ready rendering without any model owning game truth.

**Architecture:** Keep `world.social_engine` as the graph facade for nodes, edges, facts, claims, knowledge, traces, and context packets. Add focused services for NPC interpretation, contest/repair verbs, renderer-only LLM seams, and playtest validation instead of embedding social logic in dialogue commands or area prose. Runtime truth remains Django-backed and deterministic; LLM output is optional phrasing only.

**Tech Stack:** Evennia 6.0, Django ORM, Python 3.11+, `unittest`/Evennia tests through `scripts/run_tests.py`, existing AreaBuilder literal DSL, Engram for design memory only.

---

## Binding Acceptance Contract

- Vael's Crossing must prove one institutional Warden route and one non-Warden rumor/traveler route without omniscient spread.
- `ask <npc> why` and `ask <npc> about me` must explain only player-safe evidence the NPC can plausibly know.
- At least five named NPCs must have authored social identity/interpretation profiles and respond differently to the same social memory packet.
- The first dynamic Social Web quest must be acceptable, progressable, completable, and must write deterministic Social Web consequences.
- Rumor propagation must be controllable by edge scope, channel, latency, directionality, blocker metadata, and distortion policy.
- The player must have a deterministic contest/repair verb that creates Social Web claims instead of changing hidden reputation numbers directly.
- DeepSeek/LLM integration must exist only as a renderer seam with deterministic fallback, redacted payloads, and no provider call unless explicitly enabled.
- The final playtest harness must prove the route end-to-end and document exact commands for a human playtest.

## File Structure

- Modify `world/social_engine.py`: enrich fact context traces, improve channel mapping, and expose propagation explanations used by dialogue/admin.
- Create `world/social_interpretation.py`: authored NPC social identity profiles and deterministic interpretation summaries.
- Modify `world/dialogue_engine.py`: attach interpretation packets and use them in player-safe explanations.
- Modify `commands/cmd_dialogue.py`: preserve current `ask` behavior while routing richer explanations through the service layer.
- Create `world/social_claim_repair.py`: deterministic helpers for contest/repair claim creation.
- Create `commands/cmd_social_verbs.py`: player commands for first contest/repair prototype.
- Modify `commands/default_cmdsets.py`: register the new social verb commands.
- Modify `world/social_quest_offers.py` and `world/social_quest_offer_registry.py`: complete the first social quest lifecycle and add non-Warden/repair-aware offer metadata.
- Create `world/social_llm_renderer.py`: renderer-only DeepSeek-compatible seam with deterministic fallback.
- Create `scripts/playtest_social_web_vertical.py`: repo-local validation harness for the Social Web vertical.
- Create or modify focused tests under `tests/`: `test_social_web_warden_route.py`, `test_social_web_kernel.py`, `test_dialogue.py`, `test_social_quest_offers.py`, `test_social_quest_lifecycle.py`, `test_social_claim_repair.py`, `test_social_llm_renderer.py`, and `test_social_web_playtest_harness.py`.

## Slice 1: Positive Non-Warden Propagation And Explanation Proof

**Files:**
- Modify: `world/social_engine.py`
- Modify: `world/dialogue_engine.py`
- Modify: `tests/test_social_web_warden_route.py`
- Modify: `tests/test_social_web_kernel.py`

- [ ] **Step 1: Write failing tests**

Add tests proving Whistle cannot explain Calloway's Warden report until a real `inn_traveler` edge carries a locally scoped rumor or claim, then can explain only the rumor route and not the sealed Warden internals.

- [ ] **Step 2: Verify red**

Run:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_social_web_warden_route tests.test_social_web_kernel
```

Expected: new Whistle-positive tests fail because facts lack trace payloads or because the explanation cannot name the non-Warden route safely.

- [ ] **Step 3: Implement minimal propagation/explanation support**

Add fact trace payloads to `query_social_context()`, map edge types to human channels deterministically, and ensure `resolve_social_explanation()` can use current context evidence from a real propagated fact or claim without exposing keys.

- [ ] **Step 4: Verify green and commit**

Run the same command. Commit message: `feat: prove inn traveler social propagation`.

## Slice 2: True Player-Path Warden Completion Proof

**Files:**
- Modify: `tests/test_social_web_warden_route.py`
- Modify only if failing gate proves it: `world/quest_engine.py`, `commands/cmd_dialogue.py`, or `world/action_vocabulary.py`

- [ ] **Step 1: Write failing end-to-end test**

Create an Evennia-backed test that accepts `vc_q_warden_report`, receives the delivery item, talks to Commander Harven to complete the delivery, pays the authored rewards, and proves Calloway and Harven know the Social Web claim while Whistle does not.

- [ ] **Step 2: Verify red**

Run:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_social_web_warden_route
```

Expected: fail only on a real runtime gap in the player path, not on direct reward seeding.

- [ ] **Step 3: Fix the failing gate**

If delivery completion does not fire, fix the exact quest/objective/tag gate. If it already works, keep the test as proof and do not modify production code.

- [ ] **Step 4: Verify green and commit**

Run the same command. Commit message: `test: prove warden report player path`.

## Slice 3: Complete First Social Quest Lifecycle

**Files:**
- Create: `tests/test_social_quest_lifecycle.py`
- Modify: `world/social_quest_offers.py`
- Modify: `world/social_quest_offer_registry.py`
- Modify only if the lifecycle gate fails: `world/quest_engine.py`

- [ ] **Step 1: Write failing lifecycle test**

Prove `vc_sq_under_seal_dustwalkers_rest` is offered from Calloway after the Warden report, can be accepted, progresses through Whistle, the inn room, Raith, and Calloway, completes, and records a Social Web completion fact/claim.

- [ ] **Step 2: Verify red**

Run:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_social_quest_lifecycle tests.test_social_quest_offers tests.test_social_quest_grammar
```

Expected: fail on missing lifecycle wiring if the dynamic quest cannot progress through the real quest engine.

- [ ] **Step 3: Implement lifecycle fixes**

Keep the dynamic quest spec retrievable by id, preserve deterministic rewards, and add any missing actor/objective metadata through the registry rather than dialogue branches.

- [ ] **Step 4: Verify green and commit**

Run the same command. Commit message: `feat: complete first social quest lifecycle`.

## Slice 4: NPC Interpretation Layer Across Anchor NPCs

**Files:**
- Create: `world/social_interpretation.py`
- Modify: `world/dialogue_engine.py`
- Modify: `world/areas/vaels_crossing.py`
- Modify: `world/areas/ashreach_plains.py`
- Create or modify: `tests/test_social_interpretation.py`
- Modify: `tests/test_dialogue.py`

- [ ] **Step 1: Write failing interpretation tests**

Prove Calloway, Harven, Whistle, Raith, and a market/courier NPC receive the same bounded context and produce distinct interpretation packets based on role, public trait, worldview, and memory style.

- [ ] **Step 2: Verify red**

Run:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_social_interpretation tests.test_dialogue
```

Expected: fail because no interpretation service exists.

- [ ] **Step 3: Implement authored profiles and dialogue wiring**

Profiles must include `social_role`, `public_trait`, `worldview`, and `memory_style`. Dialogue context should attach `social_interpretation`, and explanation text should include the safe relationship tell when available.

- [ ] **Step 4: Verify green and commit**

Run the same command. Commit message: `feat: add authored social interpretations`.

## Slice 5: Rumor And Knowledge Propagation Controls

**Files:**
- Modify: `world/social_engine.py`
- Create or modify: `tests/test_social_web_kernel.py`

- [ ] **Step 1: Write failing propagation-control tests**

Prove edge scope tags, inactive edges, blockers, directionality, latency, bandwidth, and distortion prevent uncontrolled spread. Prove a market rumor follows `market_route` while a Warden report follows `warden_report`, and each lands with the correct channel.

- [ ] **Step 2: Verify red**

Run:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_social_web_kernel
```

Expected: fail on unsupported blocker/bandwidth/distortion/channel behavior.

- [ ] **Step 3: Implement deterministic controls**

Honor edge bandwidth in propagation, skip blocked edges unless the payload carries an allowed unblock tag, map edge type to channel, and create deterministic rumor claim copies only when an edge declares a distortion policy.

- [ ] **Step 4: Verify green and commit**

Run the same command. Commit message: `feat: add social propagation controls`.

## Slice 6: Contest And Repair Prototype

**Files:**
- Create: `world/social_claim_repair.py`
- Create: `commands/cmd_social_verbs.py`
- Modify: `commands/default_cmdsets.py`
- Create: `tests/test_social_claim_repair.py`
- Modify: `tests/test_cmd_dialogue.py` or command tests as needed

- [ ] **Step 1: Write failing repair tests**

Prove `deny <npc> about me` finds a known rumor/contested claim, records a player denial claim, marks the target NPC as knowing the denial through `direct_witness`, and leaves original facts intact. Prove unsupported/no-claim cases fail closed with a player-facing message.

- [ ] **Step 2: Verify red**

Run:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_social_claim_repair
```

Expected: fail because the service and command do not exist.

- [ ] **Step 3: Implement deterministic repair**

The command must create Social Web state through the service, not mutate standings or erase claims. It must not reveal raw claim keys to the player.

- [ ] **Step 4: Verify green and commit**

Run the same command. Commit message: `feat: add social claim denial verb`.

## Slice 7: DeepSeek/LLM Renderer Seam With Deterministic Fallback

**Files:**
- Create: `world/social_llm_renderer.py`
- Modify: `world/social_quest_offers.py`
- Create: `tests/test_social_llm_renderer.py`
- Modify: `docs/superpowers/specs/2026-07-08-social-quest-grammar-design.md`

- [ ] **Step 1: Write failing renderer tests**

Prove renderer input redacts secrets, includes only bounded `llm_context.prompt_inputs`, refuses provider calls when `provider_call_allowed` is false, falls back deterministically, and never mutates quest or Social Web state.

- [ ] **Step 2: Verify red**

Run:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_social_llm_renderer tests.test_social_quest_offers
```

Expected: fail because the renderer seam does not exist.

- [ ] **Step 3: Implement renderer seam**

Provide a provider interface compatible with DeepSeek-style chat completions, but keep provider calls disabled unless the caller explicitly passes `allow_provider_call=True` and the quest context itself allows it. No API key is read unless a provider call is actually attempted.

- [ ] **Step 4: Verify green and commit**

Run the same command. Commit message: `feat: add social llm renderer seam`.

## Slice 8: Playtest Harness And Route Script

**Files:**
- Create: `scripts/playtest_social_web_vertical.py`
- Create: `docs/playtests/social-web-vaels-crossing.md`
- Create: `tests/test_social_web_playtest_harness.py`

- [ ] **Step 1: Write failing harness test**

Prove the harness prints each required playtest beat: Warden report completion, Calloway explanation, Harven cross-zone knowledge, Whistle local rumor knowledge only after traveler propagation, dynamic social quest lifecycle, denial/repair verb, renderer fallback, and admin `socialmemory` inspection.

- [ ] **Step 2: Verify red**

Run:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_social_web_playtest_harness
```

Expected: fail because the script and docs do not exist.

- [ ] **Step 3: Implement harness and human playtest guide**

The script should be deterministic, side-effect-light, and usable from the repo without a running public server. The guide should list exact MUD commands and expected qualitative observations, not numeric reputation meters.

- [ ] **Step 4: Verify green and commit**

Run the same command. Commit message: `test: add social web playtest harness`.

## Final Audit

- [ ] Run focused Social Web test suite:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py tests.test_social_web_kernel tests.test_social_web_warden_route tests.test_social_quest_grammar tests.test_social_quest_offers tests.test_social_quest_lifecycle tests.test_social_interpretation tests.test_social_claim_repair tests.test_social_llm_renderer tests.test_social_web_playtest_harness tests.test_dialogue tests.test_cmd_dialogue tests.test_socialmemory_command tests.test_action_vocabulary tests.test_content_authoring
```

- [ ] Run full test suite:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/run_tests.py
```

- [ ] Run smoke start:

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/smoke_start.py
```

- [ ] Run formatting/lint/static checks discovered from repo tooling.
- [ ] Run security audit with available Python/static tooling and inspect new renderer code for key leakage and provider-call hazards.
- [ ] Run `git diff --check`.
- [ ] Update Engram with commit, validation, and next step.
- [ ] Commit final audit/doc updates if they are a clean boundary.
