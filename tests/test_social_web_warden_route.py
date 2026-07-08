from types import SimpleNamespace
from unittest.mock import patch

from evennia.utils.test_resources import EvenniaTest


class TestVaelWardenSocialRoute(EvenniaTest):
    """Vael's Warden report can travel by contact edge without omniscience."""

    def _seed_warden_report_route(self):
        from world.models import SocialKnowledge
        from world.social_engine import (
            assert_social_claim,
            connect_social_nodes,
            ensure_social_node,
            mark_known,
            propagate_social_knowledge,
            query_social_context,
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
        innkeeper = ensure_social_node(
            "npc",
            "npc_innkeeper_whistle",
            display_name="Whistle",
            zone_id="vaels_crossing",
            settlement_id="vaels_crossing",
        )

        ok, message, edge = connect_social_nodes(
            calloway.node_key,
            commander.node_key,
            edge_type="warden_report",
            directionality="one_way",
            trust=0.95,
            latency_seconds=0,
            scope_tags=["warden", "report", "quest"],
        )
        self.assertTrue(ok, message)
        self.assertEqual(edge.latency_seconds, 0)

        ok, message, fact = record_social_fact(
            fact_key=f"fact:{self.char1.id}:vc_q_warden_report:delivered",
            subject_node_key=player.node_key,
            actor_node_key=player.node_key,
            scope_node_key=calloway.node_key,
            event_type="quest_completed",
            summary="The player delivered Calloway's sealed field report.",
            tags=["reliable", "warden", "report", "quest"],
            visibility="institutional",
            evidence={"quest_id": "vc_q_warden_report", "source": "test_fixture"},
        )
        self.assertTrue(ok, message)

        ok, message, claim = assert_social_claim(
            claim_key=f"claim:calloway:{self.char1.id}:vc_q_warden_report:delivered",
            speaker_node_key=calloway.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="report",
            summary="Calloway reports that the player carried Warden business cleanly.",
            status="supported",
            confidence=1.0,
        )
        self.assertTrue(ok, message)

        ok, message, knowledge = mark_known(
            node_key=calloway.node_key,
            fact_key=fact.fact_key,
            claim_key=claim.claim_key,
            channel="official_report",
            confidence=1.0,
            spreading=True,
        )
        self.assertTrue(ok, message)
        self.assertEqual(knowledge.node.node_key, calloway.node_key)

        propagated = propagate_social_knowledge(
            source_node_key=calloway.node_key,
            claim_key=claim.claim_key,
        )

        self.assertEqual(
            [item.node.node_key for item in propagated],
            [commander.node_key],
        )
        self.assertIsNone(propagated[0].available_after)
        self.assertFalse(
            SocialKnowledge.objects.filter(
                node=innkeeper,
                claim=claim,
            ).exists()
        )
        return player, calloway, commander, innkeeper, fact, claim

    def test_warden_report_reaches_outpost_contact_but_not_innkeeper(self):
        from world.social_engine import query_social_context

        (
            player,
            _calloway,
            commander,
            innkeeper,
            _fact,
            claim,
        ) = self._seed_warden_report_route()

        commander_context = query_social_context(
            viewer_node_key=commander.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
        )
        innkeeper_context = query_social_context(
            viewer_node_key=innkeeper.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
        )

        self.assertEqual(commander_context["claims"][0]["claim_key"], claim.claim_key)
        self.assertEqual(
            commander_context["claims"][0]["trace"][0]["edge_type"],
            "warden_report",
        )
        self.assertEqual(innkeeper_context["claims"], [])
        self.assertEqual(innkeeper_context["facts"], [])

    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_warden_report_route_drives_deterministic_dialogue(
        self,
        mock_context_packet,
        _mock_standing_tier,
        _mock_active_quests,
    ):
        from world.dialogue_engine import _build_dialogue_context, resolve_topic_response

        self._seed_warden_report_route()
        mock_context_packet.return_value = {
            "reputation": 0,
            "network": 0,
            "betrayal_flag": False,
        }
        shared_topics = {
            "report": {
                "social_claim_status:supported": (
                    "'I know the report. You carried Warden business cleanly.'"
                ),
                "social_claim_trace_edge:warden_report": (
                    "'Calloway's report reached my desk through the Warden line. "
                    "That route does not carry praise lightly.'"
                ),
                "default": (
                    "'I have no confirmed Warden report about you.'"
                ),
            }
        }

        def npc(npc_id, key, *, zone_id, faction):
            return SimpleNamespace(
                db=SimpleNamespace(
                    zone_id=zone_id,
                    faction=faction,
                    npc_id=npc_id,
                    dialogue_topics=shared_topics,
                ),
                key=key,
            )

        calloway_npc = npc(
            "npc_warden_agent_calloway",
            "Agent Calloway",
            zone_id="vaels_crossing",
            faction="wardens",
        )
        harven_npc = npc(
            "npc_warden_outpost_commander",
            "Commander Harven",
            zone_id="ashreach_plains",
            faction="wardens",
        )
        whistle_npc = npc(
            "npc_innkeeper_whistle",
            "Whistle",
            zone_id="vaels_crossing",
            faction=None,
        )

        calloway_context = _build_dialogue_context(calloway_npc, self.char1)
        calloway_text, calloway_condition = resolve_topic_response(
            calloway_npc,
            self.char1,
            "report",
            context=calloway_context,
        )
        self.assertEqual(calloway_condition, "social_claim_status:supported")
        self.assertIn("carried Warden business cleanly", calloway_text)

        harven_context = _build_dialogue_context(harven_npc, self.char1)
        harven_text, harven_condition = resolve_topic_response(
            harven_npc,
            self.char1,
            "report",
            context=harven_context,
        )
        self.assertEqual(harven_condition, "social_claim_trace_edge:warden_report")
        self.assertIn("through the Warden line", harven_text)

        whistle_context = _build_dialogue_context(whistle_npc, self.char1)
        whistle_text, whistle_condition = resolve_topic_response(
            whistle_npc,
            self.char1,
            "report",
            context=whistle_context,
        )
        self.assertEqual(whistle_condition, "default")
        self.assertIn("no confirmed Warden report", whistle_text)
