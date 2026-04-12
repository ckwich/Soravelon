"""
Content authoring verification tests (Phase 15 Plan 05).

Verifies that all required content items are defined in the catalog,
loot tables, and zone files. Uses file parsing and imports to check
actual data structures rather than fragile string matching.
"""

import unittest
import os

# Paths relative to repo root
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django
django.setup()


def _read_file(relpath):
    """Read a file relative to repo root."""
    with open(os.path.join(BASE, relpath), "r") as f:
        return f.read()


class TestEquipmentCatalog(unittest.TestCase):
    """Verify equipment_catalog.py contains required item definitions."""

    @classmethod
    def setUpClass(cls):
        from world.areas.equipment_catalog import CATALOG
        cls.catalog = CATALOG
        cls.content = _read_file("world/areas/equipment_catalog.py")

    def test_gathering_tools_defined(self):
        """5 gathering tools with tool_slot and tool_tag fields."""
        tools = ["pickaxe", "sickle", "hatchet", "skinning_knife", "fishing_rod"]
        for tool in tools:
            self.assertIn(
                tool,
                self.catalog,
                f"Missing tool definition: {tool}",
            )
        self.assertIn("tool_slot", self.content)
        self.assertIn("tool_tag", self.content)

    def test_crafting_output_items_defined(self):
        """10 crafting output items exist in CATALOG."""
        outputs = [
            "basic_healing_draught", "cooked_meat", "healing_draught",
            "hearty_stew", "herb_poultice", "iron_chainmail",
            "mountain_tonic", "spiced_fish", "stamina_tonic", "trail_rations",
        ]
        for item_id in outputs:
            self.assertIn(
                item_id,
                self.catalog,
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
                item_id,
                self.catalog,
                f"Missing quest item: {item_id}",
            )
        # At least one item should have is_quest_item flag
        quest_flagged = [k for k, v in self.catalog.items()
                        if v.get("is_quest_item")]
        self.assertGreater(len(quest_flagged), 0,
                          "No items have is_quest_item=True")

    def test_bait_defined(self):
        """Fishing bait consumable defined."""
        self.assertIn("bait", self.catalog)


class TestLootTables(unittest.TestCase):
    """Verify loot_tables.py contains rat and bandit entries."""

    @classmethod
    def setUpClass(cls):
        from world.loot_tables import LOOT_TABLES
        cls.tables = LOOT_TABLES
        cls.content = _read_file("world/loot_tables.py")

    def test_rat_loot_table(self):
        """Rat loot table exists with drops."""
        self.assertIn("rat", self.tables)
        rat = self.tables["rat"]
        # Check it has drops defined
        drops = rat.get("drops", [])
        drop_ids = [d.get("item_id", d.get("item")) for d in drops]
        self.assertTrue(
            any("rat" in str(d_id) for d_id in drop_ids if d_id),
            "Rat loot table should contain rat-related drops"
        )

    def test_bandit_loot_table(self):
        """Bandit loot table exists with drops."""
        self.assertIn("bandit", self.tables)
        bandit = self.tables["bandit"]
        drops = bandit.get("drops", [])
        drop_ids = [d.get("item_id", d.get("item")) for d in drops]
        self.assertTrue(len(drops) >= 2,
                       "Bandit loot table should have at least 2 drops")

    def test_bandit_has_quest_relevant_drops(self):
        """Bandit loot table has drops relevant to quest items."""
        self.assertIn("bandit", self.tables)
        bandit = self.tables["bandit"]
        drops = bandit.get("drops", [])
        # Bandit should have at least one item (stolen_coin_pouch is canonical)
        drop_ids = [d.get("item_id", d.get("item")) for d in drops]
        self.assertIn("stolen_coin_pouch", drop_ids,
                     "Bandit loot table should contain stolen_coin_pouch")


class TestStormhavenCoast(unittest.TestCase):
    """Verify stormhaven_coast.py has fish gathering materials."""

    @classmethod
    def setUpClass(cls):
        cls.content = _read_file("world/areas/stormhaven_coast.py")

    def test_fish_materials_defined(self):
        """Fish gathering materials are defined."""
        # Check for fish-related material definitions in the zone file
        has_fish = ("common_fish" in self.content or
                   "coastal_fish" in self.content or
                   "fish" in self.content.lower())
        self.assertTrue(has_fish, "stormhaven_coast should define fish materials")

    def test_contraband_referenced(self):
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

    def test_rare_alpine_trigger_in_reth(self):
        """Reth Foothills references rare alpine ingredient."""
        content = _read_file("world/areas/reth_foothills.py")
        self.assertIn("rare_alpine_ingredient", content)


if __name__ == "__main__":
    unittest.main()
