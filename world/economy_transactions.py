"""Atomic, exactly-once ownership of Soravelon's durable economy writes."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import timedelta
from numbers import Integral

from django.db import transaction
from django.utils import timezone

from world.economy_ids import new_operation_id
from world.models import (
    BankAccount,
    BankDraft,
    BankTransaction,
    DebtRecord,
    InventoryItem,
    RecurringPayment,
)


MAX_TRANSACTION = 100000


class EconomyOperationConflict(RuntimeError):
    """An idempotency key was reused for a materially different operation."""


def _after_write(checkpoint: str) -> None:
    """Failure-injection seam used by rollback contract tests."""


@contextmanager
def _atomic_character_attributes(character):
    """Reset Evennia's Attribute cache after a database rollback."""

    original_carried_scales = character.db.carried_scales
    try:
        with transaction.atomic():
            yield
    except Exception:
        from evennia.utils.dbserialize import to_pickle

        character.attributes.reset_cache()
        attribute = character.attributes.get(
            "carried_scales",
            return_obj=True,
        )
        if attribute is not None:
            # The database transaction has already restored this value. The
            # Attribute model instance is shared through Evennia's idmapper,
            # so repair its in-memory pickle without issuing a compensating
            # write outside the transaction.
            attribute.db_value = to_pickle(original_carried_scales)
        raise


def _operation_id(value=None) -> str:
    operation_id = new_operation_id() if value is None else value
    if not isinstance(operation_id, str) or not operation_id.strip():
        raise ValueError("operation_id must be a non-empty string")
    if len(operation_id) > 128:
        raise ValueError("operation_id cannot exceed 128 characters")
    return operation_id


def _validate_amount(amount, *, maximum=MAX_TRANSACTION):
    if isinstance(amount, bool) or not isinstance(amount, Integral) or amount <= 0:
        return False, "Amount must be a positive whole number."
    if amount > maximum:
        return False, f"Cannot transact more than {maximum} Scales at once."
    return True, ""


def _lock_character(character):
    from evennia.objects.models import ObjectDB

    return ObjectDB.objects.select_for_update().get(pk=character.id)


def _get_locked_account(character):
    try:
        return BankAccount.objects.select_for_update().get(
            character_id=character.id,
        )
    except BankAccount.DoesNotExist:
        account = BankAccount.objects.create(
            character_id=character.id,
            balance=0,
        )
        _after_write("bank_account_created")
        return account


def get_or_create_account(character):
    with _atomic_character_attributes(character):
        _lock_character(character)
        return _get_locked_account(character)


def get_balance(character):
    try:
        return BankAccount.objects.get(character_id=character.id).balance
    except BankAccount.DoesNotExist:
        return 0


def _matching_replay(
    *,
    character,
    operation_id,
    transaction_type,
    signed_amount,
    related_id=None,
):
    existing = BankTransaction.objects.select_for_update().filter(
        operation_id=operation_id,
    ).first()
    if not existing:
        return None
    if (
        existing.character_id != character.id
        or existing.transaction_type != transaction_type
        or existing.amount != signed_amount
        or (existing.related_id or None) != (related_id or None)
    ):
        raise EconomyOperationConflict(
            f"operation_id '{operation_id}' was already used for another effect"
        )
    return existing


def _record_transaction(
    *,
    character,
    transaction_type,
    signed_amount,
    balance_after,
    operation_id,
    description="",
    related_id=None,
):
    entry = BankTransaction.objects.create(
        character_id=character.id,
        transaction_type=transaction_type,
        amount=signed_amount,
        balance_after=balance_after,
        description=description,
        related_id=related_id,
        operation_id=operation_id,
    )
    _after_write("ledger_recorded")
    return entry


def deposit(character, amount, description="deposit", *, operation_id=None):
    valid, message = _validate_amount(amount)
    if not valid:
        return False, message
    operation_id = _operation_id(operation_id)

    with _atomic_character_attributes(character):
        _lock_character(character)
        replay = _matching_replay(
            character=character,
            operation_id=operation_id,
            transaction_type="deposit",
            signed_amount=amount,
        )
        if replay:
            return True, (
                f"Deposit already completed. Banked balance: "
                f"{replay.balance_after}."
            )

        account = _get_locked_account(character)
        carried = character.db.carried_scales or 0
        if carried < amount:
            return False, f"You only have {carried} Scales on you."

        character.db.carried_scales = carried - amount
        _after_write("carried_debited")
        account.balance += amount
        account.save(update_fields=["balance", "last_accessed"])
        _after_write("bank_credited")
        _record_transaction(
            character=character,
            transaction_type="deposit",
            signed_amount=amount,
            balance_after=account.balance,
            operation_id=operation_id,
            description=description,
        )

    return True, f"Deposited {amount} Scales. Banked balance: {account.balance}."


def withdraw(character, amount, description="withdrawal", *, operation_id=None):
    valid, message = _validate_amount(amount)
    if not valid:
        return False, message
    operation_id = _operation_id(operation_id)

    with _atomic_character_attributes(character):
        _lock_character(character)
        replay = _matching_replay(
            character=character,
            operation_id=operation_id,
            transaction_type="withdraw",
            signed_amount=-amount,
        )
        if replay:
            return True, (
                f"Withdrawal already completed. Banked balance: "
                f"{replay.balance_after}."
            )

        account = _get_locked_account(character)
        if account.balance < amount:
            return False, (
                f"Insufficient funds. Banked balance: {account.balance} Scales."
            )

        account.balance -= amount
        account.save(update_fields=["balance", "last_accessed"])
        _after_write("bank_debited")
        carried = character.db.carried_scales or 0
        character.db.carried_scales = carried + amount
        _after_write("carried_credited")
        _record_transaction(
            character=character,
            transaction_type="withdraw",
            signed_amount=-amount,
            balance_after=account.balance,
            operation_id=operation_id,
            description=description,
        )

    return True, f"Withdrew {amount} Scales. Banked balance: {account.balance}."


def _debit_bank_locked(
    *,
    character,
    amount,
    transaction_type,
    description,
    related_id,
    operation_id,
):
    replay = _matching_replay(
        character=character,
        operation_id=operation_id,
        transaction_type=transaction_type,
        signed_amount=-amount,
        related_id=related_id,
    )
    if replay:
        return True, replay

    account = _get_locked_account(character)
    if account.balance < amount:
        return False, account
    account.balance -= amount
    account.save(update_fields=["balance", "last_accessed"])
    _after_write("bank_debited")
    entry = _record_transaction(
        character=character,
        transaction_type=transaction_type,
        signed_amount=-amount,
        balance_after=account.balance,
        operation_id=operation_id,
        description=description,
        related_id=related_id,
    )
    return True, entry


def deduct_from_bank(
    character,
    amount,
    transaction_type,
    description="",
    related_id=None,
    *,
    operation_id=None,
):
    valid, message = _validate_amount(amount)
    if not valid:
        return False, message
    operation_id = _operation_id(operation_id)

    with transaction.atomic():
        _lock_character(character)
        success, result = _debit_bank_locked(
            character=character,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            related_id=related_id,
            operation_id=operation_id,
        )
        if not success:
            return False, (
                f"Insufficient funds for {transaction_type}. "
                f"Balance: {result.balance}, required: {amount}."
            )
    return True, f"{amount} Scales deducted ({transaction_type})."


def credit_to_bank(
    character,
    amount,
    transaction_type,
    description="",
    related_id=None,
    *,
    operation_id=None,
):
    valid, message = _validate_amount(amount)
    if not valid:
        return False, message
    operation_id = _operation_id(operation_id)

    with transaction.atomic():
        _lock_character(character)
        replay = _matching_replay(
            character=character,
            operation_id=operation_id,
            transaction_type=transaction_type,
            signed_amount=amount,
            related_id=related_id,
        )
        if replay:
            return True, f"{amount} Scales already credited ({transaction_type})."
        account = _get_locked_account(character)
        account.balance += amount
        account.save(update_fields=["balance", "last_accessed"])
        _after_write("bank_credited")
        _record_transaction(
            character=character,
            transaction_type=transaction_type,
            signed_amount=amount,
            balance_after=account.balance,
            operation_id=operation_id,
            description=description,
            related_id=related_id,
        )
    return True, f"{amount} Scales credited ({transaction_type})."


def issue_draft(character, amount, *, operation_id=None):
    valid, message = _validate_amount(amount)
    if not valid:
        return False, message
    operation_id = _operation_id(operation_id)

    with transaction.atomic():
        _lock_character(character)
        replay = _matching_replay(
            character=character,
            operation_id=operation_id,
            transaction_type="draft_issued",
            signed_amount=-amount,
        )
        if replay:
            draft = BankDraft.objects.select_for_update().filter(
                operation_id=operation_id,
            ).first()
            if not draft:
                raise EconomyOperationConflict(
                    "draft debit exists without a durable draft record"
                )
            return True, f"Draft for {draft.denomination} Scales already issued."

        account = _get_locked_account(character)
        if account.balance < amount:
            return False, (
                f"Insufficient funds for draft_issued. Balance: "
                f"{account.balance}, required: {amount}."
            )
        account.balance -= amount
        account.save(update_fields=["balance", "last_accessed"])
        _after_write("bank_debited")
        _record_transaction(
            character=character,
            transaction_type="draft_issued",
            signed_amount=-amount,
            balance_after=account.balance,
            operation_id=operation_id,
            description=f"Draft issued for {amount} Scales",
        )

        from world.item_spawner import create_item_from_template

        draft_key = f"draft:{operation_id}"
        draft_item = create_item_from_template(
            {
                "item_id": "consortium_draft",
                "key": "Gnome Consortium Draft",
                "item_type": "draft",
                "weight": 0.01,
                "rarity": "common",
                "value": amount,
                "desc": (
                    f"A crisp Consortium Draft stamped with the value of {amount} "
                    "Scales. Redeemable at any bank or caravan."
                ),
                "denomination": amount,
                "bank_draft_key": draft_key,
            },
            location=character,
        )
        draft_item.tags.add("consortium_draft", category="item_type")
        _after_write("draft_item_created")
        BankDraft.objects.create(
            draft_key=draft_key,
            issuer_character_id=character.id,
            issuer_character_ref=character.id,
            denomination=amount,
            item_id=draft_item.id,
            operation_id=operation_id,
        )
        _after_write("draft_recorded")

    return True, f"Draft for {amount} Scales issued."


def redeem_draft(character, draft_item, *, operation_id=None):
    operation_id = _operation_id(operation_id)
    item_id = getattr(draft_item, "id", None)
    if isinstance(item_id, bool) or not isinstance(item_id, Integral):
        return False, "That Draft has no durable identity."

    with transaction.atomic():
        _lock_character(character)
        draft = BankDraft.objects.select_for_update().filter(item_id=item_id).first()
        if not draft:
            return False, "That is not a registered Consortium Draft."
        if draft.status == "redeemed" and draft.resolution_operation_id == operation_id:
            replay = _matching_replay(
                character=character,
                operation_id=operation_id,
                transaction_type="draft_redeemed",
                signed_amount=draft.denomination,
                related_id=draft.draft_key,
            )
            if not replay:
                raise EconomyOperationConflict(
                    "redeemed draft exists without its ledger operation"
                )
            return True, f"Draft redemption already completed for {draft.denomination} Scales."
        if draft.status != "issued":
            return False, f"That Draft is already {draft.status}."
        if getattr(draft_item, "location", None) != character:
            return False, "That Draft isn't yours."

        replay = _matching_replay(
            character=character,
            operation_id=operation_id,
            transaction_type="draft_redeemed",
            signed_amount=draft.denomination,
            related_id=draft.draft_key,
        )
        if replay:
            raise EconomyOperationConflict(
                "draft redemption ledger exists while the draft is still issued"
            )

        account = _get_locked_account(character)
        account.balance += draft.denomination
        account.save(update_fields=["balance", "last_accessed"])
        _after_write("bank_credited")
        _record_transaction(
            character=character,
            transaction_type="draft_redeemed",
            signed_amount=draft.denomination,
            balance_after=account.balance,
            operation_id=operation_id,
            description=f"Draft {draft.draft_key} redeemed",
            related_id=draft.draft_key,
        )
        draft.status = "redeemed"
        draft.resolved_at = timezone.now()
        draft.resolution_operation_id = operation_id
        draft.redeemed_by_id = character.id
        draft.redeemer_character_ref = character.id
        draft.save(
            update_fields=[
                "status",
                "resolved_at",
                "resolution_operation_id",
                "redeemed_by",
                "redeemer_character_ref",
            ]
        )
        _after_write("draft_resolved")
        InventoryItem.objects.filter(
            character_id=character.id,
            item_id=item_id,
        ).delete()
        _after_write("draft_inventory_unregistered")
        draft_item.delete()
        _after_write("draft_item_deleted")

    return True, f"Draft redeemed. {draft.denomination} Scales added to your account."


def create_debt(character, amount, playtime_seconds):
    valid, message = _validate_amount(amount)
    if not valid:
        return False, message
    if (
        isinstance(playtime_seconds, bool)
        or not isinstance(playtime_seconds, Integral)
        or playtime_seconds < 0
    ):
        return False, "Debt deadline must be a non-negative whole number."

    with transaction.atomic():
        _lock_character(character)
        existing = DebtRecord.objects.select_for_update().filter(
            character_id=character.id,
            status="active",
        ).first()
        if existing:
            return False, (
                f"You already owe {existing.amount} Scales to the underworld."
            )
        DebtRecord.objects.create(
            character_id=character.id,
            amount=amount,
            deadline_playtime_seconds=playtime_seconds,
            status="active",
        )
        _after_write("debt_created")
    return True, f"Debt of {amount} Scales created."


def get_active_debt(character):
    return DebtRecord.objects.filter(
        character_id=character.id,
        status="active",
    ).first()


def pay_debt(character, *, operation_id=None):
    operation_id = _operation_id(operation_id)
    with transaction.atomic():
        _lock_character(character)
        replay = BankTransaction.objects.select_for_update().filter(
            operation_id=operation_id,
        ).first()
        if replay:
            if (
                replay.character_id != character.id
                or replay.transaction_type != "debt_payment"
                or replay.amount >= 0
            ):
                raise EconomyOperationConflict(
                    f"operation_id '{operation_id}' was already used for another effect"
                )
            return True, f"Debt payment of {-replay.amount} Scales already completed."

        debt = DebtRecord.objects.select_for_update().filter(
            character_id=character.id,
            status="active",
        ).first()
        if not debt:
            return False, "You have no outstanding debt."
        success, result = _debit_bank_locked(
            character=character,
            amount=debt.amount,
            transaction_type="debt_payment",
            description="Underworld debt payment",
            related_id=f"debt:{debt.id}",
            operation_id=operation_id,
        )
        if not success:
            return False, f"Insufficient funds. You owe {debt.amount} Scales."
        debt.status = "paid"
        debt.resolved_at = timezone.now()
        debt.save(update_fields=["status", "resolved_at"])
        _after_write("debt_resolved")
    return True, f"Debt of {debt.amount} Scales paid. You're clear."


def decrement_debt_timer(character, seconds_played):
    if (
        isinstance(seconds_played, bool)
        or not isinstance(seconds_played, Integral)
        or seconds_played < 0
    ):
        raise ValueError("seconds_played must be a non-negative whole number")
    with transaction.atomic():
        debt = DebtRecord.objects.select_for_update().filter(
            character_id=character.id,
            status="active",
        ).first()
        if not debt:
            return None
        debt.deadline_playtime_seconds = max(
            0,
            debt.deadline_playtime_seconds - seconds_played,
        )
        if debt.deadline_playtime_seconds == 0:
            debt.status = "hunted"
            debt.resolved_at = timezone.now()
            debt.save(
                update_fields=[
                    "deadline_playtime_seconds",
                    "status",
                    "resolved_at",
                ]
            )
            transaction.on_commit(
                lambda: character.msg(
                    "|rYou hear a whistle in the distance. "
                    "The deadline has passed.|n"
                )
            )
            return 0
        debt.save(update_fields=["deadline_playtime_seconds"])
        return debt.deadline_playtime_seconds


def _live_character(character_id):
    from evennia.objects.models import ObjectDB

    try:
        return ObjectDB.objects.get(pk=character_id)
    except ObjectDB.DoesNotExist:
        return None


def process_recurring_payments():
    now = timezone.now()
    due_ids = list(
        RecurringPayment.objects.filter(
            active=True,
            lapsed=False,
            next_due__lte=now,
        ).values_list("id", flat=True)
    )
    for payment_id in due_ids:
        with transaction.atomic():
            payment = RecurringPayment.objects.select_for_update().filter(
                pk=payment_id,
                active=True,
                lapsed=False,
                next_due__lte=now,
            ).first()
            if not payment:
                continue
            character = _live_character(payment.character_id)
            if not character:
                continue
            _lock_character(character)
            operation_id = (
                f"recurring:{payment.id}:"
                f"{payment.next_due.isoformat()}"
            )
            success, _result = _debit_bank_locked(
                character=character,
                amount=payment.amount,
                transaction_type=payment.payment_type,
                description=f"Recurring {payment.payment_type}",
                related_id=str(payment.id),
                operation_id=operation_id,
            )
            if success:
                payment.next_due = now + timedelta(days=payment.interval_days)
                payment.grace_until = None
                payment.save(update_fields=["next_due", "grace_until"])
                transaction.on_commit(
                    lambda c=character, p=payment: c.msg(
                        f"|g{p.amount} Scales deducted for {p.payment_type}. "
                        "Coverage renewed.|n"
                    )
                )
            elif not payment.grace_until:
                payment.grace_until = now + timedelta(days=payment.interval_days)
                payment.save(update_fields=["grace_until"])
                transaction.on_commit(
                    lambda c=character, p=payment: c.msg(
                        f"|yInsufficient funds for {p.payment_type}. Coverage "
                        f"continues for {p.interval_days} more days. Deposit "
                        "Scales to maintain coverage.|n"
                    )
                )
            elif now >= payment.grace_until:
                payment.lapsed = True
                payment.active = False
                payment.save(update_fields=["lapsed", "active"])
                transaction.on_commit(
                    lambda c=character, p=payment: c.msg(
                        f"|r{p.payment_type} coverage has lapsed. Visit a bank "
                        "to reinstate.|n"
                    )
                )
