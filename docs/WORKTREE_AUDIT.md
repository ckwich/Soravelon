# Worktree Audit

Audit date: 2026-04-18

Main repo HEAD:

- `957e7adb16eccc37b9145fcf6bb93ac41e3acc7b`
- subject: `fix(17-02): close remaining test failures after worktree cherry-pick`

## Summary

`.claude/worktrees/` currently contains a mix of:

- tracked gitlinks
- copied worktree directories
- stale snapshots of already-merged Soravelon work
- one foreign-repo contamination branch

The good news is that the risky set is small. Most worktree refs are already merged into current `HEAD`.

## Cleanup result

Cleanup was completed on 2026-04-18 after the audit:

- tracked `.claude/worktrees` entries were removed from the git index
- the audited-safe nested worktrees were removed with `git worktree remove --force`
- the orphan snapshot directories `agent-a3389764`, `agent-a770457d`, `agent-a830a517`, and `agent-a8684a3a` were deleted from disk
- `git worktree list` now shows only the main Soravelon repo
- `python scripts/audit_repo_hygiene.py` now reports a clean result

The remaining `worktree-agent-*` branch refs were left intact on purpose so no commit history is lost during cleanup.

## Classification

### Safe to discard after index cleanup

These refs are already ancestors of current `HEAD` and do not represent unmerged Soravelon work:

- `worktree-agent-a15ae698`
- `worktree-agent-a22aed01`
- `worktree-agent-a24373f6`
- `worktree-agent-a267e1a4`
- `worktree-agent-a27afe80`
- `worktree-agent-a2adbc42`
- `worktree-agent-a4487341`
- `worktree-agent-a57fe147-fix`
- `worktree-agent-a6ed54c9`
- `worktree-agent-a7f14855`
- `worktree-agent-a8255c8c`
- `worktree-agent-a97b3192`
- `worktree-agent-a9b60bf8`
- `worktree-agent-ab2c7ec4`
- `worktree-agent-ab35fffa`
- `worktree-agent-ac12ce95`
- `worktree-agent-ac2e9e2e`
- `worktree-agent-acc60516`
- `worktree-agent-acdd6b3b`
- `worktree-agent-ad1b2712`
- `worktree-agent-ad202b19`
- `worktree-agent-ad39fe98`
- `worktree-agent-adc9199a`
- `worktree-agent-adf00460`
- `worktree-agent-ae046a9d`
- `worktree-agent-aecfe50b`
- `worktree-agent-aef69d46`
- `worktree-agent-af9bc8cb`
- `worktree-agent-afdbddb7`
- `worktree-agent-afde8ea0`
- `worktree-agent-abeed234-fix`

Physical directories with broken or missing ref pointers but no active recovery value:

- `agent-a3389764`
- `agent-a770457d`
- `agent-a830a517`
- `agent-a8684a3a`

### Not merged as commits, but content is already superseded in current repo

These branch refs are not ancestors of `HEAD`, but their Soravelon content is older than what currently exists in the repo. They should be archived by SHA, not merged blindly.

#### `worktree-agent-a2312494`

- commit: `ffdc6fde88f7235abe1c049d0ae0fc9fd96a13b7`
- subject: `test(07-02): add failing tests for mob template registry`
- verdict: discard
- reason: `tests/test_mob_templates.py` matches current `HEAD`; remaining diff is planning-only.

#### `worktree-agent-a2cb090d`

- commits:
  - `53a4b8ebef18593414764a0ec16f4b038c4b03f7`
  - `ca3be3c82163a37e56d72ec32b4f1ddf39fc7e16`
- subject: initial mob template registry implementation
- verdict: discard
- reason: `world/mob_templates.py`, `world/mob_spawner.py`, and `tests/test_mob_templates.py` now exist in much larger, later forms. This branch is an early seed, not missing live work.

#### `worktree-agent-a3d8b136`

- commit: `fef1dadccf40b8207b6263e9b9d8c8e6bb6246b5`
- subject: `test(06b-05): add SpawnRecord lifecycle and skill engine test suites`
- verdict: discard
- reason: `git cherry` reports patch-equivalent content already present in `HEAD`.

#### `worktree-agent-a57fe147-broken`

- commits:
  - `ece2db76162023cca32140b5584b00f799d31cdc`
  - `f7e8fd03c9497f95fb109ab37e08c1c37b5254f8`
- subject: tool command + content authoring work
- verdict: discard
- reason: sibling branch `worktree-agent-a57fe147-fix` is merged, and current repo already contains `commands/cmd_tools.py`, `tests/test_content_authoring.py`, and a much richer `world/areas/equipment_catalog.py`.

#### `worktree-agent-a737b7fe`

- commits:
  - `4dd5a113a51037b4f9abd49852fbfa7edc9e3326`
  - `156a2b8cab31e25876f498f2ee04092a98fcf735`
  - `50841eb2d5b7e402f2c63c09188c4321601272ac`
- subject: initial wandering mob system
- verdict: discard
- reason: current repo already contains `world/wander_system.py`, `tests/test_wander_system.py`, and startup registration. This branch is an earlier implementation, not missing functionality.

#### `worktree-agent-a956733a`

- commit: `dad3933e4564516813defda61a934195322df158`
- subject: `feat(07-07): author Cantera Edge forest zone with node system and Layer 1`
- verdict: discard
- reason: current repo already contains a substantially larger `world/areas/cantera_edge.py` plus associated `world/loot_tables.py` and `world/mob_templates.py`.

#### `worktree-agent-aac2e7e4`

- commits:
  - `18f5896a2bf7ba33ff565b31a2d5c32fc00be3b7`
  - `da5e86d594bb5be71036b11121b2338b6770561d`
  - `b089562590b20614c5c4dddec652d6d03ac1a7bc`
- subject: initial equipment catalog and recipe expansion
- verdict: discard
- reason: current repo already has `world/areas/equipment_catalog.py` and `world/crafting_definitions.py` in later expanded forms.

### Foreign or poisoned branch data

#### `worktree-agent-aa2bede1`

- commits:
  - `cc81c7180a76e181ee47df22b8b611d68e3d5768`
  - `31354d3fbb1211f05110447dd946677447d24445`
- visible subject: `fix(17-02): update stabilize test to match tick-based implementation`
- verdict: do not merge
- reason: the commit tree does not belong to Soravelon. `git cat-file -p 31354d3...` resolves to a tree containing unrelated files such as:
  - `.claude-plugin/plugin.json`
  - `agents/code-reviewer.md`
  - `skills/autofix/SKILL.md`
- this branch is repo contamination and was removed as a nested worktree during cleanup. The branch ref itself was intentionally left intact pending any later branch-pruning decision.

## Physical tree notes

Some physical `agent-*` directories no longer map cleanly to live refs or contain copied snapshots rather than active worktrees. The presence of a directory does not imply unique recoverable work.

The important cleanup target was the git index. That cleanup is now complete.

## Recommended cleanup order

1. Preserve this audit file.
2. Remove tracked `.claude/worktrees` entries from the git index.
3. Re-run `python scripts/audit_repo_hygiene.py`.
4. Confirm `git status` works normally.
5. Delete only the audited-safe physical directories from disk.
6. Re-run `git worktree list` and confirm only the main repo remains.

## Cleanup command

Use:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\repair_tracked_worktrees.ps1
```

This removes tracked `.claude/worktrees` entries from the git index but does not delete the directories from disk.
