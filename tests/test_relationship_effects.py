"""Authored world-state effects are validated, durable, and exactly once."""

import ast
from pathlib import Path
from unittest.mock import MagicMock

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest

from tests.quest_helpers import create_completed_quest_fixture


def _authored_quest(area_name, quest_id):
    source = Path("world/areas", f"{area_name}.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "quest"
            and node.args
            and ast.literal_eval(node.args[0]) == quest_id
        ):
            continue
        return {
            "quest_id": quest_id,
            **{
                keyword.arg: ast.literal_eval(keyword.value)
                for keyword in node.keywords
                if keyword.arg
            },
        }
    raise AssertionError(f"Missing authored quest: {area_name}:{quest_id}")


class TestAuthoredRelationshipEffects(EvenniaTest):
    def setUp(self):
        super().setUp()
        from typeclasses.mobs import SoravelonMob
        from typeclasses.rooms import SoravelonRoom

        self.room = create_object(SoravelonRoom, key="Relationship Room")
        self.mob = create_object(
            SoravelonMob,
            key="Kauroran Listener",
            location=self.room,
        )
        self.mob.db.faction = "kauroran"
        self.mob.db.base_disposition = 0.3
        self.mob.db.trust_sensitive = True
        self.char1.db.network_score = 0.0
        self.char1.db.attunement_score = 0.0
        self.char1.db.reputation_score = 0.0
        self.char1.db.ancestry = None

    def _execute_twice(self, action):
        from world.action_vocabulary import execute_action

        first = execute_action(action, {"character": self.char1})
        second = execute_action(action, {"character": self.char1})
        self.assertTrue(first[0], first[1])
        self.assertTrue(second[0], second[1])

    def test_effects_persist_once_and_change_real_dialogue_and_disposition(self):
        from world.dialogue_engine import get_standing_tier
        from world.mob_disposition import get_mob_disposition
        from world.models import GameOperation, ZoneAttunement
        from world.world_state import get_betrayal, get_trust

        before_trust = get_mob_disposition(self.mob, self.char1)
        self._execute_twice(
            {
                "action_type": "modify_dimension",
                "dimension": "network",
                "delta": 8,
                "effect_id": "test:guest_names:network",
            }
        )
        self._execute_twice(
            {
                "action_type": "modify_attunement",
                "zone_id": "kiai_grounds",
                "delta": 12,
                "effect_id": "test:witness_silence:attunement",
            }
        )
        self._execute_twice(
            {
                "action_type": "modify_trust",
                "faction_id": "kauroran",
                "delta": 30,
                "effect_id": "test:guest_names:trust",
            }
        )

        self.assertEqual(self.char1.db.network_score, 8.0)
        attunement = ZoneAttunement.objects.get(
            character=self.char1,
            zone_id="kiai_grounds",
        )
        self.assertEqual(attunement.score, 12.0)
        self.assertEqual(self.char1.db.attunement_score, 12.0)
        self.assertEqual(get_trust(self.char1, "kauroran"), 80)
        self.assertAlmostEqual(
            get_mob_disposition(self.mob, self.char1),
            before_trust + 0.1,
        )

        self._execute_twice(
            {
                "action_type": "set_betrayal",
                "faction_id": "kauroran",
                "betrayed": True,
                "effect_id": "test:broken_oath:betrayal",
            }
        )
        self.assertTrue(get_betrayal(self.char1, "kauroran"))
        self.assertEqual(get_standing_tier(self.char1, self.mob), "betrayal")
        self.assertEqual(
            GameOperation.objects.filter(
                character=self.char1,
                operation_type="relationship_effect",
            ).count(),
            4,
        )

    def test_invalid_effects_fail_closed_without_writes(self):
        from world.action_vocabulary import execute_action
        from world.models import FactionStanding, GameOperation, ZoneAttunement

        invalid_actions = (
            {
                "action_type": "modify_dimension",
                "dimension": "typo_network",
                "delta": 8,
                "effect_id": "test:bad:dimension",
            },
            {
                "action_type": "modify_attunement",
                "zone_id": "kiai_grounds",
                "delta": 12,
            },
            {
                "action_type": "modify_trust",
                "faction_id": "typo_kauroran",
                "delta": 30,
                "effect_id": "test:bad:faction",
            },
            {
                "action_type": "set_betrayal",
                "faction_id": "kauroran",
                "betrayed": "yes",
                "effect_id": "test:bad:betrayal",
            },
        )

        for action in invalid_actions:
            with self.subTest(action_type=action["action_type"]):
                success, _message = execute_action(
                    action,
                    {"character": self.char1},
                )
                self.assertFalse(success)

        self.assertEqual(self.char1.db.network_score, 0.0)
        self.assertFalse(ZoneAttunement.objects.filter(character=self.char1).exists())
        self.assertFalse(FactionStanding.objects.filter(character=self.char1).exists())
        self.assertFalse(GameOperation.objects.filter(character=self.char1).exists())

    def test_later_quest_reward_failure_rolls_back_rows_receipts_and_attribute_cache(self):
        from world.models import FactionStanding, GameOperation, ZoneAttunement
        from world.quest_engine import _pay_rewards

        failures = _pay_rewards(
            self.char1,
            {
                "quest_id": "relationship_rollback",
                "rewards": [
                    {
                        "action_type": "modify_dimension",
                        "dimension": "network",
                        "delta": 8,
                        "effect_id": "test:rollback:network",
                    },
                    {
                        "action_type": "modify_attunement",
                        "zone_id": "kiai_grounds",
                        "delta": 12,
                        "effect_id": "test:rollback:attunement",
                    },
                    {
                        "action_type": "modify_trust",
                        "faction_id": "kauroran",
                        "delta": 30,
                        "effect_id": "test:rollback:trust",
                    },
                    {"action_type": "invented_failure"},
                ],
            },
            operation_id="test:relationship:rollback",
        )

        self.assertEqual(len(failures), 1)
        self.assertEqual(self.char1.db.network_score, 0.0)
        self.assertEqual(self.char1.db.attunement_score, 0.0)
        self.assertFalse(ZoneAttunement.objects.filter(character=self.char1).exists())
        self.assertFalse(FactionStanding.objects.filter(character=self.char1).exists())
        self.assertFalse(GameOperation.objects.filter(character=self.char1).exists())

    def test_live_guest_names_inputs_create_trust_and_network_without_direct_relationship_seeding(self):
        from typeclasses.mobs import SoravelonMob
        from typeclasses.rooms import SoravelonRoom
        from world.models import CharacterQuest, GameOperation
        from world.quest_engine import (
            accept_quest,
            check_investigate_objectives,
            check_talk_to_objectives,
        )
        from world.world_state import get_trust

        self.char1.msg = MagicMock()
        spec = _authored_quest("korahei", "kor_q_guest_names")
        create_completed_quest_fixture(self.char1, "kor_q_first_bite")
        accepted, message = accept_quest(
            self.char1,
            "kor_q_guest_names",
            spec,
        )
        self.assertTrue(accepted, message)

        iren = create_object(SoravelonMob, key="Warden Iren", location=self.room)
        iren.tags.add("npc_warden_guest_iren", category="npc_id")
        sola = create_object(SoravelonMob, key="Auntie Sola", location=self.room)
        sola.tags.add("npc_market_auntie_sola", category="npc_id")
        listening_step = create_object(
            SoravelonRoom,
            key="Listening Step",
        )
        listening_step.tags.add("lt_listening_step", category="room_id")

        check_talk_to_objectives(self.char1, iren)
        check_talk_to_objectives(self.char1, sola)
        with self.captureOnCommitCallbacks(execute=True):
            check_investigate_objectives(self.char1, listening_step)

        quest = CharacterQuest.objects.get(
            character=self.char1,
            quest_id="kor_q_guest_names",
        )
        self.assertEqual(quest.status, "complete")
        self.assertEqual(self.char1.db.network_score, 8.0)
        self.assertEqual(get_trust(self.char1, "kauroran"), 80)
        self.assertEqual(
            GameOperation.objects.filter(
                character=self.char1,
                operation_type="relationship_effect",
            ).count(),
            2,
        )

        check_talk_to_objectives(self.char1, iren)
        check_talk_to_objectives(self.char1, sola)
        check_investigate_objectives(self.char1, listening_step)
        self.assertEqual(self.char1.db.network_score, 8.0)
        self.assertEqual(get_trust(self.char1, "kauroran"), 80)

        player_messages = [
            str(call.args[0])
            for call in self.char1.msg.call_args_list
            if call.args
        ]
        self.assertTrue(any("living web" in text for text in player_messages))
        self.assertTrue(any("trusts you" in text for text in player_messages))
