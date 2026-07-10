"""Two-player release gate for Soravelon's cooperative combat loop."""

from unittest.mock import MagicMock, patch

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest


class TestTwoPlayerCooperativeCombatVertical(EvenniaTest):
    """A live group can coordinate, earn, and claim independently."""

    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom
        from world.group_engine import accept_group_invite, send_group_invite

        self.room = create_object(SoravelonRoom, key="Cooperative Test Room")
        self.char1.location = self.room
        self.char2.location = self.room
        self.char1.db.base_stats = {"strength": 10}
        self.char2.db.base_stats = {"strength": 10}
        self.char1.db.carried_scales = 0
        self.char2.db.carried_scales = 0
        self.char1.ndb.presence_nonce = "leader-online"
        self.char2.ndb.presence_nonce = "ally-online"
        send_group_invite(self.char1, self.char2)
        accepted, _ = accept_group_invite(self.char2)
        self.assertTrue(accepted)

    @patch("world.loot_tables.roll_loot")
    @patch("world.base_attributes.record_stat_use")
    def test_group_action_to_tactic_to_independent_rewards(
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
            snapshot_reward_recipients,
        )
        from world.models import EncounterReward
        from world.status_effects import consume_attack_effects

        combat = MagicMock()
        combat.ndb.ally_action_count = {}
        combat._resolve_combatants.return_value = [self.char1, self.char2]
        CombatScript.record_allied_action(combat, self.char1)
        self.assertEqual(combat.ndb.ally_action_count, {str(self.char2.id): 1})

        mob = MagicMock()
        mob.id = 900
        mob.key = "Ash Wolf"
        mob.location = self.room
        mob.db.mob_type = "ash_wolf"
        mob.db.mob_template_key = None
        mob.db.personal_scales = 5
        mob.ndb.combat_handler = MagicMock()
        mob.ndb.combat_handler.get_player_combatants.return_value = [
            self.char1,
            self.char2,
        ]

        recipients = snapshot_reward_recipients(mob, self.char1)
        self.assertEqual(recipients, [self.char1, self.char2])

        self.char1.ndb.active_effects = []
        self.char2.ndb.active_effects = []
        ok, _ = _handle_tactical(
            self.char1,
            ABILITIES["coordinated_assault"],
            mob,
        )
        self.assertTrue(ok)
        preview = consume_attack_effects(self.char2, target=mob, consume=False)
        self.assertEqual(preview["damage_multiplier"], 0.2)

        corpse = MagicMock()
        corpse.id = 901
        roll_loot.side_effect = [
            [{"item_id": "wolf_pelt", "key": "wolf pelt"}],
            [{"item_id": "wolf_fang", "key": "wolf fang"}],
        ]
        create_personal_entitlements(mob, corpse, recipients)

        with patch("world.item_spawner.create_item_from_template"):
            claim = claim_personal_rewards(self.char1, corpse_id=corpse.id)

        self.assertEqual(claim["items"], ["wolf pelt"])
        self.assertEqual(self.char1.db.carried_scales, 5)
        ally_reward = EncounterReward.objects.get(
            character=self.char2,
            corpse_id=corpse.id,
        )
        self.assertIsNone(ally_reward.claimed_at)
