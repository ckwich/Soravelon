"""
Vendor commands for Soravelon.

CmdList     -- list vendor's stock with prices
CmdBuy      -- purchase an item from vendor
CmdSell     -- sell an item to vendor
CmdAppraise -- check what vendor would pay for an item
CmdView     -- inspect full item stats from vendor stock

All commands are thin dispatchers to world/vendor_engine.py.
"""

from commands.command import Command
from world.vendor_engine import (
    _find_vendor_in_room,
    buy_item,
    sell_item,
    appraise_item,
    view_item,
    get_vendor_stock,
    get_vendor_price,
)


# ---------------------------------------------------------------------------
# CmdList
# ---------------------------------------------------------------------------

class CmdList(Command):
    """
    List items available from a vendor.

    Usage:
      list

    Shows the vendor's stock with prices. Must be in a room with a vendor NPC.
    """

    key = "list"
    locks = "cmd:all()"
    help_category = "Commerce"

    def func(self):
        character = self.caller
        vendor = _find_vendor_in_room(character)
        if not vendor:
            character.msg("|rThere is no vendor here.|n")
            return

        stock = get_vendor_stock(vendor)
        if not stock:
            character.msg(f"{vendor.key} has nothing for sale.")
            return

        # Group by item_type
        grouped = {}
        for item_id, item_def in stock.items():
            itype = item_def.get("item_type", "item")
            grouped.setdefault(itype, []).append((item_id, item_def))

        lines = [f"|w{vendor.key}'s Wares|n"]
        lines.append("-" * 50)
        for itype, items in sorted(grouped.items()):
            lines.append(f"\n|y{itype.title()}:|n")
            for item_id, item_def in sorted(items, key=lambda x: x[1].get("value", 0)):
                price = get_vendor_price(vendor, item_def, character)
                key = item_def.get("key", item_id)
                lines.append(f"  {key:<30} {price:>5} Scales  |x({item_id})|n")

        character.msg("\n".join(lines))


# ---------------------------------------------------------------------------
# CmdBuy
# ---------------------------------------------------------------------------

class CmdBuy(Command):
    """
    Buy an item from a vendor.

    Usage:
      buy <item_id>

    Purchase an item using its ID (shown in parentheses when you `list`).
    Costs Scales from your carried currency.
    """

    key = "buy"
    locks = "cmd:all()"
    help_category = "Commerce"

    def func(self):
        character = self.caller
        item_id = self.args.strip()

        if not item_id:
            character.msg("|yBuy what? Usage: buy <item_id>|n")
            return

        vendor = _find_vendor_in_room(character)
        if not vendor:
            character.msg("|rThere is no vendor here.|n")
            return

        ok, msg = buy_item(character, vendor, item_id)
        if ok:
            character.msg(f"|g{msg}|n")
        else:
            character.msg(f"|r{msg}|n")


# ---------------------------------------------------------------------------
# CmdSell
# ---------------------------------------------------------------------------

class CmdSell(Command):
    """
    Sell an item to a vendor.

    Usage:
      sell <item>

    The vendor pays 33% of the item's value in Scales.
    Quest items cannot be sold. The vendor must accept the item type.
    """

    key = "sell"
    locks = "cmd:all()"
    help_category = "Commerce"

    def func(self):
        character = self.caller
        item_name = self.args.strip()

        if not item_name:
            character.msg("|ySell what? Usage: sell <item>|n")
            return

        vendor = _find_vendor_in_room(character)
        if not vendor:
            character.msg("|rThere is no vendor here.|n")
            return

        # Find item in character inventory by name (partial match)
        item_name_lower = item_name.lower()
        item = None
        for obj in character.contents:
            if obj.key.lower() == item_name_lower:
                item = obj
                break
            if obj.key.lower().startswith(item_name_lower):
                item = obj
                break

        if not item:
            character.msg(f"|rYou don't have '{item_name}' in your inventory.|n")
            return

        ok, msg = sell_item(character, vendor, item)
        if ok:
            character.msg(f"|g{msg}|n")
        else:
            character.msg(f"|r{msg}|n")


# ---------------------------------------------------------------------------
# CmdAppraise
# ---------------------------------------------------------------------------

class CmdAppraise(Command):
    """
    Ask a vendor to appraise an item.

    Usage:
      appraise <item>

    Shows how much the vendor would pay for the item.
    """

    key = "appraise"
    locks = "cmd:all()"
    help_category = "Commerce"

    def func(self):
        character = self.caller
        item_name = self.args.strip()

        if not item_name:
            character.msg("|yAppraise what? Usage: appraise <item>|n")
            return

        vendor = _find_vendor_in_room(character)
        if not vendor:
            character.msg("|rThere is no vendor here.|n")
            return

        # Find item in inventory
        item_name_lower = item_name.lower()
        item = None
        for obj in character.contents:
            if obj.key.lower() == item_name_lower:
                item = obj
                break
            if obj.key.lower().startswith(item_name_lower):
                item = obj
                break

        if not item:
            character.msg(f"|rYou don't have '{item_name}' in your inventory.|n")
            return

        ok, msg = appraise_item(character, vendor, item)
        if ok:
            character.msg(f"|y{msg}|n")
        else:
            character.msg(f"|r{msg}|n")


# ---------------------------------------------------------------------------
# CmdView
# ---------------------------------------------------------------------------

class CmdView(Command):
    """
    View full stats of an item in a vendor's stock.

    Usage:
      view <item_id>

    Shows damage, armor, stat bonuses, rarity, and value.
    No appraisal check needed -- vendors know their own stock.
    """

    key = "view"
    locks = "cmd:all()"
    help_category = "Commerce"

    def func(self):
        character = self.caller
        item_id = self.args.strip()

        if not item_id:
            character.msg("|yView what? Usage: view <item_id>|n")
            return

        vendor = _find_vendor_in_room(character)
        if not vendor:
            character.msg("|rThere is no vendor here.|n")
            return

        ok, msg = view_item(vendor, item_id)
        if ok:
            character.msg(msg)
        else:
            character.msg(f"|r{msg}|n")
