import pathlib
import subprocess
import sys
import unittest


class TestSocialWebPlaytestHarness(unittest.TestCase):
    """The playtest route is explicit enough for a human to run."""

    def test_harness_prints_every_required_vertical_beat(self):
        result = subprocess.run(
            [sys.executable, "scripts/playtest_social_web_vertical.py"],
            check=True,
            capture_output=True,
            text=True,
        )

        output = result.stdout
        required_phrases = [
            "Warden report completion",
            "Calloway explanation",
            "Harven cross-zone knowledge",
            "Whistle local rumor knowledge",
            "dynamic social quest lifecycle",
            "denial/repair verb",
            "renderer fallback",
            "socialmemory inspection",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, output)

    def test_human_playtest_guide_lists_commands_and_expected_observations(self):
        guide_path = pathlib.Path("docs/playtests/social-web-vaels-crossing.md")
        guide = guide_path.read_text()

        for command in [
            "talk Agent Calloway",
            "ask Agent Calloway why",
            "talk Commander Harven",
            "talk Whistle",
            "deny Whistle about me",
            "socialmemory npc:npc_innkeeper_whistle player:",
        ]:
            with self.subTest(command=command):
                self.assertIn(command, guide)

        for expected in [
            "Calloway can explain the supported Warden route",
            "Whistle should not know the sealed Warden details",
            "the offer uses deterministic renderer fallback",
            "the original rumor remains intact",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, guide)


if __name__ == "__main__":
    unittest.main()
