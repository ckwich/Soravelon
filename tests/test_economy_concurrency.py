"""PostgreSQL contention proof for bank withdrawal and draft redemption."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest import skipUnless

from django.db import close_old_connections, connection
from django.test import TransactionTestCase
from evennia import create_object
from evennia.objects.models import ObjectDB

from world.models import BankAccount, BankDraft, BankTransaction


@skipUnless(
    connection.vendor == "postgresql",
    "row-lock contention requires PostgreSQL",
)
class TestPostgresEconomyContention(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        from typeclasses.characters import Character
        from typeclasses.rooms import SoravelonRoom

        self.room = create_object(SoravelonRoom, key="Economy Contention Room")
        self.character = create_object(Character, key="Economy Claimant")
        self.character.location = self.room
        self.character.db.carried_scales = 0

    @staticmethod
    def _run_concurrently(worker, values):
        barrier = Barrier(len(values))

        def synchronized(value):
            close_old_connections()
            try:
                barrier.wait(timeout=5)
                return worker(value)
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=len(values)) as executor:
            return list(executor.map(synchronized, values))

    def test_concurrent_withdrawals_cannot_overdraw(self):
        from world.banking import credit_to_bank

        credited, message = credit_to_bank(
            self.character,
            100,
            "test_seed",
            operation_id="withdraw-contention:seed",
        )
        self.assertTrue(credited, message)

        def withdraw(operation_id):
            from world.banking import withdraw

            character = ObjectDB.objects.get(pk=self.character.id)
            return withdraw(character, 75, operation_id=operation_id)

        results = self._run_concurrently(
            withdraw,
            ["withdraw-contention:first", "withdraw-contention:second"],
        )

        self.assertEqual(sum(1 for success, _ in results if success), 1, results)
        self.assertEqual(BankAccount.objects.get().balance, 25)
        self.assertEqual(
            BankTransaction.objects.filter(transaction_type="withdraw").count(),
            1,
        )
        character = ObjectDB.objects.get(pk=self.character.id)
        self.assertEqual(character.db.carried_scales, 75)

    def test_concurrent_draft_redemption_pays_once(self):
        from world.banking import credit_to_bank, issue_draft

        credited, message = credit_to_bank(
            self.character,
            100,
            "test_seed",
            operation_id="draft-contention:seed",
        )
        self.assertTrue(credited, message)
        issued, message = issue_draft(
            self.character,
            100,
            operation_id="draft-contention:issue",
        )
        self.assertTrue(issued, message)
        draft = BankDraft.objects.get(operation_id="draft-contention:issue")

        def redeem(operation_id):
            from world.banking import redeem_draft

            character = ObjectDB.objects.get(pk=self.character.id)
            item = ObjectDB.objects.filter(pk=draft.item_id).first()
            if not item:
                return False, "Draft already redeemed."
            return redeem_draft(
                character,
                item,
                operation_id=operation_id,
            )

        results = self._run_concurrently(
            redeem,
            ["draft-contention:first", "draft-contention:second"],
        )

        self.assertEqual(sum(1 for success, _ in results if success), 1, results)
        self.assertEqual(BankAccount.objects.get().balance, 100)
        self.assertEqual(
            BankTransaction.objects.filter(
                transaction_type="draft_redeemed"
            ).count(),
            1,
        )
        draft.refresh_from_db()
        self.assertEqual(draft.status, "redeemed")
