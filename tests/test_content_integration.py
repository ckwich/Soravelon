"""
Integration tests for Phase 7 content:
- CmdStabilize node interaction command
- Zone spec file imports
- Zone build() function callability
- Spawn/respawn tag wiring
"""

import ast
import os
import pathlib
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

# Django setup required for Evennia command imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django  # noqa: E402
django.setup()


# ---------------------------------------------------------------------------
# Zone file import tests (pure Python, no Evennia DB needed)
# ---------------------------------------------------------------------------

class TestZoneImports(unittest.TestCase):
    """Verify authored zone spec files and equipment catalog import cleanly."""

    def test_vaels_crossing_imports(self):
        from world.areas import vaels_crossing
        self.assertTrue(hasattr(vaels_crossing, "build"))

    def test_ashreach_plains_imports(self):
        from world.areas import ashreach_plains
        self.assertTrue(hasattr(ashreach_plains, "build"))

    def test_reth_foothills_imports(self):
        from world.areas import reth_foothills
        self.assertTrue(hasattr(reth_foothills, "build"))

    def test_cantera_edge_imports(self):
        from world.areas import cantera_edge
        self.assertTrue(hasattr(cantera_edge, "build"))

    def test_stormhaven_coast_imports(self):
        from world.areas import stormhaven_coast
        self.assertTrue(hasattr(stormhaven_coast, "build"))

    def test_varath_prime_imports(self):
        from world.areas import varath_prime
        self.assertTrue(hasattr(varath_prime, "build"))

    def test_crownroad_north_imports(self):
        from world.areas import crownroad_north
        self.assertTrue(hasattr(crownroad_north, "build"))

    def test_old_causeway_imports(self):
        from world.areas import old_causeway
        self.assertTrue(hasattr(old_causeway, "build"))

    def test_ironvein_escarpment_imports(self):
        from world.areas import ironvein_escarpment
        self.assertTrue(hasattr(ironvein_escarpment, "build"))

    def test_stagcrown_preserve_imports(self):
        from world.areas import stagcrown_preserve
        self.assertTrue(hasattr(stagcrown_preserve, "build"))

    def test_korahei_imports(self):
        from world.areas import korahei
        self.assertTrue(hasattr(korahei, "build"))

    def test_veluana_outer_reefs_imports(self):
        from world.areas import veluana_outer_reefs
        self.assertTrue(hasattr(veluana_outer_reefs, "build"))

    def test_kiai_grounds_imports(self):
        from world.areas import kiai_grounds
        self.assertTrue(hasattr(kiai_grounds, "build"))

    def test_veluana_central_isle_imports(self):
        from world.areas import veluana_central_isle
        self.assertTrue(hasattr(veluana_central_isle, "build"))

    def test_colonist_ruins_imports(self):
        from world.areas import colonist_ruins
        self.assertTrue(hasattr(colonist_ruins, "build"))

    def test_equipment_catalog_imports(self):
        from world.areas import equipment_catalog
        self.assertTrue(hasattr(equipment_catalog, "build"))

    def test_all_zones_have_callable_build(self):
        """Every authored zone spec's build() must be callable."""
        from world.areas import (
            vaels_crossing, ashreach_plains, reth_foothills,
            cantera_edge, stormhaven_coast, varath_prime, crownroad_north, old_causeway,
            ironvein_escarpment, stagcrown_preserve, korahei, veluana_outer_reefs,
            kiai_grounds, veluana_central_isle, colonist_ruins, equipment_catalog,
        )
        for module in [
            vaels_crossing, ashreach_plains, reth_foothills,
            cantera_edge, stormhaven_coast, varath_prime, crownroad_north, old_causeway,
            ironvein_escarpment, stagcrown_preserve, korahei, veluana_outer_reefs,
            kiai_grounds, veluana_central_isle, colonist_ruins, equipment_catalog,
        ]:
            self.assertTrue(
                callable(getattr(module, "build", None)),
                f"{module.__name__} build() is not callable",
            )


# ---------------------------------------------------------------------------
# CmdStabilize tests (mock-based, no Evennia DB)
# ---------------------------------------------------------------------------

class TestCmdStabilize(unittest.TestCase):
    """Test CmdStabilize command logic."""

    def _make_cmd(self):
        """Import and instantiate CmdStabilize."""
        from world.node_commands import CmdStabilize
        cmd = CmdStabilize()
        cmd.caller = MagicMock()
        cmd.caller.location = MagicMock()
        cmd.caller.msg = MagicMock()
        cmd.caller.ndb = MagicMock()
        cmd.caller.ndb.stabilize_cooldown = None
        cmd.caller.ndb.stamina = 50  # Required for stabilization
        cmd.caller.db = MagicMock()
        cmd.caller.db.domain_scores = {}
        cmd.args = ""
        return cmd

    def test_stabilize_in_node_center_starts_stabilization(self):
        """CmdStabilize in a node_center room calls attempt_stabilization (tick-based)."""
        cmd = self._make_cmd()

        # Room is a node center
        cmd.caller.location.tags.has.return_value = True

        # Mock NodeScript on zone object
        mock_script = MagicMock()
        mock_script.db.failure = 50.0

        mock_zone_obj = MagicMock()
        mock_zone_obj.tags.has.return_value = True
        mock_zone_obj.scripts.get.return_value = [mock_script]

        with patch("world.node_commands.search_tag") as mock_search, \
             patch("world.node_helpers.attempt_stabilization") as mock_stab:
            mock_search.return_value = [mock_zone_obj]
            mock_stab.return_value = True
            cmd.caller.location.db.zone_id = "test_zone"
            cmd.func()

        # Command should invoke tick-based stabilization for the zone
        mock_stab.assert_called_once_with(cmd.caller, "test_zone")

    def test_stabilize_outside_node_room_shows_error(self):
        """CmdStabilize outside a node room should show error message."""
        cmd = self._make_cmd()

        # Room is NOT a node center
        cmd.caller.location.tags.has.return_value = False

        cmd.func()

        # Should have sent an error message
        cmd.caller.msg.assert_called()
        msg_text = cmd.caller.msg.call_args[0][0]
        self.assertIn("node", msg_text.lower())

    def test_stabilize_cooldown(self):
        """CmdStabilize should enforce cooldown between uses."""
        import time
        cmd = self._make_cmd()

        # Room is a node center
        cmd.caller.location.tags.has.return_value = True

        # Set cooldown in the recent past (within 5 min)
        cmd.caller.ndb.stabilize_cooldown = time.time() + 60

        cmd.func()

        # Should have sent a cooldown message
        cmd.caller.msg.assert_called()
        msg_text = cmd.caller.msg.call_args[0][0]
        self.assertTrue(
            "cooldown" in msg_text.lower() or "wait" in msg_text.lower()
            or "soon" in msg_text.lower() or "recently" in msg_text.lower(),
            f"Expected cooldown message, got: {msg_text}"
        )


# ---------------------------------------------------------------------------
# Mob template / loot table cross-reference tests
# ---------------------------------------------------------------------------

class TestContentCrossReferences(unittest.TestCase):
    """Verify mob templates and loot tables are consistent."""

    def test_mob_templates_module_imports(self):
        from world import mob_templates
        self.assertTrue(hasattr(mob_templates, "MOB_TEMPLATES"))

    def test_loot_tables_module_imports(self):
        from world import loot_tables
        self.assertTrue(hasattr(loot_tables, "LOOT_TABLES"))

    def test_captain_wrack_template_exists(self):
        from world.mob_templates import get_mob_template

        self.assertIsNotNone(get_mob_template("captain_wrack"))


# ---------------------------------------------------------------------------
# Spawn point tag tests
# ---------------------------------------------------------------------------

class TestSpawnPointTags(unittest.TestCase):
    """Verify spawn/respawn logic exists in the codebase."""

    def _make_room(self, room_id, is_respawn=False):
        room = MagicMock()
        room.id = hash(room_id)
        room.key = room_id
        room.db = SimpleNamespace(zone_id="zone")
        room.exits = []

        def has_tag(key, category=None):
            return key == "respawn_point" and category == "spawn_point" and is_respawn

        def get_tag(category=None):
            if category == "room_id":
                return room_id
            return None

        room.tags.has.side_effect = has_tag
        room.tags.get.side_effect = get_tag
        return room

    def test_greeter_room_tag_exists_in_zone_content(self):
        """Vael's Crossing should tag a room as greeter_room in spawn_point category."""
        tree = ast.parse(pathlib.Path("world/areas/vaels_crossing.py").read_text())

        found_tag = False
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Attribute) or node.func.attr != "add":
                continue
            if not node.args:
                continue
            if not isinstance(node.args[0], ast.Constant) or node.args[0].value != "greeter_room":
                continue
            for keyword in node.keywords:
                if (
                    keyword.arg == "category"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value == "spawn_point"
                ):
                    found_tag = True
                    break
            if found_tag:
                break

        self.assertTrue(found_tag, "Expected a greeter_room spawn_point tag in vaels_crossing.py")

    def test_respawn_falls_back_to_global_respawn_tag_search(self):
        """Respawn should use globally tagged respawn rooms when no local route exists."""
        from world.combat_engine import _respawn_player

        death_room = self._make_room("death_room")
        global_respawn = self._make_room("global_respawn", is_respawn=True)

        character = MagicMock()
        character.location = death_room
        character.home = None
        character.db.visited_room_ids = set()
        character.ndb.oob_debounce = {"map_update": 1.0}

        with patch("evennia.utils.search.search_tag", return_value=[global_respawn]), \
             patch("world.base_attributes.derive_max_hp", return_value=120), \
             patch("world.base_attributes.derive_max_stamina", return_value=80), \
             patch("world.oob_publisher.push_status_update"), \
             patch("world.oob_publisher.push_stat_update"), \
             patch("world.oob_publisher.push_map_update"), \
             patch("world.oob_publisher.push_inventory_update"):
            _respawn_player(character)

        character.move_to.assert_called_once_with(
            global_respawn, quiet=True, move_hooks=False
        )

    def test_cmdstabilize_registered_in_cmdset(self):
        """CmdStabilize should be registered in CharacterCmdSet."""
        from commands import default_cmdsets

        added_commands = []

        with patch.object(
            default_cmdsets.default_cmds.CharacterCmdSet,
            "at_cmdset_creation",
            return_value=None,
        ):
            cmdset = default_cmdsets.CharacterCmdSet()
            cmdset.add = added_commands.append
            cmdset.at_cmdset_creation()

        self.assertIn("stabilize", {cmd.key for cmd in added_commands})
