from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch


class TestSocialInterpretationProfiles(unittest.TestCase):
    """Anchor NPCs interpret Social Web memory through authored profiles."""

    def _context(self):
        return {
            "viewer": {"node_key": "npc:npc_warden_agent_calloway"},
            "subject": {"node_key": "player:42"},
            "purpose": "dialogue",
            "facts": [
                {
                    "fact_key": "fact:42:vc_q_warden_report:delivered",
                    "event_type": "quest_completed",
                    "summary": "The player delivered Calloway's sealed field report.",
                    "tags": ["reliable", "warden", "report", "quest"],
                    "channel": "official_report",
                    "visibility": "institutional",
                }
            ],
            "claims": [
                {
                    "claim_key": "claim:calloway:42:vc_q_warden_report:delivered",
                    "claim_type": "report",
                    "summary": (
                        "Calloway reports that the player carried Warden "
                        "business cleanly."
                    ),
                    "status": "supported",
                    "channel": "official_report",
                    "trace": [{"edge_type": "warden_report"}],
                }
            ],
        }

    def test_anchor_profiles_are_authored_and_distinct(self):
        from world.social_interpretation import get_social_profile

        expected = {
            "npc_warden_agent_calloway": "careful Warden contact",
            "npc_warden_outpost_commander": "road-worn field commander",
            "npc_innkeeper_whistle": "innkeeper with a long ear",
            "npc_debt_collector_raith": "obligation broker",
            "npc_courier_agent_renn": "route-minded courier agent",
        }

        for npc_id, public_trait in expected.items():
            with self.subTest(npc_id=npc_id):
                profile = get_social_profile(npc_id)

                self.assertEqual(profile["public_trait"], public_trait)
                self.assertIn("social_role", profile)
                self.assertIn("worldview", profile)
                self.assertIn("memory_style", profile)

    def test_same_context_produces_different_anchor_interpretations(self):
        from world.social_interpretation import build_social_interpretation

        context = self._context()

        calloway = build_social_interpretation(
            "npc_warden_agent_calloway",
            context,
        )
        whistle = build_social_interpretation(
            "npc_innkeeper_whistle",
            context,
        )
        raith = build_social_interpretation(
            "npc_debt_collector_raith",
            context,
        )

        self.assertEqual(calloway["social_role"], "gatekeeper")
        self.assertIn("supported report", calloway["summary"])
        self.assertIn("official report", calloway["evidence_channels"])

        self.assertEqual(whistle["social_role"], "gossip")
        self.assertIn("heard it as road talk", whistle["summary"])
        self.assertIn("keeps sealed details at arm's length", whistle["summary"])

        self.assertEqual(raith["social_role"], "creditor")
        self.assertIn("leverage", raith["summary"])
        self.assertIn("useful", raith["stance"])

        self.assertNotEqual(calloway["summary"], whistle["summary"])
        self.assertNotEqual(whistle["summary"], raith["summary"])

    def test_unknown_npc_gets_safe_neutral_interpretation(self):
        from world.social_interpretation import build_social_interpretation

        interpretation = build_social_interpretation(
            "npc_unknown_listener",
            self._context(),
        )

        self.assertEqual(interpretation["social_role"], "listener")
        self.assertEqual(interpretation["public_trait"], "")
        self.assertIn("nothing specific", interpretation["summary"])
        self.assertEqual(interpretation["matched_tags"], [])


class TestDialogueInterpretationIntegration(unittest.TestCase):
    """Dialogue context exposes deterministic interpretation beside raw context."""

    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    @patch("world.social_engine.query_social_context")
    @patch("world.models.CharacterQuest.objects.filter")
    def test_build_dialogue_context_includes_social_interpretation(
        self,
        mock_character_quest_filter,
        mock_social_context,
        mock_context_packet,
        _mock_standing,
        _mock_active,
    ):
        from world.dialogue_engine import _build_dialogue_context

        empty_quest_queryset = MagicMock()
        empty_quest_queryset.values_list.return_value = []
        mock_character_quest_filter.return_value = empty_quest_queryset
        social_context = {
            "viewer": {"node_key": "npc:npc_warden_agent_calloway"},
            "subject": {"node_key": "player:42"},
            "purpose": "dialogue",
            "facts": [
                {
                    "summary": "The player delivered Calloway's sealed report.",
                    "tags": ["warden", "report", "reliable"],
                    "channel": "official_report",
                    "visibility": "institutional",
                    "event_type": "quest_completed",
                }
            ],
            "claims": [],
        }
        mock_social_context.return_value = social_context
        mock_context_packet.return_value = {
            "reputation": 0,
            "network": 0,
            "betrayal_flag": False,
        }
        npc = SimpleNamespace(
            db=SimpleNamespace(
                npc_id="npc_warden_agent_calloway",
                zone_id="vaels_crossing",
                faction="wardens",
            ),
            key="Agent Calloway",
        )
        character = SimpleNamespace(id=42)

        context = _build_dialogue_context(npc, character)

        self.assertEqual(context["social_context"], social_context)
        interpretation = context["social_interpretation"]
        self.assertEqual(interpretation["npc_id"], "npc_warden_agent_calloway")
        self.assertEqual(interpretation["public_trait"], "careful Warden contact")
        self.assertIn("supported report", interpretation["summary"])


if __name__ == "__main__":
    unittest.main()
