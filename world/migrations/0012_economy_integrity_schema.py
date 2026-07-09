"""Add fail-closed economy and inventory integrity foundations."""

import django.db.models.deletion
from django.db import migrations, models
from django.db.models import Count, Q

import world.economy_ids


def _record_issue(issues, name, queryset):
    count = queryset.count()
    if not count:
        return
    ids = list(queryset.order_by("pk").values_list("pk", flat=True)[:100])
    issues.append(f"{name}:count={count}:ids={ids}")


def audit_legacy_economy_state(apps, schema_editor):
    """Abort on contradictions rather than mutating player-owned state."""

    BankAccount = apps.get_model("world", "BankAccount")
    BankTransaction = apps.get_model("world", "BankTransaction")
    DebtRecord = apps.get_model("world", "DebtRecord")
    InventoryItem = apps.get_model("world", "InventoryItem")

    issues = []
    _record_issue(
        issues,
        "bank_account_negative_balance",
        BankAccount.objects.filter(balance__lt=0),
    )
    _record_issue(
        issues,
        "bank_transaction_zero_amount",
        BankTransaction.objects.filter(amount=0),
    )
    _record_issue(
        issues,
        "bank_transaction_negative_balance_after",
        BankTransaction.objects.filter(balance_after__lt=0),
    )
    _record_issue(
        issues,
        "debt_nonpositive_amount",
        DebtRecord.objects.filter(amount__lte=0),
    )
    _record_issue(
        issues,
        "debt_negative_deadline",
        DebtRecord.objects.filter(deadline_playtime_seconds__lt=0),
    )
    duplicate_active_characters = list(
        DebtRecord.objects.filter(status="active")
        .values("character_id")
        .annotate(row_count=Count("id"))
        .filter(row_count__gt=1)
        .values_list("character_id", flat=True)
    )
    if duplicate_active_characters:
        duplicate_debts = DebtRecord.objects.filter(
            status="active",
            character_id__in=duplicate_active_characters,
        )
        _record_issue(issues, "debt_multiple_active", duplicate_debts)

    _record_issue(
        issues,
        "inventory_nonpositive_quantity",
        InventoryItem.objects.filter(quantity__lte=0),
    )
    _record_issue(
        issues,
        "inventory_invalid_equipped_state",
        InventoryItem.objects.filter(is_equipped=True).filter(
            Q(equipment_slot__isnull=True)
            | Q(equipment_slot="")
            | Q(container_id__isnull=False)
        ),
    )
    _record_issue(
        issues,
        "inventory_slot_while_unequipped",
        InventoryItem.objects.filter(
            is_equipped=False,
            equipment_slot__isnull=False,
        ),
    )

    if issues:
        raise RuntimeError(
            "Economy integrity audit failed before constraints: "
            + "; ".join(issues)
        )


def backfill_bank_transaction_operation_ids(apps, schema_editor):
    BankTransaction = apps.get_model("world", "BankTransaction")
    for transaction in BankTransaction.objects.filter(
        operation_id__isnull=True,
    ).iterator():
        BankTransaction.objects.filter(pk=transaction.pk).update(
            operation_id=f"legacy-bank-transaction-{transaction.pk}",
        )


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0011_social_knowledge_payload_xor"),
    ]

    operations = [
        migrations.CreateModel(
            name="BankDraft",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("draft_key", models.CharField(max_length=160, unique=True)),
                ("issuer_character_ref", models.BigIntegerField()),
                ("denomination", models.IntegerField()),
                ("item_id", models.BigIntegerField(unique=True)),
                (
                    "operation_id",
                    models.CharField(
                        default=world.economy_ids.new_operation_id,
                        editable=False,
                        max_length=128,
                        unique=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("issued", "Issued"),
                            ("redeemed", "Redeemed"),
                            ("void", "Void"),
                        ],
                        default="issued",
                        max_length=16,
                    ),
                ),
                ("issued_at", models.DateTimeField(auto_now_add=True)),
                ("resolved_at", models.DateTimeField(blank=True, null=True)),
                (
                    "resolution_operation_id",
                    models.CharField(
                        blank=True,
                        max_length=128,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "redeemer_character_ref",
                    models.BigIntegerField(blank=True, null=True),
                ),
                (
                    "issuer_character",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="issued_bank_drafts",
                        to="objects.objectdb",
                    ),
                ),
                (
                    "redeemed_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="redeemed_bank_drafts",
                        to="objects.objectdb",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["issuer_character", "status"],
                        name="world_draft_issuer_status_idx",
                    ),
                    models.Index(
                        fields=["status", "issued_at"],
                        name="world_draft_status_issued_idx",
                    ),
                ],
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(denomination__gt=0),
                        name="bank_draft_amount_positive",
                    ),
                    models.CheckConstraint(
                        condition=(
                            models.Q(
                                status="issued",
                                resolved_at__isnull=True,
                                resolution_operation_id__isnull=True,
                                redeemer_character_ref__isnull=True,
                            )
                            | models.Q(
                                status="redeemed",
                                resolved_at__isnull=False,
                                resolution_operation_id__isnull=False,
                                redeemer_character_ref__isnull=False,
                            )
                            | models.Q(
                                status="void",
                                resolved_at__isnull=False,
                                resolution_operation_id__isnull=False,
                                redeemer_character_ref__isnull=True,
                            )
                        ),
                        name="bank_draft_state_coherent",
                    ),
                    models.CheckConstraint(
                        condition=(
                            (
                                models.Q(issuer_character__isnull=True)
                                | models.Q(
                                    issuer_character_id=models.F(
                                        "issuer_character_ref"
                                    )
                                )
                            )
                            & (
                                models.Q(redeemed_by__isnull=True)
                                | models.Q(
                                    redeemed_by_id=models.F(
                                        "redeemer_character_ref"
                                    )
                                )
                            )
                        ),
                        name="bank_draft_actor_refs_match",
                    ),
                ],
            },
        ),
        migrations.AddField(
            model_name="banktransaction",
            name="operation_id",
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.RunPython(
            audit_legacy_economy_state,
            migrations.RunPython.noop,
        ),
        migrations.RunPython(
            backfill_bank_transaction_operation_ids,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="banktransaction",
            name="operation_id",
            field=models.CharField(
                default=world.economy_ids.new_operation_id,
                editable=False,
                max_length=128,
                unique=True,
            ),
        ),
        migrations.AddConstraint(
            model_name="bankaccount",
            constraint=models.CheckConstraint(
                condition=models.Q(balance__gte=0),
                name="bank_balance_nonnegative",
            ),
        ),
        migrations.AddConstraint(
            model_name="banktransaction",
            constraint=models.CheckConstraint(
                condition=~models.Q(amount=0),
                name="bank_tx_amount_nonzero",
            ),
        ),
        migrations.AddConstraint(
            model_name="banktransaction",
            constraint=models.CheckConstraint(
                condition=models.Q(balance_after__gte=0),
                name="bank_tx_balance_nonnegative",
            ),
        ),
        migrations.AddConstraint(
            model_name="debtrecord",
            constraint=models.UniqueConstraint(
                condition=models.Q(status="active"),
                fields=("character",),
                name="unique_active_debt",
            ),
        ),
        migrations.AddConstraint(
            model_name="debtrecord",
            constraint=models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name="debt_amount_positive",
            ),
        ),
        migrations.AddConstraint(
            model_name="debtrecord",
            constraint=models.CheckConstraint(
                condition=models.Q(deadline_playtime_seconds__gte=0),
                name="debt_deadline_nonnegative",
            ),
        ),
        migrations.AddConstraint(
            model_name="inventoryitem",
            constraint=models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="inventory_quantity_positive",
            ),
        ),
        migrations.AddConstraint(
            model_name="inventoryitem",
            constraint=models.CheckConstraint(
                condition=(
                    models.Q(
                        is_equipped=False,
                        equipment_slot__isnull=True,
                    )
                    | (
                        models.Q(
                            is_equipped=True,
                            equipment_slot__isnull=False,
                            container_id__isnull=True,
                        )
                        & ~models.Q(equipment_slot="")
                    )
                ),
                name="inventory_equipment_state",
            ),
        ),
    ]
