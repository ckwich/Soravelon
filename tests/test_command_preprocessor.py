"""
Tests for the command preprocessor (Plan 01-03, Task 1).

Written FIRST per TDD discipline. These must all fail before
any production code is written.

Note: Tests use unittest.TestCase (not EvenniaTest) because the preprocessor
is pure logic and uses only MagicMock — no Evennia DB setup required.
"""

import unittest
from unittest.mock import MagicMock


class TestResolvePrefixExactMatch(unittest.TestCase):
    """Exact match on a command key returns it immediately."""

    def test_exact_match_returns_key(self):
        from world.command_preprocessor import resolve_prefix

        resolved, matches = resolve_prefix("north", ["north", "attack", "attune"])
        self.assertEqual(resolved, "north")
        self.assertEqual(matches, [])

    def test_exact_match_case_insensitive(self):
        from world.command_preprocessor import resolve_prefix

        resolved, matches = resolve_prefix("NORTH", ["north", "attack"])
        self.assertEqual(resolved, "north")
        self.assertEqual(matches, [])


class TestResolvePrefixUnique(unittest.TestCase):
    """Unique prefix expands to the single matching command."""

    def test_unique_prefix_resolves(self):
        from world.command_preprocessor import resolve_prefix

        resolved, matches = resolve_prefix("no", ["north", "attack"])
        self.assertEqual(resolved, "north")
        self.assertEqual(matches, [])

    def test_single_letter_unique(self):
        from world.command_preprocessor import resolve_prefix

        resolved, matches = resolve_prefix("n", ["north", "attack", "drop"])
        self.assertEqual(resolved, "north")
        self.assertEqual(matches, [])


class TestResolvePrefixAmbiguous(unittest.TestCase):
    """Ambiguous prefix returns None and the sorted match list."""

    def test_ambiguous_prefix_returns_none_with_matches(self):
        from world.command_preprocessor import resolve_prefix

        resolved, matches = resolve_prefix("att", ["attack", "attune", "north"])
        self.assertIsNone(resolved)
        self.assertEqual(matches, ["attack", "attune"])

    def test_matches_are_sorted(self):
        from world.command_preprocessor import resolve_prefix

        resolved, matches = resolve_prefix("ca", ["cast", "carry", "cart"])
        self.assertIsNone(resolved)
        self.assertEqual(matches, sorted(["cast", "carry", "cart"]))


class TestResolvePrefixNoMatch(unittest.TestCase):
    """No-match prefix returns (None, []) to pass through to Evennia."""

    def test_no_match_returns_none_empty(self):
        from world.command_preprocessor import resolve_prefix

        resolved, matches = resolve_prefix("xyz", ["north", "attack"])
        self.assertIsNone(resolved)
        self.assertEqual(matches, [])


class TestExpandAliasTokenSubstitution(unittest.TestCase):
    """expand_alias correctly substitutes $1, $2, $*, $@ tokens."""

    def _make_char(self, aliases):
        char = MagicMock()
        char.db.aliases = aliases
        return char

    def test_dollar1_substitution(self):
        from world.command_preprocessor import expand_alias

        char = self._make_char({"kill": "attack $1"})
        result = expand_alias(char, "kill", "orc")
        self.assertEqual(result, ["attack orc"])

    def test_dollar_star_substitution(self):
        from world.command_preprocessor import expand_alias

        char = self._make_char({"taunt": "emote taunts $*"})
        result = expand_alias(char, "taunt", "the orc with fury")
        self.assertEqual(result, ["emote taunts the orc with fury"])

    def test_dollar_at_substitution(self):
        from world.command_preprocessor import expand_alias

        char = self._make_char({"target": "attack $@"})
        result = expand_alias(char, "target", "dark elf")
        self.assertEqual(result, ["attack dark elf"])

    def test_missing_token_leaves_empty(self):
        from world.command_preprocessor import expand_alias

        char = self._make_char({"k": "attack $1"})
        result = expand_alias(char, "k", "")
        self.assertEqual(result, ["attack "])

    def test_multiple_tokens(self):
        from world.command_preprocessor import expand_alias

        char = self._make_char({"swap": "equip $2; unequip $1"})
        result = expand_alias(char, "swap", "sword shield")
        self.assertEqual(result, ["equip shield", "unequip sword"])


class TestExpandAliasChainCap(unittest.TestCase):
    """expand_alias caps chained commands at 3 (D-16)."""

    def _make_char(self, aliases):
        char = MagicMock()
        char.db.aliases = aliases
        return char

    def test_chain_capped_at_3(self):
        from world.command_preprocessor import expand_alias

        char = self._make_char({"big": "a; b; c; d"})
        result = expand_alias(char, "big", "")
        self.assertEqual(len(result), 3)
        self.assertEqual(result, ["a", "b", "c"])

    def test_three_commands_allowed(self):
        from world.command_preprocessor import expand_alias

        char = self._make_char({"buff": "cast shield; cast haste; cast blessing"})
        result = expand_alias(char, "buff", "")
        self.assertEqual(result, ["cast shield", "cast haste", "cast blessing"])


class TestExpandAliasNotFound(unittest.TestCase):
    """expand_alias returns None for unknown alias or no aliases set."""

    def _make_char(self, aliases):
        char = MagicMock()
        char.db.aliases = aliases
        return char

    def test_unknown_alias_returns_none(self):
        from world.command_preprocessor import expand_alias

        char = self._make_char({"k": "attack $1"})
        result = expand_alias(char, "unknown", "arg")
        self.assertIsNone(result)

    def test_no_aliases_returns_none(self):
        from world.command_preprocessor import expand_alias

        char = self._make_char(None)
        result = expand_alias(char, "k", "orc")
        self.assertIsNone(result)


class TestPreprocessInputSystemExactMatch(unittest.TestCase):
    """preprocess_input returns raw_string unchanged when first word is an exact system command."""

    def _make_char(self, all_keys, aliases=None):
        char = MagicMock()
        char.db.aliases = aliases or {}
        # Build fake cmdset list structure
        cmd_mock = MagicMock()
        cmd_mock.key = None
        cmd_mock.aliases = []
        cmdset_mock = MagicMock()
        cmdset_mock.commands = []
        for key in all_keys:
            c = MagicMock()
            c.key = key
            c.aliases = []
            cmdset_mock.commands.append(c)
        char.cmdset.all.return_value = [cmdset_mock]
        return char

    def test_exact_system_command_returned_unchanged(self):
        from world.command_preprocessor import preprocess_input

        char = self._make_char(["look", "north", "attack"])
        result = preprocess_input(char, "look")
        self.assertEqual(result, "look")

    def test_exact_system_command_with_args_returned_unchanged(self):
        from world.command_preprocessor import preprocess_input

        char = self._make_char(["look", "north", "attack"])
        result = preprocess_input(char, "look here")
        self.assertEqual(result, "look here")

    def test_system_command_not_shadowed_by_alias(self):
        """D-17: alias should NOT override exact-match system command."""
        from world.command_preprocessor import preprocess_input

        char = self._make_char(["look", "north"], aliases={"look": "examine $1"})
        result = preprocess_input(char, "look")
        self.assertEqual(result, "look")


class TestPreprocessInputPrefixResolution(unittest.TestCase):
    """preprocess_input expands unique prefix to full command name."""

    def _make_char(self, all_keys, aliases=None):
        char = MagicMock()
        char.db.aliases = aliases or {}
        cmdset_mock = MagicMock()
        cmdset_mock.commands = []
        for key in all_keys:
            c = MagicMock()
            c.key = key
            c.aliases = []
            cmdset_mock.commands.append(c)
        char.cmdset.all.return_value = [cmdset_mock]
        return char

    def test_unique_prefix_expands(self):
        from world.command_preprocessor import preprocess_input

        char = self._make_char(["north", "attack"])
        result = preprocess_input(char, "no")
        self.assertEqual(result, "north")

    def test_prefix_with_args_preserved(self):
        from world.command_preprocessor import preprocess_input

        char = self._make_char(["attack", "north"])
        result = preprocess_input(char, "att orc")
        # "att" is unique prefix for "attack"
        self.assertEqual(result, "attack orc")


class TestPreprocessInputAmbiguousPrefix(unittest.TestCase):
    """Ambiguous prefix sends error message and returns None (D-14)."""

    def _make_char(self, all_keys, aliases=None):
        char = MagicMock()
        char.db.aliases = aliases or {}
        cmdset_mock = MagicMock()
        cmdset_mock.commands = []
        for key in all_keys:
            c = MagicMock()
            c.key = key
            c.aliases = []
            cmdset_mock.commands.append(c)
        char.cmdset.all.return_value = [cmdset_mock]
        return char

    def test_ambiguous_sends_did_you_mean(self):
        from world.command_preprocessor import preprocess_input

        char = self._make_char(["attack", "attune"])
        result = preprocess_input(char, "att")
        self.assertIsNone(result)
        char.msg.assert_called_once()
        call_arg = char.msg.call_args[0][0]
        self.assertIn("Did you mean", call_arg)
        self.assertIn("attack", call_arg)
        self.assertIn("attune", call_arg)


class TestPreprocessInputAliasExpansion(unittest.TestCase):
    """preprocess_input expands aliases to list of commands."""

    def _make_char(self, all_keys, aliases=None):
        char = MagicMock()
        char.db.aliases = aliases or {}
        cmdset_mock = MagicMock()
        cmdset_mock.commands = []
        for key in all_keys:
            c = MagicMock()
            c.key = key
            c.aliases = []
            cmdset_mock.commands.append(c)
        char.cmdset.all.return_value = [cmdset_mock]
        return char

    def test_alias_expands_to_list(self):
        from world.command_preprocessor import preprocess_input

        char = self._make_char(["attack", "north"], aliases={"kill": "attack $1"})
        result = preprocess_input(char, "kill orc")
        self.assertIsInstance(result, list)
        self.assertEqual(result, ["attack orc"])

    def test_chained_alias_expands_to_list(self):
        from world.command_preprocessor import preprocess_input

        char = self._make_char(
            ["cast", "north"],
            aliases={"buff": "cast shield; cast haste; cast blessing"},
        )
        result = preprocess_input(char, "buff")
        self.assertEqual(result, ["cast shield", "cast haste", "cast blessing"])
