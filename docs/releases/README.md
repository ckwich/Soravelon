# Soravelon Release Evidence

M6 is complete only when a release record derived from
`release-evidence-template.json` passes:

```bash
python scripts/verify_release_evidence.py docs/releases/<release>.json
```

The template is deliberately incomplete and must remain red until evidence is
collected. Do not turn a proof field to `true` from expectation, a unit-test
substitute, or an earlier commit. Retain the corresponding relative artifacts
and SHA-256 hashes beside the record.

The validator requires:

- one exact Git commit and world-manifest hash;
- versions for the Linux, PostgreSQL, Python, Django, Evennia, and psycopg
  environment;
- two independent fresh/restore/candidate rehearsals on distinctly named
  `soravelon_rehearsal_*` databases, with retained fresh/restore receipts;
- backup hashes and confirmed restores;
- content, economy, inventory, and quest rollback injection receipts;
- start, crash/restart, reload, stop, reboot, listener recovery, preserved
  Portal-on-reload, and zero startup content writes across both starts, backed
  by retained lifecycle receipts;
- a green MUD candidate output hash for each run;
- the retained candidate output artifact for each run;
- an exact Builder commit, retained content-contract version/artifact/hash, CI
  run, and separately green macOS ARM, macOS Intel, Windows x64, and Linux x64
  package hashes;
- observed timed fresh-player, co-op, living-world, and accessibility acceptance
  tied to the MUD commit, both real client surfaces, and a retained transcript;
- explicit limitations, rollback steps, and retained artifact metadata.

Never store secrets, passwords, credentials, private keys, or access/API tokens
in a release record. The validator rejects secret-like field names, but the
operator still owns review of free-text notes before publication.

The CLI resolves every declared artifact relative to the record directory by
default and rejects missing files, paths that escape that root, SHA-256
mismatches, and recorded size mismatches. Use
`--artifact-root` only when validating an explicitly assembled release bundle
whose record and retained artifacts have separate parent directories.
