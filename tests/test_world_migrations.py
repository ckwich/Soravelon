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
