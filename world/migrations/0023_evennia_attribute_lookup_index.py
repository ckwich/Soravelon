from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("world", "0022_encounter_reward"),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                "CREATE INDEX IF NOT EXISTS soravelon_attr_identity_ci_idx "
                "ON typeclasses_attribute "
                "(UPPER(db_key), UPPER(db_model)) "
                "WHERE db_attrtype IS NULL AND db_category IS NULL"
            ),
            reverse_sql=(
                "DROP INDEX IF EXISTS soravelon_attr_identity_ci_idx"
            ),
        ),
    ]
