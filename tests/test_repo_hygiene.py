"""Repository hygiene gate integration tests."""

from __future__ import annotations

import contextlib
import io
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import audit_repo_hygiene


class TemporaryGitRepository:
    def __init__(self):
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary_directory.name)
        self.git("init", "--quiet")
        self.git("config", "user.email", "repo-hygiene@example.test")
        self.git("config", "user.name", "Repo Hygiene Test")

    def close(self):
        self._temporary_directory.cleanup()

    def git(self, *args: str) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["git", *args],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError(result.stderr or result.stdout)
        return result

    def track(self, path: str, content: str = "fixture", *, force: bool = False):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        args = ["add"]
        if force:
            args.append("--force")
        args.extend(["--", path])
        self.git(*args)


class RepoHygieneTestCase(unittest.TestCase):
    def setUp(self):
        self.repo = TemporaryGitRepository()
        self.original_repo_root = audit_repo_hygiene.REPO_ROOT
        audit_repo_hygiene.REPO_ROOT = self.repo.root

    def tearDown(self):
        audit_repo_hygiene.REPO_ROOT = self.original_repo_root
        self.repo.close()

    def run_gate(self) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            return_code = audit_repo_hygiene.main()
        return return_code, output.getvalue()


class TestRepoHygieneRejectsTrackedArtifacts(RepoHygieneTestCase):
    def test_rejects_every_forbidden_tracked_path_family(self):
        forbidden_paths = (
            ".env",
            ".env.production",
            "server/conf/secret_settings.py",
            "server/conf/secret_settings.production.py",
            "server/logs/server.log",
            "server/logs/server.log.1",
            "server/.static/admin/js/actions.js",
            ".claude/worktrees/agent/source.py",
            "server/evennia.db3",
            "server/evennia.db3-journal",
            "world/areas/ashreach_plains.py.tmp",
            "world/areas/crownroad_north.py.bak",
            ".claude/graph.json",
            "CODEX_ROUND_9.md",
            "package/__pycache__/module.pyc",
            "server/portal.pid",
        )
        for path in forbidden_paths:
            self.repo.track(path)

        return_code, output = self.run_gate()

        self.assertEqual(return_code, 1)
        for path in forbidden_paths:
            self.assertIn(path, output)

    def test_rejects_any_tracked_path_ignored_by_git(self):
        self.repo.track(".gitignore", "ignored-build.txt\n")
        self.repo.track("ignored-build.txt", force=True)

        return_code, output = self.run_gate()

        self.assertEqual(return_code, 1)
        self.assertIn("ignored-build.txt", output)

    def test_reports_paths_without_file_contents(self):
        secret_content = "TOP_SECRET_VALUE_MUST_NOT_APPEAR"
        self.repo.track(".env", secret_content)

        return_code, output = self.run_gate()

        self.assertEqual(return_code, 1)
        self.assertIn(".env", output)
        self.assertNotIn(secret_content, output)


class TestRepoHygieneAllowsDurableProjectFiles(RepoHygieneTestCase):
    def test_allows_planning_agents_and_example_configuration(self):
        allowed_paths = (
            ".planning/PROJECT.md",
            "AGENTS.md",
            ".env.example",
            "server/conf/secret_settings.example.py",
        )
        for path in allowed_paths:
            self.repo.track(path)

        return_code, output = self.run_gate()

        self.assertEqual(return_code, 0)
        self.assertIn("Repo hygiene OK", output)
