# Stack Research

**Domain:** Evennia MUD — guild/ability system, desktop client, GUI zone builder
**Researched:** 2026-03-24
**Confidence:** MEDIUM (Ability system: HIGH — pure Python, no external deps. Client: MEDIUM — Tauri 2.0 is stable but MUD-specific usage is thin in docs. Builder: MEDIUM — React Flow is well-proven but zone-builder patterns are custom-built.)

---

## Context

This is a **subsequent-milestone** research note. The Evennia 6.0 server stack (Python 3.12, Django 6.0.3, Twisted 24.11.0) is fixed and not re-evaluated here. Three new subsystems need a stack decision:

1. **Ability system** — pure Python, lives in `world/` on the existing server
2. **Desktop client** — separate repo, connects to Evennia via WebSocket
3. **GUI zone builder** — separate tool, writes area spec `.py` files or calls a server API

---

## Recommended Stack

### 1. Ability System (Server-Side Python)

No external dependencies are needed or recommended. The ability system is pure game logic that belongs in `world/` like every other engine.

#### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python dataclasses | stdlib (3.12) | Immutable ability definitions | Dataclasses give `__repr__`, `__eq__`, slots, and frozen mode for free. Ability definitions are read-only config — freeze them. No ORM overhead, no serialization quirks. |
| Django ORM | 6.0.3 (existing) | Persisting which abilities a character has unlocked | Existing infrastructure. One new model (`CharacterAbility`) fits cleanly alongside `CharacterSkill` in `world/models.py`. |
| Evennia `db` attributes | Evennia 6.0 | Persisting cooldown state and active ability effects | Fast read path. Cooldown expiry timestamps stored as `character.db.ability_cooldowns` dict — same pattern as domain scores. |
| Evennia Traits contrib | Evennia 6.0 bundled | **Do NOT use for abilities** — see below | Listed to explicitly reject: Traits are for scalar stats (HP, STR). Using them for 360 abilities would create 360 attribute keys per character, making queries and resets expensive. |

#### Ability Engine Pattern

Store ability **definitions** as frozen dataclasses in `world/ability_defs.py` — pure Python dicts keyed by `ability_id`. Store **ownership** (which abilities a character has unlocked) in a Django model. Store **runtime state** (cooldowns, charges) on `character.db`. This mirrors how mob affixes are structured: definitions in `world/mob_affixes.py`, runtime state on the mob object.

```
world/
  ability_defs.py        # Frozen dataclasses: id, name, tier, domain, subclass, cost, cooldown, effect_fn
  ability_engine.py      # use_ability(), is_available(), get_unlocked_abilities()
  guild_engine.py        # join_guild(), advance_tier(), compute_guild_tier_score()
  subclass_registry.py   # 90 subclass definitions (domain_primary + domain_secondary → subclass)

world/models.py          # + CharacterAbility(character, ability_id, unlocked_at)
                         # + CharacterGuild(character, domain_primary, domain_secondary, tier)
```

**Confidence:** HIGH — this directly extends the established pattern. No new dependencies.

#### Skill System (General Proficiencies)

Same pattern. `world/skill_engine.py` + `CharacterSkill` model (already exists in `world/models.py` per architecture doc). Proficiency 0-100 stored as `character.db.skill_scores` dict, same as `domain_scores`.

---

### 2. Desktop Client (Separate Repo)

**Recommendation: Tauri 2.0 + React 19 + TypeScript + Vite 6**

#### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Tauri | 2.0 (stable Oct 2024) | Desktop app shell | Installers under 10 MB vs Electron's 80–120 MB. Idle memory 30–50 MB vs Electron's 200–500 MB. Uses native OS WebView (WebView2 on Windows, WebKit on macOS). Rust core with explicit security permissions. Production-stable since Oct 2024, adoption up 35% YoY. |
| React | 19.x | UI framework | Dominant ecosystem, best Tauri template support, solo developer already working in TypeScript ecosystem. React 19 concurrent features help with streaming MUD text output. |
| TypeScript | 5.x | Type safety | Non-negotiable for a solo developer maintaining a complex client. Catches protocol mismatches at compile time. |
| Vite | 6.x | Build tooling | Tauri's official scaffolding uses Vite. Sub-second HMR. `npm create tauri-app` generates this stack. Vite 8 available but Vite 6 is the current Tauri-template baseline. |
| `@tauri-apps/plugin-websocket` | latest (updated Nov 2025) | WebSocket to Evennia | Tauri's native WebSocket plugin uses a Rust client (not the browser WebSocket API). Explicit `allow-connect` / `allow-send` permissions required in capabilities config. |

#### Evennia WebSocket Protocol (what the client must speak)

Evennia's webclient protocol is JSON over WebSocket. Messages are 3-element arrays:

- **Client → Server:** `["inputfunc_name", [args], {kwargs}]`
  - Most common: `["text", ["look"], {}]` — sends a command
- **Server → Client:** Same structure, but outputfunc name
  - Most common: `["text", ["You see darkness."], {}]`

Default WebSocket port: `4002` (Portal, not the web port 4001). The custom client connects to `ws://host:4002` directly. No additional library is needed — `@tauri-apps/plugin-websocket` handles the connection; JSON parsing is stdlib.

**Confidence:** MEDIUM — Evennia's exact OOB/outputfunc message catalog needs verification against `evennia/server/portal/webclient.py` during implementation. The basic text protocol is HIGH confidence (documented).

#### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Zustand | 5.x | Client state (connection status, game output buffer, character dashboard data) | Use instead of Redux. 1 KB, hooks-native, no boilerplate. Solo dev, medium complexity — Redux is overkill. |
| shadcn/ui | latest | UI component primitives (panels, tabs, scrollable output) | Copy-paste components, not a runtime dependency. Works with Tailwind. Avoid full Radix install just for this. |
| Tailwind CSS | 4.x | Styling | Standard for Vite/React in 2025. Works out-of-the-box with Tauri templates. |
| xterm.js | 5.x | Terminal emulator widget for raw MUD text pane | Purpose-built for terminal output. Handles ANSI codes, scrollback buffer, font rendering. Use for the primary text output area. |

**Confidence for xterm.js:** MEDIUM — training data. Verify current version before implementation.

#### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `npm create tauri-app` | Project scaffolding | Generates Tauri 2.0 + React 19 + TypeScript + Vite structure out of the box |
| electron-builder | **Do NOT use** — see Alternatives | Listed to flag: this is for Electron, not Tauri |
| Rust toolchain (rustup) | Required by Tauri | Minimum Rust 1.77.2. Install via `rustup`. Developer does not write Rust — Tauri's Rust layer is config-only for this use case. |

---

### 3. GUI Zone Builder Tool (Separate Repo)

**Recommendation: Tauri 2.0 + React 19 + TypeScript + @xyflow/react + same base as client**

The zone builder is a **separate desktop tool** — not part of the game client and not embedded in the Evennia server. It produces area spec `.py` files (or calls a server management API) that feed the existing `AreaBuilder` pipeline.

#### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Tauri | 2.0 | Desktop shell | Same rationale as client. File system access (writing `.py` area specs to disk) requires `tauri-plugin-fs` — available in Tauri 2.0 plugin ecosystem. |
| React | 19.x | UI framework | Same codebase conventions as client. Potential to share component library. |
| TypeScript | 5.x | Type safety | Area spec schema must be validated before writing — TypeScript catches shape errors. |
| `@xyflow/react` | 12.5.0 (Mar 2025) | Visual room/exit graph canvas | This is the critical dependency. React Flow (now `@xyflow/react` v12) is the standard for node-based editors in React. Powers Stripe's and Typeform's internal tools. Features: drag-to-connect exits, custom node types (rooms, exits, mobs), canvas pan/zoom. Actively maintained — v12.5.0 shipped March 27, 2025. |
| Vite | 6.x | Build tooling | Same as client |
| Zustand | 5.x | Builder state (selected room, pending changes, zone metadata) | Same rationale as client |
| `tauri-plugin-fs` | Tauri 2.0 bundled | Write area spec `.py` files to disk | Required for the builder's core output path |
| `tauri-plugin-dialog` | Tauri 2.0 bundled | Open/save file dialogs | Standard Tauri 2.0 plugin |

**Confidence for @xyflow/react:** HIGH — verified current version (12.5.0, March 2025), actively maintained, multiple production deployments.

#### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| shadcn/ui | latest | Property panels, form inputs for room/mob editing | Same as client — copy-paste components |
| Tailwind CSS | 4.x | Styling | Same as client |
| Zod | 3.x | Runtime schema validation of area spec before writing to disk | Prevent corrupt `.py` files reaching AreaBuilder. Validate room IDs, exit directions, mob templates at save time. |

---

## Installation

### Ability System (server — no new packages)

No `pip install` required. Pure Python dataclasses + existing Django ORM.

```bash
# New models only — run after adding CharacterAbility, CharacterGuild to world/models.py
evennia migrate
```

### Desktop Client (new repo)

```bash
# Scaffold
npm create tauri-app@latest soravelon-client -- --template react-ts

# WebSocket plugin
npm install @tauri-apps/plugin-websocket
# Add to Cargo.toml: tauri-plugin-websocket = "2"

# State + UI
npm install zustand xterm
npm install -D tailwindcss @tailwindcss/vite

# shadcn (copy-paste, run once)
npx shadcn@latest init
```

### GUI Zone Builder (new repo)

```bash
# Scaffold (same template)
npm create tauri-app@latest soravelon-builder -- --template react-ts

# Node canvas
npm install @xyflow/react

# Validation
npm install zod

# State + UI (same as client)
npm install zustand
npm install -D tailwindcss @tailwindcss/vite

# shadcn
npx shadcn@latest init
```

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Tauri 2.0 | Electron 41 | If the developer already has a Node.js-heavy server-side process embedded in the client, or needs the full Chromium rendering engine for complex CSS. Electron is 10× larger on disk and 4–10× higher memory at idle. Not justified here. |
| `@xyflow/react` v12 | React Flow v11 (`reactflow`) | Never — v11 is the legacy package. v12 (`@xyflow/react`) is the current package. Do not install `reactflow`. |
| Tauri `tauri-plugin-websocket` | Browser native WebSocket API | Browser WebSocket works only in Tauri's webview frontend context. The plugin routes through Rust and grants explicit IPC permissions — use the plugin, not raw `new WebSocket()`, to stay within Tauri's security model. |
| Zustand | Redux Toolkit | Redux if the client grows to have >5 developers and complex side effects needing middleware. Overkill for a solo developer with medium-complexity state. |
| Python dataclasses for ability defs | Evennia Traits contrib | Traits if tracking a small number of scalar stats (STR, DEX). For 360+ ability definitions across 90 subclasses, Traits create one Attribute key per ability per character — O(n) attribute reads per lookup vs O(1) dict access. Wrong tool. |
| Dedicated zone builder tool | In-game `@dig` / `@create` commands | In-game commands for ad-hoc fixes only. The GUI builder is the primary authoring path because it produces area spec `.py` files that feed AreaBuilder's idempotent build pipeline — not raw DB object creation. |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| `reactflow` (npm package) | Legacy v11 package, deprecated in favor of `@xyflow/react`. Will not receive new features. | `@xyflow/react` v12 |
| Electron for the client | 80–120 MB installer, 200–500 MB idle memory, no technical advantage over Tauri 2.0 for this use case. | Tauri 2.0 |
| Evennia Traits contrib for abilities | Designed for 5-20 scalar stats per character. 360 ability entries per character as Attribute keys is slow to query, expensive to reset, and bypasses the established world-engine pattern. | Python dataclasses in `world/ability_defs.py` + Django model for ownership |
| New `pip` packages for ability system | The ability engine is pure game logic. Adding deps like `attrs`, `pydantic`, or `transitions` adds fragile version pinning to a project that currently runs with zero lockfile. | Python stdlib dataclasses + existing Django ORM |
| Redux for client state | Significant boilerplate, complex setup, no benefit over Zustand for a solo-developer medium-complexity client. | Zustand 5.x |
| Writing area specs via a server REST API (from builder) | Adds an API surface that must be authenticated, versioned, and kept in sync with AreaBuilder schema. File-based output (Tauri `tauri-plugin-fs`) is simpler and matches the existing `world/areas/*.py` pattern. | Write `.py` files directly via Tauri fs plugin |

---

## Stack Patterns by Variant

**If the zone builder needs to preview live zone state (not just author static specs):**
- Add a WebSocket connection (same `@tauri-apps/plugin-websocket` approach as the client)
- The builder connects to the dev server and queries zone/room state via OOB messages
- Do NOT implement this in Milestone 1 — static file output is sufficient

**If the desktop client needs to display a map:**
- Use `@xyflow/react` inside the client for the map pane (shared dep with builder)
- Rooms as nodes, exits as edges — same library, different use case
- Server sends room graph via OOB outputfunc; client renders it as a read-only flow canvas

**If the client eventually needs sound/audio:**
- Use `tauri-plugin-shell` to invoke system audio, or the Web Audio API directly in the webview
- Do NOT add Electron for this — WebKit WebView has full Web Audio API support on Windows 10+

---

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| `@tauri-apps/plugin-websocket` latest | Tauri 2.0, Rust 1.77.2+ | Plugin was updated November 2025. Requires explicit capability permissions in `src-tauri/capabilities/`. |
| `@xyflow/react` 12.5.0 | React 18+, React 19 | Confirmed React 19 compatible. Do not mix with old `reactflow` package in same project. |
| Tauri 2.0 | Node 18+, Rust 1.77.2+ | Stable since Oct 2024. Mobile support (iOS/Android) available but out of scope. |
| Vite 6.x | React 19, TypeScript 5 | Tauri scaffolding generates Vite 6. Vite 8 is available but introduces breaking changes; stay on Vite 6 until Tauri templates update. |
| Python dataclasses (stdlib) | Python 3.12 (existing) | No compatibility concern — stdlib. Frozen dataclasses require Python 3.10+. |

---

## Sources

- Tauri 2.0 official docs — https://v2.tauri.app/plugin/websocket/ — WebSocket plugin API, permissions model (HIGH confidence, docs updated Nov 2025)
- Tauri 2.0 stable release announcement — https://v2.tauri.app/blog/tauri-20/ — confirmed stable Oct 2024 (HIGH confidence)
- React Flow / xyflow official docs — https://reactflow.dev/whats-new/2025-03-27 — confirmed v12.5.0 shipped Mar 2025 (HIGH confidence)
- xyflow npm package — https://www.npmjs.com/package/@xyflow/react — current package name and version (HIGH confidence)
- Evennia Traits contrib docs — https://www.evennia.com/docs/latest/Contribs/Contrib-Traits.html — trait types, storage mechanism, limitations (HIGH confidence)
- Evennia webclient protocol — https://www.evennia.com/docs/latest/Components/Webclient.html + WebSearch — JSON `["inputfunc", [args], {kwargs}]` format (MEDIUM confidence — full OOB catalog needs code-level verification)
- Tauri vs Electron 2025 comparison — https://www.oflight.co.jp/en/columns/tauri-v2-vs-electron-comparison and https://codeology.co.nz/articles/tauri-vs-electron-2025-desktop-development.html — bundle size and memory figures (MEDIUM confidence — multiple sources agree on order of magnitude)
- Electron release timeline — https://releases.electronjs.org/ — current stable is Electron 41 (HIGH confidence)
- Zustand vs Redux 2025 — https://betterstack.com/community/guides/scaling-nodejs/zustand-vs-redux/ — consensus for solo/medium-complexity apps (MEDIUM confidence, multiple sources agree)

---

*Stack research for: Soravelon — guild/ability system, desktop MUD client, GUI zone builder*
*Researched: 2026-03-24*
