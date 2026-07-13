"""Regression contracts for reviewed dependency-security exceptions."""

from __future__ import annotations

import ast
from importlib.metadata import requires, version
from pathlib import Path
import subprocess
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
CI_PATH = REPO_ROOT / ".github" / "workflows" / "ci.yml"
SECURITY_PATH = REPO_ROOT / "docs" / "SECURITY.md"


class TestDependencySecurityPolicy(unittest.TestCase):
    def test_ci_audits_dependencies_with_only_the_reviewed_exception(self):
        workflow = CI_PATH.read_text()

        self.assertIn("pip-audit==2.10.0", workflow)
        self.assertIn(
            "python -m pip_audit --ignore-vuln PYSEC-2026-160",
            workflow,
        )
        self.assertEqual(workflow.count("--ignore-vuln"), 1)

    def test_twisted_dns_exception_matches_the_installed_runtime_contract(self):
        self.assertEqual(version("evennia"), "6.1.0")
        evennia_requirements = requires("evennia") or []
        self.assertIn("twisted<25,>=24.11.0", evennia_requirements)

        policy = SECURITY_PATH.read_text()
        for contract in (
            "PYSEC-2026-160",
            "CVE-2026-42304",
            "GHSA-grgv-6hw6-v9g4",
            "twisted.names",
            "Twisted 26.4.0",
        ):
            with self.subTest(contract=contract):
                self.assertIn(contract, policy)

    def test_project_does_not_import_the_waived_dns_subsystem(self):
        result = subprocess.run(
            ["git", "ls-files", "--", "*.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        violations: list[str] = []
        for relative_path in result.stdout.splitlines():
            path = REPO_ROOT / relative_path
            tree = ast.parse(path.read_text(), filename=relative_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    modules = [node.module or ""]
                else:
                    continue
                if any(
                    module == "twisted.names"
                    or module.startswith("twisted.names.")
                    for module in modules
                ):
                    violations.append(relative_path)

        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
