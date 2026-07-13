"""Fail-closed contracts for the M6 world-content release rehearsal."""

from types import SimpleNamespace
import unittest


def _status(state, *, target="a" * 64, applied=None):
    return SimpleNamespace(
        state=state,
        target_manifest_hash=target,
        applied_manifest_hash=applied,
        diagnostics=(),
        error="",
    )


class TestDisposableDatabaseGate(unittest.TestCase):
    def test_accepts_only_the_exact_named_rehearsal_postgres_database(self):
        from scripts.rehearse_content_release import require_disposable_postgres

        identity = require_disposable_postgres(
            {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "soravelon_rehearsal_fresh_1",
            },
            expected_name="soravelon_rehearsal_fresh_1",
        )

        self.assertEqual(identity.name, "soravelon_rehearsal_fresh_1")

    def test_rejects_normal_production_name_even_when_expected(self):
        from scripts.rehearse_content_release import RehearsalSafetyError
        from scripts.rehearse_content_release import require_disposable_postgres

        with self.assertRaisesRegex(RehearsalSafetyError, "rehearsal database"):
            require_disposable_postgres(
                {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": "soravelon",
                },
                expected_name="soravelon",
            )

    def test_rejects_database_name_mismatch_and_sqlite(self):
        from scripts.rehearse_content_release import RehearsalSafetyError
        from scripts.rehearse_content_release import require_disposable_postgres

        with self.assertRaisesRegex(RehearsalSafetyError, "does not match"):
            require_disposable_postgres(
                {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": "soravelon_rehearsal_actual",
                },
                expected_name="soravelon_rehearsal_other",
            )

        with self.assertRaisesRegex(RehearsalSafetyError, "PostgreSQL"):
            require_disposable_postgres(
                {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": "soravelon_rehearsal_fake",
                },
                expected_name="soravelon_rehearsal_fake",
            )


class TestContentRevisionRehearsal(unittest.TestCase):
    def test_fresh_path_initializes_verifies_and_reapplies_as_noop(self):
        from scripts.rehearse_content_release import rehearse_content_revision

        manifest = SimpleNamespace(manifest_hash="a" * 64)
        statuses = iter(
            [
                _status("uninitialized"),
                _status("current", applied="a" * 64),
            ]
        )
        calls = []

        evidence = rehearse_content_revision(
            database_kind="fresh",
            database_name="soravelon_rehearsal_fresh_1",
            manifest=manifest,
            git_commit="b" * 40,
            load_status=lambda: next(statuses),
            initialize=lambda target, *, git_commit: (
                calls.append(("initialize", target, git_commit))
                or SimpleNamespace(
                    state="initialized", revision=SimpleNamespace(pk=17)
                )
            ),
            apply=lambda target, *, git_commit: (
                calls.append(("apply", target, git_commit))
                or SimpleNamespace(state="no-op", revision=SimpleNamespace(pk=17))
            ),
            verify_runtime=lambda target: SimpleNamespace(
                verified_manifest_hash=target.manifest_hash,
                diagnostics=(),
            ),
        )

        self.assertEqual([call[0] for call in calls], ["initialize", "apply"])
        self.assertEqual(
            evidence.database_name,
            "soravelon_rehearsal_fresh_1",
        )
        self.assertEqual(evidence.first_state, "initialized")
        self.assertEqual(evidence.reapply_state, "no-op")
        self.assertEqual(evidence.final_state, "current")
        self.assertEqual(evidence.revision_id, 17)

    def test_restored_path_applies_then_requires_idempotent_noop(self):
        from scripts.rehearse_content_release import rehearse_content_revision

        manifest = SimpleNamespace(manifest_hash="a" * 64)
        statuses = iter(
            [
                _status("drifted", target="a" * 64, applied="c" * 64),
                _status("current", applied="a" * 64),
            ]
        )
        apply_results = iter(
            [
                SimpleNamespace(state="applied", revision=SimpleNamespace(pk=20)),
                SimpleNamespace(state="no-op", revision=SimpleNamespace(pk=20)),
            ]
        )

        evidence = rehearse_content_revision(
            database_kind="restored",
            database_name="soravelon_rehearsal_restored_1",
            manifest=manifest,
            git_commit="b" * 40,
            load_status=lambda: next(statuses),
            initialize=lambda *_args, **_kwargs: self.fail(
                "restored rehearsal must not initialize"
            ),
            apply=lambda *_args, **_kwargs: next(apply_results),
            verify_runtime=lambda target: SimpleNamespace(
                verified_manifest_hash=target.manifest_hash,
                diagnostics=(),
            ),
        )

        self.assertEqual(evidence.first_state, "applied")
        self.assertEqual(evidence.reapply_state, "no-op")

    def test_prepared_path_requires_current_and_performs_only_noops(self):
        from scripts.rehearse_content_release import rehearse_content_revision

        manifest = SimpleNamespace(manifest_hash="a" * 64)
        statuses = iter(
            [
                _status("current", applied="a" * 64),
                _status("current", applied="a" * 64),
            ]
        )
        apply_calls = []

        evidence = rehearse_content_revision(
            database_kind="prepared",
            database_name="soravelon_rehearsal_candidate_1",
            manifest=manifest,
            git_commit="b" * 40,
            load_status=lambda: next(statuses),
            initialize=lambda *_args, **_kwargs: self.fail(
                "prepared rehearsal must not initialize"
            ),
            apply=lambda *_args, **_kwargs: (
                apply_calls.append("apply")
                or SimpleNamespace(state="no-op", revision=SimpleNamespace(pk=20))
            ),
            verify_runtime=lambda target: SimpleNamespace(
                verified_manifest_hash=target.manifest_hash,
                diagnostics=(),
            ),
        )

        self.assertEqual(apply_calls, ["apply", "apply"])
        self.assertEqual(evidence.first_state, "no-op")
        self.assertEqual(evidence.reapply_state, "no-op")

    def test_rejects_wrong_initial_state_or_non_idempotent_reapply(self):
        from scripts.rehearse_content_release import ContentRehearsalError
        from scripts.rehearse_content_release import rehearse_content_revision

        manifest = SimpleNamespace(manifest_hash="a" * 64)
        common = {
            "database_kind": "fresh",
            "database_name": "soravelon_rehearsal_fresh_1",
            "manifest": manifest,
            "git_commit": "b" * 40,
            "initialize": lambda *_args, **_kwargs: SimpleNamespace(
                state="initialized", revision=SimpleNamespace(pk=1)
            ),
            "apply": lambda *_args, **_kwargs: SimpleNamespace(
                state="applied", revision=SimpleNamespace(pk=2)
            ),
            "verify_runtime": lambda target: SimpleNamespace(
                verified_manifest_hash=target.manifest_hash,
                diagnostics=(),
            ),
        }

        with self.assertRaisesRegex(ContentRehearsalError, "uninitialized"):
            rehearse_content_revision(
                **common,
                load_status=lambda: _status("current", applied="a" * 64),
            )

        statuses = iter(
            [
                _status("uninitialized"),
                _status("current", applied="a" * 64),
            ]
        )
        with self.assertRaisesRegex(ContentRehearsalError, "no-op"):
            rehearse_content_revision(
                **common,
                load_status=lambda: next(statuses),
            )


if __name__ == "__main__":
    unittest.main()
