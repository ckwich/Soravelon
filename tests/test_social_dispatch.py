"""Bounded scheduled propagation for the Social Web."""

from datetime import timedelta

from django.utils import timezone
from evennia.utils.test_resources import EvenniaTest


class TestSocialPropagationDispatch(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.social_engine import ensure_social_node

        self.player = ensure_social_node("player", str(self.char1.id))
        self.source = ensure_social_node("npc", "dispatch_source")
        self.target = ensure_social_node("npc", "dispatch_target")

    def _record_fact(self, suffix):
        from world.social_engine import record_social_fact

        ok, message, fact = record_social_fact(
            fact_key=f"fact:{self.char1.id}:dispatch:{suffix}",
            subject_node_key=self.player.node_key,
            event_type="dispatch_test",
            summary=f"Dispatch fixture {suffix}.",
            tags=["dispatch", "test"],
            visibility="institutional",
        )
        self.assertTrue(ok, message)
        return fact

    def _connect(self, *, bandwidth=1, latency_seconds=0):
        from world.social_engine import connect_social_nodes

        ok, message, edge = connect_social_nodes(
            self.source.node_key,
            self.target.node_key,
            edge_type="official_report",
            directionality="one_way",
            bandwidth=bandwidth,
            latency_seconds=latency_seconds,
            scope_tags=["dispatch"],
        )
        self.assertTrue(ok, message)
        return edge

    def test_dispatch_enforces_edge_bandwidth_without_charging_replays(self):
        from world.models import SocialKnowledge
        from world.social_engine import (
            dispatch_due_social_knowledge,
            mark_known,
        )

        first_fact = self._record_fact("first")
        second_fact = self._record_fact("second")
        self._connect(bandwidth=1)
        for fact in (first_fact, second_fact):
            ok, message, _knowledge = mark_known(
                node_key=self.source.node_key,
                fact_key=fact.fact_key,
                channel="direct_witness",
                spreading=True,
            )
            self.assertTrue(ok, message)

        now = timezone.now()
        first_report = dispatch_due_social_knowledge(limit=2, now=now)

        self.assertEqual(first_report["processed_knowledge"], 2)
        self.assertEqual(first_report["created_routes"], 1)
        self.assertEqual(first_report["skipped_bandwidth"], 1)
        self.assertTrue(
            SocialKnowledge.objects.get(
                node=self.source,
                fact=first_fact,
            ).last_dispatched_at
        )
        self.assertEqual(
            SocialKnowledge.objects.filter(node=self.target).count(),
            1,
        )

        second_report = dispatch_due_social_knowledge(limit=10, now=now)

        self.assertEqual(second_report["created_routes"], 1)
        self.assertEqual(second_report["replayed_routes"], 1)
        self.assertEqual(second_report["skipped_bandwidth"], 0)
        self.assertEqual(
            set(
                SocialKnowledge.objects.filter(node=self.target).values_list(
                    "fact__fact_key",
                    flat=True,
                )
            ),
            {first_fact.fact_key, second_fact.fact_key},
        )

    def test_dispatch_only_processes_due_knowledge_and_uses_the_given_clock(self):
        from world.models import SocialKnowledge
        from world.social_engine import (
            dispatch_due_social_knowledge,
            mark_known,
        )

        fact = self._record_fact("delayed")
        self._connect(latency_seconds=30)
        now = timezone.now()
        due_at = now + timedelta(seconds=60)
        ok, message, _knowledge = mark_known(
            node_key=self.source.node_key,
            fact_key=fact.fact_key,
            channel="direct_witness",
            spreading=True,
            available_after=due_at,
        )
        self.assertTrue(ok, message)

        early_report = dispatch_due_social_knowledge(limit=10, now=now)
        self.assertEqual(early_report["processed_knowledge"], 0)
        self.assertFalse(SocialKnowledge.objects.filter(node=self.target).exists())

        due_report = dispatch_due_social_knowledge(limit=10, now=due_at)
        self.assertEqual(due_report["created_routes"], 1)
        target_knowledge = SocialKnowledge.objects.get(
            node=self.target,
            fact=fact,
        )
        self.assertEqual(
            target_knowledge.available_after,
            due_at + timedelta(seconds=30),
        )

    def test_explicit_propagation_uses_the_same_deterministic_clock(self):
        from world.social_engine import mark_known, propagate_social_knowledge

        fact = self._record_fact("explicit")
        self._connect(latency_seconds=15)
        ok, message, _knowledge = mark_known(
            node_key=self.source.node_key,
            fact_key=fact.fact_key,
            channel="direct_witness",
            spreading=True,
        )
        self.assertTrue(ok, message)
        now = timezone.now()

        propagated = propagate_social_knowledge(
            source_node_key=self.source.node_key,
            fact_key=fact.fact_key,
            now=now,
        )

        self.assertEqual(len(propagated), 1)
        self.assertEqual(propagated[0].available_after, now + timedelta(seconds=15))
