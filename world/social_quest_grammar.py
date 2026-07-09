"""Deterministic grammar for Social Web-backed quest offers.

Incident seeds describe what happened. Quest archetypes describe the playable
structure. A future LLM renderer may phrase the offer, but it receives only the
bounded context assembled here and never owns durable truth or quest mutation.
"""

from __future__ import annotations

import copy

from world.social_taxonomy import normalize_tags


MAX_CONTEXT_ITEMS = 5
MAX_CONTEXT_TEXT_CHARS = 320
LIVE_QUEST_OBJECTIVE_TYPES = {"kill", "collect", "investigate", "deliver", "talk_to"}


class SocialQuestGrammarError(ValueError):
    """Raised when Social Web quest grammar data cannot be compiled."""


INCIDENT_CATEGORIES = {
    "crime",
    "coercion",
    "political_intrigue",
    "trade_dispute",
    "personal_debt",
    "public_need",
    "faction_pressure",
}

AGENDA_METHODS = {
    "conceal_truth",
    "extract_leverage",
    "frame_target",
    "intimidate",
    "investigate",
    "mediate",
    "protect_reputation",
    "recover_property",
    "seek_justice",
    "silence_witness",
    "trade_favor",
}

SOCIAL_SCOPES = {
    "npc",
    "household",
    "shop",
    "workplace",
    "settlement",
    "zone",
    "route",
    "guild",
    "faction",
    "institution",
    "caravan",
    "archive",
}

OBJECTIVE_TYPES = {
    "ask_npc",
    "choose_side",
    "confront_actor",
    "deliver_item",
    "inspect_evidence",
    "interview_actor",
    "mediate_dispute",
    "protect_target",
    "recover_evidence",
    "report_to_authority",
}

SOCIAL_EFFECT_TYPES = {
    "access_change",
    "relationship_delta",
    "social_claim",
    "social_fact",
    "quest_flag",
    "world_state_hint",
}

LLM_FORBIDDEN_ACTIONS = [
    "create durable facts",
    "mutate quests",
    "mutate inventory",
    "mutate standing",
    "decide who knows a fact",
    "invent NPC relationships",
    "invent locations or factions",
    "reveal hidden lore",
]


INCIDENT_SEEDS = {
    "market_square_robbery": {
        "title": "Market Square Robbery",
        "category": "crime",
        "premise": (
            "A vendor who previously discussed Market Square robberies with the "
            "player has been robbed, and the thief left torn cloth behind."
        ),
        "tags": ["theft", "market", "evidence", "personal_harm"],
        "world_scopes": ["shop", "settlement", "route"],
        "roles": {
            "victim": "shopkeeper harmed by the incident",
            "suspect": "unknown thief or fence",
            "evidence_holder": "clothier or maker who can identify torn fabric",
            "authority": "local Warden or market adjudicator",
        },
        "agenda": {
            "type": "seek_redress",
            "methods": ["investigate", "recover_property", "seek_justice"],
            "pressure": "The victim is asking because prior trust makes the risk personal.",
        },
        "evidence_types": [
            "torn_fabric",
            "counter_damage",
            "prior_conversation",
        ],
        "social_inputs": [
            "prior_interactions",
            "known_social_facts",
            "known_social_claims",
            "contact_trace",
        ],
        "compatible_archetypes": ["trace_evidence_chain"],
        "llm_brief": (
            "Phrase a personal request that remembers the earlier robbery "
            "conversation, names the fresh harm, and points to the clothier "
            "because the deterministic outline selected that route."
        ),
    },
    "council_blackmail_ledger": {
        "title": "Council Blackmail Ledger",
        "category": "political_intrigue",
        "premise": (
            "A political broker has evidence that could expose a council ally, "
            "but the evidence may be true, distorted, or strategically timed."
        ),
        "tags": ["blackmail", "council", "secret", "leverage", "faction"],
        "world_scopes": ["institution", "faction", "settlement", "archive"],
        "roles": {
            "petitioner": "person asking the player to intervene",
            "target": "official or ally vulnerable to the ledger",
            "leverage_holder": "broker holding the damaging record",
            "mediator": "neutral or respected intermediary",
            "authority": "institution that can record a formal finding",
        },
        "agenda": {
            "type": "weaponize_secret",
            "methods": ["extract_leverage", "conceal_truth", "trade_favor"],
            "pressure": "No side is clean; the player must decide what truth deserves daylight.",
        },
        "evidence_types": [
            "ledger_fragment",
            "private_meeting_trace",
            "biased_testimony",
        ],
        "social_inputs": [
            "known_social_claims",
            "faction_ties",
            "contact_trace",
        ],
        "compatible_archetypes": ["broker_compromise"],
        "llm_brief": (
            "Phrase intrigue as social leverage, not cosmic morality. Keep the "
            "offer grounded in known claims and the selected compromise route."
        ),
    },
    "witness_intimidation": {
        "title": "Witness Intimidation",
        "category": "coercion",
        "premise": (
            "A witness who could clarify a public accusation is being pressured "
            "to stay silent before the truth reaches an authority."
        ),
        "tags": ["witness", "threat", "coercion", "false_claim", "evidence"],
        "world_scopes": ["npc", "household", "settlement", "institution"],
        "roles": {
            "witness": "person with direct knowledge of the contested event",
            "coercer": "actor using fear or status to control testimony",
            "target": "person harmed by the accusation or silence",
            "authority": "node able to protect or record testimony",
            "speaker": "originator of the public accusation",
        },
        "agenda": {
            "type": "silence_threat",
            "methods": ["intimidate", "silence_witness", "protect_reputation"],
            "pressure": "The request exists because Social Web propagation has consequences.",
        },
        "evidence_types": [
            "threat_message",
            "direct_testimony",
            "contradictory_claim",
        ],
        "social_inputs": [
            "known_social_claims",
            "known_social_facts",
            "contact_trace",
        ],
        "compatible_archetypes": ["protect_witness", "expose_false_claim"],
        "llm_brief": (
            "Phrase the stakes around fear, testimony, and who can safely know "
            "the truth next. Do not turn coercion into an abstract alignment label."
        ),
    },
}


QUEST_ARCHETYPES = {
    "trace_evidence_chain": {
        "title": "Trace Evidence Chain",
        "purpose": "Turn a remembered incident into an evidence-led investigation.",
        "tags": ["investigation", "evidence", "personal_request"],
        "compatible_categories": ["crime", "coercion"],
        "compatible_tags": ["evidence", "theft", "market", "witness"],
        "required_roles": ["victim", "evidence_holder"],
        "optional_roles": ["authority", "suspect"],
        "objective_steps": [
            {
                "id": "interview_victim",
                "type": "interview_actor",
                "engine_type": "talk_to",
                "role": "victim",
                "summary": "Recover the personal account and current harm.",
            },
            {
                "id": "inspect_scene",
                "type": "inspect_evidence",
                "engine_type": "investigate",
                "role": "victim",
                "summary": "Inspect the object, damage, or trace left behind.",
            },
            {
                "id": "ask_evidence_holder",
                "type": "ask_npc",
                "engine_type": "talk_to",
                "role": "evidence_holder",
                "summary": "Ask the specialist who can identify the evidence origin.",
            },
            {
                "id": "report_authority",
                "type": "report_to_authority",
                "engine_type": "talk_to",
                "role": "authority",
                "summary": "Bring the result to a node that can act on it.",
                "optional": True,
            },
        ],
        "social_effects": [
            {
                "type": "social_fact",
                "event_type": "accepted_investigation",
                "tags": ["trusted", "helped_victim", "evidence_chain"],
            },
            {
                "type": "social_claim",
                "claim_type": "testimony",
                "tags": ["witnessed", "market"],
            },
        ],
        "llm_slots": [
            "prior_interactions",
            "victim_request",
            "evidence_detail",
            "handoff_line",
        ],
        "llm_brief": (
            "Render a specific request around the selected evidence chain. The "
            "objectives, roles, and consequences are fixed by the game."
        ),
    },
    "broker_compromise": {
        "title": "Broker Compromise",
        "purpose": "Let social leverage become a playable political choice.",
        "tags": ["intrigue", "leverage", "mediation"],
        "compatible_categories": ["political_intrigue"],
        "compatible_tags": ["blackmail", "secret", "leverage", "faction"],
        "required_roles": ["petitioner", "target", "leverage_holder", "mediator"],
        "optional_roles": ["authority"],
        "objective_steps": [
            {
                "id": "interview_petitioner",
                "type": "interview_actor",
                "engine_type": "talk_to",
                "role": "petitioner",
                "summary": "Learn why this person wants intervention now.",
            },
            {
                "id": "question_leverage_holder",
                "type": "ask_npc",
                "engine_type": "talk_to",
                "role": "leverage_holder",
                "summary": "Find out what the broker truly knows or wants.",
            },
            {
                "id": "meet_mediator",
                "type": "mediate_dispute",
                "engine_type": "talk_to",
                "role": "mediator",
                "summary": "Create a route that does not rely on omniscient truth.",
            },
            {
                "id": "choose_target_outcome",
                "type": "choose_side",
                "engine_type": "talk_to",
                "role": "target",
                "summary": "Decide whether to expose, contain, or redirect the leverage.",
            },
        ],
        "social_effects": [
            {
                "type": "social_claim",
                "claim_type": "rumor",
                "tags": ["blackmail", "political_intrigue"],
            },
            {
                "type": "relationship_delta",
                "tags": ["owed_favor", "faction_pressure"],
            },
        ],
        "llm_slots": [
            "prior_interactions",
            "known_claim",
            "leverage_detail",
            "choice_pressure",
        ],
        "llm_brief": (
            "Render the offer as pressure among people with partial knowledge. "
            "Do not declare who is morally pure."
        ),
    },
    "protect_witness": {
        "title": "Protect Witness",
        "purpose": "Turn intimidation into protection, testimony, and propagation choices.",
        "tags": ["protection", "testimony", "coercion"],
        "compatible_categories": ["coercion", "crime", "political_intrigue"],
        "compatible_tags": ["witness", "threat", "coercion", "false_claim"],
        "required_roles": ["witness", "coercer", "authority"],
        "optional_roles": ["target", "speaker"],
        "objective_steps": [
            {
                "id": "interview_witness",
                "type": "interview_actor",
                "engine_type": "talk_to",
                "role": "witness",
                "summary": "Learn what the witness knows and what they fear.",
            },
            {
                "id": "secure_witness_route",
                "type": "protect_target",
                "engine_type": "investigate",
                "role": "witness",
                "summary": "Create a safe route for testimony or escape.",
            },
            {
                "id": "confront_coercer",
                "type": "confront_actor",
                "engine_type": "talk_to",
                "role": "coercer",
                "summary": "Stop or expose the pressure source.",
            },
            {
                "id": "record_testimony",
                "type": "report_to_authority",
                "engine_type": "talk_to",
                "role": "authority",
                "summary": "Record the testimony where it can travel credibly.",
            },
        ],
        "social_effects": [
            {
                "type": "social_fact",
                "event_type": "protected_witness",
                "tags": ["protection", "testimony", "coercion"],
            },
            {
                "type": "access_change",
                "tags": ["witness_trust", "authority_notice"],
            },
        ],
        "llm_slots": [
            "prior_interactions",
            "witness_fear",
            "threat_detail",
            "safe_authority_route",
        ],
        "llm_brief": (
            "Render the offer around safety and testimony. Keep intimidation "
            "grounded in the supplied claim and evidence context."
        ),
    },
    "expose_false_claim": {
        "title": "Expose False Claim",
        "purpose": "Let players challenge a rumor or lie through Social Web evidence.",
        "tags": ["reputation_repair", "testimony", "claim_challenge"],
        "compatible_categories": ["coercion", "crime", "political_intrigue"],
        "compatible_tags": ["false_claim", "witness", "secret", "evidence"],
        "required_roles": ["speaker", "target", "witness"],
        "optional_roles": ["authority", "coercer"],
        "objective_steps": [
            {
                "id": "question_speaker",
                "type": "ask_npc",
                "engine_type": "talk_to",
                "role": "speaker",
                "summary": "Identify what claim is spreading and why.",
            },
            {
                "id": "interview_witness",
                "type": "interview_actor",
                "engine_type": "talk_to",
                "role": "witness",
                "summary": "Find a supported contradiction or missing context.",
            },
            {
                "id": "recover_corroboration",
                "type": "recover_evidence",
                "engine_type": "collect",
                "role": "target",
                "summary": "Recover corroborating evidence before correction spreads.",
            },
            {
                "id": "anchor_correction",
                "type": "report_to_authority",
                "engine_type": "talk_to",
                "role": "authority",
                "summary": "Anchor the correction in a node people plausibly trust.",
                "optional": True,
            },
        ],
        "social_effects": [
            {
                "type": "social_claim",
                "claim_type": "testimony",
                "tags": ["corrective_testimony", "reputation_repair"],
            },
            {
                "type": "quest_flag",
                "tags": ["claim_challenged"],
            },
        ],
        "llm_slots": [
            "prior_interactions",
            "known_claim",
            "contradiction",
            "correction_route",
        ],
        "llm_brief": (
            "Render the offer as a correction path, not automatic exoneration. "
            "The Social Web decides what evidence is known."
        ),
    },
}


def _safe_text(value, *, max_chars=MAX_CONTEXT_TEXT_CHARS):
    if value is None or isinstance(value, bool):
        return ""
    text = str(value).strip()
    if len(text) <= max_chars:
        return text
    return f"{text[: max_chars - 1].rstrip()}..."


def _copy_list(values):
    return copy.deepcopy(list(values or []))


def _string_list_errors(field_name, values, *, allowed=None, require_non_empty=True):
    errors = []
    if not isinstance(values, list):
        return [f"{field_name} must be a list"]
    if require_non_empty and not values:
        errors.append(f"{field_name} must not be empty")
    for index, value in enumerate(values):
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field_name}[{index}] must be a non-empty string")
            continue
        if allowed and value not in allowed:
            errors.append(f"{field_name}[{index}] unsupported value: {value}")
    return errors


def _validate_roles(seed_id, roles):
    if not isinstance(roles, dict) or not roles:
        return [f"{seed_id}.roles must be a non-empty dict"]
    errors = []
    for role, description in roles.items():
        if not isinstance(role, str) or not role.strip():
            errors.append(f"{seed_id}.roles contains an empty role key")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{seed_id}.roles.{role} must describe the role")
    return errors


def _validate_agenda(seed_id, agenda):
    if not isinstance(agenda, dict):
        return [f"{seed_id}.agenda must be a dict"]
    errors = []
    for field_name in ("type", "pressure"):
        if not isinstance(agenda.get(field_name), str) or not agenda[field_name].strip():
            errors.append(f"{seed_id}.agenda.{field_name} must be a non-empty string")
    errors.extend(
        _string_list_errors(
            f"{seed_id}.agenda.methods",
            agenda.get("methods"),
            allowed=AGENDA_METHODS,
        )
    )
    return errors


def _validate_incident_seed(seed_id, seed):
    errors = []
    if not isinstance(seed, dict):
        return [f"{seed_id} must be a dict"]
    for field_name in ("title", "category", "premise", "llm_brief"):
        if not isinstance(seed.get(field_name), str) or not seed[field_name].strip():
            errors.append(f"{seed_id}.{field_name} must be a non-empty string")
    if seed.get("category") not in INCIDENT_CATEGORIES:
        errors.append(f"{seed_id}.category unsupported value: {seed.get('category')}")
    errors.extend(_string_list_errors(f"{seed_id}.tags", seed.get("tags")))
    errors.extend(
        _string_list_errors(
            f"{seed_id}.world_scopes",
            seed.get("world_scopes"),
            allowed=SOCIAL_SCOPES,
        )
    )
    errors.extend(_validate_roles(seed_id, seed.get("roles")))
    errors.extend(_validate_agenda(seed_id, seed.get("agenda")))
    errors.extend(_string_list_errors(f"{seed_id}.evidence_types", seed.get("evidence_types")))
    errors.extend(_string_list_errors(f"{seed_id}.social_inputs", seed.get("social_inputs")))
    errors.extend(
        _string_list_errors(
            f"{seed_id}.compatible_archetypes",
            seed.get("compatible_archetypes"),
        )
    )
    return errors


def _validate_objective_steps(archetype_id, archetype):
    steps = archetype.get("objective_steps")
    if not isinstance(steps, list) or not steps:
        return [f"{archetype_id}.objective_steps must be a non-empty list"]
    known_roles = set(archetype.get("required_roles") or [])
    known_roles.update(archetype.get("optional_roles") or [])
    errors = []
    seen_step_ids = set()
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"{archetype_id}.objective_steps[{index}] must be a dict")
            continue
        step_id = step.get("id")
        if not isinstance(step_id, str) or not step_id.strip():
            errors.append(f"{archetype_id}.objective_steps[{index}].id is required")
        elif step_id in seen_step_ids:
            errors.append(f"{archetype_id}.objective_steps[{index}].id is duplicated")
        else:
            seen_step_ids.add(step_id)
        step_type = step.get("type")
        if step_type not in OBJECTIVE_TYPES:
            errors.append(
                f"{archetype_id}.objective_steps[{index}].type unsupported value: {step_type}"
            )
        engine_type = step.get("engine_type")
        if engine_type not in LIVE_QUEST_OBJECTIVE_TYPES:
            errors.append(
                f"{archetype_id}.objective_steps[{index}].engine_type unsupported "
                f"value: {engine_type}"
            )
        role = step.get("role")
        if role and role not in known_roles:
            errors.append(
                f"{archetype_id}.objective_steps[{index}].role unknown role: {role}"
            )
        if not isinstance(step.get("summary"), str) or not step["summary"].strip():
            errors.append(f"{archetype_id}.objective_steps[{index}].summary is required")
    return errors


def _validate_social_effects(archetype_id, effects):
    if not isinstance(effects, list) or not effects:
        return [f"{archetype_id}.social_effects must be a non-empty list"]
    errors = []
    for index, effect in enumerate(effects):
        if not isinstance(effect, dict):
            errors.append(f"{archetype_id}.social_effects[{index}] must be a dict")
            continue
        effect_type = effect.get("type")
        if effect_type not in SOCIAL_EFFECT_TYPES:
            errors.append(
                f"{archetype_id}.social_effects[{index}].type unsupported value: {effect_type}"
            )
        if effect_type == "social_claim" and effect.get("claim_type") not in {
            "report",
            "rumor",
            "testimony",
            "warning",
            "boast",
            "denial",
            "confession",
        }:
            errors.append(f"{archetype_id}.social_effects[{index}].claim_type is invalid")
        if effect_type == "social_fact" and not effect.get("event_type"):
            errors.append(f"{archetype_id}.social_effects[{index}].event_type is required")
        errors.extend(
            _string_list_errors(
                f"{archetype_id}.social_effects[{index}].tags",
                effect.get("tags"),
            )
        )
    return errors


def _validate_quest_archetype(archetype_id, archetype):
    errors = []
    if not isinstance(archetype, dict):
        return [f"{archetype_id} must be a dict"]
    for field_name in ("title", "purpose", "llm_brief"):
        if not isinstance(archetype.get(field_name), str) or not archetype[field_name].strip():
            errors.append(f"{archetype_id}.{field_name} must be a non-empty string")
    errors.extend(_string_list_errors(f"{archetype_id}.tags", archetype.get("tags")))
    errors.extend(
        _string_list_errors(
            f"{archetype_id}.compatible_categories",
            archetype.get("compatible_categories"),
            allowed=INCIDENT_CATEGORIES,
        )
    )
    errors.extend(_string_list_errors(
        f"{archetype_id}.compatible_tags",
        archetype.get("compatible_tags"),
    ))
    errors.extend(_string_list_errors(
        f"{archetype_id}.required_roles",
        archetype.get("required_roles"),
    ))
    errors.extend(_string_list_errors(
        f"{archetype_id}.optional_roles",
        archetype.get("optional_roles"),
        require_non_empty=False,
    ))
    errors.extend(_validate_objective_steps(archetype_id, archetype))
    errors.extend(_validate_social_effects(archetype_id, archetype.get("social_effects")))
    errors.extend(_string_list_errors(f"{archetype_id}.llm_slots", archetype.get("llm_slots")))
    if "prior_interactions" not in set(archetype.get("llm_slots") or []):
        errors.append(f"{archetype_id}.llm_slots must include prior_interactions")
    return errors


def _pair_errors(seed_id, seed, archetype_id, archetype):
    errors = []
    if archetype_id not in seed.get("compatible_archetypes", []):
        errors.append(f"{seed_id} does not list compatible archetype {archetype_id}")
    seed_category = seed.get("category")
    if seed_category not in set(archetype.get("compatible_categories") or []):
        errors.append(f"{archetype_id} does not support category {seed_category}")
    seed_tags = set(normalize_tags(seed.get("tags") or []))
    archetype_tags = set(normalize_tags(archetype.get("compatible_tags") or []))
    if seed_tags and archetype_tags and not seed_tags.intersection(archetype_tags):
        errors.append(f"{archetype_id} has no compatible tag overlap with {seed_id}")
    seed_roles = set(seed.get("roles") or {})
    for role in archetype.get("required_roles") or []:
        if role not in seed_roles:
            errors.append(f"{seed_id} missing required role {role} for {archetype_id}")
    return errors


def validate_social_quest_grammar():
    """Return validation errors for all registered incident seeds and archetypes."""
    errors = []
    for seed_id, seed in INCIDENT_SEEDS.items():
        errors.extend(_validate_incident_seed(seed_id, seed))
    for archetype_id, archetype in QUEST_ARCHETYPES.items():
        errors.extend(_validate_quest_archetype(archetype_id, archetype))
    for seed_id, seed in INCIDENT_SEEDS.items():
        for archetype_id in seed.get("compatible_archetypes", []):
            archetype = QUEST_ARCHETYPES.get(archetype_id)
            if not archetype:
                errors.append(f"{seed_id}.compatible_archetypes unknown value: {archetype_id}")
                continue
            errors.extend(_pair_errors(seed_id, seed, archetype_id, archetype))
    return errors


def get_incident_seed(seed_id):
    """Return a defensive copy of a registered incident seed, or None."""
    seed = INCIDENT_SEEDS.get(seed_id)
    return copy.deepcopy(seed) if seed else None


def get_quest_archetype(archetype_id):
    """Return a defensive copy of a registered quest archetype, or None."""
    archetype = QUEST_ARCHETYPES.get(archetype_id)
    return copy.deepcopy(archetype) if archetype else None


def compatible_archetype_ids(seed_id):
    """Return archetype ids that the seed explicitly supports."""
    seed = INCIDENT_SEEDS.get(seed_id)
    if not seed:
        return []
    return list(seed.get("compatible_archetypes") or [])


def _actor_payload(role, authored_description, supplied):
    payload = {
        "role": role,
        "authored_description": _safe_text(authored_description),
    }
    if isinstance(supplied, str):
        payload["display_name"] = _safe_text(supplied)
        return payload
    if not isinstance(supplied, dict):
        return payload
    for key in ("node_key", "display_name", "zone_id", "settlement_id", "faction_id"):
        value = _safe_text(supplied.get(key))
        if value:
            payload[key] = value
    return payload


def _actors_packet(seed, actors):
    actors = actors or {}
    return {
        role: _actor_payload(role, description, actors.get(role))
        for role, description in (seed.get("roles") or {}).items()
    }


def _bounded_interactions(prior_interactions):
    if not prior_interactions:
        return []
    if isinstance(prior_interactions, (str, dict)):
        prior_interactions = [prior_interactions]
    interactions = []
    for item in prior_interactions[:MAX_CONTEXT_ITEMS]:
        if isinstance(item, str):
            interactions.append({"summary": _safe_text(item)})
            continue
        if not isinstance(item, dict):
            continue
        entry = {}
        for key in ("topic", "summary", "fact_key", "claim_key", "source", "tone"):
            value = _safe_text(item.get(key))
            if value:
                entry[key] = value
        if entry:
            interactions.append(entry)
    return interactions


def _node_packet(node):
    if not isinstance(node, dict):
        return {}
    packet = {}
    for key in ("node_key", "node_type", "display_name", "zone_id", "settlement_id", "faction_id"):
        value = _safe_text(node.get(key))
        if value:
            packet[key] = value
    return packet


def _bounded_fact(fact):
    if not isinstance(fact, dict):
        return None
    packet = {}
    for key in ("fact_key", "event_type", "summary", "visibility", "channel"):
        value = _safe_text(fact.get(key))
        if value:
            packet[key] = value
    if isinstance(fact.get("confidence"), (int, float)) and not isinstance(
        fact.get("confidence"), bool
    ):
        packet["confidence"] = fact["confidence"]
    tags = normalize_tags(fact.get("tags") or [])
    if tags:
        packet["tags"] = tags
    return packet or None


def _bounded_trace(trace):
    if not isinstance(trace, dict):
        return None
    packet = {}
    for key in ("from_node", "to_node", "edge_key", "edge_type", "summary"):
        value = _safe_text(trace.get(key))
        if value:
            packet[key] = value
    return packet or None


def _bounded_claim(claim):
    if not isinstance(claim, dict):
        return None
    packet = {}
    for key in ("claim_key", "claim_type", "summary", "status", "channel"):
        value = _safe_text(claim.get(key))
        if value:
            packet[key] = value
    if isinstance(claim.get("confidence"), (int, float)) and not isinstance(
        claim.get("confidence"), bool
    ):
        packet["confidence"] = claim["confidence"]
    speaker = _node_packet(claim.get("speaker") or {})
    if speaker:
        packet["speaker"] = speaker
    traces = [
        bounded
        for bounded in (_bounded_trace(trace) for trace in (claim.get("trace") or [])[:MAX_CONTEXT_ITEMS])
        if bounded
    ]
    if traces:
        packet["trace"] = traces
    return packet or None


def _bounded_social_context(social_context):
    if not isinstance(social_context, dict):
        social_context = {}
    facts = [
        bounded
        for bounded in (
            _bounded_fact(fact)
            for fact in (social_context.get("facts") or [])[:MAX_CONTEXT_ITEMS]
        )
        if bounded
    ]
    claims = [
        bounded
        for bounded in (
            _bounded_claim(claim)
            for claim in (social_context.get("claims") or [])[:MAX_CONTEXT_ITEMS]
        )
        if bounded
    ]
    return {
        "viewer": _node_packet(social_context.get("viewer") or {}),
        "subject": _node_packet(social_context.get("subject") or {}),
        "purpose": _safe_text(social_context.get("purpose") or "quest_offer"),
        "facts": facts,
        "claims": claims,
    }


def _deterministic_outline(archetype):
    return {
        "required_roles": _copy_list(archetype.get("required_roles")),
        "optional_roles": _copy_list(archetype.get("optional_roles")),
        "objective_steps": copy.deepcopy(archetype.get("objective_steps") or []),
        "social_effects": copy.deepcopy(archetype.get("social_effects") or []),
    }


def _llm_context(seed, archetype, prior_interactions, social_context, outline):
    return {
        "role": "optional_voice_renderer",
        "provider_call_allowed": False,
        "allowed_task": (
            "Phrase an NPC-facing quest offer from deterministic incident, "
            "objective, evidence, and social-memory context."
        ),
        "forbidden_actions": list(LLM_FORBIDDEN_ACTIONS),
        "required_output_schema": {
            "speech": "string",
            "tone_tags": "list[string]",
        },
        "prompt_inputs": {
            "incident_brief": _safe_text(seed.get("llm_brief")),
            "archetype_brief": _safe_text(archetype.get("llm_brief")),
            "agenda": copy.deepcopy(seed.get("agenda") or {}),
            "evidence_types": _copy_list(seed.get("evidence_types")),
            "prior_interactions": copy.deepcopy(prior_interactions),
            "social_memory": {
                "facts": copy.deepcopy(social_context["facts"]),
                "claims": copy.deepcopy(social_context["claims"]),
            },
            "objective_steps": copy.deepcopy(outline["objective_steps"]),
            "llm_slots": _copy_list(archetype.get("llm_slots")),
        },
    }


def build_social_quest_context(
    seed_id,
    archetype_id,
    *,
    prior_interactions=None,
    actors=None,
    social_context=None,
):
    """Compile a deterministic social quest context packet.

    The result is suitable for deterministic quest logic and for a later
    provider-neutral voice renderer. This function performs no database work and
    never calls an external provider.
    """
    seed = get_incident_seed(seed_id)
    if not seed:
        raise SocialQuestGrammarError(f"Unknown incident seed: {seed_id}")
    archetype = get_quest_archetype(archetype_id)
    if not archetype:
        raise SocialQuestGrammarError(f"Unknown quest archetype: {archetype_id}")

    pair_errors = _pair_errors(seed_id, seed, archetype_id, archetype)
    if pair_errors:
        raise SocialQuestGrammarError(
            f"Incident {seed_id} is not compatible with {archetype_id}: "
            + "; ".join(pair_errors)
        )

    bounded_interactions = _bounded_interactions(prior_interactions)
    bounded_social_context = _bounded_social_context(social_context)
    outline = _deterministic_outline(archetype)

    return {
        "purpose": "social_quest_offer",
        "incident": {
            "id": seed_id,
            "title": seed["title"],
            "category": seed["category"],
            "premise": seed["premise"],
            "tags": normalize_tags(seed.get("tags") or []),
            "world_scopes": _copy_list(seed.get("world_scopes")),
            "evidence_types": _copy_list(seed.get("evidence_types")),
            "roles": copy.deepcopy(seed.get("roles") or {}),
            "agenda": copy.deepcopy(seed.get("agenda") or {}),
        },
        "archetype": {
            "id": archetype_id,
            "title": archetype["title"],
            "purpose": archetype["purpose"],
            "tags": normalize_tags(archetype.get("tags") or []),
            "llm_slots": _copy_list(archetype.get("llm_slots")),
        },
        "actors": _actors_packet(seed, actors),
        "social_context": bounded_social_context,
        "deterministic_outline": outline,
        "llm_context": _llm_context(
            seed,
            archetype,
            bounded_interactions,
            bounded_social_context,
            outline,
        ),
    }


def _grounding_sources(context):
    sources = set()
    if context["llm_context"]["prompt_inputs"].get("prior_interactions"):
        sources.add("prior_interactions")
    social_context = context.get("social_context") or {}
    if social_context.get("facts"):
        sources.add("known_social_facts")
    claims = social_context.get("claims") or []
    if claims:
        sources.add("known_social_claims")
    if any(claim.get("trace") for claim in claims if isinstance(claim, dict)):
        sources.add("contact_trace")
    return sources


def _require_social_grounding(seed, context):
    expected_inputs = set(seed.get("social_inputs") or [])
    relevant_inputs = expected_inputs.intersection(
        {
            "prior_interactions",
            "known_social_facts",
            "known_social_claims",
            "contact_trace",
        }
    )
    if not relevant_inputs:
        return
    if not _grounding_sources(context).intersection(relevant_inputs):
        raise SocialQuestGrammarError(
            "social grounding required: provide a prior interaction, Social Web "
            "fact, Social Web claim, or contact trace before compiling this offer"
        )


def _target_for_step(step, objective_targets):
    objective_targets = objective_targets or {}
    step_id = step.get("id")
    role = step.get("role")
    if step_id in objective_targets:
        return _safe_text(objective_targets[step_id])
    if role in objective_targets:
        return _safe_text(objective_targets[role])
    return ""


def _compile_live_objectives(archetype, objective_targets):
    objectives = []
    for step in archetype.get("objective_steps") or []:
        engine_type = step.get("engine_type")
        if engine_type not in LIVE_QUEST_OBJECTIVE_TYPES:
            raise SocialQuestGrammarError(
                f"objective step {step.get('id') or step.get('type')} has no "
                "supported quest_engine mapping"
            )

        target = _target_for_step(step, objective_targets)
        if not target:
            if step.get("optional"):
                continue
            raise SocialQuestGrammarError(
                f"objective target missing for step {step.get('id') or step.get('type')}"
            )

        objective = {
            "type": engine_type,
            "target": target,
            "count": int(step.get("count", 1) or 1),
            "description": _safe_text(step.get("summary")),
            "social_objective_type": step.get("type"),
            "social_role": step.get("role", ""),
        }
        if engine_type == "deliver":
            item_tag = _safe_text(
                objective_targets.get(f"{step.get('id')}.item_tag")
                or objective_targets.get(f"{step.get('role')}.item_tag")
                or objective_targets.get("item_tag")
                or target
            )
            objective["item_tag"] = item_tag
        objectives.append(objective)
    if not objectives:
        raise SocialQuestGrammarError("compiled quest must include at least one objective")
    return objectives


def _node_identifier(value):
    value = _safe_text(value)
    if ":" in value:
        return value.split(":", 1)[1]
    return value


def _actor_for_identifier(context, identifier):
    identifier = _node_identifier(identifier)
    if not identifier:
        return {}
    for actor in (context.get("actors") or {}).values():
        node_key = _safe_text(actor.get("node_key"))
        if _node_identifier(node_key) == identifier:
            return actor
    return {}


def _node_def(ref, node_type, identifier, actor=None):
    actor = actor or {}
    node = {
        "ref": ref,
        "node_type": node_type,
        "identifier": _node_identifier(identifier),
        "display_name": _safe_text(actor.get("display_name") or identifier),
    }
    for field_name in ("zone_id", "settlement_id", "faction_id"):
        value = _safe_text(actor.get(field_name))
        if value:
            node[field_name] = value
    return node


def _default_social_reward(context, *, quest_id, quest_giver):
    incident = context["incident"]
    archetype = context["archetype"]
    quest_giver_actor = _actor_for_identifier(context, quest_giver)
    reward_tags = normalize_tags(
        ["social_quest", incident["category"]]
        + incident.get("tags", [])
        + archetype.get("tags", [])
    )
    title = incident.get("title") or quest_id
    summary = f"The player completed the social quest '{title}'."
    speaker_id = _node_identifier(quest_giver)

    return {
        "action_type": "record_social_event",
        "nodes": [
            {
                "ref": "player",
                "node_type": "player",
                "identifier_template": "{character_id}",
                "display_name_template": "{character_key}",
            },
            _node_def("quest_giver", "npc", speaker_id, quest_giver_actor),
        ],
        "fact": {
            "fact_key_template": f"fact:{{character_id}}:{quest_id}:completed",
            "subject": "player",
            "actor": "player",
            "scope": "quest_giver",
            "event_type": "social_quest_completed",
            "summary": summary,
            "tags": reward_tags,
            "visibility": "local",
            "evidence": {
                "quest_id": quest_id,
                "incident_seed": incident["id"],
                "quest_archetype": archetype["id"],
                "source": "social_quest_grammar",
            },
        },
        "claim": {
            "claim_key_template": f"claim:{speaker_id}:{{character_id}}:{quest_id}:completed",
            "speaker": "quest_giver",
            "subject": "player",
            "claim_type": "report",
            "summary": f"{speaker_id} reports that the player followed through on {title}.",
            "status": "supported",
            "confidence": 0.8,
            "bias_tags": reward_tags,
        },
        "knowledge": [
            {
                "node": "quest_giver",
                "claim_key_template": f"claim:{speaker_id}:{{character_id}}:{quest_id}:completed",
                "channel": "direct_witness",
                "confidence": 0.8,
                "spreading": True,
            }
        ],
    }


def compile_quest_spec(
    seed_id,
    archetype_id,
    *,
    quest_id=None,
    quest_giver=None,
    name=None,
    description=None,
    actors=None,
    objective_targets=None,
    prior_interactions=None,
    social_context=None,
    extra_rewards=None,
    prerequisite_quests=None,
    one_chance=False,
    can_share=False,
    share_radius=1,
    share_cap=6,
    require_social_grounding=True,
):
    """Compile a Social Web quest grammar pair into a normal quest spec dict."""
    quest_id = _safe_text(quest_id)
    quest_giver = _safe_text(quest_giver)
    if not quest_id:
        raise SocialQuestGrammarError("quest_id is required")
    if not quest_giver:
        raise SocialQuestGrammarError("quest_giver is required")

    seed = get_incident_seed(seed_id)
    if not seed:
        raise SocialQuestGrammarError(f"Unknown incident seed: {seed_id}")
    archetype = get_quest_archetype(archetype_id)
    if not archetype:
        raise SocialQuestGrammarError(f"Unknown quest archetype: {archetype_id}")

    context = build_social_quest_context(
        seed_id,
        archetype_id,
        prior_interactions=prior_interactions,
        actors=actors,
        social_context=social_context,
    )
    if require_social_grounding:
        _require_social_grounding(seed, context)

    objectives = _compile_live_objectives(archetype, objective_targets or {})
    rewards = [_default_social_reward(context, quest_id=quest_id, quest_giver=quest_giver)]
    rewards.extend(copy.deepcopy(extra_rewards or []))

    return {
        "quest_id": quest_id,
        "name": _safe_text(name) or context["incident"]["title"],
        "description": _safe_text(description) or context["incident"]["premise"],
        "quest_type": "social",
        "quest_giver": quest_giver,
        "objectives": objectives,
        "rewards": rewards,
        "prerequisite_quests": _copy_list(prerequisite_quests),
        "one_chance": bool(one_chance),
        "can_share": bool(can_share),
        "share_radius": int(share_radius),
        "share_cap": int(share_cap),
        "incident_seed": seed_id,
        "quest_archetype": archetype_id,
        "social_quest_context": context,
    }
