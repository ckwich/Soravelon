"""
Alias commands — create and remove personal command aliases.

CmdAlias:   alias <name> = <command>  — set a new alias
CmdUnalias: unalias <name>            — remove an alias

Aliases are stored in character.db.aliases (persistent across restarts).
System command keys cannot be aliased (D-17).
Chained aliases use semicolons; max 3 commands enforced at expansion time (D-16).
"""

from commands.command import Command

# System command keys that cannot be overridden by player aliases (D-17).
# This is a conservative set covering default Evennia movement, interaction,
# and communication commands plus the alias commands themselves.
SYSTEM_COMMAND_KEYS = {
    "look", "l", "get", "drop", "give", "inventory", "inv", "i",
    "say", "whisper", "tell", "quit", "who", "help", "north", "south",
    "east", "west", "northeast", "northwest", "southeast", "southwest",
    "up", "down", "in", "out", "n", "s", "e", "w", "ne", "nw", "se", "sw",
    "alias", "unalias",
}


class CmdAlias(Command):
    """
    Create a personal command alias.

    Usage:
      alias <name> = <command>
      alias <name> = <cmd1>; <cmd2>; <cmd3>
      alias           (list all aliases)

    Examples:
      alias k = attack
      alias kill = attack $1
      alias buff = cast shield; cast haste; cast blessing

    Aliases support argument tokens: $1 $2 $* $@
      $1, $2  - first and second space-split arguments
      $*,$@   - the full argument string

    Maximum 3 chained commands per alias (excess are silently ignored).
    Aliases cannot override system commands.
    Aliases persist across server restarts.
    """

    key = "alias"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        if not self.args:
            # List current aliases
            aliases = self.caller.db.aliases or {}
            if not aliases:
                self.caller.msg("You have no aliases set.")
                return
            lines = [f"  {k} = {v}" for k, v in sorted(aliases.items())]
            self.caller.msg("Your aliases:\n" + "\n".join(lines))
            return

        if "=" not in self.args:
            self.caller.msg("Usage: alias <name> = <command>")
            return

        name, _, expansion = self.args.partition("=")
        name = name.strip().lower()
        expansion = expansion.strip()

        if not name or not expansion:
            self.caller.msg("Usage: alias <name> = <command>")
            return

        # D-17: Cannot alias system command names
        if name in SYSTEM_COMMAND_KEYS:
            self.caller.msg(f"Cannot alias '{name}': that is a system command.")
            return

        # D-16: Warn if more than 3 chain parts (expansion still stored as-is)
        parts = [p.strip() for p in expansion.split(";") if p.strip()]
        if len(parts) > 3:
            self.caller.msg(
                "Aliases support a maximum of 3 chained commands. "
                "Excess commands will be ignored when the alias is used."
            )

        # Store — SaverDict copy pattern for dict mutation
        aliases = dict(self.caller.db.aliases or {})
        aliases[name] = expansion
        self.caller.db.aliases = aliases
        self.caller.msg(f"Alias set: {name} = {expansion}")


class CmdUnalias(Command):
    """
    Remove a personal command alias.

    Usage:
      unalias <name>

    Example:
      unalias k
    """

    key = "unalias"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: unalias <name>")
            return

        name = self.args.strip().lower()
        aliases = dict(self.caller.db.aliases or {})
        if name not in aliases:
            self.caller.msg(f"No alias '{name}' found.")
            return

        del aliases[name]
        self.caller.db.aliases = aliases
        self.caller.msg(f"Alias '{name}' removed.")
