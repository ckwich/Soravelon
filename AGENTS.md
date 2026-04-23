# AGENTS.md — Soravelon Repo Guide

This file exists to keep Soravelon work aligned with the actual game you are
building, not with default MUD habits or generic RPG assumptions.

If the live repo, Obsidian vault, Engram memories, and local planning docs do
not agree, stop and reconcile the contradiction explicitly before proceeding.
Do not silently pick the version you find most convenient.

## Core Rule

- Build and debug the project the right way, every time.
- Do not rely on flimsy shortcuts, lazy workarounds, or speculative fixes when
  a correct path exists.
- Soravelon has many intentional deviations from traditional MUD design. Do not
  "normalize" it back toward genre defaults without explicit support from the
  source material.

## Startup Ritual

Start each session with a deliberate planning pass before implementation.

1. Read this file.
2. Read `CLAUDE.md` for repo layout, skills, and command/test basics.
3. Scan `git status --short` and identify a clean commit boundary before you
   touch code.
4. Read the relevant Obsidian docs from `C:\Obsidian\brain\Soravelon\`.
5. Read `C:\Obsidian\projects\Soravelon\plan.md`.
6. If the topic is system-heavy, read `C:\Obsidian\projects\Soravelon\AGENTS.md`.
7. Search Engram before making assumptions when vault docs are incomplete or
   implementation questions remain.
8. Review the latest relevant audit/remediation docs under
   `docs/superpowers/plans/` when working in a launch-readiness area.
9. Confirm the intended validation path before coding.

## Source Of Truth Order

Use sources in this order:

1. Live runtime behavior and current code for what the game does today.
2. This file and in-repo docs for execution discipline and local conventions.
3. Obsidian docs for intended game design and world logic.
4. Engram for decisions, rationale, and design context not yet backfilled into
   repo docs or Obsidian.
5. If a gap remains, flag it instead of improvising.

High-value Soravelon design references:

- `C:\Obsidian\brain\Soravelon\soravelon.md`
- `C:\Obsidian\brain\Soravelon\Soravelon_World_Bible.md`
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md`
- `C:\Obsidian\brain\Soravelon\soravelon-guilds.md`
- `C:\Obsidian\brain\Soravelon\soravelon-commands.md`
- `C:\Obsidian\brain\Soravelon\soravelon-inventory.md`
- `C:\Obsidian\brain\Soravelon\soravelon-dialogue.md`
- `C:\Obsidian\brain\Soravelon\soravelon-quests.md`
- `C:\Obsidian\brain\Soravelon\soravelon-crafting.md`
- `C:\Obsidian\brain\Soravelon\soravelon-ancestries.md`
- `C:\Obsidian\brain\Soravelon\soravelon-architecture.md`
- `C:\Obsidian\brain\Soravelon\soravelon-room-state.md`

High-value Engram memories:

- `soravelon_obsidian_gameplay_intent_synthesis_2026_04_22`
- `soravelon_world_mud_design`
- `soravelon_systems_combat_economy`
- `soravelon_architecture_2026_03_20_updates`

## Debugging Discipline

When investigating a bug, follow this exact process:

1. Lock the symptom.
2. Inspect live runtime state.
3. Prove the failing gate.
4. Change exactly one thing.
5. Re-verify.

What this means in practice:

- Do not keep patching based on theories.
- Do not continue implementation from an unproven explanation.
- Prefer direct instrumentation of the real runtime path over inference from
  side effects.
- Use the same runtime trace, check, or gate that actually decides behavior as
  the source of truth.
- If a hypothesis is disproven by observation, stop and reset rather than
  layering more guesses on top.

## Quality Bar

- Favor evidence-led debugging over trial and error.
- Favor stable, production-safe foundations over temporary convenience.
- If the right solution depends on a simple editor/setup step the user should
  perform, stop and ask instead of improvising around it.

## Session Workflow

- Start each work session with a deliberate planning pass before
  implementation.
- Use available Codex "superpowers" proactively to improve session quality:
  codebase search, architecture cross-checking, consistency review, validation
  tooling, and project-planning capabilities.
- Steelman the session before coding:
  confirm the goal, review the binding docs and current repo state, identify
  contradictions or hidden risks, define the intended validation path, and
  choose a clean commit boundary.
- If a planning document, scene setup, package decision, multiplayer-authority
  rule, or other binding design constraint conflicts with the live repo state,
  stop and resolve the contradiction explicitly before continuing.

## Execution Discipline

- Prefer boring, correct, production-worthy architecture over shortcuts.
- Keep UI, commands, networking, services, world logic, and data boundaries
  clean.
- Keep changes small, logically grouped, and easy to validate.
- Never "fix" design tension by flattening Soravelon into generic MUD patterns.
- If the right solution depends on a simple human/editor/setup step, stop and
  ask instead of improvising around it.

## Repo Discipline

- The repo may be very dirty. Never clean, reset, or revert unrelated work.
- Do not batch unrelated changes into one commit.
- End every completed work session with a git commit when a clean, scoped
  boundary exists.
- If the tree is too dirty for a safe commit boundary, call that out plainly
  instead of forcing a messy commit.
- Before committing, summarize what changed, why it changed, and how it was
  validated.

## Soravelon Design Intent

### 1. Progression Is Hidden And Narrative

- Players never see a level number.
- Backend level is internal only and exists for scaling math, not player-facing
  progression.
- Players do not choose a class from a menu.
- Players begin as Wanderers and develop domain proficiency through action.
- Guilds find players at Practiced. Guild discovery is a world event, not a
  character creation choice or trainer menu.
- Secondary domain is chosen narratively at induction, not as a detached build
  screen.

### 2. Domains Are Not Generic Mana Trees

- Soravelon uses 10 domains and 90 subclasses, not traditional classes.
- Domain resources are intentionally asymmetrical and often non-pool based.
- Focus is a timing/window mechanic, not a mana bar.
- Balance is a spectrum, not a pool.
- Reagents and Components are prepared stock, not passive combat bars.
- Echoes are investigation-informed power.
- Profession skills are universal skill tracks, not class-locked professions.

### 3. The World-State Engine And Node System Are Central

- Nodes and the five world-state dimensions are backbone systems, not flavor.
- Every major content/system judgment should consider world-state and node
  implications.
- Nodes should intensify zones, not make non-node zones feel worthless.
- Stabilization pushes systems back toward equilibrium. It is not true repair.

### 4. Open-World Play Is Intentional

- Do not assume hub-stepping progression rails.
- Do not assume level-gated zones as the default answer.
- Players should be able to go where they want.
- Guidance should come from fiction, danger signals, quest routing, logistics,
  and world reaction rather than blunt progression walls.

### 5. Mystery Must Be Preserved

- The dragon-continent truth is a discovery, not overt exposition.
- Node descriptions should not casually reveal dragon-body geometry.
- Current-era content must not casually imply that dragons are intelligent under
  the curse.
- Hints and breadcrumbs are good. Direct revelation without narrative earning is
  not.
- Factions should have understandable interests and tradeoffs, not flatten into
  obvious good/evil binaries.

### 6. Quests Must Carry Meaning

- Every quest should tell a story, reveal the world, change the world, guide
  meaningful exploration, or deepen a relationship. Preferably more than one.
- "Kill 30 wolves because I said so" is not good enough.
- Delivery quests should route players toward real places and discoveries.
- Non-shareable quests should have a narrative reason, not just a mechanical
  restriction.
- Quest completion should leave visible or trackable consequences where
  appropriate.

### 7. Dialogue Should Feel Conversational

- NPCs are not kiosks.
- Keyword/topic dialogue with hinting is the intended launch model.
- NPC tone should be shaped by Standing, Trust, quest state, and world-state.
- `talk`, `ask`, `tell`, hints, and inline quest offers should create
  conversational flow rather than menu friction.

### 8. Inventory And Economy Are Custom By Design

- Never describe inventory as slot-based capacity.
- Inventory is weight-based with graduated encumbrance.
- Equipment slots are real. Inventory slots are not.
- Keyring behavior, auto-stacking, filtering, and quest-item protection are
  intentional design choices, not temporary conveniences.
- Masterwork gear should be meaningfully desirable without invalidating dropped
  gear.

### 9. Group Play Is About Synergy, Not HP Inflation

- Group value should come from coordination, compounds, tactical proximity,
  survivability, and subclass synergy.
- Do not treat grouping as an excuse for flat numeric mob inflation.
- Personal loot is the default expectation.
- Quest drops and Scales are personal regardless of group context.

### 10. Companions And Dragons Carry Emotional Weight

- Dragon bonds are earned and chosen by the dragon.
- Companion loss/friction is deliberate. Do not casually design around removing
  all consequence.
- Other players can interact with dragons; that does not mean they can freely
  bond them.

## System Guardrails

### Commands And Help

- The parser supports shortest-unambiguous prefix matching.
- Aliases can chain up to 3 commands and never override system commands.
- Help text must be truthful to the live runtime, not legacy intent.
- Command/help drift is a real launch blocker.
- Onboarding/help should teach Soravelon's own logic, not assume players think
  in generic MUD habits.

### World State, Persistence, And Data Modeling

- Intrinsic character state belongs on `db` attributes.
- Relationships between entities belong in Django models.
- Mutable/high-churn history belongs in `ndb` during play and should be
  batch-committed at natural breakpoints.
- Do not expose backend level in UI, help, content, or commands.

### Combat And Ability Work

- If an ability's authored fantasy is sound, prefer implementing the runtime to
  match it rather than nerfing text down to the current shortcut.
- Status effects, compounds, room-state, and cross-domain interactions are part
  of Soravelon's fun, not optional garnish.
- Speed should matter, but should not become a universal trap or universal best
  answer.
- Group and AoE abilities should actually do the coordinated things their text
  promises.

### Areas And Builder Safety

- Area content must remain builder-safe and round-trippable.
- Use strict literal AreaBuilder DSL patterns that the builder app can parse:
  `area.room(...)`, `area.exit(...)`, `area.npc(...)`, `area.quest(...)`,
  `area.item(...)`, and similar literal calls.
- Do not introduce abstractions the builder cannot round-trip.
- Cross-zone exit unresolved state should be treated carefully; load-order issues
  are not the same thing as broken content.

### Narrative Content Guardrails

- Match existing world logic, faction posture, and historical continuity.
- Do not casually contradict prior lore fragments, faction stances, or regional
  culture.
- Rich, trackable history is a requirement, not bonus flavor.
- Rewards, items, and vendors should feel fair, intentional, and zone-appropriate.

## Validation Expectations

- Validate with the smallest truthful set of checks first, then broaden as
  needed.
- Prefer direct behavior tests over brittle string-presence checks.
- For systems work, use focused automated tests plus `python scripts/smoke_start.py`
  when appropriate.
- For area content, use parser/import/layout/contract validation and the
  external builder parser when the workflow calls for it.
- If you did not run an important validation path, say so explicitly.

## Audit Mindset

When auditing, do not only look for things that are broken.

Also look for:

- improvement opportunities
- design drift from Soravelon's intended identity
- misleading help/onboarding
- overpromised but under-implemented content
- fairness/balance issues
- narrative thinness
- worldbuilding contradictions
- test coverage gaps that hide real launch risk

## Before You Touch A System

Read the relevant Obsidian docs first:

- Combat/abilities: `soravelon-abilities.md`, `soravelon-guilds.md`,
  `soravelon-room-state.md`
- Commands/help/onboarding: `soravelon-commands.md`, `soravelon-dialogue.md`
- Inventory/items/economy: `soravelon-inventory.md`, `soravelon-crafting.md`
- Quests/NPCs/factions: `soravelon-quests.md`, `soravelon-dialogue.md`,
  `soravelon-ancestries.md`, `Soravelon_World_Bible.md`
- Areas/worldbuilding: `soravelon.md`, `Soravelon_World_Bible.md`,
  `soravelon-architecture.md`, `soravelon-builder.md`, `soravelon-areaspec.md`

If the docs still leave a question open, search Engram before guessing.

## Session Closeout

- Summarize what changed, why, and how it was validated.
- Log important decisions or recovered context to Engram.
- Commit if the change has a clean, scoped boundary.
- If no safe commit boundary exists because of unrelated work in the tree, say
  that explicitly.
