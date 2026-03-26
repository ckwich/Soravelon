"""
Guild join command.

CmdJoinGuild presents eligible guilds when a character qualifies (any domain
score >= 30) and has no guild. Delegates to world.guild_engine.join_guild()
with secondary domain selection.
"""

from commands.command import Command


class CmdJoinGuild(Command):
    """
    Join a guild when you receive an invitation.

    Usage:
      joinguild
      joinguild <guild_name>
      joinguild <guild_name> <secondary_domain>
    """

    key = "joinguild"
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        character = self.caller

        # Already in a guild
        if character.db.guild_id:
            from world.guild_engine import GUILDS
            guild = GUILDS.get(character.db.guild_id, {})
            guild_name = guild.get("name", character.db.guild_id)
            character.msg(f"You are already a member of {guild_name}.")
            return

        from world.guild_engine import (
            GUILDS,
            SUBCLASSES,
            check_guild_eligibility,
            join_guild,
        )
        from world.world_state import ALL_DOMAINS

        eligible = check_guild_eligibility(character)
        if not eligible:
            character.msg(
                "No guild has extended an invitation to you yet. "
                "Keep practicing your domains."
            )
            return

        args = self.args.strip().lower().split()

        # Filter out hidden guilds (vaelborn) unless remnance is discovered
        visible = []
        for gid in eligible:
            guild = GUILDS.get(gid, {})
            if guild.get("hidden") and not character.db.remnance_discovered:
                continue
            visible.append(gid)

        if not visible:
            character.msg(
                "No guild has extended an invitation to you yet. "
                "Keep practicing your domains."
            )
            return

        # Determine guild_id from args or single match
        guild_id = None
        secondary = None

        if args:
            # First arg is guild name
            guild_arg = args[0]
            for gid in visible:
                guild = GUILDS.get(gid, {})
                name_lower = guild.get("name", "").lower()
                short_name = gid.lower()
                if guild_arg == short_name or guild_arg in name_lower:
                    guild_id = gid
                    break
            if not guild_id:
                character.msg(
                    f"Unknown guild '{args[0]}'. "
                    "Type 'joinguild' to see available guilds."
                )
                return
            if len(args) > 1:
                secondary = args[1]

        elif len(visible) == 1:
            guild_id = visible[0]
        else:
            # Multiple eligible — list them
            lines = ["|wGuild Invitations|n", ""]
            for gid in visible:
                guild = GUILDS.get(gid, {})
                name = guild.get("name", gid)
                domain = guild.get("primary_domain", "unknown")
                motto = guild.get("motto", "")
                lines.append(f"  |w{name}|n ({domain})")
                lines.append(f"    |c{motto}|n")
            lines.append("")
            lines.append("Usage: |wjoinguild <guild_name> <secondary_domain>|n")
            character.msg("\n".join(lines))
            return

        guild = GUILDS.get(guild_id, {})
        primary = guild.get("primary_domain")

        # Need secondary domain
        if not secondary:
            scores = character.db.domain_scores or {}
            candidates = []
            for d in ALL_DOMAINS:
                if d == primary:
                    continue
                s = float(scores.get(d, 0.0))
                if s > 0:
                    candidates.append((d, s))
            candidates.sort(key=lambda x: x[1], reverse=True)

            lines = [
                f"|wJoining the {guild.get('name', guild_id)}|n",
                f"Primary domain: |w{primary}|n",
                "",
                "Choose a secondary domain:",
            ]
            for d, s in candidates:
                tag = " |g(recommended)|n" if candidates and d == candidates[0][0] else ""
                lines.append(f"  |w{d:15}|n (score: {s:.0f}){tag}")
            if not candidates:
                for d in ALL_DOMAINS:
                    if d != primary:
                        lines.append(f"  |w{d}|n")
            lines.append("")
            lines.append(
                f"Usage: |wjoinguild {guild_id} <secondary_domain>|n"
            )
            character.msg("\n".join(lines))
            return

        # Join with secondary
        ok, msg = join_guild(character, guild_id, secondary)
        character.msg(msg)

        if ok:
            subclass_id = character.db.subclass_id
            sc = SUBCLASSES.get(subclass_id, {})
            sc_name = sc.get("name", subclass_id)
            character.msg(
                f"|yThe {guild.get('name', guild_id)} welcomes you. "
                f"You walk the path of the {sc_name}.|n"
            )
