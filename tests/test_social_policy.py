"""Visibility, expiry, release, and edge-tag policy for the Social Web."""

from datetime import timedelta

from django.utils import timezone
from evennia.utils.test_resources import EvenniaTest


class TestSocialVisibilityPolicy(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.social_engine import ensure_social_node

        self.player = ensure_social_node("player", str(self.char1.id))
        self.source = ensure_social_node("npc", "policy_source")
        self.viewer = ensure_social_node("npc", "policy_viewer")

    def _fact(self, key, *, visibility="institutional", expires_at=None, tags=None):
        from world.social_engine import record_social_fact

        ok, message, fact = record_social_fact(
            fact_key=key,
            subject_node_key=self.player.node_key,
            event_type="policy_test",
            summary="A Social Web policy fixture.",
            tags=tags or ["warden", "report"],
            visibility=visibility,
            expires_at=expires_at,
        )
        self.assertTrue(ok, message)
        return fact

    def test_private_or_expired_payload_never_enters_dialogue_or_propagation(self):
        from world.social_engine import (
            mark_known,
            propagate_social_knowledge,
            query_social_context,
        )

        private_fact = self._fact(
            f"fact:{self.char1.id}:private",
            visibility="private",
        )
        expired_fact = self._fact(
            f"fact:{self.char1.id}:expired",
            expires_at=timezone.now() - timedelta(seconds=1),
        )
        for fact in (private_fact, expired_fact):
            ok, message, _knowledge = mark_known(
                node_key=self.source.node_key,
                fact_key=fact.fact_key,
                channel="direct_witness",
                spreading=True,
            )
            self.assertTrue(ok, message)

        context = query_social_context(
            viewer_node_key=self.source.node_key,
            subject_node_key=self.player.node_key,
            purpose="dialogue",
        )
        self.assertEqual(context["facts"], [])
        self.assertEqual(
            propagate_social_knowledge(
                source_node_key=self.source.node_key,
                fact_key=private_fact.fact_key,
            ),
            [],
        )
        self.assertEqual(
            propagate_social_knowledge(
                source_node_key=self.source.node_key,
                fact_key=expired_fact.fact_key,
            ),
            [],
        )

    def test_private_claim_stays_hidden_until_explicit_release(self):
        from world.social_engine import (
            assert_social_claim,
            mark_known,
            query_social_context,
        )
        from world.action_vocabulary import execute_action

        ok, message, claim = assert_social_claim(
            claim_key=f"claim:{self.char1.id}:private",
            speaker_node_key=self.source.node_key,
            subject_node_key=self.player.node_key,
            claim_type="report",
            summary="A private claim must not leak into dialogue.",
            visibility="private",
        )
        self.assertTrue(ok, message)
        ok, message, _knowledge = mark_known(
            node_key=self.viewer.node_key,
            claim_key=claim.claim_key,
            channel="direct_witness",
        )
        self.assertTrue(ok, message)

        private_context = query_social_context(
            viewer_node_key=self.viewer.node_key,
            subject_node_key=self.player.node_key,
            purpose="dialogue",
        )
        self.assertEqual(private_context["claims"], [])

        released, message = execute_action(
            {
                "action_type": "release_social_claim",
                "claim_key": claim.claim_key,
                "visibility": "institutional",
            },
            {"character": self.char1},
        )
        self.assertTrue(released, message)
        claim.refresh_from_db()
        released_context = query_social_context(
            viewer_node_key=self.viewer.node_key,
            subject_node_key=self.player.node_key,
            purpose="quest_offer",
        )
        self.assertEqual(
            [entry["claim_key"] for entry in released_context["claims"]],
            [claim.claim_key],
        )


class TestSocialEdgeTagPolicy(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.social_engine import ensure_social_node, record_social_fact

        self.player = ensure_social_node("player", str(self.char1.id))
        self.source = ensure_social_node("npc", "tag_policy_source")
        self.target = ensure_social_node("npc", "tag_policy_target")
        ok, message, self.fact = record_social_fact(
            fact_key=f"fact:{self.char1.id}:tag_policy",
            subject_node_key=self.player.node_key,
            event_type="tag_policy_test",
            summary="A Social Web edge policy fixture.",
            tags=["warden", "report"],
            visibility="institutional",
        )
        self.assertTrue(ok, message)

    def test_required_tags_are_all_required_and_blocked_tags_stop_propagation(self):
        from world.social_engine import (
            connect_social_nodes,
            mark_known,
            propagate_social_knowledge,
        )

        ok, message, _knowledge = mark_known(
            node_key=self.source.node_key,
            fact_key=self.fact.fact_key,
            channel="direct_witness",
            spreading=True,
        )
        self.assertTrue(ok, message)
        ok, message, edge = connect_social_nodes(
            self.source.node_key,
            self.target.node_key,
            edge_type="official_report",
            required_tags=["warden", "report"],
            blocked_tags=["sealed"],
        )
        self.assertTrue(ok, message)

        propagated = propagate_social_knowledge(
            source_node_key=self.source.node_key,
            fact_key=self.fact.fact_key,
        )
        self.assertEqual([item.node for item in propagated], [self.target])

        self.fact.tags = ["warden", "report", "sealed"]
        self.fact.save(update_fields=["tags"])
        self.assertEqual(
            propagate_social_knowledge(
                source_node_key=self.source.node_key,
                fact_key=self.fact.fact_key,
            ),
            [],
        )

        edge.required_tags = ["warden", "missing"]
        edge.blocked_tags = []
        edge.save(update_fields=["required_tags", "blocked_tags"])
        self.fact.tags = ["warden", "report"]
        self.fact.save(update_fields=["tags"])
        self.assertEqual(
            propagate_social_knowledge(
                source_node_key=self.source.node_key,
                fact_key=self.fact.fact_key,
            ),
            [],
        )

    def test_gatekept_edge_requires_an_explicit_gate(self):
        from world.social_engine import connect_social_nodes

        ok, message, edge = connect_social_nodes(
            self.source.node_key,
            self.target.node_key,
            edge_type="official_report",
            directionality="gatekept",
        )

        self.assertFalse(ok)
        self.assertIsNone(edge)
        self.assertIn("required_tags", message)
