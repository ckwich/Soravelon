"""Runtime paths for one-time exploration and investigation progression."""

from unittest.mock import MagicMock, patch

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest

from world.models import ProgressionEvent


class TestLandmarkExplorationProgression(EvenniaTest):
    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom
        from world.flight_registry import FlightRegistry

        FlightRegistry.clear()
        self.landmark = create_object(
            SoravelonRoom,
            key="Vael Courier Platform",
        )
        self.landmark.tags.add("vc_courier_platform", category="room_id")
        self.landmark.db.zone_id = "vaels_crossing"
        self.landmark.db.flight_point_id = "vaels_crossing"
        FlightRegistry.register_point(
            "vaels_crossing",
            self.landmark,
            name="Vael's Crossing",
        )
        self.char1.db.discovered_flight_points = set()
        self.char1.db.visited_room_ids = set()

    def tearDown(self):
        from world.flight_registry import FlightRegistry

        FlightRegistry.clear()
        super().tearDown()

    @patch("world.quest_engine.check_deliver_objectives")
    @patch("world.quest_engine.check_investigate_objectives")
    @patch("world.trigger_engine.fire_triggers")
    def test_entering_a_new_courier_landmark_records_one_exploration_event(
        self,
        _fire_triggers,
        _check_investigate,
        _check_deliver,
    ):
        self.landmark.at_object_receive(self.char1, self.room1)
        self.landmark.at_object_receive(self.char1, self.room1)

        event = ProgressionEvent.objects.get(
            character=self.char1,
            event_type="exploration",
        )
        self.assertEqual(event.source_id, "vaels_crossing")
        self.assertEqual(event.domain_awards, {"tactics": 20})
        self.assertEqual(event.skill_awards, {"navigation": 2})
        self.assertEqual(
            ProgressionEvent.objects.filter(character=self.char1).count(),
            1,
        )


class TestInvestigationDiscoveryProgression(EvenniaTest):
    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom

        self.archive = create_object(SoravelonRoom, key="Old Archive")
        self.archive.tags.add("old_archive", category="room_id")
        self.archive.db.lore_fragments = [
            {
                "fragment_id": "old_archive_registry_mark",
                "discovery_method": "search",
                "text": "A registry mark has been scraped from the stone.",
            }
        ]
        self.char1.location = self.archive
        self.char1.db.collected_lore_ids = []
        self.char1.db.discovered_exits = []
        self.char1.msg = MagicMock()

    def test_only_a_novel_successful_search_records_investigation_progression(self):
        from commands.cmd_search import CmdSearch

        command = CmdSearch()
        command.caller = self.char1
        command.args = ""
        with patch(
            "world.skill_engine.get_skill_value",
            return_value=100,
        ), patch("commands.cmd_search.random.randint", return_value=20):
            command.func()
            command.func()

        event = ProgressionEvent.objects.get(
            character=self.char1,
            event_type="investigation",
        )
        self.assertEqual(event.source_id, "old_archive")
        self.assertEqual(event.domain_awards, {})
        self.assertEqual(event.skill_awards, {"investigation": 1})
        self.assertEqual(
            ProgressionEvent.objects.filter(character=self.char1).count(),
            1,
        )
        self.assertEqual(
            self.char1.db.collected_lore_ids,
            ["old_archive_registry_mark"],
        )
