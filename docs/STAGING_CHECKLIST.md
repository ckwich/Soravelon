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

- `python scripts/audit_repo_hygiene.py` passes, or tracked `.claude/worktrees` entries were intentionally repaired
- `python scripts/smoke_start.py` passes
- `python scripts/run_tests.py` passes on the release candidate branch

## Database and boot

- `evennia migrate` completed without errors
- admin account created or confirmed
- systemd unit installed from `deploy/systemd/soravelon.service`
- service starts cleanly
- no startup tracebacks in `server/logs/server.log` or `server/logs/portal.log`

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

- `evennia reload` preserves expected runtime state
- service restart succeeds
- player can reconnect after restart
- spawned zones and cross-zone exits still load

## Operations

- database backup command tested
- restore process rehearsed on a disposable database
- log rotation configured
- release tag or commit hash recorded
- rollback target identified
