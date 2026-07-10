"""Data registry for Social Web-gated quest offers."""

from __future__ import annotations

import copy


class SocialQuestOfferRegistryError(ValueError):
    """An authored Social Web offer rule cannot be selected safely."""


SOCIAL_QUEST_OFFER_RULES = (
    {
        "npc_id": "npc_warden_agent_calloway",
        "quest_id": "vc_sq_under_seal_dustwalkers_rest",
        "priority": 100,
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


def _nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def _rule_sort_key(rule):
    return (-rule["priority"], rule["quest_id"])


def validate_social_quest_offer_rules(rules):
    """Reject ambiguous, ungrounded, or malformed authored offer rules."""
    if not isinstance(rules, (list, tuple)):
        raise SocialQuestOfferRegistryError("offer rules must be a sequence")

    errors = []
    seen_quest_ids = set()
    seen_npc_quest_pairs = set()
    for index, rule in enumerate(rules):
        label = f"offer rule {index}"
        if not isinstance(rule, dict):
            errors.append(f"{label} must be a dictionary")
            continue

        for field_name in (
            "npc_id",
            "quest_id",
            "seed_id",
            "archetype_id",
            "quest_giver",
        ):
            if not _nonempty_text(rule.get(field_name)):
                errors.append(f"{label} requires non-empty {field_name}")

        priority = rule.get("priority", 0)
        if isinstance(priority, bool) or not isinstance(priority, int):
            errors.append(f"{label} priority must be an integer")

        tags = rule.get("required_fact_tags", [])
        if not isinstance(tags, list) or any(
            not _nonempty_text(tag) for tag in tags
        ):
            errors.append(f"{label} required_fact_tags must be strings")
            tags = []
        fragment = rule.get("required_fact_key_fragment", "")
        if not isinstance(fragment, str):
            errors.append(f"{label} required_fact_key_fragment must be a string")
            fragment = ""
        if not tags and not fragment.strip():
            errors.append(f"{label} requires at least one fact predicate")

        if not isinstance(rule.get("actors"), dict):
            errors.append(f"{label} actors must be a dictionary")
        if not isinstance(rule.get("objective_targets"), dict):
            errors.append(f"{label} objective_targets must be a dictionary")
        if not isinstance(rule.get("description"), dict):
            errors.append(f"{label} description must be a dictionary")
        if "one_chance" in rule and not isinstance(rule["one_chance"], bool):
            errors.append(f"{label} one_chance must be a boolean")

        quest_id = rule.get("quest_id")
        npc_id = rule.get("npc_id")
        if _nonempty_text(quest_id):
            if quest_id in seen_quest_ids:
                errors.append(f"duplicate quest_id: {quest_id}")
            seen_quest_ids.add(quest_id)
        if _nonempty_text(npc_id) and _nonempty_text(quest_id):
            pair = (npc_id, quest_id)
            if pair in seen_npc_quest_pairs:
                errors.append(f"duplicate NPC/quest rule: {npc_id}/{quest_id}")
            seen_npc_quest_pairs.add(pair)

    if errors:
        raise SocialQuestOfferRegistryError("; ".join(errors))


def group_social_quest_offer_rules(rules):
    """Group validated rules for one NPC, highest priority first then quest ID."""
    validate_social_quest_offer_rules(rules)
    grouped = {}
    for rule in rules:
        grouped.setdefault(rule["npc_id"], []).append(rule)
    return {
        npc_id: tuple(sorted(npc_rules, key=_rule_sort_key))
        for npc_id, npc_rules in grouped.items()
    }


validate_social_quest_offer_rules(SOCIAL_QUEST_OFFER_RULES)
_RULES_BY_NPC_ID = group_social_quest_offer_rules(SOCIAL_QUEST_OFFER_RULES)
_RULES_BY_QUEST_ID = {rule["quest_id"]: rule for rule in SOCIAL_QUEST_OFFER_RULES}


def _copy_rule(rule):
    return copy.deepcopy(rule) if rule else None


def iter_social_quest_offer_rules():
    """Return isolated copies of every Social Web offer rule."""
    return tuple(
        copy.deepcopy(rule)
        for rule in sorted(SOCIAL_QUEST_OFFER_RULES, key=_rule_sort_key)
    )


def get_social_quest_offer_rules_by_npc(npc_id):
    """Return every offer the NPC may evaluate, in deterministic display order."""
    rules = _RULES_BY_NPC_ID.get(str(npc_id or ""), ())
    return tuple(copy.deepcopy(rule) for rule in rules)


def get_social_quest_offer_rule_by_npc(npc_id):
    """Compatibility adapter returning the first ordered NPC offer, if any."""
    rules = get_social_quest_offer_rules_by_npc(npc_id)
    return rules[0] if rules else None


def get_social_quest_offer_rule_by_quest_id(quest_id):
    """Return an isolated offer rule copy for a quest id, or None."""
    return _copy_rule(_RULES_BY_QUEST_ID.get(str(quest_id or "")))
