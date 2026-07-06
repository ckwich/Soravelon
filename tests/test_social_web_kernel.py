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
