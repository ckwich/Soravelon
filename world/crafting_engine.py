"""
Crafting engine for Soravelon.

Handles recipe validation, quality calculation, ingredient checking, item creation,
and recipe discovery. All functions use lazy imports. Functions that can fail
return (bool, str) per project convention.

Performance: craft_item makes 1 skill read + 1-2 model queries + N inventory scans.
calculate_craft_quality is pure computation (no DB).
"""

import random

from world.atomic_state import atomic_evennia_state
from world.crafting_definitions import (
    QUALITY_DISPLAY,
    QUALITY_MULTIPLIERS,
    QUALITY_TIERS,
    RECIPE_REGISTRY,
    STATION_REQUIREMENTS,
)
from world.game_operations import (
    get_operation_replay,
    normalize_operation_id,
    record_operation,
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
    Stackable inventory records contribute their full quantity instead of
    counting as only one object.

    Returns (bool, str, consume_specs) where consume_specs is a list of
    dicts with item / quantity / record to consume on success.
    """
    contents = character.contents
    items_to_consume = []
    claimed_quantities = {}

    # Processing recipe conversion ratio (D-08)
    conversion_qty = get_conversion_quantity(character, recipe)

    for ingredient in recipe.get("ingredients", []):
        tag = ingredient["item_tag"]
        needed = ingredient["quantity"]
        if conversion_qty is not None:
            needed = conversion_qty  # skill-based override for processing recipes
        matched = []
        matched_quantity = 0

        for obj in contents:
            if obj.tags.has(tag, category="item_tag"):
                record = None
                if hasattr(obj, "get_inventory_record"):
                    record = obj.get_inventory_record(character)

                available_quantity = 1
                if record and getattr(record, "quantity", None):
                    available_quantity = record.quantity
                else:
                    available_quantity = getattr(getattr(obj, "db", None), "quantity", None) or 1

                claim_key = getattr(obj, "id", id(obj))
                remaining_quantity = available_quantity - claimed_quantities.get(claim_key, 0)
                if remaining_quantity <= 0:
                    continue

                take_quantity = min(needed - matched_quantity, remaining_quantity)
                matched.append(
                    {
                        "item": obj,
                        "quantity": take_quantity,
                        "record": record,
                    }
                )
                claimed_quantities[claim_key] = claimed_quantities.get(claim_key, 0) + take_quantity
                matched_quantity += take_quantity
                if matched_quantity >= needed:
                    break

        if matched_quantity < needed:
            tag_display = tag.replace("_", " ")
            return (
                False,
                f"|rYou need {needed} {tag_display} but only have "
                f"{matched_quantity}.|n",
                [],
            )

        items_to_consume.extend(matched)

    return (True, "", items_to_consume)


def _consume_ingredients(character, items_to_consume):
    """Consume all ingredient quantities through the inventory authority."""

    from world.inventory_engine import consume_owned_quantities

    return consume_owned_quantities(character, items_to_consume)


def _best_input_quality(items_to_consume):
    """
    Return the strongest recognized quality present in the consumed inputs.

    Processing recipes use this as the raw-material quality influence so
    higher-quality gathered ingredients can improve refined outputs.
    """
    quality_index = {quality: idx for idx, quality in enumerate(QUALITY_TIERS)}
    best_index = quality_index["standard"]

    for spec in items_to_consume:
        obj = spec["item"] if isinstance(spec, dict) else spec
        obj_quality = getattr(getattr(obj, "db", None), "quality", None) or "standard"
        best_index = max(best_index, quality_index.get(obj_quality, quality_index["standard"]))

    return QUALITY_TIERS[best_index]


# --- Item Creation ---

def _create_crafted_item(character, recipe, quality):
    """
    Create the output item from a recipe with the given quality tier.

    Resolves the recipe's canonical catalog template, overlays only
    instance-specific crafting metadata, and places the item in the
    character's inventory. Returns the created item or None.
    """
    output = recipe.get("output", {})
    template_id = output.get("template_id", "unknown")
    item_name = f"{quality.capitalize()} {recipe['name']}"
    overrides = {
        "key": item_name,
        "quality": quality,
        "quality_modifier": get_quality_modifier(quality),
        "crafted": True,
        "recipe_id": template_id,
        "base_item_type": output.get("base_item_type", "misc"),
    }

    from world.item_catalog import ItemTemplateNotFound
    from world.item_spawner import create_item_from_catalog

    try:
        return create_item_from_catalog(
            template_id,
            location=character,
            overrides=overrides,
        )
    except ItemTemplateNotFound:
        return None


# --- Main Craft Entry Point ---

class _CraftRejected(RuntimeError):
    pass


def _after_write(checkpoint):
    """Failure-injection seam for composite crafting rollback tests."""


def craft_item(character, recipe_id, *, operation_id=None):
    """
    Main crafting entry point. Validates recipe, station, ingredients, skill,
    then produces an item with quality based on skill vs difficulty.

    The craft_time delay is NOT handled here -- the command layer uses
    utils.delay() before calling this function.

    Returns (bool, str). On success, the string includes quality and item name
    with color codes.
    """
    from evennia.objects.models import ObjectDB
    from world.skill_engine import accumulate_skill_use, get_skill_value

    operation_id = normalize_operation_id(operation_id)
    related_id = f"craft:{recipe_id}"

    try:
        with atomic_evennia_state(character) as tracker:
            locked_character = ObjectDB.objects.select_for_update().get(
                pk=character.id
            )
            replay = get_operation_replay(
                character=locked_character,
                operation_id=operation_id,
                operation_type="craft",
                related_id=related_id,
            )
            if replay:
                return True, replay.result["message"]

            if recipe_id not in RECIPE_REGISTRY:
                return False, f"|rUnknown recipe: {recipe_id}.|n"
            recipe = RECIPE_REGISTRY[recipe_id]

            if not recipe.get("default_known"):
                from world.models import CharacterRecipe

                _ensure_default_recipes(locked_character)
                if not CharacterRecipe.objects.filter(
                    character=locked_character,
                    recipe_id=recipe_id,
                ).exists():
                    return (
                        False,
                        f"|rYou don't know the recipe for {recipe['name']}.|n",
                    )

            station = recipe.get("station")
            if station:
                valid_station, station_message = check_station(
                    locked_character,
                    station,
                )
                if not valid_station:
                    return False, station_message

            has_ingredients, ingredient_message, items_to_consume = (
                _check_ingredients(locked_character, recipe)
            )
            if not has_ingredients:
                return False, ingredient_message
            for spec in items_to_consume:
                tracker.track(spec["item"])

            skill_id = recipe.get("skill", "cooking")
            skill_value = get_skill_value(locked_character, skill_id)
            difficulty = recipe.get("difficulty", 10)
            has_station_bonus = bool(station)
            processing = (
                recipe.get("recipe_type") == "processing"
                and recipe.get("output", {}).get("item_id")
            )

            if processing:
                from world.item_spawner import create_item_from_template

                quality = calculate_processing_quality(
                    skill_value,
                    difficulty,
                    raw_quality=_best_input_quality(items_to_consume),
                    has_station=has_station_bonus,
                )
                output_def = dict(recipe["output"])
                output_def["quality"] = quality
                item = create_item_from_template(
                    output_def,
                    location=locked_character,
                )
                if not item:
                    return False, "|rSomething went wrong creating the item.|n"
                tracker.track(item)
                item.tags.add(output_def["item_id"], category="item_tag")
                if quality != "standard":
                    quality_display = QUALITY_DISPLAY.get(quality, quality)
                    item.key = f"{quality_display} {item.key}"
                success_message = (
                    f"|gYou produce: {QUALITY_DISPLAY.get(quality, quality)} "
                    f"|w{recipe['name']}|n"
                )
            else:
                quality = calculate_craft_quality(
                    skill_value,
                    difficulty,
                    has_station_bonus=has_station_bonus,
                )
                item = _create_crafted_item(locked_character, recipe, quality)
                if not item:
                    return False, "|rSomething went wrong creating the item.|n"
                tracker.track(item)
                success_message = (
                    f"|gYou crafted: {QUALITY_DISPLAY.get(quality, quality)} "
                    f"|w{item.key}|n"
                )
            _after_write("craft_output_created")

            consumed, consume_message = _consume_ingredients(
                locked_character,
                items_to_consume,
            )
            if not consumed:
                raise _CraftRejected(consume_message)
            _after_write("craft_ingredients_consumed")

            record_operation(
                character=locked_character,
                operation_id=operation_id,
                operation_type="craft",
                related_id=related_id,
                result={
                    "message": success_message,
                    "item_object_id": item.id,
                    "quality": quality,
                },
            )
            _after_write("operation_recorded")

        accumulate_skill_use(character, skill_id, count=1)
        return True, success_message
    except _CraftRejected as error:
        return False, str(error)
