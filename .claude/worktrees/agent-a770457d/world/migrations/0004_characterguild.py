"""
Migration for CharacterGuild model.

Generated for Phase 04 — domain fingerprints and guild engine.
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("objects", "0001_initial"),
        ("world", "0003_worldeventlog"),
    ]

    operations = [
        migrations.CreateModel(
            name="CharacterGuild",
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
                    "guild_id",
                    models.CharField(db_index=True, max_length=64),
                ),
                (
                    "primary_domain",
                    models.CharField(max_length=32),
                ),
                (
                    "secondary_domain",
                    models.CharField(max_length=32),
                ),
                (
                    "subclass_id",
                    models.CharField(db_index=True, max_length=64),
                ),
                (
                    "joined_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "induction_complete",
                    models.BooleanField(default=False),
                ),
                (
                    "character",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="guild_record",
                        to="objects.objectdb",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["guild_id"],
                        name="world_charac_guild_i_idx",
                    ),
                ],
            },
        ),
    ]
