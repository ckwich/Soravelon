"""Accepted quest specifications remain authoritative for the whole run."""

from collections import UserDict, UserList
from unittest.mock import MagicMock, patch

from evennia.utils.test_resources import EvenniaTest

from world.models import CharacterQuest


class TestAcceptedQuestSnapshots(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.char1.db.carried_scales = 0
        self.char1.msg = MagicMock()

    def test_accepted_spec_drives_progress_and_rewards_after_live_content_changes(self):
        from world.quest_engine import accept_quest, check_kill_objectives

        accepted_spec = {
            "quest_id": "hold_the_old_trail",
            "name": "Hold the Old Trail",
            "objectives": [
                {
                    "type": "kill",
                    "target": "trail_wolf",
                    "count": 1,
                    "description": "Drive off the wolf stalking the trail.",
                },
            ],
            "rewards": [{"action_type": "give_scales", "amount": 7}],
        }
        accepted, _ = accept_quest(
            self.char1,
            accepted_spec["quest_id"],
            accepted_spec,
        )
        self.assertTrue(accepted)

        quest = CharacterQuest.objects.get(
            character=self.char1,
            quest_id=accepted_spec["quest_id"],
        )
        self.assertEqual(quest.accepted_spec, accepted_spec)

        changed_live_spec = {
            "quest_id": accepted_spec["quest_id"],
            "name": "Rewritten Trail",
            "objectives": [
                {"type": "kill", "target": "trail_boar", "count": 4},
            ],
            "rewards": [{"action_type": "give_scales", "amount": 999}],
        }
        wolf = MagicMock()
        wolf.db.mob_template_key = "trail_wolf"
        wolf.db.mob_instance_id = ""

        with patch(
            "world.quest_engine._get_quest_spec",
            return_value=changed_live_spec,
        ), self.captureOnCommitCallbacks(execute=True):
            check_kill_objectives(self.char1, wolf)

        quest.refresh_from_db()
        self.assertEqual(quest.status, "complete")
        self.assertEqual(quest.progress, {"kill_trail_wolf": 1})
        self.assertEqual(self.char1.db.carried_scales, 7)

    def test_acceptance_converts_attribute_wrappers_to_plain_json_values(self):
        from world.quest_engine import accept_quest

        wrapped_spec = UserDict(
            {
                "quest_id": "wrapped_offer",
                "name": "Wrapped Offer",
                "objectives": UserList(
                    [
                        UserDict(
                            {
                                "type": "investigate",
                                "target": "old_marker",
                                "count": 1,
                            }
                        )
                    ]
                ),
                "rewards": UserList(
                    [UserDict({"action_type": "give_scales", "amount": 3})]
                ),
            }
        )

        accepted, message = accept_quest(
            self.char1,
            "wrapped_offer",
            wrapped_spec,
        )

        self.assertTrue(accepted, message)
        snapshot = CharacterQuest.objects.get(
            character=self.char1,
            quest_id="wrapped_offer",
        ).accepted_spec
        self.assertIs(type(snapshot["objectives"]), list)
        self.assertIs(type(snapshot["objectives"][0]), dict)
        self.assertIs(type(snapshot["rewards"]), list)
        self.assertIs(type(snapshot["rewards"][0]), dict)
