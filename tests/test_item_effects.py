"""Behavior tests for starter consumables."""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


class TestStarterHealingPotion(unittest.TestCase):
    def test_every_starter_potion_is_a_real_consumable_that_heals(self):
        from world.ancestry_engine import STARTER_KITS
        from world.item_catalog import get_item_template
        from world.item_effects import consume_item

        for ancestry_id, template_ids in STARTER_KITS.items():
            potion_ids = [
                template_id
                for template_id in template_ids
                if template_id == "minor_healing_potion"
            ]
            with self.subTest(ancestry_id=ancestry_id):
                self.assertEqual(len(potion_ids), 2)
                template = get_item_template(potion_ids[0])
                self.assertEqual(template["item_type"], "consumable")
                self.assertEqual(template["use_effect"]["type"], "heal_hp")

                character = SimpleNamespace(
                    db=SimpleNamespace(
                        base_stats={"endurance": 10},
                        backend_level=1,
                    ),
                    ndb=SimpleNamespace(
                        in_combat=False,
                        hp=10,
                        stamina=30,
                    ),
                )
                item = MagicMock()
                item.key = template["key"]
                item.db = SimpleNamespace(
                    use_effect=template["use_effect"],
                    action_cost=1,
                )

                with patch("world.item_effects._destroy") as mock_destroy:
                    ok, message = consume_item(character, item)

                self.assertTrue(ok, message)
                self.assertEqual(character.ndb.hp, 40)
                mock_destroy.assert_called_once_with(character, item)


if __name__ == "__main__":
    unittest.main()
