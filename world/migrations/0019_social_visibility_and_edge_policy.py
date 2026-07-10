"""Make claim visibility and edge tag policy explicit and durable."""

from django.db import migrations, models


def _normalize_tags(values):
    seen = set()
    normalized = []
    for value in values or []:
        tag = str(value).strip().lower().replace(" ", "_")
        if tag and tag not in seen:
            seen.add(tag)
            normalized.append(tag)
    return normalized


def copy_legacy_blockers_to_required_tags(apps, schema_editor):
    SocialEdge = apps.get_model("world", "SocialEdge")
    for edge in SocialEdge.objects.iterator():
        SocialEdge.objects.filter(pk=edge.pk).update(
            blockers=_normalize_tags(edge.blockers),
            required_tags=_normalize_tags(edge.blockers),
            blocked_tags=[],
        )


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0018_social_trace_route_key"),
    ]

    operations = [
        migrations.AddField(
            model_name="socialclaim",
            name="expires_at",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="socialclaim",
            name="visibility",
            field=models.CharField(
                choices=[
                    ("private", "Private"),
                    ("witnessed", "Witnessed"),
                    ("local", "Local"),
                    ("institutional", "Institutional"),
                    ("route", "Route"),
                    ("global", "Global"),
                ],
                db_index=True,
                default="local",
                max_length=16,
            ),
        ),
        migrations.AddField(
            model_name="socialedge",
            name="blocked_tags",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="socialedge",
            name="required_tags",
            field=models.JSONField(default=list),
        ),
        migrations.RunPython(
            copy_legacy_blockers_to_required_tags,
            migrations.RunPython.noop,
        ),
    ]
