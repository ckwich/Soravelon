"""
Integration tests for Phase 7 content:
- CmdStabilize node interaction command
- Zone spec file imports
- Zone build() function callability
- Spawn/respawn tag wiring
"""

import os
import unittest
from unittest.mock import MagicMock, patch

# Django setup required for Evennia command imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django  # noqa: E402
django.setup()


# ---------------------------------------------------------------------------
# Zone file import tests (pure Python, no Evennia DB needed)
# ---------------------------------------------------------------------------

class TestZoneImports(unittest.TestCase):
    """Verify all 5 zone spec files and equipment catalog import cleanly."""

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

    def test_equipment_catalog_imports(self):
        from world.areas import equipment_catalog
        self.assertTrue(hasattr(equipment_catalog, "build"))

    def test_all_zones_have_callable_build(self):
        """Every zone spec's build() must be callable."""
        from world.areas import (
            vaels_crossing, ashreach_plains, reth_foothills,
            cantera_edge, stormhaven_coast, equipment_catalog,
        )
        for module in [
            vaels_crossing, ashreach_plains, reth_foothills,
            cantera_edge, stormhaven_coast, equipment_catalog,
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


# ---------------------------------------------------------------------------
# Spawn point tag tests
# ---------------------------------------------------------------------------

class TestSpawnPointTags(unittest.TestCase):
    """Verify spawn/respawn logic exists in the codebase."""

    def test_greeter_room_tag_exists_in_zone_content(self):
        """Vael's Crossing zone file should tag the arrival room as greeter_room."""
        import inspect
        from world.areas import vaels_crossing
        source = inspect.getsource(vaels_crossing)
        self.assertIn("greeter_room", source)

    def test_death_handler_references_respawn_point(self):
        """handle_player_death or _respawn_player should use respawn_point tag."""
        import inspect
        from world.combat_engine import _respawn_player
        source = inspect.getsource(_respawn_player)
        self.assertIn("respawn_point", source)

    def test_cmdstabilize_registered_in_cmdset(self):
        """CmdStabilize should be registered in CharacterCmdSet."""
        import pathlib
        source = pathlib.Path("commands/default_cmdsets.py").read_text()
        self.assertIn("CmdStabilize", source)
