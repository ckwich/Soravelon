"""Pure compiler contracts for literal AreaBuilder source."""

from pathlib import Path
import unittest


class TestAreaSourceAuthority(unittest.TestCase):
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
