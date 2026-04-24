"""Direct command coverage for vendor-facing commands."""

import os
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django
django.setup()


def _make_character(contents=None):
    character = MagicMock()
    character.contents = contents or []
    character.msg = MagicMock()
    return character


def _make_item(key):
    item = MagicMock()
    item.key = key
    return item


class TestVendorCommands(unittest.TestCase):
    """Direct tests for the thin vendor command dispatchers."""

    @patch("commands.cmd_vendor._find_vendor_in_room", return_value=None)
    def test_list_requires_vendor_in_room(self, _mock_find_vendor):
        from commands.cmd_vendor import CmdList

        cmd = CmdList()
        cmd.caller = _make_character()
        cmd.args = ""

        cmd.func()

        self.assertIn("There is no vendor here", cmd.caller.msg.call_args[0][0])

    @patch("commands.cmd_vendor.get_vendor_price", side_effect=lambda vendor, item_def, character: item_def["value"])
    @patch("commands.cmd_vendor.get_vendor_stock", return_value={
        "trail_rations": {"key": "Trail Rations", "item_type": "consumable", "value": 5},
        "iron_sword": {"key": "Iron Sword", "item_type": "equipment", "value": 25},
    })
    @patch("commands.cmd_vendor._find_vendor_in_room")
    def test_list_groups_stock_and_displays_prices(
        self,
        mock_find_vendor,
        _mock_get_stock,
        _mock_get_price,
    ):
        from commands.cmd_vendor import CmdList

        vendor = MagicMock()
        vendor.key = "Quartermaster Elra"
        mock_find_vendor.return_value = vendor

        cmd = CmdList()
        cmd.caller = _make_character()
        cmd.args = ""

        cmd.func()

        message = cmd.caller.msg.call_args[0][0]
        self.assertIn("Quartermaster Elra's Wares", message)
        self.assertIn("Consumable:", message)
        self.assertIn("Equipment:", message)
        self.assertIn("(trail_rations)", message)
        self.assertIn("(iron_sword)", message)

    def test_buy_requires_item_id(self):
        from commands.cmd_vendor import CmdBuy

        cmd = CmdBuy()
        cmd.caller = _make_character()
        cmd.args = ""

        cmd.func()

        self.assertIn("Buy what?", cmd.caller.msg.call_args[0][0])

    @patch("commands.cmd_vendor.buy_item", return_value=(True, "You buy the iron sword."))
    @patch("commands.cmd_vendor._find_vendor_in_room")
    def test_buy_passes_vendor_purchase_result_through(self, mock_find_vendor, mock_buy_item):
        from commands.cmd_vendor import CmdBuy

        vendor = MagicMock()
        mock_find_vendor.return_value = vendor
        character = _make_character()

        cmd = CmdBuy()
        cmd.caller = character
        cmd.args = "iron_sword"

        cmd.func()

        mock_buy_item.assert_called_once_with(character, vendor, "iron_sword")
        self.assertIn("|gYou buy the iron sword.|n", character.msg.call_args[0][0])

    @patch("commands.cmd_vendor.sell_item", return_value=(True, "Sold for 8 Scales."))
    @patch("commands.cmd_vendor._find_vendor_in_room")
    def test_sell_uses_partial_inventory_match(self, mock_find_vendor, mock_sell_item):
        from commands.cmd_vendor import CmdSell

        vendor = MagicMock()
        mock_find_vendor.return_value = vendor
        item = _make_item("Iron Sword")
        character = _make_character(contents=[item])

        cmd = CmdSell()
        cmd.caller = character
        cmd.args = "iron"

        cmd.func()

        mock_sell_item.assert_called_once_with(character, vendor, item)
        self.assertIn("|gSold for 8 Scales.|n", character.msg.call_args[0][0])

    @patch("commands.cmd_vendor._find_vendor_in_room")
    def test_appraise_reports_missing_inventory_item(self, mock_find_vendor):
        from commands.cmd_vendor import CmdAppraise

        mock_find_vendor.return_value = MagicMock()
        character = _make_character(contents=[])

        cmd = CmdAppraise()
        cmd.caller = character
        cmd.args = "iron sword"

        cmd.func()

        self.assertIn("don't have 'iron sword'", character.msg.call_args[0][0].lower())

    @patch("commands.cmd_vendor.view_item", return_value=(False, "That stock id is unknown."))
    @patch("commands.cmd_vendor._find_vendor_in_room")
    def test_view_reports_engine_errors(self, mock_find_vendor, mock_view_item):
        from commands.cmd_vendor import CmdView

        vendor = MagicMock()
        mock_find_vendor.return_value = vendor
        character = _make_character()

        cmd = CmdView()
        cmd.caller = character
        cmd.args = "missing_stock"

        cmd.func()

        mock_view_item.assert_called_once_with(vendor, "missing_stock")
        self.assertIn("|rThat stock id is unknown.|n", character.msg.call_args[0][0])
