"""Pure compiler contracts for literal AreaBuilder source."""

from pathlib import Path
import unittest


class TestAreaSourceAuthority(unittest.TestCase):
    def test_compiled_values_have_one_public_mutable_conversion(self):
        from world.content_compiler import (
            AreaOperation,
            FrozenMap,
            compiled_operation_value,
            thaw_compiled_value,
        )

        frozen = FrozenMap(
            (
                ("nested", FrozenMap((("items", ("first", "second")),))),
                ("enabled", True),
            )
        )

        self.assertEqual(
            thaw_compiled_value(frozen),
            {
                "nested": {"items": ["first", "second"]},
                "enabled": True,
            },
        )

        operation = AreaOperation(
            source_path="test.py",
            line=1,
            column=0,
            method="room",
            arguments=("positional",),
            keyword_arguments=FrozenMap((("value", "keyword"),)),
        )
        self.assertEqual(
            compiled_operation_value(operation, 0, "value"),
            "positional",
        )
        self.assertEqual(
            compiled_operation_value(operation, 1, "value"),
            "keyword",
        )

    def test_literal_operations_compile_with_immutable_source_locations(self):
        from world.content_compiler import (
            FrozenMap,
            SymbolicReference,
            compile_area_source,
        )

        source = """from world.area_builder import AreaBuilder

def build():
    area = AreaBuilder("test_zone")
    area.zone(name="Test Zone", zone_type="frontier", continent="varath")
    room = area.room("entry", name="Entry", desc="A threshold.")
    area.exit(room, "other_zone:gate", "out", hidden=True)
    return area.build()
"""

        result = compile_area_source(source, source_path="world/areas/test_zone.py")

        self.assertEqual(result.diagnostics, ())
        self.assertIsNotNone(result.definition)
        assert result.definition is not None
        self.assertEqual(result.definition.zone_id, "test_zone")
        self.assertEqual(
            [operation.method for operation in result.definition.operations],
            ["zone", "room", "exit", "build"],
        )
        self.assertEqual(result.definition.operations[0].line, 5)
        room_operation = result.definition.operations[1]
        self.assertEqual(room_operation.arguments, ("entry",))
        self.assertEqual(
            room_operation.keyword_arguments,
            FrozenMap((("desc", "A threshold."), ("name", "Entry"))),
        )
        exit_operation = result.definition.operations[2]
        self.assertEqual(
            exit_operation.arguments,
            (
                SymbolicReference("room", "entry"),
                "other_zone:gate",
                "out",
            ),
        )
        self.assertEqual(
            exit_operation.keyword_arguments, FrozenMap((("hidden", True),))
        )
        self.assertEqual(
            result.definition.operations[0].source_path,
            "world/areas/test_zone.py",
        )
        with self.assertRaises(AttributeError):
            result.definition.operations.append("mutation")

    def test_forbidden_runtime_mutation_blocks_definition(self):
        from world.content_compiler import compile_area_source

        source = """from world.area_builder import AreaBuilder

def build():
    area = AreaBuilder("unsafe")
    room = area.room("entry", "Entry", "A threshold.")
    room.db.initial_room_flags = {"mist": True}
    room.tags.add("greeter_room", category="spawn_point")
    return area.build()
"""

        result = compile_area_source(source, source_path="world/areas/unsafe.py")

        self.assertIsNone(result.definition)
        self.assertEqual(
            [(item.code, item.line) for item in result.diagnostics],
            [
                ("forbidden-runtime-mutation", 6),
                ("forbidden-runtime-mutation", 7),
            ],
        )
        self.assertTrue(
            all(
                item.source_path == "world/areas/unsafe.py"
                for item in result.diagnostics
            )
        )

    def test_unknown_builder_call_blocks_definition_at_exact_source(self):
        from world.content_compiler import compile_area_source

        source = """from world.area_builder import AreaBuilder

def build():
    area = AreaBuilder("unknown")
    area.zone("test_zone", "Test Zone", zone_type="frontier")
    area.teleport_everyone("entry")
    return area.build()
"""

        result = compile_area_source(source, source_path="world/areas/unknown.py")

        self.assertIsNone(result.definition)
        self.assertEqual(len(result.diagnostics), 1)
        diagnostic = result.diagnostics[0]
        self.assertEqual(diagnostic.code, "unsupported-area-operation")
        self.assertEqual(diagnostic.line, 6)
        self.assertIn("teleport_everyone", diagnostic.message)

    def test_dynamic_argument_blocks_definition_at_the_call_site(self):
        from world.content_compiler import compile_area_source

        source = """from world.area_builder import AreaBuilder

CATALOG = {"iron_sword": {"name": "Iron Sword"}}

def build():
    area = AreaBuilder("dynamic")
    area.zone(name="Dynamic", zone_type="frontier", continent="varath")
    for item_id, item_def in CATALOG.items():
        area.item(item_id, **item_def)
    return area.build()
"""

        result = compile_area_source(source, source_path="world/areas/dynamic.py")

        self.assertIsNone(result.definition)
        self.assertEqual(len(result.diagnostics), 1)
        self.assertEqual(result.diagnostics[0].code, "nonliteral-area-argument")
        self.assertEqual(result.diagnostics[0].line, 9)

    def test_legacy_dialogue_key_blocks_world_compilation(self):
        from world.content_compiler import compile_world_sources

        source = '''from world.area_builder import AreaBuilder

def build():
    area = AreaBuilder("dialogue_zone")
    area.zone(name="Dialogue Zone", zone_type="frontier", continent="varath")
    room = area.room("entry", name="Entry", desc="A threshold.")
    area.npc(
        room,
        "npc_keeper",
        dialogue={"greeting": "The keeper waves."},
    )
    return area.build()
'''

        result = compile_world_sources({"world/areas/dialogue_zone.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(len(result.diagnostics), 1)
        diagnostic = result.diagnostics[0]
        self.assertEqual(diagnostic.code, "invalid-dialogue-payload")
        self.assertEqual(diagnostic.line, 7)
        self.assertIn("legacy dialogue keys", diagnostic.message)

    def test_missing_literal_zone_id_fails_closed(self):
        from world.content_compiler import compile_area_source

        source = """from world.area_builder import AreaBuilder

def build():
    area = AreaBuilder()
    area.zone(name="Missing ID", zone_type="frontier", continent="varath")
    return area.build()
"""

        result = compile_area_source(source, source_path="world/areas/missing_id.py")

        self.assertIsNone(result.definition)
        self.assertEqual(result.diagnostics[0].code, "missing-zone-id")
        self.assertEqual(result.diagnostics[0].line, 4)


class TestLiveAreaAuthorityAudit(unittest.TestCase):
    def test_every_live_area_compiles_without_runtime_mutation_escape_hatches(self):
        from world.content_compiler import audit_area_sources

        areas_dir = Path(__file__).resolve().parents[1] / "world" / "areas"
        audit = audit_area_sources(areas_dir)
        expected_sources = {
            path.relative_to(areas_dir.parents[1]).as_posix()
            for path in areas_dir.glob("*.py")
            if not path.name.startswith("_")
        }

        self.assertEqual(audit.diagnostics, ())
        self.assertEqual(
            {definition.source_path for definition in audit.definitions},
            expected_sources,
        )


class TestWorldManifest(unittest.TestCase):
    def test_unresolved_local_and_cross_zone_exit_references_fail_closed(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("broken")
    area.zone(name="Broken", zone_type="frontier", continent="varath")
    room = area.room("entry", name="Entry", desc="A threshold.")
    area.exit(room, "missing_zone:gate", "north", one_way=True)
    area.gathering_pool("ore", rooms=["missing_room"], materials=["iron_ore"])
    return area.build()
"""

        result = compile_world_sources({"world/areas/broken.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(
            [diagnostic.code for diagnostic in result.diagnostics],
            ["unresolved-cross-zone-room", "unresolved-local-room"],
        )
        self.assertEqual([diagnostic.line for diagnostic in result.diagnostics], [6, 7])

    def test_duplicate_exit_direction_fails_closed(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("fork")
    area.zone(name="Fork", zone_type="frontier", continent="varath")
    entry = area.room("entry", name="Entry", desc="A threshold.")
    left = area.room("left", name="Left", desc="A left path.")
    right = area.room("right", name="Right", desc="A right path.")
    area.exit(entry, left, "north", one_way=True)
    area.exit(entry, right, "north", one_way=True)
    return area.build()
"""

        result = compile_world_sources({"world/areas/fork.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(len(result.diagnostics), 1)
        self.assertEqual(result.diagnostics[0].code, "duplicate-exit-direction")
        self.assertEqual(result.diagnostics[0].line, 9)

    def test_nonreciprocal_exit_requires_explicit_one_way_intent(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("intent")
    area.zone(name="Intent", zone_type="frontier", continent="varath")
    entry = area.room("entry", name="Entry", desc="A threshold.")
    ledge = area.room("ledge", name="Ledge", desc="A narrow ledge.")
    area.exit(entry, ledge, "down")
    return area.build()
"""
        explicit = source.replace('"down")', '"down", one_way=True)')

        missing = compile_world_sources({"world/areas/intent.py": source})
        accepted = compile_world_sources({"world/areas/intent.py": explicit})

        self.assertIsNone(missing.manifest)
        self.assertEqual(missing.diagnostics[0].code, "missing-reciprocal-intent")
        self.assertIsNotNone(accepted.manifest)

    def test_social_edges_require_taxonomy_and_authored_nodes(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("social")
    area.zone(name="Social", zone_type="frontier", continent="varath")
    area.social_node("npc", "keeper", display_name="Keeper")
    area.social_edge("npc:keeper", "npc:missing", edge_type="invented")
    return area.build()
"""

        result = compile_world_sources({"world/areas/social.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(
            [diagnostic.code for diagnostic in result.diagnostics],
            ["unresolved-social-node", "unsupported-social-edge-type"],
        )

    def test_runtime_registry_and_action_references_fail_closed(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("registry")
    area.zone(name="Registry", zone_type="frontier", continent="varath")
    room = area.room("entry", name="Entry", desc="A threshold.")
    npc = area.npc(room, "npc_keeper", name="Keeper")
    area.spawn(room, "missing_mob")
    area.vendor(npc, item_ids=["missing_item"])
    area.gathering_pool("ore", rooms=["entry"], materials=["missing_material"])
    area.quest("first", quest_giver="npc_missing", next_quest_id="missing_quest",
               objectives=[{"type": "investigate", "target": "entry", "count": 1}],
               rewards=[{"action_type": "invented_action"},
                        {"action_type": "give_skill_xp", "skill_id": "missing_skill"}])
    return area.build()
"""

        result = compile_world_sources({"world/areas/registry.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(
            [diagnostic.code for diagnostic in result.diagnostics],
            [
                "unknown-mob-template",
                "unknown-item-id",
                "unknown-material-id",
                "unknown-action-type",
                "unknown-skill-id",
                "unresolved-quest-giver",
                "unresolved-quest-id",
            ],
        )

    def test_relationship_factions_must_be_canonical_and_registered(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("factions")
    area.zone(name="Factions", zone_type="frontier", continent="varath")
    room = area.room("entry", name="Entry", desc="A threshold.")
    npc = area.npc(room, "npc_keeper", name="Keeper", faction="warden")
    area.vendor(npc, faction="typo_wardenz")
    area.quest("report", quest_giver="npc_keeper",
               objectives=[{"type": "talk_to", "target": "npc_keeper"}],
               rewards=[{"action_type": "modify_standing",
                         "faction_id": "warden", "delta": 2_500}])
    return area.build()
"""

        result = compile_world_sources({"world/areas/factions.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(
            [diagnostic.code for diagnostic in result.diagnostics],
            [
                "noncanonical-faction-id",
                "unknown-faction-id",
                "noncanonical-faction-id",
            ],
        )

    def test_standing_actions_reject_tiny_legacy_scale_deltas(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("standing")
    area.zone(name="Standing", zone_type="frontier", continent="varath")
    room = area.room("entry", name="Entry", desc="A threshold.")
    area.npc(room, "npc_keeper", faction="wardens")
    area.quest("report", quest_giver="npc_keeper",
               objectives=[{"type": "visit", "target": "entry"}],
               rewards=[{"action_type": "modify_standing",
                         "faction_id": "wardens", "delta": 25}])
    return area.build()
"""

        result = compile_world_sources({"world/areas/standing.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(result.diagnostics[0].code, "invalid-standing-delta")

    def test_relationship_effects_require_valid_ids_targets_and_values(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("effects")
    area.zone(name="Effects", zone_type="frontier", continent="varath")
    room = area.room("entry", name="Entry", desc="A threshold.")
    area.npc(room, "npc_keeper", faction="wardens")
    area.quest("report", quest_giver="npc_keeper",
               objectives=[{"type": "visit", "target": "entry"}],
               rewards=[
                   {"action_type": "modify_dimension", "dimension": "attunement",
                    "delta": 5, "effect_id": "effects:bad_dimension"},
                   {"action_type": "modify_attunement", "zone_id": "missing_zone",
                    "delta": 5, "effect_id": "effects:bad_zone"},
                   {"action_type": "modify_trust", "faction_id": "typo_wardenz",
                    "delta": 10, "effect_id": "effects:bad_trust"},
                   {"action_type": "set_betrayal", "faction_id": "wardens",
                    "betrayed": "yes", "effect_id": "effects:bad_betrayal"},
                   {"action_type": "modify_dimension", "dimension": "network",
                    "delta": 5},
               ])
    return area.build()
"""

        result = compile_world_sources({"world/areas/effects.py": source})

        self.assertIsNone(result.manifest)
        codes = [diagnostic.code for diagnostic in result.diagnostics]
        for expected in (
            "invalid-relationship-dimension",
            "unknown-zone-id",
            "unknown-faction-id",
            "invalid-betrayal-value",
            "invalid-relationship-effect-id",
        ):
            self.assertIn(expected, codes)

    def test_material_affordances_fail_closed_when_they_cannot_be_consumed(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("materials")
    area.zone(name="Materials", zone_type="frontier", continent="varath")
    area.material("iron_ore", tier=2, absorbed_property="",
                  profession_bonus={"missing_skill": 0.1, "smithing": 0})
    return area.build()
"""

        result = compile_world_sources({"world/areas/materials.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(
            [diagnostic.code for diagnostic in result.diagnostics],
            [
                "invalid-material-profession-bonus",
                "invalid-material-property",
                "material-tier-mismatch",
                "unknown-material-profession",
            ],
        )

    def test_quest_skill_progression_count_must_be_a_positive_integer(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("progression")
    area.zone(name="Progression", zone_type="frontier", continent="varath")
    room = area.room("entry", name="Entry", desc="A threshold.")
    npc = area.npc(room, "npc_keeper", name="Keeper")
    area.quest("first", quest_giver="npc_keeper",
               objectives=[{"type": "talk_to", "target": "npc_keeper"}],
               rewards=[{"action_type": "give_skill_xp",
                         "skill_id": "tracking", "count": 0}])
    return area.build()
"""

        result = compile_world_sources({"world/areas/progression.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(
            [diagnostic.code for diagnostic in result.diagnostics],
            ["invalid-skill-award-count"],
        )

    def test_globally_stable_entity_ids_cannot_be_redefined(self):
        from world.content_compiler import compile_world_sources

        template = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("{zone}")
    area.zone(name="{zone}", zone_type="frontier", continent="varath")
    room = area.room("entry", name="Entry", desc="A threshold.")
    area.npc(room, "npc_shared", name="Shared")
    return area.build()
"""

        result = compile_world_sources(
            {
                "world/areas/one.py": template.format(zone="one"),
                "world/areas/two.py": template.format(zone="two"),
            }
        )

        self.assertIsNone(result.manifest)
        self.assertEqual(len(result.diagnostics), 1)
        self.assertEqual(result.diagnostics[0].code, "duplicate-npc-id")
        self.assertEqual(result.diagnostics[0].source_path, "world/areas/two.py")

    def test_quest_objective_types_and_targets_resolve_to_runtime_authority(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("objectives")
    area.zone(name="Objectives", zone_type="frontier", continent="varath")
    room = area.room("entry", name="Entry", desc="A threshold.")
    area.npc(room, "npc_keeper", name="Keeper")
    area.quest("broken", quest_giver="npc_keeper", objectives=[
        {"type": "dance_forever", "target": "entry", "count": 1},
        {"type": "kill", "target": "missing_mob", "count": 1},
        {"type": "visit", "target": "missing_room", "count": 1},
    ])
    return area.build()
"""

        result = compile_world_sources({"world/areas/objectives.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(
            [diagnostic.code for diagnostic in result.diagnostics],
            [
                "unknown-objective-type",
                "unresolved-objective-target",
                "unresolved-objective-target",
            ],
        )

    def test_runtime_identity_ids_must_use_canonical_lowercase(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("canonical")
    area.zone(name="Canonical", zone_type="frontier", continent="varath")
    area.room("Room_Mixed", name="Mixed", desc="A threshold.")
    return area.build()
"""

        result = compile_world_sources({"world/areas/canonical.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(result.diagnostics[0].code, "noncanonical-identifier")
        self.assertEqual(result.diagnostics[0].line, 5)

    def test_node_operation_requires_active_zone_metadata(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("inactive_node")
    area.zone(name="Inactive", zone_type="node_active", continent="veluana")
    center = area.room("center", name="Center", desc="A threshold.")
    area.node(center, 4)
    return area.build()
"""

        result = compile_world_sources({"world/areas/inactive_node.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(result.diagnostics[0].code, "inactive-node-operation")

    def test_active_node_metadata_requires_node_operation(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("missing_node")
    area.zone(name="Missing Node", zone_type="node_active", continent="veluana",
              has_node=True, node_type="resonance")
    area.room("center", name="Center", desc="A threshold.")
    return area.build()
"""

        result = compile_world_sources({"world/areas/missing_node.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(result.diagnostics[0].code, "missing-node-operation")

    def test_node_pressure_action_requires_an_authored_node_target(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("plain_zone")
    area.zone(name="Plain Zone", zone_type="frontier", continent="varath")
    room = area.room("entry", name="Entry", desc="A threshold.")
    area.npc(room, "npc_keeper", faction="wardens")
    area.quest("pressure", quest_giver="npc_keeper",
               objectives=[{"type": "visit", "target": "entry"}],
               rewards=[{"action_type": "modify_node_failure",
                         "zone_id": "plain_zone", "delta": 5}])
    return area.build()
"""

        result = compile_world_sources({"world/areas/plain_zone.py": source})

        self.assertIsNone(result.manifest)
        self.assertEqual(
            result.diagnostics[0].code,
            "invalid-node-pressure-target",
        )

    def test_node_flag_must_be_boolean(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("invalid_node_flag")
    area.zone(name="Invalid", zone_type="frontier", continent="varath",
              has_node="yes")
    area.room("entry", name="Entry", desc="A threshold.")
    return area.build()
"""

        result = compile_world_sources(
            {"world/areas/invalid_node_flag.py": source}
        )

        self.assertIsNone(result.manifest)
        self.assertEqual(result.diagnostics[0].code, "invalid-node-flag")

    def test_node_metadata_requires_active_flag(self):
        from world.content_compiler import compile_world_sources

        source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("inactive_node_metadata")
    area.zone(name="Inactive", zone_type="frontier", continent="varath",
              node_type="resonance")
    area.room("entry", name="Entry", desc="A threshold.")
    return area.build()
"""

        result = compile_world_sources(
            {"world/areas/inactive_node_metadata.py": source}
        )

        self.assertIsNone(result.manifest)
        self.assertEqual(result.diagnostics[0].code, "inactive-node-metadata")

    def test_manifest_hash_is_semantic_and_deterministic(self):
        from world.content_compiler import compile_world_sources

        compact = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("hash_zone")
    area.zone(name="Hash Zone", zone_type="frontier", continent="varath")
    area.room("entry", name="Entry", desc="A threshold.")
    return area.build()
"""
        reformatted = """from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder("hash_zone")
    area.zone(
        name="Hash Zone",
        zone_type="frontier",
        continent="varath",
    )
    area.room(
        "entry",
        name="Entry",
        desc="A threshold.",
    )
    return area.build()
"""
        changed = reformatted.replace("A threshold.", "A changed threshold.")

        first = compile_world_sources({"world/areas/hash_zone.py": compact})
        second = compile_world_sources({"world/areas/hash_zone.py": reformatted})
        third = compile_world_sources({"world/areas/hash_zone.py": changed})

        self.assertEqual(first.diagnostics, ())
        self.assertIsNotNone(first.manifest)
        assert first.manifest is not None
        assert second.manifest is not None
        assert third.manifest is not None
        self.assertEqual(first.manifest.manifest_hash, second.manifest.manifest_hash)
        self.assertNotEqual(first.manifest.manifest_hash, third.manifest.manifest_hash)
        self.assertEqual(first.manifest.schema_version, "soravelon.world-content.v1")
        self.assertEqual(first.manifest.zones[0].zone_id, "hash_zone")

    def test_live_world_manifest_compiles_every_literal_zone(self):
        from world.content_compiler import compile_world_manifest

        areas_dir = Path(__file__).resolve().parents[1] / "world" / "areas"
        result = compile_world_manifest(areas_dir)

        self.assertEqual(result.diagnostics, ())
        self.assertIsNotNone(result.manifest)
        assert result.manifest is not None
        self.assertEqual(len(result.manifest.zones), 20)
        self.assertRegex(result.manifest.manifest_hash, r"^[0-9a-f]{64}$")


class TestWorldChangePlanning(unittest.TestCase):
    def test_live_manifest_has_stable_identity_for_every_mutable_operation(self):
        from world.content_compiler import compile_world_manifest, plan_world_changes

        areas_dir = Path(__file__).resolve().parents[1] / "world" / "areas"
        compilation = compile_world_manifest(areas_dir)
        assert compilation.manifest is not None

        result = plan_world_changes(compilation.manifest, compilation.manifest)

        self.assertEqual(result.diagnostics, ())
        self.assertIsNotNone(result.plan)
        assert result.plan is not None
        self.assertEqual(result.plan.changes, ())

    def test_plan_names_creates_updates_moves_deletes_and_player_impact(self):
        from world.content_compiler import compile_world_sources, plan_world_changes

        before_source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("change")
    area.zone(name="Change", zone_type="frontier", continent="varath")
    entry = area.room("entry", name="Entry", desc="Old threshold.")
    square = area.room("square", name="Square", desc="Open square.")
    area.npc(entry, "npc_keeper", name="Keeper")
    area.quest("welcome", quest_giver="npc_keeper", objectives=[
        {"type": "investigate", "target": "entry", "count": 1},
    ])
    return area.build()
"""
        after_source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("change")
    area.zone(name="Change", zone_type="frontier", continent="varath")
    entry = area.room("entry", name="Entry", desc="New threshold.")
    square = area.room("square", name="Square", desc="Open square.")
    area.room("tower", name="Tower", desc="A new tower.")
    area.npc(square, "npc_keeper", name="Keeper")
    return area.build()
"""
        before = compile_world_sources(
            {"world/areas/change.py": before_source}
        ).manifest
        after = compile_world_sources({"world/areas/change.py": after_source}).manifest
        assert before is not None
        assert after is not None

        result = plan_world_changes(before, after)

        self.assertEqual(result.diagnostics, ())
        self.assertIsNotNone(result.plan)
        assert result.plan is not None
        self.assertEqual(result.plan.previous_manifest_hash, before.manifest_hash)
        self.assertEqual(result.plan.target_manifest_hash, after.manifest_hash)
        self.assertEqual(
            [
                (change.action, change.entity_type, change.entity_id)
                for change in result.plan.changes
            ],
            [
                ("move", "npc", "npc_keeper"),
                ("delete", "quest", "welcome"),
                ("update", "room", "entry"),
                ("create", "room", "tower"),
            ],
        )
        quest_delete = result.plan.changes[1]
        self.assertTrue(quest_delete.destructive)
        self.assertEqual(quest_delete.player_impact, ("active-quest-progress",))

    def test_room_delete_is_explicitly_destructive_and_occupancy_sensitive(self):
        from world.content_compiler import compile_world_sources, plan_world_changes

        before_source = """from world.area_builder import AreaBuilder
def build():
    area = AreaBuilder("change")
    area.zone(name="Change", zone_type="frontier", continent="varath")
    area.room("entry", name="Entry", desc="A threshold.")
    return area.build()
"""
        after_source = before_source.replace(
            '    area.room("entry", name="Entry", desc="A threshold.")\n', ""
        )
        before = compile_world_sources(
            {"world/areas/change.py": before_source}
        ).manifest
        after = compile_world_sources({"world/areas/change.py": after_source}).manifest
        assert before is not None
        assert after is not None

        result = plan_world_changes(before, after)

        assert result.plan is not None
        room_delete = result.plan.changes[0]
        self.assertEqual(room_delete.action, "delete")
        self.assertTrue(room_delete.destructive)
        self.assertEqual(
            room_delete.player_impact,
            ("occupied-room", "contained-objects", "connected-navigation"),
        )

    def test_unmodelled_operation_identity_prevents_a_change_plan(self):
        from world.content_compiler import (
            AreaOperation,
            WorldManifest,
            ZoneSourceDefinition,
            plan_world_changes,
        )

        empty = WorldManifest("soravelon.world-content.v1", (), "before")
        unmodelled = AreaOperation(
            source_path="world/areas/future.py",
            line=7,
            column=5,
            method="future_operation",
        )
        target = WorldManifest(
            "soravelon.world-content.v1",
            (ZoneSourceDefinition("world/areas/future.py", "future", (unmodelled,)),),
            "after",
        )

        result = plan_world_changes(empty, target)

        self.assertIsNone(result.plan)
        self.assertEqual(len(result.diagnostics), 1)
        self.assertEqual(result.diagnostics[0].code, "unmodelled-change-identity")
        self.assertEqual(result.diagnostics[0].line, 7)
