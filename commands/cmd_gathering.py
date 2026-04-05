"""
Gathering commands for Soravelon.

CmdMine     -- mine ore nodes (mining skill, pickaxe tool)
CmdHarvest  -- harvest herb nodes (herbalism skill, sickle tool)
CmdChop     -- chop wood nodes (woodcutting skill, hatchet tool)
CmdForage   -- forage nodes (foraging skill, no tool required)
CmdButcher  -- butcher mob corpses (skinning skill, skinning_knife tool)

All gathering commands share _BaseGatherCmd which handles tool checks,
node lookup, skill-based delay (min 40% of base), and the delayed
callback that creates items, deducts durability, and grants skill XP.
"""

import random

from commands.command import Command


# ---------------------------------------------------------------------------
# Base gathering command
# ---------------------------------------------------------------------------

class _BaseGatherCmd(Command):
    """Base for all gathering commands. Subclasses set gather_skill,
    gather_verb, required_tool, and target_category."""

    gather_skill = None     # "mining", "herbalism", etc.
    gather_verb = None      # "mine", "harvest", etc.
    required_tool = None    # "pickaxe", "sickle", etc. None = no tool needed
    target_category = None  # "ore", "herb", "wood", "forage"
    locks = "cmd:all()"
    help_category = "Gathering"

    def func(self):
        character = self.caller

        # 1. Check tool requirement (D-19)
        if self.required_tool:
            tool = self._find_tool(character)
            if not tool:
                tool_name = self.required_tool.replace("_", " ")
                character.msg(f"|rYou need a {tool_name} to {self.gather_verb}.|n")
                return
            # Check durability (D-20)
            if tool.db.durability is not None and tool.db.durability <= 0:
                character.msg(f"|rYour {tool.key} is broken and needs repair.|n")
                return
        else:
            tool = None

        # 2. Find gathering node in room
        node = self._find_node(character)
        if not node:
            character.msg(f"|rThere is nothing to {self.gather_verb} here.|n")
            return

        # 3. Check not already gathering
        if getattr(character.ndb, "gathering_in_progress", False):
            character.msg("|rYou are already gathering.|n")
            return

        # 4. Calculate delay with skill reduction (D-14)
        from world.material_definitions import GATHER_DELAY_BY_TIER
        from world.skill_engine import get_skill_value

        skill_val = get_skill_value(character, self.gather_skill)
        base_delay = GATHER_DELAY_BY_TIER.get(node.db.tier or 1, 4)
        # Skill reduces delay: skill 100 = 40% of base (min per D-14)
        reduction = skill_val / 100.0 * 0.6  # max 60% reduction
        actual_delay = max(base_delay * 0.4, base_delay * (1 - reduction))

        # 5. Start gathering with echo
        from world.material_definitions import MATERIAL_REGISTRY

        mat = MATERIAL_REGISTRY.get(node.db.material_id or "", {})
        mat_name = mat.get("display_name", (node.db.material_id or "").replace("_", " ").title())
        character.msg(f"|xYou begin to {self.gather_verb} {mat_name}...|n")
        character.ndb.gathering_in_progress = True
        start_room = character.location

        # 6. Delayed callback
        from evennia.utils import delay

        delay(actual_delay, self._gather_callback, character, node, tool, start_room, skill_val)

    def _gather_callback(self, character, node, tool, start_room, skill_val):
        """Called after gather delay completes."""
        character.ndb.gathering_in_progress = False

        # Move cancel check (same pattern as _BaseCraftCmd)
        if character.location != start_room:
            character.msg("|rGathering interrupted by movement.|n")
            return

        # Check node still exists
        if not node or not node.pk:
            character.msg("|rThe resource has disappeared.|n")
            return

        # Perform gather
        from world.gathering_engine import gather_from_node

        success, result = gather_from_node(character, node)
        if not success:
            character.msg("|rThe resource is depleted.|n")
            return

        material_id = result

        # Create gathered item (D-04: skill affects quality AND quantity)
        from world.crafting_definitions import QUALITY_DISPLAY
        from world.crafting_engine import calculate_craft_quality
        from world.item_spawner import create_item_from_template
        from world.material_definitions import MATERIAL_REGISTRY
        from world.skill_engine import accumulate_skill_use

        mat = MATERIAL_REGISTRY.get(material_id, {})
        tier_difficulty = (node.db.tier or 1) * 15  # tier 1=15, tier 5=75
        quality = calculate_craft_quality(skill_val, tier_difficulty)

        item_def = {
            "item_id": material_id,
            "key": mat.get("display_name", material_id.replace("_", " ").title()),
            "item_type": "item",
            "weight": 0.5,
            "desc": f"Raw {mat.get('display_name', material_id)}.",
            "value": (node.db.tier or 1) * 5,
            "quality": quality,
        }
        item = create_item_from_template(item_def, location=character)

        # Quality display
        q_display = QUALITY_DISPLAY.get(quality, "")
        character.msg(f"|gYou gather {q_display} {item.key}.|n")

        # Bonus quantity at high skill (D-04): 25% chance at skill 50+, 50% at skill 80+
        bonus_chance = 0
        if skill_val >= 80:
            bonus_chance = 0.5
        elif skill_val >= 50:
            bonus_chance = 0.25
        if bonus_chance and random.random() < bonus_chance:
            bonus_item = create_item_from_template(item_def, location=character)
            character.msg(f"|gYour skill yields an extra {bonus_item.key}!|n")

        # Tool durability loss (D-20)
        if tool and tool.db.durability is not None:
            tool.db.durability -= 1
            if tool.db.durability <= 0:
                character.msg(f"|y{tool.key} has broken from use!|n")

        # Skill progression
        accumulate_skill_use(character, self.gather_skill)

    def _find_tool(self, character):
        """Find required tool in equipped tool slots or inventory."""
        # Check equipped tool slots first (CmdTools equip system)
        equipped = character.db.equipped_tools or {}
        for slot_item in equipped.values():
            if slot_item and slot_item.tags.has(self.required_tool, category="item_tag"):
                return slot_item
        # Fallback to inventory search
        for item in character.contents:
            if item.tags.has(self.required_tool, category="item_tag"):
                return item
        return None

    def _find_node(self, character):
        """Find a GatheringNode in the room matching this command's category."""
        from typeclasses.objects import GatheringNode

        for obj in character.location.contents:
            if isinstance(obj, GatheringNode) and obj.db.node_type == self.target_category:
                # Visibility check -- get_display_name returns None for hidden nodes
                display = obj.get_display_name(looker=character)
                if display is not None:
                    return obj
        return None


# ---------------------------------------------------------------------------
# Concrete gathering commands
# ---------------------------------------------------------------------------

class CmdMine(_BaseGatherCmd):
    """
    Mine ore from a mineral deposit.

    Usage:
      mine

    Requires a pickaxe in your inventory.
    """

    key = "mine"
    gather_skill = "mining"
    gather_verb = "mine"
    required_tool = "pickaxe"
    target_category = "ore"


class CmdHarvest(_BaseGatherCmd):
    """
    Harvest herbs from a plant.

    Usage:
      harvest

    Requires a sickle in your inventory.
    """

    key = "harvest"
    gather_skill = "herbalism"
    gather_verb = "harvest"
    required_tool = "sickle"
    target_category = "herb"


class CmdChop(_BaseGatherCmd):
    """
    Chop wood from a tree.

    Usage:
      chop

    Requires a hatchet in your inventory.
    """

    key = "chop"
    gather_skill = "woodcutting"
    gather_verb = "chop"
    required_tool = "hatchet"
    target_category = "wood"


class CmdForage(_BaseGatherCmd):
    """
    Forage for natural materials.

    Usage:
      forage

    No tool required.
    """

    key = "forage"
    gather_skill = "foraging"
    gather_verb = "forage"
    required_tool = None
    target_category = "forage"


class CmdButcher(_BaseGatherCmd):
    """
    Butcher a corpse to extract hides, bones, and meat.

    Usage:
      butcher
      butcher <corpse name>

    Requires a skinning knife in your inventory.
    """

    key = "butcher"
    gather_skill = "skinning"
    gather_verb = "butcher"
    required_tool = "skinning_knife"
    target_category = "hide"

    def _find_node(self, character):
        """Find a butcherable corpse OR a hide gathering node in the room."""
        from typeclasses.objects import CorpseContainer, GatheringNode

        target_name = self.args.strip().lower() if self.args else None

        # First check for corpses (primary butcher target)
        for obj in character.location.contents:
            if isinstance(obj, CorpseContainer):
                if target_name and target_name not in obj.key.lower():
                    continue
                can, msg = obj.can_butcher(character)
                if can:
                    return obj

        # Fall back to hide gathering nodes if no corpse found
        for obj in character.location.contents:
            if isinstance(obj, GatheringNode):
                if getattr(obj.db, "node_type", "") == "hide":
                    if target_name and target_name not in obj.key.lower():
                        continue
                    return obj
        return None

    def _gather_callback(self, character, node, tool, start_room, skill_val):
        """Override: butcher extracts materials from corpse, not from gathering node."""
        character.ndb.gathering_in_progress = False

        if character.location != start_room:
            character.msg("|rButchering interrupted by movement.|n")
            return

        if not node or not node.pk:
            character.msg("|rThe corpse has already decayed.|n")
            return

        # Determine butcher yields from mob type
        from world.crafting_definitions import QUALITY_DISPLAY
        from world.crafting_engine import calculate_craft_quality
        from world.gathering_engine import get_butcher_yields
        from world.item_spawner import create_item_from_template
        from world.skill_engine import accumulate_skill_use

        mob_key = node.db.mob_key or "unknown"
        yields = get_butcher_yields(mob_key)

        if not yields:
            character.msg("|rNothing useful can be salvaged from this corpse.|n")
            return

        tier_difficulty = 15  # base difficulty for butchering
        quality = calculate_craft_quality(skill_val, tier_difficulty)

        q_display = QUALITY_DISPLAY.get(quality, "")
        gathered = []
        for yield_def in yields:
            # Skill determines how many materials (1-3 based on skill)
            count = 1
            if skill_val >= 60:
                count = random.randint(1, 3)
            elif skill_val >= 30:
                count = random.randint(1, 2)
            for _ in range(count):
                item_def = {
                    "item_id": yield_def["material_id"],
                    "key": yield_def["display_name"],
                    "item_type": "item",
                    "weight": 0.3,
                    "desc": yield_def.get("desc", f"Raw material from {mob_key}."),
                    "value": yield_def.get("value", 5),
                    "quality": quality,
                }
                item = create_item_from_template(item_def, location=character)
                gathered.append(item.key)

        character.msg(f"|gYou butcher the corpse and obtain: {q_display} {', '.join(gathered)}.|n")

        # Mark corpse as butchered (prevent re-butchering)
        node.db.butchered = True

        # Tool durability
        if tool and tool.db.durability is not None:
            tool.db.durability -= 1
            if tool.db.durability <= 0:
                character.msg(f"|y{tool.key} has broken from use!|n")

        accumulate_skill_use(character, self.gather_skill)
