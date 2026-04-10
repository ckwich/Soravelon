"""
Tests for Soravelon banking system (Build Order Step 8).
Tests written FIRST per TDD.
"""

from datetime import timedelta
from django.utils import timezone
from evennia.utils.test_resources import EvenniaTest
from evennia import create_object


class BankingTestBase(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.char1.db.carried_scales = 1000


# --- Core transactions ---

class TestDepositSuccess(BankingTestBase):
    def test_deposit_success(self):
        from world.banking import deposit, get_balance
        success, msg = deposit(self.char1, 500)
        self.assertTrue(success)
        self.assertEqual(self.char1.db.carried_scales, 500)
        self.assertEqual(get_balance(self.char1), 500)


class TestDepositInsufficient(BankingTestBase):
    def test_deposit_insufficient_carried(self):
        from world.banking import deposit
        success, msg = deposit(self.char1, 2000)
        self.assertFalse(success)
        self.assertEqual(self.char1.db.carried_scales, 1000)


class TestDepositCreatesTransaction(BankingTestBase):
    def test_deposit_creates_transaction_record(self):
        from world.banking import deposit
        from world.models import BankTransaction
        deposit(self.char1, 100)
        txns = BankTransaction.objects.filter(
            character_id=self.char1.id, transaction_type="deposit"
        )
        self.assertEqual(txns.count(), 1)
        self.assertEqual(txns.first().amount, 100)
        self.assertEqual(txns.first().balance_after, 100)


class TestWithdrawSuccess(BankingTestBase):
    def test_withdraw_success(self):
        from world.banking import deposit, withdraw, get_balance
        deposit(self.char1, 500)
        success, msg = withdraw(self.char1, 200)
        self.assertTrue(success)
        self.assertEqual(get_balance(self.char1), 300)
        self.assertEqual(self.char1.db.carried_scales, 700)


class TestWithdrawInsufficient(BankingTestBase):
    def test_withdraw_insufficient_banked(self):
        from world.banking import deposit, withdraw
        deposit(self.char1, 100)
        success, msg = withdraw(self.char1, 500)
        self.assertFalse(success)


class TestWithdrawCreatesTransaction(BankingTestBase):
    def test_withdraw_creates_transaction_record(self):
        from world.banking import deposit, withdraw
        from world.models import BankTransaction
        deposit(self.char1, 500)
        withdraw(self.char1, 200)
        txns = BankTransaction.objects.filter(
            character_id=self.char1.id, transaction_type="withdraw"
        )
        self.assertEqual(txns.count(), 1)
        self.assertEqual(txns.first().amount, -200)


class TestBalanceZeroNoAccount(BankingTestBase):
    def test_balance_zero_no_account(self):
        from world.banking import get_balance
        self.assertEqual(get_balance(self.char1), 0)


class TestGetOrCreateIdempotent(BankingTestBase):
    def test_get_or_create_idempotent(self):
        from world.banking import get_or_create_account
        a1 = get_or_create_account(self.char1)
        a2 = get_or_create_account(self.char1)
        self.assertEqual(a1.id, a2.id)


class TestDeductFromBankSuccess(BankingTestBase):
    def test_deduct_from_bank_success(self):
        from world.banking import deposit, deduct_from_bank, get_balance
        deposit(self.char1, 500)
        success, _ = deduct_from_bank(self.char1, 100, "insurance_payment")
        self.assertTrue(success)
        self.assertEqual(get_balance(self.char1), 400)


class TestDeductNoOverdraft(BankingTestBase):
    def test_deduct_from_bank_no_overdraft(self):
        from world.banking import deposit, deduct_from_bank, get_balance
        deposit(self.char1, 50)
        success, _ = deduct_from_bank(self.char1, 100, "insurance_payment")
        self.assertFalse(success)
        self.assertEqual(get_balance(self.char1), 50)


class TestCreditToBank(BankingTestBase):
    def test_credit_to_bank(self):
        from world.banking import credit_to_bank, get_balance
        success, _ = credit_to_bank(self.char1, 300, "ah_proceeds")
        self.assertTrue(success)
        self.assertEqual(get_balance(self.char1), 300)


class TestTransactionImmutability(BankingTestBase):
    def test_transaction_immutability(self):
        from world.banking import deposit, withdraw
        from world.models import BankTransaction
        deposit(self.char1, 500)
        count_after_deposit = BankTransaction.objects.filter(
            character_id=self.char1.id
        ).count()
        withdraw(self.char1, 100)
        count_after_withdraw = BankTransaction.objects.filter(
            character_id=self.char1.id
        ).count()
        self.assertEqual(count_after_withdraw, count_after_deposit + 1)


# --- Recurring payments ---

class TestSetupRecurringPayment(BankingTestBase):
    def test_setup_recurring_payment(self):
        from world.banking import setup_recurring_payment
        payment = setup_recurring_payment(self.char1, "death_insurance", 50)
        self.assertTrue(payment.active)
        self.assertGreater(payment.next_due, timezone.now())


class TestSetupRecurringReplaces(BankingTestBase):
    def test_setup_recurring_payment_replaces_existing(self):
        from world.banking import setup_recurring_payment
        from world.models import RecurringPayment
        setup_recurring_payment(self.char1, "death_insurance", 50)
        setup_recurring_payment(self.char1, "death_insurance", 75)
        count = RecurringPayment.objects.filter(
            character_id=self.char1.id, payment_type="death_insurance"
        ).count()
        self.assertEqual(count, 1)


class TestCancelRecurringPayment(BankingTestBase):
    def test_cancel_recurring_payment(self):
        from world.banking import setup_recurring_payment, cancel_recurring_payment
        from world.models import RecurringPayment
        setup_recurring_payment(self.char1, "death_insurance", 50)
        result = cancel_recurring_payment(self.char1, "death_insurance")
        self.assertTrue(result)
        payment = RecurringPayment.objects.get(
            character_id=self.char1.id, payment_type="death_insurance"
        )
        self.assertFalse(payment.active)


class TestHasActiveCoverageTrue(BankingTestBase):
    def test_has_active_coverage_true(self):
        from world.banking import setup_recurring_payment, has_active_coverage
        setup_recurring_payment(self.char1, "death_insurance", 50)
        self.assertTrue(has_active_coverage(self.char1, "death_insurance"))


class TestHasActiveCoverageFalseLapsed(BankingTestBase):
    def test_has_active_coverage_false_lapsed(self):
        from world.banking import setup_recurring_payment, has_active_coverage
        from world.models import RecurringPayment
        setup_recurring_payment(self.char1, "death_insurance", 50)
        RecurringPayment.objects.filter(
            character_id=self.char1.id
        ).update(lapsed=True, active=False)
        self.assertFalse(has_active_coverage(self.char1, "death_insurance"))


class TestHasActiveCoverageInGrace(BankingTestBase):
    def test_has_active_coverage_in_grace(self):
        from world.banking import setup_recurring_payment, has_active_coverage
        from world.models import RecurringPayment
        setup_recurring_payment(self.char1, "death_insurance", 50)
        # Set next_due to past, grace_until to future
        RecurringPayment.objects.filter(
            character_id=self.char1.id
        ).update(
            next_due=timezone.now() - timedelta(days=1),
            grace_until=timezone.now() + timedelta(days=5)
        )
        self.assertTrue(has_active_coverage(self.char1, "death_insurance"))


class TestProcessPaymentSuccess(BankingTestBase):
    def test_process_payment_success(self):
        from world.banking import (
            deposit, setup_recurring_payment, process_recurring_payments
        )
        from world.models import RecurringPayment
        deposit(self.char1, 500)
        setup_recurring_payment(self.char1, "death_insurance", 50)
        # Set next_due to past to trigger processing
        RecurringPayment.objects.filter(
            character_id=self.char1.id
        ).update(next_due=timezone.now() - timedelta(hours=1))

        process_recurring_payments()

        from world.banking import get_balance
        self.assertEqual(get_balance(self.char1), 450)
        payment = RecurringPayment.objects.get(character_id=self.char1.id)
        self.assertGreater(payment.next_due, timezone.now())
        self.assertIsNone(payment.grace_until)


class TestProcessPaymentInsufficientStartsGrace(BankingTestBase):
    def test_process_payment_insufficient_starts_grace(self):
        from world.banking import setup_recurring_payment, process_recurring_payments
        from world.models import RecurringPayment
        # No deposit — balance is 0
        setup_recurring_payment(self.char1, "death_insurance", 50)
        RecurringPayment.objects.filter(
            character_id=self.char1.id
        ).update(next_due=timezone.now() - timedelta(hours=1))

        process_recurring_payments()

        payment = RecurringPayment.objects.get(character_id=self.char1.id)
        self.assertIsNotNone(payment.grace_until)
        self.assertTrue(payment.active)
        self.assertFalse(payment.lapsed)


class TestProcessPaymentGraceExpired(BankingTestBase):
    def test_process_payment_grace_expired_lapses(self):
        from world.banking import setup_recurring_payment, process_recurring_payments
        from world.models import RecurringPayment
        setup_recurring_payment(self.char1, "death_insurance", 50)
        RecurringPayment.objects.filter(
            character_id=self.char1.id
        ).update(
            next_due=timezone.now() - timedelta(days=10),
            grace_until=timezone.now() - timedelta(days=1)
        )

        process_recurring_payments()

        payment = RecurringPayment.objects.get(character_id=self.char1.id)
        self.assertTrue(payment.lapsed)
        self.assertFalse(payment.active)


# --- Drafts ---

class TestIssueDraftDeductsBank(BankingTestBase):
    def test_issue_draft_deducts_bank(self):
        from world.banking import deposit, issue_draft, get_balance
        deposit(self.char1, 500)
        success, _ = issue_draft(self.char1, 200)
        self.assertTrue(success)
        self.assertEqual(get_balance(self.char1), 300)


class TestIssueDraftCreatesItem(BankingTestBase):
    def test_issue_draft_creates_item(self):
        from world.banking import deposit, issue_draft
        deposit(self.char1, 500)
        issue_draft(self.char1, 200)
        # Find the draft in character's contents
        drafts = [
            obj for obj in self.char1.contents
            if getattr(obj.db, 'item_type', None) == "draft"
        ]
        self.assertEqual(len(drafts), 1)
        self.assertEqual(drafts[0].db.denomination, 200)


class TestRedeemDraftCreditsBank(BankingTestBase):
    def test_redeem_draft_credits_bank(self):
        from world.banking import deposit, issue_draft, redeem_draft, get_balance
        deposit(self.char1, 500)
        issue_draft(self.char1, 200)
        draft = [
            obj for obj in self.char1.contents
            if getattr(obj.db, 'item_type', None) == "draft"
        ][0]
        redeem_draft(self.char1, draft)
        self.assertEqual(get_balance(self.char1), 500)


class TestRedeemDraftDestroysItem(BankingTestBase):
    def test_redeem_draft_destroys_item(self):
        from world.banking import deposit, issue_draft, redeem_draft
        deposit(self.char1, 500)
        issue_draft(self.char1, 200)
        draft = [
            obj for obj in self.char1.contents
            if getattr(obj.db, 'item_type', None) == "draft"
        ][0]
        redeem_draft(self.char1, draft)
        remaining = [
            obj for obj in self.char1.contents
            if getattr(obj.db, 'item_type', None) == "draft"
        ]
        self.assertEqual(len(remaining), 0)


class TestRedeemNonDraftFails(BankingTestBase):
    def test_redeem_non_draft_fails(self):
        from world.banking import redeem_draft
        from typeclasses.objects import SoravelonItem
        item = create_object(SoravelonItem, key="rock", location=self.char1)
        success, msg = redeem_draft(self.char1, item)
        self.assertFalse(success)


# --- Debt ---

class TestCreateDebt(BankingTestBase):
    def test_create_debt(self):
        from world.banking import create_debt, get_active_debt
        success, _ = create_debt(self.char1, 500, 7200)
        self.assertTrue(success)
        debt = get_active_debt(self.char1)
        self.assertIsNotNone(debt)
        self.assertEqual(debt.amount, 500)
        self.assertEqual(debt.deadline_playtime_seconds, 7200)


class TestCreateDebtNoDuplicate(BankingTestBase):
    def test_create_debt_no_duplicate(self):
        from world.banking import create_debt
        create_debt(self.char1, 500, 7200)
        success, _ = create_debt(self.char1, 300, 3600)
        self.assertFalse(success)


class TestPayDebtSuccess(BankingTestBase):
    def test_pay_debt_success(self):
        from world.banking import create_debt, deposit, pay_debt, get_active_debt
        create_debt(self.char1, 500, 7200)
        deposit(self.char1, 600)
        success, _ = pay_debt(self.char1)
        self.assertTrue(success)
        self.assertIsNone(get_active_debt(self.char1))


class TestPayDebtInsufficient(BankingTestBase):
    def test_pay_debt_insufficient(self):
        from world.banking import create_debt, pay_debt, get_active_debt
        create_debt(self.char1, 500, 7200)
        success, _ = pay_debt(self.char1)
        self.assertFalse(success)
        self.assertIsNotNone(get_active_debt(self.char1))


class TestDecrementDebtTimer(BankingTestBase):
    def test_decrement_debt_timer(self):
        from world.banking import create_debt, decrement_debt_timer, get_active_debt
        create_debt(self.char1, 500, 7200)
        remaining = decrement_debt_timer(self.char1, 600)
        self.assertEqual(remaining, 6600)


class TestDebtBecomesHunted(BankingTestBase):
    def test_debt_becomes_hunted_at_zero(self):
        from world.banking import create_debt, decrement_debt_timer
        from world.models import DebtRecord
        create_debt(self.char1, 500, 600)
        decrement_debt_timer(self.char1, 600)
        debt = DebtRecord.objects.get(character_id=self.char1.id)
        self.assertEqual(debt.status, "hunted")
