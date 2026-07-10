"""Give completed quests a durable, internally consistent outcome identity."""

from django.db import migrations, models
from django.utils import timezone


def backfill_completed_quest_outcomes(apps, schema_editor):
    CharacterQuest = apps.get_model("world", "CharacterQuest")
    GameOperation = apps.get_model("world", "GameOperation")

    invalid = list(
        CharacterQuest.objects.exclude(status="complete")
        .exclude(completed_at=None)
        .values_list("pk", flat=True)[:20]
    )
    if invalid:
        raise RuntimeError(
            "character_quest_noncomplete_has_completed_at: "
            + ", ".join(str(pk) for pk in invalid)
        )

    for quest in CharacterQuest.objects.filter(status="complete").iterator():
        operation_id = f"quest-outcome:{quest.pk}"
        related_id = f"quest:{quest.quest_id}:{quest.pk}"
        completed_at = quest.completed_at or quest.started_at or timezone.now()
        result = {
            "status": "migrated_complete",
            "quest_id": quest.quest_id,
            "rewards_replayed": False,
        }

        existing = GameOperation.objects.filter(
            operation_id=operation_id,
        ).first()
        if existing and (
            existing.character_ref != quest.character_id
            or existing.operation_type != "quest_completion"
            or existing.related_id != related_id
        ):
            raise RuntimeError(
                f"character_quest_outcome_operation_conflict: {quest.pk}"
            )
        if not existing:
            GameOperation.objects.create(
                operation_id=operation_id,
                character_id=quest.character_id,
                character_ref=quest.character_id,
                operation_type="quest_completion",
                related_id=related_id,
                result=result,
            )

        CharacterQuest.objects.filter(pk=quest.pk).update(
            completed_at=completed_at,
            outcome_operation_id=operation_id,
            outcome_result=result,
        )


def remove_backfilled_quest_outcomes(apps, schema_editor):
    CharacterQuest = apps.get_model("world", "CharacterQuest")
    GameOperation = apps.get_model("world", "GameOperation")

    operation_ids = list(
        CharacterQuest.objects.filter(
            outcome_result__status="migrated_complete",
        ).values_list("outcome_operation_id", flat=True)
    )
    CharacterQuest.objects.filter(
        outcome_result__status="migrated_complete",
    ).update(
        outcome_operation_id=None,
        outcome_result={},
    )
    GameOperation.objects.filter(
        operation_id__in=[operation_id for operation_id in operation_ids if operation_id],
        operation_type="quest_completion",
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0015_game_operation"),
    ]

    operations = [
        migrations.AddField(
            model_name="characterquest",
            name="outcome_operation_id",
            field=models.CharField(
                blank=True,
                editable=False,
                max_length=128,
                null=True,
                unique=True,
            ),
        ),
        migrations.AddField(
            model_name="characterquest",
            name="outcome_result",
            field=models.JSONField(default=dict),
        ),
        migrations.RunPython(
            backfill_completed_quest_outcomes,
            remove_backfilled_quest_outcomes,
        ),
        migrations.AddConstraint(
            model_name="characterquest",
            constraint=models.CheckConstraint(
                condition=(
                    models.Q(
                        status="complete",
                        completed_at__isnull=False,
                        outcome_operation_id__isnull=False,
                    )
                    | models.Q(
                        ~models.Q(status="complete"),
                        completed_at__isnull=True,
                        outcome_operation_id__isnull=True,
                    )
                ),
                name="character_quest_completion_consistent",
            ),
        ),
    ]
