"""Persist named access grants earned from authored outcomes."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0016_atomic_quest_outcomes"),
    ]

    operations = [
        migrations.CreateModel(
            name="CharacterAccessGrant",
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
                ("grant_key", models.CharField(max_length=128)),
                (
                    "source_quest_id",
                    models.CharField(blank=True, default="", max_length=128),
                ),
                ("metadata", models.JSONField(default=dict)),
                ("granted_at", models.DateTimeField(auto_now_add=True)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="access_grants",
                        to="objects.objectdb",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["grant_key"],
                        name="world_access_grant_key_idx",
                    ),
                ],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("character", "grant_key"),
                        name="character_access_grant_unique",
                    ),
                ],
            },
        ),
    ]
