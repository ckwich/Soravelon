"""
Social commands: who, shout, whisper.

Per D-15/D-19: OOC handled by Evennia channel system.
Shout is zone-wide in-character (D-16). Whisper is in-room private (D-17).
Who shows online players (D-19).
"""

import evennia
from commands.command import Command


SHOUT_STAMINA_COST = 10


class CmdWho(Command):
    """
    List online players.

    Usage:
        who

    Shows name, ancestry, guild/domain, and current zone for each
    online player.
    """

    key = "who"
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        # Get all puppeted characters
        sessions = evennia.SESSION_HANDLER.get_sessions()
        characters = []
        for session in sessions:
            puppet = session.get_puppet()
            if puppet:
                characters.append(puppet)

        if not characters:
            self.caller.msg("No one is online.")
            return

        lines = ["|w--- Who's Online ---|n"]
        for char in characters:
            ancestry = char.db.ancestry or "Unknown"
            domain_scores = char.db.domain_scores or {}
            primary_domain = (
                max(domain_scores, key=domain_scores.get) if domain_scores else "None"
            )
            guild = char.db.guild_name or primary_domain
            # Get zone from room tag
            zone = "Unknown"
            if char.location:
                zone_tags = char.location.tags.get(
                    category="zone_id", return_list=True
                )
                if zone_tags:
                    zone = zone_tags[0].replace("_", " ").title()
            lines.append(f"  |c{char.key}|n - {ancestry}, {guild}, in {zone}")
        lines.append(f"|w--- {len(characters)} player(s) online ---|n")
        self.caller.msg("\n".join(lines))


class CmdShout(Command):
    """
    Shout a message to everyone in your zone.

    Usage:
        shout <message>

    In-character zone-wide communication. Costs 10 stamina.
    """

    key = "shout"
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        if not self.args:
            self.caller.msg("Shout what?")
            return

        character = self.caller
        message = self.args.strip()

        # Check and deduct stamina
        from world.recovery_engine import spend_stamina
        ok, msg = spend_stamina(character, SHOUT_STAMINA_COST)
        if not ok:
            character.msg(f"|rYou're too exhausted to shout.|n")
            return

        # Find all characters in same zone
        if not character.location:
            character.msg("You can't shout from here.")
            return

        zone_tags = character.location.tags.get(
            category="zone_id", return_list=True
        )
        if not zone_tags:
            character.msg("You can't shout from here.")
            return

        zone_id = zone_tags[0]
        # Find all rooms in this zone
        zone_rooms = evennia.search_tag(zone_id, category="zone_id")

        # Message all characters in zone rooms
        shout_msg = f'|y{character.key} shouts: "{message}"|n'
        for room in zone_rooms:
            for obj in room.contents:
                if (
                    hasattr(obj, "sessions")
                    and obj.sessions.count()
                    and obj.id != character.id
                ):
                    # Skip sleeping characters
                    if not (obj.ndb.is_sleeping or False):
                        obj.msg(shout_msg)

        character.msg(f'|yYou shout: "{message}"|n')


class CmdWhisper(Command):
    """
    Whisper to another player in the same room.

    Usage:
        whisper <player> <message>

    Others see that you whispered but not what you said.
    """

    key = "whisper"
    locks = "cmd:all()"
    help_category = "Social"

    def func(self):
        if not self.args or " " not in self.args.strip():
            self.caller.msg("Usage: whisper <player> <message>")
            return

        args = self.args.strip()
        target_name, _, message = args.partition(" ")

        if not message:
            self.caller.msg("Whisper what?")
            return

        # Find target in room
        target = self.caller.search(target_name, location=self.caller.location)
        if not target:
            return  # search already sends error msg

        if target == self.caller:
            self.caller.msg("You mutter to yourself.")
            return

        # Send whisper
        self.caller.msg(f'|mYou whisper to {target.key}: "{message}"|n')
        target.msg(f'|m{self.caller.key} whispers to you: "{message}"|n')

        # Notify others in room
        for obj in self.caller.location.contents:
            if (
                hasattr(obj, "sessions")
                and obj.sessions.count()
                and obj.id != self.caller.id
                and obj.id != target.id
            ):
                obj.msg(
                    f"|m{self.caller.key} whispers something to {target.key}.|n"
                )
