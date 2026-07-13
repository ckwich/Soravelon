from django.db import migrations, models


def create_deployment_lock(apps, schema_editor):
    lock = apps.get_model("world", "WorldContentDeploymentLock")
    lock.objects.get_or_create(pk=1)


class Migration(migrations.Migration):
    dependencies = [
        ("world", "0024_world_content_revision"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worldcontentrevision",
            name="manifest_hash",
            field=models.CharField(db_index=True, max_length=64),
        ),
        migrations.CreateModel(
            name="WorldContentDeploymentLock",
            fields=[
                (
                    "id",
                    models.PositiveSmallIntegerField(
                        default=1, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RunPython(create_deployment_lock, migrations.RunPython.noop),
    ]
