# Soravelon Deployment

Soravelon public v1 is designed for a single Linux host running Evennia with PostgreSQL.

## Production shape

- Ubuntu 24.04 LTS or similar
- Python 3.12
- PostgreSQL 16
- One system user, for example `soravelon`
- HTTPS reverse proxy required for the authenticated public web client

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
   python -m django createsuperuser
   ```
   This must create superuser account `#1` before systemd starts Evennia. The
   service preflight rejects an absent or non-admin account `#1` instead of
   allowing Evennia's interactive first-run prompt to restart-loop under
   systemd.

## Automated release verification

`scripts/verify_release.py` is the single owner for checks that can be proven
from the repository and configured database.

Against a disposable fresh PostgreSQL database, run the complete unsharded
gate:

```bash
python scripts/verify_release.py full
```

`full` runs repository hygiene, working and staged diff checks, migration drift,
`migrate --noinput`, Django's production deploy check, smoke imports,
economy/inventory reconciliation, and the canonical test command. It therefore
mutates the configured database by applying migrations; never point this mode at
an unbacked production database.

CI runs an early preflight job, then runs `full` independently in each shard
because every job receives its own fresh PostgreSQL service. Evennia initializes
against that configured database before Django creates the test database, so
each shard must migrate its own disposable base database first:

```bash
python scripts/verify_release.py preflight
python scripts/verify_release.py full --shard 1/4
```

All four deterministic test shards must pass. `preflight` is also the staging
database gate after backup and restore rehearsal.

This executable does not prove TLS certificates, DNS, reverse-proxy behavior,
or systemd lifecycle behavior. Those checks require the real Linux host and
remain explicit staging gates.

## Systemd units

Install the tracked `deploy/systemd/soravelon.service` unit. It runs
`evennia ipstart`, which keeps the Portal in the foreground while the Portal
owns the Server process. Do not replace it with `evennia start`: that command
daemonizes and leaves `Type=simple` supervising a launcher that has already
exited.

The pre-start executable rejects non-production settings, security warnings,
pending migrations, a missing admin account `#1`, or broken runtime imports
before it collects static assets. It checks migrations; it never applies them
implicitly. The unit creates the ignored runtime log directory and explicitly
puts the virtualenv on `PATH`, which Evennia needs when it launches `twistd`.

The relevant unit contract is:

```ini
[Unit]
Description=Soravelon Evennia Service
After=network-online.target postgresql.service
Wants=network-online.target postgresql.service

[Service]
Type=simple
User=soravelon
Group=soravelon
WorkingDirectory=/srv/soravelon
EnvironmentFile=/etc/soravelon/soravelon.env
Environment=PYTHONUNBUFFERED=1
Environment=PATH=/srv/soravelon/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStartPre=/usr/bin/install -d -m 0750 /srv/soravelon/server/logs
ExecStartPre=/srv/soravelon/.venv/bin/python scripts/verify_service_prestart.py
ExecStart=/srv/soravelon/.venv/bin/evennia ipstart
ExecStop=/srv/soravelon/.venv/bin/evennia stop
ExecReload=/srv/soravelon/.venv/bin/evennia reload
Restart=always
RestartSec=5
KillMode=control-group
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

After copying the unit to `/etc/systemd/system/soravelon.service`, run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now soravelon
sudo systemctl status soravelon
sudo journalctl -u soravelon -f
```

On staging, prove the actual lifecycle rather than inferring it from the unit
text: start; kill the service control group and observe automatic restart;
reload; stop and confirm all listeners/PIDs are gone; start again; reboot the
host; and confirm the service and player reconnection recover. Record the
commands, timestamps, exit states, and journal excerpts in the release record.

## Release procedure

1. Deploy from a clean tagged commit.
2. Confirm the PostgreSQL preflight job and all four canonical-test shards are
   green for that exact commit.
3. Back up the target database and confirm a restore on disposable PostgreSQL.
4. Activate the virtualenv and pull the tagged commit on staging.
5. Run `python scripts/verify_release.py preflight` against staging. This applies
   pending migrations and reconciles economy/inventory persistence.
6. Verify TLS, DNS, reverse proxy, and the full systemd lifecycle on the real
   host.
7. Restart the service.
8. Verify player login, movement, combat, loot, vendor, bank, and crafting on
   staging before production cutover.

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
