"""
Item inspection and comparison commands.

Per D-13: Basic desc always visible on look. Full stats require appraisal
skill check or vendor view command.
Per D-14: compare shows side-by-side stat comparison.
"""

from commands.command import Command
from world.skill_engine import get_skill_value, record_skill_use

# Appraisal DC = (rarity_number * 15) + (material_tier * 5)
RARITY_DC = {
    "common": 0,
    "normal": 0,
    "magic": 15,
    "rare": 30,
    "legendary": 45,
}


def _get_appraisal_dc(item):
    """Calculate appraisal difficulty for an item."""
    rarity = item.db.rarity or "normal"
    tier = item.db.material_tier or 1
    return RARITY_DC.get(rarity, 0) + (tier * 5)


def _get_item_stats(item):
    """Extract stat dict from an item for display/comparison."""
    stats = {}
    damage_min = item.db.damage_min or 0
    damage_max = item.db.damage_max or 0
    if damage_min or damage_max:
        stats["Damage"] = f"{damage_min}-{damage_max}"
    armor = item.db.armor_value or 0
    if armor:
        stats["Armor"] = str(armor)
    bonuses = item.db.stat_bonuses or {}
    for stat, val in bonuses.items():
        stats[stat.capitalize()] = f"+{val}"
    slot = item.db.equipment_slot or None
    if slot:
        stats["Slot"] = slot
    rarity = item.db.rarity or "normal"
    if rarity != "normal":
        stats["Rarity"] = rarity
    value = item.db.value_scales or 0
    if value:
        stats["Value"] = f"{value} Scales"
    tier = item.db.material_tier or 0
    if tier:
        stats["Material Tier"] = str(tier)
    return stats


def _format_stats(item, stats):
    """Format item stats for display."""
    lines = [f"|w{item.key}|n"]
    desc = item.db.desc or ""
    if desc:
        lines.append(desc)
    if stats:
        lines.append("|w--- Stats ---|n")
        for k, v in stats.items():
            lines.append(f"  {k}: {v}")
    return "\n".join(lines)


class CmdInspect(Command):
    """
    Inspect an item for detailed stats.

    Usage:
        inspect <item>

    Requires sufficient Appraisal skill to see mechanical stats.
    Basic description is always visible via normal look.
    """

    key = "inspect"
    aliases = ["appraise_item", "examine"]
    locks = "cmd:all()"
    help_category = "Items"

    def func(self):
        if not self.args:
            self.caller.msg("|yInspect what?|n")
            return

        # Search inventory and room
        item = self.caller.search(self.args.strip())
        if not item:
            return

        # Always show desc
        desc = item.db.desc or "You see nothing special."

        # Check appraisal skill
        skill = get_skill_value(self.caller, "appraisal")
        dc = _get_appraisal_dc(item)

        if skill >= dc:
            stats = _get_item_stats(item)
            self.caller.msg(_format_stats(item, stats))
            # Record skill use for passive advancement
            record_skill_use(self.caller, "appraisal")
        else:
            self.caller.msg(
                f"|w{item.key}|n\n{desc}\n"
                f"|yYou can't determine the exact properties. "
                f"(Appraisal skill too low)|n"
            )


class CmdCompare(Command):
    """
    Compare two items side by side.

    Usage:
        compare <item1> to <item2>
        compare <item1> <item2>

    Both items must be in your inventory or the room.
    Requires sufficient Appraisal skill for both items.
    """

    key = "compare"
    locks = "cmd:all()"
    help_category = "Items"

    def func(self):
        if not self.args:
            self.caller.msg("|yUsage: compare <item1> to <item2>|n")
            return

        # Parse args: "item1 to item2" or "item1 item2"
        args = self.args.strip()
        if " to " in args:
            name1, name2 = args.split(" to ", 1)
        else:
            parts = args.rsplit(" ", 1)
            if len(parts) < 2:
                self.caller.msg("|yUsage: compare <item1> to <item2>|n")
                return
            name1, name2 = parts

        item1 = self.caller.search(name1.strip())
        if not item1:
            return
        item2 = self.caller.search(name2.strip())
        if not item2:
            return

        # Check appraisal for both
        skill = get_skill_value(self.caller, "appraisal")
        dc1 = _get_appraisal_dc(item1)
        dc2 = _get_appraisal_dc(item2)

        if skill < dc1 or skill < dc2:
            self.caller.msg(
                "|yYou can't appraise one or both items well enough to compare.|n"
            )
            return

        stats1 = _get_item_stats(item1)
        stats2 = _get_item_stats(item2)
        all_keys = list(dict.fromkeys(list(stats1.keys()) + list(stats2.keys())))

        lines = [f"|w--- {item1.key} vs {item2.key} ---|n"]
        for key in all_keys:
            v1 = stats1.get(key, "-")
            v2 = stats2.get(key, "-")
            lines.append(f"  {key}: {v1}  |  {v2}")

        self.caller.msg("\n".join(lines))
