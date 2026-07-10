"""Tests for live Social Web-gated quest offers."""

import ast
import copy
import json
import pathlib
from types import SimpleNamespace
from unittest.mock import patch

from evennia.utils.test_resources import EvenniaTest

from tests.quest_helpers import (
    complete_quest_fixture,
    create_completed_quest_fixture,
)


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

    def test_multiple_offers_are_ordered_and_carry_only_their_qualifying_facts(self):
        from world.social_quest_offer_registry import SOCIAL_QUEST_OFFER_RULES
        from world.social_quest_offers import get_social_quest_offers_for_npc

        high = copy.deepcopy(SOCIAL_QUEST_OFFER_RULES[0])
        high.update(
            quest_id="test_social_offer_high",
            priority=20,
            required_fact_key_fragment="high",
        )
        low = copy.deepcopy(SOCIAL_QUEST_OFFER_RULES[0])
        low.update(
            quest_id="test_social_offer_low",
            priority=10,
            required_fact_key_fragment="low",
        )
        npc = _npc("npc_warden_agent_calloway")
        evidence_by_fragment = {
            "high": [{"fact_key": "fact:high", "summary": "High evidence."}],
            "low": [{"fact_key": "fact:low", "summary": "Low evidence."}],
        }
        presentation_context = {
            "viewer": {"node_key": "npc:npc_warden_agent_calloway"},
            "subject": {"node_key": f"player:{self.char1.id}"},
            "purpose": "quest_offer",
            "facts": [{"fact_key": "fact:distractor", "summary": "Ignore me."}],
            "claims": [{"claim_key": "claim:distractor", "summary": "Ignore me."}],
        }

        with patch(
            "world.social_quest_offers.get_social_quest_offer_rules_by_npc",
            return_value=(low, high),
        ), patch(
            "world.social_engine.find_social_evidence",
            side_effect=lambda **kwargs: evidence_by_fragment[
                kwargs["fact_key_fragment"]
            ],
        ), patch(
            "world.social_engine.query_social_context",
            return_value=presentation_context,
        ) as mock_context, patch(
            "world.social_quest_offers._compile_offer_from_rule",
            side_effect=lambda rule, **kwargs: {
                "quest_id": rule["quest_id"],
                "context": kwargs["social_context"],
            },
        ):
            offers = get_social_quest_offers_for_npc(npc, self.char1)

        self.assertEqual(
            [offer["quest_id"] for offer in offers],
            ["test_social_offer_high", "test_social_offer_low"],
        )
        self.assertEqual(mock_context.call_count, 1)
        self.assertEqual(
            [offer["context"]["facts"] for offer in offers],
            [evidence_by_fragment["high"], evidence_by_fragment["low"]],
        )
        self.assertEqual([offer["context"]["claims"] for offer in offers], [[], []])

        with patch(
            "world.social_quest_offers.get_social_quest_offer_rules_by_npc",
            return_value=(low, high),
        ), patch(
            "world.social_engine.find_social_evidence",
            side_effect=lambda **kwargs: evidence_by_fragment[
                kwargs["fact_key_fragment"]
            ],
        ), patch(
            "world.social_engine.query_social_context",
            return_value=presentation_context,
        ), patch(
            "world.social_quest_offers._compile_offer_from_rule",
            side_effect=lambda rule, **kwargs: {"quest_id": rule["quest_id"]},
        ):
            remaining_offers = get_social_quest_offers_for_npc(
                npc,
                self.char1,
                active_ids={"test_social_offer_high"},
            )

        self.assertEqual(
            [offer["quest_id"] for offer in remaining_offers],
            ["test_social_offer_low"],
        )

    def test_offer_rule_registry_returns_isolated_rule_copies(self):
        from world.social_quest_offer_registry import (
            get_social_quest_offer_rule_by_npc,
            get_social_quest_offer_rules_by_npc,
            get_social_quest_offer_rule_by_quest_id,
            iter_social_quest_offer_rules,
        )

        npc_rule = get_social_quest_offer_rule_by_npc("npc_warden_agent_calloway")
        quest_rule = get_social_quest_offer_rule_by_quest_id(
            "vc_sq_under_seal_dustwalkers_rest"
        )

        self.assertEqual(npc_rule["quest_id"], "vc_sq_under_seal_dustwalkers_rest")
        self.assertEqual(quest_rule["quest_giver"], "npc_warden_agent_calloway")
        self.assertEqual(npc_rule["description"]["memory_summary_field"], "summary")
        self.assertIn("explainability", npc_rule)
        self.assertIn("contest_repair_hooks", npc_rule)
        self.assertEqual(npc_rule["priority"], 100)
        self.assertEqual(
            [rule["quest_id"] for rule in iter_social_quest_offer_rules()],
            ["vc_sq_under_seal_dustwalkers_rest"],
        )

        npc_rule["actors"]["witness"]["display_name"] = "Changed"
        fresh_rule = get_social_quest_offer_rule_by_npc("npc_warden_agent_calloway")
        self.assertEqual(fresh_rule["actors"]["witness"]["display_name"], "Whistle")
        npc_rules = get_social_quest_offer_rules_by_npc(
            "npc_warden_agent_calloway"
        )
        self.assertEqual([rule["quest_id"] for rule in npc_rules], [npc_rule["quest_id"]])
        npc_rules[0]["priority"] = -1
        self.assertEqual(
            get_social_quest_offer_rules_by_npc(
                "npc_warden_agent_calloway"
            )[0]["priority"],
            100,
        )
        self.assertIsInstance(json.dumps(iter_social_quest_offer_rules()), str)

    @patch("world.quest_engine._get_all_quest_specs", return_value=[])
    def test_unknown_npc_does_not_query_social_context(self, _mock_all_specs):
        from world.quest_engine import get_available_quest_for_npc
        from world.social_engine import query_social_context

        with patch(
            "world.social_engine.query_social_context",
            wraps=query_social_context,
        ) as mocked_query:
            offer = get_available_quest_for_npc(
                _npc("npc_no_social_quest_rule"),
                self.char1,
            )

        self.assertIsNone(offer)
        mocked_query.assert_not_called()

    @patch("world.quest_engine._get_all_quest_specs", return_value=[])
    def test_no_social_offer_without_warden_report_social_context(self, _mock_all_specs):
        from world.quest_engine import get_available_quest_for_npc

        create_completed_quest_fixture(
            self.char1,
            "vc_q_warden_report",
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

        from world.social_engine import query_social_context

        with patch(
            "world.social_engine.query_social_context",
            wraps=query_social_context,
        ) as mocked_query:
            offer = get_available_quest_for_npc(
                _npc("npc_warden_agent_calloway"),
                self.char1,
            )

        self.assertIsNotNone(offer)
        self.assertEqual(mocked_query.call_count, 1)
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
        self.assertEqual(
            offer["social_quest_context"]["offer_explainability"]["summary"],
            "Calloway is acting on the sealed Warden report you delivered.",
        )
        self.assertEqual(
            offer["social_quest_context"]["offer_explainability"]["npc_safe_reason"],
            "The Wardens have a supported report that you carried sealed business cleanly.",
        )
        self.assertEqual(
            offer["social_quest_context"]["offer_explainability"]["evidence"][0][
                "summary"
            ],
            offer["social_quest_context"]["social_context"]["facts"][0]["summary"],
        )
        self.assertEqual(
            offer["social_quest_context"]["offer_explainability"]["evidence"][0][
                "channel"
            ],
            offer["social_quest_context"]["social_context"]["facts"][0]["channel"],
        )
        self.assertIn(
            "expose_false_claim",
            offer["social_quest_context"]["contest_repair_hooks"]["future_archetypes"],
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
    def test_social_offer_uses_exact_evidence_outside_the_context_packet(
        self,
        _mock_all_specs,
    ):
        from world.models import SocialKnowledge
        from world.quest_engine import get_available_quest_for_npc
        from world.social_engine import (
            mark_known,
            query_social_context,
            record_social_fact,
        )

        self._pay_warden_report_rewards()
        player_node_key = f"player:{self.char1.id}"
        calloway_node_key = "npc:npc_warden_agent_calloway"
        qualifying_fact_key = (
            f"fact:{self.char1.id}:vc_q_warden_report:delivered"
        )
        qualifying_knowledge = SocialKnowledge.objects.get(
            node__node_key=calloway_node_key,
            fact__fact_key=qualifying_fact_key,
        )
        qualifying_knowledge.confidence = 0.01
        qualifying_knowledge.save(update_fields=["confidence"])

        for index in range(6):
            ok, message, fact = record_social_fact(
                fact_key=f"fact:{self.char1.id}:offer_distractor:{index}",
                subject_node_key=player_node_key,
                event_type="offer_distractor",
                summary=f"A more recent but irrelevant fact {index}.",
                tags=["distractor"],
                visibility="institutional",
            )
            self.assertTrue(ok, message)
            ok, message, _knowledge = mark_known(
                node_key=calloway_node_key,
                fact_key=fact.fact_key,
                channel="direct_witness",
                confidence=1.0,
            )
            self.assertTrue(ok, message)

        packet = query_social_context(
            viewer_node_key=calloway_node_key,
            subject_node_key=player_node_key,
            purpose="quest_offer",
        )
        self.assertNotIn(
            qualifying_fact_key,
            [fact["fact_key"] for fact in packet["facts"]],
        )

        offer = get_available_quest_for_npc(
            _npc("npc_warden_agent_calloway"),
            self.char1,
        )

        self.assertIsNotNone(offer)
        self.assertEqual(offer["quest_id"], "vc_sq_under_seal_dustwalkers_rest")

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

        quest = CharacterQuest.objects.get(
            character=self.char1,
            quest_id="vc_sq_under_seal_dustwalkers_rest",
        )
        complete_quest_fixture(quest)

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
        from world.quest_engine import get_available_quest_for_npc

        self._pay_warden_report_rewards()
        create_completed_quest_fixture(
            self.char1,
            "vc_q_warden_report",
        )

        offer = get_available_quest_for_npc(
            _npc("npc_warden_agent_calloway"),
            self.char1,
        )

        self.assertIsNotNone(offer)
        self.assertEqual(offer["quest_id"], "vc_sq_under_seal_dustwalkers_rest")

    def test_dynamic_social_quest_spec_is_retrievable_for_completion(self):
        from world.quest_engine import _get_quest_spec
        from world.social_engine import query_social_context

        with patch(
            "world.social_engine.query_social_context",
            wraps=query_social_context,
        ) as mocked_query:
            spec = _get_quest_spec("vc_sq_under_seal_dustwalkers_rest")

        self.assertIsNotNone(spec)
        mocked_query.assert_not_called()
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
