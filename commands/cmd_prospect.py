"""
Prospect/survey and tool repair commands for Soravelon.

CmdProspect scans straight lines in cardinal directions from the
character's room, revealing gathering nodes with direction, distance,
material name, tier, and richness.

CmdRepair restores durability to damaged tools at a workbench using
smithing skill.
"""

from commands.command import Command


class CmdProspect(Command):
    """
    Scan for gathering nodes in nearby rooms.

    Usage:
      prospect
      survey

    Scans in straight lines (north, south, east, west) from your location.
    Range increases with your highest gathering skill.
    Reveals node type, tier, distance, and direction.
    """

    key = "prospect"
    aliases = ["survey"]
    locks = "cmd:all()"
    help_category = "Gathering"

    def func(self):
        character = self.caller

        # Max range based on highest gathering skill
        # Base range 2, +1 per 25 skill, max 6
        from world.skill_engine import get_skill_value
        from world.material_definitions import GATHERING_CATEGORIES

        max_skill = 0
        for cat_data in GATHERING_CATEGORIES.values():
            skill_name = cat_data["skill"]
            sv = get_skill_value(character, skill_name)
            if sv > max_skill:
                max_skill = sv

        max_range = min(6, 2 + max_skill // 25)

        from world.gathering_engine import prospect_scan

        results = prospect_scan(character, max_range)

        if not results:
            character.msg(
                "|xYou scan the surroundings but detect nothing of interest.|n"
            )
            return

        # Format output grouped by direction
        from world.material_definitions import MATERIAL_REGISTRY, MATERIAL_TIERS

        lines = ["|wYou focus your senses...|n"]

        # Sort by direction then distance
        results.sort(key=lambda r: (r["direction"], r["distance"]))

        for r in results:
            node = r["node"]
            mat = MATERIAL_REGISTRY.get(node.db.material_id, {})
            mat_name = mat.get("display_name", node.db.material_id or "Unknown")
            tier_name = MATERIAL_TIERS.get(node.db.tier, "Unknown")
            remaining = node.db.gathers_remaining or 0

            # Richness hint
            if remaining > 4:
                richness = "rich"
            elif remaining > 2:
                richness = "moderate"
            else:
                richness = "sparse"

            direction = r["direction"].capitalize()
            distance = r["distance"]
            rooms_str = "room" if distance == 1 else "rooms"

            lines.append(
                f"  |c{direction}|n, {distance} {rooms_str} away: "
                f"|w{mat_name}|n ({tier_name}) - {richness} deposit"
            )

        character.msg("\n".join(lines))


class CmdRepair(Command):
    """
    Repair a broken or damaged tool.

    Usage:
      repair <tool name>

    Requires a workbench and smithing skill. Better smithing skill
    restores more durability per repair.
    """

    key = "repair"
    locks = "cmd:all()"
    help_category = "Gathering"

    def func(self):
        character = self.caller
        args = self.args.strip().lower()

        if not args:
            character.msg("|yRepair what? Usage: repair <tool name>|n")
            return

        # Find tool in inventory
        tool = None
        for item in character.contents:
            if args in item.key.lower():
                if getattr(item.db, "durability", None) is not None:
                    tool = item
                    break

        if not tool:
            character.msg(
                f"|rYou don't have a repairable tool called '{args}'.|n"
            )
            return

        from world.gathering_engine import repair_tool

        _, message = repair_tool(character, tool)
        character.msg(message)
