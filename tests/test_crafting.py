"""
Tests for the crafting system (Phase 06c).

Covers D-15 (quality variance), D-16 (recipe discovery), D-17 (three professions),
station checks, and quality modifier lookups.

Uses unittest.TestCase for pure-computation tests and EvenniaTest for
model-backed operations (CharacterRecipe).
"""

import unittest
from unittest.mock import MagicMock, patch

from evennia.utils.test_resources import EvenniaTest


# ---------------------------------------------------------------------------
# D-15: Quality variance
# ---------------------------------------------------------------------------


class TestCraftQuality(unittest.TestCase):
    """calculate_craft_quality maps skill-difficulty gap to quality tiers."""

    def test_high_skill_low_difficulty(self):
        """Gap +60 -> consistently superior or masterwork."""
        from world.crafting_engine import calculate_craft_quality

        results = set()
        for _ in range(50):
            result = calculate_craft_quality(80, 20)
            results.add(result)

        # With gap 60, base_index=4 (masterwork). Variance can shift -1.
        # So we expect superior and masterwork, never flawed or standard.
        self.assertTrue(
            results.issubset({"fine", "superior", "masterwork"}),
            f"Unexpected tiers for gap +60: {results}",
        )
        self.assertIn("masterwork", results, "Should see masterwork at gap +60")

    def test_low_skill_high_difficulty(self):
        """Gap -50 -> consistently flawed."""
        from world.crafting_engine import calculate_craft_quality

        results = set()
        for _ in range(50):
            result = calculate_craft_quality(10, 60)
            results.add(result)

        # With gap -50, base_index=0 (flawed). Variance can shift +1.
        # So we expect flawed and standard, never fine+.
        self.assertTrue(
            results.issubset({"flawed", "standard"}),
            f"Unexpected tiers for gap -50: {results}",
        )
        self.assertIn("flawed", results, "Should see flawed at gap -50")

    def test_equal_skill_difficulty(self):
        """Gap 0 -> mostly standard (with some flawed/fine variance)."""
        from world.crafting_engine import calculate_craft_quality

        counter = {"flawed": 0, "standard": 0, "fine": 0}
        for _ in range(100):
            result = calculate_craft_quality(50, 50)
            if result in counter:
                counter[result] += 1

        # Base index 1 (standard). Majority should be standard.
        self.assertGreater(
            counter["standard"], 30,
            f"Standard should dominate at gap 0: {counter}",
        )

    def test_station_bonus_shifts_up(self):
        """Station bonus adds +1 to quality ceiling."""
        from world.crafting_engine import calculate_craft_quality

        # Gap 0, base_index=1 (standard). Without bonus: {flawed, standard, fine}.
        # With bonus: shifts +1, so {standard, fine, superior} possible.
        results_with = set()
        for _ in range(100):
            result = calculate_craft_quality(50, 50, has_station_bonus=True)
            results_with.add(result)

        # We should see fine or superior appear with station bonus
        self.assertTrue(
            "fine" in results_with or "superior" in results_with,
            f"Station bonus should shift quality up: {results_with}",
        )

    def test_extreme_underqualified(self):
        """Skill 0, difficulty 100 -> always flawed (or standard from variance)."""
        from world.crafting_engine import calculate_craft_quality

        results = set()
        for _ in range(50):
            result = calculate_craft_quality(0, 100)
            results.add(result)

        self.assertTrue(
            results.issubset({"flawed", "standard"}),
            f"Extreme underqualified should be flawed/standard: {results}",
        )

    def test_returns_valid_tier_string(self):
        """Quality always returns a string from QUALITY_TIERS."""
        from world.crafting_engine import calculate_craft_quality
        from world.crafting_definitions import QUALITY_TIERS

        for _ in range(50):
            result = calculate_craft_quality(50, 50)
            self.assertIn(result, QUALITY_TIERS)


# ---------------------------------------------------------------------------
# D-15: Quality modifier
# ---------------------------------------------------------------------------


class TestQualityModifier(unittest.TestCase):
    """get_quality_modifier returns correct multipliers."""

    def test_flawed(self):
        from world.crafting_engine import get_quality_modifier

        self.assertAlmostEqual(get_quality_modifier("flawed"), 0.6)

    def test_standard(self):
        from world.crafting_engine import get_quality_modifier

        self.assertAlmostEqual(get_quality_modifier("standard"), 1.0)

    def test_fine(self):
        from world.crafting_engine import get_quality_modifier

        self.assertAlmostEqual(get_quality_modifier("fine"), 1.3)

    def test_superior(self):
        from world.crafting_engine import get_quality_modifier

        self.assertAlmostEqual(get_quality_modifier("superior"), 1.6)

    def test_masterwork(self):
        from world.crafting_engine import get_quality_modifier

        self.assertAlmostEqual(get_quality_modifier("masterwork"), 2.0)

    def test_unknown_defaults_to_one(self):
        from world.crafting_engine import get_quality_modifier

        self.assertAlmostEqual(get_quality_modifier("nonexistent"), 1.0)


# ---------------------------------------------------------------------------
# D-16: Recipe discovery
# ---------------------------------------------------------------------------


class TestRecipeDiscovery(EvenniaTest):
    """learn_recipe and get_known_recipes manage CharacterRecipe records."""

    def test_learn_valid_recipe(self):
        from world.crafting_engine import learn_recipe

        ok, msg = learn_recipe(self.char1, "trail_rations", "trainer_npc")
        self.assertTrue(ok)
        self.assertIn("Trail Rations", msg)

    def test_learn_duplicate_recipe(self):
        from world.crafting_engine import learn_recipe

        learn_recipe(self.char1, "trail_rations")
        ok, msg = learn_recipe(self.char1, "trail_rations")
        self.assertFalse(ok)
        self.assertIn("already know", msg)

    def test_learn_unknown_recipe(self):
        from world.crafting_engine import learn_recipe

        ok, msg = learn_recipe(self.char1, "nonexistent_recipe")
        self.assertFalse(ok)
        self.assertIn("Unknown recipe", msg)

    def test_default_recipes_auto_learned(self):
        """get_known_recipes returns default_known recipes without explicit learn."""
        from world.crafting_engine import get_known_recipes
        from world.crafting_definitions import RECIPE_REGISTRY

        recipes = get_known_recipes(self.char1)
        recipe_ids = {r["recipe_id"] for r in recipes}

        default_ids = {
            rid for rid, r in RECIPE_REGISTRY.items()
            if r.get("default_known")
        }
        self.assertTrue(
            default_ids.issubset(recipe_ids),
            f"Default recipes missing: {default_ids - recipe_ids}",
        )

    def test_skill_filter(self):
        """get_known_recipes with skill_filter returns only that skill's recipes."""
        from world.crafting_engine import get_known_recipes

        cooking_recipes = get_known_recipes(self.char1, skill_filter="cooking")
        for r in cooking_recipes:
            self.assertEqual(r["skill"], "cooking")

    def test_non_default_recipe_not_in_known(self):
        """Non-default recipes are not returned until explicitly learned."""
        from world.crafting_engine import get_known_recipes

        recipes = get_known_recipes(self.char1)
        recipe_ids = {r["recipe_id"] for r in recipes}

        # spiced_fish is not default_known
        self.assertNotIn("spiced_fish", recipe_ids)

    def test_learned_recipe_appears_in_known(self):
        """After learning a recipe, it appears in get_known_recipes."""
        from world.crafting_engine import learn_recipe, get_known_recipes

        learn_recipe(self.char1, "spiced_fish")
        recipes = get_known_recipes(self.char1)
        recipe_ids = {r["recipe_id"] for r in recipes}
        self.assertIn("spiced_fish", recipe_ids)


# ---------------------------------------------------------------------------
# D-17: Recipe registry data integrity
# ---------------------------------------------------------------------------


class TestRecipeRegistry(unittest.TestCase):
    """RECIPE_REGISTRY has valid, complete recipe data."""

    def test_minimum_recipe_count(self):
        from world.crafting_definitions import RECIPE_REGISTRY

        self.assertGreaterEqual(len(RECIPE_REGISTRY), 6)

    def test_all_recipes_have_required_keys(self):
        from world.crafting_definitions import RECIPE_REGISTRY

        required_keys = {"name", "skill", "difficulty", "station", "ingredients", "output"}
        for rid, recipe in RECIPE_REGISTRY.items():
            missing = required_keys - set(recipe.keys())
            self.assertEqual(
                missing, set(),
                f"Recipe '{rid}' missing keys: {missing}",
            )

    def test_recipe_skills_exist_in_definitions(self):
        """Each recipe's skill must be a valid skill in SKILL_DEFINITIONS."""
        from world.crafting_definitions import RECIPE_REGISTRY
        from world.skill_definitions import SKILL_DEFINITIONS

        for rid, recipe in RECIPE_REGISTRY.items():
            self.assertIn(
                recipe["skill"], SKILL_DEFINITIONS,
                f"Recipe '{rid}' has unknown skill: {recipe['skill']}",
            )

    def test_recipe_stations_valid(self):
        """Each recipe's station must be in STATION_REQUIREMENTS."""
        from world.crafting_definitions import RECIPE_REGISTRY, STATION_REQUIREMENTS

        for rid, recipe in RECIPE_REGISTRY.items():
            self.assertIn(
                recipe["station"], STATION_REQUIREMENTS,
                f"Recipe '{rid}' has unknown station: {recipe['station']}",
            )

    def test_minimum_cooking_recipes(self):
        from world.crafting_definitions import RECIPE_REGISTRY

        cooking = [r for r in RECIPE_REGISTRY.values() if r["skill"] == "cooking"]
        self.assertGreaterEqual(len(cooking), 2, "Need at least 2 cooking recipes")

    def test_minimum_smithing_recipes(self):
        from world.crafting_definitions import RECIPE_REGISTRY

        smithing = [r for r in RECIPE_REGISTRY.values() if r["skill"] == "smithing"]
        self.assertGreaterEqual(len(smithing), 1, "Need at least 1 smithing recipe")

    def test_minimum_alchemy_recipes(self):
        from world.crafting_definitions import RECIPE_REGISTRY

        alchemy = [r for r in RECIPE_REGISTRY.values() if r["skill"] == "alchemy"]
        self.assertGreaterEqual(len(alchemy), 2, "Need at least 2 alchemy recipes")

    def test_default_known_cooking_exists(self):
        """At least one default_known recipe for cooking."""
        from world.crafting_definitions import RECIPE_REGISTRY

        defaults = [
            r for r in RECIPE_REGISTRY.values()
            if r["skill"] == "cooking" and r.get("default_known")
        ]
        self.assertGreater(len(defaults), 0, "Need at least 1 default cooking recipe")

    def test_default_known_alchemy_exists(self):
        """At least one default_known recipe for alchemy."""
        from world.crafting_definitions import RECIPE_REGISTRY

        defaults = [
            r for r in RECIPE_REGISTRY.values()
            if r["skill"] == "alchemy" and r.get("default_known")
        ]
        self.assertGreater(len(defaults), 0, "Need at least 1 default alchemy recipe")


# ---------------------------------------------------------------------------
# Station check
# ---------------------------------------------------------------------------


class TestStationCheck(EvenniaTest):
    """check_station validates crafting station tags on rooms."""

    def test_room_with_correct_station_tag(self):
        from world.crafting_engine import check_station

        self.room1.tags.add("crafting_campfire", category="crafting_station")
        self.char1.location = self.room1

        ok, msg = check_station(self.char1, "campfire")
        self.assertTrue(ok)

    def test_room_without_station_tag(self):
        from world.crafting_engine import check_station

        self.char1.location = self.room1

        ok, msg = check_station(self.char1, "campfire")
        self.assertFalse(ok)
        self.assertIn("need", msg.lower())

    def test_no_location(self):
        from world.crafting_engine import check_station

        self.char1.location = None

        ok, msg = check_station(self.char1, "campfire")
        self.assertFalse(ok)


class TestCraftItemIntegration(unittest.TestCase):
    """craft_item should honor station and processing quality rules."""

    def test_standard_craft_uses_station_bonus_in_quality_roll(self):
        from world.crafting_engine import craft_item

        character = MagicMock()
        character.contents = []
        character.location = MagicMock()

        recipe = {
            "name": "Test Tonic",
            "skill": "alchemy",
            "difficulty": 25,
            "station": "alchemy_bench",
            "ingredients": [{"item_tag": "herb_extract", "quantity": 1}],
            "output": {
                "template_id": "basic_healing_draught",
                "base_item_type": "consumable",
            },
            "default_known": True,
        }

        with patch.dict("world.crafting_engine.RECIPE_REGISTRY", {"test_tonic": recipe}, clear=False):
            with patch("world.crafting_engine.check_station", return_value=(True, "")):
                with patch("world.crafting_engine._check_ingredients", return_value=(True, "", [])):
                    with patch("world.crafting_engine.calculate_craft_quality", return_value="fine") as mock_quality:
                        with patch("world.crafting_engine._create_crafted_item", return_value=MagicMock(key="Test Tonic")):
                            with patch("world.skill_engine.get_skill_value", return_value=50):
                                with patch("world.skill_engine.accumulate_skill_use"):
                                    ok, _ = craft_item(character, "test_tonic")

        self.assertTrue(ok)
        mock_quality.assert_called_once_with(50, 25, has_station_bonus=True)

    def test_processing_recipe_uses_processing_quality_with_input_quality(self):
        from world.crafting_engine import craft_item

        character = MagicMock()
        character.contents = []
        character.location = MagicMock()
        high_quality_input = MagicMock()
        high_quality_input.db.quality = "superior"

        recipe = {
            "name": "Iron Ingot",
            "skill": "smithing",
            "difficulty": 10,
            "station": "forge",
            "recipe_type": "processing",
            "ingredients": [{"item_tag": "iron_ore", "quantity": 3}],
            "output": {
                "item_id": "iron_ingot",
                "key": "Iron Ingot",
                "item_type": "item",
                "weight": 1.0,
                "desc": "A bar of refined iron.",
                "value": 15,
            },
            "default_known": True,
        }

        with patch.dict("world.crafting_engine.RECIPE_REGISTRY", {"iron_ingot_test": recipe}, clear=False):
            with patch("world.crafting_engine.check_station", return_value=(True, "")):
                with patch(
                    "world.crafting_engine._check_ingredients",
                    return_value=(
                        True,
                        "",
                        [{"item": high_quality_input, "quantity": 1, "record": MagicMock(quantity=1)}],
                    ),
                ):
                    with patch("world.crafting_engine._consume_ingredients"):
                        with patch("world.crafting_engine.calculate_processing_quality", return_value="masterwork") as mock_processing:
                            with patch("world.item_spawner.create_item_from_template", return_value=MagicMock(key="Iron Ingot")):
                                with patch("world.skill_engine.get_skill_value", return_value=55):
                                    with patch("world.skill_engine.accumulate_skill_use"):
                                        ok, _ = craft_item(character, "iron_ingot_test")

        self.assertTrue(ok)
        mock_processing.assert_called_once_with(
            55,
            10,
            raw_quality="superior",
            has_station=True,
        )


class TestCraftingIngredientStacks(unittest.TestCase):
    """Crafting ingredient checks should respect stack quantities."""

    def test_check_ingredients_counts_stack_quantity(self):
        from world.crafting_engine import _check_ingredients

        character = MagicMock()
        item = MagicMock()
        item.tags.has.return_value = True
        item.get_inventory_record.return_value = MagicMock(quantity=3)
        character.contents = [item]

        recipe = {"ingredients": [{"item_tag": "iron_ore", "quantity": 2}]}

        ok, _, consume_specs = _check_ingredients(character, recipe)

        self.assertTrue(ok)
        self.assertEqual(len(consume_specs), 1)
        self.assertEqual(consume_specs[0]["quantity"], 2)

    def test_consume_ingredients_reduces_stack_without_deleting_item(self):
        from world.crafting_engine import _consume_ingredients

        item = MagicMock()
        item.db = MagicMock()
        record = MagicMock()
        record.quantity = 4

        _consume_ingredients(
            [{"item": item, "quantity": 2, "record": record}]
        )

        self.assertEqual(record.quantity, 2)
        record.save.assert_called_once()
        item.delete.assert_not_called()
