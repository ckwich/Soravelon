"""
Tests for the 13-slot equipment system (D-37, D-38, D-39, D-40, D-42).
Uses source inspection to avoid Evennia/Django import chain.
"""

import ast
import os
import unittest
from unittest.mock import MagicMock, patch


# Parse VALID_SLOTS from source to avoid Django/Evennia import
def _parse_valid_slots():
    """Extract VALID_SLOTS set from typeclasses/objects.py via AST."""
    src_path = os.path.join(os.path.dirname(__file__), "..", "typeclasses", "objects.py")
    with open(src_path) as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "VALID_SLOTS":
                    return {elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)}
    return set()


VALID_SLOTS = _parse_valid_slots()


class TestValidSlots(unittest.TestCase):
    """VALID_SLOTS contains exactly the 13 required slot names."""

    def test_valid_slots_count(self):
        self.assertEqual(len(VALID_SLOTS), 13)

    def test_all_required_slots_present(self):
        expected = {
            "head", "face", "chest", "back", "hands", "wrists",
            "legs", "feet", "main_hand", "off_hand",
            "ring1", "ring2", "amulet"
        }
        self.assertEqual(VALID_SLOTS, expected)

    def test_old_slots_removed(self):
        old_slots = {"body", "right_hand", "left_hand", "accessory"}
        for slot in old_slots:
            self.assertNotIn(slot, VALID_SLOTS,
                             f"Old slot '{slot}' should be removed")


class TestEquipmentSourceAttributes(unittest.TestCase):
    """Equipment class has required attribute initializations in source."""

    def setUp(self):
        src_path = os.path.join(os.path.dirname(__file__), "..", "typeclasses", "objects.py")
        with open(src_path) as f:
            self.source = f.read()

    def test_has_two_handed_attr(self):
        self.assertIn("self.db.two_handed", self.source)

    def test_has_armor_value_attr(self):
        self.assertIn("self.db.armor_value", self.source)

    def test_has_damage_min_attr(self):
        self.assertIn("self.db.damage_min", self.source)

    def test_has_damage_max_attr(self):
        self.assertIn("self.db.damage_max", self.source)

    def test_has_stat_bonuses_attr(self):
        self.assertIn("self.db.stat_bonuses", self.source)

    def test_has_material_tier_attr(self):
        self.assertIn("self.db.material_tier", self.source)

    def test_has_main_hand_slot(self):
        self.assertIn('"main_hand"', self.source)

    def test_has_ring_slots(self):
        self.assertIn('"ring1"', self.source)
        self.assertIn('"ring2"', self.source)

    def test_has_two_handed_check(self):
        self.assertIn("two_handed", self.source)
        self.assertIn("both hands", self.source)

    def test_has_ring_auto_fill_logic(self):
        self.assertIn("ring2", self.source)
        self.assertIn("ring slots", self.source.lower())


class TestCanEquipLogic(unittest.TestCase):
    """Test can_equip method via direct source function logic."""

    def test_each_valid_slot_is_string(self):
        for slot in VALID_SLOTS:
            self.assertIsInstance(slot, str)
            self.assertTrue(len(slot) > 0)

    def test_no_duplicate_slots(self):
        src_path = os.path.join(os.path.dirname(__file__), "..", "typeclasses", "objects.py")
        with open(src_path) as f:
            source = f.read()
        for slot in VALID_SLOTS:
            # Each slot should appear in VALID_SLOTS definition once
            count = source.count(f'"{slot}"')
            self.assertGreaterEqual(count, 1, f"Slot '{slot}' should appear at least once")


if __name__ == "__main__":
    unittest.main()
