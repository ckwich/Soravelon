"""Release proof that cooperative play leaves personal and social consequence."""

import ast
from pathlib import Path
from unittest.mock import MagicMock, patch

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest


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


class TestM4LivingWorldVertical(EvenniaTest):
    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom
        from world.group_engine import accept_group_invite, send_group_invite

        self.room = create_object(SoravelonRoom, key="Marta's Cellar")
        self.char1.location = self.room
        self.char2.location = self.room
        self.char1.db.base_stats = {"strength": 10}
        self.char2.db.base_stats = {"strength": 10}
        self.char1.db.carried_scales = 0
        self.char2.db.carried_scales = 0
        self.char1.db.reputation_score = 0.0
        self.char2.db.reputation_score = 0.0
        self.char1.msg = MagicMock()
        self.char2.msg = MagicMock()
        self.char1.ndb.presence_nonce = "cellar-leader-online"
        self.char2.ndb.presence_nonce = "cellar-ally-online"

        sent, _ = send_group_invite(self.char1, self.char2)
        joined, _ = accept_group_invite(self.char2)
        self.assertTrue(sent)
        self.assertTrue(joined)

    @staticmethod
    def _quest_command(character, args):
        from commands.cmd_quest import CmdQuest

        command = CmdQuest()
        command.caller = character
        command.args = args
        command.func()

    @patch("world.loot_tables.roll_loot")
    @patch("world.base_attributes.record_stat_use")
    def test_two_players_turn_combat_into_independent_remembered_consequence(
        self,
        _record_stat_use,
        roll_loot,
    ):
        from world.ability_engine import _handle_tactical
        from world.ability_registry import ABILITIES
        from world.combat_script import CombatScript
        from world.encounter_rewards import (
            claim_personal_rewards,
            create_personal_entitlements,
            grant_kill_credit,
            snapshot_reward_recipients,
        )
        from world.models import (
            CharacterQuest,
            EncounterReward,
            FactionStanding,
            GameOperation,
            QuestShareOffer,
            SocialFact,
            SocialKnowledge,
            SocialNode,
        )
        from world.quest_engine import accept_quest
        from world.status_effects import consume_attack_effects

        quest_spec = _authored_quest("vaels_crossing", "vc_q_rat_problem")
        self.assertTrue(quest_spec["can_share"])
        self.assertTrue(
            any(
                reward.get("action_type") == "record_social_event"
                for reward in quest_spec["rewards"]
            )
        )

        accepted, message = accept_quest(
            self.char1,
            quest_spec["quest_id"],
            quest_spec,
        )
        self.assertTrue(accepted, message)
        self._quest_command(self.char1, "share cellar")
        self._quest_command(self.char2, "accept cellar")
        self.assertEqual(QuestShareOffer.objects.count(), 1)

        combat = MagicMock()
        combat.ndb.ally_action_count = {}
        combat._resolve_combatants.return_value = [self.char1, self.char2]
        CombatScript.record_allied_action(combat, self.char1)
        self.assertEqual(combat.ndb.ally_action_count, {str(self.char2.id): 1})

        mob = MagicMock()
        mob.id = 1200
        mob.key = "Cellar Rat"
        mob.location = self.room
        mob.db.mob_type = "sewer_rat"
        mob.db.mob_template_key = "sewer_rat"
        mob.db.mob_instance_id = None
        mob.db.named_id = None
        mob.db.rarity = "normal"
        mob.db.personal_scales = 5
        mob.tags.get.return_value = None
        mob.ndb.combat_handler = MagicMock()
        mob.ndb.combat_handler.get_player_combatants.return_value = [
            self.char1,
            self.char2,
        ]

        recipients = snapshot_reward_recipients(mob, self.char1)
        self.assertEqual(recipients, [self.char1, self.char2])

        self.char1.ndb.active_effects = []
        self.char2.ndb.active_effects = []
        coordinated, _ = _handle_tactical(
            self.char1,
            ABILITIES["coordinated_assault"],
            mob,
        )
        self.assertTrue(coordinated)
        self.assertEqual(
            consume_attack_effects(self.char2, target=mob, consume=False)[
                "damage_multiplier"
            ],
            0.2,
        )

        with self.captureOnCommitCallbacks(execute=True):
            for _ in range(10):
                grant_kill_credit(recipients, mob)

        quests = CharacterQuest.objects.filter(quest_id="vc_q_rat_problem")
        self.assertEqual(quests.filter(status="complete").count(), 2)
        self.assertEqual(self.char1.db.reputation_score, 3.0)
        self.assertEqual(self.char2.db.reputation_score, 3.0)
        for character in (self.char1, self.char2):
            self.assertEqual(
                FactionStanding.objects.get(
                    character=character,
                    faction_id="consortium",
                ).standing,
                10_000,
            )

        marta = SocialNode.objects.get(node_key="npc:npc_barkeep_marta_voss")
        self.assertEqual(
            SocialFact.objects.filter(event_type="cellar_service").count(),
            2,
        )
        self.assertEqual(
            SocialKnowledge.objects.filter(node=marta, fact__isnull=False).count(),
            2,
        )
        self.assertEqual(
            GameOperation.objects.filter(
                operation_type="relationship_effect",
            ).count(),
            2,
        )

        corpse = MagicMock()
        corpse.id = 1201
        roll_loot.side_effect = [
            [{"item_id": "rat_hide", "key": "rat hide"}],
            [{"item_id": "rat_tooth", "key": "rat tooth"}],
        ]
        create_personal_entitlements(mob, corpse, recipients)
        self.assertEqual(
            EncounterReward.objects.filter(corpse_id=corpse.id).count(),
            2,
        )

        with patch("world.item_spawner.create_item_from_template"):
            leader_claim = claim_personal_rewards(
                self.char1,
                corpse_id=corpse.id,
            )
            ally_claim = claim_personal_rewards(
                self.char2,
                corpse_id=corpse.id,
            )

        self.assertEqual(leader_claim["items"], ["rat hide"])
        self.assertEqual(ally_claim["items"], ["rat tooth"])
        self.assertEqual(self.char1.db.carried_scales, 55)
        self.assertEqual(self.char2.db.carried_scales, 55)

        grant_kill_credit(recipients, mob)
        self.assertEqual(self.char1.db.reputation_score, 3.0)
        self.assertEqual(self.char2.db.reputation_score, 3.0)
        self.assertEqual(SocialFact.objects.count(), 2)
