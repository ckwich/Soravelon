"""Durable named access grants for authored gates."""

from __future__ import annotations

import re

from django.db import IntegrityError, transaction


_GRANT_KEY_PATTERN = re.compile(r"^[a-z0-9][a-z0-9:_-]{0,127}$")


def normalize_access_grant_key(value):
    """Return a safe canonical grant key or raise a descriptive error."""
    if not isinstance(value, str):
        raise ValueError("access grant key must be a string")
    grant_key = value.strip()
    if not _GRANT_KEY_PATTERN.fullmatch(grant_key):
        raise ValueError(
            "access grant key must use lowercase letters, digits, ':', '_' or '-'"
        )
    return grant_key


def grant_access(character, grant_key, *, source_quest_id="", metadata=None):
    """Persist one idempotent named grant for a character."""
    from world.models import CharacterAccessGrant

    grant_key = normalize_access_grant_key(grant_key)
    if not isinstance(source_quest_id, str) or len(source_quest_id) > 128:
        raise ValueError("source_quest_id must be a string of at most 128 characters")
    if metadata is not None and not isinstance(metadata, dict):
        raise ValueError("access grant metadata must be a dictionary")

    try:
        with transaction.atomic():
            grant, created = CharacterAccessGrant.objects.get_or_create(
                character=character,
                grant_key=grant_key,
                defaults={
                    "source_quest_id": source_quest_id,
                    "metadata": dict(metadata or {}),
                },
            )
    except IntegrityError:
        grant = CharacterAccessGrant.objects.get(
            character=character,
            grant_key=grant_key,
        )
        created = False
    return grant, created


def has_access_grant(character, grant_key):
    """Return whether the character has earned one exact named grant."""
    from world.models import CharacterAccessGrant

    try:
        grant_key = normalize_access_grant_key(grant_key)
    except ValueError:
        return False
    return CharacterAccessGrant.objects.filter(
        character=character,
        grant_key=grant_key,
    ).exists()
