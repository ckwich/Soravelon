# Staging Checklist

Use this checklist before cutting a public v1 production release.

## Host setup

- Linux host provisioned
- Python 3.12 installed
- PostgreSQL installed and reachable
- virtualenv created
- `pip install -r requirements.txt` completed
- environment file created from `.env.example`
- `SORAVELON_ENV=production` set

## Pre-boot validation

- CI release preflight passes on PostgreSQL 16 for the exact release commit
- all four canonical-test shards pass for the exact release commit
- database backup exists and a restore has been rehearsed on disposable PostgreSQL
- `python scripts/verify_release.py preflight` passes against staging after the backup
- release output confirms economy and inventory reconciliation passed

`preflight` owns hygiene, both diff checks, migration drift, migration
application, production deploy checks, smoke imports, and reconciliation. Do not
run it against an unbacked production database.

## Database and boot

- the release gate's fresh PostgreSQL migration completed without errors
- staging migrations completed through `verify_release.py preflight`
- admin account created or confirmed
- systemd unit installed from `deploy/systemd/soravelon.service`
- `scripts/verify_service_prestart.py` passes under the service environment
- service starts cleanly
- `journalctl -u soravelon` contains no startup traceback

## External host proof

These checks are intentionally not claimed by the executable release gate:

- production DNS resolves to the intended host
- the real TLS certificate chain and expiry are valid
- the reverse proxy forwards HTTPS and the expected forwarded-protocol header
- HTTP redirects to HTTPS without a loop
- `systemctl start` leaves the foreground Portal and Server healthy
- killing the staging service control group triggers one clean automatic restart
- `systemctl reload` preserves the expected live runtime state
- `systemctl stop` leaves no Soravelon listener or PID behind
- host reboot returns the enabled service and player reconnection path

## Gameplay smoke

- create or log into a player account
- enter the world successfully
- movement between rooms works
- combat works
- corpse loot works after relog/reload
- vendor purchase creates inventory ownership correctly
- crafting output creates inventory ownership correctly
- banking draft creation works
- help topics resolve for at least one file-backed topic and one dynamic topic

## Restart and persistence

- `systemctl reload soravelon` preserves expected runtime state
- service restart succeeds
- player can reconnect after restart
- spawned zones and cross-zone exits still load

## Operations

- database backup command tested
- restore process rehearsed on a disposable database
- log rotation configured
- release tag or commit hash recorded
- rollback target identified
