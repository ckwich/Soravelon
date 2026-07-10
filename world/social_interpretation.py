"""Deterministic NPC interpretation for Social Web context packets."""

from __future__ import annotations

import copy
from collections.abc import Mapping

from world.social_taxonomy import normalize_tags


VALID_INTERPRETATION_STANCES = frozenset(
    {"neutral", "favorable", "useful", "uncertain", "skeptical", "guarded"}
)


def _npc_id_from_key(value):
    npc_db = getattr(value, "db", None)
    if npc_db is not None:
        value = getattr(npc_db, "npc_id", None) or getattr(value, "key", None)
    value = str(value or "").strip()
    if ":" in value:
        return value.split(":", 1)[1]
    return value


def get_social_profile(npc):
    """Return the builder-authored profile persisted on a live NPC object."""
    npc_db = getattr(npc, "db", None)
    profile = getattr(npc_db, "social_profile", None) if npc_db else None
    return copy.deepcopy(dict(profile)) if isinstance(profile, Mapping) else {}


def _context_tags(social_context):
    tags = []
    for fact in (social_context or {}).get("facts") or []:
        tags.extend(fact.get("tags") or [])
        tags.extend([fact.get("event_type"), fact.get("channel")])
    for claim in (social_context or {}).get("claims") or []:
        tags.extend(
            [
                claim.get("claim_type"),
                claim.get("status"),
                claim.get("channel"),
            ]
        )
        for trace in claim.get("trace") or []:
            if isinstance(trace, dict):
                tags.append(trace.get("edge_type"))
    return normalize_tags(tags)


def _evidence_channels(social_context):
    channels = []
    for item in list((social_context or {}).get("facts") or []) + list(
        (social_context or {}).get("claims") or []
    ):
        channel = str(item.get("channel") or "").strip().replace("_", " ")
        if channel and channel not in channels:
            channels.append(channel)
    return channels


def _has_supported_evidence(tags):
    return bool(
        {"supported", "official_report", "warden_report", "reliable"} & set(tags)
    )


def _has_any_context(social_context):
    return bool(
        (social_context or {}).get("facts") or (social_context or {}).get("claims")
    )


def _profile_tags(worldview, field_name):
    return set(normalize_tags((worldview or {}).get(field_name) or []))


def _profile_stance(
    *,
    social_role,
    has_context,
    has_supported_evidence,
    admired_tags,
    skeptical_tags,
    feared_tags,
    preferred_channels,
):
    """Choose an authored NPC's bounded response posture for known context."""
    if not has_context:
        return "neutral"
    if feared_tags:
        return "guarded"
    if social_role == "creditor" and (admired_tags or preferred_channels):
        return "useful"
    if skeptical_tags and not (admired_tags or preferred_channels):
        return "skeptical"
    if has_supported_evidence:
        return "favorable"
    return "uncertain"


def build_social_interpretation(npc, social_context):
    """Build a bounded, player-safe interpretation packet for one NPC."""
    npc_id = _npc_id_from_key(npc)
    profile = get_social_profile(npc)
    if not profile:
        return {
            "npc_id": npc_id,
            "social_role": "listener",
            "public_trait": "",
            "memory_style": "",
            "stance": "neutral",
            "summary": "They have heard nothing specific enough to judge.",
            "matched_tags": [],
            "admired_tags": [],
            "skeptical_tags": [],
            "feared_tags": [],
            "preferred_channels": [],
            "evidence_channels": _evidence_channels(social_context),
        }

    tags = _context_tags(social_context)
    worldview = profile.get("worldview") or {}
    admires = _profile_tags(worldview, "admires")
    skeptical_of = _profile_tags(worldview, "skeptical_of")
    fears = _profile_tags(worldview, "fears")
    uses = _profile_tags(worldview, "uses")
    admired_tags = sorted(admires.intersection(tags))
    skeptical_tags = sorted(skeptical_of.intersection(tags))
    feared_tags = sorted(fears.intersection(tags))
    preferred_channels = sorted(uses.intersection(tags))
    matched = sorted(
        set(admired_tags)
        | set(skeptical_tags)
        | set(feared_tags)
        | set(preferred_channels)
    )
    templates = profile.get("templates") or {}
    has_context = _has_any_context(social_context)
    if not has_context:
        summary = templates.get("empty", "They have nothing specific to say.")
    elif _has_supported_evidence(tags):
        summary = templates.get("supported", "")
    else:
        summary = templates.get("rumor", "")
    stance = _profile_stance(
        social_role=profile.get("social_role", ""),
        has_context=has_context,
        has_supported_evidence=_has_supported_evidence(tags),
        admired_tags=admired_tags,
        skeptical_tags=skeptical_tags,
        feared_tags=feared_tags,
        preferred_channels=preferred_channels,
    )

    return {
        "npc_id": npc_id,
        "social_role": profile.get("social_role", ""),
        "public_trait": profile.get("public_trait", ""),
        "memory_style": profile.get("memory_style", ""),
        "stance": stance,
        "summary": summary,
        "matched_tags": matched,
        "admired_tags": admired_tags,
        "skeptical_tags": skeptical_tags,
        "feared_tags": feared_tags,
        "preferred_channels": preferred_channels,
        "evidence_channels": _evidence_channels(social_context),
    }
