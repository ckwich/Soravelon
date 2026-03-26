# Soravelon

## What This Is

A dark-fantasy MUD built on Evennia 6.0, set in a world where ancient dragon-built magical infrastructure is failing. Players explore zones, fight mobs, build domain mastery across 10 disciplines, and develop character identity through 90 unique subclasses formed by domain combinations. The game is a passion project backed by an original novel trilogy — the world lore is deep and the design is pre-planned.

## Core Value

**Character identity must feel mechanically distinct** — a Duskblade (Combat + Subterfuge) plays fundamentally differently from a Thornguard (Combat + Naturalism). If the 90 subclasses collapse into sameness, the game's central promise fails.

## Requirements

### Validated

<!-- Shipped and confirmed working — inferred from existing codebase. -->

- ✓ World-state engine: 5 dimensions (reputation, network, bond, legacy, attunement), 10 domains, backend level 1-50 — existing
- ✓ Node system: 5 node types, Layer 0/1 room swapping, tick-driven state machine (healthy → stressed → failing → collapsed) — existing
- ✓ Mob affix system: rarity tiers (normal/magic/rare/legendary), weighted pools, forbidden combos, progressive reveal — existing
- ✓ Mob disposition: computed float (-1.0 to +1.0) from standing + ancestry + reputation + trust — existing
- ✓ Zone scaling: per-player logarithmic scaling, no zone floors/caps, mob HP rolled once at spawn — existing
- ✓ Banking: deposits, withdrawals, Consortium Drafts, recurring payments, underworld debt — existing
- ✓ Inventory engine: weight-based, graduated encumbrance, containers with weight reduction, keyring — existing
- ✓ Group system: session-only parties (max 6), 4 loot modes, leadership transfer, proximity queries — existing
- ✓ AreaBuilder: area spec .py → Evennia DB objects, idempotent, cross-zone exits, zone/mob registries — existing
- ✓ Base typeclasses: Character, Room, Exit (Standard/Hidden/Locked), Object/Item/Container/Equipment/Keyring, Mob, Script — existing
- ✓ Faction system: standing -100k to +100k, trust 0-100, betrayal flag, subfactions, atomic F() updates — existing
- ✓ Zone attunement: per-zone 0-100 tracking, aggregate dimension score — existing
- ✓ LLM quest data collection: WorldEventLog model, questline_choices on character — existing (stubs)
- ✓ Domain fingerprints: 10 mechanical verbs locked, guild/GTS engine, CharacterGuild model — Phase 4

### Active

<!-- Current scope: Milestone 0 completion + Milestone 1 playable skeleton. -->

**Milestone 0 — Foundation (remaining)**
- [ ] Caldenmere patrol mob — invulnerable walking city, custom CmdSet (climb leg/climb down), zone-wide entry echo
- [ ] Flight path system — Dragon Courier Service instant transit, Standing-based pricing
- [ ] Command prefix matching + alias system — context-sensitive, $1/$2/$* token expansion
- [ ] Proprietary client — Electron/Tauri desktop app (separate repo), basic map + dashboard, node events, Caldenmere icon
- [ ] GUI area builder — owner mode, then contributor mode; zone content authoring tool

**Milestone 1 — Playable Skeleton**
- [x] Guild/domain/subclass system — 10 domains × 9 secondaries = 90 subclasses with mechanical identity (Phase 4)
- [ ] Ability system — 360+ abilities across 90 subclasses, 4 tiers (Guild Tier Score 0/20/50/85)
- [ ] Skill system — general proficiencies (0-100), profession tracks (Cooking, Smithing, Alchemy, Scholarly Research)
- [ ] 4 playable ancestries — Human, Kau'roran, Veth, Selvar with distinct mechanical traits
- [ ] Hub City 1: Vael's Crossing — western continent frontier town (authored via GUI builder)
- [ ] 4 starter zones — 3 with Layer 0, 1 with active node (Layer 1), authored via GUI builder
- [ ] Basic equipment — weapons/armor without procedural affixes
- [ ] Combat system — ability-driven, domain-scaled, group-aware
- [ ] NPC template system — world-state variable injection for dialogue/behavior

### Out of Scope

- Companion/mount/dragon system — Milestone 2 (requires domain mastery system first)
- Procedural equipment affixes — Milestone 4 (content push)
- LLM quest generation — post-Milestone 2 (data collection started, infrastructure deferred)
- Auction House / Wandering Exchange — future milestone (banking system ready)
- Zones beyond starter region — Milestone 4+ content push
- Hub Cities 2-5 — Milestones 4-5
- Mobile client — no plans
- Microtransactions beyond optional $5/month cosmetic tier — by design

## Context

- **Engine:** Evennia 6.0 (Django + Twisted), Python 3.12, SQLite dev / PostgreSQL prod
- **Architecture:** 3-layer (typeclasses → world engines → Django models), all game logic in `world/` modules
- **Codebase state:** 13 foundation systems built, guild/GTS engine complete, strict build order enforced
- **World lore:** Backed by original novel trilogy (Dragonsight / Dragonfall / Dragon War). The Dragon Curse is the central plot device — 1,000-year-old curse reduced dragons to animal intelligence, civilizations inherited infrastructure they can't maintain
- **Design docs:** 18 vault documents in Obsidian covering every major system
- **Ability design status:** Framework and tier structure documented (soravelon-guilds.md), but individual abilities for 90 subclasses need creative design from scratch during implementation
- **Content pipeline:** GUI area builder must be complete before zone content authoring begins
- **Client:** Separate repo, Electron or Tauri, communicates with Evennia via websocket

## Constraints

- **Tech stack**: Evennia 6.0 + Django ORM — cannot change, deeply embedded
- **Build order**: Strict dependency chain — systems must be built in documented sequence
- **No visible levels**: Backend level (1-50) is internal only — never exposed to players
- **Evennia patterns**: No `getattr(obj.db, 'attr', default)` — always `obj.db.attr or fallback`; SaverDict copy pattern for list mutations; F() expressions for balance updates
- **Solo developer**: Passion project — no team, no deadline, but production-grade discipline required
- **Client isolation**: Desktop client is a separate repo/project, not embedded in soravelon

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Per-player logarithmic scaling, no zone floors/caps | Every zone playable at any progression; no content gating by level | ✓ Good |
| 90 subclasses from domain pairs, not traditional classes | Emergent identity from 10 × 9 combinations; avoids class bloat | — Pending |
| GUI builder before content authoring | Non-developer zone authoring enables content push at scale | — Pending |
| Electron/Tauri desktop client, separate repo | Clean separation; client team (future) doesn't touch game server | — Pending |
| Full 90 subclasses in M1 scope | Core value is character identity — can't validate with stubs | — Pending |
| Abilities designed during implementation | Minimal docs exist; creative work happens alongside engine work | — Pending |
| WorldEventLog collecting data now | LLM system needs history; earlier collection = richer context at launch | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-26 after Phase 4 completion*
