"""High-level deterministic API for Soravelon's Social Web kernel."""

import hashlib
import math

from django.db.models import Prefetch, Q
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


def _coerce_non_negative_int(field_name, value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return False, f"{field_name} must be a non-negative integer", None
    return True, "", value


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

    directionality_choices = {choice[0] for choice in SocialEdge.DIRECTION_CHOICES}
    if directionality not in directionality_choices:
        return False, f"unsupported directionality: {directionality}", None

    ok, message, latency_seconds = _coerce_non_negative_int(
        "latency_seconds", latency_seconds
    )
    if not ok:
        return False, message, None

    ok, message, bandwidth = _coerce_non_negative_int("bandwidth", bandwidth)
    if not ok:
        return False, message, None

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
    if actor_node_key and not actor:
        return False, f"unknown actor_node: {actor_node_key}", None

    scope = _get_node(scope_node_key) if scope_node_key else None
    if scope_node_key and not scope:
        return False, f"unknown scope_node: {scope_node_key}", None

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
    if fact_key and not fact:
        return False, f"unknown fact: {fact_key}", None
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
    if source_node_key and not source:
        return False, f"unknown source_node: {source_node_key}", None
    if fact and claim and claim.fact_id != fact.id:
        return False, f"claim does not reference fact: {fact_key}", None
    if claim and not fact and claim.fact_id:
        fact = claim.fact

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
    return queryset.filter(Q(available_after__isnull=True) | Q(available_after__lte=now))


def _knowledge_payload_tags(knowledge):
    tags = set()
    fact = knowledge.fact
    if not fact and knowledge.claim and knowledge.claim.fact_id:
        fact = knowledge.claim.fact
    if fact:
        tags.update(normalize_tags(fact.tags or []))
    if knowledge.claim:
        tags.update(normalize_tags(knowledge.claim.bias_tags or []))
        tags.update(
            normalize_tags(
                value
                for value in (
                    knowledge.claim.claim_type,
                    knowledge.claim.status,
                    knowledge.claim.intent,
                )
                if value
            )
        )
    return tags


def _channel_for_edge_type(edge_type):
    return {
        "direct_witness": "direct_witness",
        "official_report": "official_report",
        "warden_report": "official_report",
        "market_route": "market_gossip",
        "guild_courier": "guild_record",
        "family_letter": "household_talk",
        "criminal_whisper": "criminal_whisper",
        "inn_traveler": "tavern_rumor",
        "pilgrimage": "song_or_story",
        "archive_copy": "guild_record",
        "node_response": "public_notice",
    }.get(edge_type, "tavern_rumor")


def _source_knowledge_for(source, *, fact_key="", claim_key=""):
    from django.db.models import Case, IntegerField, Value, When
    from world.models import SocialKnowledge

    queryset = SocialKnowledge.objects.filter(node=source, spreading=True).select_related(
        "fact",
        "claim",
        "claim__fact",
    )
    if fact_key:
        queryset = queryset.filter(
            Q(fact__fact_key=fact_key) | Q(claim__fact__fact_key=fact_key)
        )
    if claim_key:
        queryset = queryset.filter(claim__claim_key=claim_key)

    return (
        available_now_filter(queryset)
        .annotate(
            claim_rank=Case(
                When(claim__isnull=False, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        .order_by("claim_rank", "id")
        .first()
    )


def _merged_available_after(existing_knowledge, proposed_available_after):
    if not existing_knowledge:
        return proposed_available_after
    if existing_knowledge.available_after is None or proposed_available_after is None:
        return None
    return min(existing_knowledge.available_after, proposed_available_after)


def _knowledge_payload_key(knowledge):
    if knowledge.claim:
        return knowledge.claim.claim_key
    if knowledge.fact:
        return knowledge.fact.fact_key
    return ""


def _edge_allows_knowledge(edge, knowledge):
    if not edge.active:
        return False
    if edge.bandwidth <= 0:
        return False
    payload_tags = _knowledge_payload_tags(knowledge)
    blockers = set(normalize_tags(edge.blockers or []))
    if blockers and not blockers.intersection(payload_tags):
        return False
    scope_tags = set(normalize_tags(edge.scope_tags or []))
    if not scope_tags:
        return True
    return bool(scope_tags.intersection(payload_tags))


def _propagation_paths_for(source_node):
    from world.models import SocialEdge

    outgoing = list(
        SocialEdge.objects.filter(source_node=source_node, active=True)
        .select_related("target_node")
        .order_by("id")
    )
    reversible = list(
        SocialEdge.objects.filter(
            target_node=source_node,
            active=True,
            directionality="two_way",
        )
        .select_related("source_node")
        .order_by("id")
    )
    paths = [
        {"edge": edge, "target": edge.target_node, "reverse": False}
        for edge in outgoing
    ]
    paths.extend(
        {"edge": edge, "target": edge.source_node, "reverse": True}
        for edge in reversible
    )
    return sorted(paths, key=lambda path: path["edge"].id)


def _distorted_claim_key(edge, target, source_knowledge):
    payload_key = _knowledge_payload_key(source_knowledge)
    digest = hashlib.sha1(
        f"{edge.edge_key}|{target.node_key}|{payload_key}|{edge.distortion}".encode(
            "utf-8"
        )
    ).hexdigest()[:16]
    return f"claim:rumor:{target.id}:{digest}"


def _distorted_claim_for_edge(edge, target, source_knowledge):
    if edge.distortion != "rumor":
        return source_knowledge.claim
    if not source_knowledge.claim and not source_knowledge.fact:
        return None

    source_claim = source_knowledge.claim
    source_fact = source_knowledge.fact or source_claim.fact
    source_summary = source_claim.summary if source_claim else source_fact.summary
    subject = source_fact.subject_node if source_fact else source_claim.subject_node
    target_name = target.display_name or target.node_key
    source_key = source_claim.claim_key if source_claim else source_fact.fact_key
    claim_key = _distorted_claim_key(edge, target, source_knowledge)
    ok, _message, claim = assert_social_claim(
        claim_key=claim_key,
        speaker_node_key=target.node_key,
        subject_node_key=subject.node_key,
        fact_key=source_fact.fact_key if source_fact else "",
        claim_type="rumor",
        summary=f"A road rumor at {target_name} says: {source_summary}",
        status="rumor",
        intent="distorted_propagation",
        bias_tags=["rumor", "distorted", f"source:{source_key}"],
        confidence=min(source_knowledge.confidence, edge.trust) * 0.75,
    )
    return claim if ok else None


def propagate_social_knowledge(*, source_node_key, fact_key="", claim_key="", budget=10):
    """Copy spreadable knowledge across allowed outgoing contact edges."""
    from datetime import timedelta

    from world.models import SocialKnowledge

    source = _get_node(source_node_key)
    if not source:
        return []

    payload_key = claim_key or fact_key
    if not payload_key:
        return []

    ok, _message, budget = _coerce_non_negative_int("budget", budget)
    if not ok or budget == 0:
        return []

    source_knowledge = _source_knowledge_for(
        source,
        fact_key=fact_key,
        claim_key=claim_key,
    )
    if not source_knowledge:
        return []

    propagated = []
    for path in _propagation_paths_for(source)[:budget]:
        edge = path["edge"]
        if not _edge_allows_knowledge(edge, source_knowledge):
            continue

        available_after = None
        if edge.latency_seconds > 0:
            available_after = timezone.now() + timedelta(seconds=edge.latency_seconds)

        target = path["target"]
        carried_claim = _distorted_claim_for_edge(edge, target, source_knowledge)
        carried_fact = source_knowledge.fact
        if not carried_fact and carried_claim and carried_claim.fact_id:
            carried_fact = carried_claim.fact
        carried_payload_key = carried_claim.claim_key if carried_claim else (
            carried_fact.fact_key if carried_fact else ""
        )
        if not carried_payload_key:
            continue
        existing_target = SocialKnowledge.objects.filter(
            knowledge_key=f"knowledge:{target.node_key}:{carried_payload_key}"
        ).only("available_after").first()
        available_after = _merged_available_after(existing_target, available_after)
        confidence = min(source_knowledge.confidence, edge.trust)
        if edge.distortion:
            confidence *= 0.75
        ok, _message, knowledge = mark_known(
            node_key=target.node_key,
            fact_key=carried_fact.fact_key if carried_fact else "",
            claim_key=carried_claim.claim_key if carried_claim else "",
            source_node_key=source.node_key,
            edge_key=edge.edge_key,
            channel=_channel_for_edge_type(edge.edge_type),
            confidence=confidence,
            spreading=edge.directionality in {"broadcast", "two_way", "gatekept"},
            available_after=available_after,
            evidence={
                "propagated_from": source.node_key,
                "edge_key": edge.edge_key,
                "payload_key": carried_payload_key,
                "reverse": path["reverse"],
                "distortion": edge.distortion,
                "source_payload_key": _knowledge_payload_key(source_knowledge),
            },
        )
        if not ok:
            continue

        source_name = source.display_name or source.node_key
        target_name = target.display_name or target.node_key
        record_trace(
            knowledge,
            from_node=source,
            to_node=target,
            edge=edge,
            summary=(
                f"{source_name} propagated {carried_payload_key} to {target_name} "
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
        "to_node",
        "edge",
        "knowledge",
        "knowledge__fact",
        "knowledge__claim",
    )
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
        for trace in traces.order_by("created_at", "id")
    ]


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


def _trace_payloads_for_knowledge(knowledge):
    traces = getattr(knowledge, "_context_traces", None)
    if traces is None:
        traces = knowledge.traces.select_related(
            "from_node",
            "to_node",
            "edge",
        ).order_by("created_at", "id")

    return [
        {
            "from_node": trace.from_node.node_key if trace.from_node else "",
            "to_node": trace.to_node.node_key if trace.to_node else "",
            "edge_key": trace.edge.edge_key if trace.edge else "",
            "edge_type": trace.edge.edge_type if trace.edge else "",
            "summary": trace.summary,
        }
        for trace in traces
    ]


def query_social_context(*, viewer_node_key, subject_node_key, purpose, max_items=5):
    """Build a bounded context packet for deterministic NPC systems."""
    from world.models import SocialKnowledge, SocialTrace

    viewer = _get_node(viewer_node_key)
    subject = _get_node(subject_node_key)
    purpose = str(purpose)
    if not viewer or not subject:
        return {
            "viewer": _node_payload(viewer),
            "subject": _node_payload(subject),
            "purpose": purpose,
            "facts": [],
            "claims": [],
        }

    max_items = max(0, int(max_items))
    trace_qs = SocialTrace.objects.select_related(
        "from_node",
        "to_node",
        "edge",
    ).order_by("created_at", "id")
    knowledge_qs = (
        SocialKnowledge.objects.filter(node=viewer)
        .filter(Q(fact__subject_node=subject) | Q(claim__subject_node=subject))
        .select_related(
            "fact",
            "claim",
            "claim__speaker_node",
            "source_node",
            "edge",
        )
        .prefetch_related(
            Prefetch("traces", queryset=trace_qs, to_attr="_context_traces")
        )
    )
    knowledge_qs = available_now_filter(knowledge_qs).order_by(
        "-confidence",
        "-learned_at",
        "id",
    )

    facts = []
    claims = []
    seen_fact_keys = set()
    seen_claim_keys = set()
    for knowledge in knowledge_qs:
        if len(facts) >= max_items and len(claims) >= max_items:
            break

        if (
            knowledge.fact
            and knowledge.fact.subject_node_id == subject.id
            and knowledge.fact.fact_key not in seen_fact_keys
            and len(facts) < max_items
        ):
            seen_fact_keys.add(knowledge.fact.fact_key)
            facts.append(
                {
                    "fact_key": knowledge.fact.fact_key,
                    "event_type": knowledge.fact.event_type,
                    "summary": knowledge.fact.summary,
                    "tags": list(knowledge.fact.tags or []),
                    "visibility": knowledge.fact.visibility,
                    "confidence": knowledge.confidence,
                    "channel": knowledge.channel,
                    "trace": _trace_payloads_for_knowledge(knowledge),
                }
            )

        if (
            knowledge.claim
            and knowledge.claim.subject_node_id == subject.id
            and knowledge.claim.claim_key not in seen_claim_keys
            and len(claims) < max_items
        ):
            seen_claim_keys.add(knowledge.claim.claim_key)
            claims.append(
                {
                    "claim_key": knowledge.claim.claim_key,
                    "claim_type": knowledge.claim.claim_type,
                    "summary": knowledge.claim.summary,
                    "status": knowledge.claim.status,
                    "speaker": _node_payload(knowledge.claim.speaker_node),
                    "confidence": knowledge.confidence,
                    "channel": knowledge.channel,
                    "trace": _trace_payloads_for_knowledge(knowledge),
                }
            )

    return {
        "viewer": _node_payload(viewer),
        "subject": _node_payload(subject),
        "purpose": purpose,
        "facts": facts,
        "claims": claims,
    }
