# Soravelon Wave 9 Social, Group, and Cooperative Play Remediation

**Date:** 2026-04-22
**Fixes:** `docs/superpowers/plans/2026-04-22-wave9-social-group-coop-audit.md`

## Summary
Wave 9 remediation tightened the multiplayer surface so group formation and social commands behave more like a launch-ready game and less like a collection of happy-path features.

## Runtime Fixes

### Group invite lifecycle
- `world/group_engine.py` now stores pending invites as a structured token with:
  - `inviter_id`
  - `presence_nonce`
- The nonce is tied to the inviter's live session presence and expires on logout/reconnect.
- `accept_group_invite()` now rejects stale invites instead of accepting based on bare object existence.
- `send_group_invite()` now refuses to silently overwrite a valid pending invite.
- Stale pending invites are cleared automatically so they do not block future invites forever.

### Leadership transfer correctness
- Fixed a deeper state bug in `leave_group()`: when the leader left, leadership transferred correctly, but the old leader was still marked as grouped afterward.
- `_transfer_leadership_internal()` now accepts an `old_leader_stays` flag so normal leadership transfer and leader departure use the same helper without corrupting membership state.

### Social command cleanup
- `commands/cmd_social.py`
  - `who` now deduplicates multiple sessions puppeting the same character.
  - `whisper` now enforces the documented player-to-player behavior instead of targeting arbitrary searchable room objects.

### Help / truthfulness alignment
- Updated `world/help_entries.py` so `help group` now matches runtime behavior:
  - leadership passes on leader disconnect/leave
  - the group only dissolves when everyone leaves
- Updated the top-level `world/group_engine.py` module docstring to match the real system.

### Presence tracking
- `world/session_lifecycle.py` now creates a fresh `presence_nonce` on login and clears it on logout so invite validity can track real live presence.

## Regression Coverage Added

- `tests/test_group_engine.py`
  - pending invite token shape
  - rejecting invite overwrite
  - clearing stale invites
  - leader leave no longer leaves the old leader marked as grouped
  - stale invite rejection after inviter presence expires
- `tests/test_social.py`
  - `who` dedupes same-character multi-session output
  - `whisper` rejects non-player targets
- `tests/test_session_lifecycle.py`
  - presence nonce is created on login
  - presence nonce is cleared on logout
- `tests/test_help_entries.py`
  - group help now asserts the leadership-transfer language and guards against the old dissolve wording

## Validation

- `python -m py_compile world/group_engine.py world/session_lifecycle.py commands/cmd_social.py world/help_entries.py tests/test_group_engine.py tests/test_social.py tests/test_session_lifecycle.py tests/test_help_entries.py`
- `python scripts/run_tests.py tests.test_group_engine tests.test_social tests.test_help_entries tests.test_session_lifecycle`
  - Result: `58` tests passed
- `python scripts/run_tests.py tests.test_content_integration tests.test_help_command`
  - Result: `24` tests passed
- `python scripts/smoke_start.py`
  - Result: passed

## Remaining Wave 9 Opportunities

- Group invites are now safe against stale presence, but still minimal in UX terms. There is still room for:
  - explicit invite expiry messaging
  - optional invite timeout rules
  - more co-op teaching in onboarding/help
- The social/co-op loop is mechanically healthier now, but the next leverage point is still command-surface and golden-path coverage from Wave 10.
