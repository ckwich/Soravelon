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


class TestAncestryEffectiveStats(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.char1.db.base_stats = {
            "strength": 20,
            "agility": 20,
            "endurance": 20,
            "mana": 20,
            "acuity": 20,
            "presence": 20,
            "resonance": 20,
        }

    def test_authored_ancestry_stat_traits_use_the_live_effective_stat_path(self):
        from world.equipment_effects import get_effective_stats

        expectations = {
            ("human", None): {
                "strength": 21,
                "agility": 21,
                "endurance": 21,
                "mana": 21,
                "acuity": 21,
                "presence": 21,
                "resonance": 21,
            },
            ("kauroran", None): {"strength": 24},
            ("veth", None): {"agility": 25},
            ("selvar", "summer"): {"agility": 22},
            ("selvar", "winter"): {"endurance": 22},
        }

        for (ancestry, coat), expected in expectations.items():
            with self.subTest(ancestry=ancestry, coat=coat):
                self.char1.db.ancestry = ancestry
                self.char1.db.selvar_coat = coat

                effective = get_effective_stats(self.char1)

                for stat_name, value in expected.items():
                    self.assertEqual(effective[stat_name], value)

    def test_effective_stat_traits_do_not_mutate_or_compound_intrinsic_stats(self):
        from world.equipment_effects import get_effective_stats

        self.char1.db.ancestry = "veth"
        intrinsic = dict(self.char1.db.base_stats)

        first = get_effective_stats(self.char1)
        second = get_effective_stats(self.char1)

        self.assertEqual(first, second)
        self.assertEqual(first["agility"], 25)
        self.assertEqual(dict(self.char1.db.base_stats), intrinsic)
