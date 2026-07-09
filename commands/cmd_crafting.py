"""
Crafting commands for Soravelon.

CmdCook     -- cook recipes (cooking skill, campfire station)
CmdSmith    -- smith recipes (smithing skill, forge station)
CmdBrew     -- brew recipes (alchemy skill, alchemy_bench station)
CmdCraft    -- craft recipes (engineering skill, workbench station)
CmdRecipes  -- list known recipes

All crafting commands share a base class that handles the common flow:
validate recipe, check station, show craft echo, delay, then call craft_item.
"""

from commands.command import Command


# ---------------------------------------------------------------------------
# Base crafting command
# ---------------------------------------------------------------------------

class _BaseCraftCmd(Command):
    """Base for all crafting commands. Subclasses set craft_skill and craft_verb."""

    craft_skill = None  # override in subclass
    craft_verb = None   # override in subclass
    locks = "cmd:all()"
    help_category = "Crafting"

    def func(self):
        from world.crafting_definitions import COMMAND_TO_SKILL, RECIPE_REGISTRY
        from world.crafting_engine import craft_item

        character = self.caller
        recipe_name = self.args.strip().lower()

        if not recipe_name:
            character.msg(
                f"|yWhat do you want to {self.craft_verb}? "
                f"Usage: {self.craft_verb} <recipe>|n"
            )
            return

        # Resolve skill for this command verb
        skill = COMMAND_TO_SKILL.get(self.craft_verb)
        if not skill:
            character.msg("|rUnknown crafting skill.|n")
            return

        # Find matching recipe by name (case-insensitive, partial match)
        matched_id = None
        for recipe_id, recipe in RECIPE_REGISTRY.items():
            if recipe.get("skill") != skill:
                continue
            name_lower = recipe["name"].lower()
            id_lower = recipe_id.lower()
            if recipe_name == name_lower or recipe_name == id_lower:
                matched_id = recipe_id
                break
            if name_lower.startswith(recipe_name) or id_lower.startswith(recipe_name):
                matched_id = recipe_id
                break

        if not matched_id:
            character.msg(
                f"|rYou don't know a {skill} recipe called '{recipe_name}'.|n"
            )
            return

        recipe = RECIPE_REGISTRY[matched_id]

        # Show craft echo and use delay for crafting time
        craft_echo = recipe.get("craft_echo", f"You begin {self.craft_verb}ing...")
        craft_time = recipe.get("craft_time", 3)

        character.msg(f"|x{craft_echo}|n")

        # Track crafting state to cancel on move
        character.ndb.crafting_in_progress = True
        start_room = character.location
        from world.economy_ids import new_operation_id

        operation_id = new_operation_id()

        from evennia.utils import delay

        def _finish_craft():
            """Callback after craft delay completes."""
            # Cancel if character moved
            if character.location != start_room:
                character.msg("|rYou moved and lost your crafting progress.|n")
                character.ndb.crafting_in_progress = False
                return

            character.ndb.crafting_in_progress = False
            success, msg = craft_item(
                character,
                matched_id,
                operation_id=operation_id,
            )
            character.msg(msg)

        delay(craft_time, _finish_craft)


# ---------------------------------------------------------------------------
# Concrete crafting commands
# ---------------------------------------------------------------------------

class CmdCook(_BaseCraftCmd):
    """
    Cook a recipe at a campfire or hearth.

    Usage:
      cook <recipe>

    Requires a campfire station and cooking ingredients.
    """

    key = "cook"
    craft_skill = "cooking"
    craft_verb = "cook"


class CmdSmith(_BaseCraftCmd):
    """
    Smith an item at a forge.

    Usage:
      smith <recipe>

    Requires a forge station and smithing materials.
    """

    key = "smith"
    craft_skill = "smithing"
    craft_verb = "smith"


class CmdBrew(_BaseCraftCmd):
    """
    Brew a potion or draught at an alchemy bench.

    Usage:
      brew <recipe>

    Requires an alchemy bench and alchemical ingredients.
    """

    key = "brew"
    craft_skill = "alchemy"
    craft_verb = "brew"


class CmdCraft(_BaseCraftCmd):
    """
    Craft an item at a workbench.

    Usage:
      craft <recipe>

    Requires a workbench and engineering materials.
    """

    key = "craft"
    craft_skill = "engineering"
    craft_verb = "craft"


# ---------------------------------------------------------------------------
# CmdRecipes
# ---------------------------------------------------------------------------

class CmdRecipes(Command):
    """
    List your known recipes.

    Usage:
      recipes               (show all known recipes)
      recipes cooking        (filter by skill)
      recipes smithing
      recipes alchemy
    """

    key = "recipes"
    locks = "cmd:all()"
    help_category = "Crafting"

    def func(self):
        from world.crafting_definitions import SKILL_TO_COMMAND
        from world.crafting_engine import get_known_recipes

        character = self.caller
        skill_filter = self.args.strip().lower() or None

        # Validate skill filter
        valid_skills = set(SKILL_TO_COMMAND.keys())
        if skill_filter and skill_filter not in valid_skills:
            character.msg(
                f"|yUnknown skill. Valid filters: "
                f"{', '.join(sorted(valid_skills))}|n"
            )
            return

        recipes = get_known_recipes(character, skill_filter=skill_filter)

        if not recipes:
            if skill_filter:
                character.msg(f"|yYou don't know any {skill_filter} recipes.|n")
            else:
                character.msg("|yYou don't know any recipes yet.|n")
            return

        # Group by skill
        by_skill = {}
        for r in recipes:
            skill = r.get("skill", "other")
            by_skill.setdefault(skill, []).append(r)

        lines = ["|w=== Known Recipes ===|n"]
        for skill in sorted(by_skill.keys()):
            cmd = SKILL_TO_COMMAND.get(skill, skill)
            lines.append(f"\n|c[{skill.capitalize()}]|n (use: |w{cmd}|n)")
            for r in sorted(by_skill[skill], key=lambda x: x.get("difficulty", 0)):
                name = r.get("name", r.get("recipe_id", "?"))
                diff = r.get("difficulty", "?")
                station = r.get("station", "none")
                ingredients = r.get("ingredients", [])
                ing_strs = []
                for ing in ingredients:
                    tag = ing["item_tag"].replace("_", " ")
                    qty = ing["quantity"]
                    ing_strs.append(f"{qty}x {tag}")
                ing_display = ", ".join(ing_strs) if ing_strs else "none"
                lines.append(
                    f"  |w{name}|n (diff: {diff}, "
                    f"station: {station}, "
                    f"needs: {ing_display})"
                )

        character.msg("\n".join(lines))
