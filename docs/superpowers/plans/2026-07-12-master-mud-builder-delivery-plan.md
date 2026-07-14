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
| Builder save, packaging, and UI rebuild | B2 **active**; B1.3 native package certification is externally blocked; B1.2 **complete** | Builder commits through `895b72a` establish typed offline persistence, the target-aware packaging spine, and the active offline-workbench rebuild. Commit `de5595d` adds the read-only four-runner native package matrix. The repository now has an authorized Git remote, but hosted run `29305692460` was rejected before checkout on all four runners by the GitHub account payment/spending-limit gate. Exact clean-clone macOS ARM gates remain green; no other native target is claimed certified. This packaging gate is independent of Lightsail hosting and live-game uptime. | Resolve the existing GitHub account gate, then run the four native jobs before closing B1.3; continue B2 and hosting work independently. |
| Fresh-player, living-world integration, content quality, and release candidate | **M3 active** | M1 and M2 are complete, and B1.1 is green on the available macOS ARM package path. The compiled playable-connectivity audit now proves every launch zone reachable from a real fresh start through directed walking, reachable quest rewards, destination discovery, and the authored courier graph. Courier Manifest teaches both Tremen and Korahei; a long-haul Varath Prime–Korahei route connects the island cluster without moving the player or weakening origin-presence checks. Authored HP and effective-stat ancestry traits now run idempotently through the shared derived-stat path, and the conflicting dead additive table is gone. The selected 60–90 minute opening is calibrated to four real, one-shot Vael/Ashreach Naturalism interactions: the database-backed practice/session path reaches exactly Practiced, unlocks only Verdance eligibility, and replay adds nothing. Practice now records one typed, idempotent database event for its domain and skill awards; sub-threshold skill-use remainders are durable, event acknowledgement is atomic with both growth paths, and a forced mixed-write failure proves Evennia's live Attribute cache is repaired before exact retry. Practiced now creates a durable, one-time invitation with an authored NPC and hall; `joinguild` is route-only, `talk` reconstructs the local offer, and `accept <secondary_domain>` completes an idempotent induction at that exact contact. Membership, Social Web induction evidence, domain resource, and abilities commit only after the local scene; the retired remote mutation helpers fail closed. The database-backed live-content golden path now starts through authored spawn placement, issues and equips a canonical damaging weapon and protective armor, traverses every leg through real exits, executes the four live dynamic practice commands, walks back to Elwen, and completes `talk`/`accept` induction without debug teleportation. Actual 60–90 minute elapsed-time acceptance remains a human playtest gate. Non-processing crafted outputs now resolve through isolated canonical templates and alter only the recipe's declared live mechanic: damage, armor, or numeric consumable effect; invalid or non-mechanical quality declarations fail closed, and crafted provenance names the actual recipe. Consumables now validate the real Evennia mapping wrapper, refuse unknown or context-only effects without wasting items or combat actions, apply regeneration and poison cures through the canonical status engine, roll volatile effects back when durable ownership changes fail, and decrement one quantity from a real stack rather than deleting it. Every sold catalog tool now starts at its authored maximum durability, loses durability on real gathering, and repairs only through an owned workbench transaction that charges the declared Scales cost; insufficient funds and injected mixed-write failure preserve both tool and currency state. Processing quality now uses the quantity-weighted quality of the whole consumed batch, prevents a single premium unit from laundering poor inputs, and never downgrades the batch below its earned raw quality. All 93 registered materials now have exactly one deterministic processing path. First-hand gathering discovers non-default regional recipes; ore, herbs, wood, fish, and hide enter the authoritative material/inventory/vendor contract; authored zone properties and profession bonuses persist through processing; only the named profession receives its bonus; properties create a durable trade-value premium; and malformed material affordances fail compilation. Fishing consumes one unit from a bait stack and repairs node/bait cache state on transactional failure. Typed durable progression now reaches all seven declared sources: practice; first mastery of each material and recipe; authored quest skill outcomes; courier-landmark discovery; novel search discoveries; and one-time named or legendary combat victories. Repetition of ordinary kills, gathers, crafts, searches, or landmarks cannot duplicate an event; hidden Remnance growth stays closed until the deliberate story-visibility gate; quest payout and crafting rollback remove their progression events atomically; and player quest/reward copy is qualitative rather than numeric XP. The actual timed opening playtest, combined Social/co-op, launch-content, and twice-clean release gates remain open. B1.3's full macOS Intel/Windows/Linux native matrix remains externally unavailable because the authorized hosted run is blocked before checkout by the GitHub account payment/spending-limit gate. | Build one database-backed two-player M4 vertical that combines group combat, personal rewards, authored quest consequence, faction/world state, and Social Web without direct state seeding. |
| M4 living-world closeout (supersedes the earlier open combined Social/co-op clause) | **automated gate complete** | `8a2d71e`, `3e60386`, `9a07e3c`, `0b27f9a`, and `3909cc4` establish shared frozen quest runs, canonical faction identity/scale, exactly-once relationship effects, and reachable authored node activation. `tests/test_m4_living_world_vertical.py` now composes a real two-player group, explicit quest sharing, allied tactical synergy, nearby kill credit, independent quest and encounter rewards, Consortium standing, hidden Reputation, and per-player Social facts from live authored Cellar Menace input. The affected M4/Social/compiler gate passes 204 tests without direct relationship or Social service seeding. M3's actual 60–90 minute human timing acceptance remains separately open. | Begin M5 with the proven stale Korahei/Tremen `area.vendor(...)` contract scanners, then continue dialogue/help/content and human playtest quality gates. |
| M3/M5 status correction (supersedes the broad M3 row above) | **M3 automated complete, human timing pending; M5 automated gate complete, human acceptance pending** | The content, dialogue, help, and gathering contract group passes 120 tests, and the compiled connectivity audit reaches all 2,193 rooms from `vaels_crossing:hg_arrival`. Commit `78edd6f` adds fail-closed isolated playtest settings, real Telnet/HTTP/RFC6455 Evennia WebSocket smoke, a stock-webclient OOB bridge, and a fresh-player/co-op/Social/crafting/travel/quest/recovery/living-world human acceptance guide. A literal browser run created a real account and character, selected ancestry, received structured inventory/map/stat/status state, and emitted no unhandled OOB events. Commit `c1dcc82` removes the staff-only MudInfo channel from player defaults; real browser account creation then logged no channel-connect error. A user-authorized July 11 Taildrop snapshot (`Obsidian.zip`, SHA-256 `b1bd1017f5b640cf71679a2b3aa11de60c398bed786721b59957ffcbe8e80520`) supplied point-in-time canon authority for the sensitive rewrites. The prose chain through `f8d328f` rewrites all ten flagged zones while preserving literal AreaBuilder semantics; `python scripts/audit_content_prose.py` now reports zero scaffold or repeated-room findings, the 84-test prose/compiler/content-contract/area-validator gate passes, and the external Builder parser accepts the final 100-room Colonist Ruins source with zero errors. The snapshot is not continuous vault access, and actual 60–90 minute elapsed-time acceptance remains a human gate. | Run the broader M6 candidate against the now-green prose gate, then perform the observed 60–90 minute acceptance guide before claiming full M5/M6 completion. |
| M6 PostgreSQL and lifecycle rehearsal (supersedes the earlier pending infrastructure clause) | **automated infrastructure proof green; full M6 blocked before candidate completion** | Commits `7e1b447`, `304d89a`, `fee2e77`, `b40bd74`, `70a8b91`, `4e33df5`, `d8ef5a3`, and `4afa973` establish the disposable PostgreSQL content rehearsal, composed candidate verifier, durable evidence contract, explicit rollback injection, exact-checkout and Git-object gates, and row-level startup-write instrumentation. Commit `3140a55` fixes the real Linux failure: all 427 persistent mob spawn slots now materialize under the atomic content revision instead of first boot, preserve stable room/template identity through apply and rollback, and retire only proven slot-owned mobs. Two independently created PostgreSQL 16 databases on Ubuntu 24.04/Python 3.12/Evennia 6.1 now prove `uninitialized -> initialized -> no-op -> current`; two distinct `pg_dump -Fc` artifacts restore to `current -> no-op -> no-op` with exact manifest `2eb6243d8e6224d963f88353285c7109b877603c33602aabccf9f5a3a608f3e3`. Run 1 records zero authored-content writes on cold start, reload, and two restarts; run 2 records zero on cold start, reload, and restart. Forced whole-unit SIGKILL recovery, clean stop with zero listeners, enabled-VM reboot recovery, all five intended listeners, preserved Portal on reload, and real Telnet/stock-webclient/RFC6455 round trips pass. Commit `8dc1825` models the trusted forwarded-HTTPS proxy contract so production's secure redirect is tested rather than bypassed. The composed 16-step candidate passes Git integrity, prepared content, hygiene, owned migration drift, deploy checks, imports, reconciliation, and all 2,193-room connectivity, then fails exactly at the 1,262 prose findings. No full candidate pass, Builder four-platform matrix, or human acceptance is claimed. | Resolve the live-vault canon gate and prose findings, obtain a Builder remote for the four native packages, perform observed timed/co-op/living-world acceptance, then run and retain two completely green candidate outputs and validate the final release-evidence record. |
| M6 final automated-candidate correction (supersedes the M6 row above) | **automated twice-clean candidate complete; external acceptance and final-evidence gates pending** | The canon-backed prose chain through `f8d328f` clears all 1,262 findings. Commits `58bb236`, `267ba69`, and `d4e27f2` preserve a least-privilege application role with no `CREATEDB`, reset only explicitly named disposable test databases, and seed an unusable-password test admin plus Evennia Objects `#1`/`#2` before each independent test phase. Commit `a6d3ac7` isolates the two canonical unit tests that leaked MagicMock identities into real persistence. At exact clean commit `a6d3ac7c6e354487c2141df8530cc220621a5eb4`, independently created `soravelon_rehearsal_run1_candidate` and `soravelon_rehearsal_run2_candidate` both prove `uninitialized -> initialized -> no-op -> current`, revision 1, identical manifest `b1f1ceb5813c38c9a3071b56e0f23d6dbde224aa0d11a1f439f63fd561598e0b`. Both composed 16-step candidates pass Git integrity, prepared-content no-ops, hygiene, owned migration drift, deployment checks, imports, reconciliation, 2,193-room connectivity, zero prose findings, four rollback injections, all nine release gameplay verticals, all 2,161 canonical tests, and real Telnet/forwarded-HTTPS stock-webclient/RFC6455 WebSocket round trips. Run 1's canonical suite completes in 2,833.852 seconds and run 2's in 1,669.259 seconds on Ubuntu 24.04 ARM64, Python 3.12.3, PostgreSQL 16.14, and Evennia 6.1.0. The Builder macOS Intel/Windows/Linux native matrix, observed 60–90 minute/co-op/living-world human acceptance, candidate-output artifact hashes, and validated final release-evidence record are not claimed. | Complete the requested audit/remediation pass. If it changes the candidate, rerun the twice-clean gate at the new SHA. Then obtain the Builder remote/native matrix and observed human acceptance before validating the final evidence record or entering the hosting handoff. |
| M6 final audit correction (supersedes the automated-candidate row above) | **automated audit and twice-clean candidate complete at the audited SHA; external gates pending** | The code-health, security, gameplay, UX/accessibility, and reliability audits produced scoped remediations through `c525d90437860964ed32d42a6c09571ca9507c86`. The first post-audit candidate correctly exposed ten public-surface tests sending HTTP into the secure production profile; `c525d90` makes those requests use forwarded HTTPS without weakening the redirect. On Ubuntu 24.04 ARM64, Python 3.12.3, PostgreSQL 16.14, Django 6.0.7, and Evennia 6.1.0, independently created `soravelon_rehearsal_audit1_candidate` and `soravelon_rehearsal_audit2_candidate` both prove `uninitialized -> initialized -> no-op -> current`, revision 1, with identical manifest `b1f1ceb5813c38c9a3071b56e0f23d6dbde224aa0d11a1f439f63fd561598e0b`. Both composed 16-step candidates pass all nine release gameplay verticals, all 2,185 canonical tests, and real Telnet/forwarded-HTTPS stock-webclient/RFC6455 WebSocket round trips. The canonical suites complete in 1,457.275 and 1,924.080 seconds. Candidate logs hash to `f9d70507446e65d0ea5fd855ff8bced39ec241d533479f7be5cb1042a24dfebf` and `47c4068d28f1ccba3e3c4d21de2628855d24fa053f0a66b2a2858b82c7dafd90`. Builder native macOS Intel/Windows/Linux CI, observed 60–90 minute/co-op/living-world/accessibility acceptance, and the complete final release-evidence record remain unclaimed. | Obtain explicit Builder remote/CI authority and run the remaining native jobs; perform the observed human acceptance; then validate the complete release-evidence record. Only after those gates pass may the program enter the interactive hosting handoff. |
| M6 retained-evidence correction (supersedes the final-audit row above) | **automated M6 evidence complete and retained at the evidence-integrity SHA; external gates pending** | Commit `27cbb176e9fdc59837f3d9326d586e17ca16d959` makes the release-evidence validator prove retained artifact existence, root containment, byte hashes, generic artifact sizes, exact Builder identity/contract/CI provenance, exact human-acceptance provenance, and retained content/lifecycle receipts. Two independent PostgreSQL rehearsals, `soravelon_rehearsal_evidence1_*` and `soravelon_rehearsal_evidence2_*`, each prove fresh `uninitialized -> initialized -> no-op -> current`, independently restored `current -> no-op -> no-op`, revision 1, and manifest `b1f1ceb5813c38c9a3071b56e0f23d6dbde224aa0d11a1f439f63fd561598e0b`. Their `pg_dump -Fc` backups hash to `934a2554e0eb793e9f092b0f4ca110b8ecabcc5a154458187fd09b0841f76383` and `6cb49b2daec45e9bba7b17fc9b260b5472488fd1dcae212ee5c1fdb2b5134385`; independently restored candidate databases pass cold start, explicit whole-cgroup SIGKILL recovery, Portal-preserving reload, zero-listener stop, restart, enabled-VM reboot recovery, and zero startup content writes, with lifecycle receipts `74061f11638f385f32c72f2505cb5befa2fd3b04eb506856ccdc9d20965554d6` and `b2eed1fc1ed2216ad9cf85c6d9a8a184e8509a37d9d91f494240ee25aa5c3903`. Both composed 16-step candidates pass all rollback injections, all nine release gameplay verticals, all 2,189 canonical tests in 1,925.538 and 1,435.694 seconds, and real Telnet/forwarded-HTTPS webclient/RFC6455 WebSocket round trips. Candidate logs hash to `39028509ab539aed44ec2decadb11a33cf02750b18c68149c4df3d7325644520` and `cb954ad0a99133c5ba790a1847d87ac64e4aafb341d54c9e23308273b194c972`; all ten automated artifacts are retained in the local release bundle outside Git. The Builder four-platform native CI/packages and observed 60–90 minute/co-op/living-world/accessibility acceptance are still unclaimed, so the final record remains deliberately red and production hosting is not yet authorized by evidence. | Obtain explicit Builder remote/CI authority and all four native package artifacts; perform the observed human acceptance against this exact MUD SHA; then assemble and pass the artifact-backed final record before any hosting cutover. |
| B1.3 CI execution correction (supersedes the stale no-remote clauses above) | **active; exact-final-SHA matrix blocked by GitHub billing authority** | Builder PR `ckwich/Sora_builder#1` and branch `codex/content-contract-hardening` now provide remote CI authority. At `d43dfa437955fa6787a2365c60580164a1fff5ca`, run `29299980867` completes macOS ARM64, macOS Intel, and Linux x64 packages and proves the full Windows test gate plus Windows NSIS bundle build. The remaining Windows step exposed a verifier defect rather than an invalid package: it read only 256 bytes and rejected a valid PyInstaller PE whose header began later. Commit `61873538cba08b021553a6ca8adcbca88a22b71d` reads the PE offset from the DOS header and seeks to the real signature; its focused 20-test release/build gate passes, and a clean disposable exact-SHA checkout passes the production frontend build, 48 frontend tests, 69 sidecar tests with 16 platform skips, 14 Rust tests, and `npm audit` with zero vulnerabilities. Exact-SHA run `29300591454` was rejected before checkout on every runner with GitHub's account-payment/spending-limit annotation, so no package at `6187353` is claimed and B1.3 remains open. | Cole must resolve GitHub Billing & plans or explicitly authorize a spending cap; then rerun all four jobs at exact SHA `6187353`, retain every package/manifest outside Git, and validate hashes and contract provenance. |
| Production hosting correction (explicit user override of the earlier gate order) | **single-instance production infrastructure live and stable; final release evidence and human acceptance still open** | Cole explicitly authorized production deployment and one existing USD 12/month Lightsail instance, while prohibiting additional instances or purchases without authorization. The only instance is Ubuntu 24.04 x86_64 in Oregon with a static IP, PostgreSQL 16, Python 3.12, Nginx, Certbot, UFW, unattended upgrades, and a 2 GB swap file. Soravelon is deployed from clean exact SHA `3f928e100a15cd865fc0eda45f5cb1248c090d44`; `systemd` is active with public Telnet `4000` plus loopback web `4001`, WebSocket `4002`, and AMP `4005`. Cloudflare routes apex and `www` to the static IP, `ws` to the WebSocket proxy, and DNS-only `telnet` to the instance; Full (strict) TLS is enabled and the origin certificate covers apex, `www`, and `ws`. Content revision 1 is current across all 20 zones at manifest `b1f1ceb5813c38c9a3071b56e0f23d6dbde224aa0d11a1f439f63fd561598e0b`. Public admin authentication, Telnet, HTTPS stock webclient/OOB, and WSS smokes pass; the clean exact-SHA canonical suite passes 2,189 tests with 5 skips. The bootstrap backup `/var/backups/soravelon/soravelon-bootstrap-2d39d7d-20260714.dump` is 3,432,109 bytes with SHA-256 `04313f3e9e94f9447119e80290ac7e6e75a4b3bb25a555b7ffd21453b5488920`. A later read-only check again proved the clean exact SHA, active service, intended listeners, apex/`www` HTTP 200, and no recent traceback, critical, or failed service log entry. This does not retroactively complete the artifact-backed M6 record: its retained candidate is `27cbb17`, the exact-final-SHA Builder matrix is blocked as described above, and Cole deferred the observed 60–90 minute/co-op/living-world/accessibility playtest. | Do not create another instance or paid resource. Resolve the GitHub billing gate and retain the exact-SHA Builder matrix; perform the deferred observed acceptance; reconcile final evidence without fabricating cross-SHA proof. Do not start C1. |
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

### B2 execution status — 2026-07-13

**Status:** active. Builder commits `3f5fcba`, `b4209b3`, `9fff200`,
`ac46bdf`, `258b215`, `343715f`, `09afc3f`, `8785ce1`, `bce55a8`,
`af60e2c`, `2f6f839`, `b5aaa41`, `558b0d9`, `92c13fb`, `48efe06`,
`287dafb`, `2aeca28`, `a44f744`, `4a40d02`, and `895b72a`
establish the first truthful vertical slice of the rebuild. With no area open,
the application now presents an explicit offline local-workspace home for area
roots, recent/local files, new areas, world overview, and the local template
library; the area explorer, inspector, and Problems action do not appear until
an area document is active. `CLAUDE.md` now matches the explicit versioned
compiler/materializer contract and no longer describes startup rebuilds.

Home is now a real workspace route rather than an empty-map inference. An
author can keep an area open, press `Ctrl+0` to return to a rail-free Home, and
resume the same local document through the explicit `Resume Map & exits`
action; closing the document returns to Home and area-only routes fail closed
when no area is loaded. World and template tools remain explicit local
documents rather than competing area tabs.

Review is now one explicit area-workbench route instead of a semantic Diff tab
competing with a separate right-rail Problems tab. `Ctrl+3`, the workbench tab,
the header action, and save-blocking validation all enter the same full-width
local Review surface. It reads the existing zone/world validation stores and
saved model snapshot, shows current save state, keeps the contextual right rail
inspector-only, and removes the unused legacy `ValidationDrawer`; it does not
introduce another validator, serializer, save path, or MUD connection.

Content is now an explicit `Ctrl+2` area-workbench route over the active local
`ZoneModel`. Its searchable structured lists group characters, rewards and
resources, and world systems; selecting a row routes the real entity into the
existing Inspector forms. Creation remains in the Navigator and grammar,
reference validation, serialization, and persistence remain owned by the
existing data and store services. The workbench adds no alternate schema,
write path, server authority, or direct Builder-to-MUD connection.

Narrative is now one explicit `Ctrl+4` area-workbench route instead of a
top-level Descriptions tab plus a disconnected Dialogue route. Searchable
groups project quests, lore fragments, triggers, custom commands, practice
opportunities, and NPC conversations into their existing Inspector or focused
editor. Room descriptions still use the established virtualized bulk editor;
NPC conversations still use the established dialogue canvas and store. Both
focused editors return to Narrative, and no alternate quest, dialogue,
validation, or persistence authority was introduced.

Social is now the fifth explicit area-workbench mode at `Ctrl+5`. It projects
the literal parsed `social_nodes` and `social_edges` into searchable Nodes and
Connections groups and routes selection into the existing Social Node and
Social Edge Inspector panels. Endpoint coverage distinguishes local references
from external-or-unresolved references without declaring either valid; the
existing validator remains the authority. The workbench describes Social Web
truth as local trust, rumor, and subjective knowledge routing rather than a
global morality score, and does not simulate runtime propagation or connect to
the MUD. World and template local-document shortcuts move to `Ctrl+6` and
`Ctrl+7` respectively.

The live browser gate at compact and wide desktop widths transitions from Home
into real 108-room and 221-exit area workbenches, returns to Home without
discarding the active area, and resumes Map & exits with zero console errors or
warnings. Same-zone layout writes are
serialized through the typed IPC client, preventing overlapping atomic
transactions during first-layout creation. Cross-area ghost nodes expose the
same directional target-handle contract used by exit edges; the reproduced
Ashreach load moved from two layout errors and twenty repeated edge warnings to
zero browser errors and zero warnings. The `9fff200` clean-checkout gate passed
the production frontend build, 52 frontend tests, 69 sidecar tests with 16
platform skips, 14 Rust tests, and `npm audit` with zero vulnerabilities. At
exact `ac46bdf`, the changed frontend source matches the committed diff and
passes the production build, all 54 frontend tests, and `npm audit` with zero
vulnerabilities. At exact `258b215`, the changed frontend source passes the
production build, all 58 frontend tests, and `npm audit` with zero
vulnerabilities. The 1440x900 and 900x700 browser gates open Review from both
Map and the header, preserve compact access to semantic changes, and report
zero console errors or warnings. At exact `343715f`, the staged source matched
a clean clone byte-for-byte and passed the production build, all 60 frontend
tests, and `npm audit` with zero vulnerabilities. A live Vael's Crossing pass
projected 88 entries across all three Content groups; searching for the
quartermaster produced one result and opened the existing NPC Inspector. Wide
1440x900 and compact 900x700-with-Navigator-collapsed passes had no horizontal
overflow and reported zero console errors or warnings. The sidecar and Rust
sources are unchanged from `9fff200`. At exact `09afc3f`, the staged source
again matched a clean clone byte-for-byte and passed the production build, all
62 frontend tests, and `npm audit` with zero vulnerabilities. A live Vael's
Crossing pass projected 85 Narrative entries; quest search opened the real
Quest Inspector, the room-description entry opened all 108 rooms in the
existing virtualized editor, and NPC search opened the real dialogue canvas
with Topic and Greeting Tier controls. Both focused editors returned to
Narrative. Wide and compact-with-Navigator-collapsed passes had no horizontal
overflow and zero browser errors or warnings.

At exact `8785ce1`, the staged source matched a clean clone byte-for-byte and
passed the production build, all 64 frontend tests, and `npm audit` with zero
vulnerabilities. A live Vael's Crossing pass projected five Social nodes and
two connections, identified one external-or-unresolved endpoint reference,
opened the real Social Edge Inspector for `warden_report`, and opened the real
Social Node Inspector for Agent Calloway. Wide and compact passes with the
Navigator collapsed had no horizontal overflow and zero browser errors or
warnings.

At exact `bce55a8`, recovery is keyed by the authorized authored `.py` source
through typed browser and native commands. Auto-save derives and validates the
exact `.py.tmp` sibling, repeated recovery saves preserve a recovery backup,
and successful authored saves or explicit discard remove obsolete recovery
artifacts without touching the source or its backup. Recovering keeps the
authored source snapshot and file identity, marks the recovered model dirty,
and retains the recovery file until the author saves or discards it. A live
Vael's Crossing pass changed Social content, waited through auto-save, proved
the source hash stayed unchanged, reloaded and recovered the edit, showed the
recovered semantic change as unsaved, and then discarded only recovery
artifacts with zero browser errors or warnings. The exact clean-clone gate
passed the production build, 71 frontend tests, 69 sidecar tests with 16
platform skips, 15 Rust tests, and both dependency audits with zero
vulnerabilities.

At exact `af60e2c`, Review compares the saved local model with every authored
collection rather than rooms alone. It covers area metadata, rooms, exits,
spawns, mobs, NPCs and dialogue, quests, nodes, lore, materials, gathering,
flight, triggers, custom commands, practice, patrols, items, loot, and Social
nodes and connections; stable semantic identities prevent collection
reordering from appearing as authored change. The exact staged source matched
a clean clone byte-for-byte and passed the production build, all 74 frontend
tests, and both dependency audits with zero vulnerabilities. Sidecar and Rust
sources are unchanged from `bce55a8`.

At exact `2f6f839`, Review adds an on-demand exact source preview backed by the
same typed Python serializer used by save. It has explicit idle, loading,
failure, current, and stale-result states, exposes the generated source as a
keyboard-focusable labelled region, and neither writes a file nor introduces a
network or MUD authority path. A live Vael's Crossing pass generated the full
literal AreaBuilder output, including Social content, at wide and 900x700
desktop widths with no document-level horizontal overflow and zero browser
errors or warnings. The authored source remained unchanged and the test
recovery sibling was explicitly discarded. The exact staged diff matched a
clean clone byte-for-byte and passed the production build, all 75 frontend
tests, and both Node dependency audit scopes with zero vulnerabilities.

At exact `b5aaa41`, the header, compact status bar, and Review derive their
local-save presentation from one shared model and no longer describe a saved
recovery sibling as a saved authored file. Dirty recovery success explicitly
states that the recovery copy is saved while the authored file remains
unsaved; recovery failure is assertive for assistive technology; and a clean
document is described as matching its last safe save. A live Vael's Crossing
Social edit passed through the real 30-second recovery timer: both full-width
surfaces and the compact status remained truthful during recovery success,
Review still exposed the semantic edit, the authored source hash remained
unchanged, the 900x700 document had no horizontal overflow, and the browser
reported zero errors or warnings. The recovery sibling was then discarded
through the typed endpoint. The exact staged diff matched a clean clone
byte-for-byte and passed the production build, all 82 frontend tests, and both
Node dependency audit scopes with zero vulnerabilities. Sidecar and Rust
sources are unchanged from `bce55a8`.

At exact `558b0d9`, the existing authorized recovery inspection contract now
reports real paths and modified times for the authored source, authored
transaction backup, current recovery copy, and previous recovery copy in both
browser development and native Tauri paths. Review exposes those facts in one
read-only provenance panel that refreshes when the recovery state changes and
explicitly cannot write, restore, or publish files. A live 900x700 Vael's
Crossing pass first showed the last-safe authored timestamp and the truthful
absence of all transaction siblings, then refreshed after one real recovery
write to the exact `.py.tmp` path and after the second recovery transaction to
the exact `.py.tmp.bak` path. The semantic edit stayed visible, the authored
source hash stayed unchanged, there was no document-level horizontal overflow,
and the browser reported zero errors or warnings. Both recovery artifacts were
then discarded through the typed endpoint. The exact staged diff matched a
clean clone byte-for-byte and passed the production build, all 84 frontend
tests, 69 sidecar tests with 16 platform skips, all 16 Rust tests, Rust format,
and both Node dependency audit scopes with zero vulnerabilities.

At exact `92c13fb`, World Overview runs one read-only batch check over every
authorized non-private `.py` candidate instead of silently inheriting the
normal file browser's supported-only filter. A separate typed browser/native
candidate command retains unsupported files with their exact sidecar
inspection failure, excludes symlinks on both paths, and does not change
ordinary file browsing. Supported candidates pass through the existing parser
and validator, partial parse or validator failures remain attached to their
file, and parsed zones continue into the existing cross-zone authority. The
result panel separates file-level errors and warnings, unsupported/failed
files, and world-link findings; it can rerun locally and explicitly does not
save files or connect to the MUD. In the live 900x700 workspace, all 21 local
candidates were accounted for: the 20 canonical areas passed parse and local
validation, the unrelated dirty `vaels_crossing 2.py` remained visible as one
unsupported file with its exact player-stock round-trip-contract reason, and
the existing 11 world-link findings remained separate. All browser resources
used the local `127.0.0.1` origin, the document had no horizontal overflow, and
the browser reported zero errors or warnings. The exact staged diff matched a
clean clone byte-for-byte and passed the production build, all 90 frontend
tests, 69 sidecar tests with 16 platform skips, all 17 Rust tests, Rust format,
and both Node dependency audit scopes with zero vulnerabilities.

At exact `48efe06`, the reusable-creature Template Library is an explicit
offline local document rather than a template-shaped view leaking area state.
It owns its file identity, supported mob-template grammar label, clean/dirty
state, primary save action, compact status, browser-exit protection, and
replacement guard. Opening another library while dirty now requires an
accessible Save and Open, Discard and Open, or Cancel decision. `Ctrl+S` routes
to the active template document's existing typed atomic transaction, while
area Save As cannot fire from Home, World, or the library. A completed write
updates the serializer source baseline without erasing edits made while that
write was in flight. Header and status surfaces no longer expose a background
area's Review/save controls while a local library or read-only World Overview
is active. The compact catalog uses one real scroll region, and registered
template fields no longer change uncontrolled defaults after initialization.

In a disposable Soravelon clone at 900x700, the real 81-template library opened
from Home, the first row remained genuinely clickable, an HP edit changed only
the template document to dirty, a second open request displayed the guarded
decision, and real `Ctrl+S` produced a new parseable source plus an exact backup
of the prior file before returning all save surfaces to clean. Home preserved
and resumed that loaded library; a 1440x900 pass remained clean. Both widths
had no document-level horizontal overflow, every browser resource stayed on
the local `127.0.0.1` origin, and the browser reported zero errors or warnings.
The exact staged diff SHA
`f0b3ca5bb619c6d42392a076e6579ec8087b5123df74c21e76d6c72e2965d5b0`
matched the clean clone byte-for-byte and passed the production build, all 100
frontend tests, 69 sidecar tests with 16 platform skips, all 17 Rust tests,
Rust format, and both Node dependency audit scopes with zero vulnerabilities.

At exact `287dafb`, the Template Library's file identity, source baseline,
dirty lifecycle, selection, and mutations live in a dedicated
`templateLibraryStore`; the area-focused `editorStore` no longer owns or
mirrors that document state. Every production consumer routes directly to the
new authority, and the save-in-flight identity guard remains intact. The live
gate also caught a pre-existing form-boundary defect: numeric inputs were
entering the store as strings. Template form fields now pass through their
real schema before mutation, which converts valid numeric input to numbers and
rejects malformed or out-of-range values instead of serializing incorrect
gameplay types.

In a fresh disposable Soravelon clone at 900x700, the real 81-template library
opened from Home, `hp_max` changed from 250 to 251, `Ctrl+S` completed the
typed atomic transaction, and an AST read proved the persisted value was the
integer `251`, not a string. The transaction backup SHA exactly matched the
pre-save source, no temp candidate remained, all save surfaces returned to
clean, every browser resource stayed on local `127.0.0.1`, and the browser
reported no console warnings or page errors. The exact staged diff SHA
`0a6e4a40484388c6cf37a2fdb743eae2336edce3e6efe2d07e580124a1957374`
matched the clean clone byte-for-byte and passed the production build, all 103
frontend tests, 69 sidecar tests with 16 platform skips, all 17 Rust tests,
Rust format, and both Node dependency audit scopes with zero vulnerabilities.

At exact `2aeca28`, the versioned reference bundle, persisted
owner/contributor mode, and ten-entry recent-file history live in a dedicated
`editorContextStore` rather than the temporal area model/history store. All
production consumers route directly to the new authority; no compatibility
facade or duplicate state remains. Zone content, selection, validation,
navigation, save state, and history deliberately remain in `editorStore`.
Focused boundary tests prove startup rehydration, reference loading, mode
persistence, recent-file de-duplication and bounds, and the absence of all
three context fields from the area store.

In a fresh disposable Soravelon clone at 900x700, opening the real
`vaels_crossing.py` recorded its exact local path as the first recent file.
Changing Owner to Contributor updated the live status, persisted to browser
storage, and survived a full reload alongside the recent-file entry. The
Contributor Template route still received the bundled read-only reference
catalog. The document had no horizontal overflow, every resource stayed on
local `127.0.0.1`, and the browser reported no console warnings or page errors.
The exact staged diff SHA
`aa8c21b331aadd512ec71516db6aa23943666881312894f0e958a216723294e0`
matched the clean clone byte-for-byte and passed the production build, all 106
frontend tests, 69 sidecar tests with 16 platform skips, all 17 Rust tests,
Rust format, and both Node dependency audit scopes with zero vulnerabilities.

At exact `a44f744`, local area validation results and their update action live
in a dedicated `areaValidationStore` rather than zone mutation/history. App
save validation, World Overview's reverse-exit save workflow, Problems, and
Review all route to that authority. Cross-zone findings deliberately remain in
`worldMapStore`; zone model, save snapshot, navigation, selection, and temporal
history remain in `editorStore`. Boundary tests prove validation ownership and
the absence of both validation state and action from the area editor store.

In a fresh disposable Soravelon clone at 900x700, World Overview scanned all
20 canonical local areas and produced 11 existing world-link warnings. Opening
Vael's Crossing from that graph and entering Review reported `Current Area 0`
and `World 11` as distinct issue sources while the area still matched its last
saved snapshot. The document had no horizontal overflow, every resource stayed
on local `127.0.0.1`, and the browser reported no console warnings or page
errors. The exact staged diff SHA
`3770cd7a5db8a9abb297d295505ae4bcb6852bf9e40043bad13380900f75f1dc`
matched the clean clone byte-for-byte and passed the production build, all 108
frontend tests, 69 sidecar tests with 16 platform skips, all 17 Rust tests,
Rust format, and both Node dependency audit scopes with zero vulnerabilities.

At exact `4a40d02`, `selectionStore` is the sole active selection authority.
The app coordinator, map, outline, command palette, workbenches, inspector,
world navigation, and map projection all consume its typed interface directly;
`editorStore` no longer owns or exposes selection. Area create, delete, load,
clear, and room-rename actions synchronize the separate selection through one
typed dependency, so entity mutations do not leave a duplicated or stale
inspector target. Tests prove room-ID selection repair, creation in the selected
room, create-to-inspector handoff, deletion clearing, and the absence of
selection state/actions from area history.

In a fresh disposable Soravelon clone at 900x700, selecting the real
`hg_arrival` room opened its Inspector, adding an NPC created it in that room
and moved the Inspector to the new entity, and confirmed deletion removed the
temporary NPC and returned to the neutral Inspector. The authored source and
recovery siblings stayed unchanged. The document had no horizontal overflow,
every resource stayed on local `127.0.0.1`, and the browser reported no console
warnings or page errors. The exact staged diff SHA
`a86765f67d0ef6c3e22ce5690c87b540232a2cbc50363fc7db1d2100cd0c459f`
matched the clean clone byte-for-byte and passed the production build, all 110
frontend tests, 69 sidecar tests with 16 platform skips, all 17 Rust tests,
Rust format, and both Node dependency audit scopes with zero vulnerabilities.

At exact `895b72a`, `historyStore` owns the bounded, newest-first visible edit
ledger while zundo continues to own the real temporal `ZoneModel` snapshots.
The Navigator badge and History panel consume the new authority directly;
`editorStore` no longer exposes or mirrors ledger entries. Area load, recovery,
clear, new-document, and every typed content mutation clear or record through
the dedicated boundary. Tests prove the 50-entry bound, mutation labels,
load-time clearing, temporal restoration, and the absence of ledger state from
the area store.

The live gate exposed a pre-existing temporal-UI defect: zundo restored the
room model and outline, but the selected room Inspector retained stale
React Hook Form values because its reset gate watched only `room_id`. A focused
red-green repair now derives that gate from all room form values, so same-ID
undo and redo snapshots resynchronize the Inspector. In a fresh disposable
Soravelon clone at 1440x900, changing `hg_arrival` produced one visible named
history entry; `Ctrl+Z` restored both the outline and the Inspector input. The
authored source and recovery siblings remained unchanged, there was no
document-level horizontal overflow, and the browser reported no console or
page errors. Exact staged diff SHA
`86df3470c64f3d3b13218830f482dd2bff606441afc32b0a67e7a18b9e505af4`
matched the clean clone byte-for-byte and passed the production build, all 113
frontend tests, 69 sidecar tests with 16 platform skips, all 17 Rust tests,
Rust format, packaged ARM sidecar smoke, and both Node dependency audit scopes
with zero vulnerabilities.

This evidence does not complete B2. Further area document/session/content and
application-coordinator decomposition; the required
state/accessibility matrix;
screenshot/interaction coverage; and observed usability gates remain open.
Hosted run `29305692460` at exact Builder SHA
`bce55a8f7287ababd7925177fd75d645b43ad456`
was rejected before checkout on all four runners by the existing GitHub
payment/spending-limit gate. No hosted run exists for `af60e2c`, `2f6f839`,
`b5aaa41`, `558b0d9`, `92c13fb`, `48efe06`, `287dafb`, `2aeca28`, `a44f744`, `4a40d02`, or `895b72a`; their evidence is the exact
clean-clone gates above. GitHub Actions is required
only for the native package certification matrix, not for Lightsail hosting or
live-game uptime.

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

Current automated status: the artifact-backed twice-clean candidate proof is
green and retained at `27cbb176e9fdc59837f3d9326d586e17ca16d959`
with identical manifest
`b1f1ceb5813c38c9a3071b56e0f23d6dbde224aa0d11a1f439f63fd561598e0b` on two
independently created and restored PostgreSQL release paths. Both candidates
pass all 16 steps, all nine gameplay verticals, all 2,189 canonical tests, and
real Telnet, forwarded-HTTPS webclient, and RFC6455 WebSocket gates. Production
is separately live at `3f928e100a15cd865fc0eda45f5cb1248c090d44` by
Cole's explicit override of the earlier gate order. M6 remains open for the
exact-final-SHA Builder four-platform package matrix, observed human acceptance,
and a complete cross-SHA-reconciled evidence record.

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
