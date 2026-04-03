"""
Search command -- investigation skill check vs room search_dc.

Successful search reveals hidden exits and lore fragments (D-10, D-11).
Failed search triggers a 60-second per-room cooldown (D-12).
"""

import time
import random

from commands.command import Command


class CmdSearch(Command):
    """
    Search the current room for hidden passages and lore.

    Usage:
      search

    Rolls your investigation skill + d20 against the room's search
    difficulty. On success, hidden exits are revealed and lore
    fragments may be discovered. On failure, a 60-second cooldown
    prevents repeated searching.
    """

    key = "search"
    aliases = ["investigate"]
    locks = "cmd:all()"
    help_category = "General"

    COOLDOWN_SECONDS = 60

    def func(self):
        char = self.caller
        room = char.location
        if not room:
            char.msg("There is nothing to search here.")
            return

        # D-12: 60-second per-room cooldown after failed search
        cooldowns = char.ndb.search_cooldowns or {}
        room_key = str(room.id)
        now = time.time()
        if room_key in cooldowns:
            remaining = self.COOLDOWN_SECONDS - (now - cooldowns[room_key])
            if remaining > 0:
                char.msg(
                    f"You searched here recently. "
                    f"Try again in {int(remaining)} seconds."
                )
                return
            else:
                # Cooldown expired -- clean up
                del cooldowns[room_key]
                char.ndb.search_cooldowns = cooldowns

        search_dc = room.db.search_dc
        if not search_dc:
            char.msg("You search carefully but find nothing of interest.")
            return

        # D-10: Roll investigation skill + random(1,20) vs search_dc
        from world.skill_engine import get_skill_value, accumulate_skill_use

        skill = get_skill_value(char, "investigation")
        roll = skill + random.randint(1, 20)

        if roll < search_dc:
            # Failed -- set cooldown, vary failure message
            cooldowns[room_key] = now
            char.ndb.search_cooldowns = cooldowns
            fail_msgs = [
                "You search thoroughly but find nothing.",
                "Your investigation reveals nothing new.",
                "Despite careful searching, you come up empty.",
            ]
            char.msg(random.choice(fail_msgs))
            return

        # D-11: Success -- accumulate skill use
        accumulate_skill_use(char, "investigation")

        found_something = False

        # Reveal hidden exits
        hidden_exits = room.db.hidden_exits or []
        discovered = list(char.db.discovered_exits or [])
        discovered_set = set(str(e) for e in discovered)
        for exit_ref in hidden_exits:
            if str(exit_ref) not in discovered_set:
                discovered.append(exit_ref)
                discovered_set.add(str(exit_ref))
                found_something = True
                char.msg("|yYou discover a hidden passage!|n")
        if discovered != list(char.db.discovered_exits or []):
            char.db.discovered_exits = discovered

        # Collect lore fragments
        lore_frags = room.db.lore_fragments or []
        for frag in lore_frags:
            if frag.get("discovery_method") == "search":
                frag_id = frag.get("fragment_id", "unknown")
                collected = list(char.db.collected_lore_ids or [])
                collected_set = set(collected)
                if frag_id not in collected_set:
                    collected.append(frag_id)
                    char.db.collected_lore_ids = collected
                    char.msg(
                        f"|c{frag.get('text', 'You find an ancient inscription.')}|n"
                    )
                    found_something = True

        if not found_something:
            char.msg("Your thorough search reveals nothing new.")
