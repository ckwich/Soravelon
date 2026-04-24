"""
Domain progression display command.

CmdDomains shows the character's domain scores as proficiency descriptors
(Unaware through Transcendent). Hides Remnance until discovered (D-25).
Shows guild/subclass info if joined.
"""

from commands.command import Command


class CmdDomains(Command):
    """
    View your domain progression and guild status.

    Usage:
      domains
    """

    key = "domains"
    aliases = ["domain"]
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        character = self.caller

        from world.world_state import ALL_DOMAINS
        from world.guild_engine import (
            GUILDS,
            SUBCLASSES,
            get_domain_proficiency_label,
            get_guild_tier_label,
        )

        scores = character.db.domain_scores or {}

        lines = ["|wDomain Progression|n", ""]

        for domain in ALL_DOMAINS:
            # D-25: hide Remnance until discovered
            if domain == "remnance" and not character.db.remnance_discovered:
                continue
            score = float(scores.get(domain, 0.0))
            label = get_domain_proficiency_label(score)
            lines.append(f"  |w{domain.capitalize():15}|n |g{label}|n")

        lines.append("")

        # Guild status
        guild_id = character.db.guild_id
        if guild_id:
            guild = GUILDS.get(guild_id, {})
            guild_name = guild.get("name", guild_id)
            subclass_id = character.db.subclass_id
            sc = SUBCLASSES.get(subclass_id, {})
            sc_name = sc.get("name", subclass_id or "Unknown")
            tier_label = get_guild_tier_label(character)
            lines.append(f"|wGuild:|n {guild_name}")
            lines.append(f"|wPath:|n  {sc_name}")
            lines.append(f"|wRank:|n  {tier_label}")
        else:
            lines.append("|wGuild:|n None (Wanderer)")

        character.msg("\n".join(lines))
