"""Social Web-gated quest offers.

This module bridges the deterministic Social Web context packet to the
social-quest grammar. It does not choose quests with an LLM and it does not
write Social Web state while offering a quest.
"""

from __future__ import annotations

from django.db import OperationalError, ProgrammingError

from world.social_taxonomy import normalize_tags
from world.social_quest_grammar import compile_quest_spec


SOCIAL_QUEST_OFFER_RULES = {
    "npc_warden_agent_calloway": {
        "quest_id": "vc_sq_under_seal_dustwalkers_rest",
        "seed_id": "witness_intimidation",
        "archetype_id": "protect_witness",
        "quest_giver": "npc_warden_agent_calloway",
        "one_chance": True,
        "required_fact_tags": ["warden", "report", "quest"],
        "required_fact_key_fragment": "vc_q_warden_report:delivered",
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
}

SOCIAL_QUEST_OFFER_RULES_BY_QUEST_ID = {
    rule["quest_id"]: rule for rule in SOCIAL_QUEST_OFFER_RULES.values()
}


def _dialogue_node_identifier(value):
    if value is None or isinstance(value, bool):
        return ""
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value.strip()
    return ""


def _npc_id(npc):
    npc_db = getattr(npc, "db", None)
    return _dialogue_node_identifier(getattr(npc_db, "npc_id", None))


def _npc_social_node_key(npc):
    identifier = _npc_id(npc)
    if not identifier:
        identifier = _dialogue_node_identifier(getattr(npc, "key", None))
    return f"npc:{identifier}" if identifier else ""


def _character_social_node_key(character):
    character_id = _dialogue_node_identifier(getattr(character, "id", None))
    return f"player:{character_id}" if character_id else ""


def _context_has_required_fact_tags(context, required_tags):
    required = set(normalize_tags(required_tags or []))
    if not required:
        return True
    for fact in (context.get("facts") or []):
        fact_tags = set(normalize_tags(fact.get("tags") or []))
        if required.issubset(fact_tags):
            return True
    return False


def _context_has_required_fact_key_fragment(context, fragment):
    fragment = str(fragment or "").strip()
    if not fragment:
        return True
    return any(
        fragment in str(fact.get("fact_key") or "")
        for fact in (context.get("facts") or [])
    )


def _prior_interactions_from_context(context):
    interactions = []
    for fact in (context.get("facts") or []):
        summary = str(fact.get("summary") or "").strip()
        if not summary:
            continue
        interactions.append(
            {
                "topic": "Social Web fact",
                "summary": summary,
                "fact_key": fact.get("fact_key", ""),
                "source": fact.get("channel", ""),
            }
        )
    for claim in (context.get("claims") or []):
        summary = str(claim.get("summary") or "").strip()
        if not summary:
            continue
        interactions.append(
            {
                "topic": "Social Web claim",
                "summary": summary,
                "claim_key": claim.get("claim_key", ""),
                "source": claim.get("channel", ""),
            }
        )
    return interactions


def _under_seal_description(context):
    interactions = _prior_interactions_from_context(context)
    memory = interactions[0]["summary"] if interactions else ""
    if memory:
        return (
            f"{memory} Now Calloway has a quieter problem: Whistle at the "
            "Dustwalker's Rest saw someone pressuring access to Warden packet "
            "seals, and Raith's name keeps surfacing around the pressure. "
            "Speak with Whistle, check the inn before the story gets bent, "
            "confront Raith, and bring the testimony back under seal."
        )
    return (
        "Calloway has a quiet problem at the Dustwalker's Rest: Whistle saw "
        "someone pressuring access to Warden packet seals, and Raith's name "
        "keeps surfacing around the pressure. Speak with Whistle, check the "
        "inn, confront Raith, and bring the testimony back under seal."
    )


def _compile_offer_from_rule(rule, *, social_context=None, require_social_grounding=True):
    social_context = social_context or {}
    return compile_quest_spec(
        rule["seed_id"],
        rule["archetype_id"],
        quest_id=rule["quest_id"],
        quest_giver=rule["quest_giver"],
        description=_under_seal_description(social_context),
        actors=rule["actors"],
        objective_targets=rule["objective_targets"],
        prior_interactions=_prior_interactions_from_context(social_context),
        social_context=social_context,
        one_chance=rule.get("one_chance", True),
        require_social_grounding=require_social_grounding,
    )


def get_social_quest_spec_by_id(quest_id):
    """Return a deterministic social quest spec for later quest resolution."""
    rule = SOCIAL_QUEST_OFFER_RULES_BY_QUEST_ID.get(str(quest_id or ""))
    if not rule:
        return None
    return _compile_offer_from_rule(rule, require_social_grounding=False)


def get_social_quest_offer_for_npc(
    npc,
    character,
    *,
    active_ids=None,
    complete_ids=None,
    failed_ids=None,
):
    """Return a Social Web-gated quest offer for an NPC, or None."""
    npc_id = _npc_id(npc)
    rule = SOCIAL_QUEST_OFFER_RULES.get(npc_id)
    if not rule:
        return None

    quest_id = rule["quest_id"]
    active_ids = set(active_ids or [])
    complete_ids = set(complete_ids or [])
    failed_ids = set(failed_ids or [])
    if quest_id in active_ids:
        return None
    if rule.get("one_chance", True) and (quest_id in complete_ids or quest_id in failed_ids):
        return None

    viewer_node_key = _npc_social_node_key(npc)
    subject_node_key = _character_social_node_key(character)
    if not viewer_node_key or not subject_node_key:
        return None

    try:
        from world.social_engine import query_social_context

        social_context = query_social_context(
            viewer_node_key=viewer_node_key,
            subject_node_key=subject_node_key,
            purpose="quest_offer",
        )
    except (OperationalError, ProgrammingError):
        return None

    if not _context_has_required_fact_tags(
        social_context,
        rule.get("required_fact_tags") or [],
    ):
        return None
    if not _context_has_required_fact_key_fragment(
        social_context,
        rule.get("required_fact_key_fragment"),
    ):
        return None

    return _compile_offer_from_rule(rule, social_context=social_context)
