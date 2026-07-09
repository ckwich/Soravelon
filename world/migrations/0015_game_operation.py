"""Add durable exactly-once receipts for composite game operations."""

import django.db.models.deletion
from django.db import migrations, models

import world.economy_ids


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0014_unique_equipped_slot"),
    ]

    operations = [
        migrations.CreateModel(
            name="GameOperation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "operation_id",
                    models.CharField(
                        default=world.economy_ids.new_operation_id,
                        editable=False,
                        max_length=128,
                        unique=True,
                    ),
                ),
                ("character_ref", models.BigIntegerField()),
                ("operation_type", models.CharField(max_length=48)),
                ("related_id", models.CharField(max_length=160)),
                ("result", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "character",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="game_operations",
                        to="objects.objectdb",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["character", "operation_type"],
                        name="world_gameop_actor_type_idx",
                    ),
                    models.Index(
                        fields=["operation_type", "related_id"],
                        name="world_gameop_type_related_idx",
                    ),
                ],
                "constraints": [
                    models.CheckConstraint(
                        condition=(
                            models.Q(character__isnull=True)
                            | models.Q(character_id=models.F("character_ref"))
                        ),
                        name="game_operation_actor_ref_matches",
                    ),
                ],
            },
        ),
    ]
