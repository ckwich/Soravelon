"""Regression contracts for group encounter rewards and credit."""

import unittest
from unittest.mock import MagicMock, patch

from evennia.utils.test_resources import EvenniaTest


def _player(character_id, key, room):
    character = MagicMock()
    character.id = character_id
    character.key = key
    character.account = object()
    character.location = room
    return character


class TestEncounterParticipantSnapshot(unittest.TestCase):
    """Only a present, live combat ally is entitled to group credit."""

    @patch("world.group_engine.are_allies")
    def test_snapshot_excludes_remote_and_non_participant_group_members(
        self,
        mock_are_allies,
    ):
        from world.encounter_rewards import snapshot_reward_recipients

        room = MagicMock()
        distant_room = MagicMock()
        killer = _player(1, "Killer", room)
        ally = _player(2, "Ally", room)
        remote = _player(3, "Remote", distant_room)
        late = _player(4, "Late", room)
        mob = MagicMock()
        mob.location = room
        mob.ndb.combat_handler.get_player_combatants.return_value = [
            killer,
            ally,
            remote,
        ]
        mock_are_allies.side_effect = lambda left, right: {
            left.id,
            right.id,
        } in ({1, 2}, {1, 3}, {1, 4})

        recipients = snapshot_reward_recipients(mob, killer)

        self.assertEqual(recipients, [killer, ally])
        self.assertNotIn(remote, recipients)
        self.assertNotIn(late, recipients)


class TestPersonalRewardClaims(EvenniaTest):
    """Each participant claims only their own durable encounter reward."""

    def setUp(self):
        super().setUp()
        self.char1.db.carried_scales = 10
        self.char2.db.carried_scales = 20

    def test_claiming_one_personal_reward_cannot_consume_an_allys(self):
        from world.models import EncounterReward
        from world.encounter_rewards import claim_personal_rewards

        mine = EncounterReward.objects.create(
            character=self.char1,
            corpse_id=501,
            source_mob_key="ash_wolf",
            item_definitions=[{"item_id": "wolf_pelt", "key": "wolf pelt"}],
            scales=7,
        )
        ally = EncounterReward.objects.create(
            character=self.char2,
            corpse_id=501,
            source_mob_key="ash_wolf",
            item_definitions=[{"item_id": "wolf_fang", "key": "wolf fang"}],
            scales=9,
        )

        with patch("world.item_spawner.create_item_from_template") as create_item:
            claimed = claim_personal_rewards(self.char1, corpse_id=501)
            repeated = claim_personal_rewards(self.char1, corpse_id=501)

        self.assertEqual(claimed["items"], ["wolf pelt"])
        self.assertEqual(claimed["scales"], 7)
        self.assertEqual(repeated, {"items": [], "scales": 0, "claimed": 0})
        create_item.assert_called_once_with(
            {"item_id": "wolf_pelt", "key": "wolf pelt"},
            location=self.char1,
        )
        self.assertEqual(self.char1.db.carried_scales, 17)
        mine.refresh_from_db()
        ally.refresh_from_db()
        self.assertIsNotNone(mine.claimed_at)
        self.assertIsNone(ally.claimed_at)

    @patch("world.loot_tables.roll_loot")
    def test_each_eligible_participant_gets_a_separate_personal_roll(
        self,
        roll_loot,
    ):
        from world.encounter_rewards import create_personal_entitlements
        from world.models import EncounterReward

        mob = MagicMock()
        mob.key = "Ash Wolf"
        mob.db.mob_type = "ash_wolf"
        mob.db.mob_template_key = None
        mob.db.personal_scales = 4
        corpse = MagicMock()
        corpse.id = 502
        roll_loot.side_effect = [
            [{"item_id": "wolf_pelt", "key": "wolf pelt"}],
            [{"item_id": "wolf_fang", "key": "wolf fang"}],
        ]

        created = create_personal_entitlements(mob, corpse, [self.char1, self.char2])

        self.assertEqual(created, [self.char1, self.char2])
        rewards = list(
            EncounterReward.objects.filter(corpse_id=502).order_by("character_id")
        )
        self.assertEqual(len(rewards), 2)
        self.assertEqual(rewards[0].item_definitions[0]["item_id"], "wolf_pelt")
        self.assertEqual(rewards[1].item_definitions[0]["item_id"], "wolf_fang")
        self.assertEqual([reward.scales for reward in rewards], [4, 4])


class TestGroupKillCredit(unittest.TestCase):
    """Proximity snapshots grant each participant their own quest progress check."""

    @patch("world.quest_engine.check_kill_objectives")
    def test_grant_kill_credit_checks_each_snapshot_recipient(self, check_objectives):
        from world.encounter_rewards import grant_kill_credit

        mob = MagicMock()
        leader = _player(1, "Leader", MagicMock())
        ally = _player(2, "Ally", leader.location)

        grant_kill_credit([leader, ally], mob)

        check_objectives.assert_any_call(leader, mob)
        check_objectives.assert_any_call(ally, mob)
        self.assertEqual(check_objectives.call_count, 2)

    @patch("world.mob_spawner.schedule_respawn_from_death")
    @patch("world.encounter_rewards.grant_kill_credit")
    def test_death_lifecycle_uses_the_frozen_participant_snapshot(
        self,
        grant_credit,
        _schedule_respawn,
    ):
        from world.death_lifecycle import on_mob_death

        room = MagicMock()
        killer = _player(1, "Killer", room)
        ally = _player(2, "Ally", room)
        mob = MagicMock()
        mob.key = "Ash Wolf"
        mob.location = None
        mob.db.triggers = False
        mob.db.tome_drop = None
        mob.db.rarity = "normal"
        mob.tags.get.return_value = None
        mob.ndb.encounter_reward_recipients = [killer, ally]

        on_mob_death(mob, killer)

        grant_credit.assert_called_once_with([killer, ally], mob)
        ally.msg.assert_called_once_with("|cYou receive nearby group credit for Ash Wolf.|n")


class TestNamedCombatProgression(EvenniaTest):
    @patch("world.quest_engine.check_kill_objectives")
    def test_named_kill_records_one_outcome_for_each_present_recipient(
        self,
        check_objectives,
    ):
        from world.encounter_rewards import grant_kill_credit
        from world.models import ProgressionEvent

        mob = MagicMock()
        mob.key = "The Ash Harrow"
        mob.db.named_id = "the_ash_harrow"
        mob.db.mob_template_key = "ash_harrow"
        mob.db.rarity = "rare"
        mob.tags.get.return_value = "the_ash_harrow"

        grant_kill_credit([self.char1, self.char2], mob)
        grant_kill_credit([self.char1, self.char2], mob)

        self.assertEqual(check_objectives.call_count, 4)
        events = ProgressionEvent.objects.filter(event_type="combat_outcome")
        self.assertEqual(events.count(), 2)
        for character in (self.char1, self.char2):
            event = events.get(character=character)
            self.assertEqual(event.source_id, "the_ash_harrow")
            self.assertEqual(event.domain_awards, {"combat": 25})

    @patch("world.quest_engine.check_kill_objectives")
    def test_ordinary_repeatable_kill_is_not_a_domain_progression_event(
        self,
        _check_objectives,
    ):
        from world.encounter_rewards import grant_kill_credit
        from world.models import ProgressionEvent

        mob = MagicMock()
        mob.key = "Ash Wolf"
        mob.db.named_id = None
        mob.db.mob_template_key = "ash_wolf"
        mob.db.rarity = "normal"
        mob.tags.get.return_value = None

        grant_kill_credit([self.char1], mob)

        self.assertFalse(ProgressionEvent.objects.exists())
