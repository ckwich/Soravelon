# LLM Social Memory NPC Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Vael's Crossing runtime MVP where deterministic social memory drives NPC reactions and an optional guarded LLM voice layer can phrase those reactions safely.

**Architecture:** Add persisted social facts and NPC relationships, then derive local reputation clouds through `world/social_memory.py`. AreaBuilder stores authored NPC social profiles on NPC db attrs. Dialogue consumes deterministic social context first; `world/llm_npc.py` can render bounded speech only when explicitly enabled and validated.

**Tech Stack:** Evennia 6.0, Django ORM migrations, Python 3.11, existing `scripts/run_tests.py`, provider-neutral OpenAI-compatible chat completions for optional LLM calls.

---

## Scope Check

This plan implements the approved MVP spec:

- spec: `docs/superpowers/specs/2026-06-12-llm-social-memory-npc-integration-design.md`
- first content target: Vael's Crossing anchor NPCs
- default runtime: deterministic, LLM disabled
- provider lock-in: none

Out of scope:

- crime/bounty simulation
- schedules, homes, romance, property, employment
- generated quests
- broad NPC coverage outside Vael's Crossing

## Steelman Corrections Before Implementation

These corrections are binding. If this section conflicts with a later task
detail, this section wins.

The MVP proves a quest-authored local social-memory loop, not the full
Fable-like reputation fantasy. Do not claim full reputation coverage until a
later slice adds non-quest social fact sources such as crime, gifts, vendors,
social choices, or observed combat.

The player-facing proof must be diegetic and non-numeric:

- one immediate quest-completion echo that implies people noticed
- one later NPC recall from a different NPC in Vael's Crossing
- one contrasting reaction where two NPCs interpret the same reputation cloud
  differently

Use `npc_innkeeper_whistle` as the ordinary local in the Vael's Crossing slice.

`socialmemory` is a developer/admin inspection command only. Do not register it
with `cmd:all()` or publish player-facing help unless the command is locked to
builders/admins. A future player command must avoid score numbers and use
in-world wording.

`get_local_reputation_cloud()` must exclude `private` and `witnessed` facts,
filter expired facts, and aggregate only `settlement`, `faction`, and `global`
facts for the MVP. A future witness/rumor slice can add NPC-viewer-specific
queries and promotion from witnessed knowledge to settlement rumor.

`NpcRelationship` may ship in this MVP only if it drives at least one
deterministic context field and one visible NPC response. Otherwise defer the
model and `adjust_npc_relationship` action instead of adding unused
infrastructure.

The optional LLM path must include a per-character or per-session rate guard and
must not log raw prompts, raw API responses, API keys, or player-private data by
default. Log bounded metadata only: provider, model, cache hit/miss, latency,
input/output character counts, validation result, and fallback reason.

Add a manual or automated transcript proof before final validation: complete
`vc_q_warden_report` and `vc_q_missing_shipment`, then ask/talk to Maren,
Calloway, Carston, Marta, and Whistle. The transcript must show at least one
recall and one contrasting NPC interpretation.

## File Map

Create:

- `world/social_memory.py`: deterministic fact recording, cloud aggregation, NPC profile scoring, social context packet.
- `world/llm_npc.py`: optional provider interface, prompt assembly, JSON validation, cache, fallback reasons.
- `commands/cmd_social_memory.py`: development command for inspecting local reputation.
- `tests/test_social_memory.py`: model/service tests.
- `tests/test_llm_npc.py`: fake-provider and validation tests.
- `tests/test_vaels_crossing_social_contracts.py`: area authoring contract tests.

Modify:

- `world/models.py`: add `SocialMemoryFact` and `NpcRelationship`.
- `world/action_vocabulary.py`: add `record_social_fact` and `adjust_npc_relationship` handlers.
- `world/area_builder.py`: accept and store `social_profile` in `area.npc(...)`.
- `world/dialogue_definitions.py`: add deterministic social reaction conditions to `RESPONSE_PRIORITY`.
- `world/dialogue_engine.py`: add social context keys and condition checks.
- `commands/cmd_dialogue.py`: optional LLM rendering path for `talk`, `ask`, and NPC `tell`.
- `commands/default_cmdsets.py`: register `CmdSocialMemory`.
- `world/areas/vaels_crossing.py`: add social profiles and social-memory reward actions for anchor NPCs.
- `world/help_entries.py`: add direct help for `socialmemory` only if command
  registration is builder/admin locked.
- `tests/test_action_vocabulary.py`: add action handler tests and update handler count.
- `tests/test_dialogue.py`: add dialogue-context and optional LLM fallback tests.

Migration:

- Generate one Django migration for the new models after Task 1.

## Task 1: Persist Social Memory Models

**Files:**

- Modify: `world/models.py`
- Create: `tests/test_social_memory.py`
- Generate: `world/migrations/0009_socialmemoryfact_npcrelationship.py`

- [ ] **Step 1: Write failing model tests**

Create `tests/test_social_memory.py` with:

```python
from evennia.utils.test_resources import EvenniaTest


class TestSocialMemoryModels(EvenniaTest):
    """Persisted social memory records are character-scoped."""

    def test_social_memory_fact_unique_per_character_fact_key(self):
        from django.db import IntegrityError
        from world.models import SocialMemoryFact

        SocialMemoryFact.objects.create(
            character=self.char1,
            fact_key="vc_test_reliable",
            fact_type="test",
            settlement_id="vaels_crossing",
            zone_id="vaels_crossing",
            tags=["reliable"],
            summary="Maren saw the test character follow through.",
        )

        with self.assertRaises(IntegrityError):
            SocialMemoryFact.objects.create(
                character=self.char1,
                fact_key="vc_test_reliable",
                fact_type="test",
                settlement_id="vaels_crossing",
                zone_id="vaels_crossing",
                tags=["generous"],
                summary="Duplicate fact key should fail for the same character.",
            )

    def test_npc_relationship_unique_per_character_npc(self):
        from django.db import IntegrityError
        from world.models import NpcRelationship

        NpcRelationship.objects.create(
            character=self.char1,
            npc_id="npc_greeter_maren",
            affinity=10,
            trust=55,
        )

        with self.assertRaises(IntegrityError):
            NpcRelationship.objects.create(
                character=self.char1,
                npc_id="npc_greeter_maren",
                affinity=20,
                trust=60,
            )
```

- [ ] **Step 2: Run model tests and verify they fail**

Run:

```bash
python scripts/run_tests.py tests.test_social_memory
```

Expected: FAIL because `SocialMemoryFact` and `NpcRelationship` do not exist.

- [ ] **Step 3: Add models**

Append these classes after `WorldEventLog` in `world/models.py`:

```python
class SocialMemoryFact(models.Model):
    """
    Character-scoped social fact used to derive local reputation clouds.

    A fact records what the character is known for, where that knowledge is
    available, and which reputation tags it contributes.
    """

    VISIBILITY_CHOICES = [
        ("private", "Private"),
        ("witnessed", "Witnessed"),
        ("settlement", "Settlement"),
        ("faction", "Faction"),
        ("global", "Global"),
    ]

    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="social_memory_facts",
    )
    fact_key = models.CharField(max_length=160)
    fact_type = models.CharField(max_length=64, db_index=True)
    settlement_id = models.CharField(max_length=64, db_index=True)
    zone_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    faction_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    subject_npc_id = models.CharField(max_length=128, blank=True, default="")
    source_type = models.CharField(max_length=64, blank=True, default="")
    source_id = models.CharField(max_length=128, blank=True, default="")
    tags = models.JSONField(default=list)
    witness_npc_ids = models.JSONField(default=list)
    visibility = models.CharField(
        max_length=16,
        choices=VISIBILITY_CHOICES,
        default="settlement",
        db_index=True,
    )
    weight = models.FloatField(default=1.0)
    confidence = models.FloatField(default=1.0)
    summary = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["character", "fact_key"],
                name="unique_social_memory_fact_per_character",
            ),
        ]
        indexes = [
            models.Index(fields=["character", "settlement_id", "visibility"]),
            models.Index(fields=["character", "faction_id"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.fact_key}"


class NpcRelationship(models.Model):
    """Character-to-NPC social relationship separate from faction standing."""

    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="npc_relationships",
    )
    npc_id = models.CharField(max_length=128)
    affinity = models.IntegerField(default=0)
    trust = models.IntegerField(default=50)
    fear = models.IntegerField(default=0)
    respect = models.IntegerField(default=0)
    known_tags = models.JSONField(default=list)
    notes = models.JSONField(default=dict)
    last_interaction_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["character", "npc_id"],
                name="unique_npc_relationship_per_character",
            ),
        ]
        indexes = [
            models.Index(fields=["character", "npc_id"]),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.npc_id}"
```

- [ ] **Step 4: Generate migration**

Run:

```bash
python -m django makemigrations world --settings server.conf.settings
```

Expected: creates `world/migrations/0009_socialmemoryfact_npcrelationship.py`.

- [ ] **Step 5: Run model tests and verify they pass**

Run:

```bash
python scripts/run_tests.py tests.test_social_memory
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add world/models.py world/migrations/0009_socialmemoryfact_npcrelationship.py tests/test_social_memory.py
git commit -m "feat: add social memory models"
```

## Task 2: Implement Deterministic Social Memory Service

**Files:**

- Create: `world/social_memory.py`
- Modify: `tests/test_social_memory.py`

- [ ] **Step 1: Add failing service tests**

Append to `tests/test_social_memory.py`:

```python
class TestSocialMemoryService(EvenniaTest):
    """Social memory service derives local reputation from persisted facts."""

    def test_record_social_fact_is_idempotent(self):
        from world.models import SocialMemoryFact
        from world.social_memory import record_social_fact

        first = record_social_fact(
            self.char1,
            fact_key="vc_helped_maren",
            fact_type="quest_consequence",
            settlement_id="vaels_crossing",
            tags=[" reliable ", "Reliable", "generous"],
            summary="Maren saw the character help without fuss.",
        )
        second = record_social_fact(
            self.char1,
            fact_key="vc_helped_maren",
            fact_type="quest_consequence",
            settlement_id="vaels_crossing",
            tags=["reckless"],
            summary="This update should replace the previous payload.",
        )

        self.assertEqual(first.id, second.id)
        self.assertEqual(SocialMemoryFact.objects.count(), 1)
        self.assertEqual(second.tags, ["reckless"])

    def test_local_cloud_does_not_leak_between_settlements(self):
        from world.social_memory import (
            get_local_reputation_cloud,
            record_social_fact,
        )

        record_social_fact(
            self.char1,
            fact_key="vc_reliable",
            fact_type="test",
            settlement_id="vaels_crossing",
            tags=["reliable"],
            summary="Vael's Crossing knows this character as reliable.",
            weight=2.0,
        )
        record_social_fact(
            self.char1,
            fact_key="korahei_generous",
            fact_type="test",
            settlement_id="korahei",
            tags=["generous"],
            summary="Korahei knows this character as generous.",
            weight=3.0,
        )

        cloud = get_local_reputation_cloud(self.char1, "vaels_crossing")

        self.assertEqual(cloud[0]["tag"], "reliable")
        self.assertEqual(cloud[0]["score"], 2.0)
        self.assertNotIn("generous", [entry["tag"] for entry in cloud])

    def test_local_cloud_excludes_private_witnessed_and_expired_facts(self):
        from datetime import timedelta
        from django.utils import timezone
        from world.models import SocialMemoryFact
        from world.social_memory import get_local_reputation_cloud, record_social_fact

        record_social_fact(
            self.char1,
            fact_key="vc_settlement_reliable",
            fact_type="test",
            settlement_id="vaels_crossing",
            tags=["reliable"],
            summary="Everyone in Vael's Crossing heard this.",
            visibility="settlement",
        )
        record_social_fact(
            self.char1,
            fact_key="vc_private_generous",
            fact_type="test",
            settlement_id="vaels_crossing",
            tags=["generous"],
            summary="Only one person knows this.",
            visibility="private",
        )
        record_social_fact(
            self.char1,
            fact_key="vc_witnessed_shrewd",
            fact_type="test",
            settlement_id="vaels_crossing",
            tags=["shrewd"],
            summary="A witness has not spread this yet.",
            visibility="witnessed",
            witness_npc_ids=["npc_barkeep_marta_voss"],
        )
        expired = record_social_fact(
            self.char1,
            fact_key="vc_expired_reckless",
            fact_type="test",
            settlement_id="vaels_crossing",
            tags=["reckless"],
            summary="This rumor has gone stale.",
            visibility="settlement",
        )
        SocialMemoryFact.objects.filter(id=expired.id).update(
            expires_at=timezone.now() - timedelta(days=1)
        )

        cloud = get_local_reputation_cloud(self.char1, "vaels_crossing")
        tags = [entry["tag"] for entry in cloud]

        self.assertEqual(tags, ["reliable"])

    def test_same_cloud_scores_differently_for_two_profiles(self):
        from world.social_memory import score_npc_reaction

        cloud = [{"tag": "shrewd", "score": 2.0, "evidence_count": 1}]
        broker = {
            "values": {
                "admires": [],
                "dislikes": [],
                "fears": [],
                "finds_useful": ["shrewd"],
            }
        }
        warden = {
            "values": {
                "admires": ["reliable"],
                "dislikes": ["shrewd"],
                "fears": [],
                "finds_useful": [],
            }
        }

        broker_reaction = score_npc_reaction(broker, cloud)
        warden_reaction = score_npc_reaction(warden, cloud)

        self.assertGreater(broker_reaction["useful_score"], 0)
        self.assertGreater(warden_reaction["dislike_score"], 0)

    def test_build_social_context_includes_npc_relationship(self):
        from unittest.mock import MagicMock
        from world.models import NpcRelationship
        from world.social_memory import build_social_context

        npc = MagicMock()
        npc.db.npc_id = "npc_warden_agent_calloway"
        npc.db.zone_id = "vaels_crossing"
        npc.db.settlement_id = "vaels_crossing"
        npc.db.social_profile = {}
        NpcRelationship.objects.create(
            character=self.char1,
            npc_id="npc_warden_agent_calloway",
            trust=70,
            respect=10,
        )

        context = build_social_context(self.char1, npc=npc)

        self.assertEqual(context["npc_relationship"]["trust"], 70)
        self.assertEqual(context["npc_relationship"]["respect"], 10)
```

- [ ] **Step 2: Run tests and verify service import fails**

Run:

```bash
python scripts/run_tests.py tests.test_social_memory
```

Expected: FAIL because `world.social_memory` does not exist.

- [ ] **Step 3: Create service implementation**

Create `world/social_memory.py`:

```python
"""Deterministic social memory and local reputation helpers."""

from collections import defaultdict


VALID_VISIBILITIES = {"private", "witnessed", "settlement", "faction", "global"}


def normalize_tags(tags):
    """Normalize tag strings while preserving first-seen order."""
    normalized = []
    seen = set()
    for tag in tags or []:
        cleaned = str(tag).strip().lower().replace(" ", "_")
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        normalized.append(cleaned)
    return normalized


def _clamp_float(value, low, high, default):
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        parsed = default
    return max(low, min(high, parsed))


def _coerce_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def record_social_fact(
    character,
    *,
    fact_key,
    fact_type,
    tags,
    summary,
    settlement_id=None,
    zone_id=None,
    faction_id="",
    subject_npc_id="",
    source_type="",
    source_id="",
    witness_npc_ids=None,
    visibility="settlement",
    weight=1.0,
    confidence=1.0,
):
    """Create or update a character-scoped social fact."""
    if not character:
        raise ValueError("record_social_fact requires character")
    if not fact_key:
        raise ValueError("record_social_fact requires fact_key")
    if not fact_type:
        raise ValueError("record_social_fact requires fact_type")

    normalized_tags = normalize_tags(tags)
    if not normalized_tags:
        raise ValueError("record_social_fact requires at least one tag")

    clean_visibility = visibility if visibility in VALID_VISIBILITIES else "settlement"
    clean_zone = zone_id or settlement_id or ""
    clean_settlement = settlement_id or clean_zone or "unknown"

    from world.models import SocialMemoryFact

    fact, _created = SocialMemoryFact.objects.update_or_create(
        character=character,
        fact_key=str(fact_key),
        defaults={
            "fact_type": str(fact_type),
            "settlement_id": str(clean_settlement),
            "zone_id": str(clean_zone),
            "faction_id": str(faction_id or ""),
            "subject_npc_id": str(subject_npc_id or ""),
            "source_type": str(source_type or ""),
            "source_id": str(source_id or ""),
            "tags": normalized_tags,
            "witness_npc_ids": [
                str(npc_id) for npc_id in _coerce_list(witness_npc_ids) if npc_id
            ],
            "visibility": clean_visibility,
            "weight": _clamp_float(weight, 0.0, 100.0, 1.0),
            "confidence": _clamp_float(confidence, 0.0, 1.0, 1.0),
            "summary": str(summary or ""),
        },
    )
    return fact


def get_local_reputation_cloud(character, settlement_id, *, limit=8):
    """Return weighted reputation tags known in a local settlement."""
    from django.db.models import Q
    from django.utils import timezone
    from world.models import SocialMemoryFact

    if not character or not settlement_id:
        return []

    facts = SocialMemoryFact.objects.filter(
        character=character,
        settlement_id=settlement_id,
        visibility__in=["settlement", "faction", "global"],
    ).filter(Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now()))

    scores = defaultdict(float)
    counts = defaultdict(int)
    fact_keys = defaultdict(list)

    for fact in facts:
        contribution = float(fact.weight or 0.0) * float(fact.confidence or 0.0)
        for tag in normalize_tags(fact.tags):
            scores[tag] += contribution
            counts[tag] += 1
            fact_keys[tag].append(fact.fact_key)

    entries = [
        {
            "tag": tag,
            "score": round(score, 4),
            "evidence_count": counts[tag],
            "fact_keys": fact_keys[tag],
        }
        for tag, score in scores.items()
        if score > 0
    ]
    entries.sort(key=lambda entry: (-entry["score"], entry["tag"]))
    return entries[:limit]


def get_npc_social_profile(npc):
    """Read builder-authored social profile data from an NPC object."""
    if not npc or not hasattr(npc, "db"):
        return {}
    profile = npc.db.social_profile or {}
    return profile if isinstance(profile, dict) else {}


def get_npc_relationship_summary(character, npc):
    """Return bounded relationship state for the current character/NPC pair."""
    if not character or not npc or not hasattr(npc, "db"):
        return {}
    npc_id = npc.db.npc_id or getattr(npc, "key", "")
    if not npc_id:
        return {}

    from world.models import NpcRelationship

    relationship = NpcRelationship.objects.filter(
        character=character,
        npc_id=str(npc_id),
    ).first()
    if not relationship:
        return {}

    return {
        "npc_id": relationship.npc_id,
        "affinity": relationship.affinity,
        "trust": relationship.trust,
        "fear": relationship.fear,
        "respect": relationship.respect,
        "known_tags": list(relationship.known_tags or []),
    }


def score_npc_reaction(profile, reputation_cloud):
    """Score how an NPC profile interprets a local reputation cloud."""
    values = (profile or {}).get("values") or {}
    buckets = {
        "admires": set(normalize_tags(values.get("admires", []))),
        "dislikes": set(normalize_tags(values.get("dislikes", []))),
        "fears": set(normalize_tags(values.get("fears", []))),
        "finds_useful": set(normalize_tags(values.get("finds_useful", []))),
    }
    result = {
        "admire_score": 0.0,
        "dislike_score": 0.0,
        "fear_score": 0.0,
        "useful_score": 0.0,
        "matched_tags": [],
    }

    for entry in reputation_cloud or []:
        tag = str(entry.get("tag", "")).strip().lower()
        score = float(entry.get("score", 0.0) or 0.0)
        if tag in buckets["admires"]:
            result["admire_score"] += score
            result["matched_tags"].append(tag)
        if tag in buckets["dislikes"]:
            result["dislike_score"] += score
            result["matched_tags"].append(tag)
        if tag in buckets["fears"]:
            result["fear_score"] += score
            result["matched_tags"].append(tag)
        if tag in buckets["finds_useful"]:
            result["useful_score"] += score
            result["matched_tags"].append(tag)

    result["matched_tags"] = sorted(set(result["matched_tags"]))
    return result


def build_social_context(character, npc=None, settlement_id=None):
    """Build the player-safe social context consumed by dialogue and LLM code."""
    profile = get_npc_social_profile(npc)
    zone_id = ""
    if npc and hasattr(npc, "db"):
        zone_id = npc.db.zone_id or ""
    clean_settlement = (
        settlement_id
        or profile.get("settlement_id")
        or (npc.db.settlement_id if npc and hasattr(npc, "db") else "")
        or zone_id
        or "unknown"
    )
    cloud = get_local_reputation_cloud(character, clean_settlement)
    relationship = get_npc_relationship_summary(character, npc)
    return {
        "character_id": str(getattr(character, "id", "") or ""),
        "character_key": str(getattr(character, "key", "") or ""),
        "settlement_id": clean_settlement,
        "local_reputation_cloud": cloud,
        "npc_social_profile": profile,
        "npc_social_reaction": score_npc_reaction(profile, cloud),
        "npc_relationship": relationship,
    }
```

- [ ] **Step 4: Run social memory tests**

Run:

```bash
python scripts/run_tests.py tests.test_social_memory
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add world/social_memory.py tests/test_social_memory.py
git commit -m "feat: derive local social reputation"
```

## Task 3: Add Social Memory Action Handlers

**Files:**

- Modify: `world/action_vocabulary.py`
- Modify: `tests/test_action_vocabulary.py`

- [ ] **Step 1: Add failing action tests**

Append to `tests/test_action_vocabulary.py`:

```python
class TestSocialMemoryActions(EvenniaTest):
    """Action vocabulary can write deterministic social memory."""

    def test_record_social_fact_action(self):
        from world.action_vocabulary import execute_action
        from world.models import SocialMemoryFact

        success, msg = execute_action(
            {
                "action_type": "record_social_fact",
                "fact_key": "vc_action_reliable",
                "fact_type": "quest_consequence",
                "settlement_id": "vaels_crossing",
                "tags": ["reliable"],
                "summary": "The road remembers a reliable helper.",
                "visibility": "settlement",
            },
            {"character": self.char1},
        )

        self.assertTrue(success, msg)
        fact = SocialMemoryFact.objects.get(
            character=self.char1,
            fact_key="vc_action_reliable",
        )
        self.assertEqual(fact.tags, ["reliable"])

    def test_adjust_npc_relationship_action(self):
        from world.action_vocabulary import execute_action
        from world.models import NpcRelationship

        success, msg = execute_action(
            {
                "action_type": "adjust_npc_relationship",
                "npc_id": "npc_greeter_maren",
                "affinity_delta": 5,
                "trust_delta": 3,
                "respect_delta": 2,
                "fear_delta": 1,
                "known_tags": ["reliable"],
            },
            {"character": self.char1},
        )

        self.assertTrue(success, msg)
        rel = NpcRelationship.objects.get(
            character=self.char1,
            npc_id="npc_greeter_maren",
        )
        self.assertEqual(rel.affinity, 5)
        self.assertEqual(rel.trust, 53)
        self.assertEqual(rel.respect, 2)
        self.assertEqual(rel.fear, 1)
        self.assertEqual(rel.known_tags, ["reliable"])
```

Update existing handler registry tests in `TestActionHandlersRegistry`:

```python
self.assertEqual(len(ACTION_HANDLERS), 20)
```

and add `"record_social_fact"` and `"adjust_npc_relationship"` to the expected
set.

- [ ] **Step 2: Run action tests and verify failure**

Run:

```bash
python scripts/run_tests.py tests.test_action_vocabulary
```

Expected: FAIL because handlers are not registered.

- [ ] **Step 3: Implement handlers**

Add to `world/action_vocabulary.py` above `ACTION_HANDLERS`:

```python
def _handle_record_social_fact(action_dict, context, _depth):
    """Record a deterministic social memory fact for the character."""
    character = context.get("character")
    if not character:
        return False, "No character in context"

    room = context.get("room") or getattr(character, "location", None)
    zone_id = action_dict.get("zone_id")
    if not zone_id and room and hasattr(room, "db"):
        zone_id = room.db.zone_id or ""

    try:
        from world.social_memory import record_social_fact
        record_social_fact(
            character,
            fact_key=action_dict.get("fact_key"),
            fact_type=action_dict.get("fact_type", "action"),
            settlement_id=action_dict.get("settlement_id") or zone_id,
            zone_id=zone_id,
            faction_id=action_dict.get("faction_id", ""),
            subject_npc_id=action_dict.get("subject_npc_id", ""),
            source_type=action_dict.get("source_type", "action"),
            source_id=action_dict.get("source_id", ""),
            tags=action_dict.get("tags", []),
            witness_npc_ids=action_dict.get("witness_npc_ids", []),
            visibility=action_dict.get("visibility", "settlement"),
            weight=action_dict.get("weight", 1.0),
            confidence=action_dict.get("confidence", 1.0),
            summary=action_dict.get("summary", ""),
        )
    except ValueError as exc:
        return False, str(exc)

    return True, ""


def _clamp_int(value, low, high, default):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(low, min(high, parsed))


def _handle_adjust_npc_relationship(action_dict, context, _depth):
    """Apply bounded relationship deltas for one character/NPC pair."""
    character = context.get("character")
    if not character:
        return False, "No character in context"
    npc_id = action_dict.get("npc_id")
    if not npc_id:
        return False, "adjust_npc_relationship: missing npc_id"

    from world.models import NpcRelationship
    from world.social_memory import normalize_tags

    rel, _created = NpcRelationship.objects.get_or_create(
        character=character,
        npc_id=npc_id,
        defaults={"trust": 50},
    )
    rel.affinity = _clamp_int(
        rel.affinity + int(action_dict.get("affinity_delta", 0) or 0),
        -100,
        100,
        rel.affinity,
    )
    rel.trust = _clamp_int(
        rel.trust + int(action_dict.get("trust_delta", 0) or 0),
        0,
        100,
        rel.trust,
    )
    rel.fear = _clamp_int(
        rel.fear + int(action_dict.get("fear_delta", 0) or 0),
        0,
        100,
        rel.fear,
    )
    rel.respect = _clamp_int(
        rel.respect + int(action_dict.get("respect_delta", 0) or 0),
        0,
        100,
        rel.respect,
    )
    known = list(rel.known_tags or [])
    for tag in normalize_tags(action_dict.get("known_tags", [])):
        if tag not in known:
            known.append(tag)
    rel.known_tags = known
    rel.save()
    return True, ""
```

Register in `ACTION_HANDLERS`:

```python
"record_social_fact": _handle_record_social_fact,
"adjust_npc_relationship": _handle_adjust_npc_relationship,
```

- [ ] **Step 4: Run action tests**

Run:

```bash
python scripts/run_tests.py tests.test_action_vocabulary
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add world/action_vocabulary.py tests/test_action_vocabulary.py
git commit -m "feat: add social memory actions"
```

## Task 4: Store NPC Social Profiles Through AreaBuilder

**Files:**

- Modify: `world/area_builder.py`
- Modify: `tests/test_social_memory.py`

- [ ] **Step 1: Add failing AreaBuilder profile test**

Append to `tests/test_social_memory.py`:

```python
class TestAreaBuilderSocialProfile(EvenniaTest):
    """AreaBuilder stores authored social profiles on NPC objects."""

    def test_npc_social_profile_stored_on_db_attrs(self):
        from world.area_builder import AreaBuilder

        area = AreaBuilder("test_social_zone")
        area.zone(name="Test Social Zone", zone_type="hub")
        room = area.room("social_room", name="Social Room", desc="A test room.")
        npc = area.npc(
            room,
            "npc_social_test",
            name="Social Test",
            social_profile={
                "settlement_id": "test_social_zone",
                "values": {
                    "admires": ["reliable"],
                    "dislikes": ["reckless"],
                    "fears": [],
                    "finds_useful": ["shrewd"],
                },
                "voice": "plainspoken",
                "public_role": "test witness",
                "rumor_role": "hears test rumors",
            },
        )

        self.assertEqual(npc.db.settlement_id, "test_social_zone")
        self.assertEqual(
            npc.db.social_profile["values"]["admires"],
            ["reliable"],
        )
```

- [ ] **Step 2: Run test and verify failure**

Run:

```bash
python scripts/run_tests.py tests.test_social_memory
```

Expected: FAIL because `area.npc(...)` ignores `social_profile`.

- [ ] **Step 3: Store profile data in AreaBuilder**

In `world/area_builder.py`, inside `AreaBuilder.npc()` after `npc_obj.db.npc_id = npc_id`, add:

```python
        social_profile = kwargs.get("social_profile", {}) or {}
        if not isinstance(social_profile, dict):
            social_profile = {}
        npc_obj.db.social_profile = social_profile
        npc_obj.db.settlement_id = (
            social_profile.get("settlement_id")
            or kwargs.get("settlement_id")
            or self._zone_id
        )
```

- [ ] **Step 4: Run social memory tests**

Run:

```bash
python scripts/run_tests.py tests.test_social_memory
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add world/area_builder.py tests/test_social_memory.py
git commit -m "feat: store npc social profiles"
```

## Task 5: Add Social Context To Dialogue

**Files:**

- Modify: `world/dialogue_definitions.py`
- Modify: `world/dialogue_engine.py`
- Modify: `tests/test_dialogue.py`

- [ ] **Step 1: Add failing dialogue context tests**

Append to `tests/test_dialogue.py`:

```python
class TestDialogueSocialContext(unittest.TestCase):
    """Dialogue context includes deterministic social memory."""

    @patch("world.models.CharacterQuest.objects")
    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    @patch("world.social_memory.build_social_context")
    def test_social_context_keys_added(
        self,
        mock_social,
        mock_packet,
        mock_tier,
        mock_active,
        mock_cq,
    ):
        from world.dialogue_engine import _build_dialogue_context

        mock_packet.return_value = {"reputation": 0}
        mock_social.return_value = {
            "settlement_id": "vaels_crossing",
            "local_reputation_cloud": [{"tag": "reliable", "score": 1.0}],
            "npc_social_profile": {"values": {"admires": ["reliable"]}},
            "npc_social_reaction": {
                "admire_score": 1.0,
                "dislike_score": 0.0,
                "fear_score": 0.0,
                "useful_score": 0.0,
                "matched_tags": ["reliable"],
            },
        }
        mock_cq.filter.return_value.values_list.return_value = []
        npc = MagicMock()
        character = MagicMock()

        context = _build_dialogue_context(npc, character)

        self.assertEqual(context["settlement_id"], "vaels_crossing")
        self.assertEqual(context["local_reputation_cloud"][0]["tag"], "reliable")
        self.assertEqual(context["npc_social_reaction"]["admire_score"], 1.0)

    def test_likes_reputation_condition(self):
        from world.dialogue_engine import _check_condition

        context = {"npc_social_reaction": {"admire_score": 1.0}}

        self.assertTrue(_check_condition("likes_reputation", context))

    def test_dislikes_reputation_condition(self):
        from world.dialogue_engine import _check_condition

        context = {"npc_social_reaction": {"dislike_score": 1.0}}

        self.assertTrue(_check_condition("dislikes_reputation", context))

    def test_relationship_trust_conditions(self):
        from world.dialogue_engine import _check_condition

        trusting = {"npc_relationship": {"trust": 70}}
        distrustful = {"npc_relationship": {"trust": 30}}

        self.assertTrue(_check_condition("trusts_relationship", trusting))
        self.assertTrue(_check_condition("distrusts_relationship", distrustful))
```

- [ ] **Step 2: Run dialogue tests and verify failure**

Run:

```bash
python scripts/run_tests.py tests.test_dialogue
```

Expected: FAIL because social context keys and conditions are absent.

- [ ] **Step 3: Extend response priority**

In `world/dialogue_definitions.py`, add social conditions before `"default"`:

```python
    "likes_reputation",
    "dislikes_reputation",
    "fears_reputation",
    "uses_reputation",
    "trusts_relationship",
    "distrusts_relationship",
```

- [ ] **Step 4: Extend dialogue context and conditions**

In `world/dialogue_engine.py`, inside `_build_dialogue_context()` after quest state population, add:

```python
    from world.social_memory import build_social_context
    context.update(build_social_context(character, npc=npc))
```

Then in `_check_condition()`, add:

```python
    reaction = context.get("npc_social_reaction") or {}
    if condition == "likes_reputation":
        return float(reaction.get("admire_score") or 0.0) > 0
    if condition == "dislikes_reputation":
        return float(reaction.get("dislike_score") or 0.0) > 0
    if condition == "fears_reputation":
        return float(reaction.get("fear_score") or 0.0) > 0
    if condition == "uses_reputation":
        return float(reaction.get("useful_score") or 0.0) > 0
    relationship = context.get("npc_relationship") or {}
    if condition == "trusts_relationship":
        return float(relationship.get("trust") or 0.0) >= 65
    if condition == "distrusts_relationship":
        return float(relationship.get("trust") or 0.0) <= 35
```

- [ ] **Step 5: Run dialogue tests**

Run:

```bash
python scripts/run_tests.py tests.test_dialogue
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add world/dialogue_definitions.py world/dialogue_engine.py tests/test_dialogue.py
git commit -m "feat: add social context to dialogue"
```

## Task 6: Add Guarded LLM NPC Voice Module

**Files:**

- Create: `world/llm_npc.py`
- Create: `tests/test_llm_npc.py`

- [ ] **Step 1: Write failing LLM validation tests**

Create `tests/test_llm_npc.py`:

```python
import json
import os
import unittest
from unittest.mock import patch


class TestLlmNpcValidation(unittest.TestCase):
    """LLM NPC responses are optional, JSON-only, and validated."""

    def test_disabled_returns_none_with_reason(self):
        from world.llm_npc import render_npc_speech

        with patch.dict(os.environ, {"SORAVELON_NPC_LLM_ENABLED": "false"}):
            result = render_npc_speech(
                npc_id="npc_greeter_maren",
                topic_key="work",
                deterministic_text="Maren nods.",
                context={"local_reputation_cloud": []},
            )

        self.assertIsNone(result["speech"])
        self.assertEqual(result["fallback_reason"], "disabled")

    def test_valid_fake_provider_speech(self):
        from world.llm_npc import FakeNpcLlmProvider, render_npc_speech

        provider = FakeNpcLlmProvider(
            json.dumps(
                {
                    "speech": "Maren gives you a measuring look.",
                    "tone": "wary",
                    "referenced_fact_keys": [],
                    "used_reputation_tags": ["reliable"],
                    "safety_notes": [],
                }
            )
        )

        with patch.dict(os.environ, {"SORAVELON_NPC_LLM_ENABLED": "true"}):
            result = render_npc_speech(
                npc_id="npc_greeter_maren",
                topic_key="work",
                deterministic_text="Maren nods.",
                context={
                    "local_reputation_cloud": [
                        {"tag": "reliable", "score": 1.0, "fact_keys": []}
                    ],
                },
                provider=provider,
            )

        self.assertEqual(result["speech"], "Maren gives you a measuring look.")
        self.assertIsNone(result["fallback_reason"])

    def test_unknown_tag_falls_back(self):
        from world.llm_npc import FakeNpcLlmProvider, render_npc_speech

        provider = FakeNpcLlmProvider(
            json.dumps(
                {
                    "speech": "You are famous for impossible things.",
                    "tone": "warm",
                    "referenced_fact_keys": [],
                    "used_reputation_tags": ["dragon_truth"],
                    "safety_notes": [],
                }
            )
        )

        with patch.dict(os.environ, {"SORAVELON_NPC_LLM_ENABLED": "true"}):
            result = render_npc_speech(
                npc_id="npc_greeter_maren",
                topic_key="work",
                deterministic_text="Maren nods.",
                context={
                    "local_reputation_cloud": [
                        {"tag": "reliable", "score": 1.0, "fact_keys": []}
                    ],
                },
                provider=provider,
            )

        self.assertIsNone(result["speech"])
        self.assertEqual(result["fallback_reason"], "unknown_tag")

    def test_forbidden_hidden_term_falls_back(self):
        from world.llm_npc import FakeNpcLlmProvider, render_npc_speech

        provider = FakeNpcLlmProvider(
            json.dumps(
                {
                    "speech": "The Vaelborn told me your secret.",
                    "tone": "warm",
                    "referenced_fact_keys": [],
                    "used_reputation_tags": ["reliable"],
                    "safety_notes": [],
                }
            )
        )

        with patch.dict(os.environ, {"SORAVELON_NPC_LLM_ENABLED": "true"}):
            result = render_npc_speech(
                npc_id="npc_greeter_maren",
                topic_key="work",
                deterministic_text="Maren nods.",
                context={
                    "local_reputation_cloud": [
                        {"tag": "reliable", "score": 1.0, "fact_keys": []}
                    ],
                },
                provider=provider,
            )

        self.assertIsNone(result["speech"])
        self.assertEqual(result["fallback_reason"], "forbidden_term")

    def test_rate_limit_falls_back(self):
        from world.llm_npc import (
            FakeNpcLlmProvider,
            _CACHE,
            _RATE_GUARD,
            render_npc_speech,
        )

        _CACHE.clear()
        _RATE_GUARD.clear()
        provider = FakeNpcLlmProvider(
            json.dumps(
                {
                    "speech": "Maren nods once.",
                    "tone": "neutral",
                    "referenced_fact_keys": [],
                    "used_reputation_tags": [],
                    "safety_notes": [],
                }
            )
        )

        env = {
            "SORAVELON_NPC_LLM_ENABLED": "true",
            "SORAVELON_NPC_LLM_CACHE_TTL_SECONDS": "0",
            "SORAVELON_NPC_LLM_MAX_CALLS_PER_MINUTE": "1",
        }
        context = {"character_id": "42", "local_reputation_cloud": []}
        with patch.dict(os.environ, env):
            first = render_npc_speech(
                npc_id="npc_greeter_maren",
                topic_key="work",
                deterministic_text="Maren nods.",
                context=context,
                provider=provider,
            )
            second = render_npc_speech(
                npc_id="npc_greeter_maren",
                topic_key="rumors",
                deterministic_text="Maren nods.",
                context=context,
                provider=provider,
            )

        self.assertEqual(first["speech"], "Maren nods once.")
        self.assertIsNone(second["speech"])
        self.assertEqual(second["fallback_reason"], "rate_limited")
```

- [ ] **Step 2: Run LLM tests and verify import failure**

Run:

```bash
python scripts/run_tests.py tests.test_llm_npc
```

Expected: FAIL because `world.llm_npc` does not exist.

- [ ] **Step 3: Implement guarded module**

Create `world/llm_npc.py`:

```python
"""Optional guarded LLM voice layer for NPC dialogue."""

import json
import os
import time


PROMPT_VERSION = "social-memory-npc-v1"
FORBIDDEN_TERMS = {
    "remnance",
    "vaelborn",
    "echoes",
    "dragon continent",
    "dragon-continent",
}
VALID_TONES = {"neutral", "warm", "wary", "hostile", "amused", "respectful"}
_CACHE = {}
_RATE_GUARD = {}


class FakeNpcLlmProvider:
    """Test provider returning a fixed JSON string."""

    def __init__(self, response_text):
        self.response_text = response_text

    def complete(self, messages, timeout_seconds):
        return self.response_text


class OpenAICompatibleProvider:
    """Minimal OpenAI-compatible chat completions provider."""

    def __init__(self, api_key, base_url, model):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    def complete(self, messages, timeout_seconds):
        import urllib.error
        import urllib.request

        payload = json.dumps(
            {
                "model": self.model,
                "messages": messages,
                "temperature": 0.4,
                "response_format": {"type": "json_object"},
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(str(exc)) from exc
        return body["choices"][0]["message"]["content"]


def _enabled():
    return os.environ.get("SORAVELON_NPC_LLM_ENABLED", "false").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _timeout_seconds():
    raw = os.environ.get("SORAVELON_NPC_LLM_TIMEOUT_SECONDS", "3")
    try:
        return max(1, min(15, int(raw)))
    except ValueError:
        return 3


def _max_output_chars():
    raw = os.environ.get("SORAVELON_NPC_LLM_MAX_OUTPUT_CHARS", "500")
    try:
        return max(80, min(1200, int(raw)))
    except ValueError:
        return 500


def _cache_ttl_seconds():
    raw = os.environ.get("SORAVELON_NPC_LLM_CACHE_TTL_SECONDS", "600")
    try:
        return max(0, min(86400, int(raw)))
    except ValueError:
        return 600


def _max_calls_per_minute():
    raw = os.environ.get("SORAVELON_NPC_LLM_MAX_CALLS_PER_MINUTE", "20")
    try:
        return max(1, min(120, int(raw)))
    except ValueError:
        return 20


def _default_provider():
    api_key = os.environ.get("SORAVELON_NPC_LLM_API_KEY", "")
    base_url = os.environ.get("SORAVELON_NPC_LLM_BASE_URL", "")
    model = os.environ.get("SORAVELON_NPC_LLM_MODEL", "")
    if not api_key or not base_url or not model:
        return None
    return OpenAICompatibleProvider(api_key, base_url, model)


def _known_tags(context):
    return {
        str(entry.get("tag", "")).strip().lower()
        for entry in context.get("local_reputation_cloud", [])
        if entry.get("tag")
    }


def _known_fact_keys(context):
    keys = set()
    for entry in context.get("local_reputation_cloud", []):
        for fact_key in entry.get("fact_keys", []) or []:
            keys.add(str(fact_key))
    return keys


def _cache_key(npc_id, topic_key, context):
    tag_sig = ",".join(
        f"{entry.get('tag')}:{entry.get('score')}"
        for entry in context.get("local_reputation_cloud", [])
    )
    return f"{PROMPT_VERSION}|{npc_id}|{topic_key}|{tag_sig}"


def _rate_guard_allows(context, now):
    character_key = str(
        context.get("character_id") or context.get("character_key") or "unknown"
    )
    window_start = int(now // 60) * 60
    guard_key = (character_key, window_start)
    count = _RATE_GUARD.get(guard_key, 0)
    if count >= _max_calls_per_minute():
        return False
    _RATE_GUARD[guard_key] = count + 1

    stale_windows = [
        key for key in _RATE_GUARD
        if isinstance(key, tuple) and key[1] < window_start - 60
    ]
    for key in stale_windows:
        _RATE_GUARD.pop(key, None)
    return True


def _messages(npc_id, topic_key, deterministic_text, context):
    safe_context = {
        "npc_id": npc_id,
        "topic_key": topic_key,
        "deterministic_text": deterministic_text,
        "settlement_id": context.get("settlement_id"),
        "local_reputation_cloud": context.get("local_reputation_cloud", []),
        "npc_social_reaction": context.get("npc_social_reaction", {}),
        "npc_social_profile": context.get("npc_social_profile", {}),
        "npc_relationship": context.get("npc_relationship", {}),
    }
    return [
        {
            "role": "system",
            "content": (
                "You write one short in-character Soravelon NPC line. "
                "Use only supplied facts. Do not invent lore, quests, rewards, "
                "relationships, hidden truths, or world mutations. Return JSON "
                "with speech, tone, referenced_fact_keys, used_reputation_tags, "
                "and safety_notes."
            ),
        },
        {"role": "user", "content": json.dumps(safe_context, sort_keys=True)},
    ]


def _validate_response(raw_text, context):
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        return None, "invalid_json"

    speech = payload.get("speech")
    if not isinstance(speech, str) or not speech.strip():
        return None, "missing_speech"
    if len(speech) > _max_output_chars():
        return None, "speech_too_long"

    lower_speech = speech.lower()
    for term in FORBIDDEN_TERMS:
        if term in lower_speech:
            return None, "forbidden_term"

    tone = payload.get("tone", "neutral")
    if tone not in VALID_TONES:
        return None, "invalid_tone"

    known_tags = _known_tags(context)
    used_tags = payload.get("used_reputation_tags", []) or []
    for tag in used_tags:
        if str(tag).strip().lower() not in known_tags:
            return None, "unknown_tag"

    known_fact_keys = _known_fact_keys(context)
    referenced = payload.get("referenced_fact_keys", []) or []
    for fact_key in referenced:
        if str(fact_key) not in known_fact_keys:
            return None, "unknown_fact"

    return {
        "speech": speech.strip(),
        "tone": tone,
        "referenced_fact_keys": [str(key) for key in referenced],
        "used_reputation_tags": [str(tag).strip().lower() for tag in used_tags],
        "fallback_reason": None,
    }, None


def render_npc_speech(
    *,
    npc_id,
    topic_key,
    deterministic_text,
    context,
    provider=None,
):
    """Return validated LLM speech or a structured fallback reason."""
    if not _enabled():
        return {"speech": None, "fallback_reason": "disabled"}

    provider = provider or _default_provider()
    if provider is None:
        return {"speech": None, "fallback_reason": "provider_unconfigured"}

    key = _cache_key(npc_id, topic_key, context)
    ttl = _cache_ttl_seconds()
    now = time.time()
    cached = _CACHE.get(key)
    if cached and ttl and now - cached["created_at"] <= ttl:
        return cached["result"]

    if not _rate_guard_allows(context, now):
        return {"speech": None, "fallback_reason": "rate_limited"}

    try:
        raw = provider.complete(
            _messages(npc_id, topic_key, deterministic_text, context),
            _timeout_seconds(),
        )
    except Exception:
        return {"speech": None, "fallback_reason": "provider_error"}

    result, reason = _validate_response(raw, context)
    if reason:
        return {"speech": None, "fallback_reason": reason}

    _CACHE[key] = {"created_at": now, "result": result}
    return result
```

- [ ] **Step 4: Run LLM tests**

Run:

```bash
python scripts/run_tests.py tests.test_llm_npc
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add world/llm_npc.py tests/test_llm_npc.py
git commit -m "feat: add guarded npc llm voice layer"
```

## Task 7: Use Optional LLM Speech In Dialogue Commands

**Files:**

- Modify: `commands/cmd_dialogue.py`
- Modify: `tests/test_dialogue.py`

- [ ] **Step 1: Add failing command helper tests**

Append to `tests/test_dialogue.py`:

```python
class TestDialogueLlmRendering(unittest.TestCase):
    """Dialogue command rendering falls back safely when LLM is unavailable."""

    @patch("world.llm_npc.render_npc_speech")
    def test_render_helper_uses_llm_speech_when_valid(self, mock_render):
        from commands.cmd_dialogue import _render_npc_speech

        mock_render.return_value = {"speech": "Maren speaks freshly.", "fallback_reason": None}
        npc = MagicMock()
        npc.db.npc_id = "npc_greeter_maren"
        npc.key = "Maren"
        character = MagicMock()

        text = _render_npc_speech(
            npc,
            character,
            topic_key="work",
            deterministic_text="Maren nods.",
        )

        self.assertEqual(text, "Maren speaks freshly.")

    @patch("world.llm_npc.render_npc_speech")
    def test_render_helper_falls_back_when_disabled(self, mock_render):
        from commands.cmd_dialogue import _render_npc_speech

        mock_render.return_value = {"speech": None, "fallback_reason": "disabled"}
        npc = MagicMock()
        npc.db.npc_id = "npc_greeter_maren"
        npc.key = "Maren"
        character = MagicMock()

        text = _render_npc_speech(
            npc,
            character,
            topic_key="work",
            deterministic_text="Maren nods.",
        )

        self.assertEqual(text, "Maren nods.")
```

- [ ] **Step 2: Run dialogue tests and verify helper missing**

Run:

```bash
python scripts/run_tests.py tests.test_dialogue
```

Expected: FAIL because `_render_npc_speech` does not exist.

- [ ] **Step 3: Add render helper**

In `commands/cmd_dialogue.py`, add near `_build_quest_oob_payload()`:

```python
def _render_npc_speech(npc, character, *, topic_key, deterministic_text):
    """Optionally render NPC speech through the guarded LLM voice layer."""
    from world.dialogue_engine import _build_dialogue_context
    from world.llm_npc import render_npc_speech

    npc_id = getattr(getattr(npc, "db", None), "npc_id", None) or getattr(npc, "key", "")
    try:
        context = _build_dialogue_context(npc, character)
        rendered = render_npc_speech(
            npc_id=npc_id,
            topic_key=topic_key,
            deterministic_text=deterministic_text,
            context=context,
        )
    except Exception:
        return deterministic_text
    return rendered.get("speech") or deterministic_text
```

- [ ] **Step 4: Use helper in `CmdTalk`, `CmdAsk`, and NPC `CmdTell`**

Replace direct output of deterministic NPC speech with `_render_npc_speech(...)`.

For `CmdTalk` greeting:

```python
        rendered_greeting = _render_npc_speech(
            npc,
            character,
            topic_key="greeting",
            deterministic_text=greeting_text,
        )
        character.msg(f"|w{npc_display}|n says, \"{rendered_greeting}\"")
```

For `CmdAsk` topic response:

```python
                rendered_text = _render_npc_speech(
                    npc,
                    character,
                    topic_key=topic_key,
                    deterministic_text=text,
                )
                character.msg(f"|w{npc_display}|n says, \"{rendered_text}\"")
```

For NPC `CmdTell` topic response:

```python
                    rendered_text = _render_npc_speech(
                        npc,
                        character,
                        topic_key=topic_key,
                        deterministic_text=response_text,
                    )
                    character.msg(f"|w{npc_display}|n says, \"{rendered_text}\"")
```

- [ ] **Step 5: Run dialogue and LLM tests**

Run:

```bash
python scripts/run_tests.py tests.test_dialogue tests.test_llm_npc
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add commands/cmd_dialogue.py tests/test_dialogue.py
git commit -m "feat: allow guarded llm npc speech"
```

## Task 8: Add Social Memory Inspection Command

**Files:**

- Create: `commands/cmd_social_memory.py`
- Modify: `commands/default_cmdsets.py`
- Modify: `world/help_entries.py`
- Create or modify: `tests/test_cmd_social_memory.py`

- [ ] **Step 1: Write failing command tests**

Create `tests/test_cmd_social_memory.py`:

```python
from evennia.utils.test_resources import EvenniaCommandTestMixin, EvenniaTest


class TestCmdSocialMemory(EvenniaCommandTestMixin, EvenniaTest):
    """Development command displays local reputation cloud."""

    def test_socialmemory_here_shows_local_tags(self):
        from commands.cmd_social_memory import CmdSocialMemory
        from world.social_memory import record_social_fact

        self.char1.location.db.zone_id = "vaels_crossing"
        record_social_fact(
            self.char1,
            fact_key="vc_cmd_reliable",
            fact_type="test",
            settlement_id="vaels_crossing",
            tags=["reliable"],
            summary="Maren saw reliability.",
        )

        self.call(
            CmdSocialMemory(),
            "here",
            "Local reputation in vaels_crossing",
        )
        self.assertIn("reliable", self.char1.msg.call_args[0][0].lower())

    def test_socialmemory_named_settlement(self):
        from commands.cmd_social_memory import CmdSocialMemory
        from world.social_memory import record_social_fact

        record_social_fact(
            self.char1,
            fact_key="kor_cmd_generous",
            fact_type="test",
            settlement_id="korahei",
            tags=["generous"],
            summary="Korahei saw generosity.",
        )

        self.call(
            CmdSocialMemory(),
            "korahei",
            "Local reputation in korahei",
        )
        self.assertIn("generous", self.char1.msg.call_args[0][0].lower())
```

- [ ] **Step 2: Run command tests and verify import failure**

Run:

```bash
python scripts/run_tests.py tests.test_cmd_social_memory
```

Expected: FAIL because `commands.cmd_social_memory` does not exist.

- [ ] **Step 3: Implement command**

Create `commands/cmd_social_memory.py`:

```python
"""Development command for inspecting local social memory."""

from evennia import Command


class CmdSocialMemory(Command):
    """Inspect your local reputation cloud."""

    key = "socialmemory"
    aliases = ["reputationcloud"]
    locks = "cmd:perm(Builder)"
    help_category = "Development"

    def func(self):
        from world.social_memory import get_local_reputation_cloud
        from world.models import SocialMemoryFact

        character = self.caller
        arg = self.args.strip()
        if arg == "here" or not arg:
            room = character.location
            settlement_id = ""
            if room and hasattr(room, "db"):
                settlement_id = room.db.settlement_id or room.db.zone_id or ""
            if not settlement_id:
                character.msg("|yNo local settlement or zone is known here.|n")
                return
        else:
            settlement_id = arg

        cloud = get_local_reputation_cloud(character, settlement_id)
        lines = [f"|wLocal reputation in {settlement_id}|n"]
        if not cloud:
            lines.append("|xNo local reputation tags are known yet.|n")
        else:
            for entry in cloud:
                lines.append(
                    f"|c{entry['tag']}|n "
                    f"|x(score {entry['score']}, facts {entry['evidence_count']})|n"
                )

        facts = SocialMemoryFact.objects.filter(
            character=character,
            settlement_id=settlement_id,
        ).order_by("-created_at")[:3]
        if facts:
            lines.append("|wRecent facts|n")
            for fact in facts:
                lines.append(f"|x- {fact.summary}|n")

        character.msg("\n".join(lines))
```

- [ ] **Step 4: Register command for builders/admins only**

In `commands/default_cmdsets.py`, after social commands registration, add:

```python
        from commands.cmd_social_memory import CmdSocialMemory
        self.add(CmdSocialMemory())
```

- [ ] **Step 5: Add builder/admin-only help entry**

In `world/help_entries.py`, add a direct `socialmemory` entry only if the help
system can keep it out of ordinary player help. Use this content:

```text
Usage:
  socialmemory
  socialmemory here
  socialmemory <settlement>

Shows the local reputation tags currently known for your character in a zone or settlement.
This is a development-facing proof command for the social memory system.
```

- [ ] **Step 6: Run command and help tests**

Run:

```bash
python scripts/run_tests.py tests.test_cmd_social_memory tests.test_help_entries
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add commands/cmd_social_memory.py commands/default_cmdsets.py world/help_entries.py tests/test_cmd_social_memory.py
git commit -m "feat: add social memory inspection command"
```

## Task 9: Author Vael's Crossing Social Profiles And Fact Hooks

**Files:**

- Modify: `world/areas/vaels_crossing.py`
- Create: `tests/test_vaels_crossing_social_contracts.py`

- [ ] **Step 1: Add failing contract tests**

Create `tests/test_vaels_crossing_social_contracts.py`:

```python
import ast
from pathlib import Path
import unittest


VAEL_PATH = Path("world/areas/vaels_crossing.py")
ANCHOR_NPCS = {
    "npc_greeter_maren",
    "npc_barkeep_marta_voss",
    "npc_broker_carston",
    "npc_warden_agent_calloway",
    "npc_innkeeper_whistle",
}


class TestVaelsCrossingSocialContracts(unittest.TestCase):
    """Vael's Crossing anchor NPCs must carry social interaction data."""

    @classmethod
    def setUpClass(cls):
        cls.tree = ast.parse(VAEL_PATH.read_text())

    def _npc_calls(self):
        for node in ast.walk(self.tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "npc"
            ):
                yield node

    def _quest_calls(self):
        for node in ast.walk(self.tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "quest"
            ):
                yield node

    def _literal_arg(self, node, index):
        if len(node.args) <= index:
            return None
        arg = node.args[index]
        return arg.value if isinstance(arg, ast.Constant) else None

    def _keywords(self, node):
        return {kw.arg: kw.value for kw in node.keywords if kw.arg}

    def test_anchor_npcs_have_dialogue_and_social_profile(self):
        found = {}
        for call in self._npc_calls():
            npc_id = self._literal_arg(call, 1)
            if npc_id in ANCHOR_NPCS:
                found[npc_id] = self._keywords(call)

        self.assertEqual(set(found), ANCHOR_NPCS)
        for npc_id, keywords in found.items():
            self.assertIn("dialogue", keywords, npc_id)
            self.assertIn("social_profile", keywords, npc_id)

    def test_anchor_profiles_define_values(self):
        for call in self._npc_calls():
            npc_id = self._literal_arg(call, 1)
            if npc_id not in ANCHOR_NPCS:
                continue
            profile = self._keywords(call)["social_profile"]
            self.assertIsInstance(profile, ast.Dict)
            keys = {
                key.value
                for key in profile.keys
                if isinstance(key, ast.Constant)
            }
            self.assertIn("settlement_id", keys)
            self.assertIn("values", keys)
            self.assertIn("voice", keys)
            self.assertIn("public_role", keys)

    def test_vael_quests_record_social_facts(self):
        has_social_fact = False
        has_relationship = False
        for call in self._quest_calls():
            rewards = self._keywords(call).get("rewards")
            if not isinstance(rewards, ast.List):
                continue
            for reward in rewards.elts:
                if not isinstance(reward, ast.Dict):
                    continue
                data = {}
                for key, value in zip(reward.keys, reward.values):
                    if isinstance(key, ast.Constant) and isinstance(value, ast.Constant):
                        data[key.value] = value.value
                if data.get("action_type") == "record_social_fact":
                    has_social_fact = True
                if data.get("action_type") == "adjust_npc_relationship":
                    has_relationship = True
        self.assertTrue(has_social_fact)
        self.assertTrue(has_relationship)
```

- [ ] **Step 2: Run contract tests and verify failure**

Run:

```bash
python scripts/run_tests.py tests.test_vaels_crossing_social_contracts
```

Expected: FAIL because anchor NPCs lack `social_profile` and quests lack `record_social_fact` rewards.

- [ ] **Step 3: Add social profiles to anchor NPCs**

Modify the `area.npc(...)` calls for these NPCs in `world/areas/vaels_crossing.py`.

Use these profile payloads:

```python
social_profile={
    "settlement_id": "vaels_crossing",
    "values": {
        "admires": ["reliable", "generous"],
        "dislikes": ["reckless"],
        "fears": [],
        "finds_useful": [],
    },
    "voice": "warm but practical, civic, observant",
    "public_role": "gate greeter",
    "rumor_role": "hears first impressions from travelers",
}
```

for `npc_greeter_maren`.

```python
social_profile={
    "settlement_id": "vaels_crossing",
    "values": {
        "admires": ["generous", "reliable"],
        "dislikes": ["reckless"],
        "fears": [],
        "finds_useful": ["shrewd"],
    },
    "voice": "dry, hospitable, quick to notice who pays and who listens",
    "public_role": "barkeep",
    "rumor_role": "collects road stories and work gossip",
}
```

for `npc_barkeep_marta_voss`.

```python
social_profile={
    "settlement_id": "vaels_crossing",
    "values": {
        "admires": ["shrewd", "profit_minded"],
        "dislikes": ["reckless"],
        "fears": [],
        "finds_useful": ["reliable", "warden_aligned"],
    },
    "voice": "polished, transactional, attentive to leverage",
    "public_role": "broker",
    "rumor_role": "tracks who can make a route profitable",
}
```

for `npc_broker_carston`.

```python
social_profile={
    "settlement_id": "vaels_crossing",
    "values": {
        "admires": ["reliable", "warden_aligned"],
        "dislikes": ["reckless", "profit_minded"],
        "fears": [],
        "finds_useful": ["shrewd"],
    },
    "voice": "measured, disciplined, road-security focused",
    "public_role": "warden contact",
    "rumor_role": "listens for risks before they become incidents",
}
```

for `npc_warden_agent_calloway`.

```python
social_profile={
    "settlement_id": "vaels_crossing",
    "values": {
        "admires": ["reliable", "generous"],
        "dislikes": ["reckless"],
        "fears": [],
        "finds_useful": ["shrewd"],
    },
    "voice": "plainspoken, hospitable, close to road gossip",
    "public_role": "innkeeper",
    "rumor_role": "hears what travelers repeat when they think no one is weighing it",
}
```

for `npc_innkeeper_whistle`.

- [ ] **Step 4: Add deterministic social response lanes**

For each anchor NPC's authored `dialogue["topics"]`, add at least one topic
with `likes_reputation` and `dislikes_reputation` variants.
Calloway must also have at least one `trusts_relationship` variant so the
`NpcRelationship` model has a visible MVP use.

Example for a `work` topic:

```python
"work": {
    "likes_reputation": "You've made yourself useful here. That changes which doors open first.",
    "dislikes_reputation": "People are talking, and not all of it makes my work easier.",
    "trusts_relationship": "You have handled Warden business cleanly enough that I can be plainer with you.",
    "default": "There is always work where roads meet money and trouble.",
}
```

Keep the text specific to each NPC's role.

- [ ] **Step 5: Add social fact reward actions to at least two Vael quests**

Add `record_social_fact` rewards to these exact quests:

- `vc_q_warden_report`
- `vc_q_missing_shipment`

Warden reward for `vc_q_warden_report`:

```python
{
    "action_type": "record_social_fact",
    "fact_key": "vc_warden_report_reliable",
    "fact_type": "quest_consequence",
    "settlement_id": "vaels_crossing",
    "faction_id": "wardens",
    "source_type": "quest",
    "source_id": "vc_q_warden_report",
    "tags": ["reliable", "warden_aligned"],
    "summary": "Vael's Crossing hears that you carried Warden business without losing the thread.",
    "visibility": "settlement",
    "weight": 1.0,
}
```

Also add a relationship reward for Calloway on `vc_q_warden_report`:

```python
{
    "action_type": "adjust_npc_relationship",
    "npc_id": "npc_warden_agent_calloway",
    "trust_delta": 20,
    "respect_delta": 10,
    "known_tags": ["reliable", "warden_aligned"],
}
```

Consortium reward for `vc_q_missing_shipment`:

```python
{
    "action_type": "record_social_fact",
    "fact_key": "vc_broker_route_shrewd",
    "fact_type": "quest_consequence",
    "settlement_id": "vaels_crossing",
    "faction_id": "consortium",
    "source_type": "quest",
    "source_id": "vc_q_missing_shipment",
    "tags": ["shrewd", "profit_minded"],
    "summary": "Brokers in Vael's Crossing hear that you can make a route pay attention.",
    "visibility": "settlement",
    "weight": 1.0,
}
```

- [ ] **Step 6: Run contract tests**

Run:

```bash
python scripts/run_tests.py tests.test_vaels_crossing_social_contracts
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add world/areas/vaels_crossing.py tests/test_vaels_crossing_social_contracts.py
git commit -m "feat: add vaels crossing social npc slice"
```

## Task 10: Full Validation And Smoke

**Files:**

- No source edits unless validation exposes a defect in this plan's scope.

- [ ] **Step 1: Run focused test suite**

Run:

```bash
python scripts/run_tests.py tests.test_social_memory tests.test_llm_npc tests.test_dialogue tests.test_action_vocabulary tests.test_cmd_social_memory tests.test_vaels_crossing_social_contracts
```

Expected: PASS.

- [ ] **Step 2: Run broader launch-sensitive tests**

Run:

```bash
python scripts/run_tests.py tests.test_world_state tests.test_quest_engine tests.test_help_entries tests.test_content_integration
```

Expected: PASS.

- [ ] **Step 3: Capture diegetic social-recognition transcript**

Run a local character through the Vael's Crossing social-memory loop:

1. Complete `vc_q_warden_report`.
2. Complete `vc_q_missing_shipment`.
3. Talk/ask about work, rumors, or local trouble with:
   `npc_greeter_maren`, `npc_warden_agent_calloway`, `npc_broker_carston`,
   `npc_barkeep_marta_voss`, and `npc_innkeeper_whistle`.

Expected: transcript shows one immediate quest-completion echo, one later recall
from a different NPC, and one contrast where two NPCs interpret the same
reputation cloud differently. The transcript must not display numeric scores to
the player.

- [ ] **Step 4: Run startup smoke if migrations and settings are available**

Run:

```bash
python scripts/smoke_start.py
```

Expected: server startup smoke completes without import or migration errors.

- [ ] **Step 5: Inspect migration state**

Run:

```bash
python -m django showmigrations world --settings server.conf.settings
```

Expected: social memory migration appears in the `world` migration list.

- [ ] **Step 6: Commit validation-only fixes if needed**

If validation exposed a defect caused by this plan, commit the minimal fix:

```bash
git add <changed-files>
git commit -m "fix: stabilize social memory integration"
```

Do not include unrelated dirty files in this commit.

## Task 11: Engram Closeout

**Files:**

- No repo files.

- [ ] **Step 1: Write Engram memory**

Use `mcp__engram.write_memory` with:

```json
{
  "key": "soravelon_llm_social_memory_npc_integration_2026_06_12",
  "title": "Soravelon LLM Social Memory NPC Integration Plan",
  "project": "soravelon",
  "domain": "game-design",
  "memory_type": "handoff",
  "scope": "project",
  "tags": ["soravelon", "npc-dialogue", "social-memory", "llm", "vaels-crossing"],
  "content": "Created spec and implementation plan for a Vael's Crossing runtime MVP where deterministic social memory owns reputation truth and an optional provider-neutral LLM voice layer phrases safe NPC responses. Spec path: docs/superpowers/specs/2026-06-12-llm-social-memory-npc-integration-design.md. Plan path: docs/superpowers/plans/2026-06-12-llm-social-memory-npc-integration-implementation-plan.md. Core guardrail: game systems decide social facts, witnesses, local reputation cloud, NPC worldview reactions, access, trust, and quest effects; LLM can only render bounded speech from approved context and must fail closed to authored dialogue."
}
```

- [ ] **Step 2: Record final repo state**

Run:

```bash
git status --short
```

Expected: only unrelated pre-existing dirty files remain after plan/spec commit
and task implementation commits.

## Plan Self-Review

Spec coverage:

- deterministic social facts: Task 1, Task 2, Task 3
- local reputation cloud: Task 2
- NPC worldview profiles: Task 4, Task 9
- dialogue integration: Task 5, Task 7
- optional LLM guardrails: Task 6, Task 7
- Vael's Crossing vertical slice: Task 9
- debug surface: Task 8
- validation: Task 10
- Engram closeout: Task 11

Placeholder scan:

- No deferred implementation sections are intentionally left in this plan.
- Task 9 names the exact Vael's Crossing quest ids for social fact rewards.

Type consistency:

- `SocialMemoryFact`, `NpcRelationship`, `record_social_fact`,
  `get_local_reputation_cloud`, `score_npc_reaction`, `build_social_context`,
  and `render_npc_speech` are introduced before later tasks call them.

## Execution Choice

Plan complete and saved to
`docs/superpowers/plans/2026-06-12-llm-social-memory-npc-integration-implementation-plan.md`.

Execution options:

1. **Subagent-Driven (recommended)** - dispatch a fresh subagent per task,
   review between tasks, fast iteration.
2. **Inline Execution** - execute tasks in this session using
   `superpowers:executing-plans`, batch execution with checkpoints.
