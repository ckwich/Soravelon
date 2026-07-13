"""Behavior tests for the compiled playable-connectivity audit."""

from pathlib import Path
from unittest import TestCase

from world.connectivity_audit import audit_world_connectivity
from world.content_compiler import compile_world_manifest


class TestProductionWorldConnectivity(TestCase):
    def test_reports_flight_clusters_blocked_by_destination_discovery(self):
        compilation = compile_world_manifest(Path("world/areas"))
        self.assertIsNotNone(compilation.manifest)

        audit = audit_world_connectivity(compilation.manifest)

        self.assertEqual(
            audit.unreachable_zones,
            {
                "colonist_ruins",
                "crownroad_north",
                "greyteeth_lower_passes",
                "ironvein_escarpment",
                "kiai_grounds",
                "korahei",
                "old_causeway",
                "stagcrown_preserve",
                "tremen",
                "tremeneth_deep_mines",
                "tremeneth_high_passes",
                "tremeneth_underhalls",
                "varath_prime",
                "veluana_central_isle",
                "veluana_outer_reefs",
            },
        )
        self.assertIn(
            (
                "circular-flight-discovery",
                "vaels_crossing_courier:varath_prime_courier",
            ),
            {(item.code, item.entity_id) for item in audit.diagnostics},
        )

    def test_rejects_a_flight_route_with_an_unknown_endpoint(self):
        from world.content_compiler import WorldManifest, compile_area_source

        compilation = compile_area_source(
            """
from world.area_builder import AreaBuilder
area = AreaBuilder("test_zone")
area.zone(name="Test", tier=1, zone_type="plains", continent="varath", faction_territory="neutral")
start = area.room("start", name="Start")
area.flight_point(start, "known", name="Known")
area.flight_route("known", "missing", 10)
area.build()
""",
            source_path="test_zone.py",
        )
        self.assertIsNotNone(compilation.definition)
        manifest = WorldManifest(
            schema_version="test",
            zones=(compilation.definition,),
            manifest_hash="test",
        )

        audit = audit_world_connectivity(
            manifest,
            start_room="test_zone:start",
        )

        self.assertIn("unknown-flight-point", {item.code for item in audit.diagnostics})
