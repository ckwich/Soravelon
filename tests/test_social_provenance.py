"""Independent Social Web provenance routes must remain explainable."""

from evennia.utils.test_resources import EvenniaTest


class TestSocialProvenanceRoutes(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.social_engine import ensure_social_node, record_social_fact

        self.player = ensure_social_node(
            "player",
            str(self.char1.id),
            display_name=self.char1.key,
        )
        self.first_source = ensure_social_node("npc", "first_source")
        self.second_source = ensure_social_node("npc", "second_source")
        self.target = ensure_social_node("npc", "target")
        ok, message, self.fact = record_social_fact(
            fact_key=f"fact:{self.char1.id}:provenance",
            subject_node_key=self.player.node_key,
            event_type="provenance_test",
            summary="Two independent contacts can verify this fact.",
            tags=["provenance", "test"],
            visibility="institutional",
        )
        self.assertTrue(ok, message)

    def test_direct_routes_from_two_sources_do_not_collide(self):
        from world.social_engine import mark_known, record_trace
        from world.models import SocialTrace

        ok, message, knowledge = mark_known(
            node_key=self.target.node_key,
            fact_key=self.fact.fact_key,
            channel="direct_witness",
            confidence=0.8,
        )
        self.assertTrue(ok, message)

        record_trace(
            knowledge,
            from_node=self.first_source,
            to_node=self.target,
            summary="First source gave direct testimony.",
        )
        record_trace(
            knowledge,
            from_node=self.second_source,
            to_node=self.target,
            summary="Second source gave independent testimony.",
        )
        record_trace(
            knowledge,
            from_node=self.first_source,
            to_node=self.target,
            summary="First source replayed the same route.",
        )

        traces = SocialTrace.objects.filter(knowledge=knowledge).order_by("id")
        self.assertEqual(traces.count(), 2)
        self.assertEqual(
            set(traces.values_list("from_node__node_key", flat=True)),
            {self.first_source.node_key, self.second_source.node_key},
        )
        self.assertEqual(
            SocialTrace.objects.filter(
                knowledge=knowledge,
                from_node=self.first_source,
            ).get().summary,
            "First source replayed the same route.",
        )

    def test_two_propagation_routes_keep_both_traces_and_stronger_confidence(self):
        from world.social_engine import (
            connect_social_nodes,
            mark_known,
            propagate_social_knowledge,
            query_social_context,
        )
        from world.models import SocialKnowledge

        for source in (self.first_source, self.second_source):
            ok, message, _knowledge = mark_known(
                node_key=source.node_key,
                fact_key=self.fact.fact_key,
                channel="direct_witness",
                confidence=0.95,
                spreading=True,
            )
            self.assertTrue(ok, message)

        ok, message, _edge = connect_social_nodes(
            self.first_source.node_key,
            self.target.node_key,
            edge_type="official_report",
            trust=0.9,
        )
        self.assertTrue(ok, message)
        ok, message, _edge = connect_social_nodes(
            self.second_source.node_key,
            self.target.node_key,
            edge_type="market_route",
            trust=0.3,
        )
        self.assertTrue(ok, message)

        propagate_social_knowledge(
            source_node_key=self.first_source.node_key,
            fact_key=self.fact.fact_key,
        )
        propagate_social_knowledge(
            source_node_key=self.second_source.node_key,
            fact_key=self.fact.fact_key,
        )
        propagate_social_knowledge(
            source_node_key=self.first_source.node_key,
            fact_key=self.fact.fact_key,
        )

        knowledge = SocialKnowledge.objects.get(
            node=self.target,
            fact=self.fact,
        )
        self.assertEqual(knowledge.confidence, 0.9)
        self.assertEqual(knowledge.traces.count(), 2)
        context = query_social_context(
            viewer_node_key=self.target.node_key,
            subject_node_key=self.player.node_key,
            purpose="dialogue",
        )
        self.assertEqual(len(context["facts"]), 1)
        self.assertEqual(
            {trace["edge_type"] for trace in context["facts"][0]["trace"]},
            {"official_report", "market_route"},
        )
