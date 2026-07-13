"""Player-consented quest sharing through live group and command paths."""

from unittest.mock import MagicMock

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest

from world.models import CharacterQuest


class TestQuestSharingVertical(EvenniaTest):
    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom
        from world.group_engine import accept_group_invite, send_group_invite

        self.room = create_object(SoravelonRoom, key="Shared Trail")
        self.char1.location = self.room
        self.char2.location = self.room
        self.char1.msg = MagicMock()
        self.char2.msg = MagicMock()
        self.char1.ndb.presence_nonce = "quest-leader-online"
        self.char2.ndb.presence_nonce = "quest-ally-online"
        sent, _ = send_group_invite(self.char1, self.char2)
        joined, _ = accept_group_invite(self.char2)
        self.assertTrue(sent)
        self.assertTrue(joined)

    @staticmethod
    def _run_quest_command(character, args):
        from commands.cmd_quest import CmdQuest

        command = CmdQuest()
        command.caller = character
        command.args = args
        command.func()

    def test_nearby_ally_explicitly_accepts_independent_frozen_run(self):
        from world.models import QuestShareOffer
        from world.quest_engine import accept_quest

        spec = {
            "quest_id": "trail_names",
            "name": "Names Along the Trail",
            "description": "Learn who keeps the road alive.",
            "objectives": [
                {"type": "investigate", "target": "old_marker", "count": 1},
            ],
            "rewards": [{"action_type": "give_scales", "amount": 12}],
            "can_share": True,
            "share_radius": 1,
            "share_cap": 6,
        }
        accepted, message = accept_quest(self.char1, spec["quest_id"], spec)
        self.assertTrue(accepted, message)

        self._run_quest_command(self.char1, "share names")

        self.assertFalse(
            CharacterQuest.objects.filter(
                character=self.char2,
                quest_id=spec["quest_id"],
            ).exists()
        )
        offer = QuestShareOffer.objects.get(
            sender=self.char1,
            recipient=self.char2,
            quest_id=spec["quest_id"],
        )
        self.assertEqual(offer.status, "pending")
        self.assertEqual(offer.quest_spec, spec)
        self.assertTrue(
            any(
                "quest accept names" in str(call.args[0]).lower()
                for call in self.char2.msg.call_args_list
                if call.args
            )
        )

        self._run_quest_command(self.char2, "accept names")

        offer.refresh_from_db()
        ally_quest = CharacterQuest.objects.get(
            character=self.char2,
            quest_id=spec["quest_id"],
            status="active",
        )
        self.assertEqual(offer.status, "accepted")
        self.assertEqual(offer.accepted_quest_id, ally_quest.pk)
        self.assertEqual(ally_quest.progress, {"investigate_old_marker": 0})
        self.assertEqual(ally_quest.accepted_spec, spec)
        self.assertNotEqual(ally_quest.pk, offer.source_quest_id)

    def test_ally_can_durably_decline_without_receiving_a_quest(self):
        from world.models import QuestShareOffer
        from world.quest_engine import accept_quest

        spec = {
            "quest_id": "quiet_watch",
            "name": "The Quiet Watch",
            "objectives": [
                {"type": "investigate", "target": "watch_post", "count": 1},
            ],
            "can_share": True,
        }
        accepted, _ = accept_quest(self.char1, spec["quest_id"], spec)
        self.assertTrue(accepted)
        self._run_quest_command(self.char1, "share quiet")

        self._run_quest_command(self.char2, "decline quiet")

        offer = QuestShareOffer.objects.get(
            sender=self.char1,
            recipient=self.char2,
            quest_id=spec["quest_id"],
        )
        self.assertEqual(offer.status, "declined")
        self.assertIsNotNone(offer.responded_at)
        self.assertFalse(
            CharacterQuest.objects.filter(
                character=self.char2,
                quest_id=spec["quest_id"],
            ).exists()
        )

    def test_recipient_can_reopen_pending_offer_list(self):
        from world.quest_engine import accept_quest

        spec = {
            "quest_id": "shared_hearth",
            "name": "The Shared Hearth",
            "objectives": [
                {"type": "investigate", "target": "hearth", "count": 1},
            ],
            "can_share": True,
        }
        accepted, _ = accept_quest(self.char1, spec["quest_id"], spec)
        self.assertTrue(accepted)
        self._run_quest_command(self.char1, "share hearth")
        self.char2.msg.reset_mock()

        self._run_quest_command(self.char2, "offers")

        message = self.char2.msg.call_args[0][0]
        self.assertIn("The Shared Hearth", message)
        self.assertIn(self.char1.key, message)
        self.assertIn("quest accept", message.lower())

    def test_share_skips_recipient_who_has_not_earned_prerequisites(self):
        from world.models import QuestShareOffer
        from world.quest_engine import accept_quest

        from tests.quest_helpers import create_completed_quest_fixture

        create_completed_quest_fixture(self.char1, "learn_the_markers")
        spec = {
            "quest_id": "read_the_high_road",
            "name": "Read the High Road",
            "objectives": [
                {"type": "investigate", "target": "high_marker", "count": 1},
            ],
            "prerequisite_quests": ["learn_the_markers"],
            "can_share": True,
        }
        accepted, _ = accept_quest(self.char1, spec["quest_id"], spec)
        self.assertTrue(accepted)

        self._run_quest_command(self.char1, "share high road")

        self.assertFalse(
            QuestShareOffer.objects.filter(
                recipient=self.char2,
                quest_id=spec["quest_id"],
            ).exists()
        )
        self.assertFalse(
            CharacterQuest.objects.filter(
                character=self.char2,
                quest_id=spec["quest_id"],
            ).exists()
        )

    def test_share_respects_authored_radius_and_total_participant_cap(self):
        from typeclasses.rooms import SoravelonRoom
        from world.models import QuestShareOffer
        from world.quest_engine import accept_quest

        remote_room = create_object(SoravelonRoom, key="Remote Ridge")
        self.char2.location = remote_room
        spec = {
            "quest_id": "ridge_signals",
            "name": "Ridge Signals",
            "objectives": [
                {"type": "investigate", "target": "ridge_fire", "count": 1},
            ],
            "can_share": True,
            "share_radius": 1,
            "share_cap": 6,
        }
        accepted, _ = accept_quest(self.char1, spec["quest_id"], spec)
        self.assertTrue(accepted)

        self._run_quest_command(self.char1, "share ridge")
        self.assertFalse(QuestShareOffer.objects.exists())

        self.char2.location = self.room
        capped_spec = dict(spec, quest_id="single_witness", name="Single Witness")
        capped_spec["share_cap"] = 1
        accepted, _ = accept_quest(
            self.char1,
            capped_spec["quest_id"],
            capped_spec,
        )
        self.assertTrue(accepted)
        self._run_quest_command(self.char1, "share single")
        self.assertFalse(QuestShareOffer.objects.exists())

    def test_nonshareable_and_one_chance_runs_never_create_an_offer(self):
        from world.models import QuestShareOffer
        from world.quest_engine import accept_quest

        from tests.quest_helpers import create_completed_quest_fixture

        private_spec = {
            "quest_id": "private_confession",
            "name": "A Private Confession",
            "objectives": [
                {"type": "talk_to", "target": "witness", "count": 1},
            ],
            "can_share": False,
        }
        accepted, _ = accept_quest(
            self.char1,
            private_spec["quest_id"],
            private_spec,
        )
        self.assertTrue(accepted)
        self._run_quest_command(self.char1, "share confession")
        self.assertFalse(QuestShareOffer.objects.exists())

        one_chance_spec = {
            "quest_id": "one_last_warning",
            "name": "One Last Warning",
            "objectives": [
                {"type": "investigate", "target": "warning_stone", "count": 1},
            ],
            "one_chance": True,
            "can_share": True,
        }
        create_completed_quest_fixture(self.char2, one_chance_spec["quest_id"])
        accepted, _ = accept_quest(
            self.char1,
            one_chance_spec["quest_id"],
            one_chance_spec,
        )
        self.assertTrue(accepted)
        self._run_quest_command(self.char1, "share last warning")
        self.assertFalse(QuestShareOffer.objects.exists())

    def test_each_accepted_run_receives_its_own_delivery_item(self):
        from evennia import DefaultObject
        from world.models import InventoryItem
        from world.quest_engine import accept_quest

        self.room.db.zone_id = "sharing_test_zone"
        zone = create_object(DefaultObject, key="Sharing Test Zone")
        zone.tags.add("zone_object", category="object_type")
        zone.db.zone_id = "sharing_test_zone"
        zone.db.item_definitions = [
            {
                "item_id": "shared_delivery_token",
                "key": "shared delivery token",
                "item_type": "item",
                "weight": 0.1,
                "rarity": "normal",
                "value": 0,
                "is_quest_item": True,
            },
        ]

        spec = {
            "quest_id": "carry_the_debt_mark",
            "name": "Carry the Debt Mark",
            "objectives": [
                {
                    "type": "deliver",
                    "target": "ledger_keeper",
                    "item_tag": "shared_delivery_token",
                    "count": 1,
                },
            ],
            "can_share": True,
        }
        accepted, message = accept_quest(self.char1, spec["quest_id"], spec)
        self.assertTrue(accepted, message)
        self._run_quest_command(self.char1, "share debt mark")
        self._run_quest_command(self.char2, "accept debt mark")

        source_items = [
            item
            for item in self.char1.contents
            if item.tags.get(category="item_tag") == "shared_delivery_token"
        ]
        recipient_items = [
            item
            for item in self.char2.contents
            if item.tags.get(category="item_tag") == "shared_delivery_token"
        ]
        self.assertEqual(len(source_items), 1)
        self.assertEqual(len(recipient_items), 1)
        self.assertNotEqual(source_items[0].id, recipient_items[0].id)
        self.assertTrue(
            InventoryItem.objects.get(
                character=self.char1,
                item_id=source_items[0].id,
            ).is_quest_item
        )
        self.assertTrue(
            InventoryItem.objects.get(
                character=self.char2,
                item_id=recipient_items[0].id,
            ).is_quest_item
        )
