"""
Tests for the NPC dialogue system (Phase 06c).

Covers NPC-01 (context packet injection), NPC-02 (Standing-based responses),
NPC-03 (context packet interface stability), D-04 (dynamic hints),
D-05 (keyword extraction).

Uses unittest.TestCase with MagicMock for pure-logic functions and
EvenniaTest for model-backed operations (KnownTopicRecord).
"""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from evennia.utils.test_resources import EvenniaTest


class TestQuestOfferAcceptance(unittest.TestCase):
    """Quest-offer command edge cases that do not need live Evennia objects."""

    def test_oob_payload_handles_chained_offer_without_npc(self):
        from commands.cmd_dialogue import _build_quest_oob_payload

        payload = _build_quest_oob_payload(
            None,
            {
                "quest_id": "chain_step_two",
                "name": "Second Step",
                "quest_giver": "npc_route_captain",
            },
        )

        self.assertEqual(payload["quest_id"], "chain_step_two")
        self.assertEqual(payload["quest_name"], "Second Step")
        self.assertEqual(payload["npc_id"], "npc_route_captain")
        self.assertEqual(payload["npc_name"], "npc_route_captain")

    @patch("world.oob_publisher.push_quest_update")
    @patch("world.quest_engine.accept_quest")
    def test_accept_handles_chained_offer_without_live_npc(
        self,
        mock_accept,
        mock_push,
    ):
        from commands.cmd_dialogue import CmdAccept

        mock_accept.return_value = (True, "Quest accepted: Second Step")
        character = MagicMock()
        character.ndb = SimpleNamespace(
            pending_quest_offer={
                "npc": None,
                "quest": {
                    "quest_id": "chain_step_two",
                    "name": "Second Step",
                    "quest_giver": "npc_route_captain",
                },
            }
        )

        cmd = CmdAccept()
        cmd.caller = character
        cmd.func()

        mock_accept.assert_called_once()
        mock_push.assert_called_once()
        character.msg.assert_called_once()
        self.assertIn("Quest accepted: Second Step", character.msg.call_args[0][0])
        self.assertIsNone(character.ndb.pending_quest_offer)


# ---------------------------------------------------------------------------
# NPC-02: Standing tier mapping
# ---------------------------------------------------------------------------


class TestStandingTierMapping(unittest.TestCase):
    """Standing tier must map disposition floats to the correct 8 tiers."""

    def _make_npc(self, faction="empire"):
        npc = MagicMock()
        npc.db.faction = faction
        npc.db.is_npc = True
        return npc

    def _make_char(self):
        char = MagicMock()
        return char

    @patch("world.world_state.get_betrayal", return_value=False)
    @patch("world.mob_disposition.get_mob_disposition")
    def test_exalted_tier(self, mock_disp, mock_betray):
        from world.dialogue_engine import get_standing_tier

        mock_disp.return_value = 0.9
        tier = get_standing_tier(self._make_char(), self._make_npc())
        self.assertEqual(tier, "exalted")

    @patch("world.world_state.get_betrayal", return_value=False)
    @patch("world.mob_disposition.get_mob_disposition")
    def test_honored_tier(self, mock_disp, mock_betray):
        from world.dialogue_engine import get_standing_tier

        mock_disp.return_value = 0.7
        tier = get_standing_tier(self._make_char(), self._make_npc())
        self.assertEqual(tier, "honored")

    @patch("world.world_state.get_betrayal", return_value=False)
    @patch("world.mob_disposition.get_mob_disposition")
    def test_friendly_tier(self, mock_disp, mock_betray):
        from world.dialogue_engine import get_standing_tier

        mock_disp.return_value = 0.5
        tier = get_standing_tier(self._make_char(), self._make_npc())
        self.assertEqual(tier, "friendly")

    @patch("world.world_state.get_betrayal", return_value=False)
    @patch("world.mob_disposition.get_mob_disposition")
    def test_acknowledged_tier(self, mock_disp, mock_betray):
        from world.dialogue_engine import get_standing_tier

        mock_disp.return_value = 0.3
        tier = get_standing_tier(self._make_char(), self._make_npc())
        self.assertEqual(tier, "acknowledged")

    @patch("world.world_state.get_betrayal", return_value=False)
    @patch("world.mob_disposition.get_mob_disposition")
    def test_neutral_tier(self, mock_disp, mock_betray):
        from world.dialogue_engine import get_standing_tier

        mock_disp.return_value = 0.0
        tier = get_standing_tier(self._make_char(), self._make_npc())
        self.assertEqual(tier, "neutral")

    @patch("world.world_state.get_betrayal", return_value=False)
    @patch("world.mob_disposition.get_mob_disposition")
    def test_unfriendly_tier(self, mock_disp, mock_betray):
        from world.dialogue_engine import get_standing_tier

        mock_disp.return_value = -0.3
        tier = get_standing_tier(self._make_char(), self._make_npc())
        self.assertEqual(tier, "unfriendly")

    @patch("world.world_state.get_betrayal", return_value=False)
    @patch("world.mob_disposition.get_mob_disposition")
    def test_hostile_tier(self, mock_disp, mock_betray):
        from world.dialogue_engine import get_standing_tier

        mock_disp.return_value = -0.7
        tier = get_standing_tier(self._make_char(), self._make_npc())
        self.assertEqual(tier, "hostile")

    @patch("world.world_state.get_betrayal", return_value=True)
    @patch("world.mob_disposition.get_mob_disposition")
    def test_betrayal_overrides_disposition(self, mock_disp, mock_betray):
        """Betrayal flag returns 'betrayal' regardless of high disposition."""
        from world.dialogue_engine import get_standing_tier

        mock_disp.return_value = 0.9  # would be exalted otherwise
        tier = get_standing_tier(self._make_char(), self._make_npc())
        self.assertEqual(tier, "betrayal")


# ---------------------------------------------------------------------------
# NPC-02: Greeting resolution
# ---------------------------------------------------------------------------


class TestGreetingResolution(unittest.TestCase):
    """resolve_greeting selects correct text based on Standing tier."""

    def _make_npc(self, greetings=None, name="Blacksmith Torva"):
        npc = MagicMock()
        npc.db.dialogue_greeting_tiers = greetings or {}
        npc.db.faction = "empire"
        npc.db.is_npc = True
        npc.db.npc_name = name
        npc.key = name
        return npc

    def _make_char(self):
        return MagicMock()

    @patch("world.dialogue_engine.get_standing_tier", return_value="honored")
    def test_correct_tier_text_returned(self, mock_tier):
        from world.dialogue_engine import resolve_greeting

        npc = self._make_npc({"honored": "Well met, friend!"})
        text, tier = resolve_greeting(npc, self._make_char())
        self.assertEqual(text, "Well met, friend!")
        self.assertEqual(tier, "honored")

    @patch("world.dialogue_engine.get_standing_tier", return_value="exalted")
    def test_fallback_to_neutral(self, mock_tier):
        """Falls back to neutral when authored tier is missing."""
        from world.dialogue_engine import resolve_greeting

        npc = self._make_npc({"neutral": "Hello there."})
        text, tier = resolve_greeting(npc, self._make_char())
        self.assertEqual(text, "Hello there.")
        self.assertEqual(tier, "neutral")

    @patch("world.dialogue_engine.get_standing_tier", return_value="hostile")
    def test_generic_fallback_no_greetings(self, mock_tier):
        """Generic fallback when no greeting data exists."""
        from world.dialogue_engine import resolve_greeting

        npc = self._make_npc({}, name="Gruff Soldier")
        text, tier = resolve_greeting(npc, self._make_char())
        self.assertIn("Gruff Soldier", text)
        self.assertEqual(tier, "default")


# ---------------------------------------------------------------------------
# NPC-02: Topic priority stack
# ---------------------------------------------------------------------------


class TestTopicPriorityStack(unittest.TestCase):
    """resolve_topic_response returns the highest-priority matching condition."""

    def _make_npc(self, topics=None):
        npc = MagicMock()
        npc.db.dialogue_topics = topics or {}
        npc.db.faction = "empire"
        npc.db.is_npc = True
        npc.db.zone_id = "test_zone"
        return npc

    def _make_char(self):
        return MagicMock()

    @patch("world.dialogue_engine._build_dialogue_context")
    def test_quest_complete_wins_over_honored(self, mock_ctx):
        from world.dialogue_engine import resolve_topic_response

        mock_ctx.return_value = {
            "standing_tier": "honored",
            "completed_quests": ["quest_1"],
            "active_quests": [],
            "failed_quests": [],
            "betrayal_flag": False,
        }
        npc = self._make_npc({
            "wolves": {
                "quest_complete": "The wolves are gone, thanks to you.",
                "honored": "The wolves are a danger to travelers.",
                "default": "Wolves roam the area.",
            }
        })
        text, condition = resolve_topic_response(npc, self._make_char(), "wolves")
        self.assertEqual(condition, "quest_complete")
        self.assertIn("gone", text)

    @patch("world.dialogue_engine._build_dialogue_context")
    def test_honored_when_no_quest(self, mock_ctx):
        from world.dialogue_engine import resolve_topic_response

        mock_ctx.return_value = {
            "standing_tier": "honored",
            "completed_quests": [],
            "active_quests": [],
            "failed_quests": [],
            "betrayal_flag": False,
        }
        npc = self._make_npc({
            "wolves": {
                "quest_complete": "The wolves are gone.",
                "honored": "Between us, the wolves answer to the Greyclaw.",
                "default": "Wolves roam the area.",
            }
        })
        text, condition = resolve_topic_response(npc, self._make_char(), "wolves")
        self.assertEqual(condition, "honored")
        self.assertIn("Greyclaw", text)

    @patch("world.dialogue_engine._build_dialogue_context")
    def test_default_fallback(self, mock_ctx):
        from world.dialogue_engine import resolve_topic_response

        mock_ctx.return_value = {
            "standing_tier": "neutral",
            "completed_quests": [],
            "active_quests": [],
            "failed_quests": [],
            "betrayal_flag": False,
        }
        npc = self._make_npc({
            "wolves": {
                "honored": "Secret wolf info.",
                "default": "Wolves roam the area.",
            }
        })
        text, condition = resolve_topic_response(npc, self._make_char(), "wolves")
        self.assertEqual(condition, "default")
        self.assertIn("roam", text)

    def test_unknown_topic_returns_none(self):
        from world.dialogue_engine import resolve_topic_response

        npc = self._make_npc({"wolves": {"default": "Wolves."}})
        text, condition = resolve_topic_response(
            npc, MagicMock(), "nonexistent_topic"
        )
        self.assertIsNone(text)
        self.assertIsNone(condition)

    @patch("world.dialogue_engine._build_dialogue_context")
    def test_supplied_context_is_reused_for_topic_resolution(self, mock_ctx):
        from world.dialogue_engine import resolve_topic_response

        context = {
            "standing_tier": "friendly",
            "completed_quests": [],
            "active_quests": [],
            "failed_quests": [],
            "betrayal_flag": False,
        }
        npc = self._make_npc({
            "wolves": {
                "friendly": "Between friends, the wolves avoid the old road.",
                "default": "Wolves roam the area.",
            }
        })

        text, condition = resolve_topic_response(
            npc,
            self._make_char(),
            "wolves",
            context=context,
        )

        mock_ctx.assert_not_called()
        self.assertEqual(condition, "friendly")
        self.assertIn("old road", text)


# ---------------------------------------------------------------------------
# D-05: Keyword extraction
# ---------------------------------------------------------------------------


class TestKeywordExtraction(unittest.TestCase):
    """extract_topic matches player input to available topic keys."""

    def test_direct_match(self):
        from world.dialogue_engine import extract_topic

        result = extract_topic("wolves", ["wolves", "node", "work"])
        self.assertEqual(result, "wolves")

    def test_synonym_match(self):
        from world.dialogue_engine import extract_topic

        result = extract_topic("tell me about the wolf", ["wolves", "node"])
        self.assertEqual(result, "wolves")

    def test_partial_word_match(self):
        from world.dialogue_engine import extract_topic

        result = extract_topic(
            "I saw a strange node", ["node_reading", "wolves"]
        )
        self.assertEqual(result, "node_reading")

    def test_no_match_returns_none(self):
        from world.dialogue_engine import extract_topic

        result = extract_topic("hello there", ["wolves", "node_reading"])
        self.assertIsNone(result)

    def test_longest_match_wins(self):
        """node_reading should match before node when input has 'node reading'."""
        from world.dialogue_engine import extract_topic

        result = extract_topic(
            "what about the node reading", ["node", "node_reading"]
        )
        self.assertEqual(result, "node_reading")

    def test_empty_input_returns_none(self):
        from world.dialogue_engine import extract_topic

        self.assertIsNone(extract_topic("", ["wolves"]))
        self.assertIsNone(extract_topic(None, ["wolves"]))

    def test_empty_topics_returns_none(self):
        from world.dialogue_engine import extract_topic

        self.assertIsNone(extract_topic("wolves", []))
        self.assertIsNone(extract_topic("wolves", None))


# ---------------------------------------------------------------------------
# D-04: Dynamic hints
# ---------------------------------------------------------------------------


class TestDynamicHints(EvenniaTest):
    """get_npc_hints filters by tier, known topics, and caps at MAX_HINTS."""

    def _make_npc(
        self,
        base_hints=None,
        tier_hints=None,
        faction="empire",
    ):
        npc = MagicMock()
        npc.db.dialogue_base_hints = base_hints or []
        npc.db.dialogue_tier_hints = tier_hints or {}
        npc.db.dialogue_quest_hints = {}
        npc.db.dialogue_network_hints = []
        npc.db.dialogue_scholar_hints = []
        npc.db.dialogue_warden_hints = []
        npc.db.faction = faction
        npc.db.is_npc = True
        npc.db.zone_id = "test_zone"
        npc.db.npc_id = "test_npc"
        npc.key = "Test NPC"
        return npc

    @patch("world.dialogue_engine.get_standing_tier", return_value="friendly")
    @patch("world.dialogue_engine._build_dialogue_context")
    def test_base_hints_always_included(self, mock_ctx, mock_tier):
        from world.dialogue_engine import get_npc_hints

        mock_ctx.return_value = {
            "standing_tier": "friendly",
            "network": 0,
            "reputation": 0,
            "primary_domain": None,
            "subclass": None,
            "guild": None,
            "completed_quests": [],
        }
        npc = self._make_npc(base_hints=["wolves", "work"])
        hints = get_npc_hints(npc, self.char1)
        self.assertIn("wolves", hints)
        self.assertIn("work", hints)

    @patch("world.dialogue_engine.get_standing_tier", return_value="friendly")
    @patch("world.dialogue_engine._build_dialogue_context")
    def test_tier_hints_excluded_when_wrong_tier(self, mock_ctx, mock_tier):
        from world.dialogue_engine import get_npc_hints

        mock_ctx.return_value = {
            "standing_tier": "friendly",
            "network": 0,
            "reputation": 0,
            "primary_domain": None,
            "subclass": None,
            "guild": None,
            "completed_quests": [],
        }
        npc = self._make_npc(
            base_hints=["wolves", "work"],
            tier_hints={"honored": ["secret_node"]},
        )
        hints = get_npc_hints(npc, self.char1)
        self.assertNotIn("secret_node", hints)

    @patch("world.dialogue_engine.get_standing_tier", return_value="honored")
    @patch("world.dialogue_engine._build_dialogue_context")
    def test_tier_hints_included_when_matching(self, mock_ctx, mock_tier):
        from world.dialogue_engine import get_npc_hints

        mock_ctx.return_value = {
            "standing_tier": "honored",
            "network": 0,
            "reputation": 0,
            "primary_domain": None,
            "subclass": None,
            "guild": None,
            "completed_quests": [],
        }
        npc = self._make_npc(
            base_hints=["wolves", "work"],
            tier_hints={"honored": ["secret_node"]},
        )
        hints = get_npc_hints(npc, self.char1)
        self.assertIn("secret_node", hints)

    @patch("world.dialogue_engine.get_standing_tier", return_value="friendly")
    @patch("world.dialogue_engine._build_dialogue_context")
    def test_known_topics_excluded(self, mock_ctx, mock_tier):
        from world.dialogue_engine import get_npc_hints, record_topic_learned
        from world.dialogue_engine import _compute_context_hash

        ctx = {
            "standing_tier": "friendly",
            "network": 0,
            "reputation": 0,
            "primary_domain": None,
            "subclass": None,
            "guild": None,
            "completed_quests": [],
        }
        mock_ctx.return_value = ctx
        npc = self._make_npc(base_hints=["wolves", "work"])

        # Record 'wolves' as learned
        record_topic_learned(self.char1, "test_npc", "wolves", ctx)

        hints = get_npc_hints(npc, self.char1)
        self.assertNotIn("wolves", hints)
        self.assertIn("work", hints)

    @patch("world.dialogue_engine.get_standing_tier", return_value="friendly")
    @patch("world.dialogue_engine._build_dialogue_context")
    def test_hints_capped_at_max(self, mock_ctx, mock_tier):
        from world.dialogue_engine import get_npc_hints
        from world.dialogue_definitions import MAX_HINTS_DISPLAYED

        mock_ctx.return_value = {
            "standing_tier": "friendly",
            "network": 0,
            "reputation": 0,
            "primary_domain": None,
            "subclass": None,
            "guild": None,
            "completed_quests": [],
        }
        many_hints = [f"hint_{i}" for i in range(8)]
        npc = self._make_npc(base_hints=many_hints)
        hints = get_npc_hints(npc, self.char1)
        self.assertLessEqual(len(hints), MAX_HINTS_DISPLAYED)


# ---------------------------------------------------------------------------
# NPC-03: Context packet interface stability
# ---------------------------------------------------------------------------


class TestContextPacketInterface(unittest.TestCase):
    """_build_dialogue_context returns a dict with all required LLM keys."""

    @patch("world.models.CharacterQuest.objects")
    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_all_required_keys_present(self, mock_packet, mock_tier, mock_active, mock_cq):
        from world.dialogue_engine import _build_dialogue_context

        mock_packet.return_value = {
            "ancestry": "human",
            "primary_domain": "combat",
            "secondary_domain": "subterfuge",
            "guild": "ironblood",
            "subclass": "duskblade",
            "backend_level": 5,
            "reputation": 10.0,
            "network": 5.0,
            "bond": 0.0,
            "legacy": 0.0,
            "attunement": 0.0,
            "standing": 500,
            "trust": 0,
            "betrayal_flag": False,
            "zone_attunement": None,
            "companion_present": False,
            "companion_type": None,
            "companion_tier": None,
            "world_event_summary": None,
        }

        npc = MagicMock()
        npc.db.zone_id = "test_zone"
        npc.db.faction = "empire"
        char = MagicMock()

        context = _build_dialogue_context(npc, char)

        # NPC-03 regression guard: all keys the LLM will expect
        required_keys = {
            "ancestry", "reputation", "network", "bond", "legacy",
            "attunement", "standing", "trust", "betrayal_flag",
            "companion_present", "guild", "subclass",
            "standing_tier", "active_quests", "completed_quests",
            "failed_quests", "social_context",
        }
        missing = required_keys - set(context.keys())
        self.assertEqual(missing, set(), f"Missing context keys: {missing}")

    @patch("world.social_engine.query_social_context")
    @patch("world.models.CharacterQuest.objects")
    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_social_context_packet_from_social_web_kernel(
        self,
        mock_packet,
        mock_tier,
        mock_active,
        mock_cq,
        mock_social_context,
    ):
        """NPC-03 includes deterministic Social Web context for later LLM use."""
        from world.dialogue_engine import _build_dialogue_context

        social_packet = {
            "viewer": {"node_key": "npc:npc_greeter_maren"},
            "subject": {"node_key": "player:42"},
            "purpose": "dialogue",
            "facts": [],
            "claims": [],
        }
        mock_packet.return_value = {"reputation": 0}
        mock_social_context.return_value = social_packet

        npc = SimpleNamespace(
            db=SimpleNamespace(
                zone_id="test_zone",
                faction="empire",
                npc_id="npc_greeter_maren",
            ),
            key="Maren",
        )
        char = SimpleNamespace(id=42)

        context = _build_dialogue_context(npc, char)

        mock_social_context.assert_called_once_with(
            viewer_node_key="npc:npc_greeter_maren",
            subject_node_key="player:42",
            purpose="dialogue",
        )
        self.assertIs(context["social_context"], social_packet)

    @patch("world.social_engine.query_social_context")
    @patch("world.models.CharacterQuest.objects")
    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_missing_social_node_keys_fail_closed_to_empty_packet(
        self,
        mock_packet,
        mock_tier,
        mock_active,
        mock_cq,
        mock_social_context,
    ):
        """Missing NPC/player identifiers should not break existing dialogue."""
        from world.dialogue_engine import _build_dialogue_context

        mock_packet.return_value = {"reputation": 0}
        npc = SimpleNamespace(
            db=SimpleNamespace(zone_id="test_zone", faction="empire", npc_id=""),
            key="",
        )
        char = SimpleNamespace(id=None)

        context = _build_dialogue_context(npc, char)

        self.assertEqual(
            context["social_context"],
            {
                "viewer": {},
                "subject": {},
                "purpose": "dialogue",
                "facts": [],
                "claims": [],
            },
        )
        mock_social_context.assert_not_called()

    @patch("world.social_engine.query_social_context")
    @patch("world.models.CharacterQuest.objects")
    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_social_context_schema_unavailable_logs_and_fails_closed(
        self,
        mock_packet,
        mock_tier,
        mock_active,
        mock_cq,
        mock_social_context,
    ):
        """Dialogue stays available if Social Web schema/runtime is unavailable."""
        from django.db import OperationalError
        from world.dialogue_engine import _build_dialogue_context

        mock_packet.return_value = {"reputation": 0}
        mock_social_context.side_effect = OperationalError("no such table: world_socialnode")
        npc = SimpleNamespace(
            db=SimpleNamespace(
                zone_id="test_zone",
                faction="empire",
                npc_id="npc_greeter_maren",
            ),
            key="Maren",
        )
        char = SimpleNamespace(id=42)

        with self.assertLogs("world.dialogue_engine", level="WARNING") as logs:
            context = _build_dialogue_context(npc, char)

        self.assertEqual(
            context["social_context"],
            {
                "viewer": {},
                "subject": {},
                "purpose": "dialogue",
                "facts": [],
                "claims": [],
            },
        )
        self.assertIn("falling back", "\n".join(logs.output).lower())

    @patch("world.social_engine.query_social_context")
    @patch("world.models.CharacterQuest.objects")
    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_social_context_programming_errors_surface(
        self,
        mock_packet,
        mock_tier,
        mock_active,
        mock_cq,
        mock_social_context,
    ):
        """Programming errors in Social Web context building should not be masked."""
        from world.dialogue_engine import _build_dialogue_context

        mock_packet.return_value = {"reputation": 0}
        mock_social_context.side_effect = RuntimeError("programming mistake")
        npc = SimpleNamespace(
            db=SimpleNamespace(
                zone_id="test_zone",
                faction="empire",
                npc_id="npc_greeter_maren",
            ),
            key="Maren",
        )
        char = SimpleNamespace(id=42)

        with self.assertRaises(RuntimeError):
            _build_dialogue_context(npc, char)

    @patch("world.models.CharacterQuest.objects")
    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_standing_tier_added(self, mock_packet, mock_tier, mock_active, mock_cq):
        """Context includes standing_tier derived from get_standing_tier."""
        from world.dialogue_engine import _build_dialogue_context

        mock_packet.return_value = {"reputation": 0}

        npc = MagicMock()
        npc.db.zone_id = "test_zone"
        npc.db.faction = "empire"
        char = MagicMock()

        context = _build_dialogue_context(npc, char)
        self.assertEqual(context["standing_tier"], "neutral")

    @patch("world.models.CharacterQuest.objects")
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    @patch("world.quest_engine.get_active_quests")
    def test_quest_hints_from_active_quests(self, mock_active, mock_packet, mock_tier, mock_cq):
        """Quest state populated from quest_engine; active_quests contains quest IDs."""
        from world.dialogue_engine import _build_dialogue_context

        mock_packet.return_value = {}

        cq1 = MagicMock()
        cq1.quest_id = "wolves_hunt"
        mock_active.return_value = [cq1]

        npc = MagicMock()
        npc.db.zone_id = "test_zone"
        npc.db.faction = "empire"
        char = MagicMock()

        context = _build_dialogue_context(npc, char)
        self.assertIn("wolves_hunt", context["active_quests"])
        self.assertIn("completed_quests", context)
        self.assertIn("failed_quests", context)

    def test_context_hash_ignores_social_context(self):
        """Adding Social Web context must not churn KnownTopicRecord hashes yet."""
        from world.dialogue_engine import _compute_context_hash

        context = {
            "standing_tier": "friendly",
            "reputation": 10,
            "network": 5,
            "guild": "warcraft",
            "completed_quests": ["vc_q_warden_report"],
        }
        with_social_context = dict(
            context,
            social_context={
                "viewer": {"node_key": "npc:npc_greeter_maren"},
                "subject": {"node_key": "player:42"},
                "purpose": "dialogue",
                "facts": [{"fact_key": "fact:test"}],
                "claims": [],
            },
        )

        self.assertEqual(
            _compute_context_hash(context),
            _compute_context_hash(with_social_context),
        )


class TestContextPacketSocialWebIntegration(EvenniaTest):
    """Model-backed Social Web context reaches dialogue through the real query."""

    @patch("world.quest_engine.get_active_quests", return_value=[])
    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_build_dialogue_context_reads_model_backed_social_context(
        self,
        mock_packet,
        mock_tier,
        mock_active,
    ):
        from world.dialogue_engine import _build_dialogue_context
        from world.social_engine import (
            assert_social_claim,
            ensure_social_node,
            mark_known,
            record_social_fact,
        )

        mock_packet.return_value = {"reputation": 0, "network": 0}
        npc_identifier = f"npc_dialogue_context_{self.char1.id}"
        player = ensure_social_node(
            "player",
            str(self.char1.id),
            display_name=self.char1.key,
        )
        npc_node = ensure_social_node(
            "npc",
            npc_identifier,
            display_name="Warden Liaison",
            zone_id="ashreach_plains",
            settlement_id="ashreach_outpost",
            faction_id="wardens",
        )
        ok, message, fact = record_social_fact(
            fact_key=f"fact:dialogue_context:{self.char1.id}",
            subject_node_key=player.node_key,
            event_type="quest_completed",
            summary="The player delivered a sealed Warden report.",
            tags=["warden", "report"],
            visibility="institutional",
        )
        self.assertTrue(ok, message)
        ok, message, claim = assert_social_claim(
            claim_key=f"claim:dialogue_context:{self.char1.id}",
            speaker_node_key=npc_node.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="report",
            summary="The liaison says the player kept the Warden report sealed.",
            status="supported",
        )
        self.assertTrue(ok, message)
        ok, message, _knowledge = mark_known(
            node_key=npc_node.node_key,
            fact_key=fact.fact_key,
            claim_key=claim.claim_key,
            source_node_key=npc_node.node_key,
            channel="official_report",
            confidence=0.95,
        )
        self.assertTrue(ok, message)

        npc = SimpleNamespace(
            db=SimpleNamespace(
                zone_id="ashreach_plains",
                faction="wardens",
                npc_id=npc_identifier,
            ),
            key="Warden Liaison",
        )

        context = _build_dialogue_context(npc, self.char1)
        social_context = context["social_context"]

        self.assertEqual(social_context["viewer"]["node_key"], npc_node.node_key)
        self.assertEqual(social_context["subject"]["node_key"], player.node_key)
        self.assertEqual(social_context["purpose"], "dialogue")
        self.assertEqual(
            [item["fact_key"] for item in social_context["facts"]],
            [fact.fact_key],
        )
        self.assertEqual(
            [item["claim_key"] for item in social_context["claims"]],
            [claim.claim_key],
        )
