"""
Tests for dialogue commands with a focus on the dual-purpose tell surface.
"""

import os
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django

django.setup()


class _MockDB:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class _MockNDB:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def _make_char(name, is_npc=False, sessions_count=1):
    char = MagicMock()
    char.key = name
    char.id = id(char)
    char.db = _MockDB(is_npc=is_npc)
    char.ndb = _MockNDB()
    char.location = MagicMock()
    char.location.contents = []
    sessions = MagicMock()
    sessions.count.return_value = sessions_count
    char.sessions = sessions
    return char


class TestCmdAsk(unittest.TestCase):
    def test_ask_about_me_uses_social_explanation_surface(self):
        from commands.cmd_dialogue import CmdAsk

        caller = _make_char("Caller")
        npc = MagicMock()
        npc.key = "Maren"
        npc.db.npc_name = "Maren"
        npc.db.npc_id = "npc_greeter_maren"
        npc.db.dialogue_topics = {"work": {"default": "Start with the tavern."}}

        resolved_context = {
            "standing_tier": "neutral",
            "social_context": {"facts": [], "claims": []},
        }
        with patch("commands.cmd_dialogue._find_npc_in_room", return_value=npc), patch(
            "world.dialogue_engine.is_social_explanation_topic",
            return_value=True,
        ) as mock_is_social_topic, patch(
            "world.dialogue_engine.resolve_social_explanation",
            return_value="I have heard enough to speak plainly with you.",
        ) as mock_social_explanation, patch(
            "world.dialogue_engine._build_dialogue_context",
            return_value=resolved_context,
        ) as mock_context, patch(
            "world.dialogue_engine.extract_topic"
        ) as mock_extract, patch(
            "world.dialogue_engine.resolve_topic_response"
        ) as mock_topic_response, patch(
            "world.dialogue_engine.record_topic_learned"
        ) as mock_record:
            cmd = CmdAsk()
            cmd.caller = caller
            cmd.args = "Maren about me"
            cmd.func()

        caller.msg.assert_called_once()
        self.assertIn("I have heard enough", caller.msg.call_args[0][0])
        mock_is_social_topic.assert_called_once_with("me")
        mock_context.assert_called_once_with(npc, caller)
        mock_social_explanation.assert_called_once_with(
            npc,
            caller,
            context=resolved_context,
            pending_offer=None,
        )
        mock_extract.assert_not_called()
        mock_topic_response.assert_not_called()
        mock_record.assert_not_called()

    def test_ask_multiword_npc_why_uses_social_explanation_surface(self):
        from commands.cmd_dialogue import CmdAsk

        caller = _make_char("Caller")
        npc = MagicMock()
        npc.key = "Agent Calloway"
        npc.db.npc_name = "Agent Calloway"
        npc.db.npc_id = "npc_warden_agent_calloway"
        npc.db.dialogue_topics = {"report": {"default": "Under seal."}}

        def find_npc(_character, name):
            return npc if name == "Agent Calloway" else None

        with patch("commands.cmd_dialogue._find_npc_in_room", side_effect=find_npc), patch(
            "world.dialogue_engine._build_dialogue_context",
            return_value={"social_context": {"facts": [], "claims": []}},
        ), patch(
            "world.dialogue_engine.resolve_social_explanation",
            return_value="The Wardens have reason to hear you out.",
        ), patch(
            "world.dialogue_engine.extract_topic"
        ) as mock_extract:
            cmd = CmdAsk()
            cmd.caller = caller
            cmd.args = "Agent Calloway why"
            cmd.func()

        self.assertIn("Wardens have reason", caller.msg.call_args[0][0])
        mock_extract.assert_not_called()

    def test_ask_why_specific_topic_stays_normal_topic_resolution(self):
        from commands.cmd_dialogue import CmdAsk

        caller = _make_char("Caller")
        npc = MagicMock()
        npc.key = "Maren"
        npc.db.npc_name = "Maren"
        npc.db.npc_id = "npc_greeter_maren"
        npc.db.dialogue_topics = {"wolves": {"default": "They hunt near the road."}}

        def find_npc(_character, name):
            return npc if name == "Maren" else None

        with patch("commands.cmd_dialogue._find_npc_in_room", side_effect=find_npc), patch(
            "world.dialogue_engine.extract_topic",
            return_value="wolves",
        ) as mock_extract, patch(
            "world.dialogue_engine.resolve_topic_response",
            return_value=("They hunt near the road.", "default"),
        ) as mock_topic_response, patch(
            "world.dialogue_engine._build_dialogue_context",
            return_value={"standing_tier": "neutral", "social_context": {}},
        ), patch(
            "world.dialogue_engine.resolve_social_explanation"
        ) as mock_social_explanation, patch(
            "world.dialogue_engine.record_topic_learned"
        ):
            cmd = CmdAsk()
            cmd.caller = caller
            cmd.args = "Maren why wolves"
            cmd.func()

        mock_extract.assert_called_once_with("why wolves", ["wolves"])
        mock_topic_response.assert_called_once()
        mock_social_explanation.assert_not_called()
        self.assertIn("They hunt near the road.", caller.msg.call_args[0][0])

    def test_ask_reuses_built_context_for_matched_topic(self):
        from commands.cmd_dialogue import CmdAsk

        caller = _make_char("Caller")
        npc = MagicMock()
        npc.key = "Maren"
        npc.db.npc_name = "Maren"
        npc.db.npc_id = "npc_greeter_maren"
        npc.db.dialogue_topics = {"work": {"default": "Start with the tavern."}}

        resolved_context = {"standing_tier": "neutral", "completed_quests": []}
        with patch("commands.cmd_dialogue._find_npc_in_room", return_value=npc), patch(
            "world.dialogue_engine.extract_topic",
            return_value="work",
        ), patch(
            "world.dialogue_engine.resolve_topic_response",
            return_value=("Start with the tavern.", "default"),
        ) as mock_resolve, patch(
            "world.dialogue_engine._build_dialogue_context",
            return_value=resolved_context,
        ) as mock_context, patch(
            "world.dialogue_engine.record_topic_learned"
        ) as mock_record:
            cmd = CmdAsk()
            cmd.caller = caller
            cmd.args = "Maren about work"
            cmd.func()

        caller.msg.assert_called_once()
        self.assertIn("Start with the tavern.", caller.msg.call_args[0][0])
        mock_context.assert_called_once_with(npc, caller)
        mock_resolve.assert_called_once_with(
            npc,
            caller,
            "work",
            context=resolved_context,
        )
        mock_record.assert_called_once_with(
            caller,
            "npc_greeter_maren",
            "work",
            resolved_context,
        )
        self.assertIs(mock_resolve.call_args.kwargs["context"], resolved_context)
        self.assertIs(mock_record.call_args.args[3], resolved_context)


class TestCmdSay(unittest.TestCase):
    def test_say_reuses_built_context_for_matched_npc_topic(self):
        from commands.cmd_dialogue import CmdSay

        caller = _make_char("Caller")
        npc = MagicMock()
        npc.key = "Maren"
        npc.db.is_npc = True
        npc.db.npc_name = "Maren"
        npc.db.npc_id = "npc_greeter_maren"
        npc.db.dialogue_topics = {"work": {"default": "Start with the tavern."}}
        caller.location.contents = [npc]

        resolved_context = {"standing_tier": "neutral", "completed_quests": []}
        with patch(
            "world.dialogue_engine.get_standing_tier",
            return_value="neutral",
        ), patch(
            "world.dialogue_engine.extract_topic",
            return_value="work",
        ), patch(
            "world.dialogue_engine.resolve_topic_response",
            return_value=("Start with the tavern.", "default"),
        ) as mock_resolve, patch(
            "world.dialogue_engine._build_dialogue_context",
            return_value=resolved_context,
        ) as mock_context, patch(
            "world.dialogue_engine.record_topic_learned"
        ) as mock_record:
            cmd = CmdSay()
            cmd.caller = caller
            cmd.args = "I need work."
            cmd.func()

        caller.location.msg_contents.assert_called_once_with(
            'Caller says, "I need work."',
            exclude=[caller],
        )
        self.assertEqual(caller.msg.call_count, 2)
        self.assertIn("Start with the tavern.", caller.msg.call_args_list[1][0][0])
        mock_context.assert_called_once_with(npc, caller)
        mock_resolve.assert_called_once_with(
            npc,
            caller,
            "work",
            context=resolved_context,
        )
        mock_record.assert_called_once_with(
            caller,
            "npc_greeter_maren",
            "work",
            resolved_context,
        )
        self.assertIs(mock_resolve.call_args.kwargs["context"], resolved_context)
        self.assertIs(mock_record.call_args.args[3], resolved_context)


class TestCmdTell(unittest.TestCase):
    def test_tell_delivers_private_message_to_online_player(self):
        from commands.cmd_dialogue import CmdTell

        caller = _make_char("Caller")
        target = _make_char("Arden")
        session = MagicMock()
        session.get_puppet.return_value = target

        with patch(
            "commands.cmd_dialogue.evennia.SESSION_HANDLER.get_sessions",
            return_value=[session],
        ):
            cmd = CmdTell()
            cmd.caller = caller
            cmd.args = "Arden Meet me at the gate."
            cmd.func()

        caller.msg.assert_called_once()
        caller_msg = caller.msg.call_args[0][0]
        self.assertIn('You tell Arden, "Meet me at the gate."', caller_msg)
        target.msg.assert_called_once_with(
            '|mCaller tells you, "Meet me at the gate."|n'
        )

    def test_tell_still_uses_npc_dialogue_when_target_is_present(self):
        from commands.cmd_dialogue import CmdTell

        caller = _make_char("Caller")
        npc = MagicMock()
        npc.key = "Maren"
        npc.db.npc_name = "Maren"
        npc.db.npc_id = "npc_greeter_maren"
        npc.db.dialogue_topics = {"work": {"default": "Start with the tavern."}}

        resolved_context = {"standing_tier": "neutral", "completed_quests": []}
        with patch("commands.cmd_dialogue._find_npc_in_room", return_value=npc), patch(
            "world.dialogue_engine.extract_topic",
            return_value="work",
        ), patch(
            "world.dialogue_engine.resolve_topic_response",
            return_value=("Start with the tavern.", "default"),
        ) as mock_resolve, patch(
            "world.dialogue_engine._build_dialogue_context",
            return_value=resolved_context,
        ) as mock_context, patch(
            "world.dialogue_engine.record_topic_learned"
        ) as mock_record:
            cmd = CmdTell()
            cmd.caller = caller
            cmd.args = "Maren I need work."
            cmd.func()

        first_msg = caller.msg.call_args_list[0][0][0]
        second_msg = caller.msg.call_args_list[1][0][0]
        self.assertIn('You tell Maren, "I need work."', first_msg)
        self.assertIn("Start with the tavern.", second_msg)
        mock_context.assert_called_once_with(npc, caller)
        mock_resolve.assert_called_once_with(
            npc,
            caller,
            "work",
            context=resolved_context,
        )
        mock_record.assert_called_once_with(
            caller,
            "npc_greeter_maren",
            "work",
            resolved_context,
        )
