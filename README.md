# Soravelon

Soravelon is an Evennia 6.1 MUD focused on a server-first public v1 launch: authored zones, combat, progression, crafting, gathering, banking, social systems, and a custom help surface.

## Stack

- Python 3.12
- Evennia 6.1.0
- Django ORM
- SQLite for local development
- PostgreSQL for staging and production

## Repo layout

- `world/` game systems, Django models, migrations, authored content
- `typeclasses/` Evennia typeclasses
- `commands/` player/admin command surface
- `server/conf/` settings and lifecycle hooks
- `tests/` automated coverage
- `scripts/` canonical local automation
- `docs/` deployment and operations notes

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp server/conf/secret_settings.example.py server/conf/secret_settings.py
evennia migrate
evennia start
```

The default local database is `server/evennia.db3`.

## Canonical test command

Use the repo runner instead of plain `pytest`:

```bash
python scripts/run_tests.py
```

That command loads `server.conf.settings`, boots Django correctly, and runs the suite through Django's test runner, which is the reliable path for Evennia-backed tests.

## Smoke check

Before a deploy or after a fresh checkout:

```bash
python scripts/smoke_start.py
```

This verifies the settings import, Django bootstrap, help entry registration, and authored area module imports.

## Production configuration

Production is environment-driven.

1. Copy `.env.example` into your secret store or systemd `EnvironmentFile`.
2. Set `SORAVELON_ENV=production`.
3. Provide `SECRET_KEY`, `ALLOWED_HOSTS`, and PostgreSQL credentials.
4. Keep `server/conf/secret_settings.py` for local development only.

Tracked production overrides live in [server/conf/production_settings.py](server/conf/production_settings.py).

## Deploy and operations

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for:

- first-time host setup
- systemd service wiring
- release procedure
- backups and restore drills

For local repository cleanup and tracked worktree repair, see [docs/REPO_HYGIENE.md](docs/REPO_HYGIENE.md).

## Current launch contract

Public v1 is scoped as a server-first release:

- telnet / Evennia webclient access
- PostgreSQL-backed production deploy
- canonical test + smoke gate before release
- staged rollout on a Linux VPS or Lightsail-class host
