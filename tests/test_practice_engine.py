import unittest
import sys
import types
from contextlib import contextmanager
from unittest.mock import Mock


class _Store:
    pass


class _Character:
    def __init__(self):
        self.db = _Store()
        self.ndb = _Store()
        self.messages = []

    def msg(self, text):
        self.messages.append(text)


@contextmanager
def _practice_dependencies():
    skill_engine = types.ModuleType("world.skill_engine")
    skill_engine.accumulate_skill_use = Mock()
    progression_engine = types.ModuleType("world.progression_engine")
    progression_engine.record_progression_event = Mock(
        return_value=(True, "")
    )
    quest_engine = types.ModuleType("world.quest_engine")
    quest_engine.check_practice_objectives = Mock()

    modules = {
        "world.skill_engine": skill_engine,
        "world.progression_engine": progression_engine,
        "world.quest_engine": quest_engine,
    }
    old_attrs = {
        name: getattr(sys.modules["world"], name, None)
        for name in ("skill_engine", "progression_engine", "quest_engine")
    }
    try:
        with unittest.mock.patch.dict(sys.modules, modules):
            sys.modules["world"].skill_engine = skill_engine
            sys.modules["world"].progression_engine = progression_engine
            sys.modules["world"].quest_engine = quest_engine
            yield skill_engine, progression_engine, quest_engine
    finally:
        for name, value in old_attrs.items():
            if value is None:
                try:
                    delattr(sys.modules["world"], name)
                except AttributeError:
                    pass
            else:
                setattr(sys.modules["world"], name, value)


class TestResolvePracticeOpportunity(unittest.TestCase):
    def test_awards_skill_domain_and_practice_objective_without_xp_numbers(self):
        from world.practice_engine import resolve_practice_opportunity

        character = _Character()
        payload = {
            "opportunity_id": "vp_canal_winch_repair",
            "verb": "repair",
            "target": "canal winch",
            "skill_awards": {"engineering": 4},
            "domain_awards": {"engineering": 120},
            "success_text": "You reset the canal winch and chalk the cracked tooth for the crew.",
        }

        with _practice_dependencies() as deps:
            skill_engine, progression_engine, quest_engine = deps
            success, message = resolve_practice_opportunity(
                payload, {"character": character, "args": "canal winch"}
            )

        self.assertTrue(success)
        self.assertEqual(message, "")
        skill_engine.accumulate_skill_use.assert_not_called()
        progression_engine.record_progression_event.assert_called_once_with(
            character,
            event_id="practice:vp_canal_winch_repair",
            event_type="practice",
            source_id="vp_canal_winch_repair",
            domain_awards={"engineering": 120},
            skill_awards={"engineering": 4},
        )
        quest_engine.check_practice_objectives.assert_called_once_with(character, "vp_canal_winch_repair")
        self.assertEqual(character.messages, [payload["success_text"]])
        self.assertNotIn("XP", character.messages[0])

    def test_rejects_target_mismatch_without_awarding(self):
        from world.practice_engine import resolve_practice_opportunity

        character = _Character()
        payload = {
            "opportunity_id": "vp_canal_winch_repair",
            "verb": "repair",
            "target": "canal winch",
            "skill_awards": {"engineering": 4},
            "success_text": "You reset the winch.",
        }

        with _practice_dependencies() as deps:
            skill_engine, _progression_engine, _quest_engine = deps
            success, message = resolve_practice_opportunity(
                payload, {"character": character, "args": "broken gate"}
            )

        self.assertFalse(success)
        self.assertIn("canal winch", message)
        skill_engine.accumulate_skill_use.assert_not_called()

    def test_rejects_empty_awards(self):
        from world.practice_engine import validate_practice_payload

        valid, message = validate_practice_payload({
            "opportunity_id": "empty_practice",
            "verb": "study",
            "target": "blank slate",
        })

        self.assertFalse(valid)
        self.assertIn("at least one award", message)

    def test_rejects_non_positive_award_values(self):
        from world.practice_engine import validate_practice_payload

        invalid_payloads = [
            {
                "opportunity_id": "zero_skill",
                "verb": "study",
                "skill_awards": {"investigation": 0},
            },
            {
                "opportunity_id": "negative_domain",
                "verb": "study",
                "domain_awards": {"tactics": -5},
            },
            {
                "opportunity_id": "bool_skill",
                "verb": "study",
                "skill_awards": {"navigation": True},
            },
        ]

        for payload in invalid_payloads:
            with self.subTest(opportunity_id=payload["opportunity_id"]):
                valid, message = validate_practice_payload(payload)
                self.assertFalse(valid)
                self.assertIn("positive integer", message)

    def test_once_per_character_blocks_repeat_awards(self):
        from world.practice_engine import resolve_practice_opportunity

        character = _Character()
        payload = {
            "opportunity_id": "old_lock_study",
            "verb": "study",
            "target": "old lock",
            "skill_awards": {"lockpicking": 3},
            "success_text": "You map the lock's worn bite marks.",
            "once_per_character": True,
        }

        with _practice_dependencies() as deps:
            skill_engine, _progression_engine, _quest_engine = deps
            first_success, _ = resolve_practice_opportunity(
                payload, {"character": character, "args": "old lock"}
            )
            second_success, second_message = resolve_practice_opportunity(
                payload, {"character": character, "args": "old lock"}
            )

        self.assertTrue(first_success)
        self.assertFalse(second_success)
        self.assertIn("already", second_message.lower())
        skill_engine.accumulate_skill_use.assert_not_called()

    def test_practice_opportunities_default_to_one_shot(self):
        from world.practice_engine import resolve_practice_opportunity

        character = _Character()
        payload = {
            "opportunity_id": "road_marker_survey",
            "verb": "survey",
            "target": "road marker",
            "skill_awards": {"navigation": 3},
            "domain_awards": {"tactics": 75},
            "success_text": "You sight the road marker against the ridge and fix the route in memory.",
        }

        with _practice_dependencies() as deps:
            skill_engine, progression_engine, quest_engine = deps
            first_success, _ = resolve_practice_opportunity(
                payload, {"character": character, "args": "road marker"}
            )
            second_success, second_message = resolve_practice_opportunity(
                payload, {"character": character, "args": "road marker"}
            )

        self.assertTrue(first_success)
        self.assertFalse(second_success)
        self.assertIn("already", second_message.lower())
        skill_engine.accumulate_skill_use.assert_not_called()
        progression_engine.record_progression_event.assert_called_once_with(
            character,
            event_id="practice:road_marker_survey",
            event_type="practice",
            source_id="road_marker_survey",
            domain_awards={"tactics": 75},
            skill_awards={"navigation": 3},
        )
        quest_engine.check_practice_objectives.assert_called_once_with(character, "road_marker_survey")

    def test_remnance_domain_award_is_not_player_facing_or_awarded(self):
        from world.practice_engine import resolve_practice_opportunity

        character = _Character()
        payload = {
            "opportunity_id": "forbidden_pattern",
            "verb": "study",
            "target": "sealed pattern",
            "skill_awards": {"investigation": 2},
            "domain_awards": {"remnance": 500},
            "success_text": "This text should never reach the player.",
        }

        with _practice_dependencies() as deps:
            skill_engine, progression_engine, _quest_engine = deps
            success, message = resolve_practice_opportunity(
                payload, {"character": character, "args": "sealed pattern"}
            )

        self.assertFalse(success)
        self.assertEqual(message, "That practice is not available.")
        self.assertEqual(character.messages, [])
        self.assertNotIn("remnance", message.lower())
        skill_engine.accumulate_skill_use.assert_not_called()
        progression_engine.record_progression_event.assert_not_called()
