---
name: crafting-system
description: Crafting engine — recipe registry, quality tiers, station checks, ingredient consumption, skill-based quality, and 5 player commands
---

## Activation

This skill triggers when editing these files:
- `world/crafting_engine.py`
- `world/crafting_definitions.py`
- `commands/cmd_crafting.py`
- `tests/test_crafting.py`

Keywords: crafting, craft, cook, smith, brew, recipe, quality, ingredient, station, campfire, forge, workbench, alchemy bench

---

You are working on **soravelon's crafting system** — recipe-based item creation with skill-driven quality.

## Key Files
- `world/crafting_engine.py` — Core engine: `craft_item()`, `calculate_craft_quality()`, `check_station()`, `get_known_recipes()`, `learn_recipe()`
- `world/crafting_definitions.py` — Constants: `RECIPE_REGISTRY`, `QUALITY_TIERS`, `QUALITY_MULTIPLIERS`, `COMMAND_TO_SKILL`, `SKILL_TO_COMMAND`, `STATION_REQUIREMENTS`
- `commands/cmd_crafting.py` — 5 commands: CmdCook, CmdSmith, CmdBrew, CmdCraft, CmdRecipes + `_BaseCraftCmd` shared base class
- `world/models.py` — `CharacterRecipe` (recipe discovery tracking, `learned_from` field)

## Key Concepts
- **Quality tiers:** flawed / standard / fine / superior / masterwork. Gap = `skill_value - difficulty` maps to base tier; random variance ±1 tier (center-biased 20/60/20); station bonus +1 ceiling
- **Quality multipliers:** flawed=0.6, standard=1.0, fine=1.3, superior=1.6, masterwork=2.0 — applied to item effect amounts
- **Station check:** Rooms tagged `crafting_{station}` in category `crafting_station`. Recipe specifies required station
- **Recipe discovery:** `CharacterRecipe` model tracks known recipes. `default_known=True` recipes auto-learned via lazy `_ensure_default_recipes()`
- **_BaseCraftCmd pattern:** Shared base class with `craft_skill`/`craft_verb` overrides. Handles recipe lookup, station check, delay, and move-cancellation
- **Crafting delay:** Uses `evennia.utils.delay()` with `ndb.crafting_in_progress` flag. Cancelled if character moves (room comparison guard)
- **Ingredient matching:** Items matched by `item_tag` category tag on Evennia objects. Consumed (deleted) on successful craft
- **Skill integration:** `craft_item()` calls `get_skill_value()` for quality calc and `accumulate_skill_use()` for passive skill gain

## Critical Rules
1. **Craft delay is in command layer, not engine** — `craft_item()` is called AFTER delay completes. Don't add delay logic to the engine
2. **Recipe lookup is partial-match** — case-insensitive `startswith` on recipe name or id, filtered by command's skill
3. **Station tags use `crafting_station` category** — format: `crafting_{station_name}`. Check via `room.tags.has()`
4. **All engine functions return `(bool, str)`** — follows repo-wide convention. `_check_ingredients` returns `(bool, str, list)` as exception
5. **Lazy recipe seeding** — `_ensure_default_recipes()` called on first recipe query. Idempotent via `get_or_create`
6. **Move cancels crafting** — `_BaseCraftCmd` stores `start_room` and compares in callback. Character movement invalidates in-progress craft

## References
- **Skill Engine:** `world/skill_engine.py` — `get_skill_value()`, `accumulate_skill_use()` for quality and progression
- **Models:** `world/models.py` — `CharacterRecipe` model
- **Item Spawner:** `world/item_spawner.py` — `create_item_from_template()` used by crafted item creation (with fallback)

---
**Last Updated:** 2026-03-27
