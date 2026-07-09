"""Public command routing for Soravelon's inventory authority."""

from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import MagicMock, patch


class TestInventoryCommandRouting(TestCase):
    def test_get_routes_through_atomic_pickup(self):
        from commands.cmd_inventory import CmdGet

        room = MagicMock()
        caller = MagicMock(location=room)
        item = MagicMock()
        item.access.return_value = True
        item.at_pre_get.return_value = True
        item.get_display_name.return_value = "a gem"
        caller.search.return_value = [item]

        command = CmdGet()
        command.caller = caller
        command.args = "gem"
        command.number = None
        with patch(
            "world.inventory_engine.pick_up",
            return_value=(True, "You pick up the gem."),
        ) as pickup:
            command.func()

        pickup.assert_called_once_with(caller, item)
        self.assertIn("pick up", caller.msg.call_args[0][0])

    def test_give_routes_through_atomic_transfer(self):
        from commands.cmd_inventory import CmdGive

        room = MagicMock()
        caller = MagicMock(location=room)
        target = MagicMock()
        item = MagicMock()
        item.at_pre_give.return_value = True
        item.get_display_name.return_value = "a gem"
        caller.search.side_effect = [[item], target]

        command = CmdGive()
        command.caller = caller
        command.args = "gem = friend"
        command.lhs = "gem"
        command.rhs = "friend"
        command.number = None
        with patch(
            "world.inventory_engine.transfer_item",
            return_value=(True, "You give gem to friend."),
        ) as transfer:
            command.func()

        transfer.assert_called_once_with(caller, target, item)
        target.msg.assert_called_once()

    def test_inventory_renders_relational_categories_and_weight(self):
        from commands.cmd_inventory import CmdInventory

        caller = MagicMock()
        carried_item = SimpleNamespace(key="Trail Rations")
        carried_record = SimpleNamespace(quantity=2)
        data = {
            "equipped": [],
            "containers": {},
            "carried": [(carried_item, carried_record)],
            "keyring": [],
            "carried_scales": 17,
            "carry_state": "comfortable",
            "carry_weight": 1.5,
            "carry_capacity": 60.0,
        }
        command = CmdInventory()
        command.caller = caller
        command.args = ""

        with patch(
            "world.inventory_engine.get_inventory_display_data",
            return_value=data,
        ):
            command.func()

        output = caller.msg.call_args.kwargs["text"][0]
        self.assertIn("Trail Rations x2", output)
        self.assertIn("1.50/60.00 kg", output)
        self.assertIn("Scales:", output)

    def test_character_cmdset_overrides_every_default_inventory_bypass(self):
        from commands import default_cmdsets
        from commands.cmd_inventory import (
            CmdDrop,
            CmdGet,
            CmdGive,
            CmdInventory,
        )

        added_commands = []
        with patch.object(
            default_cmdsets.default_cmds.CharacterCmdSet,
            "at_cmdset_creation",
            return_value=None,
        ):
            cmdset = default_cmdsets.CharacterCmdSet()
            cmdset.add = added_commands.append
            cmdset.at_cmdset_creation()

        by_key = {command.key: command for command in added_commands}
        self.assertIsInstance(by_key["get"], CmdGet)
        self.assertIsInstance(by_key["drop"], CmdDrop)
        self.assertIsInstance(by_key["give"], CmdGive)
        self.assertIsInstance(by_key["inventory"], CmdInventory)
