import os
import unittest
from unittest.mock import MagicMock, patch


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django
django.setup()


class TestCmdSocialMemory(unittest.TestCase):
    """socialmemory is a locked admin inspection command."""

    def _run_command(self, args, context=None):
        from commands.cmd_socialmemory import CmdSocialMemory

        caller = MagicMock()
        cmd = CmdSocialMemory()
        cmd.caller = caller
        cmd.args = args

        if context is None:
            cmd.func()
        else:
            with patch(
                "world.social_engine.query_social_context",
                return_value=context,
            ) as mock_query:
                cmd.func()
                return caller, mock_query
        return caller

    def test_command_contract(self):
        from commands.cmd_socialmemory import CmdSocialMemory

        cmd = CmdSocialMemory()

        self.assertEqual(cmd.key, "socialmemory")
        self.assertEqual(cmd.aliases, ["socialweb"])
        self.assertEqual(cmd.locks, "cmd:perm(Builders)")
        self.assertEqual(cmd.help_category, "admin")

    def test_command_reports_usage_without_two_node_keys(self):
        for args in ("", "npc:npc_warden_outpost_commander", "a b c"):
            with self.subTest(args=args):
                caller = self._run_command(args)

                output = caller.msg.call_args[0][0]
                self.assertIn(
                    "Usage: socialmemory <viewer_node_key> <subject_node_key>",
                    output,
                )

    def test_command_queries_admin_context_for_two_node_keys(self):
        context = {
            "facts": [
                {
                    "fact_key": "fact:calloway:player:report",
                    "summary": "The player delivered the Warden report.",
                }
            ],
            "claims": [
                {
                    "claim_key": "claim:calloway:player:report",
                    "status": "supported",
                    "summary": (
                        "Calloway says the player carried Warden business "
                        "cleanly."
                    ),
                    "trace": [
                        {
                            "edge_type": "warden_report",
                            "summary": "Official Warden report carried the claim.",
                        }
                    ],
                }
            ],
        }

        caller, mock_query = self._run_command(
            "npc:npc_warden_outpost_commander player:1",
            context=context,
        )

        mock_query.assert_called_once_with(
            viewer_node_key="npc:npc_warden_outpost_commander",
            subject_node_key="player:1",
            purpose="admin",
        )
        output = caller.msg.call_args[0][0]
        self.assertIn("Social Context", output)
        self.assertIn("viewer: npc:npc_warden_outpost_commander", output)
        self.assertIn("subject: player:1", output)
        self.assertIn("facts: 1", output)
        self.assertIn("claims: 1", output)
        self.assertIn("claim:calloway:player:report [supported]", output)
        self.assertIn(
            "Calloway says the player carried Warden business cleanly.",
            output,
        )
        self.assertIn("via warden_report", output)
        self.assertIn("Official Warden report carried the claim.", output)

    def test_command_formats_direct_trace_when_edge_type_is_missing(self):
        context = {
            "facts": [],
            "claims": [
                {
                    "claim_key": "claim:direct",
                    "status": "unverified",
                    "summary": "A direct note exists.",
                    "trace": [
                        {
                            "edge_type": "",
                            "summary": "Directly known by the viewer.",
                        }
                    ],
                }
            ],
        }

        caller, _mock_query = self._run_command(
            "npc:viewer player:1",
            context=context,
        )

        output = caller.msg.call_args[0][0]
        self.assertIn("via direct: Directly known by the viewer.", output)

    def test_character_cmdset_registers_socialmemory_after_social_commands(self):
        from commands import default_cmdsets

        added_commands = []

        with patch.object(
            default_cmdsets.default_cmds.CharacterCmdSet,
            "at_cmdset_creation",
            return_value=None,
        ):
            cmdset = default_cmdsets.CharacterCmdSet()
            cmdset.add = added_commands.append
            cmdset.at_cmdset_creation()

        command_keys = [cmd.key for cmd in added_commands]
        self.assertIn("socialmemory", command_keys)
        self.assertLess(
            command_keys.index("whisper"),
            command_keys.index("socialmemory"),
        )
        self.assertLess(
            command_keys.index("socialmemory"),
            command_keys.index("inspect"),
        )
