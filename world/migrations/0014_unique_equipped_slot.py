"""Prevent contradictory equipment occupancy at the database boundary."""

from django.db import migrations, models
from django.db.models import Count


def audit_equipped_slots(apps, schema_editor):
    InventoryItem = apps.get_model("world", "InventoryItem")
    duplicate_slots = list(
        InventoryItem.objects.filter(is_equipped=True)
        .values("character_id", "equipment_slot")
        .annotate(row_count=Count("id"))
        .filter(row_count__gt=1)
        .values_list("character_id", "equipment_slot")
    )
    if not duplicate_slots:
        return

    ids = []
    for character_id, equipment_slot in duplicate_slots:
        ids.extend(
            InventoryItem.objects.filter(
                character_id=character_id,
                equipment_slot=equipment_slot,
                is_equipped=True,
            ).values_list("pk", flat=True)
        )
    raise RuntimeError(
        "Equipment-slot integrity audit failed before constraint: "
        f"duplicate_equipped_slot:count={len(ids)}:ids={sorted(ids)[:100]}"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0013_recurring_payment_integrity"),
    ]

    operations = [
        migrations.RunPython(
            audit_equipped_slots,
            migrations.RunPython.noop,
        ),
        migrations.AddConstraint(
            model_name="inventoryitem",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_equipped", True)),
                fields=("character", "equipment_slot"),
                name="unique_equipped_slot",
            ),
        ),
    ]
