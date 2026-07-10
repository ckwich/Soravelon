"""Bounded Social Web presentation and exact eligibility evidence."""

from datetime import timedelta

from django.utils import timezone
from evennia.utils.test_resources import EvenniaTest


class TestSocialRetrieval(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.social_engine import ensure_social_node

        self.player = ensure_social_node("player", str(self.char1.id))
        self.viewer = ensure_social_node("npc", "retrieval_viewer")

    def _fact(self, suffix, *, tags=None, visibility="institutional", expires_at=None):
        from world.social_engine import record_social_fact

        ok, message, fact = record_social_fact(
            fact_key=f"fact:{self.char1.id}:retrieval:{suffix}",
            subject_node_key=self.player.node_key,
            event_type="retrieval_test",
            summary=f"Retrieval fixture {suffix}.",
            tags=tags or ["retrieval"],
            visibility=visibility,
            expires_at=expires_at,
        )
        self.assertTrue(ok, message)
        return fact

    def test_context_clamps_facts_and_claims_before_building_the_packet(self):
        from world.social_engine import (
            assert_social_claim,
            mark_known,
            query_social_context,
        )

        for index in range(6):
            fact = self._fact(f"context:{index}")
            ok, message, claim = assert_social_claim(
                claim_key=f"claim:{self.char1.id}:retrieval:{index}",
                speaker_node_key=self.viewer.node_key,
                subject_node_key=self.player.node_key,
                fact_key=fact.fact_key,
                claim_type="report",
                summary=f"Retrieval claim {index}.",
                status="supported",
                visibility="institutional",
            )
            self.assertTrue(ok, message)
            for payload in (
                {"fact_key": fact.fact_key},
                {"claim_key": claim.claim_key},
            ):
                ok, message, _knowledge = mark_known(
                    node_key=self.viewer.node_key,
                    channel="official_report",
                    confidence=1.0 - (index * 0.01),
                    **payload,
                )
                self.assertTrue(ok, message)

        context = query_social_context(
            viewer_node_key=self.viewer.node_key,
            subject_node_key=self.player.node_key,
            purpose="dialogue",
            max_items=999,
        )

        self.assertEqual(len(context["facts"]), 5)
        self.assertEqual(len(context["claims"]), 5)

    def test_exact_evidence_search_excludes_private_and_expired_facts(self):
        from world.social_engine import find_social_evidence, mark_known

        private_fact = self._fact("private", visibility="private")
        expired_fact = self._fact(
            "expired",
            expires_at=timezone.now() - timedelta(seconds=1),
        )
        for fact in (private_fact, expired_fact):
            ok, message, _knowledge = mark_known(
                node_key=self.viewer.node_key,
                fact_key=fact.fact_key,
                channel="direct_witness",
            )
            self.assertTrue(ok, message)

        evidence = find_social_evidence(
            viewer_node_key=self.viewer.node_key,
            subject_node_key=self.player.node_key,
            purpose="quest_offer",
            required_fact_tags=["retrieval"],
            fact_key_fragment="retrieval",
        )

        self.assertEqual(evidence, [])

    def test_exact_evidence_requires_all_predicates_on_the_same_fact(self):
        from world.social_engine import find_social_evidence, mark_known

        tags_only = self._fact("tags_only", tags=["required"])
        fragment_only = self._fact("matching_fragment", tags=["other"])
        matching = self._fact("matching_fact", tags=["required"])
        for fact in (tags_only, fragment_only, matching):
            ok, message, _knowledge = mark_known(
                node_key=self.viewer.node_key,
                fact_key=fact.fact_key,
                channel="direct_witness",
            )
            self.assertTrue(ok, message)

        evidence = find_social_evidence(
            viewer_node_key=self.viewer.node_key,
            subject_node_key=self.player.node_key,
            purpose="quest_offer",
            required_fact_tags=["required"],
            fact_key_fragment="matching_",
            max_results=5,
        )

        self.assertEqual(
            [item["fact_key"] for item in evidence],
            [matching.fact_key],
        )

    def test_context_caps_trace_history_for_each_selected_payload(self):
        from world.models import SocialTrace
        from world.social_engine import mark_known, query_social_context

        fact = self._fact("trace_bound")
        ok, message, knowledge = mark_known(
            node_key=self.viewer.node_key,
            fact_key=fact.fact_key,
            channel="direct_witness",
        )
        self.assertTrue(ok, message)
        for index in range(6):
            SocialTrace.objects.create(
                trace_key=f"trace:{knowledge.id}:retrieval:{index}",
                route_key=f"route:retrieval:{knowledge.id}:{index}",
                knowledge=knowledge,
                to_node=self.viewer,
                summary=f"Retrieval trace {index}.",
            )

        context = query_social_context(
            viewer_node_key=self.viewer.node_key,
            subject_node_key=self.player.node_key,
            purpose="dialogue",
            max_items=1,
        )

        traces = context["facts"][0]["trace"]
        self.assertEqual(len(traces), 5)
        self.assertEqual(
            [trace["summary"] for trace in traces],
            [f"Retrieval trace {index}." for index in range(5)],
        )
