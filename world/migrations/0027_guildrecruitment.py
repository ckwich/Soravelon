from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("world", "0026_progressionevent"),
    ]

    operations = [
        migrations.CreateModel(
            name="GuildRecruitment",
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
                ("guild_id", models.CharField(max_length=64)),
                (
                    "status",
                    models.CharField(
                        choices=[("offered", "Offered"), ("completed", "Completed")],
                        default="offered",
                        max_length=16,
                    ),
                ),
                ("contact_npc_id", models.CharField(max_length=128)),
                ("location_zone_id", models.CharField(max_length=64)),
                ("location_room_id", models.CharField(max_length=128)),
                ("secondary_domain", models.CharField(blank=True, default="", max_length=32)),
                ("offered_at", models.DateTimeField(auto_now_add=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="guild_recruitments",
                        to="objects.objectdb",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="guildrecruitment",
            constraint=models.UniqueConstraint(
                fields=("character", "guild_id"),
                name="unique_character_guild_recruitment",
            ),
        ),
        migrations.AddIndex(
            model_name="guildrecruitment",
            index=models.Index(
                fields=["character", "status"],
                name="guild_recruitment_status_idx",
            ),
        ),
    ]
