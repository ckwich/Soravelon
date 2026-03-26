"""
Minimal failing tests for join_guild and complete_induction mutation functions.
TDD RED phase for Task 1 of 04-02.
"""
import unittest


class TestJoinGuildExists(unittest.TestCase):
    """join_guild function must be importable from guild_engine."""

    def test_import(self):
        from world.guild_engine import join_guild
        self.assertTrue(callable(join_guild))


class TestCompleteInductionExists(unittest.TestCase):
    """complete_induction function must be importable from guild_engine."""

    def test_import(self):
        from world.guild_engine import complete_induction
        self.assertTrue(callable(complete_induction))
