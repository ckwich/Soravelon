"""Contracts for runtime-effective authored dialogue payloads."""

import unittest
from pathlib import Path


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

    def test_every_authored_area_dialogue_payload_passes_the_schema(self):
        from world.content_compiler import (
            _frozen_map_get,
            _thaw,
            compile_world_manifest,
        )
        from world.dialogue_schema import (
            DialogueSchemaError,
            validate_dialogue_payload,
        )

        areas_dir = Path(__file__).resolve().parents[1] / "world" / "areas"
        compilation = compile_world_manifest(areas_dir)
        self.assertEqual(compilation.diagnostics, ())

        failures = []
        for zone in compilation.manifest.zones:
            for operation in zone.operations:
                if operation.method != "npc":
                    continue
                dialogue = _thaw(
                    _frozen_map_get(operation.keyword_arguments, "dialogue", {})
                )
                try:
                    validate_dialogue_payload(dialogue)
                except DialogueSchemaError as error:
                    failures.append(
                        f"{operation.source_path}:{operation.line}: {error}"
                    )

        self.assertEqual(failures, [])
