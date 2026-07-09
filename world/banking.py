"""Banking facade and non-ledger lifecycle helpers for Soravelon.

All durable money, draft, debt-payment, and recurring-charge writes are owned
by ``world.economy_transactions``. This module keeps the established caller
Interface and the coverage/death helpers that do not belong in that deep
transaction module.
"""

from __future__ import annotations

from datetime import timedelta
from numbers import Integral

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from world.economy_transactions import (
    MAX_TRANSACTION,
    create_debt,
    credit_to_bank,
    decrement_debt_timer,
    deduct_from_bank,
    deposit,
    get_active_debt,
    get_balance,
    get_or_create_account,
    issue_draft,
    pay_debt,
    process_recurring_payments,
    redeem_draft,
    withdraw,
)
from world.models import RecurringPayment


def setup_recurring_payment(character, payment_type, amount, interval_days=7):
    """Create or replace one recurring coverage contract atomically."""

    if not isinstance(payment_type, str) or not payment_type.strip():
        raise ValueError("payment_type must be a non-empty string")
    if isinstance(amount, bool) or not isinstance(amount, Integral) or amount <= 0:
        raise ValueError("recurring amount must be a positive whole number")
    if (
        isinstance(interval_days, bool)
        or not isinstance(interval_days, Integral)
        or interval_days <= 0
    ):
        raise ValueError("interval_days must be a positive whole number")

    next_due = timezone.now() + timedelta(days=interval_days)
    with transaction.atomic():
        from evennia.objects.models import ObjectDB

        # Serialize the empty-row case as well as updates. Locking only a
        # RecurringPayment row cannot prevent two first-time setup requests
        # from racing to create the same contract.
        ObjectDB.objects.select_for_update().get(pk=character.id)
        payment = RecurringPayment.objects.select_for_update().filter(
            character_id=character.id,
            payment_type=payment_type,
        ).first()
        if payment is None:
            payment = RecurringPayment(
                character_id=character.id,
                payment_type=payment_type,
            )
        payment.amount = amount
        payment.interval_days = interval_days
        payment.next_due = next_due
        payment.active = True
        payment.grace_until = None
        payment.lapsed = False
        payment.save()
    return payment


def cancel_recurring_payment(character, payment_type):
    with transaction.atomic():
        payment = RecurringPayment.objects.select_for_update().filter(
            character_id=character.id,
            payment_type=payment_type,
            active=True,
        ).first()
        if payment is None:
            return False
        payment.active = False
        payment.save(update_fields=["active"])
        return True


def has_active_coverage(character, payment_type):
    now = timezone.now()
    return (
        RecurringPayment.objects.filter(
            character_id=character.id,
            payment_type=payment_type,
            active=True,
            lapsed=False,
        )
        .filter(Q(next_due__gt=now) | Q(grace_until__gt=now))
        .exists()
    )


def banking_payment_tick(*args, **kwargs):
    process_recurring_payments()


def on_character_death(character, location):
    """Apply the carried-Scale and uncommitted-progression death penalties."""

    dropped = handle_carried_scales_on_death(character)

    if dropped > 0 and location:
        corpse_key = f"remains of {character.key}"
        for obj in location.contents:
            if obj.key == corpse_key:
                obj.db.scales = dropped
                break

    from world.world_state import ALL_DOMAINS

    for domain in ALL_DOMAINS:
        setattr(character.ndb, f"domain_xp_{domain}", 0.0)
    for attr in list(vars(character.ndb)):
        if attr.startswith("skill_use_"):
            setattr(character.ndb, attr, 0.0)

    from world.base_attributes import STAT_NAMES

    character.ndb.stat_xp_accumulators = {stat: 0.0 for stat in STAT_NAMES}
    if dropped > 0:
        character.msg(
            f"|rYou lost {dropped} Scales and any uncommitted experience.|n"
        )
    else:
        character.msg("|rYou lost any uncommitted experience.|n")


def handle_carried_scales_on_death(character):
    """Remove and return twenty percent of carried Scales."""

    carried = character.db.carried_scales or 0
    dropped = int(carried * 0.20)
    if dropped > 0:
        character.db.carried_scales = carried - dropped
    return dropped
