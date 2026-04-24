# Soravelon Wave 9 Social, Group, and Cooperative Play Audit

**Date:** 2026-04-22
**Depends on:** `docs/superpowers/plans/2026-04-22-deep-gameplay-code-health-audit-plan.md`
**Follows:** `docs/superpowers/plans/2026-04-22-wave6-gathering-crafting-travel-remediation.md`

## Scope
Wave 9 audited whether Soravelon is genuinely ready for grouped play rather than merely exposing group-related commands. This pass focused on:

- group formation, invites, disconnect behavior, and loot fairness
- social command truthfulness and practical usability
- the relationship between solo-first onboarding and cooperative discovery
- test coverage around cooperative behavior

## Evidence Reviewed

- `world/group_engine.py`
- `commands/cmd_group.py`
- `commands/cmd_social.py`
- `commands/cmd_dialogue.py`
- `world/help_entries.py`
- `world/ability_engine.py`
- `tests/test_group_engine.py`
- `tests/test_social.py`
- `tests/test_help_entries.py`
- `tests/test_session_lifecycle.py`

## Validation Run

- `python scripts/run_tests.py tests.test_group_engine tests.test_social tests.test_help_entries tests.test_session_lifecycle tests.test_content_integration tests.test_help_command`
- Result: `77` tests passed

This confirms the currently-audited social/co-op surface is stable enough to import and execute under test, but it does not mean the behavioral edge cases are fully covered.

## Findings

### Blocker
- **A pending group invite can be accepted even after the inviter is no longer actively present.**
  - `world/group_engine.py:117-128` resolves the inviter with `evennia.search_object("#" + str(inviter_id))`, which finds the character object, not a live session.
  - If the inviter has disconnected but still exists in the database, the invite accept path can still create or attach to a group anchored on that offline character.
  - Player-facing impact: invites can produce ghost groups, confusing leadership state, or acceptance into a group whose inviter is no longer meaningfully present.
  - Recommended fix direction: require the inviter to be puppeted / session-backed at accept time, or persist a richer invite token that expires when the inviter disconnects.
  - Verification needed: regression tests for accepting after inviter disconnect and for leader disconnect during an outstanding invite.

### High-Value Fix
- **The invite system is single-slot and silently overwritable.**
  - `world/group_engine.py:101` stores exactly one `pending_group_invite` on the target with no guard against replacing an existing invite.
  - A second invite can silently stomp the first, with no notice to the target or the original inviter.
  - Player-facing impact: social friction, confusing accept/decline outcomes, and easy accidental griefing in busy hubs.
  - Recommended fix direction: either reject new invites while one is pending, or replace them explicitly with clear messaging to all affected players.
  - Verification needed: tests for invite replacement, duplicate inviter attempts, and explicit decline/expiry behavior.

### High-Value Fix
- **Group disconnect behavior is internally inconsistent between code and player-facing guidance.**
  - The group engine module docstring still says groups dissolve when the leader disconnects at `world/group_engine.py:5`.
  - The live behavior does not dissolve the group. `leave_group()` transfers leadership at `world/group_engine.py:199-202`, and `on_member_disconnect()` simply delegates to `leave_group()` at `world/group_engine.py:385-388`.
  - The help text repeats the dissolve claim at `world/help_entries.py:778`.
  - Existing tests already codify transfer behavior in `tests/test_group_engine.py:101-108`.
  - Player-facing impact: players reading help will expect the party to die on leader disconnect even though the runtime promotes a new leader.
  - Recommended fix direction: decide which behavior is intended, then align engine docstrings, help text, and terminology around that decision.
  - Verification needed: help regression plus a disconnect-specific group behavior test.

### Improvement Opportunity
- **`who` can double-list a player if multiple sessions puppet the same character.**
  - `commands/cmd_social.py:33-38` iterates sessions and appends each puppet directly with no deduplication.
  - Player-facing impact: the online list can look inflated or strange for multi-session users.
  - Recommended fix direction: dedupe by character id before formatting the list.
  - Verification needed: one test with two sessions attached to the same puppet.

### Improvement Opportunity
- **`whisper` targets any searchable room object even though the UX and help describe it as player-to-player.**
  - The help topic says `whisper <player> <message>` at `world/help_entries.py:1059`.
  - The command uses a generic room search at `commands/cmd_social.py:158-160`.
  - Meanwhile `tell` already exists as the directed NPC speech command in `commands/cmd_dialogue.py`.
  - Player-facing impact: ambiguous mental model between `tell` and `whisper`, plus awkward edge cases if an NPC is matched first.
  - Recommended fix direction: either restrict `whisper` to player characters or formally document it as a private in-room message to any speaking target.
  - Verification needed: a direct command test for whispering to an NPC or non-player room object.

### Improvement Opportunity
- **Co-op is mechanically real, but still a little thin as a social loop.**
  - The runtime has good foundations: group state, loot modes, proximity queries, group-targeted abilities, zone shout, whisper, and domain channels.
  - What it lacks are more comfort features that make groups feel sticky in moment-to-moment play: clearer invite lifecycle messaging, easier regrouping affordances, and more explicit co-op teaching in onboarding/help.
  - Player-facing impact: groups can function, but the game still reads as solo-first with multiplayer layered on top.
  - Recommended fix direction: after the safety fixes, consider a small pass on co-op teaching and social convenience rather than only more mechanics.
  - Verification needed: updated help/onboarding audit after remediation.

### Already Strong / Protect With Regression Coverage
- **The underlying co-op combat hooks are much better than a superficial scan would suggest.**
  - `world/ability_engine.py` contains explicit group-targeting and party-scaling paths.
  - `world/group_engine.py` exposes zone/proximity helpers used by group-oriented abilities.
  - `tests/test_group_engine.py` and `tests/test_social.py` already cover a healthy chunk of the happy-path group and social behavior.
  - Recommendation: keep expanding from this base rather than redesigning the system wholesale.

## Wave 9 Verdict

- **Grouped play is real, but not fully launch-clean yet.**
- The biggest concrete risk is invite state handling around disconnects and overwritten invitations.
- After that, the most important work is alignment: help text, docs, and social expectations should describe the co-op model the game actually runs.
