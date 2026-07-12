"""Contracts for indexed exact internal tag lookups."""

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest

from typeclasses.objects import SoravelonObject
from world.tag_search import search_objects_by_exact_tag


class TestExactTagSearch(EvenniaTest):
    def test_matches_normalized_key_and_category_without_cross_category_leak(self):
        expected = create_object(SoravelonObject, key="Expected")
        expected.tags.add("room_alpha", category="room_id")
        wrong_category = create_object(SoravelonObject, key="Wrong Category")
        wrong_category.tags.add("room_alpha", category="zone_id")

        matches = list(search_objects_by_exact_tag("ROOM_ALPHA", "ROOM_ID"))

        self.assertEqual([obj.id for obj in matches], [expected.id])
