# Social Web Vael's Crossing Runtime Verification

This is an acceptance gate for the live Social Web route, not a printed
checklist or a set of admin shortcuts. It proves that the Warden report can be
played through the materialized world without exposing player-facing numeric
reputation meters.

## Preconditions

Run this against the database used by a normally started Soravelon server.
Area loading must already have completed: the verifier checks live state and
does not create routes, inject rumors, or repair missing topology for you.

## Runtime Gate

```text
python scripts/playtest_social_web_vertical.py --verify
```

Success prints five `PASS` lines:

- `applied migrations` — every current `world` migration leaf is applied.
- `materialized topology` — the six authored Vael's Crossing/Ashreach Social
  nodes are bound to their owning zones.
- `reciprocal exits` — the real Ashway route connects `hg_south_road` south to
  `ash_road_01`, with the northbound return exit present.
- `edge policy` — the active `warden_report` and `inn_traveler` edges retain
  their authored direction, trust, latency, and scope tags.
- `route state` — the actual room graph contains a cross-zone route from Agent
  Calloway to Commander Harven.

Any `FAIL` line is a release-blocking runtime contradiction. Fix the authored
area, migration, Social topology, or exit state that the message names; do not
work around it with an admin command or a manual Social Web write.

## Player-Path Proof

The automated acceptance suite also keeps a database-backed command and movement test for the authored delivery:

1. The player uses `talk Calloway` and `accept` at the real Warden office.
2. The player traverses the materialized exits across the Ashway into Ashreach.
3. The player uses `talk Harven` in the real outpost room.
4. The quest completes, consumes the field report, and writes the fact, claim,
   and Warden knowledge records through the normal reward path.

That test is the authority proof for acceptance through consequence. The
runtime gate is the deployment-oriented proof that the same authored route and
Social policy exist in the live database.
