"""Renderer-only seam for optional Social Web quest voice personalization."""

from __future__ import annotations

import copy
import json


SENSITIVE_KEYS = {
    "api_key",
    "api_token",
    "authorization",
    "bearer_token",
    "deepseek_api_key",
    "deepseek_api_token",
    "openai_api_key",
    "password",
    "secret",
    "token",
}


def _is_sensitive_key(key):
    normalized = str(key or "").strip().lower()
    return (
        normalized in SENSITIVE_KEYS
        or normalized.endswith("_api_key")
        or normalized.endswith("_api_token")
        or normalized.endswith("_token")
        or normalized.endswith("_password")
    )


def _redact(value, *, key=""):
    if _is_sensitive_key(key) and not isinstance(value, dict):
        return "[redacted]"
    if isinstance(value, dict):
        return {
            str(item_key): _redact(item_value, key=item_key)
            for item_key, item_value in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [_redact(item) for item in value]
    return copy.deepcopy(value)


def _llm_context_from_quest(quest_spec):
    return ((quest_spec or {}).get("social_quest_context") or {}).get(
        "llm_context"
    ) or {}


def build_social_quest_render_payload(quest_spec):
    """Build a redacted DeepSeek-compatible chat payload for a quest offer."""
    quest_spec = quest_spec or {}
    llm_context = _llm_context_from_quest(quest_spec)
    prompt_inputs = _redact(llm_context.get("prompt_inputs") or {})
    system_text = (
        "Phrase a Soravelon NPC quest offer from bounded deterministic inputs. "
        "Do not create facts, mutate quest state, invent consequences, or reveal "
        "hidden lore. Return JSON with speech and tone_tags."
    )
    return {
        "provider_contract": "deepseek_compatible_chat",
        "quest_id": str(quest_spec.get("quest_id") or ""),
        "quest_giver": str(quest_spec.get("quest_giver") or ""),
        "prompt_inputs": prompt_inputs,
        "messages": [
            {"role": "system", "content": system_text},
            {
                "role": "user",
                "content": json.dumps(prompt_inputs, sort_keys=True),
            },
        ],
        "response_format": copy.deepcopy(
            llm_context.get("required_output_schema")
            or {"speech": "string", "tone_tags": "list[string]"}
        ),
    }


def _fallback_speech(quest_spec):
    description = str((quest_spec or {}).get("description") or "").strip()
    if description:
        return description
    quest_name = str((quest_spec or {}).get("name") or "this task").strip()
    return f"I have {quest_name} for you, if you are willing."


def _normalize_rendered_response(response):
    if isinstance(response, dict) and response.get("speech"):
        return {
            "speech": str(response.get("speech") or "").strip(),
            "tone_tags": [
                str(tag).strip()
                for tag in (response.get("tone_tags") or [])
                if str(tag).strip()
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

    if provider and allow_provider_call and context_allows_provider:
        response = _normalize_rendered_response(_call_provider(provider, payload))
        if response and response.get("speech"):
            return {
                "speech": response["speech"],
                "tone_tags": response.get("tone_tags") or [],
                "provider_used": True,
                "fallback_used": False,
                "provider_contract": payload["provider_contract"],
            }

    return {
        "speech": _fallback_speech(quest_spec),
        "tone_tags": ["deterministic", "bounded"],
        "provider_used": False,
        "fallback_used": True,
        "provider_contract": payload["provider_contract"],
    }
