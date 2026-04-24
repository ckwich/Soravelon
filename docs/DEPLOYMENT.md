# Soravelon Deployment

Soravelon public v1 is designed for a single Linux host running Evennia with PostgreSQL.

## Production shape

- Ubuntu 24.04 LTS or similar
- Python 3.12
- PostgreSQL 16
- One system user, for example `soravelon`
- Reverse proxy optional for the web client, but recommended if exposing HTTP publicly

## First-time setup

1. Create the host user and clone the repo.
2. Create a virtualenv and install dependencies:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to your deployment secret store or systemd environment file.
4. Set `SORAVELON_ENV=production` and fill in the PostgreSQL values.
5. Create the database and a dedicated DB user.
6. Run migrations:
   ```bash
   evennia migrate
   ```
7. Create the admin account:
   ```bash
   evennia createsuperuser
   ```

## Systemd units

Use one service for the Evennia launcher process. A ready-to-edit template
is included at `deploy/systemd/soravelon.service`. Example:

```ini
[Unit]
Description=Soravelon Evennia
After=network.target postgresql.service

[Service]
Type=simple
User=soravelon
WorkingDirectory=/srv/soravelon
EnvironmentFile=/etc/soravelon/soravelon.env
ExecStart=/srv/soravelon/.venv/bin/evennia start
ExecStop=/srv/soravelon/.venv/bin/evennia stop
ExecReload=/srv/soravelon/.venv/bin/evennia reload
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Release procedure

1. Deploy from a clean tagged commit.
2. Activate the virtualenv.
3. Pull code.
4. Run `python scripts/smoke_start.py`.
5. Run `python scripts/run_tests.py`.
6. Run `evennia migrate`.
7. Restart the service.
8. Verify player login, movement, combat, loot, vendor, bank, and crafting on staging before production cutover.

Use [docs/STAGING_CHECKLIST.md](STAGING_CHECKLIST.md) as the release gate.

## Backups

- Database: nightly `pg_dump` to off-host storage.
- Config: back up `/etc/soravelon/soravelon.env`.
- Logs: rotate `server/logs/*.log` and retain at least 7 days.

Example backup:

```bash
pg_dump --format=custom --file "/var/backups/soravelon/soravelon-$(date +%F).dump" soravelon
```

## Restore drill

1. Stop Evennia.
2. Restore the PostgreSQL dump into a clean database.
3. Reapply the environment file.
4. Start Evennia.
5. Verify the admin account can log in and authored zones load without tracebacks.
