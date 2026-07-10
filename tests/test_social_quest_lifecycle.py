import ast
import pathlib
from unittest.mock import patch

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest


VAELS_CROSSING_PATH = pathlib.Path("world/areas/vaels_crossing.py")


def _authored_quest_kwargs(quest_id):
    tree = ast.parse(VAELS_CROSSING_PATH.read_text())
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
            "quest_id": quest_id,
            **{
                keyword.arg: ast.literal_eval(keyword.value)
                for keyword in node.keywords
                if keyword.arg
            },
        }
    raise AssertionError(f"Could not find authored quest {quest_id!r}")


def _authored_social_profile(npc_id):
    tree = ast.parse(VAELS_CROSSING_PATH.read_text())
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "npc"
            and len(node.args) >= 2
        ):
            continue
        try:
            authored_npc_id = ast.literal_eval(node.args[1])
        except (SyntaxError, ValueError):
            continue
        if authored_npc_id != npc_id:
            continue
        for keyword in node.keywords:
            if keyword.arg == "social_profile":
                return ast.literal_eval(keyword.value)
    return {}


class TestSocialQuestLifecycle(EvenniaTest):
    """The first dynamic Social Web quest is playable, not just offerable."""

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
        npc.db.social_profile = _authored_social_profile(npc_id)
        npc.tags.add(npc_id, category="npc_id")
        return npc

    def _seed_warden_report_social_state(self):
        from world.quest_engine import _pay_rewards

        failures = _pay_rewards(
            self.char1,
            _authored_quest_kwargs("vc_q_warden_report"),
        )
        self.assertEqual(failures, [])

    @patch("world.oob_publisher.push_quest_update")
    @patch("world.dialogue_engine.get_npc_hints", return_value=[])
    @patch("world.dialogue_engine.resolve_greeting", return_value=("Speak.", "neutral"))
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_calloway_social_quest_can_be_accepted_progressed_and_completed(
        self,
        mock_context_packet,
        _mock_standing_tier,
        _mock_greeting,
        _mock_hints,
        _mock_push_quest_update,
    ):
        from commands.cmd_dialogue import CmdAccept, CmdAsk, CmdTalk
        from commands.cmd_social_verbs import CmdConfront, CmdProtect, CmdReport
        from world.models import (
            CharacterAccessGrant,
            CharacterQuest,
            SocialClaim,
            SocialFact,
            SocialKnowledge,
        )
        from world.quest_engine import get_available_quest_for_npc

        mock_context_packet.return_value = {
            "reputation": 0,
            "network": 0,
            "betrayal_flag": False,
        }
        self.char1.location.tags.add("rd_inn", category="room_id")
        self._seed_warden_report_social_state()

        calloway = self._make_room_npc(
            key="Agent Calloway",
            npc_name="Agent Calloway",
            npc_id="npc_warden_agent_calloway",
            faction="wardens",
        )
        whistle = self._make_room_npc(
            key="Whistle",
            npc_name="Whistle",
            npc_id="npc_innkeeper_whistle",
        )
        raith = self._make_room_npc(
            key="Raith",
            npc_name="Raith",
            npc_id="npc_debt_collector_raith",
            faction="consortium",
        )

        with patch("world.quest_engine._get_all_quest_specs", return_value=[]):
            offer = get_available_quest_for_npc(calloway, self.char1)

        self.assertIsNotNone(offer)
        self.assertEqual(offer["quest_id"], "vc_sq_under_seal_dustwalkers_rest")
        self.assertEqual(
            [objective["type"] for objective in offer["objectives"]],
            [
                "social_interaction",
                "social_interaction",
                "social_interaction",
                "social_interaction",
                "social_interaction",
            ],
        )
        self.assertEqual(
            [objective["verb"] for objective in offer["objectives"]],
            ["ask", "protect", "confront", "ask", "report"],
        )
        self.assertEqual(
            [objective["target"] for objective in offer["objectives"]],
            [
                "npc_innkeeper_whistle",
                "npc_innkeeper_whistle",
                "npc_debt_collector_raith",
                "npc_innkeeper_whistle",
                "npc_warden_agent_calloway",
            ],
        )
        self.char1.ndb.pending_quest_offer = {"npc": calloway, "quest": offer}

        with patch.object(self.char1, "msg"):
            accept = CmdAccept()
            accept.caller = self.char1
            accept.func()

        cq = CharacterQuest.objects.get(
            character=self.char1,
            quest_id="vc_sq_under_seal_dustwalkers_rest",
        )
        self.assertEqual(cq.status, "active")
        self.assertEqual(
            cq.progress,
            {
                "social_interaction_pressure_inquiry": 0,
                "social_interaction_protect_witness": 0,
                "social_interaction_confront_coercer": 0,
                "social_interaction_record_testimony": 0,
                "social_interaction_report_authority": 0,
            },
        )

        with patch.object(self.char1, "msg"):
            talk_whistle = CmdTalk()
            talk_whistle.caller = self.char1
            talk_whistle.args = "Whistle"
            talk_whistle.func()

        cq.refresh_from_db()
        self.assertEqual(cq.progress["social_interaction_pressure_inquiry"], 0)

        whistle.db.dialogue_topics = {
            "pressure": {"default": "'I saw the pressure and remember it.'"},
            "testimony": {"default": "'I can put what I saw into a statement.'"},
        }
        raith.db.dialogue_topics = {
            "pressure": {"default": "'You have said what you came to say.'"},
        }
        calloway.db.dialogue_topics = {
            "testimony": {"default": "'Put the testimony in the record.'"},
        }

        with patch.object(self.char1, "msg"):
            confront_too_early = CmdConfront()
            confront_too_early.caller = self.char1
            confront_too_early.args = "Raith about pressure"
            confront_too_early.func()

        cq.refresh_from_db()
        self.assertEqual(cq.progress["social_interaction_confront_coercer"], 0)

        with patch.object(self.char1, "msg"):
            ask_pressure = CmdAsk()
            ask_pressure.caller = self.char1
            ask_pressure.args = "Whistle about pressure"
            ask_pressure.func()

        cq.refresh_from_db()
        self.assertEqual(cq.progress["social_interaction_pressure_inquiry"], 1)

        with patch.object(self.char1, "msg"):
            protect = CmdProtect()
            protect.caller = self.char1
            protect.args = "Whistle"
            protect.func()

        with patch.object(self.char1, "msg"):
            confront = CmdConfront()
            confront.caller = self.char1
            confront.args = "Raith about pressure"
            confront.func()

        with patch.object(self.char1, "msg"):
            ask_testimony = CmdAsk()
            ask_testimony.caller = self.char1
            ask_testimony.args = "Whistle about testimony"
            ask_testimony.func()

        cq.refresh_from_db()
        self.assertEqual(cq.status, "active")
        self.assertEqual(cq.progress["social_interaction_pressure_inquiry"], 1)
        self.assertEqual(cq.progress["social_interaction_protect_witness"], 1)
        self.assertEqual(cq.progress["social_interaction_confront_coercer"], 1)
        self.assertEqual(cq.progress["social_interaction_record_testimony"], 1)
        self.assertEqual(cq.progress["social_interaction_report_authority"], 0)

        with patch.object(self.char1, "msg"):
            report = CmdReport()
            report.caller = self.char1
            report.args = "Calloway about testimony"
            report.func()

        cq.refresh_from_db()
        self.assertEqual(cq.status, "complete")
        self.assertEqual(cq.progress["social_interaction_report_authority"], 1)

        fact_key = (
            f"fact:{self.char1.id}:"
            "vc_sq_under_seal_dustwalkers_rest:completed"
        )
        claim_key = (
            f"claim:npc_warden_agent_calloway:{self.char1.id}:"
            "vc_sq_under_seal_dustwalkers_rest:completed"
        )
        self.assertTrue(SocialFact.objects.filter(fact_key=fact_key).exists())
        self.assertTrue(SocialClaim.objects.filter(claim_key=claim_key).exists())
        self.assertTrue(
            SocialKnowledge.objects.filter(
                node__node_key="npc:npc_warden_agent_calloway",
                claim__claim_key=claim_key,
                channel="direct_witness",
            ).exists()
        )
        protected_witness = SocialFact.objects.get(
            event_type="protected_witness",
        )
        self.assertEqual(
            protected_witness.subject_node.node_key,
            "npc:npc_innkeeper_whistle",
        )
        testimony = SocialClaim.objects.get(claim_type="testimony")
        self.assertEqual(
            testimony.subject_node.node_key,
            "npc:npc_innkeeper_whistle",
        )
        self.assertTrue(
            SocialKnowledge.objects.filter(
                node__node_key="npc:npc_warden_agent_calloway",
                claim=testimony,
                channel="official_report",
            ).exists()
        )
        self.assertEqual(
            set(
                CharacterAccessGrant.objects.filter(
                    character=self.char1,
                ).values_list("grant_key", flat=True)
            ),
            {
                "social:vc_sq_under_seal_dustwalkers_rest:access:authority_notice",
                "social:vc_sq_under_seal_dustwalkers_rest:access:witness_trust",
            },
        )

        self.assertIs(whistle.location, self.char1.location)
        self.assertIs(raith.location, self.char1.location)
