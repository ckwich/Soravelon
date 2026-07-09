# Repository Hygiene Gate

Soravelon's release gate audits the Git index for sensitive, transient, and
generated files. It deliberately does not reject ignored, untracked local
runtime files: those belong on a developer machine, but never in a release
commit.

## Run the gate

```bash
python scripts/audit_repo_hygiene.py
```

Exit codes:

- `0`: no forbidden tracked paths
- `1`: one or more forbidden paths are tracked
- `2`: Git index inspection failed, so release verification must stop

Failure output contains sorted repository-relative paths only. The gate never
reads or prints file contents, including secret files.

## Rejected tracked paths

The gate fails when the index contains:

- anything Git currently considers ignored
- `.env` or `.env.*` files other than `*.example`
- non-example `server/conf/secret_settings*` modules
- runtime output under `server/logs/`
- collected static output under `server/.static/`
- `.claude/worktrees/` content
- SQLite and similar local database files, including journal/WAL companions
- temporary or backup artifacts under `world/areas/`
- known generated agent, Python cache, virtualenv, PID, and repository-analysis
  artifacts

The specific path checks remain active even if an ignore rule is accidentally
removed. The tracked-ignored check catches new ignored artifact families
without requiring a script change.

## Intentionally durable files

The gate does not classify these as artifacts:

- `AGENTS.md`
- tracked `.planning/` documents
- `.env.example`
- `server/conf/secret_settings.example.py`

They remain valid source-controlled project context unless a separate project
decision explicitly retires them.

## Repair procedure

Review every reported path before changing the index. For a local artifact that
must remain on disk, remove only its tracked entry and ensure the corresponding
ignore rule exists. Do not delete or reset unrelated working-tree changes.

Example:

```bash
git rm --cached -- path/to/local-artifact
python scripts/audit_repo_hygiene.py
```

Secrets require more than index cleanup: rotate the exposed value and assess
Git-history remediation separately.

## Release expectation

The hygiene gate must pass on the exact release index before tests, migrations,
or deployment begin. A clean working tree is a separate release requirement;
this script owns only the stronger question of whether the commit itself would
ship forbidden files.
