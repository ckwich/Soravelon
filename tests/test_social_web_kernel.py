from evennia.utils.test_resources import EvenniaTest


class TestSocialWebModels(EvenniaTest):
    """The social web kernel persists graph nodes, edges, truth, claims, and traces."""

    def test_social_node_key_is_unique(self):
        from django.db import IntegrityError, transaction
        from world.models import SocialNode

        SocialNode.objects.create(
            node_key="npc:npc_warden_agent_calloway",
            node_type="npc",
            display_name="Agent Calloway",
            zone_id="vaels_crossing",
            settlement_id="vaels_crossing",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SocialNode.objects.create(
                    node_key="npc:npc_warden_agent_calloway",
                    node_type="npc",
                    display_name="Duplicate Calloway",
                )

    def test_social_edge_connects_two_nodes(self):
        from world.models import SocialEdge, SocialNode

        calloway = SocialNode.objects.create(
            node_key="npc:npc_warden_agent_calloway",
            node_type="npc",
            display_name="Agent Calloway",
        )
        commander = SocialNode.objects.create(
            node_key="npc:npc_warden_outpost_commander",
            node_type="npc",
            display_name="Outpost Commander",
        )

        edge = SocialEdge.objects.create(
            edge_key="edge:calloway:commander:official_report",
            source_node=calloway,
            target_node=commander,
            edge_type="official_report",
            directionality="one_way",
            trust=0.9,
            latency_seconds=3600,
            scope_tags=["warden", "report", "quest"],
        )

        self.assertEqual(edge.source_node.node_key, "npc:npc_warden_agent_calloway")
        self.assertEqual(edge.target_node.node_key, "npc:npc_warden_outpost_commander")
        self.assertEqual(edge.scope_tags, ["warden", "report", "quest"])

    def test_social_fact_claim_knowledge_and_trace_link_together(self):
        from world.models import (
            SocialClaim,
            SocialEdge,
            SocialFact,
            SocialKnowledge,
            SocialNode,
            SocialTrace,
        )

        player = SocialNode.objects.create(
            node_key=f"player:{self.char1.id}",
            node_type="player",
            display_name=self.char1.key,
        )
        calloway = SocialNode.objects.create(
            node_key="npc:npc_warden_agent_calloway",
            node_type="npc",
            display_name="Agent Calloway",
        )
        commander = SocialNode.objects.create(
            node_key="npc:npc_warden_outpost_commander",
            node_type="npc",
            display_name="Outpost Commander",
        )
        edge = SocialEdge.objects.create(
            edge_key="edge:calloway:commander:official_report",
            source_node=calloway,
            target_node=commander,
            edge_type="official_report",
            directionality="one_way",
            scope_tags=["warden", "report"],
        )
        fact = SocialFact.objects.create(
            fact_key="fact:warden_report_delivered",
            subject_node=player,
            scope_node=calloway,
            event_type="quest_completed",
            summary="The player delivered Calloway's sealed field report.",
            tags=["reliable", "warden_aligned", "report"],
            visibility="institutional",
        )
        claim = SocialClaim.objects.create(
            claim_key="claim:calloway:warden_report_delivered",
            fact=fact,
            speaker_node=calloway,
            subject_node=player,
            claim_type="report",
            summary="Calloway reports that the player carried Warden business cleanly.",
            status="supported",
        )
        knowledge = SocialKnowledge.objects.create(
            knowledge_key="knowledge:commander:claim:calloway:warden_report_delivered",
            node=commander,
            fact=fact,
            claim=claim,
            source_node=calloway,
            edge=edge,
            channel="official_report",
            confidence=0.9,
            spreading=True,
        )
        trace = SocialTrace.objects.create(
            trace_key="trace:commander:claim:calloway:warden_report_delivered",
            knowledge=knowledge,
            from_node=calloway,
            to_node=commander,
            edge=edge,
            summary="Official Warden report carried the claim from Calloway to the commander.",
        )

        self.assertEqual(knowledge.fact.fact_key, "fact:warden_report_delivered")
        self.assertEqual(knowledge.claim.claim_key, "claim:calloway:warden_report_delivered")
        self.assertEqual(trace.edge.edge_type, "official_report")
        self.assertEqual(
            calloway.outgoing_social_edges.get(edge_key=edge.edge_key),
            edge,
        )
        self.assertEqual(
            commander.social_knowledge.get(knowledge_key=knowledge.knowledge_key),
            knowledge,
        )
        self.assertEqual(knowledge.traces.get(trace_key=trace.trace_key), trace)

    def test_social_knowledge_requires_fact_or_claim(self):
        from django.db import IntegrityError, transaction
        from world.models import SocialKnowledge, SocialNode

        commander = SocialNode.objects.create(
            node_key="npc:npc_warden_outpost_commander",
            node_type="npc",
            display_name="Outpost Commander",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SocialKnowledge.objects.create(
                    knowledge_key="knowledge:commander:empty",
                    node=commander,
                    channel="official_report",
                )

    def test_probability_fields_reject_values_below_zero(self):
        from django.db import IntegrityError, transaction
        from world.models import (
            SocialClaim,
            SocialEdge,
            SocialFact,
            SocialKnowledge,
            SocialNode,
        )

        player = SocialNode.objects.create(
            node_key=f"player:{self.char1.id}",
            node_type="player",
            display_name=self.char1.key,
        )
        calloway = SocialNode.objects.create(
            node_key="npc:npc_warden_agent_calloway",
            node_type="npc",
            display_name="Agent Calloway",
        )
        commander = SocialNode.objects.create(
            node_key="npc:npc_warden_outpost_commander",
            node_type="npc",
            display_name="Outpost Commander",
        )
        edge = SocialEdge.objects.create(
            edge_key="edge:calloway:commander:official_report",
            source_node=calloway,
            target_node=commander,
            edge_type="official_report",
            directionality="one_way",
        )
        fact = SocialFact.objects.create(
            fact_key="fact:warden_report_delivered",
            subject_node=player,
            event_type="quest_completed",
            summary="The player delivered Calloway's sealed field report.",
        )
        claim = SocialClaim.objects.create(
            claim_key="claim:calloway:warden_report_delivered",
            fact=fact,
            speaker_node=calloway,
            subject_node=player,
            claim_type="report",
            summary="Calloway reports that the player carried Warden business cleanly.",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SocialEdge.objects.create(
                    edge_key="edge:calloway:commander:invalid_low_trust",
                    source_node=calloway,
                    target_node=commander,
                    edge_type="official_report",
                    trust=-0.1,
                )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SocialFact.objects.create(
                    fact_key="fact:invalid_low_confidence",
                    subject_node=player,
                    event_type="quest_completed",
                    summary="Invalid low confidence.",
                    confidence=-0.1,
                )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SocialClaim.objects.create(
                    claim_key="claim:invalid_low_confidence",
                    fact=fact,
                    speaker_node=calloway,
                    subject_node=player,
                    claim_type="report",
                    summary="Invalid low confidence.",
                    confidence=-0.1,
                )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SocialKnowledge.objects.create(
                    knowledge_key="knowledge:invalid_low_confidence",
                    node=commander,
                    fact=fact,
                    claim=claim,
                    edge=edge,
                    channel="official_report",
                    confidence=-0.1,
                )

    def test_probability_fields_reject_values_above_one(self):
        from django.db import IntegrityError, transaction
        from world.models import (
            SocialClaim,
            SocialEdge,
            SocialFact,
            SocialKnowledge,
            SocialNode,
        )

        player = SocialNode.objects.create(
            node_key=f"player:{self.char1.id}",
            node_type="player",
            display_name=self.char1.key,
        )
        calloway = SocialNode.objects.create(
            node_key="npc:npc_warden_agent_calloway",
            node_type="npc",
            display_name="Agent Calloway",
        )
        commander = SocialNode.objects.create(
            node_key="npc:npc_warden_outpost_commander",
            node_type="npc",
            display_name="Outpost Commander",
        )
        edge = SocialEdge.objects.create(
            edge_key="edge:calloway:commander:official_report",
            source_node=calloway,
            target_node=commander,
            edge_type="official_report",
            directionality="one_way",
        )
        fact = SocialFact.objects.create(
            fact_key="fact:warden_report_delivered",
            subject_node=player,
            event_type="quest_completed",
            summary="The player delivered Calloway's sealed field report.",
        )
        claim = SocialClaim.objects.create(
            claim_key="claim:calloway:warden_report_delivered",
            fact=fact,
            speaker_node=calloway,
            subject_node=player,
            claim_type="report",
            summary="Calloway reports that the player carried Warden business cleanly.",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SocialEdge.objects.create(
                    edge_key="edge:calloway:commander:invalid_high_trust",
                    source_node=calloway,
                    target_node=commander,
                    edge_type="official_report",
                    trust=1.1,
                )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SocialFact.objects.create(
                    fact_key="fact:invalid_high_confidence",
                    subject_node=player,
                    event_type="quest_completed",
                    summary="Invalid high confidence.",
                    confidence=1.1,
                )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SocialClaim.objects.create(
                    claim_key="claim:invalid_high_confidence",
                    fact=fact,
                    speaker_node=calloway,
                    subject_node=player,
                    claim_type="report",
                    summary="Invalid high confidence.",
                    confidence=1.1,
                )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SocialKnowledge.objects.create(
                    knowledge_key="knowledge:invalid_high_confidence",
                    node=commander,
                    fact=fact,
                    claim=claim,
                    edge=edge,
                    channel="official_report",
                    confidence=1.1,
                )


class TestSocialWebEngine(EvenniaTest):
    """Service APIs provide graph-shaped access over relational models."""

    def test_ensure_social_node_is_idempotent(self):
        from world.models import SocialNode
        from world.social_engine import ensure_social_node

        first = ensure_social_node(
            "npc",
            "npc_warden_agent_calloway",
            display_name="Agent Calloway",
            zone_id="vaels_crossing",
            settlement_id="vaels_crossing",
        )
        second = ensure_social_node(
            "npc",
            "npc_warden_agent_calloway",
            display_name="Agent Calloway",
            zone_id="vaels_crossing",
        )

        self.assertEqual(first.id, second.id)
        self.assertEqual(SocialNode.objects.count(), 1)
        self.assertEqual(first.node_key, "npc:npc_warden_agent_calloway")

    def test_connect_social_nodes_rejects_unknown_edge_type(self):
        from world.social_engine import connect_social_nodes, ensure_social_node

        ensure_social_node("npc", "a")
        ensure_social_node("npc", "b")

        ok, message, edge = connect_social_nodes(
            "npc:a",
            "npc:b",
            edge_type="made_up_channel",
        )

        self.assertFalse(ok)
        self.assertIn("unsupported edge_type", message)
        self.assertIsNone(edge)

    def test_record_fact_and_claim_create_initial_knowledge(self):
        from world.social_engine import (
            assert_social_claim,
            ensure_social_node,
            mark_known,
            record_social_fact,
        )

        player = ensure_social_node("player", str(self.char1.id), display_name=self.char1.key)
        calloway = ensure_social_node("npc", "npc_warden_agent_calloway")

        ok, message, fact = record_social_fact(
            fact_key="fact:test_warden_report_delivered",
            subject_node_key=player.node_key,
            scope_node_key=calloway.node_key,
            event_type="quest_completed",
            summary="The player delivered the field report.",
            tags=[" reliable ", "Reliable", "warden"],
            visibility="institutional",
            evidence={"quest_id": "vc_q_warden_report"},
        )
        self.assertTrue(ok, message)
        self.assertEqual(fact.tags, ["reliable", "warden"])

        ok, message, claim = assert_social_claim(
            claim_key="claim:calloway:test_warden_report_delivered",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="report",
            summary="Calloway says the player carried Warden business cleanly.",
            status="supported",
        )
        self.assertTrue(ok, message)

        ok, message, knowledge = mark_known(
            node_key=calloway.node_key,
            fact_key=fact.fact_key,
            claim_key=claim.claim_key,
            channel="direct_witness",
            confidence=1.0,
            spreading=True,
        )
        self.assertTrue(ok, message)
        self.assertEqual(knowledge.node.node_key, calloway.node_key)

    def test_engine_rejects_out_of_range_probability_inputs(self):
        from world.social_engine import (
            assert_social_claim,
            connect_social_nodes,
            ensure_social_node,
            mark_known,
            record_social_fact,
        )

        player = ensure_social_node("player", str(self.char1.id), display_name=self.char1.key)
        calloway = ensure_social_node("npc", "npc_warden_agent_calloway")
        commander = ensure_social_node("npc", "npc_warden_outpost_commander")

        ok, message, edge = connect_social_nodes(
            calloway.node_key,
            commander.node_key,
            edge_type="official_report",
            trust=1.1,
        )
        self.assertFalse(ok)
        self.assertIn("trust must be between 0.0 and 1.0", message)
        self.assertIsNone(edge)

        ok, message, fact = record_social_fact(
            fact_key="fact:invalid_probability",
            subject_node_key=player.node_key,
            event_type="quest_completed",
            summary="Invalid confidence should be rejected before persistence.",
            confidence=-0.1,
        )
        self.assertFalse(ok)
        self.assertIn("confidence must be between 0.0 and 1.0", message)
        self.assertIsNone(fact)

        ok, message, fact = record_social_fact(
            fact_key="fact:valid_probability",
            subject_node_key=player.node_key,
            event_type="quest_completed",
            summary="Valid confidence should persist.",
            confidence=1.0,
        )
        self.assertTrue(ok, message)

        ok, message, claim = assert_social_claim(
            claim_key="claim:invalid_probability",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="report",
            summary="Invalid claim confidence should be rejected before persistence.",
            confidence=1.1,
        )
        self.assertFalse(ok)
        self.assertIn("confidence must be between 0.0 and 1.0", message)
        self.assertIsNone(claim)

        ok, message, knowledge = mark_known(
            node_key=calloway.node_key,
            fact_key=fact.fact_key,
            channel="direct_witness",
            confidence=-0.1,
        )
        self.assertFalse(ok)
        self.assertIn("confidence must be between 0.0 and 1.0", message)
        self.assertIsNone(knowledge)
