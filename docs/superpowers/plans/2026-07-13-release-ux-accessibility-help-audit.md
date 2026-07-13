# Soravelon Release Audit — UX, Accessibility, Help, And Onboarding

**Date:** 2026-07-13
**Audited code:** `c525d90437860964ed32d42a6c09571ca9507c86`
**Decision:** Reviewed public and early-player paths pass their automated and
browser gates; no full WCAG conformance claim is made.

## Lens And Deciding Gate

This audit used live browser state, DOM inspection, screenshots, and focused
behavior tests across the public landing page, account login/recovery,
webclient entry, ancestry selection, help, newcomer guidance, and progressive
map state. The deciding gate combined usable visible behavior with real HTTPS
candidate requests; screenshots alone were not treated as proof.

## Findings And Remediation

- The stock public entry lacked Soravelon identity and a clear play path.
  Commit `5fc9ddc` adds a launch-ready public surface grounded in the existing
  theme and real account/webclient routes.
- Browser assets depended on runtime third parties. Commit `7fd5101` pins and
  serves them locally.
- ANSI-heavy help was unreadable on the website, and help navigation exposed
  stale structure. Commit `a3e6c6d` normalizes public help rendering and makes
  topic/index navigation coherent.
- Login and password recovery felt detached and had inconsistent accessible
  state. Commit `0263d09` unifies branded recovery flows and accessible form
  behavior.
- Early guidance described goals without always giving a runnable interaction.
  Commit `4ccc8ce` points players to commands that exist in the live game.
- Candidate one revealed ten public-page test failures because tests sent
  insecure requests into a production profile that correctly redirects HTTP.
  Commit `c525d90` repairs the test contract by using forwarded HTTPS; it does
  not weaken the redirect.

## Evidence

- Actual browser journeys and comparison screenshots covered landing, login,
  recovery, character ancestry, help index/topic, newcomer dialogue, map, and
  webclient entry.
- Ten of ten focused public-surface tests pass locally and on the production
  Linux profile.
- Both final candidates pass forwarded-HTTPS stock-webclient and RFC6455
  WebSocket round trips.

## Residual Risk

Keyboard-only traversal, screen-reader announcements, contrast at every game
state, zoom/reflow, mobile input, and long-session fatigue still need observed
human accessibility testing. The terminal-style webclient also inherits
framework behavior outside the reviewed public shell. Record concrete issues
from the timed playtest instead of treating this audit as blanket compliance.
