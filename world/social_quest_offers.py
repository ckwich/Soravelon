"""Social Web-gated quest offers.

This module bridges the deterministic Social Web context packet to the
social-quest grammar. It does not choose quests with an LLM and it does not
write Social Web state while offering a quest.
"""

from __future__ import annotations

import copy

from django.db import OperationalError, ProgrammingError

from world.social_taxonomy import normalize_tags
from world.social_quest_grammar import compile_quest_spec
from world.social_quest_offer_registry import (
    get_social_quest_offer_rule_by_npc,
    get_social_quest_offer_rule_by_quest_id,
)


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


def _description_from_rule(rule, context):
    description = rule.get("description") or {}
    interactions = _prior_interactions_from_context(context)
    memory_summary_field = str(
        description.get("memory_summary_field") or "summary"
    ).strip() or "summary"
    memory = interactions[0].get(memory_summary_field, "") if interactions else ""
    if memory and description.get("with_memory"):
        return description["with_memory"].format(memory_summary=memory)
    return description.get("without_memory") or ""


def _safe_evidence_from_context(context):
    evidence = []
    for fact in (context.get("facts") or []):
        summary = str(fact.get("summary") or "").strip()
        if not summary:
            continue
        evidence.append(
            {
                "kind": "fact",
                "summary": summary,
                "channel": str(fact.get("channel") or "").strip(),
                "visibility": str(fact.get("visibility") or "").strip(),
                "event_type": str(fact.get("event_type") or "").strip(),
            }
        )
    for claim in (context.get("claims") or []):
        summary = str(claim.get("summary") or "").strip()
        if not summary:
            continue
        evidence.append(
            {
                "kind": "claim",
                "summary": summary,
                "channel": str(claim.get("channel") or "").strip(),
                "status": str(claim.get("status") or "").strip(),
                "claim_type": str(claim.get("claim_type") or "").strip(),
            }
        )
    return evidence


def _offer_explainability_from_rule(rule, social_context):
    explainability = copy.deepcopy(rule.get("explainability") or {})
    explainability.setdefault("summary", "")
    explainability.setdefault("npc_safe_reason", "")
    explainability.setdefault("withheld_implications", [])
    explainability["evidence"] = _safe_evidence_from_context(social_context or {})
    return explainability


def _compile_offer_from_rule(rule, *, social_context=None, require_social_grounding=True):
    social_context = social_context or {}
    spec = compile_quest_spec(
        rule["seed_id"],
        rule["archetype_id"],
        quest_id=rule["quest_id"],
        quest_giver=rule["quest_giver"],
        description=_description_from_rule(rule, social_context),
        actors=rule["actors"],
        objective_targets=rule["objective_targets"],
        prior_interactions=_prior_interactions_from_context(social_context),
        social_context=social_context,
        one_chance=rule.get("one_chance", True),
        require_social_grounding=require_social_grounding,
    )
    context = spec.setdefault("social_quest_context", {})
    context["offer_explainability"] = _offer_explainability_from_rule(
        rule,
        social_context,
    )
    context["contest_repair_hooks"] = copy.deepcopy(
        rule.get("contest_repair_hooks") or {}
    )
    return spec


def get_social_quest_spec_by_id(quest_id):
    """Return a deterministic social quest spec for later quest resolution."""
    rule = get_social_quest_offer_rule_by_quest_id(quest_id)
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
    rule = get_social_quest_offer_rule_by_npc(npc_id)
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
