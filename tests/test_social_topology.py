"""Builder-owned Social Web topology must materialize and reconcile safely."""

from evennia.utils.test_resources import EvenniaTest


class TestAuthoredSocialTopology(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.social_topology import clear_registered_social_topology

        clear_registered_social_topology()

    def _builder(self, zone_id):
        from world.area_builder import AreaBuilder

        builder = AreaBuilder(zone_id)
        builder.zone(
            name=f"{zone_id.title()} Zone",
            tier=1,
            zone_type="frontier",
            continent="varath",
        )
        return builder

    def test_literal_social_nodes_and_edges_materialize_with_builder_ownership(self):
        from world.models import SocialEdge, SocialNode, SocialTopologyBinding

        builder = self._builder("social_topology_home")
        builder.social_node(
            "npc",
            "topology_source",
            display_name="Topology Source",
            settlement_id="topology_home",
        )
        builder.social_node(
            "npc",
            "topology_target",
            display_name="Topology Target",
            settlement_id="topology_home",
        )
        builder.social_edge(
            "npc:topology_source",
            "npc:topology_target",
            edge_type="official_report",
            directionality="one_way",
            trust=0.9,
            scope_tags=["topology"],
        )
        builder.build()

        self.assertTrue(
            SocialNode.objects.filter(node_key="npc:topology_source").exists()
        )
        edge = SocialEdge.objects.get(
            edge_key=(
                "edge:npc:topology_source:npc:topology_target:official_report"
            )
        )
        self.assertEqual(edge.scope_tags, ["topology"])
        self.assertTrue(
            SocialTopologyBinding.objects.filter(
                zone_id="social_topology_home",
                kind="edge",
                object_key=edge.edge_key,
            ).exists()
        )

    def test_cross_zone_edges_resolve_after_all_zone_nodes_are_registered(self):
        from world.models import SocialEdge
        from world.social_topology import materialize_registered_social_topology

        source_builder = self._builder("social_topology_source")
        source_builder.social_node("npc", "cross_source")
        source_builder.social_edge(
            "npc:cross_source",
            "npc:cross_target",
            edge_type="guild_courier",
            directionality="one_way",
            scope_tags=["courier"],
        )
        source_builder.build()
        self.assertFalse(
            SocialEdge.objects.filter(
                edge_key=(
                    "edge:npc:cross_source:npc:cross_target:guild_courier"
                )
            ).exists()
        )

        target_builder = self._builder("social_topology_target")
        target_builder.social_node("npc", "cross_target")
        target_builder.build()
        report = materialize_registered_social_topology(finalize=True)

        self.assertEqual(report["unresolved_edges"], [])
        self.assertTrue(
            SocialEdge.objects.filter(
                edge_key=(
                    "edge:npc:cross_source:npc:cross_target:guild_courier"
                )
            ).exists()
        )

    def test_final_reconciliation_removes_stale_builder_owned_edges(self):
        from world.models import SocialEdge
        from world.social_topology import materialize_registered_social_topology

        builder = self._builder("social_topology_reconcile")
        builder.social_node("npc", "reconcile_source")
        builder.social_node("npc", "reconcile_target")
        builder.social_edge(
            "npc:reconcile_source",
            "npc:reconcile_target",
            edge_type="official_report",
            scope_tags=["reconcile"],
        )
        builder.build()
        materialize_registered_social_topology(finalize=True)
        edge_key = "edge:npc:reconcile_source:npc:reconcile_target:official_report"
        self.assertTrue(SocialEdge.objects.filter(edge_key=edge_key).exists())

        replacement = self._builder("social_topology_reconcile")
        replacement.social_node("npc", "reconcile_source")
        replacement.social_node("npc", "reconcile_target")
        replacement.build()
        materialize_registered_social_topology(finalize=True)

        self.assertFalse(SocialEdge.objects.filter(edge_key=edge_key).exists())

    def test_literal_topology_rejects_unknown_taxonomy_before_build(self):
        from world.area_builder import AreaBuilderValidationError

        builder = self._builder("social_topology_invalid")
        with self.assertRaisesRegex(
            AreaBuilderValidationError,
            "unsupported social node_type",
        ):
            builder.social_node("unknown", "bad_node")
        with self.assertRaisesRegex(
            AreaBuilderValidationError,
            "unsupported social edge_type",
        ):
            builder.social_edge(
                "npc:source",
                "npc:target",
                edge_type="telepathy",
            )
