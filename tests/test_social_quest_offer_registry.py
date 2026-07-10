"""Validation and deterministic ordering for Social Web offer rules."""

import unittest


def _rule(*, quest_id, priority=0, npc_id="npc_offer_test", **overrides):
    rule = {
        "npc_id": npc_id,
        "quest_id": quest_id,
        "priority": priority,
        "seed_id": "witness_intimidation",
        "archetype_id": "protect_witness",
        "quest_giver": npc_id,
        "required_fact_tags": ["test"],
        "required_fact_key_fragment": "test",
        "actors": {},
        "objective_targets": {},
        "description": {},
    }
    rule.update(overrides)
    return rule


class TestSocialQuestOfferRegistry(unittest.TestCase):
    def test_groups_each_npc_by_descending_priority_then_quest_id(self):
        from world.social_quest_offer_registry import group_social_quest_offer_rules

        grouped = group_social_quest_offer_rules(
            (
                _rule(quest_id="quest_beta", priority=10),
                _rule(quest_id="quest_alpha", priority=10),
                _rule(quest_id="quest_low", priority=1),
            )
        )

        self.assertEqual(
            [rule["quest_id"] for rule in grouped["npc_offer_test"]],
            ["quest_alpha", "quest_beta", "quest_low"],
        )

    def test_rejects_duplicate_quests_and_ungrounded_predicates(self):
        from world.social_quest_offer_registry import (
            SocialQuestOfferRegistryError,
            validate_social_quest_offer_rules,
        )

        with self.assertRaisesRegex(SocialQuestOfferRegistryError, "duplicate quest_id"):
            validate_social_quest_offer_rules(
                (
                    _rule(quest_id="duplicate"),
                    _rule(quest_id="duplicate", npc_id="npc_other"),
                )
            )

        with self.assertRaisesRegex(
            SocialQuestOfferRegistryError,
            "requires at least one fact predicate",
        ):
            validate_social_quest_offer_rules(
                (
                    _rule(
                        quest_id="ungrounded",
                        required_fact_tags=[],
                        required_fact_key_fragment="",
                    ),
                )
            )
