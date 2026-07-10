"""Give every SocialTrace route a durable idempotency identity."""

import hashlib

from django.db import migrations, models


def _route_key(trace):
    payload = "|".join(
        str(value or 0)
        for value in (
            trace.knowledge_id,
            trace.from_node_id,
            trace.to_node_id,
            trace.edge_id,
        )
    )
    return f"route:{hashlib.sha256(payload.encode('utf-8')).hexdigest()}"


def backfill_route_keys(apps, schema_editor):
    SocialTrace = apps.get_model("world", "SocialTrace")
    seen = {}
    for trace in SocialTrace.objects.order_by("pk").iterator():
        route_key = _route_key(trace)
        if route_key in seen:
            raise RuntimeError(
                "social_trace_duplicate_route: "
                f"{seen[route_key]}, {trace.pk}"
            )
        seen[route_key] = trace.pk
        SocialTrace.objects.filter(pk=trace.pk).update(route_key=route_key)


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0017_character_access_grant"),
    ]

    operations = [
        migrations.AddField(
            model_name="socialtrace",
            name="route_key",
            field=models.CharField(blank=True, max_length=72, null=True),
        ),
        migrations.RunPython(backfill_route_keys, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="socialtrace",
            name="route_key",
            field=models.CharField(max_length=72, unique=True),
        ),
        migrations.AddConstraint(
            model_name="socialtrace",
            constraint=models.CheckConstraint(
                condition=models.Q(route_key__gt=""),
                name="social_trace_route_key_nonempty",
            ),
        ),
    ]
