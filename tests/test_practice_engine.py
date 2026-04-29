import unittest
from unittest.mock import patch


class _Store:
    pass


class _Character:
    def __init__(self):
        self.db = _Store()
        self.ndb = _Store()
        self.messages = []

    def msg(self, text):
        self.messages.append(text)


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

        with patch("world.skill_engine.accumulate_skill_use") as mock_skill, \
                patch("world.world_state.accumulate_domain_xp") as mock_domain, \
                patch("world.quest_engine.check_practice_objectives") as mock_quest:
            success, message = resolve_practice_opportunity(
                payload, {"character": character, "args": "canal winch"}
            )

        self.assertTrue(success)
        self.assertEqual(message, "")
        mock_skill.assert_called_once_with(character, "engineering", 4)
        mock_domain.assert_called_once_with(character, "engineering", 120)
        mock_quest.assert_called_once_with(character, "vp_canal_winch_repair")
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

        with patch("world.skill_engine.accumulate_skill_use") as mock_skill:
            success, message = resolve_practice_opportunity(
                payload, {"character": character, "args": "broken gate"}
            )

        self.assertFalse(success)
        self.assertIn("canal winch", message)
        mock_skill.assert_not_called()

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

        with patch("world.skill_engine.accumulate_skill_use") as mock_skill, \
                patch("world.quest_engine.check_practice_objectives"):
            first_success, _ = resolve_practice_opportunity(
                payload, {"character": character, "args": "old lock"}
            )
            second_success, second_message = resolve_practice_opportunity(
                payload, {"character": character, "args": "old lock"}
            )

        self.assertTrue(first_success)
        self.assertFalse(second_success)
        self.assertIn("already", second_message.lower())
        mock_skill.assert_called_once_with(character, "lockpicking", 3)

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

        with patch("world.skill_engine.accumulate_skill_use") as mock_skill, \
                patch("world.world_state.accumulate_domain_xp") as mock_domain:
            success, message = resolve_practice_opportunity(
                payload, {"character": character, "args": "sealed pattern"}
            )

        self.assertFalse(success)
        self.assertEqual(message, "That practice is not available.")
        self.assertEqual(character.messages, [])
        self.assertNotIn("remnance", message.lower())
        mock_skill.assert_not_called()
        mock_domain.assert_not_called()
