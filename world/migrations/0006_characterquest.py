# Generated migration for CharacterQuest model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("objects", "0001_initial"),
        ("world", "0005_characterability"),
    ]

    operations = [
        migrations.CreateModel(
            name="CharacterQuest",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quest_id",
                    models.CharField(db_index=True, max_length=128),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("complete", "Complete"),
                            ("failed", "Failed"),
                            ("abandoned", "Abandoned"),
                        ],
                        default="active",
                        max_length=16,
                    ),
                ),
                (
                    "progress",
                    models.JSONField(default=dict),
                ),
                (
                    "started_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "completed_at",
                    models.DateTimeField(blank=True, null=True),
                ),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="character_quests",
                        to="objects.objectdb",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["character", "status"],
                        name="world_chara_charact_quest_status_idx",
                    ),
                    models.Index(
                        fields=["character", "quest_id"],
                        name="world_chara_charact_quest_id_idx",
                    ),
                ],
            },
        ),
    ]
