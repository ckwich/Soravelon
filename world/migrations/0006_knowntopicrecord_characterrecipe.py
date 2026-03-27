# Generated migration for KnownTopicRecord and CharacterRecipe models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("objects", "0001_initial"),
        ("world", "0005_characterability"),
    ]

    operations = [
        migrations.CreateModel(
            name="KnownTopicRecord",
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
                ("npc_id", models.CharField(max_length=128)),
                ("topic_key", models.CharField(max_length=128)),
                (
                    "context_hash",
                    models.CharField(blank=True, default="", max_length=64),
                ),
                ("learned_at", models.DateTimeField(auto_now_add=True)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="known_topics",
                        to="objects.objectdb",
                    ),
                ),
            ],
            options={
                "unique_together": {("character", "npc_id", "topic_key")},
            },
        ),
        migrations.AddIndex(
            model_name="knowntopicrecord",
            index=models.Index(
                fields=["character", "npc_id"],
                name="world_known_charact_424052_idx",
            ),
        ),
        migrations.CreateModel(
            name="CharacterRecipe",
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
                ("recipe_id", models.CharField(max_length=128)),
                (
                    "learned_from",
                    models.CharField(blank=True, default="", max_length=64),
                ),
                ("learned_at", models.DateTimeField(auto_now_add=True)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="known_recipes",
                        to="objects.objectdb",
                    ),
                ),
            ],
            options={
                "unique_together": {("character", "recipe_id")},
            },
        ),
        migrations.AddIndex(
            model_name="characterrecipe",
            index=models.Index(
                fields=["character_id", "recipe_id"],
                name="world_chara_charact_cbd173_idx",
            ),
        ),
    ]
