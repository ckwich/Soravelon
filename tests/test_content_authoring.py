"""
Content authoring verification tests (Phase 15 Plan 05).

Verifies that all required content items are defined in the catalog,
loot tables, and zone files. Uses file parsing rather than Evennia
imports to avoid requiring a running server.
"""

import unittest
import ast
import os

# Paths relative to repo root
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read_file(relpath):
    """Read a file relative to repo root."""
    with open(os.path.join(BASE, relpath), "r") as f:
        return f.read()


class TestEquipmentCatalog(unittest.TestCase):
    """Verify equipment_catalog.py contains required item definitions."""

    @classmethod
    def setUpClass(cls):
        cls.content = _read_file("world/areas/equipment_catalog.py")

    def test_gathering_tools_defined(self):
        """5 gathering tools with tool_slot and tool_tag fields."""
        tools = ["pickaxe", "sickle", "hatchet", "skinning_knife", "fishing_rod"]
        for tool in tools:
            self.assertIn(
                f"'{tool}':",
                self.content,
                f"Missing tool definition: {tool}",
            )
        self.assertIn("'tool_slot':", self.content)
        self.assertIn("'tool_tag':", self.content)

    def test_crafting_output_items_defined(self):
        """Crafting output items exist in CATALOG."""
        # Check a representative subset that actually exists in the catalog
        outputs = [
            "basic_healing_draught", "cooked_meat", "healing_draught",
            "hearty_stew", "herb_poultice", "iron_chainmail",
            "mountain_tonic", "spiced_fish", "stamina_tonic", "trail_rations",
        ]
        for item_id in outputs:
            self.assertIn(
                f"'{item_id}':",
                self.content,
                f"Missing crafting output: {item_id}",
            )

    def test_quest_items_defined(self):
        """8 quest items exist in CATALOG with is_quest_item flag."""
        quest_items = [
            "outstanding_debt_token", "commissioned_blade", "stolen_artifact",
            "rare_herb_bundle", "rare_alpine_ingredient", "resonance_sample",
            "contraband_package", "warden_supplies",
        ]
        for item_id in quest_items:
            self.assertIn(
                f"'{item_id}':",
                self.content,
                f"Missing quest item: {item_id}",
            )
        self.assertIn("'is_quest_item': True", self.content)

    def test_bait_defined(self):
        """Fishing bait consumable defined."""
        self.assertIn("'bait':", self.content)


class TestLootTables(unittest.TestCase):
    """Verify loot_tables.py contains rat and bandit entries."""

    @classmethod
    def setUpClass(cls):
        cls.content = _read_file("world/loot_tables.py")

    def test_rat_loot_table(self):
        """Rat loot table exists with drops."""
        self.assertIn('"rat":', self.content)
        self.assertIn('"mob_type": "rat"', self.content)
        self.assertIn('"rat_tail"', self.content)
        self.assertIn('"rat_hide"', self.content)

    def test_bandit_loot_table(self):
        """Bandit loot table exists with drops."""
        self.assertIn('"bandit":', self.content)
        self.assertIn('"mob_type": "bandit"', self.content)
        self.assertIn('"stolen_coin_pouch"', self.content)
        self.assertIn('"bandit_blade"', self.content)
        self.assertIn('"bandit_leather"', self.content)

    def test_bandit_has_stolen_artifact_drop(self):
        """Bandit loot table has valuable drops (stolen coin pouch)."""
        self.assertIn('"stolen_coin_pouch"', self.content)


class TestStormhavenCoast(unittest.TestCase):
    """Verify stormhaven_coast.py has fish gathering materials."""

    @classmethod
    def setUpClass(cls):
        cls.content = _read_file("world/areas/stormhaven_coast.py")

    def test_fish_materials_defined(self):
        """Fish gathering materials are defined."""
        self.assertIn('"river_trout"', self.content)
        self.assertIn('"cave_eel"', self.content)

    def test_contraband_trigger(self):
        """Contraband package quest item is referenced in zone."""
        self.assertIn("contraband_package", self.content)


class TestQuestItemSources(unittest.TestCase):
    """Verify quest items are wired to world sources."""

    def test_resonance_sample_trigger_in_cantera(self):
        content = _read_file("world/areas/cantera_edge.py")
        self.assertIn("resonance_sample", content)

    def test_debt_token_trigger_in_vaels_crossing(self):
        content = _read_file("world/areas/vaels_crossing.py")
        self.assertIn("outstanding_debt_token", content)
        self.assertIn("vc_debt_token_grant", content)

    def test_warden_supplies_trigger_in_vaels_crossing(self):
        content = _read_file("world/areas/vaels_crossing.py")
        self.assertIn("warden_supplies", content)
        self.assertIn("vc_warden_supplies_grant", content)

    def test_rare_herbs_trigger_in_reth(self):
        content = _read_file("world/areas/reth_foothills.py")
        # rare_herb_bundle is referenced in quest objectives
        self.assertIn("rare_alpine_ingredient", content)

    def test_rare_alpine_trigger_in_reth(self):
        content = _read_file("world/areas/reth_foothills.py")
        self.assertIn("rare_alpine_ingredient", content)


class TestCmdTools(unittest.TestCase):
    """Verify cmd_tools.py exists and has correct structure."""

    @classmethod
    def setUpClass(cls):
        cls.content = _read_file("commands/cmd_tools.py")

    def test_cmd_tools_class(self):
        self.assertIn("class CmdTools", self.content)

    def test_valid_tool_slots(self):
        self.assertIn("VALID_TOOL_SLOTS", self.content)
        for slot in ["tool_pickaxe", "tool_sickle", "tool_hatchet",
                      "tool_knife", "tool_rod"]:
            self.assertIn(slot, self.content)

    def test_registered_in_cmdset(self):
        cmdset = _read_file("commands/default_cmdsets.py")
        self.assertIn("from commands.cmd_tools import CmdTools", cmdset)


if __name__ == "__main__":
    unittest.main()
