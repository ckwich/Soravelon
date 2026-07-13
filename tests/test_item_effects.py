"""Behavior tests for starter consumables."""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from evennia.utils.test_resources import EvenniaTest

from world.models import InventoryItem


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


def _effect_character(*, hp=20, stamina=20, in_combat=False, actions=2):
    return SimpleNamespace(
        id=7,
        key="Tester",
        location=None,
        db=SimpleNamespace(
            base_stats={"endurance": 10},
            backend_level=1,
            immunities=[],
        ),
        ndb=SimpleNamespace(
            in_combat=in_combat,
            actions_remaining=actions,
            hp=hp,
            stamina=stamina,
            active_effects=[],
        ),
    )


def _effect_item(effect, *, action_cost=1, key="Test Item"):
    item = MagicMock()
    item.key = key
    item.db = SimpleNamespace(use_effect=effect, action_cost=action_cost)
    return item


class TestAuthoritativeConsumableEffects(unittest.TestCase):
    def test_unknown_effect_fails_without_item_or_action_cost(self):
        from world.item_effects import consume_item

        character = _effect_character(in_combat=True, actions=2)
        item = _effect_item({"type": "wish_for_health"})

        with patch("world.item_effects._destroy") as destroy:
            ok, message = consume_item(character, item)

        self.assertFalse(ok)
        self.assertIn("cannot be used", message.lower())
        self.assertEqual(character.ndb.actions_remaining, 2)
        destroy.assert_not_called()

    def test_bait_without_use_effect_is_fishing_only(self):
        from world.item_effects import consume_item

        character = _effect_character(in_combat=True, actions=2)
        item = _effect_item(None, key="Fishing Bait")

        with patch("world.item_effects._destroy") as destroy:
            ok, message = consume_item(character, item)

        self.assertFalse(ok)
        self.assertIn("fishing", message.lower())
        self.assertEqual(character.ndb.actions_remaining, 2)
        destroy.assert_not_called()

    def test_heal_over_time_uses_canonical_regeneration_ticks(self):
        from world.item_effects import consume_item
        from world.status_effects import has_effect, tick_effects

        character = _effect_character(hp=20)
        item = _effect_item({"type": "heal_over_time", "amount": 7, "ticks": 2})

        with patch("world.item_effects._destroy"):
            ok, message = consume_item(character, item)

        self.assertTrue(ok, message)
        self.assertTrue(has_effect(character, "regeneration"))
        tick_effects(character)
        self.assertEqual(character.ndb.hp, 27)

    def test_antidote_removes_poison_from_canonical_active_effects(self):
        from world.item_effects import consume_item
        from world.status_effects import apply_effect, has_effect

        character = _effect_character()
        apply_effect(character, "poison", duration=3, source_id=99)
        item = _effect_item({"type": "cure_poison"}, key="Antidote")

        with patch("world.item_effects._destroy"):
            ok, message = consume_item(character, item)

        self.assertTrue(ok, message)
        self.assertFalse(has_effect(character, "poison"))

    def test_antidote_without_poison_is_not_wasted(self):
        from world.item_effects import consume_item

        character = _effect_character()
        item = _effect_item({"type": "cure_poison"}, key="Antidote")

        with patch("world.item_effects._destroy") as destroy:
            ok, message = consume_item(character, item)

        self.assertFalse(ok)
        self.assertIn("not poisoned", message.lower())
        destroy.assert_not_called()

    def test_failed_inventory_consumption_rolls_back_effect_and_action(self):
        from world.item_effects import consume_item

        character = _effect_character(hp=20, in_combat=True, actions=2)
        item = _effect_item({"type": "heal_hp", "amount": 30})

        with patch(
            "world.item_effects._destroy",
            side_effect=RuntimeError("ownership changed"),
        ):
            ok, message = consume_item(character, item)

        self.assertFalse(ok)
        self.assertIn("ownership changed", message)
        self.assertEqual(character.ndb.hp, 20)
        self.assertEqual(character.ndb.actions_remaining, 2)


class TestConsumableInventoryAuthority(EvenniaTest):
    def test_using_one_consumable_decrements_a_real_stack(self):
        from world.item_effects import consume_item
        from world.item_spawner import create_item_from_catalog

        item = create_item_from_catalog(
            "basic_healing_draught",
            location=self.char1,
        )
        record = InventoryItem.objects.get(
            character_id=self.char1.id,
            item_id=item.id,
        )
        record.quantity = 2
        record.save(update_fields=["quantity"])
        self.char1.db.base_stats = {"endurance": 10}
        self.char1.db.backend_level = 1
        self.char1.ndb.in_combat = False
        self.char1.ndb.hp = 10

        with patch("world.oob_publisher.push_inventory_update"):
            self.assertEqual(
                item.db.use_effect,
                {"type": "heal_hp", "amount": 25},
            )
            ok, message = consume_item(self.char1, item)

        self.assertTrue(ok, message)
        self.assertEqual(self.char1.ndb.hp, 35)
        self.assertEqual(
            InventoryItem.objects.get(
                character_id=self.char1.id,
                item_id=item.id,
            ).quantity,
            1,
        )
        item.refresh_from_db()
        self.assertEqual(item.location, self.char1)


if __name__ == "__main__":
    unittest.main()
