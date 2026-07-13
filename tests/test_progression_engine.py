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
