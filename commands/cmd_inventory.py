"""Soravelon-aware inventory movement and display commands."""

from evennia.commands.default.general import (
    CmdDrop as EvenniaCmdDrop,
    CmdGet as EvenniaCmdGet,
    CmdGive as EvenniaCmdGive,
)
from evennia.utils import utils

from commands.command import Command


class CmdGet(EvenniaCmdGet):
    """Pick up an item through Soravelon's ownership engine.

    Usage:
        get <item>
        grab <item>
    """

    help_category = "Items"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("|yGet what?|n")
            return

        found = caller.search(
            self.args,
            location=caller.location,
            stacked=self.number,
        )
        if not found:
            return

        from world.inventory_engine import pick_up

        for item in utils.make_iter(found):
            if item == caller:
                caller.msg("|rYou can't pick yourself up.|n")
                continue
            if not item.access(caller, "get"):
                caller.msg(item.db.get_err_msg or "|rYou can't get that.|n")
                continue
            if not item.at_pre_get(caller):
                continue

            item_name = item.get_display_name(caller)
            success, message = pick_up(caller, item)
            caller.msg(("|g" if success else "|r") + message + "|n")
            if success and caller.location:
                caller.location.msg_contents(
                    f"$You() $conj(pick) up {item_name}.",
                    from_obj=caller,
                    exclude=caller,
                )


class CmdDrop(EvenniaCmdDrop):
    """Drop a directly carried item through Soravelon's ownership engine.

    Usage:
        drop <item>
    """

    help_category = "Items"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("|yDrop what?|n")
            return

        found = caller.search(
            self.args,
            location=caller,
            nofound_string=f"You aren't carrying {self.args}.",
            multimatch_string=f"You carry more than one {self.args}:",
            stacked=self.number,
        )
        if not found:
            return

        from world.inventory_engine import drop_item

        for item in utils.make_iter(found):
            if not item.at_pre_drop(caller):
                continue
            item_name = item.get_display_name(caller)
            success, message = drop_item(caller, item)
            caller.msg(("|g" if success else "|r") + message + "|n")
            if success:
                item.at_drop(caller)
                if caller.location:
                    caller.location.msg_contents(
                        f"$You() $conj(drop) {item_name}.",
                        from_obj=caller,
                        exclude=caller,
                    )


class CmdGive(EvenniaCmdGive):
    """Give an owned item to another nearby player atomically.

    Usage:
        give <item> = <player>
        give <item> to <player>
    """

    help_category = "Items"

    def func(self):
        caller = self.caller
        if not self.args or not self.rhs:
            caller.msg("|yUsage: give <item> = <player>|n")
            return

        found = caller.search(
            self.lhs,
            location=caller,
            nofound_string=f"You aren't carrying {self.lhs}.",
            multimatch_string=f"You carry more than one {self.lhs}:",
            stacked=self.number,
        )
        if not found:
            return
        target = caller.search(self.rhs, location=caller.location)
        if not target:
            return

        from world.inventory_engine import transfer_item

        for item in utils.make_iter(found):
            if not item.at_pre_give(caller, target):
                continue
            item_name = item.get_display_name(caller)
            success, message = transfer_item(caller, target, item)
            caller.msg(("|g" if success else "|r") + message + "|n")
            if success:
                item.at_give(caller, target)
                target.msg(
                    f"|g{caller.get_display_name(target)} gives you {item_name}.|n"
                )


class CmdPut(Command):
    """Place a directly carried item into an owned container.

    Usage:
        put <item> in <container>
    """

    key = "put"
    locks = "cmd:all()"
    help_category = "Items"

    def func(self):
        caller = self.caller
        before, separator, after = self.args.partition(" in ")
        if not separator or not before.strip() or not after.strip():
            caller.msg("|yUsage: put <item> in <container>|n")
            return
        item = caller.search(before.strip(), location=caller)
        container = caller.search(after.strip(), location=caller)
        if not item or not container:
            return

        from world.inventory_engine import put_in_container

        success, message = put_in_container(caller, item, container)
        caller.msg(("|g" if success else "|r") + message + "|n")


class CmdTake(Command):
    """Take an item out of one of your containers.

    Usage:
        take <item> from <container>
    """

    key = "take"
    locks = "cmd:all()"
    help_category = "Items"

    def func(self):
        caller = self.caller
        before, separator, after = self.args.partition(" from ")
        if not separator or not before.strip() or not after.strip():
            caller.msg("|yUsage: take <item> from <container>|n")
            return
        item = caller.search(before.strip(), location=caller)
        container = caller.search(after.strip(), location=caller)
        if not item or not container:
            return

        from world.inventory_engine import take_from_container

        success, message = take_from_container(caller, item, container)
        caller.msg(("|g" if success else "|r") + message + "|n")


def _item_line(item, record):
    quantity = f" x{record.quantity}" if record.quantity > 1 else ""
    return f"  {item.key}{quantity}"


class CmdInventory(Command):
    """Show weight-based carried, equipped, contained, and keyring items.

    Usage:
        inventory
        inv
        i
    """

    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    help_category = "Items"

    def func(self):
        from world.inventory_engine import get_inventory_display_data

        data = get_inventory_display_data(self.caller)
        lines = ["|wInventory|n"]
        if data["equipped"]:
            lines.append("|cEquipped|n")
            for item, record in data["equipped"]:
                lines.append(
                    f"  [{record.equipment_slot}] {item.key}"
                )
        if data["carried"]:
            lines.append("|cCarried|n")
            lines.extend(_item_line(item, record) for item, record in data["carried"])
        for container, contents in data["containers"].items():
            lines.append(f"|c{container.key}|n")
            lines.extend(_item_line(item, record) for item, record in contents)
        if data["keyring"]:
            lines.append("|cKeyring|n")
            lines.extend(_item_line(item, record) for item, record in data["keyring"])
        if not any(
            (
                data["equipped"],
                data["carried"],
                data["containers"],
                data["keyring"],
            )
        ):
            lines.append("  Nothing carried.")
        lines.append(
            f"|wWeight:|n {data['carry_weight']:.2f}/{data['carry_capacity']:.2f} kg "
            f"({data['carry_state']})"
        )
        lines.append(f"|wScales:|n {data['carried_scales']}")
        self.caller.msg(text=("\n".join(lines), {"type": "inventory"}))
