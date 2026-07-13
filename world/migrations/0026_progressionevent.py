from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("world", "0025_world_content_deployment_lock"),
    ]

    operations = [
        migrations.AddField(
            model_name="characterskill",
            name="passive_use_remainder",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name="ProgressionEvent",
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
                ("event_id", models.CharField(max_length=160)),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("combat_outcome", "Combat outcome"),
                            ("quest_outcome", "Quest outcome"),
                            ("practice", "Practice"),
                            ("gathering", "Gathering"),
                            ("crafting", "Crafting"),
                            ("exploration", "Exploration"),
                            ("investigation", "Investigation"),
                        ],
                        max_length=32,
                    ),
                ),
                ("source_id", models.CharField(max_length=128)),
                ("domain_awards", models.JSONField(default=dict)),
                ("skill_awards", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("applied_at", models.DateTimeField(blank=True, null=True)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="progression_events",
                        to="objects.objectdb",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="progressionevent",
            constraint=models.UniqueConstraint(
                fields=("character", "event_id"),
                name="unique_character_progression_event",
            ),
        ),
        migrations.AddIndex(
            model_name="progressionevent",
            index=models.Index(
                fields=["character", "applied_at"],
                name="progression_pending_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="progressionevent",
            index=models.Index(
                fields=["event_type", "created_at"],
                name="progression_type_time_idx",
            ),
        ),
    ]
