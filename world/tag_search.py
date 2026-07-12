"""Indexed exact-tag reads for internal world identifiers."""


def search_objects_by_exact_tag(key, category):
    """Return ObjectDB matches for one normalized internal tag identity.

    Evennia's general multi-tag matcher aggregates tags across every object.
    Soravelon's authored IDs and categories are exact normalized identifiers,
    so a direct relation query preserves their case-insensitive contract while
    avoiding that world-scale aggregate.
    """
    from evennia.objects.models import ObjectDB

    return ObjectDB.objects.filter(
        db_tags__db_key=str(key).strip().casefold(),
        db_tags__db_category=str(category).strip().casefold(),
        db_tags__db_model="objectdb",
        db_tags__db_tagtype__isnull=True,
    ).distinct().order_by("id")
