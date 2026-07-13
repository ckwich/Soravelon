import json
from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase


class TestOfflineContentContract(SimpleTestCase):
    def test_committed_artifact_matches_live_server_authority(self):
        from world.content_contract import (
            DEFAULT_ARTIFACT_PATH,
            build_content_contract,
            contract_artifact_is_current,
        )

        self.assertTrue(contract_artifact_is_current())
        payload = json.loads(DEFAULT_ARTIFACT_PATH.read_text())
        self.assertEqual(payload, build_content_contract())
        self.assertEqual(payload["contract_version"], "1.0.0")
        self.assertEqual(payload["validation_rules"]["network_required"], False)

    def test_every_live_manifest_call_is_declared_by_contract(self):
        from world.content_compiler import compile_world_manifest
        from world.content_contract import build_content_contract

        manifest = compile_world_manifest(Path("world/areas")).manifest
        assert manifest is not None
        declared = set(
            build_content_contract()["grammar"]["supported_operations"]
        )
        used = {
            operation.method
            for zone in manifest.zones
            for operation in zone.operations
        }
        self.assertEqual(used - declared, set())

    def test_stale_artifact_fails_closed(self):
        from world.content_contract import contract_artifact_is_current

        with TemporaryDirectory() as directory:
            path = Path(directory) / "contract.json"
            path.write_text("{}\n")
            self.assertFalse(contract_artifact_is_current(path))
