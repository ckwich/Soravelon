"""Canonical faction relationship IDs across writers and consumers."""

from evennia.utils.test_resources import EvenniaTest

from world.faction_registry import FactionIdentityError
from world.models import FactionStanding


class TestCanonicalFactionRuntime(EvenniaTest):
    def test_alias_write_and_all_relationship_reads_use_canonical_row(self):
        from world.world_state import (
            get_betrayal,
            get_standing,
            get_trust,
            modify_standing,
        )

        modify_standing(self.char1, "warden", 250, "alias test")
        row = FactionStanding.objects.get(character=self.char1)
        row.trust = 78
        row.betrayal_flag = True
        row.save(update_fields=["trust", "betrayal_flag"])

        self.assertEqual(row.faction_id, "wardens")
        self.assertEqual(get_standing(self.char1, "warden"), 250)
        self.assertEqual(get_standing(self.char1, "wardens"), 250)
        self.assertEqual(get_trust(self.char1, "warden"), 78)
        self.assertTrue(get_betrayal(self.char1, "warden"))
        self.assertFalse(
            FactionStanding.objects.filter(
                character=self.char1,
                faction_id="warden",
            ).exists()
        )

    def test_unknown_relationship_writer_fails_closed(self):
        from world.world_state import modify_standing

        with self.assertRaises(FactionIdentityError):
            modify_standing(self.char1, "typo_wardenz", 250, "invalid test")

        self.assertFalse(FactionStanding.objects.filter(character=self.char1).exists())

    def test_ancestry_disposition_accepts_declared_alias_only_at_boundary(self):
        from world.mob_disposition import get_ancestry_modifier

        self.assertEqual(
            get_ancestry_modifier("kauroran", "warden"),
            get_ancestry_modifier("kauroran", "wardens"),
        )
        self.assertEqual(get_ancestry_modifier("kauroran", "warden"), 0.15)
