# Pitfalls Research

**Domain:** Evennia MUD — large ability/class system, desktop client, GUI world builder
**Researched:** 2026-03-24
**Confidence:** HIGH (Evennia-specific), MEDIUM (ability system design), MEDIUM (client/tooling)

---

## Critical Pitfalls

### Pitfall 1: Ability Instances Stored Per-Character (The "Object Per Ability" Trap)

**What goes wrong:**
Abilities are implemented as Evennia objects (or dicts) stored directly on each character's `db` attributes. Each character has their own copy of every ability definition. When you need to change an ability's damage formula, cooldown, or description, you must iterate every character in the database and patch their individual copy — or accept that existing characters run outdated code.

**Why it happens:**
The naive Evennia approach to "give a character an ability" is to create an object and store it. It mirrors how inventory and equipment work. It feels right during early development when you only have a few test characters.

**How to avoid:**
Store ability **definitions** in a module-level registry or Django model (global, versioned). Characters store only a reference: `{ability_id: rank, unlocked: True}`. The ability engine resolves the definition at resolution time. Balance changes propagate immediately to all characters without a migration.

**Warning signs:**
- Ability logic lives inside `at_object_creation()` on a per-character basis
- A "balance patch" requires a migration script that touches every character
- You find yourself writing `for char in all_characters: char.db.abilities['fireball']['damage'] = 40`

**Phase to address:**
Ability system foundation phase — the data model must be defined before any ability is authored. Retrofitting this after 90+ abilities are implemented requires rewriting every one.

---

### Pitfall 2: Subclass Identity Collapsing to Stat Variance

**What goes wrong:**
90 subclasses exist on paper, but in practice most feel like "the same character with different numbers." A Duskblade and a Thornguard both hit things, both have a DoT, both have a defensive cooldown — the labels differ but the texture of play is identical. The game's central value proposition fails silently: character identity is a loading screen description, not a felt experience.

**Why it happens:**
When building 90 subclasses under time pressure, it is easy to reach for the same mechanical vocabulary (damage, DoT, CC, defensive) and vary only the flavor. Domain combination drives the *lore* of identity but not the *mechanics* unless each domain contributes a genuinely distinct gameplay verb.

**How to avoid:**
Define a "mechanical fingerprint" for each of the 10 primary domains before authoring any abilities: what is the core loop verb that only this domain has? (e.g., Combat = resource-building through hits; Subterfuge = positional state tracking; Naturalism = summon/persistent entity management). Subclass abilities must use the fingerprint verbs of both constituent domains. If an ability could belong to any subclass, it fails the fingerprint test.

**Warning signs:**
- Two subclasses in different domain combinations have identical ability lists except for damage type
- Abilities are designed as "Combat + Subterfuge version of Fireball" rather than "what does a Duskblade *do* that no one else can"
- Playtesters describe different subclasses as "basically the same"

**Phase to address:**
Before ability authoring begins — fingerprint design should precede any individual ability implementation.

---

### Pitfall 3: The Single Dominant Ability (Mandatory-Choice Trap)

**What goes wrong:**
One tier-1 or tier-2 ability in a subclass is so much better than its alternatives that every player of that subclass takes it, making the "choice" illusory. The remaining abilities exist only as trap options. Over time players learn which abilities are mandatory and the subclass loses perceived depth.

**Why it happens:**
In a 360+ ability system designed quickly, the designer cannot playtest every combination. Abilities with consistent uptime, unconditional triggers, or multiplicative scaling will crowd out conditional or niche options without the designer noticing.

**How to avoid:**
At each tier, ensure no single ability has >80% theoretical pick rate. Use the rule: each ability in a tier should be optimal for at least one clearly-describable playstyle. Mark abilities that grant permanent passive bonuses with extra scrutiny — they are the most likely to be mandatory.

**Warning signs:**
- Ability description says "always" or "on every hit" (unconditional = high pick rate)
- An ability has no meaningful tradeoff or activation condition
- All other abilities in the tier require setup, this one does not

**Phase to address:**
Ability authoring phase — a review pass for each subclass before finalizing its tier structure.

---

### Pitfall 4: Evennia CmdSet Explosion from Ability Commands

**What goes wrong:**
Each ability gets its own `Cmd` class and is added to the character's CmdSet dynamically. A character with 20 active abilities now has 20+ custom commands registered. Evennia's CmdSet merge algorithm runs on every command input — with large numbers of CmdSets, command lookup becomes measurably slower. More critically, command name collision becomes a constant design constraint (you can't have two abilities called "strike").

**Why it happens:**
Evennia's natural pattern is one command per action. It works fine for small command sets. With 360+ abilities across 90 subclasses, it breaks down as a design assumption.

**How to avoid:**
Use a dispatcher pattern: one `CmdUseAbility` command (or `cast`, `use`, `activate`) that takes the ability name as an argument. Ability resolution happens in Python, not in Evennia's CmdSet layer. This keeps the CmdSet small regardless of how many abilities a character unlocks. Example: `cast shadowstep` rather than `shadowstep` as a standalone command.

**Warning signs:**
- Planning to auto-register a command for each unlocked ability
- Ability names are being chosen to avoid conflicts with existing commands
- Command documentation will require players to type `help` to see their own abilities

**Phase to address:**
Combat/ability command architecture — before any ability commands are wired up.

---

### Pitfall 5: Evennia db Attribute Snapshot Drift on Ability State

**What goes wrong:**
Ability cooldown timers, charges, and active buff stacks are stored as mutable dicts in `character.db.ability_state`. Code retrieves this dict into a local variable, mutates it, and expects the mutation to persist. But Evennia's `_SaverDict` creates a snapshot on retrieval — multiple references to the same attribute diverge silently, and mutations through stale snapshots are lost.

**Why it happens:**
Evennia documents this behavior but it is easy to miss when writing complex ability resolution code across multiple function calls. The bug is invisible during testing with single characters and only surfaces under real gameplay conditions.

**How to avoid:**
Follow the copy-modify-reassign pattern for all mutable ability state: `state = dict(character.db.ability_state); state['cooldowns']['shadowstep'] = tick + 5; character.db.ability_state = state`. Never hold references to `_SaverDict` objects across function boundaries. Treat `db` attribute reads as immutable snapshots.

**Warning signs:**
- Cooldown timers that do not persist across ticks
- Buff stacks that randomly reset
- Code that passes `character.db.ability_state` as a function argument and mutates it inside

**Phase to address:**
Ability state management design — addressed in the first phase that introduces persistent ability state (cooldowns, charges, buffs).

---

### Pitfall 6: Desktop Client Built for Current Server Protocol, Not Future Protocol

**What goes wrong:**
The client is wired to the exact message format and event names that the server emits today. When the server adds new events (node failures, ability animations, NPC dialogue) the client requires a matching code change to handle them. Client and server become tightly coupled and must be released in lockstep. The "separate repo / clean separation" design goal is violated in practice.

**Why it happens:**
During early client development, the fastest path is to match the exact messages the server currently sends. Protocol abstraction feels like premature engineering.

**How to avoid:**
Define a versioned message protocol document before the client is built. Messages should be typed envelopes: `{type: "node_state_change", payload: {...}}`. The client renders unknown message types without crashing (graceful degradation). Server emits structured events, not ad-hoc strings. Even a simple v1 protocol with a handful of typed event categories prevents the worst coupling.

**Warning signs:**
- Client code has literal string comparisons against server output (e.g., `if msg.startswith("The node is failing")`)
- Adding a new server event requires a client code change to avoid a crash
- Client and server changelogs are coupled

**Phase to address:**
Client foundation phase — protocol design must precede any event handler implementation.

---

### Pitfall 7: Tauri's Platform-Specific WebView Behavior Breaking Client UI

**What goes wrong:**
Tauri uses the OS-native WebView (WebKit on macOS, WebView2 on Windows, WebKitGTK on Linux). CSS and JavaScript that works perfectly in Chrome may render incorrectly on macOS WebKit or fail silently on Linux. A MUD client with rich ANSI rendering, custom fonts, or animated node indicators discovers platform-specific rendering bugs late in development.

**Why it happens:**
Development typically happens on one platform (Windows or macOS). Cross-platform quirks only surface when testing on other platforms or when users report them.

**How to avoid:**
Test the UI on all three platforms early (not just before release). Restrict CSS to well-supported properties — avoid cutting-edge features not in the WebView2/WebKit baseline. Use a CSS reset. Treat the WebView as IE-era "unknown browser" rather than Chrome. If UI consistency is critical, Electron's single Chromium engine eliminates this entire problem at the cost of bundle size.

**Warning signs:**
- Only testing on one platform during development
- Using CSS features that require Chrome-specific prefixes
- Custom font rendering that has not been validated on macOS WebKit

**Phase to address:**
Client prototype phase — set up CI testing on Windows and macOS before the UI is finalized.

---

### Pitfall 8: GUI Area Builder Scope Grows to Match Developer Needs, Not Author Needs

**What goes wrong:**
The GUI builder starts as a tool for non-developer zone authors. Over time, developer-convenience features accumulate: bulk operations, scripted spawn patterns, node configuration panels, cross-zone reference browsers. The tool becomes powerful but intimidating. Non-developer authors cannot navigate it without a tutorial. The original goal of enabling non-dev content creation at scale is not achieved.

**Why it happens:**
The builder is being built by a developer (solo). Developer instincts optimize for power and flexibility. Non-developer usability requires active restraint — deliberately limiting what the UI exposes, and sequencing features by author workflow rather than implementation convenience.

**How to avoid:**
Define two user modes explicitly before building: "Owner mode" (full access, developer-grade) and "Contributor mode" (constrained authoring, opinionated workflows). Build contributor mode first with the smallest viable feature set. Owner mode is just contributor mode with additional panels unlocked. Test contributor mode against a non-developer mental model of "I want to place a room, describe it, and add a mob" before adding anything else.

**Warning signs:**
- Builder UI has more than 5 visible panels in contributor mode
- The first-use experience requires reading documentation
- Features are added because "it would be useful" rather than because a specific authoring workflow requires them

**Phase to address:**
GUI builder MVP phase — contributor-mode scope should be defined and frozen before implementation begins.

---

### Pitfall 9: Cross-Zone Exit Resolution Silently Fails on Area Load Order

**What goes wrong:**
This pitfall already exists in the codebase (documented in CONCERNS.md). Zone A references a room in Zone B, but Zone B loads after Zone A (alphabetical file order). The cross-zone exit is silently skipped with a warning. On next restart, it may or may not resolve depending on filename sorting. Authors building content via the GUI builder will not see this failure — their zone will appear to build successfully but connections to other zones will be missing.

**Why it happens:**
`area_builder.py` processes cross-zone exits immediately at build time without a two-pass resolution stage. Files are sorted alphabetically, creating an implicit load order dependency.

**How to avoid:**
Implement two-pass area loading: pass 1 builds all rooms and local exits; pass 2 resolves all cross-zone exits after all zones are loaded. This makes load order irrelevant. The GUI builder should surface cross-zone connection status explicitly rather than silently succeeding.

**Warning signs:**
- Area file naming conventions that hint at load order (e.g., `00_hub.py`, `01_zone.py`)
- Build output logs show "skipped cross-zone exit" warnings
- Players report missing exits after server restart

**Phase to address:**
Area builder fix phase — must be resolved before GUI builder content authoring begins, because authors will be creating cross-zone connections.

---

### Pitfall 10: Electron Memory Accumulation in Long-Running MUD Sessions

**What goes wrong:**
A MUD client is a long-running application — players may leave it open for hours or days. Electron applications accumulate memory over time due to retained renderer state, WebSocket message history in DOM, and Chromium's GC behavior. A client that starts at 150MB RAM grows to 1GB+ after a long session. Players with lower-end machines notice the client slowing down or crashing.

**Why it happens:**
MUD clients append text to a scrollback buffer continuously. Without explicit DOM pruning, the renderer's document grows unbounded. Electron does not garbage-collect DOM nodes that are no longer visible in the viewport.

**How to avoid:**
Implement scrollback buffer limits (e.g., max 5,000 lines in DOM). Virtualize the output window — render only visible lines, not the full history. Use a circular buffer for message history. Test memory usage after simulating 4 hours of gameplay (automated message injection) before launch.

**Warning signs:**
- Output pane implemented as a simple `div` with `innerHTML +=` for each message
- No scrollback limit or history cap defined
- Memory testing only done at startup, not after extended sessions

**Phase to address:**
Client output rendering phase — scrollback architecture must be decided before the output component is built.

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hardcode ability effects as Python functions | Fast to implement, no indirection | Rebalancing requires code deploys; impossible to expose to non-devs | Never for a 360+ ability system |
| Store ability state as flat `db.ability_cooldowns` dict | Simple reads/writes | SaverDict snapshot drift; no schema; hard to add new state fields | MVP only if immediately replaced |
| One Cmd class per ability | Familiar Evennia pattern | CmdSet explosion, name conflicts, slow lookup with 20+ abilities | Never at this scale |
| Build GUI builder for developer use first | Faster to build | Non-developer UX never gets prioritized; contributor mode never ships | Only if no non-dev authors planned |
| Skip message protocol versioning | Ship client faster | Client and server must be updated in lockstep; breaks clean separation | Never — define protocol types upfront |
| Append all output to DOM directly | Simple implementation | Memory accumulation in long sessions; client degrades over time | Never for a long-running client |

---

## Integration Gotchas

Common mistakes when connecting the client, server, and tools.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Evennia WebSocket → Client | Parsing raw Evennia `msg` strings with string matching | Define typed JSON envelopes server-side; client pattern-matches `type` field |
| Tauri IPC ↔ WebSocket | Routing all server messages through Tauri IPC commands (serialization overhead) | Connect the WebSocket directly from the frontend renderer; use Tauri IPC only for system-level calls (window management, file save) |
| GUI Builder → area_builder.py | GUI emits Python code strings for exec() | GUI builds structured data (dict/JSON); server-side validator converts to area spec; never exec user input |
| Client ↔ Server reconnect | No reconnect logic, assuming stable connection | Implement exponential backoff reconnect in client; server should send a "welcome back" state-sync packet on reconnect |
| Ability engine ↔ Combat system | Ability effects called directly inside combat tick | Ability effects should be queued events processed after tick resolution to avoid mid-tick state mutation |

---

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Resolving ability definitions from `character.db` on every cast | Ability cast lag increases as more abilities are added | Cache ability definition registry in module-level dict; resolve once at server start | Noticeable at 50+ casts/second across all players |
| Tick-driven buff expiration that scans all characters | Server tick lag spikes every N seconds | Track active buffs in a priority queue keyed by expiration tick; only process expired entries | 200+ concurrent players with active buffs |
| GUI builder loading all zone data on open | Builder startup slow; memory spikes | Lazy-load zones on demand; only load zone being edited | 50+ zones in the game |
| Client rendering all scrollback on reconnect | Client freezes for 2-3 seconds after reconnect | Only replay last N lines on reconnect; full history in memory-only circular buffer | Scrollback > 1,000 lines |
| Evennia `search_tag` for ability lookup | Slow with many tagged objects | Never tag ability instances on characters; use Python registry or Django model | 500+ tagged ability objects |

---

## Security Mistakes

Domain-specific security issues.

| Mistake | Risk | Prevention |
|---------|------|------------|
| GUI builder that sends ability/zone data as Python code to the server | Arbitrary code execution on server | Builder sends structured data only; server validates against a strict schema before applying |
| Client ability invocation that sends ability_id without server-side authorization check | Players invoke abilities they have not unlocked by crafting WebSocket messages | Server authorizes every ability use against character's unlocked ability list, never trusting client state |
| Ability state stored in client and synced to server | Client can manipulate cooldowns, charges, or buff stacks | All authoritative ability state lives server-side; client is display-only |
| Banking rate limiting absent (already documented in CONCERNS.md) | Scripted client can spam transactions | Add cooldown via `ndb` timestamp before banking commands are registered |

---

## UX Pitfalls

Common user experience mistakes in this domain.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Subclass abilities revealed all at once at character creation | Players choose subclass without understanding what it means; choice feels arbitrary | Progressive reveal: show tier 1 abilities at creation, unlock tier 2 preview at GTS 10 |
| GUI builder contributor mode exposes all developer options | Non-developer authors feel lost; make mistakes that break zone integrity | Contributor mode is a separate, constrained UI — not developer mode with a permission filter |
| Client output has no visual distinction between ability results, system messages, and NPC dialogue | Players cannot quickly parse combat feedback | Defined color/style protocol per message category; consistent from day one |
| Ability help text written by the developer, not the player | Dense mechanical descriptions; players don't know what to do | Write from the player's perspective: "when to use this" first, "what it does" second |
| Cross-zone exits that silently fail (already in CONCERNS.md) | Players discover missing connections during play | Build-time validation that surfaces connection failures as errors, not warnings |

---

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Ability system:** Engine resolves ability effects but has no server-authoritative cooldown enforcement — verify cooldowns are checked server-side before ability execution, not just client-side
- [ ] **Subclass registration:** 90 subclasses exist in registry but have no abilities authored yet — verify each subclass has at least one tier-1 ability before declaring "ability system complete"
- [ ] **GUI builder:** Tool creates valid area spec files but cross-zone exits only work if zones load in correct order — verify two-pass loading is implemented before GUI builder ships
- [ ] **Desktop client:** Client connects and displays text but has no reconnect logic — verify automatic reconnect with state sync works before calling client "done"
- [ ] **Ability balance:** Abilities have been designed but not stress-tested for mandatory-choice traps — verify each tier has no single dominant option before locking the subclass
- [ ] **Combat integration:** Ability effects are implemented but not hooked into the combat tick — verify abilities actually fire during combat, not just in isolation tests
- [ ] **Client memory:** Client renders correctly in a 5-minute session — verify memory is stable after a simulated 4-hour session before release

---

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Per-character ability instances (if shipped) | HIGH | Write migration script to extract all ability state from character db, build global registry, replace per-character instances with references; test every subclass after migration |
| Subclass identity collapse (discovered late) | HIGH | Requires ability redesign — the mechanical fingerprint work should have happened earlier; add a "uniqueness review" phase before any abilities are published to players |
| CmdSet explosion (if commands registered per ability) | MEDIUM | Refactor to dispatcher pattern; update all ability-triggering code to route through `CmdUseAbility`; keep old per-ability commands as aliases during transition |
| Client/server protocol coupling | MEDIUM | Define typed envelope format; add a normalization layer in server that wraps existing messages in envelopes without changing message content; update client to unwrap envelopes |
| DOM memory accumulation (discovered post-release) | LOW | Add scrollback cap and DOM pruning; ship as a patch; players will notice improvement immediately |
| Cross-zone exit failures (already exists) | LOW | Implement two-pass loading; no migration needed since no content exists yet |

---

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Ability instances stored per-character | Ability system foundation (before any ability authored) | Confirm: ability effects resolve from a global registry, not character db |
| Subclass identity collapse | Domain fingerprint design (before ability authoring) | Confirm: each domain has a documented "mechanical verb" that is exclusive to it |
| Mandatory-choice trap | Ability authoring + review pass | Confirm: no tier has a single ability with unconditional uptime bonus and no tradeoff |
| CmdSet explosion | Ability command architecture (before first ability command) | Confirm: ability dispatch uses single command + argument, not per-ability commands |
| SaverDict snapshot drift | Ability state management design | Confirm: all mutable ability state uses copy-modify-reassign pattern |
| Client/server protocol coupling | Client foundation (before first event handler) | Confirm: server emits typed JSON envelopes; client handles unknown types gracefully |
| Tauri platform WebView rendering | Client prototype phase | Confirm: UI tested on Windows and macOS before UI is finalized |
| GUI builder scope growth | GUI builder MVP scope freeze | Confirm: contributor mode spec is locked and written down before implementation |
| Cross-zone exit silent failure | Area builder fix (before GUI builder ships content) | Confirm: two-pass loading implemented; cross-zone exits verified in tests |
| Electron memory accumulation | Client output rendering phase | Confirm: scrollback has explicit cap; memory measured after simulated long session |

---

## Sources

- Evennia Attributes documentation: https://www.evennia.com/docs/latest/Components/Attributes.html
- Evennia ainneve ability system design discussion: https://github.com/evennia/ainneve/issues/31
- D&D 5e 2024 class design pitfalls: https://forum.rpg.net/index.php?threads/d-d-5th-ed-2024-class-design-pitfalls.933193/
- Keys to Meaningful Skill Trees (GDKeys): https://gdkeys.com/keys-to-meaningful-skill-trees/
- Tauri WebSocket plugin: https://v2.tauri.app/plugin/websocket/
- Tauri IPC architecture: https://v2.tauri.app/concept/inter-process-communication/
- Electron vs Tauri comparison (DoltHub, 2025): https://www.dolthub.com/blog/2025-11-13-electron-vs-tauri/
- Electron memory leak issues: https://github.com/electron/electron/issues/37569
- Scalable data-driven RPG design: https://www.gamedev.net/forums/topic/699311-scalable-data-driven-design-for-rpg/
- MMORPG power creep and class identity: https://forums.mmorpg.com/discussion/355252/design-the-perfect-class-system
- Soravelon CONCERNS.md: .planning/codebase/CONCERNS.md (cross-zone exit bug, SaverDict patterns, getattr anti-pattern)

---
*Pitfalls research for: Evennia MUD — ability system, desktop client, GUI world builder*
*Researched: 2026-03-24*
