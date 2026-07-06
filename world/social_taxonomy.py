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
