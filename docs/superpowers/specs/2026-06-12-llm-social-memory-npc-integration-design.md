# LLM Social Memory NPC Integration Design

**Date:** 2026-06-12
**Status:** Approved direction for implementation planning
**Repo:** `/Users/ckwichman/Documents/Projects/soravelon`

## Goal

Build a small, provable Vael's Crossing runtime slice where NPC interaction is
driven by deterministic social memory and can optionally be phrased by a
guarded LLM provider.

The feature should move Soravelon toward the new Fable-style social fantasy:
players are not merely good or evil, but locally known for concrete actions,
and different NPCs judge those reputations through their own values.

## Current Reality

Soravelon already has useful foundations:

- Character world-state dimensions include `reputation_score`,
  `network_score`, `bond_score`, `legacy_score`, and `attunement_score`.
- Faction standing, trust, and betrayal are persisted by `FactionStanding`.
- Mob disposition combines base disposition, faction standing, ancestry,
  scalar reputation, trust, and active quest modifiers.
- Dialogue already supports Standing-tier greetings, topic responses, hints,
  quest-state conditions, ambient echoes, and a context packet intended for a
  future LLM interface.
- `WorldEventLog` exists for significant world events.
- AreaBuilder can author literal NPC dialogue payloads and quest consequences.

But the existing system is not yet a Fable-like social reputation system:

- `reputation_score` is a scalar, not a local reputation cloud.
- Existing faction standing changes do not say what the player is known for.
- NPCs do not have authored worldview profiles that interpret the same
  reputation differently.
- `KnownTopicRecord` remembers learned dialogue topics, not NPC opinions,
  favors, grudges, fear, trust, or social memories.
- Quest `consequence_small` / `consequence_medium` text is mostly authored
  prose, not a runtime source of social behavior.
- The current live area catalog has 242 NPCs, but only 73 have authored
  dialogue and 19 have ambient behavior. Vael's Crossing has 4 dialogue-authored
  NPCs out of 55; Varath Prime has none.
- Existing area quest rewards modify faction standing, but the live scan found
  no area quest rewards that log social/world events.

## Binding Product Contract

This is not a "DeepSeek feature." It is a Soravelon social-memory feature with
an optional LLM voice layer.

The game must own truth. The LLM may phrase truth.

Deterministic systems decide:

- which social facts exist
- who witnessed those facts
- where facts are known
- which reputation tags those facts produce
- how those tags aggregate locally
- how each NPC profile interprets those tags
- whether trust, access, price, quest availability, hints, or hostility change
- what hidden lore must remain unavailable

The LLM may only:

- phrase a greeting, rumor, or topic response from approved context
- vary tone inside an already selected response lane
- summarize a local reputation cloud for player-facing display
- draft authoring suggestions outside runtime mutation paths

The LLM must not:

- create durable facts
- mutate standing, trust, quests, inventory, access, or world state
- decide whether a fact is known
- reveal Remnance, Vaelborn, Echoes, dragon-continent truth, or other hidden
  current-era content not already exposed by deterministic context
- invent quest offers, NPC relationships, locations, factions, or consequences
- override authored fallback text

## First Vertical Slice

The first implementation slice is Vael's Crossing only.

Vael's Crossing is the correct first target because it is onboarding-critical
and currently under-authored as a dialogue/social surface.

Anchor NPCs:

- `npc_greeter_maren`
- `npc_barkeep_marta_voss`
- `npc_broker_carston`
- `npc_warden_agent_calloway`
- `npc_innkeeper_whistle`

Initial reputation tags:

- `reliable`
- `reckless`
- `generous`
- `shrewd`
- `warden_aligned`
- `profit_minded`

Initial fact sources:

- quest reward actions
- admin/development command for deterministic testing
- direct social-memory service calls in tests

Combat/crime detection can come later. It should not block this slice.

## Steelman Corrections Before Implementation

These corrections are binding for the implementation pass. If this section
conflicts with a lower-level task list, this section wins.

The MVP proves a quest-authored local social-memory loop. It should not be
described as the full Fable-like reputation system until non-quest social fact
sources such as crime, gifts, vendors, social choices, or observed combat are
added.

The player-facing proof must be diegetic and non-numeric:

- one immediate quest-completion echo that implies people noticed
- one later NPC recall from a different NPC in the same settlement
- one contrasting reaction where two NPCs interpret the same reputation cloud
  differently

`socialmemory` is a developer/admin inspection command only. If a player-facing
surface is added later, it must avoid numeric scores and use in-world wording.

`private` and `witnessed` facts must not leak into the settlement reputation
cloud. For the MVP, `get_local_reputation_cloud()` aggregates only
`settlement`, `faction`, and `global` facts and filters expired facts. A later
witness/rumor pass may add NPC-viewer-specific querying and promotion from
`witnessed` to settlement knowledge.

`NpcRelationship` may ship in the MVP only if it affects at least one
deterministic context field and one visible NPC response. Otherwise it should be
deferred instead of existing as unused infrastructure.

The optional LLM layer must not log raw prompts, raw API responses, secrets, or
player-private data by default. Logging should record bounded metadata such as
provider, model, cache hit/miss, latency, character counts, validation result,
and fallback reason.

## Terminology

**Social Fact**

A persisted, character-scoped record that something socially meaningful
happened. It carries tags, source metadata, locality, visibility, witnesses,
and a short summary.

**Reputation Tag**

A named descriptor inferred from one or more social facts. Tags are not moral
judgments by themselves. `generous`, `shrewd`, and `reckless` are facts about
how the player is talked about; different NPCs decide whether those tags are
good or bad.

**Local Reputation Cloud**

The derived set of weighted tags a character is known for in a settlement or
zone. The cloud is local by default. For the MVP, `settlement_id` defaults to
`zone_id` when no richer settlement model exists.

**NPC Social Profile**

Authored NPC worldview metadata that says which tags the NPC admires, dislikes,
fears, or treats as useful. This belongs in builder-safe authored NPC data, not
in LLM prompts alone.

**NPC Relationship**

A persisted character-to-NPC relationship record containing local affinity,
trust, fear, respect, and recent interaction metadata. This is separate from
faction standing.

**LLM Voice Layer**

An optional runtime renderer that turns deterministic social context into
in-character speech. It is provider-neutral and guarded by validation,
feature flags, timeout handling, and deterministic fallback text.

## Data Model

### `SocialMemoryFact`

Create in `world/models.py`.

Fields:

- `character`: FK to `objects.ObjectDB`, `related_name="social_memory_facts"`
- `fact_key`: stable idempotency key, unique per character
- `fact_type`: string such as `quest_consequence`, `gift`, `reckless_action`
- `settlement_id`: string, defaulting to zone id when not provided
- `zone_id`: string
- `faction_id`: optional string
- `subject_npc_id`: optional string
- `source_type`: string such as `quest`, `admin`, `trigger`, `test`
- `source_id`: source-specific id such as quest id
- `tags`: JSON list of reputation tag strings
- `witness_npc_ids`: JSON list of NPC ids
- `visibility`: one of `private`, `witnessed`, `settlement`, `faction`,
  `global`
- `weight`: float, default `1.0`
- `confidence`: float, default `1.0`
- `summary`: player-safe short text
- `created_at`: timestamp
- `expires_at`: optional timestamp

Constraints and indexes:

- unique constraint on `character` + `fact_key`
- index on `character`, `settlement_id`, `visibility`
- index on `character`, `faction_id`
- index on `created_at`

### `NpcRelationship`

Create in `world/models.py`.

Fields:

- `character`: FK to `objects.ObjectDB`, `related_name="npc_relationships"`
- `npc_id`: NPC id string
- `affinity`: integer `-100` to `100`
- `trust`: integer `0` to `100`
- `fear`: integer `0` to `100`
- `respect`: integer `0` to `100`
- `known_tags`: JSON list of reputation tag strings this NPC has reacted to
- `notes`: JSON object for bounded future metadata
- `last_interaction_at`: optional timestamp
- `updated_at`: timestamp

Constraints and indexes:

- unique constraint on `character` + `npc_id`
- index on `character`, `npc_id`

### NPC Authored Social Profile

Do not create a dedicated model for static NPC profile data in the MVP.
AreaBuilder should set profile data on NPC db attributes so the content remains
builder-safe and co-located with the NPC definition.

Add optional `social_profile={...}` support to `area.npc(...)`.

Shape:

```python
social_profile={
    "settlement_id": "vaels_crossing",
    "values": {
        "admires": ["reliable", "generous"],
        "dislikes": ["reckless"],
        "fears": [],
        "finds_useful": ["shrewd"],
    },
    "voice": "practical, watchful, civic",
    "public_role": "gate greeter",
    "rumor_role": "hears early traveler stories",
}
```

AreaBuilder should store:

- `npc.db.social_profile`
- `npc.db.settlement_id`

The social profile is not secret. Hidden lore must not be placed in it.

## Deterministic Service Layer

Create `world/social_memory.py`.

Responsibilities:

- validate and normalize reputation tags
- record idempotent social facts
- derive local reputation clouds
- retrieve NPC social profiles from db attrs
- score how an NPC interprets a reputation cloud
- upsert NPC relationship deltas when explicitly requested
- build a player-safe social context packet for dialogue and LLM rendering

Important functions:

- `normalize_tags(tags) -> list[str]`
- `record_social_fact(character, *, fact_key, fact_type, tags, summary,
  settlement_id=None, zone_id=None, faction_id="", subject_npc_id="",
  source_type="", source_id="", witness_npc_ids=None,
  visibility="settlement", weight=1.0, confidence=1.0) -> SocialMemoryFact`
- `get_local_reputation_cloud(character, settlement_id, *, limit=8) -> list[dict]`
- `get_npc_social_profile(npc) -> dict`
- `get_npc_relationship_summary(character, npc) -> dict`
- `score_npc_reaction(profile, reputation_cloud) -> dict`
- `build_social_context(character, npc=None, settlement_id=None) -> dict`

The cloud scoring formula for the MVP should be simple and auditable:

```text
tag_score = sum(fact.weight * fact.confidence for visible facts carrying tag)
```

Sort by descending score, then tag name for deterministic tie-breaking.

## Dialogue Integration

Extend `world.dialogue_engine._build_dialogue_context()` to include:

- `settlement_id`
- `local_reputation_cloud`
- `npc_social_profile`
- `npc_social_reaction`
- `npc_relationship`

The existing context packet shape must remain backward compatible. Add keys;
do not rename existing keys.

Extend response conditions with small deterministic conditions:

- `likes_reputation`
- `dislikes_reputation`
- `fears_reputation`
- `uses_reputation`
- `trusts_relationship`
- `distrusts_relationship`

These conditions are driven by `score_npc_reaction()`, not by the LLM.

NPC authored dialogue should still be the first fallback. The LLM is optional.

## LLM Provider Layer

Create `world/llm_npc.py`.

Provider-neutral settings:

- `SORAVELON_NPC_LLM_ENABLED`
- `SORAVELON_NPC_LLM_PROVIDER`
- `SORAVELON_NPC_LLM_MODEL`
- `SORAVELON_NPC_LLM_API_KEY`
- `SORAVELON_NPC_LLM_BASE_URL`
- `SORAVELON_NPC_LLM_TIMEOUT_SECONDS`
- `SORAVELON_NPC_LLM_MAX_INPUT_CHARS`
- `SORAVELON_NPC_LLM_CACHE_TTL_SECONDS`
- `SORAVELON_NPC_LLM_MAX_CALLS_PER_MINUTE`

Provider support:

- MVP provider interface uses OpenAI-compatible chat completions because
  DeepSeek and many other providers support that shape.
- A fake provider must exist for tests.
- Runtime provider errors must not surface stack traces to players.

Request contract:

- Inputs must be player-safe and bounded.
- Prompt must explicitly forbid new facts, hidden lore, quest mutation, and
  system mutation.
- The LLM response must be JSON.
- The displayed text must come only from the `speech` field.

Response schema:

```json
{
  "speech": "string",
  "tone": "neutral|warm|wary|hostile|amused|respectful",
  "referenced_fact_keys": ["string"],
  "used_reputation_tags": ["string"],
  "safety_notes": []
}
```

Validation:

- reject invalid JSON
- reject missing or non-string `speech`
- reject speech above the configured length
- reject unknown `referenced_fact_keys`
- reject unknown `used_reputation_tags`
- reject hidden terms filtered by `world/remnance_visibility.py` and a small
  explicit forbidden-term list for current-era secrets
- reject attempts to include commands, unlocks, rewards, or mutation claims

Fallback:

- If disabled, errored, timed out, invalid, or unsafe, use authored
  deterministic dialogue.
- If no authored dialogue exists, use the existing generic fallback.

Caching:

Cache rendered speech by:

- `npc_id`
- `topic_key`
- `standing_tier`
- local reputation cloud tag/score signature
- relationship summary signature
- prompt version

The MVP cache can use a short-lived module-level dict. A database cache can be
added later if runtime volume requires it.

## Action Vocabulary Integration

Add action types:

- `record_social_fact`
- `adjust_npc_relationship`

Example quest reward action:

```python
{
    "action_type": "record_social_fact",
    "fact_key": "vc_maren_welcome_reliable",
    "fact_type": "quest_consequence",
    "settlement_id": "vaels_crossing",
    "tags": ["reliable"],
    "summary": "Maren saw you follow through on a small civic errand.",
    "visibility": "settlement",
    "weight": 1.0,
}
```

The action handler must be idempotent through `fact_key`.

## Player-Facing Surface

Add a development/admin command for validation:

- `socialmemory`
- `socialmemory here`
- `socialmemory <settlement_id>`

It should display the character's local reputation cloud and top fact summaries.

This is not a final player-facing social UI. It is a proof and debugging tool.

If exposed to non-admin players later, wording should stay diegetic and avoid
numbers.

## Vael's Crossing Authoring Requirements

For the MVP, add social profiles and dialogue reactions to the anchor NPCs.

Each anchor NPC must have:

- non-empty `dialogue`
- non-empty `social_profile`
- at least one `base_hints` entry
- at least one response that changes when the NPC likes the current local
  reputation
- at least one response that changes when the NPC dislikes the current local
  reputation

The ordinary local should demonstrate that non-quest NPCs can react socially
without becoming full quest dispensers.

## Safety And Lore Guardrails

All LLM context must pass through the same hidden-content discipline as other
player-facing surfaces:

- no casual Remnance exposure
- no Vaelborn exposure
- no Echoes exposure unless already discovered and visible through existing
  visibility rules
- no dragon-continent revelation
- no implication that current-era dragons are secretly intelligent under the
  curse
- no invented faction facts
- no invented quest state

The LLM must receive only player-safe summaries. It should not receive raw
internal backend level, hidden design notes, secret lore, or private developer
instructions beyond the prompt guardrails.

## Cost Guardrails

The runtime must be built so no provider call is required for ordinary gameplay.

Initial recommended policy:

- `SORAVELON_NPC_LLM_ENABLED=false` by default
- enable only in development or explicitly configured deployments
- use deterministic dialogue for all tests except fake-provider tests
- cap input context by chars
- cap output speech length
- cache aggressively
- add logging for provider, model, cache hit/miss, latency, input chars, output
  chars, validation result, and fallback reason

Current provider pricing should be checked at implementation time before any
production deployment. Pricing changes too often to bake into runtime logic.

## Validation Contract

Tests must prove real behavior, not merely string changes.

Required proofs:

- social facts are idempotently recorded by `fact_key`
- local reputation clouds aggregate tags for one settlement without leaking into
  another settlement
- local reputation clouds exclude `private`, `witnessed`, and expired facts
- the same reputation cloud produces different reactions for two NPC profiles
- dialogue context contains social memory keys without breaking existing keys
- action vocabulary can record a social fact from a quest-like context
- LLM disabled path uses deterministic fallback
- LLM calls are rate guarded when enabled
- fake LLM valid JSON can render speech
- fake LLM unsafe or invalid output falls back
- hidden/forbidden terms are rejected
- Vael's Crossing anchor NPCs have social profiles and dialogue
- Vael's Crossing play transcript proves one immediate echo, one later recall,
  and one contrasting NPC interpretation

Recommended command:

```bash
python scripts/run_tests.py tests.test_social_memory tests.test_llm_npc tests.test_dialogue tests.test_action_vocabulary tests.test_vaels_crossing_social_contracts
```

Run `python scripts/smoke_start.py` after implementation if the migration and
settings changes are complete enough to boot the server.

## Non-Goals

These are deliberately out of scope for the MVP:

- full town schedules, homes, families, romance, or marriage
- crime/bounty simulation
- property ownership and employment systems
- global rumor economics
- LLM-generated quests
- LLM mutation of durable world state
- replacing authored dialogue
- provider-specific lock-in to DeepSeek
- Varath Prime catalog-wide remediation
- full web UI for reputation

## Open Follow-Up After MVP

After the Vael's Crossing slice is proven, the next decision should be whether
to expand by:

1. more social fact sources, such as combat/crime/gifts/vendors;
2. more Vael's Crossing NPC coverage;
3. a second settlement contrast pass, likely Korahei or Varath Prime;
4. a player-facing reputation journal.

Do not expand all four at once.
