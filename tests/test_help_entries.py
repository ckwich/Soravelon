"""
Tests for file-backed help entry registration and content presence.
"""

import ast
import unittest
from pathlib import Path


def _iter_custom_command_keys():
    """Yield concrete command keys authored in the local commands package."""
    commands_dir = Path(__file__).resolve().parents[1] / "commands"
    for path in sorted(commands_dir.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            base_names = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    base_names.append(base.id)
                elif isinstance(base, ast.Attribute):
                    base_names.append(base.attr)
            if not any(name in {"Command", "EvenniaCmdHelp"} for name in base_names):
                continue

            key = None
            for stmt in node.body:
                if not isinstance(stmt, ast.Assign):
                    continue
                for target in stmt.targets:
                    if (
                        isinstance(target, ast.Name)
                        and target.id == "key"
                        and isinstance(stmt.value, ast.Constant)
                        and isinstance(stmt.value.value, str)
                    ):
                        key = stmt.value.value
            if key:
                yield key


class TestHelpEntries(unittest.TestCase):
    def test_settings_register_help_module(self):
        from server.conf import settings

        self.assertIn("world.help_entries", settings.FILE_HELP_ENTRY_MODULES)

    def test_help_entries_module_imports(self):
        from world import help_entries

        self.assertTrue(hasattr(help_entries, "HELP_ENTRY_DICTS"))

    def test_getting_started_topic_exists(self):
        from world.help_entries import HELP_ENTRY_DICTS

        keys = {entry["key"] for entry in HELP_ENTRY_DICTS}
        self.assertIn("getting started", keys)

    def test_getting_started_briefs_players_on_starter_kit(self):
        from world.help_entries import HELP_ENTRY_DICTS

        getting_started = next(
            entry for entry in HELP_ENTRY_DICTS if entry["key"] == "getting started"
        )
        text = getting_started["text"]
        self.assertIn("inventory", text)
        self.assertIn("gear", text)
        self.assertIn("equip <item>", text)
        self.assertIn("Starter kit briefing", text)

    def test_live_command_topics_exist_for_core_player_surface(self):
        from world.help_entries import HELP_ENTRY_DICTS

        keys = {entry["key"] for entry in HELP_ENTRY_DICTS}
        for key in (
            "abilities",
            "ancestry",
            "domains",
            "group",
            "joinguild",
            "quest",
            "skills",
        ):
            self.assertIn(key, keys)

    def test_guild_help_keeps_induction_local_and_progression_qualitative(self):
        from world.help_entries import HELP_ENTRY_DICTS

        by_key = {entry["key"]: entry["text"] for entry in HELP_ENTRY_DICTS}
        combined = by_key["guilds"] + by_key["joinguild"] + by_key["domains"]
        self.assertIn("talk", combined.lower())
        self.assertIn("accept <secondary_domain>", combined.lower())
        self.assertNotIn("joinguild <guild_name> <secondary_domain>", combined)
        self.assertNotIn("guild tier score", combined.lower())
        self.assertNotIn("tier thresholds", combined.lower())
        self.assertNotIn("domain scores", combined.lower())

    def test_every_custom_command_has_direct_help_coverage(self):
        from world.help_entries import HELP_ENTRY_DICTS

        help_keys = {entry["key"] for entry in HELP_ENTRY_DICTS}
        help_aliases = {
            alias
            for entry in HELP_ENTRY_DICTS
            for alias in (entry.get("aliases") or [])
        }

        missing = sorted(
            {
                key for key in _iter_custom_command_keys()
                if key not in help_keys and key not in help_aliases
            }
        )
        self.assertEqual(missing, [], f"Missing command help topics: {missing}")

    def test_every_skill_has_a_direct_help_topic(self):
        from world.help_entries import HELP_ENTRY_DICTS
        from world.skill_definitions import SKILL_DEFINITIONS

        help_keys = {entry["key"] for entry in HELP_ENTRY_DICTS}
        help_aliases = {
            alias
            for entry in HELP_ENTRY_DICTS
            for alias in (entry.get("aliases") or [])
        }

        missing = []
        for skill_key, skill_def in SKILL_DEFINITIONS.items():
            title = skill_def.get("name", skill_key).lower()
            if (
                skill_key not in help_keys
                and title not in help_keys
                and skill_key not in help_aliases
                and title not in help_aliases
            ):
                missing.append(skill_key)

        self.assertEqual(missing, [], f"Missing skill help topics: {missing}")

    def test_group_help_matches_runtime_loot_modes(self):
        from world.help_entries import HELP_ENTRY_DICTS

        group_entry = next(entry for entry in HELP_ENTRY_DICTS if entry["key"] == "group")
        text = group_entry["text"]
        self.assertIn("lootmode", text)
        self.assertNotIn("group loot <mode>", text)
        self.assertIn("personal", text)
        self.assertIn("ffa", text)
        self.assertIn("round_robin", text)
        self.assertNotIn("need/greed", text)
        self.assertIn("leadership passes", text)
        self.assertNotIn("dissolve if the leader disconnects", text)

    def test_loot_help_explains_personal_encounter_claims(self):
        from world.help_entries import HELP_ENTRY_DICTS

        loot_entry = next(entry for entry in HELP_ENTRY_DICTS if entry["key"] == "loot")
        text = loot_entry["text"]

        self.assertIn("loot rewards", text)
        self.assertIn("personal reward", text)
        self.assertIn("shared drops", text)

    def test_domains_command_no_longer_shadows_skills(self):
        from commands.cmd_domains import CmdDomains

        self.assertNotIn("skills", CmdDomains.aliases)

    def test_generated_skill_help_includes_progression_guidance(self):
        from world.help_entries import HELP_ENTRY_DICTS

        first_aid = next(
            entry for entry in HELP_ENTRY_DICTS
            if entry["key"] == "first aid" or "first_aid" in (entry.get("aliases") or [])
        )
        self.assertIn("How It Improves", first_aid["text"])
        self.assertIn("Milestones", first_aid["text"])

    def test_loadout_help_matches_live_command_shape(self):
        from world.help_entries import HELP_ENTRY_DICTS

        loadout = next(entry for entry in HELP_ENTRY_DICTS if entry["key"] == "loadout")
        self.assertIn("loadout add <ability>", loadout["text"])
        self.assertIn("loadout remove <ability>", loadout["text"])
        self.assertIn("loadout save <slot#>", loadout["text"])
        self.assertNotIn("loadout set <slot>", loadout["text"])

    def test_tell_help_covers_npcs_and_players(self):
        from world.help_entries import HELP_ENTRY_DICTS

        tell = next(entry for entry in HELP_ENTRY_DICTS if entry["key"] == "tell")
        self.assertIn("tell <npc> <text>", tell["text"])
        self.assertIn("tell <player> <message>", tell["text"])
        self.assertIn("NPC", tell["text"])
        self.assertIn("online player", tell["text"])

    def test_encumbrance_help_does_not_promise_item_banking(self):
        from world.help_entries import HELP_ENTRY_DICTS

        encumbrance = next(
            entry for entry in HELP_ENTRY_DICTS if entry["key"] == "encumbrance"
        )

        self.assertNotIn("bank vault", encumbrance["text"].lower())
        self.assertIn("weight reduction", encumbrance["text"].lower())
