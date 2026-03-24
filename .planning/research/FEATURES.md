# Feature Research

**Domain:** Deep-progression MUD — dark fantasy, 90-subclass ability system, desktop client, GUI area builder
**Researched:** 2026-03-24
**Confidence:** MEDIUM — MUD ecosystem well-documented through community sources; specific ability system design patterns informed by Achaea/Discworld/Aardwolf analysis; client features cross-verified with Mudlet official docs; GUI builder patterns from OLC tradition. Confidence limited by sparse 2025+ primary sources for MUD-specific desktop clients.

---

## Feature Landscape

### Table Stakes — Ability and Class System

Features MUD players with deep progression expect. Missing these causes "this feels half-built" reactions.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Distinct ability set per class/subclass | Core identity — a Duskblade that plays like a Thornguard fails the game's central promise | HIGH | 90 subclasses × 4 tiers = 360+ abilities; each must feel mechanically distinct, not reskinned |
| Ability tier gating by progression score | Standard in Achaea, Aardwolf, Discworld — players expect to earn access to powerful abilities | MEDIUM | Soravelon tiers at Guild Tier Score 0/20/50/85; engine must enforce this at learn/use time |
| Learn command (NPC or trainer) | Every MUD with a class system has this UX — you talk to a trainer, spend a resource, gain the ability | LOW | Trainer NPC grants abilities up to your current GTS tier; no NPC trainer = no acquisition path |
| Ability help/description text | Players must be able to read what an ability does before committing to it | LOW | `help <ability>` or `abilities <subclass>` command; must show cost, effect, cooldown |
| Active vs. passive ability distinction | Expected: some abilities you activate (commands), some are always-on bonuses | MEDIUM | Passive abilities modify combat math transparently; active abilities are player commands |
| Cooldowns and resource costs | Expected by any player who has touched an MMORPG or modern MUD — spam without cooldowns kills tactics | MEDIUM | Need at minimum: ability cooldown timer, resource (mana/stamina/energy) cost per use |
| Ability progression tracking | "Am I getting better?" — players need feedback on current tier and what unlocks next | LOW | Show current GTS, tier thresholds, locked vs. unlocked abilities |
| Class identity commands | Abilities that only your subclass has — players notice immediately if all classes feel the same | HIGH | Must have 2-3 signature mechanics per subclass that are not shared |
| Respec or subclass change path | Players make mistakes; zero respec = guaranteed churn | MEDIUM | Define cost (resource drain, lore reason) — but the path must exist |
| Ancestry mechanical traits | Race system without mechanics = cosmetic only; that's not enough | MEDIUM | 4 ancestries need stat modifiers + 1-2 passive traits + potentially 1 active racial ability |

### Table Stakes — Skill (Proficiency) System

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| General proficiency skills (0-100) | Players expect non-combat growth vectors — Discworld and Aardwolf both do this extensively | MEDIUM | Combat, Subterfuge, etc. should map to the existing 10 domains as proficiency tracks |
| Profession tracks with recipes/outputs | Crafting in MUDs is expected — Lusternia has 13 craft professions; at minimum 4 are needed | HIGH | Cooking, Smithing, Alchemy, Scholarly Research each need a recipe system and output items |
| Skill improvement via use | Learn-by-doing (TM mechanic) or spend-XP-at-trainer — one model must be chosen clearly | MEDIUM | Soravelon's domain XP system already accumulates on use — profession tracks should tap this |
| Skill prerequisites between professions | Players expect logical gates (Mining before Smithing) — MapleStory and Lusternia both do this | LOW | Scholarly Research might require a Literacy/Arcana floor; Alchemy might require Herbalism track |
| Skill check feedback | "You succeed" / "You fail and waste materials" — players need to know skill affected outcome | LOW | Tie profession check rolls to current skill percentage; show partial success at mid-range |

### Table Stakes — MUD Client (Desktop)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Persistent game connection via websocket | Basic requirement — app must maintain a live connection to Evennia's websocket protocol | MEDIUM | Evennia uses custom JSON-over-websocket (not GMCP on webclient); client must speak this |
| Scrollback buffer with search | Every MUD client since 1995 has this — missing it is a usability failure | LOW | Mudlet, MUSHclient, QMud all provide this; minimum viable scrollback = 5000 lines |
| Command input with history | Arrow-up to recall previous commands — muscle memory from every MUD ever | LOW | In-session history only is fine; optional: persist across sessions |
| Triggers and aliases | Power users expect client-side automation — triggers on text patterns, aliases for long commands | MEDIUM | Not strictly required at v1 but absence will frustrate veteran MUD players immediately |
| Color/ANSI rendering | ANSI color codes from Evennia must display correctly | LOW | Standard; any web-renderer handles this |
| Map panel | Players expect a map pane in modern MUD clients — Mudlet's mapper is the gold standard | HIGH | Requires server-side room coordinate system + GMCP/JSON room data push to client |
| Dashboard panel | Vital stats (HP, resources, domain scores) visible without typing | MEDIUM | Evennia custom OOB JSON messages push character state; client renders panels |
| Split input area | Type while scrollback is active — not having this is jarring | LOW | Standard UI pattern; any split-pane layout handles this |

### Table Stakes — GUI Area Builder

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Room creation and editing | Core OLC capability since 1993 — the minimum viable builder tool | MEDIUM | Create room, set name/description/room_type/zone, place in zone |
| Exit/connection management | Rooms without exits don't exist in a navigable world | MEDIUM | Draw connections between rooms with direction; bidirectional by default, optional one-way |
| Mob placement and configuration | Every OLC since Diku includes mob editing — expected as baseline | MEDIUM | Place mob template in room; configure patrol, disposition base, spawn count |
| Item/object placement | Tables, chests, loot containers, ambient objects | LOW | Place SoravelonObject or Container with configured attributes |
| Zone metadata editing | Zone name, continent, type, node seed | LOW | Fields matching AreaBuilder's ZoneSpec |
| Visual room graph | MapMaker (2000), Gizmo, AVAE all provide this — text-only OLC is a regression | HIGH | Canvas-based room graph; rooms as nodes, exits as edges; drag-and-drop layout |
| Preview/diff before commit | Changes should be reviewable before writing to DB or .py spec files | MEDIUM | Show pending changes; allow cancel or commit |
| Save to AreaBuilder .py spec | Soravelon uses declarative Python area specs — builder must output to this format or call the builder API | HIGH | Either write .py file (dev mode) or call AreaBuilder directly in a contributor mode |

### Differentiators — Ability System

Features that make the 90-subclass system stand out from generic MUD class design.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Domain combination identity (90 subclasses) | No other MUD derives identity from 10 × 9 combinatorial pairs — this is the core differentiator | HIGH | Engine must read (primary_domain, secondary_domain) and serve correct ability set |
| Tier-gated ability unlock with score requirement | Progression milestones feel earned — GTS 0/20/50/85 threshold feel dramatic | LOW | Already designed; implement score check at learn time |
| Cross-domain synergy abilities | Some abilities that only unlock when two specific domains combine — e.g., "Null Strike" only available to Duskblade (Combat+Subterfuge) at T3 | HIGH | Rare, high-value abilities exclusive to specific pairings; creates strong identity incentives |
| Signature subclass commands | Unique command names per subclass (not just `attack` but `shadowstep`, `thorn-bind`) | MEDIUM | Cosmetic + functional — makes each subclass feel authored, not templated |
| World-state-gated abilities | Abilities that improve or unlock based on reputation/attunement dimensions — not pure class gating | HIGH | Ties the 5 world-state dimensions into combat identity; Duskblades with high Network score gain different behavior |
| Ancestry × subclass synergy | Kau'roran Bladesingers have a different feel than Human Bladesingers — traits interact | MEDIUM | Ancestry passives should have documented interaction points with subclass abilities |

### Differentiators — Client

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Node event notifications | When a zone node shifts state (healthy → stressed), show a distinct visual alert in client | LOW | Server pushes node_state OOB message; client renders banner/icon in dashboard |
| Caldenmere zone icon / city markers | Proprietary lore flavor — custom map icons for major landmarks | LOW | Data-driven: server pushes landmark metadata; client renders custom SVG icon |
| Domain score dashboard | Show all 10 domain scores as a mini-bar chart — visible character identity without exposing backend level | MEDIUM | Server pushes domain_scores on login and change; client renders chart panel |
| World-state dimension display | 5 dimension scores (Reputation, Network, Bond, Legacy, Attunement) as persistent panel | LOW | Same OOB push mechanism as domain scores; renders as 5 labeled gauges |
| Ability panel with cooldown tracking | Visual cooldown timers on active abilities — common in graphical MMOs, rare in MUD clients | HIGH | Client must track cooldown start/duration from server messages; render countdown UI |

### Differentiators — Area Builder

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Node configuration in-builder | Set node type, tick interval, failure thresholds directly from GUI — no Python editing needed | MEDIUM | NodeSpec fields exposed as form inputs |
| Layer 0 / Layer 1 room pairing | Builder supports designating alternate "node active" room for a given room | MEDIUM | AreaBuilder already models this; GUI surfaces it as a toggle with separate description field |
| Mob template library | Browse existing mob templates, drag into room — don't retype every mob | MEDIUM | Reads from named_mob_registry or a separate MobTemplate model |
| Zone preview / playtest link | Button that launches the game at that zone's entrance for immediate testing | LOW | Deep-link into Evennia's webclient at a specific room dbref |
| Contributor access model | Owner mode (full edit) vs contributor mode (add rooms/mobs, propose changes) | HIGH | Separate permissions; owner approves contributor changes before they go live |

### Anti-Features

Features that seem like obvious additions but are actively harmful for this project.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Visible level numbers on character | Players conditioned by WoW/EQ to expect "Level 42" display | Soravelon's backend level is intentionally hidden — exposing it collapses the domain-identity system into a single number that dominates all decisions | Display domain scores + GTS tier as character identity; never show a single power number |
| Per-ability XP grind (learn-by-use for class abilities) | Feels natural in skill-based MUDs like Discworld | 360+ abilities cannot all have individual XP tracks without exploding the data model and grinding loop | Gate class abilities behind Guild Tier Score (GTS), which derives from domain progression — clean and consistent |
| Full PvP system at Milestone 1 | Players ask for PvP early; it signals community activity | PvP requires disposition, reputation, and faction systems to be deeply tuned before enabling or it becomes a griefing vector | Implement dueling (consensual arena PvP) only; full open PvP is Milestone 3+ |
| Crafting economy / auction house | Crafting without economy has no sink | Auction House is explicitly out-of-scope until banking system is proven; premature economy creates inflation | Let professions produce consumables used by player vs. environment only in M1 |
| Mobile client | Players on phones want to play | Soravelon's rich map/dashboard UI is fundamentally incompatible with mobile screen dimensions; Tauri 2.0 supports mobile but it's additive complexity | Desktop client first; mobile deferred indefinitely |
| Auto-combat scripting (triggers to fully automate combat) | MUD veterans expect trigger-based combat automation | Auto-farming destroys the scarcity of domain XP and zone scaling models; removes engagement from the zone-node event system | Provide triggers and aliases for QoL; explicitly do not build "bot-mode" and enforce it via rate-limiting |
| Hard zone level requirements / content gating | Standard MMORPG design pattern | Per-player logarithmic scaling is the design — hard level gates negate it | Display recommended "engagement level" text; never lock zone entry |
| Global leaderboards at launch | Drives competitive motivation | With small early population and unbalanced ability system, leaderboards punish early adopters and create toxic dynamics | Guild Tier Score milestones + personal progression history instead |

---

## Feature Dependencies

```
[Domain XP system] ──provides──> [Guild Tier Score]
    └──required by──> [Ability tier gating]
                          └──required by──> [Ability learn/unlock]
                                                └──required by──> [Subclass identity commands]

[Guild Tier Score]
    └──required by──> [Ancestry × subclass synergy display]

[Ability system]
    └──required by──> [Combat system]
                          └──required by──> [Combat proficiency skills]

[Profession tracks]
    └──requires──> [General proficiency skills (0-100)]
    └──requires──> [Recipe/output item system]
                       └──requires──> [Item typeclass] (already exists)

[Room coordinate system (server-side)]
    └──required by──> [Client map panel]

[OOB JSON push infrastructure (server-side)]
    └──required by──> [Client dashboard panel]
    └──required by──> [Node event notifications]
    └──required by──> [Domain score display]
    └──required by──> [Ability cooldown tracking]

[AreaBuilder .py spec format]
    └──required by──> [GUI area builder save/export]

[Mob template registry]
    └──required by──> [GUI mob placement library]

[Evennia websocket JSON protocol]
    └──required by──> [All client features]
```

### Dependency Notes

- **Domain XP system requires Guild Tier Score:** GTS is a derived aggregate of domain scores — the existing `calculate_backend_level()` pattern is the blueprint; GTS is a parallel derivation with different weights and a visible output.
- **Ability learn requires trainer NPC:** Without a delivery mechanism (NPC trainer or self-learn command), players have no acquisition path even if the ability data model is complete.
- **Map panel requires server-side coordinates:** Evennia rooms don't store x/y/z by default — the server must push room coordinates or AreaBuilder must store them. This is a non-trivial server-side addition before any client map work begins.
- **OOB push infrastructure is a prerequisite for the entire client dashboard:** Evennia supports custom OOB messages natively; these must be wired into character hooks (at_post_puppet, stat change) before client panels can display live data.
- **AreaBuilder spec format is a hard dependency for the GUI builder:** The builder tool must emit valid Python that the existing `build()` function can consume, OR it must call a programmatic AreaBuilder API directly. The Python-file approach is simpler; the API approach is more robust for live editing.

---

## MVP Definition

This is Milestone 1 scope — not a long-term product MVP. "Launch" here means playable skeleton for testing/iteration.

### Launch With (M1 Core)

- [ ] Guild/domain/subclass engine — `(primary_domain, secondary_domain)` → subclass record, GTS calculation, tier derivation
- [ ] Ability data model — ability records with tier, type (active/passive), resource cost, cooldown, description
- [ ] Tier-gated ability unlock — `learn <ability>` command with GTS tier check; trainer NPC delivery
- [ ] Active ability command dispatch — command class per active ability; passive abilities modify combat math hooks
- [ ] 90 subclass definitions — even skeleton definitions with placeholder ability lists (populate creatively during implementation)
- [ ] 4 ancestry definitions — stat modifiers + 1-2 passive traits per ancestry
- [ ] 4 general proficiency skill tracks — combat, stealth, nature, arcana as 0-100 tracked skills (use existing CharacterSkill model)
- [ ] Basic combat system — ability-driven, domain-scaled, group-aware; ties into existing zone_scaling.py math
- [ ] Server-side OOB push for stats — push HP, resources, domain scores, GTS on login and change; prerequisite for client
- [ ] Room coordinate storage in AreaBuilder — x/y grid position on each room spec; prerequisite for client map

### Add After Validation (M1.x)

- [ ] Profession tracks (Cooking, Smithing, Alchemy, Scholarly Research) — once base skill engine is confirmed solid
- [ ] Cross-domain synergy abilities — 2-3 per subclass added after base ability set is playtested
- [ ] Respec / subclass change path — once players have tested the system and feedback confirms pain points
- [ ] Client ability panel with cooldown timers — after core combat is tuned and cooldown durations are validated
- [ ] Contributor mode for GUI builder — after owner mode is stable and area authoring has begun

### Future Consideration (M2+)

- [ ] World-state-gated abilities (reputation/attunement modifiers on ability behavior) — requires large-scale play data first
- [ ] Ancestry × subclass deep synergies — requires M1 ability system fully playtested
- [ ] PvP (consensual arena) — M3; requires combat balance
- [ ] Crafting economy integration — post-banking proof

---

## Feature Prioritization Matrix

### Ability System

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| 90 subclass definitions + GTS engine | HIGH | HIGH | P1 |
| Ability tier gating + learn command | HIGH | MEDIUM | P1 |
| Active ability command dispatch | HIGH | HIGH | P1 |
| Passive ability combat math integration | HIGH | MEDIUM | P1 |
| Ancestry mechanical traits | HIGH | MEDIUM | P1 |
| 4 general proficiency skill tracks | MEDIUM | MEDIUM | P1 |
| Signature subclass commands (cosmetic identity) | HIGH | LOW | P1 |
| Profession tracks (Cooking, Smithing, etc.) | MEDIUM | HIGH | P2 |
| Cross-domain synergy abilities | HIGH | HIGH | P2 |
| Respec path | MEDIUM | MEDIUM | P2 |
| World-state-gated ability modifiers | HIGH | HIGH | P3 |

### Client

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Websocket connection + scrollback + input | HIGH | LOW | P1 |
| Dashboard panel (HP, resources, domain scores) | HIGH | MEDIUM | P1 |
| ANSI color + split input | HIGH | LOW | P1 |
| Map panel (requires room coordinates) | HIGH | HIGH | P1 |
| Node event notifications | MEDIUM | LOW | P2 |
| Domain score mini-bar chart | MEDIUM | LOW | P2 |
| Ability panel with cooldown timers | HIGH | HIGH | P2 |
| Triggers and aliases | MEDIUM | MEDIUM | P2 |
| Caldenmere custom map icon | LOW | LOW | P3 |

### GUI Area Builder

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Room creation + editing | HIGH | MEDIUM | P1 |
| Exit / connection management | HIGH | MEDIUM | P1 |
| Visual room graph (canvas) | HIGH | HIGH | P1 |
| Mob placement + configuration | HIGH | MEDIUM | P1 |
| Zone metadata editing | HIGH | LOW | P1 |
| Save to AreaBuilder .py spec | HIGH | HIGH | P1 |
| Preview / diff before commit | MEDIUM | MEDIUM | P2 |
| Node configuration in-builder | MEDIUM | MEDIUM | P2 |
| Layer 0/1 room pairing | MEDIUM | MEDIUM | P2 |
| Mob template library | MEDIUM | MEDIUM | P2 |
| Contributor access model | MEDIUM | HIGH | P3 |

---

## Competitor Feature Analysis

| Feature | Discworld MUD | Achaea (IRE) | Aardwolf | Soravelon Plan |
|---------|---------------|--------------|---------|----------------|
| Class / Guild structure | Single guild, specialisations at threshold | 20 classes, 3 skill trees per class, 100+ abilities | 7 classes + subclasses, 4 per class | 90 subclasses from 10×9 domain pairs |
| Ability count per class | Hundreds of skills in hierarchy | 100+ per class | ~50-100 per class | ~4 abilities per tier × 4 tiers = ~16 per subclass; 360+ total |
| Tier/gate structure | Primary vs. non-primary skill caps; level-based | XP-funded skill levels | Level-based with remort resets | GTS thresholds (0/20/50/85) |
| Skill advancement model | XP spend at trainer + TM learn-by-use | XP spend at trainer | XP + remort resets | Domain XP accumulation → GTS → tier unlock |
| Professions/crafting | 7 craft skill types | Crafting guilds (city-dependent) | Lusternia has 13 professions | 4 profession tracks (Cooking, Smithing, Alchemy, Research) |
| Client support | Mudlet-compatible GMCP | Nexus client + Mudlet packages | MUSHclient packages | Proprietary Electron/Tauri desktop client |
| Area building | Staff-only in-game tools | Staff-authored | Staff tools | GUI desktop builder (owner + contributor modes) |
| Race / ancestry | Race affects stat caps | Fixed race at creation, stat modifiers | 15 races, resistances + stat bonuses | 4 ancestries, mechanical traits + subclass synergy |
| Visible level | Yes (numeric) | Yes (numeric 1-99+) | Yes (numeric 1-201) | No — GTS tier label only, never a number |

---

## Sources

- [Mudlet Manual: Supported Protocols](https://wiki.mudlet.org/w/Manual:Supported_Protocols) — HIGH confidence; official Mudlet docs
- [Mudlet 4.18 Release Notes](https://www.mudlet.org/2024/07/4-18-new-release/comment-page-1/) — HIGH confidence; official release
- [Achaea Class System](https://www.achaea.com/front) — HIGH confidence; official IRE game page
- [Discworld MUD Skills](https://dwwiki.mooo.com/wiki/Skills) — HIGH confidence; official Discworld wiki
- [Discworld MUD Guilds](https://discworld.starturtle.net/lpc/playing/guilds.html) — HIGH confidence; official Discworld docs
- [Aardwolf Skills and Spells V3](https://www.aardwolf.com/v3/v3magic.html) — HIGH confidence; official Aardwolf page
- [Aardwolf 2024 Updates](https://www.aardwolf.com/blog/2024/10/27/multiple-race-changes-and-other-updates/) — HIGH confidence; official blog
- [Online Creation (OLC) overview](https://mud.fandom.com/wiki/Online_Creation) — MEDIUM confidence; community wiki
- [MUD Progression Design — MUD Coders Guild](https://mudcoders.com/off-the-cliff-ep5-progression-f16558338dbd/) — MEDIUM confidence; practitioner blog
- [Tauri 2.0 Release](https://v2.tauri.app/blog/tauri-20/) — HIGH confidence; official Tauri blog
- [Tauri WebSocket plugin](https://v2.tauri.app/plugin/websocket/) — HIGH confidence; official Tauri docs
- [Evennia Webclient Docs](https://www.evennia.com/docs/latest/Components/Webclient.html) — HIGH confidence; official Evennia docs
- [Evennia Protocols](https://www.evennia.com/docs/latest/Concepts/Protocols.html) — HIGH confidence; official Evennia docs
- [Lusternia crafting professions](https://www.lusternia.com/) — MEDIUM confidence; game website
- [MajorMUD Class Abilities](https://wiki.mud.fyi/en/majormud/classes/abilities) — MEDIUM confidence; community wiki

---
*Feature research for: Soravelon MUD — deep progression, ability system, desktop client, GUI area builder*
*Researched: 2026-03-24*
