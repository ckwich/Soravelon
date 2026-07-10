"""Compile authored Social Web effects into deterministic runtime actions."""

from __future__ import annotations

import hashlib
import json

from world.social_taxonomy import CLAIM_TYPES, normalize_tags


class SocialEffectCompilationError(ValueError):
    """A declared social effect has no faithful runtime representation."""


_EXECUTABLE_EFFECT_TYPES = {
    "access_change",
    "social_claim",
    "social_fact",
}


def access_grant_key(quest_id, tag):
    """Build the stable named grant produced by one access-change tag."""
    return f"social:{quest_id}:access:{tag}"


def _required_text(effect, field_name):
    value = effect.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise SocialEffectCompilationError(
            f"social effect {effect.get('type')!r} requires {field_name}"
        )
    return value.strip()


def _effect_tags(effect):
    raw_tags = effect.get("tags")
    if not isinstance(raw_tags, list) or not raw_tags:
        raise SocialEffectCompilationError(
            f"social effect {effect.get('type')!r} requires non-empty tags"
        )
    if any(not isinstance(tag, str) or not tag.strip() for tag in raw_tags):
        raise SocialEffectCompilationError(
            f"social effect {effect.get('type')!r} tags must be non-empty strings"
        )
    tags = normalize_tags(raw_tags)
    if not tags:
        raise SocialEffectCompilationError(
            f"social effect {effect.get('type')!r} has no usable tags"
        )
    return tags


def _node_from_key(ref, node_key, actor):
    if not isinstance(node_key, str) or ":" not in node_key:
        raise SocialEffectCompilationError(
            f"social actor {ref!r} requires a typed node_key"
        )
    node_type, identifier = node_key.split(":", 1)
    if not node_type or not identifier:
        raise SocialEffectCompilationError(
            f"social actor {ref!r} requires a valid node_key"
        )
    node = {
        "ref": ref,
        "node_type": node_type,
        "identifier": identifier,
        "display_name": str(actor.get("display_name") or identifier),
    }
    for field_name in ("zone_id", "settlement_id", "faction_id"):
        value = actor.get(field_name)
        if isinstance(value, str) and value.strip():
            node[field_name] = value.strip()
    return node


def _runtime_nodes(context, quest_giver, referenced_roles):
    quest_giver = _required_text({"quest_giver": quest_giver}, "quest_giver")
    actors = context.get("actors") or {}
    if not isinstance(actors, dict):
        raise SocialEffectCompilationError("social quest actors must be a dictionary")

    node_refs = {"player": "player", "quest_giver": "quest_giver"}
    nodes = [
        {
            "ref": "player",
            "node_type": "player",
            "identifier_template": "{character_id}",
            "display_name_template": "{character_key}",
        },
        {
            "ref": "quest_giver",
            "node_type": "npc",
            "identifier": quest_giver.removeprefix("npc:"),
            "display_name": quest_giver.removeprefix("npc:"),
        },
    ]
    for role in sorted(referenced_roles):
        actor = actors[role]
        if not isinstance(actor, dict):
            raise SocialEffectCompilationError(
                f"social actor {role!r} must be a dictionary"
            )
        ref = f"actor_{role}"
        nodes.append(_node_from_key(ref, actor.get("node_key"), actor))
        node_refs[role] = ref
    return nodes, node_refs


def _node_ref_for_role(node_refs, role, *, default):
    if role in (None, ""):
        return default
    if not isinstance(role, str) or role not in node_refs:
        raise SocialEffectCompilationError(
            f"social effect references unknown actor role {role!r}"
        )
    return node_refs[role]


def _effect_identity(quest_id, index, effect):
    encoded = json.dumps(effect, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(
        f"{quest_id}|{index}|{encoded}".encode("utf-8")
    ).hexdigest()[:16]
    return f"effect:{digest}"


def _fact_key_template(quest_id, identity):
    return f"fact:{{character_id}}:{quest_id}:{identity}"


def _claim_key_template(quest_id, identity):
    return f"claim:{{character_id}}:{quest_id}:{identity}"


def _fact_action(*, nodes, node_refs, quest_id, index, effect):
    event_type = _required_text(effect, "event_type")
    tags = _effect_tags(effect)
    identity = _effect_identity(quest_id, index, effect)
    fact_key = _fact_key_template(quest_id, identity)
    subject = _node_ref_for_role(
        node_refs,
        effect.get("subject_role"),
        default="player",
    )
    return {
        "action_type": "record_social_event",
        "nodes": nodes,
        "fact": {
            "fact_key_template": fact_key,
            "subject": subject,
            "actor": "player",
            "scope": "quest_giver",
            "event_type": event_type,
            "summary": f"Social quest {quest_id} produced {event_type}.",
            "tags": tags,
            "visibility": "institutional",
            "evidence": {
                "quest_id": quest_id,
                "effect_identity": identity,
                "source": "social_effect_compiler",
            },
        },
        "knowledge": [
            {
                "node": "quest_giver",
                "fact_key_template": fact_key,
                "channel": "direct_witness",
                "confidence": 1.0,
                "spreading": False,
            },
        ],
    }


def _claim_action(*, nodes, node_refs, quest_id, index, effect):
    claim_type = _required_text(effect, "claim_type")
    if claim_type not in CLAIM_TYPES:
        raise SocialEffectCompilationError(
            f"social claim effect has unsupported claim_type {claim_type!r}"
        )
    tags = _effect_tags(effect)
    identity = _effect_identity(quest_id, index, effect)
    fact_key = _fact_key_template(quest_id, identity)
    claim_key = _claim_key_template(quest_id, identity)
    speaker = _node_ref_for_role(
        node_refs,
        effect.get("speaker_role"),
        default="quest_giver",
    )
    subject = _node_ref_for_role(
        node_refs,
        effect.get("subject_role"),
        default="player",
    )
    return {
        "action_type": "record_social_event",
        "nodes": nodes,
        "fact": {
            "fact_key_template": fact_key,
            "subject": subject,
            "actor": "player",
            "scope": "quest_giver",
            "event_type": "social_testimony_recorded",
            "summary": f"Social quest {quest_id} recorded {claim_type}.",
            "tags": tags,
            "visibility": "institutional",
            "evidence": {
                "quest_id": quest_id,
                "effect_identity": identity,
                "source": "social_effect_compiler",
            },
        },
        "claim": {
            "claim_key_template": claim_key,
            "speaker": speaker,
            "subject": subject,
            "fact_key_template": fact_key,
            "claim_type": claim_type,
            "summary": f"A {claim_type} was recorded through social quest {quest_id}.",
            "status": "supported",
            "confidence": 1.0,
            "bias_tags": tags,
        },
        "knowledge": [
            {
                "node": "quest_giver",
                "claim_key_template": claim_key,
                "channel": "official_report",
                "confidence": 1.0,
                "spreading": True,
            },
        ],
    }


def _access_actions(*, quest_id, effect):
    tags = _effect_tags(effect)
    return [
        {
            "action_type": "grant_access",
            "grant_key": access_grant_key(quest_id, tag),
            "source_quest_id": quest_id,
            "metadata": {
                "effect_type": "access_change",
                "tag": tag,
                "source": "social_effect_compiler",
            },
        }
        for tag in sorted(tags)
    ]


def compile_social_effect_actions(context, *, quest_id, quest_giver):
    """Compile every declared effect, failing closed on unsupported semantics."""
    if not isinstance(context, dict):
        raise SocialEffectCompilationError("social quest context must be a dictionary")
    if not isinstance(quest_id, str) or not quest_id.strip():
        raise SocialEffectCompilationError("social effect compilation requires quest_id")
    outline = context.get("deterministic_outline") or {}
    effects = outline.get("social_effects")
    if not isinstance(effects, list) or not effects:
        raise SocialEffectCompilationError("social quest requires declared social_effects")

    referenced_roles = set()
    for effect in effects:
        if not isinstance(effect, dict):
            continue
        for field_name in ("subject_role", "speaker_role"):
            role = effect.get(field_name)
            if role not in (None, ""):
                if not isinstance(role, str):
                    raise SocialEffectCompilationError(
                        f"social effect {field_name} must be a string"
                    )
                referenced_roles.add(role)
    actors = context.get("actors") or {}
    unknown_roles = sorted(role for role in referenced_roles if role not in actors)
    if unknown_roles:
        raise SocialEffectCompilationError(
            "social effect references unknown actor role "
            + ", ".join(repr(role) for role in unknown_roles)
        )
    nodes, node_refs = _runtime_nodes(context, quest_giver, referenced_roles)
    actions = []
    for index, effect in enumerate(effects):
        if not isinstance(effect, dict):
            raise SocialEffectCompilationError(
                f"social effect at index {index} must be a dictionary"
            )
        effect_type = effect.get("type")
        if effect_type not in _EXECUTABLE_EFFECT_TYPES:
            raise SocialEffectCompilationError(
                f"social effect type {effect_type!r} has no executable runtime action"
            )
        if effect_type == "social_fact":
            actions.append(
                _fact_action(
                    nodes=nodes,
                    node_refs=node_refs,
                    quest_id=quest_id,
                    index=index,
                    effect=effect,
                )
            )
        elif effect_type == "social_claim":
            actions.append(
                _claim_action(
                    nodes=nodes,
                    node_refs=node_refs,
                    quest_id=quest_id,
                    index=index,
                    effect=effect,
                )
            )
        else:
            actions.extend(_access_actions(quest_id=quest_id, effect=effect))
    return actions
