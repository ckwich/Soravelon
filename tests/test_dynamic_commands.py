import unittest
import sys
import types
from contextlib import contextmanager
from unittest.mock import MagicMock, patch


def _dynamic_command_class():
    try:
        from commands.cmd_dynamic import DynamicAreaCommand
        return DynamicAreaCommand
    except ModuleNotFoundError as exc:
        if exc.name != "evennia":
            raise

    evennia = types.ModuleType("evennia")
    evennia_commands = types.ModuleType("evennia.commands")
    evennia_command = types.ModuleType("evennia.commands.command")
    evennia_cmdset = types.ModuleType("evennia.commands.cmdset")

    class BaseCommand:
        pass

    class CmdSet:
        def __init__(self):
            self.commands = []

        def add(self, command):
            self.commands.append(command)

    evennia_command.Command = BaseCommand
    evennia_cmdset.CmdSet = CmdSet

    modules = {
        "evennia": evennia,
        "evennia.commands": evennia_commands,
        "evennia.commands.command": evennia_command,
        "evennia.commands.cmdset": evennia_cmdset,
    }
    with patch.dict(sys.modules, modules):
        sys.modules.pop("commands.command", None)
        sys.modules.pop("commands.cmd_dynamic", None)
        from commands.cmd_dynamic import DynamicAreaCommand
        return DynamicAreaCommand


@contextmanager
def _practice_dependencies():
    import world

    skill_engine = types.ModuleType("world.skill_engine")
    skill_engine.accumulate_skill_use = MagicMock()
    world_state = types.ModuleType("world.world_state")
    world_state.accumulate_domain_xp = MagicMock()
    quest_engine = types.ModuleType("world.quest_engine")
    quest_engine.check_practice_objectives = MagicMock()

    modules = {
        "world.skill_engine": skill_engine,
        "world.world_state": world_state,
        "world.quest_engine": quest_engine,
    }
    old_attrs = {
        name: getattr(world, name, None)
        for name in ("skill_engine", "world_state", "quest_engine")
    }
    try:
        with patch.dict(sys.modules, modules):
            world.skill_engine = skill_engine
            world.world_state = world_state
            world.quest_engine = quest_engine
            yield skill_engine, world_state, quest_engine
    finally:
        for name, value in old_attrs.items():
            if value is None:
                try:
                    delattr(world, name)
                except AttributeError:
                    pass
            else:
                setattr(world, name, value)


class TestDynamicAreaCommand(unittest.TestCase):
    def test_passes_player_args_to_action_context(self):
        DynamicAreaCommand = _dynamic_command_class()

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

    def test_grant_practice_dynamic_command_repeat_awards_once(self):
        DynamicAreaCommand = _dynamic_command_class()

        command = DynamicAreaCommand()
        command.caller = MagicMock()
        command.caller.location = MagicMock()
        command.caller.db.practice_opportunities_completed = []
        command.args = "road marker"
        command.action_dict = {
            "action_type": "grant_practice",
            "opportunity_id": "road_marker_survey",
            "verb": "survey",
            "target": "road marker",
            "skill_awards": {"navigation": 3},
            "domain_awards": {"tactics": 75},
            "success_text": "You fix the route in memory.",
            "once_per_character": True,
        }

        with _practice_dependencies() as deps:
            skill_engine, world_state, _quest_engine = deps
            command.func()
            command.func()

        skill_engine.accumulate_skill_use.assert_called_once_with(command.caller, "navigation", 3)
        world_state.accumulate_domain_xp.assert_called_once_with(command.caller, "tactics", 75)
        command.caller.msg.assert_any_call("You have already learned what you can from that.")
