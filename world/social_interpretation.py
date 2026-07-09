"""Deterministic NPC interpretation for Social Web context packets."""

from __future__ import annotations

import copy

from world.social_taxonomy import normalize_tags


SOCIAL_INTERPRETATION_PROFILES = {
    "npc_warden_agent_calloway": {
        "social_role": "gatekeeper",
        "public_trait": "careful Warden contact",
        "memory_style": "files supported reports before rumor",
        "worldview": {
            "admires": ["reliable", "warden", "report", "supported"],
            "skeptical_of": ["rumor", "boast", "reckless"],
            "uses": ["official_report", "warden_report"],
        },
        "templates": {
            "supported": (
                "Calloway treats this as a supported report, not tavern color. "
                "He weighs the official report first and lets it decide how "
                "much road business to put in your hands."
            ),
            "rumor": (
                "Calloway notes the rumor but does not file it as confirmed. "
                "He will ask for a report before he changes Warden posture."
            ),
            "empty": "Calloway has nothing specific enough to file about you.",
        },
    },
    "npc_warden_outpost_commander": {
        "social_role": "field_commander",
        "public_trait": "road-worn field commander",
        "memory_style": "remembers what keeps patrol lines alive",
        "worldview": {
            "admires": ["reliable", "warden", "route", "report"],
            "skeptical_of": ["rumor", "delay"],
            "uses": ["warden_report", "official_report"],
        },
        "templates": {
            "supported": (
                "Harven reads this as field reliability. If the Warden line "
                "carried it, he treats the report as something that may keep "
                "the next patrol alive."
            ),
            "rumor": (
                "Harven hears the road noise but keeps it below confirmed "
                "field intelligence until a Warden line carries it."
            ),
            "empty": "Harven has no field report that changes how he reads you.",
        },
    },
    "npc_innkeeper_whistle": {
        "social_role": "gossip",
        "public_trait": "innkeeper with a long ear",
        "memory_style": "remembers who makes trouble expensive in the taproom",
        "worldview": {
            "admires": ["tavern", "road_rumor", "discreet", "reliable"],
            "skeptical_of": ["official_report", "warden", "sealed"],
            "uses": ["tavern_rumor", "inn_traveler"],
        },
        "templates": {
            "supported": (
                "Whistle heard it as road talk, not a sworn ledger. He keeps "
                "sealed details at arm's length, but he remembers that your "
                "name travels cleanly through the inn."
            ),
            "rumor": (
                "Whistle heard it as road talk and keeps sealed details at "
                "arm's length. He remembers the shape of the story, not the "
                "Warden business inside it."
            ),
            "empty": "Whistle has no fair story about you yet.",
        },
    },
    "npc_debt_collector_raith": {
        "social_role": "creditor",
        "public_trait": "obligation broker",
        "memory_style": "remembers leverage, debt, and who follows through",
        "worldview": {
            "admires": ["obligation", "leverage", "useful", "reliable"],
            "skeptical_of": ["charity", "official_report"],
            "uses": ["criminal_whisper", "tavern_rumor", "direct_witness"],
        },
        "templates": {
            "supported": (
                "Raith reads the report as leverage: a useful person who "
                "finishes sealed work may also finish uncomfortable work."
            ),
            "rumor": (
                "Raith treats the rumor as possible leverage, useful enough to "
                "watch but not clean enough to spend yet."
            ),
            "empty": "Raith has not found a useful angle on you yet.",
        },
    },
    "npc_courier_agent_renn": {
        "social_role": "broker",
        "public_trait": "route-minded courier agent",
        "memory_style": "remembers which names make routes arrive intact",
        "worldview": {
            "admires": ["route", "trade", "reliable", "report"],
            "skeptical_of": ["delay", "reckless", "rumor"],
            "uses": ["market_gossip", "official_report", "guild_record"],
        },
        "templates": {
            "supported": (
                "Renn reads this as route reliability. A name attached to a "
                "clean delivery changes who he trusts with a satchel."
            ),
            "rumor": (
                "Renn hears the rumor as route weather: useful to watch, too "
                "thin to schedule around."
            ),
            "empty": "Renn has no route note about you yet.",
        },
    },
}


def _npc_id_from_key(value):
    value = str(value or "").strip()
    if ":" in value:
        return value.split(":", 1)[1]
    return value


def get_social_profile(npc_id):
    """Return an isolated authored Social Web interpretation profile."""
    profile = SOCIAL_INTERPRETATION_PROFILES.get(_npc_id_from_key(npc_id))
    return copy.deepcopy(profile) if profile else {}


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
    return bool({"supported", "official_report", "warden_report", "reliable"} & set(tags))


def _has_any_context(social_context):
    return bool((social_context or {}).get("facts") or (social_context or {}).get("claims"))


def build_social_interpretation(npc_id, social_context):
    """Build a bounded, player-safe interpretation packet for one NPC."""
    npc_id = _npc_id_from_key(npc_id)
    profile = get_social_profile(npc_id)
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
