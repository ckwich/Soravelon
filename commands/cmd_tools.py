"""
Tool slot management commands.

Per D-20: Tool slots are SEPARATE from combat equipment slots.
character.db.equipped_tools = {"tool_pickaxe": item_id, "tool_sickle": item_id, ...}
"""

from commands.command import Command

VALID_TOOL_SLOTS = {
    "tool_pickaxe", "tool_sickle", "tool_hatchet",
    "tool_knife", "tool_rod",
}

SLOT_DISPLAY_NAMES = {
    "tool_pickaxe": "Pickaxe",
    "tool_sickle": "Sickle",
    "tool_hatchet": "Hatchet",
    "tool_knife": "Skinning Knife",
    "tool_rod": "Fishing Rod",
}

# Friendly name -> slot key mapping
FRIENDLY_NAME_TO_SLOT = {
    "pickaxe": "tool_pickaxe",
    "sickle": "tool_sickle",
    "hatchet": "tool_hatchet",
    "knife": "tool_knife",
    "skinning knife": "tool_knife",
    "rod": "tool_rod",
    "fishing rod": "tool_rod",
}


class CmdTools(Command):
    """
    View and manage your equipped gathering tools.

    Usage:
        tools                 - Show equipped tools
        tools equip <tool>    - Equip a gathering tool from inventory
        tools unequip <slot>  - Unequip a tool from a slot

    Tool slots are separate from combat equipment. You can have one
    tool of each type equipped at all times.

    Examples:
        tools
        tools equip pickaxe
        tools unequip sickle
    """

    key = "tools"
    locks = "cmd:all()"
    help_category = "Gathering"

    def func(self):
        character = self.caller
        args = self.args.strip().lower() if self.args else ""

        if args.startswith("equip "):
            self._equip_tool(character, args[6:].strip())
        elif args.startswith("unequip "):
            self._unequip_tool(character, args[8:].strip())
        else:
            self._show_tools(character)

    def _show_tools(self, character):
        equipped = character.db.equipped_tools or {}
        lines = ["|w--- Gathering Tools ---|n"]
        for slot, label in SLOT_DISPLAY_NAMES.items():
            item_id = equipped.get(slot)
            if item_id:
                item_obj = self._find_tool_by_id(character, item_id)
                name = item_obj.key if item_obj else item_id
                lines.append(f"  {label}: |c{name}|n")
            else:
                lines.append(f"  {label}: |x(empty)|n")
        character.msg("\n".join(lines))

    def _equip_tool(self, character, tool_name):
        item = character.search(tool_name, location=character)
        if not item:
            return
        tool_slot = getattr(item.db, "tool_slot", None)
        if not tool_slot or tool_slot not in VALID_TOOL_SLOTS:
            character.msg("That's not a gathering tool.")
            return
        # Copy dict to trigger SaverDict persistence
        equipped = dict(character.db.equipped_tools or {})
        equipped[tool_slot] = item.id
        character.db.equipped_tools = equipped
        character.msg(f"|gYou equip {item.key} as a gathering tool.|n")

    def _unequip_tool(self, character, slot_name):
        slot = FRIENDLY_NAME_TO_SLOT.get(slot_name, slot_name)
        if slot not in VALID_TOOL_SLOTS:
            character.msg(f"Unknown tool slot: {slot_name}")
            return
        equipped = dict(character.db.equipped_tools or {})
        if slot not in equipped:
            character.msg("Nothing equipped in that slot.")
            return
        del equipped[slot]
        character.db.equipped_tools = equipped
        character.msg("|gTool unequipped.|n")

    def _find_tool_by_id(self, character, item_id):
        """Find tool object by DB id in character's inventory."""
        for obj in character.contents:
            if obj.id == item_id:
                return obj
        return None
