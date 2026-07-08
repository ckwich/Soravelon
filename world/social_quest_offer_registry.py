"""Data registry for Social Web-gated quest offers."""

from __future__ import annotations

import copy


SOCIAL_QUEST_OFFER_RULES = (
    {
        "npc_id": "npc_warden_agent_calloway",
        "quest_id": "vc_sq_under_seal_dustwalkers_rest",
        "seed_id": "witness_intimidation",
        "archetype_id": "protect_witness",
        "quest_giver": "npc_warden_agent_calloway",
        "one_chance": True,
        "required_fact_tags": ["warden", "report", "quest"],
        "required_fact_key_fragment": "vc_q_warden_report:delivered",
        "description": {
            "memory_summary_field": "summary",
            "with_memory": (
                "{memory_summary} Now Calloway has a quieter problem: Whistle "
                "at the Dustwalker's Rest saw someone pressuring access to "
                "Warden packet seals, and Raith's name keeps surfacing around "
                "the pressure. Speak with Whistle, check the inn before the "
                "story gets bent, confront Raith, and bring the testimony back "
                "under seal."
            ),
            "without_memory": (
                "Calloway has a quiet problem at the Dustwalker's Rest: "
                "Whistle saw someone pressuring access to Warden packet seals, "
                "and Raith's name keeps surfacing around the pressure. Speak "
                "with Whistle, check the inn, confront Raith, and bring the "
                "testimony back under seal."
            ),
        },
        "explainability": {
            "summary": "Calloway is acting on the sealed Warden report you delivered.",
            "npc_safe_reason": (
                "The Wardens have a supported report that you carried sealed "
                "business cleanly."
            ),
            "withheld_implications": [
                "Do not say Harven vouched for the player unless a Warden-report trace is present.",
                "Do not imply Whistle knows the Warden report unless an inn or traveler edge carries it.",
            ],
        },
        "contest_repair_hooks": {
            "future_archetypes": [
                "expose_false_claim",
                "broker_compromise",
            ],
            "future_social_verbs": [
                "deny",
                "confess",
                "vouch",
                "warn",
            ],
            "repair_tags": [
                "corrective_testimony",
                "reputation_repair",
                "supported_report",
            ],
            "notes": (
                "If the Warden seal story later becomes contested, repair must "
                "flow through Social Web facts, claims, and traceable testimony."
            ),
        },
        "actors": {
            "witness": {
                "node_key": "npc:npc_innkeeper_whistle",
                "display_name": "Whistle",
                "zone_id": "vaels_crossing",
                "settlement_id": "vaels_crossing",
            },
            "coercer": {
                "node_key": "npc:npc_debt_collector_raith",
                "display_name": "Raith",
                "zone_id": "vaels_crossing",
                "settlement_id": "vaels_crossing",
            },
            "authority": {
                "node_key": "npc:npc_warden_agent_calloway",
                "display_name": "Agent Calloway",
                "zone_id": "vaels_crossing",
                "settlement_id": "vaels_crossing",
                "faction_id": "wardens",
            },
        },
        "objective_targets": {
            "interview_witness": "npc_innkeeper_whistle",
            "secure_witness_route": "rd_inn",
            "confront_coercer": "npc_debt_collector_raith",
            "record_testimony": "npc_warden_agent_calloway",
        },
    },
)

_RULES_BY_NPC_ID = {rule["npc_id"]: rule for rule in SOCIAL_QUEST_OFFER_RULES}
_RULES_BY_QUEST_ID = {rule["quest_id"]: rule for rule in SOCIAL_QUEST_OFFER_RULES}


def _copy_rule(rule):
    return copy.deepcopy(rule) if rule else None


def iter_social_quest_offer_rules():
    """Return isolated copies of every Social Web offer rule."""
    return tuple(copy.deepcopy(rule) for rule in SOCIAL_QUEST_OFFER_RULES)


def get_social_quest_offer_rule_by_npc(npc_id):
    """Return an isolated offer rule copy for an NPC id, or None."""
    return _copy_rule(_RULES_BY_NPC_ID.get(str(npc_id or "")))


def get_social_quest_offer_rule_by_quest_id(quest_id):
    """Return an isolated offer rule copy for a quest id, or None."""
    return _copy_rule(_RULES_BY_QUEST_ID.get(str(quest_id or "")))
