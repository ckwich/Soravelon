"""Deterministic NPC interpretation for Social Web context packets."""

from __future__ import annotations

import copy

from world.social_taxonomy import normalize_tags


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
    return copy.deepcopy(profile) if isinstance(profile, dict) else {}


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
            "evidence_channels": _evidence_channels(social_context),
        }

    tags = _context_tags(social_context)
    worldview = profile.get("worldview") or {}
    admires = set(normalize_tags(worldview.get("admires") or []))
    uses = set(normalize_tags(worldview.get("uses") or []))
    matched = sorted((admires | uses).intersection(tags))
    templates = profile.get("templates") or {}
    if not _has_any_context(social_context):
        stance = "neutral"
        summary = templates.get("empty", "They have nothing specific to say.")
    elif _has_supported_evidence(tags):
        stance = "useful" if npc_id == "npc_debt_collector_raith" else "favorable"
        summary = templates.get("supported", "")
    else:
        stance = "uncertain"
        summary = templates.get("rumor", "")

    return {
        "npc_id": npc_id,
        "social_role": profile.get("social_role", ""),
        "public_trait": profile.get("public_trait", ""),
        "memory_style": profile.get("memory_style", ""),
        "stance": stance,
        "summary": summary,
        "matched_tags": matched,
        "evidence_channels": _evidence_channels(social_context),
    }
