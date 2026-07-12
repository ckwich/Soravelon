"""Pure compiler contracts for literal AreaBuilder source."""

from pathlib import Path
import unittest


class TestAreaSourceAuthority(unittest.TestCase):
    def test_literal_operations_compile_with_immutable_source_locations(self):
        from world.content_compiler import compile_area_source

        source = """from world.area_builder import AreaBuilder

def build():
    area = AreaBuilder()
    area.zone("test_zone", "Test Zone", zone_type="frontier")
    room = area.room("entry", "Entry", "A threshold.")
    area.exit(room, "entry", "out")
    return area.build()
"""

        result = compile_area_source(source, source_path="world/areas/test_zone.py")

        self.assertEqual(result.diagnostics, ())
        self.assertIsNotNone(result.definition)
        assert result.definition is not None
        self.assertEqual(
            [operation.method for operation in result.definition.operations],
            ["zone", "room", "exit", "build"],
        )
        self.assertEqual(result.definition.operations[0].line, 5)
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
    area = AreaBuilder()
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
    area = AreaBuilder()
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
