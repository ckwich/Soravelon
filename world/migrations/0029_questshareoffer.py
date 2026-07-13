import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("world", "0028_characterquest_accepted_spec"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuestShareOffer",
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
                ("quest_id", models.CharField(db_index=True, max_length=128)),
                ("quest_spec", models.JSONField(default=dict)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("accepted", "Accepted"),
                            ("declined", "Declined"),
                            ("expired", "Expired"),
                        ],
                        default="pending",
                        max_length=16,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("responded_at", models.DateTimeField(blank=True, null=True)),
                (
                    "accepted_quest",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="accepted_share_offer",
                        to="world.characterquest",
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_quest_share_offers",
                        to="objects.objectdb",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_quest_share_offers",
                        to="objects.objectdb",
                    ),
                ),
                (
                    "source_quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="share_offers",
                        to="world.characterquest",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["recipient", "status"],
                        name="quest_share_recipient_idx",
                    ),
                    models.Index(
                        fields=["source_quest", "status"],
                        name="quest_share_source_idx",
                    ),
                ],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("source_quest", "recipient"),
                        name="unique_quest_share_recipient",
                    ),
                    models.CheckConstraint(
                        condition=~models.Q(sender=models.F("recipient")),
                        name="quest_share_sender_not_recipient",
                    ),
                    models.CheckConstraint(
                        condition=(
                            models.Q(
                                status="pending",
                                responded_at__isnull=True,
                                accepted_quest__isnull=True,
                            )
                            | models.Q(
                                status="accepted",
                                responded_at__isnull=False,
                                accepted_quest__isnull=False,
                            )
                            | models.Q(
                                status__in=("declined", "expired"),
                                responded_at__isnull=False,
                                accepted_quest__isnull=True,
                            )
                        ),
                        name="quest_share_response_consistent",
                    ),
                ],
            },
        ),
    ]
