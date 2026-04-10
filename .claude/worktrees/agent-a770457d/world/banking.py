"""
Banking engine for Soravelon.
Deposit, withdraw, recurring payments, Consortium Drafts, debt management.
All balance modifications create immutable BankTransaction records.
"""

import evennia
from django.utils import timezone
from django.db.models import Q, F
from datetime import timedelta
from world.models import BankAccount, BankTransaction, RecurringPayment, DebtRecord


def get_or_create_account(character):
    account, created = BankAccount.objects.get_or_create(
        character_id=character.id,
        defaults={"balance": 0}
    )
    return account


def get_balance(character):
    try:
        return BankAccount.objects.get(character_id=character.id).balance
    except BankAccount.DoesNotExist:
        return 0


def deposit(character, amount, description="deposit"):
    if amount <= 0:
        return False, "Amount must be positive."
    carried = getattr(character.db, 'carried_scales', 0) or 0
    if carried < amount:
        return False, f"You only have {carried} Scales on you."
    account = get_or_create_account(character)
    character.db.carried_scales = carried - amount
    # Atomic balance update via F() — safe against concurrent modifications
    BankAccount.objects.filter(id=account.id).update(balance=F('balance') + amount)
    account.refresh_from_db()
    _record_transaction(character.id, "deposit", amount, account.balance, description)
    return True, f"Deposited {amount} Scales. Banked balance: {account.balance}."


def withdraw(character, amount, description="withdrawal"):
    if amount <= 0:
        return False, "Amount must be positive."
    account = get_or_create_account(character)
    # Atomic check-and-deduct: balance__gte ensures no overdraft even under
    # concurrent access. If rows_updated==0, balance was insufficient.
    rows_updated = BankAccount.objects.filter(
        id=account.id, balance__gte=amount
    ).update(balance=F('balance') - amount)
    if not rows_updated:
        account.refresh_from_db()
        return False, f"Insufficient funds. Banked balance: {account.balance} Scales."
    account.refresh_from_db()
    carried = getattr(character.db, 'carried_scales', 0) or 0
    character.db.carried_scales = carried + amount
    _record_transaction(character.id, "withdraw", -amount, account.balance, description)
    return True, f"Withdrew {amount} Scales. Banked balance: {account.balance}."


def deduct_from_bank(character, amount, transaction_type, description="", related_id=None):
    if amount <= 0:
        return False, "Amount must be positive."
    account = get_or_create_account(character)
    # Atomic check-and-deduct: balance__gte ensures no overdraft
    rows_updated = BankAccount.objects.filter(
        id=account.id, balance__gte=amount
    ).update(balance=F('balance') - amount)
    if not rows_updated:
        account.refresh_from_db()
        return False, (
            f"Insufficient funds for {transaction_type}. "
            f"Balance: {account.balance}, required: {amount}."
        )
    account.refresh_from_db()
    _record_transaction(character.id, transaction_type, -amount, account.balance, description, related_id)
    return True, f"{amount} Scales deducted ({transaction_type})."


def credit_to_bank(character, amount, transaction_type, description="", related_id=None):
    if amount <= 0:
        return False, "Amount must be positive."
    account = get_or_create_account(character)
    # Atomic balance update via F()
    BankAccount.objects.filter(id=account.id).update(balance=F('balance') + amount)
    account.refresh_from_db()
    _record_transaction(character.id, transaction_type, amount, account.balance, description, related_id)
    return True, f"{amount} Scales credited ({transaction_type})."


def _record_transaction(character_id, transaction_type, amount, balance_after, description="", related_id=None):
    BankTransaction.objects.create(
        character_id=character_id,
        transaction_type=transaction_type,
        amount=amount,
        balance_after=balance_after,
        description=description,
        related_id=related_id
    )


def setup_recurring_payment(character, payment_type, amount, interval_days=7):
    next_due = timezone.now() + timedelta(days=interval_days)
    payment, created = RecurringPayment.objects.update_or_create(
        character_id=character.id,
        payment_type=payment_type,
        defaults={
            "amount": amount,
            "interval_days": interval_days,
            "next_due": next_due,
            "active": True,
            "grace_until": None,
            "lapsed": False,
        }
    )
    return payment


def cancel_recurring_payment(character, payment_type):
    updated = RecurringPayment.objects.filter(
        character_id=character.id,
        payment_type=payment_type,
        active=True
    ).update(active=False)
    return updated > 0


def has_active_coverage(character, payment_type):
    now = timezone.now()
    return RecurringPayment.objects.filter(
        character_id=character.id,
        payment_type=payment_type,
        active=True,
        lapsed=False
    ).filter(
        Q(next_due__gt=now) | Q(grace_until__gt=now)
    ).exists()


def process_recurring_payments():
    now = timezone.now()
    due_payments = RecurringPayment.objects.filter(
        active=True, lapsed=False, next_due__lte=now
    )
    for payment in due_payments:
        chars = evennia.search_object("#" + str(payment.character_id))
        if not chars:
            continue
        character = chars[0]
        success, _ = deduct_from_bank(
            character, payment.amount,
            transaction_type=payment.payment_type,
            description=f"Recurring {payment.payment_type}",
            related_id=str(payment.id)
        )
        if success:
            payment.next_due = now + timedelta(days=payment.interval_days)
            payment.grace_until = None
            payment.save()
            if hasattr(character, 'msg'):
                character.msg(
                    f"|g{payment.amount} Scales deducted for "
                    f"{payment.payment_type}. Coverage renewed.|n"
                )
        else:
            if not payment.grace_until:
                payment.grace_until = now + timedelta(days=payment.interval_days)
                payment.save()
                if hasattr(character, 'msg'):
                    character.msg(
                        f"|yInsufficient funds for {payment.payment_type}. "
                        f"Coverage continues for {payment.interval_days} "
                        f"more days. Deposit Scales to maintain coverage.|n"
                    )
            else:
                if now >= payment.grace_until:
                    payment.lapsed = True
                    payment.active = False
                    payment.save()
                    if hasattr(character, 'msg'):
                        character.msg(
                            f"|r{payment.payment_type} coverage has lapsed. "
                            f"Visit a bank to reinstate.|n"
                        )


def issue_draft(character, amount):
    success, msg = deduct_from_bank(
        character, amount,
        transaction_type="draft_issued",
        description=f"Draft issued for {amount} Scales"
    )
    if not success:
        return False, msg
    from evennia import create_object
    from typeclasses.objects import SoravelonItem
    draft = create_object(SoravelonItem, key="Gnome Consortium Draft", location=character)
    draft.db.item_type = "draft"
    draft.db.denomination = amount
    draft.db.stackable = False
    draft.db.weight = 0.01
    draft.db.rarity = "common"
    draft.db.desc = f"A crisp Consortium Draft stamped with the value of {amount} Scales. Redeemable at any bank or caravan."
    draft.tags.add("consortium_draft", category="item_type")
    from world.models import InventoryItem
    InventoryItem.objects.create(character_id=character.id, item_id=draft.id, quantity=1)
    return True, f"Draft for {amount} Scales issued."


def redeem_draft(character, draft_item):
    if getattr(draft_item.db, 'item_type', None) != "draft":
        return False, "That's not a Consortium Draft."
    # Verify the draft is in the redeemer's inventory
    if draft_item.location != character:
        return False, "That Draft isn't yours."
    denomination = (draft_item.db.denomination or 0)
    if denomination <= 0:
        return False, "That Draft has no value."
    account = get_or_create_account(character)
    # Atomic balance update via F()
    BankAccount.objects.filter(id=account.id).update(balance=F('balance') + denomination)
    account.refresh_from_db()
    _record_transaction(character.id, "draft_redeemed", denomination, account.balance, f"Draft #{draft_item.id} redeemed")
    from world.models import InventoryItem
    InventoryItem.objects.filter(character_id=character.id, item_id=draft_item.id).delete()
    draft_item.delete()
    return True, f"Draft redeemed. {denomination} Scales added to your account."


def create_debt(character, amount, playtime_seconds):
    existing = DebtRecord.objects.filter(character_id=character.id, status="active").first()
    if existing:
        return False, f"You already owe {existing.amount} Scales to the underworld."
    DebtRecord.objects.create(
        character_id=character.id,
        amount=amount,
        deadline_playtime_seconds=playtime_seconds,
        status="active"
    )
    return True, f"Debt of {amount} Scales created."


def get_active_debt(character):
    return DebtRecord.objects.filter(character_id=character.id, status="active").first()


def pay_debt(character):
    debt = get_active_debt(character)
    if not debt:
        return False, "You have no outstanding debt."
    success, msg = deduct_from_bank(
        character, debt.amount,
        transaction_type="debt_payment",
        description="Underworld debt payment"
    )
    if not success:
        return False, f"Insufficient funds. You owe {debt.amount} Scales."
    debt.status = "paid"
    debt.resolved_at = timezone.now()
    debt.save()
    return True, f"Debt of {debt.amount} Scales paid. You're clear."


def decrement_debt_timer(character, seconds_played):
    debt = get_active_debt(character)
    if not debt:
        return None
    debt.deadline_playtime_seconds = max(0, debt.deadline_playtime_seconds - seconds_played)
    if debt.deadline_playtime_seconds <= 0:
        debt.status = "hunted"
        debt.resolved_at = timezone.now()
        debt.save()
        if hasattr(character, 'msg'):
            character.msg("|rYou hear a whistle in the distance. The deadline has passed.|n")
        return 0
    debt.save()
    return debt.deadline_playtime_seconds


def banking_payment_tick(*args, **kwargs):
    process_recurring_payments()


def on_character_death(character, location):
    pass  # STUB


def handle_carried_scales_on_death(character):
    pass  # STUB
