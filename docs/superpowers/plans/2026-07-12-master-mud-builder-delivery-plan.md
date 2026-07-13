# Soravelon Master Delivery Plan — Playable MUD, Offline Builder, Host Readiness

**Status:** Active program plan
**Decision owner:** Cole
**Execution mode:** One small, evidence-gated, commit-bounded slice at a time
**Hosting boundary:** Hosting is deliberately deferred until the release-candidate
gate passes. On 2026-07-12 Cole explicitly authorized production deployment once
the program is stable; provider, region, domain, cost, retention, and credential
choices still require concrete user-controlled infrastructure before rollout.

## 1. Outcome

Deliver a Soravelon MUD that a new player can enter, understand, play with
others, and return to; that runs safely and predictably on a host; and that can
be authored safely through a separate, offline-first Soravelon Builder.

The Builder is a local authoring application, not a MUD control panel. It opens
local source files, validates deterministic content contracts, previews and
reviews changes, and writes reviewed files. It does **not** connect to a live
MUD, call a game API, inspect live player data, deploy content, or mutate a
staging/production database. A human-owned deployment workflow applies reviewed
content after the Builder has exported it.

The player client is intentionally outside this program. The MUD must first
ship a truthful, host-ready protocol and webclient baseline. After hosting is
working with real players, the client becomes the next program and consumes
only stable, documented game/OOB contracts.

## 2. Binding Principles

1. **Runtime truth wins.** A claimed phase is complete only when its real
   runtime gate passes on the live code and relevant database profile.
2. **Content is compiled before it is applied.** AreaBuilder remains literal
   and builder-safe; deterministic compilers and validators own truth,
   cross-zone checks, and revision planning.
3. **The Builder is offline-first.** Contract sharing happens through versioned
   files/package artifacts and fixture suites, never a direct Builder-to-MUD
   connection.
4. **Model generation proposes; deterministic systems decide.** Future model
   tools may draft bounded areas, quests, dialogue, and rewards. They never own
   canonical world truth, rewards, player state, or deployment.
5. **Social Web remains systemic.** Standing, trust, betrayal, memory,
   provenance, local rumor, and subjective NPC interpretation must cause
   player-visible, truthful consequences without reducing to a morality meter.
6. **Every slice has one owner, one deciding gate, and one clean commit.**
   Preserve unrelated dirty work in both repositories.
7. **No pretend release.** A local bundle, mocked path, or source-string check
   does not prove a hostable service or safe content workflow.

## 3. Known Starting Position

### Proven assets

- Evennia 6.1 is the runtime baseline; the upstream telnet bytes fix is in the
  dependency pin rather than a local protocol override.
- The Social Web vertical has real player-path proof: real dialogue, movement,
  quest completion, durable fact/claim/knowledge assertions, and a deterministic
  renderer boundary. Do not reopen completed Social slices without a failing
  live gate.
- Cooperative combat and personal encounter rewards have recent focused proof.
- Production settings have already received meaningful hardening; they still
  need to be exercised by the definitive release gate rather than assumed safe.

### Blocking truths

- World areas still rebuild mutable runtime state at server startup. Hosting
  requires compiled, reviewed, revisioned content application instead.
- The fresh-player progression, recruitment, equipment, quest-consequence,
  connectivity, content-quality, and golden-path gates are incomplete or not
  yet proven together.
- The Builder silently loses unsupported AreaBuilder calls. In particular,
  saving `vaels_crossing.py` currently removes five `social_node` calls and two
  `social_edge` calls. It must not be used to save Social areas until corrected.
- The Builder has no reproducible target-sidecar pipeline; its native
  save/serialize path hard-codes a Windows artifact name; and its cross-repo
  contract suite is not yet a self-contained, trustworthy release gate.
- The Builder shell exposes too much chrome before an author has a task or
  selection. Its current App/store/panel structure has grown into a broad
  all-in-one surface rather than a coherent authoring workbench.

## 4. Program Map

| Program phase | Outcome | Depends on | Exit gate |
| --- | --- | --- | --- |
| M0. Program control | A live, non-fictional backlog and verification baseline | none | every next slice is classified as complete, active, blocked, or obsolete by evidence |
| M1. Host-safe runtime | Production configuration, migrations, supervision, and release verification are truthful | M0 | disposable PostgreSQL release gate and service lifecycle proof pass |
| M2. Revisioned world content | Local authored content is compiled, planned, reviewed, and atomically applied | M1 foundation | no startup mutation; content revision can validate, plan, apply, rollback, and reapply idempotently |
| B1. Offline Builder integrity | Builder round-trips every supported local DSL construct without loss | M2 contract shape | all supported live areas preserve source semantics; unsupported files are clearly read-only/rejected |
| B2. Builder UI rebuild | Organized offline workbench makes correct authoring and review easy | B1 data contract | task-based workbenches, accessibility, recovery, and usability gates pass |
| M3. Fresh-player loop | A first character reaches meaningful play, progression, and induction | M2 | database-backed fresh-player journey passes |
| M4. Living world loop | Co-op, quest consequences, faction/world state, and Social Web operate together | M3 | two-player and social consequence verticals pass without direct seeding |
| M5. Content quality | Launch regions, dialogue, help, and authored incentives are coherent | M3/M4 | connectivity, prose, dialogue, and content contracts pass |
| M6. Release candidate | A reproducible host-ready artifact and operations runbook exist | M1–M5 | full release gate passes twice from clean disposable environments |
| H1. Host together | Cole and the agent choose and execute real infrastructure rollout | M6 | live staging then production acceptance by Cole |
| C1. Player client | A player client consumes stable hosted contracts | H1 | separate client plan accepted after host feedback |

Builder work begins early because it protects content, but it cannot bypass M2
by writing directly into a live game. M3–M5 can advance only through content
that M2 can truthfully validate and apply.

## 5. M0 — Program Control And Reality Baseline

### M0.1 Reconcile the program state

Create an evidence ledger from the current commits, the full-audit remediation
plan, current tests, builder audit, Obsidian intent, and Engram handoffs.

- Mark each legacy task **complete**, **active**, **blocked**, or **obsolete**.
- Do not reimplement verified Social Web or co-op work merely because an old
  plan still shows an unchecked box.
- Classify the dirty Soravelon and Builder trees before every implementation
  session. Never reset, clean, restore, or bundle user-owned changes.
- Promote only binding decisions from stale vault/planning docs into current
  durable docs; retain historical docs as history.

**Gate:** a compact current scorecard names the exact next unblocked slice,
source of truth, deciding command, and required commit boundary.

### M0.2 Establish the verification ladder

Every slice declares the smallest truthful check before coding:

1. focused deterministic unit/service test;
2. surrounding Evennia/Django or Builder integration suite;
3. migration/startup/package check when the slice crosses those boundaries;
4. player-path or desktop interaction proof where the user contract is live;
5. release gate only for release-affecting slices.

**Gate:** no new validator claims success through static text presence, mocks
that replace the deciding runtime, or an unrepresentative fixture.

### M0 evidence scorecard — 2026-07-12

| Workstream / legacy claim | State | Current evidence | Deciding next gate |
| --- | --- | --- | --- |
| M0 program control | **complete** | This scorecard reconciles the current branch, both dirty worktrees, the master-plan Engram handoff, and the live tests/commits below. | Keep the table current only when a later slice changes phase truth. |
| Evennia 6.1 Telnet repair | **complete** | `39c1541` removed the local compatibility path in favor of the pinned upstream repair; `3ca18a4` and `9a9af7d` provide navigation, Telnet, and live Social verifier coverage. | Reopen only if the stock-path regression or live protocol gate fails. |
| Social Web gameplay vertical | **complete** | `285647f` proves the live runtime vertical and `9a9af7d` stabilizes its verifier; `tests/test_social_web_warden_route.py` and `tests/test_social_web_playtest_harness.py` retain the player-path gates. | Re-run after content compiler, dialogue, quest, or area-contract changes. |
| Cooperative combat and personal rewards | **complete** | `57f3f08`, `6f8dbf0`, `3fa9cce`, and `96388a1` culminate in `tests/test_cooperative_combat_vertical.py`. | Re-run as part of M4 and M6 vertical proof. |
| Production configuration hardening | **M1 complete** | `ceea166` and `3676aa7` established environment-owned secrets, fail-closed production settings, listener checks, and `tests/test_production_settings.py`. A 2026-07-12 disposable restored-copy rehearsal preserved an exact sentinel through `pg_dump -Fc`/`pg_restore`, then passed the full PostgreSQL preflight. Commit `34363e2` closes the real Ubuntu/systemd failures found in a clean committed checkout: missing admin `#1`, ignored log directory, and virtualenv `PATH` for Evennia's internal `twistd` launch. Start, forced whole-cgroup crash/restart, clean stop, enabled VM reboot recovery, and reload now pass with all four intended listeners. The final PostgreSQL/systemd reload completed in 1.98 seconds, retained the Portal PID, replaced the Server PID, restored every listener, and preserved a normalized byte-identical dump of all authored content tables. No production deployment is claimed. | Carry the proven service topology into M6's twice-clean release rehearsal and eventual user-approved host deployment. |
| Executable release verification | **M1 complete; M6 twice-clean gate pending** | `df09dd8` added `scripts/verify_release.py`; `b52b50f` makes every isolated CI shard migrate its own disposable base database. Commit `3076197` adds the proven Evennia attribute lookup index, bounds exact ObjectDB tag reads without global aggregation, and makes the full-world integration test exercise production-like autocommit. Sterile PostgreSQL shards 1–4 pass respectively with 523, 453, 435, and 517 tests; this includes economy, quest, and inventory concurrency plus all 20 deferred cross-zone exits. Commit `62787ea` closes six live-command help gaps and stale lookup seams exposed by shards 1 and 3. The restored-copy preflight and the complete Linux service lifecycle are green. Framework-wide `makemigrations --check` proposes only Evennia-owned dynamic proxy migrations plus an upstream tag-index state rename; Soravelon's owned `world` migration state is clean, so no project migration was fabricated in `site-packages`. | Begin M3; retain the twice-clean full release gate for M6 evidence. |
| Revisioned world content | **M2 complete** | The M2.1 chain establishes pure literal compilation, immutable semantic manifests, complete identity, fail-closed topology/registry/action validation, and destructive/player-impact classification. M2.2 adds durable revision evidence, one-applied authority, exact bootstrap verification/adoption, explicit fresh initialization, locked atomic apply, occupied-room protection, durable failure recovery/retry, explicit historical rollback, omitted-zone reconciliation, exact full-world replay without source imports, and verification-only startup. Two complete starts produce zero SQL writes in the representative no-node/no-spawn gate; runtime `player_stock` remains preserved. The M2.2 closeout passes 374 tests and clean owned migration state. M2.3 commit `c3421ce` generates deterministic contract `1.0.0` from live AreaBuilder signatures, grammar, schemas, enums, stable IDs, and validation rules; stale artifacts fail Soravelon tests. Builder commit `62505c1` pins the byte-identical artifact, partitions every server operation into editable/read-only support, names the pinned version on newer grammar, embeds it in the native offline sidecar, and adds a packaged source-validation smoke. No network or MUD connection exists. | Repeat the Linux reload gate now that startup mutation is gone, then begin M3 fresh-player integration. |
| Builder Social DSL round trip | **complete** | Builder commits through `687a589` prove fail-closed parsing, typed storage, IPC preservation, serialization, validation, explicit dynamic-helper rejection, a real local sidecar save/reopen path, and live-area coverage. `fedd997` completes typed Social node/edge creation, outline and command-palette selection, structured inspectors, reference-safe store mutations, and linked navigation without raw JSON or a MUD connection. Commit `693888a` keeps M2 literal runtime configuration offline and round-trippable, preserves structured room-state payloads, and removes player-specific runtime stock. Commit `62505c1` pins Soravelon contract `1.0.0`, proves exact adjacent artifact parity and complete operation classification, embeds the contract in the native sidecar, and gives newer grammar a versioned recovery error. With the live Soravelon path set, 73 sidecar tests pass with one unrelated equipment-catalog skip; frontend passes 48, Rust passes 14, production build and packaged ARM sidecar contract smoke pass, and both npm audits report zero. No Builder-to-MUD connection exists. The unrelated deleted `src-tauri/binaries/.gitkeep` remains preserved. | Re-run B1.1 after parser, validator, serializer, store, Social UI, or server grammar changes. |
| Builder save, packaging, and UI rebuild | **active at B1.3**, externally blocked on matrix execution; B1.2 **complete** | Builder commits through `bd18461` establish typed offline persistence and the target-aware packaging spine. Commit `de5595d` adds a read-only four-runner GitHub Actions release gate for standard macOS ARM, macOS Intel, Windows x64, and Ubuntu x64 hosts; pins Rust 1.95.0; validates Mach-O/ELF/PE architecture instead of trusting filenames; builds a native Tauri bundle; and verifies Tauri's materialized executable. Its Rust integration smoke uses a real generated sidecar and temporary 106-room area to parse, mutate, serialize, validate persisted bytes, create the backup, and reopen the authored change. Locally on macOS ARM, actionlint passes, 48 frontend, 53 sidecar with 15 platform skips, and 14 Rust tests pass; the debug `.app` and materialized executable pass. Both npm audits remain zero. This checkout has no Git remote, so the other native jobs have not run and are not claimed green. | User must identify/authorize a Git remote and CI execution; close B1.3 only after all four native jobs pass. |
| Fresh-player, living-world integration, content quality, and release candidate | **M3 active** | M1 and M2 are complete, and B1.1 is green on the available macOS ARM package path. The compiled playable-connectivity audit now proves every launch zone reachable from a real fresh start through directed walking, reachable quest rewards, destination discovery, and the authored courier graph. Courier Manifest teaches both Tremen and Korahei; a long-haul Varath Prime–Korahei route connects the island cluster without moving the player or weakening origin-presence checks. Authored HP and effective-stat ancestry traits now run idempotently through the shared derived-stat path, and the conflicting dead additive table is gone. The selected 60–90 minute opening is calibrated to four real, one-shot Vael/Ashreach Naturalism interactions: the database-backed practice/session path reaches exactly Practiced, unlocks only Verdance eligibility, and replay adds nothing. Practice now records one typed, idempotent database event for its domain and skill awards; sub-threshold skill-use remainders are durable, event acknowledgement is atomic with both growth paths, and a forced mixed-write failure proves Evennia's live Attribute cache is repaired before exact retry. Practiced now creates a durable, one-time invitation with an authored NPC and hall; `joinguild` is route-only, `talk` reconstructs the local offer, and `accept <secondary_domain>` completes an idempotent induction at that exact contact. Membership, Social Web induction evidence, domain resource, and abilities commit only after the local scene; the retired remote mutation helpers fail closed. The database-backed live-content golden path now starts through authored spawn placement, issues and equips a canonical damaging weapon and protective armor, traverses every leg through real exits, executes the four live dynamic practice commands, walks back to Elwen, and completes `talk`/`accept` induction without debug teleportation. Actual 60–90 minute elapsed-time acceptance remains a human playtest gate. Non-processing crafted outputs now resolve through isolated canonical templates and alter only the recipe's declared live mechanic: damage, armor, or numeric consumable effect; invalid or non-mechanical quality declarations fail closed, and crafted provenance names the actual recipe. Consumables now validate the real Evennia mapping wrapper, refuse unknown or context-only effects without wasting items or combat actions, apply regeneration and poison cures through the canonical status engine, roll volatile effects back when durable ownership changes fail, and decrement one quantity from a real stack rather than deleting it. Every sold catalog tool now starts at its authored maximum durability, loses durability on real gathering, and repairs only through an owned workbench transaction that charges the declared Scales cost; insufficient funds and injected mixed-write failure preserve both tool and currency state. Processing quality now uses the quantity-weighted quality of the whole consumed batch, prevents a single premium unit from laundering poor inputs, and never downgrades the batch below its earned raw quality. All 93 registered materials now have exactly one deterministic processing path. First-hand gathering discovers non-default regional recipes; ore, herbs, wood, fish, and hide enter the authoritative material/inventory/vendor contract; authored zone properties and profession bonuses persist through processing; only the named profession receives its bonus; properties create a durable trade-value premium; and malformed material affordances fail compilation. Fishing consumes one unit from a bait stack and repairs node/bait cache state on transactional failure. Typed durable progression now reaches all seven declared sources: practice; first mastery of each material and recipe; authored quest skill outcomes; courier-landmark discovery; novel search discoveries; and one-time named or legendary combat victories. Repetition of ordinary kills, gathers, crafts, searches, or landmarks cannot duplicate an event; hidden Remnance growth stays closed until the deliberate story-visibility gate; quest payout and crafting rollback remove their progression events atomically; and player quest/reward copy is qualitative rather than numeric XP. The actual timed opening playtest, combined Social/co-op, launch-content, and twice-clean release gates remain open. B1.3's full macOS Intel/Windows/Linux native matrix remains externally unavailable because Builder has no configured remote CI authority. | Build one database-backed two-player M4 vertical that combines group combat, personal rewards, authored quest consequence, faction/world state, and Social Web without direct state seeding. |
| M4 living-world closeout (supersedes the earlier open combined Social/co-op clause) | **automated gate complete** | `8a2d71e`, `3e60386`, `9a07e3c`, `0b27f9a`, and `3909cc4` establish shared frozen quest runs, canonical faction identity/scale, exactly-once relationship effects, and reachable authored node activation. `tests/test_m4_living_world_vertical.py` now composes a real two-player group, explicit quest sharing, allied tactical synergy, nearby kill credit, independent quest and encounter rewards, Consortium standing, hidden Reputation, and per-player Social facts from live authored Cellar Menace input. The affected M4/Social/compiler gate passes 204 tests without direct relationship or Social service seeding. M3's actual 60–90 minute human timing acceptance remains separately open. | Begin M5 with the proven stale Korahei/Tremen `area.vendor(...)` contract scanners, then continue dialogue/help/content and human playtest quality gates. |
| M3/M5 status correction (supersedes the broad M3 row above) | **M3 automated complete, human timing pending; M5 automated gate complete, human acceptance pending** | The content, dialogue, help, and gathering contract group passes 120 tests, and the compiled connectivity audit reaches all 2,193 rooms from `vaels_crossing:hg_arrival`. Commit `78edd6f` adds fail-closed isolated playtest settings, real Telnet/HTTP/RFC6455 Evennia WebSocket smoke, a stock-webclient OOB bridge, and a fresh-player/co-op/Social/crafting/travel/quest/recovery/living-world human acceptance guide. A literal browser run created a real account and character, selected ancestry, received structured inventory/map/stat/status state, and emitted no unhandled OOB events. Commit `c1dcc82` removes the staff-only MudInfo channel from player defaults; real browser account creation then logged no channel-connect error. A user-authorized July 11 Taildrop snapshot (`Obsidian.zip`, SHA-256 `b1bd1017f5b640cf71679a2b3aa11de60c398bed786721b59957ffcbe8e80520`) supplied point-in-time canon authority for the sensitive rewrites. The prose chain through `f8d328f` rewrites all ten flagged zones while preserving literal AreaBuilder semantics; `python scripts/audit_content_prose.py` now reports zero scaffold or repeated-room findings, the 84-test prose/compiler/content-contract/area-validator gate passes, and the external Builder parser accepts the final 100-room Colonist Ruins source with zero errors. The snapshot is not continuous vault access, and actual 60–90 minute elapsed-time acceptance remains a human gate. | Run the broader M6 candidate against the now-green prose gate, then perform the observed 60–90 minute acceptance guide before claiming full M5/M6 completion. |
| M6 PostgreSQL and lifecycle rehearsal (supersedes the earlier pending infrastructure clause) | **automated infrastructure proof green; full M6 blocked before candidate completion** | Commits `7e1b447`, `304d89a`, `fee2e77`, `b40bd74`, `70a8b91`, `4e33df5`, `d8ef5a3`, and `4afa973` establish the disposable PostgreSQL content rehearsal, composed candidate verifier, durable evidence contract, explicit rollback injection, exact-checkout and Git-object gates, and row-level startup-write instrumentation. Commit `3140a55` fixes the real Linux failure: all 427 persistent mob spawn slots now materialize under the atomic content revision instead of first boot, preserve stable room/template identity through apply and rollback, and retire only proven slot-owned mobs. Two independently created PostgreSQL 16 databases on Ubuntu 24.04/Python 3.12/Evennia 6.1 now prove `uninitialized -> initialized -> no-op -> current`; two distinct `pg_dump -Fc` artifacts restore to `current -> no-op -> no-op` with exact manifest `2eb6243d8e6224d963f88353285c7109b877603c33602aabccf9f5a3a608f3e3`. Run 1 records zero authored-content writes on cold start, reload, and two restarts; run 2 records zero on cold start, reload, and restart. Forced whole-unit SIGKILL recovery, clean stop with zero listeners, enabled-VM reboot recovery, all five intended listeners, preserved Portal on reload, and real Telnet/stock-webclient/RFC6455 round trips pass. Commit `8dc1825` models the trusted forwarded-HTTPS proxy contract so production's secure redirect is tested rather than bypassed. The composed 16-step candidate passes Git integrity, prepared content, hygiene, owned migration drift, deploy checks, imports, reconciliation, and all 2,193-room connectivity, then fails exactly at the 1,262 prose findings. No full candidate pass, Builder four-platform matrix, or human acceptance is claimed. | Resolve the live-vault canon gate and prose findings, obtain a Builder remote for the four native packages, perform observed timed/co-op/living-world acceptance, then run and retain two completely green candidate outputs and validate the final release-evidence record. |
| Historical Evennia 6.0/local Telnet override proposals | **obsolete** | `requirements.txt`, `AGENTS.md`, `CLAUDE.md`, and commit `39c1541` establish Evennia 6.1 with no project-local protocol override. | None unless a new upstream defect is proven. |

**External gate:** the native matrix and packaged save/reopen proof are committed
and locally green, but `/Users/ckwichman/Documents/Projects/Sora_builder` has no
Git remote. Obtain the user's explicit destination/push authorization, run the
read-only workflow, and inspect every native job. Do not create a repository or
publish the branch by assumption. B1.3 closes only when all four results are
green; if a runner fails, use that exact job as the next red gate. The user
explicitly removed the Builder GSD-workflow requirement for this program;
continue with the repository's tests and scoped commit discipline.

## 6. M1 — Host-Safe Runtime

### M1.1 Production configuration and secret truth

Re-run the production-settings audit against current code, then close only
proven gaps:

- environment-only non-placeholder secret, hosts, CSRF origins, and PostgreSQL
  configuration;
- secure reverse-proxy HTTPS, cookie, HSTS, content-type, and referrer policy;
- unique and explicit listener topology (Telnet, web, websocket, optional SSH);
- no tracked local secret or runtime artifact; and
- a documented, fail-closed production configuration check.

**Gate:** a sterile production import and Django deploy check fail closed for
missing/malformed configuration and pass only with an explicit test profile.

### M1.2 Migrations and persistent data integrity

- Resolve migration drift without silently changing a developer or player DB.
- Rehearse migrations from empty and restored PostgreSQL copies.
- Add only database constraints that have an audited repair/migration path.
- Make economy, inventory ownership, and quest completion exactly-once,
transactional operations before player data can be hosted.

**Gate:** injected failure and concurrent-actor tests prove no duplicated reward,
negative balance, orphaned inventory, or partially completed quest.

### M1.3 Operations and executable release verification

- Run Evennia under a real foreground supervisor topology with preflight,
  migration, and revision checks.
- Add `scripts/verify_release.py` as the one executable gate for hygiene,
  migrations, production settings, smoke boot, canonical tests, reconciliation,
  connectivity, content revision, and player-path checks.
- Run that gate in CI with PostgreSQL and publish exact failure artifacts.

**Gate:** start, crash restart, reload, stop, and reboot behavior pass in a
Linux-like staging environment with logs and no daemonization ambiguity.

## 7. M2 — Revisioned World Content And Shared Offline Contract

### M2.1 Literal AreaBuilder becomes a deterministic compiler input

- Keep literal `area.room`, `area.exit`, `area.npc`, `area.quest`,
  `area.item`, `area.social_node`, and `area.social_edge` authoring patterns.
- Compile them into immutable `ZoneDefinition`/world manifests before touching
  persistent runtime state.
- Validate local and cross-zone references, exit direction uniqueness,
  reciprocal intent, action/registry IDs, Social taxonomy, and destructive
  world changes.
- Reject direct `.db`, `.tags`, `.attributes`, or `.scripts` mutation in area
  modules. Add a literal DSL operation if a supported behavior needs authoring.

**Gate:** the compiler reports every source location and cannot construct a
mutation plan from an unmodelled area operation.

**Gate evidence:** all 20 live literal zones compile without diagnostics into
an immutable semantic-hash manifest. Dynamic expressions, unresolved room and
Social references, ambiguous directions, unstated one-way exits, invalid
runtime identifiers, and unmodelled change identities fail closed at their
source locations. A manifest-to-itself plan is a proven no-op; representative
create/update/move/delete and destructive-impact classifications are covered.

### M2.2 Plan, review, apply, and record revisions

- Add `worldcontent validate`, `plan`, `apply`, and `status`.
- `plan` is read-only and names creates, updates, moves, deletes, unresolved
  references, player impact, and manifest/Git hashes.
- `apply` holds a deployment lock, is atomic, produces a durable revision
  record, retries idempotently, and refuses destructive occupied-room changes
  outside explicit maintenance approval.
- Startup verifies the applied revision but never rebuilds/deletes content.

**Gate:** a revision validates, plans, applies, rolls back after injected
failure, reapplies as a no-op, and lets a restart leave content unchanged.

### M2.3 Versioned offline contract artifact

Define a pure, versioned content-contract artifact generated from the MUD source
and consumed by the Builder tests/sidecar. It contains the supported literal DSL
grammar, data schemas, enums, stable IDs, validation rules, and contract version.

- It must be usable with no network and no running Evennia service.
- The Builder pins a known version and states when a local file needs a newer
  Builder/contract version.
- Server and Builder CI compare the generated artifact and real source calls.
- Future model-generation tools emit proposal documents against this same
  versioned contract, then compile/validate like human-authored content.

**Non-goal:** no Builder HTTP client, websocket, Django import, remote database,
or live deploy action.

**Gate:** a server grammar change fails CI until the contract and Builder support
or explicit read-only rejection are updated together.

## 8. B1 — Offline Builder Integrity And Desktop Release

### B1.1 Lossless AreaBuilder support

- Make any unrecognized `area.*` call a precise unsupported-file error; never
  silently omit it.
- Add `social_nodes` and `social_edges` to the Builder model, parser,
  serializer, validator, store, inspector, and source-preservation fixtures.
- Test exact source-call preservation for Vael's Crossing, Ashreach, and every
  supported real area—not merely model-to-model round trips.
- Treat dynamic helper modules such as the equipment catalog as a distinct,
  explicit grammar or clearly unsupported/read-only files. Do not advertise
  them as editable zones.

**Gate:** saving a supported Social area changes no semantic DSL call; unsupported
syntax blocks editing with a useful source location and recovery path.

### B1.2 One authoritative offline save pipeline

- One Rust-owned atomic write/backup/recovery transaction handles zones,
  templates, and future content files in both desktop and browser-dev modes.
- Every write serializes, parses, validates, writes a temp file, validates the
  temp file, backs up the prior version, and atomically replaces it.
- Constrain file capabilities to user-selected roots and typed operations.
  Remove generic dev endpoints for arbitrary paths, directories, and sidecar
  subcommands.

**Gate:** deliberate validation, write, and replacement failures preserve the
original local file and provide a recoverable, accessible message.

### B1.3 Reproducible multi-platform sidecar and verification

- Pin the Python test/build environment and generate target-named sidecars for
  macOS ARM/Intel, Windows, and Linux in a repeatable build command.
- Remove the Windows-only native path assumption and use one target-aware Tauri
  sidecar execution path for parser, serializer, and validator.
- Make `npm run verify` self-contained for its documented local prerequisites
  and add CI for all target packaging plus a real packaged save smoke test.
- Deliberately resolve production dependency audit findings and rerun all gates.

**Gate:** fresh macOS, Windows, and Linux packages can load, validate, save,
reopen, and compare a Social area without a manual sidecar artifact.

## 9. B2 — Full Builder UI Rebuild

### B2.0 Design brief

**Surface:** Soravelon Builder desktop authoring workbench.
**Primary user:** a world/content author working locally on one or several
AreaBuilder files.
**User goal:** understand the current area, make a correct focused change,
see its consequences, resolve validation problems, and save/recover safely.
**Product goal:** make the correct offline authoring path easier than raw source
editing while preserving exact round-trip trust.
**Observed friction:** the current three-rail shell creates competing navigation,
large empty states, and inspector dependence before an author has selected work.
The surface mixes global tools, area navigation, history, mode switches, and
entity editors. `App.tsx`, `editorStore.ts`, and several panels have become
oversized coordination points.
**Constraints:** offline-first; native desktop; local files; no live MUD link;
large content graphs; keyboard-first; accessible; content safety outweighs
visual novelty.
**Success:** an author can open a local area, orient within seconds, make an
edit, understand validation impact, inspect a semantic diff, save safely, and
reopen without loss.
**Failure:** key content is hidden, a save state is ambiguous, visual polish
masks an unsupported grammar, or a redesign makes keyboard/recovery harder.

### B2.1 Information architecture: one workbench, explicit contexts

Replace the current general-purpose three-rail experience with this structure:

1. **Home / Local workspace** — choose a local content root, recent files,
   create area, recover draft, and open an explicit local library. This is not
   an empty canvas disguised as an editor.
2. **Area workbench** — one area is active. A narrow explorer shows its content
   tree and search; the main canvas/list presents the selected work mode; a
   contextual inspector appears only when a selection needs properties.
3. **Work modes** — Map & exits, Content, Narrative, Social, and Review. Modes
   are task lenses over the same local model, not separate stores or hidden
   feature tabs.
4. **Local libraries** — templates, item/catalog sources, and reusable
   definitions open as explicitly labelled local documents with their own
   supported grammar state. They are not mixed into an active area.
5. **Review drawer** — validation, semantic diff, save state, backup/recovery,
   and cross-area checks live in one persistent review surface. It never
   competes with the primary authoring task until needed.

The app bar is reduced to document identity, offline/saved/unsaved state,
undo/redo, command palette, and the primary review/save action. It must not
promise server connection, deployment, online ownership, or live player state.

### B2.2 Workbench behavior

| Work mode | Primary task | Main surface | Required local evidence |
| --- | --- | --- | --- |
| Map & exits | build navigable place | room graph and route inspector | directional uniqueness, reciprocal intent, unresolved cross-zone link state |
| Content | author entities and rewards | searchable structured lists plus selected form | schema field help, reference integrity, reward/catalog resolution |
| Narrative | write dialogue, lore, descriptions, quests | topic/quest flow plus readable text editor | topic/schema validity, player-facing preview, prose checks |
| Social | author local social topology and NPC interpretation | typed social graph and profile inspector | node/edge taxonomy, scope/channel/visibility, cross-zone unresolved state |
| Review | decide whether local file is safe to write | problems, semantic diff, source preview, save/recovery | errors vs warnings, exact affected source, backup and last-safe-save state |

### B2.3 Rebuild sequence

1. **UI foundation:** define tokens, typography, spacing, states, icon use,
   keyboard focus rules, responsive desktop widths, reduced motion, and a small
   component contract. Preserve useful existing primitives only after audit.
2. **App shell and document model:** replace global/area/template competition
   with Home, Local Library, and Area Workbench routes; split document/session
   state from content mutation state.
3. **Area explorer and Map & exits:** create the fastest and safest high-volume
   workflow first, including duplicate-direction prevention, linked selection,
   route inspection, and inline problems.
4. **Content and Narrative workbenches:** move entity forms into consistent,
   sectioned editors with relationship pickers, defaults, validation, and
   keyboard-safe creation/deletion flows.
5. **Social workbench:** land only after B1 supports lossless Social DSL. Show
   typed nodes, typed edges, NPC interpretation metadata, unresolved external
   edges, and local policy explanation without connecting to the MUD.
6. **Local libraries:** give templates/catalogs their own explicit, supported
   document flows. Do not treat a dynamic helper module as an area file.
7. **Review, recovery, and quality pass:** semantic diff, validation drawer,
   save/backup/recovery, batch local validation, empty/loading/error/unsupported
   states, accessibility, and performance.

### B2.4 Required states and accessibility

Every workbench supplies default, loading, empty, parse-error, unsupported-file,
validation-error, dirty, saving, save-success, save-failure, recovery, and
read-only states. It supports keyboard navigation, visible focus, sensible
reading order, high contrast, touch targets, reduced motion, zoom, long labels,
large areas, and screen-reader names for graph controls and validation links.

### B2.5 UI acceptance and validation

- A new author completes: open local area -> find room -> create paired exit ->
  add NPC/quest/social edge -> resolve problem -> review diff -> save/reopen.
- An experienced author completes the same path with keyboard-only operation.
- An unsupported file is clearly read-only and cannot be silently saved.
- A failed save leaves a visible recovery option and an untouched last-safe file.
- Screenshot and interaction tests cover all work modes and required states at
  compact and wide desktop widths.
- At least one observed usability session per major workbench tests task
  orientation, validation comprehension, and recovery—not aesthetic preference.

### B2.6 Architecture guardrails

- Decompose the oversized `App.tsx` into route/workbench coordinators.
- Split `editorStore.ts` into document/session, area content, selection,
  history, review, and library stores with explicit interfaces.
- Keep parser/serializer/validator as data services; UI components do not
  recreate grammar rules.
- Use one selection/reference model and one typed IPC client. Do not introduce
  a second source of truth to make a screen easier to render.

## 10. M3 — A Truthful Fresh-Player Loop

### M3.1 Character, equipment, and progression

- One canonical equipment/item catalog; starter kit items truly equip and work;
  consumables, crafting output, materials, quality, and tools have real
  consumers or are removed from player-facing claims.
- Ancestry traits are observable through one runtime path.
- Typed, idempotent authored progression events award domain/skill growth from
  meaningful play—not generic hit XP—and never expose a player-facing level.

### M3.2 Reachable narrative identity

- A fresh player travels through a coherent Vael/Ashreach route, learns danger
  and logistics from the world, receives useful starter outcomes, and reaches
  one fitting Practiced threshold.
- The first-Practiced calibration budget is four meaningful, one-shot
  Naturalism interactions across Vael's Crossing and Ashreach. Human playtest
  acceptance must place that arc between 60 and 90 minutes without forcing
  exhaustive completion or exposing its numeric score.
- Guild recruitment and induction are authored social events; remote joining and
  detached numeric build screens do not return.
- World connectivity validation checks walking, flight discovery, reciprocal
  exits, and circular gates from a real fresh start.

**Gate:** a database-backed fresh-character journey reaches and completes an
induction path with usable gear, meaningful action, and no debug teleportation.

## 11. M4 — Living World And Social Consequence

### M4.1 Cooperative play

- Allies, personal loot/Scales, proximity credit, and authored quest sharing
  have real group/team semantics.
- Group value comes from coordination, positioning, compounds, and subclass
  synergy—not flat HP inflation.

### M4.2 Factions, nodes, quests, and world state

- Canonicalize faction IDs and standing scale; all writers/consumers agree.
- Give dimensions, Attunement, Trust, Betrayal, node pressure, and stabilization
  explicit authored writers and visible consequences.
- Snapshot accepted quest specifications, execute deterministic consequences,
  and prove retries cannot duplicate rewards or world effects.

### M4.3 Social Web release proof

- Retain completed player-path Social vertical proof.
- Re-run it after every content compiler, dialogue, quest, or area contract
  change; add only missing proofs exposed by a real failure.
- The renderer remains optional, redacted, deterministic-fallback-first, and
  incapable of game-state mutation.

**Gate:** a two-player/group path and a Social path run from gameplay input to
durable consequence without direct service seeding or hidden numeric leakage.

## 12. M5 — Content, Dialogue, Help, And Playtest Quality

- Normalize dialogue into a validated authored schema with topic/hint flow.
- Make help and onboarding truthful to Soravelon's custom systems: hidden
  progression, domains, weight, conversation, social consequences, and
  open-world guidance.
- Add prose and content-quality gates, then rewrite affected zones one at a
  time with source-backed lore, mystery constraints, regional labor, spatial
  cues, and meaningful reasons to explore.
- Build human playtest scripts for fresh-player, co-op, social, crafting,
  travel, quest, and recovery paths. Test actual telnet/webclient behavior,
  not a local mock of it.

**Gate:** launch regions pass content, connectivity, dialogue, prose, help, and
human playtest acceptance without contradicting authored world intent.

## 13. M6 — Release Candidate And Host-Together Readiness

### M6.1 Release candidate proof

On disposable PostgreSQL and a production-like Linux service environment:

1. migrate from empty and a restored copy;
2. compile, validate, plan, apply, verify, and idempotently reapply content;
3. inject content/economy/inventory/quest failure and prove rollback;
4. start/reload/restart twice with zero startup content mutation;
5. run canonical suite, Builder contract suite, golden player path, co-op path,
   Social path, content audits, and real protocol/webclient smoke checks;
6. build and test each Builder desktop package independently; and
7. capture release artifacts, versions, hashes, known limitations, backups, and
   rollback instructions.

### M6.2 Hosting handoff — deliberately interactive

Only after M6 passes, Cole and the agent decide together:

- hosting provider and region;
- domain, DNS, TLS, mail/monitoring, cost budget, and data-retention policy;
- managed PostgreSQL/backups, secrets storage, firewall, reverse proxy, and
  access/admin workflow;
- staging-to-production rollout window and invite/playtest cohort.

This plan does not create an account, buy a domain, deploy a server, expose a
port, or move player data without Cole's explicit approval at that time.

**Gate:** Cole accepts a staging checklist, performs/observes a live smoke
playtest, and explicitly approves production rollout.

## 14. C1 — Player Client After Hosting

The client phase starts only after hosted MUD contracts and player feedback are
stable. Its first plan will inventory protocol/OOB messages, auth/session flow,
accessibility, responsive webclient gaps, telemetry/privacy, and the highest
friction observed in real play. It will not force a client-driven rewrite of
MUD truth or Builder contracts.

## 15. Hourly Autonomous Execution Rules

Each scheduled run must:

1. read this plan, `AGENTS.md`, `CLAUDE.md`, and the latest relevant Engram
   handoff;
2. inspect both worktrees and avoid unrelated user changes;
3. select the smallest unblocked slice in program order, or report the true
   blocker instead of guessing;
4. follow red -> green -> focused integration -> appropriate runtime/package
   proof;
5. update this plan only when phase truth changes;
6. commit a clean scoped boundary when it owns only its changed files; and
7. write an Engram handoff with decision, validation, commit, and next slice.

The automation must never deploy, host, buy services, access production data,
or establish a direct Builder-to-MUD connection. It pauses for Cole when a
choice would materially affect product direction, cost, external authority,
or world canon.

## 16. First Execution Queue

1. **M0.1:** build the evidence scorecard and classify legacy plans against
   current commits/tests without touching user work.
2. **M2.3/B1.1 contract spike:** write a failing server/Builder source-call
   preservation test for `social_node`/`social_edge`; make unknown `area.*`
   calls fail loudly before adding any Builder UI affordance.
3. **B1.2:** unify Builder save semantics and close local dev capability gaps.
4. **B1.3:** add reproducible sidecar build/test commands and package smoke
   coverage.
5. **B2.0/B2.1:** record the Builder UI foundation and information architecture;
   then begin the App/store decomposition behind behavior-preserving tests.
6. **M1/M2 release foundations:** continue only after the current worktree
   classification identifies the next unproven release gate and safe ownership
   boundary.

The ordering is intentional: we first prevent an offline authoring tool from
destroying Social World content, then make both content and runtime safe to
ship, then expand the authoring experience and player-facing loops.
