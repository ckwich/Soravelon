"""Durable authority for typed, authored progression events."""

from collections.abc import Callable, Mapping
from numbers import Integral

from django.db import transaction
from django.utils import timezone

from world.domain_definitions import ALL_DOMAINS
from world.remnance_visibility import HIDDEN_CURRENT_ERA_DOMAINS
from world.skill_definitions import SKILL_DEFINITIONS


EVENT_TYPES = frozenset(
    {
        "combat_outcome",
        "quest_outcome",
        "practice",
        "gathering",
        "crafting",
        "exploration",
        "investigation",
    }
)


def _normalized_domain_awards(domain_awards: Mapping) -> dict[str, int]:
    if not isinstance(domain_awards, Mapping):
        raise ValueError("Progression domain awards must be a mapping.")

    normalized = {}
    for domain, raw_xp in domain_awards.items():
        if domain not in ALL_DOMAINS:
            raise ValueError(f"Unknown progression domain: {domain}")
        if domain in HIDDEN_CURRENT_ERA_DOMAINS:
            raise ValueError("That progression is not available.")
        if (
            isinstance(raw_xp, bool)
            or not isinstance(raw_xp, Integral)
            or raw_xp <= 0
        ):
            raise ValueError(
                f"Progression award for {domain} must be a positive integer."
            )
        normalized[domain] = int(raw_xp)
    return dict(sorted(normalized.items()))


def _normalized_skill_awards(skill_awards: Mapping) -> dict[str, int]:
    if not isinstance(skill_awards, Mapping):
        raise ValueError("Progression skill awards must be a mapping.")

    normalized = {}
    for skill_id, use_count in skill_awards.items():
        if skill_id not in SKILL_DEFINITIONS:
            raise ValueError(f"Unknown progression skill: {skill_id}")
        if (
            isinstance(use_count, bool)
            or not isinstance(use_count, Integral)
            or use_count <= 0
        ):
            raise ValueError(
                f"Progression award for {skill_id} must be a positive integer."
            )
        normalized[skill_id] = int(use_count)
    return dict(sorted(normalized.items()))


def record_progression_event(
    character,
    *,
    event_id: str,
    event_type: str,
    source_id: str,
    domain_awards: Mapping | None = None,
    skill_awards: Mapping | None = None,
):
    """Persist one authored award, replaying identical input as a no-op."""

    if not isinstance(event_id, str) or not event_id.strip() or len(event_id) > 160:
        return False, "Progression event id is invalid."
    if event_type not in EVENT_TYPES:
        return False, f"Unknown progression event type: {event_type}"
    if not isinstance(source_id, str) or not source_id.strip() or len(source_id) > 128:
        return False, "Progression event source is invalid."
    try:
        domains = _normalized_domain_awards(
            {} if domain_awards is None else domain_awards
        )
        skills = _normalized_skill_awards(
            {} if skill_awards is None else skill_awards
        )
    except ValueError as err:
        return False, str(err)
    if not domains and not skills:
        return False, "Progression event needs at least one award."

    from world.models import ProgressionEvent

    with transaction.atomic():
        event, created = ProgressionEvent.objects.get_or_create(
            character=character,
            event_id=event_id,
            defaults={
                "event_type": event_type,
                "source_id": source_id,
                "domain_awards": domains,
                "skill_awards": skills,
            },
        )
        if not created and (
            event.event_type != event_type
            or event.source_id != source_id
            or event.domain_awards != domains
            or event.skill_awards != skills
        ):
            return False, "Progression event id was reused with different awards."

    return True, ""


def apply_pending_progression_events(
    character,
    apply_awards: Callable[[dict[str, int], dict[str, int]], None],
) -> int:
    """Atomically apply and acknowledge every pending event for a character."""

    from world.models import ProgressionEvent

    with transaction.atomic():
        pending = list(
            ProgressionEvent.objects.select_for_update()
            .filter(character=character, applied_at__isnull=True)
            .order_by("id")
        )
        domain_awards: dict[str, int] = {}
        skill_awards: dict[str, int] = {}
        for event in pending:
            for domain, raw_xp in event.domain_awards.items():
                domain_awards[domain] = domain_awards.get(domain, 0) + int(raw_xp)
            for skill_id, use_count in event.skill_awards.items():
                skill_awards[skill_id] = skill_awards.get(skill_id, 0) + int(use_count)

        apply_awards(domain_awards, skill_awards)

        if pending:
            ProgressionEvent.objects.filter(
                id__in=[event.id for event in pending]
            ).update(applied_at=timezone.now())

    return len(pending)
