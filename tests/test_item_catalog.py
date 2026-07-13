"""Contract tests for the canonical item catalog."""

import unittest

from world.crafting_definitions import RECIPE_REGISTRY
from world.item_catalog import CATALOG, ItemTemplateNotFound, get_item_template


_REQUIRED_TEMPLATE_FIELDS = {
    "item_id",
    "key",
    "item_type",
    "weight",
    "rarity",
    "value",
    "desc",
}


class TestCraftingOutputCatalogContracts(unittest.TestCase):
    """Every standard recipe resolves to a mechanically complete template."""

    def test_every_non_processing_recipe_resolves_to_complete_template(self):
        for recipe_id, recipe in RECIPE_REGISTRY.items():
            if recipe.get("recipe_type") == "processing":
                continue

            output = recipe["output"]
            template_id = output["template_id"]
            with self.subTest(recipe_id=recipe_id, template_id=template_id):
                template = get_item_template(template_id)
                self.assertIsNotNone(template)
                self.assertFalse(
                    _REQUIRED_TEMPLATE_FIELDS - set(template),
                    f"{template_id} is missing required template fields",
                )
                self.assertEqual(template["item_id"], template_id)

    def test_recipe_outputs_are_mechanically_valid_for_their_authored_kind(self):
        for recipe_id, recipe in RECIPE_REGISTRY.items():
            if recipe.get("recipe_type") == "processing":
                continue

            output = recipe["output"]
            template = get_item_template(output["template_id"])
            authored_kind = output["base_item_type"]
            with self.subTest(recipe_id=recipe_id, authored_kind=authored_kind):
                if authored_kind == "weapon":
                    self.assertEqual(template["item_type"], "equipment")
                    self.assertEqual(template.get("equip_slot"), "main_hand")
                    self.assertGreater(template.get("damage_min", 0), 0)
                    self.assertGreaterEqual(
                        template.get("damage_max", 0), template["damage_min"]
                    )
                    self.assertIn("scaling_stat", template)
                elif authored_kind == "armor":
                    self.assertEqual(template["item_type"], "equipment")
                    self.assertIn(template.get("equip_slot"), {
                        "head", "face", "chest", "back", "hands", "wrists",
                        "legs", "feet", "off_hand", "ring1", "amulet",
                    })
                    self.assertGreater(template.get("armor_value", 0), 0)
                elif authored_kind == "consumable":
                    self.assertEqual(template["item_type"], "consumable")
                    effect = template.get("use_effect")
                    self.assertIsInstance(effect, dict)
                    self.assertTrue(effect.get("type"))
                else:
                    self.fail(f"Unsupported authored output kind: {authored_kind}")

    def test_quality_affects_names_a_real_scalable_mechanic(self):
        for recipe_id, recipe in RECIPE_REGISTRY.items():
            if recipe.get("recipe_type") == "processing":
                continue
            output = recipe["output"]
            template = get_item_template(output["template_id"])
            quality_affects = output.get("quality_affects")
            with self.subTest(recipe_id=recipe_id, quality_affects=quality_affects):
                self.assertIn(
                    quality_affects,
                    {"damage", "armor_value", "effect_amount", None},
                )
                if quality_affects == "damage":
                    self.assertGreater(template.get("damage_min", 0), 0)
                    self.assertGreaterEqual(
                        template.get("damage_max", 0),
                        template["damage_min"],
                    )
                elif quality_affects == "armor_value":
                    self.assertGreater(template.get("armor_value", 0), 0)
                elif quality_affects == "effect_amount":
                    effect = template.get("use_effect") or {}
                    self.assertTrue(
                        any(
                            isinstance(effect.get(field), (int, float))
                            for field in ("amount", "hp", "stamina")
                        ),
                        f"{recipe_id} declares effect_amount without a numeric effect",
                    )

    def test_lookup_returns_an_isolated_copy(self):
        template = get_item_template("iron_dagger")
        template["key"] = "mutated"
        template["stat_bonuses"]["agility"] = 99

        self.assertEqual(CATALOG["iron_dagger"]["key"], "Iron Dagger")
        self.assertEqual(CATALOG["iron_dagger"]["stat_bonuses"]["agility"], 1)

    def test_unknown_template_fails_loudly(self):
        with self.assertRaises(ItemTemplateNotFound):
            get_item_template("not_a_real_item")


if __name__ == "__main__":
    unittest.main()
