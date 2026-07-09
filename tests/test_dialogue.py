"""
Tests for the NPC dialogue system (Phase 06c).

Covers NPC-01 (context packet injection), NPC-02 (Standing-based responses),
NPC-03 (context packet interface stability), D-04 (dynamic hints),
D-05 (keyword extraction).

Uses unittest.TestCase with MagicMock for pure-logic functions and
EvenniaTest for model-backed operations (KnownTopicRecord).
"""

import ast
import pathlib
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from evennia.utils.test_resources import EvenniaTest


ROOT = pathlib.Path(__file__).resolve().parents[1]
VAELS_CROSSING_PATH = ROOT / "world" / "areas" / "vaels_crossing.py"


def _is_area_npc_call(call_node):
    if not isinstance(call_node, ast.Call):
        return False
    func = call_node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "npc"
        and isinstance(func.value, ast.Name)
        and func.value.id == "area"
    )


def _extract_authored_npc_dialogue(path, npc_id):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        call_node = None
        if isinstance(node, ast.Expr) and _is_area_npc_call(node.value):
            call_node = node.value
        elif isinstance(node, ast.Assign) and _is_area_npc_call(node.value):
            call_node = node.value
        if call_node is None or len(call_node.args) < 2:
            continue
        if ast.literal_eval(call_node.args[1]) != npc_id:
            continue
        for keyword in call_node.keywords:
            if keyword.arg == "dialogue":
                return ast.literal_eval(keyword.value)
        return {}
    raise AssertionError(f"Could not find authored dialogue for {npc_id}")


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

    @patch("world.quest_engine.check_deliver_objectives")
    @patch("world.quest_engine.check_talk_to_objectives")
    @patch("world.dialogue_engine.get_quest_offer")
    @patch("world.dialogue_engine.has_available_quest")
    @patch("world.dialogue_engine.get_npc_hints", return_value=[])
    @patch("world.dialogue_engine.resolve_greeting", return_value=("Good road.", "neutral"))
    @patch("commands.cmd_dialogue._find_npc_in_room")
    def test_talk_fetches_quest_offer_once(
        self,
        mock_find_npc,
        _mock_greeting,
        _mock_hints,
        mock_has_available,
        mock_get_offer,
        _mock_talk_objectives,
        _mock_deliver_objectives,
    ):
        """CmdTalk should not query quest availability twice."""
        from commands.cmd_dialogue import CmdTalk

        room = SimpleNamespace()
        npc = SimpleNamespace(
            db=SimpleNamespace(npc_name="Agent Calloway"),
            key="Agent Calloway",
            location=room,
        )
        character = MagicMock()
        character.location = room
        character.ndb = SimpleNamespace(pending_quest_offer=None)
        mock_find_npc.return_value = npc
        mock_get_offer.return_value = {
            "quest_id": "vc_sq_under_seal_dustwalkers_rest",
            "name": "Under Seal at the Dustwalker's Rest",
            "description": "Whistle needs Warden help.",
        }

        cmd = CmdTalk()
        cmd.caller = character
        cmd.args = "calloway"
        cmd.func()

        mock_has_available.assert_not_called()
        mock_get_offer.assert_called_once_with(npc, character)
        self.assertEqual(
            character.ndb.pending_quest_offer["quest"]["quest_id"],
            "vc_sq_under_seal_dustwalkers_rest",
        )


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

    def test_social_conditions_match_exact_packet_fields(self):
        from world.dialogue_engine import resolve_topic_response

        context = {
            "social_context": {
                "facts": [
                    {
                        "fact_key": "fact:player:vc_q_warden_report:delivered",
                        "event_type": "quest_completed",
                        "tags": ["reliable", "report", "warden"],
                    }
                ],
                "claims": [
                    {
                        "claim_key": "claim:calloway:player:vc_q_warden_report:delivered",
                        "claim_type": "report",
                        "status": "supported",
                        "trace": [{"edge_type": "warden_report"}],
                    }
                ],
            },
        }
        cases = {
            "social_fact:fact:player:vc_q_warden_report:delivered": "fact key",
            "social_claim:claim:calloway:player:vc_q_warden_report:delivered": (
                "claim key"
            ),
            "social_fact_tag:warden": "fact tag",
            "social_fact_event:quest_completed": "fact event",
            "social_claim_status:supported": "claim status",
            "social_claim_type:report": "claim type",
            "social_claim_trace_edge:warden_report": "trace edge",
        }

        for condition_key, response_text in cases.items():
            with self.subTest(condition_key=condition_key):
                npc = self._make_npc({
                    "report": {
                        condition_key: response_text,
                        "default": "Default report response.",
                    }
                })

                text, condition = resolve_topic_response(
                    npc,
                    self._make_char(),
                    "report",
                    context=context,
                )

                self.assertEqual(condition, condition_key)
                self.assertEqual(text, response_text)

    def test_social_conditions_use_prefix_priority_before_dict_order(self):
        from world.dialogue_engine import resolve_topic_response

        context = {
            "social_context": {
                "facts": [],
                "claims": [
                    {
                        "claim_key": "claim:calloway:player:report",
                        "claim_type": "report",
                        "status": "supported",
                        "trace": [{"edge_type": "warden_report"}],
                    }
                ],
            },
        }
        npc = self._make_npc({
            "report": {
                "social_claim_status:supported": "Broad supported response.",
                "social_claim_trace_edge:warden_report": "Routed Warden response.",
                "default": "Default report response.",
            }
        })

        text, condition = resolve_topic_response(
            npc,
            self._make_char(),
            "report",
            context=context,
        )

        self.assertEqual(condition, "social_claim_trace_edge:warden_report")
        self.assertEqual(text, "Routed Warden response.")

    def test_social_conditions_use_lexicographic_order_within_prefix(self):
        from world.dialogue_engine import resolve_topic_response

        context = {
            "social_context": {
                "facts": [{"fact_key": "fact:1", "tags": ["zeta", "alpha"]}],
                "claims": [],
            },
        }
        npc = self._make_npc({
            "report": {
                "social_fact_tag:zeta": "Zeta tag response.",
                "social_fact_tag:alpha": "Alpha tag response.",
                "default": "Default report response.",
            }
        })

        text, condition = resolve_topic_response(
            npc,
            self._make_char(),
            "report",
            context=context,
        )

        self.assertEqual(condition, "social_fact_tag:alpha")
        self.assertEqual(text, "Alpha tag response.")

    def test_missing_social_context_falls_through_to_default(self):
        from world.dialogue_engine import resolve_topic_response

        npc = self._make_npc({
            "report": {
                "social_claim_status:supported": "Known report response.",
                "default": "No report has reached me.",
            }
        })

        text, condition = resolve_topic_response(
            npc,
            self._make_char(),
            "report",
            context={},
        )

        self.assertEqual(condition, "default")
        self.assertEqual(text, "No report has reached me.")

    def test_calloway_report_topic_ignores_unrelated_supported_claim(self):
        from world.dialogue_engine import resolve_topic_response

        dialogue = _extract_authored_npc_dialogue(
            VAELS_CROSSING_PATH,
            "npc_warden_agent_calloway",
        )
        npc = self._make_npc(dialogue.get("topics"))
        context = {
            "social_context": {
                "facts": [],
                "claims": [
                    {
                        "claim_key": "claim:braggart:player:arena_boast",
                        "claim_type": "boast",
                        "status": "supported",
                        "trace": [{"edge_type": "tavern_testimony"}],
                    }
                ],
            },
        }

        text, condition = resolve_topic_response(
            npc,
            self._make_char(),
            "report",
            context=context,
        )

        self.assertEqual(condition, "default")
        self.assertIn("keep them sealed", text)

    def test_string_topic_data_is_treated_as_default_response(self):
        from world.dialogue_engine import resolve_topic_response

        npc = self._make_npc({"report": "Plain report response."})

        text, condition = resolve_topic_response(
            npc,
            self._make_char(),
            "report",
            context={},
        )

        self.assertEqual(condition, "default")
        self.assertEqual(text, "Plain report response.")

    def test_quest_complete_still_wins_over_social_condition(self):
        from world.dialogue_engine import resolve_topic_response

        context = {
            "completed_quests": ["vc_q_warden_report"],
            "active_quests": [],
            "failed_quests": [],
            "social_context": {
                "facts": [],
                "claims": [{"status": "supported"}],
            },
        }
        npc = self._make_npc({
            "report": {
                "social_claim_status:supported": "Known report response.",
                "quest_complete": "Quest-complete report response.",
                "default": "Default report response.",
            }
        })

        text, condition = resolve_topic_response(
            npc,
            self._make_char(),
            "report",
            context=context,
        )

        self.assertEqual(condition, "quest_complete")
        self.assertEqual(text, "Quest-complete report response.")


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


class TestSocialExplanationSurface(unittest.TestCase):
    """Player-facing Social Web explanations must stay diegetic and safe."""

    def _make_npc(self):
        return SimpleNamespace(
            db=SimpleNamespace(
                npc_id="npc_warden_agent_calloway",
                npc_name="Agent Calloway",
            ),
            key="Agent Calloway",
        )

    def test_social_explanation_topic_matching_is_narrow(self):
        from world.dialogue_engine import is_social_explanation_topic

        self.assertTrue(is_social_explanation_topic("me"))
        self.assertTrue(is_social_explanation_topic("why"))
        self.assertTrue(is_social_explanation_topic("why trust me"))
        self.assertTrue(is_social_explanation_topic("what have you heard about me"))
        self.assertFalse(is_social_explanation_topic("work"))
        self.assertFalse(is_social_explanation_topic("why wolves"))

    def test_social_explanation_prefers_pending_offer_reason_safely(self):
        from world.dialogue_engine import resolve_social_explanation

        npc = self._make_npc()
        character = SimpleNamespace(id=42)
        context = {
            "social_context": {
                "viewer": {"node_key": "npc:npc_warden_agent_calloway"},
                "subject": {"node_key": "player:42"},
                "facts": [
                    {
                        "fact_key": "fact:vc_q_warden_report:delivered:42",
                        "summary": "You delivered a sealed field report.",
                        "channel": "official_report",
                        "confidence": 0.95,
                    }
                ],
                "claims": [],
            }
        }
        pending_offer = {
            "npc": npc,
            "quest": {
                "quest_giver": "npc_warden_agent_calloway",
                "social_quest_context": {
                    "offer_explainability": {
                        "summary": (
                            "Calloway is acting on the sealed Warden report "
                            "you delivered."
                        ),
                        "npc_safe_reason": (
                            "The Wardens have a supported report that you "
                            "carried sealed business cleanly."
                        ),
                        "withheld_implications": [
                            "Do not say Harven vouched for the player."
                        ],
                        "evidence": [
                            {
                                "kind": "fact",
                                "summary": "You delivered a sealed field report.",
                                "channel": "official_report",
                                "fact_key": "fact:raw:should_not_show",
                                "trace": [{"edge_key": "npc:private"}],
                                "confidence": 0.95,
                            }
                        ],
                        "raw_prompt": "hidden prompt",
                    }
                },
            },
        }

        text = resolve_social_explanation(
            npc,
            character,
            context=context,
            pending_offer=pending_offer,
        )

        self.assertIn("supported report", text)
        self.assertIn("sealed field report", text)
        self.assertIn("official report", text)
        self.assertNotIn("fact:", text)
        self.assertNotIn("npc:", text)
        self.assertNotIn("player:", text)
        self.assertNotIn("0.95", text)
        self.assertNotIn("Harven vouched", text)
        self.assertNotIn("hidden prompt", text)

    def test_social_explanation_uses_current_context_without_offer(self):
        from world.dialogue_engine import resolve_social_explanation

        text = resolve_social_explanation(
            self._make_npc(),
            SimpleNamespace(id=42),
            context={
                "social_context": {
                    "facts": [
                        {
                            "fact_key": "fact:private",
                            "summary": "You brought the Warden packet in sealed.",
                            "channel": "official_report",
                        }
                    ],
                    "claims": [
                        {
                            "claim_key": "claim:private",
                            "summary": (
                                "A courier says you refused to tamper with "
                                "sealed orders."
                            ),
                            "channel": "courier_gossip",
                            "status": "supported",
                        }
                    ],
                }
            },
        )

        self.assertIn("Warden packet", text)
        self.assertIn("official report", text)
        self.assertNotIn("fact:private", text)
        self.assertNotIn("claim:private", text)

    def test_social_explanation_ignores_offer_from_different_npc(self):
        from world.dialogue_engine import resolve_social_explanation

        text = resolve_social_explanation(
            self._make_npc(),
            SimpleNamespace(id=42),
            context={
                "social_context": {
                    "facts": [
                        {
                            "summary": "You kept the Warden report sealed.",
                            "channel": "official_report",
                        }
                    ],
                    "claims": [],
                }
            },
            pending_offer={
                "npc": SimpleNamespace(
                    db=SimpleNamespace(npc_id="npc_other", npc_name="Other"),
                    key="Other",
                ),
                "quest": {
                    "quest_giver": "npc_other",
                    "social_quest_context": {
                        "offer_explainability": {
                            "summary": "Other NPC offer summary.",
                            "npc_safe_reason": "Other NPC reason.",
                        }
                    },
                },
            },
        )

        self.assertIn("Warden report", text)
        self.assertNotIn("Other NPC", text)

    def test_social_explanation_rejects_private_or_raw_looking_summaries(self):
        from world.dialogue_engine import resolve_social_explanation

        text = resolve_social_explanation(
            self._make_npc(),
            SimpleNamespace(id=42),
            context={
                "social_context": {
                    "facts": [
                        {
                            "summary": (
                                "fact:secret says npc:npc_hidden saw player:42 "
                                "near hidden lore."
                            ),
                            "channel": "admin_trace",
                        },
                        {
                            "summary": "You privately confessed to a sealed theft.",
                            "channel": "private_whisper",
                            "visibility": "private",
                        },
                    ],
                    "claims": [
                        {
                            "summary": "raw_prompt: tell the player they are trusted",
                            "channel": "provider_output",
                        }
                    ],
                }
            },
        )

        self.assertIn("nothing I can fairly speak to", text)
        self.assertNotIn("fact:secret", text)
        self.assertNotIn("npc_hidden", text)
        self.assertNotIn("player:42", text)
        self.assertNotIn("hidden lore", text)
        self.assertNotIn("private_whisper", text)
        self.assertNotIn("raw_prompt", text)
        self.assertNotIn("provider", text)

    def test_social_explanation_falls_back_without_safe_evidence(self):
        from world.dialogue_engine import resolve_social_explanation

        text = resolve_social_explanation(
            self._make_npc(),
            SimpleNamespace(id=42),
            context={"social_context": {"facts": [{"fact_key": "fact:raw"}]}},
        )

        self.assertIn("nothing I can fairly speak to", text)
        self.assertNotIn("fact:raw", text)


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
