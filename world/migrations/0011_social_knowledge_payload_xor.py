"""Keep authoritative facts separate from claims a social node believes."""

from django.db import migrations, models


def keep_claim_only_for_ambiguous_knowledge(apps, schema_editor):
    """Conservatively remove inferred fact knowledge from legacy dual rows.

    Before this migration, ``mark_known`` attached ``claim.fact`` to the same
    knowledge row even when callers supplied only a claim. Existing rows cannot
    prove that the node learned the authoritative fact independently, so the
    safe migration is to retain the claim and clear the fact link.
    """

    SocialKnowledge = apps.get_model("world", "SocialKnowledge")
    SocialKnowledge.objects.filter(
        fact__isnull=False,
        claim__isnull=False,
    ).update(fact=None)


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0010_reconcile_world_schema"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="socialknowledge",
            name="social_knowledge_has_fact_or_claim",
        ),
        migrations.RunPython(
            keep_claim_only_for_ambiguous_knowledge,
            migrations.RunPython.noop,
        ),
        migrations.AddConstraint(
            model_name="socialknowledge",
            constraint=models.CheckConstraint(
                condition=(
                    models.Q(("claim__isnull", True), ("fact__isnull", False))
                    | models.Q(("claim__isnull", False), ("fact__isnull", True))
                ),
                name="social_knowledge_exactly_one_payload",
            ),
        ),
    ]
