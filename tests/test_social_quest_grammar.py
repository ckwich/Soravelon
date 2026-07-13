"""Tests for Social Web-backed generated quest grammar.

The registry is deliberately deterministic: incident seeds and quest
archetypes define structure, while a future LLM may only phrase bounded context.
"""

import json
import unittest

from evennia.utils.test_resources import EvenniaTest


class TestSocialQuestGrammarRegistry(unittest.TestCase):
    """Incident seeds and quest archetypes are expandable data, not prose hacks."""

    def test_registered_grammar_validates_cleanly(self):
        from world.social_quest_grammar import validate_social_quest_grammar

        errors = validate_social_quest_grammar()

        self.assertEqual(errors, [])

    def test_registry_covers_crime_intrigue_and_coercive_agendas(self):
        from world.social_quest_grammar import INCIDENT_SEEDS

        categories = {seed["category"] for seed in INCIDENT_SEEDS.values()}
        agenda_methods = {
            method
            for seed in INCIDENT_SEEDS.values()
            for method in seed["agenda"]["methods"]
        }

        self.assertIn("crime", categories)
        self.assertIn("political_intrigue", categories)
        self.assertIn("coercion", categories)
        self.assertIn("extract_leverage", agenda_methods)
        self.assertIn("intimidate", agenda_methods)
        self.assertIn("conceal_truth", agenda_methods)

    def test_market_robbery_supports_evidence_chain_personalized_by_memory(self):
        from world.social_quest_grammar import (
            build_social_quest_context,
            compatible_archetype_ids,
        )

        compatible = compatible_archetype_ids("market_square_robbery")
        self.assertIn("trace_evidence_chain", compatible)

        context = build_social_quest_context(
            "market_square_robbery",
            "trace_evidence_chain",
            prior_interactions=[
                {
                    "topic": "mysterious robberies in Market Square",
                    "summary": (
                        "The player and vendor talked about a pattern of "
                        "night thefts near the stalls."
                    ),
                }
            ],
            actors={
                "victim": {
                    "node_key": "npc:market_vendor_sella",
                    "display_name": "Sella",
                },
                "evidence_holder": {
                    "node_key": "npc:market_clothier_tavin",
                    "display_name": "Tavin",
                },
            },
            social_context={
                "viewer": {"node_key": "npc:market_vendor_sella"},
                "subject": {"node_key": "player:12"},
                "purpose": "quest_offer",
                "facts": [
                    {
                        "fact_key": "fact:player:12:helped_vendor",
                        "event_type": "helped_victim",
                        "summary": "Sella saw the player help a frightened vendor.",
                        "tags": ["trusted", "market"],
                        "confidence": 0.9,
                    }
                ],
                "claims": [],
            },
        )

        self.assertEqual(context["purpose"], "social_quest_offer")
        self.assertEqual(context["incident"]["id"], "market_square_robbery")
        self.assertEqual(context["archetype"]["id"], "trace_evidence_chain")
        self.assertEqual(
            context["actors"]["evidence_holder"]["display_name"],
            "Tavin",
        )
        self.assertIn(
            "mysterious robberies in Market Square",
            context["llm_context"]["prompt_inputs"]["prior_interactions"][0]["topic"],
        )
        objective_roles = [
            step.get("role")
            for step in context["deterministic_outline"]["objective_steps"]
        ]
        self.assertIn("evidence_holder", objective_roles)
        self.assertFalse(context["llm_context"]["provider_call_allowed"])

    def test_llm_context_is_renderer_only_and_excludes_secrets(self):
        from world.social_quest_grammar import build_social_quest_context

        context = build_social_quest_context(
            "council_blackmail_ledger",
            "broker_compromise",
            prior_interactions=[
                {"summary": "The player noticed a council aide avoiding questions."}
            ],
        )
        llm_context = context["llm_context"]

        self.assertEqual(llm_context["role"], "optional_voice_renderer")
        self.assertIn("create durable facts", llm_context["forbidden_actions"])
        self.assertIn("mutate quests", llm_context["forbidden_actions"])
        self.assertIn("reveal hidden lore", llm_context["forbidden_actions"])
        self.assertNotIn("api_key", str(llm_context).lower())
        self.assertNotIn("deepseek", str(llm_context).lower())

    def test_compile_quest_spec_targets_existing_quest_engine_shape(self):
        from world.quest_engine import OBJECTIVE_TYPES
        from world.social_quest_grammar import compile_quest_spec

        first = compile_quest_spec(
            "market_square_robbery",
            "trace_evidence_chain",
            quest_id="sq_market_robbery_sella",
            quest_giver="npc_market_vendor_sella",
            actors={
                "victim": {
                    "node_key": "npc:npc_market_vendor_sella",
                    "display_name": "Sella",
                    "zone_id": "vaels_crossing",
                    "settlement_id": "vaels_crossing",
                },
                "evidence_holder": {
                    "node_key": "npc:npc_market_clothier_tavin",
                    "display_name": "Tavin",
                    "zone_id": "vaels_crossing",
                    "settlement_id": "vaels_crossing",
                },
                "authority": {
                    "node_key": "npc:npc_market_adjudicator",
                    "display_name": "Market Adjudicator",
                    "zone_id": "vaels_crossing",
                    "settlement_id": "vaels_crossing",
                },
            },
            objective_targets={
                "interview_victim": "npc_market_vendor_sella",
                "inspect_scene": "vc_market_square_sella_counter",
                "ask_evidence_holder": "npc_market_clothier_tavin",
                "report_authority": "npc_market_adjudicator",
            },
            prior_interactions=[
                {
                    "topic": "mysterious robberies in Market Square",
                    "summary": "The vendor already trusted the player with the worry.",
                }
            ],
        )
        second = compile_quest_spec(
            "market_square_robbery",
            "trace_evidence_chain",
            quest_id="sq_market_robbery_sella",
            quest_giver="npc_market_vendor_sella",
            actors={
                "victim": {
                    "node_key": "npc:npc_market_vendor_sella",
                    "display_name": "Sella",
                    "zone_id": "vaels_crossing",
                    "settlement_id": "vaels_crossing",
                },
                "evidence_holder": {
                    "node_key": "npc:npc_market_clothier_tavin",
                    "display_name": "Tavin",
                    "zone_id": "vaels_crossing",
                    "settlement_id": "vaels_crossing",
                },
                "authority": {
                    "node_key": "npc:npc_market_adjudicator",
                    "display_name": "Market Adjudicator",
                    "zone_id": "vaels_crossing",
                    "settlement_id": "vaels_crossing",
                },
            },
            objective_targets={
                "interview_victim": "npc_market_vendor_sella",
                "inspect_scene": "vc_market_square_sella_counter",
                "ask_evidence_holder": "npc_market_clothier_tavin",
                "report_authority": "npc_market_adjudicator",
            },
            prior_interactions=[
                {
                    "topic": "mysterious robberies in Market Square",
                    "summary": "The vendor already trusted the player with the worry.",
                }
            ],
        )

        self.assertEqual(first, second)
        json.dumps(first)
        self.assertEqual(first["quest_id"], "sq_market_robbery_sella")
        self.assertEqual(first["quest_giver"], "npc_market_vendor_sella")
        self.assertFalse(first["repeatable"])
        self.assertEqual(first["incident_seed"], "market_square_robbery")
        self.assertEqual(first["quest_archetype"], "trace_evidence_chain")
        self.assertIn("social_quest_context", first)
        self.assertTrue(first["objectives"])
        self.assertTrue(
            {objective["type"] for objective in first["objectives"]}.issubset(
                OBJECTIVE_TYPES
            )
        )
        reward = first["rewards"][0]
        self.assertEqual(reward["action_type"], "record_social_event")
        self.assertEqual(reward["fact"]["event_type"], "social_quest_completed")
        self.assertEqual(reward["claim"]["claim_type"], "report")
        self.assertEqual(reward["knowledge"][0]["node"], "quest_giver")
        self.assertFalse(
            first["social_quest_context"]["llm_context"]["provider_call_allowed"]
        )

    def test_compile_quest_spec_requires_social_grounding_for_personal_offer(self):
        from world.social_quest_grammar import (
            SocialQuestGrammarError,
            compile_quest_spec,
        )

        with self.assertRaisesRegex(SocialQuestGrammarError, "social grounding"):
            compile_quest_spec(
                "market_square_robbery",
                "trace_evidence_chain",
                quest_id="sq_empty_robbery",
                quest_giver="npc_market_vendor_sella",
                objective_targets={
                    "interview_victim": "npc_market_vendor_sella",
                    "inspect_scene": "vc_market_square_sella_counter",
                    "ask_evidence_holder": "npc_market_clothier_tavin",
                },
            )

    def test_compile_quest_spec_requires_real_quest_identity(self):
        from world.social_quest_grammar import (
            SocialQuestGrammarError,
            compile_quest_spec,
        )

        with self.assertRaisesRegex(SocialQuestGrammarError, "quest_id"):
            compile_quest_spec(
                "market_square_robbery",
                "trace_evidence_chain",
                quest_giver="npc_market_vendor_sella",
            )

        with self.assertRaisesRegex(SocialQuestGrammarError, "quest_giver"):
            compile_quest_spec(
                "market_square_robbery",
                "trace_evidence_chain",
                quest_id="sq_market_robbery_sella",
            )

    def test_unknown_or_incompatible_pair_fails_closed(self):
        from world.social_quest_grammar import (
            SocialQuestGrammarError,
            build_social_quest_context,
        )

        with self.assertRaisesRegex(SocialQuestGrammarError, "Unknown incident"):
            build_social_quest_context("missing_seed", "trace_evidence_chain")

        with self.assertRaisesRegex(SocialQuestGrammarError, "not compatible"):
            build_social_quest_context(
                "market_square_robbery",
                "broker_compromise",
            )


class TestCompiledSocialQuestReward(EvenniaTest):
    """Compiled social quest rewards execute through action_vocabulary."""

    def test_compiled_social_reward_records_social_web_state(self):
        from world.action_vocabulary import execute_action
        from world.models import SocialClaim, SocialFact, SocialKnowledge
        from world.social_quest_grammar import compile_quest_spec

        quest = compile_quest_spec(
            "market_square_robbery",
            "trace_evidence_chain",
            quest_id="sq_market_robbery_sella",
            quest_giver="npc_market_vendor_sella",
            actors={
                "victim": {
                    "node_key": "npc:npc_market_vendor_sella",
                    "display_name": "Sella",
                    "zone_id": "vaels_crossing",
                    "settlement_id": "vaels_crossing",
                },
                "evidence_holder": {
                    "node_key": "npc:npc_market_clothier_tavin",
                    "display_name": "Tavin",
                    "zone_id": "vaels_crossing",
                    "settlement_id": "vaels_crossing",
                },
            },
            objective_targets={
                "interview_victim": "npc_market_vendor_sella",
                "inspect_scene": "vc_market_square_sella_counter",
                "ask_evidence_holder": "npc_market_clothier_tavin",
            },
            prior_interactions=[
                {
                    "topic": "mysterious robberies in Market Square",
                    "summary": "Sella trusted the player with the earlier rumor.",
                }
            ],
        )
        self.assertEqual(
            quest["rewards"][0]["knowledge"][0]["claim_key_template"],
            "claim:npc_market_vendor_sella:{character_id}:sq_market_robbery_sella:completed",
        )
        self.assertNotIn("fact_key", quest["rewards"][0]["knowledge"][0])

        success, message = execute_action(
            quest["rewards"][0],
            {"character": self.char1, "room": self.room1},
        )

        self.assertTrue(success, message)
        fact_key = f"fact:{self.char1.id}:sq_market_robbery_sella:completed"
        claim_key = (
            f"claim:npc_market_vendor_sella:{self.char1.id}:"
            "sq_market_robbery_sella:completed"
        )
        self.assertTrue(SocialFact.objects.filter(fact_key=fact_key).exists())
        self.assertTrue(SocialClaim.objects.filter(claim_key=claim_key).exists())
        self.assertTrue(
            SocialKnowledge.objects.filter(
                node__node_key="npc:npc_market_vendor_sella",
                claim__claim_key=claim_key,
            ).exists()
        )


if __name__ == "__main__":
    unittest.main()
