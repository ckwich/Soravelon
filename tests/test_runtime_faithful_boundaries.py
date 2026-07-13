"""Production modules must not know which test-double library tests use."""

import unittest
from pathlib import Path


class TestRuntimeFaithfulBoundaries(unittest.TestCase):
    def test_world_modules_do_not_detect_or_import_mock_types(self):
        world_root = Path(__file__).resolve().parents[1] / "world"
        offenders = []

        for path in sorted(world_root.rglob("*.py")):
            source = path.read_text()
            if "unittest.mock" in source or "MagicMock" in source:
                offenders.append(path.relative_to(world_root.parent).as_posix())

        self.assertEqual(offenders, [])
