import copy
import unittest

from django.test import override_settings


class _RecordingProvider:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def render(self, payload):
        self.calls.append(copy.deepcopy(payload))
        return self.response


class TestSocialLLMRenderer(unittest.TestCase):
    """LLM personalization is a renderer seam, never world truth."""

    def _quest_spec(self):
        from world.social_quest_offers import get_social_quest_spec_by_id

        quest = get_social_quest_spec_by_id("vc_sq_under_seal_dustwalkers_rest")
        self.assertIsNotNone(quest)
        return quest

    def test_renderer_falls_back_deterministically_without_mutating_quest(self):
        from world.social_llm_renderer import render_social_quest_offer

        quest = self._quest_spec()
        original = copy.deepcopy(quest)

        rendered = render_social_quest_offer(quest)

        self.assertFalse(rendered["provider_used"])
        self.assertTrue(rendered["fallback_used"])
        self.assertIn("speech", rendered)
        self.assertIn("Whistle", rendered["speech"])
        self.assertEqual(quest, original)

    def test_provider_payload_is_semantic_and_excludes_social_metadata(self):
        from world.social_llm_renderer import build_social_quest_render_payload

        quest = self._quest_spec()
        llm_context = quest["social_quest_context"]["llm_context"]
        llm_context["prompt_inputs"] = {
            "incident_brief": "Keep the witness safe before the story bends.",
            "archetype_brief": "Ask for quiet, credible help.",
            "prior_interactions": [
                {
                    "fact_key": "fact:player:private-route",
                    "summary": "The player delivered Calloway's sealed field report.",
                    "source": "official_report",
                }
            ],
            "social_memory": {
                "facts": [
                    {
                        "fact_key": "fact:player:warden-report",
                        "summary": "The player delivered Calloway's sealed field report.",
                        "visibility": "institutional",
                        "channel": "official_report",
                        "confidence": 0.95,
                        "tags": ["warden", "report"],
                    },
                    {
                        "fact_key": "fact:player:private",
                        "summary": "Private evidence must never leave the server.",
                        "visibility": "private",
                        "confidence": 1.0,
                    },
                ],
                "claims": [
                    {
                        "claim_key": "claim:calloway:player:report",
                        "summary": "Calloway has a withheld implication.",
                        "status": "supported",
                        "confidence": 0.8,
                        "trace": [{"edge_key": "edge:secret"}],
                    }
                ],
            },
            "objective_steps": [
                {
                    "id": "pressure_inquiry",
                    "target": "npc_innkeeper_whistle",
                    "summary": "Learn what the witness knows.",
                }
            ],
            "api_key": "sk-should-not-leak",
        }
        quest["social_quest_context"]["actors"] = {
            "witness": {
                "node_key": "npc:npc_innkeeper_whistle",
                "display_name": "Whistle",
            }
        }
        quest["social_quest_context"]["offer_explainability"] = {
            "withheld_implications": ["Never send this to a provider."],
        }

        payload = build_social_quest_render_payload(quest)

        payload_text = str(payload).lower()
        semantic_packet = payload["semantic_packet"]
        self.assertIn("The player delivered Calloway's sealed field report.", str(semantic_packet))
        self.assertIn("Whistle", semantic_packet["allowed_entities"])
        self.assertNotIn("prompt_inputs", payload)
        self.assertNotIn("sk-should-not-leak", payload_text)
        self.assertNotIn("fact:player", payload_text)
        self.assertNotIn("claim:calloway", payload_text)
        self.assertNotIn("npc:npc_innkeeper", payload_text)
        self.assertNotIn("edge:secret", payload_text)
        self.assertNotIn("0.95", payload_text)
        self.assertNotIn("never leave the server", payload_text)
        self.assertNotIn("withheld implication", payload_text)

    @override_settings(SOCIAL_RENDERER_ENABLED=True)
    def test_provider_call_is_refused_when_context_forbids_it(self):
        from world.social_llm_renderer import render_social_quest_offer

        quest = self._quest_spec()
        provider = _RecordingProvider({"speech": "Provider text", "tone_tags": []})

        rendered = render_social_quest_offer(
            quest,
            provider=provider,
            allow_provider_call=True,
        )

        self.assertFalse(rendered["provider_used"])
        self.assertTrue(rendered["fallback_used"])
        self.assertEqual(provider.calls, [])

    @override_settings(SOCIAL_RENDERER_ENABLED=True)
    def test_provider_call_requires_explicit_caller_permission(self):
        from world.social_llm_renderer import render_social_quest_offer

        quest = self._quest_spec()
        quest["social_quest_context"]["llm_context"]["provider_call_allowed"] = True
        provider = _RecordingProvider({"speech": "Whistle needs your help.", "tone_tags": []})

        rendered = render_social_quest_offer(
            quest,
            provider=provider,
            allow_provider_call=False,
        )

        self.assertFalse(rendered["provider_used"])
        self.assertTrue(rendered["fallback_used"])
        self.assertEqual(provider.calls, [])

    @override_settings(SOCIAL_RENDERER_ENABLED=False)
    def test_provider_call_requires_runtime_renderer_configuration(self):
        from world.social_llm_renderer import render_social_quest_offer

        quest = self._quest_spec()
        quest["social_quest_context"]["llm_context"]["provider_call_allowed"] = True
        provider = _RecordingProvider({"speech": "Whistle needs your help.", "tone_tags": []})

        rendered = render_social_quest_offer(
            quest,
            provider=provider,
            allow_provider_call=True,
        )

        self.assertFalse(rendered["provider_used"])
        self.assertTrue(rendered["fallback_used"])
        self.assertEqual(provider.calls, [])

    @override_settings(SOCIAL_RENDERER_ENABLED=True)
    def test_provider_is_used_only_when_all_three_gates_allow_it(self):
        from world.social_llm_renderer import render_social_quest_offer

        quest = self._quest_spec()
        quest["social_quest_context"]["llm_context"]["provider_call_allowed"] = True
        provider = _RecordingProvider(
            {
                "speech": "Whistle needs quiet help now.",
                "tone_tags": ["personal", "quiet"],
            }
        )

        rendered = render_social_quest_offer(
            quest,
            provider=provider,
            allow_provider_call=True,
        )

        self.assertTrue(rendered["provider_used"])
        self.assertFalse(rendered["fallback_used"])
        self.assertEqual(
            rendered["speech"],
            "Whistle needs quiet help now.",
        )
        self.assertEqual(rendered["tone_tags"], ["personal", "quiet"])
        self.assertEqual(len(provider.calls), 1)

    @override_settings(SOCIAL_RENDERER_ENABLED=True)
    def test_provider_output_with_ids_entities_lore_or_excess_length_falls_back(self):
        from world.social_llm_renderer import render_social_quest_offer

        quest = self._quest_spec()
        quest["social_quest_context"]["llm_context"]["provider_call_allowed"] = True
        unsafe_speeches = (
            "Maren wants to discuss the road.",
            "Whistle read fact:player:secret in the report.",
            "Remnance changes everything here.",
            "x" * 481,
        )

        for speech in unsafe_speeches:
            with self.subTest(speech=speech[:24]):
                provider = _RecordingProvider({"speech": speech, "tone_tags": []})

                rendered = render_social_quest_offer(
                    quest,
                    provider=provider,
                    allow_provider_call=True,
                )

                self.assertFalse(rendered["provider_used"])
                self.assertTrue(rendered["fallback_used"])
                self.assertEqual(len(provider.calls), 1)


if __name__ == "__main__":
    unittest.main()
