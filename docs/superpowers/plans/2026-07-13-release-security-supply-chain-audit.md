# Soravelon Release Audit — Security And Supply Chain

**Date:** 2026-07-13
**Audited code:** `c525d90437860964ed32d42a6c09571ca9507c86`
**Decision:** Application and disposable-host security gates pass with one
documented upstream dependency advisory; an Internet edge is not yet claimed.

## Lens And Deciding Gate

This audit covered production settings, secrets and repository history,
service privilege, endpoint parsing, SQL identifier composition, browser asset
provenance, Python dependency findings, and static security analysis. Findings
had to be fixed or narrowly governed before the twice-clean release candidate.

## Findings And Remediation

- Commit `d12c412` applies a least-privilege systemd sandbox to the production
  service contract.
- Commits `fb63fbe` and `164f960` clarify the WebSocket handshake hash and reject
  malformed production endpoint configuration.
- Commit `1dfcf6b` composes audit SQL identifiers through the database driver
  instead of string interpolation.
- Commits `ea6858d` and `8ce3fbb` narrow scanner waivers and fail CI on
  unreviewed medium-or-higher Python findings.
- Commit `aeb833f` records the Twisted DNS advisory as a governed upstream
  exception until Evennia supports a repaired Twisted release.
- Commit `7fd5101` serves pinned browser assets locally rather than depending on
  third-party runtime CDNs.

## Evidence

- Bandit: 128,785 lines of code scanned; zero medium/high findings.
- Semgrep Python and Django rules: zero findings and zero scan errors.
- Gitleaks full-history scan: zero findings.
- `detect-secrets`: 38 candidates manually inspected; all were examples,
  fixtures, hashes, or other non-secrets.
- `pip-audit`: no unreviewed findings; the documented Twisted advisory is the
  only governed exception.
- Production Django deploy checks, fail-closed settings checks, and real
  Telnet/HTTPS/WebSocket protocol gates passed in both final candidates.

## Residual Risk

Twisted 24.11.0 retains a DNS-resolution advisory through the Evennia 6.1
dependency ceiling. The audited Soravelon runtime does not invoke the affected
resolver path, and the waiver is scoped rather than global. Re-audit when
Evennia supports Twisted 26.4 or later. DNS, TLS certificates, firewall rules,
mail, monitoring, credential storage, and DDoS posture remain hosting choices;
this document does not certify an unbuilt Internet edge.
