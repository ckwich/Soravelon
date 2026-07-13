import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("world", "0023_evennia_attribute_lookup_index"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorldContentRevision",
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
                ("manifest_hash", models.CharField(max_length=64, unique=True)),
                ("schema_version", models.CharField(max_length=64)),
                ("manifest", models.JSONField()),
                ("plan", models.JSONField(default=dict)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("planned", "Planned"),
                            ("applying", "Applying"),
                            ("applied", "Applied"),
                            ("superseded", "Superseded"),
                            ("failed", "Failed"),
                            ("rolled_back", "Rolled Back"),
                        ],
                        db_index=True,
                        default="planned",
                        max_length=16,
                    ),
                ),
                ("git_commit", models.CharField(max_length=64)),
                ("maintenance_approved", models.BooleanField(default=False)),
                ("error", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("applied_at", models.DateTimeField(blank=True, null=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                (
                    "previous_revision",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="next_revisions",
                        to="world.worldcontentrevision",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["status", "-created_at"],
                        name="world_content_status_idx",
                    )
                ],
                "constraints": [
                    models.UniqueConstraint(
                        condition=models.Q(("status", "applied")),
                        fields=("status",),
                        name="world_content_single_applied_revision",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("manifest_hash__regex", "^[0-9a-f]{64}$")),
                        name="world_content_manifest_hash_hex",
                    ),
                ],
            },
        ),
    ]
