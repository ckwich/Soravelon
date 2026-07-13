from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("world", "0027_guildrecruitment"),
    ]

    operations = [
        migrations.AddField(
            model_name="characterquest",
            name="accepted_spec",
            field=models.JSONField(default=dict),
        ),
    ]
