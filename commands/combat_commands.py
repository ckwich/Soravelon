"""
Combat commands and CombatCmdSet.

CmdAttack initiates combat or performs basic attack on current target.
CmdFlee attempts escape with speed/skill check per D-28.
CmdTarget switches auto-target per D-14 (does NOT consume an action).
CmdPass forfeits remaining actions and ends turn.
CombatCmdSet replaces default commands during combat per D-17.

CombatCmdSet is added/removed dynamically by CombatScript, not by
CharacterCmdSet. CmdAttack is also in CharacterCmdSet so players can
initiate combat from outside CombatCmdSet.
"""

import random

from evennia.commands.cmdset import CmdSet

from commands.command import Command


# ---------------------------------------------------------------------------
# CmdAttack
# ---------------------------------------------------------------------------

class CmdAttack(Command):
    """
    Attack a target or initiate combat.

    Usage:
      attack [<target>]

    If not in combat, this starts a fight with the specified mob
    (or the first valid mob in the room). If already in combat,
    performs a basic attack on your current target or specified target.
    """

    key = "attack"
    aliases = ["a", "hit", "strike"]
    locks = "cmd:all()"
    help_category = "Combat"

    def func(self):
        character = self.caller
        handler = character.ndb.combat_handler

        if not handler:
            # Not in combat -- initiate
            self._initiate_combat(character)
        else:
            # In combat -- basic attack
            self._combat_attack(character, handler)

    def _initiate_combat(self, character):
        """Find a mob in the room and start combat."""
        room = character.location
        if not room:
            character.msg("|rYou are nowhere.|n")
            return

        # Find target from args or first hostile mob
        target = None
        if self.args and self.args.strip():
            target = character.search(self.args.strip())
            if not target:
                return  # search() already sends error

            # Validate target is a mob with combat_enabled
            if not hasattr(target, "get_behavior_toward"):
                character.msg("|rYou can't attack that.|n")
                return
            if target.db.combat_enabled is False:
                character.msg("|rThat creature cannot be fought.|n")
                return
        else:
            # Find first attackable mob in room
            for obj in room.contents:
                if obj == character:
                    continue
                if hasattr(obj, "get_behavior_toward") and (obj.db.combat_enabled is not False):
                    target = obj
                    break

        if not target:
            character.msg("|rThere is nothing to attack here.|n")
            return

        # Start combat
        from world.combat_script import start_combat
        start_combat(room, character, [target])

        # Set auto-target
        character.ndb.combat_target_id = target.id

    def _combat_attack(self, character, handler):
        """Perform basic attack during combat."""
        # Validate it's this character's turn
        current = handler.get_current_combatant()
        if current is None or current.id != character.id:
            character.msg("|rIt's not your turn.|n")
            return

        # Resolve target
        target = None
        if self.args and self.args.strip():
            target = character.search(self.args.strip())
            if not target:
                return
            if not handler.is_combatant(target):
                character.msg(f"|r{target.key} is not in this combat.|n")
                return

        # Update auto-target if explicit target given
        if target:
            character.ndb.combat_target_id = target.id

        handler.process_player_action(character, "basic_attack", target)


# ---------------------------------------------------------------------------
# CmdFlee (per D-28)
# ---------------------------------------------------------------------------

class CmdFlee(Command):
    """
    Attempt to flee from combat.

    Usage:
      flee

    Speed check based on agility vs mob agility, with bonus from
    subterfuge domain score. Blocked if rooted or stunned. On success,
    you move to a random adjacent room and leave combat. On failure,
    you lose your turn.
    """

    key = "flee"
    aliases = ["escape", "run"]
    locks = "cmd:all()"
    help_category = "Combat"

    def func(self):
        character = self.caller
        handler = character.ndb.combat_handler

        if not handler:
            character.msg("|rYou are not in combat.|n")
            return

        # Validate turn
        current = handler.get_current_combatant()
        if current is None or current.id != character.id:
            character.msg("|rIt's not your turn.|n")
            return

        handler.process_player_action(character, "flee")


# ---------------------------------------------------------------------------
# CmdTarget (per D-14)
# ---------------------------------------------------------------------------

class CmdTarget(Command):
    """
    Switch your auto-target to a different combatant.

    Usage:
      target <name>

    Does NOT consume an action. Your next attack and abilities will
    target this combatant by default.
    """

    key = "target"
    aliases = ["t"]
    locks = "cmd:all()"
    help_category = "Combat"

    def func(self):
        character = self.caller
        handler = character.ndb.combat_handler

        if not handler:
            character.msg("|rYou are not in combat.|n")
            return

        if not self.args or not self.args.strip():
            character.msg("Usage: target <name>")
            return

        target = character.search(self.args.strip())
        if not target:
            return  # search() sends error

        if not handler.is_combatant(target):
            character.msg(f"|r{target.key} is not in this combat.|n")
            return

        character.ndb.combat_target_id = target.id
        character.msg(f"|wYou focus your attention on {target.key}.|n")


# ---------------------------------------------------------------------------
# CmdPass
# ---------------------------------------------------------------------------

class CmdPass(Command):
    """
    Pass your turn and forfeit remaining actions.

    Usage:
      pass
    """

    key = "pass"
    aliases = ["wait", "skip"]
    locks = "cmd:all()"
    help_category = "Combat"

    def func(self):
        character = self.caller
        handler = character.ndb.combat_handler

        if not handler:
            character.msg("|rYou are not in combat.|n")
            return

        # Validate turn
        current = handler.get_current_combatant()
        if current is None or current.id != character.id:
            character.msg("|rIt's not your turn.|n")
            return

        handler.process_player_action(character, "pass")


# ---------------------------------------------------------------------------
# CombatCmdSet
# ---------------------------------------------------------------------------

class CombatCmdSet(CmdSet):
    """
    Command set active during combat. Replaces default commands with
    combat-specific versions. Added/removed dynamically by CombatScript.

    mergetype = "Replace" with priority 10 blocks normal exit traversal
    and non-combat commands. Players can still look around and use
    abilities.
    """

    key = "CombatCmdSet"
    mergetype = "Replace"
    priority = 10
    no_exits = True

    def at_cmdset_creation(self):
        from commands.cmd_abilities import CmdAbilities, CmdUseAbility
        from evennia.commands.default.general import CmdLook

        self.add(CmdAttack())
        self.add(CmdFlee())
        self.add(CmdTarget())
        self.add(CmdPass())
        self.add(CmdUseAbility())
        self.add(CmdAbilities())
        self.add(CmdLook())
