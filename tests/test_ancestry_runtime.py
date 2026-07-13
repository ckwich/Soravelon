"""Behavior tests for canonical ancestry traits in live calculations."""

from evennia.utils.test_resources import EvenniaTest


class TestAncestryMaximumHealth(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.char1.db.base_stats = {
            "strength": 10,
            "endurance": 10,
            "agility": 10,
            "acuity": 10,
            "resonance": 10,
            "presence": 10,
            "willpower": 10,
        }
        self.char1.db.backend_level = 1

    def test_kauroran_hp_bonus_uses_authored_multiplier(self):
        from world.base_attributes import derive_max_hp

        self.char1.db.ancestry = None
        baseline = derive_max_hp(self.char1)
        self.char1.db.ancestry = "kauroran"

        self.assertEqual(derive_max_hp(self.char1), round(baseline * 1.30))

    def test_derived_hp_is_idempotent_across_repeated_reads(self):
        from world.base_attributes import derive_max_hp

        self.char1.db.ancestry = "kauroran"

        self.assertEqual(derive_max_hp(self.char1), derive_max_hp(self.char1))
