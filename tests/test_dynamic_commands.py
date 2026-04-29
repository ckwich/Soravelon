import unittest
from unittest.mock import MagicMock, patch


class TestDynamicAreaCommand(unittest.TestCase):
    def test_passes_player_args_to_action_context(self):
        from commands.cmd_dynamic import DynamicAreaCommand

        command = DynamicAreaCommand()
        command.caller = MagicMock()
        command.caller.location = MagicMock()
        command.args = "canal winch"
        command.action_dict = {
            "action_type": "grant_practice",
            "opportunity_id": "workshop_winch_repair",
        }

        with patch("world.action_vocabulary.execute_action", return_value=(True, "")) as mock_execute:
            command.func()

        mock_execute.assert_called_once()
        _action, context = mock_execute.call_args[0]
        self.assertEqual(context["args"], "canal winch")
