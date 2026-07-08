"""
Static data definitions for the NPC dialogue system.

No Django imports, no side effects. Pure data module consumed by
dialogue_engine.py and dialogue commands.

Standing tier thresholds map mob disposition floats to named tiers.
Response priority defines the topic condition evaluation order.
Topic synonyms enable keyword extraction from freeform player input.
"""

# Maximum number of hint topics displayed after a greeting.
# Balances information density vs visual clutter.
MAX_HINTS_DISPLAYED = 4

# Disposition float -> Standing tier string.
# Evaluated top-down; first threshold the disposition meets or exceeds wins.
# Below the lowest threshold (-0.6) maps to "hostile".
# Betrayal is checked separately before disposition lookup.
STANDING_TIER_THRESHOLDS = [
    (0.8, "exalted"),
    (0.6, "honored"),
    (0.4, "friendly"),
    (0.2, "acknowledged"),
    (-0.2, "neutral"),
    (-0.4, "unfriendly"),
    (-0.6, "hostile"),
]

# Topic response condition evaluation order.
# First matching condition wins. Every topic MUST have a "default" response.
RESPONSE_PRIORITY = [
    "quest_complete",
    "quest_failed",
    "quest_active",
    "betrayal",
    "exalted",
    "honored",
    "friendly",
    "acknowledged",
    "suspicious",
    "unfriendly",
    "hostile",
    "scholar_present",
    "warden_present",
    "dragon_present",
    "network_high",
    "reputation_high",
    "social_context",
    "default",
]

# Social Web condition prefixes are evaluated when RESPONSE_PRIORITY reaches
# the "social_context" sentinel. Prefix order is deterministic and specific
# route evidence beats broader claim metadata.
SOCIAL_CONDITION_PREFIX_PRIORITY = [
    "social_fact:",
    "social_claim:",
    "social_claim_trace_edge:",
    "social_fact_tag:",
    "social_fact_event:",
    "social_claim_status:",
    "social_claim_type:",
]

# Global synonym dict for keyword extraction.
# Maps canonical topic key -> list of player-typed words that resolve to it.
TOPIC_SYNONYMS = {
    "wolves": ["wolf", "pack", "animals", "beasts", "creatures"],
    "node": ["magic", "ruins", "glow", "strange", "old magic", "failing", "eight"],
    "work": ["job", "quest", "help", "hire", "pay", "coin", "task", "need"],
    "guilds": ["poachers", "children of men", "hunters", "criminals"],
    "empire": ["imperial", "soldiers", "emperor", "throne"],
    "wardens": ["dragon wardens", "protection", "law"],
    "dragons": ["dragon", "beast", "flying", "scaled"],
    "trade": ["buy", "sell", "goods", "wares", "merchant", "shop"],
    "rumors": ["rumor", "news", "gossip", "heard", "word"],
}

# Dimension thresholds for hint/response conditions
NETWORK_HINT_THRESHOLD = 40
REPUTATION_HINT_THRESHOLD = 40
