"""
Equipment commands: equip, unequip, gear (show equipped items).
"""

from commands.command import Command


class CmdEquip(Command):
    """
    Equip an item from your inventory.

    Usage:
        equip <item>

    Equips the named item to its designated slot. Two-handed weapons
    require both hand slots free. Ring items auto-fill ring1 then ring2.
    """

    key = "equip"
    aliases = ["wear", "wield"]
    locks = "cmd:all()"
    help_category = "Equipment"

    def func(self):
        character = self.caller
        if not self.args:
            character.msg("|yEquip what?|n")
            return

        item_name = self.args.strip()
        item = character.search(item_name, location=character)
        if not item:
            return  # search() already sends error

        from world.inventory_engine import equip_item
        ok, msg = equip_item(character, item)
        character.msg(msg)


class CmdUnequip(Command):
    """
    Unequip a worn or wielded item.

    Usage:
        unequip <item>

    Returns the item to your carried inventory.
    """

    key = "unequip"
    aliases = ["remove", "unwield"]
    locks = "cmd:all()"
    help_category = "Equipment"

    def func(self):
        character = self.caller
        if not self.args:
            character.msg("|yUnequip what?|n")
            return

        item_name = self.args.strip()
        item = character.search(item_name, location=character)
        if not item:
            return

        from world.inventory_engine import unequip_item
        ok, msg = unequip_item(character, item)
        character.msg(msg)


class CmdGear(Command):
    """
    Show your currently equipped items.

    Usage:
        gear
        equipment
    """

    key = "gear"
    aliases = ["equipment", "eq"]
    locks = "cmd:all()"
    help_category = "Equipment"

    def func(self):
        character = self.caller
        from world.models import InventoryItem
        from evennia.objects.models import ObjectDB

        equipped = InventoryItem.objects.filter(
            character_id=character.id,
            is_equipped=True,
        ).order_by("equipment_slot")

        if not equipped:
            character.msg("|yYou have nothing equipped.|n")
            return

        lines = ["|wEquipped Gear:|n"]
        for record in equipped:
            try:
                obj = ObjectDB.objects.get(id=record.item_id)
                slot = record.equipment_slot or "unknown"
                lines.append(f"  |c{slot:>12}|n: {obj.key}")
            except ObjectDB.DoesNotExist:
                continue

        character.msg("\n".join(lines))
