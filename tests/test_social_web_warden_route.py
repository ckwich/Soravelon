import ast
import pathlib
from types import SimpleNamespace
from unittest.mock import patch

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest

from tests.quest_helpers import create_completed_quest_fixture
from django.db.models import Q


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

        quest = {
            "quest_id": "vc_q_warden_report",
            **_authored_quest_kwargs("vc_q_warden_report"),
        }
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

    def _make_room_npc(self, *, key, npc_name, npc_id, faction=None):
        from typeclasses.mobs import SoravelonMob

        npc = create_object(SoravelonMob, key=key, location=self.char1.location)
        npc.db.is_npc = True
        npc.db.combat_enabled = False
        npc.db.npc_name = npc_name
        npc.db.npc_id = npc_id
        npc.db.faction = faction
        npc.db.zone_id = "vaels_crossing"
        npc.db.dialogue_topics = {}
        npc.tags.add(npc_id, category="npc_id")
        return npc

    def _make_zone_object_with_items(self, *, zone_id, item_ids, quest_definitions=None):
        from evennia.objects.objects import DefaultObject
        from world.areas.equipment_catalog import CATALOG

        zone = create_object(DefaultObject, key=f"test_zone_{zone_id}_{self.char1.id}")
        zone.tags.add("zone_object", category="object_type")
        zone.db.zone_id = zone_id
        zone.db.item_definitions = [dict(CATALOG[item_id]) for item_id in item_ids]
        zone.db.quest_definitions = list(quest_definitions or [])
        return zone

    def test_vael_south_road_reaches_harven_through_real_exit_objects(self):
        import evennia

        from world.areas import ashreach_plains, vaels_crossing

        # Build the destination first so Vael's authored cross-zone exit must
        # resolve to the real Ashway room rather than a local stand-in.
        ashreach_plains.build()
        vaels_crossing.build()

        source = next(
            room
            for room in evennia.search_tag("hg_south_road", category="room_id")
            if room.db.zone_id == "vaels_crossing"
        )
        harven = next(
            npc
            for npc in evennia.search_tag(
                "npc_warden_outpost_commander",
                category="npc_id",
            )
            if npc.db.zone_id == "ashreach_plains"
        )

        predecessor = {source.id: None}
        frontier = [source]
        while frontier and harven.location.id not in predecessor:
            room = frontier.pop(0)
            for exit_obj in room.exits:
                destination = exit_obj.destination
                if not destination or destination.id in predecessor:
                    continue
                predecessor[destination.id] = (room, exit_obj)
                frontier.append(destination)

        self.assertIn(harven.location.id, predecessor)
        route = []
        room = harven.location
        while predecessor[room.id] is not None:
            previous_room, exit_obj = predecessor[room.id]
            route.append(exit_obj)
            room = previous_room
        route.reverse()

        self.char1.location = source
        self.assertEqual(route[0].key, "south")
        self.assertEqual(route[0].destination.db.zone_id, "ashreach_plains")
        for exit_obj in route:
            destination = exit_obj.destination
            exit_obj.at_traverse(self.char1, destination)
            self.assertIs(self.char1.location, destination, exit_obj.key)

        self.assertIs(self.char1.location, harven.location)

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
        self.assertEqual(commander_context["facts"], [])
        self.assertEqual(innkeeper_context["claims"], [])
        self.assertEqual(innkeeper_context["facts"], [])

    @patch("world.oob_publisher.push_quest_update")
    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_player_path_accepts_delivers_and_records_warden_report_social_reward(
        self,
        mock_context_packet,
        _mock_standing_tier,
        _mock_active_quests,
        _mock_push_quest_update,
    ):
        from commands.cmd_dialogue import CmdAccept, CmdTalk
        from world.models import CharacterQuest, SocialClaim, SocialFact, SocialKnowledge

        self.char1.location.db.zone_id = "vaels_crossing"
        quest = {
            "quest_id": "vc_q_warden_report",
            **_authored_quest_kwargs("vc_q_warden_report"),
        }
        self.assertEqual(quest["rewards"][2]["action_type"], "record_social_event")
        self.assertEqual(len(quest["rewards"][2]["nodes"]), 3)
        zone = self._make_zone_object_with_items(
            zone_id="vaels_crossing",
            item_ids=["warden_field_report"],
            quest_definitions=[quest],
        )
        self.assertEqual(len(zone.db.quest_definitions[0]["rewards"][2]["nodes"]), 3)
        mock_context_packet.return_value = {
            "reputation": 0,
            "network": 0,
            "betrayal_flag": False,
        }

        calloway = self._make_room_npc(
            key="Agent Calloway",
            npc_name="Agent Calloway",
            npc_id="npc_warden_agent_calloway",
            faction="wardens",
        )
        harven = self._make_room_npc(
            key="Commander Harven",
            npc_name="Commander Harven",
            npc_id="npc_warden_outpost_commander",
            faction="wardens",
        )

        self.char1.ndb.pending_quest_offer = {"npc": calloway, "quest": quest}

        def search_tag_side_effect(tag, category=None):
            if tag == "zone_object" and category == "object_type":
                return [zone]
            return []

        with patch(
            "evennia.search_tag",
            side_effect=search_tag_side_effect,
        ), patch.object(self.char1, "msg") as mock_msg:
            accept = CmdAccept()
            accept.caller = self.char1
            accept.func()

        accept_output = "\n".join(str(call.args[0]) for call in mock_msg.call_args_list)
        self.assertTrue(
            CharacterQuest.objects.filter(
                character=self.char1,
                quest_id="vc_q_warden_report",
            ).exists(),
            accept_output,
        )

        cq = CharacterQuest.objects.get(
            character=self.char1,
            quest_id="vc_q_warden_report",
        )
        self.assertEqual(cq.status, "active")
        self.assertEqual(
            cq.progress,
            {"deliver_npc_warden_outpost_commander": 0},
        )
        self.assertTrue(
            any(
                item.tags.has("warden_field_report", category="item_tag")
                for item in self.char1.contents
            )
        )

        from world.action_vocabulary import execute_action

        with patch(
            "world.action_vocabulary.execute_action",
            wraps=execute_action,
        ) as mock_execute_action, patch(
            "evennia.search_tag",
            side_effect=search_tag_side_effect,
        ), patch.object(self.char1, "msg") as mock_talk_msg:
            talk = CmdTalk()
            talk.caller = self.char1
            talk.args = "Harven"
            talk.func()
        talk_output = "\n".join(str(call.args[0]) for call in mock_talk_msg.call_args_list)
        executed_social_actions = [
            call.args[0]
            for call in mock_execute_action.call_args_list
            if call.args and call.args[0].get("action_type") == "record_social_event"
        ]
        self.assertTrue(executed_social_actions)
        self.assertEqual(len(executed_social_actions[0].get("nodes") or []), 3)

        cq.refresh_from_db()
        self.assertEqual(cq.status, "complete")
        self.assertEqual(
            cq.progress,
            {"deliver_npc_warden_outpost_commander": 1},
        )
        self.assertFalse(
            any(
                item.tags.has("warden_field_report", category="item_tag")
                for item in self.char1.contents
            )
        )

        fact_key = f"fact:{self.char1.id}:vc_q_warden_report:delivered"
        claim_key = f"claim:calloway:{self.char1.id}:vc_q_warden_report:delivered"
        self.assertTrue(
            SocialFact.objects.filter(fact_key=fact_key).exists(),
            talk_output,
        )
        self.assertTrue(
            SocialClaim.objects.filter(claim_key=claim_key).exists(),
            talk_output,
        )
        self.assertEqual(
            set(
                SocialKnowledge.objects.filter(claim__claim_key=claim_key).values_list(
                    "node__node_key",
                    flat=True,
                )
            ),
            {
                "npc:npc_warden_agent_calloway",
                "npc:npc_warden_outpost_commander",
            },
        )
        self.assertEqual(
            set(
                SocialKnowledge.objects.filter(
                    fact__fact_key=fact_key,
                ).values_list("node__node_key", flat=True)
            ),
            {"npc:npc_warden_agent_calloway"},
        )
        self.assertIs(harven.location, self.char1.location)

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

    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_player_can_ask_calloway_why_after_social_offer_but_not_whistle(
        self,
        mock_context_packet,
        _mock_standing_tier,
        _mock_active_quests,
    ):
        from commands.cmd_dialogue import CmdAsk, CmdTalk
        from world.models import SocialEdge, SocialKnowledge
        from world.social_engine import query_social_context

        (
            player,
            calloway_node,
            _harven_node,
            innkeeper_node,
            fact,
            claim,
        ) = self._pay_warden_report_rewards()
        payload_query = Q(fact=fact) | Q(claim=claim)
        self.assertEqual(
            set(
                SocialKnowledge.objects.filter(payload_query).values_list(
                    "node__node_key",
                    flat=True,
                )
            ),
            {
                "npc:npc_warden_agent_calloway",
                "npc:npc_warden_outpost_commander",
            },
        )
        self.assertFalse(
            SocialEdge.objects.filter(
                Q(source_node=innkeeper_node) | Q(target_node=innkeeper_node)
            ).exists()
        )

        calloway_context = query_social_context(
            viewer_node_key=calloway_node.node_key,
            subject_node_key=player.node_key,
            purpose="quest_offer",
        )
        self.assertEqual(
            [item["fact_key"] for item in calloway_context["facts"]],
            [fact.fact_key],
        )
        self.assertEqual(
            [item["claim_key"] for item in calloway_context["claims"]],
            [claim.claim_key],
        )

        create_completed_quest_fixture(
            self.char1,
            "vc_q_warden_report",
        )
        mock_context_packet.return_value = {
            "reputation": 0,
            "network": 0,
            "betrayal_flag": False,
        }

        calloway = self._make_room_npc(
            key="Agent Calloway",
            npc_name="Agent Calloway",
            npc_id="npc_warden_agent_calloway",
            faction="wardens",
        )
        self._make_room_npc(
            key="Whistle",
            npc_name="Whistle",
            npc_id="npc_innkeeper_whistle",
            faction=None,
        )

        with patch("world.dialogue_engine.resolve_greeting", return_value=("Speak.", "neutral")), patch(
            "world.dialogue_engine.get_npc_hints",
            return_value=[],
        ), patch("world.quest_engine.check_talk_to_objectives"), patch(
            "world.quest_engine.check_deliver_objectives"
        ), patch.object(self.char1, "msg") as mock_msg:
            talk = CmdTalk()
            talk.caller = self.char1
            talk.args = "Calloway"
            talk.func()

            pending_offer = self.char1.ndb.pending_quest_offer
            self.assertIsNotNone(pending_offer)
            self.assertIs(pending_offer["npc"], calloway)
            self.assertEqual(
                pending_offer["quest"]["quest_id"],
                "vc_sq_under_seal_dustwalkers_rest",
            )

            mock_msg.reset_mock()
            ask_calloway = CmdAsk()
            ask_calloway.caller = self.char1
            ask_calloway.args = "Calloway why"
            ask_calloway.func()

            calloway_text = mock_msg.call_args[0][0]
            self.assertIn("supported report", calloway_text)
            self.assertIn("sealed field report", calloway_text)
            self.assertIn("official report", calloway_text)
            for forbidden in (
                "fact:",
                "claim:",
                "npc:",
                "player:",
                "edge:",
                "edge_key",
                "node_key",
                "fact_key",
                "claim_key",
                "confidence",
                "0.95",
                "1.0",
                "warden_report",
                "Harven",
                "raw_prompt",
                "provider",
            ):
                self.assertNotIn(forbidden, calloway_text)

            mock_msg.reset_mock()
            ask_whistle = CmdAsk()
            ask_whistle.caller = self.char1
            ask_whistle.args = "Whistle why"
            ask_whistle.func()

            whistle_text = mock_msg.call_args[0][0]
            self.assertIn("nothing I can fairly speak to", whistle_text)
            self.assertNotIn("Warden report", whistle_text)
            self.assertNotIn("sealed field report", whistle_text)

    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_inn_traveler_route_lets_whistle_explain_local_rumor_safely(
        self,
        mock_context_packet,
        _mock_standing_tier,
        _mock_active_quests,
    ):
        from commands.cmd_dialogue import CmdAsk
        from world.social_engine import (
            assert_social_claim,
            connect_social_nodes,
            ensure_social_node,
            mark_known,
            propagate_social_knowledge,
            query_social_context,
        )

        (
            player,
            _calloway_node,
            _harven_node,
            innkeeper_node,
            _fact,
            _claim,
        ) = self._pay_warden_report_rewards()
        traveler_node = ensure_social_node(
            "gathering",
            f"vc_inn_travelers_{self.char1.id}",
            display_name="Dustwalker's Rest travelers",
            zone_id="vaels_crossing",
            settlement_id="vaels_crossing",
        )
        ok, message, rumor_claim = assert_social_claim(
            claim_key=(
                f"claim:vc_inn_travelers:{self.char1.id}:"
                "warden_packet_rumor"
            ),
            speaker_node_key=traveler_node.node_key,
            subject_node_key=player.node_key,
            claim_type="rumor",
            summary=(
                "A road traveler says you carried Calloway's packet without "
                "selling the story at the bar."
            ),
            status="rumor",
            intent="tavern_recall",
            bias_tags=["tavern", "report", "road_rumor"],
            confidence=0.6,
        )
        self.assertTrue(ok, message)
        ok, message, _source_knowledge = mark_known(
            node_key=traveler_node.node_key,
            claim_key=rumor_claim.claim_key,
            channel="tavern_rumor",
            confidence=0.6,
            spreading=True,
        )
        self.assertTrue(ok, message)

        before_route = query_social_context(
            viewer_node_key=innkeeper_node.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
        )
        self.assertEqual(before_route["claims"], [])

        ok, message, _edge = connect_social_nodes(
            traveler_node.node_key,
            innkeeper_node.node_key,
            edge_type="inn_traveler",
            directionality="one_way",
            trust=0.55,
            scope_tags=["tavern", "road_rumor", "report"],
        )
        self.assertTrue(ok, message)
        propagated = propagate_social_knowledge(
            source_node_key=traveler_node.node_key,
            claim_key=rumor_claim.claim_key,
        )
        self.assertEqual([item.node.node_key for item in propagated], [innkeeper_node.node_key])

        whistle_context = query_social_context(
            viewer_node_key=innkeeper_node.node_key,
            subject_node_key=player.node_key,
            purpose="dialogue",
        )
        self.assertEqual(whistle_context["claims"][0]["claim_key"], rumor_claim.claim_key)
        self.assertEqual(whistle_context["claims"][0]["trace"][0]["edge_type"], "inn_traveler")
        self.assertEqual(whistle_context["claims"][0]["channel"], "tavern_rumor")

        mock_context_packet.return_value = {
            "reputation": 0,
            "network": 0,
            "betrayal_flag": False,
        }
        whistle = self._make_room_npc(
            key="Whistle",
            npc_name="Whistle",
            npc_id="npc_innkeeper_whistle",
            faction=None,
        )

        with patch.object(self.char1, "msg") as mock_msg:
            ask_whistle = CmdAsk()
            ask_whistle.caller = self.char1
            ask_whistle.args = "Whistle why"
            ask_whistle.func()

        self.assertIs(whistle.location, self.char1.location)
        whistle_text = mock_msg.call_args[0][0]
        self.assertIn("tavern rumor", whistle_text)
        self.assertIn("carried Calloway's packet", whistle_text)
        self.assertIn("selling the story at the bar", whistle_text)
        for forbidden in (
            "fact:",
            "claim:",
            "npc:",
            "player:",
            "edge:",
            "edge_key",
            "node_key",
            "claim_key",
            "confidence",
            "warden_report",
            "official report",
            "sealed field report",
            "Harven",
            "raw_prompt",
            "provider",
        ):
            self.assertNotIn(forbidden, whistle_text)
