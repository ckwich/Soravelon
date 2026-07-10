import ast
from collections import UserDict
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch


class TestSocialInterpretationProfiles(unittest.TestCase):
    """Anchor NPCs interpret Social Web memory through authored profiles."""

    @staticmethod
    def _authored_profile(npc_id):
        root = Path(__file__).resolve().parents[1]
        for area_path in (
            root / "world" / "areas" / "vaels_crossing.py",
            root / "world" / "areas" / "ashreach_plains.py",
        ):
            tree = ast.parse(area_path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "npc"
                    and len(node.args) >= 2
                ):
                    continue
                try:
                    authored_id = ast.literal_eval(node.args[1])
                except (SyntaxError, ValueError):
                    continue
                if authored_id != npc_id:
                    continue
                for keyword in node.keywords:
                    if keyword.arg == "social_profile":
                        return ast.literal_eval(keyword.value)
        raise AssertionError(f"Missing authored social profile for {npc_id}")

    def _npc(self, npc_id):
        return SimpleNamespace(
            key=npc_id,
            db=SimpleNamespace(
                npc_id=npc_id,
                social_profile=self._authored_profile(npc_id),
            ),
        )

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
                profile = get_social_profile(self._npc(npc_id))

                self.assertEqual(profile["public_trait"], public_trait)
                self.assertIn("social_role", profile)
                self.assertIn("worldview", profile)
                self.assertIn("memory_style", profile)

    def test_same_context_produces_different_anchor_interpretations(self):
        from world.social_interpretation import build_social_interpretation

        context = self._context()

        calloway = build_social_interpretation(
            self._npc("npc_warden_agent_calloway"),
            context,
        )
        whistle = build_social_interpretation(
            self._npc("npc_innkeeper_whistle"),
            context,
        )
        raith = build_social_interpretation(
            self._npc("npc_debt_collector_raith"),
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

    def test_same_rumor_produces_distinct_safe_dialogue_explanations(self):
        """Authored interpretation must affect what each NPC safely says."""
        from world.dialogue_engine import resolve_social_explanation
        from world.social_interpretation import build_social_interpretation

        character = SimpleNamespace(id=42)
        social_context = {
            "viewer": {"node_key": "npc:npc_warden_agent_calloway"},
            "subject": {"node_key": "player:42"},
            "purpose": "dialogue",
            "facts": [],
            "claims": [
                {
                    "claim_key": "claim:private:road-rumor",
                    "claim_type": "rumor",
                    "summary": "A traveler says the player kept a hard road clean.",
                    "status": "rumor",
                    "channel": "tavern_rumor",
                }
            ],
        }
        calloway = self._npc("npc_warden_agent_calloway")
        whistle = self._npc("npc_innkeeper_whistle")

        calloway_text = resolve_social_explanation(
            calloway,
            character,
            context={
                "social_context": social_context,
                "social_interpretation": build_social_interpretation(
                    calloway,
                    social_context,
                ),
            },
        )
        whistle_text = resolve_social_explanation(
            whistle,
            character,
            context={
                "social_context": social_context,
                "social_interpretation": build_social_interpretation(
                    whistle,
                    social_context,
                ),
            },
        )

        self.assertIn("notes the rumor", calloway_text)
        self.assertIn("heard it as road talk", whistle_text)
        self.assertNotEqual(calloway_text, whistle_text)
        for text in (calloway_text, whistle_text):
            self.assertNotIn("fact:", text)
            self.assertNotIn("claim:", text)
            self.assertNotIn("0.95", text)

    def test_unknown_npc_gets_safe_neutral_interpretation(self):
        from world.social_interpretation import build_social_interpretation

        interpretation = build_social_interpretation(
            SimpleNamespace(
                key="npc_unknown_listener",
                db=SimpleNamespace(npc_id="npc_unknown_listener", social_profile={}),
            ),
            self._context(),
        )

        self.assertEqual(interpretation["social_role"], "listener")
        self.assertEqual(interpretation["public_trait"], "")
        self.assertIn("nothing specific", interpretation["summary"])
        self.assertEqual(interpretation["matched_tags"], [])

    def test_profile_reader_accepts_persisted_mapping_values(self):
        from world.social_interpretation import get_social_profile

        profile = UserDict(
            {
                "social_role": "gatekeeper",
                "worldview": {"admires": ["reliable"]},
            }
        )
        npc = SimpleNamespace(
            key="npc_mapping_profile",
            db=SimpleNamespace(npc_id="npc_mapping_profile", social_profile=profile),
        )

        result = get_social_profile(npc)

        self.assertEqual(result["social_role"], "gatekeeper")
        self.assertIsInstance(result, dict)
        self.assertIsNot(result, profile)

    def test_profile_preferences_produce_a_guarded_interpretation(self):
        from world.social_interpretation import build_social_interpretation

        npc = SimpleNamespace(
            key="npc_test_listener",
            db=SimpleNamespace(
                npc_id="npc_test_listener",
                social_profile={
                    "social_role": "listener",
                    "worldview": {
                        "admires": ["reliable"],
                        "skeptical_of": ["rumor"],
                        "fears": ["coercion"],
                        "uses": ["official_report"],
                    },
                    "templates": {
                        "supported": "They take supported business seriously.",
                    },
                },
            ),
        )
        context = self._context()
        context["facts"][0]["tags"].append("coercion")

        interpretation = build_social_interpretation(npc, context)

        self.assertEqual(interpretation["stance"], "guarded")
        self.assertEqual(interpretation["admired_tags"], ["reliable"])
        self.assertEqual(interpretation["skeptical_tags"], [])
        self.assertEqual(interpretation["feared_tags"], ["coercion"])
        self.assertEqual(interpretation["preferred_channels"], ["official_report"])


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
                social_profile=TestSocialInterpretationProfiles._authored_profile(
                    "npc_warden_agent_calloway"
                ),
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
