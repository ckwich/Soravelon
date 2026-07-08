import ast
import pathlib
from types import SimpleNamespace
from unittest.mock import patch

from evennia.utils.test_resources import EvenniaTest


def _authored_quest_kwargs(quest_id):
    path = pathlib.Path("world/areas/vaels_crossing.py")
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute) or node.func.attr != "quest":
            continue
        if not node.args:
            continue
        try:
            authored_quest_id = ast.literal_eval(node.args[0])
        except (SyntaxError, ValueError):
            continue
        if authored_quest_id != quest_id:
            continue
        return {
            keyword.arg: ast.literal_eval(keyword.value)
            for keyword in node.keywords
            if keyword.arg
        }
    raise AssertionError(f"Could not find authored quest {quest_id!r}")


class TestVaelWardenSocialRoute(EvenniaTest):
    """Vael's Warden report can travel by contact edge without omniscience."""

    def _pay_warden_report_rewards(self):
        from world.quest_engine import _pay_rewards
        from world.social_engine import ensure_social_node

        from world.models import SocialClaim, SocialFact, SocialNode

        quest = _authored_quest_kwargs("vc_q_warden_report")
        failures = _pay_rewards(self.char1, quest)
        self.assertEqual(failures, [])

        fact_key = f"fact:{self.char1.id}:vc_q_warden_report:delivered"
        claim_key = f"claim:calloway:{self.char1.id}:vc_q_warden_report:delivered"
        innkeeper = ensure_social_node(
            "npc",
            "npc_innkeeper_whistle",
            display_name="Whistle",
            zone_id="vaels_crossing",
            settlement_id="vaels_crossing",
        )
        return (
            SocialNode.objects.get(node_key=f"player:{self.char1.id}"),
            SocialNode.objects.get(node_key="npc:npc_warden_agent_calloway"),
            SocialNode.objects.get(node_key="npc:npc_warden_outpost_commander"),
            innkeeper,
            SocialFact.objects.get(fact_key=fact_key),
            SocialClaim.objects.get(claim_key=claim_key),
        )

    def test_warden_report_reaches_outpost_contact_but_not_innkeeper(self):
        from world.social_engine import query_social_context

        (
            player,
            _calloway,
            commander,
            innkeeper,
            _fact,
            claim,
        ) = self._pay_warden_report_rewards()

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

        self._pay_warden_report_rewards()
        mock_context_packet.return_value = {
            "reputation": 0,
            "network": 0,
            "betrayal_flag": False,
        }
        shared_topics = {
            "report": {
                "social_claim_type:report": (
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
        self.assertEqual(calloway_condition, "social_claim_type:report")
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
