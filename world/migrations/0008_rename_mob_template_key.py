from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('world', '0007_merge_20260326_2012'),
    ]
    operations = [
        migrations.RenameField(
            model_name='spawnrecord',
            old_name='mob_template',
            new_name='mob_template_key',
        ),
    ]
