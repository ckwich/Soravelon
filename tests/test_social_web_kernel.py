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

        self.assertIsNone(knowledge.fact)
        self.assertEqual(knowledge.claim.claim_key, "claim:calloway:warden_report_delivered")
        self.assertEqual(knowledge.claim.fact, fact)
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

    def test_social_knowledge_rejects_fact_and_claim_together(self):
        from django.db import IntegrityError, transaction
        from world.models import SocialClaim, SocialFact, SocialKnowledge, SocialNode

        player = SocialNode.objects.create(
            node_key=f"player:{self.char1.id}",
            node_type="player",
        )
        calloway = SocialNode.objects.create(
            node_key="npc:npc_warden_agent_calloway",
            node_type="npc",
        )
        fact = SocialFact.objects.create(
            fact_key="fact:dual_payload_rejected",
            subject_node=player,
            event_type="quest_completed",
            summary="The report arrived.",
        )
        claim = SocialClaim.objects.create(
            claim_key="claim:dual_payload_rejected",
            fact=fact,
            speaker_node=calloway,
            subject_node=player,
            claim_type="report",
            summary="Calloway says the report arrived.",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SocialKnowledge.objects.create(
                    knowledge_key="knowledge:dual_payload_rejected",
                    node=calloway,
                    fact=fact,
                    claim=claim,
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

    def test_connect_social_nodes_rejects_invalid_directionality_and_integer_fields(self):
        from world.models import SocialEdge
        from world.social_engine import connect_social_nodes, ensure_social_node

        calloway = ensure_social_node("npc", "npc_warden_agent_calloway")
        commander = ensure_social_node("npc", "npc_warden_outpost_commander")

        ok, message, edge = connect_social_nodes(
            calloway.node_key,
            commander.node_key,
            edge_type="official_report",
            directionality="sideways",
        )
        self.assertFalse(ok)
        self.assertEqual(message, "unsupported directionality: sideways")
        self.assertIsNone(edge)

        ok, message, edge = connect_social_nodes(
            calloway.node_key,
            commander.node_key,
            edge_type="official_report",
            latency_seconds=-1,
        )
        self.assertFalse(ok)
        self.assertEqual(message, "latency_seconds must be a non-negative integer")
        self.assertIsNone(edge)

        ok, message, edge = connect_social_nodes(
            calloway.node_key,
            commander.node_key,
            edge_type="official_report",
            bandwidth=1.5,
        )
        self.assertFalse(ok)
        self.assertEqual(message, "bandwidth must be a non-negative integer")
        self.assertIsNone(edge)
        self.assertEqual(SocialEdge.objects.count(), 0)

    def test_record_social_fact_rejects_unknown_actor_or_scope_nodes(self):
        from world.models import SocialFact
        from world.social_engine import ensure_social_node, record_social_fact

        player = ensure_social_node("player", str(self.char1.id), display_name=self.char1.key)

        ok, message, fact = record_social_fact(
            fact_key="fact:unknown_actor",
            subject_node_key=player.node_key,
            actor_node_key="npc:missing_actor",
            event_type="quest_completed",
            summary="Unknown actors should be rejected before persistence.",
        )
        self.assertFalse(ok)
        self.assertEqual(message, "unknown actor_node: npc:missing_actor")
        self.assertIsNone(fact)

        ok, message, fact = record_social_fact(
            fact_key="fact:unknown_scope",
            subject_node_key=player.node_key,
            scope_node_key="npc:missing_scope",
            event_type="quest_completed",
            summary="Unknown scopes should be rejected before persistence.",
        )
        self.assertFalse(ok)
        self.assertEqual(message, "unknown scope_node: npc:missing_scope")
        self.assertIsNone(fact)
        self.assertFalse(SocialFact.objects.filter(fact_key__startswith="fact:unknown").exists())

    def test_assert_social_claim_rejects_unknown_fact_key(self):
        from world.models import SocialClaim
        from world.social_engine import assert_social_claim, ensure_social_node

        player = ensure_social_node("player", str(self.char1.id), display_name=self.char1.key)
        calloway = ensure_social_node("npc", "npc_warden_agent_calloway")

        ok, message, claim = assert_social_claim(
            claim_key="claim:unknown_fact",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key="fact:missing",
            claim_type="report",
            summary="Missing facts should not silently become unattached claims.",
        )

        self.assertFalse(ok)
        self.assertEqual(message, "unknown fact: fact:missing")
        self.assertIsNone(claim)
        self.assertFalse(SocialClaim.objects.filter(claim_key="claim:unknown_fact").exists())

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

        ok, message, fact_knowledge = mark_known(
            node_key=calloway.node_key,
            fact_key=fact.fact_key,
            channel="direct_witness",
            confidence=1.0,
            spreading=False,
        )
        self.assertTrue(ok, message)
        ok, message, claim_knowledge = mark_known(
            node_key=calloway.node_key,
            claim_key=claim.claim_key,
            channel="direct_witness",
            confidence=1.0,
            spreading=True,
        )
        self.assertTrue(ok, message)
        self.assertEqual(fact_knowledge.node.node_key, calloway.node_key)
        self.assertEqual(claim_knowledge.node.node_key, calloway.node_key)
        self.assertIsNone(fact_knowledge.claim)
        self.assertIsNone(claim_knowledge.fact)

    def test_mark_known_rejects_unknown_source_node(self):
        from world.models import SocialKnowledge
        from world.social_engine import ensure_social_node, mark_known, record_social_fact

        player = ensure_social_node("player", str(self.char1.id), display_name=self.char1.key)
        calloway = ensure_social_node("npc", "npc_warden_agent_calloway")
        ok, message, fact = record_social_fact(
            fact_key="fact:known_source_check",
            subject_node_key=player.node_key,
            event_type="quest_completed",
            summary="Known fact for source-node validation.",
        )
        self.assertTrue(ok, message)

        ok, message, knowledge = mark_known(
            node_key=calloway.node_key,
            fact_key=fact.fact_key,
            source_node_key="npc:missing_source",
            channel="direct_witness",
        )

        self.assertFalse(ok)
        self.assertEqual(message, "unknown source_node: npc:missing_source")
        self.assertIsNone(knowledge)
        self.assertFalse(
            SocialKnowledge.objects.filter(
                knowledge_key=f"knowledge:{calloway.node_key}:{fact.fact_key}"
            ).exists()
        )

    def test_mark_known_rejects_fact_and_claim_together(self):
        from world.models import SocialKnowledge
        from world.social_engine import (
            assert_social_claim,
            ensure_social_node,
            mark_known,
            record_social_fact,
        )

        player = ensure_social_node("player", str(self.char1.id), display_name=self.char1.key)
        calloway = ensure_social_node("npc", "npc_warden_agent_calloway")
        ok, message, delivered_fact = record_social_fact(
            fact_key="fact:delivered_report",
            subject_node_key=player.node_key,
            event_type="quest_completed",
            summary="The player delivered the field report.",
        )
        self.assertTrue(ok, message)
        ok, message, claim = assert_social_claim(
            claim_key="claim:calloway:delivered_report",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key=delivered_fact.fact_key,
            claim_type="report",
            summary="Calloway reports the Warden business.",
            status="supported",
        )
        self.assertTrue(ok, message)

        ok, message, knowledge = mark_known(
            node_key=calloway.node_key,
            fact_key=delivered_fact.fact_key,
            claim_key=claim.claim_key,
            channel="direct_witness",
        )

        self.assertFalse(ok)
        self.assertEqual(message, "fact_key and claim_key are mutually exclusive")
        self.assertIsNone(knowledge)
        self.assertFalse(
            SocialKnowledge.objects.filter(
                knowledge_key=f"knowledge:{calloway.node_key}:{claim.claim_key}"
            ).exists()
        )

    def test_mark_known_keeps_claim_knowledge_separate_from_linked_fact(self):
        from world.social_engine import (
            assert_social_claim,
            ensure_social_node,
            mark_known,
            record_social_fact,
        )

        player = ensure_social_node("player", str(self.char1.id), display_name=self.char1.key)
        calloway = ensure_social_node("npc", "npc_warden_agent_calloway")
        ok, message, fact = record_social_fact(
            fact_key="fact:claim_infers_fact",
            subject_node_key=player.node_key,
            event_type="quest_completed",
            summary="The player delivered the field report.",
        )
        self.assertTrue(ok, message)
        ok, message, claim = assert_social_claim(
            claim_key="claim:calloway:claim_infers_fact",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="report",
            summary="Calloway reports that the player carried Warden business cleanly.",
            status="supported",
        )
        self.assertTrue(ok, message)

        ok, message, knowledge = mark_known(
            node_key=calloway.node_key,
            claim_key=claim.claim_key,
            channel="direct_witness",
        )

        self.assertTrue(ok, message)
        self.assertEqual(knowledge.claim, claim)
        self.assertIsNone(knowledge.fact)
        self.assertEqual(knowledge.claim.fact, fact)

        from world.social_engine import query_social_context

        context = query_social_context(
            viewer_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
        )
        self.assertEqual(context["facts"], [])
        self.assertEqual(
            [item["claim_key"] for item in context["claims"]],
            [claim.claim_key],
        )

    def test_available_now_filter_uses_single_q_filter(self):
        from django.db.models import Q
        from world.social_engine import available_now_filter

        class RecordingQuerySet:
            def __init__(self):
                self.calls = []

            def filter(self, *args, **kwargs):
                self.calls.append((args, kwargs))
                return "filtered"

        queryset = RecordingQuerySet()

        result = available_now_filter(queryset)

        self.assertEqual(result, "filtered")
        self.assertEqual(len(queryset.calls), 1)
        args, kwargs = queryset.calls[0]
        self.assertEqual(kwargs, {})
        self.assertEqual(len(args), 1)
        self.assertIsInstance(args[0], Q)

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


class TestSocialWebPropagation(EvenniaTest):
    """Knowledge crosses only real contact edges."""

    def _seed_report_graph(self):
        from world.social_engine import (
            assert_social_claim,
            connect_social_nodes,
            ensure_social_node,
            mark_known,
            record_social_fact,
        )

        player = ensure_social_node("player", str(self.char1.id), display_name=self.char1.key)
        calloway = ensure_social_node(
            "npc",
            "npc_warden_agent_calloway",
            display_name="Agent Calloway",
        )
        commander = ensure_social_node(
            "npc",
            "npc_warden_outpost_commander",
            display_name="Outpost Commander",
        )
        innkeeper = ensure_social_node(
            "npc",
            "npc_innkeeper_whistle",
            display_name="Whistle Innkeeper",
        )
        ok, message, edge = connect_social_nodes(
            calloway.node_key,
            commander.node_key,
            edge_type="warden_report",
            directionality="one_way",
            trust=0.8,
            latency_seconds=60,
            scope_tags=["warden", "report", "quest"],
        )
        self.assertTrue(ok, message)
        ok, message, innkeeper_edge = connect_social_nodes(
            calloway.node_key,
            innkeeper.node_key,
            edge_type="inn_traveler",
            directionality="one_way",
            trust=0.6,
            scope_tags=["market"],
        )
        self.assertTrue(ok, message)
        ok, message, fact = record_social_fact(
            fact_key="fact:test_warden_report_delivered",
            subject_node_key=player.node_key,
            scope_node_key=calloway.node_key,
            event_type="quest_completed",
            summary="The player delivered Calloway's sealed field report.",
            tags=["reliable", "warden", "report"],
            visibility="institutional",
        )
        self.assertTrue(ok, message)
        ok, message, claim = assert_social_claim(
            claim_key="claim:calloway:test_warden_report_delivered",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="report",
            summary="Calloway reports the player carried Warden business cleanly.",
            status="supported",
            bias_tags=["warden", "report", "quest"],
        )
        self.assertTrue(ok, message)
        ok, message, knowledge = mark_known(
            node_key=calloway.node_key,
            claim_key=claim.claim_key,
            channel="official_report",
            confidence=0.95,
            spreading=True,
        )
        self.assertTrue(ok, message)
        return player, calloway, commander, innkeeper, edge, innkeeper_edge, fact, claim, knowledge

    def test_propagation_uses_matching_warden_contact_edge(self):
        from django.utils import timezone
        from world.models import SocialKnowledge
        from world.social_engine import propagate_social_knowledge

        (
            _player,
            calloway,
            commander,
            innkeeper,
            _edge,
            _innkeeper_edge,
            _fact,
            claim,
            _knowledge,
        ) = self._seed_report_graph()
        before = timezone.now()

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        target_keys = [item.node.node_key for item in propagated]
        self.assertEqual(target_keys, [commander.node_key])
        self.assertNotIn(innkeeper.node_key, target_keys)
        target_knowledge = propagated[0]
        self.assertEqual(target_knowledge.confidence, 0.8)
        self.assertIsNotNone(target_knowledge.available_after)
        self.assertGreater(target_knowledge.available_after, before)
        self.assertFalse(target_knowledge.spreading)
        self.assertFalse(
            SocialKnowledge.objects.filter(
                node=innkeeper,
                claim=claim,
            ).exists()
        )

    def test_propagation_sets_spreading_from_edge_directionality(self):
        from world.models import SocialEdge
        from world.social_engine import propagate_social_knowledge

        (
            _player,
            calloway,
            _commander,
            _innkeeper,
            edge,
            _innkeeper_edge,
            _fact,
            claim,
            _knowledge,
        ) = self._seed_report_graph()

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )
        self.assertEqual(len(propagated), 1)
        self.assertFalse(propagated[0].spreading)

        SocialEdge.objects.filter(id=edge.id).update(directionality="two_way")

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual(len(propagated), 1)
        self.assertTrue(propagated[0].spreading)

    def test_fact_only_propagation_never_substitutes_a_linked_claim(self):
        from world.social_engine import mark_known, propagate_social_knowledge

        (
            _player,
            calloway,
            commander,
            _innkeeper,
            _edge,
            _innkeeper_edge,
            fact,
            claim,
            _knowledge,
        ) = self._seed_report_graph()
        ok, message, _fact_only_knowledge = mark_known(
            node_key=calloway.node_key,
            fact_key=fact.fact_key,
            channel="direct_witness",
            confidence=0.4,
            spreading=True,
        )
        self.assertTrue(ok, message)

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            fact_key=fact.fact_key,
        )

        self.assertEqual(len(propagated), 1)
        self.assertEqual(propagated[0].node, commander)
        self.assertEqual(propagated[0].fact, fact)
        self.assertIsNone(propagated[0].claim)
        self.assertEqual(
            propagated[0].knowledge_key,
            f"knowledge:{commander.node_key}:{fact.fact_key}",
        )
        self.assertEqual(propagated[0].confidence, 0.4)

    def test_future_source_knowledge_does_not_propagate(self):
        from datetime import timedelta

        from django.utils import timezone
        from world.models import SocialKnowledge
        from world.social_engine import propagate_social_knowledge

        (
            _player,
            calloway,
            commander,
            _innkeeper,
            _edge,
            _innkeeper_edge,
            _fact,
            claim,
            knowledge,
        ) = self._seed_report_graph()
        knowledge.available_after = timezone.now() + timedelta(hours=1)
        knowledge.save(update_fields=["available_after"])

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual(propagated, [])
        self.assertFalse(
            SocialKnowledge.objects.filter(
                node=commander,
                claim=claim,
            ).exists()
        )

    def test_repeated_propagation_preserves_existing_availability(self):
        from world.models import SocialEdge
        from world.social_engine import propagate_social_knowledge

        (
            _player,
            calloway,
            _commander,
            _innkeeper,
            edge,
            _innkeeper_edge,
            _fact,
            claim,
            _knowledge,
        ) = self._seed_report_graph()

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )
        target_knowledge = propagated[0]
        first_available_after = target_knowledge.available_after
        self.assertIsNotNone(first_available_after)

        SocialEdge.objects.filter(id=edge.id).update(latency_seconds=3600)
        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        target_knowledge = propagated[0]
        target_knowledge.refresh_from_db()
        self.assertEqual(target_knowledge.available_after, first_available_after)

        target_knowledge.available_after = None
        target_knowledge.save(update_fields=["available_after"])
        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        target_knowledge = propagated[0]
        target_knowledge.refresh_from_db()
        self.assertIsNone(target_knowledge.available_after)

    def test_claim_metadata_tags_can_satisfy_edge_scope(self):
        from world.models import SocialEdge
        from world.social_engine import propagate_social_knowledge

        (
            _player,
            calloway,
            commander,
            _innkeeper,
            edge,
            _innkeeper_edge,
            _fact,
            claim,
            _knowledge,
        ) = self._seed_report_graph()
        SocialEdge.objects.filter(id=edge.id).update(scope_tags=["supported"])

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual([item.node.node_key for item in propagated], [commander.node_key])
        self.assertEqual(propagated[0].claim, claim)

    def test_propagation_rejects_edge_without_matching_scope_tags(self):
        from world.models import SocialEdge, SocialKnowledge
        from world.social_engine import propagate_social_knowledge

        (
            _player,
            calloway,
            commander,
            _innkeeper,
            edge,
            _innkeeper_edge,
            _fact,
            claim,
            _knowledge,
        ) = self._seed_report_graph()
        SocialEdge.objects.filter(id=edge.id).update(scope_tags=["market"])

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual(propagated, [])
        self.assertFalse(
            SocialKnowledge.objects.filter(
                node=commander,
                claim=claim,
            ).exists()
        )

    def test_inactive_and_zero_bandwidth_edges_do_not_propagate(self):
        from world.models import SocialEdge, SocialKnowledge
        from world.social_engine import propagate_social_knowledge

        (
            _player,
            calloway,
            commander,
            _innkeeper,
            edge,
            _innkeeper_edge,
            _fact,
            claim,
            _knowledge,
        ) = self._seed_report_graph()
        SocialEdge.objects.filter(id=edge.id).update(active=False)

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual(propagated, [])
        self.assertFalse(SocialKnowledge.objects.filter(node=commander, claim=claim).exists())

        SocialEdge.objects.filter(id=edge.id).update(active=True, bandwidth=0)
        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual(propagated, [])
        self.assertFalse(SocialKnowledge.objects.filter(node=commander, claim=claim).exists())

    def test_blockers_require_payload_unblock_tag(self):
        from world.models import SocialEdge, SocialKnowledge
        from world.social_engine import propagate_social_knowledge

        (
            _player,
            calloway,
            commander,
            _innkeeper,
            edge,
            _innkeeper_edge,
            _fact,
            claim,
            _knowledge,
        ) = self._seed_report_graph()
        SocialEdge.objects.filter(id=edge.id).update(
            scope_tags=["warden"],
            blockers=["field_clearance"],
        )

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual(propagated, [])
        self.assertFalse(SocialKnowledge.objects.filter(node=commander, claim=claim).exists())

        claim.bias_tags = ["warden", "report", "field_clearance"]
        claim.save(update_fields=["bias_tags"])
        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual([item.node.node_key for item in propagated], [commander.node_key])

    def test_two_way_edges_allow_reverse_propagation_without_one_way_backflow(self):
        from world.models import SocialEdge, SocialKnowledge
        from world.social_engine import mark_known, propagate_social_knowledge

        (
            _player,
            calloway,
            commander,
            _innkeeper,
            edge,
            _innkeeper_edge,
            fact,
            claim,
            _knowledge,
        ) = self._seed_report_graph()
        SocialKnowledge.objects.filter(node=calloway, claim=claim).delete()
        ok, message, _commander_knowledge = mark_known(
            node_key=commander.node_key,
            claim_key=claim.claim_key,
            channel="official_report",
            confidence=0.9,
            spreading=True,
        )
        self.assertTrue(ok, message)

        propagated = propagate_social_knowledge(
            source_node_key=commander.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual(propagated, [])
        self.assertFalse(SocialKnowledge.objects.filter(node=calloway, claim=claim).exists())

        SocialEdge.objects.filter(id=edge.id).update(directionality="two_way")
        propagated = propagate_social_knowledge(
            source_node_key=commander.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual([item.node.node_key for item in propagated], [calloway.node_key])

    def test_edge_type_maps_to_channel_without_flattening_routes(self):
        from world.models import SocialEdge
        from world.social_engine import propagate_social_knowledge

        (
            _player,
            calloway,
            commander,
            innkeeper,
            edge,
            innkeeper_edge,
            _fact,
            claim,
            _knowledge,
        ) = self._seed_report_graph()
        SocialEdge.objects.filter(id=edge.id).update(latency_seconds=0)
        SocialEdge.objects.filter(id=innkeeper_edge.id).update(
            edge_type="market_route",
            scope_tags=["warden"],
        )

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        channels_by_node = {item.node.node_key: item.channel for item in propagated}
        self.assertEqual(channels_by_node[commander.node_key], "official_report")
        self.assertEqual(channels_by_node[innkeeper.node_key], "market_gossip")

    def test_distortion_creates_deterministic_rumor_claim_copy(self):
        from world.models import SocialEdge, SocialKnowledge
        from world.social_engine import propagate_social_knowledge

        (
            _player,
            calloway,
            _commander,
            innkeeper,
            _edge,
            innkeeper_edge,
            _fact,
            claim,
            _knowledge,
        ) = self._seed_report_graph()
        SocialEdge.objects.filter(id=innkeeper_edge.id).update(
            distortion="rumor",
            scope_tags=["warden"],
        )

        first = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )
        second = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        innkeeper_knowledge = [item for item in first if item.node == innkeeper][0]
        self.assertNotEqual(innkeeper_knowledge.claim.claim_key, claim.claim_key)
        self.assertEqual(innkeeper_knowledge.claim.claim_type, "rumor")
        self.assertEqual(innkeeper_knowledge.claim.status, "rumor")
        self.assertEqual(innkeeper_knowledge.claim.speaker_node, innkeeper)
        self.assertIn("road rumor", innkeeper_knowledge.claim.summary)
        self.assertEqual(innkeeper_knowledge.channel, "tavern_rumor")
        self.assertFalse(
            SocialKnowledge.objects.filter(
                node=innkeeper,
                claim=claim,
            ).exists()
        )
        self.assertEqual(
            [item.claim.claim_key for item in first if item.node == innkeeper],
            [item.claim.claim_key for item in second if item.node == innkeeper],
        )

    def test_trace_social_route_explains_how_target_learned_claim(self):
        from world.social_engine import propagate_social_knowledge, trace_social_route

        (
            _player,
            calloway,
            commander,
            _innkeeper,
            _edge,
            _innkeeper_edge,
            _fact,
            claim,
            _knowledge,
        ) = self._seed_report_graph()
        propagate_social_knowledge(source_node_key=calloway.node_key, claim_key=claim.claim_key)

        trace = trace_social_route(
            source_node_key=calloway.node_key,
            target_node_key=commander.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual(len(trace), 1)
        self.assertEqual(trace[0]["from_node"], calloway.node_key)
        self.assertEqual(trace[0]["to_node"], commander.node_key)
        self.assertEqual(trace[0]["edge_type"], "warden_report")
        self.assertIn("Calloway", trace[0]["summary"])


class TestSocialContextPack(EvenniaTest):
    """Context packs expose only bounded, cited social knowledge."""

    def _seed_context_graph(self):
        from world.social_engine import (
            assert_social_claim,
            connect_social_nodes,
            ensure_social_node,
            mark_known,
            propagate_social_knowledge,
            record_social_fact,
        )

        player = ensure_social_node(
            "player",
            str(self.char1.id),
            display_name=self.char1.key,
            zone_id="vaels_crossing",
            settlement_id="vaels_crossing",
        )
        calloway = ensure_social_node(
            "npc",
            "npc_warden_agent_calloway",
            display_name="Agent Calloway",
            zone_id="vaels_crossing",
            settlement_id="vaels_crossing",
            faction_id="wardens",
        )
        commander = ensure_social_node(
            "npc",
            "npc_warden_outpost_commander",
            display_name="Outpost Commander",
            zone_id="ashreach_plains",
            settlement_id="ashreach_outpost",
            faction_id="wardens",
        )
        ok, message, _edge = connect_social_nodes(
            calloway.node_key,
            commander.node_key,
            edge_type="warden_report",
            directionality="one_way",
            trust=0.9,
            scope_tags=["warden", "report"],
        )
        self.assertTrue(ok, message)
        ok, message, fact = record_social_fact(
            fact_key="fact:context_pack_report",
            subject_node_key=player.node_key,
            scope_node_key=calloway.node_key,
            event_type="quest_completed",
            summary="The player delivered the sealed report.",
            tags=["warden", "report", "reliable"],
            visibility="institutional",
        )
        self.assertTrue(ok, message)
        ok, message, claim = assert_social_claim(
            claim_key="claim:context_pack_report",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="report",
            summary="Calloway says the player did not drop the name.",
            status="supported",
            bias_tags=["warden", "report", "reliable"],
        )
        self.assertTrue(ok, message)
        ok, message, _fact_knowledge = mark_known(
            node_key=calloway.node_key,
            fact_key=fact.fact_key,
            channel="official_report",
            confidence=1.0,
            spreading=True,
        )
        self.assertTrue(ok, message)
        ok, message, _claim_knowledge = mark_known(
            node_key=calloway.node_key,
            claim_key=claim.claim_key,
            channel="official_report",
            confidence=1.0,
            spreading=True,
        )
        self.assertTrue(ok, message)
        propagated_facts = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            fact_key=fact.fact_key,
        )
        propagated_claims = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )
        self.assertEqual(
            [item.node.node_key for item in propagated_facts],
            [commander.node_key],
        )
        self.assertEqual(
            [item.node.node_key for item in propagated_claims],
            [commander.node_key],
        )
        return player, calloway, commander, fact, claim

    def _record_commander_context_item(
        self,
        *,
        index,
        player,
        calloway,
        commander,
        confidence,
        available_after=None,
    ):
        from world.social_engine import assert_social_claim, mark_known, record_social_fact

        ok, message, fact = record_social_fact(
            fact_key=f"fact:context_bound_{index}",
            subject_node_key=player.node_key,
            scope_node_key=calloway.node_key,
            event_type="quest_completed",
            summary=f"Context bound fact {index}.",
            tags=["warden", "report"],
            visibility="institutional",
        )
        self.assertTrue(ok, message)
        ok, message, claim = assert_social_claim(
            claim_key=f"claim:context_bound_{index}",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="report",
            summary=f"Context bound claim {index}.",
            status="supported",
            bias_tags=["warden", "report"],
        )
        self.assertTrue(ok, message)
        ok, message, _fact_knowledge = mark_known(
            node_key=commander.node_key,
            fact_key=fact.fact_key,
            source_node_key=calloway.node_key,
            channel="official_report",
            confidence=confidence,
            available_after=available_after,
        )
        self.assertTrue(ok, message)
        ok, message, knowledge = mark_known(
            node_key=commander.node_key,
            claim_key=claim.claim_key,
            source_node_key=calloway.node_key,
            channel="official_report",
            confidence=confidence,
            available_after=available_after,
        )
        self.assertTrue(ok, message)
        return fact, claim, knowledge

    def test_query_social_context_returns_known_claims_with_traces(self):
        from world.social_engine import query_social_context

        player, calloway, commander, fact, claim = self._seed_context_graph()

        context = query_social_context(
            viewer_node_key=commander.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
        )

        self.assertEqual(
            context["viewer"],
            {
                "node_key": commander.node_key,
                "node_type": "npc",
                "display_name": "Outpost Commander",
                "zone_id": "ashreach_plains",
                "settlement_id": "ashreach_outpost",
                "faction_id": "wardens",
            },
        )
        self.assertEqual(context["subject"]["node_key"], player.node_key)
        self.assertEqual(context["purpose"], "dialogue")
        self.assertEqual(context["facts"][0]["fact_key"], fact.fact_key)
        self.assertEqual(context["facts"][0]["event_type"], "quest_completed")
        self.assertEqual(context["facts"][0]["visibility"], "institutional")
        self.assertEqual(context["facts"][0]["channel"], "official_report")
        self.assertEqual(context["claims"][0]["claim_key"], claim.claim_key)
        self.assertEqual(context["claims"][0]["status"], "supported")
        self.assertEqual(context["claims"][0]["speaker"]["node_key"], calloway.node_key)
        self.assertEqual(context["claims"][0]["trace"][0]["edge_type"], "warden_report")

    def test_query_social_context_returns_known_facts_with_traces(self):
        from world.social_engine import query_social_context

        player, _calloway, commander, fact, _claim = self._seed_context_graph()

        context = query_social_context(
            viewer_node_key=commander.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
        )

        self.assertEqual(context["facts"][0]["fact_key"], fact.fact_key)
        self.assertEqual(context["facts"][0]["trace"][0]["edge_type"], "warden_report")
        self.assertIn("propagated", context["facts"][0]["trace"][0]["summary"])

    def test_context_excludes_future_knowledge_and_bounds_facts_and_claims(self):
        from datetime import timedelta

        from django.utils import timezone
        from world.social_engine import query_social_context

        player, calloway, commander, base_fact, base_claim = self._seed_context_graph()
        future_available_after = timezone.now() + timedelta(hours=1)
        future_fact, future_claim, _future_knowledge = self._record_commander_context_item(
            index="future",
            player=player,
            calloway=calloway,
            commander=commander,
            confidence=1.0,
            available_after=future_available_after,
        )
        first_fact, first_claim, _first_knowledge = self._record_commander_context_item(
            index="first",
            player=player,
            calloway=calloway,
            commander=commander,
            confidence=0.8,
        )
        second_fact, second_claim, _second_knowledge = self._record_commander_context_item(
            index="second",
            player=player,
            calloway=calloway,
            commander=commander,
            confidence=0.7,
        )
        third_fact, third_claim, _third_knowledge = self._record_commander_context_item(
            index="third",
            player=player,
            calloway=calloway,
            commander=commander,
            confidence=0.6,
        )

        context = query_social_context(
            viewer_node_key=commander.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
            max_items=2,
        )

        fact_keys = [item["fact_key"] for item in context["facts"]]
        claim_keys = [item["claim_key"] for item in context["claims"]]
        self.assertEqual(len(fact_keys), 2)
        self.assertEqual(len(claim_keys), 2)
        self.assertNotIn(future_fact.fact_key, fact_keys)
        self.assertNotIn(future_claim.claim_key, claim_keys)
        self.assertIn(base_fact.fact_key, fact_keys)
        self.assertIn(base_claim.claim_key, claim_keys)
        self.assertIn(first_fact.fact_key, fact_keys)
        self.assertNotIn(second_fact.fact_key, fact_keys)
        self.assertNotIn(third_fact.fact_key, fact_keys)
        self.assertIn(first_claim.claim_key, claim_keys)
        self.assertNotIn(second_claim.claim_key, claim_keys)
        self.assertNotIn(third_claim.claim_key, claim_keys)

    def test_context_deduplicates_before_applying_max_items(self):
        from world.models import SocialKnowledge
        from world.social_engine import query_social_context

        player, calloway, commander, base_fact, base_claim = self._seed_context_graph()
        SocialKnowledge.objects.create(
            knowledge_key=(
                f"knowledge:{commander.node_key}:{base_claim.claim_key}:duplicate"
            ),
            node=commander,
            claim=base_claim,
            source_node=calloway,
            channel="official_report",
            confidence=0.85,
        )
        distinct_fact, distinct_claim, _distinct_knowledge = (
            self._record_commander_context_item(
                index="distinct",
                player=player,
                calloway=calloway,
                commander=commander,
                confidence=0.8,
            )
        )

        context = query_social_context(
            viewer_node_key=commander.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
            max_items=2,
        )

        self.assertEqual(
            [item["fact_key"] for item in context["facts"]],
            [base_fact.fact_key, distinct_fact.fact_key],
        )
        self.assertEqual(
            [item["claim_key"] for item in context["claims"]],
            [base_claim.claim_key, distinct_claim.claim_key],
        )

    def test_context_claim_trace_uses_exact_available_knowledge_row(self):
        from datetime import timedelta

        from django.utils import timezone
        from world.models import SocialEdge, SocialKnowledge, SocialTrace
        from world.social_engine import query_social_context

        player, calloway, commander, fact, claim = self._seed_context_graph()
        edge = SocialEdge.objects.get(
            source_node=calloway,
            target_node=commander,
            edge_type="warden_report",
        )
        future_knowledge = SocialKnowledge.objects.create(
            knowledge_key=f"knowledge:{commander.node_key}:{claim.claim_key}:future",
            node=commander,
            claim=claim,
            source_node=calloway,
            edge=edge,
            channel="official_report",
            confidence=1.0,
            available_after=timezone.now() + timedelta(hours=1),
        )
        SocialTrace.objects.create(
            trace_key=f"trace:{future_knowledge.knowledge_key}:future",
            knowledge=future_knowledge,
            from_node=calloway,
            to_node=commander,
            edge=edge,
            summary="Future unavailable trace should not leak into context.",
        )

        context = query_social_context(
            viewer_node_key=commander.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
        )

        trace_summaries = [
            item["summary"] for item in context["claims"][0]["trace"]
        ]
        self.assertEqual(len(trace_summaries), 1)
        self.assertNotIn(
            "Future unavailable trace should not leak into context.",
            trace_summaries,
        )

    def test_context_purpose_is_primitive_string(self):
        from world.social_engine import query_social_context

        class Purpose:
            def __str__(self):
                return "dialogue:warden"

        player, _calloway, commander, _fact, _claim = self._seed_context_graph()

        context = query_social_context(
            viewer_node_key=commander.node_key,
            subject_node_key=player.node_key,
            purpose=Purpose(),
        )

        self.assertEqual(context["purpose"], "dialogue:warden")
        self.assertIsInstance(context["purpose"], str)

    def test_missing_viewer_or_subject_returns_empty_context(self):
        from world.social_engine import ensure_social_node, query_social_context

        player = ensure_social_node("player", str(self.char1.id), display_name=self.char1.key)
        commander = ensure_social_node(
            "npc",
            "npc_warden_outpost_commander",
            display_name="Outpost Commander",
        )

        missing_viewer_context = query_social_context(
            viewer_node_key="npc:missing_viewer",
            subject_node_key=player.node_key,
            purpose="dialogue",
        )
        missing_subject_context = query_social_context(
            viewer_node_key=commander.node_key,
            subject_node_key="player:missing_subject",
            purpose="dialogue",
        )

        self.assertEqual(missing_viewer_context["viewer"], {})
        self.assertEqual(missing_viewer_context["subject"]["node_key"], player.node_key)
        self.assertEqual(missing_viewer_context["facts"], [])
        self.assertEqual(missing_viewer_context["claims"], [])
        self.assertEqual(missing_subject_context["viewer"]["node_key"], commander.node_key)
        self.assertEqual(missing_subject_context["subject"], {})
        self.assertEqual(missing_subject_context["facts"], [])
        self.assertEqual(missing_subject_context["claims"], [])
