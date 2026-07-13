# Soravelon Release Audit — Reliability And Operations

**Date:** 2026-07-13
**Audited code:** `c525d90437860964ed32d42a6c09571ca9507c86`
**Decision:** The MUD's automated host-ready candidate is twice-clean on a
disposable Linux/PostgreSQL environment; production and the complete program
remain gated by external Builder, human, and infrastructure decisions.

## Lens And Deciding Gate

This audit covered clean-checkout reproducibility, fresh database initialization,
idempotent content state, rollback injections, test-database isolation, service
lifecycle, protocol health, evidence integrity, and failure visibility. The
deciding gate was two fully independent 16-step candidates at one exact SHA.

## Environment

- Ubuntu 24.04.4 LTS ARM64 in the disposable `soravelon-supervisor` VM.
- Python 3.12.3, PostgreSQL 16.14, Django 6.0.7, Evennia 6.1.0, psycopg 3.3.4.
- Clean detached checkout at `c525d90437860964ed32d42a6c09571ca9507c86`.
- Compiled manifest
  `b1f1ceb5813c38c9a3071b56e0f23d6dbde224aa0d11a1f439f63fd561598e0b`.

## Twice-Clean Evidence

Candidate 1 used `soravelon_rehearsal_audit1_candidate` and proved
`uninitialized -> initialized -> no-op -> current`, revision 1. All 16 steps,
all nine gameplay verticals, 2,185 canonical tests in 1,457.275 seconds, and
real Telnet/forwarded-HTTPS webclient/RFC6455 WebSocket checks passed. Log:
`audit1_candidate.log`, 8,776 bytes, SHA-256
`f9d70507446e65d0ea5fd855ff8bced39ec241d533479f7be5cb1042a24dfebf`.

Candidate 2 used `soravelon_rehearsal_audit2_candidate` and independently proved
the same content-state transition and manifest. All 16 steps, nine gameplay
verticals in 196.836 seconds, 2,185 canonical tests in 1,924.080 seconds, and
the three real protocol checks passed. Log: `audit2_candidate.log`, 8,777
bytes, SHA-256
`47c4068d28f1ccba3e3c4d21de2628855d24fa053f0a66b2a2858b82c7dafd90`.

The first attempted audit candidate at `0263d09` failed exactly ten public-page
tests with HTTP 301 responses. The production redirect was correct; the test
requests were not secure. Commit `c525d90` changed that one contract, focused
Linux validation passed 10/10, and only then were both final candidates run.

## Residual Gates

- Builder native macOS Intel, Windows x64, and Linux x64 jobs cannot run until
  the user authorizes a remote CI destination; macOS ARM is locally green.
- Observed 60–90 minute fresh-player, co-op, living-world, and accessibility
  acceptance remains human-owned.
- The final release-evidence record cannot be truthfully marked complete until
  those external results exist.
- No hosting account, region, DNS, TLS, monitoring, retention, secrets, budget,
  rollout window, or production dataset has been selected or created.

This is reproducible host-readiness evidence, not a claim that production is
already online.
