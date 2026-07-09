"""Migration-level contracts for the relational world state schema."""

from django.db import IntegrityError, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase
from django.utils import timezone


class TestWorldSchemaReconciliationMigration(TransactionTestCase):
    """The schema reconciliation must preserve data and portable uniqueness."""

    migrate_from = [("world", "0009_social_web_kernel")]
    migrate_to = [("world", "0010_reconcile_world_schema")]

    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        ObjectDB = old_apps.get_model("objects", "ObjectDB")
        FactionStanding = old_apps.get_model("world", "FactionStanding")
        CharacterGuild = old_apps.get_model("world", "CharacterGuild")
        CharacterAbility = old_apps.get_model("world", "CharacterAbility")
        CharacterQuest = old_apps.get_model("world", "CharacterQuest")
        CharacterRecipe = old_apps.get_model("world", "CharacterRecipe")
        KnownTopicRecord = old_apps.get_model("world", "KnownTopicRecord")

        character = ObjectDB.objects.create(
            db_key="Migration Sentinel",
            db_date_created=timezone.now(),
            db_lock_storage="",
        )
        self.character_id = character.pk
        self.row_ids = {
            "standing": FactionStanding.objects.create(
                character_id=character.pk,
                faction_id="wardens",
                standing=2750,
                trust=61,
            ).pk,
            "guild": CharacterGuild.objects.create(
                character_id=character.pk,
                guild_id="wardens",
                primary_domain="martial",
                secondary_domain="nature",
                subclass_id="trailwarden",
            ).pk,
            "ability": CharacterAbility.objects.create(
                character_id=character.pk,
                ability_id="sentinel_watch",
                times_used=7,
            ).pk,
            "quest": CharacterQuest.objects.create(
                character_id=character.pk,
                quest_id="migration_sentinel",
                progress={"report": 1},
            ).pk,
            "recipe": CharacterRecipe.objects.create(
                character_id=character.pk,
                recipe_id="field_dressing",
                learned_from="migration",
            ).pk,
            "topic": KnownTopicRecord.objects.create(
                character_id=character.pk,
                npc_id="calloway",
                topic_key="ashway",
                context_hash="sentinel",
            ).pk,
        }
        self.duplicate_standing_id = None
        if connection.vendor == "sqlite":
            duplicate = FactionStanding.objects.create(
                character_id=character.pk,
                faction_id="wardens",
                standing=3100,
                trust=66,
                betrayal_flag=True,
            )
            self.duplicate_standing_id = duplicate.pk

        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_to)
        self.apps = executor.loader.project_state(self.migrate_to).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_preserves_rows_relationships_and_primary_keys(self):
        expected_models = {
            "guild": "CharacterGuild",
            "ability": "CharacterAbility",
            "quest": "CharacterQuest",
            "recipe": "CharacterRecipe",
            "topic": "KnownTopicRecord",
        }

        for key, model_name in expected_models.items():
            model = self.apps.get_model("world", model_name)
            row = model.objects.get(pk=self.row_ids[key])
            self.assertEqual(row.character_id, self.character_id)
            self.assertEqual(
                model._meta.get_field("id").get_internal_type(),
                "BigAutoField",
            )

        standing = self.apps.get_model("world", "FactionStanding").objects.get(
            pk=self.row_ids["standing"]
        )
        self.assertEqual(standing.character_id, self.character_id)
        if self.duplicate_standing_id is None:
            self.assertEqual(standing.standing, 2750)
            self.assertEqual(standing.trust, 61)
        else:
            self.assertEqual(standing.standing, 3100)
            self.assertEqual(standing.trust, 66)
            self.assertTrue(standing.betrayal_flag)
            self.assertFalse(
                self.apps.get_model("world", "FactionStanding")
                .objects.filter(pk=self.duplicate_standing_id)
                .exists()
            )

    def test_enforces_top_level_and_subfaction_uniqueness(self):
        FactionStanding = self.apps.get_model("world", "FactionStanding")

        with self.assertRaises(IntegrityError), transaction.atomic():
            FactionStanding.objects.create(
                character_id=self.character_id,
                faction_id="wardens",
                standing=1,
            )

        FactionStanding.objects.create(
            character_id=self.character_id,
            faction_id="wardens",
            subfaction_id="ashway_watch",
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            FactionStanding.objects.create(
                character_id=self.character_id,
                faction_id="wardens",
                subfaction_id="ashway_watch",
            )

        FactionStanding.objects.create(
            character_id=self.character_id,
            faction_id="wardens",
            subfaction_id="river_watch",
        )


class TestSocialKnowledgePayloadMigration(TransactionTestCase):
    """Legacy inferred facts are removed before the XOR constraint lands."""

    migrate_from = [("world", "0010_reconcile_world_schema")]
    migrate_to = [("world", "0011_social_knowledge_payload_xor")]

    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        SocialNode = old_apps.get_model("world", "SocialNode")
        SocialFact = old_apps.get_model("world", "SocialFact")
        SocialClaim = old_apps.get_model("world", "SocialClaim")
        SocialKnowledge = old_apps.get_model("world", "SocialKnowledge")

        player = SocialNode.objects.create(
            node_key="player:migration_social_payload",
            node_type="player",
        )
        calloway = SocialNode.objects.create(
            node_key="npc:migration_social_payload_calloway",
            node_type="npc",
        )
        fact = SocialFact.objects.create(
            fact_key="fact:migration_social_payload",
            subject_node=player,
            event_type="quest_completed",
            summary="The report arrived.",
        )
        claim = SocialClaim.objects.create(
            claim_key="claim:migration_social_payload",
            fact=fact,
            speaker_node=calloway,
            subject_node=player,
            claim_type="report",
            summary="Calloway says the report arrived.",
        )
        self.node_id = calloway.pk
        self.fact_id = fact.pk
        self.claim_id = claim.pk
        self.dual_id = SocialKnowledge.objects.create(
            knowledge_key="knowledge:migration_social_payload:dual",
            node=calloway,
            fact=fact,
            claim=claim,
            channel="official_report",
        ).pk
        self.fact_only_id = SocialKnowledge.objects.create(
            knowledge_key="knowledge:migration_social_payload:fact",
            node=calloway,
            fact=fact,
            channel="direct_witness",
        ).pk
        self.claim_only_id = SocialKnowledge.objects.create(
            knowledge_key="knowledge:migration_social_payload:claim",
            node=calloway,
            claim=claim,
            channel="official_report",
        ).pk

        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_to)
        self.apps = executor.loader.project_state(self.migrate_to).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_conservatively_keeps_claim_for_legacy_dual_rows(self):
        SocialKnowledge = self.apps.get_model("world", "SocialKnowledge")

        dual = SocialKnowledge.objects.get(pk=self.dual_id)
        self.assertIsNone(dual.fact_id)
        self.assertEqual(dual.claim_id, self.claim_id)

        fact_only = SocialKnowledge.objects.get(pk=self.fact_only_id)
        self.assertEqual(fact_only.fact_id, self.fact_id)
        self.assertIsNone(fact_only.claim_id)

        claim_only = SocialKnowledge.objects.get(pk=self.claim_only_id)
        self.assertIsNone(claim_only.fact_id)
        self.assertEqual(claim_only.claim_id, self.claim_id)

    def test_enforces_exactly_one_payload_after_migration(self):
        SocialKnowledge = self.apps.get_model("world", "SocialKnowledge")

        with self.assertRaises(IntegrityError), transaction.atomic():
            SocialKnowledge.objects.create(
                knowledge_key="knowledge:migration_social_payload:neither",
                node_id=self.node_id,
                channel="official_report",
            )

        with self.assertRaises(IntegrityError), transaction.atomic():
            SocialKnowledge.objects.create(
                knowledge_key="knowledge:migration_social_payload:both_again",
                node_id=self.node_id,
                fact_id=self.fact_id,
                claim_id=self.claim_id,
                channel="official_report",
            )


class TestEconomyIntegrityMigration(TransactionTestCase):
    """Economy and inventory invariants become durable without losing rows."""

    migrate_from = [("world", "0011_social_knowledge_payload_xor")]
    migrate_to = [("world", "0012_economy_integrity_schema")]

    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        ObjectDB = old_apps.get_model("objects", "ObjectDB")
        BankAccount = old_apps.get_model("world", "BankAccount")
        BankTransaction = old_apps.get_model("world", "BankTransaction")
        DebtRecord = old_apps.get_model("world", "DebtRecord")
        InventoryItem = old_apps.get_model("world", "InventoryItem")

        character = ObjectDB.objects.create(
            db_key="Economy Migration Sentinel",
            db_date_created=timezone.now(),
            db_lock_storage="",
        )
        item = ObjectDB.objects.create(
            db_key="Migration Satchel",
            db_date_created=timezone.now(),
            db_lock_storage="",
            db_location_id=character.pk,
        )
        invalid_balance_character = ObjectDB.objects.create(
            db_key="Negative Balance Sentinel",
            db_date_created=timezone.now(),
            db_lock_storage="",
        )
        self.character_id = character.pk
        self.invalid_balance_character_id = invalid_balance_character.pk
        self.account_id = BankAccount.objects.create(
            character_id=character.pk,
            balance=100,
        ).pk
        self.transaction_id = BankTransaction.objects.create(
            character_id=character.pk,
            transaction_type="migration_seed",
            amount=100,
            balance_after=100,
            description="Migration sentinel",
        ).pk
        self.debt_id = DebtRecord.objects.create(
            character_id=character.pk,
            amount=50,
            deadline_playtime_seconds=600,
            status="active",
        ).pk
        self.inventory_id = InventoryItem.objects.create(
            character_id=character.pk,
            item_id=item.pk,
            quantity=1,
        ).pk

        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_to)
        self.apps = executor.loader.project_state(self.migrate_to).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_preserves_rows_and_backfills_operation_identity(self):
        BankAccount = self.apps.get_model("world", "BankAccount")
        BankTransaction = self.apps.get_model("world", "BankTransaction")
        DebtRecord = self.apps.get_model("world", "DebtRecord")
        InventoryItem = self.apps.get_model("world", "InventoryItem")

        self.assertEqual(BankAccount.objects.get(pk=self.account_id).balance, 100)
        transaction_row = BankTransaction.objects.get(pk=self.transaction_id)
        self.assertEqual(
            transaction_row.operation_id,
            f"legacy-bank-transaction-{self.transaction_id}",
        )
        self.assertEqual(DebtRecord.objects.get(pk=self.debt_id).amount, 50)
        self.assertEqual(InventoryItem.objects.get(pk=self.inventory_id).quantity, 1)

    def test_enforces_balance_debt_inventory_and_operation_constraints(self):
        BankAccount = self.apps.get_model("world", "BankAccount")
        BankTransaction = self.apps.get_model("world", "BankTransaction")
        DebtRecord = self.apps.get_model("world", "DebtRecord")
        InventoryItem = self.apps.get_model("world", "InventoryItem")

        invalid_creates = (
            lambda: BankAccount.objects.create(
                character_id=self.invalid_balance_character_id,
                balance=-1,
            ),
            lambda: DebtRecord.objects.create(
                character_id=self.character_id,
                amount=25,
                deadline_playtime_seconds=300,
                status="active",
            ),
            lambda: InventoryItem.objects.create(
                character_id=self.character_id,
                item_id=9001,
                quantity=0,
            ),
            lambda: InventoryItem.objects.create(
                character_id=self.character_id,
                item_id=9002,
                quantity=1,
                is_equipped=True,
            ),
            lambda: InventoryItem.objects.create(
                character_id=self.character_id,
                item_id=9003,
                quantity=1,
                is_equipped=True,
                equipment_slot="head",
                container_id=9004,
            ),
            lambda: BankTransaction.objects.create(
                character_id=self.character_id,
                transaction_type="duplicate_operation",
                amount=1,
                balance_after=101,
                operation_id=f"legacy-bank-transaction-{self.transaction_id}",
            ),
        )
        for invalid_create in invalid_creates:
            with self.assertRaises(IntegrityError), transaction.atomic():
                invalid_create()

    def test_creates_durable_stateful_bank_drafts(self):
        BankDraft = self.apps.get_model("world", "BankDraft")
        ObjectDB = self.apps.get_model("objects", "ObjectDB")

        draft = BankDraft.objects.create(
            draft_key="draft:migration-sentinel",
            issuer_character_id=self.character_id,
            issuer_character_ref=self.character_id,
            denomination=75,
            item_id=9100,
            operation_id="operation:migration-draft-issued",
        )
        self.assertEqual(draft.status, "issued")
        self.assertIsNone(draft.resolved_at)

        with self.assertRaises(IntegrityError), transaction.atomic():
            BankDraft.objects.create(
                draft_key="draft:invalid-denomination",
                issuer_character_id=self.character_id,
                issuer_character_ref=self.character_id,
                denomination=0,
                item_id=9101,
                operation_id="operation:invalid-denomination",
            )
        with self.assertRaises(IntegrityError), transaction.atomic():
            BankDraft.objects.create(
                draft_key="draft:invalid-redeemed-state",
                issuer_character_id=self.character_id,
                issuer_character_ref=self.character_id,
                denomination=25,
                item_id=9102,
                operation_id="operation:invalid-redeemed",
                status="redeemed",
            )

        ObjectDB.objects.filter(pk=self.character_id).delete()
        draft.refresh_from_db()
        self.assertIsNone(draft.issuer_character_id)
        self.assertEqual(draft.issuer_character_ref, self.character_id)


class TestEconomyIntegrityPreConstraintAudit(TransactionTestCase):
    """The migration refuses inconsistent legacy state instead of deleting it."""

    migrate_from = [("world", "0011_social_knowledge_payload_xor")]
    migrate_to = [("world", "0012_economy_integrity_schema")]

    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        ObjectDB = old_apps.get_model("objects", "ObjectDB")
        BankAccount = old_apps.get_model("world", "BankAccount")
        character = ObjectDB.objects.create(
            db_key="Invalid Economy Migration Sentinel",
            db_date_created=timezone.now(),
            db_lock_storage="",
        )
        self.invalid_account_id = BankAccount.objects.create(
            character_id=character.pk,
            balance=-10,
        ).pk

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps
        old_apps.get_model("world", "BankAccount").objects.filter(
            pk=self.invalid_account_id,
        ).delete()
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_aborts_before_constraints_when_legacy_rows_are_invalid(self):
        executor = MigrationExecutor(connection)

        with self.assertRaisesRegex(
            RuntimeError,
            "bank_account_negative_balance",
        ):
            executor.migrate(self.migrate_to)


class TestRecurringPaymentIntegrityMigration(TransactionTestCase):
    """Recurring contracts survive the new database invariants."""

    migrate_from = [("world", "0012_economy_integrity_schema")]
    migrate_to = [("world", "0013_recurring_payment_integrity")]

    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        ObjectDB = old_apps.get_model("objects", "ObjectDB")
        RecurringPayment = old_apps.get_model("world", "RecurringPayment")
        character = ObjectDB.objects.create(
            db_key="Recurring Migration Sentinel",
            db_date_created=timezone.now(),
            db_lock_storage="",
        )
        self.character_id = character.pk
        self.payment_id = RecurringPayment.objects.create(
            character_id=character.pk,
            payment_type="death_insurance",
            amount=50,
            interval_days=7,
            next_due=timezone.now(),
        ).pk

        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_to)
        self.apps = executor.loader.project_state(self.migrate_to).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_preserves_valid_contract_and_enforces_all_constraints(self):
        RecurringPayment = self.apps.get_model("world", "RecurringPayment")
        payment = RecurringPayment.objects.get(pk=self.payment_id)
        self.assertEqual(payment.amount, 50)
        self.assertEqual(payment.interval_days, 7)

        invalid_creates = (
            lambda: RecurringPayment.objects.create(
                character_id=self.character_id,
                payment_type="death_insurance",
                amount=75,
                interval_days=7,
                next_due=timezone.now(),
            ),
            lambda: RecurringPayment.objects.create(
                character_id=self.character_id,
                payment_type="invalid_amount",
                amount=0,
                interval_days=7,
                next_due=timezone.now(),
            ),
            lambda: RecurringPayment.objects.create(
                character_id=self.character_id,
                payment_type="invalid_interval",
                amount=50,
                interval_days=0,
                next_due=timezone.now(),
            ),
        )
        for invalid_create in invalid_creates:
            with self.assertRaises(IntegrityError), transaction.atomic():
                invalid_create()


class TestRecurringPaymentPreConstraintAudit(TransactionTestCase):
    """Legacy duplicate contracts stop migration instead of being merged."""

    migrate_from = [("world", "0012_economy_integrity_schema")]
    migrate_to = [("world", "0013_recurring_payment_integrity")]

    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        ObjectDB = old_apps.get_model("objects", "ObjectDB")
        RecurringPayment = old_apps.get_model("world", "RecurringPayment")
        character = ObjectDB.objects.create(
            db_key="Duplicate Recurring Migration Sentinel",
            db_date_created=timezone.now(),
            db_lock_storage="",
        )
        for amount in (50, 75):
            RecurringPayment.objects.create(
                character_id=character.pk,
                payment_type="death_insurance",
                amount=amount,
                interval_days=7,
                next_due=timezone.now(),
            )

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps
        old_apps.get_model("world", "RecurringPayment").objects.all().delete()
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_aborts_before_unique_constraint(self):
        executor = MigrationExecutor(connection)

        with self.assertRaisesRegex(RuntimeError, "recurring_duplicate_contract"):
            executor.migrate(self.migrate_to)


class TestUniqueEquippedSlotMigration(TransactionTestCase):
    """Valid equipment survives while duplicate slot occupancy is rejected."""

    migrate_from = [("world", "0013_recurring_payment_integrity")]
    migrate_to = [("world", "0014_unique_equipped_slot")]

    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        ObjectDB = old_apps.get_model("objects", "ObjectDB")
        InventoryItem = old_apps.get_model("world", "InventoryItem")
        character = ObjectDB.objects.create(
            db_key="Equipment Migration Sentinel",
            db_date_created=timezone.now(),
            db_lock_storage="",
        )
        first_item = ObjectDB.objects.create(
            db_key="First Migration Helm",
            db_date_created=timezone.now(),
            db_lock_storage="",
            db_location_id=character.pk,
        )
        second_item = ObjectDB.objects.create(
            db_key="Second Migration Helm",
            db_date_created=timezone.now(),
            db_lock_storage="",
            db_location_id=character.pk,
        )
        self.character_id = character.pk
        self.second_item_id = second_item.pk
        self.equipped_id = InventoryItem.objects.create(
            character_id=character.pk,
            item_id=first_item.pk,
            quantity=1,
            is_equipped=True,
            equipment_slot="head",
        ).pk

        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_to)
        self.apps = executor.loader.project_state(self.migrate_to).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_preserves_valid_equipment_and_enforces_unique_slot(self):
        InventoryItem = self.apps.get_model("world", "InventoryItem")
        equipped = InventoryItem.objects.get(pk=self.equipped_id)
        self.assertTrue(equipped.is_equipped)
        self.assertEqual(equipped.equipment_slot, "head")

        with self.assertRaises(IntegrityError), transaction.atomic():
            InventoryItem.objects.create(
                character_id=self.character_id,
                item_id=self.second_item_id,
                quantity=1,
                is_equipped=True,
                equipment_slot="head",
            )


class TestUniqueEquippedSlotPreConstraintAudit(TransactionTestCase):
    """Legacy duplicate equipped slots stop instead of choosing player gear."""

    migrate_from = [("world", "0013_recurring_payment_integrity")]
    migrate_to = [("world", "0014_unique_equipped_slot")]

    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps
        ObjectDB = old_apps.get_model("objects", "ObjectDB")
        InventoryItem = old_apps.get_model("world", "InventoryItem")

        character = ObjectDB.objects.create(
            db_key="Duplicate Equipment Migration Sentinel",
            db_date_created=timezone.now(),
            db_lock_storage="",
        )
        for index in range(2):
            item = ObjectDB.objects.create(
                db_key=f"Duplicate Migration Helm {index}",
                db_date_created=timezone.now(),
                db_lock_storage="",
                db_location_id=character.pk,
            )
            InventoryItem.objects.create(
                character_id=character.pk,
                item_id=item.pk,
                quantity=1,
                is_equipped=True,
                equipment_slot="head",
            )

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps
        old_apps.get_model("world", "InventoryItem").objects.all().delete()
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_aborts_before_unique_slot_constraint(self):
        executor = MigrationExecutor(connection)

        with self.assertRaisesRegex(RuntimeError, "duplicate_equipped_slot"):
            executor.migrate(self.migrate_to)
