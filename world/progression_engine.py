"""Durable authority for typed, authored progression events."""

from collections.abc import Callable, Mapping
from numbers import Integral

from django.db import transaction
from django.utils import timezone

from world.domain_definitions import ALL_DOMAINS
from world.remnance_visibility import (
    HIDDEN_CURRENT_ERA_DOMAINS,
    domain_is_player_visible,
)
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


QUEST_DOMAIN_XP_PER_SKILL_USE = 5
GATHERING_DOMAIN_XP_PER_TIER = 5
EXPLORATION_LANDMARK_DOMAIN_XP = 20
EXPLORATION_LANDMARK_SKILL_USES = 2
INVESTIGATION_DISCOVERY_DOMAIN_XP = 10
NAMED_COMBAT_DOMAIN_XP = 25
LEGENDARY_COMBAT_DOMAIN_XP = 50


def _normalized_domain_awards(
    domain_awards: Mapping,
    *,
    character=None,
) -> dict[str, int]:
    if not isinstance(domain_awards, Mapping):
        raise ValueError("Progression domain awards must be a mapping.")

    normalized = {}
    for domain, raw_xp in domain_awards.items():
        if domain not in ALL_DOMAINS:
            raise ValueError(f"Unknown progression domain: {domain}")
        if (
            domain in HIDDEN_CURRENT_ERA_DOMAINS
            and not domain_is_player_visible(domain, character)
        ):
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
            {} if domain_awards is None else domain_awards,
            character=character,
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


def _record_skill_outcome(
    character,
    *,
    event_id,
    event_type,
    source_id,
    skill_id,
    domain_raw_xp,
    skill_uses=0,
):
    """Map one authored skill to its domain without exposing numeric growth."""
    skill = SKILL_DEFINITIONS.get(skill_id)
    if not skill:
        return False, f"Unknown progression skill: {skill_id}"

    domain_awards = {}
    domain = skill.get("domain_bonus")
    if (
        domain
        and domain_raw_xp > 0
        and domain_is_player_visible(domain, character)
    ):
        domain_awards[domain] = domain_raw_xp
    skill_awards = {skill_id: skill_uses} if skill_uses > 0 else {}
    if not domain_awards and not skill_awards:
        return True, ""
    return record_progression_event(
        character,
        event_id=event_id,
        event_type=event_type,
        source_id=source_id,
        domain_awards=domain_awards,
        skill_awards=skill_awards,
    )


def record_gathering_outcome(character, material_id):
    """Reward first-hand mastery of one authored material, not repeated pulls."""
    from world.material_definitions import MATERIAL_REGISTRY

    material = MATERIAL_REGISTRY.get(material_id)
    if not material:
        return False, f"Unknown gathering progression source: {material_id}"
    return _record_skill_outcome(
        character,
        event_id=f"gathering:{material_id}",
        event_type="gathering",
        source_id=material_id,
        skill_id=material["gathering_skill"],
        domain_raw_xp=material["tier"] * GATHERING_DOMAIN_XP_PER_TIER,
    )


def record_crafting_outcome(character, recipe_id):
    """Reward the first successful completion of one authored recipe."""
    from world.crafting_definitions import RECIPE_REGISTRY

    recipe = RECIPE_REGISTRY.get(recipe_id)
    if not recipe:
        return False, f"Unknown crafting progression source: {recipe_id}"
    difficulty = recipe.get("difficulty", 10)
    if (
        isinstance(difficulty, bool)
        or not isinstance(difficulty, Integral)
        or difficulty <= 0
    ):
        return False, f"Invalid crafting progression difficulty: {recipe_id}"
    return _record_skill_outcome(
        character,
        event_id=f"crafting:{recipe_id}",
        event_type="crafting",
        source_id=recipe_id,
        skill_id=recipe.get("skill", "cooking"),
        domain_raw_xp=max(5, min(25, int(difficulty) // 2)),
    )


def record_quest_outcome(
    character,
    quest_id,
    reward_index,
    skill_id,
    skill_uses,
):
    """Convert one explicit quest skill reward into a durable typed outcome."""
    if (
        isinstance(reward_index, bool)
        or not isinstance(reward_index, Integral)
        or reward_index < 0
    ):
        return False, "Quest progression reward index is invalid."
    if (
        isinstance(skill_uses, bool)
        or not isinstance(skill_uses, Integral)
        or skill_uses <= 0
    ):
        return False, "Quest progression skill award is invalid."
    return _record_skill_outcome(
        character,
        event_id=f"quest:{quest_id}:reward:{reward_index}",
        event_type="quest_outcome",
        source_id=quest_id,
        skill_id=skill_id,
        domain_raw_xp=int(skill_uses) * QUEST_DOMAIN_XP_PER_SKILL_USE,
        skill_uses=int(skill_uses),
    )


def record_exploration_outcome(character, landmark_id):
    """Reward discovery of one authored courier landmark once."""
    return _record_skill_outcome(
        character,
        event_id=f"exploration:landmark:{landmark_id}",
        event_type="exploration",
        source_id=landmark_id,
        skill_id="navigation",
        domain_raw_xp=EXPLORATION_LANDMARK_DOMAIN_XP,
        skill_uses=EXPLORATION_LANDMARK_SKILL_USES,
    )


def record_investigation_outcome(character, discovery_id):
    """Reward a novel search discovery while respecting future-story secrecy."""
    return _record_skill_outcome(
        character,
        event_id=f"investigation:{discovery_id}",
        event_type="investigation",
        source_id=discovery_id,
        skill_id="investigation",
        domain_raw_xp=INVESTIGATION_DISCOVERY_DOMAIN_XP,
        skill_uses=1,
    )


def record_combat_outcome(
    character,
    source_id,
    *,
    is_named,
    is_legendary,
):
    """Reward named or legendary victories; ordinary kills remain grind-free."""
    if not is_named and not is_legendary:
        return True, ""
    raw_xp = (
        LEGENDARY_COMBAT_DOMAIN_XP
        if is_legendary
        else NAMED_COMBAT_DOMAIN_XP
    )
    return record_progression_event(
        character,
        event_id=f"combat:{source_id}",
        event_type="combat_outcome",
        source_id=source_id,
        domain_awards={"combat": raw_xp},
    )


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
