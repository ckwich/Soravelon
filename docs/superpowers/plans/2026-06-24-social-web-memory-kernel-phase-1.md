# Social Web Memory Kernel Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the deterministic Soravelon-native Engram kernel that can record social facts, claims, knowledge, contact edges, context packets, and traceable cross-zone propagation.

**Architecture:** Start with Django relational models and graph-shaped service APIs under `world/`. Do not start with LLM calls, broad NPC dialogue rewrites, schedules, or social verbs. Phase 1 proves the substrate: "this NPC knows this claim because this contact edge carried it."

**Tech Stack:** Evennia 6.0, Django ORM, Python 3.11, existing `world` app migrations, `unittest`/Evennia test suite.

---

## Scope Check

This plan implements the first build layer of:

- Spec: `docs/superpowers/specs/2026-06-20-social-web-memory-engine-design.md`
- Engram memory: `soravelon_social_web_memory_engine_north_star_2026_06_20`

The spec is larger than one implementation pass. This plan covers only Phase 1:

- social graph primitives
- facts, claims, knowledge, and traces
- deterministic propagation across contact edges
- bounded context-pack query
- Vael Warden-report proof fixture
- builder/admin inspection scaffolding

Out of scope for Phase 1:

- LLM NPC speech generation
- non-quest social verbs such as `gift`, `boast`, `vouch`, `confess`
- town mood, settlement traits, myth compaction, property, jobs, romance
- broad Vael's Crossing dialogue/content rewrites
- external graph/vector storage
- use of the user's personal Engram Hub for live player state

## Start Here

Start with **Task 1**. Do not start by editing `world/areas/vaels_crossing.py` or `world/dialogue_engine.py`. Those surfaces cannot be correct until the kernel can prove:

- which social node knows a fact or claim
- which edge carried it
- whether the edge was allowed to carry it
- what trace explains a future NPC reaction

## File Map

Create:

- `tests/test_social_web_kernel.py`: model and service tests for the kernel.
- `tests/test_social_web_warden_route.py`: content-independent Vael Warden-route proof.
- `tests/test_socialmemory_command.py`: admin inspection command tests.
- `world/social_taxonomy.py`: accepted node, edge, visibility, knowledge, and claim constants.
- `world/social_engine.py`: high-level API for nodes, edges, facts, claims, knowledge, propagation, context packs, and traces.
- `commands/cmd_socialmemory.py`: builder/admin-only inspection command.
- `world/migrations/0009_social_web_kernel.py`: generated migration for the new models.

Modify:

- `world/models.py`: add `SocialNode`, `SocialEdge`, `SocialFact`, `SocialClaim`, `SocialKnowledge`, `SocialTrace`.
- `world/area_builder.py`: persist authored `social_profile` and `social_edges` db attributes on NPCs.
- `world/zone_serializer.py`: allow JSON NPC definitions to pass `social_profile` and `social_edges` through unchanged via existing kwargs mapping.
- `commands/default_cmdsets.py`: register `CmdSocialMemory`.
- `tests/test_area_builder.py`: verify `AreaBuilder.npc()` persists `social_profile` and `social_edges` attrs.

Do not modify in Phase 1:

- `world/dialogue_engine.py`
- `world/dialogue_definitions.py`
- `commands/cmd_dialogue.py`
- `world/areas/vaels_crossing.py`
- `world/areas/equipment_catalog.py`

## Task 1: Persist Social Web Kernel Models

**Files:**

- Modify: `world/models.py`
- Create: `tests/test_social_web_kernel.py`
- Generate: `world/migrations/0009_social_web_kernel.py`

- [ ] **Step 1: Write failing model tests**

Create `tests/test_social_web_kernel.py`:

```python
from evennia.utils.test_resources import EvenniaTest


class TestSocialWebModels(EvenniaTest):
    """The social web kernel persists graph nodes, edges, truth, claims, and traces."""

    def test_social_node_key_is_unique(self):
        from django.db import IntegrityError
        from world.models import SocialNode

        SocialNode.objects.create(
            node_key="npc:npc_warden_agent_calloway",
            node_type="npc",
            display_name="Agent Calloway",
            zone_id="vaels_crossing",
            settlement_id="vaels_crossing",
        )

        with self.assertRaises(IntegrityError):
            SocialNode.objects.create(
                node_key="npc:npc_warden_agent_calloway",
                node_type="npc",
                display_name="Duplicate Calloway",
            )

    def test_social_edge_connects_two_nodes(self):
        from world.models import SocialEdge, SocialNode

        calloway = SocialNode.objects.create(
            node_key="npc:npc_warden_agent_calloway",
            node_type="npc",
            display_name="Agent Calloway",
        )
        commander = SocialNode.objects.create(
            node_key="npc:npc_warden_outpost_commander",
            node_type="npc",
            display_name="Outpost Commander",
        )

        edge = SocialEdge.objects.create(
            edge_key="edge:calloway:commander:official_report",
            source_node=calloway,
            target_node=commander,
            edge_type="official_report",
            directionality="one_way",
            trust=0.9,
            latency_seconds=3600,
            scope_tags=["warden", "report", "quest"],
        )

        self.assertEqual(edge.source_node.node_key, "npc:npc_warden_agent_calloway")
        self.assertEqual(edge.target_node.node_key, "npc:npc_warden_outpost_commander")
        self.assertEqual(edge.scope_tags, ["warden", "report", "quest"])

    def test_social_fact_claim_knowledge_and_trace_link_together(self):
        from world.models import (
            SocialClaim,
            SocialEdge,
            SocialFact,
            SocialKnowledge,
            SocialNode,
            SocialTrace,
        )

        player = SocialNode.objects.create(
            node_key=f"player:{self.char1.id}",
            node_type="player",
            display_name=self.char1.key,
        )
        calloway = SocialNode.objects.create(
            node_key="npc:npc_warden_agent_calloway",
            node_type="npc",
            display_name="Agent Calloway",
        )
        commander = SocialNode.objects.create(
            node_key="npc:npc_warden_outpost_commander",
            node_type="npc",
            display_name="Outpost Commander",
        )
        edge = SocialEdge.objects.create(
            edge_key="edge:calloway:commander:official_report",
            source_node=calloway,
            target_node=commander,
            edge_type="official_report",
            directionality="one_way",
            scope_tags=["warden", "report"],
        )
        fact = SocialFact.objects.create(
            fact_key="fact:warden_report_delivered",
            subject_node=player,
            scope_node=calloway,
            event_type="quest_completed",
            summary="The player delivered Calloway's sealed field report.",
            tags=["reliable", "warden_aligned", "report"],
            visibility="institutional",
        )
        claim = SocialClaim.objects.create(
            claim_key="claim:calloway:warden_report_delivered",
            fact=fact,
            speaker_node=calloway,
            subject_node=player,
            claim_type="report",
            summary="Calloway reports that the player carried Warden business cleanly.",
            status="supported",
        )
        knowledge = SocialKnowledge.objects.create(
            knowledge_key="knowledge:commander:claim:calloway:warden_report_delivered",
            node=commander,
            fact=fact,
            claim=claim,
            source_node=calloway,
            edge=edge,
            channel="official_report",
            confidence=0.9,
            spreading=True,
        )
        trace = SocialTrace.objects.create(
            trace_key="trace:commander:claim:calloway:warden_report_delivered",
            knowledge=knowledge,
            from_node=calloway,
            to_node=commander,
            edge=edge,
            summary="Official Warden report carried the claim from Calloway to the commander.",
        )

        self.assertEqual(knowledge.fact.fact_key, "fact:warden_report_delivered")
        self.assertEqual(knowledge.claim.claim_key, "claim:calloway:warden_report_delivered")
        self.assertEqual(trace.edge.edge_type, "official_report")
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```bash
python scripts/run_tests.py tests.test_social_web_kernel
```

Expected: FAIL because `SocialNode`, `SocialEdge`, `SocialFact`, `SocialClaim`, `SocialKnowledge`, and `SocialTrace` do not exist.

- [ ] **Step 3: Add model classes**

Append these classes after `WorldEventLog` in `world/models.py`:

```python
class SocialNode(models.Model):
    """A node in Soravelon's runtime social knowledge graph."""

    node_key = models.CharField(max_length=192, unique=True)
    node_type = models.CharField(max_length=32, db_index=True)
    display_name = models.CharField(max_length=160, blank=True, default="")
    zone_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    settlement_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    faction_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["node_type", "zone_id"]),
            models.Index(fields=["node_type", "settlement_id"]),
            models.Index(fields=["faction_id"]),
        ]

    def __str__(self):
        return self.node_key


class SocialEdge(models.Model):
    """A contact path that can carry social facts or claims between nodes."""

    DIRECTION_CHOICES = [
        ("one_way", "One Way"),
        ("two_way", "Two Way"),
        ("broadcast", "Broadcast"),
        ("gatekept", "Gatekept"),
    ]

    edge_key = models.CharField(max_length=240, unique=True)
    source_node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="outgoing_social_edges",
    )
    target_node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="incoming_social_edges",
    )
    edge_type = models.CharField(max_length=64, db_index=True)
    directionality = models.CharField(
        max_length=16,
        choices=DIRECTION_CHOICES,
        default="one_way",
    )
    trust = models.FloatField(default=0.5)
    latency_seconds = models.PositiveIntegerField(default=0)
    bandwidth = models.PositiveIntegerField(default=3)
    secrecy = models.CharField(max_length=32, blank=True, default="")
    distortion = models.CharField(max_length=32, blank=True, default="")
    scope_tags = models.JSONField(default=list)
    blockers = models.JSONField(default=list)
    active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["source_node", "active"]),
            models.Index(fields=["target_node", "active"]),
            models.Index(fields=["edge_type", "active"]),
        ]

    def __str__(self):
        return self.edge_key


class SocialFact(models.Model):
    """Authoritative social truth recorded by game systems."""

    VISIBILITY_CHOICES = [
        ("private", "Private"),
        ("witnessed", "Witnessed"),
        ("local", "Local"),
        ("institutional", "Institutional"),
        ("route", "Route"),
        ("global", "Global"),
    ]

    fact_key = models.CharField(max_length=192, unique=True)
    subject_node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="subject_social_facts",
    )
    actor_node = models.ForeignKey(
        SocialNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="actor_social_facts",
    )
    scope_node = models.ForeignKey(
        SocialNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="scoped_social_facts",
    )
    event_type = models.CharField(max_length=64, db_index=True)
    summary = models.TextField()
    tags = models.JSONField(default=list)
    visibility = models.CharField(
        max_length=16,
        choices=VISIBILITY_CHOICES,
        default="local",
        db_index=True,
    )
    evidence = models.JSONField(default=dict)
    weight = models.FloatField(default=1.0)
    confidence = models.FloatField(default=1.0)
    occurred_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["subject_node", "visibility"]),
            models.Index(fields=["event_type", "created_at"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.fact_key


class SocialClaim(models.Model):
    """A social assertion made by a node about a fact or subject."""

    STATUS_CHOICES = [
        ("supported", "Supported"),
        ("rumor", "Rumor"),
        ("contested", "Contested"),
        ("false", "False"),
        ("unknown", "Unknown"),
    ]

    claim_key = models.CharField(max_length=224, unique=True)
    fact = models.ForeignKey(
        SocialFact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="claims",
    )
    speaker_node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="spoken_social_claims",
    )
    subject_node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="subject_social_claims",
    )
    claim_type = models.CharField(max_length=64, db_index=True)
    summary = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="rumor")
    intent = models.CharField(max_length=64, blank=True, default="")
    bias_tags = models.JSONField(default=list)
    confidence = models.FloatField(default=0.5)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["speaker_node", "claim_type"]),
            models.Index(fields=["subject_node", "status"]),
        ]

    def __str__(self):
        return self.claim_key


class SocialKnowledge(models.Model):
    """A record that a node knows or believes a fact or claim."""

    knowledge_key = models.CharField(max_length=260, unique=True)
    node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="social_knowledge",
    )
    fact = models.ForeignKey(
        SocialFact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="known_by",
    )
    claim = models.ForeignKey(
        SocialClaim,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="known_by",
    )
    source_node = models.ForeignKey(
        SocialNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sourced_social_knowledge",
    )
    edge = models.ForeignKey(
        SocialEdge,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="carried_social_knowledge",
    )
    channel = models.CharField(max_length=64, db_index=True)
    confidence = models.FloatField(default=0.5)
    spreading = models.BooleanField(default=False, db_index=True)
    learned_at = models.DateTimeField(auto_now_add=True, db_index=True)
    available_after = models.DateTimeField(null=True, blank=True, db_index=True)
    evidence = models.JSONField(default=dict)

    class Meta:
        indexes = [
            models.Index(fields=["node", "channel"]),
            models.Index(fields=["node", "spreading"]),
            models.Index(fields=["available_after"]),
        ]

    def __str__(self):
        return self.knowledge_key


class SocialTrace(models.Model):
    """Audit trail explaining how social knowledge reached a node."""

    trace_key = models.CharField(max_length=280, unique=True)
    knowledge = models.ForeignKey(
        SocialKnowledge,
        on_delete=models.CASCADE,
        related_name="traces",
    )
    from_node = models.ForeignKey(
        SocialNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="outgoing_social_traces",
    )
    to_node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="incoming_social_traces",
    )
    edge = models.ForeignKey(
        SocialEdge,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="social_traces",
    )
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["to_node", "created_at"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.trace_key
```

- [ ] **Step 4: Generate migration**

Run:

```bash
python -m django makemigrations world --settings server.conf.settings
```

Expected: creates `world/migrations/0009_social_web_kernel.py`. If Django names the file differently, rename it to `0009_social_web_kernel.py` and keep the dependency on `("world", "0008_rename_mob_template_key")`.

- [ ] **Step 5: Run model tests**

Run:

```bash
python scripts/run_tests.py tests.test_social_web_kernel
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add world/models.py world/migrations/0009_social_web_kernel.py tests/test_social_web_kernel.py
git commit -m "feat: add social web kernel models"
```

## Task 2: Add Social Taxonomy And Engine API

**Files:**

- Create: `world/social_taxonomy.py`
- Create: `world/social_engine.py`
- Modify: `tests/test_social_web_kernel.py`

- [ ] **Step 1: Add failing engine tests**

Append to `tests/test_social_web_kernel.py`:

```python
class TestSocialWebEngine(EvenniaTest):
    """Service APIs provide graph-shaped access over relational models."""

    def test_ensure_social_node_is_idempotent(self):
        from world.models import SocialNode
        from world.social_engine import ensure_social_node

        first = ensure_social_node(
            "npc",
            "npc_warden_agent_calloway",
            display_name="Agent Calloway",
            zone_id="vaels_crossing",
            settlement_id="vaels_crossing",
        )
        second = ensure_social_node(
            "npc",
            "npc_warden_agent_calloway",
            display_name="Agent Calloway",
            zone_id="vaels_crossing",
        )

        self.assertEqual(first.id, second.id)
        self.assertEqual(SocialNode.objects.count(), 1)
        self.assertEqual(first.node_key, "npc:npc_warden_agent_calloway")

    def test_connect_social_nodes_rejects_unknown_edge_type(self):
        from world.social_engine import connect_social_nodes, ensure_social_node

        ensure_social_node("npc", "a")
        ensure_social_node("npc", "b")

        ok, message, edge = connect_social_nodes(
            "npc:a",
            "npc:b",
            edge_type="made_up_channel",
        )

        self.assertFalse(ok)
        self.assertIn("unsupported edge_type", message)
        self.assertIsNone(edge)

    def test_record_fact_and_claim_create_initial_knowledge(self):
        from world.social_engine import (
            assert_social_claim,
            ensure_social_node,
            mark_known,
            record_social_fact,
        )

        player = ensure_social_node("player", str(self.char1.id), display_name=self.char1.key)
        calloway = ensure_social_node("npc", "npc_warden_agent_calloway")

        ok, message, fact = record_social_fact(
            fact_key="fact:test_warden_report_delivered",
            subject_node_key=player.node_key,
            scope_node_key=calloway.node_key,
            event_type="quest_completed",
            summary="The player delivered the field report.",
            tags=[" reliable ", "Reliable", "warden"],
            visibility="institutional",
            evidence={"quest_id": "vc_q_warden_report"},
        )
        self.assertTrue(ok, message)
        self.assertEqual(fact.tags, ["reliable", "warden"])

        ok, message, claim = assert_social_claim(
            claim_key="claim:calloway:test_warden_report_delivered",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="report",
            summary="Calloway says the player carried Warden business cleanly.",
            status="supported",
        )
        self.assertTrue(ok, message)

        ok, message, knowledge = mark_known(
            node_key=calloway.node_key,
            fact_key=fact.fact_key,
            claim_key=claim.claim_key,
            channel="direct_witness",
            confidence=1.0,
            spreading=True,
        )
        self.assertTrue(ok, message)
        self.assertEqual(knowledge.node.node_key, calloway.node_key)
```

- [ ] **Step 2: Run tests and verify import failure**

Run:

```bash
python scripts/run_tests.py tests.test_social_web_kernel
```

Expected: FAIL because `world.social_engine` and `world.social_taxonomy` do not exist.

- [ ] **Step 3: Create taxonomy constants**

Create `world/social_taxonomy.py`:

```python
"""Approved vocabulary for Soravelon's Social Web kernel."""

NODE_TYPES = {
    "player",
    "npc",
    "household",
    "shop",
    "guild",
    "faction",
    "institution",
    "route",
    "settlement",
    "zone",
    "caravan",
    "crew",
    "archive",
    "gathering",
}

EDGE_TYPES = {
    "direct_witness",
    "official_report",
    "warden_report",
    "market_route",
    "guild_courier",
    "family_letter",
    "criminal_whisper",
    "inn_traveler",
    "pilgrimage",
    "archive_copy",
    "node_response",
}

CLAIM_TYPES = {
    "report",
    "rumor",
    "testimony",
    "warning",
    "boast",
    "denial",
    "confession",
}

KNOWLEDGE_CHANNELS = {
    "direct_witness",
    "official_report",
    "tavern_rumor",
    "market_gossip",
    "guild_record",
    "faction_intelligence",
    "household_talk",
    "criminal_whisper",
    "public_notice",
    "song_or_story",
}

VISIBILITIES = {
    "private",
    "witnessed",
    "local",
    "institutional",
    "route",
    "global",
}


def normalize_tag(value):
    return str(value).strip().lower().replace(" ", "_")


def normalize_tags(values):
    normalized = []
    seen = set()
    for value in values or []:
        tag = normalize_tag(value)
        if not tag or tag in seen:
            continue
        seen.add(tag)
        normalized.append(tag)
    return normalized
```

- [ ] **Step 4: Create engine implementation**

Create `world/social_engine.py`:

```python
"""High-level deterministic API for Soravelon's Social Web kernel."""

from django.utils import timezone

from world.social_taxonomy import (
    CLAIM_TYPES,
    EDGE_TYPES,
    KNOWLEDGE_CHANNELS,
    NODE_TYPES,
    VISIBILITIES,
    normalize_tags,
)


def make_node_key(node_type, identifier):
    return f"{node_type}:{identifier}"


def ensure_social_node(
    node_type,
    identifier,
    *,
    display_name="",
    zone_id="",
    settlement_id="",
    faction_id="",
    metadata=None,
):
    from world.models import SocialNode

    if node_type not in NODE_TYPES:
        raise ValueError(f"unsupported node_type: {node_type}")

    node_key = make_node_key(node_type, identifier)
    defaults = {
        "node_type": node_type,
        "display_name": display_name,
        "zone_id": zone_id,
        "settlement_id": settlement_id,
        "faction_id": faction_id,
        "metadata": metadata or {},
    }
    node, created = SocialNode.objects.get_or_create(node_key=node_key, defaults=defaults)
    if not created:
        changed = False
        for field, value in defaults.items():
            if value and getattr(node, field) != value:
                setattr(node, field, value)
                changed = True
        if changed:
            node.save(update_fields=[
                "node_type",
                "display_name",
                "zone_id",
                "settlement_id",
                "faction_id",
                "metadata",
                "updated_at",
            ])
    return node


def _get_node(node_key):
    from world.models import SocialNode

    try:
        return SocialNode.objects.get(node_key=node_key)
    except SocialNode.DoesNotExist:
        return None


def _get_fact(fact_key):
    from world.models import SocialFact

    if not fact_key:
        return None
    try:
        return SocialFact.objects.get(fact_key=fact_key)
    except SocialFact.DoesNotExist:
        return None


def _get_claim(claim_key):
    from world.models import SocialClaim

    if not claim_key:
        return None
    try:
        return SocialClaim.objects.get(claim_key=claim_key)
    except SocialClaim.DoesNotExist:
        return None


def connect_social_nodes(
    source_node_key,
    target_node_key,
    *,
    edge_type,
    directionality="one_way",
    trust=0.5,
    latency_seconds=0,
    bandwidth=3,
    secrecy="",
    distortion="",
    scope_tags=None,
    blockers=None,
):
    from world.models import SocialEdge

    if edge_type not in EDGE_TYPES:
        return False, f"unsupported edge_type: {edge_type}", None

    source = _get_node(source_node_key)
    target = _get_node(target_node_key)
    if not source or not target:
        return False, "source_node and target_node must both exist", None

    edge_key = f"edge:{source_node_key}:{target_node_key}:{edge_type}"
    edge, _created = SocialEdge.objects.update_or_create(
        edge_key=edge_key,
        defaults={
            "source_node": source,
            "target_node": target,
            "edge_type": edge_type,
            "directionality": directionality,
            "trust": trust,
            "latency_seconds": latency_seconds,
            "bandwidth": bandwidth,
            "secrecy": secrecy,
            "distortion": distortion,
            "scope_tags": normalize_tags(scope_tags or []),
            "blockers": blockers or [],
            "active": True,
        },
    )
    return True, "connected", edge


def record_social_fact(
    *,
    fact_key,
    subject_node_key,
    event_type,
    summary,
    actor_node_key="",
    scope_node_key="",
    tags=None,
    visibility="local",
    evidence=None,
    weight=1.0,
    confidence=1.0,
    occurred_at=None,
    expires_at=None,
):
    from world.models import SocialFact

    if visibility not in VISIBILITIES:
        return False, f"unsupported visibility: {visibility}", None

    subject = _get_node(subject_node_key)
    if not subject:
        return False, f"unknown subject_node: {subject_node_key}", None

    actor = _get_node(actor_node_key) if actor_node_key else None
    scope = _get_node(scope_node_key) if scope_node_key else None

    fact, _created = SocialFact.objects.update_or_create(
        fact_key=fact_key,
        defaults={
            "subject_node": subject,
            "actor_node": actor,
            "scope_node": scope,
            "event_type": event_type,
            "summary": summary,
            "tags": normalize_tags(tags or []),
            "visibility": visibility,
            "evidence": evidence or {},
            "weight": float(weight),
            "confidence": float(confidence),
            "occurred_at": occurred_at,
            "expires_at": expires_at,
        },
    )
    return True, "recorded", fact


def assert_social_claim(
    *,
    claim_key,
    speaker_node_key,
    subject_node_key,
    claim_type,
    summary,
    fact_key="",
    status="rumor",
    intent="",
    bias_tags=None,
    confidence=0.5,
):
    from world.models import SocialClaim

    if claim_type not in CLAIM_TYPES:
        return False, f"unsupported claim_type: {claim_type}", None

    speaker = _get_node(speaker_node_key)
    subject = _get_node(subject_node_key)
    fact = _get_fact(fact_key)
    if not speaker or not subject:
        return False, "speaker_node and subject_node must both exist", None

    claim, _created = SocialClaim.objects.update_or_create(
        claim_key=claim_key,
        defaults={
            "fact": fact,
            "speaker_node": speaker,
            "subject_node": subject,
            "claim_type": claim_type,
            "summary": summary,
            "status": status,
            "intent": intent,
            "bias_tags": normalize_tags(bias_tags or []),
            "confidence": float(confidence),
        },
    )
    return True, "asserted", claim


def mark_known(
    *,
    node_key,
    channel,
    fact_key="",
    claim_key="",
    source_node_key="",
    edge_key="",
    confidence=0.5,
    spreading=False,
    available_after=None,
    evidence=None,
):
    from world.models import SocialEdge, SocialKnowledge

    if channel not in KNOWLEDGE_CHANNELS:
        return False, f"unsupported channel: {channel}", None
    if not fact_key and not claim_key:
        return False, "fact_key or claim_key is required", None

    node = _get_node(node_key)
    fact = _get_fact(fact_key)
    claim = _get_claim(claim_key)
    source = _get_node(source_node_key) if source_node_key else None
    edge = None
    if edge_key:
        try:
            edge = SocialEdge.objects.get(edge_key=edge_key)
        except SocialEdge.DoesNotExist:
            return False, f"unknown edge: {edge_key}", None
    if not node:
        return False, f"unknown node: {node_key}", None
    if fact_key and not fact:
        return False, f"unknown fact: {fact_key}", None
    if claim_key and not claim:
        return False, f"unknown claim: {claim_key}", None

    payload_key = claim_key or fact_key
    knowledge_key = f"knowledge:{node_key}:{payload_key}"
    knowledge, _created = SocialKnowledge.objects.update_or_create(
        knowledge_key=knowledge_key,
        defaults={
            "node": node,
            "fact": fact,
            "claim": claim,
            "source_node": source,
            "edge": edge,
            "channel": channel,
            "confidence": float(confidence),
            "spreading": bool(spreading),
            "available_after": available_after,
            "evidence": evidence or {},
        },
    )
    return True, "marked known", knowledge


def record_trace(knowledge, *, from_node=None, to_node=None, edge=None, summary=""):
    from world.models import SocialTrace

    to_node = to_node or knowledge.node
    trace_key = f"trace:{knowledge.knowledge_key}:{edge.edge_key if edge else 'direct'}"
    trace, _created = SocialTrace.objects.update_or_create(
        trace_key=trace_key,
        defaults={
            "knowledge": knowledge,
            "from_node": from_node,
            "to_node": to_node,
            "edge": edge,
            "summary": summary,
        },
    )
    return trace


def available_now_filter(queryset):
    now = timezone.now()
    return queryset.filter(available_after__isnull=True) | queryset.filter(available_after__lte=now)
```

- [ ] **Step 5: Run tests**

Run:

```bash
python scripts/run_tests.py tests.test_social_web_kernel
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add world/social_taxonomy.py world/social_engine.py tests/test_social_web_kernel.py
git commit -m "feat: add social web engine API"
```

## Task 3: Add Deterministic Propagation And Trace Queries

**Files:**

- Modify: `world/social_engine.py`
- Modify: `tests/test_social_web_kernel.py`

- [ ] **Step 1: Add failing propagation tests**

Append to `tests/test_social_web_kernel.py`:

```python
class TestSocialWebPropagation(EvenniaTest):
    """Knowledge crosses only real contact edges."""

    def _seed_report_graph(self):
        from world.social_engine import (
            assert_social_claim,
            connect_social_nodes,
            ensure_social_node,
            mark_known,
            record_social_fact,
        )

        player = ensure_social_node("player", str(self.char1.id), display_name=self.char1.key)
        calloway = ensure_social_node("npc", "npc_warden_agent_calloway")
        commander = ensure_social_node("npc", "npc_warden_outpost_commander")
        innkeeper = ensure_social_node("npc", "npc_innkeeper_whistle")
        ok, message, edge = connect_social_nodes(
            calloway.node_key,
            commander.node_key,
            edge_type="warden_report",
            directionality="one_way",
            trust=0.9,
            scope_tags=["warden", "report", "quest"],
        )
        self.assertTrue(ok, message)
        ok, message, fact = record_social_fact(
            fact_key="fact:test_warden_report_delivered",
            subject_node_key=player.node_key,
            scope_node_key=calloway.node_key,
            event_type="quest_completed",
            summary="The player delivered Calloway's sealed field report.",
            tags=["reliable", "warden", "report"],
            visibility="institutional",
        )
        self.assertTrue(ok, message)
        ok, message, claim = assert_social_claim(
            claim_key="claim:calloway:test_warden_report_delivered",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="report",
            summary="Calloway reports the player carried Warden business cleanly.",
            status="supported",
        )
        self.assertTrue(ok, message)
        ok, message, knowledge = mark_known(
            node_key=calloway.node_key,
            fact_key=fact.fact_key,
            claim_key=claim.claim_key,
            channel="official_report",
            confidence=1.0,
            spreading=True,
        )
        self.assertTrue(ok, message)
        return player, calloway, commander, innkeeper, edge, fact, claim, knowledge

    def test_propagation_uses_contact_edge(self):
        from world.social_engine import propagate_social_knowledge

        player, calloway, commander, innkeeper, edge, fact, claim, knowledge = self._seed_report_graph()

        propagated = propagate_social_knowledge(source_node_key=calloway.node_key, claim_key=claim.claim_key)

        target_keys = [item.node.node_key for item in propagated]
        self.assertEqual(target_keys, [commander.node_key])
        self.assertNotIn(innkeeper.node_key, target_keys)

    def test_propagation_rejects_edge_without_matching_scope_tags(self):
        from world.models import SocialEdge, SocialKnowledge
        from world.social_engine import propagate_social_knowledge

        player, calloway, commander, innkeeper, edge, fact, claim, knowledge = self._seed_report_graph()
        SocialEdge.objects.filter(id=edge.id).update(scope_tags=["market"])

        propagated = propagate_social_knowledge(source_node_key=calloway.node_key, claim_key=claim.claim_key)

        self.assertEqual(propagated, [])
        self.assertFalse(
            SocialKnowledge.objects.filter(
                node=commander,
                claim=claim,
            ).exists()
        )

    def test_trace_social_route_explains_how_target_learned_claim(self):
        from world.social_engine import propagate_social_knowledge, trace_social_route

        player, calloway, commander, innkeeper, edge, fact, claim, knowledge = self._seed_report_graph()
        propagate_social_knowledge(source_node_key=calloway.node_key, claim_key=claim.claim_key)

        trace = trace_social_route(
            source_node_key=calloway.node_key,
            target_node_key=commander.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual(len(trace), 1)
        self.assertEqual(trace[0]["edge_type"], "warden_report")
        self.assertIn("Calloway", trace[0]["summary"])
```

- [ ] **Step 2: Run tests and verify missing functions fail**

Run:

```bash
python scripts/run_tests.py tests.test_social_web_kernel
```

Expected: FAIL because `propagate_social_knowledge` and `trace_social_route` do not exist.

- [ ] **Step 3: Implement propagation helpers**

Append to `world/social_engine.py`:

```python
def _knowledge_payload_tags(knowledge):
    if knowledge.claim and knowledge.claim.fact:
        return set(knowledge.claim.fact.tags or [])
    if knowledge.fact:
        return set(knowledge.fact.tags or [])
    if knowledge.claim:
        return set(knowledge.claim.bias_tags or [])
    return set()


def _edge_allows_knowledge(edge, knowledge):
    if not edge.active:
        return False
    scope_tags = set(edge.scope_tags or [])
    if not scope_tags:
        return True
    payload_tags = _knowledge_payload_tags(knowledge)
    return bool(scope_tags.intersection(payload_tags))


def _outgoing_edges_for(source_node):
    from world.models import SocialEdge

    return SocialEdge.objects.filter(source_node=source_node, active=True).order_by("id")


def propagate_social_knowledge(*, source_node_key, fact_key="", claim_key="", budget=10):
    """Copy spreadable knowledge across allowed outgoing contact edges."""
    from datetime import timedelta
    from world.models import SocialKnowledge

    source = _get_node(source_node_key)
    if not source:
        return []

    payload_key = claim_key or fact_key
    source_knowledge_key = f"knowledge:{source_node_key}:{payload_key}"
    try:
        source_knowledge = SocialKnowledge.objects.get(
            knowledge_key=source_knowledge_key,
            spreading=True,
        )
    except SocialKnowledge.DoesNotExist:
        return []

    propagated = []
    for edge in _outgoing_edges_for(source)[:budget]:
        if not _edge_allows_knowledge(edge, source_knowledge):
            continue
        available_after = None
        if edge.latency_seconds:
            available_after = timezone.now() + timedelta(seconds=edge.latency_seconds)
        ok, _message, knowledge = mark_known(
            node_key=edge.target_node.node_key,
            fact_key=source_knowledge.fact.fact_key if source_knowledge.fact else "",
            claim_key=source_knowledge.claim.claim_key if source_knowledge.claim else "",
            source_node_key=source.node_key,
            edge_key=edge.edge_key,
            channel="official_report" if edge.edge_type in {"warden_report", "official_report"} else "tavern_rumor",
            confidence=min(source_knowledge.confidence, edge.trust),
            spreading=edge.directionality in {"broadcast", "two_way", "gatekept"},
            available_after=available_after,
            evidence={"propagated_from": source.node_key, "edge_key": edge.edge_key},
        )
        if not ok:
            continue
        record_trace(
            knowledge,
            from_node=source,
            to_node=edge.target_node,
            edge=edge,
            summary=(
                f"{source.display_name or source.node_key} carried social knowledge "
                f"to {edge.target_node.display_name or edge.target_node.node_key} "
                f"through {edge.edge_type}."
            ),
        )
        propagated.append(knowledge)
    return propagated


def trace_social_route(*, source_node_key, target_node_key, fact_key="", claim_key=""):
    """Return a compact route explanation for admin/debug surfaces."""
    from world.models import SocialTrace

    target = _get_node(target_node_key)
    if not target:
        return []

    traces = SocialTrace.objects.filter(to_node=target).select_related(
        "from_node",
        "edge",
        "knowledge",
        "knowledge__fact",
        "knowledge__claim",
    ).order_by("created_at")
    if source_node_key:
        traces = traces.filter(from_node__node_key=source_node_key)
    if fact_key:
        traces = traces.filter(knowledge__fact__fact_key=fact_key)
    if claim_key:
        traces = traces.filter(knowledge__claim__claim_key=claim_key)

    return [
        {
            "from_node": trace.from_node.node_key if trace.from_node else "",
            "to_node": trace.to_node.node_key,
            "edge_key": trace.edge.edge_key if trace.edge else "",
            "edge_type": trace.edge.edge_type if trace.edge else "",
            "summary": trace.summary,
        }
        for trace in traces
    ]
```

- [ ] **Step 4: Run tests**

Run:

```bash
python scripts/run_tests.py tests.test_social_web_kernel
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add world/social_engine.py tests/test_social_web_kernel.py
git commit -m "feat: propagate social knowledge across contact edges"
```

## Task 4: Add Bounded Social Context Packs

**Files:**

- Modify: `world/social_engine.py`
- Modify: `tests/test_social_web_kernel.py`

- [ ] **Step 1: Add failing context-pack test**

Append to `tests/test_social_web_kernel.py`:

```python
class TestSocialContextPack(EvenniaTest):
    """Context packs expose only bounded, cited social knowledge."""

    def test_query_social_context_returns_known_claims_with_traces(self):
        from world.social_engine import (
            assert_social_claim,
            connect_social_nodes,
            ensure_social_node,
            mark_known,
            propagate_social_knowledge,
            query_social_context,
            record_social_fact,
        )

        player = ensure_social_node("player", str(self.char1.id), display_name=self.char1.key)
        calloway = ensure_social_node("npc", "npc_warden_agent_calloway", display_name="Agent Calloway")
        commander = ensure_social_node("npc", "npc_warden_outpost_commander", display_name="Outpost Commander")
        connect_social_nodes(
            calloway.node_key,
            commander.node_key,
            edge_type="warden_report",
            scope_tags=["warden", "report"],
        )
        ok, message, fact = record_social_fact(
            fact_key="fact:context_pack_report",
            subject_node_key=player.node_key,
            scope_node_key=calloway.node_key,
            event_type="quest_completed",
            summary="The player delivered the sealed report.",
            tags=["warden", "report", "reliable"],
            visibility="institutional",
        )
        self.assertTrue(ok, message)
        ok, message, claim = assert_social_claim(
            claim_key="claim:context_pack_report",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="report",
            summary="Calloway says the player did not drop the name.",
            status="supported",
        )
        self.assertTrue(ok, message)
        mark_known(
            node_key=calloway.node_key,
            fact_key=fact.fact_key,
            claim_key=claim.claim_key,
            channel="official_report",
            confidence=1.0,
            spreading=True,
        )
        propagate_social_knowledge(source_node_key=calloway.node_key, claim_key=claim.claim_key)

        context = query_social_context(
            viewer_node_key=commander.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
        )

        self.assertEqual(context["viewer"]["node_key"], commander.node_key)
        self.assertEqual(context["subject"]["node_key"], player.node_key)
        self.assertEqual(context["claims"][0]["claim_key"], claim.claim_key)
        self.assertEqual(context["claims"][0]["status"], "supported")
        self.assertEqual(context["claims"][0]["trace"][0]["edge_type"], "warden_report")
```

- [ ] **Step 2: Run tests and verify missing function fails**

Run:

```bash
python scripts/run_tests.py tests.test_social_web_kernel
```

Expected: FAIL because `query_social_context` does not exist.

- [ ] **Step 3: Implement context-pack query**

Append to `world/social_engine.py`:

```python
def _node_payload(node):
    if not node:
        return {}
    return {
        "node_key": node.node_key,
        "node_type": node.node_type,
        "display_name": node.display_name,
        "zone_id": node.zone_id,
        "settlement_id": node.settlement_id,
        "faction_id": node.faction_id,
    }


def query_social_context(*, viewer_node_key, subject_node_key, purpose, max_items=5):
    """Build a bounded context packet for deterministic NPC systems."""
    from world.models import SocialKnowledge

    viewer = _get_node(viewer_node_key)
    subject = _get_node(subject_node_key)
    if not viewer or not subject:
        return {
            "viewer": _node_payload(viewer),
            "subject": _node_payload(subject),
            "purpose": purpose,
            "facts": [],
            "claims": [],
        }

    knowledge_qs = SocialKnowledge.objects.filter(node=viewer).select_related(
        "fact",
        "claim",
        "claim__speaker_node",
        "claim__subject_node",
        "source_node",
        "edge",
    ).order_by("-confidence", "-learned_at")

    facts = []
    claims = []
    for knowledge in knowledge_qs:
        if knowledge.fact and knowledge.fact.subject_node_id == subject.id and len(facts) < max_items:
            facts.append({
                "fact_key": knowledge.fact.fact_key,
                "event_type": knowledge.fact.event_type,
                "summary": knowledge.fact.summary,
                "tags": knowledge.fact.tags,
                "visibility": knowledge.fact.visibility,
                "confidence": knowledge.confidence,
                "channel": knowledge.channel,
            })
        if knowledge.claim and knowledge.claim.subject_node_id == subject.id and len(claims) < max_items:
            claims.append({
                "claim_key": knowledge.claim.claim_key,
                "claim_type": knowledge.claim.claim_type,
                "summary": knowledge.claim.summary,
                "status": knowledge.claim.status,
                "speaker": _node_payload(knowledge.claim.speaker_node),
                "confidence": knowledge.confidence,
                "channel": knowledge.channel,
                "trace": trace_social_route(
                    source_node_key=knowledge.source_node.node_key if knowledge.source_node else "",
                    target_node_key=viewer.node_key,
                    claim_key=knowledge.claim.claim_key,
                ),
            })

    return {
        "viewer": _node_payload(viewer),
        "subject": _node_payload(subject),
        "purpose": purpose,
        "facts": facts,
        "claims": claims,
    }
```

- [ ] **Step 4: Run tests**

Run:

```bash
python scripts/run_tests.py tests.test_social_web_kernel
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add world/social_engine.py tests/test_social_web_kernel.py
git commit -m "feat: build social context packets"
```

## Task 5: Prove The Vael Warden Route Without Editing Content

**Files:**

- Create: `tests/test_social_web_warden_route.py`

- [ ] **Step 1: Add Warden-route proof test**

Create `tests/test_social_web_warden_route.py`:

```python
from evennia.utils.test_resources import EvenniaTest


class TestVaelWardenSocialRoute(EvenniaTest):
    """Vael's Warden report can travel beyond the settlement without omniscience."""

    def test_warden_report_reaches_outpost_contact_but_not_innkeeper(self):
        from world.models import SocialKnowledge
        from world.social_engine import (
            assert_social_claim,
            connect_social_nodes,
            ensure_social_node,
            mark_known,
            propagate_social_knowledge,
            query_social_context,
            record_social_fact,
        )

        player = ensure_social_node(
            "player",
            str(self.char1.id),
            display_name=self.char1.key,
            zone_id="vaels_crossing",
            settlement_id="vaels_crossing",
        )
        calloway = ensure_social_node(
            "npc",
            "npc_warden_agent_calloway",
            display_name="Agent Calloway",
            zone_id="vaels_crossing",
            settlement_id="vaels_crossing",
            faction_id="wardens",
        )
        commander = ensure_social_node(
            "npc",
            "npc_warden_outpost_commander",
            display_name="Outpost Commander",
            zone_id="ashreach_plains",
            settlement_id="ashreach_outpost",
            faction_id="wardens",
        )
        innkeeper = ensure_social_node(
            "npc",
            "npc_innkeeper_whistle",
            display_name="Whistle",
            zone_id="vaels_crossing",
            settlement_id="vaels_crossing",
        )
        ok, message, edge = connect_social_nodes(
            calloway.node_key,
            commander.node_key,
            edge_type="warden_report",
            directionality="one_way",
            trust=0.95,
            scope_tags=["warden", "report", "quest"],
        )
        self.assertTrue(ok, message)

        ok, message, fact = record_social_fact(
            fact_key=f"fact:{self.char1.id}:vc_q_warden_report:delivered",
            subject_node_key=player.node_key,
            actor_node_key=player.node_key,
            scope_node_key=calloway.node_key,
            event_type="quest_completed",
            summary="The player delivered Calloway's sealed field report.",
            tags=["reliable", "warden", "report", "quest"],
            visibility="institutional",
            evidence={"quest_id": "vc_q_warden_report", "source": "test_fixture"},
        )
        self.assertTrue(ok, message)
        ok, message, claim = assert_social_claim(
            claim_key=f"claim:calloway:{self.char1.id}:vc_q_warden_report:delivered",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="report",
            summary="Calloway reports that the player carried Warden business cleanly.",
            status="supported",
            confidence=1.0,
        )
        self.assertTrue(ok, message)
        ok, message, knowledge = mark_known(
            node_key=calloway.node_key,
            fact_key=fact.fact_key,
            claim_key=claim.claim_key,
            channel="official_report",
            confidence=1.0,
            spreading=True,
        )
        self.assertTrue(ok, message)

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual([item.node.node_key for item in propagated], [commander.node_key])
        self.assertFalse(
            SocialKnowledge.objects.filter(
                node=innkeeper,
                claim=claim,
            ).exists()
        )

        commander_context = query_social_context(
            viewer_node_key=commander.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
        )
        innkeeper_context = query_social_context(
            viewer_node_key=innkeeper.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
        )

        self.assertEqual(commander_context["claims"][0]["claim_key"], claim.claim_key)
        self.assertEqual(innkeeper_context["claims"], [])
```

- [ ] **Step 2: Run Warden-route test**

Run:

```bash
python scripts/run_tests.py tests.test_social_web_warden_route
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/test_social_web_warden_route.py
git commit -m "test: prove warden social route propagation"
```

## Task 6: Persist NPC Social Authoring Metadata In AreaBuilder

**Files:**

- Modify: `world/area_builder.py`
- Modify: `tests/test_area_builder.py`

- [ ] **Step 1: Add failing AreaBuilder test**

Append to `tests/test_area_builder.py`:

```python
    def test_npc_social_profile_and_edges_persist_on_db_attrs(self):
        ab = AreaBuilder("social_authoring_zone")
        room = ab.room("square", name="Square", desc="A square.")

        npc = ab.npc(
            room,
            "npc_social_anchor",
            name="Social Anchor",
            social_profile={
                "social_role": "warden_contact",
                "public_trait": "careful Warden contact",
                "worldview": {
                    "admires": ["reliable"],
                    "dislikes": ["reckless"],
                },
            },
            social_edges=[
                {
                    "target": "npc:npc_outpost_contact",
                    "edge_type": "warden_report",
                    "directionality": "one_way",
                    "scope_tags": ["warden", "report"],
                }
            ],
        )

        self.assertEqual(npc.db.social_profile["social_role"], "warden_contact")
        self.assertEqual(npc.db.social_profile["public_trait"], "careful Warden contact")
        self.assertEqual(npc.db.social_edges[0]["edge_type"], "warden_report")
```

- [ ] **Step 2: Run AreaBuilder test and verify it fails**

Run:

```bash
python scripts/run_tests.py tests.test_area_builder.AreaBuilderTestBase.test_npc_social_profile_and_edges_persist_on_db_attrs
```

Expected: FAIL because `social_profile` and `social_edges` are not persisted.

- [ ] **Step 3: Store social metadata on NPC db attrs**

In `world/area_builder.py`, inside `AreaBuilder.npc()` after the dialogue db attrs block, add:

```python
        # --- Social Web authoring metadata -------------------------------
        npc_obj.db.social_profile = kwargs.get("social_profile", {})
        npc_obj.db.social_edges = kwargs.get("social_edges", [])
```

Also include the metadata in `npc_def` near the top of `AreaBuilder.npc()`:

```python
            "social_profile": kwargs.get("social_profile", {}),
            "social_edges": kwargs.get("social_edges", []),
```

- [ ] **Step 4: Run AreaBuilder test**

Run:

```bash
python scripts/run_tests.py tests.test_area_builder.AreaBuilderTestBase.test_npc_social_profile_and_edges_persist_on_db_attrs
```

Expected: PASS.

- [ ] **Step 5: Run zone serializer smoke test**

Run:

```bash
python scripts/run_tests.py tests.test_zone_serializer
```

Expected: PASS. `world/zone_serializer.py` should not need code changes because it already passes unknown NPC kwargs through to `AreaBuilder.npc()`.

- [ ] **Step 6: Commit**

```bash
git add world/area_builder.py tests/test_area_builder.py
git commit -m "feat: persist npc social web metadata"
```

## Task 7: Add Builder/Admin Social Memory Inspection Command

**Files:**

- Create: `commands/cmd_socialmemory.py`
- Create: `tests/test_socialmemory_command.py`
- Modify: `commands/default_cmdsets.py`

- [ ] **Step 1: Write failing command tests**

Create `tests/test_socialmemory_command.py`:

```python
import unittest
from unittest.mock import MagicMock, patch


class TestCmdSocialMemory(unittest.TestCase):
    """socialmemory is a locked admin inspection command."""

    def test_command_is_builder_locked(self):
        from commands.cmd_socialmemory import CmdSocialMemory

        cmd = CmdSocialMemory()

        self.assertEqual(cmd.key, "socialmemory")
        self.assertIn("perm(Builders)", cmd.locks)

    def test_command_reports_usage_without_args(self):
        from commands.cmd_socialmemory import CmdSocialMemory

        caller = MagicMock()
        cmd = CmdSocialMemory()
        cmd.caller = caller
        cmd.args = ""
        cmd.func()

        output = caller.msg.call_args[0][0]
        self.assertIn("Usage: socialmemory", output)

    @patch("world.social_engine.query_social_context")
    def test_command_prints_context_packet(self, mock_query):
        from commands.cmd_socialmemory import CmdSocialMemory

        mock_query.return_value = {
            "facts": [],
            "claims": [
                {
                    "claim_key": "claim:calloway:player:report",
                    "status": "supported",
                    "summary": "Calloway says the player carried Warden business cleanly.",
                    "trace": [
                        {
                            "edge_type": "warden_report",
                            "summary": "Official Warden report carried the claim.",
                        }
                    ],
                }
            ],
        }
        caller = MagicMock()
        cmd = CmdSocialMemory()
        cmd.caller = caller
        cmd.args = "npc:npc_warden_outpost_commander player:1"
        cmd.func()

        output = caller.msg.call_args[0][0]
        self.assertIn("Social Context", output)
        self.assertIn("npc:npc_warden_outpost_commander", output)
        self.assertIn("player:1", output)
        self.assertIn("warden_report", output)
```

- [ ] **Step 2: Run command tests and verify import failure**

Run:

```bash
python scripts/run_tests.py tests.test_socialmemory_command
```

Expected: FAIL because `commands.cmd_socialmemory` does not exist.

- [ ] **Step 3: Create command**

Create `commands/cmd_socialmemory.py`:

```python
"""Builder/admin inspection command for the Social Web kernel."""

from commands.command import Command


class CmdSocialMemory(Command):
    """
    Inspect social knowledge known by one node about another node.

    Usage:
      socialmemory <viewer_node_key> <subject_node_key>

    Example:
      socialmemory npc:npc_warden_outpost_commander player:42
    """

    key = "socialmemory"
    aliases = ["socialweb"]
    locks = "cmd:perm(Builders)"
    help_category = "Admin"

    def func(self):
        args = (self.args or "").strip().split()
        if len(args) != 2:
            self.caller.msg(
                "Usage: socialmemory <viewer_node_key> <subject_node_key>"
            )
            return

        viewer_node_key, subject_node_key = args
        from world.social_engine import query_social_context

        context = query_social_context(
            viewer_node_key=viewer_node_key,
            subject_node_key=subject_node_key,
            purpose="admin",
        )

        lines = [
            "|wSocial Context|n",
            f"viewer: {viewer_node_key}",
            f"subject: {subject_node_key}",
            f"facts: {len(context.get('facts', []))}",
            f"claims: {len(context.get('claims', []))}",
        ]
        for claim in context.get("claims", []):
            lines.append(
                f"- {claim['claim_key']} [{claim['status']}]: {claim['summary']}"
            )
            for trace in claim.get("trace", []):
                lines.append(
                    f"  via {trace['edge_type'] or 'direct'}: {trace['summary']}"
                )
        self.caller.msg("\n".join(lines))
```

- [ ] **Step 4: Register command**

In `commands/default_cmdsets.py`, after the social commands block, add:

```python
        from commands.cmd_socialmemory import CmdSocialMemory
        self.add(CmdSocialMemory())
```

- [ ] **Step 5: Run command tests**

Run:

```bash
python scripts/run_tests.py tests.test_socialmemory_command
```

Expected: PASS.

- [ ] **Step 6: Run cmdset import smoke**

Run:

```bash
python - <<'PY'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django
django.setup()
from commands.default_cmdsets import CharacterCmdSet
cmdset = CharacterCmdSet()
cmdset.at_cmdset_creation()
print("cmdset-ok")
PY
```

Expected: prints `cmdset-ok`.

- [ ] **Step 7: Commit**

```bash
git add commands/cmd_socialmemory.py commands/default_cmdsets.py tests/test_socialmemory_command.py
git commit -m "feat: add social web inspection command"
```

## Task 8: Phase 1 Validation And Handoff

**Files:**

- Modify: `docs/superpowers/plans/2026-06-24-social-web-memory-kernel-phase-1.md` only if implementation discoveries require plan correction.

- [ ] **Step 1: Run focused Social Web suite**

Run:

```bash
python scripts/run_tests.py tests.test_social_web_kernel tests.test_social_web_warden_route tests.test_socialmemory_command
```

Expected: PASS.

- [ ] **Step 2: Run touched adjacent suites**

Run:

```bash
python scripts/run_tests.py tests.test_area_builder tests.test_zone_serializer tests.test_dialogue tests.test_social
```

Expected: PASS.

- [ ] **Step 3: Run migration check**

Run:

```bash
python -m django makemigrations --check --dry-run --settings server.conf.settings
```

Expected: no model changes detected.

- [ ] **Step 4: Run smoke start if available**

Run:

```bash
python scripts/smoke_start.py
```

Expected: server startup smoke completes. If this script is absent or blocked by local Evennia state, record the exact error in the closeout.

- [ ] **Step 5: Write Engram closeout memory**

Write a concise Engram memory with:

- repo path
- branch
- final commit hash
- models and services added
- tests run
- known gaps
- next recommended slice

Suggested key:

```text
soravelon_social_web_kernel_phase_1_2026_06_24
```

- [ ] **Step 6: Final commit if validation changed docs**

If Task 8 required plan/doc corrections, commit them:

```bash
git add docs/superpowers/plans/2026-06-24-social-web-memory-kernel-phase-1.md
git commit -m "docs: update social web kernel phase 1 plan"
```

## Plan Self-Review

Spec coverage:

- Social graph primitives: Task 1.
- Soravelon-native Engram kernel: Tasks 1-4.
- Contact-edge propagation beyond one settlement: Tasks 3 and 5.
- Warden report first proof route: Task 5.
- Bounded context packets: Task 4.
- Admin inspection: Task 7.
- AreaBuilder metadata scaffold: Task 6.

Intentional gaps:

- No LLM integration.
- No dialogue hook.
- No social verbs.
- No settlement mood or myth compaction.
- No live Vael's Crossing content mutation.

These are gaps by design. They should become separate follow-up plans after the kernel is in place and validated.

## Next Plan After Phase 1

The next plan should be **Social Web Dialogue Hook Phase 2**:

- feed `query_social_context()` into `world/dialogue_engine._build_dialogue_context()`
- add deterministic condition keys for supported claims and reputation tags
- wire `vc_q_warden_report` completion into `record_social_fact()` and `assert_social_claim()`
- let Calloway and one out-of-settlement Warden contact react differently
- keep `npc_innkeeper_whistle` ignorant until an inn/traveler edge exists
