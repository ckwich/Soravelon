"""High-level deterministic API for Soravelon's Social Web kernel."""

import math

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


def _coerce_probability(field_name, value):
    try:
        probability = float(value)
    except (TypeError, ValueError):
        return False, f"{field_name} must be between 0.0 and 1.0", None

    if not math.isfinite(probability) or probability < 0.0 or probability > 1.0:
        return False, f"{field_name} must be between 0.0 and 1.0", None
    return True, "", probability


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
            node.save(
                update_fields=[
                    "node_type",
                    "display_name",
                    "zone_id",
                    "settlement_id",
                    "faction_id",
                    "metadata",
                    "updated_at",
                ]
            )
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

    ok, message, trust = _coerce_probability("trust", trust)
    if not ok:
        return False, message, None

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

    ok, message, confidence = _coerce_probability("confidence", confidence)
    if not ok:
        return False, message, None

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
            "confidence": confidence,
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

    ok, message, confidence = _coerce_probability("confidence", confidence)
    if not ok:
        return False, message, None

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
            "confidence": confidence,
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

    ok, message, confidence = _coerce_probability("confidence", confidence)
    if not ok:
        return False, message, None

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
            "confidence": confidence,
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
    return queryset.filter(available_after__isnull=True) | queryset.filter(
        available_after__lte=now
    )
