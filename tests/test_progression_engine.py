"""Durability and idempotency contracts for authored progression events."""

from unittest.mock import patch

from evennia.utils.test_resources import EvenniaTest

from world.models import ProgressionEvent


class TestProgressionEventIdentity(EvenniaTest):
    def test_identical_replay_is_noop_and_conflicting_reuse_fails_closed(self):
        from world.progression_engine import record_progression_event

        event = {
            "event_id": "quest:missing-shipment:outcome",
            "event_type": "quest_outcome",
            "source_id": "vc_q_missing_shipment",
            "domain_awards": {"naturalism": 75},
            "skill_awards": {"investigation": 10},
        }

        first = record_progression_event(self.char1, **event)
        replay = record_progression_event(self.char1, **event)
        conflict = record_progression_event(
            self.char1,
            **{**event, "skill_awards": {"investigation": 20}},
        )

        self.assertEqual(first, (True, ""))
        self.assertEqual(replay, (True, ""))
        self.assertFalse(conflict[0])
        self.assertIn("different awards", conflict[1])
        self.assertEqual(
            ProgressionEvent.objects.filter(character=self.char1).count(),
            1,
        )

    def test_hidden_current_era_domain_cannot_be_recorded(self):
        from world.progression_engine import record_progression_event

        success, message = record_progression_event(
            self.char1,
            event_id="investigation:sealed-pattern",
            event_type="investigation",
            source_id="sealed_pattern",
            domain_awards={"remnance": 75},
        )

        self.assertFalse(success)
        self.assertNotIn("remnance", message.lower())
        self.assertFalse(
            ProgressionEvent.objects.filter(character=self.char1).exists()
        )

    def test_hidden_domain_can_progress_only_after_its_story_visibility_gate(self):
        from world.progression_engine import record_progression_event

        self.char1.db.remnance_player_visible = True
        success, message = record_progression_event(
            self.char1,
            event_id="investigation:opened-pattern",
            event_type="investigation",
            source_id="opened_pattern",
            domain_awards={"remnance": 10},
        )

        self.assertTrue(success, message)
        event = ProgressionEvent.objects.get(character=self.char1)
        self.assertEqual(event.domain_awards, {"remnance": 10})


class TestMeaningfulOutcomePolicies(EvenniaTest):
    def test_gathering_and_crafting_reward_first_mastery_not_repetition(self):
        from world.progression_engine import (
            record_crafting_outcome,
            record_gathering_outcome,
        )

        first_gather = record_gathering_outcome(self.char1, "greyteeth_iron")
        repeated_gather = record_gathering_outcome(self.char1, "greyteeth_iron")
        first_craft = record_crafting_outcome(self.char1, "iron_ingot")
        repeated_craft = record_crafting_outcome(self.char1, "iron_ingot")

        self.assertEqual(first_gather, (True, ""))
        self.assertEqual(repeated_gather, (True, ""))
        self.assertEqual(first_craft, (True, ""))
        self.assertEqual(repeated_craft, (True, ""))
        events = {
            event.event_type: event
            for event in ProgressionEvent.objects.filter(character=self.char1)
        }
        self.assertEqual(set(events), {"gathering", "crafting"})
        self.assertEqual(events["gathering"].source_id, "greyteeth_iron")
        self.assertEqual(events["gathering"].domain_awards, {"combat": 10})
        self.assertEqual(events["gathering"].skill_awards, {})
        self.assertEqual(events["crafting"].source_id, "iron_ingot")
        self.assertEqual(events["crafting"].domain_awards, {"engineering": 5})
        self.assertEqual(events["crafting"].skill_awards, {})

    def test_landmark_and_novel_investigation_use_distinct_typed_events(self):
        from world.progression_engine import (
            record_exploration_outcome,
            record_investigation_outcome,
        )

        explored = record_exploration_outcome(self.char1, "vaels_crossing")
        investigated = record_investigation_outcome(self.char1, "old_archive")

        self.assertEqual(explored, (True, ""))
        self.assertEqual(investigated, (True, ""))
        exploration = ProgressionEvent.objects.get(
            character=self.char1,
            event_type="exploration",
        )
        investigation = ProgressionEvent.objects.get(
            character=self.char1,
            event_type="investigation",
        )
        self.assertEqual(exploration.domain_awards, {"tactics": 20})
        self.assertEqual(exploration.skill_awards, {"navigation": 2})
        self.assertEqual(investigation.domain_awards, {})
        self.assertEqual(investigation.skill_awards, {"investigation": 1})

    def test_named_and_legendary_combat_outcomes_are_one_time_achievements(self):
        from world.progression_engine import record_combat_outcome

        normal = record_combat_outcome(
            self.char1,
            "ash_wolf",
            is_named=False,
            is_legendary=False,
        )
        named = record_combat_outcome(
            self.char1,
            "the-ash-harrow",
            is_named=True,
            is_legendary=False,
        )
        legendary = record_combat_outcome(
            self.char1,
            "the-glass-tyrant",
            is_named=True,
            is_legendary=True,
        )
        repeated = record_combat_outcome(
            self.char1,
            "the-glass-tyrant",
            is_named=True,
            is_legendary=True,
        )

        self.assertEqual(normal, (True, ""))
        self.assertEqual(named, (True, ""))
        self.assertEqual(legendary, (True, ""))
        self.assertEqual(repeated, (True, ""))
        events = list(
            ProgressionEvent.objects.filter(
                character=self.char1,
                event_type="combat_outcome",
            ).order_by("source_id")
        )
        self.assertEqual(len(events), 2)
        self.assertEqual(
            {event.source_id: event.domain_awards for event in events},
            {
                "the-ash-harrow": {"combat": 25},
                "the-glass-tyrant": {"combat": 50},
            },
        )


class TestDurablePracticeProgression(EvenniaTest):
    def test_earned_domain_progress_survives_volatile_accumulator_loss(self):
        from world.practice_engine import resolve_practice_opportunity
        from world.world_state import commit_session_xp, init_session_accumulators

        self.char1.db.domain_scores = {}
        init_session_accumulators(self.char1)
        payload = {
            "opportunity_id": "durable_wolf_sign",
            "verb": "track",
            "target": "wolf sign",
            "skill_awards": {"tracking": 10},
            "domain_awards": {"naturalism": 75},
            "success_text": "You separate the wolf prints from the road traffic.",
            "once_per_character": True,
        }

        success, message = resolve_practice_opportunity(
            payload,
            {"character": self.char1, "args": "wolf sign"},
        )
        self.assertTrue(success, message)

        # Simulate process/session recovery before the natural commit point.
        init_session_accumulators(self.char1)
        commit_session_xp(self.char1)

        self.assertEqual(self.char1.db.domain_scores, {"naturalism": 7.5})
        from world.models import CharacterSkill

        skill = CharacterSkill.objects.get(character=self.char1, skill_id="tracking")
        self.assertEqual(skill.value, 0.1)
        self.assertEqual(skill.passive_use_remainder, 0)
        event = ProgressionEvent.objects.get(character=self.char1)
        self.assertIsNotNone(event.applied_at)

        # A second recovery/commit cannot apply the durable event again.
        init_session_accumulators(self.char1)
        commit_session_xp(self.char1)
        self.assertEqual(self.char1.db.domain_scores, {"naturalism": 7.5})
        skill.refresh_from_db()
        self.assertEqual(skill.value, 0.1)

    def test_failed_atomic_apply_repairs_evennia_attribute_cache_for_retry(self):
        from world.progression_engine import record_progression_event
        from world.world_state import commit_session_xp, init_session_accumulators

        self.char1.db.domain_scores = {}
        init_session_accumulators(self.char1)
        success, message = record_progression_event(
            self.char1,
            event_id="practice:cache-repair",
            event_type="practice",
            source_id="cache_repair",
            domain_awards={"naturalism": 75},
            skill_awards={"tracking": 10},
        )
        self.assertTrue(success, message)

        with patch(
            "world.skill_engine.apply_skill_use_counts",
            side_effect=RuntimeError("forced skill write failure"),
        ):
            with self.assertRaisesRegex(RuntimeError, "forced skill write failure"):
                commit_session_xp(self.char1)

        event = ProgressionEvent.objects.get(character=self.char1)
        self.assertIsNone(event.applied_at)
        self.assertEqual(self.char1.db.domain_scores, {})

        commit_session_xp(self.char1)
        self.assertEqual(self.char1.db.domain_scores, {"naturalism": 7.5})
