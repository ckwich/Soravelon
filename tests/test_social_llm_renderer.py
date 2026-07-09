import copy
import unittest


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

    def test_provider_payload_uses_only_redacted_prompt_inputs(self):
        from world.social_llm_renderer import build_social_quest_render_payload

        quest = self._quest_spec()
        llm_context = quest["social_quest_context"]["llm_context"]
        llm_context["prompt_inputs"]["api_key"] = "sk-should-not-leak"
        llm_context["prompt_inputs"]["nested_secret"] = {
            "deepseek_api_token": "secret-token",
            "safe": "kept",
        }
        quest["social_quest_context"]["admin_secret"] = "outside-prompt-inputs"

        payload = build_social_quest_render_payload(quest)

        payload_text = str(payload).lower()
        self.assertIn("prompt_inputs", payload)
        self.assertNotIn("sk-should-not-leak", payload_text)
        self.assertNotIn("secret-token", payload_text)
        self.assertNotIn("outside-prompt-inputs", payload_text)
        self.assertEqual(
            payload["prompt_inputs"]["nested_secret"]["deepseek_api_token"],
            "[redacted]",
        )
        self.assertEqual(payload["prompt_inputs"]["nested_secret"]["safe"], "kept")

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

    def test_provider_is_used_only_when_both_flags_allow_it(self):
        from world.social_llm_renderer import render_social_quest_offer

        quest = self._quest_spec()
        quest["social_quest_context"]["llm_context"]["provider_call_allowed"] = True
        provider = _RecordingProvider(
            {
                "speech": ("Remember the sealed report? Whistle needs quiet help now."),
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
            "Remember the sealed report? Whistle needs quiet help now.",
        )
        self.assertEqual(rendered["tone_tags"], ["personal", "quiet"])
        self.assertEqual(len(provider.calls), 1)


if __name__ == "__main__":
    unittest.main()
