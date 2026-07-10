"""Truthful quest-state fixtures shared by integration tests."""

from django.utils import timezone

from world.models import CharacterQuest, GameOperation


def complete_quest_fixture(quest):
    """Create the same durable state required of a runtime completion."""
    operation_id = f"quest-outcome:{quest.pk}"
    related_id = f"quest:{quest.quest_id}:{quest.pk}"
    result = {
        "status": "test_complete",
        "quest_id": quest.quest_id,
        "reward_count": 0,
    }
    GameOperation.objects.create(
        operation_id=operation_id,
        character=quest.character,
        character_ref=quest.character_id,
        operation_type="quest_completion",
        related_id=related_id,
        result=result,
    )
    CharacterQuest.objects.filter(pk=quest.pk).update(
        status="complete",
        completed_at=timezone.now(),
        outcome_operation_id=operation_id,
        outcome_result=result,
    )
    quest.refresh_from_db()
    return quest


def create_completed_quest_fixture(character, quest_id, *, progress=None):
    quest = CharacterQuest.objects.create(
        character=character,
        quest_id=quest_id,
        progress=progress or {},
    )
    return complete_quest_fixture(quest)
