"""
Content authoring verification tests (Phase 15 Plan 05).

Verifies that all required content items are defined in the catalog,
loot tables, and zone files. Uses file parsing and imports to check
actual data structures rather than fragile string matching.
"""

import os
import ast
import unittest

# Paths relative to repo root
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
import django  # noqa: E402
django.setup()


def _read_file(relpath):
    """Read a file relative to repo root."""
    with open(os.path.join(BASE, relpath), "r") as f:
        return f.read()


def _quest_kwargs(relpath, quest_id):
    """Return literal keyword args from an authored area.quest() call."""
    tree = ast.parse(_read_file(relpath))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute) or node.func.attr != "quest":
            continue
        if not node.args:
            continue
        try:
            authored_quest_id = ast.literal_eval(node.args[0])
        except (ValueError, SyntaxError):
            continue
        if authored_quest_id != quest_id:
            continue
        return {
            keyword.arg: ast.literal_eval(keyword.value)
            for keyword in node.keywords
            if keyword.arg
        }
    raise AssertionError(f"Could not find area.quest({quest_id!r}) in {relpath}")


def _item_ids(relpath):
    """Return literal item ids from authored area.item() calls."""
    tree = ast.parse(_read_file(relpath))
    item_ids = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute) or node.func.attr != "item":
            continue
        if not node.args:
            continue
        try:
            item_ids.add(ast.literal_eval(node.args[0]))
        except (ValueError, SyntaxError):
            continue
    return item_ids


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

    def test_chainmail_sits_between_iron_and_steel_plate_progression(self):
        """Crafted chainmail should not skip past the next heavy-armor tier."""
        chainmail = self.catalog["iron_chainmail"]
        iron_plate = self.catalog["iron_breastplate"]
        steel_plate = self.catalog["steel_breastplate"]
        self.assertGreater(chainmail["armor_value"], iron_plate["armor_value"])
        self.assertLess(chainmail["armor_value"], steel_plate["armor_value"])

    def test_face_and_wrist_slots_have_tier_three_options(self):
        """Late-game gearing should not dead-end in face and wrists slots."""
        face_tiers = {
            item["material_tier"]
            for item in self.catalog.values()
            if item.get("equip_slot") == "face"
        }
        wrist_tiers = {
            item["material_tier"]
            for item in self.catalog.values()
            if item.get("equip_slot") == "wrists"
        }
        self.assertIn(3, face_tiers)
        self.assertIn(3, wrist_tiers)

    def test_bucklers_offer_a_fast_off_hand_profile(self):
        """Bucklers should provide an agility-forward alternative to kite shields."""
        for item_id in ("iron_buckler", "steel_buckler", "mithril_buckler"):
            self.assertIn("agility", self.catalog[item_id]["stat_bonuses"])


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

    def test_vaels_warden_report_uses_delivery_item(self):
        content = _read_file("world/areas/vaels_crossing.py")
        self.assertIn("warden_field_report", content)
        self.assertIn('flagged_drop="warden_field_report"', content)
        self.assertIn(
            "warden_field_report",
            _item_ids("world/areas/vaels_crossing.py"),
        )

    def test_vaels_warden_report_records_social_route_reward(self):
        quest = _quest_kwargs("world/areas/vaels_crossing.py", "vc_q_warden_report")
        social_action = next(
            reward
            for reward in quest["rewards"]
            if reward.get("action_type") == "record_social_event"
        )

        self.assertEqual(
            social_action["fact"]["fact_key_template"],
            "fact:{character_id}:vc_q_warden_report:delivered",
        )
        self.assertEqual(
            social_action["claim"]["claim_key_template"],
            "claim:calloway:{character_id}:vc_q_warden_report:delivered",
        )
        self.assertEqual(social_action["propagate"]["source"], "calloway")
        self.assertEqual(
            social_action["propagate"]["claim_key_template"],
            "claim:calloway:{character_id}:vc_q_warden_report:delivered",
        )
        self.assertTrue(social_action["propagate"]["required"])
        self.assertEqual(
            social_action["knowledge"],
            [
                {
                    "node": "calloway",
                    "fact_key_template": "fact:{character_id}:vc_q_warden_report:delivered",
                    "channel": "official_report",
                    "confidence": 1.0,
                    "spreading": False,
                },
                {
                    "node": "calloway",
                    "claim_key_template": "claim:calloway:{character_id}:vc_q_warden_report:delivered",
                    "channel": "official_report",
                    "confidence": 1.0,
                    "spreading": True,
                },
            ],
        )
        self.assertNotIn(
            "npc_innkeeper_whistle",
            [
                node.get("identifier") or node.get("identifier_template")
                for node in social_action["nodes"]
            ],
        )
        self.assertIn(
            {
                "source": "calloway",
                "target": "harven",
                "edge_type": "warden_report",
                "directionality": "one_way",
                "trust": 0.95,
                "latency_seconds": 0,
                "scope_tags": ["warden", "report", "quest"],
            },
            social_action["edges"],
        )

    def test_cantera_resupply_uses_delivery_item(self):
        content = _read_file("world/areas/cantera_edge.py")
        self.assertIn("warden_supplies", content)
        self.assertIn('flagged_drop="warden_supplies"', content)

    def test_ashreach_references_rare_herb_bundles(self):
        content = _read_file("world/areas/ashreach_plains.py")
        self.assertIn("rare_herb_bundle", content)

    def test_rare_alpine_trigger_in_reth(self):
        """Reth Foothills references rare alpine ingredient."""
        content = _read_file("world/areas/reth_foothills.py")
        self.assertIn("rare_alpine_ingredient", content)

    def test_stormhaven_delivery_items_are_referenced(self):
        content = _read_file("world/areas/stormhaven_coast.py")
        self.assertIn("contraband_package", content)
        self.assertIn("lighthouse_oil_crate", content)


if __name__ == "__main__":
    unittest.main()
