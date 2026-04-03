"""
Lore journal command -- review collected lore fragments organized by zone.

Players discover lore fragments via the search command. This journal
lets them revisit collected fragments at any time, organized by zone
with collection progress tracking.
"""

from commands.command import Command


class CmdLore(Command):
    """
    Review collected lore fragments organized by zone.

    Usage:
      lore              - Show zones with fragment counts
      lore <zone>       - Show collected fragments for a zone

    Lore fragments are discovered by searching rooms throughout the world.
    Your journal tracks everything you have found so far.
    """

    key = "lore"
    aliases = ["journal", "lore journal"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        from world.lore_registry import get_all_zones, get_zone_fragments

        caller = self.caller
        collected = set(caller.db.collected_lore_ids or [])

        if not self.args.strip():
            self._show_overview(caller, collected, get_all_zones, get_zone_fragments)
        else:
            self._show_zone(caller, collected, self.args.strip(), get_all_zones, get_zone_fragments)

    def _show_overview(self, caller, collected, get_all_zones, get_zone_fragments):
        """Show zone list with fragment counts."""
        zones = get_all_zones()
        if not zones:
            caller.msg("No lore fragments have been catalogued in this world yet.")
            return

        has_any = False
        lines = []
        lines.append("|wLore Journal|n")
        lines.append("|xFragments of history, collected through exploration.|n")
        lines.append("")

        for zone_id, zone_name in zones:
            zone_frags = get_zone_fragments(zone_id)
            total = len(zone_frags)
            if total == 0:
                continue
            found = len(collected & set(zone_frags.keys()))
            if found > 0:
                has_any = True
            lines.append(f"|c{zone_name}|n: {found}/{total} fragments collected")

        if not has_any:
            caller.msg(
                "You have not yet discovered any lore fragments. "
                "Try |wsearch|n in rooms as you explore."
            )
            return

        lines.append("")
        lines.append("Type |wlore <zone name>|n to read collected fragments.")
        caller.msg("\n".join(lines))

    def _show_zone(self, caller, collected, query, get_all_zones, get_zone_fragments):
        """Show collected fragments for a specific zone."""
        zones = get_all_zones()

        # Match zone by case-insensitive partial match
        query_lower = query.lower()
        matched = None
        for zone_id, zone_name in zones:
            if zone_name.lower() == query_lower:
                matched = (zone_id, zone_name)
                break
        if not matched:
            # Try partial match
            for zone_id, zone_name in zones:
                if query_lower in zone_name.lower():
                    matched = (zone_id, zone_name)
                    break

        if not matched:
            caller.msg("Unknown zone. Type |wlore|n to see available zones.")
            return

        zone_id, zone_name = matched
        zone_frags = get_zone_fragments(zone_id)
        total = len(zone_frags)
        collected_frags = {k: v for k, v in zone_frags.items() if k in collected}
        found = len(collected_frags)

        if found == 0:
            caller.msg(
                f"You haven't discovered any lore in {zone_name} yet. "
                "Search carefully as you explore."
            )
            return

        lines = []
        lines.append(f"|wLore: {zone_name}|n ({found}/{total} fragments)")
        lines.append("")

        for _frag_id, frag_data in sorted(collected_frags.items()):
            title = frag_data.get("title", "Unknown Fragment")
            text = frag_data.get("text", "")
            lines.append(f"|y--- {title} ---|n")
            lines.append(text)
            lines.append("")

        remaining = total - found
        if remaining > 0:
            lines.append(
                f"|xYou have {remaining} more fragment{'s' if remaining != 1 else ''} "
                f"to discover in this zone.|n"
            )

        caller.msg("\n".join(lines))
