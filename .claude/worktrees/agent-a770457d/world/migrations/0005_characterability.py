# Generated migration for CharacterAbility model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("objects", "0001_initial"),
        ("world", "0004_characterguild"),
    ]

    operations = [
        migrations.CreateModel(
            name="CharacterAbility",
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
                    "ability_id",
                    models.CharField(db_index=True, max_length=128),
                ),
                (
                    "unlocked_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "times_used",
                    models.IntegerField(default=0),
                ),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="character_abilities",
                        to="objects.objectdb",
                    ),
                ),
            ],
            options={
                "unique_together": {("character", "ability_id")},
                "indexes": [
                    models.Index(
                        fields=["character_id", "ability_id"],
                        name="world_charac_charact_idx",
                    ),
                ],
            },
        ),
    ]
