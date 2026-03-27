"""
Tests for the NPC dialogue system (Phase 06c).

Covers NPC-01 (context packet injection), NPC-02 (Standing-based responses),
NPC-03 (context packet interface stability), D-04 (dynamic hints),
D-05 (keyword extraction).

Uses unittest.TestCase with MagicMock for pure-logic functions and
EvenniaTest for model-backed operations (KnownTopicRecord).
"""

import unittest
from unittest.mock import MagicMock, patch

from evennia.utils.test_resources import EvenniaTest


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

    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_all_required_keys_present(self, mock_packet, mock_tier):
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
            "failed_quests",
        }
        missing = required_keys - set(context.keys())
        self.assertEqual(missing, set(), f"Missing context keys: {missing}")

    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_standing_tier_added(self, mock_packet, mock_tier):
        """Context includes standing_tier derived from get_standing_tier."""
        from world.dialogue_engine import _build_dialogue_context

        mock_packet.return_value = {"reputation": 0}

        npc = MagicMock()
        npc.db.zone_id = "test_zone"
        npc.db.faction = "empire"
        char = MagicMock()

        context = _build_dialogue_context(npc, char)
        self.assertEqual(context["standing_tier"], "neutral")

    @patch("world.dialogue_engine.get_standing_tier", return_value="neutral")
    @patch("world.world_state.get_character_context_packet")
    def test_quest_stubs_present(self, mock_packet, mock_tier):
        """Quest state stubs are empty lists until quest system is built."""
        from world.dialogue_engine import _build_dialogue_context

        mock_packet.return_value = {}

        npc = MagicMock()
        npc.db.zone_id = "test_zone"
        npc.db.faction = "empire"
        char = MagicMock()

        context = _build_dialogue_context(npc, char)
        self.assertEqual(context["active_quests"], [])
        self.assertEqual(context["completed_quests"], [])
        self.assertEqual(context["failed_quests"], [])
