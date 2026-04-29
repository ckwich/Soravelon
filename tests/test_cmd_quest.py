"""Direct command coverage for quest display and abandonment flows."""

import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django
django.setup()


def _make_character():
    character = MagicMock()
    character.msg = MagicMock()
    return character


def _make_active_quest(quest_id, progress=None):
    return SimpleNamespace(quest_id=quest_id, progress=progress or {})


class TestCmdQuest(unittest.TestCase):
    """Behavior-focused coverage for CmdQuest."""

    def _make_cmd(self, character, args=""):
        from commands.cmd_quest import CmdQuest

        cmd = CmdQuest()
        cmd.caller = character
        cmd.args = args
        return cmd

    @patch("world.quest_engine.get_active_quests", return_value=[])
    def test_quest_lists_no_active_quests_cleanly(self, _mock_get_active_quests):
        character = _make_character()
        cmd = self._make_cmd(character)

        cmd.func()

        self.assertIn("no active quests", character.msg.call_args[0][0].lower())

    @patch("world.quest_engine._normalize_quest_spec", side_effect=lambda spec: spec)
    @patch("world.quest_engine._get_quest_spec", return_value={
        "name": "Roadwarden's Request",
        "quest_giver": "npc_roadwarden_talia",
        "objectives": [
            {"type": "deliver", "target": "sealed_satchel", "count": 1},
            {"type": "kill", "target": "road_wolf", "count": 2},
        ],
    })
    @patch("world.quest_engine.get_active_quests", return_value=[
        _make_active_quest(
            "roadwardens_request",
            progress={"deliver_sealed_satchel": 1, "kill_road_wolf": 1},
        )
    ])
    def test_quest_lists_progress_and_giver(
        self,
        _mock_get_active_quests,
        _mock_get_spec,
        _mock_normalize,
    ):
        character = _make_character()
        cmd = self._make_cmd(character)

        cmd.func()

        message = character.msg.call_args[0][0]
        self.assertIn("Roadwarden's Request", message)
        self.assertIn("Roadwarden Talia", message)
        self.assertIn("66%", message)

    @patch("world.quest_engine._normalize_quest_spec", side_effect=lambda spec: spec)
    @patch("world.quest_engine._get_quest_spec", return_value={
        "name": "Roadwarden's Request",
        "description": "Carry the satchel and thin the wolves stalking the road.",
        "quest_giver": "npc_roadwarden_talia",
        "objectives": [
            {
                "type": "deliver",
                "target": "sealed_satchel",
                "count": 1,
                "description": "Deliver the sealed satchel to the north watch.",
            },
            {
                "type": "kill",
                "target": "road_wolf",
                "count": 2,
                "description": "Cull the wolves prowling the road.",
            },
        ],
        "rewards": [
            {"action_type": "give_scales", "amount": 18},
            {"action_type": "give_skill_xp", "skill_id": "tracking", "count": 2},
        ],
    })
    @patch("world.quest_engine.get_active_quests", return_value=[
        _make_active_quest(
            "roadwardens_request",
            progress={"deliver_sealed_satchel": 1, "kill_road_wolf": 1},
        )
    ])
    def test_quest_detail_shows_objectives_and_rewards(
        self,
        _mock_get_active_quests,
        _mock_get_spec,
        _mock_normalize,
    ):
        character = _make_character()
        cmd = self._make_cmd(character, "roadwarden")

        cmd.func()

        message = character.msg.call_args[0][0]
        self.assertIn("Carry the satchel", message)
        self.assertIn("[DONE]", message)
        self.assertIn("[1/2]", message)
        self.assertIn("18 Scales", message)
        self.assertIn("+2 Tracking XP", message)

    @patch("world.quest_engine._normalize_quest_spec", side_effect=lambda spec: spec)
    @patch("world.quest_engine._get_quest_spec", return_value={
        "name": "The Jammed Winch",
        "description": "Help the canal crew understand why the old mechanism keeps slipping.",
        "quest_giver": "npc_canal_foreman",
        "objectives": [
            {
                "type": "practice",
                "target": "vp_canal_winch_repair",
                "count": 1,
                "description": "Repair the canal winch in the north service bay.",
            },
        ],
        "rewards": [
            {
                "action_type": "grant_practice",
                "skill_awards": {"engineering": 4},
                "domain_awards": {"engineering": 120},
            },
        ],
    })
    @patch("world.quest_engine.get_active_quests", return_value=[
        _make_active_quest("jammed_winch", progress={})
    ])
    def test_quest_detail_shows_practice_rewards_without_xp_numbers(
        self,
        _mock_get_active_quests,
        _mock_get_spec,
        _mock_normalize,
    ):
        character = _make_character()
        cmd = self._make_cmd(character, "winch")

        cmd.func()

        message = character.msg.call_args[0][0]
        self.assertIn("Repair the canal winch", message)
        self.assertIn("Meaningful practice", message)
        self.assertNotIn("XP", message)

    @patch("world.quest_engine.abandon_quest", return_value=(True, "You abandon the job."))
    @patch("world.quest_engine._normalize_quest_spec", side_effect=lambda spec: spec)
    @patch("world.quest_engine._get_quest_spec", return_value={
        "name": "Roadwarden's Request",
        "quest_giver": "npc_roadwarden_talia",
    })
    @patch("world.quest_engine.get_active_quests", return_value=[
        _make_active_quest("roadwardens_request")
    ])
    def test_quest_abandon_matches_partial_name_and_calls_engine(
        self,
        _mock_get_active_quests,
        _mock_get_spec,
        _mock_normalize,
        mock_abandon_quest,
    ):
        character = _make_character()
        cmd = self._make_cmd(character, "abandon roadwarden")

        cmd.func()

        mock_abandon_quest.assert_called_once_with(character, "roadwardens_request")
        self.assertIn("|yYou abandon the job.|n", character.msg.call_args[0][0])
