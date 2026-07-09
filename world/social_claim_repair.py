"""Deterministic player contest/repair helpers for Social Web claims."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib


REPAIRABLE_STATUSES = {"rumor", "contested", "unknown"}


@dataclass
class ClaimRepairResult:
    ok: bool
    message: str
    claim: object | None = None
    answered_claim_key: str = ""


def _npc_id(npc):
    npc_db = getattr(npc, "db", None)
    return getattr(npc_db, "npc_id", "") or getattr(npc, "key", "") or "unknown_npc"


def _display_name(obj):
    obj_db = getattr(obj, "db", None)
    return getattr(obj_db, "npc_name", "") or getattr(obj, "key", "") or str(obj)


def _ensure_actor_nodes(character, npc):
    from world.social_engine import ensure_social_node

    character_node = ensure_social_node(
        "player",
        str(character.id),
        display_name=getattr(character, "key", ""),
    )
    npc_db = getattr(npc, "db", None)
    npc_node = ensure_social_node(
        "npc",
        _npc_id(npc),
        display_name=_display_name(npc),
        zone_id=getattr(npc_db, "zone_id", "") or "",
        faction_id=getattr(npc_db, "faction", "") or "",
    )
    return character_node, npc_node


def _topic_matches_claim(claim, topic_text):
    topic = str(topic_text or "").strip().lower()
    if not topic or topic == "me":
        return True
    haystack = " ".join(
        str(value or "")
        for value in (
            claim.get("claim_type"),
            claim.get("status"),
            claim.get("summary"),
        )
    ).lower()
    return topic in haystack


def _find_repairable_claim(npc_node_key, character_node_key, topic_text):
    from world.social_engine import query_social_context

    context = query_social_context(
        viewer_node_key=npc_node_key,
        subject_node_key=character_node_key,
        purpose="claim_repair",
        max_items=10,
    )
    for claim in context.get("claims") or []:
        if claim.get("status") not in REPAIRABLE_STATUSES:
            continue
        if _topic_matches_claim(claim, topic_text):
            return claim
    return None


def _denial_claim_key(character_node_key, npc_node_key, answered_claim_key):
    digest = hashlib.sha256(
        f"{character_node_key}|{npc_node_key}|{answered_claim_key}".encode("utf-8")
    ).hexdigest()[:16]
    character_id = character_node_key.split(":", 1)[-1]
    return f"claim:denial:{character_id}:{digest}"


def deny_social_claim(character, npc, *, topic_text="me"):
    """Record a player denial against a claim the target NPC already knows."""
    from world.models import SocialClaim
    from world.social_engine import assert_social_claim, mark_known, record_trace

    if not getattr(character, "id", None):
        return ClaimRepairResult(
            ok=False,
            message="Your denial does not have a stable identity to attach to.",
        )

    character_node, npc_node = _ensure_actor_nodes(character, npc)
    repairable_claim = _find_repairable_claim(
        npc_node.node_key,
        character_node.node_key,
        topic_text,
    )
    if not repairable_claim:
        return ClaimRepairResult(
            ok=False,
            message=(
                f"{_display_name(npc)} has nothing specific about you that "
                "you can answer right now."
            ),
        )

    answered_claim_key = repairable_claim.get("claim_key", "")
    try:
        answered_claim = SocialClaim.objects.select_related("fact").get(
            claim_key=answered_claim_key,
        )
    except SocialClaim.DoesNotExist:
        return ClaimRepairResult(
            ok=False,
            message="That story is no longer available to answer.",
        )

    summary = (
        f"{getattr(character, 'key', 'The player')} says they deny the story that "
        f"{repairable_claim.get('summary', 'is traveling about them')}"
    )
    ok, message, denial_claim = assert_social_claim(
        claim_key=_denial_claim_key(
            character_node.node_key,
            npc_node.node_key,
            answered_claim.claim_key,
        ),
        speaker_node_key=character_node.node_key,
        subject_node_key=character_node.node_key,
        fact_key=answered_claim.fact.fact_key if answered_claim.fact_id else "",
        claim_type="denial",
        summary=summary,
        status="contested",
        intent="claim_repair",
        bias_tags=["denial", "claim_repair", f"answered:{answered_claim.claim_type}"],
        confidence=0.7,
    )
    if not ok:
        return ClaimRepairResult(ok=False, message=message)

    ok, message, knowledge = mark_known(
        node_key=npc_node.node_key,
        claim_key=denial_claim.claim_key,
        source_node_key=character_node.node_key,
        channel="direct_witness",
        confidence=0.7,
        spreading=False,
        evidence={"answered_claim_key": answered_claim.claim_key},
    )
    if not ok:
        return ClaimRepairResult(ok=False, message=message)

    record_trace(
        knowledge,
        from_node=character_node,
        to_node=npc_node,
        summary=(
            f"{getattr(character, 'key', 'The player')} denied a story directly "
            f"to {_display_name(npc)}."
        ),
    )

    return ClaimRepairResult(
        ok=True,
        message=(
            "hears your denial and weighs it against the story already "
            "moving around you."
        ),
        claim=denial_claim,
        answered_claim_key=answered_claim.claim_key,
    )
