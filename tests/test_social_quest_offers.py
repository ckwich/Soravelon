"""Tests for live Social Web-gated quest offers."""

import ast
import pathlib
from types import SimpleNamespace
from unittest.mock import patch

from evennia.utils.test_resources import EvenniaTest


VAELS_CROSSING_PATH = pathlib.Path("world/areas/vaels_crossing.py")


def _npc(npc_id):
    return SimpleNamespace(
        db=SimpleNamespace(npc_id=npc_id),
        key=npc_id,
    )


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
            keyword.arg: ast.literal_eval(keyword.value)
            for keyword in node.keywords
            if keyword.arg
        }
    raise AssertionError(f"Could not find authored quest {quest_id!r}")


class TestSocialQuestOffers(EvenniaTest):
    """Dynamic social quests must be grounded in real Social Web knowledge."""

    def _pay_warden_report_rewards(self):
        from world.quest_engine import _pay_rewards

        failures = _pay_rewards(
            self.char1,
            _authored_quest_kwargs("vc_q_warden_report"),
        )
        self.assertEqual(failures, [])

    @patch("world.quest_engine._get_all_quest_specs", return_value=[])
    def test_no_social_offer_without_warden_report_social_context(self, _mock_all_specs):
        from world.models import CharacterQuest
        from world.quest_engine import get_available_quest_for_npc

        CharacterQuest.objects.create(
            character=self.char1,
            quest_id="vc_q_warden_report",
            status="complete",
            progress={},
        )

        offer = get_available_quest_for_npc(
            _npc("npc_warden_agent_calloway"),
            self.char1,
        )

        self.assertIsNone(offer)

    @patch("world.quest_engine._get_all_quest_specs", return_value=[])
    def test_warden_social_offer_uses_query_social_context(self, _mock_all_specs):
        from world.quest_engine import get_available_quest_for_npc

        self._pay_warden_report_rewards()

        offer = get_available_quest_for_npc(
            _npc("npc_warden_agent_calloway"),
            self.char1,
        )

        self.assertIsNotNone(offer)
        self.assertEqual(offer["quest_id"], "vc_sq_under_seal_dustwalkers_rest")
        self.assertEqual(offer["quest_giver"], "npc_warden_agent_calloway")
        self.assertEqual(offer["incident_seed"], "witness_intimidation")
        self.assertEqual(offer["quest_archetype"], "protect_witness")
        self.assertIn("sealed field report", offer["description"])
        self.assertIn("Whistle", offer["description"])
        self.assertIn("Raith", offer["description"])
        self.assertNotIn("Harven vouched", offer["description"])
        self.assertEqual(
            offer["social_quest_context"]["social_context"]["facts"][0]["event_type"],
            "quest_completed",
        )
        self.assertEqual(
            offer["social_quest_context"]["llm_context"]["prompt_inputs"][
                "prior_interactions"
            ][0]["topic"],
            "Social Web fact",
        )
        self.assertFalse(
            offer["social_quest_context"]["llm_context"]["provider_call_allowed"]
        )
        self.assertEqual(
            [objective["type"] for objective in offer["objectives"]],
            ["talk_to", "investigate", "talk_to", "talk_to"],
        )
        self.assertEqual(offer["objectives"][0]["target"], "npc_innkeeper_whistle")
        self.assertEqual(offer["objectives"][1]["target"], "rd_inn")
        self.assertEqual(offer["objectives"][2]["target"], "npc_debt_collector_raith")
        self.assertEqual(offer["rewards"][0]["action_type"], "record_social_event")

    @patch("world.quest_engine._get_all_quest_specs", return_value=[])
    def test_social_offer_respects_active_and_completed_quest_state(self, _mock_all_specs):
        from world.models import CharacterQuest
        from world.quest_engine import get_available_quest_for_npc

        self._pay_warden_report_rewards()
        CharacterQuest.objects.create(
            character=self.char1,
            quest_id="vc_sq_under_seal_dustwalkers_rest",
            status="active",
            progress={},
        )

        active_offer = get_available_quest_for_npc(
            _npc("npc_warden_agent_calloway"),
            self.char1,
        )
        self.assertIsNone(active_offer)

        CharacterQuest.objects.filter(
            character=self.char1,
            quest_id="vc_sq_under_seal_dustwalkers_rest",
        ).update(status="complete")

        completed_offer = get_available_quest_for_npc(
            _npc("npc_warden_agent_calloway"),
            self.char1,
        )
        self.assertIsNone(completed_offer)

    @patch(
        "world.quest_engine._get_all_quest_specs",
        return_value=[
            {
                "quest_id": "vc_q_warden_report",
                "quest_giver": "npc_warden_agent_calloway",
                "one_chance": True,
            },
        ],
    )
    def test_completed_static_warden_report_does_not_block_social_followup(
        self,
        _mock_all_specs,
    ):
        from world.models import CharacterQuest
        from world.quest_engine import get_available_quest_for_npc

        self._pay_warden_report_rewards()
        CharacterQuest.objects.create(
            character=self.char1,
            quest_id="vc_q_warden_report",
            status="complete",
            progress={},
        )

        offer = get_available_quest_for_npc(
            _npc("npc_warden_agent_calloway"),
            self.char1,
        )

        self.assertIsNotNone(offer)
        self.assertEqual(offer["quest_id"], "vc_sq_under_seal_dustwalkers_rest")

    def test_dynamic_social_quest_spec_is_retrievable_for_completion(self):
        from world.quest_engine import _get_quest_spec

        spec = _get_quest_spec("vc_sq_under_seal_dustwalkers_rest")

        self.assertIsNotNone(spec)
        self.assertEqual(spec["quest_id"], "vc_sq_under_seal_dustwalkers_rest")
        self.assertEqual(spec["quest_giver"], "npc_warden_agent_calloway")
        self.assertTrue(spec["one_chance"])
        self.assertEqual(
            [objective["target"] for objective in spec["objectives"]],
            [
                "npc_innkeeper_whistle",
                "rd_inn",
                "npc_debt_collector_raith",
                "npc_warden_agent_calloway",
            ],
        )

    def test_warden_report_is_authored_one_chance_so_social_followup_can_surface(self):
        quest = _authored_quest_kwargs("vc_q_warden_report")

        self.assertTrue(quest["one_chance"])
