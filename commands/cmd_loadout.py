"""
Loadout management command.

Allows players to view, add, remove, and clear abilities from their active
loadout (max 8 slots), and save/load up to 5 named presets.

Exports:
    CmdLoadout
"""

from commands.command import Command

MAX_LOADOUT_SIZE = 8
MAX_PRESETS = 5


class CmdLoadout(Command):
    """
    Manage your ability loadout.

    Usage:
      loadout                - view current loadout
      loadout add <ability>  - add an ability to your loadout
      loadout remove <ability> - remove an ability from your loadout
      loadout clear          - clear your entire loadout
      loadout save <slot#>   - save current loadout to preset (1-5)
      loadout <slot#>        - load a saved preset

    Your loadout determines which abilities (up to 8) are ready for use.
    You can save up to 5 preset configurations and swap between them.
    """

    key = "loadout"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        char = self.caller
        args = self.args.strip()

        if not args:
            self._view_loadout(char)
            return

        # Parse subcommand
        parts = args.split(None, 1)
        subcmd = parts[0].lower()
        rest = parts[1].strip() if len(parts) > 1 else ""

        if subcmd == "add":
            self._add_ability(char, rest)
        elif subcmd == "remove":
            self._remove_ability(char, rest)
        elif subcmd == "clear":
            self._clear_loadout(char)
        elif subcmd == "save":
            self._save_preset(char, rest)
        elif subcmd.isdigit():
            self._load_preset(char, int(subcmd))
        else:
            char.msg("Usage: loadout [add|remove|clear|save <slot>|<slot#>]")

    def _view_loadout(self, char):
        """Display current active loadout."""
        from world.ability_registry import get_ability

        loadout = list(char.db.active_loadout or [])
        if not loadout:
            char.msg("Your loadout is empty. Use |wloadout add <ability>|n to add abilities.")
            return

        lines = ["|wActive Loadout:|n"]
        for i, ability_id in enumerate(loadout, 1):
            ability = get_ability(ability_id)
            if ability:
                lines.append(
                    f"  {i}. {ability['name']} (Tier {ability['tier']}, "
                    f"{ability['domain'].capitalize()})"
                )
            else:
                lines.append(f"  {i}. {ability_id} (unknown)")
        char.msg("\n".join(lines))

    def _find_ability_by_name(self, query):
        """Search ABILITIES by name (case-insensitive prefix match).

        Returns (ability_id, ability_dict) or (None, error_message).
        """
        from world.ability_registry import ABILITIES

        query_lower = query.lower()
        matches = []
        for aid, ability in ABILITIES.items():
            if ability["name"].lower() == query_lower:
                return aid, ability
            if ability["name"].lower().startswith(query_lower):
                matches.append((aid, ability))

        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            names = ", ".join(m[1]["name"] for m in matches[:5])
            return None, f"Multiple matches: {names}. Be more specific."
        return None, f"No ability found matching '{query}'."

    def _add_ability(self, char, query):
        """Add an ability to the active loadout."""
        from world.ability_engine import _check_ability_access

        if not query:
            char.msg("Usage: loadout add <ability name>")
            return

        result = self._find_ability_by_name(query)
        if result[0] is None:
            char.msg(result[1])
            return

        ability_id, ability = result

        # Check access
        ok, reason = _check_ability_access(char, ability_id)
        if not ok:
            char.msg(reason)
            return

        loadout = list(char.db.active_loadout or [])

        if len(loadout) >= MAX_LOADOUT_SIZE:
            char.msg(
                f"Your loadout is full ({MAX_LOADOUT_SIZE} abilities). "
                "Remove one first."
            )
            return

        if ability_id in loadout:
            char.msg(f"{ability['name']} is already in your loadout.")
            return

        loadout.append(ability_id)
        char.db.active_loadout = loadout
        char.msg(f"Added |w{ability['name']}|n to your loadout (slot {len(loadout)}).")

    def _remove_ability(self, char, query):
        """Remove an ability from the active loadout."""
        from world.ability_registry import get_ability

        if not query:
            char.msg("Usage: loadout remove <ability name>")
            return

        loadout = list(char.db.active_loadout or [])
        if not loadout:
            char.msg("Your loadout is already empty.")
            return

        # Find matching ability in current loadout
        query_lower = query.lower()
        found_id = None
        for aid in loadout:
            ability = get_ability(aid)
            if ability and ability["name"].lower().startswith(query_lower):
                found_id = aid
                break

        if not found_id:
            char.msg(f"No ability matching '{query}' in your loadout.")
            return

        ability = get_ability(found_id)
        loadout.remove(found_id)
        char.db.active_loadout = loadout
        char.msg(f"Removed |w{ability['name']}|n from your loadout.")

    def _clear_loadout(self, char):
        """Clear the entire loadout."""
        char.db.active_loadout = []
        char.msg("Loadout cleared.")

    def _save_preset(self, char, slot_str):
        """Save current loadout to a preset slot."""
        if not slot_str or not slot_str.strip().isdigit():
            char.msg("Usage: loadout save <slot#> (1-5)")
            return

        slot = int(slot_str.strip())
        if slot < 1 or slot > MAX_PRESETS:
            char.msg(f"Preset slot must be between 1 and {MAX_PRESETS}.")
            return

        presets = dict(char.db.loadout_presets or {})
        presets[slot] = list(char.db.active_loadout or [])
        char.db.loadout_presets = presets
        char.msg(f"Loadout saved to preset {slot}.")

    def _load_preset(self, char, slot):
        """Load a preset into the active loadout."""
        if slot < 1 or slot > MAX_PRESETS:
            char.msg(f"Preset slot must be between 1 and {MAX_PRESETS}.")
            return

        presets = dict(char.db.loadout_presets or {})
        preset = presets.get(slot)
        if not preset:
            char.msg(f"No preset saved in slot {slot}.")
            return

        char.db.active_loadout = list(preset)
        char.msg(f"Loaded preset {slot}.")
