# Soravelon Security Policy

## Reporting

Report suspected vulnerabilities privately to the repository maintainer. Include
the affected surface, reproduction steps, likely impact, and whether player or
operator data may be involved. Do not include live credentials or player data
in an issue, log excerpt, or release artifact.

## Release security gates

Soravelon releases require all of the following:

- environment-owned, non-placeholder production secrets;
- a clean Django `check --deploy --fail-level WARNING` result;
- PostgreSQL and explicit HTTPS reverse-proxy configuration;
- repository-hygiene checks that reject tracked secret files and runtime data;
- dependency auditing that fails on every unreviewed advisory; and
- the tracked sandboxed systemd unit on the Linux host.

Scanner output is evidence, not proof that a release is secure. Findings must be
classified against the reachable runtime path, and accepted exceptions must be
narrow, documented, tested, and removed when their upstream constraint clears.

## Reviewed dependency exception: Twisted DNS decompression

Status: accepted but unresolved. Last reviewed: 2026-07-13.

`pip-audit` reports `PYSEC-2026-160`, also published as `CVE-2026-42304`
and `GHSA-grgv-6hw6-v9g4`, for the installed Twisted 24.11.0 runtime. The
affected code is DNS-name decompression in the `twisted.names` DNS server. The
upstream fix is Twisted 26.4.0.

Soravelon does not import `twisted.names`, configure a DNS factory, or expose a
DNS listener. Its production network surface is the Evennia game/web/WebSocket
set, with optional SSH or SSL, and the systemd unit restricts sockets to
`AF_UNIX`, `AF_INET`, and `AF_INET6`. The vulnerable package code is therefore
installed but is not reachable through the audited Soravelon service topology.
This is a reachability-based exception, not a claim that Twisted 24.11.0 is
fixed.

Evennia 6.1.0 declares `twisted>=24.11.0,<25`, so forcing Twisted 26.4.0 would
violate the supported framework runtime. Soravelon must not override that cap
or vendor the framework's DNS implementation merely to silence the scanner.
CI ignores only `PYSEC-2026-160`; any other dependency finding fails the audit.

This exception expires immediately if Soravelon or a project dependency adds a
`twisted.names` import, a DNS listener, or any other path to the affected
decompression code. It must also be removed when a stable Evennia release
supports Twisted 26.4.0 or newer. At that point, upgrade through the supported
Evennia dependency contract and rerun the complete release candidate gate.
