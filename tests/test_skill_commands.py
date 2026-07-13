"""Player-facing skill detail truthfulness contracts."""

import unittest
from unittest.mock import MagicMock, patch


class TestSkillDetailAvailability(unittest.TestCase):
    def _render_detail(self, query):
        from commands.skill_commands import CmdSkills

        caller = MagicMock()
        command = CmdSkills()
        command.caller = caller
        command.args = query
        with patch("world.skill_engine.get_skill_value", return_value=20):
            command.func()
        return caller.msg.call_args.args[0]

    def test_planned_skill_marks_behavior_and_thresholds_as_not_live(self):
        message = self._render_detail("tracking")

        self.assertIn("Status:|n Planned", message)
        self.assertIn("not live", message.lower())
        self.assertIn("Design targets", message)

    def test_companion_skill_names_the_missing_ownership_loop(self):
        message = self._render_detail("beast training")

        self.assertIn("Status:|n Planned", message)
        self.assertIn("companion ownership", message.lower())

    def test_live_skill_is_labeled_live(self):
        message = self._render_detail("appraisal")

        self.assertIn("Status:|n Live", message)
        self.assertNotIn("Design targets", message)
