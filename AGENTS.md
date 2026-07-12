# AGENTS.md — Soravelon Engineering and Design Contract

Soravelon is not a generic MUD. Preserve its authored, open-world,
social-memory RPG identity instead of normalizing it toward genre defaults.
Build and debug the real system; do not substitute a lookalike, shortcut, or
cosmetic approximation for the requested runtime behavior.

## Documentation Contract

- This file is the durable engineering, source-of-truth, and design contract.
- `CLAUDE.md` is the concise repository map: current runtime baseline,
  commands, typeclasses, and domain-skill index. It must not duplicate policy
  from this file.
- `README.md` is contributor/deployment onboarding.
- `docs/superpowers/plans/` records audits and implementation plans. Treat a
  plan's stack declaration as historical unless it matches `requirements.txt`
  and live runtime verification.

When the documents conflict, do not silently choose the convenient one. State
the contradiction, verify the live path, and reconcile the durable docs in the
same clean slice where appropriate.

### Superseded Vault Proposals

- `brain/Soravelon/soravelon-llm-quests.md` is an exploratory March 2026
  proposal, not an implementation authority. Its model-generated zones,
  rewards, and world consequences are superseded by this contract: authored,
  deterministic systems own quest structure, rewards, and state mutation;
  any LLM use is bounded phrasing over allowlisted context.
- `projects/Soravelon/plan.md` and older vault architecture headers that name
  Evennia 6.0 are historical runtime snapshots. The active baseline is the
  `requirements.txt` pin and its live verification.

## Session Start: Establish Truth Before Editing

1. Read this file and `CLAUDE.md`.
2. Inspect `git status --short`; preserve unrelated work and identify the
   intended commit boundary.
3. Confirm the active runtime/dependency contract in `requirements.txt` and
   the relevant source and tests.
4. Read the relevant Soravelon design sources in the Obsidian vault:
   `C:\Obsidian\brain\Soravelon\` and
   `C:\Obsidian\projects\Soravelon\plan.md`.
5. For system-heavy work, also read
   `C:\Obsidian\projects\Soravelon\AGENTS.md` and the latest relevant
   audit/remediation document under `docs/superpowers/plans/`.
6. Check Engram before assuming missing context. Prove that the Hub is
   reachable; a local memory cache is not a substitute for the Hub.
7. Define the runtime contract and its validation gate before coding.

### Vault and Remote Access

The Windows Obsidian vault is the design source, not a local-path convention.
From macOS, use an existing authenticated, read-only LAN/Tailscale mount or
other user-authorized access path. If access requires credentials or the Hub
cannot expose the raw files, report that gate; do not invent a local copy,
reconfigure remote services, or treat stale cached notes as live-vault proof.
A user-authorized Taildrop bundle is a point-in-time source snapshot: verify
its integrity and received date, use it for the current session, and do not
represent it as continuous vault access.

Use tools proactively for code search, architecture cross-checks, upstream
dependency verification, focused tests, live playtests, and Engram retrieval.
Tool output is evidence, not a replacement for the source-of-truth order
below.

## Source-of-Truth Order

1. Live runtime behavior and current code for what the game does today.
2. `requirements.txt`, this file, `CLAUDE.md`, and current in-repo docs for
   technical contracts and local conventions.
3. Obsidian for intended game design, world logic, and narrative continuity.
4. Engram for decisions, rationale, and cross-session context not yet
   backfilled into the repo or vault.
5. If a gap remains, flag it instead of improvising.

High-value vault references include `soravelon.md`,
`Soravelon_World_Bible.md`, `soravelon-abilities.md`,
`soravelon-guilds.md`, `soravelon-commands.md`,
`soravelon-inventory.md`, `soravelon-dialogue.md`, `soravelon-quests.md`,
`soravelon-crafting.md`, `soravelon-ancestries.md`,
`soravelon-architecture.md`, and `soravelon-room-state.md`.

## Non-Negotiable Engineering Rules

- Prefer boring, correct, production-worthy boundaries between commands, UI,
  networking, services, world logic, and data.
- Preserve dirty unrelated work. Never reset, clean, or revert it.
- Keep changes small, logically grouped, and directly testable.
- Do not claim a fallback, mock, heuristic, or test fixture is the real
  feature. Label temporary fallbacks in code, docs, and handoff notes.
- Do not keep bridge code alive after a chosen runtime cutover. Remove dead
  paths in the same clean boundary when safe.
- If a simple human setup action is required for the correct solution, stop
  and ask rather than improvising around it.

### Debugging Discipline

For every bug:

1. Lock the symptom.
2. Inspect the live runtime state.
3. Prove the failing gate.
4. Change exactly one thing.
5. Re-verify through that same gate.

Do not layer speculative patches. If evidence disproves a hypothesis, reset
the model instead of preserving the patch.

### Runtime and Dependency Policy

- The supported baseline is Python 3.12+ and `evennia==6.1.0`.
- `requirements.txt` is the pinned runtime authority. Historical plan headers
  that say Evennia 6.0 or Python 3.11 are not active configuration.
- Prefer an upstream repair plus a tested dependency upgrade over copying an
  upstream protocol or framework method into `server/`.
- The Evennia 6.0 Telnet bytes/regex defect was repaired upstream in 6.1;
  there is intentionally no project-local `TELNET_PROTOCOL_CLASS` override.
  A future compatibility layer needs a proven upstream gap, a stock-path
  regression test, removal criteria, and an explicit upgrade plan.
- Activate the virtual environment before using `evennia`; its launcher calls
  `twistd` from `PATH`.

## Soravelon Design Identity

### Character Growth and Domains

- Progression is hidden and narrative. Backend level is scaling math only;
  players never see a level number or choose a class menu.
- Players begin as Wanderers, gain domain proficiency through action, and are
  discovered by guilds at Practiced. Secondary domain is chosen narratively at
  induction.
- The ten domains and ninety subclasses are not generic mana trees. Focus is
  a timing/window mechanic; Balance, reagents, components, and echoes retain
  their asymmetric authored behavior. Profession skills are universal tracks.

### World, Exploration, and Mystery

- Nodes and the five world-state dimensions are backbone systems. Nodes
  intensify zones; they do not make non-node zones worthless. Stabilization is
  a return toward equilibrium, not true repair.
- Open-world play is intentional. Guide through fiction, danger, logistics,
  quest routing, and world reaction—not hub-stepping rails or blunt level
  gates.
- Preserve the dragon-continent mystery. Do not reveal dragon-body geometry or
  current-era dragon intelligence without narrative earning. Factions need
  understandable interests and tradeoffs, not easy good/evil labels.

### Relationships, Quests, and Dialogue

- The Social Web is local standing, trust, betrayal, rumor, and subjective
  NPC worldview—not a global morality number. It may route and personalize
  authored content; it must not replace authored truth with freeform AI.
- Deterministic authored systems own quest structure, rewards, and world-state
  mutation. An LLM may phrase bounded, allowlisted context only.
- Every quest must tell a story, reveal or change the world, guide meaningful
  exploration, or deepen a relationship. Completion should leave visible or
  trackable consequences when appropriate.
- NPCs are conversational, not kiosks. Keyword/topic dialogue, `talk`,
  `ask`, `tell`, hints, and inline offers should reflect Standing, Trust,
  quest state, and world state.

### Economy, Groups, and Companions

- Inventory is weight-based with graduated encumbrance; equipment slots are
  real, inventory slots are not. Preserve keyring, stacking, filters, and
  quest-item protection.
- Group value comes from coordination, compounds, proximity, survivability,
  and subclass synergy—not flat HP inflation. Personal loot is the default;
  quest drops and Scales are personal.
- Dragon bonds are earned and chosen by the dragon. Companion loss and
  friction have deliberate weight; do not casually remove their consequences.

## System Guardrails

### Commands, Help, and Player-Facing Language

- The parser supports shortest-unambiguous prefix matching. Aliases chain up
  to three commands and never override system commands.
- Help, onboarding, and command output must describe live behavior, not
  legacy intent. Command/help drift is a launch blocker.
- Player-facing commands, help, and dialogue must filter hidden current-era
  Remnance, Vaelborn, and Echoes through `world/remnance_visibility.py`.
  Internal engine data remains complete.

### Data and Runtime State

- Intrinsic character state belongs on `db` attributes; relationships belong
  in Django models; mutable high-churn history belongs in `ndb` and is
  committed at natural breakpoints.
- Never expose backend level in UI, help, content, or commands.
- When Evennia may return either a wrapped Character or a database row, use
  `world.world_state._as_typeclass()` rather than assuming `.typeclass`.

### Combat, Areas, and Content

- Implement sound authored ability fantasy rather than nerfing prose to match
  a shortcut. Status effects, compounds, room state, and cross-domain
  interactions are gameplay, not garnish.
- Area content must be builder-safe and round-trippable. Use literal
  `area.room(...)`, `area.exit(...)`, `area.npc(...)`, `area.quest(...)`, and
  `area.item(...)` calls that the builder can parse; do not introduce opaque
  abstractions. Treat cross-zone load-order deferrals separately from broken
  content.
- Narrative content must match world logic, faction posture, history, and
  regional culture. Rewards, items, and vendors must be fair, intentional,
  and zone-appropriate.

## Validation, Audits, and Closeout

- Validate the smallest truthful gate first, then broaden in proportion to
  risk. Prefer behavior tests over string-presence checks.
- Use `python scripts/run_tests.py` for the canonical test runner and
  `python scripts/smoke_start.py` for bootstrap/import proof. See `CLAUDE.md`
  for focused commands and correct Evennia settings syntax.
- Runtime/networking work requires a focused test plus a live path when
  feasible. Social Web work must prove the real persistence and routing path,
  not only fixtures or static topology.
- Area work requires parser/import/layout/contract validation and the external
  builder parser when relevant.
- Audits must cover design drift, misleading help/onboarding, overpromised
  content, fairness, narrative contradictions, security, and missing tests—not
  only crashes.
- Close every clean session with a scoped commit. Summarize the change, why,
  validation, remaining limits, and write a concise Engram memory when the Hub
  is reachable.
