"""Renderer-only seam for optional Social Web quest voice personalization."""

from __future__ import annotations

import json
import re


MAX_SEMANTIC_EVIDENCE = 3
MAX_SEMANTIC_OBJECTIVES = 4
MAX_SEMANTIC_TEXT_CHARS = 320
MAX_RENDERED_SPEECH_CHARS = 480
MAX_RENDERED_TONE_TAGS = 4
PUBLIC_SEMANTIC_VISIBILITIES = {
    "witnessed",
    "local",
    "institutional",
    "route",
    "global",
}
RAW_IDENTIFIER_PATTERN = re.compile(
    r"\b(?:fact|claim|npc|player|node|edge):",
    re.IGNORECASE,
)
UNSAFE_RENDERED_SPEECH_PATTERN = re.compile(
    r"\b(?:secret|withheld|admin)\b|\|[A-Za-z]",
    re.IGNORECASE,
)
CAPITALIZED_TOKEN_PATTERN = re.compile(r"\b[A-Z][A-Za-z'-]*\b")
TONE_TAG_PATTERN = re.compile(r"^[a-z][a-z0-9_ -]{0,31}$")
COMMON_CAPITALIZED_OUTPUT_TOKENS = {
    "a",
    "an",
    "and",
    "ask",
    "bring",
    "but",
    "come",
    "confront",
    "do",
    "for",
    "follow",
    "go",
    "help",
    "i",
    "if",
    "in",
    "it",
    "its",
    "keep",
    "meet",
    "of",
    "or",
    "our",
    "please",
    "protect",
    "report",
    "return",
    "road",
    "roads",
    "speak",
    "take",
    "that",
    "the",
    "their",
    "them",
    "these",
    "they",
    "this",
    "those",
    "to",
    "us",
    "warden",
    "wardens",
    "we",
    "what",
    "when",
    "where",
    "witness",
    "witnesses",
    "work",
    "you",
    "your",
}


def _safe_semantic_text(value):
    if value is None or isinstance(value, bool):
        return ""
    text = str(value).strip()
    if not text or RAW_IDENTIFIER_PATTERN.search(text):
        return ""
    if len(text) > MAX_SEMANTIC_TEXT_CHARS:
        text = f"{text[: MAX_SEMANTIC_TEXT_CHARS - 1].rstrip()}..."
    return text


def _safe_entity_names(quest_spec):
    context = (quest_spec or {}).get("social_quest_context") or {}
    actors = context.get("actors") or {}
    names = []
    for actor in actors.values() if isinstance(actors, dict) else ():
        if not isinstance(actor, dict):
            continue
        name = _safe_semantic_text(actor.get("display_name"))
        if name and name not in names:
            names.append(name)
    return names


def _semantic_evidence(prompt_inputs):
    social_memory = (prompt_inputs or {}).get("social_memory") or {}
    evidence = []
    for fact in social_memory.get("facts") or []:
        if not isinstance(fact, dict):
            continue
        visibility = str(fact.get("visibility") or "").strip().lower()
        if visibility not in PUBLIC_SEMANTIC_VISIBILITIES:
            continue
        summary = _safe_semantic_text(fact.get("summary"))
        if not summary:
            continue
        channel = _safe_semantic_text(fact.get("channel")).replace("_", " ")
        item = {"summary": summary}
        if channel:
            item["channel"] = channel
        evidence.append(item)
        if len(evidence) >= MAX_SEMANTIC_EVIDENCE:
            return evidence

    for interaction in (prompt_inputs or {}).get("prior_interactions") or []:
        if not isinstance(interaction, dict):
            continue
        summary = _safe_semantic_text(interaction.get("summary"))
        if not summary or any(item["summary"] == summary for item in evidence):
            continue
        evidence.append({"summary": summary})
        if len(evidence) >= MAX_SEMANTIC_EVIDENCE:
            break
    return evidence


def _semantic_objectives(prompt_inputs):
    objectives = []
    for objective in (prompt_inputs or {}).get("objective_steps") or []:
        if not isinstance(objective, dict):
            continue
        summary = _safe_semantic_text(objective.get("summary"))
        if summary:
            objectives.append(summary)
        if len(objectives) >= MAX_SEMANTIC_OBJECTIVES:
            break
    return objectives


def _llm_context_from_quest(quest_spec):
    return ((quest_spec or {}).get("social_quest_context") or {}).get(
        "llm_context"
    ) or {}


def build_social_quest_render_payload(quest_spec):
    """Build an allowlisted semantic chat payload for a quest-offer voice."""
    quest_spec = quest_spec or {}
    llm_context = _llm_context_from_quest(quest_spec)
    prompt_inputs = llm_context.get("prompt_inputs") or {}
    semantic_packet = {
        "purpose": "social_quest_offer_voice",
        "incident_brief": _safe_semantic_text(prompt_inputs.get("incident_brief")),
        "archetype_brief": _safe_semantic_text(prompt_inputs.get("archetype_brief")),
        "evidence": _semantic_evidence(prompt_inputs),
        "objectives": _semantic_objectives(prompt_inputs),
        "allowed_entities": _safe_entity_names(quest_spec),
    }
    system_text = (
        "Phrase a Soravelon NPC quest offer only from the semantic packet. "
        "Do not use identifiers, traces, confidence, private evidence, secrets, "
        "hidden lore, or entities outside allowed_entities. Do not create facts, "
        "mutate quest state, or invent consequences. Return JSON with speech and "
        "tone_tags."
    )
    return {
        "provider_contract": "deepseek_compatible_chat",
        "semantic_packet": semantic_packet,
        "messages": [
            {"role": "system", "content": system_text},
            {
                "role": "user",
                "content": json.dumps(semantic_packet, sort_keys=True),
            },
        ],
        "response_format": {"speech": "string", "tone_tags": "list[string]"},
    }


def _fallback_speech(quest_spec):
    description = str((quest_spec or {}).get("description") or "").strip()
    if description:
        return description
    quest_name = str((quest_spec or {}).get("name") or "this task").strip()
    return f"I have {quest_name} for you, if you are willing."


def _normalize_rendered_response(response):
    if isinstance(response, dict) and isinstance(response.get("speech"), str):
        tone_tags = response.get("tone_tags") or []
        if not isinstance(tone_tags, list):
            return None
        return {
            "speech": response["speech"].strip(),
            "tone_tags": [
                tag.strip()
                for tag in tone_tags
                if isinstance(tag, str) and tag.strip()
            ],
        }

    content = None
    if isinstance(response, dict):
        choices = response.get("choices") or []
        if choices:
            message = (choices[0] or {}).get("message") or {}
            content = message.get("content")
    if not content:
        return None

    try:
        parsed = json.loads(content)
    except (TypeError, ValueError):
        parsed = {"speech": str(content)}
    return _normalize_rendered_response(parsed)


def _call_provider(provider, payload):
    if hasattr(provider, "render"):
        return provider.render(payload)
    if hasattr(provider, "create_chat_completion"):
        return provider.create_chat_completion(payload)
    if callable(provider):
        return provider(payload)
    raise TypeError("provider must be callable or expose render(payload)")


def _provider_calls_enabled():
    from django.conf import settings

    return bool(getattr(settings, "SOCIAL_RENDERER_ENABLED", False))


def _allowed_entity_tokens(payload):
    semantic_packet = (payload or {}).get("semantic_packet") or {}
    allowed = set()
    for name in semantic_packet.get("allowed_entities") or []:
        allowed.update(token.lower() for token in re.findall(r"[A-Za-z'-]+", name))
    return allowed


def _contains_hidden_lore(text):
    from world.remnance_visibility import (
        HIDDEN_CURRENT_ERA_DOMAINS,
        HIDDEN_CURRENT_ERA_GUILDS,
        HIDDEN_CURRENT_ERA_RESOURCES,
    )

    return any(
        re.search(rf"\b{re.escape(term)}\b", text, re.IGNORECASE)
        for term in (
            HIDDEN_CURRENT_ERA_DOMAINS
            | HIDDEN_CURRENT_ERA_GUILDS
            | HIDDEN_CURRENT_ERA_RESOURCES
        )
    )


def _uses_only_allowed_entities(text, payload):
    allowed_tokens = _allowed_entity_tokens(payload)
    for token in CAPITALIZED_TOKEN_PATTERN.findall(text):
        normalized = token.lower()
        if (
            normalized not in allowed_tokens
            and normalized not in COMMON_CAPITALIZED_OUTPUT_TOKENS
        ):
            return False
    return True


def _validate_rendered_response(response, payload):
    if not response:
        return None
    speech = response.get("speech") or ""
    if not speech or len(speech) > MAX_RENDERED_SPEECH_CHARS:
        return None
    if RAW_IDENTIFIER_PATTERN.search(speech) or UNSAFE_RENDERED_SPEECH_PATTERN.search(
        speech
    ):
        return None
    if _contains_hidden_lore(speech):
        return None
    if not _uses_only_allowed_entities(speech, payload):
        return None

    tone_tags = response.get("tone_tags") or []
    if len(tone_tags) > MAX_RENDERED_TONE_TAGS or any(
        not TONE_TAG_PATTERN.fullmatch(tag) for tag in tone_tags
    ):
        return None
    return {"speech": speech, "tone_tags": tone_tags}


def _fallback_render(quest_spec, payload, *, reason):
    return {
        "speech": _fallback_speech(quest_spec),
        "tone_tags": ["deterministic", "bounded"],
        "provider_used": False,
        "fallback_used": True,
        "fallback_reason": reason,
        "provider_contract": payload["provider_contract"],
    }


def render_social_quest_offer(
    quest_spec,
    *,
    provider=None,
    allow_provider_call=False,
):
    """Render quest-offer speech without granting the provider world authority."""
    payload = build_social_quest_render_payload(quest_spec)
    llm_context = _llm_context_from_quest(quest_spec)
    context_allows_provider = bool(llm_context.get("provider_call_allowed"))

    if (
        provider
        and _provider_calls_enabled()
        and allow_provider_call
        and context_allows_provider
    ):
        try:
            response = _normalize_rendered_response(_call_provider(provider, payload))
        except Exception:
            return _fallback_render(quest_spec, payload, reason="provider_error")
        response = _validate_rendered_response(response, payload)
        if response:
            return {
                "speech": response["speech"],
                "tone_tags": response.get("tone_tags") or [],
                "provider_used": True,
                "fallback_used": False,
                "fallback_reason": "",
                "provider_contract": payload["provider_contract"],
            }

    if not provider:
        reason = "no_provider"
    elif not _provider_calls_enabled():
        reason = "renderer_disabled"
    elif not allow_provider_call:
        reason = "caller_disallowed"
    elif not context_allows_provider:
        reason = "packet_disallowed"
    else:
        reason = "validation_failed"
    return _fallback_render(quest_spec, payload, reason=reason)
