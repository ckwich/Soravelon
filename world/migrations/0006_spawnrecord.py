# Generated manually for SpawnRecord model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0005_characterability"),
    ]

    operations = [
        migrations.CreateModel(
            name="SpawnRecord",
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
                ("room_id", models.IntegerField(db_index=True)),
                ("spawn_index", models.IntegerField()),
                ("mob_template", models.CharField(max_length=64)),
                ("active_mob_ids", models.JSONField(default=list)),
                ("respawn_at", models.DateTimeField(db_index=True, null=True)),
                ("is_named", models.BooleanField(default=False)),
                (
                    "named_id",
                    models.CharField(blank=True, default="", max_length=128),
                ),
            ],
            options={
                "unique_together": {("room_id", "spawn_index")},
                "indexes": [
                    models.Index(
                        fields=["respawn_at"],
                        name="world_spawn_respawn_idx",
                    ),
                    models.Index(
                        fields=["is_named"],
                        name="world_spawn_is_named_idx",
                    ),
                ],
            },
        ),
    ]
