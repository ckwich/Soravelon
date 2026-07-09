"""Failure-injection contracts for atomic economy operations."""

from types import SimpleNamespace
from unittest.mock import patch

from django.db import IntegrityError, transaction
from django.utils import timezone
from evennia.objects.models import ObjectDB
from evennia.utils.test_resources import EvenniaTest

from world.models import (
    BankAccount,
    BankDraft,
    BankTransaction,
    DebtRecord,
    RecurringPayment,
)


class AtomicEconomyTestBase(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.char1.db.carried_scales = 1000

    def stored_carried_scales(self):
        through = ObjectDB.db_attributes.through
        return through.objects.filter(
            objectdb_id=self.char1.id,
            attribute__db_key="carried_scales",
            attribute__db_category__isnull=True,
        ).values_list("attribute__db_value", flat=True).get()

    def assert_carried_scales(self, expected):
        self.assertEqual(self.stored_carried_scales(), expected)
        self.assertEqual(self.char1.db.carried_scales, expected)

    @staticmethod
    def fail_at(expected_checkpoint):
        def _fail(checkpoint):
            if checkpoint == expected_checkpoint:
                raise RuntimeError(f"injected failure at {checkpoint}")

        return _fail


class TestAtomicCashAndBankOperations(AtomicEconomyTestBase):
    def test_explicit_blank_operation_id_is_rejected(self):
        from world.economy_transactions import deposit

        with self.assertRaisesRegex(ValueError, "non-empty"):
            deposit(self.char1, 200, operation_id="")

        self.assert_carried_scales(1000)
        self.assertFalse(BankAccount.objects.exists())
        self.assertFalse(BankTransaction.objects.exists())

    def test_deposit_rolls_back_after_every_write(self):
        from world.economy_transactions import deposit

        for checkpoint in (
            "bank_account_created",
            "carried_debited",
            "bank_credited",
            "ledger_recorded",
        ):
            with self.subTest(checkpoint=checkpoint):
                BankTransaction.objects.all().delete()
                BankAccount.objects.all().delete()
                self.char1.db.carried_scales = 1000

                with patch(
                    "world.economy_transactions._after_write",
                    side_effect=self.fail_at(checkpoint),
                ), self.assertRaisesRegex(RuntimeError, checkpoint):
                    deposit(
                        self.char1,
                        200,
                        operation_id=f"deposit-failure:{checkpoint}",
                    )

                self.assert_carried_scales(1000)
                self.assertFalse(BankAccount.objects.exists())
                self.assertFalse(BankTransaction.objects.exists())

    def test_withdraw_rolls_back_bank_carried_and_ledger(self):
        from world.economy_transactions import deposit, withdraw

        ok, message = deposit(
            self.char1,
            500,
            operation_id="withdraw-rollback:seed",
        )
        self.assertTrue(ok, message)

        for checkpoint in (
            "bank_debited",
            "carried_credited",
            "ledger_recorded",
        ):
            with self.subTest(checkpoint=checkpoint):
                with patch(
                    "world.economy_transactions._after_write",
                    side_effect=self.fail_at(checkpoint),
                ), self.assertRaisesRegex(RuntimeError, checkpoint):
                    withdraw(
                        self.char1,
                        100,
                        operation_id=f"withdraw-failure:{checkpoint}",
                    )

                self.assert_carried_scales(500)
                self.assertEqual(BankAccount.objects.get().balance, 500)
                self.assertEqual(BankTransaction.objects.count(), 1)

    def test_same_operation_id_is_exactly_once(self):
        from world.economy_transactions import deposit

        first = deposit(self.char1, 200, operation_id="deposit:exactly-once")
        second = deposit(self.char1, 200, operation_id="deposit:exactly-once")

        self.assertTrue(first[0], first[1])
        self.assertTrue(second[0], second[1])
        self.assert_carried_scales(800)
        self.assertEqual(BankAccount.objects.get().balance, 200)
        self.assertEqual(BankTransaction.objects.count(), 1)

    def test_reusing_operation_id_for_different_effect_is_rejected(self):
        from world.economy_transactions import EconomyOperationConflict, deposit

        deposit(self.char1, 200, operation_id="deposit:conflict")

        with self.assertRaises(EconomyOperationConflict):
            deposit(self.char1, 201, operation_id="deposit:conflict")


class TestAtomicBankDrafts(AtomicEconomyTestBase):
    def setUp(self):
        super().setUp()
        from world.economy_transactions import deposit

        ok, message = deposit(
            self.char1,
            500,
            operation_id="draft-tests:seed",
        )
        self.assertTrue(ok, message)

    def test_issue_draft_rolls_back_money_item_and_record(self):
        from world.economy_transactions import issue_draft

        original_object_ids = set(ObjectDB.objects.values_list("id", flat=True))
        for checkpoint in (
            "bank_debited",
            "ledger_recorded",
            "draft_item_created",
            "draft_recorded",
        ):
            with self.subTest(checkpoint=checkpoint):
                with patch(
                    "world.economy_transactions._after_write",
                    side_effect=self.fail_at(checkpoint),
                ), self.assertRaisesRegex(RuntimeError, checkpoint):
                    issue_draft(
                        self.char1,
                        200,
                        operation_id=f"draft-failure:{checkpoint}",
                    )

                self.assertEqual(BankAccount.objects.get().balance, 500)
                self.assertEqual(BankTransaction.objects.count(), 1)
                self.assertFalse(BankDraft.objects.exists())
                self.assertEqual(
                    set(ObjectDB.objects.values_list("id", flat=True)),
                    original_object_ids,
                )

    def test_redeem_uses_durable_draft_value_and_is_exactly_once(self):
        from world.economy_transactions import issue_draft, redeem_draft

        ok, message = issue_draft(
            self.char1,
            200,
            operation_id="draft:issue",
        )
        self.assertTrue(ok, message)
        draft_record = BankDraft.objects.get(operation_id="draft:issue")
        draft_item = ObjectDB.objects.get(pk=draft_record.item_id)
        draft_item.db.denomination = 999999

        ok, message = redeem_draft(
            self.char1,
            draft_item,
            operation_id="draft:redeem",
        )

        self.assertTrue(ok, message)
        self.assertEqual(BankAccount.objects.get().balance, 500)
        draft_record.refresh_from_db()
        self.assertEqual(draft_record.status, "redeemed")
        self.assertEqual(draft_record.resolution_operation_id, "draft:redeem")
        self.assertEqual(draft_record.redeemer_character_ref, self.char1.id)
        self.assertFalse(ObjectDB.objects.filter(pk=draft_record.item_id).exists())

        replay_item = SimpleNamespace(id=draft_record.item_id)
        ok, message = redeem_draft(
            self.char1,
            replay_item,
            operation_id="draft:redeem",
        )
        self.assertTrue(ok, message)
        self.assertEqual(BankAccount.objects.get().balance, 500)
        self.assertEqual(
            BankTransaction.objects.filter(operation_id="draft:redeem").count(),
            1,
        )

    def test_redeem_rolls_back_every_durable_write(self):
        from world.economy_transactions import issue_draft, redeem_draft

        ok, message = issue_draft(
            self.char1,
            200,
            operation_id="draft:rollback-issue",
        )
        self.assertTrue(ok, message)
        draft_record = BankDraft.objects.get(
            operation_id="draft:rollback-issue",
        )
        item_id = draft_record.item_id

        for checkpoint in (
            "bank_credited",
            "ledger_recorded",
            "draft_resolved",
            "draft_inventory_unregistered",
            "draft_item_deleted",
        ):
            with self.subTest(checkpoint=checkpoint):
                draft_item = ObjectDB.objects.get(pk=item_id)
                with patch(
                    "world.economy_transactions._after_write",
                    side_effect=self.fail_at(checkpoint),
                ), self.assertRaisesRegex(RuntimeError, checkpoint):
                    redeem_draft(
                        self.char1,
                        draft_item,
                        operation_id=f"draft-rollback:{checkpoint}",
                    )

                self.assertEqual(BankAccount.objects.get().balance, 300)
                draft_record.refresh_from_db()
                self.assertEqual(draft_record.status, "issued")
                self.assertIsNone(draft_record.resolution_operation_id)
                self.assertTrue(ObjectDB.objects.filter(pk=item_id).exists())
                self.assertFalse(
                    BankTransaction.objects.filter(
                        operation_id=f"draft-rollback:{checkpoint}",
                    ).exists()
                )


class TestAtomicDebtPayment(AtomicEconomyTestBase):
    def test_debt_payment_failure_rolls_back_debit_and_debt_state(self):
        from world.economy_transactions import create_debt, deposit, pay_debt

        ok, message = create_debt(self.char1, 300, 600)
        self.assertTrue(ok, message)
        ok, message = deposit(
            self.char1,
            500,
            operation_id="debt:seed",
        )
        self.assertTrue(ok, message)

        with patch(
            "world.economy_transactions._after_write",
            side_effect=self.fail_at("debt_resolved"),
        ), self.assertRaisesRegex(RuntimeError, "debt_resolved"):
            pay_debt(
                self.char1,
                operation_id="debt:payment",
            )

        self.assertEqual(BankAccount.objects.get().balance, 500)
        debt = DebtRecord.objects.get()
        self.assertEqual(debt.status, "active")
        self.assertIsNone(debt.resolved_at)
        self.assertFalse(
            BankTransaction.objects.filter(operation_id="debt:payment").exists()
        )


class TestRecurringPaymentIntegrity(AtomicEconomyTestBase):
    def test_database_rejects_duplicate_character_payment_type(self):
        values = {
            "character_id": self.char1.id,
            "payment_type": "death_insurance",
            "amount": 50,
            "interval_days": 7,
            "next_due": timezone.now(),
        }
        RecurringPayment.objects.create(**values)

        with self.assertRaises(IntegrityError), transaction.atomic():
            RecurringPayment.objects.create(**values)

    def test_database_rejects_nonpositive_amount_and_interval(self):
        for invalid_values in (
            {"amount": 0, "interval_days": 7},
            {"amount": 50, "interval_days": 0},
        ):
            with self.subTest(invalid_values=invalid_values):
                with self.assertRaises(IntegrityError), transaction.atomic():
                    RecurringPayment.objects.create(
                        character_id=self.char1.id,
                        payment_type=f"invalid:{invalid_values['amount']}",
                        next_due=timezone.now(),
                        **invalid_values,
                    )
