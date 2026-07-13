"""Guild invitation breadcrumb; induction itself happens with the contact."""

from commands.command import Command


def _display_contact(npc_id):
    """Turn stable authored contact ids into their established short names."""
    return str(npc_id).rsplit("_", 1)[-1].replace("-", " ").title()


def _display_location(stable_id, prefix):
    value = str(stable_id)
    if value.startswith(prefix):
        value = value[len(prefix):]
    return value.replace("_", " ").title()


class CmdJoinGuild(Command):
    """
    Review guild invitations and learn where to answer them.

    Usage:
      joinguild
      joinguild <guild_name>

    Guild membership cannot be completed remotely. Meet the named contact,
    talk with them, and choose your second path in that conversation.
    """

    key = "joinguild"
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        character = self.caller

        if character.db.guild_id:
            from world.guild_engine import GUILDS

            guild = GUILDS.get(character.db.guild_id, {})
            guild_name = guild.get("name", character.db.guild_id)
            character.msg(f"You are already a member of {guild_name}.")
            return

        from world.guild_engine import GUILDS, get_open_guild_recruitments
        from world.remnance_visibility import guild_is_player_visible

        invitations = [
            invitation
            for invitation in get_open_guild_recruitments(character)
            if guild_is_player_visible(
                invitation.guild_id,
                GUILDS.get(invitation.guild_id, {}),
                character,
            )
        ]
        if not invitations:
            character.msg(
                "No guild has sent you an invitation yet. Keep learning through "
                "meaningful work in the world."
            )
            return

        requested = self.args.strip().lower().split()
        if requested:
            guild_arg = requested[0]
            matched = [
                invitation
                for invitation in invitations
                if guild_arg == invitation.guild_id.lower()
                or guild_arg in GUILDS.get(invitation.guild_id, {}).get("name", "").lower()
            ]
            if not matched:
                character.msg(
                    f"No open invitation matches '{requested[0]}'. "
                    "Type |wjoinguild|n to review the letters you carry."
                )
                return
            invitations = matched

        lines = ["|wGuild Invitations|n", ""]
        for invitation in invitations:
            guild = GUILDS.get(invitation.guild_id, {})
            guild_name = guild.get("name", invitation.guild_id)
            contact = _display_contact(invitation.contact_npc_id)
            room = _display_location(invitation.location_room_id, "gq_")
            zone = _display_location(invitation.location_zone_id, "")
            lines.append(f"  |w{guild_name}|n")
            lines.append(f"    Meet |w{contact}|n at the |w{room}|n in {zone}.")
            lines.append(
                f"    Speak face to face: |wtalk {contact}|n. "
                "Your second path is chosen in that conversation."
            )
        character.msg("\n".join(lines))
