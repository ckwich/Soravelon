---
phase: 06c-npc-dialogue-and-crafting
plan: 02
type: execute
wave: 1
depends_on: []
files_modified:
  - world/crafting_definitions.py
  - world/crafting_engine.py
autonomous: true
requirements: [SKL-03]
must_haves:
  truths:
    - "Recipe lookup returns recipe data including required skill, difficulty, ingredients, station, and output"
    - "Quality calculation produces tier from flawed to masterwork based on skill vs difficulty gap"
    - "Craft attempt validates: known recipe, correct station, sufficient ingredients, then produces item with quality"
    - "Recipe discovery tracking uses CharacterRecipe model with default recipes auto-learned"
  artifacts:
    - path: "world/crafting_definitions.py"
      provides: "RECIPE_REGISTRY, QUALITY_TIERS, STATION_REQUIREMENTS, SKILL_TO_COMMAND mapping"
      exports: ["RECIPE_REGISTRY", "QUALITY_TIERS", "STATION_REQUIREMENTS"]
    - path: "world/crafting_engine.py"
      provides: "Crafting logic: quality calc, recipe validation, craft execution, discovery"
      exports: ["craft_item", "learn_recipe", "get_known_recipes", "calculate_craft_quality", "check_station"]
  key_links:
    - from: "world/crafting_engine.py"
      to: "world/skill_engine.py"
      via: "get_skill_value() for quality calculation"
      pattern: "get_skill_value"
    - from: "world/crafting_engine.py"
      to: "world/models.py"
      via: "CharacterRecipe for discovery tracking"
      pattern: "CharacterRecipe"
---

<objective>
Build the crafting data definitions and engine. This creates the recipe registry, quality tier system, station requirements, and all crafting logic (quality calculation, ingredient validation, recipe discovery).

Purpose: Crafting commands (Plan 05) dispatch to this engine. Independent of dialogue system so can be built in parallel.
Output: world/crafting_definitions.py, world/crafting_engine.py
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/06c-npc-dialogue-and-crafting/06c-CONTEXT.md
@.planning/phases/06c-npc-dialogue-and-crafting/06C-RESEARCH.md

@world/skill_engine.py
@world/skill_definitions.py
@world/models.py

<interfaces>
<!-- Key types and contracts the executor needs -->

From world/skill_engine.py:
```python
def get_skill_value(character, skill_id):
    """Get current value (0-100) of a skill. Returns 0.0 for unlearned."""

def accumulate_skill_use(character, skill_id, count=1):
    """Increment ndb accumulator for passive skill gain."""
```

From world/skill_definitions.py:
```python
SKILL_DEFINITIONS = {
    "cooking": {"name": "Cooking", "skill_type": "general", ...},
    "smithing": {"name": "Smithing", "skill_type": "general", ...},
    "alchemy": {"name": "Alchemy", "skill_type": "general", ...},
    "engineering": {"name": "Engineering", "skill_type": "general", ...},
    # ... 21 total skills
}
```

CharacterRecipe model (created in Plan 01, but can be built against the interface):
```python
class CharacterRecipe(models.Model):
    character = ForeignKey("objects.ObjectDB", CASCADE, related_name="known_recipes")
    recipe_id = CharField(max_length=128)
    learned_from = CharField(max_length=64, blank=True, default="")
    learned_at = DateTimeField(auto_now_add=True)
    # unique_together = ("character", "recipe_id")
```
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Crafting definitions registry</name>
  <files>world/crafting_definitions.py</files>
  <action>
Create world/crafting_definitions.py as a pure-data module (no Django imports). Per D-15, D-16, D-17, D-18, D-19 and research Pattern 5/6.

**QUALITY_TIERS** — ordered list: ["flawed", "standard", "fine", "superior", "masterwork"]

**STATION_REQUIREMENTS** — dict mapping station type to description string:
```python
STATION_REQUIREMENTS = {
    "campfire": "a campfire or cooking hearth",
    "forge": "a smithing forge",
    "alchemy_bench": "an alchemist's workbench",
    "workbench": "an engineering workbench",
}
```

**SKILL_TO_COMMAND** — maps skill_id to the command verb:
```python
SKILL_TO_COMMAND = {
    "cooking": "cook",
    "smithing": "smith",
    "alchemy": "brew",
    "engineering": "craft",
}
COMMAND_TO_SKILL = {v: k for k, v in SKILL_TO_COMMAND.items()}
```

**RECIPE_REGISTRY** — dict keyed by recipe_id. Per research Example 4. Include 6-8 starter recipes across the three professions (D-17):

Cooking (campfire station, cooking skill):
- "trail_rations" — difficulty 10, raw_meat + wild_herb, output: consumable hp_regen, default_known=True
- "hearty_stew" — difficulty 25, raw_meat x2 + root_vegetable + clean_water, output: consumable stamina_regen, default_known=True
- "spiced_fish" — difficulty 40, raw_fish + wild_herb + spice, output: consumable stat_buff, default_known=False

Smithing (forge station, smithing skill):
- "iron_dagger" — difficulty 20, iron_ingot x2, output: weapon, default_known=True
- "iron_chainmail" — difficulty 40, iron_ingot x4 + leather_strip x2, output: armor, default_known=False

Alchemy (alchemy_bench station, alchemy skill):
- "basic_healing_draught" — difficulty 20, thornroot x2 + clean_water, output: consumable instant_heal, default_known=True
- "antidote" — difficulty 30, thornroot + nightpetal + clean_water, output: consumable cure_poison, default_known=False
- "stamina_tonic" — difficulty 35, ironbark_sap + clean_water + spice, output: consumable stamina_restore, default_known=False

Each recipe entry has:
```python
{
    "name": "Display Name",
    "skill": "cooking",          # skill_id from SKILL_DEFINITIONS
    "difficulty": 10,            # 0-100
    "station": "campfire",       # key in STATION_REQUIREMENTS
    "ingredients": [
        {"item_tag": "raw_meat", "quantity": 1},
    ],
    "output": {
        "template_id": "trail_rations",  # for item_spawner
        "base_item_type": "consumable",
        "quality_affects": "effect_amount",  # what quality modifies
    },
    "default_known": True,       # auto-learned by all characters
    "command": "cook",           # which command verb to use
    "craft_time": 3,             # seconds delay (Claude's discretion: short delay for immersion)
    "craft_echo": "You tend the fire, turning the food carefully...",
}
```

NOTE per D-18: Engineering (craft) skill is SEPARATE from Engineering domain. The engineering recipes use the "engineering" general proficiency skill, NOT the Engineering domain score.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "from world.crafting_definitions import RECIPE_REGISTRY, QUALITY_TIERS, STATION_REQUIREMENTS, SKILL_TO_COMMAND; assert len(RECIPE_REGISTRY) >= 6; assert len(QUALITY_TIERS) == 5; print(f'{len(RECIPE_REGISTRY)} recipes, {len(QUALITY_TIERS)} quality tiers')"</automated>
  </verify>
  <done>RECIPE_REGISTRY has 6+ starter recipes across cooking/smithing/alchemy. QUALITY_TIERS, STATION_REQUIREMENTS, SKILL_TO_COMMAND all exported.</done>
</task>

<task type="auto">
  <name>Task 2: Crafting engine</name>
  <files>world/crafting_engine.py</files>
  <action>
Create world/crafting_engine.py following the thin-engine pattern. All functions use lazy imports. Follow `(bool, str)` return tuple pattern for functions that can fail.

Functions to implement:

1. `calculate_craft_quality(skill_value, recipe_difficulty, has_station_bonus=False)` — Per research Pattern 5. Compute quality tier from skill vs difficulty gap with random variance (+/- 1 tier, weighted center). Station bonus adds +1 ceiling. Returns quality tier string from QUALITY_TIERS.

2. `check_station(character, required_station)` — Per research Pattern 6. Check character's room for tag `crafting_{station}` in category `crafting_station`. Returns `(bool, str)`.

3. `get_known_recipes(character, skill_filter=None)` — Query CharacterRecipe model for character. If skill_filter provided, only return recipes for that skill. Also include default_known recipes from RECIPE_REGISTRY even if no CharacterRecipe record exists. Returns list of recipe dicts from RECIPE_REGISTRY.

4. `learn_recipe(character, recipe_id, learned_from="")` — Create CharacterRecipe record via get_or_create. Returns `(bool, str)`. If already known, return (False, "You already know that recipe.").

5. `_ensure_default_recipes(character)` — Called lazily on first craft/recipe check. For each recipe with default_known=True in RECIPE_REGISTRY, create CharacterRecipe via get_or_create with learned_from="default". Idempotent.

6. `_check_ingredients(character, recipe)` — Check character's inventory for required ingredients by item_tag. Uses Evennia's `character.contents` and `obj.tags.has(item_tag, category="item_tag")`. Returns `(bool, str, list_of_items)` where list_of_items are the matched inventory objects to consume.

7. `_consume_ingredients(items_to_consume)` — Delete the matched inventory item objects (call `obj.delete()` on each). This removes them from the game world.

8. `_create_crafted_item(character, recipe, quality)` — Use lazy import of `item_spawner.create_item_from_template` to create the output item. Apply quality modifier to item name/description. Place item in character's inventory. Returns the created item or None.

9. `craft_item(character, recipe_id)` — Main entry point per D-15, D-19. Validates:
   - Recipe exists in RECIPE_REGISTRY
   - Character knows the recipe (check CharacterRecipe or default_known)
   - Correct station present in room (check_station)
   - Character has required ingredients (_check_ingredients)
   - Then: calculate quality from skill_value vs difficulty, consume ingredients, create item, accumulate_skill_use for passive skill gain.
   Returns `(bool, str)`. On success, the string includes quality and item name with color codes.
   The craft_time delay is NOT handled here — the command layer will use `utils.delay()` before calling this.

10. `get_quality_modifier(quality_tier)` — Return a multiplier for item effect amounts based on quality:
    - flawed: 0.6, standard: 1.0, fine: 1.3, superior: 1.6, masterwork: 2.0

All error messages use Evennia color codes per project convention.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "from world.crafting_engine import craft_item, learn_recipe, get_known_recipes, calculate_craft_quality, check_station, get_quality_modifier; print('All imports OK')"</automated>
  </verify>
  <done>crafting_engine.py exports all 10 functions. calculate_craft_quality produces correct tiers. craft_item validates recipe, station, ingredients, skill, and produces item with quality. All follow (bool, str) pattern.</done>
</task>

</tasks>

<verification>
- `from world.crafting_definitions import RECIPE_REGISTRY` succeeds with 6+ recipes
- `from world.crafting_engine import craft_item, calculate_craft_quality` succeeds
- No circular imports on any import chain
- calculate_craft_quality(80, 20) returns "superior" or "masterwork" (high skill vs low difficulty)
- calculate_craft_quality(10, 60) returns "flawed" (low skill vs high difficulty)
</verification>

<success_criteria>
- RECIPE_REGISTRY has starter recipes for cooking, smithing, and alchemy per D-17
- Quality calculation produces correct tier gradient from skill gap
- Station check uses room tags per established convention
- Recipe discovery uses CharacterRecipe model (not db attributes) per Pitfall 7
- All functions use lazy imports and follow project conventions
</success_criteria>

<output>
After completion, create `.planning/phases/06c-npc-dialogue-and-crafting/06c-02-SUMMARY.md`
</output>
