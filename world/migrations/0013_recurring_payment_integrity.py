"""Make recurring-payment identity and numeric invariants durable."""

from django.db import migrations, models
from django.db.models import Count


def _record_issue(issues, name, queryset):
    count = queryset.count()
    if not count:
        return
    ids = list(queryset.order_by("pk").values_list("pk", flat=True)[:100])
    issues.append(f"{name}:count={count}:ids={ids}")


def audit_recurring_payment_state(apps, schema_editor):
    """Refuse to guess how contradictory player contracts should be merged."""

    RecurringPayment = apps.get_model("world", "RecurringPayment")
    issues = []
    _record_issue(
        issues,
        "recurring_nonpositive_amount",
        RecurringPayment.objects.filter(amount__lte=0),
    )
    _record_issue(
        issues,
        "recurring_nonpositive_interval",
        RecurringPayment.objects.filter(interval_days__lte=0),
    )

    duplicate_keys = list(
        RecurringPayment.objects.values("character_id", "payment_type")
        .annotate(row_count=Count("id"))
        .filter(row_count__gt=1)
        .values_list("character_id", "payment_type")
    )
    for character_id, payment_type in duplicate_keys:
        _record_issue(
            issues,
            "recurring_duplicate_contract",
            RecurringPayment.objects.filter(
                character_id=character_id,
                payment_type=payment_type,
            ),
        )

    if issues:
        raise RuntimeError(
            "Recurring-payment integrity audit failed before constraints: "
            + "; ".join(issues)
        )


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0012_economy_integrity_schema"),
    ]

    operations = [
        migrations.RunPython(
            audit_recurring_payment_state,
            migrations.RunPython.noop,
        ),
        migrations.AddConstraint(
            model_name="recurringpayment",
            constraint=models.UniqueConstraint(
                fields=("character", "payment_type"),
                name="unique_recurring_payment",
            ),
        ),
        migrations.AddConstraint(
            model_name="recurringpayment",
            constraint=models.CheckConstraint(
                condition=models.Q(("amount__gt", 0)),
                name="recurring_amount_positive",
            ),
        ),
        migrations.AddConstraint(
            model_name="recurringpayment",
            constraint=models.CheckConstraint(
                condition=models.Q(("interval_days__gt", 0)),
                name="recurring_interval_positive",
            ),
        ),
    ]
