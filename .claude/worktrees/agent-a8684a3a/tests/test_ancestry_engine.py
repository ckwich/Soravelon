"""
Tests for world/ancestry_engine.py.

Covers ANC-01 through ANC-05: four playable ancestries, starting standings,
trait lookup, and rejection of invalid/duplicate ancestry selection.

Uses unittest.TestCase + MagicMock -- pure logic, no DB needed.
"""
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch, call


# ---------------------------------------------------------------------------
# Helper: mock character with db namespace
# ---------------------------------------------------------------------------

def _mock_character(ancestry=None, selvar_coat=None):
    """Create a MagicMock character with db attributes for ancestry tests."""
    char = MagicMock()
    char.db = SimpleNamespace(ancestry=ancestry, selvar_coat=selvar_coat)
    return char


# ===========================================================================
# ANC-01: Human ancestry
# ===========================================================================


class TestHumanAncestry(unittest.TestCase):
    """Human ancestry sets db.ancestry and applies Empire +10k standing."""

    @patch("world.world_state.modify_standing")
    def test_human_sets_ancestry(self, mock_modify):
        from world.ancestry_engine import set_ancestry

        char = _mock_character()
        ok, msg = set_ancestry(char, "human")

        self.assertTrue(ok)
        self.assertEqual(char.db.ancestry, "human")

    @patch("world.world_state.modify_standing")
    def test_human_empire_standing(self, mock_modify):
        from world.ancestry_engine import set_ancestry

        char = _mock_character()
        set_ancestry(char, "human")

        mock_modify.assert_called_once_with(
            char, "empire", 10000, "ancestry_starting"
        )


# ===========================================================================
# ANC-02: Kauroran ancestry
# ===========================================================================


class TestKauroranAncestry(unittest.TestCase):
    """Kauroran ancestry applies 3 faction standings."""

    @patch("world.world_state.modify_standing")
    def test_kauroran_three_standings(self, mock_modify):
        from world.ancestry_engine import set_ancestry

        char = _mock_character()
        set_ancestry(char, "kauroran")

        expected_calls = [
            call(char, "kauroran", 20000, "ancestry_starting"),
            call(char, "wardens", 10000, "ancestry_starting"),
            call(char, "empire", -15000, "ancestry_starting"),
        ]
        mock_modify.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_modify.call_count, 3)


# ===========================================================================
# ANC-03: Veth ancestry
# ===========================================================================


class TestVethAncestry(unittest.TestCase):
    """Veth ancestry applies Consortium +7500 standing."""

    @patch("world.world_state.modify_standing")
    def test_veth_consortium(self, mock_modify):
        from world.ancestry_engine import set_ancestry

        char = _mock_character()
        set_ancestry(char, "veth")

        mock_modify.assert_called_once_with(
            char, "consortium", 7500, "ancestry_starting"
        )


# ===========================================================================
# ANC-04: Selvar ancestry
# ===========================================================================


class TestSelvarAncestry(unittest.TestCase):
    """Selvar ancestry requires coat, applies -5k to all factions + guild offset."""

    @patch("world.world_state.modify_standing")
    def test_selvar_requires_coat(self, mock_modify):
        from world.ancestry_engine import set_ancestry

        char = _mock_character()
        ok, msg = set_ancestry(char, "selvar")

        self.assertFalse(ok)
        self.assertIn("coat", msg.lower())
        mock_modify.assert_not_called()

    @patch("world.world_state.modify_standing")
    def test_selvar_summer_coat(self, mock_modify):
        from world.ancestry_engine import set_ancestry

        char = _mock_character()
        ok, msg = set_ancestry(char, "selvar", coat="summer")

        self.assertTrue(ok)
        self.assertEqual(char.db.selvar_coat, "summer")
        self.assertEqual(char.db.ancestry, "selvar")

    @patch("world.world_state.modify_standing")
    def test_selvar_all_factions_penalty(self, mock_modify):
        from world.ancestry_engine import set_ancestry, KNOWN_FACTIONS_AT_CREATION

        char = _mock_character()
        set_ancestry(char, "selvar", coat="winter")

        # -5000 penalty for each of 4 known factions + 2500 guild offset = 5 calls
        expected_calls = []
        for faction_id in KNOWN_FACTIONS_AT_CREATION:
            expected_calls.append(
                call(char, faction_id, -5000, "ancestry_starting")
            )
        expected_calls.append(
            call(char, "guilds", 2500, "ancestry_starting")
        )

        mock_modify.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_modify.call_count, 5)


# ===========================================================================
# ANC-05: Rejection cases
# ===========================================================================


class TestAncestryRejection(unittest.TestCase):
    """Ancestry engine rejects duplicate and unknown ancestry choices."""

    @patch("world.world_state.modify_standing")
    def test_rejects_second_ancestry(self, mock_modify):
        from world.ancestry_engine import set_ancestry

        char = _mock_character(ancestry="human")
        ok, msg = set_ancestry(char, "veth")

        self.assertFalse(ok)
        self.assertIn("already", msg.lower())
        mock_modify.assert_not_called()

    @patch("world.world_state.modify_standing")
    def test_rejects_unknown_ancestry(self, mock_modify):
        from world.ancestry_engine import set_ancestry

        char = _mock_character()
        ok, msg = set_ancestry(char, "dwarf")

        self.assertFalse(ok)
        self.assertIn("unknown", msg.lower())
        mock_modify.assert_not_called()


# ===========================================================================
# Trait lookup
# ===========================================================================


class TestGetAncestryTrait(unittest.TestCase):
    """get_ancestry_trait returns trait values or defaults."""

    def test_returns_trait_value(self):
        from world.ancestry_engine import get_ancestry_trait

        char = _mock_character(ancestry="human")
        result = get_ancestry_trait(char, "reputation_generation")
        self.assertEqual(result, 1.15)

    def test_returns_default_when_no_ancestry(self):
        from world.ancestry_engine import get_ancestry_trait

        char = _mock_character(ancestry=None)
        result = get_ancestry_trait(char, "hp_bonus", default=42)
        self.assertEqual(result, 42)

    def test_returns_default_for_missing_trait(self):
        from world.ancestry_engine import get_ancestry_trait

        char = _mock_character(ancestry="human")
        result = get_ancestry_trait(char, "nonexistent_trait", default="nope")
        self.assertEqual(result, "nope")
