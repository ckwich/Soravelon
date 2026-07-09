# Soravelon Full Audit Remediation Plan

**Date:** 2026-07-09

**Repo:** `/Users/ckwichman/Documents/Projects/soravelon`

**Branch at plan creation:** `worktree-agent-abeed234-fix`

**Baseline:** `20d8cce`

**Execution mode:** test-driven, one system boundary per commit, selective staging in a dirty worktree

## Goal

Turn Soravelon from a broad, well-tested systems scaffold with broken end-to-end
contracts into a runtime whose security, deployment, world topology, progression,
equipment, crafting, co-op, world state, quests, dialogue, and Social Web are
truthful to the player-facing design.

This is not a polish pass. A finding is complete only when the real runtime path
works, its durable state is safe, the authored content uses it, player-facing
copy is truthful, and a test proves the actual contract.

## Baseline Evidence

- Canonical suite: `1720` tests passed in `1251.832s`.
- Focused Social Web suite: `205` tests passed in `45.581s`.
- Smoke imports passed.
- The local DB has only `world` migrations `0001` and `0002` applied.
- `makemigrations --check --dry-run` currently proposes six index renames and
  five `AutoField` to `BigAutoField` changes.
- Production `check --deploy` reports security warnings.
- The repository is public and tracks a local Django secret, runtime logs, and
  generated static output.
- Fresh world traversal has four disconnected walking components; flight
  discovery creates a circular access gate.
- The Social Web schema and compiler are substantial, but the local runtime is
  unmigrated and the showcased route is not physically traversable as authored.

## Binding Design Contracts

These decisions already exist in `AGENTS.md`, repo specs, and source-backed
Engram context. They are not reopened by this plan.

1. Progression is hidden and narrative. Players never see level or numeric
   domain XP.
2. Characters begin as Wanderers. Guilds approach at Practiced, and secondary
   domain choice occurs during an authored induction.
3. Open-world access uses routes, fiction, danger signals, and logistics—not
   level gates.
4. Inventory is weight-based. Equipment slots are real; inventory slots are not.
5. Equipment metadata must affect combat. Crafted and looted items must obey the
   same runtime contract.
6. Personal loot means independent player entitlements. Quest drops and Scales
   are personal regardless of ordinary loot mode.
7. Nodes and all five world-state dimensions are backbone systems.
8. `wardens` is the canonical faction relationship identifier. Singular
   `warden` remains valid only where it is prose or a non-faction enum.
9. Facts, claims, belief, provenance, and interpretation are distinct Social Web
   concepts. An LLM never owns truth or durable mutation.
10. AreaBuilder remains a literal, round-trippable authoring interface.

## Explicit Gates And Assumptions

### External incident actions

The repository can prevent recurrence, but these actions require the real
deployment/repository owner and must not be faked locally:

- rotate the production Django `SECRET_KEY` in the real secret store;
- restart production and invalidate signed sessions;
- run a redacted full-history secret scan;
- coordinate any public-history rewrite and force-push with collaborators;
- back up and restore-rehearse PostgreSQL before production migrations;
- verify TLS, DNS, reverse proxy, and systemd on the Linux host.

No public Git history rewrite or remote force-push is authorized by this plan.

### Missing narrative source

The required Windows-style Obsidian vault is not mounted on this Mac. Engram is
healthy and supplies design decisions, but it is not a substitute for the World
Bible when rewriting lore-bearing prose or inventing induction/node scenes.

All systems, schema, runtime, tests, validators, and source-backed content work
proceeds immediately. These commits wait for the vault:

- ten zone-wide prose rewrites;
- final guild induction scene prose and named contact selection;
- final Tremeneth/Veluana node manifestation prose and cadence tuning.

The temporary progression acceptance target is: one authored hub-to-outbound
quest line can make one fitting domain Practiced without grinding or exhausting
all one-shot practices. Final hours-to-Practiced tuning remains a playtest lock.

## Execution Discipline

For every numbered implementation slice:

1. Lock the symptom with the real deciding gate.
2. Write one focused failing test.
3. Run the narrow test and verify it fails for the intended reason.
4. Implement one coherent contract.
5. Re-run the same gate, then its surrounding suite.
6. Inspect the diff and stage only owned files.
7. Commit the green boundary.

Do not merge unrelated cleanup into a slice. Preserve existing dirty `.claude`,
`CLAUDE.md`, area backup, and user-owned changes unless a finding explicitly
requires ownership of that path.

## Phase 0 — Record The Program

### 0.1 Commit this plan

**Commit:** `docs: plan full audit remediation`

Proof:

- every audit finding maps to a task below;
- every task names a runtime contract and validation path;
- external and vault-dependent work is explicit rather than silently degraded.

## Phase 1 — Security, Configuration, Migrations, And Release Truth

### 1.1 Remove the committed secret and close the import override

**Commit:** `security: remove committed django secret`

RED:

- production environment `SECRET_KEY` cannot be overridden by a local module;
- missing production configuration fails closed;
- unknown `SORAVELON_ENV` fails closed;
- `git ls-files server/conf/secret_settings.py` is empty.

Implementation:

- delete the tracked secret file;
- load local secret settings only in development;
- never import them after production settings;
- keep a placeholder-only example file;
- add `tests/test_production_settings.py`.

### 1.2 Make production configuration fail closed

**Commit:** `security: harden production configuration`

RED:

- production requires PostgreSQL, allowed hosts, trusted HTTPS origins, and a
  real environment secret;
- secure cookies, proxy SSL, security middleware, frame policy, referrer policy,
  and content-type protection are active;
- enabled listener ports must be unique;
- dead local override imports cannot be silently ignored.

Implementation:

- harden `server/conf/production_settings.py`;
- standardize telnet `4000`, public web `4001`, WebSocket `4002`, optional SSL
  `4003`, optional SSH `4004`, internal web `4005`;
- remove misleading no-op SSH/SSL environment knobs or make enable flags real;
- correct `.env.example`;
- make reverse-proxy HTTPS mandatory for the authenticated webclient.

### 1.3 Stop tracking runtime/generated/private artifacts

**Commit:** `chore: stop tracking runtime artifacts`

Implementation:

- untrack runtime logs without deleting the developer's local copies;
- untrack generated `server/.static/` output and regenerate with collectstatic;
- repair ignore rules so tracked `AGENTS.md` and durable docs are intentional;
- keep local `.planning` material out of Git after promoting any unique binding
  decision into `docs/superpowers/`;
- never print secret contents during scans.

### 1.4 Replace the false hygiene check

**Commit:** `release: enforce repository hygiene`

RED:

`scripts/audit_repo_hygiene.py` must fail on tracked ignored files, local secret
settings, `.env`, runtime logs, collectstatic output, worktrees, databases,
temporary files, and area backups.

Add `tests/test_repo_hygiene.py` and document safe generated-file handling.

### 1.5 Resolve migration drift and the SQLite standing constraint

**Commit:** `db: reconcile world migrations`

RED:

- a migration-executor test preserves rows and relationships across the change;
- `makemigrations --check --dry-run` reports no changes;
- SQLite does not emit the current nullable uniqueness warning;
- PostgreSQL creates the intended constraints.

Implementation:

- give current indexes their historical explicit names;
- deliberately choose and migrate the five primary-key types;
- replace `nulls_distinct=False` with explicit conditional uniqueness that is
  truthful on both SQLite and PostgreSQL;
- coordinate one migration number across all remediation lanes.

Do not silently migrate the user's current DB. Rehearse fresh and copied
PostgreSQL first, then back up before local/staging application.

### 1.6 Add one executable release gate

**Commit:** `release: add executable verification`

Create `scripts/verify_release.py` and make CI use PostgreSQL 16. The gate runs:

1. repo hygiene and `git diff --check`;
2. migration drift and fresh migration;
3. production settings import and `check --deploy --fail-level WARNING`;
4. smoke imports;
5. canonical tests, with enough time or sharding for the measured 21-minute run;
6. economy/inventory reconciliation;
7. world connectivity, content, and applied-revision checks.

### 1.7 Supervise Evennia in the foreground

**Commit:** `ops: supervise evennia in foreground`

- replace daemonizing `evennia start` under `Type=simple` with a verified
  foreground topology;
- add pre-start configuration, migration, and content-revision checks;
- send output to journald and define restart/stop behavior;
- add deployment-asset tests and Linux staging verification instructions.

Host proof must cover start, crash restart, reload, stop, and reboot.

## Phase 2 — Atomic State And Safe World Deployment

### 2.1 Add economy integrity schema

**Commit:** `economy: add ledger integrity schema`

- non-negative bank balances;
- operation/idempotency identifiers;
- durable immutable bank drafts with issued/redeemed/void state;
- one active debt per character;
- positive inventory quantities;
- equipped items require a slot and cannot also be contained.

Run a pre-constraint audit and fail on inconsistent data instead of deleting it.

### 2.2 Introduce atomic economy operations

**Commit:** `economy: make ledger operations atomic`

Add `world/economy_transactions.py` as the owner for deposits, withdrawals,
bank debit/credit, drafts, debt, and recurring charges. Use transactions,
row locks, idempotency keys, and post-commit messages. Inject failure after each
write and prove full rollback.

### 2.3 Make inventory ownership atomic

**Commit:** `inventory: make ownership mutation atomic`

Wrap pickup, stacking, drop, container movement, equip/unequip, registration,
and unregistration so ObjectDB location, quantity, and ownership metadata change
together or not at all. Add failure and two-actor contention tests. Remove
production awareness of `MagicMock` from this path.

### 2.4 Migrate composite consumers

**Commit:** `economy: make composite purchases exactly once`

Prove:

- spawn failure does not charge a vendor purchase;
- craft-output failure does not consume ingredients;
- flight setup failure does not retain fare;
- reward retry does not duplicate currency/items;
- concurrent draft redemption pays once;
- concurrent withdrawals cannot overdraw.

### 2.5 Make quest outcomes durable

**Commit:** `quest: commit completion and outcomes atomically`

- lock the `CharacterQuest` row;
- assign a durable outcome/idempotency key;
- execute required rewards and consequences before marking complete;
- rollback all durable effects on failure;
- emit messages/OOB after commit;
- concurrent completion pays once.

This is the shared owner used by Social rewards; do not build a competing
Social-only transaction path.

### 2.6 Close direct area-authoring escape hatches

**Commit:** `world: close area authoring escape hatches`

Add literal DSL calls for vendor configuration, medics, spawn tags, initial room
state, Social nodes, and other currently direct mutations. Add an AST contract
test forbidding direct `.db`, `.tags`, `.attributes`, and `.scripts` mutation in
area modules.

### 2.7 Separate world definitions from persistence

**Commit:** `world: compile immutable content definitions`

Keep AreaBuilder's public literal Interface, but compile a deterministic
`ZoneDefinition` graph and manifest hash before persistence. Validate local and
cross-zone references, action IDs, registry IDs, and destructive intent without
touching the DB.

### 2.8 Plan and review world mutations

**Commit:** `world: plan content deployment`

Add a mutation-free `WorldContentPlan` that reports creates, updates, moves,
deletes, unresolved references, and player-impacting changes. Require explicit
destructive approval and refuse occupied-room deletion outside maintenance.

### 2.9 Apply world content atomically and record revisions

**Commit:** `world: apply content as a revision`

- acquire a deployment lock;
- apply the reviewed manifest in one maintenance transaction;
- resolve all cross-zone references before commit;
- record hash, Git commit, status, timestamps, and report;
- use `transaction.on_commit` for process-local swaps;
- prove idempotent second apply and total rollback after injected failure.

### 2.10 Remove content mutation from server startup

**Commit:** `world: verify content revisions at startup`

Add `worldcontent validate|plan|apply|status`. Startup loads persisted registries
and verifies the applied revision; it no longer rebuilds/deletes the world and
continues after exceptions. Production fails boot on revision mismatch.

## Phase 3 — A Truthful Fresh-Player And Equipment Loop

### 3.1 Create one canonical item catalog

**Commit:** `items: centralize canonical templates`

Extract the equipment catalog into `world/item_catalog.py`. Every non-processing
recipe, vendor item, quest grant, loot template, and starter item must resolve to
a complete catalog template. Weapons/armor are equipment with valid slots;
consumables have supported effects.

### 3.2 Repair and safely equip starter kits

**Commit:** `onboarding: issue usable starter kits`

- potions use the consumable effect contract and really heal;
- starter armor uses `armor_value`;
- starter gear auto-equips only into empty slots;
- ancestry selection rolls back on partial issuance failure;
- existing gear is never displaced.

### 3.3 Add a deep equipment-effects Module

**Commit:** `combat: apply equipment effects`

Add a small Interface for effective stats, equipped armor, weapon scaling stat,
and armor mitigation. Replace hardcoded Strength, aggregate bonuses once, and
use a capped diminishing armor curve. NPCs without inventory retain their
existing path. Do not invent undocumented domain-score gear scaling.

### 3.4 Make crafted output identical to catalog output

**Commit:** `crafting: create mechanically complete items`

Resolve `template_id`, overlay quality/provenance, apply only authored
`quality_affects`, and delete the generic cosmetic output fallback. Every
crafted weapon/armor is equippable and every crafted consumable usable.

### 3.5 Repair consumable effects

**Commit:** `items: make consumable effects authoritative`

- healing-over-time uses the canonical status/tick system;
- antidote cures poison from canonical active effects;
- unknown effects fail without consuming item or action;
- bait is fishing-only;
- item destruction occurs only after a valid effect begins.

### 3.6 Activate material, quality, and tool durability contracts

**Commit:** `crafting: consume material affordances`

Material quality survives processing; profession bonuses affect only the named
profession; every live material property has a consumer or becomes an authoring
error. Catalog tools receive durability, lose it through real use, and can be
repaired. Cosmetic metadata must not masquerade as mechanics.

### 3.7 Establish one ancestry-trait runtime

**Commit:** `ancestry: make authored traits observable`

Use `ANCESTRY_TRAITS` and matching help as the canonical fantasy. Add focused
hooks for stats, HP, speed, detection, disposition, and status duration. Delete
the conflicting dead additive modifier table after stronger behavior tests pass.
Derived effects must be idempotent across login.

### 3.8 Introduce authored progression events

**Commit:** `progression: award domains from meaningful play`

Add `world/progression_engine.py` with typed, idempotent events for combat
outcomes, quest outcomes, practice, gathering, crafting, exploration, and
investigation. Awards are explicit authored mappings, never generic every-hit
XP. Hidden domains cannot progress before discovery, and UI remains qualitative.

### 3.9 Calibrate a reachable Practiced path

**Commit:** `progression: make guild discovery reachable`

A fresh Vael-to-Ashreach journey must reach one fitting domain's threshold,
cannot unlock unrelated guilds, cannot repeat one-shot practice, survives
session commit, and emits one narrative recruitment.

### 3.10 Replace detached joining with recruitment and induction

**Commit:** `guilds: require authored recruitment and induction`

Eligibility creates durable recruitment, acceptance routes to an induction
contact/location, secondary domain selection belongs to that interaction, and
abilities are granted only on induction completion. `joinguild` cannot remotely
join or display numeric scores. Final scene prose waits for the vault.

### 3.11 Add graph-level world connectivity validation

**Commit:** `world: audit playable connectivity`

Add `scripts/audit_world_connectivity.py` and a system test. From fresh spawn,
every launch zone must be reachable through walking plus learnable flight.
Detect reciprocal-link defects, disconnected flight points, and circular
discovery gates.

### 3.12 Repair Vael/Ashreach and the courier graph

**Commit:** `travel: connect launch regions`

- add the real reciprocal Vael-to-Ashreach exit;
- repair intended cross-zone pairs;
- connect Korahei to the courier graph;
- let authored courier/map knowledge discover a route destination while
  retaining arrival discovery and origin-presence checks;
- prove the Warden route without teleportation.

## Phase 4 — Social Web Truth And Playable Consequence

### 4.1 Separate fact knowledge from claim belief

**Commit:** `fix: separate social fact knowledge from claims`

- enforce exactly one fact or claim per knowledge row;
- remove implicit fact inference from a claim;
- make authoring explicit;
- migrate dual rows conservatively to claim-only;
- let `SocialClaim.fact` remain admin provenance, not NPC knowledge;
- propagate the Warden claim—not canonical fact—to Harven.

### 4.2 Preserve every provenance route

**Commit:** `feat: preserve multi-route social provenance`

Normalize routes in `SocialTrace`, retain multiple independent routes, keep
same-route replay idempotent, aggregate belief confidence without overwriting
stronger knowledge, and show all routes in admin inspection.

### 4.3 Make visibility and propagation policy real

**Commit:** `feat: enforce social propagation policy`

Add claim visibility/expiry, explicit required and blocked tags, purpose policy,
real bandwidth, distinct gatekept/broadcast/two-way behavior, release actions,
and deterministic batch dispatch. Expired/private evidence cannot propagate,
appear in dialogue, activate offers, or enter renderer packets.

### 4.4 Add scheduled propagation without omniscience

**Commit:** `feat: schedule bounded social propagation`

Process due knowledge by availability and edge policy using a bounded batch and
idempotent trace identity. Keep explicit quest-event propagation on the same
policy path. Add operational visibility and a deterministic test clock.

### 4.5 Bound retrieval and separate eligibility from presentation

**Commit:** `perf: bound social retrieval and exact evidence`

Query facts/claims independently with DB limits, fetch traces only for selected
knowledge, clamp packet size, and add `find_social_evidence()` for exact offer
eligibility. Older qualifying evidence outside the dialogue packet must still
work; expired/private evidence must not.

### 4.6 Support multiple grounded offers

**Commit:** `feat: support multiple social offers`

Group rules per NPC, validate duplicates/predicates, order by priority and ID,
evaluate lifecycle per offer, and carry only qualifying evidence. Keep a short
compatibility adapter while dialogue becomes explicitly plural.

### 4.7 Materialize authored Social topology

**Commit:** `feat: materialize authored social topology`

Add literal `social_node`/`social_edge` DSL operations, materialize NPC profiles,
resolve cross-zone edges in a second pass, remove stale builder-owned topology,
and validate taxonomy. Move five anchor profiles out of hardcoded Python data.

### 4.8 Repair the physical Warden route

**Commit:** `fix: connect vael to the ashway`

Replace false internal stubs with a real southbound exit from Vael to
`ashreach_plains:ash_road_01`. Build both zones, move a real character through
Exit objects, and reach Harven without co-location or teleportation.

### 4.9 Activate the traveler rumor through gameplay

**Commit:** `feat: carry ashway conduct to whistle`

Author the traveler gathering node and edge. Actual quest completion records a
separate public road-conduct claim. After latency Whistle learns only that claim,
never the sealed report or institutional fact. Tests may not create topology or
invoke propagation directly.

### 4.10 Make denial/repair atomic

**Commit:** `fix: commit social repair atomically`

Claim, knowledge, trace, and any access consequence commit together. Failure
rolls all of them back; retry is idempotent; original facts remain intact.

### 4.11 Replace proxy social objectives

**Commit:** `feat: implement social quest interactions`

Remove `protect -> investigate` and `confront -> talk_to` aliases. Add authored
interaction objectives with verb, target, topic/evidence, and prerequisites.
The route becomes pressure inquiry, visible protection action, specific
confrontation, testimony, and report—in order. Whistle and Raith receive real
dialogue.

### 4.12 Compile and execute Social effects

**Commit:** `feat: execute authored social effects`

Compile `protected_witness`, testimony, knowledge, and access changes into
validated deterministic actions. Add durable named access grants consumed by a
real dialogue/quest/exit condition. Unsupported effects fail compilation and
effect failure leaves the quest pending.

### 4.13 Surface interpretation through behavior

**Commit:** `feat: surface authored social interpretations`

Evaluate admired, skeptical, feared, and channel preferences from builder-owned
profiles. The same rumor must produce distinct safe answers and at least one
practical offer/access consequence. Social changes update the dialogue hint
digest. Never expose raw keys or numeric confidence.

### 4.14 Harden and integrate the renderer last

**Commit:** `fix: enforce semantic social privacy`

Build an allowlisted semantic packet without raw IDs, traces, confidence,
private evidence, secrets, or withheld implications. Validate provider output
for IDs/entities/lore/length and fall back deterministically. A provider call
requires configuration, caller permission, and packet permission. Dialogue
uses the render result, while deterministic authored fallback remains normal.

### 4.15 Replace the decorative playtest harness

**Commit:** `test: prove social web in the live runtime`

`--verify` checks applied migrations, materialized topology, reciprocal exits,
policy, and route state. Remove fake commands and manual rumor triggers. Keep a
database-backed end-to-end command/movement test from acceptance through
consequences.

## Phase 5 — Cooperative Play, Factions, World State, Quests, And Help

### 5.1 Give combat an explicit ally Interface

**Commit:** `combat: record only allied actions`

Enemy actions cannot charge Command. Same-team actions can. Centralize action
recording for attacks and abilities and use the actual group/team relationship,
including member-side leader state.

### 5.2 Implement true personal loot and proximity credit

**Commit:** `groups: grant personal encounter rewards`

Snapshot eligible nearby participants at death. Persist independent entitlements
for personal drops and Scales. One claim cannot consume another. Nearby group
members receive quest credit; remote/late members do not. Ordinary shared drops
alone may use FFA/round-robin rules.

### 5.3 Implement authored quest sharing

**Commit:** `quests: share eligible runs with nearby group members`

Honor `can_share`, radius, cap, prerequisites, active limits, one-chance state,
and personal delivery items. Recipients receive independent progress from the
same frozen spec. Non-shareable remains the default and must retain a narrative
reason in content.

### 5.4 Canonicalize faction identity

**Commit:** `factions: canonicalize relationship identifiers`

Add a registry and aliases, normalize reads/writes, merge legacy
`warden`/`wardens` rows without losing standing/trust/betrayal, and mechanically
rewrite relationship IDs while leaving prose/enums alone.

### 5.5 Normalize the standing scale in all consumers and content

**Commit:** `factions: use the canonical standing scale`

Keep the documented internal `-100000..100000` scale. Centralize normalization,
move flight/vendor/disposition thresholds to that scale, prevent negative
discounts, and migrate content rewards that currently use tiny `25/50/75`
amounts into meaningful canonical units.

### 5.6 Give dimensions, Attunement, Trust, and Betrayal real writers

**Commit:** `world-state: execute authored relationship changes`

Add validated idempotent actions for dimensions, zone Attunement, Trust, and
Betrayal. Wire selected quest/practice/exploration outcomes explicitly and make
changes visible in dialogue/disposition. Do not infer mutations from prose.

### 5.7 Make node authoring feasible and self-validating

**Commit:** `nodes: make authored activation reachable`

Validate node flag/declaration pairs, repair Veluana, resolve Tremeneth intent
when the vault is available, replace the global lifetime `+5` cap with an
auditable rolling/per-presence policy, add real pressure sources and
stabilization sinks, and prove awakening/activation/recovery in simulation.

### 5.8 Snapshot accepted quest contracts

**Commit:** `quests: persist accepted specifications`

Add versioned spec snapshots to `CharacterQuest`. Offer lookup uses catalogs;
accepted progress/detail/reward/completion uses the frozen snapshot. Backfill
legacy active rows deliberately and preserve Social compiled context.

### 5.9 Execute quest consequences

**Commit:** `quests: execute visible world consequences`

Add explicit consequence action lists using world events, room state, standing,
Trust, Social state, access, and quest flags. Prose remains summary only. Migrate
one hub/outbound chain at a time; never parse English consequence text into
guessed mutations.

### 5.10 Reconcile death, encumbrance, tools, banking copy, and deferred promises

**Commit:** `help: make survival and utility promises truthful`

- preserve equipped gear on death if keeping the current explicit help promise;
  otherwise wait for a contrary vault decision and change both together;
- implement documented Moderate/Heavy encumbrance effects or remove the claims;
- remove nonexistent bank item-vault instructions;
- make tool durability real as covered in Phase 3;
- clearly defer unimplemented companion and planned-skill identities instead of
  presenting them as live;
- keep hidden progression hidden.

## Phase 6 — Dialogue And Content Quality

### 6.1 Normalize and validate dialogue definitions

**Commit:** `dialogue: enforce the authored schema`

Add `world/dialogue_schema.py`. During migration, map legacy `greeting` to a
neutral tier and convert hints into real topic references. Rewrite all affected
payloads, then make legacy keys a build error. Critical onboarding NPCs must
produce non-generic greetings, usable hints, and valid topics.

### 6.2 Add a prose-quality release gate

**Commit:** `content: reject scaffold and meta prose`

Add `scripts/audit_content_prose.py` and tests that reject player-facing meta
phrases, exact duplicate descriptions, and excessive repeated sentences. Keep
the allowlist narrow and reviewed. The gate is written now; it remains red until
the source-backed rewrites land.

### 6.3 Rewrite affected zones one at a time

**Vault-dependent commits:**

1. Korahei
2. Veluana Central Isle
3. Veluana Outer Reefs
4. Kiai Grounds
5. Colonist Ruins
6. Tremen
7. Greyteeth Lower Passes
8. Tremeneth Deep Mines
9. Tremeneth Underhalls
10. Tremeneth High Passes

For each zone, preserve IDs, topology, quest targets, mystery constraints, and
literal DSL. Replace scaffold prose with concrete sensory evidence, local labor
and social detail, spatial cues, danger signals, and interactable reasons to be
there. Synonym-swapping templates is not acceptable.

## Phase 7 — Runtime-Faithful Verification And Closeout

### 7.1 Remove production awareness of mocks

**Commit:** `test: use runtime-faithful interfaces`

Replace production `unittest.mock` branches with faithful fakes, local
implementations, or integration fixtures. Keep interaction mocks only where the
interaction itself is the contract.

### 7.2 Add the database-backed golden path

**Commit:** `test: prove the truthful player journey`

Prove, through real owned interfaces:

> fresh character -> ancestry -> usable starter item -> equipped gear -> combat
> bonuses and mitigation -> Vael road quest -> real walk to Ashreach -> group
> kill with personal loot/credit -> meaningful domain progress -> recruitment
> and induction -> gather/process/craft/use -> quest consequence changes
> dialogue/world state -> node pressure and stabilization -> Social fact/claim
> propagation and repair

### 7.3 Final release proof

On disposable PostgreSQL:

1. migrate from empty and from a restored copy;
2. validate and apply content once;
3. apply again and prove no-op;
4. inject content/economy/quest failures and prove rollback;
5. start/reload twice and prove zero world mutation;
6. run focused suites, golden path, and all tests;
7. run smoke imports, deploy checks, hygiene, connectivity, prose audit, economy
   reconciliation, inventory reconciliation, and `git diff --check`;
8. inspect the final diff and commit boundaries;
9. write an Engram closeout with commits, validation, remaining external gates,
   and the next playtest.

## Finding Traceability

| Audit finding | Owning tasks |
|---|---|
| Tracked/overriding secret | 1.1, external incident actions |
| Insecure production settings, port collision, dead overrides | 1.2 |
| Invalid systemd supervision and optional HTTPS | 1.7 |
| Migration drift and SQLite uniqueness warning | 1.5 |
| Incomplete CI/release gate | 1.6 |
| Tracked logs/static and false hygiene report | 1.3, 1.4 |
| Untrustworthy dirty/untagged release provenance | 1.6, 7.3 |
| Non-atomic banking/inventory/drafts/debt | 2.1-2.4 |
| Quest completion before rewards | 2.5 |
| Fail-open startup world rebuild | 2.6-2.10 |
| Unreachable zones and circular flight discovery | 3.11, 3.12 |
| Broken starter items and dormant ancestry traits | 3.2, 3.7 |
| Equipment/armor/scaling ignored | 3.3 |
| Hollow crafted items, material metadata, consumables, tools | 3.4-3.6 |
| Unreachable domain progression and detached guild joining | 3.8-3.10 |
| Fact/claim knowledge collapse | 4.1 |
| Last-write-wins provenance | 4.2 |
| Expiry/secrecy/bandwidth/direction/policy/scheduler gaps | 4.3, 4.4 |
| Unbounded Social queries and top-five offer gating | 4.5 |
| One offer per NPC overwrite | 4.6 |
| Inert AreaBuilder Social metadata/profiles | 4.7 |
| False Warden route and test-seeded traveler route | 4.8, 4.9 |
| Non-atomic denial and Social outcomes | 4.10, 2.5 |
| Proxy protect/confront objectives and silent NPCs | 4.11 |
| Inert authored Social effects/access changes | 4.12 |
| Inert interpretation and hint hashing | 4.13 |
| Renderer privacy/consumer gap | 4.14 |
| Decorative playtest harness | 4.15 |
| Enemy actions counted as allies and incomplete group identity | 5.1 |
| Killer-only loot/credit and missing quest share | 5.2, 5.3 |
| `warden`/`wardens` and standing-scale drift | 5.4, 5.5 |
| No writers for dimensions/Attunement/Trust/Betrayal | 5.6 |
| Impossible/inert node activation and Veluana mismatch | 5.7 |
| Mutable quest specs and decorative consequences | 5.8, 5.9 |
| Death/encumbrance/bank/help/companion/tool overpromises | 5.10 |
| Ignored dialogue schema | 6.1 |
| Template/meta room prose | 6.2, 6.3 |
| Production mock branches and proxy-heavy tests | 7.1, 7.2 |

## Definition Of Done

The program is complete when:

- no repository or runtime security finding remains unowned;
- a clean PostgreSQL environment passes migrations and production deploy checks;
- server startup does not mutate authored world content;
- a fresh player can reach every launch region and progress into an authored
  induction through ordinary play;
- equipment, armor, crafting, consumables, materials, and tools alter gameplay;
- group rewards and credit are independently personal;
- world-state dimensions and nodes have reachable authored sources/sinks;
- quests freeze their accepted contracts and commit consequences durably;
- Social claims do not leak facts, provenance is multi-route, propagation policy
  is real, and the route is playable without test-only setup;
- dialogue/content schemas reject inert authoring;
- the prose gate is green after source-backed zone rewrites;
- the runtime golden path and canonical suite pass;
- all commits are scoped, reviewed, and recorded in Engram;
- external secret rotation/history/TLS/systemd actions are either verified or
  explicitly remain operator-blocked rather than falsely claimed complete.
