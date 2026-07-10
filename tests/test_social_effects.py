"""Executable, deterministic Social Web quest effects."""

from unittest.mock import MagicMock

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest


class TestSocialEffectCompilation(EvenniaTest):
    def test_warden_effects_compile_to_facts_knowledge_and_named_access(self):
        from world.social_quest_offers import get_social_quest_spec_by_id

        quest = get_social_quest_spec_by_id(
            "vc_sq_under_seal_dustwalkers_rest",
        )

        protected_witness_actions = [
            action
            for action in quest["rewards"]
            if action.get("action_type") == "record_social_event"
            and action.get("fact", {}).get("event_type") == "protected_witness"
        ]
        self.assertEqual(len(protected_witness_actions), 1)
        self.assertEqual(
            protected_witness_actions[0]["knowledge"][0]["node"],
            "quest_giver",
        )
        access_keys = {
            action["grant_key"]
            for action in quest["rewards"]
            if action.get("action_type") == "grant_access"
        }
        self.assertEqual(
            access_keys,
            {
                "social:vc_sq_under_seal_dustwalkers_rest:access:authority_notice",
                "social:vc_sq_under_seal_dustwalkers_rest:access:witness_trust",
            },
        )

    def test_unsupported_effect_fails_compilation_instead_of_becoming_decorative(self):
        from world.social_effects import (
            SocialEffectCompilationError,
            compile_social_effect_actions,
        )

        with self.assertRaisesRegex(
            SocialEffectCompilationError,
            "world_state_hint",
        ):
            compile_social_effect_actions(
                {
                    "actors": {},
                    "deterministic_outline": {
                        "social_effects": [
                            {"type": "world_state_hint", "tags": ["warning"]},
                        ],
                    },
                },
                quest_id="unsupported_effect_quest",
                quest_giver="npc_test_authority",
            )

    def test_public_quest_compiler_rejects_an_archetype_with_unimplemented_effects(self):
        from world.social_quest_grammar import (
            SocialQuestGrammarError,
            compile_quest_spec,
        )

        with self.assertRaisesRegex(
            SocialQuestGrammarError,
            "relationship_delta",
        ):
            compile_quest_spec(
                "council_blackmail_ledger",
                "broker_compromise",
                quest_id="sq_broker_compromise",
                quest_giver="npc_test_mediator",
                actors={
                    "petitioner": {"node_key": "npc:npc_test_petitioner"},
                    "target": {"node_key": "npc:npc_test_target"},
                    "leverage_holder": {
                        "node_key": "npc:npc_test_leverage_holder",
                    },
                    "mediator": {"node_key": "npc:npc_test_mediator"},
                },
                objective_targets={
                    "interview_petitioner": "npc_test_petitioner",
                    "question_leverage_holder": "npc_test_leverage_holder",
                    "meet_mediator": "npc_test_mediator",
                    "choose_target_outcome": "npc_test_target",
                },
                require_social_grounding=False,
            )


class TestSocialAccessGrantRuntime(EvenniaTest):
    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom

        self.origin = create_object(SoravelonRoom, key="Access Grant Origin")
        self.destination = create_object(
            SoravelonRoom,
            key="Access Grant Destination",
        )
        self.destination.db.action_budget_penalty = 0
        self.char1.location = self.origin
        self.char1.msg = MagicMock()

    def test_named_grant_is_durable_idempotent_and_unlocks_a_real_exit(self):
        from typeclasses.exits import SoravelonExit
        from world.action_vocabulary import execute_action
        from world.models import CharacterAccessGrant

        grant_key = "social:test_access:access:authority_notice"
        exit_obj = create_object(
            SoravelonExit,
            key="sealed archive passage",
            location=self.origin,
            destination=self.destination,
        )
        exit_obj.db.requires_access_grant = grant_key

        self.assertFalse(exit_obj.at_traverse(self.char1, self.destination))

        first = execute_action(
            {
                "action_type": "grant_access",
                "grant_key": grant_key,
                "source_quest_id": "test_access",
            },
            {"character": self.char1, "room": self.origin},
        )
        second = execute_action(
            {
                "action_type": "grant_access",
                "grant_key": grant_key,
                "source_quest_id": "test_access",
            },
            {"character": self.char1, "room": self.origin},
        )

        self.assertTrue(first[0], first[1])
        self.assertTrue(second[0], second[1])
        self.assertEqual(
            CharacterAccessGrant.objects.filter(
                character=self.char1,
                grant_key=grant_key,
            ).count(),
            1,
        )
        self.assertNotEqual(exit_obj.at_traverse(self.char1, self.destination), False)


class TestSocialEffectQuestOutcome(EvenniaTest):
    def test_effect_failure_rolls_back_social_writes_and_leaves_quest_pending(self):
        from world.models import (
            CharacterAccessGrant,
            CharacterQuest,
            SocialFact,
        )
        from world.quest_engine import _check_quest_completion
        from world.social_quest_offers import get_social_quest_spec_by_id

        quest_spec = get_social_quest_spec_by_id(
            "vc_sq_under_seal_dustwalkers_rest",
        )
        for action in quest_spec["rewards"]:
            if action.get("action_type") == "grant_access":
                action["grant_key"] = ""
                break
        else:
            self.fail("Expected the compiled quest to grant named access.")

        progress = {
            f"{objective['type']}_{objective['target']}": objective.get("count", 1)
            for objective in quest_spec["objectives"]
        }
        quest = CharacterQuest.objects.create(
            character=self.char1,
            quest_id=quest_spec["quest_id"],
            progress=progress,
        )

        completed = _check_quest_completion(self.char1, quest, quest_spec)

        quest.refresh_from_db()
        self.assertFalse(completed)
        self.assertEqual(quest.status, "active")
        self.assertFalse(
            SocialFact.objects.filter(
                fact_key__contains="vc_sq_under_seal_dustwalkers_rest",
            ).exists()
        )
        self.assertFalse(
            CharacterAccessGrant.objects.filter(character=self.char1).exists(),
        )
