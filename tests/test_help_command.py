"""Regression coverage for dynamic help resolution behavior."""

import unittest


class TestHelpCommand(unittest.TestCase):
    def test_resolve_ability_help_query_accepts_spaced_names(self):
        from commands.cmd_help import resolve_ability_help_query

        abilities = {
            "momentum_strike": {"id": "momentum_strike", "name": "Momentum Strike"},
            "wild_mend": {"id": "wild_mend", "name": "Wild Mend"},
        }

        ability, matches = resolve_ability_help_query("momentum strike", abilities)

        self.assertEqual(ability["id"], "momentum_strike")
        self.assertEqual(matches, [])

    def test_resolve_ability_help_query_supports_unique_prefixes(self):
        from commands.cmd_help import resolve_ability_help_query

        abilities = {
            "momentum_strike": {"id": "momentum_strike", "name": "Momentum Strike"},
            "wild_mend": {"id": "wild_mend", "name": "Wild Mend"},
        }

        ability, matches = resolve_ability_help_query("wild", abilities)

        self.assertEqual(ability["id"], "wild_mend")
        self.assertEqual(matches, [])

    def test_resolve_ability_help_query_reports_ambiguity(self):
        from commands.cmd_help import resolve_ability_help_query

        abilities = {
            "meteor_strike": {"id": "meteor_strike", "name": "Meteor Strike"},
            "meteor_guard": {"id": "meteor_guard", "name": "Meteor Guard"},
        }

        ability, matches = resolve_ability_help_query("meteor", abilities)

        self.assertIsNone(ability)
        self.assertEqual(
            {match["id"] for match in matches},
            {"meteor_guard", "meteor_strike"},
        )
