"""
Crafting engine for Soravelon.

Handles recipe validation, quality calculation, ingredient checking, item creation,
and recipe discovery. All functions use lazy imports. Functions that can fail
return (bool, str) per project convention.

Performance: craft_item makes 1 skill read + 1-2 model queries + N inventory scans.
calculate_craft_quality is pure computation (no DB).
"""

import random

from world.crafting_definitions import (
    QUALITY_DISPLAY,
    QUALITY_MULTIPLIERS,
    QUALITY_TIERS,
    RECIPE_REGISTRY,
    STATION_REQUIREMENTS,
)


# --- Quality Calculation ---

def calculate_craft_quality(skill_value, recipe_difficulty, has_station_bonus=False):
    """
    Compute quality tier from skill vs difficulty gap with random variance.

    The gap determines a base tier index (0-4). Random variance shifts +/- 1 tier,
    weighted toward center. Station bonus adds +1 ceiling to the roll.
    Returns a quality tier string from QUALITY_TIERS.
    """
    gap = skill_value - recipe_difficulty

    # Map gap to base tier index
    if gap < 0:
        base_index = 0  # flawed — underqualified
    elif gap < 15:
        base_index = 1  # standard
    elif gap < 30:
        base_index = 2  # fine
    elif gap < 50:
        base_index = 3  # superior
    else:
        base_index = 4  # masterwork

    # Random variance: weighted center, can shift +/- 1
    variance = random.choices([-1, 0, 1], weights=[20, 60, 20], k=1)[0]
    final_index = base_index + variance

    # Station bonus: shift ceiling up by 1
    if has_station_bonus:
        final_index += 1

    # Clamp to valid range
    final_index = max(0, min(len(QUALITY_TIERS) - 1, final_index))

    return QUALITY_TIERS[final_index]


def get_quality_modifier(quality_tier):
    """
    Return a multiplier for item effect amounts based on quality tier.

    flawed: 0.6, standard: 1.0, fine: 1.3, superior: 1.6, masterwork: 2.0
    """
    return QUALITY_MULTIPLIERS.get(quality_tier, 1.0)


# --- Station Check ---

def check_station(character, required_station):
    """
    Check if the character's current room has the required crafting station.

    Rooms are tagged with crafting_{station} in category 'crafting_station'.
    Returns (bool, str).
    """
    room = character.location
    if not room:
        return (False, "|rYou need to be somewhere to craft.|n")

    tag_key = f"crafting_{required_station}"
    if room.tags.has(tag_key, category="crafting_station"):
        return (True, "")

    station_desc = STATION_REQUIREMENTS.get(
        required_station, f"a {required_station}"
    )
    return (
        False,
        f"|rYou need {station_desc} to craft this.|n",
    )


# --- Recipe Discovery ---

def _ensure_default_recipes(character):
    """
    Ensure all default_known recipes have CharacterRecipe records.

    Called lazily on first craft/recipe check. Idempotent via get_or_create.
    """
    from world.models import CharacterRecipe

    for recipe_id, recipe in RECIPE_REGISTRY.items():
        if recipe.get("default_known"):
            CharacterRecipe.objects.get_or_create(
                character=character,
                recipe_id=recipe_id,
                defaults={"learned_from": "default"},
            )


def get_known_recipes(character, skill_filter=None):
    """
    Get all recipes known by a character.

    Includes explicitly learned recipes (CharacterRecipe records) and
    default_known recipes from RECIPE_REGISTRY even without a record.
    If skill_filter provided, only return recipes for that skill.
    Returns list of recipe dicts from RECIPE_REGISTRY.
    """
    from world.models import CharacterRecipe

    _ensure_default_recipes(character)

    # Get all CharacterRecipe records for this character
    known_ids = set(
        CharacterRecipe.objects.filter(
            character=character
        ).values_list("recipe_id", flat=True)
    )

    # Also include default_known recipes (defensive — _ensure_default_recipes
    # should have created records, but this covers edge cases)
    for recipe_id, recipe in RECIPE_REGISTRY.items():
        if recipe.get("default_known"):
            known_ids.add(recipe_id)

    result = []
    for recipe_id in known_ids:
        recipe = RECIPE_REGISTRY.get(recipe_id)
        if not recipe:
            continue
        if skill_filter and recipe.get("skill") != skill_filter:
            continue
        result.append({"recipe_id": recipe_id, **recipe})

    return result


def learn_recipe(character, recipe_id, learned_from=""):
    """
    Teach a recipe to a character. Creates CharacterRecipe record.

    Returns (bool, str). If already known, returns failure message.
    """
    from world.models import CharacterRecipe

    if recipe_id not in RECIPE_REGISTRY:
        return (False, f"|rUnknown recipe: {recipe_id}.|n")

    recipe = RECIPE_REGISTRY[recipe_id]
    _, created = CharacterRecipe.objects.get_or_create(
        character=character,
        recipe_id=recipe_id,
        defaults={"learned_from": learned_from},
    )

    if not created:
        return (False, "|yYou already know that recipe.|n")

    return (True, f"|g[Recipe learned: {recipe['name']}]|n")


# --- Conversion Ratio (D-08) ---

def get_conversion_quantity(character, recipe):
    """
    Calculate ingredient quantity needed based on skill for processing recipes (D-08).

    Returns adjusted quantity if recipe has conversion_ratio, else None.
    Thresholds: [30, 60, 85] -> quantities [3, 2, 1] (low -> mid -> high skill).
    """
    conversion = recipe.get("conversion_ratio")
    if not conversion:
        return None

    from world.skill_engine import get_skill_value

    skill = get_skill_value(character, recipe["skill"])
    thresholds = conversion["thresholds"]
    quantities = conversion["quantities"]

    for i, threshold in enumerate(thresholds):
        if skill < threshold:
            return quantities[i]
    return quantities[-1]


# --- Processing Quality (D-07) ---

def calculate_processing_quality(character_skill, recipe_difficulty, raw_quality="standard", has_station=False):
    """
    Quality propagation for processing recipes (D-07).

    Raw material quality sets a floor. Processing skill can raise but not lower quality.
    Returns a quality tier string from QUALITY_TIERS.
    """
    base_quality = calculate_craft_quality(character_skill, recipe_difficulty, has_station)

    raw_index = QUALITY_TIERS.index(raw_quality) if raw_quality in QUALITY_TIERS else 1
    base_index = QUALITY_TIERS.index(base_quality)

    # Final quality is average of raw and skill-based, rounded down (floor influence)
    final_index = (raw_index + base_index) // 2
    return QUALITY_TIERS[final_index]


# --- Ingredient Checking ---

def _check_ingredients(character, recipe):
    """
    Check if character has required ingredients in inventory.

    Uses Evennia's character.contents and obj.tags.has(item_tag, category="item_tag").
    Returns (bool, str, list_of_items) where list_of_items are the matched
    inventory objects to consume on success.
    """
    contents = character.contents
    items_to_consume = []

    # Processing recipe conversion ratio (D-08)
    conversion_qty = get_conversion_quantity(character, recipe)

    for ingredient in recipe.get("ingredients", []):
        tag = ingredient["item_tag"]
        needed = ingredient["quantity"]
        if conversion_qty is not None:
            needed = conversion_qty  # skill-based override for processing recipes
        matched = []

        for obj in contents:
            if obj in items_to_consume:
                continue  # already claimed by another ingredient
            if obj.tags.has(tag, category="item_tag"):
                matched.append(obj)
                if len(matched) >= needed:
                    break

        if len(matched) < needed:
            tag_display = tag.replace("_", " ")
            return (
                False,
                f"|rYou need {needed} {tag_display} but only have "
                f"{len(matched)}.|n",
                [],
            )

        items_to_consume.extend(matched)

    return (True, "", items_to_consume)


def _consume_ingredients(items_to_consume):
    """
    Delete matched inventory item objects, removing them from the game world.
    """
    for obj in items_to_consume:
        obj.delete()


# --- Item Creation ---

def _create_crafted_item(character, recipe, quality):
    """
    Create the output item from a recipe with the given quality tier.

    Uses item_spawner.create_item_from_template if available, otherwise
    creates a basic Evennia object with quality metadata. Places item
    in character's inventory. Returns the created item or None.
    """
    output = recipe.get("output", {})
    template_id = output.get("template_id", "unknown")
    quality_display = QUALITY_DISPLAY.get(quality, quality)
    item_name = f"{quality.capitalize()} {recipe['name']}"

    try:
        from world.item_spawner import create_item_from_template

        # Build a proper item_def dict from recipe output + quality metadata
        item_def = dict(output)  # copy to avoid mutating recipe
        item_def["quality"] = quality
        item_def["quality_modifier"] = get_quality_modifier(quality)
        item_def["crafted"] = True
        item_def.setdefault("key", item_name)
        item_def.setdefault("item_type", output.get("base_item_type", "item"))

        item = create_item_from_template(item_def, location=character)
        if item:
            return item
    except ImportError:
        pass

    # Fallback: create a basic Evennia object with crafting metadata
    from evennia.utils.create import create_object

    item = create_object(
        typeclass="typeclasses.objects.SoravelonObject",
        key=item_name,
        location=character,
    )

    if item:
        item.db.crafted = True
        item.db.quality = quality
        item.db.quality_modifier = get_quality_modifier(quality)
        item.db.recipe_id = template_id
        item.db.base_item_type = output.get("base_item_type", "misc")
        item.tags.add(template_id, category="item_tag")
        item.tags.add(output.get("base_item_type", "misc"), category="item_type")

    return item


# --- Main Craft Entry Point ---

def craft_item(character, recipe_id):
    """
    Main crafting entry point. Validates recipe, station, ingredients, skill,
    then produces an item with quality based on skill vs difficulty.

    The craft_time delay is NOT handled here -- the command layer uses
    utils.delay() before calling this function.

    Returns (bool, str). On success, the string includes quality and item name
    with color codes.
    """
    from world.skill_engine import accumulate_skill_use, get_skill_value

    # 1. Recipe exists?
    if recipe_id not in RECIPE_REGISTRY:
        return (False, f"|rUnknown recipe: {recipe_id}.|n")

    recipe = RECIPE_REGISTRY[recipe_id]

    # 2. Character knows the recipe?
    if not recipe.get("default_known"):
        from world.models import CharacterRecipe

        _ensure_default_recipes(character)
        if not CharacterRecipe.objects.filter(
            character=character, recipe_id=recipe_id
        ).exists():
            return (
                False,
                f"|rYou don't know the recipe for {recipe['name']}.|n",
            )

    # 3. Correct station?
    station = recipe.get("station")
    if station:
        ok, msg = check_station(character, station)
        if not ok:
            return (False, msg)

    # 4. Has ingredients?
    ok, msg, items_to_consume = _check_ingredients(character, recipe)
    if not ok:
        return (False, msg)

    # 5. Calculate quality from skill vs difficulty
    skill_id = recipe.get("skill", "cooking")
    skill_value = get_skill_value(character, skill_id)
    difficulty = recipe.get("difficulty", 10)
    quality = calculate_craft_quality(skill_value, difficulty)

    # 6. Create item FIRST — only consume ingredients on success
    # Processing recipes use inline output dict (Phase 13)
    if recipe.get("recipe_type") == "processing" and recipe.get("output", {}).get("item_id"):
        from world.item_spawner import create_item_from_template

        output_def = dict(recipe["output"])  # copy to avoid mutation
        output_def["quality"] = quality
        item = create_item_from_template(output_def, location=character)
        if not item:
            return (False, "|rSomething went wrong creating the item.|n")
        _consume_ingredients(items_to_consume)
        item.tags.add(output_def["item_id"], category="item_tag")
        if quality != "standard":
            quality_display = QUALITY_DISPLAY.get(quality, quality)
            item.key = f"{quality_display} {item.key}"
        accumulate_skill_use(character, skill_id, count=1)
        return (
            True,
            f"|gYou produce: {QUALITY_DISPLAY.get(quality, quality)} |w{recipe['name']}|n",
        )

    # Standard crafting item creation
    item = _create_crafted_item(character, recipe, quality)
    if not item:
        return (
            False,
            "|rSomething went wrong creating the item.|n",
        )
    _consume_ingredients(items_to_consume)

    # 8. Accumulate skill use for passive gain
    accumulate_skill_use(character, skill_id, count=1)

    # 9. Success message
    quality_display = QUALITY_DISPLAY.get(quality, quality)
    return (
        True,
        f"|gYou crafted: {quality_display} |w{item.key}|n",
    )
