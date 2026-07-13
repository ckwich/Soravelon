"""
Ancestry selection command.

CmdSetAncestry lets the player choose from 4 ancestries (Human, Kau'roran,
Veth, Selvar) during character creation. Delegates to
world.ancestry_engine.set_ancestry(). This choice is permanent.
"""

from commands.command import Command


class CmdSetAncestry(Command):
    """
    Choose your ancestry at character creation.

    Usage:
      ancestry <name>
      ancestry selvar <summer||winter>

    Available ancestries: Human, Kau'roran, Veth, Selvar
    Selvar requires a coat choice (summer or winter).
    This choice is permanent.
    """

    key = "ancestry"
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        character = self.caller

        # Already chosen — permanent choice
        if character.db.ancestry:
            from world.ancestry_engine import ANCESTRY_TRAITS
            traits = ANCESTRY_TRAITS.get(character.db.ancestry, {})
            display_name = traits.get("name", character.db.ancestry)
            character.msg(f"Your ancestry is already {display_name}.")
            return

        from world.ancestry_engine import (
            ANCESTRY_TRAITS,
            VALID_ANCESTRIES,
            set_ancestry,
        )

        args = self.args.strip().lower().split()

        # No args — show available ancestries
        if not args:
            lines = ["|wAvailable Ancestries|n", ""]
            for aid in VALID_ANCESTRIES:
                traits = ANCESTRY_TRAITS[aid]
                name = traits["name"]
                ability = traits.get("starting_ability", "none")
                lines.append(f"  |w{name:15}|n Starting ability: {ability}")
            lines.append("")
            lines.append("Usage: |wancestry <name>|n")
            lines.append("Selvar requires: |wancestry selvar <summer||winter>|n")
            character.msg("\n".join(lines))
            return

        # Parse ancestry_id and optional coat
        raw_id = args[0]
        # Accept both "kauroran" and "kau'roran"
        if raw_id in ("kauroran", "kau'roran"):
            ancestry_id = "kauroran"
        else:
            ancestry_id = raw_id

        coat = args[1] if len(args) > 1 else None

        ok, msg = set_ancestry(character, ancestry_id, coat)
        character.msg(msg)

        if ok:
            # Flavor line per ancestry
            flavor = {
                "human": "The Empire's blood runs in your veins. Adaptable. Resilient.",
                "kauroran": "The mountain clans remember. Your strength is your heritage.",
                "veth": "Quick and cunning, the warrens shaped your instincts.",
                "selvar": "Bold and reckless, the Selvar carve their own path.",
            }
            character.msg(f"|c{flavor.get(ancestry_id, '')}|n")
