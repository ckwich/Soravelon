import pathlib
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from unittest.mock import patch

from evennia.utils.test_resources import EvenniaTest

from scripts import playtest_social_web_vertical


class TestSocialWebPlaytestHarness(unittest.TestCase):
    """The playtest route is explicit enough for a human to run."""

    def test_verify_mode_runs_the_runtime_gate_and_reports_each_check(self):
        expected_checks = {
            "applied migrations": "all current",
            "materialized topology": "Vael route present",
            "reciprocal exits": "road route connected",
            "edge policy": "Warden and traveler policy valid",
            "route state": "Calloway to Harven traversable",
        }
        output = StringIO()

        with redirect_stdout(output):
            result = playtest_social_web_vertical.main(
                ["--verify"],
                verify_runtime=lambda: expected_checks,
            )

        self.assertEqual(result, 0)
        for check, detail in expected_checks.items():
            with self.subTest(check=check):
                self.assertIn(f"PASS {check}: {detail}", output.getvalue())

    def test_verify_mode_reports_an_actionable_runtime_failure(self):
        from world.social_playtest_verification import SocialWebRuntimeVerificationError

        output = StringIO()
        with redirect_stdout(output):
            result = playtest_social_web_vertical.main(
                ["--verify"],
                verify_runtime=lambda: (_ for _ in ()).throw(
                    SocialWebRuntimeVerificationError("materialized route missing")
                ),
            )

        self.assertEqual(result, 1)
        self.assertIn("FAIL materialized route missing", output.getvalue())

    def test_script_requires_verify_instead_of_printing_a_decorative_route(self):
        with redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit) as raised:
                playtest_social_web_vertical.main([])

        self.assertEqual(raised.exception.code, 2)
        self.assertFalse(
            hasattr(playtest_social_web_vertical, "build_playtest_beats")
        )

    def test_human_playtest_guide_describes_runtime_verification_without_fake_commands(self):
        guide = pathlib.Path("docs/playtests/social-web-vaels-crossing.md").read_text()

        for expected in [
            "python scripts/playtest_social_web_vertical.py --verify",
            "applied migrations",
            "materialized topology",
            "reciprocal exits",
            "edge policy",
            "route state",
            "database-backed command and movement test",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, guide)

        for forbidden in [
            "travel to Ashreach Outpost",
            "trigger the inn-traveler rumor route",
            "socialmemory npc:",
        ]:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, guide)

class TestSocialWebLiveRuntimeVerification(EvenniaTest):
    """The verification gate inspects the materialized game, not a checklist."""

    def test_verifier_proves_the_materialized_vaels_to_harven_route(self):
        from world.areas import ashreach_plains, vaels_crossing
        from world.social_playtest_verification import verify_social_web_runtime

        ashreach_plains.build()
        vaels_crossing.build()
        # The server's second pass revisits an area after its cross-zone target
        # exists. Rebuilding Ashreach here materializes its authored northbound
        # return exit without widening this focused test to every area module.
        ashreach_plains.build()

        checks = verify_social_web_runtime()

        self.assertIn("world migrations current", checks["applied migrations"])
        self.assertIn("6 nodes", checks["materialized topology"])
        self.assertIn("hg_south_road south", checks["reciprocal exits"])
        self.assertIn("warden_report", checks["edge policy"])
        self.assertIn("Agent Calloway", checks["route state"])
        self.assertIn("Commander Harven", checks["route state"])

    def test_verify_command_uses_the_real_runtime_verifier(self):
        from world.areas import ashreach_plains, vaels_crossing

        ashreach_plains.build()
        vaels_crossing.build()
        ashreach_plains.build()

        output = StringIO()
        with redirect_stdout(output):
            result = playtest_social_web_vertical.main(["--verify"])

        self.assertEqual(result, 0)
        self.assertIn("PASS applied migrations:", output.getvalue())
        self.assertIn("PASS route state:", output.getvalue())


class TestSocialWebCommandMovementAcceptance(EvenniaTest):
    """The Warden route is playable through real command and exit seams."""

    def test_accept_move_and_delivery_write_live_social_consequences(self):
        import evennia

        from commands.cmd_dialogue import CmdAccept, CmdTalk
        from world.areas import ashreach_plains, vaels_crossing
        from world.models import CharacterQuest, SocialClaim, SocialFact, SocialKnowledge
        from world.social_playtest_verification import _shortest_route

        ashreach_plains.build()
        vaels_crossing.build()
        ashreach_plains.build()

        calloway = next(
            npc
            for npc in evennia.search_tag(
                "npc_warden_agent_calloway", category="npc_id"
            )
            if npc.db.zone_id == "vaels_crossing"
        )
        harven = next(
            npc
            for npc in evennia.search_tag(
                "npc_warden_outpost_commander", category="npc_id"
            )
            if npc.db.zone_id == "ashreach_plains"
        )
        self.char1.location = calloway.location

        with patch.object(self.char1, "msg"), patch(
            "world.oob_publisher.push_quest_update"
        ):
            talk = CmdTalk()
            talk.caller = self.char1
            talk.args = "Calloway"
            talk.func()

            self.assertEqual(
                self.char1.ndb.pending_quest_offer["quest"]["quest_id"],
                "vc_q_warden_report",
            )

            accept = CmdAccept()
            accept.caller = self.char1
            accept.args = ""
            accept.func()

            route = _shortest_route(calloway.location, harven.location)
            self.assertTrue(route)
            for exit_obj in route:
                exit_obj.at_traverse(self.char1, exit_obj.destination)
                self.assertIs(self.char1.location, exit_obj.destination)
            self.assertIs(self.char1.location, harven.location)

            deliver = CmdTalk()
            deliver.caller = self.char1
            deliver.args = "Harven"
            deliver.func()

        quest = CharacterQuest.objects.get(
            character=self.char1,
            quest_id="vc_q_warden_report",
        )
        self.assertEqual(quest.status, "complete")
        fact_key = f"fact:{self.char1.id}:vc_q_warden_report:delivered"
        claim_key = f"claim:calloway:{self.char1.id}:vc_q_warden_report:delivered"
        self.assertTrue(SocialFact.objects.filter(fact_key=fact_key).exists())
        self.assertTrue(SocialClaim.objects.filter(claim_key=claim_key).exists())
        self.assertEqual(
            set(
                SocialKnowledge.objects.filter(claim__claim_key=claim_key).values_list(
                    "node__node_key", flat=True
                )
            ),
            {
                "npc:npc_warden_agent_calloway",
                "npc:npc_warden_outpost_commander",
            },
        )


if __name__ == "__main__":
    unittest.main()
