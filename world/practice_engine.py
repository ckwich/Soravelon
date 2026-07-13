"""
Practice opportunity engine for Soravelon.

Practice opportunities are builder-authored, fiction-justified interactions
that feed skill practice and optional domain XP without exposing numeric XP.
"""

import re

from world.skill_definitions import SKILL_DEFINITIONS
from world.domain_definitions import ALL_DOMAINS
from world.remnance_visibility import HIDDEN_CURRENT_ERA_DOMAINS


UNAVAILABLE_MESSAGE = "That practice is not available."


def _normalize_text(value):
    """Normalize player args and authored targets for forgiving matching."""
    text = str(value or "").lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _target_matches(expected_target, player_args):
    """Return True when command args clearly refer to the authored target."""
    target = _normalize_text(expected_target)
    args = _normalize_text(player_args)
    if not target:
        return True
    if not args:
        return False
    return args == target or args in target or target in args


def _completed_ids(character):
    current = getattr(character.db, "practice_opportunities_completed", None)
    if not current:
        return set()
    return set(current)


def _mark_completed(character, opportunity_id):
    completed = _completed_ids(character)
    completed.add(opportunity_id)
    character.db.practice_opportunities_completed = sorted(completed)


def _has_hidden_player_facing_domain(skill_awards, domain_awards):
    """Block hidden domains from generic current-era practice hooks."""
    authored_domains = set((domain_awards or {}).keys())
    authored_skills = set((skill_awards or {}).keys())
    return bool(
        authored_domains.intersection(HIDDEN_CURRENT_ERA_DOMAINS)
        or authored_skills.intersection(HIDDEN_CURRENT_ERA_DOMAINS)
    )


def _positive_int(value):
    """Return True for positive integer award values, excluding bools."""
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def validate_practice_payload(payload):
    """
    Validate a practice payload for builder/runtime use.

    Returns (bool, message). Messages are safe to show to players and therefore
    never name hidden domains.
    """
    if not payload.get("opportunity_id"):
        return False, "Practice opportunity is missing an id."

    skill_awards = payload.get("skill_awards") or payload.get("skills") or {}
    domain_awards = payload.get("domain_awards") or payload.get("domains") or {}

    if not skill_awards and not domain_awards:
        return False, "Practice opportunity needs at least one award."

    if _has_hidden_player_facing_domain(skill_awards, domain_awards):
        return False, UNAVAILABLE_MESSAGE

    for skill_id, count in skill_awards.items():
        if skill_id not in SKILL_DEFINITIONS:
            return False, f"Unknown practice skill: {skill_id}"
        if not _positive_int(count):
            return False, f"Practice skill award for {skill_id} must be a positive integer."

    for domain, raw_xp in domain_awards.items():
        if domain not in ALL_DOMAINS:
            return False, f"Unknown practice domain: {domain}"
        if not _positive_int(raw_xp):
            return False, f"Practice domain award for {domain} must be a positive integer."

    return True, ""


def resolve_practice_opportunity(payload, context):
    """
    Execute a practice opportunity from a custom command or trigger.

    Records skill-use counts and raw domain XP as one durable authored event.
    The player sees authored prose, never numeric XP.
    """
    character = context.get("character")
    if not character:
        return False, "No character in context"

    valid, validation_msg = validate_practice_payload(payload)
    if not valid:
        return False, validation_msg

    opportunity_id = payload["opportunity_id"]
    target = payload.get("target", "")
    if not _target_matches(target, context.get("args", "")):
        verb = payload.get("verb") or "use"
        return False, f"Try: {verb} {target}."

    once_per_character = payload.get("once_per_character", True)
    if once_per_character and opportunity_id in _completed_ids(character):
        return False, "You have already learned what you can from that."

    skill_awards = payload.get("skill_awards") or payload.get("skills") or {}
    domain_awards = payload.get("domain_awards") or payload.get("domains") or {}

    if domain_awards or skill_awards:
        from world.progression_engine import record_progression_event

        recorded, record_message = record_progression_event(
            character,
            event_id=f"practice:{opportunity_id}",
            event_type="practice",
            source_id=opportunity_id,
            domain_awards=domain_awards,
            skill_awards=skill_awards,
        )
        if not recorded:
            return False, record_message

    from world.quest_engine import check_practice_objectives
    check_practice_objectives(character, opportunity_id)

    if once_per_character:
        _mark_completed(character, opportunity_id)

    success_text = payload.get("success_text") or "You take a moment to learn from the work."
    character.msg(success_text)
    return True, ""
