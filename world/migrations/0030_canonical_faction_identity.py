from django.db import migrations


STANDING_MIN = -100000
STANDING_MAX = 100000
FACTION_ALIASES = {
    "warden": "wardens",
}


def canonicalize_faction_relationships(apps, schema_editor):
    """Merge legacy alias rows into canonical relationship identities."""
    FactionStanding = apps.get_model("world", "FactionStanding")
    database = schema_editor.connection.alias

    for alias, canonical in FACTION_ALIASES.items():
        alias_rows = list(
            FactionStanding.objects.using(database)
            .filter(faction_id=alias)
            .order_by("pk")
        )
        for alias_row in alias_rows:
            canonical_row = (
                FactionStanding.objects.using(database)
                .filter(
                    character_id=alias_row.character_id,
                    faction_id=canonical,
                    subfaction_id=alias_row.subfaction_id,
                )
                .first()
            )
            if canonical_row is None:
                FactionStanding.objects.using(database).filter(
                    pk=alias_row.pk
                ).update(faction_id=canonical)
                continue

            combined_standing = max(
                STANDING_MIN,
                min(
                    STANDING_MAX,
                    canonical_row.standing + alias_row.standing,
                ),
            )
            FactionStanding.objects.using(database).filter(
                pk=canonical_row.pk
            ).update(
                standing=combined_standing,
                trust=max(canonical_row.trust, alias_row.trust),
                betrayal_flag=(
                    canonical_row.betrayal_flag or alias_row.betrayal_flag
                ),
                last_updated=max(
                    canonical_row.last_updated,
                    alias_row.last_updated,
                ),
            )
            FactionStanding.objects.using(database).filter(
                pk=alias_row.pk
            ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("world", "0029_questshareoffer"),
    ]

    operations = [
        migrations.RunPython(
            canonicalize_faction_relationships,
            migrations.RunPython.noop,
        ),
    ]
