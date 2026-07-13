"""Contracts for the durable M6 release-evidence record."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "verify_release_evidence.py"
HASH = "a" * 64
COMMIT = "b" * 40


def _content(kind, database, *, run_number):
    return {
        "database_kind": kind,
        "database_name": database,
        "initial_state": "uninitialized" if kind == "fresh" else "current",
        "first_state": "initialized" if kind == "fresh" else "no-op",
        "reapply_state": "no-op",
        "final_state": "current",
        "manifest_hash": HASH,
        "revision_id": run_number,
        "git_commit": COMMIT,
    }


def _rehearsal(run_number):
    prefix = f"soravelon_rehearsal_run{run_number}"
    return {
        "run_id": f"run-{run_number}",
        "fresh_content": _content(
            "fresh",
            f"{prefix}_fresh",
            run_number=run_number,
        ),
        "restored_content": _content(
            "restored",
            f"{prefix}_restored",
            run_number=run_number,
        ),
        "candidate_database": f"{prefix}_candidate",
        "backup": {
            "artifact": f"artifacts/run-{run_number}.dump",
            "sha256": HASH,
            "restore_verified": True,
        },
        "failure_injection": {
            "content": True,
            "economy": True,
            "inventory": True,
            "quest": True,
        },
        "lifecycle": {
            "start": True,
            "crash_restart": True,
            "reload": True,
            "stop": True,
            "reboot": True,
            "listeners_recovered": True,
            "portal_pid_preserved_on_reload": True,
            "startup_content_writes": [0, 0],
        },
        "candidate": {
            "passed": True,
            "output_sha256": HASH,
        },
    }


def _valid_record():
    return {
        "schema_version": "soravelon.release-evidence.v1",
        "release": {
            "git_commit": COMMIT,
            "manifest_hash": HASH,
            "created_at_utc": "2026-07-13T10:00:00Z",
            "limitations": ["Public DNS and production credentials are not artifacts."],
            "rollback_instructions": [
                "Stop the service.",
                "Restore the verified database dump.",
                "Check out the recorded rollback commit and rerun preflight.",
            ],
        },
        "environment": {
            "os": "Ubuntu 24.04.4 LTS",
            "architecture": "aarch64",
            "python": "3.12.3",
            "postgresql": "16.14",
            "django": "6.0.7",
            "evennia": "6.1.0",
            "psycopg": "3.3.4",
        },
        "rehearsals": [_rehearsal(1), _rehearsal(2)],
        "builder_packages": [
            {
                "platform": platform,
                "artifact": f"artifacts/builder-{platform}.zip",
                "sha256": HASH,
                "tests_passed": True,
            }
            for platform in (
                "macos-arm64",
                "macos-x64",
                "windows-x64",
                "linux-x64",
            )
        ],
        "human_acceptance": {
            "timed_fresh_player": True,
            "co_op": True,
            "living_world": True,
            "observed_by": "Cole",
            "notes": "Observed against the recorded candidate.",
        },
        "artifacts": [
            {
                "path": "artifacts/release-candidate.log",
                "sha256": HASH,
                "size_bytes": 1024,
            }
        ],
    }


class TestReleaseEvidenceValidation(unittest.TestCase):
    def test_complete_record_passes(self):
        from scripts.verify_release_evidence import validate_release_evidence

        self.assertEqual(validate_release_evidence(_valid_record()), [])

    def test_requires_two_complete_independent_rehearsals(self):
        from scripts.verify_release_evidence import validate_release_evidence

        record = _valid_record()
        record["rehearsals"] = record["rehearsals"][:1]
        record["rehearsals"][0]["candidate"]["passed"] = False
        record["rehearsals"][0]["lifecycle"]["startup_content_writes"] = [0, 1]

        report = "\n".join(validate_release_evidence(record))

        self.assertIn("exactly two", report)
        self.assertIn("candidate.passed", report)
        self.assertIn("startup_content_writes", report)

    def test_rejects_secret_fields_unsafe_database_names_and_absolute_artifacts(self):
        from scripts.verify_release_evidence import validate_release_evidence

        record = _valid_record()
        record["environment"]["database_password"] = "do-not-store"
        record["rehearsals"][0]["fresh_content"]["database_name"] = "soravelon"
        record["artifacts"][0]["path"] = "/var/backups/private.dump"

        report = "\n".join(validate_release_evidence(record))

        self.assertIn("secret-like field", report)
        self.assertIn("soravelon_rehearsal", report)
        self.assertIn("relative", report)

    def test_cli_accepts_complete_json_and_rejects_incomplete_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            valid_path = Path(temp_dir) / "valid.json"
            invalid_path = Path(temp_dir) / "invalid.json"
            valid_path.write_text(json.dumps(_valid_record()))
            invalid_path.write_text("{}")

            valid = subprocess.run(
                [sys.executable, str(SCRIPT), str(valid_path)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            invalid = subprocess.run(
                [sys.executable, str(SCRIPT), str(invalid_path)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertIn("passed", valid.stdout.lower())
        self.assertEqual(invalid.returncode, 1)
        self.assertIn("FAILED", invalid.stderr)

    def test_committed_template_is_deliberately_incomplete(self):
        from scripts.verify_release_evidence import validate_release_evidence

        template = json.loads(
            (
                REPO_ROOT
                / "docs"
                / "releases"
                / "release-evidence-template.json"
            ).read_text()
        )

        report = "\n".join(validate_release_evidence(template))

        self.assertIn("candidate.passed", report)
        self.assertIn("human_acceptance.timed_fresh_player", report)
        self.assertIn("release.git_commit", report)


if __name__ == "__main__":
    unittest.main()
