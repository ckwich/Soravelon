# Project Research Summary

**Project:** Soravelon — Evennia 6.0 dark-fantasy MUD
**Domain:** Deep-progression MUD — 90-subclass ability system, desktop client, GUI zone builder
**Researched:** 2026-03-24
**Confidence:** MEDIUM-HIGH

## Executive Summary

Soravelon's next milestones add three major systems to a fixed Evennia 6.0 stack: a server-side ability/guild engine, a standalone desktop MUD client, and a GUI zone authoring tool. The server-side ability work is pure Python extending the established `world/` engine pattern — no new dependencies, HIGH confidence on approach. The desktop client is a Tauri 2.0 + React 19 + TypeScript application that connects to Evennia's existing JSON-over-WebSocket protocol; Tauri 2.0 is production-stable and the right choice over Electron for a solo developer. The GUI zone builder is a second Tauri app using `@xyflow/react` v12 as the canvas, writing `.py` area spec files to disk — the existing `AreaBuilder` pipeline consumes them unchanged on server reload.

The recommended approach across all three systems is consistent: data-driven registries for 360+ abilities (definitions global, ownership in Django model, runtime state on `character.db`), a push-only OOB protocol for server→client state updates, and a file-system-only contract between the builder and the server. These patterns are direct extensions of what Soravelon already does for mob affixes, domain scores, and zone specs. The main design risk is subclass identity — 90 subclasses backed by combinatorial domain pairs will collapse to stat variance unless each of the 10 domains gets a distinct "mechanical fingerprint" before any ability is authored.

The single most critical pre-condition for all ability work is establishing that fingerprint: what gameplay verb is exclusive to each domain. The single most critical pre-condition for the client is defining a typed OOB message protocol before writing any event handlers. The single most critical pre-condition for the builder is fixing the known cross-zone exit two-pass loading bug before any content authoring begins. In all three cases, a small design decision made early eliminates entire categories of rework later.

## Key Findings

### Recommended Stack

The server-side ability system requires no new packages. Python frozen dataclasses in `world/abilities/` hold definitions; a single `world/ability_registry.py` builds a module-level lookup dict at server start; `CharacterAbility` and `CharacterGuild` Django models in `world/models.py` track ownership; `character.db.ability_cooldowns` dict holds runtime state — same pattern as `domain_scores`. Evennia's Traits contrib is explicitly rejected for this use case (one attribute key per ability per character at 360+ abilities is O(n) to query and expensive to reset).

Both the desktop client and the GUI builder are separate repos sharing the same base stack: Tauri 2.0 + React 19 + TypeScript + Vite 6 + Zustand 5 + Tailwind 4 + shadcn/ui. The client adds `@tauri-apps/plugin-websocket` and `xterm.js` for MUD output; the builder adds `@xyflow/react` v12.5.0 (confirmed current, March 2025) and Zod 3 for area spec validation before disk write.

**Core technologies:**
- Python dataclasses (stdlib): Frozen ability definitions — zero overhead, no new deps, matches established pattern
- Django ORM (existing 6.0.3): `CharacterAbility` / `CharacterGuild` models for ownership persistence
- Evennia `db` attributes: Cooldown timestamps and runtime ability state on `character.db`
- Tauri 2.0: Desktop app shell for both client and builder — <10 MB installer vs Electron's 80-120 MB, 30-50 MB idle vs 200-500 MB
- `@xyflow/react` v12.5.0: Visual room/exit graph canvas for the zone builder — production-proven, actively maintained
- `@tauri-apps/plugin-websocket`: Rust-native WebSocket to Evennia port 4008; required for Tauri's security model
- xterm.js 5.x: Terminal emulator for MUD text pane — handles ANSI, scrollback, font rendering
- Zod 3.x: Runtime schema validation of area specs before writing to disk

### Expected Features

**Must have (table stakes):**
- Distinct ability set per subclass — core identity; 90 subclasses × 4 tiers = 360+ abilities, each mechanically distinct
- Ability tier gating by Guild Tier Score (GTS 0/20/50/85) with learn command and trainer NPC delivery
- Active vs. passive ability distinction with cooldowns and resource costs
- 90 subclass definitions derived from `(primary_domain, secondary_domain)` pairs
- 4 ancestry definitions with stat modifiers and 1-2 passive traits each
- 4 general proficiency skill tracks (0-100), tapping existing domain XP accumulation
- Basic ability-driven combat system integrated with existing zone_scaling.py math
- Server-side OOB push for HP/resources/domain scores (prerequisite for all client panels)
- Room coordinate storage in AreaBuilder specs (prerequisite for client map panel)
- Desktop client: WebSocket connection, scrollback buffer (5000+ lines), command history, ANSI rendering, split input
- Desktop client: Dashboard panel with HP/resources/domain scores pushed via OOB
- GUI builder: Room/exit creation with visual canvas, mob placement, zone metadata, save to `.py` spec

**Should have (competitive differentiators):**
- Domain combination identity display — no other MUD derives identity from 10×9 combinatorial pairs
- Cross-domain synergy abilities exclusive to specific pairings (e.g., Null Strike for Duskblade only)
- Signature subclass command names (shadowstep, thorn-bind) — cosmetic + mechanical identity
- Node event notifications in client (zone state changes as visual alerts)
- Domain score mini-bar chart and world-state dimension gauges in client dashboard
- Ability panel with cooldown timers in client
- Node configuration and Layer 0/1 room pairing in GUI builder
- Mob template library in GUI builder

**Defer (v2+):**
- World-state-gated ability modifiers (requires large-scale play data)
- Ancestry × subclass deep synergies (requires M1 ability system playtested)
- Profession tracks: Cooking, Smithing, Alchemy, Scholarly Research (after base skill engine proven)
- Respec / subclass change path (after player feedback confirms pain points)
- Consensual arena PvP (M3 — requires combat balance data)
- Contributor access model for GUI builder (after owner mode is stable)
- Client triggers and aliases (QoL for veterans, not blocking)

**Anti-features to avoid:**
- Visible level numbers — collapses domain-identity system; display GTS tier label only
- Per-ability XP grind — 360 individual XP tracks explode the data model; use GTS gating
- Auto-combat trigger scripting — destroys domain XP scarcity model
- Hard zone level gates — negates the logarithmic per-player scaling design

### Architecture Approach

All new server-side systems follow the same three-layer pattern already present in `world/`: typeclasses as thin interfaces, engine modules for business logic, Django models for persistence. The ability engine is generic code that reads from a module-level registry dict; it does not know what subclass it is serving. The subclass engine is the single gating layer — all other systems call it, never recompute subclass or tier themselves. All state pushed to the desktop client goes through a single `world/oob_publisher.py` to prevent OOB call patterns from scattering. The GUI builder writes `.py` files to disk via Tauri's fs plugin; the server loads them at reload time — no live HTTP API between builder and server.

**Major components:**
1. `world/ability_registry.py` — loads all 90 subclass definition files at server start into a `dict[key -> AbilityDef]`; read-only after start
2. `world/subclass_engine.py` — derives active subclass and GTS tier from existing `character.db.domain_scores`; pure function, no write path
3. `world/ability_engine.py` — activation logic: gate checks against subclass_engine, effect dispatch to combat_engine, cooldown writes, OOB push
4. `world/combat_engine.py` — turn sequencing, damage resolution using zone_scaling.py math, calls ability engine for effect application
5. `world/oob_publisher.py` — centralized server→client push for all structured data (status, map, node events)
6. `world/ancestry_engine.py` — applies ancestry stat modifiers and traits at character creation; reads from `character.db.ancestry`
7. `soravelon-client/` — Tauri 2.0 app: EventniaSocket.ts, TerminalPane, MapPanel, StatusPanel, NodeEventPanel
8. `soravelon-builder/` — Tauri 2.0 app: `@xyflow/react` canvas, ZoneSerializer.ts, FileManager.ts writing to `world/areas/*.py`

### Critical Pitfalls

1. **Ability instances stored per-character** — store only a reference (`ability_id`) per character; all definitions live in global registry. Retrofitting this after 90 abilities are authored requires rewriting every one. Must be established before any ability is coded.

2. **Subclass identity collapsing to stat variance** — define a "mechanical fingerprint" (the exclusive gameplay verb) for each of the 10 primary domains before authoring any ability. If an ability could belong to any subclass, it fails. This is the central game design risk.

3. **CmdSet explosion from per-ability commands** — use one generic `CmdUseAbility` dispatcher that takes ability name as argument; never register a separate Evennia `Cmd` class per ability. At 360+ abilities, per-ability commands create CmdSet lookup overhead and name collision constraints.

4. **Evennia `_SaverDict` snapshot drift on ability state** — always use copy-modify-reassign for mutable `character.db` dicts: read into a local `dict()` copy, mutate, write back. Never mutate a `_SaverDict` in place or pass it across function boundaries.

5. **Cross-zone exit silent failure on area load order** — the known bug in `area_builder.py` (alphabetical load order causes cross-zone exits to be silently skipped) must be fixed with two-pass loading before the GUI builder ships. Authors will not see this failure — their zones appear to build successfully but connections are missing.

6. **Client/server protocol coupling** — define a typed OOB envelope format (`{type: "...", payload: {...}}`) before writing any client event handlers. The client must handle unknown types without crashing. This prevents client and server from requiring lockstep releases.

7. **Client memory accumulation in long sessions** — MUD clients run for hours. Implement scrollback buffer cap (5000 lines), virtualized output rendering, and circular message history buffer before the output component is built. Simulated 4-hour session memory test required before launch.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Domain Fingerprints and Ability Foundation

**Rationale:** The ability registry, data model, and subclass engine are prerequisites for every downstream phase. More critically, the 10 domain mechanical fingerprints must be locked before a single ability is authored — retrofitting identity design after 360+ abilities exist is a full rewrite. This phase produces no player-visible features but gates everything else.

**Delivers:** `world/ability_registry.py`, `world/subclass_engine.py`, `world/abilities/` directory structure, `CharacterAbility`/`CharacterGuild` Django models, domain fingerprint document, GTS calculation, migration.

**Addresses:** Ability data model, subclass engine, GTS-tier derivation (FEATURES.md table stakes).

**Avoids:** Per-character ability instances pitfall, subclass identity collapse pitfall (PITFALLS.md critical pitfalls 1 and 2).

**Research flag:** Standard patterns — HIGH confidence. No deeper phase research needed.

---

### Phase 2: Ancestry Engine and Character Creation

**Rationale:** Ancestry has no upstream dependencies and must be resolved before subclass decisions are meaningful to players. It writes to `character.db` once at creation and is read-only thereafter — low risk, low complexity, clears a prerequisite.

**Delivers:** `world/ancestry_engine.py`, 4 ancestry definitions with stat modifiers and passive traits, integration into `typeclasses/characters.py at_object_creation()`.

**Addresses:** Ancestry mechanical traits table-stakes feature (FEATURES.md).

**Avoids:** Ancestry becoming cosmetic-only (named explicitly as table stakes failure mode in FEATURES.md).

**Research flag:** Standard patterns — no phase research needed.

---

### Phase 3: Ability Authoring and Tier Gating

**Rationale:** With registry and fingerprints established in Phase 1, ability definitions can now be authored per subclass. The learn command and trainer NPC deliver the acquisition path. This phase builds out the 90 subclass definitions (even skeleton tier-1 sets) and wires the `CmdUseAbility` dispatcher.

**Delivers:** 90 subclass definition files in `world/abilities/`, `CmdUseAbility` dispatcher, `learn <ability>` command with GTS tier check, trainer NPC type, ability help text, active/passive distinction in data schema.

**Addresses:** Tier-gated ability unlock, learn command, active/passive distinction, signature subclass commands (FEATURES.md P1 features).

**Avoids:** CmdSet explosion pitfall (use dispatcher, not per-ability Cmd classes), mandatory-choice trap (review pass per subclass tier).

**Research flag:** Standard patterns for engine plumbing. The 90-subclass definition content itself is design work — likely needs a focused content-authoring phase within this work that uses the fingerprint doc as guard rail.

---

### Phase 4: Combat Engine Integration

**Rationale:** Cannot build combat without the ability effect dispatch layer in place. Zone scaling math already exists. This phase wires ability effects into the combat tick, integrates passive ability hooks, and adds resource/cooldown enforcement.

**Delivers:** `world/combat_engine.py`, ability effect queue, resource deduction, server-authoritative cooldown checks, zone_scaling.py integration, domain XP award on combat events.

**Addresses:** Basic combat system, passive ability combat math integration (FEATURES.md P1).

**Avoids:** Ability effects called directly inside combat tick (queued events pattern from PITFALLS.md integration gotchas), client-side cooldown trust (server-authoritative enforcement required).

**Research flag:** Evennia contrib cooldowns integration (`evennia.contrib.game_systems.cooldowns`) needs code-level verification during this phase — confirm cooldown state persists across disconnects.

---

### Phase 5: OOB Push Infrastructure and Skill Tracks

**Rationale:** The OOB publisher is the prerequisite for every client panel. It can be built in parallel with or after combat since the protocol is known. Skill tracks (0-100 proficiencies) are low-risk extensions of the existing `CharacterSkill` model and slot naturally here before client work begins.

**Delivers:** `world/oob_publisher.py` with push_status, push_map_update, push_node_event functions; 4 general proficiency skill tracks wired to domain XP accumulation; OOB push hooks in character login and combat events.

**Addresses:** Server-side OOB push for stats (FEATURES.md MVP prerequisite), 4 general proficiency skill tracks, room coordinate storage in AreaBuilder (prerequisite for client map).

**Avoids:** OOB types proliferating without a contract — all pushes go through oob_publisher.py, never scattered `character.msg()` calls.

**Research flag:** Standard patterns — Evennia's `character.msg(cmdname=kwargs)` OOB mechanism is well-documented.

---

### Phase 6: Desktop Client Foundation

**Rationale:** With OOB infrastructure live, the client can display live character state from day one. Protocol must be designed before any event handlers are written. This phase establishes the connection layer, terminal pane, and core dashboard.

**Delivers:** `soravelon-client/` Tauri 2.0 repo, `EventniaSocket.ts` with typed OOB message protocol and reconnect logic, `TerminalPane` (xterm.js), `StatusPanel` (HP/resources/domain scores), split input with command history, ANSI rendering, scrollback buffer with 5000-line cap.

**Addresses:** WebSocket connection, scrollback buffer, command history, ANSI, dashboard panel (FEATURES.md P1 client features).

**Avoids:** Client/server protocol coupling pitfall (typed envelopes before first handler), client memory accumulation (scrollback cap in TerminalPane before first line rendered), Tauri WebView platform quirks (test Windows + macOS in this phase, not at release).

**Research flag:** Needs code-level verification of full Evennia OOB/outputfunc message catalog against `evennia/server/portal/webclient.py` — ARCHITECTURE.md flags this as MEDIUM confidence.

---

### Phase 7: Client Map Panel and Area Builder Fix

**Rationale:** Map panel requires room coordinates in AreaBuilder specs (added in Phase 5) and depends on the client foundation (Phase 6). The cross-zone exit two-pass loading fix must be done before GUI builder ships — these two deliverables belong together.

**Delivers:** `MapPanel.tsx` rendering room graph from OOB map_update messages, room x/y coordinate schema in AreaBuilder, two-pass area loading fix in `area_builder.py` (resolves known CONCERNS.md bug).

**Addresses:** Map panel (FEATURES.md P1 high-value client feature), cross-zone exit silent failure fix (PITFALLS.md critical pitfall 9).

**Avoids:** Cross-zone exits silently skipped in GUI builder content, map panel built without room coordinate foundation.

**Research flag:** Two-pass area loading is a targeted fix to existing code — low research need. Map panel OOB message schema should be finalized during Phase 5 OOB design so this phase is just implementation.

---

### Phase 8: GUI Area Builder MVP

**Rationale:** Builder has no server-side dependencies — it writes `.py` files and the server loads them. It should launch after the cross-zone fix (Phase 7) so authors can immediately build cross-zone content without hitting the known bug. This is the content authoring enabler.

**Delivers:** `soravelon-builder/` Tauri 2.0 repo with `@xyflow/react` canvas, room/exit creation and editing, mob placement from template library, zone metadata form, `ZoneSerializer.ts` → AreaBuilder `.py` output, `FileManager.ts` disk writes via Tauri fs plugin, Zod validation before write, contributor mode scope frozen before implementation begins.

**Addresses:** All GUI builder P1 features (FEATURES.md). Contributor mode spec locked.

**Avoids:** Builder scope growth pitfall (contributor mode defined and frozen first), GUI builder → server direct API anti-pattern (file-only contract), exec() security mistake (structured data → server-side validator, never exec user input).

**Research flag:** `@xyflow/react` v12 patterns are well-documented and production-proven (HIGH confidence). Zod schema design for AreaBuilder spec needs a spec document before implementation — write the TypeScript type for AreaSpec first.

---

### Phase Ordering Rationale

- Phases 1-2 are purely foundational — they produce no player-facing features but gate everything downstream. Skipping them causes the highest-cost pitfalls (per-character ability instances, identity collapse).
- Phases 3-4 (ability authoring → combat) are strictly sequential: the registry must exist before abilities are authored, combat must wait for ability effects.
- Phase 5 (OOB + skills) can run in parallel with late Phase 4 combat work — they share no code path.
- Phase 6 (client) unlocks after Phase 5 because the OOB protocol must be defined before any client event handlers are written.
- Phase 7 (map + area builder fix) is sequenced after Phase 6 so map panel has a working client foundation, and after Phase 5 because room coordinates are added to AreaBuilder specs there.
- Phase 8 (GUI builder) comes last on the server side because it depends on the cross-zone fix (Phase 7) and the AreaBuilder spec schema being stable.

### Research Flags

**Needs deeper research during planning:**
- **Phase 4 (Combat):** Evennia contrib cooldowns (`evennia.contrib.game_systems.cooldowns`) — confirm state persistence across disconnects and API for attaching CooldownHandler to Character typeclass.
- **Phase 6 (Client):** Full Evennia OOB/outputfunc message catalog — verify all outputfunc names and payload shapes against webclient.py source before locking the typed protocol document.
- **Phase 3 (Ability authoring):** Subclass mechanical fingerprint design — not a code research question but a design artifact that must exist before implementation. Treat as a required deliverable in the phase, not as something that emerges during coding.

**Standard patterns (skip research-phase):**
- **Phase 1 (Foundation):** Pure Python dataclass registry pattern — well-established, no novel decisions.
- **Phase 2 (Ancestry):** Character creation hook pattern — direct extension of existing `at_object_creation()`.
- **Phase 5 (OOB):** Evennia `character.msg(cmdname=kwargs)` — documented and used by existing contribs.
- **Phase 7 (Map panel):** Two-pass area loading fix — targeted bug fix on known code, standard pattern.
- **Phase 8 (GUI builder):** `@xyflow/react` v12 — HIGH confidence, production-proven.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Tauri 2.0 stable Oct 2024, `@xyflow/react` v12.5.0 confirmed March 2025, server-side stack is fixed. Only gap: xterm.js current version needs pre-implementation verification. |
| Features | MEDIUM | Table stakes derived from Achaea/Discworld/Aardwolf analysis (MEDIUM confidence community sources) and official Mudlet/Evennia docs (HIGH confidence). Competitor feature analysis is solid; specific ability counts and tier thresholds are design decisions, not research findings. |
| Architecture | HIGH | Evennia protocol verified against official docs. Patterns are direct extensions of established soravelon architecture. Main MEDIUM-confidence gap: full OOB outputfunc message catalog needs code-level verification. |
| Pitfalls | HIGH (Evennia-specific), MEDIUM (design) | Evennia `_SaverDict` behavior and CmdSet explosion are well-documented failure modes. Subclass identity collapse and mandatory-choice trap are design risks that cannot be fully addressed by research — they require playtesting. |

**Overall confidence:** MEDIUM-HIGH

### Gaps to Address

- **Full Evennia OOB message catalog:** ARCHITECTURE.md flags this as MEDIUM confidence — the basic text protocol is documented but the complete outputfunc catalog needs verification against `evennia/server/portal/webclient.py` before client event handler implementation. Resolve in Phase 6 planning.
- **Evennia contrib cooldowns persistence:** Whether `CooldownHandler` state survives server reload/disconnect is unverified in research. Resolve in Phase 4 planning before combat is designed around it.
- **xterm.js current version:** STACK.md notes "verify current version before implementation." Low-stakes gap — npm install will resolve it, but confirm API stability before building TerminalPane.
- **AreaBuilder spec TypeScript type:** The Zod schema for the builder's area spec output must be formally defined before Phase 8 implementation begins. This is a design artifact, not a research question.
- **Subclass mechanical fingerprints:** 10 domain fingerprints need to be authored as a design document before Phase 3. This is the highest-risk gap — it is a creative design task, not something research can pre-solve.

## Sources

### Primary (HIGH confidence)
- Tauri 2.0 official docs — https://v2.tauri.app/plugin/websocket/ — WebSocket plugin API, permissions model
- Tauri 2.0 stable release — https://v2.tauri.app/blog/tauri-20/ — confirmed stable Oct 2024
- `@xyflow/react` v12.5.0 release — https://reactflow.dev/whats-new/2025-03-27 — confirmed current March 2025
- Evennia Webclient docs — https://www.evennia.com/docs/latest/Components/Webclient.html — JSON protocol format
- Evennia Messagepath docs — https://www.evennia.com/docs/latest/Concepts/Messagepath.html
- Evennia Traits contrib — https://www.evennia.com/docs/latest/Contribs/Contrib-Traits.html — rejected for ability system
- Evennia Attributes docs — https://www.evennia.com/docs/latest/Components/Attributes.html — SaverDict behavior
- Mudlet Manual — https://wiki.mudlet.org/w/Manual:Supported_Protocols — client feature baseline
- Achaea class system — https://www.achaea.com/front — tier gate and ability count comparison
- Discworld MUD guilds/skills — https://discworld.starturtle.net/lpc/playing/guilds.html — progression model comparison
- Aardwolf skills — https://www.aardwolf.com/v3/v3magic.html — class/subclass comparison

### Secondary (MEDIUM confidence)
- Tauri vs Electron 2025 comparisons — bundle size and memory figures (multiple sources agree on order of magnitude)
- Zustand vs Redux 2025 — https://betterstack.com/community/guides/scaling-nodejs/zustand-vs-redux/ — solo-dev consensus
- MUD Coders Guild progression design — https://mudcoders.com/off-the-cliff-ep5-progression — practitioner analysis
- GDKeys skill tree design — https://gdkeys.com/keys-to-meaningful-skill-trees/ — mandatory-choice trap analysis
- Soravelon CONCERNS.md — `.planning/codebase/CONCERNS.md` — cross-zone exit bug, SaverDict patterns confirmed in codebase

### Tertiary (LOW confidence)
- Lusternia crafting professions — game website, thin documentation; profession feature count used as reference only
- Online Creation (OLC) overview — MUD community wiki; builder feature expectations cross-referenced with other sources

---
*Research completed: 2026-03-24*
*Ready for roadmap: yes*
