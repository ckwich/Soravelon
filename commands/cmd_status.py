"""
Character sheet display command.

CmdStatus shows the full character sheet: vitals, stats (descriptors only),
dimensions, domains (proficiency labels only), guild/subclass, economy, loadout.
Numeric stat values are NEVER shown to the player (D-07).
Domain scores are shown as proficiency labels only (D-08).
"""

from commands.command import Command


class CmdStatus(Command):
    """
    View your full character sheet.

    Usage:
      status
      score
      stats
      sheet
    """

    key = "status"
    aliases = ["score", "stats", "sheet"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        char = self.caller

        from world.base_attributes import (
            STAT_NAMES,
            get_stat_descriptor,
            derive_max_hp,
            derive_max_stamina,
        )
        from world.world_state import ALL_DIMENSIONS, ALL_DOMAINS
        from world.guild_engine import (
            GUILDS,
            SUBCLASSES,
            FINGERPRINTS,
            get_domain_proficiency_label,
            get_guild_tier_label,
        )
        from world.banking import get_balance
        from world.ancestry_engine import ANCESTRY_TRAITS
        from world.ability_registry import get_ability

        lines = []

        # --- Header: Name + Ancestry ---
        ancestry_id = char.db.ancestry
        if ancestry_id:
            traits = ANCESTRY_TRAITS.get(ancestry_id, {})
            ancestry_name = traits.get("name", ancestry_id.capitalize())
        else:
            ancestry_name = "Unknown"
        lines.append(f"|w=== {char.key} |n|c({ancestry_name})|n |w===|n")
        lines.append("")

        # --- Vitals ---
        lines.append("|wVitals|n")
        max_hp = derive_max_hp(char)
        current_hp = char.ndb.hp if char.ndb.hp is not None else max_hp
        max_stamina = derive_max_stamina(char)
        current_stamina = char.ndb.stamina if char.ndb.stamina is not None else max_stamina
        lines.append(f"  |wHP:|n       |y{current_hp}|n / |y{max_hp}|n")
        lines.append(f"  |wStamina:|n  |y{current_stamina}|n / |y{max_stamina}|n")

        # Domain resource (only if guild member)
        guild_id = char.db.guild_id
        if guild_id:
            guild = GUILDS.get(guild_id, {})
            domain = guild.get("primary_domain")
            fp = FINGERPRINTS.get(domain, {})
            resource_name = fp.get("resource", "Resource")
            res_data = char.ndb.domain_resource
            if res_data and isinstance(res_data, dict):
                res_current = res_data.get("current", 0)
                res_max = res_data.get("max", 100)
                lines.append(f"  |w{resource_name}:|n  |y{res_current}|n / |y{res_max}|n")
            else:
                lines.append(f"  |w{resource_name}:|n  |y0|n")
        lines.append("")

        # --- Stats (descriptors ONLY -- D-07) ---
        lines.append("|wAttributes|n")
        base_stats = char.db.base_stats or {}
        for stat in STAT_NAMES:
            value = base_stats.get(stat, 10)
            descriptor = get_stat_descriptor(stat, value)
            lines.append(f"  {stat.capitalize():12s} |c{descriptor}|n")
        lines.append("")

        # --- Dimensions ---
        lines.append("|wDimensions|n")
        for dim in ALL_DIMENSIONS:
            score = getattr(char.db, f"{dim}_score", 0.0) or 0.0
            lines.append(f"  {dim.capitalize():12s} |c{score:.0f}|n")
        lines.append("")

        # --- Domains (proficiency labels ONLY -- D-08) ---
        lines.append("|wDomains|n")
        domain_scores = char.db.domain_scores or {}
        has_domain = False
        for domain in ALL_DOMAINS:
            # D-25: hide Remnance until discovered
            if domain == "remnance" and not char.db.remnance_discovered:
                continue
            score = float(domain_scores.get(domain, 0.0))
            if score > 0:
                label = get_domain_proficiency_label(score)
                lines.append(f"  {domain.capitalize():12s} |c{label}|n")
                has_domain = True
        if not has_domain:
            lines.append("  |xNone yet|n")

        # Guild / subclass info
        if guild_id:
            guild = GUILDS.get(guild_id, {})
            guild_name = guild.get("name", guild_id)
            subclass_id = char.db.subclass_id
            sc = SUBCLASSES.get(subclass_id, {}) if subclass_id else {}
            sc_name = sc.get("name", subclass_id or "None")
            tier_label = get_guild_tier_label(char)
            lines.append("")
            lines.append(f"  |wGuild:|n  {guild_name}")
            lines.append(f"  |wPath:|n   {sc_name}")
            lines.append(f"  |wRank:|n   {tier_label}")
        lines.append("")

        # --- Economy (D-09) ---
        lines.append("|wEconomy|n")
        carried = char.db.carried_scales or 0
        banked = get_balance(char)
        lines.append(f"  |wCarried:|n  |y{carried}|n Scales")
        lines.append(f"  |wBanked:|n   |y{banked}|n Scales")
        lines.append("")

        # --- Loadout ---
        lines.append("|wLoadout|n")
        loadout = char.db.active_loadout or []
        if loadout:
            for ability_id in loadout:
                ability = get_ability(ability_id)
                name = ability["name"] if ability else ability_id
                lines.append(f"  |c{name}|n")
        else:
            lines.append("  |xEmpty|n")

        char.msg("\n".join(lines))
