"""Validation for literal, runtime-effective NPC dialogue payloads."""

from collections.abc import Mapping

from world.dialogue_definitions import STANDING_TIER_THRESHOLDS


LEGACY_DIALOGUE_KEYS = frozenset({"greeting", "hints"})
LIST_HINT_FIELDS = frozenset(
    {
        "base_hints",
        "network_hints",
        "scholar_hints",
        "warden_hints",
    }
)
MAPPED_HINT_FIELDS = frozenset({"tier_hints", "quest_hints"})
SUPPORTED_DIALOGUE_KEYS = frozenset(
    {"greeting_tiers", "topics"} | LIST_HINT_FIELDS | MAPPED_HINT_FIELDS
)
SUPPORTED_GREETING_TIERS = frozenset(
    {tier for _threshold, tier in STANDING_TIER_THRESHOLDS}
    | {"betrayal"}
)


class DialogueSchemaError(ValueError):
    """Raised when authored dialogue would be ignored or misrouted."""


def _nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def _validate_topic_references(field_name, references, topic_keys, errors):
    if not isinstance(references, (list, tuple)):
        errors.append(f"{field_name} must be a list of topic keys")
        return
    for reference in references:
        if not _nonempty_text(reference):
            errors.append(f"{field_name} contains a non-text topic reference")
        elif reference not in topic_keys:
            errors.append(
                f"{field_name} references unknown topic '{reference}'"
            )


def validate_dialogue_payload(payload):
    """Return ``payload`` after proving every authored field affects runtime.

    Hints are topic identifiers, never display prose. Legacy ``greeting`` and
    ``hints`` keys are rejected so content cannot silently fall through an
    ignored compatibility path.
    """

    if payload in (None, {}):
        return {}
    if not isinstance(payload, Mapping):
        raise DialogueSchemaError("dialogue must be a mapping")

    errors = []
    keys = set(payload)
    legacy = sorted(keys & LEGACY_DIALOGUE_KEYS)
    if legacy:
        errors.append(
            "legacy dialogue keys are not supported: " + ", ".join(legacy)
        )
    unknown = sorted(
        (repr(key) for key in keys - SUPPORTED_DIALOGUE_KEYS - LEGACY_DIALOGUE_KEYS)
    )
    if unknown:
        errors.append("unknown dialogue keys: " + ", ".join(unknown))

    greetings = payload.get("greeting_tiers", {})
    if not isinstance(greetings, Mapping):
        errors.append("greeting_tiers must be a mapping")
    else:
        for tier, text in greetings.items():
            if tier not in SUPPORTED_GREETING_TIERS:
                errors.append(f"greeting_tiers contains unsupported tier '{tier}'")
            if not _nonempty_text(text):
                errors.append(f"greeting_tiers['{tier}'] must be non-empty text")

    topics = payload.get("topics", {})
    topic_keys = set()
    if not isinstance(topics, Mapping):
        errors.append("topics must be a mapping")
    else:
        for topic_key, responses in topics.items():
            if not _nonempty_text(topic_key):
                errors.append("topics contains an empty or non-text topic key")
                continue
            topic_keys.add(topic_key)
            if _nonempty_text(responses):
                continue
            if not isinstance(responses, Mapping):
                errors.append(
                    f"topic '{topic_key}' must be text or a response mapping"
                )
                continue
            if not _nonempty_text(responses.get("default")):
                errors.append(
                    f"topic '{topic_key}' response mapping needs non-empty default text"
                )
            for condition, text in responses.items():
                if not _nonempty_text(condition) or not _nonempty_text(text):
                    errors.append(
                        f"topic '{topic_key}' responses must map conditions to text"
                    )

    for field_name in sorted(LIST_HINT_FIELDS):
        _validate_topic_references(
            field_name,
            payload.get(field_name, []),
            topic_keys,
            errors,
        )

    for field_name in sorted(MAPPED_HINT_FIELDS):
        grouped_hints = payload.get(field_name, {})
        if not isinstance(grouped_hints, Mapping):
            errors.append(f"{field_name} must map conditions to topic-key lists")
            continue
        for condition, references in grouped_hints.items():
            if not _nonempty_text(condition):
                errors.append(f"{field_name} contains an empty condition key")
                continue
            _validate_topic_references(
                f"{field_name}['{condition}']",
                references,
                topic_keys,
                errors,
            )

    if errors:
        raise DialogueSchemaError("; ".join(errors))
    return payload
