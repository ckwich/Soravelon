"""Atomic and exactly-once contracts for cross-system economy workflows."""

from types import SimpleNamespace
from unittest.mock import patch

from evennia import create_object
from evennia.objects.models import ObjectDB
from evennia.utils.test_resources import EvenniaTest

from world.models import (
    BankTransaction,
    GameOperation,
    InventoryItem,
)


class CompositeEconomyTestBase(EvenniaTest):
    def setUp(self):
        super().setUp()
        from typeclasses.mobs import SoravelonMob
        from typeclasses.rooms import SoravelonRoom

        self.room = create_object(SoravelonRoom, key="Composite Economy Room")
        self.char1.location = self.room
        self.char1.db.carried_scales = 100
        self.vendor = create_object(
            SoravelonMob,
            key="Composite Vendor",
            location=self.room,
        )
        self.vendor.db.is_vendor = True
        self.vendor.db.vendor_accepts = ["equipment", "consumable", "item"]
        self.vendor.db.vendor_faction = None
        self.vendor.db.vendor_item_ids = ["iron_dagger"]
        self.vendor.db.vendor_exclude_item_ids = []
        self.vendor.db.player_stock = {}

    @staticmethod
    def fail_at(expected_checkpoint):
        def _fail(checkpoint):
            if checkpoint == expected_checkpoint:
                raise RuntimeError(f"injected failure at {checkpoint}")

        return _fail


class TestAtomicVendorBuy(CompositeEconomyTestBase):
    def test_spawn_failure_does_not_charge_or_consume_player_stock(self):
        from world.vendor_engine import buy_item

        self.vendor.db.player_stock = {
            "used_dagger": {
                "item_id": "used_dagger",
                "key": "Used Dagger",
                "item_type": "equipment",
                "value": 15,
                "stock_quantity": 1,
            }
        }
        with patch(
            "world.vendor_engine.create_item_from_template",
            side_effect=RuntimeError("spawn failed"),
        ), self.assertRaisesRegex(RuntimeError, "spawn failed"):
            buy_item(
                self.char1,
                self.vendor,
                "used_dagger",
                operation_id="vendor-buy:spawn-failure",
            )

        self.assertEqual(self.char1.db.carried_scales, 100)
        self.assertIn("used_dagger", self.vendor.db.player_stock)
        self.assertFalse(
            GameOperation.objects.filter(
                operation_id="vendor-buy:spawn-failure"
            ).exists()
        )

    def test_failure_after_spawn_rolls_back_item_currency_and_receipt(self):
        from world.vendor_engine import buy_item

        original_object_ids = set(ObjectDB.objects.values_list("id", flat=True))
        for checkpoint in ("purchase_item_spawned", "operation_recorded"):
            with self.subTest(checkpoint=checkpoint):
                with patch(
                    "world.vendor_engine._after_write",
                    side_effect=self.fail_at(checkpoint),
                ), self.assertRaisesRegex(RuntimeError, checkpoint):
                    buy_item(
                        self.char1,
                        self.vendor,
                        "iron_dagger",
                        operation_id=f"vendor-buy:{checkpoint}",
                    )

                self.assertEqual(self.char1.db.carried_scales, 100)
                self.assertEqual(
                    set(ObjectDB.objects.values_list("id", flat=True)),
                    original_object_ids,
                )
                self.assertFalse(GameOperation.objects.exists())

    def test_same_buy_operation_charges_and_spawns_once(self):
        from world.vendor_engine import buy_item

        first = buy_item(
            self.char1,
            self.vendor,
            "iron_dagger",
            operation_id="vendor-buy:exactly-once",
        )
        second = buy_item(
            self.char1,
            self.vendor,
            "iron_dagger",
            operation_id="vendor-buy:exactly-once",
        )

        self.assertTrue(first[0], first[1])
        self.assertTrue(second[0], second[1])
        self.assertEqual(first[1], second[1])
        self.assertEqual(self.char1.db.carried_scales, 85)
        self.assertEqual(
            InventoryItem.objects.filter(character_id=self.char1.id).count(),
            1,
        )
        self.assertEqual(
            GameOperation.objects.filter(
                operation_id="vendor-buy:exactly-once"
            ).count(),
            1,
        )


class TestAtomicVendorSell(CompositeEconomyTestBase):
    def setUp(self):
        super().setUp()
        from world.item_spawner import create_item_from_catalog

        self.item = create_item_from_catalog("iron_dagger", location=self.char1)
        self.item_id = self.item.id

    def test_failure_after_each_sale_write_restores_every_state(self):
        from world.vendor_engine import sell_item

        for checkpoint in (
            "scales_credited",
            "vendor_stock_credited",
            "sale_item_destroyed",
            "operation_recorded",
        ):
            with self.subTest(checkpoint=checkpoint):
                with patch(
                    "world.vendor_engine._after_write",
                    side_effect=self.fail_at(checkpoint),
                ), self.assertRaisesRegex(RuntimeError, checkpoint):
                    sell_item(
                        self.char1,
                        self.vendor,
                        self.item,
                        operation_id=f"vendor-sell:{checkpoint}",
                    )

                self.assertEqual(self.char1.db.carried_scales, 100)
                self.assertEqual(self.vendor.db.player_stock, {})
                self.assertTrue(ObjectDB.objects.filter(pk=self.item_id).exists())
                self.assertTrue(
                    InventoryItem.objects.filter(item_id=self.item_id).exists()
                )
                self.assertFalse(GameOperation.objects.exists())

    def test_same_sale_operation_credits_and_stocks_once_after_item_deletion(self):
        from world.vendor_engine import sell_item

        first = sell_item(
            self.char1,
            self.vendor,
            self.item,
            operation_id="vendor-sell:exactly-once",
        )
        second = sell_item(
            self.char1,
            self.vendor,
            SimpleNamespace(id=self.item_id),
            operation_id="vendor-sell:exactly-once",
        )

        self.assertTrue(first[0], first[1])
        self.assertTrue(second[0], second[1])
        self.assertEqual(first[1], second[1])
        self.assertEqual(self.char1.db.carried_scales, 104)
        self.assertFalse(ObjectDB.objects.filter(pk=self.item_id).exists())
        self.assertEqual(len(self.vendor.db.player_stock), 1)
        only_entry = next(iter(self.vendor.db.player_stock.values()))
        self.assertEqual(only_entry["stock_quantity"], 1)


class TestAtomicCrafting(CompositeEconomyTestBase):
    def setUp(self):
        super().setUp()
        from world.item_spawner import create_item_from_template

        self.room.tags.add("crafting_forge", category="crafting_station")
        self.ingredient = create_item_from_template(
            {
                "item_id": "iron_ingot",
                "key": "Iron Ingot",
                "item_type": "item",
                "weight": 1.0,
                "value": 5,
                "stackable": True,
                "quantity": 2,
            },
            location=self.char1,
        )
        self.ingredient_id = self.ingredient.id

    def test_output_creation_failure_keeps_all_ingredients(self):
        from world.crafting_engine import craft_item

        with patch(
            "world.crafting_engine._create_crafted_item",
            return_value=None,
        ):
            success, _ = craft_item(
                self.char1,
                "iron_dagger",
                operation_id="craft:output-failure",
            )

        self.assertFalse(success)
        self.assertEqual(
            InventoryItem.objects.get(item_id=self.ingredient_id).quantity,
            2,
        )
        self.assertTrue(ObjectDB.objects.filter(pk=self.ingredient_id).exists())
        self.assertFalse(GameOperation.objects.exists())

    def test_failure_after_consumption_restores_inputs_and_removes_output(self):
        from world.crafting_engine import craft_item

        original_ids = set(ObjectDB.objects.values_list("id", flat=True))
        with patch(
            "world.crafting_engine._after_write",
            side_effect=self.fail_at("craft_ingredients_consumed"),
        ), self.assertRaisesRegex(RuntimeError, "craft_ingredients_consumed"):
            craft_item(
                self.char1,
                "iron_dagger",
                operation_id="craft:consumption-rollback",
            )

        self.assertEqual(
            InventoryItem.objects.get(item_id=self.ingredient_id).quantity,
            2,
        )
        self.assertEqual(
            set(ObjectDB.objects.values_list("id", flat=True)),
            original_ids,
        )
        self.assertFalse(GameOperation.objects.exists())

    def test_same_craft_operation_consumes_and_creates_once(self):
        from world.crafting_engine import craft_item

        first = craft_item(
            self.char1,
            "iron_dagger",
            operation_id="craft:exactly-once",
        )
        second = craft_item(
            self.char1,
            "iron_dagger",
            operation_id="craft:exactly-once",
        )

        self.assertTrue(first[0], first[1])
        self.assertTrue(second[0], second[1])
        self.assertEqual(first[1], second[1])
        self.assertFalse(ObjectDB.objects.filter(pk=self.ingredient_id).exists())
        receipt = GameOperation.objects.get(operation_id="craft:exactly-once")
        self.assertTrue(
            ObjectDB.objects.filter(pk=receipt.result["item_object_id"]).exists()
        )
        self.assertEqual(
            InventoryItem.objects.filter(character_id=self.char1.id).count(),
            1,
        )


class TestAtomicFlightBooking(CompositeEconomyTestBase):
    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom
        from world.banking import credit_to_bank
        from world.flight_registry import FlightRegistry

        FlightRegistry.clear()
        self.destination = create_object(SoravelonRoom, key="Flight Destination")
        FlightRegistry.register_point("origin", self.room, name="Origin")
        FlightRegistry.register_point(
            "destination",
            self.destination,
            name="Destination",
        )
        FlightRegistry.register_route(
            "origin",
            "destination",
            base_fare=50,
            leg_duration=30,
        )
        self.char1.db.discovered_flight_points = {"destination"}
        credited, message = credit_to_bank(
            self.char1,
            100,
            "test_seed",
            operation_id="flight-tests:seed",
        )
        self.assertTrue(credited, message)

    def tearDown(self):
        from world.flight_registry import FlightRegistry

        FlightRegistry.clear()
        super().tearDown()

    def test_script_setup_failure_rolls_back_fare_and_script(self):
        from evennia.scripts.models import ScriptDB
        from world.banking import get_balance
        from world.flight_engine import book_flight

        with patch("world.flight_engine.logger.exception"), patch(
            "world.flight_engine._after_write",
            side_effect=self.fail_at("flight_script_configured"),
        ):
            success, message = book_flight(
                self.char1,
                "origin",
                "destination",
                operation_id="flight:setup-failure",
            )

        self.assertFalse(success)
        self.assertIn("no fare", message)
        self.assertEqual(get_balance(self.char1), 100)
        self.assertFalse(
            BankTransaction.objects.filter(
                operation_id="flight:setup-failure"
            ).exists()
        )
        self.assertFalse(
            GameOperation.objects.filter(
                operation_id="flight:setup-failure"
            ).exists()
        )
        self.assertFalse(
            ScriptDB.objects.filter(
                db_obj=self.char1,
                db_key="flight_script",
            ).exists()
        )

    def test_start_failure_compensates_committed_fare(self):
        from evennia.scripts.models import ScriptDB
        from world.banking import get_balance
        from world.flight_engine import book_flight

        with patch("world.flight_engine.logger.exception"), patch(
            "world.scripts.flight_script.FlightScript.start_journey",
            side_effect=RuntimeError("start failed"),
        ):
            success, message = book_flight(
                self.char1,
                "origin",
                "destination",
                operation_id="flight:start-failure",
            )

        self.assertFalse(success)
        self.assertIn("no fare", message)
        self.assertEqual(get_balance(self.char1), 100)
        self.assertFalse(
            GameOperation.objects.filter(
                operation_id="flight:start-failure"
            ).exists()
        )
        self.assertFalse(
            BankTransaction.objects.filter(
                character_id=self.char1.id,
                transaction_type="flight_fare",
            ).exists()
        )
        self.assertFalse(
            ScriptDB.objects.filter(
                db_obj=self.char1,
                db_key="flight_script",
            ).exists()
        )

    def test_same_booking_operation_charges_and_creates_one_script(self):
        from evennia.scripts.models import ScriptDB
        from world.banking import get_balance
        from world.flight_engine import book_flight

        with patch(
            "world.scripts.flight_script.FlightScript.start_journey"
        ) as start:
            first = book_flight(
                self.char1,
                "origin",
                "destination",
                operation_id="flight:exactly-once",
            )
            second = book_flight(
                self.char1,
                "origin",
                "destination",
                operation_id="flight:exactly-once",
            )

        self.assertTrue(first[0], first[1])
        self.assertTrue(second[0], second[1])
        self.assertEqual(get_balance(self.char1), 50)
        self.assertEqual(start.call_count, 1)
        self.assertEqual(
            BankTransaction.objects.filter(
                operation_id="flight:exactly-once",
                transaction_type="flight_fare",
            ).count(),
            1,
        )
        self.assertEqual(
            ScriptDB.objects.filter(
                db_obj=self.char1,
                db_key="flight_script",
            ).count(),
            1,
        )


class TestExactlyOnceRewardBatch(CompositeEconomyTestBase):
    def setUp(self):
        super().setUp()
        from typeclasses.objects import SoravelonObject

        self.room.db.zone_id = "reward_test_zone"
        zone = create_object(SoravelonObject, key="Reward Test Zone")
        zone.db.zone_id = "reward_test_zone"
        zone.db.item_definitions = [
            {
                "item_id": "reward_token",
                "key": "Reward Token",
                "item_type": "item",
                "weight": 0.1,
                "value": 1,
                "desc": "A test reward token.",
            }
        ]
        zone.tags.add("zone_object", category="object_type")
        self.spec = {
            "quest_id": "quest_reward_exactly_once",
            "rewards": [
                {"action_type": "give_scales", "amount": 10},
                {"action_type": "give_item", "template_id": "reward_token"},
            ],
        }

    def test_retry_does_not_duplicate_currency_or_item(self):
        from world.quest_engine import _pay_rewards

        first = _pay_rewards(
            self.char1,
            self.spec,
            operation_id="quest-reward:exactly-once",
        )
        second = _pay_rewards(
            self.char1,
            self.spec,
            operation_id="quest-reward:exactly-once",
        )

        self.assertEqual(first, [])
        self.assertEqual(second, [])
        self.assertEqual(self.char1.db.carried_scales, 110)
        self.assertEqual(
            InventoryItem.objects.filter(character_id=self.char1.id).count(),
            1,
        )
        self.assertEqual(
            GameOperation.objects.filter(
                operation_id="quest-reward:exactly-once"
            ).count(),
            1,
        )

    def test_receipt_failure_rolls_back_all_prior_rewards(self):
        from world.quest_engine import _pay_rewards

        original_ids = set(ObjectDB.objects.values_list("id", flat=True))
        with patch(
            "world.quest_engine._reward_after_write",
            side_effect=self.fail_at("operation_recorded"),
        ), self.assertRaisesRegex(RuntimeError, "operation_recorded"):
            _pay_rewards(
                self.char1,
                self.spec,
                operation_id="quest-reward:rollback",
            )

        self.assertEqual(self.char1.db.carried_scales, 100)
        self.assertEqual(
            set(ObjectDB.objects.values_list("id", flat=True)),
            original_ids,
        )
        self.assertFalse(GameOperation.objects.exists())
