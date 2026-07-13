"""Contracts for runtime-effective authored dialogue payloads."""

import unittest


class TestDialogueSchema(unittest.TestCase):
    def test_accepts_tiered_greeting_topics_and_topic_hints(self):
        from world.dialogue_schema import validate_dialogue_payload

        payload = {
            "greeting_tiers": {"neutral": "The keeper looks up."},
            "topics": {
                "work": {
                    "friendly": "There is careful work for a familiar hand.",
                    "default": "There is work if you listen first.",
                },
                "roads": "The eastern road floods after hard rain.",
            },
            "base_hints": ["work"],
            "tier_hints": {"friendly": ["roads"]},
            "quest_hints": {"vc_q_help": ["work"]},
        }

        self.assertIs(validate_dialogue_payload(payload), payload)

    def test_rejects_legacy_keys(self):
        from world.dialogue_schema import (
            DialogueSchemaError,
            validate_dialogue_payload,
        )

        with self.assertRaisesRegex(DialogueSchemaError, "greeting, hints"):
            validate_dialogue_payload(
                {
                    "greeting": "Hello.",
                    "topics": {"work": "Ask before acting."},
                    "hints": ["work"],
                }
            )

    def test_rejects_hint_prose_that_is_not_a_topic_reference(self):
        from world.dialogue_schema import (
            DialogueSchemaError,
            validate_dialogue_payload,
        )

        with self.assertRaisesRegex(DialogueSchemaError, "unknown topic"):
            validate_dialogue_payload(
                {
                    "topics": {"work": "Ask before acting."},
                    "base_hints": ["Try asking the keeper about work."],
                }
            )

    def test_rejects_conditional_topic_without_default_response(self):
        from world.dialogue_schema import (
            DialogueSchemaError,
            validate_dialogue_payload,
        )

        with self.assertRaisesRegex(DialogueSchemaError, "needs non-empty default"):
            validate_dialogue_payload(
                {
                    "topics": {
                        "work": {"friendly": "For you, there is always work."}
                    }
                }
            )

    def test_rejects_unknown_fields(self):
        from world.dialogue_schema import (
            DialogueSchemaError,
            validate_dialogue_payload,
        )

        with self.assertRaisesRegex(DialogueSchemaError, "unknown dialogue keys"):
            validate_dialogue_payload({"topics": {}, "quest_copy": {}})
