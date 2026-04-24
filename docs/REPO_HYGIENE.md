# Repo Hygiene

Soravelon currently has one known repo-level failure mode: tracked content under `.claude/worktrees/`.

## Why it matters

If `.claude/worktrees/` contains tracked gitlinks or tracked copied files, normal commands such as `git status` can fail or become noisy. That breaks release review, clean deployment checks, and any workflow that depends on a trustworthy worktree.

## Audit

Run:

```bash
python scripts/audit_repo_hygiene.py
```

If the repo is clean, the script exits successfully. If not, it reports the tracked entries under `.claude/worktrees`.

## Repair

The safe intent is:

1. remove tracked `.claude/worktrees` entries from the git index
2. keep `.claude/worktrees/` ignored going forward
3. delete the physical directories only after reviewing whether anything local still matters

This repo includes a repair helper:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\repair_tracked_worktrees.ps1
```

That command removes tracked `.claude/worktrees` entries from the git index with `git update-index --force-remove`. It does not delete the directories from disk.

## Current state

As of 2026-04-18:

- `python scripts/audit_repo_hygiene.py` passes
- `.claude/worktrees/` is no longer tracked in the git index
- the nested worktree directories were removed from disk after audit review
- `git worktree list` shows only the main Soravelon repo

The staged `.claude/worktrees/...` deletions visible in `git status` are expected and should be committed as part of the cleanup.

## Release expectation

Before any public launch cutover:

- `git status` must work from the main repo root
- `.claude/worktrees/` must be ignored and untracked
- release commits must not include transient agent worktree state
