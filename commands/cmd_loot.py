"""
Corpse loot command. Respects CorpseContainer.can_loot() phase checks.
Per D-27: replaces default `get` which bypasses loot phases.
"""

from commands.command import Command
from typeclasses.objects import CorpseContainer


class CmdLoot(Command):
    """
    Loot items from a corpse.

    Usage:
        loot
        loot <corpse>
        loot rewards

    Respects loot phases: killer gets first access (2 min grace period),
    then open to all, then corpse decays.

    In groups, loot distribution follows the group's loot mode setting.
    """
    key = "loot"
    locks = "cmd:all()"
    help_category = "Combat"

    def func(self):
        character = self.caller

        if (self.args or "").strip().lower() == "rewards":
            self._claim_personal_rewards(character)
            return

        # Find corpse in room
        corpse = self._find_corpse(character)
        if not corpse:
            character.msg("|yThere is nothing to loot here.|n")
            return

        # Personal rewards are independent of the shared corpse contents and
        # cannot be claimed by another group member.
        personal_claim = self._claim_personal_rewards(character, corpse.id)

        # Check loot phase for ordinary shared drops.
        ok, msg = corpse.can_loot(character)
        if not ok:
            if personal_claim["claimed"]:
                return
            character.msg(f"|r{msg}|n")
            return

        # Check group loot mode
        from world.group_engine import is_in_group, get_designated_looter
        if is_in_group(character):
            designated = get_designated_looter(character, corpse)
            if designated and designated.id != character.id:
                character.msg(f"|rIt's {designated.key}'s turn to loot.|n")
                return

        # Transfer all items from corpse to character
        from world.inventory_engine import pick_up
        looted_items = []
        for item in list(corpse.contents):
            success, result_msg = pick_up(character, item, container=corpse)
            if success:
                looted_items.append(item.key)

        # Transfer Scales
        corpse_scales = corpse.db.scales or 0
        if corpse_scales > 0:
            character.db.carried_scales = (character.db.carried_scales or 0) + corpse_scales
            corpse.db.scales = 0
            looted_items.append(f"{corpse_scales} Scales")

        if looted_items:
            character.msg("|gYou loot: " + ", ".join(looted_items) + ".|n")
            # Advance round robin if applicable
            if is_in_group(character):
                from world.group_engine import advance_round_robin
                advance_round_robin(character, corpse=corpse)
        elif not personal_claim["claimed"]:
            character.msg("|yThe corpse is empty.|n")

    def _claim_personal_rewards(self, character, corpse_id=None):
        from world.encounter_rewards import claim_personal_rewards

        claim = claim_personal_rewards(character, corpse_id=corpse_id)
        if not claim["claimed"]:
            if corpse_id is None:
                character.msg("|yYou have no personal encounter rewards waiting.|n")
            return claim

        rewards = list(claim["items"])
        if claim["scales"]:
            rewards.append(f"{claim['scales']} Scales")
        character.msg("|gYou claim your personal reward: " + ", ".join(rewards) + ".|n")
        return claim

    def _find_corpse(self, character):
        """Find a CorpseContainer in character's room, optionally matching args."""
        target_name = self.args.strip().lower() if self.args else None
        for obj in character.location.contents:
            if isinstance(obj, CorpseContainer):
                if not target_name or target_name in obj.key.lower():
                    return obj
        return None
