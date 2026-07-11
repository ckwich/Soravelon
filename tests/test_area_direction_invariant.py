"""Repository-wide authoring contracts for player navigation."""

import ast
from collections import defaultdict
from pathlib import Path
from unittest import TestCase


class TestAreaDirectionInvariant(TestCase):
    def test_every_authored_room_direction_is_unique(self):
        """Area DSL specs expose one player destination per direction."""
        duplicates = []
        for area_path in Path("world/areas").glob("*.py"):
            tree = ast.parse(area_path.read_text(), filename=str(area_path))
            exits_by_direction = defaultdict(list)
            for node in ast.walk(tree):
                if not (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "exit"
                    and len(node.args) >= 3
                ):
                    continue
                source, _destination, direction = node.args[:3]
                if not (
                    isinstance(source, ast.Name)
                    and isinstance(direction, ast.Constant)
                    and isinstance(direction.value, str)
                ):
                    continue
                exits_by_direction[(source.id, direction.value)].append(node.lineno)

            for (source, direction), lines in exits_by_direction.items():
                if len(lines) > 1:
                    duplicates.append(
                        f"{area_path}:{source}:{direction} at lines {lines}"
                    )

        self.assertEqual(duplicates, [])
